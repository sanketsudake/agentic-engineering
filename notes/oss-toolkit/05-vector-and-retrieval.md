# 05 Vector and Retrieval

> Your embedding model matters more than your vector database. Start with pgvector or Qdrant.

| Tool | Sub-Category | What It Does | Best Use Case | Language | License | Difficulty | Adoption | Link |
|---|---|---|---|---|---|---|---|---|
| Qdrant | Vector database | Rust vector engine with payload filtering, hybrid search, quantisation and multi tenancy | The pragmatic default for production agent memory | Rust | Apache-2.0 | Beginner | Very High | https://github.com/qdrant/qdrant |
| Milvus | Vector database | Distributed database built for billion scale vectors with GPU indexing | Very large corpora and separate storage and compute | Go, C++ | Apache-2.0 | Advanced | Very High | https://github.com/milvus-io/milvus |
| Weaviate | Vector database | Vector database with built in vectorisation modules and a GraphQL style query API | Teams that want the database to handle embedding too | Go | BSD-3 | Intermediate | Very High | https://github.com/weaviate/weaviate |
| Chroma | Vector database | Developer friendly embedded store that runs in process with almost no setup | Prototypes, notebooks and small local agents | Python, Rust | Apache-2.0 | Beginner | Very High | https://github.com/chroma-core/chroma |
| pgvector | Postgres extension | Adds vector types and HNSW indexes to Postgres you already run | Keeping vectors and business data in one transactional database | C | PostgreSQL | Beginner | Very High | https://github.com/pgvector/pgvector |
| LanceDB | Embedded database | Serverless columnar vector store on the Lance format with fast filtered search | Vectors on object storage without running a server | Rust | Apache-2.0 | Beginner | High | https://github.com/lancedb/lancedb |
| FAISS | Library | Meta similarity search library that most vector databases wrap internally | Custom retrieval research and in memory indexes | C++, Python | MIT | Intermediate | Very High | https://github.com/facebookresearch/faiss |
| Vespa | Search engine | Big serving engine that combines vector, lexical, structured filters and ranking models | Complex ranking pipelines at very large scale | Java, C++ | Apache-2.0 | Advanced | Medium | https://github.com/vespa-engine/vespa |
| OpenSearch | Search engine | Fork of Elasticsearch with a mature k nearest neighbour plugin and hybrid search | Adding vectors to existing log and search infrastructure | Java | Apache-2.0 | Intermediate | High | https://github.com/opensearch-project/OpenSearch |
| Elasticsearch | Search engine | Industry standard lexical search with dense vector and ELSER sparse retrieval | Enterprise search teams adding semantic ranking | Java | Elastic and SSPL | Intermediate | Very High | https://github.com/elastic/elasticsearch |
| Typesense | Search engine | Typo tolerant fast search with vector support and a very simple API | Instant search plus semantic fallback | C++ | GPL-3.0 | Beginner | Medium | https://github.com/typesense/typesense |
| txtai | Toolkit | All in one embeddings database with pipelines, graph and workflow support | One dependency semantic search for small projects | Python | Apache-2.0 | Beginner | Medium | https://github.com/neuml/txtai |
| sqlite-vec | Embedded | Vector search as a single SQLite extension that runs anywhere SQLite runs | Edge and mobile agents with local memory | C | Apache-2.0 | Beginner | Medium | https://github.com/asg017/sqlite-vec |
| USearch | Library | Compact single file similarity engine with bindings for a dozen languages | Embedding search inside a non Python service | C++ | Apache-2.0 | Intermediate | Medium | https://github.com/unum-cloud/usearch |
| RediSearch | In-memory | Vector similarity plus full text on Redis with millisecond latency | Session and short term agent memory | C | RSAL | Intermediate | High | https://github.com/RediSearch/RediSearch |
| Neo4j | Graph database | Property graph database with a vector index, the usual base for GraphRAG | Relationship heavy knowledge that flat chunks lose | Java | GPL-3.0 and commercial | Intermediate | High | https://github.com/neo4j/neo4j |
| FlagEmbedding | Models and rerank | BAAI toolkit for training and serving embedding and reranking models | Fine tuning a retriever on your own domain | Python | MIT | Advanced | High | https://github.com/FlagOpen/FlagEmbedding |
| FastEmbed | Library | Lightweight quantised ONNX embedding runtime with no torch dependency | Cutting container size and cold start time | Python | Apache-2.0 | Beginner | Medium | https://github.com/qdrant/fastembed |
| Infinity | Database | Purpose built AI database combining dense, sparse, tensor and full text search | Fusion retrieval in a single query | C++ | Apache-2.0 | Advanced | Emerging | https://github.com/infiniflow/infinity |
