"""Time Interval module."""
from datetime import datetime
from croniter import croniter


def crontab_sleep(cron_expression):
    """
    Function that calculates the number of seconds to sleep to get to the next loop cycle.

    Args:
        cron_expression: String representing the cron expression.

    Returns:
        Integer representing the number of seconds to sleep.
    """

    # Get the current date and time in local time zone
    now = datetime.now().astimezone()

    # Create a croniter object from the cron expression.
    cron = croniter(cron_expression, now)

    # Get the timestamp time of the next loop cycle.
    next_cycle = cron.get_next()

    # Calculate the difference in seconds between the current time and the next cycle.
    seconds_difference = next_cycle - now.timestamp()

    return int(seconds_difference)


def main():
    """Main function for local tests only."""
    next_cycle_sleep = crontab_sleep("00 * * * *")
    print(f"Seconds to sleep: {next_cycle_sleep}")

if __name__ == "__main__":
    main()
