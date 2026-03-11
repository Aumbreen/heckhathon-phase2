"""
Prompt History Record (PHR) Manager
Handles creation, routing, and validation of PHR files for the SDD workflow.
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
import re


class PHRManager:
    """Manages Prompt History Records (PHRs) for knowledge capture and traceability."""

    # Valid stages for PHR classification
    VALID_STAGES = {
        "constitution",
        "spec",
        "plan",
        "tasks",
        "red",
        "green",
        "refactor",
        "explainer",
        "misc",
        "general",
        "implementation",
        "debugging",
        "discussion",
    }

    def __init__(self, repo_root: str):
        """
        Initialize PHRManager with repository root.

        Args:
            repo_root: Absolute path to the repository root
        """
        self.repo_root = Path(repo_root)
        self.history_dir = self.repo_root / "history" / "prompts"
        self.history_dir.mkdir(parents=True, exist_ok=True)

    def generate_slug(self, title: str) -> str:
        """Convert title to slug format for filename."""
        slug = title.lower()
        slug = re.sub(r"[^\w\s-]", "", slug)
        slug = re.sub(r"[-\s]+", "-", slug)
        return slug.strip("-")

    def get_next_id(self, route_dir: Path) -> int:
        """
        Get the next available ID for a PHR in a given directory.

        Args:
            route_dir: Directory to search for existing PHRs

        Returns:
            Next available ID
        """
        if not route_dir.exists():
            return 1

        max_id = 0
        for file in route_dir.glob("*.prompt.md"):
            match = re.match(r"^(\d+)-", file.name)
            if match:
                file_id = int(match.group(1))
                max_id = max(max_id, file_id)

        return max_id + 1

    def determine_route(
        self, stage: str, feature: Optional[str] = None
    ) -> Path:
        """
        Determine the route directory for a PHR based on stage and feature.

        Args:
            stage: PHR stage (constitution|spec|plan|tasks|...|general)
            feature: Feature name (only required for feature-specific stages)

        Returns:
            Full path to the route directory

        Raises:
            ValueError: If stage is invalid or routing cannot be determined
        """
        if stage not in self.VALID_STAGES:
            raise ValueError(f"Invalid stage: {stage}. Must be one of {self.VALID_STAGES}")

        if stage == "constitution":
            route_dir = self.history_dir / "constitution"
        elif stage == "general":
            route_dir = self.history_dir / "general"
        else:
            # Feature-specific stages require feature context
            if not feature or feature == "none":
                feature = "general"
            route_dir = self.history_dir / feature

        route_dir.mkdir(parents=True, exist_ok=True)
        return route_dir

    def create_phr(
        self,
        title: str,
        stage: str,
        prompt_text: str,
        response_text: str,
        feature: Optional[str] = None,
        model: Optional[str] = None,
        files_created: Optional[List[str]] = None,
        labels: Optional[List[str]] = None,
        **kwargs,
    ) -> str:
        """
        Create a Prompt History Record (PHR).

        Args:
            title: 3-7 word descriptive title
            stage: Work stage (constitution|spec|plan|tasks|...|general)
            prompt_text: Complete user input (verbatim)
            response_text: Key assistant output
            feature: Feature name (optional, defaults to 'none')
            model: Model used (optional)
            files_created: List of files created/modified
            labels: List of label tags
            **kwargs: Additional metadata (branch, user, command, etc.)

        Returns:
            Path to created PHR file

        Raises:
            ValueError: If validation fails
        """
        if not title or len(title.split()) < 3:
            raise ValueError("Title must be 3-7 words")

        if stage not in self.VALID_STAGES:
            raise ValueError(f"Invalid stage: {stage}")

        # Determine routing
        feature = feature or kwargs.get("feature", "none")
        route_dir = self.determine_route(stage, feature)

        # Get next ID
        phr_id = self.get_next_id(route_dir)

        # Generate filename
        slug = self.generate_slug(title)
        file_ext = f".{stage}.prompt.md" if stage != "general" else ".general.prompt.md"
        filename = f"{phr_id:03d}-{slug}{file_ext}"
        filepath = route_dir / filename

        # Prepare metadata
        date_iso = datetime.now().strftime("%Y-%m-%d")
        branch = kwargs.get("branch", "master")
        user = kwargs.get("user", "unknown")
        command = kwargs.get("command", "")
        files_yaml = self._format_yaml_list(files_created or [])
        labels_list = labels or []

        # Build YAML frontmatter
        frontmatter = f"""---
id: {phr_id}
title: {title}
stage: {stage}
date: {date_iso}
surface: agent
model: {model or "unknown"}
feature: {feature}
branch: {branch}
user: {user}
command: {command}
labels: {json.dumps(labels_list)}
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:{files_yaml}
tests:
- No tests run or added
---
"""

        # Build content
        content = frontmatter + f"\n## Prompt\n\n{prompt_text}\n\n## Response\n\n{response_text}\n"

        # Write file
        filepath.write_text(content, encoding="utf-8")

        return str(filepath)

    @staticmethod
    def _format_yaml_list(items: List[str]) -> str:
        """Format a list for YAML output."""
        if not items:
            return " null"
        return "\n" + "\n".join(f"- {item}" for item in items)

    def list_phrs(self, stage: Optional[str] = None, feature: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all PHRs, optionally filtered by stage or feature."""
        phrs = []

        if stage:
            if stage == "constitution":
                dirs = [self.history_dir / "constitution"]
            elif stage == "general":
                dirs = [self.history_dir / "general"]
            else:
                feature = feature or "general"
                dirs = [self.history_dir / feature]
        else:
            dirs = list(self.history_dir.glob("*"))

        for dir_path in dirs:
            if dir_path.is_dir():
                for file in sorted(dir_path.glob("*.prompt.md")):
                    match = re.match(r"^(\d+)-(.+?)\.(.+?)\.prompt\.md$", file.name)
                    if match:
                        phr_id, slug, detected_stage = match.groups()
                        phrs.append(
                            {
                                "id": int(phr_id),
                                "title": slug,
                                "stage": detected_stage,
                                "path": str(file),
                            }
                        )

        return sorted(phrs, key=lambda x: (x["stage"], x["id"]))
