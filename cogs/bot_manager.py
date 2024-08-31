import logging
import discord
from discord.ext import commands
from config import settings
from src import utilities

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class BotManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.assets = utilities.load_json(settings.ASSETS_JSON)
        self.msg = utilities.load_json(settings.BOT_MESSAGE_JSON)

    @commands.hybrid_command(name="sync", help="Sync guild commands.")
    @commands.is_owner()
    async def sync(self, ctx):
        """
        Sync guild commands with Discord.

        This command can only be used by the bot owner.

        Parameters
        ----------
        ctx : commands.Context
            Represents the context in which a command is being invoked.
        """
        try:
            await self.bot.tree.sync(guild=ctx.guild)

        except Exception as e:
            logger.exception("Failed to sync commands: %s", e)
        
        else:
            await ctx.send(self.msg["sync"]["succeeded"], ephemeral=True)

    @commands.hybrid_command(name="shutdown")
    @commands.has_any_role(settings.ADMIN_ROLE_ID)
    async def shutdown(self, ctx):
        """
        Shut down the bot.

        This command can only be used by admin.

        Parameters
        ----------
        ctx : commands.Context
            Represents the context in which a command is being invoked.
        """
        await self.bot.close()

    @commands.hybrid_command(name="loaded_cogs", help="Show loaded cogs.")
    @commands.is_owner()
    async def loaded_cogs(self, ctx):
        """
        Show loaded cogs.

        This command can only be used by the bot owner.

        Parameters
        ----------
        ctx : commands.Context
            Represents the context in which a command is being invoked.
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

        await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="set_game", help="set_game <name>")
    @commands.is_owner()
    async def set_game(self, ctx, name):
        """
        Set the game status of the bot.

        This command can only be used by the bot owner.

        Parameters
        ----------
        ctx : discord.commands.Context
            Represents the context in which a command is being invoked.
        name : str
            The game's name or message to be displayed. "default" or "d" restores to default status.

        NOTE
        ----
        - "discord.BaseActivity" includes: Activity, Game, Streaming, CustomActivity.
        - "discord.Status" includes: online, offline, idle, dnd, do_not_disturb, invisible.

        TODO
        ----
        - Add more choices of activity type.
        - Add another function to customize the details of activity.
        """
        match name:
            case "default" | "d":
                activity = None
                status = None

            case "Black Desert Online" | "BDO" | "bdo" | "黑色沙漠" | "黑沙":
                activity = discord.Game(name="Black Desert Online")
                status = discord.Status.online
                
            case _:
                activity = discord.Game(name=name)
                status = discord.Status.do_not_disturb

        try:
            await self.bot.change_presence(activity=activity, status=status)

        except Exception as e:
            logger.exception("Failed to set activity: %s", e)
            await ctx.send(self.msg["failed"], ephemeral=True)

        else:
            await ctx.send(self.msg["succeeded"], ephemeral=True)

async def setup(bot):
    await bot.add_cog(BotManager(bot))
