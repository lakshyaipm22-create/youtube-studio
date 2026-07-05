"""
YouTube Studio - Subtitle Generation

Generate SRT subtitles from voiceover audio using faster-whisper.

Usage:
    python pipeline/subtitles.py output/001_what_is_python/voiceover.wav
    python pipeline/subtitles.py output/001_what_is_python/voiceover.mp3 --model medium

Output:
    output/{video_name}/subtitles.srt
"""

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "output"


def format_timestamp(seconds: float) -> str:
    """Convert seconds to SRT timestamp format (HH:MM:SS,mmm)."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def generate_subtitles(audio_path: Path, output_path: Path, model_size: str = "medium"):
    """Generate SRT subtitles from audio file."""
    try:
        from faster_whisper import WhisperModel
    except ImportError as err:
        print("❌ faster-whisper not installed. Install with: pip install faster-whisper")
        raise SystemExit(1) from err

    print(f"📝 Generating subtitles with faster-whisper ({model_size} model)...")
    print(f"   Audio: {audio_path.name}")

    # Load model (uses int8 for CPU efficiency)
    model = WhisperModel(model_size, compute_type="int8")

    # Transcribe
    segments, info = model.transcribe(str(audio_path), beam_size=5)

    print(f"   Language: {info.language} (confidence: {info.language_probability:.2f})")

    # Write SRT
    output_path.parent.mkdir(parents=True, exist_ok=True)
    subtitle_count = 0

    with open(output_path, "w", encoding="utf-8") as f:
        for _i, segment in enumerate(segments, 1):
            start_time = format_timestamp(segment.start)
            end_time = format_timestamp(segment.end)
            text = segment.text.strip()

            if text:  # Skip empty segments
                subtitle_count += 1
                f.write(f"{subtitle_count}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{text}\n\n")

    print(f"✅ Subtitles saved: {output_path.relative_to(ROOT)}")
    print(f"   Total segments: {subtitle_count}")

    return output_path


def main():
    parser = argparse.ArgumentParser(description="Generate subtitles from audio")
    parser.add_argument("audio", help="Path to voiceover audio file")
    parser.add_argument(
        "--model",
        default="medium",
        choices=["tiny", "base", "small", "medium", "large-v3"],
        help="Whisper model size (default: medium)",
    )

    args = parser.parse_args()
    audio_path = Path(args.audio).resolve()

    if not audio_path.exists():
        print(f"❌ Audio file not found: {args.audio}")
        raise SystemExit(1)

    # Output SRT next to the audio file
    output_path = audio_path.parent / "subtitles.srt"

    generate_subtitles(audio_path, output_path, model_size=args.model)

    video_name = audio_path.parent.name
    print(f"\n🎬 Next: make export v={video_name}")


if __name__ == "__main__":
    main()
