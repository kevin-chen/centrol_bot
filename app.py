from configs.config import CentrolConfig
from flask import Flask

app = Flask(__name__)

config = CentrolConfig()

app.config.from_object(config)


@app.route("/")
def hello_world():
    return "Hello"


if __name__ == "__main__":
    app.run(threaded=True, port=5000)
