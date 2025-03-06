import logging
from datetime import datetime

import discord
from discord.ext import commands

import settings
import utilities

import traceback

logger = logging.getLogger(__name__)


class MemberEvent(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.guild = settings.guild
        self.event_message = utilities.load_json(settings.event_message_template)

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

    @commands.hybrid_command(name="form", description="Pop up a form")
    async def form(self, ctx: commands.Context):
        apply_form_modal = OnboardFormModal()
        await ctx.interaction.response.send_modal(apply_form_modal)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """
        Send an embed message in the log channel and send a welcome message when a new member joins the guild.

        Parameters
        ----------
        member : discord.Member
            The member who joined the guild.
        """
        logger.info("%s - %s, %s (%d) has joined the guild", member.guild, member.display_name, member.name, member.id)
        timestamp = datetime.now()
        log_channel = discord.utils.get(member.guild.channels, id=self.guild["channel"]["log"]["id"])

        # Construct embed log message
        title = self.event_message["join"]["title"]
        description = self.event_message["join"]["description"].format(mention=member.mention)
        embed = discord.Embed(title=title, description=description, timestamp=timestamp)
        embed.add_field(
            name=self.event_message["join"]["fields"][0]["name"], 
            value=self.event_message["join"]["fields"][0]["value"].format(id=member.id), 
            inline=self.event_message["join"]["fields"][0]["inline"]
        )
        embed.add_field(
            name=self.event_message["join"]["fields"][1]["name"], 
            value=self.event_message["join"]["fields"][1]["value"].format(displayname=member.display_name), 
            inline=self.event_message["join"]["fields"][1]["inline"]
        )
        embed.add_field(
            name=self.event_message["join"]["fields"][2]["name"], 
            value=self.event_message["join"]["fields"][2]["value"].format(username=member.name), 
            inline=self.event_message["join"]["fields"][2]["inline"]
        )
        embed.add_field(
            name=self.event_message["join"]["fields"][3]["name"], 
            value=self.event_message["join"]["fields"][3]["value"].format(date=member.created_at.strftime("%Y-%m-%d")), 
            inline=self.event_message["join"]["fields"][3]["inline"]
        )
        url = self.get_avatar_url(member)
        embed.set_thumbnail(url=url)

        # Sign bot on embed log message
        text = self.bot.user.display_name
        icon_url = self.get_avatar_url(member)
        embed.set_footer(text=text, icon_url=icon_url)
        await log_channel.send(embed=embed)

        # Send welcome message
        welcome_channel = discord.utils.get(member.guild.channels, id=self.guild["channel"]["welcome"]["id"])
        draft = self.event_message["join"]["welcome"].format(mention=member.mention, guild=member.guild)
        await welcome_channel.send(draft)

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        """
        Send an embed message in the log channel when a member's display name is changed.

        Parameters
        ----------
        before : discord.Member
            The member's details before the update.
        after : discord.Member
            The member's details after the update.
        """
        logger.info("%s - %s, %s (%d) has updated", before.guild, before.display_name, before.name, before.id)
        timestamp = datetime.now()
        log_channel = discord.utils.get(before.guild.channels, id=self.guild["channel"]["log"]["id"])

        # Search for latest log
        guild = discord.utils.get(self.bot.guilds, id=before.guild.id)
        async for entry in guild.audit_logs(action=discord.AuditLogAction.member_update, limit=1):
            if before.display_name != after.display_name:
                logger.info("%s - %s, %s (%d) display name changed to %s", before.guild, before.display_name, before.name, before.id, after.display_name)

                # Construct embed log message
                title = self.event_message["update"]["displayname"]["title"]
                description = self.event_message["update"]["displayname"]["description"].format(mention=entry.target.mention, nickname_before=before.display_name, nickname_after=after.display_name, username=after.name, id=after.id)
                embed = discord.Embed(title=title, description=description, timestamp=timestamp)

                url = self.get_avatar_url(before)
                embed.set_thumbnail(url=url)

                # Sign moderator on embed log message
                text = entry.user.display_name
                icon_url = self.get_avatar_url(entry.user)
                embed.set_footer(text=text, icon_url=icon_url)
                await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_raw_member_remove(self, payload: discord.RawMemberRemoveEvent):
        """
        Send an embed message in the log channel when a member leaves the guild.

        Parameters
        ----------
        payload : discord.RawMemberRemoveEvent
            The payload of the member leaving the guild.
        """
        logger.info("%s - %s, %s (%d) has left the guild", payload.guild_id, payload.user.display_name, payload.user.name, payload.user.id)
        timestamp = datetime.now()
        guild = discord.utils.get(self.bot.guilds, id=payload.guild_id)
        log_channel = discord.utils.get(guild.channels, id=self.guild["channel"]["log"]["id"])

        # Construct embed log message
        title = self.event_message["remove"]["title"]
        description = self.event_message["remove"]["description"].format(mention=payload.user.mention, nickname=payload.user.display_name, username=payload.user.name, id=payload.user.id)
        embed = discord.Embed(title=title, description=description, timestamp=timestamp)
        url = self.get_avatar_url(payload.user)
        embed.set_thumbnail(url=url)

        # Sign bot on embed log message
        text = self.bot.user.display_name
        icon_url = self.get_avatar_url(payload.user)
        embed.set_footer(text=text, icon_url=icon_url)
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """
        Assign a role to a member when they react to a specified post.

        Parameters
        ----------
        payload : discord.RawReactionActionEvent
            The payload of the reaction.

        Notes
        -----
        The guild information be formatted in dictionary.
        This function assumes the dictionary is defined at the "base/" settings.py file.
        """
        # If an emoji is reacted to specified post
        message_id = payload.message_id
        if message_id == self.guild["message"]["role"]["id"]:
            guild_id = payload.guild_id
            guild = discord.utils.get(self.bot.guilds, id=guild_id)
            role = None

            # Check that emoji name is in the list
            emoji_name = payload.emoji.name
            emoji_list = self.guild["emoji"].keys()
            if emoji_name in emoji_list:
                logger.debug("emoji: %s is in the list %s", emoji_name, emoji_list)

                # Check that emoji wether is connected to a role
                role_list = self.guild["role"].keys()
                if self.guild["emoji"][emoji_name]["role"] in role_list:
                    logger.debug("emoji: %s is connected to a role %s", emoji_name, self.guild["role"][self.guild["emoji"][emoji_name]["role"]].keys())
                    role = discord.utils.get(guild.roles, id=self.guild["role"][self.guild["emoji"][emoji_name]["role"]]["id"])

                else:
                    logger.debug("emoji: %s is NOT connected to a role", payload.emoji.name)
            else:
                logger.debug("emoji: %s is NOT in the list", payload.emoji.name)

            # Assign the corresponding role to that member
            if role is not None:
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                if member is not None:
                    logger.info("%s role added to %s", role.name, member.display_name)
                    await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        """
        Remove a role from a member when they remove their reaction to a specified post.

        Parameters
        ----------
        payload : discord.RawReactionActionEvent

        Notes
        -----
        The guild information be formatted in dictionary.
        This function assumes the dictionary is defined at the "base/" settings.py file.
        """
        # If an emoji is reacted to specified post
        message_id = payload.message_id
        if message_id == self.guild["message"]["role"]["id"]:
            guild_id = payload.guild_id
            guild = discord.utils.get(self.bot.guilds, id=guild_id)
            role = None

            # Check that emoji name is in the list
            emoji_name = payload.emoji.name
            emoji_list = self.guild["emoji"].keys()
            if emoji_name in emoji_list:
                logger.debug("emoji: %s is in the list %s", emoji_name, emoji_list)

                # Check that emoji wether is connected to a role
                role_list = self.guild["role"].keys()
                if self.guild["emoji"][emoji_name]["role"] in role_list:
                    logger.debug("emoji: %s is connected to a role %s", emoji_name, self.guild["role"][self.guild["emoji"][emoji_name]["role"]])
                    role = discord.utils.get(guild.roles, id=self.guild["role"][self.guild["emoji"][emoji_name]["role"]]["id"])

                else:
                    logger.debug("emoji: %s is NOT connected to a role", payload.emoji.name)
            else:
                logger.debug("emoji: %s is NOT in the list", payload.emoji.name)

            # Remove the corresponding role from that member
            if role is not None:
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                if member is not None:
                    logger.info("%s role removed from %s", role.name, member.display_name)
                    await member.remove_roles(role)

# Buttons for approval
class ButtonView(discord.ui.View):
    guild = settings.guild
    status = None
    event_message = utilities.load_json(settings.event_message_template)

    async def disable_all_items(self):
        logger.info("Disabling items..")
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)
    
    async def on_timeout(self):
        logger.info(f"{self.message} timeout")
        await self.disable_all_items()

    @discord.ui.button(label="Approve", style=discord.ButtonStyle.success)
    async def approve_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.status = True
        await interaction.response.send_message(self.event_message["onboard"]["decision"]["approve"])
        self.stop()

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.danger)
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.status = False
        await interaction.response.send_message(self.event_message["onboard"]["decision"]["decline"])
        self.stop()

class OnboardFormModal(discord.ui.Modal):
    guild = settings.guild
    event_message = utilities.load_json(settings.event_message_template)

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

    # Construct the form
    title = event_message["onboard"]["form"]["title"]
    familyname = discord.ui.TextInput(
        style=discord.TextStyle.short, 
        label=event_message["onboard"]["form"]["familyname"]["label"], 
        required=True, 
        placeholder=event_message["onboard"]["form"]["familyname"]["placeholder"]
    )
    nickname = discord.ui.TextInput(
        style=discord.TextStyle.short, 
        label=event_message["onboard"]["form"]["nickname"]["label"], 
        required=False, 
        placeholder=event_message["onboard"]["form"]["nickname"]["placeholder"]
    )
    message = discord.ui.TextInput(
        style=discord.TextStyle.long, 
        label=event_message["onboard"]["form"]["message"]["label"], 
        required=False, 
        max_length=100, 
        placeholder=event_message["onboard"]["form"]["message"]["placeholder"]
    )

    async def on_submit(self, interaction: discord.Interaction):
        logger.info("%s - %s, %s (%d) has submitted a form", interaction.user.guild, interaction.user.display_name, interaction.user.name, interaction.user.id)
        timestamp = datetime.now()
        log_channel = discord.utils.get(interaction.guild.channels, id=self.guild["channel"]["log"]["id"])

        # Construct embed log message
        title = self.event_message["apply"]["title"]
        description = self.event_message["apply"]["description"].format(mention=interaction.user.mention, nickname=interaction.user.display_name, username=interaction.user.name, id=interaction.user.id)
        embed = discord.Embed(title=title, description=description, timestamp=timestamp)
        embed.add_field(
            name=self.event_message["apply"]["fields"][0]["name"], 
            value=self.event_message["apply"]["fields"][0]["value"].format(id=interaction.user.id), 
            inline=self.event_message["apply"]["fields"][0]["inline"]
        )
        embed.add_field(
            name=self.event_message["apply"]["fields"][1]["name"], 
            value=self.event_message["apply"]["fields"][1]["value"].format(displayname=interaction.user.display_name), 
            inline=self.event_message["apply"]["fields"][1]["inline"]
        )
        embed.add_field(
            name=self.event_message["apply"]["fields"][2]["name"], 
            value=self.event_message["apply"]["fields"][2]["value"].format(username=interaction.user.name), 
            inline=self.event_message["apply"]["fields"][2]["inline"]
        )
        embed.add_field(
            name=self.event_message["apply"]["fields"][3]["name"], 
            value=self.event_message["apply"]["fields"][3]["value"].format(date=interaction.user.created_at.strftime("%Y-%m-%d")), 
            inline=self.event_message["apply"]["fields"][3]["inline"]
        )
        embed.add_field(
            name=self.event_message["apply"]["fields"][4]["name"], 
            value=self.event_message["apply"]["fields"][4]["value"], 
            inline=self.event_message["apply"]["fields"][4]["inline"]
        )
        embed.add_field(
            name=self.event_message["apply"]["fields"][5]["name"], 
            value=self.event_message["apply"]["fields"][5]["value"].format(familyname=self.familyname.value), 
            inline=self.event_message["apply"]["fields"][5]["inline"]
        )
        embed.add_field(
            name=self.event_message["apply"]["fields"][6]["name"], 
            value=self.event_message["apply"]["fields"][6]["value"].format(nickname=self.nickname.value), 
            inline=self.event_message["apply"]["fields"][6]["inline"]
        )
        embed.add_field(
            name=self.event_message["apply"]["fields"][7]["name"], 
            value=self.event_message["apply"]["fields"][7]["value"].format(message=self.message.value), 
            inline=self.event_message["apply"]["fields"][7]["inline"]
        )
        url = self.get_avatar_url(interaction.user)
        embed.set_thumbnail(url=url)

        # Sign bot on embed log message
        text = interaction.user.display_name
        icon_url = self.get_avatar_url(interaction.user)
        embed.set_footer(text=text, icon_url=icon_url)

        # Create buttons
        view = ButtonView(timeout=20)
        log_message = await log_channel.send(embed=embed, view=view)
        view.message = log_message

        # Response to the candidate
        await interaction.response.send_message(self.event_message["apply"]["response"])

        await view.wait()

        if view.status is True:
            # Approve
            await log_channel.send(self.event_message["onboard"]["decision"]["approve"])
        else:
            # Decline
            await log_channel.send(self.event_message["onboard"]["decision"]["decline"])

        await view.disable_all_items()

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message(self.event_message["apply"]["error"])
        # Make sure we know what the error actually is
        traceback.print_exception(type(error), error, error.__traceback__)


async def setup(bot: commands.Bot):
    await bot.add_cog(MemberEvent(bot))
