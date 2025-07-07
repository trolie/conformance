import os
import pytest

from test.helpers import Role, TrolieClient

from glob import glob

# In order to organize the conformance tests into different "profiles", i.e., forecasting, realtime, seasonal, and peering,
# we need to help pytest-bdd find the step definitions. The simplest way to do this is
# get them loaded via the pytest_plugins.
# https://gist.github.com/peterhurford/09f7dcda0ab04b95c026c60fa49c2a68?permalink_comment_id=3453153#gistcomment-3453153
pytest_plugins = [
    fixture.replace("/", ".").replace(".py", "")
    for fixture in glob("test/**/step_defs/*.py")
    if "__" not in fixture
] + ["test.common.common_steps"]


def pytest_bdd_apply_tag(tag, function):
    using_mock = os.getenv("TROLIE_BASE_URL") == "http://localhost:4010"
    should_skip = tag == "prism_fail" and using_mock
    if should_skip or tag == "todo":
        reason = "Prism mock does not support this test" if using_mock else "TODO"
        marker = pytest.mark.skip(reason=reason)
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


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Add a pretty summary of test results at the end of the pytest run."""
    passed = len(terminalreporter.stats.get('passed', []))
    failed = len(terminalreporter.stats.get('failed', []))
    skipped = len(terminalreporter.stats.get('skipped', []))
    deselected = len(terminalreporter.stats.get('deselected', []))
    warnings = len(terminalreporter.stats.get('warnings', []))

    terminalreporter.write('\n')
    terminalreporter.write('==================== 🧪 Test Results Summary ====================\n', bold=True)
    terminalreporter.write(f'  ✅ Passed:      ', bold=True)
    terminalreporter.write(f'{passed}\n', green=True, bold=True)
    terminalreporter.write(f'  ❌ Failed:      ', bold=True)
    terminalreporter.write(f'{failed}\n', red=True, bold=True)
    terminalreporter.write(f'  ⚠️ Skipped:     ', bold=True)
    terminalreporter.write(f'{skipped}\n', yellow=True, bold=True)
    terminalreporter.write(f'  🚫 Deselected:  ', bold=True)
    terminalreporter.write(f'{deselected}\n', yellow=True)
    terminalreporter.write(f'  ⚠️ Warnings:    ', bold=True)
    terminalreporter.write(f'{warnings}\n', yellow=True)
    # List out passed and failed tests
    if passed:
        terminalreporter.write(f'\n  ✅ Passed Tests:\n', green=True, bold=True)
        for rep in terminalreporter.stats.get('passed', []):
            if hasattr(rep, 'nodeid'):
                terminalreporter.write(f'    - {rep.nodeid}\n', green=True)
    if failed:
        terminalreporter.write(f'\n  ❌ Failed Tests:\n', red=True, bold=True)
        for rep in terminalreporter.stats.get('failed', []):
            if hasattr(rep, 'nodeid'):
                terminalreporter.write(f'    - {rep.nodeid}\n', red=True)
    terminalreporter.write('===============================================================\n', bold=True)