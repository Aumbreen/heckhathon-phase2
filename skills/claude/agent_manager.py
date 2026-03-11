"""
Agent Manager
Manages agent loading and orchestration.
"""

from pathlib import Path
from typing import Dict, List, Optional, Any
import re

try:
    import yaml
except ImportError:
    yaml = None


class AgentManager:
    """Manages agent loading and orchestration."""

    def __init__(self, repo_root: str):
        """
        Initialize AgentManager.

        Args:
            repo_root: Path to repository root
        """
        self.repo_root = Path(repo_root)
        self.agents_dir = self.repo_root / ".claude" / "agents"
        self.agents = self._load_agents()

    def _load_agents(self) -> Dict[str, Dict[str, Any]]:
        """Load all agent definitions from .claude/agents/."""
        agents = {}

        if not self.agents_dir.exists():
            return agents

        for agent_file in self.agents_dir.glob("*.md"):
            try:
                agent_name = agent_file.stem
                content = agent_file.read_text(encoding="utf-8")
                metadata = self._parse_agent_metadata(content)
                agents[agent_name] = {
                    "name": agent_name,
                    "file": str(agent_file),
                    "content": content,
                    **metadata,
                }
            except Exception:
                pass

        return agents

    def _parse_agent_metadata(self, content: str) -> Dict[str, Any]:
        """
        Parse agent metadata from YAML frontmatter.

        Args:
            content: Agent file content

        Returns:
            Metadata dictionary
        """
        metadata = {}

        # Extract YAML frontmatter
        match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
        if not match:
            return metadata

        frontmatter_text = match.group(1)

        # Try yaml first if available, fallback to simple parsing
        if yaml:
            try:
                metadata = yaml.safe_load(frontmatter_text) or {}
            except Exception:
                metadata = self._parse_frontmatter_simple(frontmatter_text)
        else:
            metadata = self._parse_frontmatter_simple(frontmatter_text)

        return metadata

    def _parse_frontmatter_simple(self, frontmatter_text: str) -> Dict[str, Any]:
        """Fallback simple YAML frontmatter parser."""
        metadata = {}
        for line in frontmatter_text.strip().split("\n"):
            if ": " in line:
                key, value = line.split(": ", 1)
                metadata[key.strip()] = value.strip().strip('"')
        return metadata

    def get_agent(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get agent definition by name.

        Args:
            name: Agent name

        Returns:
            Agent definition or None
        """
        return self.agents.get(name)

    def list_agents(self) -> List[str]:
        """List all available agent names."""
        return sorted(self.agents.keys())

    def get_agents_by_type(self, agent_type: str) -> List[Dict[str, Any]]:
        """
        Get agents filtered by type or category.

        Args:
            agent_type: Type to filter by (e.g., 'backend', 'database', 'architecture')

        Returns:
            List of matching agents
        """
        matching = []
        for name, agent in self.agents.items():
            if agent_type.lower() in name.lower():
                matching.append(agent)
        return matching

    def get_agent_description(self, name: str) -> str:
        """Get short description of an agent."""
        agent = self.get_agent(name)
        if agent:
            return agent.get("description", "No description")
        return "Agent not found"

    def reload_agents(self) -> None:
        """Reload agents from disk."""
        self.agents = self._load_agents()
