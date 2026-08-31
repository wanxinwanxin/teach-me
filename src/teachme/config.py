"""Instance configuration: which component fills each slot of the pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class RoleConfig:
    backend: str = "claude_cli"
    model: str = "sonnet"
    # Only for API backends. Prefer environment variables; this field exists
    # so a host application can inject a per-run key programmatically.
    api_key: str | None = None


@dataclass
class RendererConfig:
    name: str = "manim"
    quality: str = "m"  # manim quality flag: l, m, h, k
    fps: int = 30


@dataclass
class TtsConfig:
    backend: str = "macos_say"
    voice: str = "Samantha"
    rate: int = 180  # words per minute (macos_say only)


@dataclass
class Limits:
    max_scenes: int = 6
    max_critique_iters: int = 2
    max_render_fixes: int = 3
    llm_timeout_s: int = 1800
    source_char_budget: int = 80000


@dataclass
class NotifyConfig:
    method: str = "macos"  # "macos" | "command" | "none"
    command: str = ""  # shell command; {video} and {topic} get substituted


@dataclass
class TeachmeConfig:
    roles: dict[str, RoleConfig] = field(default_factory=dict)
    renderer: RendererConfig = field(default_factory=RendererConfig)
    tts: TtsConfig = field(default_factory=TtsConfig)
    limits: Limits = field(default_factory=Limits)
    notify: NotifyConfig = field(default_factory=NotifyConfig)

    ROLE_NAMES = ("researcher", "director", "animator", "critic")

    def __post_init__(self) -> None:
        for name in self.ROLE_NAMES:
            self.roles.setdefault(name, RoleConfig())

    @staticmethod
    def load(path: Path | None) -> "TeachmeConfig":
        if path is None:
            return TeachmeConfig()
        data = yaml.safe_load(Path(path).read_text()) or {}
        roles = {
            name: RoleConfig(**spec) for name, spec in (data.get("roles") or {}).items()
        }
        return TeachmeConfig(
            roles=roles,
            renderer=RendererConfig(**(data.get("renderer") or {})),
            tts=TtsConfig(**(data.get("tts") or {})),
            limits=Limits(**(data.get("limits") or {})),
            notify=NotifyConfig(**(data.get("notify") or {})),
        )
