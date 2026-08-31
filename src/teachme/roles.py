"""The four agent roles. Each role = a prompt template + an LLM backend."""

from __future__ import annotations

import json
from pathlib import Path

from .backends.base import LLMBackend, extract_json, strip_code_fences
from .types import Critique, SceneSpec, Storyboard

PROMPTS_DIR = Path(__file__).parent / "prompts"


def _load_prompt(name: str) -> str:
    return (PROMPTS_DIR / f"{name}.md").read_text()


def _style_guide() -> str:
    return _load_prompt("style_guide")


def _beats_block(scene: SceneSpec) -> str:
    return "\n".join(
        f"{i}: {b.duration:.1f}s -> {b.text}" for i, b in enumerate(scene.narration)
    )


class Researcher:
    def __init__(self, backend: LLMBackend, timeout_s: int = 1800):
        self.backend = backend
        self.timeout_s = timeout_s

    def run(
        self,
        topic: str,
        sources: dict[str, str],
        clarification: str = "",
        allow_web: bool = True,
    ) -> str:
        if sources:
            parts = ["SOURCE MATERIAL (authoritative, prefer over memory):"]
            for name, text in sources.items():
                parts.append(f"\n--- SOURCE: {name} ---\n{text}")
            sources_block = "\n".join(parts)
        else:
            sources_block = (
                "No source files were provided. Research the topic yourself."
            )
        prompt = _load_prompt("researcher").format(
            topic=topic,
            clarification=(
                f"SCOPE CLARIFICATION FROM THE USER: {clarification}"
                if clarification
                else ""
            ),
            sources_block=sources_block,
        )
        return self.backend.complete(
            prompt, allow_web=allow_web, timeout_s=self.timeout_s
        )


class Director:
    def __init__(self, backend: LLMBackend, timeout_s: int = 1800):
        self.backend = backend
        self.timeout_s = timeout_s

    def run(self, topic: str, brief: str, max_scenes: int) -> Storyboard:
        prompt = _load_prompt("director").format(
            topic=topic,
            brief=brief,
            style_guide=_style_guide(),
            max_scenes=max_scenes,
        )
        reply = self.backend.complete(prompt, timeout_s=self.timeout_s)
        try:
            board = Storyboard.from_json(extract_json(reply))
        except (ValueError, KeyError, json.JSONDecodeError) as err:
            repair = self.backend.complete(
                "The JSON below is malformed or does not match the required "
                f"storyboard schema ({err}). Output ONLY the corrected JSON, "
                f"changing nothing else:\n\n{reply}",
                timeout_s=self.timeout_s,
            )
            board = Storyboard.from_json(extract_json(repair))
        board.scenes = board.scenes[:max_scenes]
        return board


class Animator:
    def __init__(self, backend: LLMBackend, code_contract: str, timeout_s: int = 1800):
        self.backend = backend
        self.code_contract = code_contract
        self.timeout_s = timeout_s

    def _base_prompt(self, video_title: str, scene: SceneSpec) -> str:
        beats_list = [round(b.duration or 5.0, 2) for b in scene.narration]
        return _load_prompt("animator").format(
            video_title=video_title,
            scene_id=scene.id,
            scene_title=scene.title,
            goal=scene.goal,
            beats_block=_beats_block(scene),
            visual_spec=scene.visual_spec,
            notes=scene.notes or "(none)",
            style_guide=_style_guide(),
            code_contract=self.code_contract,
            beats_list=beats_list,
        )

    def write(self, video_title: str, scene: SceneSpec) -> str:
        reply = self.backend.complete(
            self._base_prompt(video_title, scene), timeout_s=self.timeout_s
        )
        return strip_code_fences(reply, "python")

    def fix(self, video_title: str, scene: SceneSpec, code: str, stderr: str) -> str:
        prompt = (
            self._base_prompt(video_title, scene)
            + "\n\nYour previous code FAILED to render. The code:\n```python\n"
            + code
            + "\n```\n\nThe error output:\n```\n"
            + stderr[-3000:]
            + "\n```\n\nFix the error. Output ONLY the full corrected Python "
            "code in one ```python block."
        )
        reply = self.backend.complete(prompt, timeout_s=self.timeout_s)
        return strip_code_fences(reply, "python")

    def revise(
        self, video_title: str, scene: SceneSpec, code: str, critique: Critique
    ) -> str:
        issues = "\n".join(
            f"- [{i.severity}] {i.description}\n  Fix: {i.fix}"
            for i in critique.issues
        )
        prompt = (
            self._base_prompt(video_title, scene)
            + "\n\nYour previous code rendered, and a critic reviewed the "
            "frames. Apply every fix below while keeping what already works. "
            "The code:\n```python\n"
            + code
            + "\n```\n\nCritique:\n"
            + issues
            + "\n\nOutput ONLY the full revised Python code in one "
            "```python block."
        )
        reply = self.backend.complete(prompt, timeout_s=self.timeout_s)
        return strip_code_fences(reply, "python")


class Critic:
    def __init__(self, backend: LLMBackend, timeout_s: int = 1800):
        self.backend = backend
        self.timeout_s = timeout_s

    def run(
        self, video_title: str, scene: SceneSpec, frames: list[Path]
    ) -> Critique:
        prompt = _load_prompt("critic").format(
            video_title=video_title,
            scene_id=scene.id,
            scene_title=scene.title,
            goal=scene.goal,
            beats_block=_beats_block(scene),
            visual_spec=scene.visual_spec,
            style_guide=_style_guide(),
        )
        reply = self.backend.complete(
            prompt, images=frames, timeout_s=self.timeout_s
        )
        try:
            return Critique.from_json(extract_json(reply))
        except (ValueError, json.JSONDecodeError):
            # An unparseable critique must not sink the pipeline.
            return Critique(verdict="pass", issues=[])
