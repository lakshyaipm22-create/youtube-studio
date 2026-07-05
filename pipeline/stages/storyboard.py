"""
YouTube Studio - Storyboard Stage

Takes script.md and generates storyboard.md with per-scene visual plans.
"""

import logging
from pathlib import Path

from pipeline.llm import generate
from pipeline.stages.base import StageRunner

logger = logging.getLogger("pipeline")

ROOT = Path(__file__).resolve().parent.parent.parent


class StoryboardStage(StageRunner):
    """Generate a storyboard from the script."""

    name = "storyboard"
    required_inputs = ["script.md"]
    expected_outputs = ["storyboard.md"]

    def run(self) -> bool:
        """Generate storyboard.md from script.md using LLM."""
        script_path = self.video_dir / "script.md"
        script_content = script_path.read_text()

        # Load scene planner template
        template_path = ROOT / "prompts" / "scene_planner.md"
        template = ""
        if template_path.exists():
            template = template_path.read_text()

        prompt = f"""Design the visual storyboard for the following video script.

Script:
{script_content}

Follow the scene planning format from the template:
{template}

For each scene, provide:
1. Visual Goal
2. Animation Sequence with timestamps
3. Duration
4. Manim Objects to use
5. Transitions

Output as markdown."""

        system_prompt = (
            "You are a visual director for educational YouTube animations. "
            "Design clear, engaging storyboards that keep viewers watching."
        )

        response = generate(prompt, system_prompt=system_prompt)

        output_path = self.video_dir / "storyboard.md"
        with open(output_path, "w") as f:
            f.write(response)

        logger.info(f"[storyboard] Saved: {output_path.name}")
        return True
