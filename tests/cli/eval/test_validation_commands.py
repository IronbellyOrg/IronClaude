"""Structural audit of ``docs/eval/validation-commands.md`` (OPS-004).

This test guards the OPS-004 contract documented at
``docs/eval/validation-commands.md`` (T06.11 / D-0114). It does **not**
execute the four validation commands itself — the operator-facing
reproduction recipe is in §6 of the document and is exercised manually
or by CI. The test instead asserts that the document continues to:

1. Reference each of the four canonical commands in the prescribed order.
2. Link the evidence log for each command under the canonical OPS-004
   evidence root.
3. Carry the structural sections required by the AC map.

If the contract is renegotiated (e.g. a fifth command is added or one
is dropped), update both the document and this test in the same commit
so the audit cannot drift silently.
"""

from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
DOC_PATH = REPO_ROOT / "docs" / "eval" / "validation-commands.md"
EVIDENCE_ROOT = (
    REPO_ROOT / ".dev" / "releases" / "current" / "cliEval" / "evidence" / "T06.11"
)

# The canonical four-command sequence pinned by OPS-004. Order matters —
# §3 of the document mandates "in order" execution. Each tuple is
# (command-substring, evidence-filename).
OPS_004_COMMANDS: tuple[tuple[str, str], ...] = (
    (
        "uv run pytest tests/cli/eval/test_describe.py tests/cli/eval/test_doctor.py -v",
        "01-targeted-pytest.log",
    ),
    (
        "make verify-sync",
        "02-make-verify-sync.log",
    ),
    (
        "uv run superclaude eval doctor",
        "03-eval-doctor.log",
    ),
    (
        "uv run superclaude eval run --suite real --eval E1",
        "04-eval-run-E1.log",
    ),
)

REQUIRED_SECTIONS: tuple[str, ...] = (
    "## 1. Contract",
    "## 2. Command details + evidence locations",
    "## 3. Execution order and idempotency",
    "## 4. Acceptance map (T06.11)",
    "## 5. Known blockers",
    "## 6. Reproducibility",
    "## 7. Cross-references",
)


@pytest.fixture(scope="module")
def doc_text() -> str:
    """Read ``validation-commands.md`` once per module."""

    assert DOC_PATH.exists(), (
        f"OPS-004 document missing at {DOC_PATH.relative_to(REPO_ROOT)}. "
        "T06.11 / D-0114 has not landed yet."
    )
    return DOC_PATH.read_text(encoding="utf-8")


def test_doc_exists_at_canonical_path() -> None:
    """The OPS-004 contract lives at ``docs/eval/validation-commands.md``."""

    assert DOC_PATH.is_file(), DOC_PATH


@pytest.mark.parametrize("command, _evidence", OPS_004_COMMANDS, ids=[
    "01-targeted-pytest",
    "02-make-verify-sync",
    "03-eval-doctor",
    "04-eval-run-E1",
])
def test_doc_references_each_command(
    doc_text: str, command: str, _evidence: str
) -> None:
    """Every OPS-004 command appears verbatim in the document."""

    assert command in doc_text, (
        f"OPS-004 command not found in {DOC_PATH.relative_to(REPO_ROOT)}: {command!r}"
    )


def test_doc_lists_commands_in_canonical_order(doc_text: str) -> None:
    """Commands appear in §1 in the prescribed inside-out order."""

    positions = [doc_text.find(cmd) for cmd, _ in OPS_004_COMMANDS]
    assert all(p >= 0 for p in positions), positions
    assert positions == sorted(positions), (
        "OPS-004 commands appear out of order in validation-commands.md "
        f"(positions={positions}). §3 mandates pytest → verify-sync → "
        "eval doctor → eval run."
    )


@pytest.mark.parametrize("_command, evidence", OPS_004_COMMANDS, ids=[
    "01-targeted-pytest",
    "02-make-verify-sync",
    "03-eval-doctor",
    "04-eval-run-E1",
])
def test_doc_links_evidence_log(
    doc_text: str, _command: str, evidence: str
) -> None:
    """Each command links its evidence log under the canonical root."""

    assert evidence in doc_text, (
        f"Evidence filename {evidence!r} not referenced in "
        f"{DOC_PATH.relative_to(REPO_ROOT)}."
    )


@pytest.mark.parametrize("section", REQUIRED_SECTIONS)
def test_doc_carries_required_section(doc_text: str, section: str) -> None:
    """Each AC-mandated section heading is present."""

    assert section in doc_text, (
        f"Required section heading not found in "
        f"{DOC_PATH.relative_to(REPO_ROOT)}: {section!r}"
    )


def test_evidence_root_directory_exists() -> None:
    """The OPS-004 evidence root directory has been provisioned."""

    assert EVIDENCE_ROOT.is_dir(), (
        f"OPS-004 evidence root missing: {EVIDENCE_ROOT.relative_to(REPO_ROOT)}. "
        "Re-run the §6 reproduction recipe to populate it."
    )


@pytest.mark.parametrize("_command, evidence", OPS_004_COMMANDS, ids=[
    "01-targeted-pytest",
    "02-make-verify-sync",
    "03-eval-doctor",
    "04-eval-run-E1",
])
def test_evidence_log_present_with_exit_code(
    _command: str, evidence: str
) -> None:
    """Each evidence log exists and carries a trailing ``EXIT_CODE=<n>`` marker."""

    log = EVIDENCE_ROOT / evidence
    assert log.is_file(), f"Evidence log missing: {log.relative_to(REPO_ROOT)}"

    body = log.read_text(encoding="utf-8", errors="replace")
    assert "EXIT_CODE=" in body, (
        f"Evidence log {log.relative_to(REPO_ROOT)} does not carry a "
        "trailing 'EXIT_CODE=<n>' line. Re-run the §6 reproduction recipe."
    )


def test_doc_records_known_blockers_section(doc_text: str) -> None:
    """B1 (_new_run_id) and B2 (ptytest) are explicitly recorded."""

    assert "### B1" in doc_text, "Known blocker B1 must be enumerated in §5."
    assert "### B2" in doc_text, "Known blocker B2 must be enumerated in §5."
    assert "_new_run_id" in doc_text, (
        "B1 must name the missing helper (_new_run_id) so the follow-up "
        "task scope is unambiguous."
    )
    assert "ptytest" in doc_text.lower(), (
        "B2 must reference ptytest vendoring as the second blocker."
    )
