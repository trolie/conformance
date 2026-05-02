from pytest_bdd import when
from test.helpers import TrolieClient


@when("the client requests the Seasonal Rating Proposal Status")
def request_seasonal_rating_proposal_status(client: TrolieClient):
    return client.request("/rating-proposals/seasonal")


@when("the client submits a Seasonal Ratings Proposal")
def submit_seasonal_ratings_proposal(client: TrolieClient):
    return client.request("/rating-proposals/seasonal", method="PATCH")
