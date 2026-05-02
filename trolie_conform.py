#!/usr/bin/env python3
"""
trolie-conform: Run the TROLIE conformance suite against a target implementation
and produce a formatted conformance report to stdout.

Usage:
    python trolie_conform.py [OPTIONS]

Examples:
    python trolie_conform.py
    python trolie_conform.py --url https://trolie.example.com --token MY_TOKEN
    python trolie_conform.py --profile forecasting --profile realtime
    python trolie_conform.py --url https://trolie.example.com --ssl-verify
"""
from __future__ import annotations

import argparse
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import pytest

# ── Repo root (the directory that contains this script) ───────────────────────
_REPO_ROOT = Path(__file__).parent.resolve()

# ── ASCII banner ──────────────────────────────────────────────────────────────
_BANNER = """\
          _yyg@@RPPPR@$gy_                                                                                                 
       _a@P~~     s    `~~R$y_                                                                                             
     y@F~   a_    $    _*   ~Rg_                            
   y$F       ~=  ___  =~      ~@g          
  z@`      _yyyyEZZZ@yyyy_      ~@_        
 g@       g@@@@@@@@@@@@@@@L      ~@,       
y@^       @@$````4@`````@@$       4$       
$$        @@$ _aE4@  yg,@@$        @L                                                                                      
$[        @@$=@F 4@W0=~ @@$        $$                                           ___                                        
$l        @@$"   4@ ~   @@$        $$      a@@@@@@@@@@@@@  @@@@@@@@@gy_     _a@@@@@@$y     @@@L         4@@@   0@@@@@@@@@@$
4$        @@@@@@@@@@@@@@@@$        @       fFFFF5@@@FFFFF  @@@~~~~~@@@@,   y@@@~~`~4@@$    @@@L         4@@@   $@@@FFFFFFFF
 @L       @@@_$@ggggg$Ly@@$       a@            4@@$       @@@      $@@$   @@@^     4@@$   @@@L         4@@@   $@@$        
 ~@_      @@@@@@@@@@@@@@@@P      z@             4@@$       @@@      $@@F  g@@@       @@@   @@@L         4@@@   $@@$        
  ~@y     _PgFFFFFFFFFFFgR_     a@              4@@$       @@@____yg@@F   $@@$       @@@L  @@@L         4@@@   $@@$ggggggg 
   `4$_  yFaEZZZZZZZZZZZZ$My  y@F               4@@$       @@@@@@@@@@y_   $@@$       @@@L  @@@L         4@@@   $@@@RRRRRRR 
     ~4$g@$yyyyagggggyyyyy@@g@F                 4@@$       @@@    `~@@@   4@@$       @@@   @@@L         4@@@   $@@$        
        ~$$~~~~~~~~~~~~~~~@F~                   4@@$       @@@      @@@L  4@@@      y@@@   @@@L         4@@@   $@@$        
        =$@===============@P                    4@@$       @@@      @@@[   $@@L    _$@@F   @@@L         4@@@   $@@$        
        a$$aaaaaaaaaaa uaa@w                    4@@$       @@@      $@@$    4@@@ggg@@@F    @@@@@@@@@@@$ 4@@@   $@@@@@@@@@@@
         $$               @L                    `~~~       ~~~      `~~~     `~FPPPF~      ~~~~~~~~~~~^ `~~~   ^~~~~~~~~~~~
         4@aaaaaaaaaaaaaaa@L
"""


# ── Conformance profiles ───────────────────────────────────────────────────────
PROFILES: dict[str, dict] = {
    "forecasting": {
        "label": "Forecasting",
        "match": "forecasting/conformance",
        "path": str(
            _REPO_ROOT / "test/forecasting/conformance/test_forecasting_conformance.py"
        ),
        "description": "Core forecasting limits functionality",
    },
    "realtime": {
        "label": "Real-Time",
        "match": "realtime/conformance",
        "path": str(
            _REPO_ROOT / "test/realtime/conformance/test_realtime_conformance.py"
        ),
        "description": "Real-time limits snapshot functionality",
    },
    "seasonal": {
        "label": "Seasonal",
        "match": "seasonal/conformance",
        "path": str(
            _REPO_ROOT / "test/seasonal/conformance/test_seasonal_conformance.py"
        ),
        "description": "Seasonal ratings functionality",
    },
    "seasonal_overrides": {
        "label": "Seasonal Overrides",
        "match": "seasonal_overrides/conformance",
        "path": str(
            _REPO_ROOT
            / "test/seasonal_overrides/conformance/test_seasonal_overrides.py"
        ),
        "description": "Seasonal overrides functionality",
    },
    "temporary_aar_exceptions": {
        "label": "Temporary AAR Exceptions",
        "match": "temporary_aar_exceptions/conformance",
        "path": str(
            _REPO_ROOT
            / "test/temporary_aar_exceptions/conformance/test_temporary_aar_exceptions.py"
        ),
        "description": "Temporary AAR exceptions functionality",
    },
    "monitoring_sets": {
        "label": "Monitoring Sets",
        "match": "monitoring_sets/conformance",
        "path": str(
            _REPO_ROOT / "test/monitoring_sets/conformance/test_monitoring_sets.py"
        ),
        "description": "Monitoring sets functionality",
    },
}


# ── Terminal colour helpers ────────────────────────────────────────────────────
def _is_tty() -> bool:
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


class _C:
    """ANSI escape codes — automatically disabled when stdout is not a TTY."""

    _on = _is_tty()
    RESET = "\033[0m" if _on else ""
    BOLD = "\033[1m" if _on else ""
    DIM = "\033[2m" if _on else ""
    GREEN = "\033[32m" if _on else ""
    RED = "\033[31m" if _on else ""
    YELLOW = "\033[33m" if _on else ""
    CYAN = "\033[36m" if _on else ""
    B_GREEN = "\033[1;32m" if _on else ""
    B_RED = "\033[1;31m" if _on else ""
    B_CYAN = "\033[1;36m" if _on else ""


# ── Data model ─────────────────────────────────────────────────────────────────
@dataclass
class ScenarioResult:
    nodeid: str
    feature: Optional[str]
    scenario: Optional[str]
    outcome: str  # "passed" | "failed" | "skipped"
    failure_summary: Optional[str] = None
    skip_reason: Optional[str] = None


@dataclass
class ProfileResults:
    key: str
    label: str
    description: str
    results: list[ScenarioResult] = field(default_factory=list)

    @property
    def passed(self) -> list[ScenarioResult]:
        return [r for r in self.results if r.outcome == "passed"]

    @property
    def failed(self) -> list[ScenarioResult]:
        return [r for r in self.results if r.outcome == "failed"]

    @property
    def skipped(self) -> list[ScenarioResult]:
        return [r for r in self.results if r.outcome == "skipped"]

    @property
    def conformant(self) -> bool:
        return len(self.failed) == 0 and len(self.results) > 0


# ── pytest plugin ──────────────────────────────────────────────────────────────
class _ConformancePlugin:
    """Collects BDD test results and optionally prints live progress dots."""

    def __init__(
        self,
        profile_results: dict[str, ProfileResults],
        verbose: bool = False,
    ):
        self._profiles = profile_results
        self._verbose = verbose
        # nodeid → (feature_name, scenario_name)
        self._bdd_meta: dict[str, tuple[str, str]] = {}
        self._progress_started: set[str] = set()

    # ── pytest-bdd hook: captures human-readable names before the scenario runs
    def pytest_bdd_before_scenario(self, request, feature, scenario):
        self._bdd_meta[request.node.nodeid] = (feature.name, scenario.name)

    def pytest_runtest_logreport(self, report):
        # Capture the "call" phase for normal outcomes; "setup" for early skips
        is_early_skip = report.when == "setup" and report.skipped
        if report.when != "call" and not is_early_skip:
            return

        nodeid = report.nodeid
        feature_name, scenario_name = self._bdd_meta.get(
            nodeid, (None, _humanize(nodeid))
        )

        if report.passed:
            outcome = "passed"
        elif report.skipped:
            outcome = "skipped"
        else:
            outcome = "failed"

        failure_summary: Optional[str] = None
        skip_reason: Optional[str] = None

        if report.failed and report.longrepr:
            failure_summary = _summarize_failure(report.longrepr)
        if report.skipped and report.longrepr:
            skip_reason = _summarize_skip(report.longrepr)

        result = ScenarioResult(
            nodeid=nodeid,
            feature=feature_name,
            scenario=scenario_name,
            outcome=outcome,
            failure_summary=failure_summary,
            skip_reason=skip_reason,
        )

        pkey = self._profile_key_for(nodeid)
        if pkey and pkey in self._profiles:
            self._profiles[pkey].results.append(result)

        if self._verbose:
            self._emit_dot(pkey, outcome)

    def _profile_key_for(self, nodeid: str) -> Optional[str]:
        for key, info in PROFILES.items():
            if info["match"] in nodeid:
                return key
        return None

    def _emit_dot(self, profile_key: Optional[str], outcome: str) -> None:
        label = (
            PROFILES[profile_key]["label"]
            if profile_key and profile_key in PROFILES
            else "(unknown)"
        )
        if profile_key not in self._progress_started:
            sep = "\n" if self._progress_started else ""
            print(f"{sep}  {_C.BOLD}{label:<28}{_C.RESET}", end="", flush=True)
            self._progress_started.add(profile_key)

        if outcome == "passed":
            print(f"{_C.GREEN}.{_C.RESET}", end="", flush=True)
        elif outcome == "failed":
            print(f"{_C.RED}F{_C.RESET}", end="", flush=True)
        else:
            print(f"{_C.YELLOW}s{_C.RESET}", end="", flush=True)


# ── Helpers ────────────────────────────────────────────────────────────────────
def _humanize(nodeid: str) -> str:
    """Convert a pytest node ID into a readable scenario label."""
    parts = nodeid.split("::")
    name = parts[-1] if len(parts) > 1 else nodeid
    name = name.removeprefix("test_")
    base, _, params = name.partition("[")
    base = base.replace("_", " ").strip()
    if params:
        return f"{base} [{params.rstrip(']').replace('_', ' ')}]"
    return base


def _summarize_failure(longrepr) -> str:
    """Extract the most useful line from a pytest failure representation."""
    text = str(longrepr)
    lines = [ln for ln in text.splitlines() if ln.strip()]
    # Prefer lines that look like assertion errors
    for line in reversed(lines):
        stripped = line.strip()
        if (
            stripped.startswith("AssertionError")
            or stripped.startswith("assert ")
            or (stripped.startswith("E ") and len(stripped) > 2)
        ):
            return stripped.lstrip("E").strip()
    return lines[-1].strip() if lines else str(longrepr)


def _summarize_skip(longrepr) -> str:
    """Extract the skip reason from a pytest skip representation."""
    if isinstance(longrepr, tuple) and len(longrepr) == 3:
        return str(longrepr[2]).removeprefix("Skipped: ").strip()
    return str(longrepr).strip()


# ── Report renderer ────────────────────────────────────────────────────────────
_W = 72  # report width


def _rule(char: str = "─") -> str:
    return char * _W


def _print_report(
    profiles: dict[str, ProfileResults],
    target_url: str,
    show_skipped: bool = True,
) -> int:
    """
    Render the conformance report to stdout.
    Returns 0 if all tested profiles are conformant, 1 otherwise.
    """
    inner = _W - 4

    def _box_line(text: str) -> str:
        if len(text) > inner:
            text = text[: inner - 1] + "…"
        return f"║ {text:<{inner}} ║"

    print()
    print(f"{_C.B_CYAN}╔{'═' * (_W - 2)}╗{_C.RESET}")
    print(f"{_C.B_CYAN}{_box_line('TROLIE Conformance Report')}{_C.RESET}")
    print(f"{_C.B_CYAN}{_box_line(f'Target:  {target_url}')}{_C.RESET}")
    print(f"{_C.B_CYAN}╚{'═' * (_W - 2)}╝{_C.RESET}")
    print()

    overall_pass = overall_fail = overall_skip = 0
    any_tested = False

    for profile in profiles.values():
        if not profile.results:
            continue
        any_tested = True

        n_pass = len(profile.passed)
        n_fail = len(profile.failed)
        n_skip = len(profile.skipped)
        overall_pass += n_pass
        overall_fail += n_fail
        overall_skip += n_skip

        verdict = (
            f"{_C.B_GREEN}CONFORMANT{_C.RESET}"
            if profile.conformant
            else f"{_C.B_RED}NON-CONFORMANT{_C.RESET}"
        )
        print(f"{_C.BOLD}{profile.label}{_C.RESET}  {verdict}")
        print(f"{_C.DIM}{profile.description}{_C.RESET}")
        print(f"{_C.DIM}{_rule()}{_C.RESET}")

        # Group scenarios by their parent feature name
        by_feature: dict[str, list[ScenarioResult]] = {}
        for r in profile.results:
            feat = r.feature or "Scenarios"
            by_feature.setdefault(feat, []).append(r)

        for feat_name, scenarios in by_feature.items():
            print(f"\n  {_C.BOLD}{feat_name}{_C.RESET}")
            for r in scenarios:
                name = r.scenario or _humanize(r.nodeid)
                if r.outcome == "passed":
                    icon = f"{_C.GREEN}✓{_C.RESET}"
                    label = f"{_C.GREEN}{name}{_C.RESET}"
                    detail = ""
                elif r.outcome == "failed":
                    icon = f"{_C.RED}✗{_C.RESET}"
                    label = f"{_C.RED}{name}{_C.RESET}"
                    detail = (
                        f"\n       {_C.DIM}{r.failure_summary}{_C.RESET}"
                        if r.failure_summary
                        else ""
                    )
                else:
                    if not show_skipped:
                        continue
                    icon = f"{_C.YELLOW}○{_C.RESET}"
                    label = f"{_C.YELLOW}{name}{_C.RESET}"
                    detail = (
                        f"  {_C.DIM}({r.skip_reason}){_C.RESET}"
                        if r.skip_reason
                        else ""
                    )
                print(f"    {icon}  {label}{detail}")

        print()
        print(
            f"  {_C.GREEN}{n_pass} passed{_C.RESET}  "
            f"{_C.RED}{n_fail} failed{_C.RESET}  "
            f"{_C.YELLOW}{n_skip} skipped{_C.RESET}"
        )
        print()

    # ── Overall summary ────────────────────────────────────────────────────────
    all_conformant = overall_fail == 0 and any_tested
    verdict = (
        f"{_C.B_GREEN}CONFORMANT{_C.RESET}"
        if all_conformant
        else f"{_C.B_RED}NON-CONFORMANT{_C.RESET}"
    )
    print(_rule("═"))
    print(f"  Overall:  {verdict}")
    print(
        f"  {_C.GREEN}{overall_pass} passed{_C.RESET}  "
        f"{_C.RED}{overall_fail} failed{_C.RESET}  "
        f"{_C.YELLOW}{overall_skip} skipped{_C.RESET}"
    )
    print(_rule("═"))
    print()

    return 0 if all_conformant else 1


# ── CLI ────────────────────────────────────────────────────────────────────────
def _build_parser() -> argparse.ArgumentParser:
    profile_help = "  \n".join(
        f"  {k:<30} {v['description']}" for k, v in PROFILES.items()
    )
    parser = argparse.ArgumentParser(
        prog="trolie-conform",
        description=(
            "Run TROLIE conformance tests against an implementation\n"
            "and output a formatted conformance report to stdout."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"Available profiles:\n{profile_help}",
    )
    parser.add_argument(
        "--url",
        metavar="URL",
        default=os.getenv("TROLIE_BASE_URL", "http://localhost:4010"),
        help=(
            "Base URL of the TROLIE implementation under test "
            "(default: $TROLIE_BASE_URL or http://localhost:4010)"
        ),
    )
    parser.add_argument(
        "--token",
        metavar="TOKEN",
        default=os.getenv("RATINGS_PROVIDER_TOKEN"),
        help="Bearer token for the Ratings Provider role (default: $RATINGS_PROVIDER_TOKEN)",
    )
    parser.add_argument(
        "--profile",
        action="append",
        choices=list(PROFILES),
        metavar="PROFILE",
        dest="profiles",
        help=(
            f"Conformance profile to run (repeatable; default: all). "
            f"Choices: {', '.join(PROFILES)}"
        ),
    )
    parser.add_argument(
        "--ssl-verify",
        action="store_true",
        default=False,
        help="Enable SSL certificate verification (disabled by default)",
    )
    parser.add_argument(
        "--hide-skipped",
        action="store_true",
        default=False,
        help="Omit skipped scenarios from the report",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        help="Print per-test progress dots while the suite runs",
    )
    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    # ── Configure environment ──────────────────────────────────────────────────
    os.environ["TROLIE_BASE_URL"] = args.url
    if args.token:
        os.environ["RATINGS_PROVIDER_TOKEN"] = args.token
    if args.ssl_verify:
        os.environ["TROLIE_VERIFY_SSL"] = "true"

    # ── Resolve profiles ───────────────────────────────────────────────────────
    selected = args.profiles or list(PROFILES)

    missing = [k for k in selected if not Path(PROFILES[k]["path"]).exists()]
    for k in missing:
        print(
            f"warning: conformance test file for profile '{k}' not found, skipping",
            file=sys.stderr,
        )
    selected = [k for k in selected if k not in missing]

    if not selected:
        print("error: no valid conformance profiles to run", file=sys.stderr)
        return 2

    profile_results: dict[str, ProfileResults] = {
        key: ProfileResults(
            key=key,
            label=PROFILES[key]["label"],
            description=PROFILES[key]["description"],
        )
        for key in selected
    }

    # ── Banner ─────────────────────────────────────────────────────────────────
    print(f"{_C.CYAN}{_BANNER}{_C.RESET}", end="")
    print(
        f"{_C.BOLD}Target:{_C.RESET}  {_C.CYAN}{args.url}{_C.RESET}"
    )
    if args.verbose:
        print(f"{_C.DIM}  (. pass  F fail  s skip){_C.RESET}")

    # ── Run pytest ─────────────────────────────────────────────────────────────
    plugin = _ConformancePlugin(profile_results, verbose=args.verbose)

    pytest_args = [
        "--rootdir",
        str(_REPO_ROOT),
        "-p",
        "no:terminal",  # suppress pytest's own terminal output
        # Note: --tb is owned by the terminal plugin so it cannot be used here
        "-p",
        "no:logging",  # suppress log capture output
        *[PROFILES[k]["path"] for k in selected],
    ]

    try:
        pytest_exit = pytest.main(pytest_args, plugins=[plugin])
    except KeyboardInterrupt:
        print("\nInterrupted.", file=sys.stderr)
        return 130

    if args.verbose:
        print()  # end the dots line

    # ── Render report ──────────────────────────────────────────────────────────
    report_exit = _print_report(
        profile_results,
        args.url,
        show_skipped=not args.hide_skipped,
    )

    # pytest exit codes: 0=all passed, 1=some failed, 2=interrupted,
    # 3=internal error, 4=usage error, 5=no tests collected
    if pytest_exit not in (0, 1):
        print(
            f"warning: pytest exited with code {pytest_exit} "
            "(check the output above for details)",
            file=sys.stderr,
        )
        return int(pytest_exit)

    return report_exit


if __name__ == "__main__":
    sys.exit(main())
