import json
from pathlib import Path
from typing import Optional
import os

class FileManager:
    """
    A utility class for managing file paths and checking file existence.
    The root_path attribute is used as the base path for all file operations.
    Default file location: root_path/extraction_engine/managers/file_manager.py
    """

    root_path: Path = Path(__file__).resolve().parents[2]  # Default root path
    paths_location: Path = root_path / "config" / "paths.json"
    _paths_cache = None  # Cache for file paths

    @classmethod
    def set_root_path(cls, path: str):
        """Sets the root path for file management operations.
        Args: path (str): The new root path.
        """
        cls.root_path = cls._to_path(path)

    @classmethod
    def _to_path(cls, path_str: str) -> Path:
        """Converts a string to a Path object, raising an exception if the conversion fails.

        Args: path_str (str): The string to convert.
        Returns: Path: The resulting Path object.
        Raises: ValueError: If the string cannot be converted to a Path object.
        """
        try:
            return Path(path_str)
        except Exception as e:
            raise ValueError(f"Failed to convert string to Path: {e}")

    @classmethod
    def _load_paths(cls):
        """Load and cache file paths from the JSON file."""
        with open(cls.paths_location, 'r') as file:
            cls._paths_cache = json.load(file)

    @classmethod
    def _get_cached_path(cls, filepath_name: str) -> Optional[str]:
        """Get a file path from the cache."""
        if cls._paths_cache is None:
            cls._load_paths()
        # Now check if _paths_cache is a dictionary and contains the filepath_name
        if isinstance(cls._paths_cache, dict) and filepath_name in cls._paths_cache:
            return cls._paths_cache.get(filepath_name)
        else:
            return None

    @classmethod
    def construct_path(cls, filepath_str: str, base_str: Optional[str] = None) -> Path:
        """Constructs the full path for a given filename, optionally based on a specified base path.

        Args:
            filepath_str (str): The name of the file.
            base_path (Optional[str]): The base path. If None, uses the class's root_path.

        Returns:
            Path: The full path to the file.
        """
        filename = cls._to_path(filepath_str)
        if base_str is None:
            base_path = cls.root_path
        else:
            base_path = cls._to_path(base_str)
        return base_path.joinpath(filename)

    @staticmethod
    def is_valid_file(filepath_str: str) -> bool:
        """Checks if the provided path exists and is a file.

        Args:
            filepath (str): The filepath to check.

        Returns:
            bool: True if the filepath exists and is a file, otherwise False.
        """
        filepath = FileManager._to_path(filepath_str)
        return filepath.exists() and filepath.is_file()

    @classmethod
    def get_filepaths(cls, filepath_name: str) -> Path:
        """Returns the path to the file location.

        Args:filepath_name (str): The name of the file path in the paths.json file.

        Returns: Path: The path to the file.
        """
        relative_path_str = cls._get_cached_path(filepath_name)
        if not relative_path_str:
            raise ValueError(f"No path found for filepath name: {filepath_name}")
        return cls.construct_path(relative_path_str)

    @classmethod
    def get_env_paths_or_default(cls, env_var: str) -> Path:
        """Resolves the full path of the paths file, allowing for environment variable overrides.

        Args:
            env_var (str): The name of the environment variable that may override the default path.

        Returns:
            Path: The resolved path to the paths file.
        """
        env_var_value = os.environ.get(env_var)
        if env_var_value:
            cls.paths_location = cls._to_path(env_var_value)
        # Now reload the paths, as the location may have changed
        cls._load_paths()
        return cls.paths_location
