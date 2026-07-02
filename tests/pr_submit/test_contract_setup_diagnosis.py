"""Diagnosis-helper tests for detection-contract readiness (contract_setup.diagnose).

Covers the ``ContractState`` outcomes produced by the read-only
``diagnose(...)`` probe: ``missing``, ``unlocked``, ``unparseable``,
``evidence_missing``, ``validation_missing``, ``validation_failed``, ``ready``,
and the ``declined_by_user`` cancellation state. Also pins that:

- ``checked_paths`` are recorded (local override + shipped ref),
- ``next_command`` values are current and actionable (missing → the
  ``superclaude reflect contract-status`` setup command; validation-family →
  the ``--validate`` variant; ready → ``/sc:pr-submit --monitor 1``),
- shipped-only fail-closed behavior: with no local override, ``diagnose`` never
  reports the shipped ``locked:false`` source as ``ready`` — it reports
  ``missing``,
- ``Diagnosis.summary()`` never leaks raw payload bodies.

Every ``diagnose(...)`` call passes an explicit ``cwd=tmp_path`` so the local
override is resolved under the temp tree and the real
``.dev/pr-monitor/`` tree is never touched. These tests do NOT duplicate or
weaken ``test_detection_contract.py::test_t210_locked_false_halts`` — that
loader arm-gate regression is intentionally left to that module.
"""

from __future__ import annotations

import json
from pathlib import Path

import yaml

from superclaude.pr_submit.contract_setup import (
    ContractState,
    Diagnosis,
    declined_by_user,
    diagnose,
)

RAW_BODY_SENTINEL = "RAW_BODY_SENTINEL_DO_NOT_PRINT"

# The gitignored operator-local locked-contract path, relative to the repo root
# (mirrors detection._LOCAL_OVERRIDE_REL). diagnose(cwd=...) resolves it here.
OVERRIDE_REL = Path(".dev/pr-monitor/detection-contract.locked.md")


def _write_override(tmp_path: Path, yaml_body: str) -> Path:
    """Write a local locked-override contract markdown file under tmp_path.

    Matches the shape the existing detection tests build: a heading, then a
    fenced ```yaml block whose body is ``yaml_body``.
    """
    override = tmp_path / OVERRIDE_REL
    override.parent.mkdir(parents=True, exist_ok=True)
    override.write_text(
        f"# local locked contract\n\n```yaml\n{yaml_body}\n```\n",
        encoding="utf-8",
    )
    return override


def _write_evidence(probe_dir: Path, *, repo: str, pr_number: int) -> Path:
    """Write a minimal probe evidence dir with a combined-payload.json.

    Returns the evidence FILE path (combined-payload.json). The payload carries a
    raw-body sentinel so summary-redaction can be asserted. ``load_evidence``
    (called by diagnose to hash the evidence) reads this dir.
    """
    probe_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "metadata": {"repo": repo, "pr_number": pr_number},
        "reviews": [
            {"author": {"login": "augmentcode[bot]"}, "body": RAW_BODY_SENTINEL}
        ],
        "comments": [],
        "check_runs": [],
    }
    combined = probe_dir / "combined-payload.json"
    combined.write_text(json.dumps(payload), encoding="utf-8")
    return combined


def _ready_evidence_sha(probe_dir: Path) -> str:
    """Compute the same canonical evidence sha256 diagnose() will derive."""
    from superclaude.pr_submit.contract_setup.evidence import load_evidence

    return load_evidence(probe_dir).sha256


# --------------------------------------------------------------------------- #
# missing (fail-closed: shipped-only, no local override)                       #
# --------------------------------------------------------------------------- #


def test_missing_when_no_local_override(tmp_path):
    """No local override → state MISSING, both paths checked, actionable command."""
    d = diagnose(repo="IronbellyOrg/IronClaude", pr_number=42, cwd=tmp_path)

    assert isinstance(d, Diagnosis)
    assert d.state is ContractState.MISSING
    assert d.override_present is False
    # checked_paths records the local override AND the shipped ref.
    assert len(d.checked_paths) == 2
    override_path = tmp_path / OVERRIDE_REL
    assert override_path in d.checked_paths
    # The shipped ref is the OTHER checked path (not under tmp_path).
    assert any(p != override_path for p in d.checked_paths)
    assert d.blockers  # a non-empty reason is recorded
    assert (
        d.next_command
        == "superclaude reflect contract-status --repo IronbellyOrg/IronClaude --pr 42"
    )


def test_missing_never_reports_shipped_locked_false_as_ready(tmp_path):
    """Fail-closed: the shipped source ships locked:false; with no local override
    diagnose must NOT classify it as ready — it is MISSING. This is the diagnosis
    sibling of the T-210 loader arm-gate (which we leave to test_detection_contract)."""
    d = diagnose(cwd=tmp_path)
    assert d.state is ContractState.MISSING
    assert d.state is not ContractState.READY
    # The shipped contract's locked flag is surfaced but never armable via diagnose.
    assert d.shipped_locked is False
    # Placeholder next command (no repo/pr supplied).
    assert (
        d.next_command
        == "superclaude reflect contract-status --repo <owner/repo> --pr <number>"
    )


# --------------------------------------------------------------------------- #
# unparseable / unlocked                                                       #
# --------------------------------------------------------------------------- #


def test_unparseable_when_override_has_no_yaml_block(tmp_path):
    """Local override present but with no parseable YAML → state UNPARSEABLE."""
    override = tmp_path / OVERRIDE_REL
    override.parent.mkdir(parents=True, exist_ok=True)
    override.write_text("# broken\n\nno fenced yaml here at all\n", encoding="utf-8")

    d = diagnose(cwd=tmp_path)
    assert d.state is ContractState.UNPARSEABLE
    assert d.override_present is True
    assert d.blockers
    # Unparseable is a validation-family (non-ready) state → validate variant.
    assert d.next_command.startswith("superclaude reflect contract-status")


def test_unlocked_when_override_locked_false(tmp_path):
    """Local override with locked:false → state UNLOCKED, validate next command."""
    _write_override(
        tmp_path,
        'augment_bot_login: "augmentcode[bot]"\nlocked: false',
    )
    d = diagnose(repo="IronbellyOrg/IronClaude", pr_number=7, cwd=tmp_path)

    assert d.state is ContractState.UNLOCKED
    assert d.override_present is True
    assert d.override_locked is False
    assert (
        d.next_command == "superclaude reflect contract-status --validate "
        "--repo IronbellyOrg/IronClaude --pr 7"
    )


# --------------------------------------------------------------------------- #
# evidence_missing                                                             #
# --------------------------------------------------------------------------- #


def test_evidence_missing_when_locked_but_no_probe_evidence_file(tmp_path):
    """Locked override naming a nonexistent probe_evidence → state EVIDENCE_MISSING."""
    _write_override(
        tmp_path,
        'augment_bot_login: "augmentcode[bot]"\n'
        "locked: true\n"
        "probe_evidence: .dev/pr-monitor/probes/nope/combined-payload.json",
    )
    d = diagnose(repo="IronbellyOrg/IronClaude", pr_number=7, cwd=tmp_path)

    assert d.state is ContractState.EVIDENCE_MISSING
    assert d.override_present is True
    assert d.override_locked is True
    assert d.blockers
    # Validation-family → the --validate next command.
    assert "--validate" in d.next_command


def test_evidence_missing_when_probe_evidence_absent_field(tmp_path):
    """Locked override with NO probe_evidence field at all → EVIDENCE_MISSING."""
    _write_override(
        tmp_path,
        'augment_bot_login: "augmentcode[bot]"\nlocked: true',
    )
    d = diagnose(cwd=tmp_path)
    assert d.state is ContractState.EVIDENCE_MISSING


# --------------------------------------------------------------------------- #
# validation_missing                                                           #
# --------------------------------------------------------------------------- #


def test_validation_missing_when_evidence_present_but_no_report(tmp_path):
    """Locked + real evidence file but no validation-report.yaml → VALIDATION_MISSING."""
    probe_dir = tmp_path / ".dev" / "pr-monitor" / "probes" / "p1"
    _write_evidence(probe_dir, repo="IronbellyOrg/IronClaude", pr_number=42)
    _write_override(
        tmp_path,
        'augment_bot_login: "augmentcode[bot]"\n'
        "locked: true\n"
        "probe_evidence: .dev/pr-monitor/probes/p1/combined-payload.json",
    )

    d = diagnose(repo="IronbellyOrg/IronClaude", pr_number=42, cwd=tmp_path)
    assert d.state is ContractState.VALIDATION_MISSING
    assert d.evidence_path is not None
    assert d.evidence_sha256 is not None
    assert d.validation_report_path is not None
    assert "--validate" in d.next_command


# --------------------------------------------------------------------------- #
# validation_failed                                                            #
# --------------------------------------------------------------------------- #


def test_validation_failed_when_report_result_not_passed(tmp_path):
    """Report exists with a failing result → state VALIDATION_FAILED, no raw body."""
    probe_dir = tmp_path / ".dev" / "pr-monitor" / "probes" / "p2"
    evidence = _write_evidence(probe_dir, repo="IronbellyOrg/IronClaude", pr_number=42)
    sha = _ready_evidence_sha(probe_dir)
    (probe_dir / "validation-report.yaml").write_text(
        yaml.safe_dump(
            {
                "result": "failed",
                "repo": "IronbellyOrg/IronClaude",
                "pr_number": 42,
                "evidence_sha256": sha,
            }
        ),
        encoding="utf-8",
    )
    _write_override(
        tmp_path,
        'augment_bot_login: "augmentcode[bot]"\n'
        "locked: true\n"
        f"probe_evidence: {evidence.relative_to(tmp_path)}",
    )

    d = diagnose(repo="IronbellyOrg/IronClaude", pr_number=42, cwd=tmp_path)
    assert d.state is ContractState.VALIDATION_FAILED
    assert d.validation_result == "failed"
    assert d.blockers
    assert "--validate" in d.next_command


# --------------------------------------------------------------------------- #
# ready                                                                        #
# --------------------------------------------------------------------------- #


def test_ready_when_locked_evidence_and_passed_report(tmp_path):
    """Locked override + evidence + a passing, matching report → state READY."""
    probe_dir = tmp_path / ".dev" / "pr-monitor" / "probes" / "p3"
    evidence = _write_evidence(probe_dir, repo="IronbellyOrg/IronClaude", pr_number=42)
    sha = _ready_evidence_sha(probe_dir)
    (probe_dir / "validation-report.yaml").write_text(
        yaml.safe_dump(
            {
                "result": "passed",
                "repo": "IronbellyOrg/IronClaude",
                "pr_number": 42,
                "evidence_sha256": sha,
            }
        ),
        encoding="utf-8",
    )
    _write_override(
        tmp_path,
        'augment_bot_login: "augmentcode[bot]"\n'
        "locked: true\n"
        f"probe_evidence: {evidence.relative_to(tmp_path)}",
    )

    d = diagnose(repo="IronbellyOrg/IronClaude", pr_number=42, cwd=tmp_path)
    assert d.state is ContractState.READY
    assert d.validation_result == "passed"
    assert d.blockers == []
    # Ready → the arm command, not a further contract-status command.
    assert d.next_command == "/sc:pr-submit --monitor 1 --pr 42"


def test_ready_next_command_uses_placeholder_pr_when_absent(tmp_path):
    """Ready with no PR context → the arm command keeps a <number> placeholder."""
    probe_dir = tmp_path / ".dev" / "pr-monitor" / "probes" / "p4"
    evidence = _write_evidence(probe_dir, repo="IronbellyOrg/IronClaude", pr_number=99)
    sha = _ready_evidence_sha(probe_dir)
    (probe_dir / "validation-report.yaml").write_text(
        yaml.safe_dump({"result": "passed", "evidence_sha256": sha}),
        encoding="utf-8",
    )
    _write_override(
        tmp_path,
        'augment_bot_login: "augmentcode[bot]"\n'
        "locked: true\n"
        f"probe_evidence: {evidence.relative_to(tmp_path)}",
    )

    d = diagnose(cwd=tmp_path)
    assert d.state is ContractState.READY
    assert d.next_command == "/sc:pr-submit --monitor 1 --pr <number>"


def test_ready_when_probe_evidence_is_a_directory(tmp_path):
    """probe_evidence pointing at the probe DIRECTORY (not the payload file) still
    resolves to READY.

    Regression (PR #209 Augment finding F1): diagnose() previously forced
    EVIDENCE_MISSING unless probe_evidence resolved to a *file*, even though
    load_evidence()/_evidence_sha256() accept a probe directory. A locked
    contract whose probe_evidence is the dir must diagnose the same as one whose
    probe_evidence is the combined-payload.json inside it.
    """
    probe_dir = tmp_path / ".dev" / "pr-monitor" / "probes" / "pdir"
    _write_evidence(probe_dir, repo="IronbellyOrg/IronClaude", pr_number=42)
    sha = _ready_evidence_sha(probe_dir)
    (probe_dir / "validation-report.yaml").write_text(
        yaml.safe_dump(
            {
                "result": "passed",
                "repo": "IronbellyOrg/IronClaude",
                "pr_number": 42,
                "evidence_sha256": sha,
            }
        ),
        encoding="utf-8",
    )
    _write_override(
        tmp_path,
        'augment_bot_login: "augmentcode[bot]"\n'
        "locked: true\n"
        # probe_evidence is the DIRECTORY, not the payload file.
        f"probe_evidence: {probe_dir.relative_to(tmp_path)}",
    )

    d = diagnose(repo="IronbellyOrg/IronClaude", pr_number=42, cwd=tmp_path)
    assert d.state is not ContractState.EVIDENCE_MISSING
    assert d.state is ContractState.READY
    assert d.validation_result == "passed"
    assert d.evidence_sha256 == sha
    assert d.validation_report_path == probe_dir / "validation-report.yaml"


# --------------------------------------------------------------------------- #
# declined_by_user                                                             #
# --------------------------------------------------------------------------- #


def test_declined_by_user_leaves_files_untouched(tmp_path):
    """declined_by_user() → cancellation state; records paths; touches no files."""
    d = declined_by_user(repo="IronbellyOrg/IronClaude", pr_number=42, cwd=tmp_path)

    assert d.state is ContractState.DECLINED_BY_USER
    assert len(d.checked_paths) == 2
    assert (tmp_path / OVERRIDE_REL) in d.checked_paths
    assert d.blockers
    assert "cancelled" in d.next_command.lower()
    # No override was created by the declined path.
    assert not (tmp_path / OVERRIDE_REL).exists()


# --------------------------------------------------------------------------- #
# summary() redaction — no raw payload bodies                                  #
# --------------------------------------------------------------------------- #


def test_summary_omits_raw_payload_bodies(tmp_path):
    """Diagnosis.summary() renders status/paths/hashes/counts/blockers, never a
    serialized review/comment body. The evidence payload carries a sentinel body;
    the summary must not leak it."""
    probe_dir = tmp_path / ".dev" / "pr-monitor" / "probes" / "p5"
    evidence = _write_evidence(probe_dir, repo="IronbellyOrg/IronClaude", pr_number=42)
    _write_override(
        tmp_path,
        'augment_bot_login: "augmentcode[bot]"\n'
        "locked: true\n"
        f"probe_evidence: {evidence.relative_to(tmp_path)}",
    )

    d = diagnose(repo="IronbellyOrg/IronClaude", pr_number=42, cwd=tmp_path)
    summary = d.summary()

    # The raw evidence JSON on disk still contains the sentinel...
    assert RAW_BODY_SENTINEL in evidence.read_text(encoding="utf-8")
    # ...but the human-facing summary must NOT.
    assert RAW_BODY_SENTINEL not in summary
    # Sanity: the summary still surfaces useful safe metadata.
    assert "state=" in summary
    assert "checked_paths=" in summary
    assert "next_command=" in summary


def test_summary_omits_raw_bodies_across_all_states(tmp_path):
    """Redaction holds for the MISSING state summary too (no payload involved,
    but the summary shape must stay body-free)."""
    d = diagnose(cwd=tmp_path)
    summary = d.summary()
    assert RAW_BODY_SENTINEL not in summary
    assert summary.startswith("state=missing")
