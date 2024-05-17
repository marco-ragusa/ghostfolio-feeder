"""Ghostfolio Feeder main."""
import json
from os import path, getenv
from time import sleep
from ghostfolio_feeder import ghostfolio_feeder
from time_interval import crontab_sleep


def loop(host: str, access_token: str, crontab: str) -> None:
    """Ghostfolio Feeder loop."""
    json_file_path = path.join(path.dirname(__file__), 'data', 'profiles.json')
    while True:
        with open(json_file_path, 'r', encoding='UTF8') as file:
            data_list = json.load(file)

        for data in data_list:
            print(f"Processing {data['symbol']} symbol...")
            try:
                ghostfolio_feeder(
                    host,
                    access_token,
                    data['symbol'],
                    data['profile_data'],
                    data['data_source']
                )
            except Exception as e:
                print(f"ERROR: {e}")

        seconds_next_interval = crontab_sleep(crontab)
        print(f"Wait {seconds_next_interval} seconds until the next loop")
        sleep(seconds_next_interval)


def main():
    """Main function."""
    host = getenv('HOST', 'https://example.com')
    access_token = getenv('ACCESS_TOKEN', 'your_access_token')
    crontab = getenv("CRONTAB", '00 * * * *')
    loop(host, access_token, crontab)


if __name__ == "__main__":
    main()
