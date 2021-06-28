from centrol.get_data import (
    get_latest_crypto_price,
    get_latest_stock_price,
    get_latest_iex_stock_price,
)
import telebot
from log import logger
import pyjokes
import os
import time

logger.setup_logger()

bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"), parse_mode="Markdown") # can set the parse_mode to HTML or Markdown

# Defining a message handler which handles /start and /help commands
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, """
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

If you have any suggestions or feature requests, add them here: https://share.centrol.io/e/feedback""")

# Decorated message handler - this only accepts one arg: the message.
@bot.message_handler(func=lambda m: True)
def send_reply(message):
    if message.text.startswith("/s"):
        sym = "".join(message.text.split("/s")).strip().upper()
        data = get_latest_stock_price(sym)
        bot.reply_to(message, data)

    if message.text.startswith("/c"):
        sym = "".join(message.text.split("/c")).strip().lower()
        data = get_latest_crypto_price(sym)
        bot.reply_to(message, data)

    if message.text.startswith("/j"):
        bot.reply_to(message, pyjokes.get_joke(category="neutral"))

# todo: testing whether this will work and what the latest price is compared to market price
    if message.text.startswith("/iprice"):
        sym = "".join(message.text.split("/c")).strip().lower()
        data = get_latest_iex_stock_price(sym)
        bot.reply_to(message, data)


while True:
    try:
        bot.polling(none_stop=True)
        # ConnectionError and ReadTimeout because of possible timout of the requests library
        # maybe there are others, therefore Exception
    except Exception:
        time.sleep(15)
