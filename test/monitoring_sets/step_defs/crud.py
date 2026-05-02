from pytest_bdd import when
from test.helpers import TrolieClient

_PLACEHOLDER_ID = "placeholder-id"


@when("the client creates a Monitoring Set")
def create_monitoring_set(client: TrolieClient):
    return client.request("/monitoring-sets", method="POST")


@when("the client requests a Monitoring Set by id")
def get_monitoring_set_by_id(client: TrolieClient):
    return client.request(f"/monitoring-sets/{_PLACEHOLDER_ID}")


@when("the client updates a Monitoring Set by id")
def update_monitoring_set(client: TrolieClient):
    return client.request(f"/monitoring-sets/{_PLACEHOLDER_ID}", method="PUT")


@when("the client deletes a Monitoring Set by id")
def delete_monitoring_set(client: TrolieClient):
    return client.request(f"/monitoring-sets/{_PLACEHOLDER_ID}", method="DELETE")


@when("the client requests the Default Monitoring Set")
def get_default_monitoring_set(client: TrolieClient):
    return client.request("/default-monitoring-set")
