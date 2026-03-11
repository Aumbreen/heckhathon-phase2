"""
Configuration Loader
Loads and manages configuration for Claude agents.
"""

import os
import json
from pathlib import Path
from typing import Any, Dict, Optional


class ConfigLoader:
    """Loads and manages configuration for Claude agents."""

    def __init__(self, repo_root: Optional[str] = None):
        """
        Initialize ConfigLoader.

        Args:
            repo_root: Repository root path (auto-detected if not provided)
        """
        self.repo_root = Path(repo_root or self._find_repo_root())
        self.config = self._load_config()
        self.agents = self._load_agents()

    def _find_repo_root(self) -> str:
        """Find repository root by looking for .git or marked sentinel files."""
        current = Path.cwd()
        while current != current.parent:
            if (current / ".git").exists() or (current / "CLAUDE.md").exists():
                return str(current)
            current = current.parent
        return str(Path.cwd())

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from config.json."""
        config_path = self.repo_root / ".claude" / "config.json"

        if not config_path.exists():
            return {}

        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _load_agents(self) -> Dict[str, Dict[str, Any]]:
        """Load agent definitions from .claude/agents/."""
        agents = {}
        agents_dir = self.repo_root / ".claude" / "agents"

        if not agents_dir.exists():
            return agents

        for agent_file in agents_dir.glob("*.md"):
            try:
                content = agent_file.read_text(encoding="utf-8")
                # Parse agent name from filename (e.g., "architecture-agent.md" -> "architecture-agent")
                agent_name = agent_file.stem
                agents[agent_name] = {
                    "path": str(agent_file),
                    "name": agent_name,
                    "content": content,
                }
            except Exception:
                pass

        return agents

    def get_config(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.config.get(key, default)

    def get_provider(self, name: str) -> Optional[Dict[str, Any]]:
        """Get provider configuration by name."""
        providers = self.config.get("Providers", [])
        for provider in providers:
            if provider.get("name") == name:
                return provider
        return None

    def get_router_config(self, route: str = "default") -> str:
        """Get router configuration for a specific route."""
        router = self.config.get("Router", {})
        return router.get(route, router.get("default", ""))

    def get_agent(self, name: str) -> Optional[Dict[str, Any]]:
        """Get agent definition by name."""
        return self.agents.get(name)

    def list_agents(self) -> list:
        """List all available agents."""
        return list(self.agents.keys())

    def get_repo_root(self) -> Path:
        """Get repository root path."""
        return self.repo_root

    def get_project_paths(self) -> Dict[str, Path]:
        """Get common project paths."""
        return {
            "repo": self.repo_root,
            "claude": self.repo_root / ".claude",
            "skills": self.repo_root / "skills" / "claude",
            "history": self.repo_root / "history",
            "specs": self.repo_root / "specs",
            ".specify": self.repo_root / ".specify",
        }

    def reload_config(self) -> None:
        """Reload configuration from disk."""
        self.config = self._load_config()
        self.agents = self._load_agents()
