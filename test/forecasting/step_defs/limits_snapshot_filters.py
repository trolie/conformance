from pytest_bdd import given, when, then, parsers
from test.helpers import TrolieClient
from test.forecasting.forecast_helpers import (
    get_forecast_limits_snapshot,
    get_todays_iso8601_for,
)


@given(parsers.parse("the current wall clock time at the Clearinghouse is today at 11am GMT, i.e., {server_time}"))
def clearinghouse_wall_clock_today_at_11amGMT(server_time, client: TrolieClient):
    client.set_header(
        "X-TROLIE-Testing-Current-DateTime",
        get_todays_iso8601_for(server_time),
    )


@when(parsers.parse("the client requests forecast limits with `offset-period-start` for an hour from then at {request_offset_time}"))
def forecast_snapshot_request_filter_offset_period_start(request_offset_time, client: TrolieClient):
    client.set_query_param("offset-period-start", get_todays_iso8601_for(request_offset_time))
    get_forecast_limits_snapshot(client)


@when(parsers.parse("the client requests forecast limits with period-end {request_last_period}"))
def forecast_snapshot_request_filter_last_period(request_last_period, client: TrolieClient):
    client.set_query_param("period-end", get_todays_iso8601_for(request_last_period))
    get_forecast_limits_snapshot(client)


@then(parsers.parse("the response should only include forecast limits starting at the `offset-period-start` in the server's time zone, i.e., {response_first_period}"))
def forecast_snapshot_request_first_period_starts_on(response_first_period, client: TrolieClient):
    expected_start = get_todays_iso8601_for(response_first_period)
    limits = client.get_json()["limits"]
    targets = ((entry["resource-id"], entry["periods"][0]["period-start"]) for entry in limits)
    for resource_id, period_start in targets:
        assert expected_start == period_start, f"Failed for resource {resource_id}"


@then(parsers.parse("the response should include forecast limits up to {response_last_period} in the server's time zone"))
def forecast_snapshot_request_last_period_includes(response_last_period, client: TrolieClient):
    expected_end = get_todays_iso8601_for(response_last_period)
    limits = client.get_json()["limits"]
    targets = ((limits_entry["resource-id"], limits_entry["periods"][-1]["period-end"]) for limits_entry in limits)
    for resource_id, period_end in targets:
        assert expected_end == period_end, f"Failed for resource {resource_id}"
