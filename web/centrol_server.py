from configs.config import CentrolConfig
from flask import Flask

app = Flask(__name__)

config = CentrolConfig()

app.config.from_object(config)


@app.route("/")
def hello_world():
    return "Hello"


if __name__ == "__main__":
    app.run(
        host=app.config.get("URL"),
        port=app.config.get("PORT"),
        debug=app.config.get("DEBUG"),
    )
