from pytest_bdd import when
from test.helpers import TrolieClient

_PLACEHOLDER_ID = "placeholder-id"


@when("the client requests the list of Temporary AAR Exceptions")
def request_temporary_aar_exceptions_list(client: TrolieClient):
    return client.request("/temporary-aar-exceptions")


@when("the client creates a Temporary AAR Exception")
def create_temporary_aar_exception(client: TrolieClient):
    return client.request("/temporary-aar-exceptions", method="POST")


@when("the client requests a Temporary AAR Exception by id")
def get_temporary_aar_exception_by_id(client: TrolieClient):
    return client.request(f"/temporary-aar-exceptions/{_PLACEHOLDER_ID}")


@when("the client deletes a Temporary AAR Exception by id")
def delete_temporary_aar_exception(client: TrolieClient):
    return client.request(f"/temporary-aar-exceptions/{_PLACEHOLDER_ID}", method="DELETE")


@when("the client deletes a Temporary AAR Exception that is in use")
def delete_temporary_aar_exception_in_use(client: TrolieClient):
    # A real server would reject deletion of an in-use exception with 409
    return client.request(f"/temporary-aar-exceptions/{_PLACEHOLDER_ID}", method="DELETE")


@when("the client updates a Temporary AAR Exception by id")
def update_temporary_aar_exception(client: TrolieClient):
    return client.request(f"/temporary-aar-exceptions/{_PLACEHOLDER_ID}", method="PUT")
