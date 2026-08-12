# 08 Tools MCP and Sandbox

> Learn MCP properly. It is on almost every AI engineering job description now.

| Tool | Sub-Category | What It Does | Best Use Case | Language | License | Difficulty | Adoption | Link |
|---|---|---|---|---|---|---|---|---|
| Model Context Protocol | Protocol | Open standard for connecting agents to tools, resources and prompts over a common wire format | The USB C port of agent tooling, learn this first | Spec | MIT | Beginner | Very High | https://github.com/modelcontextprotocol/modelcontextprotocol |
| MCP Servers | Reference servers | Official collection of reference servers for filesystem, git, fetch, memory and more | Copy paste starting points for your own server | Python, TS | MIT | Beginner | Very High | https://github.com/modelcontextprotocol/servers |
| MCP Python SDK | SDK | Official Python SDK for building MCP clients and servers | Wrapping an internal API as an agent tool | Python | MIT | Beginner | Very High | https://github.com/modelcontextprotocol/python-sdk |
| MCP TypeScript SDK | SDK | Official TypeScript SDK with stdio, HTTP and streamable transports | Node and edge deployed MCP servers | TypeScript | MIT | Beginner | Very High | https://github.com/modelcontextprotocol/typescript-sdk |
| FastMCP | SDK | Pythonic decorator based way to build MCP servers, plus proxying, auth and composition | Shipping a server in twenty lines instead of two hundred | Python | Apache-2.0 | Beginner | Very High | https://github.com/jlowin/fastmcp |
| MCP Inspector | Dev tool | Visual debugger to call your server tools by hand and inspect the message flow | Debugging a server before you wire an agent to it | TypeScript | MIT | Beginner | High | https://github.com/modelcontextprotocol/inspector |
| Playwright MCP | Server | Official Microsoft MCP server exposing browser control through the accessibility tree | Giving any MCP client reliable browsing | TypeScript | Apache-2.0 | Beginner | Very High | https://github.com/microsoft/playwright-mcp |
| Chrome DevTools MCP | Server | Lets an agent inspect network requests, performance traces and the live DOM | Debugging web apps with an agent | TypeScript | Apache-2.0 | Intermediate | High | https://github.com/ChromeDevTools/chrome-devtools-mcp |
| Composio | Tool platform | Managed auth and 250 plus app integrations exposed as agent tools | Skipping the OAuth work for Gmail, Slack, Jira and Notion | Python, TS | Elastic v2 | Beginner | High | https://github.com/ComposioHQ/composio |
| Arcade | Tool platform | Tool calling platform with per user authorisation so agents act as the user, not as a bot | Agents that must respect each user permissions | Python | MIT | Intermediate | Medium | https://github.com/ArcadeAI/arcade-ai |
| A2A Protocol | Protocol | Agent to agent protocol for discovery and task delegation between independent agents | Multi vendor agent ecosystems | Spec | Apache-2.0 | Intermediate | High | https://github.com/a2aproject/A2A |
| E2B | Sandbox | Cloud sandboxes that boot in about 150 milliseconds for running agent generated code | Executing untrusted code from an agent safely | Python, TS | Apache-2.0 | Beginner | Very High | https://github.com/e2b-dev/E2B |
| Firecracker | Sandbox | AWS microVM that gives hardware isolation with container like startup time | Building your own multi tenant execution platform | Rust | Apache-2.0 | Advanced | Very High | https://github.com/firecracker-microvm/firecracker |
| gVisor | Sandbox | User space kernel that intercepts syscalls for defence in depth around containers | Hardening container based tool execution | Go | Apache-2.0 | Advanced | High | https://github.com/google/gvisor |
| microsandbox | Sandbox | Self hosted microVM sandboxes with an MCP interface for agent code execution | Sandboxing on your own infrastructure | Rust | Apache-2.0 | Intermediate | Emerging | https://github.com/microsandbox/microsandbox |
| Daytona | Sandbox | Fast elastic development environments used as agent workspaces | Giving each agent run a clean disposable machine | Go, TS | AGPL-3.0 | Intermediate | Medium | https://github.com/daytonaio/daytona |
| Docker | Isolation | The baseline container runtime every agent deployment eventually needs | Reproducible tool environments and local sandboxes | Go | Apache-2.0 | Beginner | Very High | https://github.com/moby/moby |
| SearxNG | Search tool | Self hosted meta search engine you can hand to an agent as a free web search tool | Web search without per query API fees | Python | AGPL-3.0 | Intermediate | High | https://github.com/searxng/searxng |
| Open WebUI Tools | Tool registry | Community tool and function registry that plugs into the Open WebUI runtime | Adding tools to a self hosted chat UI | Python | BSD-3 | Beginner | High | https://github.com/open-webui/open-webui |
