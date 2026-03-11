"""
File Utilities
Helper functions for file operations in the SDD workflow.
"""

import os
from pathlib import Path
from typing import List, Optional, Dict, Any
import re
import json


class FileUtils:
    """Utilities for file operations and project structure management."""

    @staticmethod
    def read_file(filepath: str, encoding: str = "utf-8") -> str:
        """
        Read complete file contents.

        Args:
            filepath: Path to file to read
            encoding: File encoding (default: utf-8)

        Returns:
            File contents as string

        Raises:
            FileNotFoundError: If file does not exist
        """
        file_path = Path(filepath)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        return file_path.read_text(encoding=encoding)

    @staticmethod
    def write_file(filepath: str, content: str, encoding: str = "utf-8") -> str:
        """
        Write content to file.

        Args:
            filepath: Path where file should be written
            content: Content to write
            encoding: File encoding (default: utf-8)

        Returns:
            Absolute path to written file
        """
        file_path = Path(filepath)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding=encoding)
        return str(file_path.absolute())

    @staticmethod
    def find_files(
        root: str,
        pattern: str = "*",
        file_type: Optional[str] = None,
    ) -> List[str]:
        """
        Find files matching pattern in directory tree.

        Args:
            root: Root directory to search
            pattern: Glob pattern to match
            file_type: Optional file extension filter (e.g., '.py')

        Returns:
            List of matching file paths
        """
        root_path = Path(root)
        matches = []

        for file in root_path.rglob(pattern):
            if file.is_file():
                if file_type and not file.suffix == file_type:
                    continue
                matches.append(str(file))

        return sorted(matches)

    @staticmethod
    def load_json(filepath: str) -> Dict[str, Any]:
        """
        Load JSON file.

        Args:
            filepath: Path to JSON file

        Returns:
            Parsed JSON as dictionary
        """
        content = FileUtils.read_file(filepath)
        return json.loads(content)

    @staticmethod
    def save_json(filepath: str, data: Dict[str, Any], indent: int = 2) -> str:
        """
        Save dictionary as JSON file.

        Args:
            filepath: Path where JSON should be written
            data: Dictionary to serialize
            indent: JSON indentation level

        Returns:
            Path to written file
        """
        content = json.dumps(data, indent=indent, ensure_ascii=False)
        return FileUtils.write_file(filepath, content)

    @staticmethod
    def ensure_directory(dirpath: str) -> str:
        """
        Ensure directory exists, creating if necessary.

        Args:
            dirpath: Directory path to ensure

        Returns:
            Absolute path to directory
        """
        dir_path = Path(dirpath)
        dir_path.mkdir(parents=True, exist_ok=True)
        return str(dir_path.absolute())

    @staticmethod
    def list_directory(dirpath: str, recursive: bool = False) -> List[str]:
        """
        List contents of directory.

        Args:
            dirpath: Directory path to list
            recursive: Whether to list recursively

        Returns:
            List of file and directory names
        """
        dir_path = Path(dirpath)
        if not dir_path.exists():
            return []

        if recursive:
            items = [str(p) for p in dir_path.rglob("*")]
        else:
            items = [str(p.name) for p in dir_path.iterdir()]

        return sorted(items)

    @staticmethod
    def get_relative_path(filepath: str, base_path: str) -> str:
        """
        Get relative path from base.

        Args:
            filepath: Full file path
            base_path: Base directory path

        Returns:
            Relative path
        """
        file_path = Path(filepath)
        base = Path(base_path)
        try:
            return str(file_path.relative_to(base))
        except ValueError:
            return str(file_path)

    @staticmethod
    def file_exists(filepath: str) -> bool:
        """Check if file exists."""
        return Path(filepath).exists()

    @staticmethod
    def directory_exists(dirpath: str) -> bool:
        """Check if directory exists."""
        return Path(dirpath).is_dir()

    @staticmethod
    def delete_file(filepath: str) -> bool:
        """
        Delete file if it exists.

        Returns:
            True if file was deleted, False if it didn't exist
        """
        file_path = Path(filepath)
        if file_path.exists():
            file_path.unlink()
            return True
        return False

    @staticmethod
    def copy_file(src: str, dst: str) -> str:
        """
        Copy file from src to dst.

        Returns:
            Path to destination file
        """
        import shutil

        src_path = Path(src)
        dst_path = Path(dst)
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_path, dst_path)
        return str(dst_path)
