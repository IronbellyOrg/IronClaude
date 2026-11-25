8b15d2ff88ae732825660a101866fa453832b953
Review one task for spec compliance.

Task brief: Wire foreground marker publication with reproducing CLI tests

Read the diagnostic report's Proposed Fix and repair acceptance, `run_cmd`'s post-dispatch continuation in `src/superclaude/cli/swarm/commands.py`, `reduce_wave3` and `emit_done_sentinel` in `src/superclaude/cli/swarm/reduce.py`, and `OnCompletion` in `src/superclaude/cli/swarm/models.py`. In `tests/swarm/test_e2e_user_guide.py`, replace the existing `test_quickstart_does_not_emit_done_sentinel` limitation assertion with a positive default-on regression, including a name/docstring that states the new behavior. Extend `tests/swarm/test_commands_run.py` using its `_runnable_spec` and `_write_spec` helpers for spec-file/stdin policy and boundary cases. Run the newly positive tests before the source change and save their expected missing-marker failures to `./artifacts/foreground-before.txt`.

In `run_cmd`, retain the contract returned by the existing reduction, persist terminal state through `_write_swarm_state`, then publish with the existing `emit_done_sentinel` only when reduction actually produced the persisted contract and `inline_job.runtime.on_completion.write_done_sentinel` enables it. Use the returned status and an absolute resolved path to that output directory's existing `return-contract.yaml`; do not move publication into the reducer or the generic state writer. Keep no-reduction branches explicit so there is no unbound contract or marker pointing at a missing result. Add no abstraction unless the existing code requires one.


Acceptance criteria:
T1.AC1: The new foreground marker-presence test fails on the unmodified continuation for the reported omission, then passes after this change. Save both command lines, exit codes and complete focused pytest output under `./artifacts/foreground-before.txt` and `./artifacts/foreground-after.txt`; an expected pre-fix failure is evidence, not a passing repaired test.
T1.AC2: Through the registered `swarm_group` CLI, a stub `--lens bare-review --target ... --output ...` run produces a parseable `done.json` with exactly `atomic_write`, `terminal_status` and `contract_path`; `atomic_write` is true, status equals the actual YAML contract status, and the absolute contract path resolves to the persisted contract in the same output root. Default-on spec-file and stdin runs behave equivalently, including a relative output-path case.
T1.AC3: Explicit foreground `write_done_sentinel=false` leaves no marker in a fresh output root while still producing the contract and terminal state. Controlled success/partial/failed worker outcomes exercise the real CLI continuation and reducer; each enabled terminal marker mirrors the persisted result rather than the CLI's exit-0 convention. Do not replace the reducer or writer with mocks for this status check.
T1.AC4: Ordering tests wrap and delegate to the real writers: at terminal-state publication the contract already exists and the new marker does not; at marker publication the contract is readable and the persisted state is terminal. A reducer/contract-write exception or terminal-state-write exception must not produce a new completion marker. Early preflight/transport errors, no-output execution and a no-normalization/no-reduction path must not acquire a fabricated marker.
T1.AC5: Capture one actual UV-launched `superclaude swarm run` with stub transport, isolated HOME and a fresh output directory under `./artifacts/foreground-cli/`; save argv, checkout/import provenance, stdout, stderr, exit code and parsed state/contract/marker comparisons under `./artifacts/foreground-cli-check.txt`. Pair this positive witness with the immutable diagnostic negative witness. Do not substitute a direct helper call or pytest success alone for the public-entrypoint capture.
T1.AC6: Run `uv run pytest tests/swarm/test_commands_run.py tests/swarm/test_e2e_user_guide.py tests/swarm/test_swarm_run_inputs.py tests/swarm/test_run_tui_integration.py tests/swarm/test_done_sentinel.py tests/swarm/test_imm6_atomic_write.py`; record results in `./artifacts/foreground-after.txt`. Registration in `src/superclaude/cli/swarm/__init__.py`, existing stdout signatures, TUI continuation, writer atomicity and kill's separate publication path stay compatible. Repair only failures caused by this scoped change; report unrelated failures without changing their code.
Global constraints: - Only issue 540 is covered. The diagnostic package `.dev/troubleshoot/bug-issue540-completion-marker-20261123191058/` is immutable context; read `REPORT.md`, `evidence-validation.md`, `tier1-observation.md` and `contract-ledger.md` there when executing tasks. Its historical absolute paths refer to the old checkout and must not be used as live edit destinations.
- The user authorized this planning step after the recorded pre-fix planning ambiguity was explained. That does not clear the report's blocked repair closure or authorize implementation. Execute this plan only after a separate implementation request; do not repeat diagnosis merely to obtain a plan. Keep the original report unchanged.
- Preserve the recorded negative CLI witness from `artifacts/negative-witness.txt` in that diagnostic package. Successful repair requires new positive public-CLI evidence paired with it; neither the earlier diagnostic review PASS nor this plan certifies a repair. All new evidence belongs under this package's `./artifacts/`, using fresh isolated job output roots and an isolated HOME. Never overwrite the old foreground/resume evidence.
- Production edits are limited to the two completion continuations in `src/superclaude/cli/swarm/commands.py`. Reuse `reduce.emit_done_sentinel`, `ResultContract.status`, existing filename constants and atomic writers. Do not create a new marker schema, duplicate contract emission, change CLI exit/stdout contracts, or implement `print_contract_to_stdout`.
- Respect the effective foreground or rehydrated resume policy. Arbitrary original runtime override recovery on resume is incomplete and is not part of this fix: do not change `Manifest`, `preflight.resume_mode`, caller/lens metadata recovery, or persistence formats to address it. A disabled effective resume policy can be tested through a controlled rehydration seam, but must not be advertised as original-policy persistence.
- Detached parents only launch; children own completion. Preserve `_emit_killed_done_sentinel`, `kill_cmd`, the killed marker's empty contract path, existing writer atomicity and existing resume worker-skip/merge semantics. No new cleanup, stale-marker lifecycle protocol, or adjacent behavior change is included.
- Issues 501, 555 and 568, their task packages and shared diagnostic counters are outside scope. Do not import, edit or stage their files. Stage only this newly created task package as required by project policy; never stage generated `.claude/` mirrors. No commit, push, GitHub write or automatic implementation handoff is authorized.
- All future Python and test execution uses UV. Use stub transports, no live model calls or credentials; read any required credentials from the environment without logging values. A skipped or unavailable live detached check is not a pass and cannot establish complete detached repair coverage.
Start sha: 8b15d2ff88ae732825660a101866fa453832b953
Diff against the start snapshot: diff --git a/src/superclaude/cli/swarm/commands.py b/src/superclaude/cli/swarm/commands.py
index 8577805b1..1d88cbe0f 100644
--- a/src/superclaude/cli/swarm/commands.py
+++ b/src/superclaude/cli/swarm/commands.py
@@ -2092,6 +2092,7 @@ def run_cmd(
     # and the ``--suspect-source`` recommended-next-command so the bare-review
     # return contract is complete (closing the R3 §1.4 inline-vs-resume asymmetry).
     recipe_name = inline_job.normalization.recipe
+    result_contract = None
     if state_output_dir is not None and recipe_name:
         from superclaude.cli.swarm.normalize import normalize_wave2
         from superclaude.cli.swarm.reduce import reduce_wave3
@@ -2142,7 +2143,7 @@ def run_cmd(
             "compare_files",
             ",".join(["<existing-review>", *succeeded_final_paths]),
         )
-        reduce_wave3(
+        result_contract = reduce_wave3(
             normalized_workers,
             mode=inline_job.amalgamation_mode,
             output_dir=state_output_dir,
@@ -2168,6 +2169,20 @@ def run_cmd(
             preflight_result.manifest.job_id,
         )
 
+    # Publish only after both the result and terminal state are durable. The
+    # no-reduction path has no contract and must not manufacture completion.
+    if (
+        result_contract is not None
+        and state_output_dir is not None
+        and inline_job.runtime.on_completion.write_done_sentinel
+    ):
+        from superclaude.cli.swarm.reduce import emit_done_sentinel
+
+        emit_done_sentinel(
+            result_contract.status,
+            (state_output_dir / RESULT_CONTRACT_FILENAME).resolve(),
+        )
+
     # Single grep-friendly success line -- preserved verbatim so the documented
     # stdout signature (and the e2e tests pinning it) stays stable.
     click.echo(
diff --git a/tests/swarm/test_commands_run.py b/tests/swarm/test_commands_run.py
index 70bf51ef2..217506fcc 100644
--- a/tests/swarm/test_commands_run.py
+++ b/tests/swarm/test_commands_run.py
@@ -566,3 +566,123 @@ def test_run_cmd_stub_transport_dispatches_workers_not_noop(
     assert log_body.count("worker_done") == 3, (
         f"expected exactly 3 worker_done events (one per worker slot); log:\n{log_body}"
     )
+
+
+@pytest.mark.parametrize("stdin", [False, True])
+@pytest.mark.parametrize("enabled", [False, True])
+def test_completion_policy_input_modes(tmp_path, monkeypatch, stdin, enabled):
+    """Spec/stdin honor opt-out, including relative output roots."""
+    import yaml
+
+    spec = _runnable_spec(tmp_path)
+    spec["runtime"]["on_completion"]["write_done_sentinel"] = enabled
+    spec["output"]["dir"] = "out"
+    path = _write_spec(tmp_path, spec)
+    monkeypatch.chdir(tmp_path)
+    args = ["--stdin"] if stdin else [str(path)]
+    result = CliRunner().invoke(
+        swarm_group, ["run", *args, "--output", "out"],
+        input=json.dumps(spec) if stdin else None,
+    )
+    assert result.exit_code == EXIT_OK, result.output
+    out = tmp_path / "out"
+    assert json.loads((out / ".swarm-state.json").read_text())["state"] == "terminal"
+    contract = yaml.safe_load((out / "return-contract.yaml").read_text())
+    assert (out / "done.json").exists() is enabled
+    if enabled:
+        assert json.loads((out / "done.json").read_text()) == {
+            "atomic_write": True, "terminal_status": contract["status"],
+            "contract_path": str(out / "return-contract.yaml"),
+        }
+
+
+@pytest.mark.parametrize("successes,expected", [(3, "success"), (2, "partial"), (0, "failed")])
+def test_completion_uses_reduced_status_and_order(tmp_path, monkeypatch, successes, expected):
+    """Real reduction and writer publish actual verdict only after terminal persistence."""
+    import yaml
+    import superclaude.cli.swarm.commands as commands
+    import superclaude.cli.swarm.dispatch as dispatch
+    import superclaude.cli.swarm.reduce as reducer
+    spec = _runnable_spec(tmp_path)
+    spec["amalgamation_mode"] = "normalize"
+    out = tmp_path / "out"
+    real_dispatch = dispatch.dispatch_wave1
+
+    def workers(*args, **kwargs):
+        results = real_dispatch(*args, **kwargs)
+        for worker in results[successes:]:
+            worker.status = "timeout"
+        return results
+
+    monkeypatch.setattr(dispatch, "dispatch_wave1", workers)
+    events = []
+    real_state, real_marker = commands._write_swarm_state, reducer.emit_done_sentinel
+
+    def state(root, value, job_id):
+        if value == "terminal":
+            assert (root / "return-contract.yaml").is_file()
+            assert not (root / "done.json").exists()
+            events.append("terminal")
+        return real_state(root, value, job_id)
+
+    def marker(status, contract_path):
+        assert json.loads((out / ".swarm-state.json").read_text())["state"] == "terminal"
+        assert yaml.safe_load(Path(contract_path).read_text())["status"] == status
+        events.append("marker")
+        return real_marker(status, contract_path)
+
+    monkeypatch.setattr(commands, "_write_swarm_state", state)
+    monkeypatch.setattr(reducer, "emit_done_sentinel", marker)
+    result = CliRunner().invoke(swarm_group, ["run", str(_write_spec(tmp_path, spec)), "--output", str(out)])
+    assert result.exit_code == EXIT_OK, result.output
+    assert json.loads((out / "done.json").read_text())["terminal_status"] == expected
+    assert events == ["terminal", "marker"]
+
+
+@pytest.mark.parametrize("failure", ["reduce", "contract", "terminal"])
+def test_completion_not_published_when_persistence_fails(tmp_path, monkeypatch, failure):
+    import superclaude.cli.swarm.commands as commands
+    import superclaude.cli.swarm.reduce as reducer
+
+    spec = _runnable_spec(tmp_path)
+    out = tmp_path / "out"
+    real_state = commands._write_swarm_state
+
+    def fail(*a, **kw):
+        raise OSError("injected persistence failure")
+
+    if failure == "reduce":
+        monkeypatch.setattr(reducer, "reduce_wave3", fail)
+    elif failure == "contract":
+        monkeypatch.setattr(reducer, "emit_contract", fail)
+    else:
+        def state(root, value, job_id):
+            if value == "terminal":
+                fail()
+            return real_state(root, value, job_id)
+        monkeypatch.setattr(commands, "_write_swarm_state", state)
+    result = CliRunner().invoke(swarm_group, ["run", str(_write_spec(tmp_path, spec)), "--output", str(out)])
+    assert result.exit_code != EXIT_OK
+    assert isinstance(result.exception, OSError)
+    assert not (out / "done.json").exists()
+
+
+@pytest.mark.parametrize("branch", ["no-output", "no-recipe", "preflight", "transport"])
+def test_completion_not_fabricated_without_terminal_reduction(tmp_path, monkeypatch, branch):
+    import superclaude.cli.swarm.commands as commands
+
+    spec = _runnable_spec(tmp_path)
+    out = tmp_path / "out"
+    args = [] if branch == "no-output" else ["--output", str(out)]
+    if branch == "no-recipe":
+        spec["normalization"]["recipe"] = ""
+    elif branch == "preflight":
+        Path(spec["target"]["path"]).write_text("tiny")
+    elif branch == "transport":
+        from superclaude.cli.swarm.transports.openai_compat import TransportEnvError
+        def fail(*a, **kw):
+            raise TransportEnvError("injected missing environment")
+        monkeypatch.setattr(commands, "_resolve_run_transport_factory", fail)
+    result = CliRunner().invoke(swarm_group, ["run", str(_write_spec(tmp_path, spec)), *args])
+    assert result.exit_code == (EXIT_INVALID if branch in {"preflight", "transport"} else EXIT_OK), result.output
+    assert not (out / "done.json").exists()
diff --git a/tests/swarm/test_e2e_user_guide.py b/tests/swarm/test_e2e_user_guide.py
index 1d49e5f11..c4853bf07 100644
--- a/tests/swarm/test_e2e_user_guide.py
+++ b/tests/swarm/test_e2e_user_guide.py
@@ -114,11 +114,8 @@ def test_quickstart_lens_bare_review_emits_observability_artifacts(
     assert state["state"] == TERMINAL_STATE_VALUE
 
 
-def test_quickstart_does_not_emit_done_sentinel(runner, target, tmp_path):
-    """WS-0 (G-4): the inline pipeline now emits merged.md + return-contract.yaml
-    (see test_quickstart_emits_normalized_artifacts), but NOT the done.json sentinel
-    (reduce_wave3 does not write it; the on_completion done-sentinel step is not wired
-    on this inline path). This is the narrowed remnant of the old M5-absent assertion."""
+def test_quickstart_emits_done_sentinel(runner, target, tmp_path):
+    """A completed default run publishes the marker after its result and state."""
     out = tmp_path / "out"
     result = _run(
         runner,
@@ -133,9 +130,17 @@ def test_quickstart_does_not_emit_done_sentinel(runner, target, tmp_path):
         "stub",
     )
     assert result.exit_code == EXIT_OK, result.output
-    assert not (out / DONE_SENTINEL_FILENAME).exists(), (
-        f"{DONE_SENTINEL_FILENAME} should not exist on the inline (non-resume) WS-0 path"
-    )
+    import yaml
+
+    marker = json.loads((out / DONE_SENTINEL_FILENAME).read_text())
+    contract = yaml.safe_load((out / RESULT_CONTRACT_FILENAME).read_text())
+    assert marker == {
+        "atomic_write": True,
+        "terminal_status": contract["status"],
+        "contract_path": str((out / RESULT_CONTRACT_FILENAME).resolve()),
+    }
+    assert contract["status"] == "success"
+    assert json.loads((out / SWARM_STATE_FILENAME).read_text())["state"] == "terminal"
 
 
 def test_quickstart_emits_normalized_artifacts(runner, target, tmp_path):
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
