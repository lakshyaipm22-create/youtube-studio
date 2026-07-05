"""
YouTube Studio - Reusable Manim Library

This package contains the core reusable components for all channel videos:
- styles: Brand colors, fonts, timing constants
- base: StudioScene base class (inherit from this)
- intro: Branded intro animation
- outro: Branded outro animation

Usage:
    from studio.base import StudioScene
    from studio.styles import *

Only add new modules here after you've copied the same animation
into 3+ videos. Keep this minimal and intentional.
"""

from studio.styles import *
from studio.base import StudioScene
