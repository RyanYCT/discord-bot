import logging
import random
from typing import Tuple

import discord
from discord.ext import commands

import settings
import utilities

logger = logging.getLogger("message_handler")


class MessageHandler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.guild = settings.guild
        self.all_keywords = utilities.load_json(settings.all_keywords)
        self.any_keywords = utilities.load_json(settings.any_keywords)
        self.vip_keywords = utilities.load_json(settings.vip_keywords)

    @staticmethod
    def convertible_to_int(string: str) -> bool:
        try:
            int(string)
            return True
        except ValueError:
            return False

    @staticmethod
    def get_avatar_url(user: discord.User) -> str:
        """
        In case the user object has no avatar, return the default avatar URL instead of None by default.

        Parameters
        ----------
        user : discord.User
            The user whose avatar URL needs to be retrieved.

        Returns
        -------
        str
            The avatar URL of the user.
        """
        try:
            url = user.avatar.url
        except AttributeError:
            url = user.default_avatar.url
        return url

    @staticmethod
    def on_chance(percent: int) -> bool:
        return random.randint(1, 100) <= percent

    @commands.hybrid_command(name="forward", description="forward <message>")
    @commands.has_any_role(settings.guild["role"]["admin"]["id"])
    async def forward(self, ctx: commands.Context, *, message: str):
        """
        Forward a message to the current channel and send an ephemeral confirmation.

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

    @commands.hybrid_command(name="react_emoji", description="react_emoji <message_id> <number_of_option>")
    @commands.has_any_role(settings.guild["role"]["admin"]["id"])
    async def react_emoji(self, ctx: commands.Context, message_id, number_of_option):
        """
        React emoji on a message.

        Parameters
        ----------
        ctx : commands.Context
            The context in which the command was invoked.
        message_id : int
            The ID of the message to be react.
        number_of_option : str
            The number of option to react.
        """
        if not self.convertible_to_int(message_id):
            await ctx.send("Warning: The message_id must be an integer.", ephemeral=True)

        elif not self.convertible_to_int(number_of_option):
            await ctx.send("Warning: The number_of_option must be an integer.", ephemeral=True)

        else:
            try:
                number_of_option = int(number_of_option)
                message = await ctx.fetch_message(message_id)

                # Prepare reaction emojis for the voting
                emojis = [
                    "\U0001F1E6", "\U0001F1E7", "\U0001F1E8",
                    "\U0001F1E9", "\U0001F1EA", "\U0001F1EB",
                    "\U0001F1EC", "\U0001F1ED", "\U0001F1EE",
                    "\U0001F1EF", "\U0001F1F0", "\U0001F1F1",
                    "\U0001F1F2", "\U0001F1F3", "\U0001F1F4",
                    "\U0001F1F5", "\U0001F1F6", "\U0001F1F7",
                    "\U0001F1F8", "\U0001F1F9", "\U0001F1FA",
                    "\U0001F1FB", "\U0001F1FC", "\U0001F1FD",
                    "\U0001F1FE", "\U0001F1FF"
                ]

                for i in range(number_of_option):
                    await message.add_reaction(emojis[i])

            except Exception as e:
                logger.exception("Failed to send announcement: %s", e)

    @commands.hybrid_command(name="announce", description="send a predefine embed announcement")
    @commands.has_any_role(settings.guild["role"]["admin"]["id"])
    async def announce(self, ctx: commands.Context):
        """
        Send an embed message to the current channel and send an ephemeral confirmation.

        Parameters
        ----------
        ctx : commands.Context
            The context in which the command was invoked.

        Notes
        -----
        This function assumes the embed message is defined at the "languages/<language>/templates" embed.json file.
        """
        try:
            # Construct embed message
            draft = utilities.load_json(settings.embed_message_template)
            embed = discord.Embed.from_dict(draft)

            # Sign bot on embed message
            text = self.bot.user.display_name
            icon_url = self.get_avatar_url(self.bot.user)
            embed.set_footer(text=text, icon_url=icon_url)

            await ctx.channel.send(embed=embed)
            await ctx.send("Embed message sent", ephemeral=True)

        except Exception as e:
            logger.exception("Failed to send announcement: %s", e)

    @commands.hybrid_command(name="edit_embed", description="edit to a embed message")
    @commands.has_any_role(settings.guild["role"]["admin"]["id"])
    async def edit_embed(self, ctx: commands.Context, message_id):
        """
        Edit the specified embed message with a draft file.

        Parameters
        ----------
        ctx : commands.Context
            The context in which the command was invoked.
        message_id : int
            The ID of the message to be edited.

        Notes
        -----
        This function assumes the embed message is defined at the "languages/<language>/templates" embed.json file.
        """
        if not self.convertible_to_int(message_id):
            await ctx.send("Warning: The message_id must be an integer.", ephemeral=True)

        else:
            try:
                # Construct embed message
                draft = utilities.load_json(settings.embed_message_template)
                embed = discord.Embed.from_dict(draft)

                # Sign bot on embed message
                text = self.bot.user.display_name
                icon_url = self.get_avatar_url(self.bot.user)
                embed.set_footer(text=text, icon_url=icon_url)

                message = await ctx.fetch_message(message_id)
                await message.edit(embed=embed)

            except Exception as e:
                logger.exception("Failed to edit announcement: %s", e)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """
        Handle the event when a message is sent in the channel. Respond based on message sender and content.

        Parameters
        ----------
        message : discord.Message
            The message that was sent.
        """
        logger.info("%s - %s - %s, %s (%d): %s", message.guild, message.channel, message.author.display_name, message.author, message.author.id, message.content)

        # Ignore message sent by bot
        if message.author == self.bot.user:
            return

        # Ignore messages in a specific channel
        if message.channel.id == self.guild["channel"]["conference"]["id"]:
            return

        # Ignore emoji, gif and links
        if (message.content.startswith("<:") or message.content.startswith("<a:") or message.content.startswith("https://")):
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

    def check_all_keywords(self, content: str) -> Tuple[bool, str]:
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
        for topic, data in self.all_keywords["topic"].items():
            keywords = list(data["keyword"])
            if all(word in content for word in keywords):
                logger.debug("Message included all keywords in a topic %s", topic)
                if self.on_chance(percent=data["chance"]):
                    return True, random.choice(data["reply"])
        return False, ""

    def check_any_keywords(self, content: str) -> Tuple[bool, str]:
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
        for topic, data in self.any_keywords["topic"].items():
            keywords = list(data["keyword"])
            if any(word in content for word in keywords):
                logger.debug("Message included any keywords in a topic %s", topic)
                if self.on_chance(percent=data["chance"]):
                    return True, random.choice(data["reply"])
        return False, ""

    def check_vip_sender(self, message: discord.Message) -> Tuple[bool, str]:
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
        for user, data in self.vip_keywords.items():
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

    def check_vip_mentioned(self, message: discord.Message) -> Tuple[bool, str]:
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
                for user, data in self.vip_keywords.items():
                    if member.id == data["id"]:
                        logger.debug("Message mentioned VIP %s", user)
                        if self.on_chance(percent=data["topic"]["be_mentioned"]["chance"]):
                            return True, random.choice(data["topic"]["be_mentioned"]["reply"])
            logger.debug("Message mentioned NonVIP user")
        else:
            logger.debug("Message NOT mentioned anyone")
        return False, ""


async def setup(bot: commands.Bot):
    await bot.add_cog(MessageHandler(bot))
