"""Tools shared by the good and buggy agents under test.

Deterministic and in-process: Lab 8 is about writing graders, not building
interesting tools. Three of them (`lookup_price`, `get_weather`,
`search_docs`) raise `ValueError` on an unknown key. `tasks.py` uses that
to plant the tool failure the eval must catch.
"""
from __future__ import annotations

import ast
import operator

_OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub,
    ast.Mult: operator.mul, ast.Div: operator.truediv,
    ast.USub: operator.neg,
}

CATALOG = {"widget": "$9.99", "gadget": "$14.99", "sensor": "$29.99"}
WEATHER = {"tokyo": "Rainy, 18C", "cairo": "Clear, 34C", "oslo": "Cloudy, 9C"}
DOCS = {
    "hours": "Support hours are 9am-5pm ET.",
    "refund policy": "Refunds within 30 days with receipt.",
    "warranty": "1 year limited warranty.",
}


def _eval_node(node: ast.expr) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval_node(node.left), _eval_node(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval_node(node.operand))
    raise ValueError(f"unsupported expression: {ast.dump(node)}")


def calculator(expr: str) -> str:
    """Evaluate an arithmetic expression like "6 * 7"."""
    tree = ast.parse(expr, mode="eval")
    return str(_eval_node(tree.body))


def word_count(text: str) -> str:
    """Count the words in `text`."""
    return str(len(text.split()))


def lookup_price(item: str) -> str:
    """Return the catalog price of `item`."""
    key = item.strip().lower()
    if key not in CATALOG:
        raise ValueError(f"no such item: {item}")
    return CATALOG[key]


def get_weather(city: str) -> str:
    """Return today's weather for `city`."""
    key = city.strip().lower()
    if key not in WEATHER:
        raise ValueError(f"no such city: {city}")
    return WEATHER[key]


def search_docs(query: str) -> str:
    """Return the doc snippet matching `query`."""
    key = query.strip().lower()
    if key not in DOCS:
        raise ValueError(f"no matching doc: {query}")
    return DOCS[key]


TOOLS = {
    "calculator": calculator,
    "word_count": word_count,
    "lookup_price": lookup_price,
    "get_weather": get_weather,
    "search_docs": search_docs,
}
