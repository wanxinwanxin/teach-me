"""End-to-end orchestration: topic -> narrated explainer video.

Stages: research -> direct -> narrate (TTS) -> per scene
[animate -> render -> critique -> revise] -> mux -> concat -> notify.

Every stage writes its artifact to the output directory, and --resume
skips any stage whose artifact already exists. That makes long runs
cheap to restart.
"""

from __future__ import annotations

import datetime
import re
import sys
import threading
import traceback
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from . import assemble
from .config import TeachmeConfig
from .notify import notify
from .registry import BACKENDS, RENDERERS, TTS_BACKENDS, load
from .roles import Animator, Critic, Director, Researcher
from .types import RenderError, SceneSpec, Storyboard

_print_lock = threading.Lock()


class Pipeline:
    def __init__(self, config: TeachmeConfig, out_dir: Path, resume: bool = False):
        self.cfg = config
        self.out = Path(out_dir).resolve()
        self.out.mkdir(parents=True, exist_ok=True)
        self.resume = resume
        self.log_file = self.out / "run.log"

        def backend_for(role: str):
            rc = self.cfg.roles[role]
            return load(BACKENDS, rc.backend, model=rc.model)

        t = self.cfg.limits.llm_timeout_s
        self.renderer = load(
            RENDERERS,
            self.cfg.renderer.name,
            quality=self.cfg.renderer.quality,
            fps=self.cfg.renderer.fps,
        )
        self.researcher = Researcher(backend_for("researcher"), t)
        self.director = Director(backend_for("director"), t)
        self.animator = Animator(
            backend_for("animator"), self.renderer.code_contract, t
        )
        self.critic = Critic(backend_for("critic"), t)
        self.tts = load(
            TTS_BACKENDS,
            self.cfg.tts.backend,
            voice=self.cfg.tts.voice,
            rate=self.cfg.tts.rate,
        )

    def log(self, msg: str) -> None:
        stamp = datetime.datetime.now().strftime("%H:%M:%S")
        line = f"[{stamp}] {msg}"
        with _print_lock:
            print(line, flush=True)
            with self.log_file.open("a") as f:
                f.write(line + "\n")

    # ---------- stages ----------

    def load_sources(self, source_paths: list[Path]) -> dict[str, str]:
        budget = self.cfg.limits.source_char_budget
        files: list[Path] = []
        for p in source_paths:
            if p.is_dir():
                files.extend(sorted(f for f in p.rglob("*") if f.is_file()))
            else:
                files.append(p)
        sources: dict[str, str] = {}
        per_file = budget // max(1, len(files))
        for f in files:
            try:
                text = f.read_text(errors="ignore")
            except OSError:
                continue
            sources[f.name] = text[:per_file]
        return sources

    def research(self, topic: str, sources: dict[str, str], clarification: str,
                 allow_web: bool) -> str:
        brief_path = self.out / "brief.md"
        if self.resume and brief_path.exists():
            self.log("research: reusing existing brief.md")
            return brief_path.read_text()
        self.log(f"research: {len(sources)} source file(s), web={allow_web}")
        brief = self.researcher.run(topic, sources, clarification, allow_web)
        brief_path.write_text(brief)
        self.log(f"research: brief written ({len(brief)} chars)")
        return brief

    def direct(self, topic: str, brief: str) -> Storyboard:
        board_path = self.out / "storyboard.json"
        if self.resume and board_path.exists():
            self.log("direct: reusing existing storyboard.json")
            return Storyboard.from_json(board_path.read_text())
        self.log("direct: writing storyboard")
        board = self.director.run(topic, brief, self.cfg.limits.max_scenes)
        board.save(board_path)
        self.log(
            f"direct: {len(board.scenes)} scenes — "
            + "; ".join(s.title for s in board.scenes)
        )
        return board

    def narrate(self, board: Storyboard) -> None:
        """Synthesize every beat, fill in durations, build per-scene tracks."""
        for scene in board.scenes:
            audio_dir = self.out / "scenes" / scene.id / "audio"
            track = audio_dir / "scene.wav"
            wavs = []
            for i, beat in enumerate(scene.narration):
                wav = audio_dir / f"beat_{i:02d}.wav"
                if not (self.resume and wav.exists()):
                    self.tts.synthesize(beat.text, wav)
                from .audio.base import probe_duration

                beat.duration = probe_duration(wav) + 0.6  # breathing room
                wavs.append(wav)
            assemble.concat_wavs(wavs, track)
            self.log(
                f"narrate: scene {scene.id} — {len(wavs)} beats, "
                f"{scene.total_duration:.0f}s"
            )
        board.save(self.out / "storyboard.json")

    def build_scene(self, board: Storyboard, scene: SceneSpec) -> Path:
        scene_dir = self.out / "scenes" / scene.id
        final = scene_dir / "scene_final.mp4"
        if self.resume and final.exists():
            self.log(f"scene {scene.id}: reusing scene_final.mp4")
            return final
        scene_dir.mkdir(parents=True, exist_ok=True)

        code = self.animator.write(board.title, scene)
        version = 1
        (scene_dir / f"code_v{version}.py").write_text(code)
        video = self._render_with_fixes(board, scene, scene_dir, code, version)

        for it in range(self.cfg.limits.max_critique_iters):
            frames = assemble.sample_frames(video, scene_dir / "frames", count=8)
            critique = self.critic.run(board.title, scene, frames)
            (scene_dir / f"critique_v{version}.json").write_text(critique.to_json())
            n_high = sum(1 for i in critique.issues if i.severity == "high")
            self.log(
                f"scene {scene.id}: critique v{version} -> {critique.verdict} "
                f"({len(critique.issues)} issues, {n_high} high)"
            )
            if not critique.needs_revision:
                break
            code = self.animator.revise(board.title, scene, code, critique)
            version += 1
            (scene_dir / f"code_v{version}.py").write_text(code)
            video = self._render_with_fixes(board, scene, scene_dir, code, version)

        assemble.mux(video, scene_dir / "audio" / "scene.wav", final)
        self.log(f"scene {scene.id}: done -> {final.name}")
        return final

    def _render_with_fixes(
        self,
        board: Storyboard,
        scene: SceneSpec,
        scene_dir: Path,
        code: str,
        version: int,
    ) -> Path:
        workdir = scene_dir / f"render_v{version}"
        for attempt in range(self.cfg.limits.max_render_fixes + 1):
            try:
                video = self.renderer.render(code, workdir)
                self.log(f"scene {scene.id}: rendered v{version} (try {attempt + 1})")
                (scene_dir / f"code_v{version}.py").write_text(code)
                return video
            except RenderError as err:
                if attempt >= self.cfg.limits.max_render_fixes:
                    raise
                self.log(
                    f"scene {scene.id}: render failed (try {attempt + 1}), "
                    "asking animator to fix"
                )
                code = self.animator.fix(board.title, scene, code, str(err))
        raise RuntimeError("unreachable")

    # ---------- entry point ----------

    def run(
        self,
        topic: str,
        source_paths: list[Path] | None = None,
        clarification: str = "",
        allow_web: bool = True,
        parallel: int = 2,
    ) -> Path:
        sources = self.load_sources(source_paths or [])
        brief = self.research(topic, sources, clarification, allow_web)
        board = self.direct(topic, brief)
        self.narrate(board)

        results: dict[str, Path] = {}
        errors: dict[str, str] = {}

        def worker(scene: SceneSpec) -> None:
            try:
                results[scene.id] = self.build_scene(board, scene)
            except Exception:
                errors[scene.id] = traceback.format_exc()
                self.log(f"scene {scene.id}: FAILED\n{errors[scene.id]}")

        with ThreadPoolExecutor(max_workers=max(1, parallel)) as pool:
            list(pool.map(worker, board.scenes))

        if errors:
            self.log(
                f"{len(errors)} scene(s) failed: {', '.join(sorted(errors))}. "
                "Fix and re-run with --resume to keep finished scenes."
            )
            sys.exit(1)

        slug = re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-")[:60]
        final = self.out / f"{slug}.mp4"
        assemble.concat_videos(
            [results[s.id] for s in board.scenes], final
        )
        self.log(f"final video: {final}")
        notify(self.cfg.notify, topic, final)
        return final
