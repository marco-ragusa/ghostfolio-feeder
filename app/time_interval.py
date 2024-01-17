from datetime import datetime, timedelta


def seconds_until_next_interval(interval_minutes: int) -> int:
    # Get the current time
    current_time = datetime.now()

    # Calculate the time remaining until the next specified interval
    next_interval = current_time.replace(second=0, microsecond=0) + timedelta(
        minutes=(interval_minutes - current_time.minute % interval_minutes)
    )

    return (next_interval - current_time).seconds
