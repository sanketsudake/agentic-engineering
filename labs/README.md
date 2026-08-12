# Labs

Hands-on labs, one standalone uv project each.
Every lab completes **offline with zero API keys**;
live-model runs are optional extras behind the `live` pytest marker.

Workflow:

```bash
cd labs/lab03-tool-loop
uv sync
uv run pytest                      # red tests are your task list
LAB_TARGET=solution uv run pytest  # see the reference solution pass
```

| Lab | Title | Level | Stack | Offline mechanism | Chapter |
|---|---|---|---|---|---|
| 01 | First model call + structured output | L1 | anthropic SDK | mockllm | Ch 2 *(planned)* |
| 02 | Define and dispatch tools | L1 | plain Python | ScriptedModel | Ch 4 |
| 03 | Build the tool loop | L1 | plain Python | ScriptedModel | Ch 1 |
| 04 | Context truncation & compaction | L2 | plain Python | ScriptedModel | Ch 3 *(planned)* |
| 05 | Debug a broken agent | L2 | plain Python | ScriptedModel | Ch 4 |
| 06 | Multi-agent handoffs | L2 | OpenAI Agents SDK | mockllm | Ch 9 *(planned)* |
| 07 | Stateful graph agent + checkpointing | L2 | LangGraph | fake chat model | Ch 5 |
| 08 | Write an eval | L2 | plain Python | ScriptedModel + transcripts | Ch 10 *(planned)* |
| 09 | Operate a coding agent | L2 | Claude Code | transcripts + config linting | Ch 8 *(planned)* |
| 10 | Tracing & failure taxonomy | L3 | plain Python | recorded transcripts | Ch 12 *(planned)* |
| 11 | Guardrails & tool-permission design | L3 | framework-agnostic | adversarial scripts | Ch 11 *(planned)* |
| 12 | Capstone: eval-gated release | L3 | your choice | composes labs 03 + 08 | Ch 14 *(planned)* |

`labs/common/` holds `worksheet_common`, the shared offline harness:
`ScriptedModel` (deterministic in-process fake model),
`mockllm` (a stdlib HTTP server with OpenAI- and Anthropic-shaped endpoints),
and transcript helpers.
