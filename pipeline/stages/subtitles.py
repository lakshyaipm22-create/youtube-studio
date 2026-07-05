"""
YouTube Studio - Subtitles Stage

Takes voiceover audio and generates subtitles using the existing
pipeline/subtitles.py logic.
"""

import logging

from pipeline.stages.base import StageRunner

logger = logging.getLogger("pipeline")


class SubtitlesStage(StageRunner):
    """Generate subtitles from voiceover audio."""

    name = "subtitles"
    required_inputs = []  # Checked dynamically in validate_input
    expected_outputs = ["subtitles/subtitles.srt"]

    def validate_input(self) -> bool:
        """Check that voiceover audio exists (either .wav or .mp3)."""
        wav_path = self.video_dir / "voice" / "voiceover.wav"
        mp3_path = self.video_dir / "voice" / "voiceover.mp3"

        if wav_path.exists() or mp3_path.exists():
            return True

        logger.error("[subtitles] Missing input: voice/voiceover.wav or voice/voiceover.mp3")
        return False

    def run(self) -> bool:
        """Generate subtitles/subtitles.srt from voiceover audio."""
        from pipeline.subtitles import generate_subtitles

        # Find voiceover file
        audio_path = self.video_dir / "voice" / "voiceover.wav"
        if not audio_path.exists():
            audio_path = self.video_dir / "voice" / "voiceover.mp3"

        output_dir = self.video_dir / "subtitles"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "subtitles.srt"

        try:
            generate_subtitles(audio_path, output_path)
        except (SystemExit, Exception) as e:
            logger.error(f"[subtitles] Generation failed: {e}")
            return False

        logger.info(f"[subtitles] Saved: {output_path.name}")
        return True
