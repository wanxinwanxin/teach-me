"""LLM backend that shells out to the Claude Code CLI (`claude -p`).

This is the zero-config default: if you can run Claude Code, you can
run teachme. No API key required. For image inputs, the CLI reads the
files itself through its Read tool.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path


class ClaudeCliBackend:
    def __init__(self, model: str = "sonnet", executable: str = "claude"):
        self.model = model
        self.executable = executable

    def complete(
        self,
        prompt: str,
        *,
        images: list[Path] | None = None,
        allow_web: bool = False,
        timeout_s: int = 1200,
    ) -> str:
        cmd = [self.executable, "-p", "--model", self.model]
        tools = []
        if images:
            tools.append("Read")
            listing = "\n".join(f"- {p.resolve()}" for p in images)
            prompt = (
                "First, use the Read tool to look at each of these image "
                f"files:\n{listing}\n\nThen do the task below.\n\n{prompt}"
            )
        if allow_web:
            tools.extend(["WebSearch", "WebFetch"])
        if tools:
            cmd.extend(["--allowedTools", ",".join(tools)])

        # Never inherit a parent Claude Code session's context.
        env = {
            k: v
            for k, v in os.environ.items()
            if k not in ("CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT")
        }
        result = subprocess.run(
            cmd,
            input=prompt,
            capture_output=True,
            text=True,
            timeout=timeout_s,
            env=env,
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"claude CLI failed (exit {result.returncode}):\n"
                f"{result.stderr[-2000:]}"
            )
        return result.stdout.strip()
