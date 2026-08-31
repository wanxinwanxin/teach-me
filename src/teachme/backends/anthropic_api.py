"""LLM backend for the Anthropic API. Requires ANTHROPIC_API_KEY.

Install with: pip install teachme[anthropic]
"""

from __future__ import annotations

import base64
import mimetypes
from pathlib import Path


class AnthropicApiBackend:
    def __init__(self, model: str = "claude-sonnet-5", max_tokens: int = 16000):
        import anthropic

        self.client = anthropic.Anthropic()
        self.model = model
        self.max_tokens = max_tokens

    def complete(
        self,
        prompt: str,
        *,
        images: list[Path] | None = None,
        allow_web: bool = False,
        timeout_s: int = 1200,
    ) -> str:
        content: list[dict] = []
        for p in images or []:
            media_type = mimetypes.guess_type(p.name)[0] or "image/png"
            content.append(
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": media_type,
                        "data": base64.standard_b64encode(p.read_bytes()).decode(),
                    },
                }
            )
        content.append({"type": "text", "text": prompt})

        kwargs: dict = {}
        if allow_web:
            kwargs["tools"] = [
                {"type": "web_search_20250305", "name": "web_search", "max_uses": 8}
            ]
        message = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=[{"role": "user", "content": content}],
            timeout=timeout_s,
            **kwargs,
        )
        return "".join(
            block.text for block in message.content if block.type == "text"
        ).strip()
