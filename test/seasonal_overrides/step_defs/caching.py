from pytest_bdd import given
from test.helpers import TrolieClient
from test.forecasting.forecast_helpers import get_etag


@given("the client has obtained the current Seasonal Overrides list with an ETag", target_fixture="etag")
def get_etag_for_seasonal_overrides(client: TrolieClient):
    client.request("/seasonal-overrides")
    return get_etag(client)
