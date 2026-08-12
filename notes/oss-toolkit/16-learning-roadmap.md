# 16 Learning Roadmap

> Twelve weeks from zero to shipped. Two hours a day is enough if you build every week.

| Week | Focus | What To Learn | What To Build | Tools To Use | Proof Of Work |
|---|---|---|---|---|---|
| Week 1 | LLM fundamentals | Tokens, context windows, temperature, system prompts, function calling schemas, cost per million tokens | A CLI script that answers questions and calls one Python function you wrote | Ollama, LiteLLM, any free API tier | A GitHub repo with a README explaining what a tool call actually is |
| Week 2 | The agent loop by hand | Think, act, observe. Write the while loop yourself, no framework. Parse tool calls, handle errors, cap iterations | A 150 line agent that uses three tools: web search, calculator, file writer | Python, SearxNG, requests | A blog post breaking down your own loop line by line |
| Week 3 | Frameworks | Compare LangGraph, CrewAI and Pydantic AI on the same task. Learn state, nodes, edges and handoffs | The same agent from week 2 rebuilt three times, with a comparison table | LangGraph, CrewAI, Pydantic AI | A comparison post on latency, tokens and lines of code |
| Week 4 | Tools and MCP | MCP architecture, transports, tools versus resources versus prompts, and writing your own server | An MCP server that exposes your college or company data as agent tools | FastMCP, MCP Inspector | A published MCP server other people can install |
| Week 5 | Retrieval | Chunking strategies, embeddings, hybrid search, reranking and why naive RAG fails on real documents | A RAG agent over 200 PDFs with citations that link back to the page | Docling, Qdrant, BGE-M3, LlamaIndex | A demo where every answer shows its source |
| Week 6 | Memory | Short term versus long term memory, summarisation, fact extraction and knowledge graphs | Add persistent memory so the agent remembers users across sessions | Mem0, Postgres, LangGraph checkpointers | A video showing the agent recalling something from last week |
| Week 7 | Evaluation | Building a golden dataset, LLM as judge, faithfulness metrics and regression testing in CI | An eval suite with 50 test cases that runs on every commit | Ragas, DeepEval, GitHub Actions | A passing CI badge on your agent repo |
| Week 8 | Observability | Traces, spans, token accounting, latency breakdown and finding the slow step | Self hosted Langfuse wired into your agent with a cost dashboard | Langfuse, OpenTelemetry | Screenshots of a real trace with cost per run |
| Week 9 | Guardrails and security | Prompt injection, excessive agency, PII leakage, sandboxing and the OWASP LLM Top 10 | Add input scanning, output validation and a sandboxed code tool | LLM Guard, Guardrails AI, E2B | A red team report where you attack your own agent |
| Week 10 | Self hosting models | Quantisation, VRAM maths, throughput versus latency, batching and OpenAI compatible serving | Serve a 7B to 14B model on a rented GPU and point your agent at it | vLLM, Qwen3, SkyPilot | A benchmark post on tokens per second and cost per million tokens |
| Week 11 | Deployment | Containers, queues, retries, timeouts, streaming responses and durable execution | Deploy the agent with a web UI, background workers and monitoring | Docker, Coolify, Redis, Chainlit | A live public URL anyone can try |
| Week 12 | Ship and specialise | Pick one vertical, do the domain research and go deep instead of building another chatbot | A finished product with real users, a landing page and a demo video | Your chosen stack | A launch post with usage numbers |
