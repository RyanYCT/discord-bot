import os
import pathlib
from logging.config import dictConfig

from dotenv import load_dotenv

load_dotenv()

# Bot
token = os.getenv("DISCORD_TOKEN")

# Guild
guild_id = os.getenv("DISCORD_GUILD_ID")
guild_lan = os.getenv("DISCORD_GUILD_LANGUAGE", "en")
welcome_channel_name = os.getenv("DISCORD_WELCOME_CHANNEL_NAME", "welcome")
welcome_channel_id = int(os.getenv("DISCORD_WELCOME_CHANNEL_ID"))
log_channel_name = os.getenv("DISCORD_LOG_CHANNEL_NAME", "logs")
log_channel_id = int(os.getenv("DISCORD_LOG_CHANNEL_ID"))
test_channel_name = os.getenv("DISCORD_TEST_CHANNEL_NAME", "test")
test_channel_id = int(os.getenv("DISCORD_TEST_CHANNEL_ID"))
admin_role_name = os.getenv("DISCORD_ADMIN_ROLE_NAME", "admin")
admin_role_id = int(os.getenv("DISCORD_ADMIN_ROLE_ID"))
tester_role_name = os.getenv("DISCORD_TESTER_ROLE_NAME", "tester")
tester_role_id = int(os.getenv("DISCORD_TESTER_ROLE_ID"))
member_role_name = os.getenv("DISCORD_MEMBER_ROLE_NAME", "member")
member_role_id = int(os.getenv("DISCORD_MEMBER_ROLE_ID"))

# Directories
base_dir = pathlib.Path(__file__).parent
cogs_dir = base_dir / "cogs"
logs_dir = base_dir / "logs"
msg_dir = base_dir / "messages" / guild_lan
src_dir = base_dir / "src"
utils_dir = src_dir / "utils"

# Files
all_json = msg_dir / "all.json"
any_json = msg_dir / "any.json"
bot_json = msg_dir / "bot.json"
event_json = msg_dir / "event.json"
vip_json = msg_dir / "vip.json"

# Cogs / extensions desire to load
cog_list = [
    "bot_manager.py",
    "extension_manager.py",
    "member_event.py",
    "message_handler.py",
]


log_config = {
    "version": 1,
    "formatters": {
        "detailed": {
            "format": "{asctime} {levelname} {name} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "detailed",
            "level": "INFO",
        },
        # "file": {
        #     "class": "logging.FileHandler",
        #     "formatter": "detailed",
        #     "level": "INFO",
        #     "filename": "logs/discord.log",
        #     "mode": "w",
        #     "encoding": "utf-8",
        # },
    },
    "loggers": {
        "bot": {"handlers": ["console"], "level": "INFO", "propagate": False},
    },
}

dictConfig(log_config)
