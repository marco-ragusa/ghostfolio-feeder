import json
from ghostfolio_feeder import ghostfolio_feeder
from time_interval import seconds_until_next_interval
from os import path, getenv
from time import sleep


def loop(host: str, access_token: str, interval_minutes: int) -> None:
    json_file_path = path.join(path.dirname(__file__), 'data', 'data.json')
    while True:
        with open(json_file_path, 'r') as file:
            data_list = json.load(file)

        for data in data_list:
            print(f"Processing {data['symbol']} symbol...")
            try:
                ghostfolio_feeder(host, access_token, data['symbol'], data['profile_data'], data['data_source'])
            except Exception as e:
                print(f"ERROR: {e}")

        seconds_next_interval = seconds_until_next_interval(interval_minutes)
        print(f"Wait {seconds_next_interval} seconds until the next loop")
        sleep(seconds_next_interval)


def main():
    host = getenv('HOST', 'https://example.com')
    access_token = getenv('ACCESS_TOKEN', 'your_access_token')
    interval_minutes = int(getenv("INTERVAL_MINUTES", 30))
    loop(host, access_token, interval_minutes)


if __name__ == "__main__":
    main()
