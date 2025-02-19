from pytest_bdd import given, when, then, parsers
from test.forecasting.forecast_helpers import get_forecast_limits_snapshot, get_todays_iso8601_for, get_etag


@given("the client has obtained the current Forecast Limits Snapshot with an ETag", target_fixture="etag")
def get_etag_for_forecast_limits_snapshot(client):
    current_time = get_todays_iso8601_for("11:00:00Z")
    client.set_header("X-TROLIE-Testing-Current-DateTime", current_time)
    return get_etag(get_forecast_limits_snapshot(client))


@when("the client immediately requests the Forecast Limits Snapshot with an If-None-Match header set to the ETag of the previously obtained Forecast Limits Snapshot")
def request_with_if_none_match(client, etag):
    client.set_header("If-None-Match", etag)
    client.send()


@then("the server should respond with a 304 Not Modified status code")
def check_304_status(client):
    assert client.get_status_code() == 304


@then("the response should not include the Forecast Limits Snapshot")
def check_no_snapshot_in_response(client):
    assert client.response_is_empty()


@when(parsers.parse("the client immediately requests the Forecast Limits Snapshot with an Accept header of `{accept_header_2}`"), target_fixture="client")
def request_forecast_limits_snapshot_with_different_accept_header(client, accept_header_2):
    client.set_header("Accept", accept_header_2)
    return get_forecast_limits_snapshot(client)


@then("the etags should not match")
def etags_should_not_match(client, etag):
    new_etag = get_etag(client)
    assert etag != new_etag, "ETags should not match for different representations"
