
## Ghostfolio Data Feeder

Ghostfolio-feeder extends the functionality of Ghostfolio by automatically adding data via internal APIs. The datasources from which the data is taken are obtained by scraping finacial websites.

### Configuration
The configurations are contained in the directory `app/data/` and are in the following format:
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

### Build and run
```bash
# Modify the env file before executing
# vi .env.example
cp .env.example .env
docker compose up -d --build --force-recreate
```
