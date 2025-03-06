import os
import pathlib
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

# Bot
token: str = os.getenv("DISCORD_TOKEN", "")
language: str = os.getenv("DISCORD_GUILD_LANGUAGE", "en")

# Directories
ROOT_DIR = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))
cogs_directory = ROOT_DIR / "cogs"
languages_directory = ROOT_DIR / "languages"

# Files
keywords_directory = languages_directory / language / "keywords"
all_keywords = keywords_directory / "all.json"
any_keywords = keywords_directory / "any.json"
vip_keywords = keywords_directory / "vip.json"

templates_directory = languages_directory / language / "templates"
bot_message_template = templates_directory / "bot.json"
embed_message_template = templates_directory / "embed.json"
event_message_template = templates_directory / "event.json"
item_report_template = templates_directory / "item_report.json"
overall_report_template = templates_directory / "overall_report.json"
vote_message_template = templates_directory / "vote.json"
vote_emojis = templates_directory / "vote_emojis.json"

# Cogs / extensions desire to load at start
cogs = [
    "bot_manager.py",
    "extension_manager.py",
    "guild_manager.py",
    "member_event.py",
    "message_handler.py",
    "report_manager.py",
]

# Guild setting
guild: Dict[str, Any] = {
    "id": int(os.getenv("GUILD_ID")),
    "channel": {
        "log": {"id": int(os.getenv("LOG_CHANNEL_ID"))},
        "welcome": {"id": int(os.getenv("WELCOME_CHANNEL_ID"))},
        "test": {"id": int(os.getenv("TEST_CHANNEL_ID"))},
        "role": {"id": int(os.getenv("ROLE_CHANNEL_ID"))},
        "conference": {"id": int(os.getenv("CONFERENCE_CHANNEL_ID"))},
    },
    "role": {
        "admin": {"id": int(os.getenv("ADMIN_ROLE_ID")), "emoji": None},
        "tester": {"id": int(os.getenv("TESTER_ROLE_ID")), "emoji": None},
        "member": {"id": int(os.getenv("MEMBER_ROLE_ID")), "emoji": None},
        "subscriber": {"id": int(os.getenv("SUBSCRIBER_ROLE_ID")), "emoji": "🔔"},
    },
    "emoji": {
        "🔔": {"role": "subscriber"},
    },
    "message": {
        "role": {"id": int(os.getenv("ROLE_MESSAGE_ID"))}
    }
}

# Logging configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": os.getenv("LOG_LEVEL", "INFO"),
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["console"],
            "level": os.getenv("LOG_LEVEL", "INFO"),
            "propagate": True,
        },
        "discord": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    }
}

# API URL
api_url: str = os.getenv("API_URL")
