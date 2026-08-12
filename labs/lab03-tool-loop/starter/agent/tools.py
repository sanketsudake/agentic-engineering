"""Lab 3 tools. Two work; `calculator` needs its TODO finished.

A tool here is a plain callable taking keyword arguments and returning a
string. The loop (your job, in loop.py) is what turns a model's ToolCall
into a call of one of these and feeds the string back as a tool result.
"""
from __future__ import annotations

import ast
import operator
from pathlib import Path

_OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub,
    ast.Mult: operator.mul, ast.Div: operator.truediv,
    ast.USub: operator.neg,
}


def read_file(path: str) -> str:
    """Return the text of a file under the current directory."""
    p = Path(path)
    if p.is_absolute() or ".." in p.parts:
        raise ValueError(f"path escapes the working directory: {path}")
    return p.read_text()


def _eval_node(node: ast.expr) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval_node(node.left), _eval_node(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval_node(node.operand))
    raise ValueError(f"unsupported expression: {ast.dump(node)}")


def calculator(expr: str) -> str:
    """Evaluate an arithmetic expression like "6 * 7".

    TODO(you): validate the argument before parsing. `expr` must be a
    non-empty string; anything else should raise ValueError with a message
    that names the problem (the model will read it and correct itself).
    """
    tree = ast.parse(expr, mode="eval")
    return str(_eval_node(tree.body))


TOOLS = {
    "read_file": read_file,
    "calculator": calculator,
}
