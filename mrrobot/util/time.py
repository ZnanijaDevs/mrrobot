from datetime import datetime
import pytz
from mrrobot.config import TIMEZONE


timezone = pytz.timezone(TIMEZONE)


def ts_to_date(timestamp: str | float) -> str:
    """Convert Slack timestamp to a human readable date"""
    if isinstance(timestamp, str):
        timestamp = float(timestamp)

    return datetime.fromtimestamp(timestamp, timezone).strftime("%d.%m.%Y %H:%M:%S")
