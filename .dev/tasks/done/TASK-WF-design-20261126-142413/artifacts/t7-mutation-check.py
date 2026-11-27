"""In-memory mutation check for the Phase A depth pins (Task 7).

Run from the repository root with ``uv run python <this file>``. It loads
``tests/cli/reflect/test_remediation_route_table.py`` from its repository path, runs
the five new tests on the unmutated text, then runs nine mutations in memory.
No tracked file is written. Only AssertionError counts as a detection.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

TEST_FILE = Path("tests/cli/reflect/test_remediation_route_table.py").resolve()
TESTS = [
    "test_phase_a_depth_ref_region",
    "test_phase_a_depth_skill_region",
    "test_phase_a_depth_delegation_row",
    "test_no_placeholder_depth_on_sc_workflow_lines",
    "test_review_only_decision_stays_written_down",
]
SITE_TEST = {
    "ref": "test_phase_a_depth_ref_region",
    "skill": "test_phase_a_depth_skill_region",
    "row": "test_phase_a_depth_delegation_row",
}
FLAG = "--depth standard"
KINDS = {"deep": "--depth deep", "delete": "", "placeholder": "--depth <d>"}


def load_module():
    spec = importlib.util.spec_from_file_location("route_table_under_test", TEST_FILE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_tests(mod) -> dict[str, str]:
    result = {}
    for name in TESTS:
        try:
            getattr(mod, name)()
            result[name] = "pass"
        except AssertionError:
            result[name] = "fail"
    return result


def expected_failures(site: str, kind: str) -> set[str]:
    failing = {SITE_TEST[site]}
    if kind == "placeholder":
        failing.add("test_no_placeholder_depth_on_sc_workflow_lines")
    if site == "row" and kind == "deep":
        failing.add("test_review_only_decision_stays_written_down")
    return failing


def main() -> int:
    mod = load_module()
    ref0, skill0 = mod._REF, mod._SKILL
    # (variable the slice lives in, original text, slice text)
    sites = {
        "ref": ("_REF", ref0, mod._region(ref0, "### Phase A", "### Phase B")),
        "skill": ("_SKILL", skill0, mod._region(skill0, "- **Phase A", "- **Phase B")),
        "row": ("_SKILL", skill0, mod._delegation_row()),
    }
    mismatches = 0

    base = run_tests(mod)
    ok = all(v == "pass" for v in base.values())
    print(f"unmutated: {base} -> {'OK' if ok else 'MISMATCH'}")
    mismatches += 0 if ok else 1

    for site, (var, text0, piece) in sites.items():
        assert text0.count(piece) == 1, f"{site}: slice must occur once"
        assert piece.count(FLAG) == 1, f"{site}: slice must hold {FLAG!r} once"
        for kind, replacement in KINDS.items():
            changed_piece = piece.replace(FLAG, replacement, 1)
            changed = text0.replace(piece, changed_piece, 1)
            assert changed != text0, f"{site}/{kind}: mutation changed nothing"
            setattr(mod, var, changed)
            try:
                got = run_tests(mod)
            finally:
                setattr(mod, var, text0)
            failed = {n for n, v in got.items() if v == "fail"}
            want = expected_failures(site, kind)
            verdict = "OK" if failed == want else "MISMATCH"
            mismatches += 0 if failed == want else 1
            print(
                f"case {site}/{kind}: failed={sorted(failed)} "
                f"expected={sorted(want)} -> {verdict}"
            )

    restored = run_tests(mod)
    ok = all(v == "pass" for v in restored.values())
    print(f"restored: {restored} -> {'OK' if ok else 'MISMATCH'}")
    mismatches += 0 if ok else 1
    print(f"mismatches: {mismatches}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
