import logging
import random

from discord.ext import commands

import config
import utilities

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class MessageHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.all = utilities.load_json(config.all_json)
        self.any = utilities.load_json(config.any_json)
        self.vip = utilities.load_json(config.vip_json)

    @staticmethod
    def on_chance(percent):
        return random.randint(1, 100) <= percent

    @commands.hybrid_command(name="forward", description="forward <message>")
    @commands.has_any_role(config.admin_role_id)
    async def forward(self, ctx, *, message):
        """
        Forward a message to the current channel and send an ephemeral confirmation.

        This command can only be used by admin.

        Parameters
        ----------
        ctx : commands.Context
            The context in which the command was invoked.
        message : str
            The message to be forwarded.
        """
        try:
            await ctx.channel.send(message)
            await ctx.send(f"Forwarded message: {message}", ephemeral=True)

        except Exception as e:
            logger.exception("Failed to forward message: %s", e)

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Handle the event when a message is sent in the channel. Respond based on message sender and content.

        Parameters
        ----------
        message : discord.Message
            The message that was sent.
        """
        logger.info(
            "%s - %s - %s, %s (%d): %s",
            message.guild,
            message.channel,
            message.author.display_name,
            message.author,
            message.author.id,
            message.content,
        )

        # Ignore message sent by bot
        if message.author == self.bot.user:
            return

        # Ignore emoji, gif and links
        if (
            message.content.startswith("<:")
            or message.content.startswith("<a:")
            or message.content.startswith("https://")
        ):
            return

        reply, draft = self.check_all_keywords(message.content)
        if not reply:
            reply, draft = self.check_vip_mentioned(message)
        if not reply:
            reply, draft = self.check_vip_sender(message)
        if not reply:
            reply, draft = self.check_any_keywords(message.content)

        if reply:
            await message.channel.send(draft)

    def check_all_keywords(self, content):
        """
        Check whether the message contains all keywords for a topic.

        Parameters
        ----------
        content : str
            The content of the message.

        Returns
        -------
        tuple
            (reply: bool, draft: str)
        """
        for topic, data in self.all["topic"].items():
            keywords = list(data["keyword"])
            if all(word in content for word in keywords):
                logger.debug("Message included all keywords in a topic %s", topic)
                if self.on_chance(percent=data["chance"]):
                    return True, random.choice(data["reply"])
        return False, ""

    def check_any_keywords(self, content):
        """
        Check whether the message contains any keywords for a topic.

        Parameters
        ----------
        content : str
            The content of the message.

        Returns
        -------
        tuple
            (reply: bool, draft: str)
        """
        for topic, data in self.any["topic"].items():
            keywords = list(data["keyword"])
            if any(word in content for word in keywords):
                logger.debug("Message included any keywords in a topic %s", topic)
                if self.on_chance(percent=data["chance"]):
                    return True, random.choice(data["reply"])
        return False, ""

    def check_vip_sender(self, message):
        """
        Check whether the message is sent by a VIP.

        Parameters
        ----------
        message : discord.Message
            The message that was sent.

        Returns
        -------
        tuple
            (reply: bool, draft: str)
        """
        for user, data in self.vip.items():
            if message.author.id == data["id"]:
                logger.debug("Message send by a VIP %s", user)
                if len(message.mentions) > 0:
                    if self.on_chance(percent=data["topic"]["mentions"]["chance"]):
                        return True, random.choice(data["topic"]["mentions"]["reply"])
                else:
                    if self.on_chance(percent=data["topic"]["send"]["chance"]):
                        topics = list(data["topic"].keys())
                        keyword = random.choice(topics)
                        return True, random.choice(data["topic"][keyword]["reply"])
        return False, ""

    def check_vip_mentioned(self, message):
        """
        Check whether the message mentioned a VIP.

        Parameters
        ----------
        message : discord.Message
            The message that was sent.

        Returns
        -------
        tuple
            (reply: bool, draft: str)
        """
        if len(message.mentions) > 0:
            logger.debug("Message mentioned someone")
            for member in message.mentions:
                for user, data in self.vip.items():
                    if member.id == data["id"]:
                        logger.debug("Message mentioned VIP %s", user)
                        if self.on_chance(
                            percent=data["topic"]["be_mentioned"]["chance"]
                        ):
                            return True, random.choice(
                                data["topic"]["be_mentioned"]["reply"]
                            )
            logger.debug("Message mentioned NonVIP user")
        else:
            logger.debug("Message NOT mentioned anyone")
        return False, ""


async def setup(bot):
    await bot.add_cog(MessageHandler(bot))
