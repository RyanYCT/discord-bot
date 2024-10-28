import logging

import discord
from discord.ext import commands

import config
import utilities

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class BotManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.msg = utilities.load_json(config.bot_json)

    @commands.hybrid_command(name="sync", help="sync <option>")
    @commands.is_owner()
    async def sync(self, ctx, option):
        """
        Sync commands with Discord.

        This command can only be used by the bot owner.

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
                    await ctx.send(self.msg["sync"]["succeeded"], ephemeral=True)

                case "global" | "gl" | "..":
                    await self.bot.tree.sync()
                    await ctx.send(self.msg["sync"]["succeeded"], ephemeral=True)

                case _:
                    logger.info("%s failed to sync commands: invalid option %s", ctx.author, option)
                    await ctx.send(self.msg["sync"]["invalid"], ephemeral=True)

        except commands.errors.MissingAnyRole as mar:
            logger.exception("%s failed to sync commands: %s", ctx.author, mar)
            await ctx.send(self.msg["exception"]["mar"], ephemeral=True)

        except Exception as e:
            logger.exception("%s failed to sync commands: %s", ctx.author, e)
            await ctx.send(self.msg["sync"]["e"], ephemeral=True)

    @commands.hybrid_command(name="shutdown", help="Shut down the bot.")
    @commands.has_any_role(config.admin_role_id)
    async def shutdown(self, ctx):
        """
        Shut down the bot.

        This command can only be used by admin.

        Parameters
        ----------
        ctx : commands.Context
            Represent the context in which a command is being invoked.
        """
        try:
            await self.bot.close()

        except commands.errors.MissingAnyRole as mar:
            logger.exception("%s failed to shut down the bot: %s", ctx.author, mar)
            await ctx.send(self.msg["exception"]["mar"], ephemeral=True)

        else:
            await ctx.send(self.msg["shutdown"]["succeeded"], ephemeral=True)

    @commands.hybrid_command(name="loaded_cogs", help="Show loaded cogs.")
    @commands.is_owner()
    async def loaded_cogs(self, ctx):
        """
        Show loaded cogs.

        This command can only be used by the bot owner.

        Parameters
        ----------
        ctx : commands.Context
            Represent the context in which a command is being invoked.
        """
        # Construct the embed message
        title = self.msg["loaded_cogs"]["title"]
        description = self.msg["loaded_cogs"]["description"]
        embed = discord.Embed(title=title, description=description)
        name = self.msg["loaded_cogs"]["name"]
        value = ""
        for cog in self.bot.cogs:
            value += f"{cog}\n"
        embed.add_field(name=name, value=value, inline=False)

        logger.info("%s show loaded cogs: %s", ctx.author, value)
        await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="set_activity", help="set_activity <name>")
    @commands.is_owner()
    async def set_activity(self, ctx, name):
        """
        Set the activity of the bot.

        This command can only be used by the bot owner.

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

        Note
        ----
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
                status = discord.Status.do_not_disturb

        try:
            await self.bot.change_presence(activity=activity, status=status)

        except commands.errors.MissingAnyRole as mar:
            logger.exception("%s failed to set activity: %s", ctx.author, mar)
            await ctx.send(self.msg["exception"]["mar"], ephemeral=True)

        except Exception as e:
            logger.exception("%s failed to set activity: %s", ctx.author, e)
            await ctx.send(self.msg["set_activity"]["failed"], ephemeral=True)

        else:
            await ctx.send(self.msg["set_activity"]["succeeded"], ephemeral=True)


async def setup(bot):
    await bot.add_cog(BotManager(bot))
