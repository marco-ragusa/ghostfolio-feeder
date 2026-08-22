# Ghostfolio Data Feeder

Ghostfolio Feeder imports market data that is not available through the
standard Ghostfolio data providers. It reads a small JSON configuration,
fetches prices from the selected source, and upserts them as `MANUAL` assets.

The current API integration supports Ghostfolio 3.13.0 or newer. The E2E
environment is pinned to the official Ghostfolio 3.58.0 image.

## Supported sources

| `data_source` | Ticker format | Description |
|---|---|---|
| `boerse_frankfurt` | `MIC:ISIN` | Börse Frankfurt, for example `XETR:CH1199067674` |
| `corriere` | Corriere chart code | Corriere Borsa, for example `FC.ALPFRA12` |
| `byblos` | Fund code | Byblos pension fund |
| `fondofonte` | URL slug | Fon.Te. pension fund |
| `mediafond` | Fund code | MEDIAFOND pension fund |
| `previcoop` | URL slug | Previdenza Cooperativa pension fund |
| `cometa` | URL slug | Cometa pension fund |
| `cfs` | APIR code | Colonial First State fund |
| `local` | File path | Local CSV or JSON file |

MVIS was removed because historical data now requires authentication. The old
embedded API key no longer works. The former Corriere ticker
`PEX0ALPFRA12.EUR` was also retired by the source. Allianz Insieme Linea
Azionaria now uses `FC.ALPFRA12`.

External websites can change without notice. A failure in one source is logged
without stopping the other configured profiles.

## Configuration

Copy the example files and edit them:

```bash
cp .env.example .env
cp app/data/profiles.json.example app/data/profiles.json
```

Each profile has this shape:

```json
{
  "symbol": "GF_21BC_DE",
  "profile_data": {
    "assetClass": "EQUITY",
    "assetSubClass": "CRYPTOCURRENCY",
    "comment": "",
    "currency": "EUR",
    "name": "21Shares Bitcoin Core ETP",
    "scraperConfiguration": {
      "url": "https://api.live.deutsche-boerse.com/v1/data/quote_box/single?isin=CH1199067674&mic=XETR",
      "selector": "$.lastPrice"
    },
    "symbolMapping": {}
  },
  "data_source": {
    "name": "boerse_frankfurt",
    "ticker": "XETR:CH1199067674",
    "start_date": "2022-07-31"
  }
}
```

All example symbols follow Ghostfolio's `GF_` convention for new `MANUAL`
assets. Existing legacy symbols already stored in Ghostfolio keep working.
Omit `scraperConfiguration` when it is not used; Ghostfolio requires `url` and
`selector` whenever that optional object is present.

Required environment variables:

- `HOST`: Ghostfolio URL. From Docker, a local installation is usually
  `http://host.docker.internal:3333`.
- `ACCESS_TOKEN`: access token of a Ghostfolio administrator.
- `CRONTAB`: optional schedule, default `00 * * * *`.

TLS certificates are verified. For a private certificate authority, use the
standard `REQUESTS_CA_BUNDLE` environment variable.

## Run

```bash
docker compose up -d --build --force-recreate
```

## Tests

Unit tests use only the Python standard library mocks:

```bash
python -m unittest discover -s app/tests -t app -v
```

The E2E test starts a clean PostgreSQL, Redis, and the official Ghostfolio
container; it creates a user, feeds a local asset, verifies it through the real
API, and removes the stack:

```bash
python e2e.py
```

The default image is `ghostfolio/ghostfolio:3.58.0`. Override it when checking
a different upstream release:

```bash
GHOSTFOLIO_IMAGE=ghostfolio/ghostfolio:latest python e2e.py
```
