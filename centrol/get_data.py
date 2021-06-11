import requests
import logging
import json

log = logging.getLogger(__name__)


def get_latest_price(sym: str):
    f_url = f"https://api.centrol.io/finance/stock/{sym}/quote"
    r = requests.get(f_url)
    if r.status_code == 200:
        data = json.loads(r.content)
        percent_change = "{:.3f} %".format(100 * (data["changePercent"]))
        data["percent_change"] = percent_change
        return data
    else:
        log.error(f"Faild to get {r.status_code}. {sym}")
        return ""
