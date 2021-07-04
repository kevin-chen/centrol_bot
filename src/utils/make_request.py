import requests
import logging
from typing import Optional

log = logging.getLogger(__name__)


def get(url: str) -> Optional[bytes]:
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.content
    except Exception as e:
        log.error(f"Failed to fetch data: {r.status_code} {e}")
        return None
