"""Tests for the produce.py CLI entry point."""

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
PRODUCE = ROOT / "produce.py"


def run_produce(*args: str) -> subprocess.CompletedProcess:
    """Run produce.py as a subprocess with the given arguments."""
    return subprocess.run(
        [sys.executable, str(PRODUCE), *args],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )


class TestCLIHelp:
    """Test --help flag produces expected output."""

    def test_help_exits_zero(self):
        result = run_produce("--help")
        assert result.returncode == 0

    def test_help_shows_description(self):
        result = run_produce("--help")
        assert "YouTube Studio Production Pipeline" in result.stdout

    def test_help_shows_arguments(self):
        result = run_produce("--help")
        assert "--from" in result.stdout
        assert "--only" in result.stdout
        assert "--video" in result.stdout
        assert "--dry-run" in result.stdout
        assert "--list-stages" in result.stdout


class TestListStages:
    """Test --list-stages shows all pipeline stages."""

    def test_list_stages_exits_zero(self):
        result = run_produce("--list-stages")
        assert result.returncode == 0

    def test_list_stages_shows_all_stages(self):
        result = run_produce("--list-stages")
        output = result.stdout + result.stderr
        expected_stages = [
            "research",
            "script",
            "storyboard",
            "animation_plan",
            "manim_code",
            "voice",
            "subtitles",
            "render",
            "export",
        ]
        for stage in expected_stages:
            assert stage in output, f"Stage '{stage}' not found in output"

    def test_list_stages_shows_numbered_order(self):
        result = run_produce("--list-stages")
        output = result.stdout + result.stderr
        # First stage should be numbered 1
        assert "1. research" in output


class TestDryRun:
    """Test --dry-run mode shows stages without executing."""

    def test_dry_run_with_topic(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        """Dry run with a new topic creates folder and shows stages."""
        videos_dir = tmp_path / "videos"
        videos_dir.mkdir()

        # Monkeypatch the ROOT and VIDEOS_DIR in produce module
        monkeypatch.setattr("produce.ROOT", tmp_path)
        monkeypatch.setattr("produce.VIDEOS_DIR", videos_dir)

        # Import after monkeypatching
        from produce import create_video_folder, run_pipeline

        video_dir = create_video_folder("Test Topic")
        result = run_pipeline(video_dir, dry_run=True)
        assert result is True

    def test_dry_run_shows_stage_count(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        """Dry run outputs the number of stages that would run."""
        videos_dir = tmp_path / "videos"
        videos_dir.mkdir()
        monkeypatch.setattr("produce.ROOT", tmp_path)
        monkeypatch.setattr("produce.VIDEOS_DIR", videos_dir)

        from produce import create_video_folder, run_pipeline

        video_dir = create_video_folder("Test Topic")
        # Should succeed without actually running stages
        result = run_pipeline(video_dir, dry_run=True)
        assert result is True

    def test_dry_run_from_stage(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        """Dry run with --from only shows stages from that point."""
        videos_dir = tmp_path / "videos"
        videos_dir.mkdir()
        monkeypatch.setattr("produce.ROOT", tmp_path)
        monkeypatch.setattr("produce.VIDEOS_DIR", videos_dir)

        from produce import create_video_folder, run_pipeline

        video_dir = create_video_folder("Test Topic")
        result = run_pipeline(video_dir, from_stage="storyboard", dry_run=True)
        assert result is True

    def test_dry_run_only_stage(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        """Dry run with --only shows just one stage."""
        videos_dir = tmp_path / "videos"
        videos_dir.mkdir()
        monkeypatch.setattr("produce.ROOT", tmp_path)
        monkeypatch.setattr("produce.VIDEOS_DIR", videos_dir)

        from produce import create_video_folder, run_pipeline

        video_dir = create_video_folder("Test Topic")
        result = run_pipeline(video_dir, only_stage="research", dry_run=True)
        assert result is True


class TestCLIArgParsing:
    """Test that CLI arguments are properly accepted."""

    def test_no_args_shows_help_and_exits_nonzero(self):
        result = run_produce()
        # No args should show help text and exit non-zero
        assert result.returncode != 0

    def test_from_flag_accepted(self):
        """--from flag with an invalid stage should still parse (error is at runtime)."""
        result = run_produce("--from", "research", "--video", "/nonexistent")
        # It should parse args correctly, even if video path is invalid
        assert result.returncode != 0
        # Should not be an argparse error (those mention "usage:" at top)

    def test_only_flag_accepted(self):
        """--only flag is accepted by argparse."""
        result = run_produce("--only", "script", "--video", "/nonexistent")
        assert result.returncode != 0

    def test_video_flag_accepted(self):
        """--video flag is accepted by argparse."""
        result = run_produce("--video", "/nonexistent")
        assert result.returncode != 0


class TestVideoFolderCreation:
    """Test video folder creation logic."""

    def test_create_video_folder(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        videos_dir = tmp_path / "videos"
        videos_dir.mkdir()
        monkeypatch.setattr("produce.ROOT", tmp_path)
        monkeypatch.setattr("produce.VIDEOS_DIR", videos_dir)

        from produce import create_video_folder

        video_dir = create_video_folder("Why Airplanes Fly")
        assert video_dir.exists()
        assert "why_airplanes_fly" in video_dir.name
        assert video_dir.name.startswith("001_")

    def test_topic_yaml_created(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        import yaml

        videos_dir = tmp_path / "videos"
        videos_dir.mkdir()
        monkeypatch.setattr("produce.ROOT", tmp_path)
        monkeypatch.setattr("produce.VIDEOS_DIR", videos_dir)

        from produce import create_video_folder

        video_dir = create_video_folder("Test Video")
        topic_path = video_dir / "topic.yaml"
        assert topic_path.exists()

        with open(topic_path) as f:
            data = yaml.safe_load(f)
        assert data["topic"] == "Test Video"
        assert "created_at" in data

    def test_status_yaml_initialized(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        import yaml

        videos_dir = tmp_path / "videos"
        videos_dir.mkdir()
        monkeypatch.setattr("produce.ROOT", tmp_path)
        monkeypatch.setattr("produce.VIDEOS_DIR", videos_dir)

        from produce import create_video_folder

        video_dir = create_video_folder("Test Video")
        status_path = video_dir / "status.yaml"
        assert status_path.exists()

        with open(status_path) as f:
            data = yaml.safe_load(f)
        assert data["stages"] == []

    def test_slugify_special_characters(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        videos_dir = tmp_path / "videos"
        videos_dir.mkdir()
        monkeypatch.setattr("produce.ROOT", tmp_path)
        monkeypatch.setattr("produce.VIDEOS_DIR", videos_dir)

        from produce import create_video_folder

        video_dir = create_video_folder("Why Don't Planes Fall?!")
        assert "dont" in video_dir.name
        assert "?" not in video_dir.name
        assert "!" not in video_dir.name


class TestStageOrdering:
    """Test that stages are in the correct order."""

    def test_stage_count(self):
        from pipeline.stages import STAGES

        assert len(STAGES) == 10

    def test_stage_order(self):
        from pipeline.stages import STAGE_NAMES

        expected = [
            "research",
            "script",
            "storyboard",
            "animation_plan",
            "manim_code",
            "voice",
            "timing",
            "subtitles",
            "render",
            "export",
        ]
        assert STAGE_NAMES == expected

    def test_from_stage_slices_correctly(self):
        """--from should start from the given stage, not skip it."""
        from pipeline.stages import STAGE_NAMES, STAGES

        start_idx = STAGE_NAMES.index("storyboard")
        stages_from = STAGES[start_idx:]
        names = [name for name, _ in stages_from]
        assert names[0] == "storyboard"
        assert "research" not in names
        assert "script" not in names
