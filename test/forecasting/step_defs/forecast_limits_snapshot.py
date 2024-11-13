from pytest_bdd import given, when
from test.helpers import Role, TrolieClient


@given(
    "a TROLIE client that has been authenticated as a Ratings Provider",
    target_fixture="client",
)
def client_authenticated_as_ratings_provider():
    return TrolieClient(role=Role.RATINGS_PROVIDER)


@when("the client requests the current Forecast Limits Snapshot")
@given("the client requests the current Forecast Limits Snapshot")
def request_forecast_limits_snapshot(client: TrolieClient):
    return client.request("/limits/forecast-snapshot")
