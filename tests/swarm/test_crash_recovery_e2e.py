"""T06.08 -- NFR-005 kill-then-resume end-to-end crash recovery.

Covers roadmap row R-116 (NFR-005). Pins the operator-visible
contract of the full crash-recovery cycle: a swarm job whose Wave 1
dispatch is terminated mid-flight (SIGKILL-equivalent) leaves a
partially-populated output directory on disk (``manifest.json`` from
Wave 0 + per-worker ``*.meta.json`` / ``*.final.md`` sidecars for the
slots that made it before the kill); a follow-up
``swarm run --resume <job_id> --output <dir>`` reads the manifest,
classifies slot state from the sidecars, re-dispatches only the
remaining slots, and reaches a terminal state with ``merged.md``
regenerated when ``amalgamation_mode == "normalize+merge"``.

The differentiator from :mod:`tests/swarm/test_resume_crash_recovery`
(T06.04, the resume-orchestrator unit surface) is the **full lifecycle
in one test**: phase 1 runs ``run_cmd`` with a real on-disk spec, a
real target file, a real ``--output`` directory, and a real
``StubTransport``, with ``dispatch_wave1`` rigged to leave partial
work on disk before raising a kill-equivalent exception; phase 2 then
invokes ``run_cmd --resume`` against the directory phase 1 left
behind and asserts that the second run completes the work without
duplicating it.

The acceptance contract this module pins (phase-6-tasklist.md §T06.08):

    * **Kill-then-resume reaches terminal state with no duplicate work** --
      after phase 2 every requested slot is accounted for exactly once
      (the slot-0 sidecar from phase 1 survives the resume verbatim;
      the redispatch outputs land at the missing slot indices).
    * **Worker-level skip honored** -- the redispatch count equals the
      number of slots whose sidecars were missing or non-success at
      resume time; the stdout success line reports
      ``skipped=<S> redispatched=<R>`` with ``S + R == workers_requested``.
    * **Remaining slots re-dispatched** -- ``dispatch_wave1`` is called
      exactly once during phase 2 with ``workers_requested`` equal to
      the redispatch count, not the original N.
    * **Merge regenerated when applicable** -- when phase 1 crashes
      before merge ran (no ``merged.md`` on disk), phase 2 writes one;
      when phase 1 left a stale ``merged.md``, phase 2 replaces it
      with a fresh body that reflects the post-resume worker set
      (INV-010 via :func:`reduce_wave3` ``resume=True``).

The "kill" is modelled as a ``SystemExit(137)`` raised from a
monkeypatched ``dispatch_wave1`` after the partial sidecars have been
flushed to disk. Exit code 137 is the conventional shell signal-kill
encoding (``128 + 9``) so the simulation matches the operator's
mental model for a SIGKILL'd subprocess without requiring an actual
``os.kill`` (which would also kill the test runner).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from click.testing import CliRunner

from superclaude.cli.swarm.commands import (
    EXIT_OK,
    discover_succeeded_slots,
    run_cmd,
)
from superclaude.cli.swarm.models import WorkerResult
from superclaude.cli.swarm.schema import (
    CANONICAL_INJECTION_GUARD_SENTENCE,
    CURRENT_SPEC_VERSION,
)

# ---------------------------------------------------------------------------
# Fixture helpers -- minimal valid JobSpec wired through preflight end-to-end
# so the manifest emitted by Wave 0 is authentic (no hand-rolled manifest).
# ---------------------------------------------------------------------------


JOB_ID: str = "job-crash-recovery-T06.08"
LENS_NAME: str = "bare-review"
RECIPE_NAME: str = "bare-review-v1"
MODEL_SLUG: str = "stub-model"


def _runnable_spec(tmp_path: Path) -> dict[str, Any]:
    """Return a minimal valid JobSpec dict with paths resolved under tmp_path.

    The shape mirrors ``tests/swarm/test_commands_run.py::_runnable_spec``
    so the kill-then-resume cycle exercises the same preflight surface
    as the T03.01 smoke test. The transport is ``stub`` so phase 1 can
    run preflight to completion (the stub does not need env vars) and
    the kill simulation only has to defeat dispatch.
    """
    target = tmp_path / "target.py"
    target.write_text(
        "# T06.08 crash-recovery E2E target\n"
        + "def hello() -> str:\n    return 'hello world from a target'\n"
        + "# padding to clear the IMM-4 byte-floor guard\n" * 4,
        encoding="utf-8",
    )
    return {
        "spec_version": CURRENT_SPEC_VERSION,
        "job_id": JOB_ID,
        "created": "2026-06-01T00:00:00Z",
        "caller": {
            "skill": "sc-bare-review",
            "skill_version": "1.0.0",
            "invocation_label": "t06-08-crash-recovery-e2e",
            "kind": "cli",
        },
        "lens": LENS_NAME,
        "custom_prompt_dir": None,
        "workers": {
            "count": 3,
            "models": ["gpt-5-codex", "claude-haiku-4.5", "gemini-1.5-pro"],
            "timeout_sec": 180,
            "temperature": 0.2,
            "retry": {
                "on_5xx": True,
                "on_5xx_backoff_sec": 2,
                "on_4xx": False,
                "on_timeout": False,
            },
        },
        "transport": {
            "kind": "stub",
            "base_url_env": "T2ProxyUrl",
            "api_key_env": "T2ProxyKey",
        },
        "prompt": {
            "system": (
                "You are a code reviewer. " + CANONICAL_INJECTION_GUARD_SENTENCE
            ),
            "user_template": "Review: {{target}}",
            "variables": {},
        },
        "target": {
            "kind": "file",
            "path": str(target),
            "truncation": {"line_cap": 4000, "byte_floor": 50},
            "delimiters": {
                "open": "<<<TARGET>>>",
                "close": "<<<END TARGET>>>",
            },
            "injection_guard": {
                "enabled": True,
                "required_substring": CANONICAL_INJECTION_GUARD_SENTENCE,
            },
        },
        "normalization": {
            "recipe": RECIPE_NAME,
            "template_path": "/abs/path/to/template.j2",
            "schema_version": "1.0",
            "recipe_args": {},
            "on_parse_error": {"salvage": True, "retain_raw": True},
        },
        "output": {
            "dir": str(tmp_path / "out"),
            "filename_template": "{lens}-{index:02d}-{model_slug}.md",
            "lens_name": LENS_NAME,
            "atomic_write": True,
            "emit_meta_sidecar": True,
        },
        "amalgamation_mode": "normalize+merge",
        "status_policy": {
            "floor": 2,
            "success_first": True,
            "partial_threshold": 2,
        },
        "recommended_next_command_template": "sc:reflect on {job_id}",
        "recommended_next_command_substitutions": {"job_id": JOB_ID},
        "runtime": {
            "mode": "inline",
            "log_level": "info",
            "on_completion": {
                "write_done_sentinel": True,
                "print_contract_to_stdout": True,
            },
        },
    }


def _write_spec(tmp_path: Path, spec: dict[str, Any]) -> Path:
    """Serialize ``spec`` to ``tmp_path/spec.json`` and return the path."""
    path = tmp_path / "spec.json"
    path.write_text(json.dumps(spec), encoding="utf-8")
    return path


def _stage_succeeded_slot(
    output_dir: Path,
    *,
    slot_index: int,
    body: str,
) -> tuple[Path, Path]:
    """Flush the ``*.meta.json`` + ``*.final.md`` pair for one slot to disk.

    This is what the dispatcher would write before a SIGKILL hit it
    mid-loop (slot finished, sidecar landed atomically via
    ``normalize._emit_meta``). The pair is the on-disk signal that
    ``discover_succeeded_slots`` reads at resume time.

    Returns ``(meta_path, final_path)`` so the test can pin their
    contents and assert byte-for-byte survival across the resume.
    """
    stem = f"{LENS_NAME}-{slot_index:02d}-{MODEL_SLUG}"
    final_path = output_dir / f"{stem}.final.md"
    final_path.write_text(body, encoding="utf-8")
    meta_path = output_dir / f"{stem}.meta.json"
    meta_payload = {
        "recipe": RECIPE_NAME,
        "schema_version": "1.0",
        "salvaged": False,
        "status": "success",
        "bytes": len(body.encode("utf-8")),
    }
    meta_path.write_text(
        json.dumps(meta_payload, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    return meta_path, final_path


# ---------------------------------------------------------------------------
# Phase 1 helpers -- crash-injecting dispatch shims.
# ---------------------------------------------------------------------------


class _SimulatedKill(SystemExit):
    """SIGKILL-equivalent raised from inside the patched ``dispatch_wave1``.

    Using :class:`SystemExit` (not a plain :class:`Exception`) so the
    behavior matches a process that was killed: Click's runner reports
    the exit code via ``result.exception``; the test harness can
    inspect it without confusing the kill with a programming error.
    The integer ``137`` mirrors ``128 + SIGKILL`` (the shell-visible
    exit code of a kill-9'd subprocess).
    """

    def __init__(self) -> None:
        super().__init__(137)


def _crashing_dispatch_factory(
    output_dir: Path,
    *,
    survivors: list[int],
    survivor_body_template: str = "phase-1 slot {index} body\n",
):
    """Return a ``dispatch_wave1`` shim that stages survivors then crashes.

    Args:
        output_dir: ``--output`` dir preflight materialized; sidecars
            land here so the resume orchestrator finds them.
        survivors: list of slot indices to mark "succeeded" on disk
            before the simulated kill. The shim flushes one
            ``*.meta.json`` + ``*.final.md`` pair per index, mirroring
            what the real dispatcher would have written for slots that
            completed before the kill.
        survivor_body_template: deterministic final-body content so the
            byte-survival assertion is stable across runs.

    The returned shim raises :class:`_SimulatedKill` after staging so
    ``run_cmd`` propagates the kill up through Click and the test can
    observe a non-zero exit. The output directory is left in the
    partially-populated state a real SIGKILL'd dispatcher would have
    produced -- exactly the state the resume orchestrator must handle.
    """

    def _shim(preflight_result: Any, transport: Any = None, **kwargs: Any) -> list[Any]:
        for index in survivors:
            _stage_succeeded_slot(
                output_dir,
                slot_index=index,
                body=survivor_body_template.format(index=index),
            )
        raise _SimulatedKill()

    return _shim


# ---------------------------------------------------------------------------
# Phase 2 helpers -- resume-side dispatch + normalize shims.
# ---------------------------------------------------------------------------


def _resume_dispatch_factory(
    captured: dict[str, Any],
    *,
    body_template: str = "phase-2 fresh slot {index} body\n",
):
    """Return a ``dispatch_wave1`` shim used by the resume phase.

    The shim records ``preflight_result.manifest.preflight.workers_requested``
    so the test can assert the redispatch is sized to the remaining
    slot count -- not the original N. It returns one ``WorkerResult``
    per redispatched slot with ``status="success"`` so the downstream
    normalize / reduce stages have something to consume.

    Slot indices on the returned ``WorkerResult`` instances are
    0..K-1 (the dispatcher's local view); the resume orchestrator
    in :func:`commands._run_resume_branch` reindexes them onto the
    original missing slot positions before reduce runs.
    """

    def _shim(
        preflight_result: Any, transport: Any = None, **kwargs: Any
    ) -> list[WorkerResult]:
        K = preflight_result.manifest.preflight.workers_requested  # noqa: N806
        captured.setdefault("calls", []).append(
            {
                "workers_requested": K,
                "job_id": preflight_result.manifest.job_id,
                "transport_kind": preflight_result.manifest.preflight.transport_kind,
                "lens_name": preflight_result.manifest.resolved_lens_entry.name,
            }
        )
        return [
            WorkerResult(
                index=i,
                status="success",
                model_id=f"fresh-model-{i}",
                model_label=f"fresh-model-{i}",
            )
            for i in range(K)
        ]

    return _shim


def _passthrough_normalize_factory(
    output_dir: Path,
    captured: dict[str, Any],
    *,
    body_template: str = "phase-2 normalized slot {index}\n",
):
    """Return a ``normalize_wave2`` shim that writes sidecars + finals.

    The real normalize stage emits the ``*.meta.json`` + ``*.final.md``
    pair for every worker it processes (see
    :func:`normalize._emit_meta`). The resume orchestrator passes
    redispatched workers through this stage so their on-disk sidecars
    land next to phase-1 survivors. The shim mirrors that behavior --
    flushing one pair per worker at the slot index assigned by the
    redispatch reindex -- so the post-resume directory state matches
    what the real normalize would have produced.
    """

    def _shim(
        workers: list[WorkerResult], recipe_name: str, **kwargs: Any
    ) -> list[WorkerResult]:
        captured.setdefault("normalize_calls", []).append([w.index for w in workers])
        for worker in workers:
            _stage_succeeded_slot(
                output_dir,
                slot_index=worker.index,
                body=body_template.format(index=worker.index),
            )
            stem = f"{LENS_NAME}-{worker.index:02d}-{MODEL_SLUG}"
            worker.final_path = str(output_dir / f"{stem}.final.md")
            worker.meta_path = str(output_dir / f"{stem}.meta.json")
        return list(workers)

    return _shim


# ---------------------------------------------------------------------------
# Phase 1 baseline -- the simulated SIGKILL is observable.
# ---------------------------------------------------------------------------


def test_phase1_crash_leaves_manifest_and_partial_sidecars(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """AC: phase 1 crash leaves manifest + survivor sidecars on disk.

    Verifies the kill-injection harness itself: preflight ran to
    completion (``manifest.json`` exists), the survivor slot's
    sidecar + final body landed before the kill, and the missing-slot
    sidecars are absent (so the resume orchestrator will classify
    them as "redispatch me"). No ``merged.md`` exists -- the kill
    fired before Wave 3 had a chance to run.
    """
    spec = _runnable_spec(tmp_path)
    spec_path = _write_spec(tmp_path, spec)
    out_dir = Path(spec["output"]["dir"])

    import superclaude.cli.swarm.dispatch as dispatch_mod

    monkeypatch.setattr(
        dispatch_mod,
        "dispatch_wave1",
        _crashing_dispatch_factory(out_dir, survivors=[0]),
    )

    runner = CliRunner()
    result = runner.invoke(run_cmd, [str(spec_path), "--output", str(out_dir)])

    # The simulated kill propagates: Click's runner records the
    # SystemExit(137) on result.exit_code.
    assert result.exit_code == 137, (
        f"expected SIGKILL-equivalent exit=137; got {result.exit_code}\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}\n"
        f"exception:\n{result.exception!r}"
    )

    # Preflight ran first -- manifest.json must be on disk.
    manifest_path = out_dir / "manifest.json"
    assert manifest_path.is_file(), (
        f"phase 1 must leave a manifest behind for phase 2 to resume "
        f"from; output dir contents: {list(out_dir.iterdir())}"
    )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["job_id"] == JOB_ID
    assert manifest["preflight"]["workers_requested"] == 3
    assert manifest["resolved_lens_entry"]["name"] == LENS_NAME

    # Survivor sidecar + final body landed before the kill.
    survivor_meta = out_dir / f"{LENS_NAME}-00-{MODEL_SLUG}.meta.json"
    survivor_final = out_dir / f"{LENS_NAME}-00-{MODEL_SLUG}.final.md"
    assert survivor_meta.is_file()
    assert survivor_final.is_file()
    assert json.loads(survivor_meta.read_text(encoding="utf-8"))["status"] == "success"

    # Missing slots have no sidecars (the kill cut the loop short).
    for missing_index in (1, 2):
        assert not (
            out_dir / f"{LENS_NAME}-{missing_index:02d}-{MODEL_SLUG}.meta.json"
        ).exists()

    # No merge ran -- merged.md must NOT exist after the kill.
    assert not (out_dir / "merged.md").exists()


# ---------------------------------------------------------------------------
# Canonical kill-then-resume cycle -- the primary T06.08 verification.
# ---------------------------------------------------------------------------


def test_kill_then_resume_reaches_terminal_state_no_duplicate_work(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """AC: kill-then-resume completes with no duplicate work.

    Phase 1 -- start the swarm; preflight emits the manifest; the
    patched dispatch stages slot 0 then raises a SIGKILL-equivalent
    exit. Slots 1 and 2 never write their sidecars.

    Phase 2 -- invoke ``swarm run --resume <job_id> --output <dir>``.
    The resume orchestrator:

        * Loads the manifest from disk (INV-001 source-of-truth).
        * Discovers slot 0 as succeeded (sidecar reports
          ``status: success``); slots 1 and 2 as missing.
        * Re-dispatches exactly 2 slots (NOT 3 -- no duplicate work).
        * Re-runs Wave 2 normalize on the 2 redispatched workers
          (NOT slot 0 -- it stays untouched on disk).
        * Regenerates ``merged.md`` via reduce_wave3(resume=True)
          since amalgamation_mode == "normalize+merge".

    The byte-survival assertion on the slot-0 final body proves the
    "no duplicate work" invariant: a redispatch that touched slot 0
    would either overwrite the body or write to a fresh path that
    misses the kept slot. Neither happens here.
    """
    spec = _runnable_spec(tmp_path)
    spec_path = _write_spec(tmp_path, spec)
    out_dir = Path(spec["output"]["dir"])

    # --- Phase 1: simulated SIGKILL after staging slot 0. ----------------
    import superclaude.cli.swarm.dispatch as dispatch_mod
    import superclaude.cli.swarm.normalize as normalize_mod

    survivor_body = "PHASE-1-SURVIVOR-SLOT-0-BODY-MUST-SURVIVE-RESUME\n"
    monkeypatch.setattr(
        dispatch_mod,
        "dispatch_wave1",
        _crashing_dispatch_factory(
            out_dir,
            survivors=[0],
            survivor_body_template=survivor_body,
        ),
    )

    runner = CliRunner()
    phase1_result = runner.invoke(run_cmd, [str(spec_path), "--output", str(out_dir)])
    assert phase1_result.exit_code == 137, (
        f"phase 1 must surface SIGKILL-equivalent exit; "
        f"got {phase1_result.exit_code}\nstderr:\n{phase1_result.stderr}\n"
        f"exception:\n{phase1_result.exception!r}"
    )

    # Capture the survivor body bytes BEFORE the resume runs so we can
    # prove they survive byte-for-byte (no overwrite by redispatch).
    survivor_final = out_dir / f"{LENS_NAME}-00-{MODEL_SLUG}.final.md"
    pre_resume_survivor_bytes = survivor_final.read_bytes()
    survivor_meta = out_dir / f"{LENS_NAME}-00-{MODEL_SLUG}.meta.json"
    pre_resume_survivor_meta_bytes = survivor_meta.read_bytes()

    # Sanity check the harness: discover_succeeded_slots agrees with
    # what we staged. (Mirrors the resume orchestrator's view.)
    succeeded = discover_succeeded_slots(out_dir, workers_requested=3)
    assert set(succeeded) == {0}

    # --- Phase 2: swap in resume-side shims and invoke --resume. ---------
    captured: dict[str, Any] = {}
    monkeypatch.setattr(
        dispatch_mod,
        "dispatch_wave1",
        _resume_dispatch_factory(captured),
    )
    monkeypatch.setattr(
        normalize_mod,
        "normalize_wave2",
        _passthrough_normalize_factory(out_dir, captured),
    )

    phase2_result = runner.invoke(
        run_cmd,
        ["--resume", JOB_ID, "--output", str(out_dir)],
    )
    assert phase2_result.exit_code == EXIT_OK, (
        f"phase 2 (resume) must reach terminal state; "
        f"got {phase2_result.exit_code}\n"
        f"stdout:\n{phase2_result.stdout}\nstderr:\n{phase2_result.stderr}"
    )

    # --- Verification: skip + redispatch counts ---------------------------
    assert "skipped=1" in phase2_result.stdout, phase2_result.stdout
    assert "redispatched=2" in phase2_result.stdout, phase2_result.stdout
    assert f"job_id={JOB_ID}" in phase2_result.stdout

    # Dispatch was called exactly once during resume, with 2 slots
    # (NOT 3 -- the original N).
    assert len(captured["calls"]) == 1
    assert captured["calls"][0]["workers_requested"] == 2
    assert captured["calls"][0]["job_id"] == JOB_ID
    # The manifest's lens snapshot (INV-001) flowed through verbatim.
    assert captured["calls"][0]["lens_name"] == LENS_NAME
    # The manifest carries the original transport kind (stub).
    assert captured["calls"][0]["transport_kind"] == "stub"

    # Normalize ran once on the redispatched workers only (NOT slot 0).
    assert "normalize_calls" in captured
    assert len(captured["normalize_calls"]) == 1
    redispatched_indices = sorted(captured["normalize_calls"][0])
    assert redispatched_indices == [1, 2], (
        f"normalize must process slots 1+2 only; got {redispatched_indices}"
    )

    # --- Verification: slot 0 survived byte-for-byte (no dup work) -------
    assert survivor_final.read_bytes() == pre_resume_survivor_bytes, (
        "slot 0's final body was overwritten by the resume -- "
        "duplicate work invariant violated"
    )
    assert survivor_meta.read_bytes() == pre_resume_survivor_meta_bytes, (
        "slot 0's meta sidecar was rewritten by the resume -- "
        "the resume orchestrator must leave succeeded sidecars untouched"
    )

    # --- Verification: missing slots now have sidecars + finals ----------
    for missing_index in (1, 2):
        meta = out_dir / f"{LENS_NAME}-{missing_index:02d}-{MODEL_SLUG}.meta.json"
        final = out_dir / f"{LENS_NAME}-{missing_index:02d}-{MODEL_SLUG}.final.md"
        assert meta.is_file(), f"slot {missing_index} sidecar missing post-resume"
        assert final.is_file(), f"slot {missing_index} final missing post-resume"
        payload = json.loads(meta.read_text(encoding="utf-8"))
        assert payload["status"] == "success"

    # --- Verification: every slot present exactly once -------------------
    sidecar_indices: list[int] = []
    for meta_file in sorted(out_dir.glob("*.meta.json")):
        # Filename shape: bare-review-NN-stub-model.meta.json
        stem = meta_file.stem.removesuffix(".meta")
        # Parse "bare-review-NN-stub-model" -> NN
        parts = stem.split("-")
        # Layout: ["bare", "review", "NN", "stub", "model"]
        nn_segment = parts[2]
        sidecar_indices.append(int(nn_segment))
    assert sidecar_indices == [0, 1, 2], (
        f"every slot must appear exactly once; got {sidecar_indices}"
    )

    # --- Verification: merge regenerated when applicable ------------------
    merged_path = out_dir / "merged.md"
    assert merged_path.is_file(), (
        "merged.md must be regenerated under amalgamation_mode "
        "== 'normalize+merge' once M >= floor"
    )


# ---------------------------------------------------------------------------
# Variant: every slot crashed -- no skip, full redispatch.
# ---------------------------------------------------------------------------


def test_kill_before_any_sidecar_resumes_with_full_redispatch(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """AC: kill before any sidecar -> full redispatch on resume.

    Compose the worst-case crash: preflight ran but the kill fired
    before ANY worker flushed its sidecar. Resume must redispatch the
    full original N (no skip), and ``merged.md`` must land afresh.
    """
    spec = _runnable_spec(tmp_path)
    spec_path = _write_spec(tmp_path, spec)
    out_dir = Path(spec["output"]["dir"])

    import superclaude.cli.swarm.dispatch as dispatch_mod
    import superclaude.cli.swarm.normalize as normalize_mod

    monkeypatch.setattr(
        dispatch_mod,
        "dispatch_wave1",
        _crashing_dispatch_factory(out_dir, survivors=[]),
    )

    runner = CliRunner()
    phase1 = runner.invoke(run_cmd, [str(spec_path), "--output", str(out_dir)])
    assert phase1.exit_code == 137, (
        f"phase 1 must surface SIGKILL-equivalent exit; "
        f"got {phase1.exit_code}\nstderr:\n{phase1.stderr}\n"
        f"exception:\n{phase1.exception!r}"
    )

    # No sidecars on disk -- resume must redispatch every slot.
    assert discover_succeeded_slots(out_dir, workers_requested=3) == {}

    captured: dict[str, Any] = {}
    monkeypatch.setattr(
        dispatch_mod,
        "dispatch_wave1",
        _resume_dispatch_factory(captured),
    )
    monkeypatch.setattr(
        normalize_mod,
        "normalize_wave2",
        _passthrough_normalize_factory(out_dir, captured),
    )

    phase2 = runner.invoke(
        run_cmd,
        ["--resume", JOB_ID, "--output", str(out_dir)],
    )
    assert phase2.exit_code == EXIT_OK, phase2.stderr
    assert "skipped=0" in phase2.stdout
    assert "redispatched=3" in phase2.stdout
    assert captured["calls"][0]["workers_requested"] == 3

    # Merge regenerated post-resume even when all slots came from the
    # redispatch -- the resume hook fires unconditionally for
    # normalize+merge mode (INV-010 / T06.02).
    assert (out_dir / "merged.md").is_file()


# ---------------------------------------------------------------------------
# Variant: stale merged.md from a partial pre-kill merge is replaced.
# ---------------------------------------------------------------------------


def test_kill_after_stale_merge_resume_regenerates_merge(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """AC: stale ``merged.md`` from before the kill is replaced on resume.

    INV-010 / T06.02 guarantees that a pre-existing ``merged.md`` does
    not survive a resume when ``amalgamation_mode == "normalize+merge"``.
    Compose the scenario by hand-staging a stale ``merged.md`` next to
    the phase-1 manifest + slot-0 sidecar, then assert the resume
    overwrites it with fresh bytes that mention the post-resume
    workers.
    """
    spec = _runnable_spec(tmp_path)
    spec_path = _write_spec(tmp_path, spec)
    out_dir = Path(spec["output"]["dir"])

    import superclaude.cli.swarm.dispatch as dispatch_mod
    import superclaude.cli.swarm.normalize as normalize_mod

    monkeypatch.setattr(
        dispatch_mod,
        "dispatch_wave1",
        _crashing_dispatch_factory(out_dir, survivors=[0]),
    )

    runner = CliRunner()
    phase1 = runner.invoke(run_cmd, [str(spec_path), "--output", str(out_dir)])
    assert phase1.exit_code == 137, (
        f"phase 1 must surface SIGKILL-equivalent exit; "
        f"got {phase1.exit_code}\nstderr:\n{phase1.stderr}\n"
        f"exception:\n{phase1.exception!r}"
    )

    # Hand-stage a stale merged.md as if a prior partial merge had
    # written it before the kill fired. The post-resume contents MUST
    # NOT contain this body.
    stale_merged = out_dir / "merged.md"
    stale_bytes = b"STALE-MERGE-FROM-PRE-KILL-PARTIAL-WRITE\n"
    stale_merged.write_bytes(stale_bytes)
    assert stale_merged.read_bytes() == stale_bytes

    captured: dict[str, Any] = {}
    monkeypatch.setattr(
        dispatch_mod,
        "dispatch_wave1",
        _resume_dispatch_factory(captured),
    )
    monkeypatch.setattr(
        normalize_mod,
        "normalize_wave2",
        _passthrough_normalize_factory(out_dir, captured),
    )

    phase2 = runner.invoke(
        run_cmd,
        ["--resume", JOB_ID, "--output", str(out_dir)],
    )
    assert phase2.exit_code == EXIT_OK, phase2.stderr

    # Stale bytes are gone; merged.md exists with a fresh body.
    assert stale_merged.exists()
    post_resume_bytes = stale_merged.read_bytes()
    assert b"STALE-MERGE-FROM-PRE-KILL-PARTIAL-WRITE" not in post_resume_bytes, (
        "stale merged.md must NOT survive resume under normalize+merge"
    )
    assert len(post_resume_bytes) > 0, "merged.md regenerated to empty body"


# ---------------------------------------------------------------------------
# Variant: two-slot survivor / one-slot redispatch.
# ---------------------------------------------------------------------------


def test_kill_with_two_survivors_resumes_single_redispatch(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """AC: 2 survivors + 1 missing -> redispatch sized to 1.

    Sanity-checks the skip/redispatch arithmetic for the mid-range
    case (most slots succeeded; only one was lost to the kill). The
    arithmetic ``skipped + redispatched == workers_requested`` is the
    NFR-005 invariant.
    """
    spec = _runnable_spec(tmp_path)
    spec_path = _write_spec(tmp_path, spec)
    out_dir = Path(spec["output"]["dir"])

    import superclaude.cli.swarm.dispatch as dispatch_mod
    import superclaude.cli.swarm.normalize as normalize_mod

    monkeypatch.setattr(
        dispatch_mod,
        "dispatch_wave1",
        _crashing_dispatch_factory(out_dir, survivors=[0, 2]),
    )

    runner = CliRunner()
    phase1 = runner.invoke(run_cmd, [str(spec_path), "--output", str(out_dir)])
    assert phase1.exit_code == 137, (
        f"phase 1 must surface SIGKILL-equivalent exit; "
        f"got {phase1.exit_code}\nstderr:\n{phase1.stderr}\n"
        f"exception:\n{phase1.exception!r}"
    )

    # Sanity: discovery sees the two survivors.
    survivors = discover_succeeded_slots(out_dir, workers_requested=3)
    assert set(survivors) == {0, 2}

    captured: dict[str, Any] = {}
    monkeypatch.setattr(
        dispatch_mod,
        "dispatch_wave1",
        _resume_dispatch_factory(captured),
    )
    monkeypatch.setattr(
        normalize_mod,
        "normalize_wave2",
        _passthrough_normalize_factory(out_dir, captured),
    )

    phase2 = runner.invoke(
        run_cmd,
        ["--resume", JOB_ID, "--output", str(out_dir)],
    )
    assert phase2.exit_code == EXIT_OK, phase2.stderr
    assert "skipped=2" in phase2.stdout
    assert "redispatched=1" in phase2.stdout

    # Redispatch sized to 1; normalize processed only slot 1.
    assert captured["calls"][0]["workers_requested"] == 1
    assert captured["normalize_calls"] == [[1]]

    # Final sidecar coverage matches the original N.
    final_indices = sorted(
        int(p.stem.split("-")[2]) for p in out_dir.glob("*.meta.json")
    )
    assert final_indices == [0, 1, 2]
