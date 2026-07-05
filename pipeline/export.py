"""
YouTube Studio - Final Video Export

Assembles the final YouTube-ready video:
1. Concatenates rendered scene MP4s
2. Mixes voiceover + background music
3. Combines video + mixed audio
4. Optionally burns subtitles
5. Outputs H.264/AAC MP4 optimized for YouTube

Usage:
    python pipeline/export.py 001_what_is_python
    python pipeline/export.py 001_what_is_python --burn-subs
    python pipeline/export.py 001_what_is_python --music assets/music/chill_bg.mp3
    python pipeline/export.py 001_what_is_python --no-music

Output:
    output/{video_name}/final.mp4
"""

import argparse
import glob
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "output"
ASSETS_DIR = ROOT / "assets"


def find_rendered_scenes(video_name: str) -> list[Path]:
    """Find all rendered MP4 scene files for a video."""
    video_output = OUTPUT_DIR / video_name
    # Manim outputs to media/videos/ subdirectories
    patterns = [
        str(video_output / "**" / "*.mp4"),
        str(video_output / "*.mp4"),
    ]
    mp4_files = []
    for pattern in patterns:
        mp4_files.extend(glob.glob(pattern, recursive=True))

    # Filter out any 'final' or 'partial' exports
    scene_files = [Path(f) for f in sorted(mp4_files) if "final" not in f and "partial" not in f]
    return scene_files


def concat_scenes(scene_files: list[Path], output_path: Path) -> bool:
    """Concatenate scene MP4s using FFmpeg."""
    if len(scene_files) == 1:
        # Single scene — just copy
        import shutil

        shutil.copy2(scene_files[0], output_path)
        return True

    # Create concat file list
    concat_list = output_path.parent / "concat_list.txt"
    with open(concat_list, "w") as f:
        for scene_file in scene_files:
            f.write(f"file '{scene_file}'\n")

    cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat_list),
        "-c",
        "copy",
        str(output_path),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    concat_list.unlink(missing_ok=True)  # Clean up

    return result.returncode == 0


def mix_audio(
    voiceover_path: Path, music_path: Path | None, output_path: Path, music_volume: float = 0.12
) -> bool:
    """Mix voiceover with background music using FFmpeg."""
    if music_path is None or not music_path.exists():
        # No music — just copy voiceover
        import shutil

        shutil.copy2(voiceover_path, output_path)
        return True

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(voiceover_path),
        "-i",
        str(music_path),
        "-filter_complex",
        f"[1:a]volume={music_volume},aloop=loop=-1:size=2e+09[bg];"
        f"[bg]atrim=0=duration=9999[bgt];"
        f"[0:a][bgt]amix=inputs=2:duration=first:dropout_transition=2",
        "-c:a",
        "pcm_s16le",
        str(output_path),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0


def combine_video_audio(
    video_path: Path, audio_path: Path, output_path: Path, srt_path: Path | None = None
) -> bool:
    """Combine video with audio, optionally burning subtitles."""
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(video_path),
        "-i",
        str(audio_path),
    ]

    # Video filter (burn subtitles if requested)
    if srt_path and srt_path.exists():
        # Escape path for FFmpeg subtitle filter
        srt_escaped = str(srt_path).replace("\\", "/").replace(":", "\\:")
        cmd.extend(["-vf", f"subtitles='{srt_escaped}':force_style='FontSize=22,FontName=Inter'"])
        cmd.extend(["-c:v", "libx264", "-preset", "slow", "-crf", "18"])
    else:
        cmd.extend(["-c:v", "copy"])

    cmd.extend(
        [
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-ar",
            "48000",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            str(output_path),
        ]
    )

    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(description="Export final YouTube-ready video")
    parser.add_argument("video", help="Video folder name (e.g., 001_what_is_python)")
    parser.add_argument("--music", default=None, help="Path to background music file")
    parser.add_argument("--no-music", action="store_true", help="Skip background music")
    parser.add_argument("--burn-subs", action="store_true", help="Burn subtitles into video")
    parser.add_argument(
        "--music-volume",
        type=float,
        default=0.12,
        help="Background music volume (0.0-1.0, default: 0.12)",
    )

    args = parser.parse_args()
    video_name = args.video
    video_output = OUTPUT_DIR / video_name
    video_output.mkdir(parents=True, exist_ok=True)

    print(f"\n🎬 Exporting: {video_name}")
    print()

    # Step 1: Find rendered scenes
    scene_files = find_rendered_scenes(video_name)
    if not scene_files:
        print("❌ No rendered scene files found.")
        print(f"   Run first: make render v={video_name}")
        raise SystemExit(1)

    print(f"   📹 Found {len(scene_files)} scene(s)")

    # Step 2: Concatenate scenes
    merged_video = video_output / "merged_video.mp4"
    print("   🔗 Concatenating scenes...")
    if not concat_scenes(scene_files, merged_video):
        print("   ❌ Failed to concatenate scenes.")
        raise SystemExit(1)

    # Step 3: Mix audio (if voiceover exists)
    voiceover = None
    for ext in ["wav", "mp3"]:
        candidate = video_output / f"voiceover.{ext}"
        if candidate.exists():
            voiceover = candidate
            break

    mixed_audio = None
    if voiceover:
        print("   🎵 Mixing audio...")
        mixed_audio = video_output / "mixed_audio.wav"
        music_path = Path(args.music) if args.music else None
        if args.no_music:
            music_path = None
        mix_audio(voiceover, music_path, mixed_audio, args.music_volume)
    else:
        print("   ⚠️  No voiceover found. Exporting video-only.")

    # Step 4: Combine video + audio
    final_output = video_output / "final.mp4"
    srt_path = video_output / "subtitles.srt" if args.burn_subs else None

    if mixed_audio:
        print("   🎬 Combining video + audio...")
        if not combine_video_audio(merged_video, mixed_audio, final_output, srt_path):
            print("   ❌ Failed to combine video and audio.")
            raise SystemExit(1)
    else:
        # No audio — just copy merged video
        import shutil

        shutil.copy2(merged_video, final_output)

    # Cleanup intermediate files
    if merged_video.exists() and merged_video != final_output:
        merged_video.unlink()
    if mixed_audio and mixed_audio.exists():
        mixed_audio.unlink()

    print(f"\n✅ Final video: output/{video_name}/final.mp4")
    print("   Ready for YouTube upload!")
    print()


if __name__ == "__main__":
    main()
