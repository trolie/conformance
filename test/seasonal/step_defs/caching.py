from pytest_bdd import given
from test.helpers import TrolieClient
from test.forecasting.forecast_helpers import get_etag


def _get_etag_for(client: TrolieClient, url: str) -> str:
    client.request(url)
    return get_etag(client)


@given("the client has obtained the current Seasonal Rating Snapshot with an ETag", target_fixture="etag")
def get_etag_for_seasonal_rating_snapshot(client: TrolieClient):
    return _get_etag_for(client, "/seasonal-ratings/snapshot")


@given("the client has obtained the current Seasonal Rating Proposal Status with an ETag", target_fixture="etag")
def get_etag_for_seasonal_rating_proposal_status(client: TrolieClient):
    return _get_etag_for(client, "/rating-proposals/seasonal")
