import logging
import discord
from discord.ext import commands
from config import settings
from src import utilities

logger = logging.getLogger(__name__)


class Woof(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.msg = utilities.load_json(settings.WOOF_MESSAGE_JSON)

    @commands.hybrid_command(name="woof", help="Check the key:value pair is implemented correctly.")
    async def woof(self, ctx):
        """
        Sending msg["woof_message"] to the channel where the command was invoked to check the key:value pair is implemented correctly.

        Args:
            ctx (commands.Context): Represents the context in which a command is being invoked under.
        """
        await ctx.send(self.msg["woof_message"])

    @commands.hybrid_command(name="echo", help="Echo the message you input.")
    async def echo(self, ctx):
        """
        Echo the message you input.

        Args:
            ctx (commands.Context): Represents the context in which a command is being invoked under.
        """
        await ctx.send(ctx.message.content)

    # A trail of using interaction
    @commands.hybrid_command(name="echo_i", help="Echo the message you input using interaction.")
    async def echo_i(self, ctx, interaction):
        """
        Echo the message you input using interaction.

        Args:
            ctx (commands.Context): Represents the context in which a command is being invoked under.
            interaction (discord.Interaction): Represents the original interaction response message.
        """
        await interaction.response.defer()
        await interaction.followup.send(ctx.message.content)

    # A trail of using embed message
    @commands.hybrid_command(name="list_commands", help="List available commands.")
    @commands.has_any_role(settings.ADMIN_ROLE_ID, settings.TESTER_ROLE_ID)
    async def list_commands(self, ctx):
        """
        List available commands. Behave like the /help command.

        This command can only be used by admin and tester.

        Args:
            ctx (commands.Context): Represents the context in which a command is being invoked under.
        """
        # Construct the embed message
        title = self.msg["list"]["title"]
        description = self.msg["list"]["description"]
        embed = discord.Embed(title=title, description=description)
        name = self.msg["list"]["name"]
        value = ""
        for command in self.bot.tree.walk_commands():
            value += (f"{command.name} - {command.wrapped.module} - {command.description}\n")
        embed.add_field(name=name, value=value, inline=False)

        await ctx.send(embed=embed)

    @commands.hybrid_command(name="activity", help="Change bot activity")
    async def activity(self, interaction, activity, custom_message):
        """
        Change activity of bot

        Args:
            interaction (discord.Interaction): The interaction object representing the command invocation.
            activity (str): The activity to set.
            *custom_message (str): The custom message to set as the activity if the activity is "Custom".
        """
        match activity:
            case "Playing":
                activity_type = discord.ActivityType.playing
                activity_message = self.msg["activity_message"]["playing"]
            case "Streaming":
                activity_type = discord.ActivityType.streaming
                activity_message = self.msg["activity_message"]["streaming"]
            case "Listening":
                activity_type = discord.ActivityType.listening
                activity_message = self.msg["activity_message"]["listening"]
            case "Watching":
                activity_type = discord.ActivityType.watching
                activity_message = self.msg["activity_message"]["watching"]
            case "Competing":
                activity_type = discord.ActivityType.competing
                activity_message = self.msg["activity_message"]["competing"]
            case _:
                activity_type = discord.ActivityType.custom
                activity_message = custom_message

        await self.bot.change_presence(activity=discord.Activity(type=activity_type, name=activity_message))
        await interaction.response.send_message(f'Activity set to "{activity}"', ephemeral=True)


async def setup(bot):
    await bot.add_cog(Woof(bot))
