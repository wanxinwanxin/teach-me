"""TTS through the OpenAI API. Requires OPENAI_API_KEY.

Install with: pip install teachme[openai]
"""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

from .base import probe_duration


class OpenAiTtsBackend:
    def __init__(self, voice: str = "onyx", rate: int = 0, model: str = "tts-1-hd"):
        from openai import OpenAI

        self.client = OpenAI()
        self.voice = voice
        self.model = model

    def synthesize(self, text: str, out_path: Path) -> float:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
            mp3 = Path(tmp.name)
        try:
            with self.client.audio.speech.with_streaming_response.create(
                model=self.model, voice=self.voice, input=text
            ) as response:
                response.stream_to_file(mp3)
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
