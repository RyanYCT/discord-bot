import os
import pathlib

from dotenv import load_dotenv

load_dotenv()

# API URL
api_url = "http://localhost:5000"

# Bot
token = os.getenv("DISCORD_TOKEN")
language = os.getenv("DISCORD_GUILD_LANGUAGE", "en")

# Guild setting
guild = {
    "name": "Guild Name",
    "id": 1234567890123456789,
    "channel": {
        "welcome": {
            "name": "welcome-channel-name",
            "id": 1234567890123456789,
        },
        "log": {
            "name": "log-channel-name",
            "id": 1234567890123456789,
        },
        "test": {
            "name": "testing-channel-name",
            "id": 1234567890123456789,
        },
        "role": {
            "name": "reaction-role-channel-name",
            "id": 1234567890123456789,
        },
    },
    "role": {
        "admin": {"id": 1234567890123456789, "name": "admin", "emoji": None},
        "tester": {"id": 1234567890123456789, "name": "tester", "emoji": None},
        "member": {"id": 1234567890123456789, "name": "member", "emoji": None},
        "custom_role": {
            "id": 1234567890123456789,
            "name": "custom_role_name",
            "emoji": "emoji_name",
        },
    },
    # Fill emoji information if that is connected to a role
    "emoji": {"emoji_name": {"role": "custom_role"}},
    # Special message that will trigger event
    "message": {
        # This message responsible for reaction role
        "role": {"id": 1234567890123456789}
    },
}

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
overall_report_template = templates_directory / "overall_report.json"
vote_message_template = templates_directory / "vote.json"
vote_emojis = templates_directory / "vote_emojis.json"

# Cogs / extensions desire to load at start
cogs = [
    "bot_manager.py",
    "extension_manager.py",
    "guild_manager.py",
    "member_event.py",
    "message_handler.py"
]
