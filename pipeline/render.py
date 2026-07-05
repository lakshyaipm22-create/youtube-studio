"""
YouTube Studio - Scene Rendering

Render all Manim scenes for a video in the correct order.
Reads scene order from video.yaml and renders each class.

Usage:
    python pipeline/render.py 001_what_is_python
    python pipeline/render.py 001_what_is_python --quality low
    python pipeline/render.py 001_what_is_python --quality 4k
    python pipeline/render.py 001_what_is_python --scene Intro  # Single scene

Quality options:
    low   → 480p @ 15fps  (fast preview)
    medium → 720p @ 30fps (draft)
    high  → 1080p @ 60fps (production, default)
    4k    → 2160p @ 60fps (final)
"""

import argparse
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
VIDEOS_DIR = ROOT / "videos"
OUTPUT_DIR = ROOT / "output"

QUALITY_FLAGS = {
    "low": "-ql",
    "medium": "-qm",
    "high": "-qh",
    "4k": "-qk",
}


def get_scene_order(video_dir: Path) -> list[str]:
    """Read scene class names from video.yaml."""
    video_yaml = video_dir / "video.yaml"

    if not video_yaml.exists():
        print("⚠️  No video.yaml found. Rendering all scenes in file order.")
        return []

    with open(video_yaml) as f:
        config = yaml.safe_load(f) or {}

    return config.get("scenes", [])


def render_scene(video_dir: Path, scene_name: str, quality: str = "high") -> bool:
    """Render a single scene class."""
    scenes_file = video_dir / "scenes.py"
    quality_flag = QUALITY_FLAGS.get(quality, "-qh")
    video_name = video_dir.name

    # Output directory for this video
    output_dir = OUTPUT_DIR / video_name

    cmd = [
        sys.executable,
        "-m",
        "manim",
        "render",
        quality_flag,
        "--media_dir",
        str(output_dir),
        str(scenes_file),
        scene_name,
    ]

    print(f"   🎬 Rendering: {scene_name} ({quality})...")

    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))

    if result.returncode != 0:
        print(f"   ❌ Failed: {scene_name}")
        if result.stderr:
            # Show last few lines of error
            error_lines = result.stderr.strip().split("\n")[-5:]
            for line in error_lines:
                print(f"      {line}")
        return False

    print(f"   ✅ Done: {scene_name}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Render video scenes")
    parser.add_argument("video", help="Video folder name (e.g., 001_what_is_python)")
    parser.add_argument(
        "--quality",
        default="high",
        choices=["low", "medium", "high", "4k"],
        help="Render quality (default: high)",
    )
    parser.add_argument("--scene", default=None, help="Render a single scene by name")

    args = parser.parse_args()
    video_dir = VIDEOS_DIR / args.video

    if not video_dir.exists():
        print(f"❌ Video not found: {args.video}")
        available = [d.name for d in VIDEOS_DIR.iterdir() if d.is_dir() and d.name != "_template"]
        print(f"   Available: {available}")
        raise SystemExit(1)

    scenes_file = video_dir / "scenes.py"
    if not scenes_file.exists():
        print(f"❌ No scenes.py found in {args.video}/")
        raise SystemExit(1)

    print(f"\n🎬 Rendering: {args.video}")
    print(f"   Quality: {args.quality}")
    print()

    # Determine which scenes to render
    if args.scene:
        scenes = [args.scene]
    else:
        scenes = get_scene_order(video_dir)
        if not scenes:
            print("   ⚠️  No scenes listed in video.yaml. Rendering entire file.")
            # Render entire file without specifying scene name
            scenes = []

    # Render
    if scenes:
        successes = 0
        failures = 0
        for scene_name in scenes:
            if render_scene(video_dir, scene_name, quality=args.quality):
                successes += 1
            else:
                failures += 1

        print(f"\n📊 Results: {successes} rendered, {failures} failed")
    else:
        # Render all scenes in file
        quality_flag = QUALITY_FLAGS.get(args.quality, "-qh")
        output_dir = OUTPUT_DIR / args.video
        cmd = [
            sys.executable,
            "-m",
            "manim",
            "render",
            quality_flag,
            "--media_dir",
            str(output_dir),
            "-a",  # Render all scenes
            str(scenes_file),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))
        if result.returncode == 0:
            print("   ✅ All scenes rendered.")
        else:
            print("   ❌ Render failed.")
            if result.stderr:
                print(result.stderr[-500:])

    video_name = args.video
    print(f"\n🎬 Next: make export v={video_name}")


if __name__ == "__main__":
    main()
