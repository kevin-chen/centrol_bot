from configs.config import CentrolConfig
from flask import Flask

app = Flask(__name__)

config = CentrolConfig()

app.config.from_object(config)


@app.route("/")
def hello_world():
    return """<!DOCTYPE html>
        <html>
        <head>
            <title>Centrol Trader Bot</title>
        </head>
        <body style="background-color:black;color:white">
            <img src="https://logo.clearbit.com/https://centrol.io"> 
            <h1>Welcome to the Centrol Trader Bot</h1>
            <p>The Trader Bot is a simple tool that connects to your discord server and can serve a whole bunch of awesome financial queries. Check out our Github repo for more information.</p>
            <div style="text-align:right">
            <a href="https://centrol.io/terms.html">Terms</a> | <a href="https://centrol.io/privacy.html">Privacy</a> | © 2021 Centrol.io
            </div>
        </body>
        </html>"""


if __name__ == "__main__":
    app.run(threaded=True, port=5000)
  