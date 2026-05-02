from pytest_bdd import when, parsers
from test.helpers import TrolieClient


@when(parsers.parse("the client requests real-time limits with monitoring-set filter {monitoring_set_id}"))
def realtime_snapshot_filter_monitoring_set(monitoring_set_id, client: TrolieClient):
    client.set_query_param("monitoring-set", monitoring_set_id)
    client.request("/limits/realtime-snapshot")


@when(parsers.parse("the client requests real-time limits with resource-id filter {resource_id}"))
def realtime_snapshot_filter_resource_id(resource_id, client: TrolieClient):
    client.set_query_param("resource-id", resource_id)
    client.request("/limits/realtime-snapshot")


@when(parsers.parse("the client requests regional real-time limits with monitoring-set filter {monitoring_set_id}"))
def regional_realtime_snapshot_filter_monitoring_set(monitoring_set_id, client: TrolieClient):
    client.set_query_param("monitoring-set", monitoring_set_id)
    client.request("/limits/regional/realtime-snapshot")


@when(parsers.parse("the client requests regional real-time limits with resource-id filter {resource_id}"))
def regional_realtime_snapshot_filter_resource_id(resource_id, client: TrolieClient):
    client.set_query_param("resource-id", resource_id)
    client.request("/limits/regional/realtime-snapshot")
