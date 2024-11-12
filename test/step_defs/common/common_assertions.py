from pytest_bdd import then
from test.helpers import TrolieClient


@then("the response is 200 OK")
def request_forecast_limits_snapshot(client: TrolieClient):
    assert client.get_status_code() == 200


@then("the response is 415 Unsupported Media Type")
def request_forecast_limits_snapshot_415(client: TrolieClient):
    assert client.get_status_code() == 415


@then("the response is schema-valid")
def valid_snapshot(client: TrolieClient):
    assert client.validate_response()
