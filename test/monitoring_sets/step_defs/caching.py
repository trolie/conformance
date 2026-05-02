from pytest_bdd import given
from test.helpers import TrolieClient
from test.forecasting.forecast_helpers import get_etag


@given("the client has obtained the current Default Monitoring Set with an ETag", target_fixture="etag")
def get_etag_for_default_monitoring_set(client: TrolieClient):
    client.request("/default-monitoring-set")
    return get_etag(client)
