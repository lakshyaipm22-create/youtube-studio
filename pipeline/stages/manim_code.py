"""
YouTube Studio - Manim Code Generation Stage

Takes animation_plan.yaml and generates scenes.py with Manim scene classes
that use the studio/ library (StudioScene, brand helpers, timing constants).
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

MANDATORY IMPORTS AND PATTERNS:

The file MUST start with these exact imports:
```python
from manim import *

from studio.base import StudioScene
from studio.styles import *
```

MANDATORY RULES:

1. Every scene class MUST inherit from StudioScene (not Scene):
   class MyScene(StudioScene):

2. Use brand helpers for ALL text:
   - brand_text("text") for body text
   - brand_title("text") for titles
   - self.make_title("text") for positioned titles
   - self.make_body("text") for positioned body text

3. Use timing constants for ALL animations:
   - run_time=FADE_NORMAL (0.5s) for standard transitions
   - run_time=FADE_FAST (0.3s) for quick transitions
   - run_time=FADE_SLOW (0.8s) for dramatic reveals
   - self.pause_beat() between animations
   - self.pause_medium() for viewer absorption
   - self.pause_short() for brief reading pauses

4. Use position constants:
   - POS_TITLE for title positioning
   - POS_CENTER for center content
   - POS_SUBTITLE for subtitles
   - POS_FOOTER for captions

5. Transitions between content:
   - self.fade_out_all() to clear everything
   - Use FadeIn, FadeOut, Write, Create, Transform, GrowArrow
   - NEVER use self.add() or self.remove() directly
   - Always animate entrances and exits

6. No static frame longer than 3 seconds:
   - Always have motion or transformation
   - Use self.wait() sparingly and only with short durations

7. Use brand colors:
   - BRAND_PRIMARY for highlights
   - BRAND_SECONDARY for accents
   - BRAND_LIGHT for text
   - BRAND_ACCENT for success/tips

Output ONLY the Python code. No markdown code fences. No explanations."""

        system_prompt = (
            "You are a Manim expert who writes production-quality animation code "
            "using the studio/ library. Generate clean, working Manim code "
            "that inherits from StudioScene and uses brand helpers and timing constants."
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
