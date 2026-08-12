"""A deterministic in-process fake model.

Labs inject this where a real provider client would go, so the reader's loop
is exercised for real while everything stays offline. The script is a fixed
sequence of responses; the model returns them in order, one per call.

This is deliberately NOT a replay of a recorded session: the reader's harness
must actually append tool results and loop, or the script runs out of turns
in the wrong place and the tests fail.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Protocol


@dataclass
class ToolCall:
    """One tool invocation the model asks for."""
    id: str
    name: str
    input: dict[str, Any]


@dataclass
class ModelResponse:
    """What a model call returns: final text, or tool calls, never both."""
    text: str | None = None
    tool_calls: list[ToolCall] = field(default_factory=list)

    @property
    def stop_reason(self) -> str:
        return "tool_use" if self.tool_calls else "end_turn"


class Model(Protocol):
    """The seam labs build against. A real client adapter fits it too."""

    def complete(self, messages: list[dict], tools: dict) -> ModelResponse: ...


class ScriptExhausted(AssertionError):
    """The harness called the model more times than the script allows."""


class ScriptedModel:
    """Returns scripted responses in order.

    Args:
        script: responses returned one per `complete()` call. An entry may
            also be a (check, response) tuple; `check(messages)` runs before
            the response is returned and should raise AssertionError with a
            readable message if the conversation is not in the expected state.
        cycle: when True, the last response repeats forever (models a model
            that never stops calling tools — the runaway-loop script).
    """

    def __init__(self, script: list[ModelResponse | tuple[Callable[[list[dict]], None], ModelResponse]],
                 cycle: bool = False):
        self._script = list(script)
        self._cycle = cycle
        self.calls: list[list[dict]] = []  # every messages list we were sent

    def complete(self, messages: list[dict], tools: dict) -> ModelResponse:
        self.calls.append([dict(m) for m in messages])
        i = len(self.calls) - 1
        if i >= len(self._script):
            if self._cycle and self._script:
                i = len(self._script) - 1
            else:
                raise ScriptExhausted(
                    f"model called {len(self.calls)} times but the script has "
                    f"{len(self._script)} responses — is your loop appending "
                    f"tool results and stopping on final text?")
        entry = self._script[i]
        if isinstance(entry, tuple):
            check, response = entry
            check(messages)
            return response
        return entry
