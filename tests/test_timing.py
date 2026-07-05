"""Tests for the timing pipeline stage and studio/timing.py helper module."""

from pathlib import Path

import yaml

from pipeline.stages.timing import (
    TimingStage,
    _split_sentences,
    _text_similarity,
    match_segments_to_scenes,
    parse_script_scenes,
)
from studio.timing import (
    SceneTiming,
    SentenceTiming,
    VideoTiming,
    _parse_timing_data,
    get_scene_duration,
    load_timing,
)

SAMPLE_SCRIPT = """# Scene 1: Hook (Intro)

[VISUAL: Number "400" scales up massively]

A Boeing 747 weighs 400 tons. That is 80 elephants.

And somehow it flies.

# Scene 2: The Wrong Answer (WindAndWing)

[VISUAL: Classic textbook wing diagram draws in]

You probably learned this in school. The wing is curved on top.

Sounds clean. One problem: planes can fly upside down.

# Scene 3: Recap (Outro)

[VISUAL: Clean final diagram]

So remember: angle of attack is what keeps planes up.

If this made flight click for you, hit subscribe.
"""


class TestParseScriptScenes:
    """Test script parsing into scenes."""

    def test_parses_scenes_from_script(self, tmp_path: Path):
        """Correctly identifies scenes from # Scene headers."""
        script_path = tmp_path / "script.md"
        script_path.write_text(SAMPLE_SCRIPT)

        scenes = parse_script_scenes(script_path)
        assert len(scenes) == 3

    def test_extracts_scene_names(self, tmp_path: Path):
        """Extracts scene names from parentheses or colon text."""
        script_path = tmp_path / "script.md"
        script_path.write_text(SAMPLE_SCRIPT)

        scenes = parse_script_scenes(script_path)
        assert scenes[0]["name"] == "Intro"
        assert scenes[1]["name"] == "WindAndWing"
        assert scenes[2]["name"] == "Outro"

    def test_extracts_narration_sentences(self, tmp_path: Path):
        """Extracts narration (non-VISUAL) lines as sentences."""
        script_path = tmp_path / "script.md"
        script_path.write_text(SAMPLE_SCRIPT)

        scenes = parse_script_scenes(script_path)
        # Scene 1 has narration sentences
        assert len(scenes[0]["sentences"]) > 0
        # Visual directions are excluded
        for sentence in scenes[0]["sentences"]:
            assert not str(sentence).startswith("[VISUAL")

    def test_skips_visual_directions(self, tmp_path: Path):
        """VISUAL direction lines are excluded from sentences."""
        script_path = tmp_path / "script.md"
        script_path.write_text(SAMPLE_SCRIPT)

        scenes = parse_script_scenes(script_path)
        all_sentences = []
        for scene in scenes:
            all_sentences.extend(scene["sentences"])

        for sentence in all_sentences:
            assert "[VISUAL" not in str(sentence)

    def test_empty_script_returns_no_scenes(self, tmp_path: Path):
        """Empty script returns an empty list."""
        script_path = tmp_path / "script.md"
        script_path.write_text("")

        scenes = parse_script_scenes(script_path)
        assert scenes == []


class TestSplitSentences:
    """Test sentence splitting logic."""

    def test_splits_on_period(self):
        """Splits text at sentence-ending periods."""
        result = _split_sentences("First sentence. Second sentence.")
        assert len(result) == 2
        assert result[0] == "First sentence."
        assert result[1] == "Second sentence."

    def test_single_sentence(self):
        """Single sentence returns as-is."""
        result = _split_sentences("Just one sentence.")
        assert len(result) == 1
        assert result[0] == "Just one sentence."

    def test_handles_question_marks(self):
        """Splits on question marks."""
        result = _split_sentences("Is this a question? Yes it is.")
        assert len(result) == 2

    def test_handles_exclamation(self):
        """Splits on exclamation marks."""
        result = _split_sentences("Wow! That is amazing.")
        assert len(result) == 2

    def test_empty_string(self):
        """Empty string returns empty list."""
        result = _split_sentences("")
        assert result == []


class TestTextSimilarity:
    """Test text similarity function."""

    def test_identical_strings(self):
        """Identical strings have similarity 1.0."""
        assert _text_similarity("hello world", "hello world") == 1.0

    def test_no_overlap(self):
        """Completely different strings have similarity 0.0."""
        assert _text_similarity("hello world", "foo bar") == 0.0

    def test_partial_overlap(self):
        """Partial overlap returns value between 0 and 1."""
        score = _text_similarity("hello world", "hello there")
        assert 0.0 < score < 1.0

    def test_empty_strings(self):
        """Empty strings return 0.0."""
        assert _text_similarity("", "") == 0.0
        assert _text_similarity("hello", "") == 0.0


class TestMatchSegmentsToScenes:
    """Test matching transcribed segments to script scenes."""

    def test_basic_matching(self):
        """Segments get assigned to correct scenes based on text overlap."""
        scenes = [
            {"name": "Intro", "sentences": ["A Boeing 747 weighs 400 tons."]},
            {"name": "Core", "sentences": ["The wing is curved on top."]},
        ]
        segments = [
            {"text": "A Boeing 747 weighs 400 tons.", "start": 0.0, "end": 3.0},
            {"text": "The wing is curved on top.", "start": 3.0, "end": 6.0},
        ]

        result = match_segments_to_scenes(segments, scenes)
        assert len(result) == 2
        assert result[0]["name"] == "Intro"
        assert result[1]["name"] == "Core"
        assert len(result[0]["sentences"]) == 1
        assert len(result[1]["sentences"]) == 1

    def test_empty_segments(self):
        """Empty segments list returns empty scene timings."""
        scenes = [{"name": "Intro", "sentences": ["Some text."]}]
        result = match_segments_to_scenes([], scenes)
        assert result == []

    def test_empty_scenes(self):
        """Empty scenes list returns empty result."""
        segments = [{"text": "Hello", "start": 0.0, "end": 1.0}]
        result = match_segments_to_scenes(segments, [])
        assert result == []

    def test_timing_values_correct(self):
        """Scene timing start/end/duration are computed from segments."""
        scenes = [
            {"name": "Only", "sentences": ["First sentence.", "Second sentence."]},
        ]
        segments = [
            {"text": "First sentence.", "start": 1.5, "end": 3.0},
            {"text": "Second sentence.", "start": 3.0, "end": 5.5},
        ]

        result = match_segments_to_scenes(segments, scenes)
        assert result[0]["start"] == 1.5
        assert result[0]["end"] == 5.5
        assert result[0]["duration"] == 4.0

    def test_sentence_timing_has_required_fields(self):
        """Each sentence in result has text, start, end, duration."""
        scenes = [{"name": "S1", "sentences": ["Hello world."]}]
        segments = [{"text": "Hello world.", "start": 0.0, "end": 2.0}]

        result = match_segments_to_scenes(segments, scenes)
        sentence = result[0]["sentences"][0]
        assert "text" in sentence
        assert "start" in sentence
        assert "end" in sentence
        assert "duration" in sentence


class TestTimingStage:
    """Test the TimingStage pipeline stage."""

    def test_validate_input_requires_script(self, tmp_path: Path):
        """Timing stage requires script.md."""
        runner = TimingStage(tmp_path)
        assert runner.validate_input() is False

    def test_validate_input_requires_voiceover(self, tmp_path: Path):
        """Timing stage requires voiceover audio."""
        (tmp_path / "script.md").write_text("# Scene 1: Test\nHello.")
        runner = TimingStage(tmp_path)
        assert runner.validate_input() is False

    def test_validate_input_passes(self, tmp_path: Path):
        """Timing stage passes when both script and voiceover exist."""
        (tmp_path / "script.md").write_text("# Scene 1: Test (Intro)\nHello.")
        voice_dir = tmp_path / "voice"
        voice_dir.mkdir()
        (voice_dir / "voiceover.wav").write_bytes(b"fake audio")

        runner = TimingStage(tmp_path)
        assert runner.validate_input() is True

    def test_validate_input_accepts_mp3(self, tmp_path: Path):
        """Timing stage accepts .mp3 voiceover."""
        (tmp_path / "script.md").write_text("# Scene 1: Test (Intro)\nHello.")
        voice_dir = tmp_path / "voice"
        voice_dir.mkdir()
        (voice_dir / "voiceover.mp3").write_bytes(b"fake audio")

        runner = TimingStage(tmp_path)
        assert runner.validate_input() is True

    def test_stage_name(self):
        """Stage name is 'timing'."""
        runner = TimingStage(Path("/tmp/fake"))
        assert runner.name == "timing"

    def test_expected_outputs(self):
        """Stage expects timing.yaml output."""
        runner = TimingStage(Path("/tmp/fake"))
        assert "timing.yaml" in runner.expected_outputs


class TestStudioTiming:
    """Test the studio/timing.py helper module."""

    def test_load_timing_from_yaml(self, tmp_path: Path):
        """load_timing reads and parses timing.yaml correctly."""
        timing_data = {
            "total_duration": 143.5,
            "scenes": [
                {
                    "name": "Intro",
                    "start": 0.0,
                    "end": 18.2,
                    "duration": 18.2,
                    "sentences": [
                        {
                            "text": "A Boeing 747 weighs 400 tons.",
                            "start": 0.0,
                            "end": 3.1,
                            "duration": 3.1,
                        },
                        {
                            "text": "That is 80 elephants.",
                            "start": 3.1,
                            "end": 5.6,
                            "duration": 2.5,
                        },
                    ],
                },
                {
                    "name": "WindAndWing",
                    "start": 18.2,
                    "end": 65.0,
                    "duration": 46.8,
                    "sentences": [],
                },
            ],
        }

        timing_path = tmp_path / "timing.yaml"
        with open(timing_path, "w") as f:
            yaml.dump(timing_data, f, default_flow_style=False)

        result = load_timing(tmp_path)

        assert isinstance(result, VideoTiming)
        assert result.total_duration == 143.5
        assert len(result.scenes) == 2

    def test_get_scene_by_name(self, tmp_path: Path):
        """get_scene returns the correct SceneTiming."""
        timing_data = {
            "total_duration": 50.0,
            "scenes": [
                {"name": "Intro", "start": 0.0, "end": 20.0, "duration": 20.0, "sentences": []},
                {"name": "Core", "start": 20.0, "end": 50.0, "duration": 30.0, "sentences": []},
            ],
        }

        timing_path = tmp_path / "timing.yaml"
        with open(timing_path, "w") as f:
            yaml.dump(timing_data, f, default_flow_style=False)

        result = load_timing(tmp_path)
        scene = result.get_scene("Intro")

        assert scene is not None
        assert isinstance(scene, SceneTiming)
        assert scene.name == "Intro"
        assert scene.duration == 20.0

    def test_get_scene_returns_none_for_missing(self, tmp_path: Path):
        """get_scene returns None if scene name does not exist."""
        timing_data = {
            "total_duration": 10.0,
            "scenes": [
                {"name": "Intro", "start": 0.0, "end": 10.0, "duration": 10.0, "sentences": []},
            ],
        }

        timing_path = tmp_path / "timing.yaml"
        with open(timing_path, "w") as f:
            yaml.dump(timing_data, f, default_flow_style=False)

        result = load_timing(tmp_path)
        assert result.get_scene("NonExistent") is None

    def test_get_scene_duration_helper(self, tmp_path: Path):
        """get_scene_duration returns duration for a named scene."""
        timing_data = {
            "total_duration": 30.0,
            "scenes": [
                {"name": "Intro", "start": 0.0, "end": 15.0, "duration": 15.0, "sentences": []},
                {"name": "Core", "start": 15.0, "end": 30.0, "duration": 15.0, "sentences": []},
            ],
        }

        timing_path = tmp_path / "timing.yaml"
        with open(timing_path, "w") as f:
            yaml.dump(timing_data, f, default_flow_style=False)

        assert get_scene_duration("Intro", tmp_path) == 15.0
        assert get_scene_duration("Core", tmp_path) == 15.0
        assert get_scene_duration("Missing", tmp_path) == 0.0

    def test_load_timing_file_not_found(self, tmp_path: Path):
        """load_timing raises FileNotFoundError if timing.yaml missing."""
        import pytest

        with pytest.raises(FileNotFoundError):
            load_timing(tmp_path)

    def test_sentence_timing_dataclass(self):
        """SentenceTiming dataclass stores all fields."""
        sent = SentenceTiming(text="Hello world.", start=0.0, end=2.0, duration=2.0)
        assert sent.text == "Hello world."
        assert sent.start == 0.0
        assert sent.end == 2.0
        assert sent.duration == 2.0

    def test_scene_timing_dataclass(self):
        """SceneTiming dataclass stores all fields including sentences."""
        sent = SentenceTiming(text="Test.", start=0.0, end=1.0, duration=1.0)
        scene = SceneTiming(name="Intro", start=0.0, end=10.0, duration=10.0, sentences=[sent])
        assert scene.name == "Intro"
        assert scene.duration == 10.0
        assert len(scene.sentences) == 1
        assert scene.sentences[0].text == "Test."

    def test_video_timing_dataclass(self):
        """VideoTiming dataclass stores total_duration and scenes."""
        timing = VideoTiming(total_duration=100.0, scenes=[])
        assert timing.total_duration == 100.0
        assert timing.scenes == []

    def test_parse_timing_data_handles_none(self):
        """_parse_timing_data handles None input gracefully."""
        result = _parse_timing_data(None)
        assert result.total_duration == 0.0
        assert result.scenes == []

    def test_parse_timing_data_handles_empty_dict(self):
        """_parse_timing_data handles empty dict."""
        result = _parse_timing_data({})
        assert result.total_duration == 0.0
        assert result.scenes == []


class TestTimingStageInRegistry:
    """Test that timing stage is properly registered in the pipeline."""

    def test_timing_in_stage_names(self):
        """Timing stage is in the STAGE_NAMES list."""
        from pipeline.stages import STAGE_NAMES

        assert "timing" in STAGE_NAMES

    def test_timing_after_voice(self):
        """Timing stage comes after voice in the pipeline order."""
        from pipeline.stages import STAGE_NAMES

        voice_idx = STAGE_NAMES.index("voice")
        timing_idx = STAGE_NAMES.index("timing")
        assert timing_idx > voice_idx

    def test_timing_before_render(self):
        """Timing stage comes before render in the pipeline order."""
        from pipeline.stages import STAGE_NAMES

        timing_idx = STAGE_NAMES.index("timing")
        render_idx = STAGE_NAMES.index("render")
        assert timing_idx < render_idx

    def test_timing_stage_class_registered(self):
        """TimingStage class is the registered class for 'timing'."""
        from pipeline.stages import STAGES

        timing_entries = [(name, cls) for name, cls in STAGES if name == "timing"]
        assert len(timing_entries) == 1
        assert timing_entries[0][1] is TimingStage


class TestExportDurationValidation:
    """Test the export stage duration validation."""

    def test_get_media_duration_returns_none_for_missing_file(self, tmp_path: Path):
        """_get_media_duration returns None for nonexistent file."""
        from pipeline.stages.export import _get_media_duration

        result = _get_media_duration(tmp_path / "nonexistent.mp4")
        assert result is None

    def test_export_stage_has_validate_method(self):
        """ExportStage has _validate_duration_sync method."""
        from pipeline.stages.export import ExportStage

        runner = ExportStage(Path("/tmp/fake"))
        assert hasattr(runner, "_validate_duration_sync")

    def test_validate_duration_sync_skips_when_no_voiceover(self, tmp_path: Path):
        """Duration validation is skipped when voiceover_path is None."""
        from pipeline.stages.export import ExportStage

        runner = ExportStage(tmp_path)
        # Should not raise - just returns early
        runner._validate_duration_sync(tmp_path / "video.mp4", None)
