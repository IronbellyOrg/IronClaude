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
def test_quickstart_lens_bare_review_emits_observability_artifacts(
    runner, target, tmp_path
):
    """User Guide §1 / README quickstart: a stub `--lens bare-review` run exits 0,
    dispatches 3 workers, and writes the four observability artifacts. Post-WS-0 the
    same run ALSO emits the normalized per-reviewer bodies + return-contract.yaml +
    merged.md (covered by test_quickstart_emits_normalized_artifacts), so this test
    asserts the observability artifacts are PRESENT (subset) rather than the exact set."""
    out = tmp_path / "out"
    result = _run(
        runner,
        "run",
        "--lens",
        "bare-review",
        "--target",
        str(target),
        "--output",
        str(out),
        "--transport",
        "stub",
    )
    assert result.exit_code == EXIT_OK, result.output
    assert "dispatched job (mode=lens, workers=3, results=3)" in result.output

    names = _artifact_names(out)
    assert {
        SWARM_STATE_FILENAME,
        EXECUTION_LOG_JSONL_FILENAME,
        EXECUTION_LOG_MD_FILENAME,
        MANIFEST_FILENAME,
    } <= names, f"observability artifacts missing from set: {names}"

    # state reaches terminal
    state = json.loads((out / SWARM_STATE_FILENAME).read_text())
    assert state["state"] == TERMINAL_STATE_VALUE


def test_quickstart_does_not_emit_done_sentinel(runner, target, tmp_path):
    """WS-0 (G-4): the inline pipeline now emits merged.md + return-contract.yaml
    (see test_quickstart_emits_normalized_artifacts), but NOT the done.json sentinel
    (reduce_wave3 does not write it; the on_completion done-sentinel step is not wired
    on this inline path). This is the narrowed remnant of the old M5-absent assertion."""
    out = tmp_path / "out"
    result = _run(
        runner,
        "run",
        "--lens",
        "bare-review",
        "--target",
        str(target),
        "--output",
        str(out),
        "--transport",
        "stub",
    )
    assert result.exit_code == EXIT_OK, result.output
    assert not (out / DONE_SENTINEL_FILENAME).exists(), (
        f"{DONE_SENTINEL_FILENAME} should not exist on the inline (non-resume) WS-0 path"
    )


def test_quickstart_emits_normalized_artifacts(runner, target, tmp_path):
    """WS-0 (G-3): the inline (no ``--resume``) ``swarm run --lens bare-review``
    path now runs the full Wave 1->2->3 pipeline, so it emits ``return-contract.yaml``
    AND a normalized per-reviewer body for each of the 3 workers. This is the exact
    inverse of the pre-WS-0 absent-contract assertion."""
    out = tmp_path / "out"
    result = _run(
        runner,
        "run",
        "--lens",
        "bare-review",
        "--target",
        str(target),
        "--output",
        str(out),
        "--transport",
        "stub",
    )
    assert result.exit_code == EXIT_OK, result.output

    # Contract is now emitted (was absent pre-WS-0).
    assert (out / RESULT_CONTRACT_FILENAME).exists(), (
        "WS-0 must emit return-contract.yaml"
    )

    # One normalized body per reviewer (final_path), each carrying the rendered
    # bare-review header and the target checksum (cf. test_recipe_bare_review.py).
    final_bodies = sorted(out.glob("bare-review-*.final.md"))
    assert len(final_bodies) == 3, (
        f"expected 3 normalized bodies, got {[p.name for p in final_bodies]}"
    )
    for body_path in final_bodies:
        body = body_path.read_text(encoding="utf-8")
        assert "T2-Bare Review" in body, f"missing rendered header in {body_path.name}"
        assert "target_checksum:" in body, (
            f"missing target checksum in {body_path.name}"
        )

    # The contract parses and records the 3-reviewer success run.
    contract = (out / RESULT_CONTRACT_FILENAME).read_text(encoding="utf-8")
    assert "status: success" in contract
    assert "workers_requested: 3" in contract
    assert "--suspect-source" in contract, (
        "bare-review contract must carry the suspect-source next command"
    )

    # PG2 C1: the recommended_next_command must be ACTIONABLE — the lens template's
    # {suspect_files}/{compare_files} placeholders must be substituted with real
    # reviewer paths (legacy t2_normalize parity), not shipped verbatim.
    assert "{suspect_files}" not in contract, (
        "next-command placeholder left unsubstituted"
    )
    assert "{compare_files}" not in contract, (
        "next-command placeholder left unsubstituted"
    )
    assert ".final.md" in contract, (
        "next-command must reference the reviewer output paths"
    )


def test_label_flag_stamps_caller_label_frontmatter(runner, target, tmp_path):
    """B-4: ``--label`` is stamped into each per-reviewer body's caller_label
    frontmatter (legacy t2_preflight.sh --label parity)."""
    out = tmp_path / "label-out"
    result = _run(
        runner,
        "run",
        "--lens",
        "bare-review",
        "--label",
        "my-caller-ctx",
        "--target",
        str(target),
        "--output",
        str(out),
        "--transport",
        "stub",
    )
    assert result.exit_code == EXIT_OK, result.output
    bodies = sorted(out.glob("bare-review-*.final.md"))
    assert bodies, "no normalized bodies emitted"
    for body_path in bodies:
        assert 'caller_label: "my-caller-ctx"' in body_path.read_text(encoding="utf-8")


def test_reviewers_flag_rejects_below_range(runner, target, tmp_path):
    """B-1 / AC-1.4: ``--reviewers 1`` (below the inclusive [2,4] floor) is a usage error."""
    out = tmp_path / "rev-low"
    result = _run(
        runner,
        "run",
        "--lens",
        "bare-review",
        "--reviewers",
        "1",
        "--target",
        str(target),
        "--output",
        str(out),
        "--transport",
        "stub",
    )
    assert result.exit_code == EXIT_USAGE, result.output


def test_target_line_cap_and_timeout_flags_accepted(runner, target, tmp_path):
    """B-2 / B-3: ``--target-line-cap`` and ``--timeout-sec`` are accepted and the run
    completes successfully (their behavioral effect is not observable via the stub
    stdout; this guards the flag surface + spec threading from a usage regression)."""
    out = tmp_path / "caps-out"
    result = _run(
        runner,
        "run",
        "--lens",
        "bare-review",
        "--target-line-cap",
        "2000",
        "--timeout-sec",
        "120",
        "--target",
        str(target),
        "--output",
        str(out),
        "--transport",
        "stub",
    )
    assert result.exit_code == EXIT_OK, result.output
    assert (out / RESULT_CONTRACT_FILENAME).exists()


# ---------------------------------------------------------------------------
# §2 Validate the bundled lens registry
# ---------------------------------------------------------------------------
def test_validate_lenses_registry_ok(runner):
    """User Guide §2: registry validates with 9 entries inspected, 8 validated."""
    result = _run(runner, "validate-lenses")
    assert result.exit_code == EXIT_OK, result.output
    assert "registry OK (9 entries inspected, 8 validated)" in result.output


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
        runner,
        "run",
        "--lens",
        "edge-case-hunt",
        "--target",
        str(target),
        "--output",
        str(out),
        "--transport",
        "stub",
    )
    assert result.exit_code == EXIT_OK, result.output
    assert "dispatched job (mode=lens, workers=4, results=4)" in result.output


# ---------------------------------------------------------------------------
# WS-0 B-1 — --reviewers overrides the bare-review worker count [2,4]
# ---------------------------------------------------------------------------
def test_reviewers_flag_overrides_worker_count(runner, target, tmp_path):
    """B-1 / AC-1.4: ``--reviewers 4`` actually dispatches 4 workers — the value
    must survive both the (test-only) ``count == 4`` reset and the INV-005
    model-pool guard, proving it reached the post-expansion spec."""
    out = tmp_path / "rev-out"
    result = _run(
        runner,
        "run",
        "--lens",
        "bare-review",
        "--reviewers",
        "4",
        "--target",
        str(target),
        "--output",
        str(out),
        "--transport",
        "stub",
    )
    assert result.exit_code == EXIT_OK, result.output
    assert "dispatched job (mode=lens, workers=4, results=4)" in result.output
    manifest = json.loads((out / MANIFEST_FILENAME).read_text())
    assert manifest["preflight"]["workers_requested"] == 4


def test_reviewers_flag_rejects_out_of_range(runner, target, tmp_path):
    """B-1 / AC-1.4: ``--reviewers`` outside the inclusive [2, 4] range is a usage
    error (legacy ``t2_preflight.sh`` invariant)."""
    out = tmp_path / "rev-bad"
    result = _run(
        runner,
        "run",
        "--lens",
        "bare-review",
        "--reviewers",
        "5",
        "--target",
        str(target),
        "--output",
        str(out),
        "--transport",
        "stub",
    )
    assert result.exit_code == EXIT_USAGE, result.output


# WS-0 B-1 regression — --reviewers must NOT clobber a spec-file/--stdin caller's
# real ``workers.models`` (Augment PR #178 MEDIUM). The placeholder resize is gated
# to lens mode; spec-file/stdin keep their real model IDs and rely on the INV-005
# warn-with-defaults clamp if --reviewers exceeds the pool. (spec-file and --stdin
# share the same ``mode != "lens"`` branch, so these spec-file tests cover stdin too.)
def test_reviewers_preserves_real_models_in_spec_file_mode(
    runner, target, tmp_path, monkeypatch
):
    """Augment PR #178 MEDIUM: in spec-file mode ``--reviewers N`` overrides the worker
    COUNT without overwriting caller-supplied real model IDs in ``workers.models``.
    Captures the spec dict at the ``run_preflight`` boundary (the only place
    ``workers.models`` is behaviorally consumed) and asserts the real IDs survived."""
    import superclaude.cli.swarm.preflight as swarm_preflight

    spec = tmp_path / "job.json"
    out = tmp_path / "rev-specfile-out"
    _run(runner, "scaffold", "--lens", "bare-review", "--output", str(spec))
    doc = json.loads(spec.read_text())
    doc["target"]["path"] = str(target)
    doc["output"]["dir"] = str(out)
    doc["workers"]["count"] = 3
    doc["workers"]["models"] = ["alpha-model", "beta-model", "gamma-model"]
    spec.write_text(json.dumps(doc, indent=2))

    captured: dict = {}
    real_run_preflight = swarm_preflight.run_preflight

    def _capturing_run_preflight(spec_dict, **kwargs):
        workers = spec_dict.get("workers", {})
        captured["models"] = list(workers.get("models", []))
        captured["count"] = workers.get("count")
        return real_run_preflight(spec_dict, **kwargs)

    monkeypatch.setattr(swarm_preflight, "run_preflight", _capturing_run_preflight)
    result = _run(
        runner,
        "run",
        str(spec),
        "--reviewers",
        "3",
        "--output",
        str(out),
        "--transport",
        "stub",
    )
    assert result.exit_code == EXIT_OK, result.output
    assert captured["models"] == ["alpha-model", "beta-model", "gamma-model"]
    assert captured["count"] == 3
    assert not any(m.startswith("lens-default-model-") for m in captured["models"])


def test_reviewers_does_not_inflate_spec_file_pool(runner, target, tmp_path):
    """Augment PR #178 MEDIUM: ``--reviewers`` must not fabricate placeholder models to
    pad a spec-file caller's real pool. With a real 2-model pool + ``--reviewers 4`` the
    INV-005 warn-with-defaults guard clamps the count to the real pool size (2); the OLD
    code synthesized 4 placeholders and dispatched 4. The clamp is the observable proof
    the real pool was preserved."""
    spec = tmp_path / "job.json"
    out = tmp_path / "rev-clamp-out"
    _run(runner, "scaffold", "--lens", "bare-review", "--output", str(spec))
    doc = json.loads(spec.read_text())
    doc["target"]["path"] = str(target)
    doc["output"]["dir"] = str(out)
    doc["workers"]["count"] = 2
    doc["workers"]["models"] = ["alpha-model", "beta-model"]
    spec.write_text(json.dumps(doc, indent=2))

    result = _run(
        runner,
        "run",
        str(spec),
        "--reviewers",
        "4",
        "--output",
        str(out),
        "--transport",
        "stub",
    )
    assert result.exit_code == EXIT_OK, result.output
    manifest = json.loads((out / MANIFEST_FILENAME).read_text())
    assert manifest["preflight"]["workers_requested"] == 2


# ---------------------------------------------------------------------------
# §5 Inspecting results — status / logs / manifest
# ---------------------------------------------------------------------------
@pytest.fixture()
def completed_run(runner, target, tmp_path) -> Path:
    out = tmp_path / "out"
    result = _run(
        runner,
        "run",
        "--lens",
        "bare-review",
        "--target",
        str(target),
        "--output",
        str(out),
        "--transport",
        "stub",
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
    records = [
        json.loads(line)
        for line in js.output.splitlines()
        if line.strip().startswith("{")
    ]
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
        runner,
        "run",
        "--lens",
        "bare-review",
        "--target",
        str(target),
        "--output",
        str(out),
        "--transport",
        "openai_compat",
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
        runner,
        "run",
        "--lens",
        "bare-review",
        "--target",
        str(tiny),
        "--output",
        str(out),
        "--transport",
        "stub",
    )
    assert result.exit_code == EXIT_INVALID, result.output
    assert "preflight FAILED" in result.output
    assert "imm4.target_too_small" in result.output
    assert not out.exists(), "output dir must not be created on preflight failure"


def test_unknown_lens_is_usage_error(runner, target, tmp_path):
    """User Guide §11: an unknown lens name -> exit 2."""
    result = _run(
        runner,
        "run",
        "--lens",
        "does-not-exist",
        "--target",
        str(target),
        "--output",
        str(tmp_path / "o"),
        "--transport",
        "stub",
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
