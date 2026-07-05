"""
YouTube Studio - Production Pipeline CLI

Main entry point for producing videos from topic to final export.

Usage:
    python produce.py "Why Airplanes Don't Fall"       # Full pipeline
    python produce.py --from script                     # Resume from script stage
    python produce.py --only voice                      # Run only voice stage
    python produce.py --from script --video videos/001_why_airplanes_dont_fall
    python produce.py --list-stages                     # Show available stages
"""

import argparse
import logging
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
VIDEOS_DIR = ROOT / "videos"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("pipeline")


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


def create_video_folder(topic: str) -> Path:
    """Create a new video folder with topic.yaml.

    Args:
        topic: The video topic title.

    Returns:
        Path to the created video directory.
    """
    number = get_next_number()
    slug = slugify(topic)
    folder_name = f"{number:03d}_{slug}"
    video_dir = VIDEOS_DIR / folder_name

    video_dir.mkdir(parents=True, exist_ok=True)

    # Create topic.yaml
    topic_data = {
        "topic": topic,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "tags": [],
        "duration_target": "3-5 min",
    }

    topic_path = video_dir / "topic.yaml"
    with open(topic_path, "w") as f:
        yaml.dump(topic_data, f, default_flow_style=False, sort_keys=False)

    # Initialize status.yaml
    status_data = {"stages": []}
    status_path = video_dir / "status.yaml"
    with open(status_path, "w") as f:
        yaml.dump(status_data, f, default_flow_style=False, sort_keys=False)

    logger.info(f"Created video folder: {video_dir.relative_to(ROOT)}")
    return video_dir


def find_video_folder(video_path: str | None, topic: str | None) -> Path | None:
    """Find or create the video folder.

    Args:
        video_path: Explicit path to a video folder (--video flag).
        topic: Topic string for creating a new folder.

    Returns:
        Path to the video directory, or None if not found.
    """
    if video_path:
        path = Path(video_path)
        if not path.is_absolute():
            path = ROOT / path
        if path.exists():
            return path
        logger.error(f"Video folder not found: {video_path}")
        return None

    if topic:
        # Check if a folder for this topic already exists
        slug = slugify(topic)
        for item in VIDEOS_DIR.iterdir():
            if item.is_dir() and slug in item.name:
                logger.info(f"Found existing folder: {item.relative_to(ROOT)}")
                return item
        # Create new folder
        return create_video_folder(topic)

    return None


def load_status(video_dir: Path) -> dict:
    """Load status.yaml from video directory.

    Args:
        video_dir: Path to the video directory.

    Returns:
        Status data dictionary.
    """
    status_path = video_dir / "status.yaml"
    if status_path.exists():
        with open(status_path) as f:
            return yaml.safe_load(f) or {"stages": []}
    return {"stages": []}


def get_completed_stages(video_dir: Path) -> set[str]:
    """Get set of completed stage names from status.yaml.

    Args:
        video_dir: Path to the video directory.

    Returns:
        Set of stage names that have been completed.
    """
    status = load_status(video_dir)
    completed = set()
    for entry in status.get("stages", []):
        if entry.get("status") == "complete":
            completed.add(entry["name"])
    return completed


def print_status(video_dir: Path) -> None:
    """Print current pipeline status for a video."""
    from pipeline.stages import STAGE_NAMES

    completed = get_completed_stages(video_dir)

    logger.info(f"\nPipeline status: {video_dir.name}")
    logger.info("-" * 40)
    for name in STAGE_NAMES:
        mark = "+" if name in completed else " "
        logger.info(f"  [{mark}] {name}")
    logger.info("")


def run_pipeline(
    video_dir: Path,
    from_stage: str | None = None,
    only_stage: str | None = None,
    dry_run: bool = False,
) -> bool:
    """Run the production pipeline on a video folder.

    Args:
        video_dir: Path to the video directory.
        from_stage: Stage name to resume from (skips prior stages).
        only_stage: Run only this single stage.
        dry_run: If True, show stages that would run without executing.

    Returns:
        True if all stages completed successfully.
    """
    from pipeline.stages import STAGE_NAMES, STAGES

    # Determine which stages to run
    if only_stage:
        if only_stage not in STAGE_NAMES:
            logger.error(f"Unknown stage: {only_stage}")
            logger.error(f"Available stages: {', '.join(STAGE_NAMES)}")
            return False
        stages_to_run = [(name, cls) for name, cls in STAGES if name == only_stage]
    elif from_stage:
        if from_stage not in STAGE_NAMES:
            logger.error(f"Unknown stage: {from_stage}")
            logger.error(f"Available stages: {', '.join(STAGE_NAMES)}")
            return False
        start_idx = STAGE_NAMES.index(from_stage)
        stages_to_run = STAGES[start_idx:]
    else:
        stages_to_run = list(STAGES)

    # Dry run mode
    if dry_run:
        logger.info(f"\nDry run for: {video_dir.name}")
        logger.info(f"Stages to run ({len(stages_to_run)}):")
        for name, _ in stages_to_run:
            logger.info(f"  -> {name}")
        return True

    # Run stages
    logger.info(f"\nProducing: {video_dir.name}")
    logger.info(f"Running {len(stages_to_run)} stage(s)...")
    logger.info("")

    for name, stage_class in stages_to_run:
        runner = stage_class(video_dir)
        success = runner.execute()
        if not success:
            logger.error(f"\nPipeline stopped at stage: {name}")
            print_status(video_dir)
            return False

    logger.info("\nPipeline complete!")
    print_status(video_dir)
    return True


def main():
    """CLI entry point."""
    from pipeline.stages import STAGE_NAMES

    parser = argparse.ArgumentParser(
        description="YouTube Studio Production Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python produce.py "Why Airplanes Don't Fall"       Full pipeline
  python produce.py --from script                     Resume from script stage
  python produce.py --only voice                      Run only voice stage
  python produce.py --list-stages                     Show available stages
  python produce.py --video videos/001_foo --only voice   Specific folder + stage
""",
    )

    parser.add_argument(
        "topic",
        nargs="?",
        default=None,
        help="Video topic (creates new folder if none exists)",
    )
    parser.add_argument(
        "--from",
        dest="from_stage",
        default=None,
        metavar="STAGE",
        help="Resume pipeline from this stage",
    )
    parser.add_argument(
        "--only",
        dest="only_stage",
        default=None,
        metavar="STAGE",
        help="Run only this single stage",
    )
    parser.add_argument(
        "--video",
        default=None,
        help="Path to existing video folder",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show stages that would run without executing",
    )
    parser.add_argument(
        "--list-stages",
        action="store_true",
        help="List all available pipeline stages",
    )

    args = parser.parse_args()

    # List stages
    if args.list_stages:
        logger.info("Available pipeline stages:")
        for i, name in enumerate(STAGE_NAMES, 1):
            logger.info(f"  {i}. {name}")
        return

    # Validate arguments
    if not args.topic and not args.video:
        if args.from_stage or args.only_stage:
            parser.error("--from/--only requires either a topic or --video path")
        parser.print_help()
        sys.exit(1)

    # Find or create video folder
    video_dir = find_video_folder(args.video, args.topic)
    if video_dir is None:
        sys.exit(1)

    # Run pipeline
    success = run_pipeline(
        video_dir,
        from_stage=args.from_stage,
        only_stage=args.only_stage,
        dry_run=args.dry_run,
    )

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
