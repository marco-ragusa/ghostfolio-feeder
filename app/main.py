"""Ghostfolio Feeder entry point."""

import json
from os import getenv, path
from time import sleep

from ghostfolio import Ghostfolio
from ghostfolio_feeder import ghostfolio_feeder
from time_interval import crontab_sleep


def loop(host: str, access_token: str, crontab: str) -> None:
    """Read configured profiles and feed them at each scheduled interval."""
    json_file_path = path.join(path.dirname(__file__), "data", "profiles.json")

    while True:
        with open(json_file_path, "r", encoding="UTF8") as file:
            profiles = json.load(file)

        # Authenticate once per cycle instead of once per symbol.
        ghostfolio = Ghostfolio(host, access_token)

        for profile in profiles:
            symbol = profile["symbol"]
            print(f"Processing {symbol} symbol...")
            try:
                ghostfolio_feeder(
                    ghostfolio,
                    symbol,
                    profile["profile_data"],
                    profile["data_source"],
                )
            except Exception as error:
                print(f"ERROR [{symbol}]: {error}")

        seconds_next_interval = crontab_sleep(crontab)
        print(f"Wait {seconds_next_interval} seconds until the next loop")
        sleep(seconds_next_interval)


def main() -> None:
    """Load configuration from the environment and start the feeder."""
    host = getenv("HOST")
    access_token = getenv("ACCESS_TOKEN")

    if not host or not access_token:
        raise RuntimeError("HOST and ACCESS_TOKEN environment variables are required")

    loop(host, access_token, getenv("CRONTAB", "00 * * * *"))


if __name__ == "__main__":
    main()
