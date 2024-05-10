# Ghostfolio Data Feeder

Ghostfolio-feeder extends the functionality of Ghostfolio by automatically adding data via internal APIs. The sources of the data are taken by scraping financial websites.

## Supported sources

| data_source      | Description                       |
|------------------|-----------------------------------|
| investing        | Investing.com                     |
| boerse_frankfurt | Frankfurt Stock Exchange          |
| corriere         | Italian finance site              |
| byblos           | Italian pension fund              |
| fondofonte       | Italian pension fund              |
| mediafond        | Italian pension fund              |
| previcoop        | Italian pension fund              |
| mvis             | Crypto indices used by Bitpanda   |
| local            | CSV and JSON files stored locally |

## Configuration

The configurations can be found in the path `app/data/` and are structured in the following format:

```json
[
    {
        "symbol": "SPY",
        "profile_data": {
            "assetClass": "EQUITY",
            "assetSubClass": "ETF",
            "comment": "",
            "currency": "USD",
            "name": "SPDR® S&P 500",
            "scraperConfiguration": {},
            "symbolMapping": {}
        },
        "data_source": {
            "name": "investing",
            "ticker": {
                "domain": "www",
                "symbol": "spy",
                "exchange": "nyse",
                "retry": 5
            },
            "start_date": "2020-01-01"
        }
    },
    {
        "symbol": "21BC.DE",
        "profile_data": {
            "assetClass": "EQUITY",
            "assetSubClass": "CRYPTOCURRENCY",
            "comment": "",
            "currency": "EUR",
            "name": "21Shares Bitcoin Core ETP",
            "scraperConfiguration": {},
            "symbolMapping": {}
        },
        "data_source": {
            "name": "boerse_frankfurt",
            "ticker": "XETR:CH1199067674",
            "start_date": "2020-01-01"
        }
    }
]
```

## Build and run

Make your own copies of the environment and configured stocks, and edit them.
To run this alongside a local ghostfolio docker installation:

* Set `HOST` to `http://host.docker.internal:3333`
* Set `ACCESS_TOKEN` to your access token for docker.

```bash
cp .env.example .env
# Modify the env file before executing
# vi .env
cp app/data/profiles.json.example app/data/profiles.json
# Modify the profiles.json file before executing
# vi app/data/profiles.json
docker compose up -d --build --force-recreate
```
