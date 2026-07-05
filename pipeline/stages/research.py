"""
YouTube Studio - Research Stage

Takes topic.yaml and generates research.yaml with YouTube-optimized
research: hooks, surprising facts, misconceptions, analogies, and thumbnail ideas.
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
        duration = topic_data.get("duration_target", "3-4 min")

        prompt = f"""Research the following topic for a {duration} educational YouTube video.

Topic: {topic}
Tags: {", ".join(tags) if tags else "general education"}

Your job is to find everything needed to make this video IRRESISTIBLE to click and
IMPOSSIBLE to stop watching. Think like a top YouTube creator, not a textbook author.

Provide your research as clean YAML with these exact fields:

topic: "{topic}"

hook_ideas:
  # 3 opening lines that create a CURIOSITY GAP.
  # Each must make the viewer NEED to know the answer.
  # Never start with "Hello everyone" or "In this video".
  # Use: surprising facts, impossible questions, shocking comparisons.

surprising_facts:
  # 4-5 facts that make people say "Wait... really?"
  # These are retention anchors - spread throughout the video.
  # Include specific numbers, counterintuitive truths, mind-blowing comparisons.

misconceptions:
  # 2-3 things most people believe that are WRONG about this topic.
  # Debunking misconceptions is one of the strongest retention tools.
  # Frame as "most people think X, but actually Y".

analogies:
  # 3 simple analogies a 16-year-old would immediately understand.
  # Use everyday experiences (car window, kitchen, sports, phone).
  # Each analogy must make a complex idea feel obvious.

key_facts:
  # 5-6 core facts that form the educational backbone.
  # Order them from most engaging to most technical.
  # Each fact should be animatable (can be shown visually).

thumbnail_idea:
  # ONE powerful visual concept for the thumbnail.
  # Must be simple, high-contrast, and trigger curiosity.
  # Describe what the viewer sees (not abstract concepts).

sources:
  # 2-3 authoritative references for accuracy.

Output ONLY valid YAML. No markdown code fences. No extra commentary."""

        system_prompt = (
            "You are a research assistant for educational YouTube videos. "
            "Your research optimizes for viewer curiosity, retention, and shareability. "
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
