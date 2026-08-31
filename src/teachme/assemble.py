"""ffmpeg plumbing: frame sampling, audio concat, muxing, final concat."""

from __future__ import annotations

import subprocess
from pathlib import Path

from .audio.base import probe_duration


def _run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, capture_output=True, text=True)


def sample_frames(video: Path, out_dir: Path, count: int = 8) -> list[Path]:
    """Extract `count` uniformly spaced frames, named by timestamp."""
    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("t*.png"):
        old.unlink()
    duration = probe_duration(video)
    frames = []
    for i in range(count):
        t = duration * (i + 0.5) / count
        frame = out_dir / f"t{t:06.1f}s.png"
        _run(
            [
                "ffmpeg",
                "-y",
                "-v",
                "error",
                "-ss",
                f"{t:.2f}",
                "-i",
                str(video),
                "-frames:v",
                "1",
                str(frame),
            ]
        )
        frames.append(frame)
    return frames


def concat_wavs(wavs: list[Path], out_path: Path) -> float:
    listing = out_path.with_suffix(".txt")
    listing.write_text("".join(f"file '{w.resolve()}'\n" for w in wavs))
    _run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(listing),
            "-c",
            "copy",
            str(out_path),
        ]
    )
    listing.unlink()
    return probe_duration(out_path)


def mux(video: Path, audio: Path, out_path: Path) -> Path:
    """Combine silent video with narration. Freeze the last frame if the
    narration outlasts the video; pad silence if the video is longer."""
    vd = probe_duration(video)
    ad = probe_duration(audio)
    target = max(vd, ad) + 0.4
    _run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-i",
            str(video),
            "-i",
            str(audio),
            "-filter_complex",
            f"[0:v]tpad=stop_mode=clone:stop_duration={max(0.0, target - vd):.2f}[v];"
            f"[1:a]apad=whole_dur={target:.2f}[a]",
            "-map",
            "[v]",
            "-map",
            "[a]",
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "20",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "160k",
            "-t",
            f"{target:.2f}",
            str(out_path),
        ]
    )
    return out_path


def concat_videos(videos: list[Path], out_path: Path) -> Path:
    listing = out_path.with_suffix(".txt")
    listing.write_text("".join(f"file '{v.resolve()}'\n" for v in videos))
    _run(
        [
            "ffmpeg",
            "-y",
            "-v",
            "error",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(listing),
            "-c",
            "copy",
            str(out_path),
        ]
    )
    listing.unlink()
    return out_path
