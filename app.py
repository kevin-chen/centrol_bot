from configs.config import CentrolConfig
from flask import Flask

app = Flask(__name__)

config = CentrolConfig()

app.config.from_object(config)


@app.route("/")
def hello_world():
    return "<img src="https://logo.clearbit.com/https://centrol.io"></img>If you've made it here, know that you are an exceptional being 🤓. <br>See <a href="https://centrol.io/terms.html">Terms</a> and <a href="https://centrol.io/privacy.html">Privacy</a> @ Centrol.io. <br><br>© 2021 Centrol.io"


if __name__ == "__main__":
    app.run(threaded=True, port=5000)
