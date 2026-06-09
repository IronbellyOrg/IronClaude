"""End-to-end tests that execute the ``docs/swarm/user-guide.md`` examples and
pin their documented outcomes against the real CLI.

Each test mirrors a numbered User Guide / README section and asserts the exact
exit code, stdout signature, and on-disk artifact set the docs promise. The
``swarm_group`` is invoked through click's ``CliRunner`` so the full
**Wave 0 preflight -> Wave 1 dispatch -> artifact write** path runs for real.
Every runnable example uses ``--transport stub`` (in-process, deterministic, no
network), exactly as the guide instructs, so these tests are hermetic and CI-safe.

If the swarm CLI surface changes, these tests are the contract that keeps the docs
honest: a failure here means either the code regressed or a doc example went stale.

Source of expected values: docs/swarm/{README,user-guide,command-reference}.md and
the live-captured ground truth in .dev/swarm-docs-work/ground-truth.md.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from superclaude.cli.swarm import swarm_group
from superclaude.cli.swarm.commands import (
    DONE_SENTINEL_FILENAME,
    EXECUTION_LOG_JSONL_FILENAME,
    EXECUTION_LOG_MD_FILENAME,
    EXIT_INVALID,
    EXIT_OK,
    EXIT_USAGE,
    RESULT_CONTRACT_FILENAME,
    SWARM_STATE_FILENAME,
    TERMINAL_STATE_VALUE,
)

MANIFEST_FILENAME = "manifest.json"
MERGED_FILENAME = "merged.md"

# A target with >=50 non-whitespace bytes so it clears the IMM-4 preflight floor
# (User Guide §1). Mirrors the guide's worked example verbatim.
TARGET_SRC = (
    "def calculate_total(items, tax_rate):\n"
    "    subtotal = 0\n"
    "    for item in items:\n"
    "        subtotal = subtotal - item.price   # bug: should be +=\n"
    "    return subtotal + subtotal * tax_rate\n"
)

# All env keys that gate the openai_compat transport (User Guide §6).
_T2_ENV_KEYS = ["T2ProxyUrl", "T2ProxyKey"] + [f"T2Model0{i}" for i in range(1, 10)]


@pytest.fixture()
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture()
def target(tmp_path: Path) -> Path:
    p = tmp_path / "target.py"
    p.write_text(TARGET_SRC)
    return p


def _run(runner: CliRunner, *args: str, **kwargs):
    """Invoke `superclaude swarm <args>` through the registered group."""
    return runner.invoke(swarm_group, list(args), **kwargs)


def _artifact_names(d: Path) -> set[str]:
    return {p.name for p in d.iterdir()} if d.is_dir() else set()


# ---------------------------------------------------------------------------
# §1 Quickstart — first swarm (stub transport)
# ---------------------------------------------------------------------------
def test_quickstart_lens_bare_review_emits_four_artifacts(runner, target, tmp_path):
    """User Guide §1 / README quickstart: a stub `--lens bare-review` run exits 0,
    dispatches 3 workers, and writes exactly the four observability artifacts."""
    out = tmp_path / "out"
    result = _run(
        runner, "run", "--lens", "bare-review",
        "--target", str(target), "--output", str(out), "--transport", "stub",
    )
    assert result.exit_code == EXIT_OK, result.output
    assert "dispatched job (mode=lens, workers=3, results=3)" in result.output

    names = _artifact_names(out)
    assert names == {
        SWARM_STATE_FILENAME,
        EXECUTION_LOG_JSONL_FILENAME,
        EXECUTION_LOG_MD_FILENAME,
        MANIFEST_FILENAME,
    }, f"unexpected artifact set: {names}"

    # state reaches terminal
    state = json.loads((out / SWARM_STATE_FILENAME).read_text())
    assert state["state"] == TERMINAL_STATE_VALUE


def test_quickstart_does_not_emit_m5_artifacts(runner, target, tmp_path):
    """README 'What a run emits today': the dispatch-only path does NOT produce
    merged.md / return-contract.yaml / done.json (pending M5)."""
    out = tmp_path / "out"
    result = _run(
        runner, "run", "--lens", "bare-review",
        "--target", str(target), "--output", str(out), "--transport", "stub",
    )
    assert result.exit_code == EXIT_OK, result.output
    for absent in (MERGED_FILENAME, RESULT_CONTRACT_FILENAME, DONE_SENTINEL_FILENAME):
        assert not (out / absent).exists(), f"{absent} should not exist on the M-state run path"


# ---------------------------------------------------------------------------
# §2 Validate the bundled lens registry
# ---------------------------------------------------------------------------
def test_validate_lenses_registry_ok(runner):
    """User Guide §2: registry validates with 8 entries inspected, 7 validated."""
    result = _run(runner, "validate-lenses")
    assert result.exit_code == EXIT_OK, result.output
    assert "registry OK (8 entries inspected, 7 validated)" in result.output


def test_validate_lenses_warning_mode_exits_zero(runner):
    """User Guide §2: --warning-mode is non-blocking (exit 0)."""
    result = _run(runner, "validate-lenses", "--warning-mode")
    assert result.exit_code == EXIT_OK, result.output


# ---------------------------------------------------------------------------
# §3 Scaffold -> edit -> validate -> run a full JobSpec
# ---------------------------------------------------------------------------
def test_scaffold_emits_schema_valid_spec(runner, tmp_path):
    """User Guide §3a + command-reference: a scaffolded spec passes `validate`
    out of the box, with target.path / output.dir as empty placeholders."""
    spec = tmp_path / "job.json"
    r1 = _run(runner, "scaffold", "--lens", "bare-review", "--output", str(spec))
    assert r1.exit_code == EXIT_OK, r1.output
    assert spec.exists()

    doc = json.loads(spec.read_text())
    assert doc["lens"] == "bare-review"
    assert doc["target"]["path"] == ""
    assert doc["output"]["dir"] == ""

    r2 = _run(runner, "validate", str(spec))
    assert r2.exit_code == EXIT_OK, r2.output
    assert "OK" in r2.output


def test_full_spec_roundtrip_with_worker_override(runner, target, tmp_path):
    """User Guide §3: scaffold -> patch target/output + worker override ->
    validate (0) -> run (0) reports mode=spec-file with the overridden count."""
    spec = tmp_path / "job.json"
    out = tmp_path / "job-out"
    _run(runner, "scaffold", "--lens", "bare-review", "--output", str(spec))

    doc = json.loads(spec.read_text())
    doc["target"]["path"] = str(target)
    doc["output"]["dir"] = str(out)
    doc["workers"]["count"] = 2
    doc["workers"]["models"] = doc["workers"]["models"][:2]  # keep count <= |models|
    spec.write_text(json.dumps(doc, indent=2))

    rv = _run(runner, "validate", str(spec))
    assert rv.exit_code == EXIT_OK, rv.output

    rr = _run(runner, "run", str(spec), "--output", str(out), "--transport", "stub")
    assert rr.exit_code == EXIT_OK, rr.output
    assert "dispatched job (mode=spec-file, workers=2, results=2)" in rr.output


# ---------------------------------------------------------------------------
# §4 Choosing a lens — worker-count differences
# ---------------------------------------------------------------------------
def test_edge_case_hunt_defaults_to_four_workers(runner, target, tmp_path):
    """User Guide §4: edge-case-hunt is a 4-worker lens."""
    out = tmp_path / "edge-out"
    result = _run(
        runner, "run", "--lens", "edge-case-hunt",
        "--target", str(target), "--output", str(out), "--transport", "stub",
    )
    assert result.exit_code == EXIT_OK, result.output
    assert "dispatched job (mode=lens, workers=4, results=4)" in result.output


# ---------------------------------------------------------------------------
# §5 Inspecting results — status / logs / manifest
# ---------------------------------------------------------------------------
@pytest.fixture()
def completed_run(runner, target, tmp_path) -> Path:
    out = tmp_path / "out"
    result = _run(
        runner, "run", "--lens", "bare-review",
        "--target", str(target), "--output", str(out), "--transport", "stub",
    )
    assert result.exit_code == EXIT_OK, result.output
    return out


def test_status_reports_terminal(runner, completed_run):
    """User Guide §5: status on a finished job reports phase=terminal, exit 0."""
    result = _run(runner, "status", "--output", str(completed_run))
    assert result.exit_code == EXIT_OK, result.output
    assert "phase=terminal" in result.output


def test_status_missing_dir_is_usage_error(runner, tmp_path):
    """User Guide §11 / command-reference: missing output dir -> exit 2."""
    result = _run(runner, "status", "--output", str(tmp_path / "nope"))
    assert result.exit_code == EXIT_USAGE, result.output


def test_logs_md_and_jsonl_share_the_same_stream(runner, completed_run):
    """User Guide §5: both log surfaces dump cleanly; JSONL parses per-line and
    carries event_type records."""
    md = _run(runner, "logs", "--output", str(completed_run))
    assert md.exit_code == EXIT_OK, md.output
    assert md.output.strip(), "md log dump was empty"

    js = _run(runner, "logs", "--output", str(completed_run), "--jsonl")
    assert js.exit_code == EXIT_OK, js.output
    records = [json.loads(line) for line in js.output.splitlines() if line.strip().startswith("{")]
    assert records, "no JSONL records parsed"
    assert all("event_type" in r for r in records)
    # the dispatch path always emits the opening wave transition
    assert any(r["event_type"] == "wave_transition" for r in records)


def test_manifest_records_lens_and_transport(runner, completed_run):
    """User Guide §5: manifest is the durable lens snapshot + preflight summary."""
    manifest = json.loads((completed_run / MANIFEST_FILENAME).read_text())
    assert manifest["job_id"]
    assert manifest["preflight"]["transport_kind"] == "stub"
    assert manifest["preflight"]["workers_requested"] == 3
    assert manifest["resolved_lens_entry"]["name"] == "bare-review"


# ---------------------------------------------------------------------------
# §6 Real proxy — env-missing fails at transport construction
# ---------------------------------------------------------------------------
def test_openai_compat_missing_env_fails_at_transport_construction(
    runner, target, tmp_path, monkeypatch
):
    """User Guide §6c: openai_compat with the T2 env contract unset fails with a
    'cannot construct transport' diagnostic naming the missing vars, exit 1.
    manifest + state are written; no return-contract.yaml (run never reaches Wave 1)."""
    for key in _T2_ENV_KEYS:
        monkeypatch.delenv(key, raising=False)

    out = tmp_path / "env-out"
    result = _run(
        runner, "run", "--lens", "bare-review",
        "--target", str(target), "--output", str(out), "--transport", "openai_compat",
    )
    assert result.exit_code == EXIT_INVALID, result.output
    assert "cannot construct 'openai_compat' transport" in result.output
    assert "missing:" in result.output
    # forensic artifacts written, but no contract (fails before dispatch)
    assert not (out / RESULT_CONTRACT_FILENAME).exists()


# ---------------------------------------------------------------------------
# §11 Troubleshooting — documented failure modes
# ---------------------------------------------------------------------------
def test_too_small_target_fails_preflight_and_creates_no_output(runner, tmp_path):
    """User Guide §11: a <50-nonws-byte target fails IMM-4 (exit 1) and the output
    directory is NOT created."""
    tiny = tmp_path / "tiny.py"
    tiny.write_text("x = 1\n")
    out = tmp_path / "tiny-out"
    result = _run(
        runner, "run", "--lens", "bare-review",
        "--target", str(tiny), "--output", str(out), "--transport", "stub",
    )
    assert result.exit_code == EXIT_INVALID, result.output
    assert "preflight FAILED" in result.output
    assert "imm4.target_too_small" in result.output
    assert not out.exists(), "output dir must not be created on preflight failure"


def test_unknown_lens_is_usage_error(runner, target, tmp_path):
    """User Guide §11: an unknown lens name -> exit 2."""
    result = _run(
        runner, "run", "--lens", "does-not-exist",
        "--target", str(target), "--output", str(tmp_path / "o"), "--transport", "stub",
    )
    assert result.exit_code == EXIT_USAGE, result.output


def test_validate_is_schema_only_and_misses_imm4(runner, tmp_path):
    """User Guide §3c gotcha: `validate` is schema-only, so a spec pointing at a
    too-small target PASSES validate (exit 0) but its `run` fails preflight (exit 1).
    This pins the documented validate-vs-preflight gap."""
    tiny = tmp_path / "tiny.py"
    tiny.write_text("x = 1\n")
    out = tmp_path / "out"
    spec = tmp_path / "job.json"
    _run(runner, "scaffold", "--lens", "bare-review", "--output", str(spec))
    doc = json.loads(spec.read_text())
    doc["target"]["path"] = str(tiny)
    doc["output"]["dir"] = str(out)
    spec.write_text(json.dumps(doc, indent=2))

    rv = _run(runner, "validate", str(spec))
    assert rv.exit_code == EXIT_OK, f"schema validate should pass: {rv.output}"

    rr = _run(runner, "run", str(spec), "--output", str(out), "--transport", "stub")
    assert rr.exit_code == EXIT_INVALID, rr.output
    assert "preflight FAILED" in rr.output


def test_validate_missing_file_is_usage_error(runner, tmp_path):
    """command-reference: validate on a missing file -> exit 2."""
    result = _run(runner, "validate", str(tmp_path / "nope.json"))
    assert result.exit_code == EXIT_USAGE, result.output


def test_validate_malformed_json_is_usage_error(runner, tmp_path):
    """command-reference: validate on non-JSON -> exit 2."""
    bad = tmp_path / "bad.json"
    bad.write_text("{not valid json")
    result = _run(runner, "validate", str(bad))
    assert result.exit_code == EXIT_USAGE, result.output
