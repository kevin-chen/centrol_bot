from configs.config import CentrolConfig
import requests
import logging
from typing import Optional, Dict, Any
from flask import current_app
from configs.config import CentrolConfig

log = logging.getLogger(__name__)
config = CentrolConfig()

# TODO: look into working inside app context and pull from flask config
_token = config.BOT_TOKEN
_headers = {"Authorization": f"Bearer {_token}"}

_timeout = 5


def get(url: str) -> Optional[bytes]:
    try:
        # don't put sensitive content into logs
        log.info("Fetching: {}".format(url.split("?")[0]))
        r = requests.get(url, headers=_headers, timeout=_timeout)
        if r.status_code == 200:
            return r.content
        else:
            log.error(f"Failed to fetch data: {r.status_code}")
    except Exception as e:
        log.error(f"Failed to fetch data: {e}")
        return None


def post(url: str, data: Dict[str, Any]) -> Optional[bytes]:
    try:
        log.info("Fetching: {}".format(url))
        r = requests.post(url, headers=_headers, json=data, timeout=_timeout)
        if r.status_code == 200:
            return r.content
        else:
            log.error(f"Failed to fetch data: {r.status_code}")
    except Exception as e:
        log.error(f"Failed to fetch data: {e}")
    return None
