from pytest_bdd import scenario, given, when, then
import pytest
from test.helpers import trolie_request, get_period


@pytest.mark.Forecasting
@scenario(
    "forecasting_requires_authentication.feature",
    "Get Forecast Limits Snapshot requires authorization",
)
def test_snapshot_authorization():
    pass


@pytest.mark.Forecasting
@scenario(
    "forecasting_requires_authentication.feature",
    "Get Historical Forecast Limits Snapshot requires authorization",
)
def test_historical_snapshot_authorization():
    pass


@pytest.mark.Forecasting
@scenario(
    "forecasting_requires_authentication.feature",
    "Get Regional Forecast Limits Snapshot requires authorization",
)
def test_regional_snapshot_authorization():
    pass


@pytest.mark.Forecasting
@scenario(
    "forecasting_requires_authentication.feature",
    "Updating the Regional Forecast Limits Snapshot requires authorization",
)
def test_regional_forecast_proposal_authorization():
    pass


@pytest.mark.Forecasting
@scenario(
    "forecasting_requires_authentication.feature",
    "Submitting a Forecast Proposal requires authorization",
)
def test_forecast_proposal_authorization():
    pass


@pytest.mark.Forecasting
@scenario(
    "forecasting_requires_authentication.feature",
    "Obtain Forecast Proposal Status requires authorization",
)
def test_forecast_proposal_status_authorization():
    pass


@given("a TROLIE client that has not been authenticated", target_fixture="auth_token")
def client_not_authorized():
    return None


@given("an empty body and no Content-Type specified")
def empty_body():
    return None


@given("a Forecast Proposal ID which may or may not exist")
def forecast_proposal_id():
    pass


@when(
    "the client requests a Historical Forecast Limits Snapshot",
    target_fixture="response",
)
def request_historical_forecast_limits_snapshot():
    return trolie_request(f"/limits/forecast-snapshot/{get_period(-1)}")


@when(
    "the client requests a Regional Forecast Limits Snapshot",
    target_fixture="response",
)
def request_regional_forecast_limits_snapshot():
    return trolie_request("/limits/regional/forecast-snapshot")


@when(
    "the client submits a Regional Forecast Limits Snapshot", target_fixture="response"
)
def submit_regional_forecast_limits_snapshot():
    return trolie_request("/limits/regional/forecast-snapshot", method="POST")


@when("the client submits a Forecast Proposal", target_fixture="response")
def submit_regional_forecast_snapshot():
    return trolie_request("/rating-proposals/forecast", method="PATCH")


@when(
    "the client requests the status of a Forecast Proposal", target_fixture="response"
)
def request_forecast_proposal_status():
    return trolie_request("/rating-proposals/forecast")


@then("the response is Unauthorized")
def response_is_unauthorized(response):
    assert response.status_code == 401
