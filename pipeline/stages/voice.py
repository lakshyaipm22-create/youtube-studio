"""
YouTube Studio - Voice Stage

Takes script.md and generates voiceover audio using the existing
pipeline/voiceover.py logic.
"""

import logging
from pathlib import Path

from pipeline.stages.base import StageRunner

logger = logging.getLogger("pipeline")

ROOT = Path(__file__).resolve().parent.parent.parent


class VoiceStage(StageRunner):
    """Generate voiceover audio from the script."""

    name = "voice"
    required_inputs = ["script.md"]
    expected_outputs = ["voice/voiceover.wav"]

    def run(self) -> bool:
        """Generate voice/voiceover.wav from script.md."""
        from pipeline.voiceover import extract_narration, generate_with_kokoro

        script_path = self.video_dir / "script.md"
        text = extract_narration(script_path)

        if not text.strip():
            logger.error("[voice] No narration text found in script.md")
            return False

        output_dir = self.video_dir / "voice"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "voiceover.wav"

        try:
            generate_with_kokoro(text, output_path)
        except SystemExit:
            # Kokoro not available, try edge-tts
            logger.info("[voice] Kokoro unavailable, trying Edge-TTS...")
            try:
                from pipeline.voiceover import generate_with_edge_tts

                output_path = output_dir / "voiceover.mp3"
                generate_with_edge_tts(text, output_path)
            except (SystemExit, Exception) as e:
                logger.error(f"[voice] Both TTS engines failed: {e}")
                return False
        except Exception as e:
            logger.error(f"[voice] TTS generation failed: {e}")
            return False

        logger.info(f"[voice] Saved: {output_path.name}")
        return True

    def validate_output(self) -> bool:
        """Check for either .wav or .mp3 output."""
        wav_path = self.video_dir / "voice" / "voiceover.wav"
        mp3_path = self.video_dir / "voice" / "voiceover.mp3"

        if wav_path.exists() or mp3_path.exists():
            return True

        logger.error("[voice] Missing expected output: voice/voiceover.wav or voice/voiceover.mp3")
        return False
