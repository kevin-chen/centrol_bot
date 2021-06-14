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
        <body style="background-color:black;color:white;">
            <p style="text-align:center"><img src="https://logo.clearbit.com/https://centrol.io"></p>
            <h1 style="text-align:center">Welcome to the Centrol Trader Bot</h1>
            <p style="text-align:center">The Trader Bot is a simple tool that connects to your discord server and can serve a whole bunch of awesome financial queries. Check out our Github repo for more information.</p>
        </body>
        <div style="position:absolute;bottom:0;right:0;padding-right:5px;padding-bottom:5px">
            <a href="https://centrol.io/terms.html">Terms</a> | <a href="https://centrol.io/privacy.html">Privacy</a> | © 2021 Centrol.io
            </div>
        </html>"""

if __name__ == "__main__":
    app.run(threaded=True, port=5000)
  
