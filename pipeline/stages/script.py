"""
YouTube Studio - Script Stage

Takes research.yaml and generates script.md using the script_writer prompt template.
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
            research_data = yaml.safe_load(f)

        # Load prompt template
        template_path = ROOT / "prompts" / "script_writer.md"
        template = ""
        if template_path.exists():
            template = template_path.read_text()

        topic = research_data.get("topic", "Unknown Topic")
        hook_ideas = research_data.get("hook_ideas", [])
        key_facts = research_data.get("key_facts", [])
        misconceptions = research_data.get("misconceptions", [])
        analogies = research_data.get("analogies", [])

        prompt = f"""Write a YouTube video script based on the following research.

Topic: {topic}

Hook Ideas:
{_format_list(hook_ideas)}

Key Facts:
{_format_list(key_facts)}

Misconceptions to Address:
{_format_list(misconceptions)}

Analogies:
{_format_list(analogies)}

Follow the script format from the template:
{template}

Write the complete script in markdown. Include [VISUAL] directions and NARRATION text.
Use the hook ideas, facts, and analogies naturally.
Target length: 3-4 minutes of narration."""

        system_prompt = (
            "You are a YouTube script writer. Write engaging, educational scripts "
            "with clear narration and visual directions. Keep sentences short and natural."
        )

        response = generate(prompt, system_prompt=system_prompt)

        output_path = self.video_dir / "script.md"
        with open(output_path, "w") as f:
            f.write(response)

        logger.info(f"[script] Saved: {output_path.name}")
        return True


def _format_list(items: list) -> str:
    """Format a list of items as bullet points."""
    if not items:
        return "  (none)"
    return "\n".join(f"  - {item}" for item in items)
