import logging
import random
from discord.ext import commands
from config import settings
from src import utilities

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class MessageHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.chat = utilities.load_json(settings.CHAT_JSON)

    @staticmethod
    def on_chance(percent):
        return random.randint(1, 100) <= percent

    @commands.Cog.listener()
    async def on_message(self, message):
        logger.info("%s - %s - %s, %s (%d): %s", message.guild, message.channel, message.author.display_name, message.author, message.author.id, message.content)
        # Ignore message sent by bot
        if message.author == self.bot.user:
            logger.debug("Ignore message sent by bot")
            return

        # Ignore emoji, gif and links
        elif message.content.startswith("<:") or message.content.startswith("<a:") or message.content.startswith("https://"):
            logger.debug("Ignore message contains emoji, gif or link")
            return

        else:
            logger.debug("vvvvvvvvvvvvv message handling vvvvvvvvvvvv")
            reply = False
            draft = ""

            # Message send by a VIP
            match message.author.id:
                # VIP send message
                case sakuratoy if message.author.id == self.chat["sakuratoy"]["id"]:
                    logger.debug("case VIP sakuratoy send message")
                    reply = self.on_chance(percent=33)
                    # Select a reply from random topic
                    topics = list(self.chat["sakuratoy"]["topic"].keys())
                    topic_keyword = random.choice(topics)
                    draft = random.choice(self.chat["sakuratoy"]["topic"][topic_keyword]["reply"])

                # VIP mentioned someone
                case sakuratoy_mentions if message.author.id == self.chat["sakuratoy"]["id"] and len(message.mentions) > 0:
                    logger.debug("case VIP sakuratoy send message and mentioned someone")
                    reply = self.on_chance(percent=66)
                    draft = random.choice(self.chat["sakuratoy"]["topic"]["missyou"]["reply"])

                case _:
                    pass


        # NOTE VIP mentioned - unit test: PASS
            # Message mentioned a VIP
            # message.mentions include @user and reply to user
            if len(message.mentions) > 0:
                logger.debug("message mentioned someone")
                for member in message.mentions:
                    # VIP be mentioned
                    match member.id:
                        case guild_bot if member.id == self.chat["bot"]["id"]:
                            logger.debug("case VIP BOT be mentioned")
                            reply = self.on_chance(percent=100)
                            draft = random.choice(self.chat["bot"]["topic"]["be_mentioned"]["reply"])

                        case usagiyaki if member.id == self.chat["usagiyaki"]["id"]:
                            logger.debug("case VIP usagiyaki be mentioned")
                            reply = self.on_chance(percent=87)
                            draft = random.choice(self.chat["usagiyaki"]["topic"]["be_mentioned"]["reply"])

                        case captainfmafrica if member.id == self.chat["captainfmafrica"]["id"]:
                            logger.debug("case VIP captainfmafrica be mentioned")
                            reply = self.on_chance(percent=87)
                            draft = random.choice(self.chat["captainfmafrica"]["topic"]["be_mentioned"]["reply"])

                        case _:
                            logger.debug("case NON VIP be mentioned")
                            pass

            else:
                logger.debug("message NOT mentioned anyone")

            if reply:
                await message.channel.send(draft)
        # NOTE VIP mentioned - unit test: PASS
            # # Message with keyword
            # keywords = list(self.chat["keyword"].keys())
            # if any(words in message.content for words in self.chat[keywords]["keyword"]):
            #     logger.debug("Message with keyword detected")
            #     reply = self.on_chance(percent=100)
            #     draft = random.choice(self.chat[keywords]["reply"])

            # if reply:
            #     draft = random.choice(self.chat["reply"])
            #     await message.channel.send(draft)

        logger.debug("^^^^^^^^^^^^^ message handled ^^^^^^^^^^^^")

async def setup(bot):
    await bot.add_cog(MessageHandler(bot))
