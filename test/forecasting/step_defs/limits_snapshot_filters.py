from pytest_bdd import given, when, then, parsers
from test.helpers import TrolieClient
from test.forecasting.forecast_helpers import (
    get_forecast_limits_snapshot,
    get_todays_iso8601_for,
)


@given(
    parsers.parse(
        "the current wall clock time at the Clearinghouse is today at 11am GMT, i.e., {server_wall_clock_time}"
    )
)
def clearinghouse_wall_clock_today_at_11amGMT(
    server_wall_clock_time, client: TrolieClient
):
    client.set_header(
        "X-TROLIE-Testing-Current-DateTime",
        get_todays_iso8601_for(server_wall_clock_time),
    )


@when(
    parsers.parse(
        "the client requests forecast limits with `offset-period-start` for an hour from then at {request_offset_time}"
    )
)
def forecast_snapshot_request_filter_offset_period_start(
    request_offset_time, client: TrolieClient
):
    client.set_query_param(
        "offset-period-start", get_todays_iso8601_for(request_offset_time)
    )
    get_forecast_limits_snapshot(client)


@then(
    parsers.parse(
        "the response should only include forecast limits starting at the `offset-period-start` in the server's time zone, i.e., {response_first_period}"
    )
)
def forecast_snapshot_request_first_period_starts_on(
    response_first_period, client: TrolieClient
):
    assert client.get_json()["limits"][0]["periods"][0][
        "period-start"
    ] == get_todays_iso8601_for(response_first_period)
