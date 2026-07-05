"""
YouTube Studio - Timing Helper

Provides functions for Manim scenes to load and consume timing data
from timing.yaml. This allows animations to adapt their pacing
to match the voiceover duration automatically.

Usage:
    from studio.timing import load_timing, get_scene_duration

    class Intro(StudioScene):
        def construct(self):
            timing = load_timing()
            scene_timing = timing.get_scene("Intro")
            # Use scene_timing.duration for overall pacing
            # Use scene_timing.sentences[i].duration for per-sentence pacing
"""

from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class SentenceTiming:
    """Timing data for a single narration sentence."""

    text: str
    start: float
    end: float
    duration: float


@dataclass
class SceneTiming:
    """Timing data for a single scene."""

    name: str
    start: float
    end: float
    duration: float
    sentences: list[SentenceTiming] = field(default_factory=list)


@dataclass
class VideoTiming:
    """Complete timing data for a video, loaded from timing.yaml."""

    total_duration: float
    scenes: list[SceneTiming] = field(default_factory=list)

    def get_scene(self, name: str) -> SceneTiming | None:
        """Get timing data for a scene by name.

        Args:
            name: The scene name (e.g., "Intro", "WindAndWing").

        Returns:
            SceneTiming for the matched scene, or None if not found.
        """
        for scene in self.scenes:
            if scene.name == name:
                return scene
        return None


def load_timing(video_dir: Path | None = None) -> VideoTiming:
    """Load timing.yaml from the video directory.

    Searches for timing.yaml in the given directory. If no directory is
    provided, attempts to find it relative to the calling scene file
    by walking up to find a timing.yaml.

    Args:
        video_dir: Path to the video directory containing timing.yaml.
                   If None, searches parent directories.

    Returns:
        VideoTiming dataclass with all timing information.

    Raises:
        FileNotFoundError: If timing.yaml cannot be found.
    """
    if video_dir is not None:
        timing_path = Path(video_dir) / "timing.yaml"
    else:
        # Try to find timing.yaml by searching upward from CWD
        timing_path = _find_timing_yaml()

    if not timing_path.exists():
        raise FileNotFoundError(f"timing.yaml not found at: {timing_path}")

    with open(timing_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return _parse_timing_data(data)


def get_scene_duration(name: str, video_dir: Path | None = None) -> float:
    """Get the duration of a specific scene from timing.yaml.

    Convenience function for quick duration lookups.

    Args:
        name: The scene name to look up.
        video_dir: Path to the video directory. If None, auto-discovers.

    Returns:
        Duration in seconds, or 0.0 if the scene is not found.
    """
    timing = load_timing(video_dir)
    scene = timing.get_scene(name)
    if scene is None:
        return 0.0
    return scene.duration


def _find_timing_yaml() -> Path:
    """Search for timing.yaml starting from CWD and walking upward.

    Returns:
        Path to timing.yaml (may not exist).
    """
    cwd = Path.cwd()

    # Check CWD first
    candidate = cwd / "timing.yaml"
    if candidate.exists():
        return candidate

    # Walk up to 5 levels
    current = cwd
    for _ in range(5):
        current = current.parent
        candidate = current / "timing.yaml"
        if candidate.exists():
            return candidate

    # Fall back to CWD
    return cwd / "timing.yaml"


def _parse_timing_data(data: dict) -> VideoTiming:
    """Parse raw YAML data into VideoTiming dataclass.

    Args:
        data: Dictionary loaded from timing.yaml.

    Returns:
        VideoTiming instance with all scenes and sentences.
    """
    if data is None:
        return VideoTiming(total_duration=0.0)

    scenes = []
    for scene_data in data.get("scenes", []):
        sentences = []
        for sent_data in scene_data.get("sentences", []):
            sentences.append(
                SentenceTiming(
                    text=sent_data.get("text", ""),
                    start=float(sent_data.get("start", 0.0)),
                    end=float(sent_data.get("end", 0.0)),
                    duration=float(sent_data.get("duration", 0.0)),
                )
            )

        scenes.append(
            SceneTiming(
                name=scene_data.get("name", ""),
                start=float(scene_data.get("start", 0.0)),
                end=float(scene_data.get("end", 0.0)),
                duration=float(scene_data.get("duration", 0.0)),
                sentences=sentences,
            )
        )

    return VideoTiming(
        total_duration=float(data.get("total_duration", 0.0)),
        scenes=scenes,
    )
