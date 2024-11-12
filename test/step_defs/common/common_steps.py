from pytest_bdd import given, then, when
from test.helpers import TrolieClient


@given("the client has bad query parameters")
def bad_query_parameters(client: TrolieClient):
    client.set_query_param("bad", "value")


@then("the response is 200 OK")
def request_forecast_limits_snapshot(client: TrolieClient):
    assert client.get_status_code() == 200


@then("the response is 304 Not Modified")
def request_forecast_limits_snapshot_304(client: TrolieClient):
    assert client.get_status_code() == 304


@then("the response is 400 Bad Request")
def request_forecast_limits_snapshot_400(client: TrolieClient):
    assert client.get_status_code() == 400


@then("the response is 415 Unsupported Media Type")
def request_forecast_limits_snapshot_415(client: TrolieClient):
    assert client.get_status_code() == 415


@then("the response is schema-valid")
def valid_snapshot(client: TrolieClient):
    assert client.validate_response()


@when("the client issues a conditional GET for the same resource")
def conditional_get(client: TrolieClient):
    client.set_header("If-None-Match", client.get_response_header("ETag"))
    client.send()


@then("the response is empty")
def empty_response(client: TrolieClient):
    assert not client.get_json()
    assert not client.get_response_header("Content-Type")
