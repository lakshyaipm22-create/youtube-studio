"""Shared test fixtures for the YouTube Studio pipeline."""

from pathlib import Path

import pytest
import yaml


@pytest.fixture
def video_dir(tmp_path: Path) -> Path:
    """Create a temporary video directory with topic.yaml and status.yaml."""
    topic_data = {
        "topic": "Why Airplanes Fly",
        "created_at": "2024-01-01T00:00:00+00:00",
        "tags": ["physics", "aviation"],
        "duration_target": "3-5 min",
    }
    topic_path = tmp_path / "topic.yaml"
    with open(topic_path, "w") as f:
        yaml.dump(topic_data, f, default_flow_style=False, sort_keys=False)

    status_data = {"stages": []}
    status_path = tmp_path / "status.yaml"
    with open(status_path, "w") as f:
        yaml.dump(status_data, f, default_flow_style=False, sort_keys=False)

    return tmp_path


@pytest.fixture
def video_dir_with_research(video_dir: Path) -> Path:
    """Video directory that also has research.yaml (ready for script stage)."""
    research_data = {
        "topic": "Why Airplanes Fly",
        "hook_ideas": [
            "Did you know planes actually push air DOWN to stay up?",
            "What if everything you learned about lift is wrong?",
        ],
        "key_facts": [
            "Wings generate lift by deflecting air downward",
            "Bernoulli's principle only tells part of the story",
            "Angle of attack is the primary lift variable",
            "Planes can fly upside down, disproving simple Bernoulli",
        ],
        "misconceptions": [
            "Air moves faster over the top because the path is longer",
            "Bernoulli's principle alone explains all lift",
        ],
        "analogies": [
            "Think of a wing like your hand out a car window",
            "Lift is like a ski jump pushing air one way and you another",
        ],
        "sources": [
            "NASA Glenn Research Center - Theories of Lift",
            "Feynman Lectures on Physics Vol. II",
        ],
    }
    research_path = video_dir / "research.yaml"
    with open(research_path, "w") as f:
        yaml.dump(research_data, f, default_flow_style=False, sort_keys=False)

    return video_dir


@pytest.fixture
def video_dir_with_script(video_dir_with_research: Path) -> Path:
    """Video directory that also has script.md (ready for storyboard stage)."""
    script_content = """# Scene 1: Hook
[VISUAL: Airplane flying through clouds]
Have you ever looked up at a massive airplane and wondered how it stays in the air?

# Scene 2: Introduction
[VISUAL: Title card - Why Airplanes Fly]
Today we are going to bust some myths about how flight actually works.

# Scene 3: Core Concept
[VISUAL: Wing cross-section with airflow arrows]
The real reason planes fly is surprisingly simple. It is all about pushing air down.

# Scene 4: Example
[VISUAL: Hand out car window demonstration]
Think of sticking your hand out of a car window at an angle.

# Scene 5: Recap
[VISUAL: Summary diagram]
So remember: angle of attack, not Bernoulli alone, is what keeps planes up.

# Scene 6: Outro
[VISUAL: Subscribe animation]
If this changed how you think about flight, hit subscribe.
"""
    script_path = video_dir_with_research / "script.md"
    script_path.write_text(script_content)

    return video_dir_with_research


@pytest.fixture
def video_dir_with_storyboard(video_dir_with_script: Path) -> Path:
    """Video directory that also has storyboard.md (ready for animation_plan stage)."""
    storyboard_content = """## Scene 1: Hook
Duration: 10s

Visual Goal: Grab attention with airplane visual

Animation Sequence:
1. [0.0s] Airplane SVG flies across screen
2. [3.0s] Question text fades in
3. [7.0s] Transition to title

Manim Objects: SVGMobject, Text
Transition: Fade

## Scene 2: Core Concept
Duration: 40s

Visual Goal: Show airflow over a wing

Animation Sequence:
1. [0.0s] Wing cross-section draws in
2. [5.0s] Arrows show airflow direction
3. [15.0s] Angle of attack label appears
4. [25.0s] Force vectors animate

Manim Objects: SVGMobject, Arrow, Text, VGroup
Transition: Slide left
"""
    storyboard_path = video_dir_with_script / "storyboard.md"
    storyboard_path.write_text(storyboard_content)

    return video_dir_with_script


@pytest.fixture
def video_dir_with_animation_plan(video_dir_with_storyboard: Path) -> Path:
    """Video directory that also has animation_plan.yaml (ready for manim_code stage)."""
    plan_data = {
        "scenes": [
            {
                "name": "Hook",
                "duration": 10,
                "objects": [
                    {
                        "type": "Text",
                        "content": "How do planes fly?",
                        "position": "center",
                        "font_size": 48,
                    }
                ],
                "animations": [
                    {"action": "FadeIn", "target": "text_0", "time": 0.0},
                    {"action": "FadeOut", "target": "all", "time": 8.0},
                ],
            },
            {
                "name": "CoreConcept",
                "duration": 40,
                "objects": [
                    {
                        "type": "Text",
                        "content": "Angle of Attack",
                        "position": "top",
                        "font_size": 36,
                    },
                    {
                        "type": "Arrow",
                        "start": "left",
                        "end": "right",
                    },
                ],
                "animations": [
                    {"action": "Write", "target": "text_0", "time": 0.0},
                    {"action": "GrowArrow", "target": "arrow_0", "time": 5.0},
                ],
            },
        ]
    }
    plan_path = video_dir_with_storyboard / "animation_plan.yaml"
    with open(plan_path, "w") as f:
        yaml.dump(plan_data, f, default_flow_style=False, sort_keys=False)

    return video_dir_with_storyboard
