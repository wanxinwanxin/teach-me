"""Core data contracts of the teachme pipeline.

Every stage reads and writes these types. A plug-in only has to
speak this contract. Keep this file small and stable.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path


@dataclass
class Beat:
    """One narration beat: a few sentences spoken over one visual action."""

    text: str
    # Seconds of synthesized speech. The TTS stage fills this in.
    duration: float | None = None


@dataclass
class SceneSpec:
    """One scene of the storyboard. The director writes these."""

    id: str
    title: str
    # The one idea this scene must land.
    goal: str
    narration: list[Beat]
    # Concrete description of what is on screen and what moves, beat by beat.
    visual_spec: str
    notes: str = ""

    @property
    def total_duration(self) -> float:
        return sum(b.duration or 0.0 for b in self.narration)


@dataclass
class Storyboard:
    topic: str
    title: str
    audience: str
    scenes: list[SceneSpec] = field(default_factory=list)

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)

    @staticmethod
    def from_json(text: str) -> "Storyboard":
        data = json.loads(text)
        scenes = []
        for s in data.get("scenes", []):
            beats = [
                Beat(text=b["text"], duration=b.get("duration"))
                for b in s["narration"]
            ]
            scenes.append(
                SceneSpec(
                    id=str(s["id"]),
                    title=s["title"],
                    goal=s.get("goal", ""),
                    narration=beats,
                    visual_spec=s["visual_spec"],
                    notes=s.get("notes", ""),
                )
            )
        return Storyboard(
            topic=data["topic"],
            title=data["title"],
            audience=data.get("audience", "technically curious viewers"),
            scenes=scenes,
        )

    def save(self, path: Path) -> None:
        path.write_text(self.to_json())


@dataclass
class CritiqueIssue:
    severity: str  # "high" | "medium" | "low"
    description: str
    fix: str


@dataclass
class Critique:
    verdict: str  # "pass" | "revise"
    issues: list[CritiqueIssue] = field(default_factory=list)

    @property
    def needs_revision(self) -> bool:
        if self.verdict == "revise":
            return True
        highs = sum(1 for i in self.issues if i.severity == "high")
        mediums = sum(1 for i in self.issues if i.severity == "medium")
        return highs > 0 or mediums >= 3

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)

    @staticmethod
    def from_json(text: str) -> "Critique":
        data = json.loads(text)
        issues = [
            CritiqueIssue(
                severity=i.get("severity", "medium"),
                description=i.get("description", ""),
                fix=i.get("fix", ""),
            )
            for i in data.get("issues", [])
        ]
        return Critique(verdict=data.get("verdict", "revise"), issues=issues)


class RenderError(RuntimeError):
    """The renderer failed. The message carries the tail of stderr."""
