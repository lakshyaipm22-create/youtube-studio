"""
YouTube Studio - Render Stage

Takes scenes/scenes.py and renders Manim scenes to MP4 files
using the existing pipeline/render.py logic.
"""

import logging
import subprocess
import sys
from pathlib import Path

from pipeline.stages.base import StageRunner

logger = logging.getLogger("pipeline")

ROOT = Path(__file__).resolve().parent.parent.parent


class RenderStage(StageRunner):
    """Render Manim scenes to video files."""

    name = "render"
    required_inputs = ["scenes/scenes.py"]
    expected_outputs = []  # Dynamic: depends on number of scenes

    def run(self) -> bool:
        """Render scenes/scenes.py to output/ directory."""
        scenes_file = self.video_dir / "scenes" / "scenes.py"
        output_dir = self.video_dir / "output"
        output_dir.mkdir(parents=True, exist_ok=True)

        cmd = [
            sys.executable,
            "-m",
            "manim",
            "render",
            "-qh",
            "--media_dir",
            str(output_dir),
            "-a",
            str(scenes_file),
        ]

        logger.info(f"[render] Rendering scenes from: {scenes_file.name}")

        result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))

        if result.returncode != 0:
            logger.error(f"[render] Manim render failed:\n{result.stderr[-500:]}")
            return False

        logger.info("[render] All scenes rendered successfully")
        return True

    def validate_output(self) -> bool:
        """Check that at least one MP4 was rendered."""
        output_dir = self.video_dir / "output"
        if not output_dir.exists():
            logger.error("[render] No output/ directory created")
            return False

        mp4_files = list(output_dir.rglob("*.mp4"))
        if not mp4_files:
            logger.error("[render] No MP4 files found in output/")
            return False

        logger.info(f"[render] Found {len(mp4_files)} rendered file(s)")
        return True
