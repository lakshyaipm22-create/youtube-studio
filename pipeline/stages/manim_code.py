"""
YouTube Studio - Manim Code Generation Stage

Takes animation_plan.yaml and generates scenes.py with Manim scene classes.
"""

import logging

from pipeline.llm import generate
from pipeline.stages.base import StageRunner

logger = logging.getLogger("pipeline")


class ManimCodeStage(StageRunner):
    """Generate Manim scenes.py from animation plan."""

    name = "manim_code"
    required_inputs = ["animation_plan.yaml"]
    expected_outputs = ["scenes/scenes.py"]

    def run(self) -> bool:
        """Generate scenes/scenes.py from animation_plan.yaml using LLM."""
        plan_path = self.video_dir / "animation_plan.yaml"

        with open(plan_path) as f:
            plan_content = f.read()

        prompt = f"""Generate a complete Manim Python file (scenes.py) from this animation plan.

Animation Plan:
{plan_content}

Requirements:
- Import from manim: from manim import *
- Each scene is a class inheriting from Scene
- Class names must match the scene names from the plan
- Each class has a construct(self) method
- Use proper Manim animations: FadeIn, FadeOut, Write, Create, Transform, etc.
- Use self.play() for animations and self.wait() for pauses
- Keep the code clean and well-commented
- Add a module docstring at the top

Output ONLY the Python code. No markdown code fences."""

        system_prompt = (
            "You are a Manim expert. Generate clean, working Manim code "
            "that produces smooth educational animations."
        )

        response = generate(prompt, system_prompt=system_prompt)

        # Clean up response (remove code fences if present)
        response = _clean_code_response(response)

        # Write to scenes directory
        scenes_dir = self.video_dir / "scenes"
        scenes_dir.mkdir(parents=True, exist_ok=True)

        output_path = scenes_dir / "scenes.py"
        with open(output_path, "w") as f:
            f.write(response)

        logger.info("[manim_code] Saved: scenes/scenes.py")
        return True


def _clean_code_response(text: str) -> str:
    """Remove markdown code fences from LLM response."""
    lines = text.strip().splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]
    return "\n".join(lines) + "\n"
