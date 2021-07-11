import logging
from utils.make_request import get, post
from configs.config import CentrolConfig
import json

log = logging.getLogger(__name__)


class CentrolUser:
    def __init__(self):
        log.info("Loading centrol user module")
        self.config = CentrolConfig()

    def check_user(self, user: str) -> bool:
        check_url = self.config.SERVER_URL + f"/bot/check_user?user={user}"
        resp = get(check_url)
        if resp is not None:
            data = json.loads(resp)
            return data["flag"]

        return False

    def create_user(self, email: str, c_id: str, name: str, src: str) -> bool:
        create_url = self.config.SERVER_URL + f"/bot/create_user"
        data = {"email": email, "id": str(c_id), "name": name, "src": src}

        resp = post(create_url, data)
        if resp is not None:
            data = json.loads(resp)
            return data["flag"]

        return False

    def add_coinbase_token(self, user, token, passphrase, secret, account_typ) -> bool:
        token_url = self.config.SERVER_URL + f"/bot/add_coinbase_token"
        data = {
            "id": user,
            "token": token,
            "passphrase": passphrase,
            "secret": secret,
            "account_typ": account_typ,
        }

        resp = post(token_url, data)
        if resp is not None:
            data = json.loads(resp)
            return data["flag"]

        return False
