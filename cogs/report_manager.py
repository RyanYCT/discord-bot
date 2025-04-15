import json
import locale
import logging
from datetime import datetime as dt
from typing import Any, Dict

import discord
import pandas as pd
import requests
from discord.ext import commands

import settings
import utilities

logger = logging.getLogger("report_manager")


locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

class ReportManager(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.bot_message = utilities.load_json(settings.bot_message_template)

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
    def map_enhance_level(number: int) -> str:
        enhance_map = {0: "_", 1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI", 7: "VII", 8: "VIII", 9: "IX", 10: "X"}
        return enhance_map.get(number, str("_"))

    @staticmethod
    def format_thousands(number: int) -> str:
        return locale.format_string("%d", number, grouping=True)
    
    @commands.hybrid_command(name="health", description="Check the status of the API server")
    @commands.has_any_role(settings.guild["role"]["admin"]["id"], settings.guild["role"]["tester"]["id"])
    async def health(self, ctx: commands.Context) -> None:
        """
        Checks the status of the API server and sends a message with the status.

        Parameters
        ----------
        ctx : discord.ext.commands.Context
            The context in which the command was invoked.
        """
        try:
            response = requests.get(f"{settings.api_url}/health", timeout=10)
            if response.status_code == 200:
                await ctx.send(f"API server is online and reachable: {response.status_code}")
            else:
                logger.warning("status code: %s", response.status_code)
                await ctx.send(f"API server returned status code: {response.status_code}")

        except requests.exceptions.RequestException as re:
            logger.exception("Failed to ping API server: %s", re)
            await ctx.send(f"An error occurred while checking health of the API server: {re}")

    def generate_report(self, json_string: Dict[str, Any], template: Dict[str, Any], report_type: str, category: str = None, name: str = None, enhance: int = None, period: int = 7) -> discord.Embed:
        """
        Generate a formatted report based on the provided data and filters.

        Parameters
        ----------
        json_string : Dict[str, Any]
            The JSON response form the API containing report data
        template : Dict[str, Any]
            The template for formatting the report
        report_type : str
            Type of report ("profit" or "trends")
        category : str, optional
            Category filter ("buff" or "costume" or "accessory")
        name : str, optional
            Item name filter
        enhance_level : int, optional
            Enhancement level filter (0 - 10)
        period : int, optional
            Period filter for trends report (1 - 30 days)

        Returns
        -------
        discord.Embed
            The formatted report as a Discord embed object
        """
        logger.debug(f"Generating report for {report_type=}, {category=}, {name=}, {enhance=}, {period=}")

        # Extract data from the API responsed json string
        report_time = dt.fromisoformat(json_string["timestamp"])
        report_data = json_string["data"]

        # Process report content
        df = pd.DataFrame(report_data)
        logger.debug(f"DataFrame shape: {df.shape}")

        # Apply filters if provided
        if category:
            # Filter by category
            df = df[df["category"] == category]
            template["description"] = template["description"] + f"\nFilter by category: {category}"
        if name:
            # Filter by item name
            df = df[df["name"].str.contains(name, case=False)]
            template["description"] = template["description"] + f"\nFilter by item name: {name}"
        if enhance:
            # Filter by enhance level
            df = df[df["enhance"].astype(int) == enhance]
            template["description"] = template["description"] + f"\nFilter by enhance level: {enhance}"
        if period:
            template["description"] = template["description"] + f"\nWithin {period} days"

        # Construct embed message
        embed = discord.Embed()

        # Message head
        embed.title = template["title"]
        embed.description = template["description"]

        # Message footer
        footer_text = template["footer"]["text"]
        footer_icon_url = template["footer"]["icon_url"].format(icon_url=self.get_avatar_url(self.bot.user))
        embed.set_footer(text=footer_text, icon_url=footer_icon_url)

        # Get the field template
        field_template = template["fields"][0]

        # Construct fields based on report type
        try:
            # Up to 18 items or available data
            max_items = min(18, len(df))
            for i in range(max_items):
                row = df.iloc[i]

                # Field value, format field value based on report type
                if report_type == "profit":
                    # Field name
                    item_category = row["category"]
                    item_enhance = self.map_enhance_level(row["enhance"])
                    item_name = row["name"]
                    field_name = field_template["name"].format(
                        category=item_category,
                        enhance=item_enhance,
                        name=item_name
                    )
                    # Prepare item's stat
                    item_price = self.format_thousands(row["price"])
                    item_profit = self.format_thousands(row["profit"])
                    item_rate = f"{row['rate']:.3f}"
                    item_stock = row["stock"]
                    # Field value for that item
                    field_value = field_template["value"].format(
                        category=item_category,
                        price=item_price,
                        profit=item_profit,
                        rate=item_rate,
                        stock=item_stock
                    )

                if report_type == "trends":
                    # Field name
                    item_enhance = self.map_enhance_level(row["enhance"])
                    item_name = row["name"]
                    field_name = field_template["name"].format(
                        enhance=item_enhance,
                        name=item_name
                    )
                    # Prepare item's stat
                    item_category = row["category"]
                    item_price = self.format_thousands(row["price"])
                    item_stock = row["stock"]
                    item_volume_change = row["volumechange"]
                    item_average_trades = row["averagetradesperday"]
                    # Field value for that item
                    field_value = field_template["value"].format(
                        category=item_category,
                        price=item_price,
                        stock=item_stock,
                        volumechange=item_volume_change,
                        averagetradesperday=f"{item_average_trades:.3f}"
                    )

                # Field inline
                field_inline = field_template["inline"]

                embed.add_field(
                    name=field_name,
                    value=field_value,
                    inline=field_inline
                )

            # Add the reference field
            reference_field_template = template["fields"][-1]
            ps_name = reference_field_template["name"]
            ps_value = reference_field_template["value"]
            ps_inline = reference_field_template["inline"]
            embed.add_field(
                name=ps_name,
                value=ps_value,
                inline=ps_inline
            )

            # Set timestamp
            embed.timestamp = report_time
            return embed

        except IndexError as ie:
            logger.error("Error adding fields: %s", ie)
        except KeyError as ke:
            logger.error("Missing required field in data: %s", ke)

    @commands.hybrid_command(name="report", description="report <report_type> [category] [name] [enhance] [period]")
    @commands.has_any_role(settings.guild["role"]["doge"]["id"])
    async def report(self, ctx: commands.Context, report_type: str, category: str = None, name: str = None, enhance: str = None, period: str = None) -> None:
        """
        Fetches the latest report from the API server and sends it as an embedded message.

        Parameters
        ----------
        ctx : discord.ext.commands.Context
            The context in which the command was invoked.
        report_type : str
            "p" for profit report
            "t" for trends report
        category : str, optional
            Can be either:
            "buff" or "costume" or "accessory"
        name : str, optional
            Filter by item name
        enhance : str, optional
            Filter by enhancement level (0 - 10)
        period : str, optional
            Filter by period (1 - 30 days), available for trends report only.

        Raises
        ------
        requests.exceptions.RequestException
            If there is an error while making the request to the API server.
        """
        logger.debug(f"Report command invoked by {ctx.author} with args: {report_type=}, {category=}, {name=}, {enhance=}, {period=}")
        try:            
            # Process report type
            match report_type:
                case "profit" | "p":
                    template = utilities.load_json(settings.profit_report_template)
                    report_type = "profit"
                case "trends" | "t":
                    template = utilities.load_json(settings.trends_report_template)
                    report_type = "trends"
                case _:
                    await ctx.send(f"Invalid report type: {report_type}")
                    return

            # Process filters
            category = category.lower() if category is not None else None
            name = name.lower() if name is not None else None
            enhance = int(enhance) if enhance is not None else None
            period = int(period) if period is not None else None

            logger.debug(f"{report_type=}, {category=}, {name=}, {enhance=}, {period=}")

            # Requests report from API server
            params = {"period": period}
            response = requests.get(
                f"{settings.api_url}/report/{report_type}",
                params={key: value for key, value in params.items() if value is not None}
            )
            logger.debug(f"Request URL: {response.url}")
            logger.debug(f"API response: {response.status_code}")

            if response.status_code == 200:
                json_string = response.json()
                # Generate and send report
                embed = self.generate_report(
                    json_string,
                    template=template,
                    report_type=report_type,
                    category=category,
                    name=name,
                    enhance=enhance,
                    period=period
                )
                await ctx.send(embed=embed)

            else:
                logger.warning("status code: %d", response.status_code)
                await ctx.send(f"status code: {response.status_code}")

        except requests.exceptions.RequestException as re:
            await ctx.send(f"An error occurred: {re}")



async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ReportManager(bot))
