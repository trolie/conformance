import uuid
from pytest_bdd import given, when, then
from test.helpers import Role, TrolieClient, get_period


@given("a TROLIE client that has not been authenticated", target_fixture="client")
def client_not_authorized():
    return TrolieClient(role=Role.UNAUTHENTICATED)


@given("an empty body and no Content-Type specified")
def empty_body(client: TrolieClient):
    return client.ensure_empty_request()


@given(
    "a Forecast Proposal ID which may or may not exist", target_fixture="proposal_id"
)
def forecast_proposal_id():
    return uuid.uuid4()


@when("the client requests a Historical Forecast Limits Snapshot")
def request_historical_forecast_limits_snapshot(client: TrolieClient):
    return client.request(f"/limits/forecast-snapshot/{get_period(-1)}")


@when("the client requests a Regional Forecast Limits Snapshot")
def request_regional_forecast_limits_snapshot(client: TrolieClient):
    return client.request("/limits/regional/forecast-snapshot")


@when("the client submits a Regional Forecast Limits Snapshot")
def submit_regional_forecast_limits_snapshot(client: TrolieClient):
    return client.request("/limits/regional/forecast-snapshot", method="POST")


@when("the client submits a Forecast Proposal")
def submit_regional_forecast_snapshot(client: TrolieClient):
    return client.request("/rating-proposals/forecast", method="PATCH")


@when("the client requests the status of a Forecast Proposal")
def request_forecast_proposal_status(client: TrolieClient):
    return client.request("/rating-proposals/forecast")


@then("the response is Unauthorized")
def response_is_unauthorized(client: TrolieClient):
    assert client.get_status_code() == 401
