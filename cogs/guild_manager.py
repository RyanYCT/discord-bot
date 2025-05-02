import logging

import discord
from discord.ext import commands

import settings
import utilities

logger = logging.getLogger("guild_manager")


class GuildManager(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot_message = utilities.load_json(settings.bot_message_template)

    @commands.hybrid_command(name="audit_log", help="audit_log <number of rows>")
    @commands.has_any_role(settings.guild["role"]["admin"]["id"], settings.guild["role"]["tester"]["id"])
    async def audit_log(self, ctx: commands.Context, number: int):
        """
        Retrieves the latest audit log entries for the guild.

        Parameters
        ----------
        ctx : commands.Context
            Represents the context in which a command is being invoked.
        number : int
            The number of rows to retrieve from the audit log.

        Returns
        -------
        None
            Sends a confirmation message in the Discord channel.
        """
        # Retrieves latest logs
        guild = discord.utils.get(self.bot.guilds, id=ctx.guild.id)
        async for entry in guild.audit_logs(limit=number):
            draft = str(entry) + "\n"
            await ctx.send(draft)


async def setup(bot: commands.Bot):
    await bot.add_cog(GuildManager(bot))
