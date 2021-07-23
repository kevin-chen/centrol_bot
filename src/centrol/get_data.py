import requests
import logging
import json
import random
from utils.make_request import get

log = logging.getLogger(__name__)

# Stock price provided from IEX Stock Quote call. stock price + peripheral information about the security
def get_latest_stock_price(sym: str):
    f_url = f"https://api.centrol.io/finance/stock/{sym}/quote"
    r = get(f_url)
    if r is not None:
        if r == b"":
            return f"D'oh! {sym} not found 😱"

        data = json.loads(r)
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

https://elite.finviz.com/chart.ashx?t={data["symbol"]}&ty=c&ta=st_c,sch_200p,rsi_b_14,macd_b_12_26_9,sma_50,sma_200,sma_20&p=d&s=lx=${random.uniform(0,1)}.png

"""
        return resp
    else:
        log.error(f"Failed to get: {sym}")
        return "This is embarrassing. We are having server issues."


# Crypto price provided from IEX Crypto Quote call
# TODO: [CENTROL-13] considering the use of CoinGecko for this instead of IEX so that we can get more information instead of just price for a handful of crypto's
def get_latest_crypto_price(sym: str):

    if not sym[-3:] in ["usd", "gbp", "eur"]:
        sym += "usd"

    f_url = f"https://api.centrol.io/finance/crypto/{sym}/quote"
    r = get(f_url)

    if r is not None:
        if r == b"":
            return f"D'oh! {sym.upper()[:-3]} not found 😯"

        data = json.loads(r)
        p = ("%.5f" % float(data["latestPrice"])).rstrip("0").rstrip(".")
        resp = f"""
```yaml
{data["symbol"]}

Price: {p}
```

https://elite.finviz.com/fx_image.ashx?{data["symbol"]}_m5_l.png


"""
        return resp
    else:
        log.error(f"Faild to get: {sym}")
        return "This is embarrassing. We are having server issues."
