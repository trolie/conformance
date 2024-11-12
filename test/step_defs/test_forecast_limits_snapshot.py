from pytest_bdd import scenario, given, then, parsers

from test.helpers import Header, MediaType, Role, TrolieClient, TrolieMessages


@scenario("forecast_limits_snapshot.feature", "Obtaining the latest forecast snapshot")
def test_latest_snapshot():
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
    assert client.get_response_header(Header.ContentType) == content_type


@then("the response is a valid Forecast Limits Snapshot")
def valid_snapshot(client: TrolieClient):
    response_json = client.get_json()
    assert TrolieMessages.is_valid(
        message=response_json, media_type=MediaType.FORECAST_LIMITS_SNAPSHOT
    )
