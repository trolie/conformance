from pytest_bdd import given
from test.helpers import TrolieClient
from test.forecasting.forecast_helpers import get_etag


def _get_etag_for(client: TrolieClient, url: str) -> str:
    client.request(url)
    return get_etag(client)


@given("the client has obtained the current Real-Time Limits Snapshot with an ETag", target_fixture="etag")
def get_etag_for_realtime_snapshot(client: TrolieClient):
    return _get_etag_for(client, "/limits/realtime-snapshot")


@given("the client has obtained the current Regional Real-Time Limits Snapshot with an ETag", target_fixture="etag")
def get_etag_for_regional_realtime_snapshot(client: TrolieClient):
    return _get_etag_for(client, "/limits/regional/realtime-snapshot")


@given("the client has obtained the current Real-Time Proposal Status with an ETag", target_fixture="etag")
def get_etag_for_realtime_proposal_status(client: TrolieClient):
    return _get_etag_for(client, "/rating-proposals/realtime")
