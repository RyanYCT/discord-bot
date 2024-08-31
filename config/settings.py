import pathlib
import os
from logging.config import dictConfig
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

BASE_DIR = pathlib.Path(__file__).parent.parent
ASSETS_DIR = BASE_DIR / "assets"
ASSETS_JSON = ASSETS_DIR / "assets.json"
IMG_DIR = ASSETS_DIR / "img"
COGS_DIR = BASE_DIR / "cogs"
CONFIG_DIR = BASE_DIR / "config"
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
MESSAGES_DIR = BASE_DIR / "messages"
BOT_MESSAGE_JSON = MESSAGES_DIR / "bot_message.json"
CHAT_JSON = MESSAGES_DIR / "chat.json"
EVENT_MESSAGE_JSON = MESSAGES_DIR / "event_message.json"
EXTENSION_MESSAGE_JSON = MESSAGES_DIR / "extension_message.json"
WOOF_MESSAGE_JSON = MESSAGES_DIR / "woof_message.json"
SRC_DIR = BASE_DIR / "src"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "{asctime} {levelname} {name} {message}", "style": "{"},
        "standard": {
            "format": "{asctime} {levelname:<8} {name:<15} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "console2": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "logs/discord.log",
            "encoding": "utf-8",
            "mode": "w",
            "formatter": "standard",
        },
    },
    "loggers": {
        "bot": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "discord": {
            "handlers": ["console2", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

dictConfig(LOGGING_CONFIG)


GUILD_ID = os.getenv("DISCORD_GUILD_ID")
WELCOME_CHANNEL_NAME = os.getenv("DISCORD_WELCOME_CHANNEL_NAME")
LOG_CHANNEL_NAME = os.getenv("DISCORD_LOG_CHANNEL_NAME")
TEST_CHANNEL_NAME = os.getenv("DISCORD_TEST_CHANNEL_NAME")

ADMIN_ROLE_NAME = os.getenv("DISCORD_ADMIN_ROLE_NAME")
ADMIN_ROLE_ID = int(os.getenv("DISCORD_ADMIN_ROLE_ID"))
TESTER_ROLE_NAME = os.getenv("DISCORD_TESTER_ROLE_NAME")
TESTER_ROLE_ID = int(os.getenv("DISCORD_TESTER_ROLE_ID"))
