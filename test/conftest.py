import os
import pytest

from test.helpers import Role, TrolieClient


pytest_plugins = [
    "test.common.common_steps",
    "test.forecasting.step_defs.require_authentication",
    "test.forecasting.step_defs.limits_snapshot",
]


def pytest_bdd_apply_tag(tag, function):
    if tag == "prism_fail":
        marker = pytest.mark.skip(reason="Prism mock does not support this test")
        marker(function)
        return True
    else:
        # Fall back to the default behavior of pytest-bdd
        return None


def pytest_bdd_after_scenario(request, feature, scenario):
    if "skip_rate_limiting" in feature.tags or "skip_rate_limiting" in scenario.tags:
        return
    client: TrolieClient = request.getfixturevalue("client")
    if not getattr(client, "response", None):
        return
    if not request.session.shouldfail:
        if os.getenv("RATE_LIMITING"):
            if client.role == Role.UNAUTHENTICATED:
                assert client.get_response_header("X-Rate-Limit-Limit") == 0
                assert client.get_response_header("X-Rate-Limit-Remaining") == 0
                assert client.get_response_header("X-Rate-Limit-Reset") == 0
            else:
                assert client.get_response_header("X-Rate-Limit-Limit") > 0
                assert client.get_response_header("X-Rate-Limit-Remaining") > 0
                assert client.get_response_header("X-Rate-Limit-Reset") > 0

        if client.get_status_code() >= 200 and client.get_status_code() < 300:
            assert client.get_response_header("ETag")
