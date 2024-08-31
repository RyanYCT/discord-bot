import logging
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def load_json(file):
    msg = {}
    try:
        with open(file, "r", encoding="utf-8") as file:
            msg = json.load(file)

    except FileNotFoundError as fnfe:
        logger.error(f"Error: {file} not found. {fnfe}")

    except json.JSONDecodeError as jde:
        logger.error(f"Error: Invalid JSON format in {file}. {jde}")
        
    return msg
