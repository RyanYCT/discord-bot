import logging
from logging.config import dictConfig

from dotenv import load_dotenv

import settings
from guild_bot import GuildBot

# Load environment variables
load_dotenv()

# Apply logging configuration
dictConfig(settings.LOGGING_CONFIG)
logger = logging.getLogger(__name__)

def run() -> None:
    logger.info("Starting the bot...")
    bot = GuildBot()
    bot.run(settings.token, log_handler=None, root_logger=False)


if __name__ == "__main__":
    run()
