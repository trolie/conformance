import os
import pytest

from test.helpers import TrolieClient


pytest_plugins = [
    "test.step_defs.common.forecasting",
    "test.step_defs.common.common_assertions",
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
    if not request.session.shouldfail and os.getenv("RATE_LIMITING"):
        client: TrolieClient = request.getfixturevalue("client")
        assert client.get_response_header("X-Rate-Limit-Limit")
        assert client.get_response_header("X-Rate-Limit-Remaining")
        assert client.get_response_header("X-Rate-Limit-Reset")
