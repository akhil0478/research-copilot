import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  ListToolsRequestSchema,
  CallToolRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import fetch from "node-fetch";

const server = new Server(
  {
    name: "research-mcp",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// -----------------------------
// TOOL LIST
// -----------------------------
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "query_papers",
        description:
          "Search stored research papers. Always use this first.",
        inputSchema: {
          type: "object",
          properties: {
            query: { type: "string" },
          },
          required: ["query"],
        },
      },
      {
        name: "fetch_papers",
        description:
          "Fetch new research papers from arXiv ONLY if needed.",
        inputSchema: {
          type: "object",
          properties: {
            topic: { type: "string" },
          },
          required: ["topic"],
        },
      },
    ],
  };
});

// -----------------------------
// TOOL EXECUTION
// -----------------------------
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  // QUERY TOOL
  if (name === "query_papers") {
    const response = await fetch(
      `http://localhost:8000/query?q=${encodeURIComponent(args.query)}`
    );

    const data = await response.json();

    return {
      content: [
        {
          type: "text",
          text: `
You are given raw research paper excerpts.

Query:
${args.query}

Papers:
${data.papers.map(p => `
TITLE: ${p.title}
CONTENT: ${p.text.substring(0, 500)}
`).join("\n\n")}

Instructions:
- Identify distinct papers
- Summarize each
- Compare methods
- Identify research gaps
- Do NOT assume system errors
`,
        },
      ],
    };
  }

  // FETCH TOOL
  if (name === "fetch_papers") {
    const response = await fetch(
      "http://localhost:5678/webhook/fetch-papers",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ topic: args.topic }),
      }
    );

    const data = await response.json();

    return {
      content: [
        {
          type: "text",
          text: `
New papers are being fetched and stored.

Status:
${JSON.stringify(data)}

You should now call query_papers again.
`,
        },
      ],
    };
  }

  return {
    content: [{ type: "text", text: "Unknown tool" }],
  };
});

// -----------------------------
// START SERVER
// -----------------------------
const transport = new StdioServerTransport();
await server.connect(transport);
