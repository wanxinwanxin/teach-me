"""LLM backend protocol.

A backend is anything that can complete a prompt. Plug in your own:
implement this protocol and register it in the registry, or point the
config at a "module.path:ClassName" dotted path.
"""

from __future__ import annotations

from pathlib import Path
from typing import Protocol, runtime_checkable


@runtime_checkable
class LLMBackend(Protocol):
    def complete(
        self,
        prompt: str,
        *,
        images: list[Path] | None = None,
        allow_web: bool = False,
        timeout_s: int = 1200,
    ) -> str:
        """Return the model's text answer.

        images: local image files the model must look at (for critique).
        allow_web: permit web research tools if the backend has them.
        """
        ...


def strip_code_fences(text: str, language: str | None = None) -> str:
    """Extract the content of the first fenced code block, if any.

    Falls back to the raw text when no fence is present.
    """
    lines = text.splitlines()
    starts = [
        i
        for i, ln in enumerate(lines)
        if ln.strip().startswith("```")
        and (language is None or ln.strip().lstrip("`").strip().startswith(language) or ln.strip() == "```")
    ]
    if not starts:
        return text.strip()
    start = starts[0]
    for j in range(start + 1, len(lines)):
        if lines[j].strip().startswith("```"):
            return "\n".join(lines[start + 1 : j]).strip()
    return "\n".join(lines[start + 1 :]).strip()


def extract_json(text: str) -> str:
    """Pull the first JSON object out of a model reply."""
    fenced = strip_code_fences(text, "json")
    candidate = fenced if fenced.lstrip().startswith("{") else text
    start = candidate.find("{")
    if start == -1:
        raise ValueError(f"No JSON object in model reply:\n{text[:500]}")
    depth = 0
    in_string = False
    escape = False
    for i in range(start, len(candidate)):
        ch = candidate[i]
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return candidate[start : i + 1]
    raise ValueError("Unbalanced JSON in model reply")
