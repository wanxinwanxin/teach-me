"""TTS backend protocol."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol, runtime_checkable


@runtime_checkable
class TtsBackend(Protocol):
    def synthesize(self, text: str, out_path: Path) -> float:
        """Write a WAV file to out_path and return its duration in seconds."""
        ...


def probe_duration(path: Path) -> float:
    """Return media duration in seconds via ffprobe."""
    import subprocess

    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(result.stdout.strip())
