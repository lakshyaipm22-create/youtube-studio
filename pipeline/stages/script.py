"""
YouTube Studio - Script Stage

Takes research.yaml and generates script.md following the YouTube strategy rules:
hook first, conversational tone, visual directions, curiosity loops.
"""

import logging
from pathlib import Path

import yaml

from pipeline.llm import generate
from pipeline.stages.base import StageRunner

logger = logging.getLogger("pipeline")

ROOT = Path(__file__).resolve().parent.parent.parent


class ScriptStage(StageRunner):
    """Generate a narration script from research."""

    name = "script"
    required_inputs = ["research.yaml"]
    expected_outputs = ["script.md"]

    def run(self) -> bool:
        """Generate script.md from research.yaml using LLM."""
        research_path = self.video_dir / "research.yaml"

        with open(research_path) as f:
            research_content = f.read()

        with open(research_path) as f:
            research_data = yaml.safe_load(f)

        topic = research_data.get("topic", "Unknown Topic")

        prompt = f"""Write a YouTube video script for: "{topic}"

Here is the complete research to work from:

---
{research_content}
---

SCRIPT RULES (follow ALL of these):

1. HOOK (first 5-10 seconds):
   - Open with a surprising fact, shocking comparison, or impossible question.
   - NEVER start with "Hello everyone", "Today we are going to", or "In this video".
   - The viewer must immediately NEED to know the answer.

2. TONE:
   - Conversational. Like explaining to a curious friend.
   - Short sentences. Simple words. No jargon without immediate explanation.
   - Natural humor where it fits (funny comparisons, mild exaggeration).
   - No filler words or phrases. Every sentence earns its place.

3. VISUAL DIRECTIONS:
   - Every 2-3 sentences, include a [VISUAL: ...] direction.
   - Each [VISUAL] must describe what appears on screen and how it moves.
   - Every sentence must be animatable. If you cannot picture it, rewrite it.

4. STRUCTURE:
   - Use curiosity loops: hint at something coming, deliver later.
   - Alternate between explanations, examples, rhetorical questions, and surprises.
   - Build from simple to complex.
   - Debunk at least one misconception.

5. LENGTH:
   - Target 500-700 words of narration (3-4 minutes when spoken).
   - Keep paragraphs to 2-3 sentences max.

6. ENDING:
   - Brief recap of the key insight (1-2 sentences).
   - Call to action: subscribe, comment, or question for next video.
   - End on a memorable line or callback to the hook.

FORMAT:
- Use markdown with # headers for scene breaks.
- [VISUAL: description] on its own line before the narration it accompanies.
- Write narration as plain text (what the voice says).

Write the complete script now."""

        system_prompt = (
            "You are a YouTube script writer who creates viral educational content. "
            "Write engaging, visual, punchy scripts with short sentences and natural humor. "
            "Every script must hook in the first 5 seconds and keep viewers watching."
        )

        response = generate(prompt, system_prompt=system_prompt)

        output_path = self.video_dir / "script.md"
        with open(output_path, "w") as f:
            f.write(response)

        logger.info(f"[script] Saved: {output_path.name}")
        return True
