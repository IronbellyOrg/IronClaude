"""CLI tests for the ``superclaude reflect contract-status`` sibling command.

OQ-2 selected the sibling Click command
``superclaude reflect contract-status [--validate] --repo <owner/repo> --pr <n>``
as the SINGLE reflect readiness surface (see
``.dev/tasks/to-do/TASK-RF-detection-contract-20260701-164700/phase-outputs/plans/OQ-2-reflect-surface-decision.md``).
These tests exercise exactly that surface via ``CliRunner`` and prove it:

* is a real subcommand of ``reflect_group`` exposing ``--validate``/``--repo``/``--pr``;
* runs WITHOUT a tasklist argument (unlike ``reflect run``) and prints readiness
  metadata (``state:`` ...);
* NEVER launches the normal reflect audit machinery
  (``ReflectRunner`` / ``resolve_config`` / ``ClaudeProcess``);
* NEVER writes the local ``detection-contract.locked.md`` lock by default, even
  under ``--validate``;
* emits readiness metadata only (no raw GitHub payload bodies).

``diagnose()`` in ``superclaude.pr_submit.contract_setup.diagnosis`` probes the
LOCAL override at ``<cwd>/.dev/pr-monitor/detection-contract.locked.md`` because
the CLI calls it without an explicit ``cwd=`` (so it uses ``Path.cwd()``). Every
test therefore runs inside ``CliRunner.isolated_filesystem()`` so the probe reads
a scratch cwd and NEVER touches the real ``/config/workspace/IronClaude/.dev/pr-monitor/``.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner

from superclaude.cli.reflect.commands import contract_status, reflect_group

# A unique sentinel that would only appear if a raw GitHub payload body leaked
# into readiness output. Readiness output is metadata-only, so it must be absent.
_RAW_BODY_SENTINEL = "RAW_BODY_SENTINEL_DO_NOT_PRINT"

# Local lock path (relative to the isolated cwd) that the readiness/validate path
# must NEVER create.
_LOCK_REL = Path(".dev/pr-monitor/detection-contract.locked.md")


def _block_reflect_audit_machinery():
    """Patch every reflect-audit entry point to raise if invoked.

    ``contract-status`` imports ONLY from ``superclaude.pr_submit.contract_setup``;
    ``ReflectRunner``/``resolve_config``/``ClaudeProcess`` live in
    ``superclaude.cli.reflect.{runner,config}`` and are imported lazily *inside*
    ``reflect run()``. Patching them to raise proves ``contract-status`` never
    reaches that code path.
    """
    return (
        patch(
            "superclaude.cli.reflect.runner.ReflectRunner",
            side_effect=AssertionError("ReflectRunner was invoked by contract-status"),
        ),
        patch(
            "superclaude.cli.reflect.config.resolve_config",
            side_effect=AssertionError("resolve_config was invoked by contract-status"),
        ),
        patch(
            "superclaude.cli.reflect.runner.ClaudeProcess",
            side_effect=AssertionError("ClaudeProcess was invoked by contract-status"),
        ),
    )


def test_group_help_lists_contract_status(cli_runner: CliRunner) -> None:
    """``reflect --help`` lists the ``contract-status`` subcommand (single surface)."""
    result = cli_runner.invoke(reflect_group, ["--help"])
    assert result.exit_code == 0
    assert "contract-status" in result.output


def test_contract_status_help_lists_validate_repo_pr(cli_runner: CliRunner) -> None:
    """``contract-status --help`` exposes exactly the OQ-2 option set."""
    result = cli_runner.invoke(reflect_group, ["contract-status", "--help"])
    assert result.exit_code == 0
    for flag in ("--validate", "--repo", "--pr"):
        assert flag in result.output, f"missing option in contract-status help: {flag}"


def test_contract_status_runs_without_tasklist(cli_runner: CliRunner) -> None:
    """``contract-status`` needs no tasklist argument and prints readiness fields.

    ``reflect run`` requires a positional ``tasklist`` (Click ``exists=True``);
    the sibling ``contract-status`` command must be independently invocable.
    """
    with cli_runner.isolated_filesystem():
        result = cli_runner.invoke(reflect_group, ["contract-status"])
    assert result.exit_code == 0, result.output
    # Readiness metadata surface (missing-contract diagnosis in a clean cwd).
    assert "state:" in result.output
    assert "state: missing" in result.output
    assert "next_command:" in result.output
    assert "validation_requested: false" in result.output


def test_contract_status_does_not_launch_reflect_audit_machinery(
    cli_runner: CliRunner,
) -> None:
    """``contract-status`` never constructs ReflectRunner/resolve_config/ClaudeProcess.

    All three are patched to raise; the command must still succeed and emit
    readiness metadata, proving it takes the diagnose-only path.
    """
    p_runner, p_config, p_claude = _block_reflect_audit_machinery()
    with cli_runner.isolated_filesystem():
        with p_runner as m_runner, p_config as m_config, p_claude as m_claude:
            result = cli_runner.invoke(
                reflect_group, ["contract-status", "--repo", "owner/repo", "--pr", "42"]
            )
    assert result.exit_code == 0, result.output
    assert "state:" in result.output
    m_runner.assert_not_called()
    m_config.assert_not_called()
    m_claude.assert_not_called()


def test_contract_status_validate_does_not_write_lock_by_default(
    cli_runner: CliRunner,
) -> None:
    """``--validate`` with no evidence prints a skip message and writes no lock.

    Runs inside an isolated cwd so ``diagnose()``'s probe reads a scratch dir.
    With no evidence available the command reports
    ``validation_error: validation skipped: ...`` and never creates the local
    ``detection-contract.locked.md``. Reflect-audit machinery is also blocked to
    prove ``--validate`` stays on the readiness path.
    """
    p_runner, p_config, p_claude = _block_reflect_audit_machinery()
    with cli_runner.isolated_filesystem() as fs:
        with p_runner, p_config, p_claude:
            result = cli_runner.invoke(
                reflect_group,
                ["contract-status", "--validate", "--repo", "owner/repo", "--pr", "7"],
            )
        lock_path = Path(fs) / _LOCK_REL
        lock_exists = lock_path.exists()
    assert result.exit_code == 0, result.output
    assert "validation_requested: true" in result.output
    # No evidence => validation is skipped, never a lock write.
    assert "validation skipped" in result.output
    assert not lock_exists, f"contract-status --validate wrote a lock at {lock_path}"


def test_contract_status_output_is_metadata_only(cli_runner: CliRunner) -> None:
    """Readiness/status output carries no raw GitHub payload body sentinels.

    NOTE: this runs in an empty cwd (``state=missing``, no evidence), so it only
    guards the missing-state metadata surface. The stronger
    ``--validate``/``validation_summary`` leak vector is guarded separately by
    ``test_contract_status_validate_output_redacts_raw_payload_body`` below, which
    plants a real sentinel-bearing payload and drives the run to ``state=ready``.
    """
    with cli_runner.isolated_filesystem():
        result = cli_runner.invoke(
            reflect_group, ["contract-status", "--repo", "owner/repo", "--pr", "9"]
        )
    assert result.exit_code == 0, result.output
    # Raw payload bodies (reviews[].body / comments[].body / check_run text) must
    # never appear in metadata-only readiness output.
    assert _RAW_BODY_SENTINEL not in result.output
    assert "body:" not in result.output


def _plant_locked_evidence_with_sentinel_body(
    fs: Path, *, repo: str, pr_number: int
) -> Path:
    """Build a locked override + a sentinel-bearing probe under the isolated cwd.

    The probe payload plants ``_RAW_BODY_SENTINEL`` into BOTH ``reviews[].body`` and
    ``comments[].body`` (the two raw-body surfaces the CLI ``validation_summary``
    echo could plausibly leak). The payload is otherwise a valid single-Augment
    ``clean`` review so ``derive_candidate``/``validate_candidate`` succeed and the
    ``--validate`` branch reaches the ``validation_summary:`` echo (``state=ready``).

    Layout mirrors the READY-state fixtures in
    ``tests/pr_submit/test_contract_setup_diagnosis.py`` /
    ``test_contract_setup_writer.py``:
      * probe dir under ``.dev/pr-monitor/probes/...`` (required by
        ``write_report``'s destination gate);
      * locked override at ``.dev/pr-monitor/detection-contract.locked.md`` whose
        ``probe_evidence`` points at the probe's ``combined-payload.json``.

    Returns the evidence FILE path (``combined-payload.json``) so callers can assert
    the sentinel is genuinely on disk (making the redaction guard non-trivial).
    """
    probe_dir = fs / ".dev" / "pr-monitor" / "probes" / f"pr-{pr_number}"
    probe_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "metadata": {
            "repo": repo,
            "pr_number": pr_number,
            "captured_at": "2026-07-01T00:00:00Z",
        },
        "reviews": [
            {
                "user": {"login": "augmentcode[bot]"},
                "app": {"slug": "augmentcode"},
                "author_association": "NONE",
                "state": "COMMENTED",
                "submitted_at": "2026-07-01T00:00:00Z",
                "body": _RAW_BODY_SENTINEL,
            }
        ],
        "comments": [{"user": {"login": "human"}, "body": _RAW_BODY_SENTINEL}],
        "check_runs": [],
    }
    combined = probe_dir / "combined-payload.json"
    combined.write_text(json.dumps(payload), encoding="utf-8")
    (probe_dir / "manifest.json").write_text(
        json.dumps(
            {
                "repo": repo,
                "pr_number": pr_number,
                "captured_at": "2026-07-01T00:00:00Z",
            }
        ),
        encoding="utf-8",
    )
    override = fs / _LOCK_REL
    override.parent.mkdir(parents=True, exist_ok=True)
    override.write_text(
        "# local locked contract\n\n```yaml\n"
        'augment_bot_login: "augmentcode[bot]"\n'
        "locked: true\n"
        f"probe_evidence: .dev/pr-monitor/probes/pr-{pr_number}/combined-payload.json\n"
        "```\n",
        encoding="utf-8",
    )
    return combined


def test_contract_status_validate_output_redacts_raw_payload_body(
    cli_runner: CliRunner,
) -> None:
    """``--validate`` reaches ``validation_summary:`` yet leaks no raw payload body.

    This closes the P4-QA-001 gap: the pre-existing metadata-only test ran in an
    empty ``state=missing`` cwd where the ``validation_summary:`` echo (the
    strongest CLI leak vector, ``commands.py`` L179-182) is never reached, so its
    sentinel-absence assertion passed trivially.

    Here we plant a locked override + a sentinel-bearing probe payload under the
    isolated cwd, then invoke ``contract-status --validate`` so the run:
      1. loads the sentinel-bearing evidence,
      2. derives + validates the candidate,
      3. writes a validation report, and
      4. echoes ``report.summary()`` under the ``validation_summary:`` block.

    The guard is non-trivial: we FIRST assert the sentinel is genuinely present in
    the on-disk evidence JSON (so a real leak *could* surface), THEN assert it is
    absent from the CLI output while the ``validation_summary:`` block and safe
    metadata (``state:``/``evidence_sha256:``/``blocker_count:``) ARE present.
    """
    repo, pr = "owner/repo", 9
    with cli_runner.isolated_filesystem() as fs:
        evidence_file = _plant_locked_evidence_with_sentinel_body(
            Path(fs), repo=repo, pr_number=pr
        )
        # The sentinel is genuinely on disk in the raw evidence body (a leak COULD
        # surface) -- this is what makes the absence assertion below meaningful.
        on_disk = evidence_file.read_text(encoding="utf-8")
        assert _RAW_BODY_SENTINEL in on_disk
        assert '"body"' in on_disk  # raw body key really is present in the payload

        result = cli_runner.invoke(
            reflect_group,
            ["contract-status", "--validate", "--repo", repo, "--pr", str(pr)],
        )

    assert result.exit_code == 0, result.output
    # The validate/ready path was actually exercised (NOT the empty missing path):
    # the validation_summary echo block and READY state are both present.
    assert "state: ready" in result.output
    assert "validation_summary:" in result.output
    assert "validation_requested: true" in result.output
    # Safe metadata IS surfaced (status / hash / counts).
    assert "evidence_sha256:" in result.output
    assert "blocker_count:" in result.output
    # ...but the raw payload body sentinel is NOT — redaction holds on the CLI
    # boundary through the validation_summary echo.
    assert _RAW_BODY_SENTINEL not in result.output
    assert "body:" not in result.output


def test_contract_status_is_a_real_reflect_subcommand() -> None:
    """Import the REAL command symbol and confirm group registration (no fakes)."""
    assert "contract-status" in reflect_group.commands
    assert reflect_group.commands["contract-status"] is contract_status
