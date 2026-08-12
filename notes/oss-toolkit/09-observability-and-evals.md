# 09 Observability and Evals

> If you cannot see the trace, you cannot fix the agent. Wire this in on day one.

| Tool | Sub-Category | What It Does | Best Use Case | Language | License | Difficulty | Adoption | Link |
|---|---|---|---|---|---|---|---|---|
| Langfuse | Tracing | Open source LLM engineering platform with traces, prompt management, evals and cost tracking | The default self hosted observability layer | TypeScript | MIT core | Beginner | Very High | https://github.com/langfuse/langfuse |
| Arize Phoenix | Tracing | Notebook friendly tracing and evaluation built on OpenTelemetry conventions | Debugging retrieval and agent traces during development | Python | Elastic v2 | Beginner | Very High | https://github.com/Arize-ai/phoenix |
| OpenLLMetry | Instrumentation | OpenTelemetry extensions that trace LLM calls into any existing observability backend | Sending agent traces to Datadog, Grafana or Honeycomb | Python, TS | Apache-2.0 | Intermediate | High | https://github.com/traceloop/openllmetry |
| Opik | Tracing and evals | Comet platform for tracing, annotation queues, evaluation and production monitoring | Teams that want scoring and tracing in one tool | Python, TS | Apache-2.0 | Beginner | High | https://github.com/comet-ml/opik |
| Langtrace | Tracing | OpenTelemetry native tracing with framework specific spans and self hosting | Standards first tracing without vendor lock in | Python, TS | AGPL-3.0 | Intermediate | Medium | https://github.com/Scale3-Labs/langtrace |
| Helicone | Gateway and logs | Proxy that logs every request with caching, rate limits and cost analytics | One line integration for logging and spend control | TypeScript | Apache-2.0 | Beginner | High | https://github.com/Helicone/helicone |
| MLflow | Lifecycle | Experiment tracking, model registry and now GenAI tracing and evaluation | Organisations already standardised on MLflow | Python | Apache-2.0 | Intermediate | Very High | https://github.com/mlflow/mlflow |
| Weave | Tracing and evals | Weights and Biases toolkit for tracking agent traces and running scorers | W and B users extending into LLM apps | Python, TS | Apache-2.0 | Beginner | High | https://github.com/wandb/weave |
| DeepEval | Evaluation | Pytest style unit testing for LLM output with 40 plus metrics including agent specific ones | Putting evals into CI so regressions fail the build | Python | Apache-2.0 | Beginner | Very High | https://github.com/confident-ai/deepeval |
| Ragas | Evaluation | Reference free RAG metrics like faithfulness, context precision and answer relevancy | Proving your retrieval actually improved | Python | Apache-2.0 | Beginner | Very High | https://github.com/explodinggradients/ragas |
| Promptfoo | Evaluation | Declarative YAML test cases, side by side model comparison and red teaming | Comparing prompts and models before you commit | TypeScript | MIT | Beginner | Very High | https://github.com/promptfoo/promptfoo |
| Inspect AI | Evaluation | Rigorous evaluation framework from the UK AI Security Institute with solvers and scorers | Serious agent capability evaluations | Python | MIT | Advanced | High | https://github.com/UKGovernmentBEIS/inspect_ai |
| lm-evaluation-harness | Benchmarking | The standard harness behind most open model leaderboards, 60 plus academic benchmarks | Benchmarking a fine tuned model honestly | Python | MIT | Intermediate | Very High | https://github.com/EleutherAI/lm-evaluation-harness |
| SWE-bench | Benchmark | Real GitHub issues that an agent must resolve with a passing test suite | Measuring coding agent ability | Python | MIT | Advanced | Very High | https://github.com/SWE-bench/SWE-bench |
| Terminal-Bench | Benchmark | Terminal tasks that measure whether an agent can actually operate a shell | Evaluating command line agents | Python | Apache-2.0 | Advanced | High | https://github.com/laude-institute/terminal-bench |
| tau-bench | Benchmark | Simulates real users and domain policies to test tool agents in retail and airline settings | Testing policy compliance, not just task success | Python | MIT | Advanced | High | https://github.com/sierra-research/tau-bench |
| AgentBench | Benchmark | Multi environment benchmark spanning OS, database, web and game tasks | Comparing agent reasoning across domains | Python | Apache-2.0 | Advanced | Medium | https://github.com/THUDM/AgentBench |
| Evidently | Monitoring | Data and model monitoring with drift detection extended to LLM outputs | Watching quality drift after launch | Python | Apache-2.0 | Intermediate | High | https://github.com/evidentlyai/evidently |
| Giskard | Testing | Automatically scans LLM apps for hallucination, bias and prompt injection issues | A quick quality and safety report before launch | Python | Apache-2.0 | Intermediate | Medium | https://github.com/Giskard-AI/giskard |
| OpenTelemetry GenAI | Standard | Semantic conventions that define what an LLM and agent span should contain | Making traces portable between vendors | Spec | Apache-2.0 | Intermediate | High | https://github.com/open-telemetry/semantic-conventions |
