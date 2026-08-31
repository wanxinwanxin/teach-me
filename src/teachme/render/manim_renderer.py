"""Renders generated scene code with Manim Community Edition."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

from ..types import RenderError

QUALITY_DIRS = {"l": "480p15", "m": "720p30", "h": "1080p60", "k": "2160p60"}


class ManimRenderer:
    code_contract = """\
- Write a single Python file containing exactly one class named `TeachScene`
  that subclasses `manim.Scene`.
- Import everything you need from `manim` (`from manim import *` is fine).
- Import the beat clock with: `from teachme_manim import BeatClock`.
- In `construct`, first set `self.camera.background_color = "#0e1015"`, then
  create the clock: `clock = BeatClock(self, BEATS)` where `BEATS` is the
  list of beat durations given in the task.
- Drive ALL animation through `clock.play(...)` and `clock.wait(...)`, and
  ALWAYS pass an explicit `run_time=` to `clock.play`. Call
  `clock.end_beat(i)` after the visuals for beat i (0-indexed).
- The frame is 14.2 x 8 Manim units. Keep every mobject inside x in
  [-6.4, 6.4] and y in [-3.6, 3.6]. Nothing may touch the frame edge.
- Use `MathTex` for equations (LaTeX is available) and `Text` for words.
"""

    def __init__(self, quality: str = "m", fps: int = 30, python: str | None = None):
        self.quality = quality
        self.fps = fps
        self.python = python or sys.executable

    def render(self, scene_code: str, workdir: Path) -> Path:
        workdir.mkdir(parents=True, exist_ok=True)
        scene_file = workdir / "scene.py"
        scene_file.write_text(scene_code)
        helper_src = Path(__file__).parent.parent / "manim_lib" / "teachme_manim.py"
        shutil.copy(helper_src, workdir / "teachme_manim.py")

        cmd = [
            self.python,
            "-m",
            "manim",
            "render",
            f"-q{self.quality}",
            "--fps",
            str(self.fps),
            "--media_dir",
            str(workdir / "media"),
            str(scene_file),
            "TeachScene",
        ]
        result = subprocess.run(
            cmd, capture_output=True, text=True, cwd=workdir, timeout=1800
        )
        if result.returncode != 0:
            raise RenderError(
                (result.stderr or "")[-4000:] + "\n" + (result.stdout or "")[-2000:]
            )
        quality_dir = QUALITY_DIRS.get(self.quality, "720p30")
        out = workdir / "media" / "videos" / "scene" / quality_dir / "TeachScene.mp4"
        if not out.exists():
            candidates = list((workdir / "media").rglob("TeachScene.mp4"))
            if not candidates:
                raise RenderError("Manim reported success but produced no MP4.")
            out = candidates[0]
        return out
