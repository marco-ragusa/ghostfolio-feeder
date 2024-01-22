# Ghostfolio Data Feeder

Ghostfolio-feeder extends the functionality of Ghostfolio by automatically adding data via internal APIs. The sources of the data are taken by scraping financial websites.

## Configuration

The configurations can be found in the path `app/data/` and are structured in the following format:

```json
[
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
cp app/data/data.json.example app/data/data.json
# Modify the data.json file before executing
# vi app/data/data.json
docker compose up -d --build --force-recreate
```
