import logging

from discord.ext import commands

import config
import utilities

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ExtensionManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.msg = utilities.load_json(config.bot_json)

    @commands.hybrid_command(name="load", help="load <filename>")
    @commands.has_any_role(config.admin_role_id, config.tester_role_id)
    async def load(self, ctx, extension):
        """
        Load an extension into the bot.

        This command can be used by admin and tester.

        Parameters
        ----------
        ctx : commands.Context
            Represent the context in which a command is being invoked.
        extension : str
            The name of the extension to be loaded or "all" to load all extensions.
        """

        @staticmethod
        async def load_helper(file):
            """
            Helper function to load a single extension.

            Parameters
            ----------
            file : str
                The name of the file to be loaded as an extension.
            """
            if not file.startswith("__") and file.endswith(".py"):
                file = file[:-3]
                try:
                    await self.bot.load_extension(f"cogs.{file}")

                except commands.errors.MissingAnyRole as mar:
                    logger.exception("%s failed to load %s: %s", ctx.author, file, mar)
                    await ctx.send(self.msg["exception"]["mar"], ephemeral=True)

                except commands.ExtensionNotFound as enf:
                    logger.exception("%s failed to load %s: %s", ctx.author, file, enf)
                    await ctx.send(self.msg["exception"]["enf"].format(file=file), ephemeral=True)

                except commands.ExtensionAlreadyLoaded as eal:
                    logger.exception("%s failed to load %s: %s", ctx.author, file, eal)
                    await ctx.send(self.msg["exception"]["eal"].format(file=file), ephemeral=True)

                else:
                    logger.info("%s loaded %s", ctx.author, file)
                    await ctx.send(self.msg["load"]["succeeded"].format(file=file), ephemeral=True)

        extension = extension.lower()
        if extension == "all":
            for file in config.cog_list:
                await load_helper(file)

        else:
            await load_helper(extension)

    @commands.hybrid_command(name="unload", help="unload <filename>")
    @commands.has_any_role(config.admin_role_id, config.tester_role_id)
    async def unload(self, ctx, extension):
        """
        Unload an extension from the bot.

        This command can be used by admin and tester.

        Parameters
        ----------
        ctx : commands.Context
            Represent the context in which a command is being invoked.
        extension : str
            The name of the extension to be unloaded or "all" to unload all extensions.
        """

        @staticmethod
        async def unload_helper(file):
            """
            Helper function to unload a single extension.

            Parameters
            ----------
            file : str
                The name of the file to be unloaded as an extension.
            """
            if not file.startswith("__") and file.endswith(".py"):
                file = file[:-3]
                try:
                    await self.bot.unload_extension(f"cogs.{file}")

                except commands.errors.MissingAnyRole as mar:
                    logger.exception("%s failed to unload %s: %s", ctx.author, file, mar)
                    await ctx.send(self.msg["exception"]["mar"], ephemeral=True)

                except commands.ExtensionNotFound as enf:
                    logger.exception("%s failed to unload %s: %s", ctx.author, file, enf)
                    await ctx.send(self.msg["exception"]["enf"].format(file=file), ephemeral=True)

                except commands.ExtensionNotLoaded as enl:
                    logger.exception("%s failed to unload %s: %s", ctx.author, file, enl)
                    await ctx.send(self.msg["exception"]["enl"].format(file=file), ephemeral=True)

                else:
                    logger.info("%s unloaded %s", ctx.author, file)
                    await ctx.send(self.msg["unload"]["succeeded"].format(file=file), ephemeral=True)

        extension = extension.lower()
        if extension == "all":
            for file in config.cog_list:
                await unload_helper(file)

        else:
            await unload_helper(extension)

    @commands.hybrid_command(name="reload", help="reload <filename>")
    @commands.has_any_role(config.admin_role_id, config.tester_role_id)
    async def reload(self, ctx, extension):
        """
        Reload an extension in the bot.

        This command can be used by admin and tester.

        Parameters
        ----------
        ctx : commands.Context
            Represent the context in which a command is being invoked.
        extension : str
            The name of the extension to be reloaded or "all" to reload all extensions.
        """

        @staticmethod
        async def reload_helper(file):
            """
            Helper function to reload a single extension.

            Parameters
            ----------
            file : str
                The name of the file to be reloaded as an extension.
            """
            try:
                if not file.startswith("__") and file.endswith(".py"):
                    file = file[:-3]
                    await self.bot.reload_extension(f"cogs.{file}")

            except commands.errors.MissingAnyRole as mar:
                logger.exception("%s failed to reload %s: %s", ctx.author, file, mar)
                await ctx.send(self.msg["exception"]["mar"], ephemeral=True)

            except commands.ExtensionNotFound as enf:
                logger.exception("%s failed to reload %s: %s", ctx.author, file, enf)
                await ctx.send(self.msg["exception"]["enf"].format(file=file), ephemeral=True)

            except commands.ExtensionNotLoaded as enl:
                logger.exception("%s failed to reload %s: %s", ctx.author, file, enl)
                await ctx.send(self.msg["exception"]["enl"].format(file=file), ephemeral=True)

            else:
                logger.info("%s reloaded %s", ctx.author, file)
                await ctx.send(self.msg["reload"]["succeeded"].format(file=file), ephemeral=True)

        extension = extension.lower()
        if extension == "all":
            for file in config.cog_list:
                await reload_helper(file)

        else:
            await reload_helper(extension)


async def setup(bot):
    await bot.add_cog(ExtensionManager(bot))
