
import os
from pytest_bdd import scenario, given, when, then
import pytest
import requests

def trolie_url(relative_path):
    return os.getenv('TROLIE_BASE_URL') + relative_path

@pytest.mark.Forecasting
@scenario('require_authorization.feature', 'Get Forecast Limits Snapshot requires authorization')
def test_authorization():
    pass


@given('a TROLIE client that has not been authorized', target_fixture='client')
def client_not_authorized():
    return requests.Request(method='GET', url=trolie_url('/limits/forecast-snapshot'))

@when('the client requests the current Forecast Limits Snapshot',
      target_fixture='response')
def request_forecast_limits_snapshot(client):
    session = requests.Session()
    prepared_request = session.prepare_request(client)
    return session.send(prepared_request)

@then('the response is Unauthorized')
def response_is_unauthorized(response):
    assert response.status_code == 401
