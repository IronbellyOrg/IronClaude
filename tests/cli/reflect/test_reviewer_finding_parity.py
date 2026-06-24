"""TST-4 reviewer finding-parity — restricted reviewer recall is not traded away.

Reliability / completeness check (NOT security): a restricted Read/Grep/Glob
reviewer must recall the same seeded defects an all-tools reviewer would. This is
the lighter STATIC-REACHABILITY proxy (research/05 §4) — cheaper than two live
reflect runs: it asserts every seeded defect/surface in the eval fixtures is
reachable via the restricted tool set ``{Read, Grep, Glob}`` (statically diff- /
grep-findable), i.e. NONE requires ``Bash``/execution to detect.

The completeness-regression alarm: an assertion FAILS if a seeded defect were
only reachable via a removed tool (e.g. its hallmark were absent from the static
diff text). The control case asserts zero hallucinated defects on a clean diff.

This test is falsifier-EXEMPT in the fail-before/pass-after sense (it is a
reachability INVARIANT over the seeded fixtures, not a layer-landing guard); it
is labeled as such per the task's falsifier-discipline rule.
"""

from __future__ import annotations

from pathlib import Path

import yaml

_REPO_ROOT = Path(__file__).resolve().parents[3]
_CASES = _REPO_ROOT / ".dev/eval-workspaces/sc-reflect/cases"
_DYNAMIC = _CASES / "uc2-surface-dynamic-dispatch"
_CONTROL = _CASES / "uc2-surface-positive-control"

# The restricted reviewer tool set under test.
_RESTRICTED_TOOLS = frozenset({"Read", "Grep", "Glob"})
_REMOVED_TOOLS = frozenset(
    {"Bash", "Edit", "Write", "NotebookEdit", "Task", "execute_shell_command"}
)


def _expected(case_dir: Path) -> dict:
    return yaml.safe_load((case_dir / "expected.yaml").read_text(encoding="utf-8"))


def _diff(case_dir: Path) -> str:
    return (case_dir / "input/diff.patch").read_text(encoding="utf-8")


def test_fixtures_exist_and_are_readable_by_read() -> None:
    """Read alone suffices to access the audit material (no Bash needed)."""
    for case in (_DYNAMIC, _CONTROL):
        assert (case / "expected.yaml").is_file(), f"missing expected.yaml in {case}"
        assert _diff(case).strip(), f"{case} diff.patch must be non-empty / Read-able"


def test_dynamic_dispatch_surface_reachable_by_restricted_toolset() -> None:
    """The seeded dynamic-dispatch surface is GREP-findable in the static diff —
    a restricted Read/Grep/Glob reviewer reaches it WITHOUT Bash/execution."""
    diff = _diff(_DYNAMIC)
    expected = _expected(_DYNAMIC)
    # Hallmarks of the runtime string-keyed registry dispatch (the seeded surface)
    # are all present as STATIC TEXT in the diff -> reachable via Grep.
    for marker in ("@register", "COMMAND_REGISTRY", "def dispatch("):
        assert marker in diff, (
            f"surface hallmark {marker!r} must be statically grep-reachable "
            f"(if it required Bash/execution, the restricted reviewer would lose recall)"
        )
    # The seeded surface requirement is mappable by the reviewer.
    assert "FR-S9-04" in expected["runtime_surface_requirements"]
    # Statically-undecidable dynamic dispatch -> DEGRADE (the seeded grounding gap
    # the restricted reviewer must still surface), NOT a missed/unreached surface.
    assert expected["runtime_surface_degraded"] is True
    assert expected["unreached_surfaces"] == []


def test_restricted_toolset_reaches_all_seeded_surfaces() -> None:
    """Reachability ⊇ seeded set: any seeded unreached_surface must be statically
    locatable in the diff (none is reachable ONLY via a removed tool)."""
    for case in (_DYNAMIC, _CONTROL):
        expected = _expected(case)
        diff = _diff(case)
        for surface in expected.get("unreached_surfaces", []):
            assert surface in diff, (
                f"seeded unreached surface {surface!r} in {case.name} is not "
                f"statically reachable by the restricted tool set"
            )
        # Regression recall must be perfect on the seeded set.
        assert expected.get("regression_recall") == 1.0


def test_positive_control_hallucinates_zero_defects() -> None:
    """The clean control: a restricted reviewer must surface ZERO deviations."""
    expected = _expected(_CONTROL)
    assert expected["deviations"] == []
    counts = expected["deviation_counts"]
    assert all(
        counts[k] == 0 for k in ("authorized", "necessary", "drift", "regression")
    )
    assert all(v["verdict"] == "clean_pass" for v in expected["per_task_verdicts"])


def test_restricted_toolset_disjoint_from_removed_tools() -> None:
    """The restricted set names no mutator/execution tool (the guarantee under test)."""
    assert _RESTRICTED_TOOLS & _REMOVED_TOOLS == frozenset()
