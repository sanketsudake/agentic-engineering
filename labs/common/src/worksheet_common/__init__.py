"""Shared offline harness for the labs.

- scripted_model: a deterministic in-process fake model (no network, no keys).
- mockllm: a stdlib HTTP server with OpenAI- and Anthropic-shaped endpoints.
- transcripts: load/assert helpers for recorded session transcripts.
"""
from .scripted_model import Model, ModelResponse, ScriptedModel, ToolCall

__all__ = ["Model", "ModelResponse", "ScriptedModel", "ToolCall"]
