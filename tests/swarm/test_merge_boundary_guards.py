"""T05.05 / FR-012 -- four-guard wiring assertion for the mechanical-merge
boundary.

This test is the *meta-guard*: it verifies that every one of the four
structural guards on ``src/superclaude/cli/swarm/merge.py`` is still
present and discoverable. The individual guards each have their own
enforcement mechanism (docstring text, LOC counter, CI workflow,
3-worker concat test); this file asserts the wiring is intact so a
well-meaning refactor cannot silently dismantle one corner of the
boundary while leaving the others looking fine.

The four guards (T05.05 acceptance):

1. **Docstring contract** -- ``merge.py`` module docstring must
   explicitly enumerate ALLOWED and DISALLOWED operations so reviewers
   can pattern-match drift on inspection.
2. **<=30 LOC ceiling** -- enforced by
   ``tests/swarm/test_merge_loc_ceiling.py`` (T05.08, NFR-008).
3. **PR-review discipline** -- enforced by
   ``.github/workflows/boundary-guard.yml`` which flags PR touches on
   the boundary files and writes a structured reviewer checklist into
   the run summary.
4. **Boundary test** -- ``tests/swarm/test_merge_mechanical_only.py``
   (T05.09, NFR-009) pins 3-worker concat, slot-index order, verbatim
   bodies, and provenance-header-only output.

A failure here means a guard was removed or renamed without updating
the wiring. Fix by restoring the guard or, if intentional, updating
this test plus the merge.py docstring's "four structural guards"
section in lockstep.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

import superclaude.cli.swarm.merge as merge_module

REPO_ROOT = Path(__file__).resolve().parents[2]
MERGE_PATH = Path(merge_module.__file__)
LOC_CEILING_TEST = REPO_ROOT / "tests" / "swarm" / "test_merge_loc_ceiling.py"
MECHANICAL_TEST = REPO_ROOT / "tests" / "swarm" / "test_merge_mechanical_only.py"
BOUNDARY_WORKFLOW = REPO_ROOT / ".github" / "workflows" / "boundary-guard.yml"


# --- Guard 1: docstring contract ------------------------------------------


def _module_docstring() -> str:
    doc = merge_module.__doc__
    assert doc, "merge.py module docstring missing entirely -- Guard 1 lost."
    return doc


def test_guard1_docstring_enumerates_allowed_operations() -> None:
    """The module docstring must label the ALLOWED operations block."""
    doc = _module_docstring()
    assert "ALLOWED operations" in doc, (
        "merge.py docstring must contain an 'ALLOWED operations' section "
        "enumerating exactly the surface the module is permitted to grow "
        "into (verbatim concat, slot-index sort, provenance header). "
        "Guard 1 (docstring contract) is the first-line review aid."
    )


def test_guard1_docstring_enumerates_disallowed_operations() -> None:
    """The module docstring must label the DISALLOWED operations block."""
    doc = _module_docstring()
    assert "DISALLOWED operations" in doc, (
        "merge.py docstring must contain a 'DISALLOWED operations' "
        "section enumerating the boundary violations (sort / score / "
        "dedup / filter / rewrite / reorder). Guard 1 (docstring "
        "contract) makes these the first thing a reviewer reads."
    )


@pytest.mark.parametrize(
    "forbidden_term",
    [
        "sort",
        "rank",
        "score",
        "dedup",
        "filter",
        "rewrite",
        "reorder",
    ],
)
def test_guard1_docstring_lists_every_disallowed_term(forbidden_term: str) -> None:
    """Each of the seven canonical forbidden operations must appear in the
    DISALLOWED block. If a term goes missing, drift becomes invisible to
    a docstring-only reviewer."""
    doc = _module_docstring().lower()
    assert forbidden_term in doc, (
        f"merge.py docstring no longer names '{forbidden_term}' as a "
        "DISALLOWED operation. Restore the term in the DISALLOWED "
        "block -- the enumeration is load-bearing for review discipline."
    )


def test_guard1_docstring_names_provenance_header_format() -> None:
    """The exact provenance header format must be pinned in the docstring
    so any reformat is caught on inspection, not just by the boundary
    test."""
    doc = _module_docstring()
    assert "## From {model_label} ({elapsed_ms}ms)" in doc, (
        "merge.py docstring no longer pins the exact provenance header "
        "format '## From {model_label} ({elapsed_ms}ms)'. Restore it -- "
        "this is the one structural addition the module is allowed to "
        "make to worker bodies."
    )


def test_guard1_docstring_enumerates_all_four_guards() -> None:
    """The 'four structural guards' section must remain in the docstring
    and reference each guard's enforcement mechanism."""
    doc = _module_docstring()
    assert "four structural guards" in doc.lower(), (
        "merge.py docstring must keep its 'four structural guards' "
        "section -- it is the discovery surface that points reviewers "
        "at this meta-test and the three enforcement mechanisms."
    )
    assert "test_merge_loc_ceiling.py" in doc, (
        "Guard 2 enforcement reference missing from docstring."
    )
    assert "test_merge_mechanical_only.py" in doc, (
        "Guard 4 enforcement reference missing from docstring."
    )


# --- Guard 2: <=30 LOC ceiling --------------------------------------------


def test_guard2_loc_ceiling_test_file_exists() -> None:
    """The LOC-ceiling test file must be present at the documented path."""
    assert LOC_CEILING_TEST.is_file(), (
        f"Guard 2 enforcement test missing: {LOC_CEILING_TEST.relative_to(REPO_ROOT)}. "
        "Restore the test or update the four-guards wiring in merge.py "
        "+ this meta-guard in lockstep."
    )


def test_guard2_loc_ceiling_test_pins_thirty_line_limit() -> None:
    """The LOC ceiling must remain at 30 (NFR-008). Relaxing the ceiling
    silently is a Guard 2 bypass; the constant must change in the test
    file *and* the docstring must be updated in the same review."""
    source = LOC_CEILING_TEST.read_text(encoding="utf-8")
    assert "LOC_CEILING = 30" in source, (
        f"Guard 2 ceiling no longer pinned at 30 in {LOC_CEILING_TEST.relative_to(REPO_ROOT)}. "
        "If NFR-008 was intentionally raised, update merge.py docstring's "
        "'<=30 LOC' references and this assertion together."
    )


# --- Guard 3: PR-review discipline (CI workflow) --------------------------


def test_guard3_boundary_ci_workflow_exists() -> None:
    """The boundary-guard CI workflow must be present at the documented
    path so PR touches on merge.py trigger the human-review flag."""
    assert BOUNDARY_WORKFLOW.is_file(), (
        f"Guard 3 CI workflow missing: {BOUNDARY_WORKFLOW.relative_to(REPO_ROOT)}. "
        "Restore it or update the four-guards wiring -- without this "
        "workflow, PR touches on merge.py merge without elevated review."
    )


def test_guard3_boundary_ci_workflow_triggers_on_merge_path() -> None:
    """The workflow must list ``src/superclaude/cli/swarm/merge.py`` in
    its ``pull_request.paths`` filter so it actually runs on merge.py
    edits."""
    data = yaml.safe_load(BOUNDARY_WORKFLOW.read_text(encoding="utf-8"))
    # PyYAML parses bare-word ``on:`` as boolean True.
    triggers = data.get("on") or data.get(True)
    assert triggers is not None, (
        "boundary-guard.yml has no triggers section -- workflow will "
        "never run. Restore 'on: pull_request:' with paths filter."
    )
    pr_block = triggers["pull_request"]
    paths = pr_block.get("paths", [])
    assert "src/superclaude/cli/swarm/merge.py" in paths, (
        "boundary-guard.yml does not list merge.py in pull_request.paths "
        "-- the workflow will not trigger on the file it is supposed to "
        "guard. Add it back to the paths filter."
    )


@pytest.mark.parametrize(
    "guarded_path",
    [
        "src/superclaude/cli/swarm/merge.py",
        "tests/swarm/test_merge_mechanical_only.py",
        "tests/swarm/test_merge_loc_ceiling.py",
    ],
)
def test_guard3_boundary_ci_workflow_covers_all_core_files(guarded_path: str) -> None:
    """Each core boundary file must appear in the workflow's paths filter
    so any edit to any of the four guards routes through human review."""
    data = yaml.safe_load(BOUNDARY_WORKFLOW.read_text(encoding="utf-8"))
    triggers = data.get("on") or data.get(True)
    paths = triggers["pull_request"].get("paths", [])
    assert guarded_path in paths, (
        f"boundary-guard.yml missing '{guarded_path}' from pull_request.paths "
        "-- edits to this guard file would not surface the boundary-touch "
        "warning on review."
    )


# --- Guard 4: boundary test file ------------------------------------------


def test_guard4_boundary_test_file_exists() -> None:
    """The 3-worker mechanical-only boundary test file must be present
    at the documented path."""
    assert MECHANICAL_TEST.is_file(), (
        f"Guard 4 boundary test missing: {MECHANICAL_TEST.relative_to(REPO_ROOT)}. "
        "Restore the test or update merge.py docstring's four-guards "
        "section -- without this test, slot-index ordering and verbatim "
        "passthrough are no longer pinned."
    )


def test_guard4_boundary_test_covers_three_workers() -> None:
    """The boundary test must reference three workers (per NFR-009
    acceptance) and exercise slot-index ordering."""
    source = MECHANICAL_TEST.read_text(encoding="utf-8")
    assert "three_workers" in source, (
        f"{MECHANICAL_TEST.relative_to(REPO_ROOT)} no longer references "
        "a 3-worker fixture. Guard 4 acceptance requires a 3-worker "
        "concat assertion."
    )
    assert (
        "slot" in source.lower()
        or "slot_index" in source.lower()
        or "slot-index" in source.lower()
    ), (
        f"{MECHANICAL_TEST.relative_to(REPO_ROOT)} no longer documents "
        "slot-index ordering in its assertions. Guard 4 must pin "
        "ordering by WorkerResult.index."
    )


# --- All-guards-present aggregate snapshot --------------------------------


def test_all_four_guards_wired() -> None:
    """Aggregate check: every guard file/mechanism is present.

    Failure here means a guard wiring went missing. The per-guard tests
    above pinpoint *which* guard; this test exists so a single-glance
    pytest summary line still flags the boundary even when filter flags
    skip the granular tests.
    """
    missing: list[str] = []
    if not MERGE_PATH.is_file():
        missing.append(f"Guard 0 (module itself): {MERGE_PATH}")
    if not LOC_CEILING_TEST.is_file():
        missing.append(f"Guard 2 (LOC ceiling test): {LOC_CEILING_TEST}")
    if not BOUNDARY_WORKFLOW.is_file():
        missing.append(f"Guard 3 (CI workflow): {BOUNDARY_WORKFLOW}")
    if not MECHANICAL_TEST.is_file():
        missing.append(f"Guard 4 (boundary test): {MECHANICAL_TEST}")
    doc = merge_module.__doc__ or ""
    if "ALLOWED operations" not in doc or "DISALLOWED operations" not in doc:
        missing.append("Guard 1 (docstring contract)")
    assert not missing, (
        "Mechanical-merge boundary guards missing:\n  - "
        + "\n  - ".join(missing)
        + "\nRestore the guard(s) or, if intentional, update merge.py "
        "docstring's 'four structural guards' section and this "
        "meta-guard in lockstep."
    )
