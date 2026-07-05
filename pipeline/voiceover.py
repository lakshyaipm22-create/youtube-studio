"""
YouTube Studio - Voiceover Generation

Generate narration audio from a video's script.md using AI TTS.

Supports two backends:
- Kokoro-82M (local, Apache 2.0, best quality)
- Edge-TTS (cloud, free, zero setup, good fallback)

Usage:
    python pipeline/voiceover.py videos/001_what_is_python/script.md
    python pipeline/voiceover.py videos/001_what_is_python/script.md --engine edge
    python pipeline/voiceover.py videos/001_what_is_python/script.md --voice af_heart
    python pipeline/voiceover.py videos/001_what_is_python/script.md \\
        --voice en-US-AriaNeural --engine edge

Output:
    output/{video_name}/voiceover.wav
"""

import argparse
import asyncio
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "output"


def extract_narration(script_path: Path) -> str:
    """Extract narration text from script.md.

    Rules:
    - Ignores lines starting with # (headings)
    - Ignores lines starting with > (stage directions)
    - Ignores lines starting with [ (timing markers)
    - Strips empty lines, combines paragraphs
    """
    text_lines = []

    with open(script_path) as f:
        for line in f:
            line = line.strip()
            # Skip headings, directions, markers, empty lines
            if not line:
                continue
            if line.startswith("#"):
                continue
            if line.startswith(">"):
                continue
            if line.startswith("["):
                continue
            if line.startswith("---"):
                continue
            text_lines.append(line)

    return " ".join(text_lines)


def get_video_name(script_path: Path) -> str:
    """Extract video folder name from script path."""
    # script_path is like: videos/001_what_is_python/script.md
    return script_path.parent.name


def generate_with_kokoro(text: str, output_path: Path, voice: str = "af_heart"):
    """Generate voiceover using Kokoro-82M (local TTS)."""
    try:
        import kokoro
    except ImportError as err:
        print("❌ Kokoro not installed. Install with: pip install kokoro")
        print("   Or use --engine edge for Edge-TTS instead.")
        raise SystemExit(1) from err

    print(f"🎙️  Generating voiceover with Kokoro (voice: {voice})...")
    print(f"   Text length: {len(text)} characters")

    # Generate audio
    pipeline = kokoro.KPipeline(lang_code="a")  # 'a' for American English
    audio_segments = []

    for result in pipeline(text, voice=voice):
        if result.audio is not None:
            audio_segments.append(result.audio)

    if not audio_segments:
        print("❌ No audio generated. Check your script content.")
        raise SystemExit(1)

    # Concatenate and save
    import numpy as np
    import soundfile as sf

    full_audio = np.concatenate(audio_segments)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(output_path), full_audio, samplerate=24000)

    print(f"✅ Voiceover saved: {output_path.relative_to(ROOT)}")


def generate_with_edge_tts(text: str, output_path: Path, voice: str = "en-US-AriaNeural"):
    """Generate voiceover using Edge-TTS (cloud, free)."""
    try:
        import edge_tts
    except ImportError as err:
        print("❌ Edge-TTS not installed. Install with: pip install edge-tts")
        raise SystemExit(1) from err

    print(f"🎙️  Generating voiceover with Edge-TTS (voice: {voice})...")
    print(f"   Text length: {len(text)} characters")

    async def _generate():
        communicate = edge_tts.Communicate(text, voice)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        await communicate.save(str(output_path))

    asyncio.run(_generate())
    print(f"✅ Voiceover saved: {output_path.relative_to(ROOT)}")


def main():
    parser = argparse.ArgumentParser(description="Generate voiceover from script")
    parser.add_argument("script", help="Path to script.md")
    parser.add_argument(
        "--engine",
        choices=["kokoro", "edge"],
        default="kokoro",
        help="TTS engine (default: kokoro)",
    )
    parser.add_argument(
        "--voice",
        default=None,
        help="Voice name (default: af_heart for Kokoro, en-US-AriaNeural for Edge)",
    )

    args = parser.parse_args()
    script_path = Path(args.script).resolve()

    if not script_path.exists():
        print(f"❌ Script not found: {args.script}")
        raise SystemExit(1)

    # Extract narration text
    text = extract_narration(script_path)
    if not text.strip():
        print("❌ No narration text found in script. Make sure your script has content")
        print("   (lines not starting with #, >, [, or ---).")
        raise SystemExit(1)

    # Determine output path
    video_name = get_video_name(script_path)
    output_dir = OUTPUT_DIR / video_name
    output_path = output_dir / "voiceover.wav"

    # Generate based on engine choice
    if args.engine == "kokoro":
        voice = args.voice or "af_heart"
        generate_with_kokoro(text, output_path, voice=voice)
    else:
        voice = args.voice or "en-US-AriaNeural"
        # Edge-TTS outputs mp3 natively
        output_path = output_dir / "voiceover.mp3"
        generate_with_edge_tts(text, output_path, voice=voice)

    print(f"\n🎬 Next: make render v={video_name}")


if __name__ == "__main__":
    main()
