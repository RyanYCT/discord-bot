import json
import locale
import logging
from datetime import datetime
from typing import Dict, Any

import discord
import pandas as pd
import requests
from discord.ext import commands

import settings
import utilities

logger = logging.getLogger(__name__)


locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

class ReportManager(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.bot_message = utilities.load_json(settings.bot_message_template)

    @staticmethod
    def convertible_to_int(string: str) -> bool:
        try:
            int(string)
            return True
        except ValueError:
            return False

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

    @staticmethod
    def map_enhance(number: int) -> str:
        enhance_map = {0: "_", 1: "I", 2: "II", 3: "III", 4: "IV", 5: "V"}
        return enhance_map.get(number, str("_"))

    @staticmethod
    def format_thousands(number: int) -> str:
        return locale.format_string("%d", number, grouping=True)

    def generate_report(self, json_string: Dict[str, Any], template: Dict[str, Any], report_type: str = "overall", keyword: str = None) -> discord.Embed:
        logger.debug(f"Generating report for {report_type=}, {keyword=}")

        # Extract data from the API responsed json string
        report_time = datetime.fromisoformat(json_string["report_time"])
        report_data = json.loads(json_string["report"])

        # Construct embed message
        embed = discord.Embed()
        # Message head
        embed.title = template["title"]
        embed.description = template["description"]
        # Message footer
        footer_text = template["footer"]["text"]
        footer_icon_url = template["footer"]["icon_url"].format(icon_url=self.get_avatar_url(self.bot.user))
        embed.set_footer(text=footer_text, icon_url=footer_icon_url)
        # Message body
        df = pd.DataFrame(report_data)
        # If keyword is provided, filter the dataframe
        if keyword:
            # Set title to the keyword
            embed.title = template["title"].format(keyword=keyword)
            # If the keyword is number, filter by enhancement level
            if self.convertible_to_int(keyword):
                df = df[df["enhance"] == int(keyword)]
            # Else filter by item name
            else:
                df = df[df["name"].str.contains(keyword, case=False)]
        # Construct fields up to the top 18 items
        try:
            for i in range(18):
                row = df.iloc[i]
                # Field name
                item_enhance = self.map_enhance(row["enhance"])
                item_name = row["name"]
                field_name = template["fields"][i]["name"].format(enhance=item_enhance, name=item_name)
                # Field value
                item_price = self.format_thousands(row["price"])
                item_profit = self.format_thousands(row["profit"])
                item_rate = f"{row['rate']:.3f}"
                field_value = template["fields"][i]["value"].format(
                    price=item_price, 
                    profit=item_profit, 
                    odds=item_rate, 
                    stock=row["stock"]
                )
                # Field inline
                field_inline = template["fields"][i]["inline"]
                embed.add_field(name=field_name, value=field_value, inline=field_inline)

        except IndexError as ie:
            logger.error(f"{ie=}")
        
        # Last field for postscript
        ps_name = template["fields"][-1]["name"]
        ps_value = template["fields"][-1]["value"]
        ps_inline = template["fields"][-1]["inline"]
        embed.add_field(name=ps_name, value=ps_value, inline=ps_inline)
        embed.timestamp = report_time
        return embed

    @commands.hybrid_command(name="report", description="report <option>")
    @commands.has_any_role(settings.guild["role"]["subscriber"]["id"])
    async def report(self, ctx: commands.Context, option: str) -> None:
        """
        Fetches the latest report from the API server and sends it as an embedded message.

        Parameters
        ----------
        ctx : discord.ext.commands.Context
            The context in which the command was invoked.
        
        option : str
            "a" for overall, <keyword> and [0-5] for filtering item and enhancement level.

            The option to generate the report.
            If "overall", "o", "all" or "a" is provided, the overall report will be sent.
            If the option is a string, the report will be filtered by the provided keyword.
            If the option is a number, the report will be filtered by the enhancement level.
            If no option is provided, the overall report will be sent by default.

        Raises
        ------
        requests.exceptions.RequestException
            If there is an error while making the request to the API server.
        """
        try:
            # Requests latest report from API server
            response = requests.get(f"{settings.api_url}/report")
            if response.status_code == 200:
                json_string = response.json()
                # Based on the type of report, load the corresponding template
                template = None
                option.lower()
                match option:
                    case "overall" | "o" | "all" | "a":
                        template = utilities.load_json(settings.overall_report_template)
                        report_type = "overall"
                        keyword = None
                    case _:
                        template = utilities.load_json(settings.item_report_template)
                        report_type = "item"
                        keyword = option.title()
                await ctx.send(embed=self.generate_report(json_string, template=template, report_type=report_type, keyword=keyword))

            else:
                logger.warning("status code: %d", response.status_code)
                await ctx.send(f"status code: {response.status_code}")

        except requests.exceptions.RequestException as re:
            await ctx.send(f"An error occurred: {re}")

    @commands.hybrid_command(name="ping", description="Check the status of the API server")
    @commands.has_any_role(settings.guild["role"]["admin"]["id"], settings.guild["role"]["tester"]["id"])
    async def ping(self, ctx: commands.Context) -> None:
        """
        Checks the status of the API server and sends a message with the status.

        Parameters
        ----------
        ctx : discord.ext.commands.Context
            The context in which the command was invoked.
        """
        try:
            response = requests.get(f"{settings.api_url}/ping")
            if response.status_code == 200:
                await ctx.send("API server is online and reachable.")
            else:
                logger.warning("status code: %d", response.status_code)
                await ctx.send(f"API server returned status code: {response.status_code}")

        except requests.exceptions.RequestException as re:
            logger.exception("Failed to ping API server: %s", re)
            await ctx.send(f"An error occurred while pinging the API server: {re}")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ReportManager(bot))
