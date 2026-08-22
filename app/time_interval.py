"""Cron schedule helpers."""

from datetime import datetime

from croniter import croniter


def crontab_sleep(cron_expression: str) -> int:
    """Return seconds until the next cron occurrence."""
    now = datetime.now().astimezone()
    return int(croniter(cron_expression, now).get_next() - now.timestamp())
