"""
YouTube Studio - New Video Scaffolding

Creates a new video folder from the _template with correct numbering.

Usage:
    python pipeline/new_video.py "What is Python?"
    python pipeline/new_video.py "Variables Explained" --series python-basics

This will:
1. Determine the next video number (e.g., 001, 002, ...)
2. Create videos/NNN_snake_case_title/
3. Copy all template files
4. Update video.yaml with the title and metadata
5. Print the path so you can start working immediately
"""

import argparse
import re
import shutil
from pathlib import Path

import yaml

# Project root (assumes script is run from repo root or via Makefile)
ROOT = Path(__file__).resolve().parent.parent
VIDEOS_DIR = ROOT / "videos"
TEMPLATE_DIR = VIDEOS_DIR / "_template"
CATALOG_FILE = ROOT / "catalog.yaml"


def slugify(title: str) -> str:
    """Convert title to snake_case slug."""
    slug = title.lower().strip()
    slug = re.sub(r"[^a-z0-9\s]", "", slug)
    slug = re.sub(r"\s+", "_", slug)
    return slug


def get_next_number() -> int:
    """Determine the next video number by scanning existing folders."""
    if not VIDEOS_DIR.exists():
        return 1

    existing_numbers = []
    for item in VIDEOS_DIR.iterdir():
        if item.is_dir() and item.name != "_template":
            match = re.match(r"^(\d+)_", item.name)
            if match:
                existing_numbers.append(int(match.group(1)))

    return max(existing_numbers, default=0) + 1


def create_video(title: str, series: str = "", tags: str = "") -> Path:
    """Create a new video folder from template."""
    number = get_next_number()
    slug = slugify(title)
    folder_name = f"{number:03d}_{slug}"
    video_dir = VIDEOS_DIR / folder_name

    if video_dir.exists():
        raise FileExistsError(f"Video folder already exists: {video_dir}")

    # Copy template
    shutil.copytree(TEMPLATE_DIR, video_dir)

    # Update video.yaml
    video_yaml_path = video_dir / "video.yaml"
    video_config = {
        "title": title,
        "number": number,
        "series": series or "",
        "status": "draft",
        "duration_target": "3-4 min",
        "tags": [t.strip() for t in tags.split(",")] if tags else [],
        "published": None,
        "youtube_url": None,
        "scenes": ["Intro", "Main", "Outro"],
    }

    with open(video_yaml_path, "w") as f:
        yaml.dump(video_config, f, default_flow_style=False, sort_keys=False)

    # Update catalog.yaml
    update_catalog(folder_name, video_config)

    # Create research directory (with .gitkeep to track empty dir)
    research_dir = video_dir / "research"
    research_dir.mkdir(exist_ok=True)
    (research_dir / ".gitkeep").touch()

    return video_dir


def update_catalog(folder_name: str, config: dict):
    """Add the new video entry to catalog.yaml."""
    catalog = {"videos": {}}

    if CATALOG_FILE.exists():
        with open(CATALOG_FILE) as f:
            catalog = yaml.safe_load(f) or {"videos": {}}

    if catalog.get("videos") is None:
        catalog["videos"] = {}

    catalog["videos"][folder_name] = {
        "title": config["title"],
        "series": config["series"],
        "status": config["status"],
        "duration_target": config["duration_target"],
        "tags": config["tags"],
    }

    with open(CATALOG_FILE, "w") as f:
        yaml.dump(catalog, f, default_flow_style=False, sort_keys=False)


def main():
    parser = argparse.ArgumentParser(description="Create a new video folder")
    parser.add_argument("title", help="Video title (e.g., 'What is Python?')")
    parser.add_argument("--series", default="", help="Series name (e.g., python-basics)")
    parser.add_argument("--tags", default="", help="Comma-separated tags")

    args = parser.parse_args()
    video_dir = create_video(args.title, series=args.series, tags=args.tags)

    print(f"\n✅ Created: {video_dir.relative_to(ROOT)}")
    print(f"   Title:  {args.title}")
    print(f"   Number: {video_dir.name.split('_')[0]}")
    print("\n📝 Next steps:")
    print(f"   1. Write your script:     {video_dir.relative_to(ROOT)}/script.md")
    print(f"   2. Plan your scenes:      {video_dir.relative_to(ROOT)}/storyboard.md")
    print(f"   3. Code your animations:  {video_dir.relative_to(ROOT)}/scenes.py")
    print(f"   4. Produce:               make produce v={video_dir.name}")
    print()


if __name__ == "__main__":
    main()
