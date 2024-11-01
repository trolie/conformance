from datetime import datetime, timedelta
import requests
import os
import pytz


def trolie_request(relative_path, auth_token=None, method="GET"):
    trolie_url = os.getenv("TROLIE_BASE_URL") + relative_path
    return requests.request(method=method, url=trolie_url)


def get_period(hours=0):
    tz_name = os.getenv("TZ", "UTC")
    timezone = pytz.timezone(tz_name)
    return (
        (datetime.now(timezone) + timedelta(hours=hours))
        .replace(minute=0, second=0, microsecond=0)
        .isoformat()
    )
