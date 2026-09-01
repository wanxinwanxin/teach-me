"""TTS through Kokoro-82M (open weights, Apache-2.0, runs locally on CPU).

The default voice of teachme: near-commercial narration quality with no
API key. Requires `pip install kokoro soundfile` and the espeak-ng
system package.
"""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

from .base import probe_duration

_pipeline = None


def _get_pipeline():
    global _pipeline
    if _pipeline is None:
        from kokoro import KPipeline

        # 'a' = American English
        _pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    return _pipeline


class KokoroBackend:
    def __init__(self, voice: str = "af_heart", rate: int = 0, speed: float = 1.0):
        self.voice = voice
        # `rate` exists for config compatibility; nonzero maps to speed.
        self.speed = speed if rate == 0 else max(0.5, min(2.0, rate / 180.0))

    def synthesize(self, text: str, out_path: Path) -> float:
        import numpy as np
        import soundfile as sf

        out_path.parent.mkdir(parents=True, exist_ok=True)
        pipeline = _get_pipeline()
        chunks = [
            audio
            for _, _, audio in pipeline(text, voice=self.voice, speed=self.speed)
        ]
        wave = np.concatenate(chunks) if len(chunks) > 1 else chunks[0]
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            raw = Path(tmp.name)
        try:
            sf.write(raw, wave, 24000)
            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-v",
                    "error",
                    "-i",
                    str(raw),
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
            raw.unlink(missing_ok=True)
        return probe_duration(out_path)
