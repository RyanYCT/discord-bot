import logging

import discord
from discord.ext import commands

import settings
import utilities

logger = logging.getLogger("bot_manager")


class BotManager(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot_message = utilities.load_json(settings.bot_message_template)

    @commands.hybrid_command(name="sync", help="sync <option>")
    @commands.has_any_role(settings.guild["role"]["admin"]["id"], settings.guild["role"]["tester"]["id"])
    async def sync(self, ctx: commands.Context, option: str):
        """
        Sync commands with Discord. Use this when new command no show in Discord client.

        Parameters
        ----------
        ctx : commands.Context
            Represents the context in which a command is being invoked.
        option : str
            A string representing the sync option.
            Valid options:
            - "guild", "g", "." : Sync commands for the current guild.
            - "global", "gl", ".." : Sync commands globally.

        Returns
        -------
        None
            Sends a confirmation message in the Discord channel.
        """
        try:
            match option:
                case "guild" | "g" | ".":
                    await self.bot.tree.sync(guild=ctx.guild)
                    await ctx.send(self.bot_message["sync"]["succeeded"])

                case "global" | "gl" | "..":
                    await self.bot.tree.sync()
                    await ctx.send(self.bot_message["sync"]["succeeded"])

                case _:
                    logger.info("%s failed to sync commands: invalid option %s", ctx.author, option)
                    await ctx.send(self.bot_message["sync"]["invalid"])

        except commands.errors.MissingAnyRole as mar:
            logger.exception("%s failed to sync commands: %s", ctx.author, mar)
            await ctx.send(self.bot_message["exception"]["mar"])

        except Exception as e:
            logger.exception("%s failed to sync commands: %s", ctx.author, e)
            await ctx.send(self.bot_message["sync"]["e"])

    @commands.hybrid_command(name="shutdown", help="Shut down the bot.")
    @commands.has_any_role(settings.guild["role"]["admin"]["id"], settings.guild["role"]["tester"]["id"])
    async def shutdown(self, ctx: commands.Context):
        """
        Shut down the bot.

        Parameters
        ----------
        ctx : commands.Context
            Represent the context in which a command is being invoked.
        """
        try:
            await self.bot.close()

        except commands.errors.MissingAnyRole as mar:
            logger.exception("%s failed to shut down the bot: %s", ctx.author, mar)
            await ctx.send(self.bot_message["exception"]["mar"])

        else:
            await ctx.send(self.bot_message["shutdown"]["succeeded"])

    @commands.hybrid_command(name="loaded_cogs", help="Show loaded cogs.")
    @commands.has_any_role(settings.guild["role"]["admin"]["id"], settings.guild["role"]["tester"]["id"])
    async def loaded_cogs(self, ctx: commands.Context):
        """
        Show loaded cogs.

        Parameters
        ----------
        ctx : commands.Context
            Represent the context in which a command is being invoked.
        """
        # Construct the embed message
        title = self.bot_message["loaded_cogs"]["title"]
        description = self.bot_message["loaded_cogs"]["description"]
        embed = discord.Embed(title=title, description=description)
        name = self.bot_message["loaded_cogs"]["name"]
        value = ""
        for cog in self.bot.cogs:
            value += f"{cog}\n"
        embed.add_field(name=name, value=value, inline=False)

        logger.info("%s show loaded cogs: %s", ctx.author, value)
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="set_activity", help="set_activity <name>")
    @commands.has_any_role(settings.guild["role"]["admin"]["id"], settings.guild["role"]["tester"]["id"])
    async def set_activity(self, ctx: commands.Context, name: str):
        """
        Set the activity of the bot.

        Parameters
        ----------
        ctx : discord.commands.Context
            Represents the context in which a command is being invoked.
        name : str
            The game's name or message to be displayed.
            Use "default" or "d" to restore the default status.

        Returns
        -------
        None
            Sends a confirmation message after setting the activity.

        Notes
        -----
        - Currently, only the Game activity type is supported.
        - The bot's status is set to "do not disturb" when a custom activity is set.
        - Future updates may include more activity types and customization options.
        """
        match name:
            case "default" | "d":
                activity = None
                status = None

            case _:
                activity = discord.Game(name=name)
                status = discord.Status.online

        try:
            await self.bot.change_presence(activity=activity, status=status)

        except commands.errors.MissingAnyRole as mar:
            logger.exception("%s failed to set activity: %s", ctx.author, mar)
            await ctx.send(self.bot_message["exception"]["mar"])

        except Exception as e:
            logger.exception("%s failed to set activity: %s", ctx.author, e)
            await ctx.send(self.bot_message["set_activity"]["failed"])

        else:
            await ctx.send(self.bot_message["set_activity"]["succeeded"])


async def setup(bot: commands.Bot):
    await bot.add_cog(BotManager(bot))
