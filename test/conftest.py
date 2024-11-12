import pytest


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
