# 14 Deploy and Infra

> Most agents need no GPU at all. Only the model does.

| Tool | Sub-Category | What It Does | Best Use Case | Language | License | Difficulty | Adoption | Link |
|---|---|---|---|---|---|---|---|---|
| Docker | Containers | Package the agent and its dependencies into a reproducible image | The first step in every deployment path | Go | Apache-2.0 | Beginner | Very High | https://github.com/moby/moby |
| Kubernetes | Orchestration | Scheduling, scaling and self healing for agent services and GPU workloads | Multi service agent platforms at scale | Go | Apache-2.0 | Advanced | Very High | https://github.com/kubernetes/kubernetes |
| Helm | Packaging | Templated Kubernetes releases so a stack deploys with one command | Shipping your agent stack to another cluster | Go | Apache-2.0 | Intermediate | Very High | https://github.com/helm/helm |
| Ray | Distributed compute | Distributed Python for parallel agent runs, batch inference and training | Running thousands of agent tasks in parallel | Python, C++ | Apache-2.0 | Advanced | Very High | https://github.com/ray-project/ray |
| KubeRay | Operator | Runs Ray clusters natively on Kubernetes with autoscaling | GPU sharing across teams | Go | Apache-2.0 | Advanced | High | https://github.com/ray-project/kuberay |
| Temporal | Durable execution | Workflows that survive crashes, retries and week long waits with full history | Long running agents that must never lose state | Go, Java | MIT | Advanced | Very High | https://github.com/temporalio/temporal |
| Prefect | Orchestration | Python native flows with retries, caching and observability | Scheduled agent jobs and data pipelines | Python | Apache-2.0 | Intermediate | Very High | https://github.com/PrefectHQ/prefect |
| Dagster | Orchestration | Asset oriented orchestration with lineage and data quality checks | Keeping a knowledge base pipeline fresh and auditable | Python | Apache-2.0 | Intermediate | Very High | https://github.com/dagster-io/dagster |
| Apache Airflow | Orchestration | The most widely deployed DAG scheduler, now with LLM operator support | Enterprises that already run Airflow | Python | Apache-2.0 | Intermediate | Very High | https://github.com/apache/airflow |
| Celery | Task queue | Battle tested distributed task queue for background agent jobs | Simple async job processing | Python | BSD-3 | Beginner | Very High | https://github.com/celery/celery |
| NATS | Messaging | Lightweight messaging with JetStream persistence for agent to agent events | Event driven multi agent systems | Go | Apache-2.0 | Intermediate | High | https://github.com/nats-io/nats-server |
| Apache Kafka | Streaming | Durable event log that many teams use as the agent event backbone | High volume event driven architectures | Java, Scala | Apache-2.0 | Advanced | Very High | https://github.com/apache/kafka |
| OpenTofu | Infrastructure | Community fork of Terraform for declaring cloud infrastructure as code | Reproducible GPU and cluster provisioning | Go | MPL-2.0 | Intermediate | High | https://github.com/opentofu/opentofu |
| Prometheus | Metrics | Time series metrics and alerting, the default for infrastructure monitoring | Latency, error rate and token cost dashboards | Go | Apache-2.0 | Intermediate | Very High | https://github.com/prometheus/prometheus |
| Grafana | Dashboards | Visualisation layer over metrics, logs and traces | One pane of glass for an agent platform | TypeScript, Go | AGPL-3.0 | Beginner | Very High | https://github.com/grafana/grafana |
| OpenTelemetry Collector | Telemetry | Vendor neutral pipeline to receive, process and export traces and metrics | Routing agent traces anywhere without code changes | Go | Apache-2.0 | Intermediate | Very High | https://github.com/open-telemetry/opentelemetry-collector |
| Coolify | PaaS | Self hosted Heroku style platform that deploys from git to your own VPS | Cheap production hosting for side projects | PHP | Apache-2.0 | Beginner | Very High | https://github.com/coollabsio/coolify |
| Dokploy | PaaS | Lightweight self hosted deployment platform with Docker Compose support | One VPS running your whole agent stack | TypeScript | Apache-2.0 | Beginner | High | https://github.com/Dokploy/dokploy |
| Supabase | Backend | Postgres, auth, storage, edge functions and pgvector in one open source backend | Skipping backend work on an agent product | TypeScript | Apache-2.0 | Beginner | Very High | https://github.com/supabase/supabase |
| Keycloak | Identity | Open identity and access management with OAuth and OIDC | User auth and per user agent permissions | Java | Apache-2.0 | Intermediate | Very High | https://github.com/keycloak/keycloak |
| MinIO | Object storage | S3 compatible storage for documents, artefacts and model weights | Self hosted storage for agent outputs | Go | AGPL-3.0 | Intermediate | Very High | https://github.com/minio/minio |
| Kong | API gateway | Gateway with an AI plugin suite for routing, rate limiting and prompt guards | Putting a controlled edge in front of model traffic | Lua, Go | Apache-2.0 | Intermediate | Very High | https://github.com/Kong/kong |
