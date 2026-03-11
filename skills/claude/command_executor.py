"""
Command Executor
Handles execution of spec-driven commands (.specify workflow).
"""

from pathlib import Path
from typing import Dict, List, Optional, Any
import os
import re


class CommandExecutor:
    """Executes and manages SDD workflow commands."""

    # Registered commands from .claude/commands/
    BUILTIN_COMMANDS = {
        "sp.phr": "Record this AI exchange as a structured PHR artifact",
        "sp.specify": "Create a detailed feature specification",
        "sp.plan": "Create an implementation plan",
        "sp.tasks": "Break down work into actionable tasks",
        "sp.implement": "Execute implementation tasks",
        "sp.adr": "Create an Architectural Decision Record",
        "sp.checklist": "Create a verification checklist",
        "sp.clarify": "Clarify requirements with structured questions",
        "sp.analyze": "Analyze code or requirements",
        "sp.reverse-engineer": "Reverse engineer existing functionality",
        "sp.git.commit_pr": "Generate git commit or PR",
        "sp.taskstoissues": "Convert tasks to GitHub issues",
        "sp.constitution": "Define project constitution",
    }

    def __init__(self, repo_root: str):
        """
        Initialize CommandExecutor with repository root.

        Args:
            repo_root: Path to repository root
        """
        self.repo_root = Path(repo_root)
        self.commands_dir = self.repo_root / ".claude" / "commands"

    def get_command_path(self, command_name: str) -> Optional[Path]:
        """
        Get path to command file.

        Args:
            command_name: Name of the command (e.g., 'sp.phr')

        Returns:
            Path to command file or None if not found
        """
        command_file = self.commands_dir / f"{command_name}.md"
        if command_file.exists():
            return command_file
        return None

    def get_command_help(self, command_name: str) -> Optional[str]:
        """
        Get help text for a command.

        Args:
            command_name: Name of the command

        Returns:
            Command description or None
        """
        if command_name in self.BUILTIN_COMMANDS:
            return self.BUILTIN_COMMANDS[command_name]
        return None

    def list_commands(self) -> Dict[str, str]:
        """List all available commands with descriptions."""
        return self.BUILTIN_COMMANDS.copy()

    def load_command(self, command_name: str) -> Optional[str]:
        """
        Load command content from file.

        Args:
            command_name: Name of the command to load

        Returns:
            Command content or None if not found
        """
        command_path = self.get_command_path(command_name)
        if command_path and command_path.exists():
            return command_path.read_text(encoding="utf-8")
        return None

    def extract_command_metadata(self, command_name: str) -> Optional[Dict[str, Any]]:
        """
        Extract metadata from command file.

        Args:
            command_name: Name of the command

        Returns:
            Dictionary with description and metadata
        """
        content = self.load_command(command_name)
        if not content:
            return None

        # Extract YAML frontmatter
        match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
        if not match:
            return {"name": command_name}

        frontmatter = match.group(1)
        metadata = {}

        for line in frontmatter.strip().split("\n"):
            if ": " in line:
                key, value = line.split(": ", 1)
                metadata[key.strip()] = value.strip().strip('"')

        return metadata
