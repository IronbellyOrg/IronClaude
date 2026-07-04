"""Shared fixtures for the ``tests/pr_submit`` suite (spec §6.3).

Provides ``load_fixture`` (the JSON fixture loader), ``mock_gh`` (in-process
monkeypatch of the ``pr_submit`` gh-wrapper seam, recording argv to assert the
``--repo`` pin), ``mock_monitor`` (stubs Monitor arming), ``fixture_findings``
(loads a finding set), and ``tmp_skill_dir`` (a ``tmp_path``-based skill dir). The
in-process monkeypatch is preferred over a PATH-shim for unit speed (research/04 §D).
"""

from __future__ import annotations

import ast
import inspect
import json
import re
from pathlib import Path

import pytest

from superclaude.pr_submit.contract_setup import candidate as _candidate_mod
from superclaude.pr_submit.contract_setup import diagnosis as _diagnosis_mod
from superclaude.pr_submit.contract_setup import lockgate as _lockgate_mod
from superclaude.pr_submit.contract_setup import validation as _validation_mod

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def load_fixture():
    """Return a loader: ``load_fixture("name.json")`` → parsed JSON from ``fixtures/``."""

    def _load(name: str):
        return json.loads((FIXTURES_DIR / name).read_text(encoding="utf-8"))

    return _load


@pytest.fixture
def mock_gh(monkeypatch):
    """Monkeypatch the ``detection`` poll seam to a fixture-returning fake; record calls.

    Returns a recorder object: set ``recorder.payload`` to control the returned poll
    payload; read ``recorder.calls`` (a list of pr_num args) to assert invocations.
    Keeps tests in-process (no subprocess) per the repo's unit-speed precedent.
    """
    from superclaude.pr_submit import detection

    class _MockGh:
        def __init__(self) -> None:
            self.calls: list = []
            self.payload: dict = {"reviews": [], "comments": []}

        def fetch(self, pr_num):
            self.calls.append(pr_num)
            return dict(self.payload)

    recorder = _MockGh()
    monkeypatch.setattr(detection, "_fetch_payload", recorder.fetch)
    return recorder


@pytest.fixture
def mock_monitor():
    """A stand-in for the Monitor arming seam — records each arm call."""

    class _MockMonitor:
        def __init__(self) -> None:
            self.calls = 0

        def __call__(self, *_args, **_kwargs) -> None:
            self.calls += 1

    return _MockMonitor()


@pytest.fixture
def fixture_findings():
    """Load the default finding set (the medium+high AC-2 fixture)."""
    return json.loads(
        (FIXTURES_DIR / "finding-medium-high.json").read_text(encoding="utf-8")
    )


@pytest.fixture
def tmp_skill_dir(tmp_path, monkeypatch):
    """A tmp_path-based skill/output dir for run-log and artifact writes."""
    d = tmp_path / "pr-monitor"
    d.mkdir(parents=True, exist_ok=True)
    return d


# ===========================================================================
# FX5 — gate-helper negative + differential coverage collector (Step 2.7a).
#
# Regression lock for the F4 class. GATE_LOAD_BEARING_HELPERS is the ENFORCED
# registry: every entry MUST carry BOTH a negative AND a differential
# (mutation-must-fail) test in
# tests/pr_submit/test_gate_helper_differentials.py (HELPER_TEST_MAP). The
# pytest_generate_tests hook reports one test id per registered helper (so a
# missing pair FAILs that helper individually), and a drift alarm FAILs when a
# NEW gate-shaped module-level helper appears unregistered. There is NO
# per-helper exemption: a registered helper may never skip its pair.
#
# Residual-risk NON-GOALS (documented, research/02 §4.3 / MEDIUM-2):
#   * Auto-enumeration: the drift alarm walks MODULE-LEVEL defs ONLY, so dataclass
#     methods (validation.ValidationReport.passed,
#     candidate.CandidateContract.required_unobserved) and the validation._*_checks
#     builder family are NOT auto-enumerable — a future gate helper of those shapes
#     must be hand-registered. The two load-bearing ones
#     (candidate.CandidateContract.required_unobserved §5.3,
#     validation._negative_control_checks §5.5) ARE hand-registered with pairs.
#   * Scope boundary: gate-load-bearing helpers OUTSIDE these 4 modules
#     (classify, DetectionContract.from_yaml, load_evidence) are handed to their
#     own suites; FX5 does not cover them.
# ===========================================================================

GATE_LOAD_BEARING_HELPERS = (
    # Drift-alarm-matched module-level gate helpers (9).
    "candidate._path_resolves",
    "candidate._findings_locus",
    "candidate._review_completeness_signal",
    "candidate._selected_identity",
    "candidate._selected_app_slug",
    "lockgate._paths_resolve",
    "lockgate._emission_shape_observed",
    "diagnosis._resolve_optional_path",
    "diagnosis._stale_blockers",
    # Hand-registered (2) — outside the auto-enumerated drift-alarm set by design.
    "candidate.CandidateContract.required_unobserved",
    "validation._negative_control_checks",
)

_GATE_MODULES = {
    "candidate": _candidate_mod,
    "lockgate": _lockgate_mod,
    "diagnosis": _diagnosis_mod,
    "validation": _validation_mod,
}

# The SINGLE documented gate-shaped pattern (Step 2.4 reconciliation, resolution
# (ii)): the task brief's literal pattern over-matched 5 non-gate resolution
# primitives (candidate._observed_logins/_observed_app_slugs/_observed_associations/
# _observed_severity_path via bare `_observed_`, and candidate._shape_observed via
# `_shape_observed`). The bare `_observed_` token was dropped and `_shape_observed`
# narrowed to `_emission_shape_observed` so this pattern's matched set over the 4
# modules' module-level defs EQUALS exactly the 9 registered module-level helpers
# above (a strict subset of the 11-helper registry) — never a superset.
GATE_HELPER_DEF_PATTERN = re.compile(
    r"_(path|paths)_resolv|_resolve_|_findings_|_selected_|_stale_"
    r"|_emission_shape_observed|_review_completeness"
)


def _differentials_module():
    """Return the FX5 differential test module (its HELPER_TEST_MAP + test names)."""
    try:
        import test_gate_helper_differentials as module

        return module
    except ImportError:  # pragma: no cover - fallback if not yet on sys.path
        import importlib.util

        path = Path(__file__).parent / "test_gate_helper_differentials.py"
        spec = importlib.util.spec_from_file_location(
            "test_gate_helper_differentials", path
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module


def _resolve_dotted(dotted: str) -> object:
    """Resolve a `module.attr[.attr...]` dotted name on the live gate module."""
    module_name, _, rest = dotted.partition(".")
    obj: object = _GATE_MODULES[module_name]
    for attr in rest.split("."):
        obj = getattr(obj, attr)
    return obj


def _module_level_gate_shaped_defs() -> list[str]:
    """Dotted names of MODULE-LEVEL defs matching the gate-shaped pattern."""
    matched: list[str] = []
    for module_name, module in _GATE_MODULES.items():
        tree = ast.parse(inspect.getsource(module), filename=module.__file__)
        for node in tree.body:  # module-level only: parent is ast.Module
            if isinstance(node, ast.FunctionDef) and GATE_HELPER_DEF_PATTERN.search(
                node.name
            ):
                matched.append(f"{module_name}.{node.name}")
    return matched


def assert_gate_helper_has_negative_and_differential(dotted: str) -> None:
    """Existence + coverage + drift-alarm assertions for one registered helper."""
    module = _differentials_module()
    helper_map = module.HELPER_TEST_MAP

    # Registry ≡ authored-pair set — the two can never silently diverge.
    assert set(GATE_LOAD_BEARING_HELPERS) == set(helper_map), (
        "GATE_LOAD_BEARING_HELPERS ≠ HELPER_TEST_MAP keys: "
        f"registry-only={sorted(set(GATE_LOAD_BEARING_HELPERS) - set(helper_map))}, "
        f"map-only={sorted(set(helper_map) - set(GATE_LOAD_BEARING_HELPERS))}."
    )

    # (a) Existence — the registered helper still resolves on the live module.
    try:
        assert _resolve_dotted(dotted) is not None
    except (KeyError, AttributeError) as exc:
        raise AssertionError(
            f"Registered gate helper {dotted!r} no longer resolves on the live "
            f"module ({exc!r}); a silent rename orphaned its FX5 tests."
        ) from exc

    # (b) Coverage — both a negative and a differential test are registered AND exist.
    entry = helper_map.get(dotted, {})
    for kind in ("negative", "differential"):
        name = entry.get(kind)
        assert name, f"Gate helper {dotted!r} is missing a {kind.upper()} test entry."
        assert hasattr(module, name), (
            f"Gate helper {dotted!r} {kind} test {name!r} is not defined in "
            "test_gate_helper_differentials.py."
        )

    # (c) Drift alarm — no unregistered gate-shaped MODULE-LEVEL helper.
    registry = set(GATE_LOAD_BEARING_HELPERS)
    for found in _module_level_gate_shaped_defs():
        assert found in registry, (
            f"New gate-shaped module-level helper {found!r} is not registered for "
            "FX5 coverage. Author its negative + differential pair and register it "
            "in HELPER_TEST_MAP + GATE_LOAD_BEARING_HELPERS, or (if genuinely not "
            "gate-load-bearing) tighten GATE_HELPER_DEF_PATTERN — never a per-helper "
            "carve-out."
        )


def pytest_generate_tests(metafunc):
    """Parametrize the FX5 coverage test one case per registered gate helper.

    Additive: pytest runs BOTH the plugin's pytest_collection_modifyitems and this
    package-scoped hook, so this does not conflict with the global plugin.
    """
    if metafunc.function.__name__ == "test_gate_helper_has_negative_and_differential":
        metafunc.parametrize(
            "gate_helper",
            list(GATE_LOAD_BEARING_HELPERS),
            ids=list(GATE_LOAD_BEARING_HELPERS),
        )


@pytest.fixture
def assert_gate_helper_coverage():
    """Expose the FX5 coverage assertion to the parametrized coverage test."""
    return assert_gate_helper_has_negative_and_differential
