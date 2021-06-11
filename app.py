from configs.config import CentrolConfig
from flask import Flask

app = Flask(__name__)

config = CentrolConfig()

app.config.from_object(config)


@app.route("/")
def hello_world():
    return "If you've made it here, know that you are an exceptional being 🤓. See Terms and Privacy @ Centrol.io.  © 2021 Centrol.io"


if __name__ == "__main__":
    app.run(threaded=True, port=5000)
