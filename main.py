import logging.config

from dotenv import load_dotenv

import settings
from guild_bot import GuildBot

# Load environment variables
load_dotenv()

# Apply logging configuration
logging.config.dictConfig(settings.LOGGING_CONFIG)

def run() -> None:
    logger = logging.getLogger(__name__)
    logger.info("Starting the bot...")
    bot = GuildBot()
    bot.run(settings.token, log_handler=None, root_logger=False)


if __name__ == "__main__":
    run()
