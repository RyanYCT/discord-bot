import datetime
import logging

import discord
from discord.ext import commands

import config
import utilities

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class MemberEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.event = utilities.load_json(config.event_json)

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
        Send an embed message in the log channel and send a welcome message when a new member joins the guild.

        Parameters
        ----------
        member : discord.Member
            The member who joined the guild.
        """
        logger.info(
            "%s - %s, %s (%d) has joined the guild",
            member.guild,
            member.display_name,
            member.name,
            member.id,
        )
        timestamp = datetime.datetime.now()
        log_channel = discord.utils.get(member.guild.channels, id=config.log_channel_id)

        # Construct embed message
        title = self.event["join"]["title"]
        description = self.event["join"]["description"].format(
            mention=member.mention,
            nickname=member.display_name,
            username=member.name,
            id=member.id,
        )
        embed = discord.Embed(title=title, description=description, timestamp=timestamp)
        url = self.get_avatar_url(member)
        embed.set_thumbnail(url=url)

        # Sign bot on embed message
        text = self.bot.user.display_name
        icon_url = self.bot.user.avatar.url
        embed.set_footer(text=text, icon_url=icon_url)
        await log_channel.send(embed=embed)

        # Send welcome message
        welcome_channel = discord.utils.get(
            member.guild.channels, id=config.welcome_channel_id
        )
        draft = self.event["join"]["welcome"].format(
            mention=member.mention, guild=member.guild
        )
        await welcome_channel.send(draft)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """
        Send an embed message in the log channel when a member is removed from the guild.

        Parameters
        ----------
        member : discord.Member
            The member who was removed from the guild.
        """
        logger.info(
            "%s - %s, %s (%d) is removed from the guild",
            member.guild,
            member.display_name,
            member.name,
            member.id,
        )
        timestamp = datetime.datetime.now()
        log_channel = discord.utils.get(member.guild.channels, id=config.log_channel_id)

        # Search for the latest audit log
        guild = discord.utils.get(self.bot.guilds, id=member.guild.id)
        async for entry in guild.audit_logs(
            action=discord.AuditLogAction.kick, limit=1
        ):
            # Construct embed message
            title = self.event["remove"]["title"]
            if entry.target.id == member.id:
                logger.info(
                    "has been kicked by %s, %s (%d)".format(
                        entry.user.display_name, entry.user.name, entry.user.id
                    )
                )
                reason = entry.reason
            else:
                logger.info(
                    "%s, %s (%d) has left on his own",
                    member.display_name,
                    member.name,
                    member.id,
                )
                reason = "left on his/her own"
            description = self.event["remove"]["description"].format(
                mention=member.mention,
                nickname=member.display_name,
                username=member.name,
                id=member.id,
                reason=reason,
            )
            embed = discord.Embed(
                title=title, description=description, timestamp=timestamp
            )
            url = self.get_avatar_url(member)
            embed.set_thumbnail(url=url)

            # Sign moderator on embed message
            text = entry.user.display_name
            icon_url = entry.user.avatar.url
            embed.set_footer(text=text, icon_url=icon_url)
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """
        Send an embed message in the log channel when a member's display name is changed.

        Parameters
        ----------
        before : discord.Member
            The member's details before the update.
        after : discord.Member
            The member's details after the update.
        """
        logger.info(
            "%s - %s, %s (%d) has updated",
            before.guild,
            before.display_name,
            before.name,
            before.id,
        )
        timestamp = datetime.datetime.now()
        log_channel = discord.utils.get(before.guild.channels, id=config.log_channel_id)

        # Search for latest log
        guild = discord.utils.get(self.bot.guilds, id=before.guild.id)
        async for entry in guild.audit_logs(
            action=discord.AuditLogAction.member_update, limit=1
        ):
            if before.display_name != after.display_name:
                logger.info(
                    "%s - %s, %s (%d) display name changed to %s",
                    before.guild,
                    before.display_name,
                    before.name,
                    before.id,
                    after.display_name,
                )

                # Construct embed message
                title = self.event["update"]["displayname"]["title"]
                description = self.event["update"]["displayname"]["description"].format(
                    mention=entry.target.mention,
                    nickname_before=before.display_name,
                    nickname_after=after.display_name,
                    username=after.name,
                    id=after.id,
                )
                embed = discord.Embed(
                    title=title, description=description, timestamp=timestamp
                )

                url = self.get_avatar_url(before)
                embed.set_thumbnail(url=url)

                # Sign moderator on embed message
                text = entry.user.display_name
                icon_url = self.get_avatar_url(entry.user)
                embed.set_footer(text=text, icon_url=icon_url)
                await log_channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(MemberEvent(bot))
