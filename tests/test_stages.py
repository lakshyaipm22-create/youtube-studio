"""Tests for pipeline stages: input validation, execution, and status tracking."""

from pathlib import Path

import yaml

from pipeline.stages.animation_plan import AnimationPlanStage
from pipeline.stages.base import StageRunner
from pipeline.stages.manim_code import ManimCodeStage
from pipeline.stages.research import ResearchStage
from pipeline.stages.script import ScriptStage
from pipeline.stages.storyboard import StoryboardStage


class TestInputValidation:
    """Test that stages fail gracefully when required inputs are missing."""

    def test_research_requires_topic_yaml(self, tmp_path: Path):
        """Research stage fails if topic.yaml is missing."""
        runner = ResearchStage(tmp_path)
        assert runner.validate_input() is False

    def test_script_requires_research_yaml(self, tmp_path: Path):
        """Script stage fails if research.yaml is missing."""
        runner = ScriptStage(tmp_path)
        assert runner.validate_input() is False

    def test_storyboard_requires_script_md(self, tmp_path: Path):
        """Storyboard stage fails if script.md is missing."""
        runner = StoryboardStage(tmp_path)
        assert runner.validate_input() is False

    def test_animation_plan_requires_storyboard(self, tmp_path: Path):
        """Animation plan stage fails if storyboard.md is missing."""
        runner = AnimationPlanStage(tmp_path)
        assert runner.validate_input() is False

    def test_manim_code_requires_animation_plan(self, tmp_path: Path):
        """Manim code stage fails if animation_plan.yaml is missing."""
        runner = ManimCodeStage(tmp_path)
        assert runner.validate_input() is False

    def test_research_passes_with_topic_yaml(self, video_dir: Path):
        """Research stage passes validation when topic.yaml exists."""
        runner = ResearchStage(video_dir)
        assert runner.validate_input() is True

    def test_script_passes_with_research_yaml(self, video_dir_with_research: Path):
        """Script stage passes validation when research.yaml exists."""
        runner = ScriptStage(video_dir_with_research)
        assert runner.validate_input() is True

    def test_storyboard_passes_with_script_md(self, video_dir_with_script: Path):
        """Storyboard stage passes validation when script.md exists."""
        runner = StoryboardStage(video_dir_with_script)
        assert runner.validate_input() is True

    def test_animation_plan_passes_with_storyboard(self, video_dir_with_storyboard: Path):
        """Animation plan passes when storyboard.md exists."""
        runner = AnimationPlanStage(video_dir_with_storyboard)
        assert runner.validate_input() is True

    def test_manim_code_passes_with_animation_plan(self, video_dir_with_animation_plan: Path):
        """Manim code passes when animation_plan.yaml exists."""
        runner = ManimCodeStage(video_dir_with_animation_plan)
        assert runner.validate_input() is True


class TestStageExecution:
    """Test that AI stages produce correct output files using placeholder LLM."""

    def test_research_stage_produces_output(self, video_dir: Path, monkeypatch):
        """Research stage generates research.yaml from topic.yaml."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)

        runner = ResearchStage(video_dir)
        result = runner.execute()

        assert result is True
        output = video_dir / "research.yaml"
        assert output.exists()

        # Verify valid YAML
        with open(output) as f:
            data = yaml.safe_load(f)
        assert data is not None
        assert "topic" in data or "hook_ideas" in data

    def test_script_stage_produces_output(self, video_dir_with_research: Path, monkeypatch):
        """Script stage generates script.md from research.yaml."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)

        runner = ScriptStage(video_dir_with_research)
        result = runner.execute()

        assert result is True
        output = video_dir_with_research / "script.md"
        assert output.exists()

        content = output.read_text()
        assert len(content) > 50  # Non-trivial content
        assert "Scene" in content

    def test_storyboard_stage_produces_output(self, video_dir_with_script: Path, monkeypatch):
        """Storyboard stage generates storyboard.md from script.md."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)

        runner = StoryboardStage(video_dir_with_script)
        result = runner.execute()

        assert result is True
        output = video_dir_with_script / "storyboard.md"
        assert output.exists()

        content = output.read_text()
        assert len(content) > 50
        assert "Scene" in content

    def test_animation_plan_stage_produces_output(
        self, video_dir_with_storyboard: Path, monkeypatch
    ):
        """Animation plan stage generates animation_plan.yaml from storyboard.md."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)

        runner = AnimationPlanStage(video_dir_with_storyboard)
        result = runner.execute()

        assert result is True
        output = video_dir_with_storyboard / "animation_plan.yaml"
        assert output.exists()

        with open(output) as f:
            data = yaml.safe_load(f)
        assert data is not None
        assert "scenes" in data

    def test_manim_code_stage_produces_output(
        self, video_dir_with_animation_plan: Path, monkeypatch
    ):
        """Manim code stage generates scenes/scenes.py from animation_plan.yaml."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)

        runner = ManimCodeStage(video_dir_with_animation_plan)
        result = runner.execute()

        assert result is True
        output = video_dir_with_animation_plan / "scenes" / "scenes.py"
        assert output.exists()

        content = output.read_text()
        assert "from manim import" in content
        assert "class" in content
        assert "def construct" in content


class TestStatusTracking:
    """Test that status.yaml is updated correctly after stage execution."""

    def test_status_updated_on_success(self, video_dir: Path, monkeypatch):
        """Successful stage execution marks status as complete."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)

        runner = ResearchStage(video_dir)
        runner.execute()

        status_path = video_dir / "status.yaml"
        with open(status_path) as f:
            data = yaml.safe_load(f)

        stages = data["stages"]
        assert len(stages) == 1
        assert stages[0]["name"] == "research"
        assert stages[0]["status"] == "complete"
        assert "completed_at" in stages[0]

    def test_status_updated_on_failure(self, tmp_path: Path):
        """Failed stage execution marks status as failed."""
        # No topic.yaml - research will fail at validation
        status_path = tmp_path / "status.yaml"
        status_path.write_text("stages: []\n")

        runner = ResearchStage(tmp_path)
        result = runner.execute()

        assert result is False
        with open(status_path) as f:
            data = yaml.safe_load(f)

        stages = data["stages"]
        assert len(stages) == 1
        assert stages[0]["name"] == "research"
        assert stages[0]["status"] == "failed"

    def test_multiple_stages_tracked(self, video_dir: Path, monkeypatch):
        """Multiple stage completions are all tracked in status.yaml."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)

        # Run research
        research_runner = ResearchStage(video_dir)
        research_runner.execute()

        # Run script (research.yaml should now exist)
        script_runner = ScriptStage(video_dir)
        script_runner.execute()

        status_path = video_dir / "status.yaml"
        with open(status_path) as f:
            data = yaml.safe_load(f)

        stages = data["stages"]
        assert len(stages) == 2
        names = [s["name"] for s in stages]
        assert "research" in names
        assert "script" in names

    def test_rerun_updates_existing_entry(self, video_dir: Path, monkeypatch):
        """Re-running a stage updates the existing entry rather than duplicating."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)

        runner = ResearchStage(video_dir)
        runner.execute()
        runner.execute()  # Run again

        status_path = video_dir / "status.yaml"
        with open(status_path) as f:
            data = yaml.safe_load(f)

        stages = data["stages"]
        research_entries = [s for s in stages if s["name"] == "research"]
        assert len(research_entries) == 1


class TestOutputValidation:
    """Test that output validation works correctly."""

    def test_validate_output_fails_when_missing(self, tmp_path: Path):
        """Output validation fails when expected files do not exist."""
        runner = ResearchStage(tmp_path)
        assert runner.validate_output() is False

    def test_validate_output_passes_when_present(self, tmp_path: Path):
        """Output validation passes when expected files exist."""
        (tmp_path / "research.yaml").write_text("topic: test\n")
        runner = ResearchStage(tmp_path)
        assert runner.validate_output() is True


class TestExecuteLifecycle:
    """Test the full execute() lifecycle (validate -> run -> validate -> status)."""

    def test_execute_returns_false_on_missing_input(self, tmp_path: Path):
        """Execute fails early if input validation fails."""
        (tmp_path / "status.yaml").write_text("stages: []\n")
        runner = ResearchStage(tmp_path)
        assert runner.execute() is False

    def test_execute_returns_true_on_success(self, video_dir: Path, monkeypatch):
        """Execute returns True when all steps succeed."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        runner = ResearchStage(video_dir)
        assert runner.execute() is True


class TestStageRunnerInterface:
    """Test the StageRunner base class interface contract."""

    def test_all_stages_have_name(self):
        """All registered stages must have a non-empty name."""
        from pipeline.stages import STAGES

        for name, cls in STAGES:
            instance = cls(Path("/tmp/fake"))
            assert instance.name == name
            assert len(instance.name) > 0

    def test_ai_stages_have_required_inputs(self):
        """AI stages should declare required inputs."""
        from pipeline.stages import STAGES

        # Only check stages that are testable (AI stages)
        ai_stages = ["research", "script", "storyboard", "animation_plan", "manim_code"]
        for name, cls in STAGES:
            if name in ai_stages:
                instance = cls(Path("/tmp/fake"))
                assert len(instance.required_inputs) > 0, f"{name} has no required_inputs"

    def test_ai_stages_have_expected_outputs(self):
        """AI stages should declare expected outputs."""
        from pipeline.stages import STAGES

        ai_stages = ["research", "script", "storyboard", "animation_plan", "manim_code"]
        for name, cls in STAGES:
            if name in ai_stages:
                instance = cls(Path("/tmp/fake"))
                assert len(instance.expected_outputs) > 0, f"{name} has no expected_outputs"

    def test_stage_runner_is_abstract(self):
        """StageRunner cannot be instantiated directly."""
        import pytest

        with pytest.raises(TypeError):
            StageRunner(Path("/tmp/fake"))  # type: ignore[abstract]
