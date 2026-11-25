1e33f422dadf9034876adec8c03894ab6ccfca76
Review one task for spec compliance.

Task brief: Add detached launcher and child completion regression coverage

Depends on: Task 2

Read `_launch_detached_run` in `src/superclaude/cli/swarm/commands.py`, its snapshot/child argv contract, and the tmux gating and cleanup fixtures in `tests/swarm/test_tmux_detached.py`. Add regression tests to that module, using deterministic stub jobs with unique job IDs, absolute target/output paths and isolated HOME. Reuse the existing missing-tmux checks in `tests/swarm/test_tmux_fallback.py` rather than adding a new launcher implementation.

Add an always-runnable test that intercepts `swarm_tmux.launch_detached` to capture the actual staged child request without running a child yet. Assert the launcher has not published a marker. Then execute the captured snapshot through the real registered child CLI continuation with stub transport and assert publication, with enabled/disabled completion policy variants. This is deterministic launcher/child-boundary coverage, not proof of a live tmux session. Add a separate live tmux stub-child integration test using the module's existing availability rules; use a bounded wait that surfaces child failure/timeout and cleans up only the test-owned session.


Acceptance criteria:
T3.AC1: Before simulated or live child completion, the parent-created snapshot preserves the requested completion policy and no marker is produced by the parent. After successful child completion, enabled policy produces the existing marker with matching actual contract status/path and terminal state; disabled policy does not. The test exercises the child execution path, not a direct marker-writer call.
T3.AC2: The live test launches the actual detached CLI using UV, captures output and waits for the child-owned marker with a fixed deadline. It validates the contract and terminal state once the marker appears. Save command, environment capability (without secret values), stdout/stderr, observed artifacts and result under `./artifacts/detached-cli/` and `./artifacts/detached-check.txt`. If tmux is missing or nesting is unsupported, record the explicit skip and retain detached runtime acceptance as NOT PROVEN; deterministic simulation is not a substitute and full repair closure must not be claimed.
T3.AC3: Run `uv run pytest tests/swarm/test_tmux_detached.py tests/swarm/test_tmux_fallback.py tests/swarm/test_kill_cmd.py tests/swarm/test_done_sentinel.py tests/swarm/test_three_layer_artifacts.py tests/swarm/test_imm6_atomic_write.py tests/cli/reflect/test_ensemble_unit.py tests/cli/reflect/test_ensemble_stub_integration.py` and save results including skips in `./artifacts/completion-compatibility.txt`.
T3.AC4: `_launch_detached_run` remains launcher-only; `_emit_killed_done_sentinel` and `kill_cmd` keep their existing killed marker, empty contract path and idempotence. The existing `run_tier2_ensemble` caller in `src/superclaude/cli/reflect/ensemble.py` and direct helper tests still use the unchanged writer API/schema; do not add swarm-state prerequisites to that helper or broaden this task into reflect changes.
Global constraints: - Only issue 540 is covered. The diagnostic package `.dev/troubleshoot/bug-issue540-completion-marker-20261123191058/` is immutable context; read `REPORT.md`, `evidence-validation.md`, `tier1-observation.md` and `contract-ledger.md` there when executing tasks. Its historical absolute paths refer to the old checkout and must not be used as live edit destinations.
- The user authorized this planning step after the recorded pre-fix planning ambiguity was explained. That does not clear the report's blocked repair closure or authorize implementation. Execute this plan only after a separate implementation request; do not repeat diagnosis merely to obtain a plan. Keep the original report unchanged.
- Preserve the recorded negative CLI witness from `artifacts/negative-witness.txt` in that diagnostic package. Successful repair requires new positive public-CLI evidence paired with it; neither the earlier diagnostic review PASS nor this plan certifies a repair. All new evidence belongs under this package's `./artifacts/`, using fresh isolated job output roots and an isolated HOME. Never overwrite the old foreground/resume evidence.
- Production edits are limited to the two completion continuations in `src/superclaude/cli/swarm/commands.py`. Reuse `reduce.emit_done_sentinel`, `ResultContract.status`, existing filename constants and atomic writers. Do not create a new marker schema, duplicate contract emission, change CLI exit/stdout contracts, or implement `print_contract_to_stdout`.
- Respect the effective foreground or rehydrated resume policy. Arbitrary original runtime override recovery on resume is incomplete and is not part of this fix: do not change `Manifest`, `preflight.resume_mode`, caller/lens metadata recovery, or persistence formats to address it. A disabled effective resume policy can be tested through a controlled rehydration seam, but must not be advertised as original-policy persistence.
- Detached parents only launch; children own completion. Preserve `_emit_killed_done_sentinel`, `kill_cmd`, the killed marker's empty contract path, existing writer atomicity and existing resume worker-skip/merge semantics. No new cleanup, stale-marker lifecycle protocol, or adjacent behavior change is included.
- Issues 501, 555 and 568, their task packages and shared diagnostic counters are outside scope. Do not import, edit or stage their files. Stage only this newly created task package as required by project policy; never stage generated `.claude/` mirrors. No commit, push, GitHub write or automatic implementation handoff is authorized.
- All future Python and test execution uses UV. Use stub transports, no live model calls or credentials; read any required credentials from the environment without logging values. A skipped or unavailable live detached check is not a pass and cannot establish complete detached repair coverage.
Start sha: 1e33f422dadf9034876adec8c03894ab6ccfca76
Diff against the start snapshot: diff --git a/tests/swarm/test_tmux_detached.py b/tests/swarm/test_tmux_detached.py
index 6b6eb8c93..a069d7585 100644
--- a/tests/swarm/test_tmux_detached.py
+++ b/tests/swarm/test_tmux_detached.py
@@ -253,3 +253,139 @@ def test_detached_session_survives_caller_exit(tmp_path) -> None:
     finally:
         if swarm_tmux.has_session(job_id):
             swarm_tmux.kill(job_id)
+
+
+def _completion_spec(tmp_path, enabled=True):
+    import json
+
+    from superclaude.cli.swarm.commands import _build_spec_from_lens
+
+    spec = _build_spec_from_lens("bare-review")
+    spec["job_id"] = "completion-" + uuid.uuid4().hex[:12]
+    target = tmp_path / "target.txt"
+    target.write_text("Review this isolated completion test target.\n" * 10)
+    spec["target"]["path"] = str(target)
+    spec["output"]["dir"] = str(tmp_path / "out")
+    spec["transport"]["kind"] = "stub"
+    spec["runtime"]["on_completion"]["write_done_sentinel"] = enabled
+    path = tmp_path / "spec.json"
+    path.write_text(json.dumps(spec))
+    return spec, path
+
+
+@pytest.mark.parametrize("enabled", [False, True])
+def test_detached_parent_defers_completion_to_actual_child(
+    tmp_path, monkeypatch, enabled
+):
+    import json
+    from pathlib import Path
+
+    from click.testing import CliRunner
+
+    from superclaude.cli.swarm.commands import run_cmd
+
+    home = tmp_path / "home"
+    home.mkdir()
+    monkeypatch.setenv("HOME", str(home))
+    spec, path = _completion_spec(tmp_path, enabled)
+    out = tmp_path / "out"
+    requests = []
+    monkeypatch.setattr(swarm_tmux, "is_tmux_available", lambda: True)
+
+    def launch(job_id, argv, **kwargs):
+        assert not (out / "done.json").exists()
+        requests.append(argv)
+        return swarm_tmux.session_name(job_id)
+
+    monkeypatch.setattr(swarm_tmux, "launch_detached", launch)
+    parent = CliRunner().invoke(
+        run_cmd, [str(path), "--detached", "--output", str(out)]
+    )
+    assert parent.exit_code == 0, parent.output
+    assert not (out / "done.json").exists()
+    assert len(requests) == 1
+    snapshot = Path(requests[0][-1])
+    assert (
+        json.loads(snapshot.read_text())["runtime"]["on_completion"][
+            "write_done_sentinel"
+        ]
+        is enabled
+    )
+    # Execute precisely the captured child request, not a repaired test-only argv.
+    child = CliRunner().invoke(run_cmd, requests[0][5:])
+    assert child.exit_code == 0, child.output
+    assert (out / "done.json").exists() is enabled
+    if enabled:
+        import yaml
+
+        marker = json.loads((out / "done.json").read_text())
+        assert (
+            marker["terminal_status"]
+            == yaml.safe_load((out / "return-contract.yaml").read_text())["status"]
+        )
+        assert marker["contract_path"] == str((out / "return-contract.yaml").resolve())
+        assert (
+            json.loads((out / ".swarm-state.json").read_text())["state"] == "terminal"
+        )
+
+
+@requires_tmux
+@pytest.mark.skipif(
+    not NOT_NESTED, reason="nested tmux does not support detached launch"
+)
+def test_detached_live_cli_child_publishes_completion(tmp_path, monkeypatch):
+    import json
+    import sys
+    from pathlib import Path
+
+    spec, path = _completion_spec(tmp_path)
+    out = tmp_path / "out"
+    home = tmp_path / "home"
+    home.mkdir()
+    env = dict(
+        os.environ,
+        HOME=str(home),
+        PYTHONPATH=str(Path(__file__).resolve().parents[2] / "src"),
+        PYTHONDONTWRITEBYTECODE="1",
+    )
+    command = [
+        "uv",
+        "run",
+        "--no-project",
+        "--python",
+        sys.executable,
+        "superclaude",
+        "swarm",
+        "run",
+        str(path),
+        "--detached",
+        "--output",
+        str(out),
+    ]
+    result = subprocess.run(
+        command, capture_output=True, text=True, env=env, timeout=30
+    )
+    try:
+        assert result.returncode == 0, result.stdout + result.stderr
+        deadline = time.monotonic() + 10
+        while time.monotonic() < deadline and not (out / "done.json").exists():
+            if not swarm_tmux.has_session(spec["job_id"]):
+                break
+            time.sleep(0.1)
+        assert (out / "done.json").is_file(), (
+            f"child ended without completion: {sorted(p.name for p in out.iterdir())}"
+        )
+        import yaml
+
+        marker = json.loads((out / "done.json").read_text())
+        assert (
+            marker["terminal_status"]
+            == yaml.safe_load((out / "return-contract.yaml").read_text())["status"]
+            == "success"
+        )
+        assert (
+            json.loads((out / ".swarm-state.json").read_text())["state"] == "terminal"
+        )
+    finally:
+        if swarm_tmux.has_session(spec["job_id"]):
+            swarm_tmux.kill(spec["job_id"])
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
