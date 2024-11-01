from pytest_bdd import scenario, given, then, parsers


@scenario("forecast_limits_snapshot.feature", "Obtaining the latest forecast snapshot")
def test_latest_snapshot():
    pass


@given("a TROLIE client that has been authenticated as a Ratings Provider")
def client_authenticated_as_ratings_provider():
    pass


@given(parsers.parse("the Accept header is set to {content_type}"))
def accept_header(content_type):
    pass


@then(parsers.parse("the Content-Type header in the response is {content_type}"))
def content_type_header(content_type):
    pass


@then("the response is a valid Forecast Limits Snapshot")
def valid_snapshot(request):
    pass
