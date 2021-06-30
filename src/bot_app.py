import asyncio
from log import logger
from configs.config import CentrolConfig
from quart import Quart, render_template
from centrol.get_data import (
    get_latest_crypto_price,
    get_latest_stock_price,
)
import pyjokes

logger.setup_logger()
import discord
import os
import asyncio
from aiogram import Bot, Dispatcher, types

app = Quart(__name__, template_folder="web")
config = CentrolConfig()
app.config.from_object(config)

discord_client = discord.Client()
tele_bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
tele_dp = Dispatcher(tele_bot)

# @app.before_serving
# async def before_serving():
#    loop = asyncio.get_event_loop()
#    await discord_client.login(os.getenv("DISCORD_CLIENT_ID"))

### Discord
@discord_client.event
async def on_message(message):

    if message.author == discord_client.user:
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

    if message.content.startswith("!buy"):
        sym = "".join(message.content.split("!buy")).strip().lower()
        await message.author.send(
            f"""
Hi!

You just tried to buy a stock with the Centrol Trading bot. To process this we need to first connect with an Alpaca account.

1. If you don't have a alpaca account, first create one using the link below.
https://alpaca.markets/algotrading

2. You can then either fund your account or using a virtual account (paper trading) to try out the bot!

3. Connect your alpaca account using the below link:
https://centrol.io/connect_alpaca

"""
        )


####
#### Telegram


async def start_handler(event: types.Message):
    await event.answer(
        f"Hello, {event.from_user.get_mention(as_html=True)} 👋!",
        parse_mode=types.ParseMode.HTML,
    )


@tele_dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply(
        """
Hello from the Centrol Trader Bot 👋

_To get stock data: _
    ```
    /s -> stock
    /s AAPL```

_To get cryptocurrency data: _
    ```
    /c -> crypto
    /c BTC```

By default we provide USD prices. To get data for EUR or GBP, simply add currency as a suffix. e.g. /c BTCEUR.

*Unfortunately at this time we can only provide price data for crypto tokens, we are looking to provide more data as we grow. *

If you have any suggestions or feature requests, add them here: https://share.centrol.io/e/feedback""",
    )


# Decorated message handler - this only accepts one arg: the message.
@tele_dp.message_handler()
async def send_reply(message):
    if message.text.startswith("/s"):
        sym = "".join(message.text.split("/s")).strip().upper()
        data = get_latest_stock_price(sym)
        await message.reply(data)

    if message.text.startswith("/c"):
        sym = "".join(message.text.split("/c")).strip().lower()
        data = get_latest_crypto_price(sym)
        await message.reply(data)

    if message.text.startswith("/j"):
        await message.reply(pyjokes.get_joke(category="neutral"))

    # todo: testing whether this will work and what the latest price is compared to market price
    if message.text.startswith("/iprice"):
        sym = "".join(message.text.split("/iprice")).strip().lower()
        data = get_latest_iex_stock_price(sym)
        await message.reply(data)


async def tele():
    try:
        tele_dp.register_message_handler(start_handler, commands={"start", "restart"})
        await tele_dp.start_polling()
    finally:
        await tele_bot.close()


####


@app.route("/")
async def hello_world():
    return await render_template("index.html")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(app.run_task())
    loop.create_task(tele())

    discord_client.run(os.getenv("DISCORD_CLIENT_ID"))
