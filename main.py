import os
import logging
from dotenv import load_dotenv
from guild_bot import GuildBot

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

load_dotenv()


def run():
    bot = GuildBot()
    bot.run(os.getenv("DISCORD_TOKEN"), root_logger=True)


if __name__ == "__main__":
    run()
