import logging

from dotenv import load_dotenv

import settings
from guild_bot import GuildBot

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def run():
    logger.info("Starting the bot...")
    bot = GuildBot()
    bot.run(settings.token, root_logger=True)


if __name__ == "__main__":
    run()
