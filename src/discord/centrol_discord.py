import logging
import discord
import os
from centrol.get_data import (
    get_latest_crypto_price,
    get_latest_stock_price,
)
import asyncio
import pyjokes

log = logging.getLogger(__name__)


class DiscordClient:
    async def connect(self):
        token = os.getenv("DISCORD_CLIENT_ID")

        try:
            await self.client.login(token)
            self.loop.create_task(self.client.connect())
        finally:
            log.warning("stopping")

    async def send_broadcast(self):
        user = await self.client.fetch_user("id")

        await user.send("This is a test broadcast")
        return ""

    def __init__(self):
        log.info("Setting up discord client")
        self.client = discord.Client()
        self.loop = asyncio.get_event_loop()

        @self.client.event
        async def on_ready():
            log.info("Logged in as")
            log.info(self.client.user.name)
            log.info(self.client.user.id)

        @self.client.event
        async def on_message(message):

            if message.author == self.client.user:
                return

            if message.content.startswith("!hello"):
                await message.channel.send("Hello!")

            if message.content.startswith("!help"):
                await message.channel.send(
                    f"""
        Hello from the Centrol Trader Bot 👋

        _To get stock data: _
            ```
            !s -> stock
            !s AAPL
            ```

        _To get cryptocurrency data: _
            ```
            !c -> crypto
            !c BTC
            ```

        By default we provide USD prices. To get data for EUR or GBP, simply add currency as a suffix. e.g. !c BTCEUR.

        *Unfortunately at this time we can only provide price data for crypto tokens, we are looking to provide more data as we grow. *

        If you have any suggestions or feature requests, add them here: https://share.centrol.io/e/feedback"""
                )

            if message.content.startswith("!j"):
                await message.channel.send(pyjokes.get_joke(category="neutral"))

            if message.content.startswith("!s"):
                sym = "".join(message.content.split("!s")).strip().upper()
                data = get_latest_stock_price(sym)
                await message.channel.send(data)

            if message.content.startswith("!c"):
                sym = "".join(message.content.split("!c")).strip().lower()
                data = get_latest_crypto_price(sym)
                await message.channel.send(data)

            # TODO: need to set up url for https://centrol.io/connect_alpaca <-- currently does not exist.
            if message.content.startswith("!buy"):
                sym = "".join(message.content.split("!buy")).strip().lower()
                await message.author.send(
                    f"""
        Hi!

        You just tried to buy a stock with the Centrol Trading bot. To process this we need to first connect with an Alpaca account.

        1. If you don't have a Alpaca account, first create one using the link below.
        https://alpaca.markets/algotrading

        2. You can then either fund your account or using a virtual account (paper trading) to try out the bot!

        3. Connect your Alpaca account using the below link:
        https://centrol.io/connect_alpaca

        """
                )
