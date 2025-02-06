from datetime import datetime
from test.helpers import TrolieClient


def get_forecast_limits_snapshot(client: TrolieClient):
    return client.request("/limits/forecast-snapshot")


def get_todays_iso8601_for(time_with_timezone: str) -> str:
    iso8601_offset = datetime.now().strftime(f"%Y-%m-%dT{time_with_timezone}")
    try:
        datetime.fromisoformat(iso8601_offset)
    except ValueError:
        raise ValueError(f"Invalid ISO8601 format: {iso8601_offset}")
    return iso8601_offset
