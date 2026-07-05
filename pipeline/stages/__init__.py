"""
YouTube Studio - Pipeline Stage Registry

Ordered list of all pipeline stages. Each stage is a module in pipeline/stages/
with a run() function that takes a video directory path.
"""

from pipeline.stages.animation_plan import AnimationPlanStage
from pipeline.stages.base import StageRunner
from pipeline.stages.export import ExportStage
from pipeline.stages.manim_code import ManimCodeStage
from pipeline.stages.render import RenderStage
from pipeline.stages.research import ResearchStage
from pipeline.stages.script import ScriptStage
from pipeline.stages.storyboard import StoryboardStage
from pipeline.stages.subtitles import SubtitlesStage
from pipeline.stages.voice import VoiceStage

# Ordered list of (stage_name, stage_class) tuples
STAGES: list[tuple[str, type[StageRunner]]] = [
    ("research", ResearchStage),
    ("script", ScriptStage),
    ("storyboard", StoryboardStage),
    ("animation_plan", AnimationPlanStage),
    ("manim_code", ManimCodeStage),
    ("voice", VoiceStage),
    ("subtitles", SubtitlesStage),
    ("render", RenderStage),
    ("export", ExportStage),
]

STAGE_NAMES: list[str] = [name for name, _ in STAGES]

__all__ = ["STAGES", "STAGE_NAMES", "StageRunner"]
