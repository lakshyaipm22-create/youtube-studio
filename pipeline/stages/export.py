"""
YouTube Studio - Export Stage

Takes rendered scenes, voiceover, and subtitles to produce final.mp4.
Uses the existing pipeline/export.py logic. Includes duration validation
to ensure rendered video duration approximately matches voiceover duration.
"""

import logging
import shutil
import subprocess
from pathlib import Path

from pipeline.stages.base import StageRunner

logger = logging.getLogger("pipeline")

DURATION_TOLERANCE_SECONDS = 2.0


class ExportStage(StageRunner):
    """Assemble final video from rendered scenes and audio."""

    name = "export"
    required_inputs = []  # Checked dynamically
    expected_outputs = ["output/final.mp4"]

    def validate_input(self) -> bool:
        """Check that rendered MP4s exist in output/."""
        output_dir = self.video_dir / "output"
        if not output_dir.exists():
            logger.error("[export] Missing input: output/ directory")
            return False

        mp4_files = list(output_dir.rglob("*.mp4"))
        # Filter out any previous final.mp4
        mp4_files = [f for f in mp4_files if f.name != "final.mp4"]
        if not mp4_files:
            logger.error("[export] No rendered MP4 files found in output/")
            return False

        return True

    def run(self) -> bool:
        """Assemble final.mp4 from rendered scenes and audio."""
        from pipeline.export import combine_video_audio, concat_scenes, mix_audio

        output_dir = self.video_dir / "output"

        # Find rendered scene MP4s
        mp4_files = sorted(output_dir.rglob("*.mp4"))
        mp4_files = [f for f in mp4_files if f.name != "final.mp4" and "partial" not in f.name]

        if not mp4_files:
            logger.error("[export] No scene MP4 files to concatenate")
            return False

        logger.info(f"[export] Found {len(mp4_files)} scene file(s)")

        # Concatenate scenes
        merged_path = output_dir / "merged_video.mp4"
        if not concat_scenes(mp4_files, merged_path):
            logger.error("[export] Failed to concatenate scenes")
            return False

        # Find voiceover
        voiceover_path = None
        for ext in ["wav", "mp3"]:
            candidate = self.video_dir / "voice" / f"voiceover.{ext}"
            if candidate.exists():
                voiceover_path = candidate
                break

        final_path = output_dir / "final.mp4"

        if voiceover_path:
            # Mix audio (no background music for now)
            mixed_audio_path = output_dir / "mixed_audio.wav"
            mix_audio(voiceover_path, None, mixed_audio_path)

            # Find subtitles
            srt_path = self.video_dir / "subtitles" / "subtitles.srt"
            srt_for_burn = srt_path if srt_path.exists() else None

            # Combine video + audio
            if not combine_video_audio(merged_path, mixed_audio_path, final_path, srt_for_burn):
                logger.error("[export] Failed to combine video and audio")
                return False

            # Cleanup intermediate
            mixed_audio_path.unlink(missing_ok=True)
        else:
            # No audio, just use merged video
            shutil.copy2(merged_path, final_path)

        # Cleanup merged
        if merged_path.exists() and merged_path != final_path:
            merged_path.unlink(missing_ok=True)

        logger.info(f"[export] Final video: {final_path.name}")

        # Validate duration sync between video and voiceover
        self._validate_duration_sync(final_path, voiceover_path)

        return True

    def _validate_duration_sync(self, video_path: Path, voiceover_path: Path | None) -> None:
        """Check that rendered video duration approximately matches voiceover duration.

        Logs a warning if the difference exceeds the tolerance threshold.

        Args:
            video_path: Path to the final rendered video.
            voiceover_path: Path to the voiceover audio file, or None.
        """
        if voiceover_path is None:
            return

        video_duration = _get_media_duration(video_path)
        voice_duration = _get_media_duration(voiceover_path)

        if video_duration is None or voice_duration is None:
            logger.warning("[export] Could not determine media durations for sync validation")
            return

        diff = abs(video_duration - voice_duration)
        if diff > DURATION_TOLERANCE_SECONDS:
            logger.warning(
                f"[export] Duration mismatch: video={video_duration:.1f}s, "
                f"voice={voice_duration:.1f}s, diff={diff:.1f}s "
                f"(tolerance: {DURATION_TOLERANCE_SECONDS}s)"
            )
        else:
            logger.info(
                f"[export] Duration sync OK: video={video_duration:.1f}s, "
                f"voice={voice_duration:.1f}s, diff={diff:.1f}s"
            )


def _get_media_duration(file_path: Path) -> float | None:
    """Get the duration of a media file using ffprobe.

    Args:
        file_path: Path to a video or audio file.

    Returns:
        Duration in seconds, or None if ffprobe is unavailable or fails.
    """
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "quiet",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(file_path),
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0 and result.stdout.strip():
            return float(result.stdout.strip())
    except (FileNotFoundError, subprocess.TimeoutExpired, ValueError):
        pass
    return None
