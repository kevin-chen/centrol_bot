import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from configs import user_messages as user_msgs
from dotenv import load_dotenv

from centrol.get_data import (
    get_latest_crypto_price,
    get_latest_stock_price,
)
import pyjokes

from centrol.stocks import send_crypto_order
from typing import Tuple
from centrol.user import CentrolUser

log = logging.getLogger(__name__)

load_dotenv()

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
        self.user = CentrolUser()

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
                user_msgs.HELP.format(op="/"),
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

            if message.text.startswith("/buy crypto mkt"):
                data = "".join(message.content.split("/buy crypto mkt")).strip().upper()
                try:
                    crypto_pair, amount = data.split(" ")
                except:
                    return await message.reply(user_msgs.EXAMPLE_BUY_ORDER.format(op="!"))

                success, msg = await self.buy_crypto(
                    message, crypto_pair, amount, "buy-mkt"
                )

                return await message.reply(msg)

            if message.text.startswith("/sell crypto mkt"):
                data = (
                    "".join(message.content.split("/sell crypto mkt")).strip().upper()
                )
                try:
                    crypto_pair, amount = data.split(" ")
                except:
                    return await message.reply(
                        user_msgs.EXAMPLE_SELL_ORDER.format(op="!")
                    )

                success, msg = await self.buy_crypto(
                    message, crypto_pair, amount, "sell-mkt"
                )

                return await message.reply(msg)

            if message.text.startswith("/add-token coinbase"):
                data = "".join(message.content.split("/add-token coinbase")).strip()
                try:
                    token, passphrase, secret = data.split(" ")
                except:
                    return await message.reply(
                        user_msgs.FAILED_TOKEN_ADD.format(op="!")
                    )
                success = self.user.add_coinbase_token(
                    str(message.author.id), token, passphrase, secret, "sandbox"
                )

                if success:
                    return await message.reply("Added token successully")
                else:
                    return await message.reply("Failed to add token")
        
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
