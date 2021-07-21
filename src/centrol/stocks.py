from utils.make_request import post
from centrol.user import CentrolUser
from typing import Tuple
from configs import user_messages as user_msgs
import json
from configs.config import CentrolConfig

user = CentrolUser()

# API_PREFIX = "https://api.centrol.io"
config = CentrolConfig()
API_PREFIX = config.SERVER_URL


def buy_stock(message) -> Tuple[bool, str]:
    if user.check_user(message.author.id):
        return True, ""

    return False, user_msgs.ALPACA_CONNECT


def send_crypto_order(user_id, crypto_pair, price, typ, account_typ, src):
    data = {
        "id": str(user_id),
        "account_typ": account_typ,
        "src": src,
        "crypto_pair": crypto_pair,
        "amount": "",
        "price": price,
        "typ": typ,
    }

    resp = post(API_PREFIX + "/bot/crypto_order", data)
    if resp is not None:
        resp = json.loads(resp)
    return resp
