import logging

from dotenv import load_dotenv

import config
from guild_bot import GuildBot

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

load_dotenv()


def run():
    bot = GuildBot()
    bot.run(config.token, root_logger=True)


if __name__ == "__main__":
    run()
