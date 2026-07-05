"""
YouTube Studio - Research Stage

Takes topic.yaml and generates research.yaml with key facts,
hook ideas, misconceptions, analogies, and sources.
"""

import logging

import yaml

from pipeline.llm import generate
from pipeline.stages.base import StageRunner

logger = logging.getLogger("pipeline")


class ResearchStage(StageRunner):
    """Generate research material from a topic."""

    name = "research"
    required_inputs = ["topic.yaml"]
    expected_outputs = ["research.yaml"]

    def run(self) -> bool:
        """Generate research.yaml from topic.yaml using LLM."""
        topic_path = self.video_dir / "topic.yaml"

        with open(topic_path) as f:
            topic_data = yaml.safe_load(f)

        topic = topic_data.get("topic", "Unknown Topic")
        tags = topic_data.get("tags", [])

        prompt = f"""Research the following topic for a 3-5 minute educational YouTube video.

Topic: {topic}
Tags: {", ".join(tags) if tags else "general education"}

Provide your research in YAML format with these fields:
- topic: the topic name
- hook_ideas: 2-3 attention-grabbing opening lines
- key_facts: 4-6 important facts to cover
- misconceptions: 2-3 common misconceptions to address
- analogies: 2-3 simple analogies to explain complex parts
- sources: 2-3 reference sources

Output ONLY valid YAML, no markdown code fences."""

        system_prompt = (
            "You are a research assistant for educational YouTube videos. "
            "Provide accurate, well-structured research in YAML format."
        )

        response = generate(prompt, system_prompt=system_prompt)

        # Clean up response (remove code fences if present)
        response = _clean_yaml_response(response)

        # Validate YAML
        try:
            yaml.safe_load(response)
        except yaml.YAMLError as e:
            logger.error(f"[research] LLM returned invalid YAML: {e}")
            return False

        output_path = self.video_dir / "research.yaml"
        with open(output_path, "w") as f:
            f.write(response)

        logger.info(f"[research] Saved: {output_path.name}")
        return True


def _clean_yaml_response(text: str) -> str:
    """Remove markdown code fences from LLM response."""
    lines = text.strip().splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]
    return "\n".join(lines) + "\n"
