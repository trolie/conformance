from pytest_bdd import when
from test.helpers import trolie_request


@when(
    "the client requests the current Forecast Limits Snapshot",
    target_fixture="response",
)
def request_forecast_limits_snapshot():
    return trolie_request("/limits/forecast-snapshot")
