import os
import logging
from discord.ext import commands
from config import settings
from src import utilities

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ExtensionManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.msg = utilities.load_json(settings.EXTENSION_MESSAGE_JSON)

    @commands.hybrid_command(name="load", help="load <filename>")
    @commands.has_any_role(settings.ADMIN_ROLE_ID, settings.TESTER_ROLE_ID)
    @commands.is_owner()
    async def load(self, ctx, extension):
        """
        Load extension into the bot.

        This command can be used by admin and tester.

        Args:
            ctx (commands.Context): Represents the context in which a command is being invoked under.
            extension (str): The name of the extension to be loaded or "all" to load all extensions.
        """

        @staticmethod
        async def load_helper(file):
            if not file.startswith("__") and file.endswith(".py"):
                file = file[:-3]
                try:
                    await self.bot.load_extension(f"cogs.{file}")

                except commands.ExtensionNotFound as enf:
                    await ctx.send(f"Extension {file} not found. Please check the filename.", ephemeral=True)
                    logger.exception("Failed to load %s: %s", file, enf)

                except commands.ExtensionAlreadyLoaded as eal:
                    await ctx.send(f"Extension {file} is already loaded", ephemeral=True)
                    logger.exception("Failed to load %s: %s", file, eal)
                
                else:
                    await ctx.send(f"Loaded {file}", ephemeral=True)
                    logger.info("Loaded %s", file)


        extension = extension.lower()
        if extension == "all":
            for file in os.listdir(settings.COGS_DIR):
                await load_helper(file)

        else:
            await load_helper(extension)

    @commands.hybrid_command(name="unload", help="unload <filename>")
    @commands.is_owner()
    async def unload(self, ctx, extension):
        """
        Unload extension from the bot.

        This command can be used by admin and tester.

        Args:
            ctx (commands.Context): Represents the context in which a command is being invoked under.
            extension (str): The name of the extension to be unloaded or "all" to unload all extensions.
        """

        @staticmethod
        async def unload_helper(file):
            if not file.startswith("__") and file.endswith(".py"):
                file = file[:-3]
                try:
                    await self.bot.unload_extension(f"cogs.{file}")

                except commands.ExtensionNotFound as enf:
                    await ctx.send(f"Extension {file} not found. Please check the filename.", ephemeral=True)
                    logger.exception("Failed to unload %s: %s", file, enf)

                except commands.ExtensionNotLoaded as enl:
                    await ctx.send(f"Extension {file} is not loaded", ephemeral=True)
                    logger.exception("Failed to unload %s: %s", file, enl)
                
                else:
                    await ctx.send(f"Unloaded {file}", ephemeral=True)
                    logger.info("Unloaded %s", file)

        extension = extension.lower()
        if extension == "all":
            for file in os.listdir(settings.COGS_DIR):
                await unload_helper(file)

        else:
            await unload_helper(extension)

    @commands.hybrid_command(name="reload", help="reload <filename>")
    @commands.has_any_role(settings.ADMIN_ROLE_ID, settings.TESTER_ROLE_ID)
    async def reload(self, ctx, extension):
        """
        Reload extension in the bot.

        This command can be used by admin and tester.

        Args:
            ctx (commands.Context): Represents the context in which a command is being invoked under.
            extension (str): The name of the extension to be reloaded or "all" to reload all extensions.
        """

        @staticmethod
        async def reload_helper(file):
            if not file.startswith("__") and file.endswith(".py"):
                file = file[:-3]
                try:
                    await self.bot.reload_extension(f"cogs.{file}")

                except commands.ExtensionNotLoaded as enl:
                    await ctx.send(f"Extension {file} is not loaded", ephemeral=True)
                    logger.exception("Failed to unload %s: %s", file, enl)

                except commands.ExtensionNotFound as enf:
                    await ctx.send(f"Extension {file} not found. Please check the filename.", ephemeral=True)
                    logger.exception("Failed to unload %s: %s", file, enf)
                
                else:
                    await ctx.send(f"Reloaded {file}", ephemeral=True)
                    logger.info("Reloaded %s", file)

        extension = extension.lower()
        if extension == "all":
            for file in os.listdir(settings.COGS_DIR):
                await reload_helper(file)
                
        else:
            await reload_helper(extension)


async def setup(bot):
    await bot.add_cog(ExtensionManager(bot))
