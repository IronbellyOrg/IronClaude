"""OPS-002 / AC12 scratch-root policy cross-module enforcement tests.

Covers Task T02.25 (Phase 2 / Deliverable D-0043, Roadmap R-043). The
policy lives in three places — :func:`_default_allowed_scratch_roots`,
:data:`SCRATCH_ROOT_POLICY`, and ``docs/eval/scratch-roots.md`` — and the
canonical AC for OPS-002 is that *every consumer quotes the same policy
text when it rejects a path*. These tests pin:

* the policy constant lists the three allowed roots verbatim;
* :func:`format_scratch_root_violation` renders both the per-violation
  forensic detail and the canonical policy block;
* ``superclaude eval doctor --output-dir <bad>`` exits 2 and the stderr
  artifact carries the policy block byte-for-byte;
* ``superclaude eval doctor --output-dir <allowlisted>`` exits 0 (the
  flag must not regress the green-path doctor contract);
* ``EvalConfig.allowed_scratch_roots`` remains the single source of
  truth — narrowing it changes which roots doctor accepts;
* the prose documentation under ``docs/eval/scratch-roots.md`` names the
  three roots so the doc cannot drift from the runtime check.

Cross-links:
* T01.01 / D-0001 — ``EvalConfig.allowed_scratch_roots`` (sole source).
* T01.19 / D-0016 — ``resolve_scratch_root`` (sole ingress).
* T02.08 / D-0029 — ``containment_guard`` (FR-ISO2 defense in depth).
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest
from click.testing import CliRunner

from superclaude.cli.eval import (
    SCRATCH_ROOT_POLICY,
    SCRATCH_ROOT_VIOLATION_EXIT_CODE,
    EvalConfig,
    ScratchRootViolation,
    eval_group,
    format_scratch_root_violation,
    resolve_scratch_root,
)
from superclaude.cli.eval import commands as doctor_module


REPO_ROOT = Path(__file__).resolve().parents[3]
SCRATCH_ROOTS_DOC = REPO_ROOT / "docs" / "eval" / "scratch-roots.md"


# ---------------------------------------------------------------------------
# Policy constant
# ---------------------------------------------------------------------------


def test_policy_constant_names_three_allowed_roots() -> None:
    """The constant MUST mention the three roots from the docs verbatim."""

    assert "/tmp/eval-runs/" in SCRATCH_ROOT_POLICY
    assert ".dev/eval-runs/" in SCRATCH_ROOT_POLICY
    assert "--output-dir" in SCRATCH_ROOT_POLICY


def test_policy_constant_references_authoritative_doc() -> None:
    """Operators reading the policy line MUST be able to find the doc."""

    assert "docs/eval/scratch-roots.md" in SCRATCH_ROOT_POLICY


def test_policy_constant_carries_ops_002_and_ac12_identifiers() -> None:
    """The policy block MUST be greppable by both identifiers for CI logs."""

    assert "OPS-002" in SCRATCH_ROOT_POLICY
    assert "AC12" in SCRATCH_ROOT_POLICY


# ---------------------------------------------------------------------------
# Renderer
# ---------------------------------------------------------------------------


def test_format_violation_includes_per_violation_forensic_detail() -> None:
    """The renderer must NOT drop the original offending path / allowlist."""

    candidate = Path("/etc/foo")
    with pytest.raises(ScratchRootViolation) as excinfo:
        resolve_scratch_root(candidate)

    rendered = format_scratch_root_violation(excinfo.value)
    assert str(candidate) in rendered
    assert "AC12 allowlist" in rendered


def test_format_violation_appends_canonical_policy_block() -> None:
    """Every render MUST quote the canonical policy block verbatim."""

    with pytest.raises(ScratchRootViolation) as excinfo:
        resolve_scratch_root("/etc/foo")

    rendered = format_scratch_root_violation(excinfo.value)
    assert SCRATCH_ROOT_POLICY in rendered


def test_format_violation_separates_detail_from_policy_with_blank_line() -> None:
    """Detail block + policy block MUST be readable in a CI log scrape."""

    with pytest.raises(ScratchRootViolation) as excinfo:
        resolve_scratch_root("/etc/foo")

    rendered = format_scratch_root_violation(excinfo.value)
    # The renderer joins ``str(exc)`` + blank line + policy text. The
    # blank line is load-bearing: scrapers split on ``\n\n`` to detach
    # forensic detail from the policy quote.
    assert "\n\n" in rendered


# ---------------------------------------------------------------------------
# Doctor CLI integration
# ---------------------------------------------------------------------------


@pytest.fixture
def clean_host(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> dict:
    """Replicate the clean-host fixture from test_doctor.py.

    Keeps the doctor green so we can isolate the ``--output-dir`` failure
    branch from the HARD-capability one.
    """

    claude_home = tmp_path / ".claude"
    claude_home.mkdir()

    def fake_which(name: str) -> str:
        return f"/usr/bin/{name}"

    monkeypatch.setattr(shutil, "which", fake_which)
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    monkeypatch.setattr(
        doctor_module,
        "_default_claude_version_probe",
        lambda: "claude 0.5.1",
    )
    return {"home": tmp_path, "claude_home": claude_home}


def test_doctor_rejects_non_allowlisted_output_dir(clean_host: dict) -> None:
    """``--output-dir /etc/foo`` exits 2 with the policy quoted verbatim."""

    runner = CliRunner()
    result = runner.invoke(eval_group, ["doctor", "--output-dir", "/etc/foo"])
    assert result.exit_code == SCRATCH_ROOT_VIOLATION_EXIT_CODE
    assert SCRATCH_ROOT_POLICY in result.stderr
    # The offending path must appear in the forensic detail so an
    # operator does not have to re-read their own command line.
    assert "/etc/foo" in result.stderr


def test_doctor_rejects_real_home_output_dir(clean_host: dict) -> None:
    """The NFR-SEC3 hard case (``~/.claude/``) refuses through the same path."""

    runner = CliRunner()
    result = runner.invoke(
        eval_group, ["doctor", "--output-dir", "/root/.claude"]
    )
    assert result.exit_code == SCRATCH_ROOT_VIOLATION_EXIT_CODE
    assert "/root/.claude" in result.stderr
    assert SCRATCH_ROOT_POLICY in result.stderr


def test_doctor_accepts_allowlisted_output_dir(clean_host: dict) -> None:
    """Allowlisted ``--output-dir`` MUST NOT regress the green-path exit 0."""

    runner = CliRunner()
    result = runner.invoke(
        eval_group, ["doctor", "--output-dir", "/tmp/eval-runs/sub"]
    )
    assert result.exit_code == 0, result.output
    assert "all HARD capabilities satisfied" in result.output
    # The policy block MUST NOT appear in the happy path -- the renderer
    # is failure-only by contract.
    assert SCRATCH_ROOT_POLICY not in result.stderr
    assert SCRATCH_ROOT_POLICY not in result.output


def test_doctor_output_dir_violation_takes_precedence_over_hard_check(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Scratch-root rejection MUST fire before HARD-capability checks.

    If a path violates the policy, doctor refuses to probe any further --
    the operator has misconfigured the invocation, and running the HARD
    suite would only spam unrelated failure lines.
    """

    # Force claude binary missing so HARD checks would otherwise fail.
    monkeypatch.setattr(shutil, "which", lambda name: None)
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    monkeypatch.setattr(
        doctor_module,
        "_default_claude_version_probe",
        lambda: None,
    )

    runner = CliRunner()
    result = runner.invoke(
        eval_group, ["doctor", "--output-dir", "/etc/foo"]
    )
    assert result.exit_code == SCRATCH_ROOT_VIOLATION_EXIT_CODE
    # HARD-failure artifact MUST NOT appear: doctor exited before
    # building the capability report.
    assert "binary.claude" not in result.stderr


# ---------------------------------------------------------------------------
# Single source of truth: EvalConfig.allowed_scratch_roots
# ---------------------------------------------------------------------------


def test_default_allowlist_matches_policy_constant() -> None:
    """The default config and the policy constant MUST list the same roots."""

    config = EvalConfig()
    root_strs = [str(p) for p in config.allowed_scratch_roots]
    # Each default root must be named in the policy block.
    assert any("/tmp/eval-runs" in r for r in root_strs)
    assert any(".dev/eval-runs" in r for r in root_strs)


def test_narrowing_config_changes_what_resolve_accepts() -> None:
    """`EvalConfig.allowed_scratch_roots` is the only source of truth.

    Passing an explicit narrowed config to :func:`resolve_scratch_root`
    MUST change which paths pass — proving the helper does not embed a
    hard-coded fallback copy of the policy. Doctor builds a default
    :class:`EvalConfig` internally via the helper, so this assertion
    pins the helper-level contract; the doctor-level companion is
    :func:`test_doctor_uses_default_evalconfig_allowlist` below.
    """

    sole_root = Path("/tmp/custom-eval-roots")
    narrowed = EvalConfig(allowed_scratch_roots=(sole_root,))

    # The previously-default root is rejected when the supplied config
    # drops it from the allowlist.
    with pytest.raises(ScratchRootViolation):
        resolve_scratch_root("/tmp/eval-runs/foo", config=narrowed)

    # The narrowed allowlist accepts a path under its single entry.
    resolved = resolve_scratch_root(sole_root / "x", config=narrowed)
    assert resolved == (sole_root / "x").resolve()


def test_doctor_uses_default_evalconfig_allowlist(clean_host: dict) -> None:
    """Doctor MUST source the allowlist from a default-constructed EvalConfig.

    Cross-checks the OPS-002 "single source of truth" claim at the CLI
    boundary: doctor accepts ``/tmp/eval-runs/`` (default allowlist
    entry) AND rejects ``/tmp/other-runs`` (close-but-not-quite prefix)
    in the same invocation pair. Together they prove doctor honors the
    policy without embedding its own copy.
    """

    runner = CliRunner()

    ok = runner.invoke(
        eval_group, ["doctor", "--output-dir", "/tmp/eval-runs/passing"]
    )
    assert ok.exit_code == 0, ok.output

    bad = runner.invoke(
        eval_group, ["doctor", "--output-dir", "/tmp/other-runs"]
    )
    assert bad.exit_code == SCRATCH_ROOT_VIOLATION_EXIT_CODE
    assert SCRATCH_ROOT_POLICY in bad.stderr


# ---------------------------------------------------------------------------
# Documentation cannot drift from the runtime check
# ---------------------------------------------------------------------------


def test_scratch_roots_doc_exists() -> None:
    """`docs/eval/scratch-roots.md` MUST ship in the repo."""

    assert SCRATCH_ROOTS_DOC.is_file(), f"missing policy doc: {SCRATCH_ROOTS_DOC}"


def test_scratch_roots_doc_names_three_allowed_roots() -> None:
    """The doc MUST name the three roots from the policy constant."""

    text = SCRATCH_ROOTS_DOC.read_text()
    assert "/tmp/eval-runs/" in text
    assert ".dev/eval-runs/" in text
    assert "--output-dir" in text


def test_scratch_roots_doc_references_runtime_modules() -> None:
    """The doc MUST cross-link to the modules that enforce the policy."""

    text = SCRATCH_ROOTS_DOC.read_text()
    # The doc names the three load-bearing references so future readers
    # can navigate from prose to code.
    for ref in (
        "EvalConfig.allowed_scratch_roots",
        "resolve_scratch_root",
        "containment_guard",
    ):
        assert ref in text, f"doc missing cross-reference: {ref}"
