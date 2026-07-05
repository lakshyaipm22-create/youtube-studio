"""
YouTube Studio - Storyboard Stage

Takes script.md and generates storyboard.md with detailed per-scene
visual plans: entrances, exits, transforms, timing, and SVG requirements.
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

        prompt = f"""Design a detailed visual storyboard for the following video script.

Script:
---
{script_content}
---

STORYBOARD RULES:

1. For each scene segment, define what appears on screen every 3-5 seconds.
   - No static frame may last longer than 3 seconds.
   - Something must always be entering, moving, transforming, or exiting.

2. For each visual beat, specify:
   - ENTRANCE: How does it appear? (FadeIn, Write, Create, GrowFromCenter, etc.)
   - ON SCREEN: What transforms happen? (scale, recolor, move, morph)
   - EXIT: How does it leave? (FadeOut, Uncreate, shrink, slide off)

3. Specify SVGs or illustrations needed:
   - What objects need custom SVG artwork?
   - What can be built from primitives (arrows, circles, text)?

4. Plan camera movement:
   - When to zoom in (draw attention to detail)
   - When to zoom out (show big picture)
   - When to pan (follow a sequence)
   - Default: static (only move with purpose)

5. Ensure visual variety:
   - Never show text alone without an accompanying visual
   - Alternate between diagrams, comparisons, transformations, and reveals
   - Build complexity gradually within each scene

FORMAT for each scene:

## Scene N: [Name]
Duration: Xs

Visual Goal: [What the viewer should understand from this scene]

| Time | Element | Animation | Notes |
|------|---------|-----------|-------|
| 0.0s | ... | Entrance: FadeIn | ... |
| 3.0s | ... | Transform: scale up | ... |
| 5.0s | ... | Exit: FadeOut | ... |

SVGs Needed: [list any custom illustrations]
Camera: [static / zoom in / pan left / etc.]
Transition to Next: [how this scene ends and connects to the next]

Create the storyboard now. Be specific and practical."""

        system_prompt = (
            "You are a visual director for educational YouTube animations. "
            "Design storyboards where every second has purpose and motion. "
            "No frame stays static for more than 3 seconds. Think like an animator."
        )

        response = generate(prompt, system_prompt=system_prompt)

        output_path = self.video_dir / "storyboard.md"
        with open(output_path, "w") as f:
            f.write(response)

        logger.info(f"[storyboard] Saved: {output_path.name}")
        return True
