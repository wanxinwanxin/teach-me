"""TTS through the macOS `say` command. Free, offline, always present on a Mac."""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

from .base import probe_duration


class MacosSayBackend:
    def __init__(self, voice: str = "Samantha", rate: int = 180):
        self.voice = voice
        self.rate = rate

    def synthesize(self, text: str, out_path: Path) -> float:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(suffix=".aiff", delete=False) as tmp:
            aiff = Path(tmp.name)
        try:
            subprocess.run(
                ["say", "-v", self.voice, "-r", str(self.rate), "-o", str(aiff), text],
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-v",
                    "error",
                    "-i",
                    str(aiff),
                    "-ar",
                    "44100",
                    "-ac",
                    "1",
                    str(out_path),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
        finally:
            aiff.unlink(missing_ok=True)
        return probe_duration(out_path)
