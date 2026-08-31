"""Runtime helpers for generated Manim scenes.

The animator agent writes scenes against this small API. BeatClock keeps
the visuals synchronized with the narration beats: all play/wait calls go
through the clock, and end_beat(i) pads with a wait so that each beat's
visuals span exactly the beat's audio duration.
"""

from __future__ import annotations


class BeatClock:
    def __init__(self, scene, beat_durations):
        self.scene = scene
        self.durations = list(beat_durations)
        self.elapsed = 0.0

    def play(self, *animations, run_time: float = 1.0, **kwargs):
        self.scene.play(*animations, run_time=run_time, **kwargs)
        self.elapsed += run_time

    def wait(self, seconds: float = 1.0):
        if seconds > 0:
            self.scene.wait(seconds)
            self.elapsed += seconds

    def beat_budget(self, index: int) -> float:
        """Seconds available for beat `index`."""
        return self.durations[index]

    def end_beat(self, index: int):
        """Pad with a wait so visuals line up with the end of this beat's audio."""
        target = sum(self.durations[: index + 1])
        remaining = target - self.elapsed
        if remaining > 1e-3:
            self.wait(remaining)
        self.elapsed = max(self.elapsed, target)
