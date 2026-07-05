"""
Video: {Video Title}

Scenes for this video. Each class is one scene segment.
Render order is defined in video.yaml.

Usage:
    make preview v={video_folder} s=Intro
    make render v={video_folder}
"""

from manim import *
from studio.base import StudioScene
from studio.intro import IntroScene
from studio.outro import OutroScene
from studio.styles import *


class Intro(IntroScene):
    TITLE = "Video Title"
    SUBTITLE = ""


class Main(StudioScene):
    def construct(self):
        # TODO: Design your animation here
        # Refer to storyboard.md for the visual plan
        title = self.make_title("Main Content")
        self.play(FadeIn(title))
        self.pause_medium()
        self.fade_out_all()


class Outro(OutroScene):
    NEXT_VIDEO = ""
