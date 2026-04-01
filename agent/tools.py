import pathlib
import subprocess
from typing import Tuple, Dict

from langchain_core.tools import tool

FILE_STORAGE: Dict[str, str] = {}


def safe_path_for_project(path: str) -> str:
    """Normalizes path and return as string key."""
    if ".." in path:
        raise ValueError("Path must not contain '..'")
    return path.replace("\\", "/").lstrip("/")


@tool
def write_file(path: str, content: str) -> str:
    """Writes content to in-memory storage."""
    normalized_path = safe_path_for_project(path)
    FILE_STORAGE[normalized_path] = content
    return f"""WROTE: {normalized_path}"""


@tool
def read_file(path: str) -> str:
    """Reads content from in-memory storage."""
    normalized_path = safe_path_for_project(path)
    return FILE_STORAGE.get(normalized_path, "")


@tool
def get_current_directory() -> str:
    """Returns the virtual project root."""
    return "/"


@tool
def list_files(directory: str = ".") -> str:
    """Lists all files in memory storage."""
    normalized_dir = safe_path_for_project(directory) if directory != "." else ""

    files = [
        path for path in FILE_STORAGE.keys()
        if not normalized_dir or path.startswith(normalized_dir)
    ]
    return "\n".join(files) if files else "No files found."


def clear_storage():
    """Clear all files from memory - call before each new generation"""
    FILE_STORAGE.clear()

def get_all_files() -> Dict[str, str]:
    """Get all generated files as a dictionary"""
    return FILE_STORAGE.copy()