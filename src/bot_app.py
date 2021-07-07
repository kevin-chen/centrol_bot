import asyncio
from log import logger
from configs.config import CentrolConfig
from quart import Quart, render_template
# from moesifwsgi import MoesifMiddleware

import logging

# moesif_settings = {'MOESIF_ID'}
# app.wsgi_app = MoesifMiddleware(app.wsgi_app, moesif_settings)

logger.setup_logger()
import os
import asyncio
from hypercorn.asyncio import serve
from hypercorn.config import Config

loop = asyncio.get_event_loop()

app = Quart(__name__, template_folder="web", static_folder="web", static_url_path="")
config = CentrolConfig()
app.config.from_object(config)
log = logging.getLogger(__name__)

from discord.centrol_discord import DiscordClient
from telegram.centrol_telegram import TelegramClient

discord = DiscordClient()
telegram = TelegramClient()


@app.route("/")
async def hello_world():
    return await render_template("index.html")


# loop.create_task(app.run_task())
loop.create_task(telegram.connect())
loop.create_task(discord.connect())

if os.getenv("ENV") == "prod":
    port = os.getenv("PORT")
    config = Config()
    config.bind = ["0.0.0.0:" + port]

    log.info(f"\n\nRunning on: {config.bind}\n\n")
    loop.run_until_complete(serve(app, config))
else:
    loop.run_until_complete(serve(app, Config()))
