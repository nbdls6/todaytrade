
import yaml
from pathlib import Path
from typing import Any, Dict, Union

def load_yaml(file_path: Union[str, Path]) -> Dict[str, Any]:
    """Load a YAML file and return its contents as a dictionary."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"YAML file not found: {file_path}")
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing YAML file {file_path}: {e}")


def load_txt(file_path: Union[str, Path]) -> str:
    """Load a text file and return its contents as a string."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Text file not found: {file_path}")
    except UnicodeDecodeError:
        raise UnicodeDecodeError(f"Error reading text file {file_path}: cannot decode with UTF-8")