import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def load_json(file: str) -> Dict[str, Any]:
    data: Dict[str, Any] = {}
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError as fnfe:
        logger.error(f"Error: {file} not found. {fnfe}")
    except json.JSONDecodeError as jde:
        logger.error(f"Error: Invalid JSON format in {file}. {jde}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
    return data
