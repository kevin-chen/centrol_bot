import requests
import logging
import json

log = logging.getLogger(__name__)


def get_latest_stock_price(sym: str):
    f_url = f"https://api.centrol.io/finance/stock/{sym}/quote"
    r = requests.get(f_url)
    if r.status_code == 200:
        data = json.loads(r.content)
        percent_change = "{:.3f} %".format(100 * (data["changePercent"]))
        data["percent_change"] = percent_change

        resp = f"""
```yaml
{data["symbol"]} {data["companyName"]}

Price: {data["latestPrice"]} ({data["percent_change"]})

Market cap: {data["marketCap"]:,}
Previous volume: {data["previousVolume"]:,}
Previous close: {data["previousClose"]:,}
Average 30-day volume: {data["avgTotalVolume"]:,}
52-week High: {data["week52High"]:,}
52-week Low: {data["week52Low"]:,}
```
"""
        return resp
    else:
        log.error(f"Faild to get {r.status_code}. {sym}")
        return ""


def get_latest_crypto_price(sym: str):

    if not sym[-3:] in ["usd", "gbp", "eur"]:
        sym += "usd"

    f_url = f"https://api.centrol.io/finance/crypto/{sym}/quote"
    r = requests.get(f_url)

    if r.content == b"":
        return f"{sym.upper()[:-3]} Not supported"

    if r.status_code == 200:
        data = json.loads(r.content)
        print(data)
        p = ("%.5f" % float(data["latestPrice"])).rstrip("0").rstrip(".")
        resp = f"""
```yaml
{data["symbol"]}

Price: {p}
```
"""
        return resp
    else:
        log.error(f"Faild to get {r.status_code}. {sym}")
        return ""
