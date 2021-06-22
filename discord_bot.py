from centrol.get_data import (
    get_latest_crypto_price,
    get_latest_stock_price,
)
import discord
from log import logger
import pyjokes
import os

logger.setup_logger()

client = discord.Client()

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):

    if message.author == client.user:
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


client.run(os.getenv("DISCORD_CLIENT_ID"))