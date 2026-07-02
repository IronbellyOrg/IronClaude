"""Safe-writer tests for detection-contract setup (research doc §5).

These tests exercise the REAL public writer surface in
``superclaude.pr_submit.contract_setup.writer``:

- ``write_lock(candidate, evidence, report, *, confirmed, dest=...)`` refuses to
  write unless ``confirmed=True`` AND every ``LockGate`` predicate passes, and it
  resolves its destination to *exactly*
  ``<cwd>/.dev/pr-monitor/detection-contract.locked.md`` (rejecting shipped-ref /
  ``.claude`` mirror targets). The refusal is a ``ContractSetupRefused``.
- ``write_report(report, evidence, dest_dir)`` writes report artifacts under a
  ``.dev/pr-monitor/probes/...`` directory only.

Destination parameterization: the writer resolves the lock path relative to
``Path.cwd()`` (via ``_active_root_lock_path`` / ``detection._LOCAL_OVERRIDE_REL``).
Rather than patch module internals, these tests ``monkeypatch.chdir(tmp_path)`` so
the *active repository root* is a throwaway tmp tree — the real repo is never
touched. The probe/evidence tree is likewise built under ``tmp_path``.

No monitor/PR side effects: the writer package must never import or invoke the FSM
seams (arm/push/reply/resolve/retrigger/retry/resume). ``test_writer_package_imports_no_fsm_seams``
asserts that statically.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from superclaude.pr_submit.contract_setup.candidate import derive_candidate
from superclaude.pr_submit.contract_setup.evidence import load_evidence
from superclaude.pr_submit.contract_setup.validation import validate_candidate
from superclaude.pr_submit.contract_setup.writer import (
    ContractSetupRefused,
    write_lock,
    write_report,
)
from superclaude.pr_submit.detection import _LOCAL_OVERRIDE_REL

# ---------------------------------------------------------------------------
# Fixtures / builders
# ---------------------------------------------------------------------------

_REPO = "IronbellyOrg/IronClaude"
_PR = 4242


def _clean_augment_payload() -> dict:
    """A payload that classifies as ``clean``: one Augment review, no findings."""
    return {
        "metadata": {
            "repo": _REPO,
            "pr_number": _PR,
            "captured_at": "2026-07-01T00:00:00Z",
        },
        "reviews": [
            {
                "user": {"login": "augmentcode[bot]"},
                "app": {"slug": "augmentcode"},
                "author_association": "NONE",
                "state": "COMMENTED",
                "submitted_at": "2026-07-01T00:00:00Z",
                "body": "Review completed. No issues found.",
            }
        ],
        "comments": [],
        "check_runs": [],
    }


def _write_probe_dir(base: Path, payload: dict | None = None) -> Path:
    """Create a valid probe evidence dir under ``<base>/.dev/pr-monitor/probes``.

    Returns the probe directory. ``load_evidence`` reads ``combined-payload.json``
    plus a ``manifest.json`` (for repo/pr metadata).
    """
    payload = payload if payload is not None else _clean_augment_payload()
    probe_dir = base / ".dev" / "pr-monitor" / "probes" / "pr-4242"
    probe_dir.mkdir(parents=True, exist_ok=True)
    (probe_dir / "combined-payload.json").write_text(
        json.dumps(payload), encoding="utf-8"
    )
    (probe_dir / "gh-reviews.json").write_text(
        json.dumps(payload.get("reviews", [])), encoding="utf-8"
    )
    (probe_dir / "manifest.json").write_text(
        json.dumps(
            {"repo": _REPO, "pr_number": _PR, "captured_at": "2026-07-01T00:00:00Z"}
        ),
        encoding="utf-8",
    )
    return probe_dir


def _passing_bundle(base: Path, payload: dict | None = None):
    """Build ``(candidate, evidence, report)`` that PASS the full LockGate.

    Also writes the validation report under the probe dir so the gate's
    ``report_written`` predicate (which reads ``<probe_dir>/validation-report.yaml``
    and checks the evidence hash is present) is satisfied.
    """
    probe_dir = _write_probe_dir(base, payload)
    evidence = load_evidence(probe_dir)
    candidate = derive_candidate(evidence)
    report = validate_candidate(candidate, evidence, expected_result="clean")
    # The gate's report_written predicate reads probe_dir/validation-report.yaml.
    write_report(report, evidence, probe_dir)
    return candidate, evidence, report


@pytest.fixture
def repo_root(tmp_path, monkeypatch):
    """Make ``tmp_path`` the active repository root for cwd-relative resolution."""
    monkeypatch.chdir(tmp_path)
    return tmp_path


# ---------------------------------------------------------------------------
# 1. Explicit confirmation is required
# ---------------------------------------------------------------------------


def test_write_lock_requires_explicit_confirmation(repo_root):
    """Without ``confirmed=True`` the write is refused and NOTHING is written."""
    candidate, evidence, report = _passing_bundle(repo_root)
    lock_path = (repo_root / _LOCAL_OVERRIDE_REL).resolve()
    assert not lock_path.exists()

    with pytest.raises(ContractSetupRefused) as excinfo:
        write_lock(candidate, evidence, report, confirmed=False)

    # The refusal names the failed user_confirmed predicate; nothing was written.
    assert "user_confirmed" in str(excinfo.value)
    assert not lock_path.exists()


def test_write_lock_writes_when_confirmed_and_gate_passes(repo_root):
    """With ``confirmed=True`` and a passing gate the lock file is written."""
    candidate, evidence, report = _passing_bundle(repo_root)
    result = write_lock(candidate, evidence, report, confirmed=True)
    assert result.exists()
    assert result.is_file()


# ---------------------------------------------------------------------------
# 2. The ONLY lock destination is <base>/.dev/pr-monitor/detection-contract.locked.md
# ---------------------------------------------------------------------------


def test_lock_destination_is_exactly_dev_pr_monitor_under_cwd(repo_root):
    """The resolved lock path is exactly ``<cwd>/.dev/pr-monitor/detection-contract.locked.md``."""
    candidate, evidence, report = _passing_bundle(repo_root)
    result = write_lock(candidate, evidence, report, confirmed=True)

    expected = (repo_root / _LOCAL_OVERRIDE_REL).resolve()
    assert result.resolve() == expected
    # Confirm the exact relative shape under the active root.
    assert result.resolve().relative_to(repo_root.resolve()) == _LOCAL_OVERRIDE_REL
    # And it lives under a real tmp tree, never the actual repo checkout.
    assert str(result).startswith(str(repo_root))


def test_lock_destination_off_target_is_refused(repo_root):
    """A ``dest`` that is not the canonical local override path is refused."""
    candidate, evidence, report = _passing_bundle(repo_root)
    off_target = repo_root / ".dev" / "pr-monitor" / "somewhere-else.md"

    with pytest.raises(ContractSetupRefused) as excinfo:
        write_lock(candidate, evidence, report, confirmed=True, dest=off_target)

    assert "lock destination" in str(excinfo.value).lower()
    assert not off_target.exists()


# ---------------------------------------------------------------------------
# 3. No shipped-ref mutation and NO writes under any .claude mirror
# ---------------------------------------------------------------------------


def test_no_write_under_claude_mirror(repo_root):
    """A ``.claude/`` mirror destination is refused and nothing is written there."""
    candidate, evidence, report = _passing_bundle(repo_root)
    claude_dest = repo_root / ".claude" / "pr-monitor" / "detection-contract.locked.md"

    with pytest.raises(ContractSetupRefused):
        write_lock(candidate, evidence, report, confirmed=True, dest=claude_dest)

    assert not claude_dest.exists()
    assert not (repo_root / ".claude").exists()


def test_no_write_under_src_shipped_ref(repo_root):
    """A shipped-ref (``src/``) destination is refused; the shipped tree is untouched."""
    candidate, evidence, report = _passing_bundle(repo_root)
    src_dest = repo_root / "src" / "superclaude" / "detection-contract.locked.md"

    with pytest.raises(ContractSetupRefused):
        write_lock(candidate, evidence, report, confirmed=True, dest=src_dest)

    assert not src_dest.exists()
    assert not (repo_root / "src").exists()


def test_confirmed_write_creates_no_claude_or_src_trees(repo_root):
    """A successful confirmed write must NOT create any ``.claude`` or ``src`` tree."""
    candidate, evidence, report = _passing_bundle(repo_root)
    write_lock(candidate, evidence, report, confirmed=True)

    assert not (repo_root / ".claude").exists()
    assert not (repo_root / "src").exists()


# ---------------------------------------------------------------------------
# 4. write_report writes artifacts under .dev/pr-monitor/probes/...
# ---------------------------------------------------------------------------


def test_write_report_writes_under_probes(repo_root):
    """``write_report`` writes report + summary under ``.dev/pr-monitor/probes/...``."""
    probe_dir = _write_probe_dir(repo_root)
    evidence = load_evidence(probe_dir)
    candidate = derive_candidate(evidence)
    report = validate_candidate(candidate, evidence, expected_result="clean")

    report_path = write_report(report, evidence, probe_dir)

    assert report_path.exists()
    assert report_path.name == "validation-report.yaml"
    assert (probe_dir / "validation-summary.md").exists()
    # Destination is under .dev/pr-monitor/probes.
    parts = report_path.resolve().parts
    assert ".dev" in parts and "pr-monitor" in parts and "probes" in parts


def test_write_report_refuses_non_probes_destination(repo_root):
    """``write_report`` refuses a destination not under ``.dev/pr-monitor/probes``."""
    probe_dir = _write_probe_dir(repo_root)
    evidence = load_evidence(probe_dir)
    candidate = derive_candidate(evidence)
    report = validate_candidate(candidate, evidence, expected_result="clean")

    bad_dir = repo_root / ".dev" / "pr-monitor" / "not-probes"
    with pytest.raises(ContractSetupRefused):
        write_report(report, evidence, bad_dir)


def test_write_report_refuses_claude_destination(repo_root):
    """``write_report`` refuses a ``.claude/`` destination outright."""
    probe_dir = _write_probe_dir(repo_root)
    evidence = load_evidence(probe_dir)
    candidate = derive_candidate(evidence)
    report = validate_candidate(candidate, evidence, expected_result="clean")

    claude_dir = repo_root / ".claude" / "pr-monitor" / "probes"
    with pytest.raises(ContractSetupRefused):
        write_report(report, evidence, claude_dir)
    assert not (repo_root / ".claude").exists()


# ---------------------------------------------------------------------------
# 5. Lock metadata includes evidence hash + validation-report reference
# ---------------------------------------------------------------------------


def test_lock_metadata_includes_evidence_hash_and_validation_report(repo_root):
    """The written lock file embeds the evidence sha256 and a validation-report ref."""
    candidate, evidence, report = _passing_bundle(repo_root)
    result = write_lock(candidate, evidence, report, confirmed=True)

    text = result.read_text(encoding="utf-8")
    # Evidence hash present and matches the real bundle hash.
    assert evidence.sha256 in text
    # Validation-report reference (the probe validation-report.yaml path).
    assert "validation_report" in text
    assert "validation-report.yaml" in text
    # Validation result + classifier result surfaced in metadata.
    assert "validation_result" in text
    assert report.result in text  # "passed"
    assert "locked: true" in text or "locked: True" in text


# ---------------------------------------------------------------------------
# 6. Writers refuse when a LockGate predicate fails (GateResult fail => refused)
# ---------------------------------------------------------------------------


def test_write_lock_refused_when_gate_predicate_fails_cross_pr_shape_only(repo_root):
    """A cross-PR (shape-only) evidence bundle fails the pr_identity_recorded predicate.

    Even with ``confirmed=True`` the write is refused because the gate does not pass.
    """
    payload = _clean_augment_payload()
    payload["metadata"]["cross_pr_shape_only"] = True
    payload["cross_pr_shape_only"] = True
    candidate, evidence, report = _passing_bundle(repo_root, payload=payload)
    assert evidence.cross_pr_shape_only is True

    lock_path = (repo_root / _LOCAL_OVERRIDE_REL).resolve()
    with pytest.raises(ContractSetupRefused) as excinfo:
        write_lock(candidate, evidence, report, confirmed=True)

    assert "safe lock gate failed" in str(excinfo.value)
    assert not lock_path.exists()


def test_write_lock_refused_when_expected_result_polling(repo_root):
    """A payload with no Augment review classifies as ``polling`` => gate fails.

    ``expected_not_polling`` / ``classifier_matches`` predicates fail, so the write is
    refused despite explicit confirmation.
    """
    payload = {
        "metadata": {
            "repo": _REPO,
            "pr_number": _PR,
            "captured_at": "2026-07-01T00:00:00Z",
        },
        "reviews": [{"user": {"login": "human-reviewer"}, "body": "lgtm"}],
        "comments": [],
        "check_runs": [],
    }
    probe_dir = _write_probe_dir(repo_root, payload)
    evidence = load_evidence(probe_dir)
    candidate = derive_candidate(evidence)
    report = validate_candidate(candidate, evidence, expected_result="clean")
    write_report(report, evidence, probe_dir)

    lock_path = (repo_root / _LOCAL_OVERRIDE_REL).resolve()
    with pytest.raises(ContractSetupRefused) as excinfo:
        write_lock(candidate, evidence, report, confirmed=True)

    assert "safe lock gate failed" in str(excinfo.value)
    assert not lock_path.exists()


def test_write_lock_refused_when_report_not_written(repo_root):
    """If the validation report was never written, the ``report_written`` predicate fails.

    Same passing evidence, but we DO NOT call ``write_report`` first, so the gate's
    ``report_written`` check (which reads ``<probe_dir>/validation-report.yaml``) fails.
    """
    probe_dir = _write_probe_dir(repo_root)
    evidence = load_evidence(probe_dir)
    candidate = derive_candidate(evidence)
    report = validate_candidate(candidate, evidence, expected_result="clean")
    # Intentionally NOT calling write_report here.

    lock_path = (repo_root / _LOCAL_OVERRIDE_REL).resolve()
    with pytest.raises(ContractSetupRefused) as excinfo:
        write_lock(candidate, evidence, report, confirmed=True)

    assert "safe lock gate failed" in str(excinfo.value)
    assert not lock_path.exists()


# ---------------------------------------------------------------------------
# 7. No monitor/PR side effects: the writer package touches no FSM seam
# ---------------------------------------------------------------------------


def test_writer_package_imports_no_fsm_seams():
    """The contract_setup writer package must not import the FSM / monitor seams.

    The safe writers arm/push/reply/resolve/retrigger/retry/resume NOTHING. We assert
    the whole contract_setup package graph never imports ``fsm`` or ``monitor`` modules,
    so a write path structurally cannot invoke a monitor/PR side-effect seam.
    """
    import superclaude.pr_submit.contract_setup as pkg
    import superclaude.pr_submit.contract_setup.candidate  # noqa: F401
    import superclaude.pr_submit.contract_setup.evidence  # noqa: F401
    import superclaude.pr_submit.contract_setup.lockgate  # noqa: F401
    import superclaude.pr_submit.contract_setup.validation  # noqa: F401
    import superclaude.pr_submit.contract_setup.writer  # noqa: F401

    forbidden = ("fsm", "monitor", "reply_resolve", "review_retrigger")
    contract_setup_modules = [
        name
        for name in sys.modules
        if name.startswith("superclaude.pr_submit.contract_setup")
    ]
    assert contract_setup_modules  # sanity: the package graph is loaded

    for mod_name in contract_setup_modules:
        module = sys.modules[mod_name]
        source_file = getattr(module, "__file__", None)
        if not source_file:
            continue
        text = Path(source_file).read_text(encoding="utf-8")
        for seam in forbidden:
            assert f"pr_submit.{seam}" not in text and f"import {seam}" not in text, (
                f"{mod_name} references forbidden FSM seam '{seam}'"
            )

    # And the package itself exposes only setup helpers, no arming entrypoint.
    assert not hasattr(pkg, "arm_monitor")


def test_confirmed_write_performs_no_pr_side_effects(repo_root, monkeypatch):
    """A full confirmed write must not invoke any FSM seam.

    We install tripwires on the monitor/FSM seam functions; a genuine write path must
    never call them. (If the writer imported and drove a seam, these would fire.)
    """
    tripped: list[str] = []

    import superclaude.pr_submit.fsm as fsm_mod

    for seam_name in ("run_skill", "run_monitor", "arm_monitor"):
        if hasattr(fsm_mod, seam_name):
            monkeypatch.setattr(
                fsm_mod,
                seam_name,
                lambda *a, _n=seam_name, **k: tripped.append(_n),
                raising=False,
            )

    candidate, evidence, report = _passing_bundle(repo_root)
    result = write_lock(candidate, evidence, report, confirmed=True)

    assert result.exists()
    assert tripped == []
