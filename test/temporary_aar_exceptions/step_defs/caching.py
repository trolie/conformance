from pytest_bdd import given
from test.helpers import TrolieClient
from test.forecasting.forecast_helpers import get_etag


@given("the client has obtained the current Temporary AAR Exceptions list with an ETag", target_fixture="etag")
def get_etag_for_temporary_aar_exceptions(client: TrolieClient):
    client.request("/temporary-aar-exceptions")
    return get_etag(client)
