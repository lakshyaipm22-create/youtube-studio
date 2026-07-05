"""
YouTube Studio - Timing Stage

Runs after the voice stage to extract per-segment timing from the voiceover
using faster-whisper with word-level timestamps. Matches transcribed segments
to script scenes (using # Scene headers) and outputs timing.yaml with
per-scene and per-sentence timing data.

This timing data becomes the single source of truth for animation pacing,
ensuring rendered scenes match voiceover duration.
"""

import logging
import re
from pathlib import Path

import yaml

from pipeline.stages.base import StageRunner

logger = logging.getLogger("pipeline")


def parse_script_scenes(script_path: Path) -> list[dict[str, str | list[str]]]:
    """Parse script.md into scenes with their narration text.

    Extracts scene headers (# Scene N: Name) and the narration lines
    (non-VISUAL, non-empty lines) for each scene.

    Args:
        script_path: Path to the script.md file.

    Returns:
        List of dicts with 'name' and 'sentences' keys.
    """
    content = script_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    scenes: list[dict[str, str | list[str]]] = []
    current_scene: dict[str, str | list[str]] | None = None

    for line in lines:
        # Match scene headers like "# Scene 1: Hook (Intro)" or "# Scene 2: The Wrong Answer"
        header_match = re.match(r"^#\s+Scene\s+\d+", line)
        if header_match:
            if current_scene is not None:
                scenes.append(current_scene)
            # Extract name: prefer parenthesized name, fall back to colon text
            name = _extract_scene_name(line)
            current_scene = {"name": name, "sentences": []}
            continue

        if current_scene is None:
            continue

        # Skip visual direction lines and empty lines
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("[VISUAL"):
            continue
        if stripped.startswith("["):
            continue

        # This is narration text - split into sentences
        # Append each sentence separately
        sentences = _split_sentences(stripped)
        current_scene["sentences"].extend(sentences)  # type: ignore[union-attr]

    if current_scene is not None:
        scenes.append(current_scene)

    return scenes


def _split_sentences(text: str) -> list[str]:
    """Split text into individual sentences.

    Handles common sentence-ending punctuation while preserving
    abbreviations and numbers.

    Args:
        text: A paragraph or line of narration text.

    Returns:
        List of individual sentences.
    """
    # Split on sentence-ending punctuation followed by a space or end
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p.strip() for p in parts if p.strip()]


def _extract_scene_name(header_line: str) -> str:
    """Extract scene name from a header line.

    Prefers parenthesized name (class identifier) over colon-separated
    descriptive name.

    Examples:
        "# Scene 1: Hook (Intro)" -> "Intro"
        "# Scene 2: The Wrong Answer (WindAndWing)" -> "WindAndWing"
        "# Scene 3: Recap" -> "Recap"

    Args:
        header_line: A script scene header line.

    Returns:
        Extracted scene name as a PascalCase identifier.
    """
    # First, look for a parenthesized name (class identifier)
    paren_match = re.search(r"\((\w+)\)\s*$", header_line)
    if paren_match:
        return paren_match.group(1)

    # Fall back to colon-separated name
    colon_match = re.search(r":\s*(.+?)(?:\s*\(.*\))?\s*$", header_line)
    if colon_match:
        name = colon_match.group(1).strip()
        # Convert to PascalCase identifier
        return re.sub(r"[^a-zA-Z0-9]", "", name.title().replace(" ", ""))

    return "Unknown"


def match_segments_to_scenes(
    segments: list[dict],
    scenes: list[dict[str, str | list[str]]],
) -> list[dict]:
    """Match transcribed audio segments to script scenes.

    Uses text similarity to align faster-whisper segments with the
    sentences defined in each script scene.

    Args:
        segments: List of dicts with 'text', 'start', 'end' from transcription.
        scenes: Parsed script scenes with 'name' and 'sentences'.

    Returns:
        List of scene timing dicts suitable for timing.yaml output.
    """
    if not segments or not scenes:
        return []

    # Build a flat list of all expected sentences across scenes
    # with their scene index
    scene_sentence_map: list[tuple[int, str]] = []
    for scene_idx, scene in enumerate(scenes):
        for sentence in scene["sentences"]:  # type: ignore[union-attr]
            scene_sentence_map.append((scene_idx, str(sentence)))

    # Assign each segment to the best-matching scene sentence
    # Use sequential matching: segments arrive in order matching script order
    segment_assignments: list[list[dict]] = [[] for _ in scenes]

    # Simple sequential assignment: walk through segments and sentences together
    sentence_idx = 0
    for seg in segments:
        seg_text = seg["text"].strip().lower()
        if not seg_text:
            continue

        # Find the best matching sentence from current position forward
        best_idx = sentence_idx
        best_score = 0.0

        search_end = min(sentence_idx + 5, len(scene_sentence_map))
        for i in range(sentence_idx, search_end):
            _, expected = scene_sentence_map[i]
            score = _text_similarity(seg_text, expected.lower())
            if score > best_score:
                best_score = score
                best_idx = i

        # If we have a reasonable match, advance
        if best_score > 0.2:
            sentence_idx = best_idx + 1

        # Assign segment to the scene of the best matching sentence
        if best_idx < len(scene_sentence_map):
            scene_idx = scene_sentence_map[best_idx][0]
        else:
            scene_idx = len(scenes) - 1

        segment_assignments[scene_idx].append(seg)

    # Build timing output
    result = []
    for scene_idx, scene in enumerate(scenes):
        assigned = segment_assignments[scene_idx]
        if assigned:
            scene_start = assigned[0]["start"]
            scene_end = assigned[-1]["end"]
        elif result:
            # No segments matched - use end of previous scene
            scene_start = result[-1]["end"]
            scene_end = scene_start
        else:
            scene_start = 0.0
            scene_end = 0.0

        sentences = []
        for seg in assigned:
            sentences.append(
                {
                    "text": seg["text"].strip(),
                    "start": float(round(seg["start"], 3)),
                    "end": float(round(seg["end"], 3)),
                    "duration": float(round(seg["end"] - seg["start"], 3)),
                }
            )

        result.append(
            {
                "name": scene["name"],
                "start": float(round(scene_start, 3)),
                "end": float(round(scene_end, 3)),
                "duration": float(round(scene_end - scene_start, 3)),
                "sentences": sentences,
            }
        )

    return result


def _text_similarity(a: str, b: str) -> float:
    """Compute simple word-overlap similarity between two strings.

    Args:
        a: First string (lowercased).
        b: Second string (lowercased).

    Returns:
        Float between 0.0 and 1.0 representing overlap ratio.
    """
    words_a = set(re.findall(r"\w+", a))
    words_b = set(re.findall(r"\w+", b))

    if not words_a or not words_b:
        return 0.0

    intersection = words_a & words_b
    union = words_a | words_b
    return len(intersection) / len(union)


class TimingStage(StageRunner):
    """Extract timing information from voiceover and map to script scenes."""

    name = "timing"
    required_inputs = ["script.md"]
    expected_outputs = ["timing.yaml"]

    def validate_input(self) -> bool:
        """Check that script.md and voiceover audio exist."""
        if not (self.video_dir / "script.md").exists():
            logger.error("[timing] Missing required input: script.md")
            return False

        wav_path = self.video_dir / "voice" / "voiceover.wav"
        mp3_path = self.video_dir / "voice" / "voiceover.mp3"
        if not wav_path.exists() and not mp3_path.exists():
            logger.error("[timing] Missing required input: voice/voiceover.wav or .mp3")
            return False

        return True

    def run(self) -> bool:
        """Transcribe voiceover and generate timing.yaml."""
        script_path = self.video_dir / "script.md"
        scenes = parse_script_scenes(script_path)

        if not scenes:
            logger.error("[timing] No scenes found in script.md")
            return False

        logger.info(f"[timing] Parsed {len(scenes)} scenes from script")

        # Find voiceover
        audio_path = self.video_dir / "voice" / "voiceover.wav"
        if not audio_path.exists():
            audio_path = self.video_dir / "voice" / "voiceover.mp3"

        # Transcribe with word timestamps
        segments = self._transcribe(audio_path)
        if segments is None:
            return False

        logger.info(f"[timing] Transcribed {len(segments)} segments")

        # Match segments to scenes
        scene_timings = match_segments_to_scenes(segments, scenes)

        # Compute total duration
        total_duration = 0.0
        if scene_timings:
            total_duration = float(max(s["end"] for s in scene_timings))

        # Write timing.yaml
        timing_data = {
            "total_duration": round(total_duration, 3),
            "scenes": scene_timings,
        }

        output_path = self.video_dir / "timing.yaml"
        with open(output_path, "w", encoding="utf-8") as f:
            yaml.dump(timing_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

        logger.info(f"[timing] Saved: timing.yaml (total: {total_duration:.1f}s)")
        return True

    def _transcribe(self, audio_path: Path) -> list[dict] | None:
        """Transcribe audio file using faster-whisper with segment timestamps.

        Args:
            audio_path: Path to the audio file.

        Returns:
            List of segment dicts with 'text', 'start', 'end', or None on failure.
        """
        try:
            from faster_whisper import WhisperModel
        except ImportError:
            logger.error("[timing] faster-whisper not installed")
            return None

        try:
            model = WhisperModel("medium", compute_type="int8")
            segments_iter, info = model.transcribe(
                str(audio_path),
                beam_size=5,
                word_timestamps=True,
            )

            logger.info(
                f"[timing] Language: {info.language} (confidence: {info.language_probability:.2f})"
            )

            segments = []
            for segment in segments_iter:
                text = segment.text.strip()
                if text:
                    segments.append(
                        {
                            "text": text,
                            "start": segment.start,
                            "end": segment.end,
                        }
                    )

            return segments

        except Exception as e:
            logger.error(f"[timing] Transcription failed: {e}")
            return None
