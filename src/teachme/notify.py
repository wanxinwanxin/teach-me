"""Completion notification. Pluggable through config: macOS banner by
default, or any shell command (email, Slack webhook, and so on)."""

from __future__ import annotations

import shlex
import subprocess
from pathlib import Path

from .config import NotifyConfig


def notify(cfg: NotifyConfig, topic: str, video: Path) -> None:
    if cfg.method == "none":
        return
    if cfg.method == "command" and cfg.command:
        cmd = cfg.command.format(video=shlex.quote(str(video)), topic=shlex.quote(topic))
        subprocess.run(cmd, shell=True, check=False)
        return
    # Default: macOS notification banner.
    script = (
        f'display notification "Explainer ready: {topic}" '
        f'with title "teachme" sound name "Glass"'
    )
    subprocess.run(["osascript", "-e", script], check=False, capture_output=True)
