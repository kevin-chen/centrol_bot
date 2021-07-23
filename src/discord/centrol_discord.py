import logging
from src.centrol.stocks import send_crypto_order
from configs import user_messages as user_msgs
import discord
import os
from centrol.get_data import (
    get_latest_crypto_price,
    get_latest_stock_price,
    get_stock_chart,
    get_crypto_chart,
)
import asyncio
import pyjokes
from centrol.user import CentrolUser
from configs import user_messages as user_msgs
from typing import Tuple

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
        self.user = CentrolUser()

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
                await message.channel.send(user_msgs.HELP.format(op="!"))

            if message.content.startswith("!j"):
                await message.channel.send(pyjokes.get_joke(category="neutral"))

            # TODO: need to set up url for https://centrol.io/connect_alpaca <-- currently does not exist.
            # if message.content.startswith("!buy"):
            #    sym = "".join(message.content.split("!buy")).strip().lower()
            #
            #    success, msg = buy_stock(message)
            #    if success:
            #        return "Completed!"
            #    else:
            #        await message.author.send(msg)

            # !buy crypto btc 0.00001
            if message.content.startswith("!buy crypto mkt"):
                data = "".join(message.content.split("!buy crypto mkt")).strip().upper()
                try:
                    crypto_pair, amount = data.split(" ")
                except:
                    return await message.author.send(
                        user_msgs.EXAMPLE_BUY_ORDER.format(op="!")
                    )

                success, msg = await self.buy_crypto(
                    message, crypto_pair, amount, "buy-mkt"
                )

                return await message.author.send(msg)

            # !buy crypto btc 0.00001
            if message.content.startswith("!sell crypto mkt"):
                data = (
                    "".join(message.content.split("!sell crypto mkt")).strip().upper()
                )
                try:
                    crypto_pair, amount = data.split(" ")
                except:
                    return await message.author.send(
                        user_msgs.EXAMPLE_SELL_ORDER.format(op="!")
                    )

                success, msg = await self.buy_crypto(
                    message, crypto_pair, amount, "sell-mkt"
                )

                return await message.author.send(msg)

            if message.content.startswith("!add-token coinbase"):
                data = "".join(message.content.split("!add-token coinbase")).strip()
                try:
                    token, passphrase, secret = data.split(" ")
                except:
                    return await message.author.send(
                        user_msgs.FAILED_TOKEN_ADD.format(op="!")
                    )
                success = self.user.add_coinbase_token(
                    str(message.author.id), token, passphrase, secret, "sandbox"
                )

                if success:
                    return await message.author.send("Added token successully")
                else:
                    return await message.author.send("Failed to add token")

            # Stock Price Request
            if message.content.startswith("!s"):
                sym = "".join(message.content.split("!s")).strip().upper()
                data = get_latest_stock_price(sym)
                
                c = discord.Embed()
                chart = c.set_ImageURL(get_stock_chart(sym))
                
                return await message.channel.send(data)
                return await message.channel.send(chart)

            # Crypto Price Request
            if message.content.startswith("!c"):
                sym = "".join(message.content.split("!c")).strip().lower()
                data = get_latest_crypto_price(sym)
                
                c = discord.Embed()
                chart = c.set_ImageURL(get_crypto_chart(sym))
                
                return await message.channel.send(data)
                return await message.channel.send(chart)
                

    async def buy_crypto(self, message, crypto_pair, price, typ) -> Tuple[bool, str]:
        if not self.user.check_user(message.author.id):
            self.user.create_user("", message.author.id, message.author.name, "discord")

        resp = send_crypto_order(
            message.author.id, crypto_pair, price, typ, "sandbox", "discord"
        )
        if resp["msg"] == "TOKEN_MISSING":
            return False, user_msgs.COINBASE_CONNECT.format(op="!")

        if resp["flag"] == True:
            return True, user_msgs.SUCCESSFUL_ORDER.format(
                url="https://public.sandbox.pro.coinbase.com/orders"
            )

        return False, resp["msg"]
