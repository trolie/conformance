from pytest_bdd import when
from test.helpers import TrolieClient


@when("the client requests the current Forecast Limits Snapshot")
def request_forecast_limits_snapshot(client: TrolieClient):
    return client.request("/limits/forecast-snapshot")
