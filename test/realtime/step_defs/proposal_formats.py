from pytest_bdd import when
from test.helpers import TrolieClient


@when("the client requests for the current real-time proposal status")
def request_realtime_proposal_status(client: TrolieClient):
    return client.request("/rating-proposals/realtime")

@when("the client submits a real-time rating proposal")
def submit_realtime_proposal_status(client: TrolieClient):
    return client.request("/rating-proposals/realtime", method="POST")