from pytest_bdd import given, when
from test.helpers import TrolieClient

@when("the client requests the current Forecast Limits Snapshot")
@given("the client requests the current Forecast Limits Snapshot")
def request_forecast_limits_snapshot(client: TrolieClient):
    return client.request("/limits/forecast-snapshot")


@when("the client requests a Historical Forecast Limits Snapshot at time frame {time_frame}")
def request_historical_forecast_limits_snapshot_at_period(client: TrolieClient, time_frame):
    return client.request(f"/limits/forecast-snapshot/{time_frame}")

