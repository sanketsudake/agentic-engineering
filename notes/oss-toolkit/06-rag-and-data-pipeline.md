# 06 RAG and Data Pipeline

> Most RAG failures are parsing and chunking failures, not model failures.

| Tool | Sub-Category | What It Does | Best Use Case | Language | License | Difficulty | Adoption | Link |
|---|---|---|---|---|---|---|---|---|
| LlamaIndex | Framework | Ingestion, indexing, retrieval and query engines with 300 plus data connectors | The reference toolkit for document heavy agents | Python, TS | MIT | Beginner | Very High | https://github.com/run-llama/llama_index |
| RAGFlow | Platform | Deep document understanding engine with visual chunk inspection and citation grounding | Messy PDFs, scans and tables where naive chunking fails | Python | Apache-2.0 | Intermediate | Very High | https://github.com/infiniflow/ragflow |
| Docling | Parsing | IBM parser that converts PDF, DOCX, PPTX and HTML into structured document objects | Layout aware parsing that keeps tables and reading order intact | Python | MIT | Beginner | Very High | https://github.com/docling-project/docling |
| Unstructured | Parsing | Preprocessing library that turns 25 plus file types into clean chunks for retrieval | One parser for a mixed enterprise document dump | Python | Apache-2.0 | Beginner | Very High | https://github.com/Unstructured-IO/unstructured |
| MarkItDown | Parsing | Lightweight Microsoft converter from Office files, PDFs and audio into Markdown for LLMs | Cheap fast conversion when layout fidelity is not critical | Python | MIT | Beginner | High | https://github.com/microsoft/markitdown |
| Marker | Parsing | Converts PDF and images to Markdown or JSON with high accuracy on equations and tables | Academic papers, textbooks and financial reports | Python | GPL-3.0 | Intermediate | High | https://github.com/datalab-to/marker |
| Surya | OCR | Multilingual OCR, layout analysis and reading order detection across 90 plus languages | Scanned Indian language documents and forms | Python | GPL-3.0 | Intermediate | High | https://github.com/datalab-to/surya |
| PaddleOCR | OCR | Mature production OCR with strong table, formula and handwriting recognition | High volume OCR pipelines | Python | Apache-2.0 | Intermediate | Very High | https://github.com/PaddlePaddle/PaddleOCR |
| Firecrawl | Web ingestion | Turns any website into clean LLM ready Markdown with crawl, scrape and search modes | Building a knowledge base from public web pages | TypeScript | AGPL-3.0 | Beginner | Very High | https://github.com/firecrawl/firecrawl |
| Crawl4AI | Web ingestion | Async crawler built for LLM pipelines with adaptive extraction strategies | Free self hosted alternative to paid scraping APIs | Python | Apache-2.0 | Beginner | Very High | https://github.com/unclecode/crawl4ai |
| Scrapy | Web ingestion | Battle tested crawling framework for large structured scrapes | Scheduled crawls of thousands of pages | Python | BSD-3 | Intermediate | Very High | https://github.com/scrapy/scrapy |
| Chonkie | Chunking | Focused chunking library with token, semantic, recursive and late chunking strategies | Getting chunking right instead of splitting on 1000 characters | Python | MIT | Beginner | High | https://github.com/chonkie-inc/chonkie |
| GraphRAG | Graph RAG | Microsoft pipeline that builds an entity graph and community summaries for global questions | Questions that need the whole corpus, not the top five chunks | Python | MIT | Advanced | Very High | https://github.com/microsoft/graphrag |
| LightRAG | Graph RAG | Cheaper faster graph plus vector retrieval with incremental index updates | GraphRAG quality without the full indexing bill | Python | MIT | Intermediate | High | https://github.com/HKUDS/LightRAG |
| R2R | Platform | Production RAG engine with ingestion, graphs, auth and an API out of the box | Skipping three months of RAG plumbing | Python | MIT | Intermediate | High | https://github.com/SciPhi-AI/R2R |
| Verba | Application | Weaviate reference RAG application you can fork and rebrand | Learning a full RAG stack end to end | Python | BSD-3 | Beginner | Medium | https://github.com/weaviate/Verba |
| Cognita | Platform | Modular RAG framework built for teams to move from notebook to production | Organised RAG codebases with swappable components | Python | Apache-2.0 | Intermediate | Medium | https://github.com/truefoundry/cognita |
| ColPali | Visual retrieval | Retrieves document pages directly from images using vision language embeddings, skipping OCR | Slide decks, charts and layout heavy PDFs | Python | MIT | Advanced | High | https://github.com/illuin-tech/colpali |
| Instructor | Structured output | Pydantic based structured extraction with automatic retries on validation failure | Reliable JSON from any model | Python | MIT | Beginner | Very High | https://github.com/567-labs/instructor |
| Outlines | Structured output | Constrained decoding that guarantees output matches a regex, JSON schema or grammar | Tool calls that can never be malformed | Python | Apache-2.0 | Intermediate | High | https://github.com/dottxt-ai/outlines |
| Semantic Router | Routing | Fast embedding based decision layer that routes queries before an LLM call | Cutting latency and cost with a cheap first hop | Python | MIT | Intermediate | Medium | https://github.com/aurelio-labs/semantic-router |
| Airbyte | Data ingestion | 600 plus connectors to move data from SaaS and databases into your vector store | Keeping the knowledge base in sync with source systems | Java, Python | Elastic v2 | Intermediate | Very High | https://github.com/airbytehq/airbyte |
