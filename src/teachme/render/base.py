"""Renderer protocol."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol, runtime_checkable


@runtime_checkable
class Renderer(Protocol):
    #: Text the animator prompt embeds so the code targets this renderer.
    code_contract: str

    def render(self, scene_code: str, workdir: Path) -> Path:
        """Render scene code to a silent MP4 and return its path.

        Raise types.RenderError with useful stderr on failure.
        """
        ...
