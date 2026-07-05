"""
YouTube Studio - Visual Style Constants

Single source of truth for all visual styling across the channel.
Every scene imports from here. Change once, update everywhere.

Usage:
    from studio.styles import *
"""

from manim import *

# ============================================================
# BRAND COLORS
# ============================================================
BRAND_PRIMARY = "#6C63FF"  # Main brand purple
BRAND_SECONDARY = "#FF6584"  # Accent pink/coral
BRAND_DARK = "#1A1A2E"  # Background dark blue
BRAND_LIGHT = "#F5F5F5"  # Text light
BRAND_ACCENT = "#00D9A6"  # Green accent (tips, success)
BRAND_WARNING = "#FFB347"  # Orange (warnings)
BRAND_ERROR = "#FF4444"  # Red (errors, important)
BRAND_MUTED = "#8892B0"  # Muted text, secondary info

# ============================================================
# TYPOGRAPHY
# ============================================================
FONT_PRIMARY = "Inter"
FONT_CODE = "JetBrains Mono"

FONT_SIZE_HERO = 56  # Main title / hero text
FONT_SIZE_TITLE = 44  # Section titles
FONT_SIZE_SUBTITLE = 36  # Subtitles
FONT_SIZE_BODY = 28  # Body text, bullet points
FONT_SIZE_CODE = 22  # Code blocks
FONT_SIZE_CAPTION = 18  # Small captions, labels
FONT_SIZE_TINY = 14  # Footnotes

# ============================================================
# ANIMATION TIMING
# ============================================================
FADE_FAST = 0.3  # Quick transitions
FADE_NORMAL = 0.5  # Standard fade in/out
FADE_SLOW = 0.8  # Deliberate, dramatic reveals
WRITE_SPEED = 0.7  # Text write animation speed
PAUSE_BEAT = 0.3  # Brief beat between animations
PAUSE_SHORT = 0.5  # Short pause for reading
PAUSE_MEDIUM = 1.0  # Medium pause (let viewer absorb)
PAUSE_LONG = 2.0  # Long pause (important content)
STAGGER_DELAY = 0.2  # Delay between staggered items

# ============================================================
# LAYOUT
# ============================================================
SAFE_MARGIN = 0.5  # Edge margin (keep content visible)
CONTENT_WIDTH = 12.0  # Usable width
CONTENT_HEIGHT = 7.0  # Usable height

# Standard positions
POS_TITLE = UP * 3.0  # Title position
POS_SUBTITLE = UP * 2.2  # Subtitle position
POS_CENTER = ORIGIN  # Center of screen
POS_FOOTER = DOWN * 3.5  # Footer / caption position
POS_LEFT = LEFT * 4.0  # Left panel
POS_RIGHT = RIGHT * 4.0  # Right panel

# ============================================================
# HELPERS
# ============================================================


def brand_text(
    text: str, font_size: int = FONT_SIZE_BODY, color: str = BRAND_LIGHT, **kwargs
) -> Text:
    """Create text with brand styling."""
    return Text(text, font=FONT_PRIMARY, font_size=font_size, color=color, **kwargs)


def brand_title(text: str, **kwargs) -> Text:
    """Create a title with brand styling."""
    return brand_text(text, font_size=FONT_SIZE_TITLE, **kwargs)


def brand_code(code: str, language: str = "python", **kwargs) -> Code:
    """Create a code block with brand styling."""
    return Code(
        code=code,
        tab_width=4,
        language=language,
        font=FONT_CODE,
        font_size=FONT_SIZE_CODE,
        background="rectangle",
        background_stroke_color=BRAND_PRIMARY,
        background_stroke_width=1,
        **kwargs,
    )
