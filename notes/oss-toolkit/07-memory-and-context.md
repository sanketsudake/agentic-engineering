# 07 Memory and Context

> Context engineering is the core 2026 skill. Decide what enters the window at every step.

| Tool | Sub-Category | What It Does | Best Use Case | Language | License | Difficulty | Adoption | Link |
|---|---|---|---|---|---|---|---|---|
| Mem0 | Memory layer | Extracts, consolidates and retrieves facts across sessions with a hybrid vector and graph store | Personalised assistants that remember user preferences | Python, TS | Apache-2.0 | Beginner | Very High | https://github.com/mem0ai/mem0 |
| Graphiti | Temporal graph | Zep engine that builds a bi temporal knowledge graph so facts can be superseded, not overwritten | Memory where the timeline matters, like CRM or support history | Python | Apache-2.0 | Advanced | High | https://github.com/getzep/graphiti |
| Letta | Agent memory OS | Memory hierarchy with core, recall and archival tiers plus self editing memory blocks | Agents that must run for months without losing context | Python | Apache-2.0 | Intermediate | High | https://github.com/letta-ai/letta |
| Cognee | Memory engine | Builds a semantic graph plus vector index from your data in a few lines, ECL pipeline style | Replacing naive RAG with connected memory | Python | Apache-2.0 | Intermediate | High | https://github.com/topoteretes/cognee |
| Memobase | User profiles | Profile based long term memory that stores structured user attributes over time | Consumer apps where the user profile drives the experience | Python | Apache-2.0 | Beginner | Medium | https://github.com/memodb-io/memobase |
| Supermemory | Memory API | Universal memory layer with a router that trims context automatically | Adding memory to an existing app without a rewrite | TypeScript | MIT | Beginner | Medium | https://github.com/supermemoryai/supermemory |
| LangGraph checkpointers | State persistence | Saves full graph state to Postgres, SQLite or Redis so runs pause, resume and time travel | Human in the loop approvals and crash recovery | Python, JS | MIT | Intermediate | Very High | https://github.com/langchain-ai/langgraph |
| Redis | Working memory | In memory store used for session state, queues, rate limits and short term context | The hot path cache in front of every agent | C | RSAL and AGPL | Beginner | Very High | https://github.com/redis/redis |
| Postgres | Durable state | The boring reliable choice for conversation logs, checkpoints and vectors via pgvector | One database for state, audit trail and retrieval | C | PostgreSQL | Beginner | Very High | https://github.com/postgres/postgres |
| Prompt caching | Technique | Provider side reuse of a stable prompt prefix, cuts cost and latency on repeated system prompts | Any agent with a long fixed system prompt and tool list | Concept | N/A | Beginner | Very High | https://docs.claude.com/en/docs/build-with-claude/prompt-caching |
| Context compaction | Technique | Summarise or prune old turns when the window fills instead of truncating blindly | Long running chat and coding agents | Concept | N/A | Intermediate | Very High | https://github.com/langchain-ai/langgraph |
| File system as memory | Technique | Let the agent write notes, plans and scratchpads to disk and read them back on demand | Cheap unlimited memory for coding and research agents | Concept | N/A | Beginner | Very High | https://github.com/openclaw/openclaw |
