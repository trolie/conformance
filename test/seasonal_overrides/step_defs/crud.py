import uuid
from pytest_bdd import given, when, then
from test.helpers import TrolieClient

_PLACEHOLDER_ID = "placeholder-id"


@given("a Seasonal Override id which may or may not exist", target_fixture="override_id")
def seasonal_override_id():
    return str(uuid.uuid4())


@when("the client requests the list of Seasonal Overrides")
def request_seasonal_overrides_list(client: TrolieClient):
    return client.request("/seasonal-overrides")


@when("the client creates a Seasonal Override")
def create_seasonal_override(client: TrolieClient):
    return client.request("/seasonal-overrides", method="POST")


@when("the client requests a Seasonal Override by id")
def get_seasonal_override_by_id(client: TrolieClient):
    return client.request(f"/seasonal-overrides/{_PLACEHOLDER_ID}")


@when("the client deletes a Seasonal Override by id")
def delete_seasonal_override(client: TrolieClient):
    return client.request(f"/seasonal-overrides/{_PLACEHOLDER_ID}", method="DELETE")


@when("the client updates a Seasonal Override by id")
def update_seasonal_override(client: TrolieClient):
    return client.request(f"/seasonal-overrides/{_PLACEHOLDER_ID}", method="PUT")


@then("the response is 201 Created")
def response_is_201(client: TrolieClient):
    assert client.get_status_code() == 201


@then("the response is 204 No Content")
def response_is_204(client: TrolieClient):
    assert client.get_status_code() == 204
