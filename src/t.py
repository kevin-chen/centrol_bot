import asyncio
from log import logger

from quart import Quart, render_template

logger.setup_logger()
import discord
import os

app = Quart(__name__, template_folder="web")
discord_client = discord.Client()


# @app.before_serving
# async def before_serving():
#    loop = asyncio.get_event_loop()
#    await discord_client.login(os.getenv("DISCORD_CLIENT_ID"))


@discord_client.event
async def on_message(message):

    if message.author == discord_client.user:
        return

    if message.content.startswith("!hello"):
        await message.channel.send("Hello!")


@app.route("/")
async def hello_world():
    return await render_template("index.html")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(app.run_task())

    discord_client.run(os.getenv("DISCORD_CLIENT_ID"))
