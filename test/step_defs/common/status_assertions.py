from pytest_bdd import then
from test.helpers import TrolieClient


@then("the response is 200 OK")
def request_forecast_limits_snapshot(client: TrolieClient):
    assert client.get_status_code() == 200
