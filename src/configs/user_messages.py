HELP: str = """
Hello from the Centrol Trader Bot 👋

_To get stock data: _
    ```
    {op}s -> stock
    {op}s AAPL
    ```

_To get cryptocurrency data: _
    ```
    {op}c -> crypto
    {op}c BTC
    ```

By default we provide USD prices. To get data for EUR or GBP, simply add currency as a suffix. e.g. {op}c BTCEUR.

*Unfortunately at this time we can only provide price data for crypto tokens, we are looking to provide more data as we grow. *

If you have any suggestions or feature requests, add them here: https://share.centrol.io/e/feedback

"""

ALPACA_CONNECT: str = """
Hi!

You just tried to buy a stock with the Centrol Trading bot. To process this we need to first connect with an Alpaca account.

1. If you don't have a Alpaca account, first create one using the link below.
https://alpaca.markets/algotrading

2. You can then either fund your account or using a virtual account (paper trading) to try out the bot!

3. Connect your Alpaca account using the below link:
https://centrol.io/connect_alpaca

"""

COINBASE_CONNECT: str = """
Hi!

You just tried to buy a crypto token with the Centrol Trading bot. We are currently using Coinbase PRO to facilitate this.

You can connect you Coinbase PRO account by linking an api token with the bot.

We are currently only allowing paper trading accounts, so ensure you are setting up the key here:
https://public.sandbox.pro.coinbase.com

To do this:

1. Generate an API key, using the information here:
https://help.coinbase.com/en/pro/other-topics/api/how-do-i-create-an-api-key-for-coinbase-pro


Under Permissions ensure to select 'View' and 'Trade'

If you want to try out the api, you can create a new portfolio and select this when generating the key.

2. Link the token with the bot by running:
{op}add-token coinbase api_key_from_coinbase passphrase_from_coinbase secret_from_coinbase

Replace above *_from_coinbase options with the one's you got when generating the key.

Thats it! You are now linked and can view/trade using Coinbase PRO!!
To see the available commands, run:
{op}help-crypto
"""

SUCCESSFUL_ORDER: str = """
Thanks for placing the order!
To check the status of your order, please visit:
{url}
"""

EXAMPLE_BUY_ORDER: str = """
Please enter order in the below format:
{op}buy crypto mkt <crypto pair> <amount in USD>

"""

EXAMPLE_SELL_ORDER: str = """
Please enter order in the below format:
{op}sell crypto mkt <crypto pair> <amount in USD>

"""

FAILED_TOKEN_ADD: str = """
Failed to add token, please use the format:
{op}!add-token coinbase api_key_from_coinbase passphrase_from_coinbase secret_from_coinbase

Replace above *_from_coinbase options with the one's you got when generating the key.
"""
