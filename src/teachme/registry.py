"""Plug-in registry.

Built-in components register here by short name. Third-party components
plug in through a dotted path in the config, for example:
    backend: "my_package.backends:MyBackend"
"""

from __future__ import annotations

import importlib
from typing import Any

BACKENDS: dict[str, str] = {
    "claude_cli": "teachme.backends.claude_cli:ClaudeCliBackend",
    "anthropic_api": "teachme.backends.anthropic_api:AnthropicApiBackend",
}

RENDERERS: dict[str, str] = {
    "manim": "teachme.render.manim_renderer:ManimRenderer",
}

TTS_BACKENDS: dict[str, str] = {
    "macos_say": "teachme.audio.macos_say:MacosSayBackend",
    "openai_tts": "teachme.audio.openai_tts:OpenAiTtsBackend",
    "edge_tts": "teachme.audio.edge_tts:EdgeTtsBackend",
}


def load(table: dict[str, str], name: str, **kwargs: Any) -> Any:
    """Instantiate a component by short name or dotted path."""
    path = table.get(name, name)
    if ":" not in path:
        raise ValueError(
            f"Unknown component {name!r}. Use a registered name "
            f"({', '.join(table)}) or a 'module.path:ClassName' string."
        )
    module_name, class_name = path.split(":", 1)
    module = importlib.import_module(module_name)
    cls = getattr(module, class_name)
    return cls(**kwargs)
