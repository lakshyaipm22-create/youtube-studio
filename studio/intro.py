"""
YouTube Studio - Branded Intro Scene

Reusable intro animation for all videos.
Displays logo/brand mark + video title + subtle entrance animation.

Usage:
    # In your video's scenes.py:
    from studio.intro import IntroScene

    class Intro(IntroScene):
        TITLE = "What is Python?"
        SUBTITLE = "A Beginner's Guide"

    # Or use the intro helper inside another scene:
    from studio.intro import play_intro

    class MyScene(StudioScene):
        def construct(self):
            play_intro(self, title="What is Python?")
            # ... rest of scene
"""

from manim import *
from studio.base import StudioScene
from studio.styles import *


class IntroScene(StudioScene):
    """Branded intro scene. Override TITLE and SUBTITLE in subclass."""

    TITLE: str = "Video Title"
    SUBTITLE: str = ""
    DURATION: float = 4.0  # Total intro duration in seconds

    def construct(self):
        play_intro(self, title=self.TITLE, subtitle=self.SUBTITLE)
        self.wait(max(0, self.DURATION - 3.0))


def play_intro(scene: StudioScene, title: str, subtitle: str = ""):
    """Play the branded intro animation within any scene.

    Animation sequence:
    1. Brand accent line draws across center
    2. Title fades in above line
    3. Subtitle fades in below (if provided)
    4. Brief pause for viewer
    """
    # Accent line
    line = Line(LEFT * 3, RIGHT * 3, color=BRAND_PRIMARY, stroke_width=3)
    line.move_to(ORIGIN)

    # Title
    title_text = brand_text(title, font_size=FONT_SIZE_HERO, color=BRAND_LIGHT)
    title_text.next_to(line, UP, buff=0.5)

    # Build animation sequence
    scene.play(Create(line), run_time=FADE_SLOW)
    scene.pause_beat()
    scene.play(FadeIn(title_text, shift=UP * 0.3), run_time=FADE_NORMAL)

    # Subtitle (optional)
    if subtitle:
        sub_text = brand_text(subtitle, font_size=FONT_SIZE_SUBTITLE, color=BRAND_MUTED)
        sub_text.next_to(line, DOWN, buff=0.4)
        scene.play(FadeIn(sub_text, shift=DOWN * 0.2), run_time=FADE_NORMAL)

    scene.pause_medium()
