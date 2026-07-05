"""
YouTube Studio - Base Stage Infrastructure

Provides the StageRunner base class that all pipeline stages inherit from.
Handles input validation, output validation, status tracking, and logging.
"""

import logging
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from pathlib import Path

import yaml

logger = logging.getLogger("pipeline")


class StageRunner(ABC):
    """Base class for pipeline stages.

    Each stage:
    - Validates that required input files from previous stages exist
    - Runs its main logic
    - Validates that expected output files were created
    - Updates status.yaml with completion info
    """

    name: str = ""
    """Human-readable stage name (set by subclasses)."""

    required_inputs: list[str] = []
    """Relative paths (from video dir) that must exist before running."""

    expected_outputs: list[str] = []
    """Relative paths (from video dir) that should exist after running."""

    def __init__(self, video_dir: Path):
        self.video_dir = video_dir

    def validate_input(self) -> bool:
        """Check that all required input files exist.

        Returns:
            True if all inputs are present, False otherwise.
        """
        missing = []
        for rel_path in self.required_inputs:
            full_path = self.video_dir / rel_path
            if not full_path.exists():
                missing.append(rel_path)

        if missing:
            logger.error(f"[{self.name}] Missing required inputs: {', '.join(missing)}")
            return False
        return True

    def validate_output(self) -> bool:
        """Check that all expected output files were created.

        Returns:
            True if all outputs exist, False otherwise.
        """
        missing = []
        for rel_path in self.expected_outputs:
            full_path = self.video_dir / rel_path
            if not full_path.exists():
                missing.append(rel_path)

        if missing:
            logger.error(f"[{self.name}] Missing expected outputs: {', '.join(missing)}")
            return False
        return True

    @abstractmethod
    def run(self) -> bool:
        """Execute the stage logic.

        Returns:
            True if the stage completed successfully, False otherwise.
        """
        ...

    def execute(self) -> bool:
        """Run the full stage lifecycle: validate inputs, run, validate outputs, update status.

        Returns:
            True if the stage completed successfully, False otherwise.
        """
        logger.info(f"[{self.name}] Starting...")

        if not self.validate_input():
            self.update_status("failed")
            return False

        try:
            success = self.run()
        except Exception as e:
            logger.error(f"[{self.name}] Failed with error: {e}")
            self.update_status("failed")
            return False

        if not success:
            logger.error(f"[{self.name}] Stage returned failure")
            self.update_status("failed")
            return False

        if not self.validate_output():
            self.update_status("failed")
            return False

        self.update_status("complete")
        logger.info(f"[{self.name}] Complete")
        return True

    def update_status(self, status: str) -> None:
        """Update the status.yaml file for this stage.

        Args:
            status: One of 'complete', 'failed', 'running', 'pending'.
        """
        status_path = self.video_dir / "status.yaml"

        if status_path.exists():
            with open(status_path) as f:
                data = yaml.safe_load(f) or {}
        else:
            data = {}

        stages = data.get("stages", [])

        # Find existing entry or create new one
        found = False
        for entry in stages:
            if entry.get("name") == self.name:
                entry["status"] = status
                if status == "complete":
                    entry["completed_at"] = datetime.now(timezone.utc).isoformat()
                found = True
                break

        if not found:
            entry = {"name": self.name, "status": status}
            if status == "complete":
                entry["completed_at"] = datetime.now(timezone.utc).isoformat()
            stages.append(entry)

        data["stages"] = stages
        status_path.parent.mkdir(parents=True, exist_ok=True)

        with open(status_path, "w") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
