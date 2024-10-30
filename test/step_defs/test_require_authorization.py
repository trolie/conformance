
from datetime import datetime, timedelta
import os, time, pytz
from pytest_bdd import scenario, given, when, then
import pytest
import requests

def trolie_request(relative_path, auth_token=None, method='GET'):
    trolie_url = os.getenv('TROLIE_BASE_URL') + relative_path
    return requests.request(method=method, url=trolie_url)

def get_period(hours=0):
    tz_name = os.getenv('TZ', 'UTC')
    timezone = pytz.timezone(tz_name)
    return (datetime.now(timezone) + timedelta(hours=hours)).replace(minute=0, second=0, microsecond=0).isoformat()

@pytest.mark.Forecasting
@scenario('require_authorization.feature', 'Get Forecast Limits Snapshot requires authorization')
def test_snapshot_authorization():
    pass

@pytest.mark.Forecasting
@scenario('require_authorization.feature', 'Get Historical Forecast Limits Snapshot requires authorization')
def test_historical_snapshot_authorization():
    pass

@given('a TROLIE client that has not been authorized', target_fixture='auth_token')
def client_not_authorized():
    return None

@when('the client requests the current Forecast Limits Snapshot',
      target_fixture='response')
def request_forecast_limits_snapshot():
    return trolie_request('/limits/forecast-snapshot')

@when('the client requests a Historical Forecast Limits Snapshot',
      target_fixture='response')
def request_forecast_limits_snapshot():
    return trolie_request(f"/limits/forecast-snapshot/{get_period(-1)}")

@then('the response is Unauthorized')
def response_is_unauthorized(response):
    assert response.status_code == 401
