import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types

from centrol.get_data import (
    get_latest_crypto_price,
    get_latest_stock_price,
)
import pyjokes

log = logging.getLogger(__name__)


class TelegramClient:
    async def connect(self):

        try:
            self.tele_dp.register_message_handler(
                self.start_handler, commands={"start", "restart"}
            )
            self.loop.create_task(self.tele_dp.start_polling())
            # await tele_dp.start_polling()
        finally:
            await self.tele_bot.close()

    async def start_handler(self, event: types.Message):
        await event.answer(
            f"Hello, {event.from_user.get_mention(as_html=True)} 👋!",
            parse_mode=types.ParseMode.HTML,
        )

    def __init__(self):
        log.info("Setting up telegram client")

        self.loop = asyncio.get_event_loop()
        token = os.getenv("TELEGRAM_TOKEN")

        self.tele_bot = Bot(
            token=token, parse_mode="Markdown"
        )  # can set the parse_mode to HTML or Markdown
        self.tele_dp = Dispatcher(self.tele_bot)

        @self.tele_dp.message_handler(commands=["start", "help"])
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
        @self.tele_dp.message_handler()
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
