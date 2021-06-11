from centrol.get_data import get_latest_price
import discord
import requests
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
Use:
```
    !s -> stock
    !s AAPL

    !c -> crypto
    !c BTC

    !j -> You might enjoy these if you are a programmer
```
"""
        )

    if message.content.startswith("!j"):
        await message.channel.send(pyjokes.get_joke(category="neutral"))

    if message.content.startswith("!s"):
        sym = "".join(message.content.split("!s")).strip().upper()
        data = get_latest_price(sym)
        await message.channel.send(
            f"""
```yaml
{data["symbol"]} {data["companyName"]}

Price: {data["latestPrice"]} ({data["percent_change"]})

Market cap: {data["marketCap"]:,}
Previous volume: {data["previousVolume"]:,}
Previous close: {data["previousClose"]:,}
Average 30-day volume: {data["avgTotalVolume"]:,}
52-week High: {data["week52High"]:,}
52-week Low: {data["week52Low"]:,}
```                                 
"""
        )


client.run(os.getenv("DISCORD_CLIENT_ID"))
