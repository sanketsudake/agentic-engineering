# 10 Guardrails and Security

> Prompt injection has no complete fix. Limit what the agent is allowed to do instead.

| Tool | Sub-Category | What It Does | Best Use Case | Language | License | Difficulty | Adoption | Link |
|---|---|---|---|---|---|---|---|---|
| NeMo Guardrails | Guardrails | Programmable rails in Colang that constrain dialogue, topics and tool use | Enforcing conversation policy at runtime | Python | Apache-2.0 | Intermediate | Very High | https://github.com/NVIDIA/NeMo-Guardrails |
| Guardrails AI | Validation | Input and output validators from a community hub, with automatic re asking on failure | Structural and content validation around every call | Python | Apache-2.0 | Beginner | Very High | https://github.com/guardrails-ai/guardrails |
| LLM Guard | Security toolkit | Scanners for prompt injection, secrets, toxicity, PII and code in both directions | A first defensive layer in front of user input | Python | MIT | Beginner | High | https://github.com/protectai/llm-guard |
| Rebuff | Injection defence | Multi layer prompt injection detector with canary tokens and a learning database | Catching injections that reach your tools | Python | Apache-2.0 | Intermediate | Medium | https://github.com/protectai/rebuff |
| garak | Red teaming | Vulnerability scanner that probes a model with dozens of known attack families | Automated red team run before every release | Python | Apache-2.0 | Intermediate | High | https://github.com/NVIDIA/garak |
| PyRIT | Red teaming | Microsoft risk identification toolkit for automated multi turn attacks | Systematic adversarial testing at scale | Python | MIT | Advanced | High | https://github.com/Azure/PyRIT |
| Presidio | PII | Detects and anonymises personal data in text and images before it reaches a model | Data protection compliance in prompts and logs | Python | MIT | Beginner | Very High | https://github.com/microsoft/presidio |
| PurpleLlama and Llama Guard | Safety models | Meta safety classifiers for input and output plus the CyberSecEval benchmark | Cheap policy classification on your own hardware | Python | Custom | Intermediate | Very High | https://github.com/meta-llama/PurpleLlama |
| Granite Guardian | Safety models | IBM risk detection models covering harm, jailbreak and RAG groundedness | Detecting hallucination in grounded answers | Python | Apache-2.0 | Intermediate | Medium | https://github.com/ibm-granite/granite-guardian |
| ShieldGemma | Safety models | Google content safety classifiers in small sizes that run alongside your agent | Filtering at low latency and low cost | Model | Gemma terms | Beginner | Medium | https://huggingface.co/google/shieldgemma-2b |
| Open Policy Agent | Authorisation | General policy engine to decide which tools an agent may call in a given context | Fine grained permissions on agent actions | Go | Apache-2.0 | Advanced | Very High | https://github.com/open-policy-agent/opa |
| HashiCorp Vault | Secrets | Secret storage with dynamic short lived credentials for agent tool access | Never putting a long lived API key in an agent prompt | Go | BUSL-1.1 | Intermediate | Very High | https://github.com/hashicorp/vault |
| SPIRE | Identity | SPIFFE implementation that gives every workload a cryptographic identity | Machine identity for agent to service calls | Go | Apache-2.0 | Advanced | High | https://github.com/spiffe/spire |
| Semgrep | Code scanning | Static analysis to review code an agent wrote before it merges | Guarding the pull requests your coding agent opens | OCaml, Python | LGPL-2.1 | Beginner | Very High | https://github.com/semgrep/semgrep |
| Trivy | Supply chain | Scans containers, dependencies and IaC for vulnerabilities and leaked secrets | Securing the images your agents run in | Go | Apache-2.0 | Beginner | Very High | https://github.com/aquasecurity/trivy |
| OWASP Top 10 for LLM Apps | Framework | The reference risk list covering prompt injection, data leakage and excessive agency | The checklist to run your design review against | Guide | CC | Beginner | Very High | https://genai.owasp.org/llm-top-10/ |
| MITRE ATLAS | Framework | Adversarial tactics and techniques knowledge base for AI systems | Threat modelling an agent deployment | Guide | Public | Intermediate | High | https://atlas.mitre.org/ |
| NIST AI Risk Management Framework | Framework | Voluntary framework for governing AI risk across the lifecycle | Enterprise governance documentation | Guide | Public | Intermediate | High | https://www.nist.gov/itl/ai-risk-management-framework |
| EU AI Act | Regulation | Risk tiered legal obligations that apply to anyone serving EU users | Compliance planning if you have EU customers | Regulation | Public | Intermediate | High | https://artificialintelligenceact.eu/ |
| India DPDP Act | Regulation | Indian data protection law that governs consent, purpose limitation and cross border data flow | Any agent handling Indian user data | Regulation | Public | Intermediate | High | https://www.meity.gov.in/ |
