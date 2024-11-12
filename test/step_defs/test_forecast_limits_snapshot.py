from pytest_bdd import scenario, given, then, parsers

from test.helpers import Header, Role, TrolieClient


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


@given(
    "a TROLIE client that has been authenticated as a Ratings Provider",
    target_fixture="client",
)
def client_authenticated_as_ratings_provider():
    return TrolieClient(role=Role.RATINGS_PROVIDER)


@given(parsers.parse("the Accept header is set to {content_type}"))
def accept_header(content_type, client):
    client.set_header(Header.Accept, content_type)


@then(parsers.parse("the Content-Type header in the response is {content_type}"))
def content_type_header(content_type, client):
    assert content_type == client.get_response_header(Header.ContentType)
