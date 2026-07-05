"""
YouTube Studio - Animation Plan Stage

Takes storyboard.md and generates animation_plan.yaml with technical
Manim object specs, timing, and SVG requirements.
"""

import logging

import yaml

from pipeline.llm import generate
from pipeline.stages.base import StageRunner

logger = logging.getLogger("pipeline")


class AnimationPlanStage(StageRunner):
    """Generate technical animation plan from storyboard."""

    name = "animation_plan"
    required_inputs = ["storyboard.md"]
    expected_outputs = ["animation_plan.yaml"]

    def run(self) -> bool:
        """Generate animation_plan.yaml from storyboard.md using LLM."""
        storyboard_path = self.video_dir / "storyboard.md"
        storyboard_content = storyboard_path.read_text()

        prompt = f"""Convert this storyboard into a technical animation plan in YAML format.

Storyboard:
{storyboard_content}

For each scene, specify:
- name: scene class name (PascalCase, valid Python identifier)
- duration: seconds (integer)
- objects: list of Manim objects with type, content/params, position, style
- animations: ordered list with action, target, and time offset

Output ONLY valid YAML with a top-level 'scenes' key. No markdown code fences."""

        system_prompt = (
            "You are a Manim animation engineer. Convert storyboards into precise "
            "technical animation plans. Use valid Manim class names and parameters."
        )

        response = generate(prompt, system_prompt=system_prompt)

        # Clean up response
        response = _clean_yaml_response(response)

        # Validate YAML
        try:
            yaml.safe_load(response)
        except yaml.YAMLError as e:
            logger.error(f"[animation_plan] LLM returned invalid YAML: {e}")
            return False

        output_path = self.video_dir / "animation_plan.yaml"
        with open(output_path, "w") as f:
            f.write(response)

        logger.info(f"[animation_plan] Saved: {output_path.name}")
        return True


def _clean_yaml_response(text: str) -> str:
    """Remove markdown code fences from LLM response."""
    lines = text.strip().splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]
    return "\n".join(lines) + "\n"
