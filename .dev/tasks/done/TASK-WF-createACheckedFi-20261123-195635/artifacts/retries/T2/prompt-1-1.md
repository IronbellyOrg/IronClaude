260a67c768f6e745b806c67988f60276e4abefa4
Review one task for spec compliance.

Task brief: Wire resumed marker publication with skipped and redispatched tests

Depends on: Task 1

Read the diagnostic report's resume evidence and scope limits, `_run_resume_branch` and `discover_succeeded_slots` in `src/superclaude/cli/swarm/commands.py`, `resume_mode` in `src/superclaude/cli/swarm/preflight.py`, and the existing skipped-worker and redispatch scenarios in `tests/swarm/test_resume_crash_recovery.py`. Extend that test module with completion-marker assertions before editing the resume continuation. Use an independent manifest/sidecar fixture with no pre-existing marker so Task 1's new foreground marker cannot make a missing resume publication appear to pass. Record the resume regression's pre-change failure in `./artifacts/resume-before.txt`.

In `_run_resume_branch`, retain the returned `reduce_wave3(..., resume=True)` contract, retain the current terminal-state write, then call `emit_done_sentinel` with the actual result status and resolved persisted contract path when `rehydrated_spec.runtime.on_completion.write_done_sentinel` is enabled. Follow the foreground ordering without changing worker classification, redispatch mapping, manifest rehydration, merge regeneration or error exits.


Acceptance criteria:
T2.AC1: The new all-workers-skipped resume regression fails for a missing marker before this continuation changes and passes afterward; save commands, exit codes and outputs in `./artifacts/resume-before.txt` and `./artifacts/resume-after.txt`. Foreground publication must not satisfy the resume assertion accidentally.
T2.AC2: Both all-workers-already-succeeded and remaining-workers-redispatched CLI paths write the existing three-field marker after the contract and terminal state. The marker's status and absolute contract path match the persisted result. Succeeded sidecars/bodies are preserved, dispatch runs only for remaining indices, no duplicate slot outputs appear, and `merged.md` still regenerates.
T2.AC3: Parameterized real-reducer CLI tests cover success, partial and failed terminal results, including redispatched degraded outcomes. Explicitly supplying a disabled effective policy through a controlled `resume_mode` return object suppresses publication while preserving terminal state/contract; the normal manifest-based path uses its present default-on policy. No test or documentation claims arbitrary original opt-out recovery across resume.
T2.AC4: Delegating writer wrappers prove contract persistence precedes terminal-state persistence and marker emission follows it. Contract/reducer failure and terminal-state-write failure leave no new marker in clean fixtures; missing/malformed/mismatched manifests likewise do not manufacture completion.
T2.AC5: Capture a separate actual UV-launched `superclaude swarm run --resume ... --transport stub --output ...` with isolated HOME and output artifacts under `./artifacts/resume-cli/`. Seed the fixture independently or remove only this task's known prior marker before resume, recording that setup, so the positive witness demonstrates new resume publication. Save argv, provenance, stdout/stderr, exit code, skip/redispatch counts and parsed marker/state/contract comparisons in `./artifacts/resume-cli-check.txt`, paired with the diagnostic resume negative evidence.
T2.AC6: Run `uv run pytest tests/swarm/test_resume_crash_recovery.py tests/swarm/test_resume_regenerates_merge.py tests/swarm/test_resume_uses_manifest_lens.py tests/swarm/test_crash_recovery_e2e.py tests/swarm/test_force_relens.py`; retain results in `./artifacts/resume-after.txt`. `run_cmd`'s resume dispatch and the manifest lens snapshot/force-relens behavior remain compatible without changes outside this omission fix.
Global constraints: - Only issue 540 is covered. The diagnostic package `.dev/troubleshoot/bug-issue540-completion-marker-20261123191058/` is immutable context; read `REPORT.md`, `evidence-validation.md`, `tier1-observation.md` and `contract-ledger.md` there when executing tasks. Its historical absolute paths refer to the old checkout and must not be used as live edit destinations.
- The user authorized this planning step after the recorded pre-fix planning ambiguity was explained. That does not clear the report's blocked repair closure or authorize implementation. Execute this plan only after a separate implementation request; do not repeat diagnosis merely to obtain a plan. Keep the original report unchanged.
- Preserve the recorded negative CLI witness from `artifacts/negative-witness.txt` in that diagnostic package. Successful repair requires new positive public-CLI evidence paired with it; neither the earlier diagnostic review PASS nor this plan certifies a repair. All new evidence belongs under this package's `./artifacts/`, using fresh isolated job output roots and an isolated HOME. Never overwrite the old foreground/resume evidence.
- Production edits are limited to the two completion continuations in `src/superclaude/cli/swarm/commands.py`. Reuse `reduce.emit_done_sentinel`, `ResultContract.status`, existing filename constants and atomic writers. Do not create a new marker schema, duplicate contract emission, change CLI exit/stdout contracts, or implement `print_contract_to_stdout`.
- Respect the effective foreground or rehydrated resume policy. Arbitrary original runtime override recovery on resume is incomplete and is not part of this fix: do not change `Manifest`, `preflight.resume_mode`, caller/lens metadata recovery, or persistence formats to address it. A disabled effective resume policy can be tested through a controlled rehydration seam, but must not be advertised as original-policy persistence.
- Detached parents only launch; children own completion. Preserve `_emit_killed_done_sentinel`, `kill_cmd`, the killed marker's empty contract path, existing writer atomicity and existing resume worker-skip/merge semantics. No new cleanup, stale-marker lifecycle protocol, or adjacent behavior change is included.
- Issues 501, 555 and 568, their task packages and shared diagnostic counters are outside scope. Do not import, edit or stage their files. Stage only this newly created task package as required by project policy; never stage generated `.claude/` mirrors. No commit, push, GitHub write or automatic implementation handoff is authorized.
- All future Python and test execution uses UV. Use stub transports, no live model calls or credentials; read any required credentials from the environment without logging values. A skipped or unavailable live detached check is not a pass and cannot establish complete detached repair coverage.
Start sha: 260a67c768f6e745b806c67988f60276e4abefa4
Diff against the start snapshot: diff --git a/src/superclaude/cli/swarm/commands.py b/src/superclaude/cli/swarm/commands.py
index 1d88cbe0f..6aadf676f 100644
--- a/src/superclaude/cli/swarm/commands.py
+++ b/src/superclaude/cli/swarm/commands.py
@@ -2590,7 +2590,7 @@ def _run_resume_branch(
         # via IMM-5 based on M/N.
 
     # ----- Wave 3 reduce with resume=True (merge regen per INV-010) ---------
-    reduce_wave3(
+    result_contract = reduce_wave3(
         combined,
         mode=amalgamation_mode,
         output_dir=output_path,
@@ -2605,6 +2605,14 @@ def _run_resume_branch(
     # the ``--output`` root via the same atomic writer the inline path uses).
     _write_swarm_state(output_path, "terminal", manifest_obj.job_id)
 
+    if rehydrated_spec.runtime.on_completion.write_done_sentinel:
+        from superclaude.cli.swarm.reduce import emit_done_sentinel
+
+        emit_done_sentinel(
+            result_contract.status,
+            (output_path / RESULT_CONTRACT_FILENAME).resolve(),
+        )
+
     click.echo(
         f"swarm run --resume: job_id={manifest_obj.job_id} "
         f"workers={workers_requested} "
diff --git a/tests/swarm/test_resume_crash_recovery.py b/tests/swarm/test_resume_crash_recovery.py
index f33a4e6e7..2bce1e043 100644
--- a/tests/swarm/test_resume_crash_recovery.py
+++ b/tests/swarm/test_resume_crash_recovery.py
@@ -387,6 +387,7 @@ def test_resume_skips_succeeded_workers_and_redispatches_remaining(
     assert "skipped=1" in result.stdout
     assert "redispatched=2" in result.stdout
     assert JOB_ID in result.stdout
+    assert json.loads((out_dir / "done.json").read_text())["terminal_status"] == "success"
 
 
 def test_resume_all_workers_succeeded_skips_redispatch(
@@ -422,6 +423,7 @@ def test_resume_all_workers_succeeded_skips_redispatch(
     assert dispatch_calls == []
     assert "skipped=3" in result.stdout
     assert "redispatched=0" in result.stdout
+    assert json.loads((out_dir / "done.json").read_text())["terminal_status"] == "success"
 
 
 def test_resume_regenerates_merged_md(
@@ -538,3 +540,134 @@ def test_discover_succeeded_slots_exported() -> None:
 
     assert "discover_succeeded_slots" in commands_mod.__all__
     assert callable(commands_mod.discover_succeeded_slots)
+
+
+@pytest.mark.parametrize("enabled", [False, True])
+@pytest.mark.parametrize("successes", [0, 2, 3])
+@pytest.mark.parametrize("skip_all", [False, True])
+def test_resume_completion_policy_status_and_order(
+    tmp_path, monkeypatch, enabled, successes, skip_all
+):
+    """Independent manifests prevent a fresh-run marker from masking missing resume wiring."""
+    import yaml
+
+    import superclaude.cli.swarm.commands as commands
+    import superclaude.cli.swarm.dispatch as dispatch
+    import superclaude.cli.swarm.normalize as normalize
+    import superclaude.cli.swarm.preflight as preflight
+    import superclaude.cli.swarm.reduce as reducer
+
+    out = tmp_path / "out"
+    _write_manifest(out, workers_requested=3)
+    saved = []
+    if skip_all:
+        for index in range(3):
+            meta, final = _write_succeeded_sidecar(out, slot_index=index)
+            saved.extend([(meta, meta.read_bytes()), (final, final.read_bytes())])
+    assert not (out / "done.json").exists()
+    real_rehydrate = preflight.resume_mode
+
+    def rehydrate(*a, **kw):
+        spec = real_rehydrate(*a, **kw)
+        spec.runtime.on_completion.write_done_sentinel = enabled
+        return spec
+
+    monkeypatch.setattr(preflight, "resume_mode", rehydrate)
+    calls = []
+
+    def workers(pf, **kwargs):
+        calls.append(pf.manifest.preflight.workers_requested)
+        return [
+            WorkerResult(index=i, status="success" if i < successes else "timeout")
+            for i in range(3)
+        ]
+
+    monkeypatch.setattr(dispatch, "dispatch_wave1", workers)
+    monkeypatch.setattr(normalize, "normalize_wave2", lambda workers, **kwargs: workers)
+    events = []
+    real_state, real_marker = commands._write_swarm_state, reducer.emit_done_sentinel
+
+    def state(root, value, job_id):
+        assert (out / "return-contract.yaml").is_file()
+        assert not (out / "done.json").exists()
+        events.append("terminal")
+        return real_state(root, value, job_id)
+
+    def marker(status, contract_path):
+        assert (
+            json.loads((out / ".swarm-state.json").read_text())["state"] == "terminal"
+        )
+        assert yaml.safe_load(Path(contract_path).read_text())["status"] == status
+        events.append("marker")
+        return real_marker(status, contract_path)
+
+    monkeypatch.setattr(commands, "_write_swarm_state", state)
+    monkeypatch.setattr(reducer, "emit_done_sentinel", marker)
+    result = CliRunner().invoke(run_cmd, ["--resume", JOB_ID, "--output", str(out)])
+    assert result.exit_code == EXIT_OK, result.output
+    assert calls == ([] if skip_all else [3])
+    assert events == (["terminal", "marker"] if enabled else ["terminal"])
+    expected = (
+        "success"
+        if skip_all or successes == 3
+        else "partial"
+        if successes == 2
+        else "failed"
+    )
+    assert (
+        yaml.safe_load((out / "return-contract.yaml").read_text())["status"] == expected
+    )
+    assert (out / "done.json").exists() is enabled
+    if enabled:
+        assert json.loads((out / "done.json").read_text()) == {
+            "atomic_write": True,
+            "terminal_status": expected,
+            "contract_path": str((out / "return-contract.yaml").resolve()),
+        }
+    assert (
+        len(
+            {
+                w["index"]
+                for w in yaml.safe_load((out / "return-contract.yaml").read_text())[
+                    "output_files"
+                ]
+            }
+        )
+        == 3
+    )
+    for path, original in saved:
+        assert path.read_bytes() == original
+
+
+@pytest.mark.parametrize(
+    "failure", ["reduce", "contract", "terminal", "missing", "malformed", "mismatch"]
+)
+def test_resume_no_marker_on_error(tmp_path, monkeypatch, failure):
+    import superclaude.cli.swarm.commands as commands
+    import superclaude.cli.swarm.reduce as reducer
+
+    out = tmp_path / "out"
+    manifest = _write_manifest(out, workers_requested=3)
+    for i in range(3):
+        _write_succeeded_sidecar(out, slot_index=i)
+
+    def fail(*a, **kw):
+        raise OSError("injected resume persistence failure")
+
+    if failure == "reduce":
+        monkeypatch.setattr(reducer, "reduce_wave3", fail)
+    elif failure == "contract":
+        monkeypatch.setattr(reducer, "emit_contract", fail)
+    elif failure == "terminal":
+        monkeypatch.setattr(commands, "_write_swarm_state", fail)
+    elif failure == "missing":
+        manifest.unlink()
+    elif failure == "malformed":
+        manifest.write_text("not JSON")
+    else:
+        data = json.loads(manifest.read_text())
+        data["job_id"] = "different-job"
+        manifest.write_text(json.dumps(data))
+    result = CliRunner().invoke(run_cmd, ["--resume", JOB_ID, "--output", str(out)])
+    assert result.exit_code != EXIT_OK
+    assert not (out / "done.json").exists()
Codegraph context
index_state: fresh
checked_at: 2026-11-23T20:14:00Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-540-completion-marker
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-540-completion-marker
call codegraph only when index_state: fresh, never to widen scope
Dependents outside this diff: CLI registration; resume continuation; detached child; unchanged writer and kill callers; existing TUI/input/status tests. Source call sites were Read in implementation context. These are context, not extra requirements.

Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
