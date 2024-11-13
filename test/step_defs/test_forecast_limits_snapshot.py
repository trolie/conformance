from pytest_bdd import scenario, given

from test.helpers import Role, TrolieClient


@scenario("forecast_limits_snapshot.feature", "Obtaining the latest forecast snapshot")
def test_latest_snapshot():
    pass


@scenario(
    "forecast_limits_snapshot.feature", "Obtaining the latest slim forecast snapshot"
)
def test_latest_slim_snapshot():
    pass


@scenario(
    "forecast_limits_snapshot.feature",
    "Requesting the slim forecast snapshot requires a limit type",
)
def test_latest_slim_snapshot_requires_limit_type():
    pass


@scenario(
    "forecast_limits_snapshot.feature", "Limit forecasts should support conditional GET"
)
def test_limit_forecasts_conditional_get():
    pass


@scenario("forecast_limits_snapshot.feature", "Bad query params are malformed requests")
def test_bad_query_parameters():
    pass


@scenario(
    "forecast_limits_snapshot.feature",
    "Sending a body with a GET request is a bad request",
)
def test_non_empty_body_in_get():
    pass


@given(
    "a TROLIE client that has been authenticated as a Ratings Provider",
    target_fixture="client",
)
def client_authenticated_as_ratings_provider():
    return TrolieClient(role=Role.RATINGS_PROVIDER)
