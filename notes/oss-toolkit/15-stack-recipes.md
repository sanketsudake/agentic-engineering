# 15 Stack Recipes

> Copy one of these instead of assembling a stack from scratch. Upgrade a layer only when it actually breaks.

| Stack | Budget | Orchestration | Model Layer | Retrieval | Memory | Observability | Deployment |
|---|---|---|---|---|---|---|---|
| Learning stack | Zero rupees | Smolagents or Pydantic AI | Ollama with Qwen3 4B | Chroma | JSON file on disk | Print statements then Phoenix | Runs on your laptop |
| Student portfolio stack | Under 1,000 INR a month | LangGraph | Free API tier or Groq style hosted open weights | Qdrant free tier with BGE-M3 | Postgres with pgvector | Langfuse self hosted | Coolify on a small VPS |
| Startup MVP stack | 10,000 to 50,000 INR a month | LangGraph plus FastAPI | Hosted frontier model with a small model router | Qdrant with a reranker | Mem0 plus Postgres | Langfuse with OpenTelemetry | Docker on a managed host, Supabase for auth |
| Enterprise stack | Committed infrastructure | Microsoft Agent Framework or LangGraph Platform | Mixed, self hosted open weights plus API fallback | Milvus or Elasticsearch hybrid | Graphiti temporal graph | Langfuse or MLflow with OTel collector | Kubernetes with KServe and Temporal |
| Fully private stack | Hardware cost only | LangGraph or Agno | vLLM serving Qwen3 or gpt-oss on your own GPU | Qdrant self hosted | Postgres and Redis | Langfuse self hosted | Docker Compose behind your firewall |
| Voice agent stack | Usage based | Pipecat or LiveKit Agents | Small fast model for low latency turns | Qdrant for the knowledge base | Redis session state | Langfuse | Kubernetes near your users for latency |
| Coding agent stack | Usage based | Claude Agent SDK or OpenHands | Frontier model for planning, Qwen3-Coder locally for bulk edits | Repository map plus embeddings | File system as memory | Traces plus Semgrep on output | Runs in CI with sandboxed execution |
