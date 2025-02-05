from pytest_bdd import given, when, then, parsers
from test.helpers import TrolieClient


@given(
    parsers.parse(
        "the current wall clock time at the Clearinghouse is today at 11am GMT, i.e., {server_wall_clock_time}"
    )
)
def clearinghouse_wall_clock_today_at_11amGMT(
    server_wall_clock_time, client: TrolieClient
):
    pass


@when(
    "the client requests forecast limits with `offset-period-start` for an hour from then, e.g., <request_offset_time>"
)
def forecast_snapshot_request_filter_offset_period_start(
    request_offset_time, client: TrolieClient
):
    pass


@then(
    "the response should only include forecast limits starting at the `offset-period-start` in the server's time zone, i.e., <response_first_period>"
)
def forecast_snapshot_request_first_period_starts_on(
    response_first_period, client: TrolieClient
):
    pass
