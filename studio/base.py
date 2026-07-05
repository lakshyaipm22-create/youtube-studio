"""
YouTube Studio - Base Scene Class

All video scenes should inherit from StudioScene.
This provides consistent background, setup, and common utilities.

Usage:
    from studio.base import StudioScene

    class MyScene(StudioScene):
        def construct(self):
            title = self.make_title("Hello World")
            self.play(FadeIn(title))
            self.pause_beat()
"""

from manim import *

from studio.styles import *


class StudioScene(Scene):
    """Base scene class for all channel videos.

    Provides:
    - Consistent dark background
    - Common utility methods
    - Standard animation helpers
    """

    def setup(self):
        """Set up the scene with brand defaults."""
        self.camera.background_color = BRAND_DARK

    # ================================================================
    # TEXT HELPERS
    # ================================================================

    def make_title(self, text: str, position=POS_TITLE, **kwargs) -> Text:
        """Create a positioned title."""
        title = brand_title(text, **kwargs)
        title.move_to(position)
        return title

    def make_subtitle(self, text: str, position=POS_SUBTITLE, **kwargs) -> Text:
        """Create a positioned subtitle."""
        subtitle = brand_text(text, font_size=FONT_SIZE_SUBTITLE, color=BRAND_MUTED, **kwargs)
        subtitle.move_to(position)
        return subtitle

    def make_body(self, text: str, position=POS_CENTER, **kwargs) -> Text:
        """Create positioned body text."""
        body = brand_text(text, **kwargs)
        body.move_to(position)
        return body

    # ================================================================
    # TIMING HELPERS
    # ================================================================

    def pause_beat(self):
        """Brief beat between animations."""
        self.wait(PAUSE_BEAT)

    def pause_short(self):
        """Short pause for reading."""
        self.wait(PAUSE_SHORT)

    def pause_medium(self):
        """Medium pause to let viewer absorb."""
        self.wait(PAUSE_MEDIUM)

    def pause_long(self):
        """Long pause for important content."""
        self.wait(PAUSE_LONG)

    # ================================================================
    # TRANSITION HELPERS
    # ================================================================

    def fade_out_all(self, run_time: float = FADE_NORMAL):
        """Fade out everything on screen."""
        if self.mobjects:
            self.play(FadeOut(*self.mobjects), run_time=run_time)

    def clear_scene(self):
        """Instantly remove all mobjects (no animation)."""
        self.clear()
        self.camera.background_color = BRAND_DARK

    def transition_to(self, *new_mobjects, run_time: float = FADE_NORMAL):
        """Fade out current content and fade in new content."""
        animations = []
        if self.mobjects:
            animations.append(FadeOut(*self.mobjects))
        self.play(*animations, run_time=run_time)
        if new_mobjects:
            self.play(FadeIn(*new_mobjects), run_time=run_time)

    # ================================================================
    # SVG HELPERS
    # ================================================================

    def load_svg(self, path: str, height: float = 2.0, **kwargs) -> SVGMobject:
        """Load an SVG from assets/svg/ with consistent sizing."""
        svg = SVGMobject(path, **kwargs)
        svg.set_height(height)
        return svg
