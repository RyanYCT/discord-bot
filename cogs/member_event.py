import logging
import datetime
import discord
from discord.ext import commands
from config import settings
from utils import utilities

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class MemberEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.msg = utilities.load_json(settings.EVENT_MESSAGE_JSON)

    @staticmethod
    def get_avatar_url(member):
        try:
            url = member.avatar.url
        except AttributeError:
            url = member.default_avatar.url
        return url

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """
        Handle the event when a new member joins the guild.

        Logs the event, sends a welcome message, and posts an embed in the log channel.

        Parameters
        ----------
        member : discord.Member
            The member who joined the guild.
        """
        logger.info("%s - %s, %s (%d) has joined the guild", member.guild, member.display_name, member.name, member.id)
        timestamp = datetime.datetime.now()
        log_channel = discord.utils.get(member.guild.channels, name=settings.LOG_CHANNEL_NAME)

        # Construct embed message
        title = self.msg["join"]["title"]
        description = self.msg["join"]["description"].format(mention=member.mention, nickname=member.display_name, username=member.name, id=member.id)
        embed = discord.Embed(title=title, description=description, timestamp=timestamp)
        url = self.get_avatar_url(member)
        embed.set_thumbnail(url=url)

        # Sign by bot
        text = self.bot.user.display_name
        icon_url = self.bot.user.avatar.url
        embed.set_footer(text=text, icon_url=icon_url)
        await log_channel.send(embed=embed)

        # Send welcome message
        welcome_channel = discord.utils.get(member.guild.channels, name=settings.WELCOME_CHANNEL_NAME)
        draft = self.msg["join"]["welcome"].format(mention=member.mention, guild=member.guild)
        await welcome_channel.send(draft)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """
        Handle the event when a member is removed from the guild.

        Logs the event, searches for the latest audit log entry, and posts an embed in the log channel.

        Parameters
        ----------
        member : discord.Member
            The member who was removed from the guild.
        """
        logger.info("%s - %s, %s (%d) is removed from the guild", member.guild, member.display_name, member.name, member.id)
        timestamp = datetime.datetime.now()
        log_channel = discord.utils.get(member.guild.channels, name=settings.LOG_CHANNEL_NAME)

        # Search for the latest log
        guild = discord.utils.get(self.bot.guilds, name=member.guild.name)
        async for entry in guild.audit_logs(action=discord.AuditLogAction.kick, limit=1):
            # Construct embed message
            title = self.msg["remove"]["title"]
            if entry.target.id == member.id:
                logger.info("has been kicked by %s, %s (%d)".format(entry.user.display_name, entry.user.name, entry.user.id))
                reason = entry.reason
            else:
                logger.info("%s, %s (%d) has left on his own", member.display_name, member.name, member.id)
                reason = "left on his/her own"
            description = self.msg["remove"]["description"].format(mention=member.mention, nickname=member.display_name, username=member.name, id=member.id, reason=reason)
            embed = discord.Embed(title=title, description=description, timestamp=timestamp)
            url = self.get_avatar_url(member)
            embed.set_thumbnail(url=url)

            # Sign by moderator
            text = entry.user.display_name
            icon_url = entry.user.avatar.url
            embed.set_footer(text=text, icon_url=icon_url)
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """
        Handle the event when a member's details are updated in the guild.

        Logs the event, searches for the latest audit log entry, and posts an embed in the log channel if the display name is changed.

        Parameters
        ----------
        before : discord.Member
            The member's details before the update.
        after : discord.Member
            The member's details after the update.
        """
        logger.info("%s - %s, %s (%d) has updated", before.guild, before.display_name, before.name, before.id)
        timestamp = datetime.datetime.now()
        log_channel = discord.utils.get(before.guild.channels, name=settings.LOG_CHANNEL_NAME)

        # Search for latest log
        guild = discord.utils.get(self.bot.guilds, name=before.guild.name)
        async for entry in guild.audit_logs(action=discord.AuditLogAction.member_update, limit=1):
            if before.display_name != after.display_name:
                logger.info("%s - %s, %s (%d) display name changed to %s", before.guild, before.display_name, before.name, before.id, after.display_name)

                # Construct embed message
                title = self.msg["update"]["displayname"]["title"]
                description = self.msg["update"]["displayname"]["description"].format(mention=entry.target.mention, nickname_before=before.display_name, nickname_after=after.display_name, username=after.name, id=after.id)
                embed = discord.Embed(title=title, description=description, timestamp=timestamp)

                url = self.get_avatar_url(before)
                embed.set_thumbnail(url=url)

                # Moderator signed
                text = entry.user.display_name
                icon_url = self.get_avatar_url(entry.user)
                embed.set_footer(text=text, icon_url=icon_url)
                await log_channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(MemberEvent(bot))
