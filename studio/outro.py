"""
YouTube Studio - Branded Outro Scene

Reusable outro animation for all videos.
Subscribe CTA + channel branding + smooth exit.

Usage:
    # In your video's scenes.py:
    from studio.outro import OutroScene

    class Outro(OutroScene):
        NEXT_VIDEO = "Variables in Python"

    # Or use the outro helper inside another scene:
    from studio.outro import play_outro

    class MyScene(StudioScene):
        def construct(self):
            # ... main content ...
            play_outro(self, next_video="Variables in Python")
"""

from manim import *

from studio.base import StudioScene
from studio.styles import *


class OutroScene(StudioScene):
    """Branded outro scene. Override NEXT_VIDEO in subclass."""

    NEXT_VIDEO: str = ""
    DURATION: float = 5.0

    def construct(self):
        play_outro(self, next_video=self.NEXT_VIDEO)
        self.wait(max(0, self.DURATION - 4.0))


def play_outro(scene: StudioScene, next_video: str = ""):
    """Play the branded outro animation.

    Animation sequence:
    1. Fade out current content
    2. "Thanks for watching" text appears
    3. Subscribe CTA with accent
    4. Next video teaser (if provided)
    5. Fade to dark
    """
    scene.fade_out_all()
    scene.pause_beat()

    # Thanks message
    thanks = brand_text("Thanks for watching!", font_size=FONT_SIZE_TITLE, color=BRAND_LIGHT)
    thanks.move_to(UP * 1.0)

    # Subscribe CTA
    cta = brand_text("Subscribe for more", font_size=FONT_SIZE_BODY, color=BRAND_PRIMARY)
    cta.move_to(ORIGIN)

    scene.play(FadeIn(thanks, shift=UP * 0.3), run_time=FADE_NORMAL)
    scene.pause_beat()
    scene.play(FadeIn(cta, shift=UP * 0.2), run_time=FADE_NORMAL)

    # Next video teaser
    if next_video:
        next_text = brand_text(
            f"Next: {next_video}", font_size=FONT_SIZE_CAPTION, color=BRAND_MUTED
        )
        next_text.move_to(DOWN * 1.5)
        scene.play(FadeIn(next_text, shift=UP * 0.2), run_time=FADE_NORMAL)

    scene.pause_long()
    scene.fade_out_all()
