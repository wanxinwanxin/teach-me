"""TTS through Microsoft Edge neural voices (edge-tts package).

Free, no API key, works on Linux servers. The default voice for hosted
teachme instances.
"""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

from .base import probe_duration


class EdgeTtsBackend:
    def __init__(self, voice: str = "en-US-AndrewNeural", rate: int = 0):
        self.voice = voice
        # rate is a percentage delta; 0 keeps the natural pace.
        self.rate = rate

    def synthesize(self, text: str, out_path: Path) -> float:
        import asyncio

        import edge_tts

        out_path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
            mp3 = Path(tmp.name)
        try:
            rate_str = f"{self.rate:+d}%"
            # The Edge endpoint fails transiently now and then; retry.
            for attempt in range(4):
                try:
                    communicate = edge_tts.Communicate(
                        text, self.voice, rate=rate_str
                    )
                    asyncio.run(communicate.save(str(mp3)))
                    break
                except Exception:
                    if attempt == 3:
                        raise
                    import time

                    time.sleep(2 * (attempt + 1))
            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-v",
                    "error",
                    "-i",
                    str(mp3),
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
            mp3.unlink(missing_ok=True)
        return probe_duration(out_path)
