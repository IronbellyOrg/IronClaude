8ed35fd4f4641e3f8c9fdedc64b3eb360c9c09a7
Review one task for spec compliance.

Task brief: ## Task 1: Add stale-marker and overlapping-entry regression cases

Read the retained test_resume_marker.py and reproduction-expanded.log in .dev/troubleshoot/bug-stale-done-json-on-resume-20261126145119/ and the closure report Evidence and Pipeline Hardening Closure sections. Use tests/swarm/test_resume_crash_recovery.py's existing CliRunner, manifest and sidecar helpers to add regressions without changing production code. Create the previous marker through an actual successful fresh stub CLI run, not a marker-shaped placeholder. Observe marker existence at dispatch entry; repeat with the effective resume policy patched true and false through real preflight.resume_mode. Preserve the distinction between a dispatch-entry observer and actual transport execution. Add the nested active-fresh-run resume rejection regression from the retained case, recording prior artifact bytes before entering the nested CLI.

Acceptance criteria:
T1.AC1: Before editing commands.py, run `PYTHONPATH=src uv run --no-project /opt/uv/tools/superclaude/bin/python -m pytest tests/swarm/test_resume_crash_recovery.py -k 'stale_marker or overlapping_resume' -vv -s`; save the command, exit code, baseline HEAD, exact failing assertion and stdout/stderr under ./artifacts/t1-red.txt. The new test names contain stale_marker or overlapping_resume so the command cannot silently select zero cases.
T1.AC2: Observe failures caused by the previous marker still present and overlapping entry still accepted, not by missing dependencies, wrong fixtures or CLI usage. Record both policy values and the disabled completed-attempt old-byte equality. Do not rerun the original diagnostic solely for planning.
T1.AC3: Existing tests are retained, including test_resume_completion_policy_status_and_order and test_resume_no_marker_on_error. Task 1 is not complete without an observed failing regression before production changes; retained historical failures alone do not satisfy this implementation checkpoint.

Global constraints: 
- This is a plan, not implementation authority. The coordinator decides whether to dispatch implementation after reading its checked contents. The paused ordinary agent and its unapproved native plan remain untouched.
- Preserve .dev/troubleshoot/issue540-diagnostic-closure-20261126-1515/REPORT.md, return-contract.yaml and evidence-validation.md, and all original evidence in .dev/troubleshoot/bug-stale-done-json-on-resume-20261126145119/. Their diagnosis is established, their repair status is not implemented, and their hardening verdict remains blocked. Do not rewrite those files, lower their gates, invent a waiver or claim their 121-test baseline proves repaired behavior.
- Only production delivery file: src/superclaude/cli/swarm/commands.py. Only checked-in test delivery file: tests/swarm/test_resume_crash_recovery.py. Evidence and the local simulated-worker witness belong under ./artifacts/. No issue 555 work, manifest schema expansion, completion-policy restoration redesign, shared marker-writer rewrite, dependency installation, source mirror edits or general concurrency redesign.
- Reuse dispatch_wave1, reduce_wave3, _write_swarm_state and emit_done_sentinel. Preserve fresh and resumed contract -> terminal state -> optional atomic marker order, the merged original marker-emission fix, detached absolute output behavior and kill-twice marker byte preservation. Do not change kill behavior or sibling reflect completion emission.
- Scope of ownership protection: the observed nested same-process invocation, including concurrent threads in that process. Current code has no trustworthy live owner record. A saved dispatching state can mean a crash and must never alone cause rejection. Cross-process output ownership remains unchanged and unproven, not a solved two-process race. If evidence establishes that a broader mechanism is necessary for these acceptance checks, stop and return the concrete design/scope blocker to the coordinator rather than silently adding a lock subsystem.
- Use UV for all Python operations and no installs. Commands below use the existing environment: PYTHONPATH=src uv run --no-project /opt/uv/tools/superclaude/bin/python -m pytest. If that interpreter is unavailable, report the environment blocker, not a product pass. Run only stub transports with isolated temporary HOME and output roots; never use a real provider or print credentials. Keep all intermediate evidence.
- Independent corrected-boundary review is mandatory after all implementation tasks complete, through the fresh managed FINAL archive review, separate from this plan's builtin pre-review. It must read actual current delivery files and package runtime evidence, not accept a self-reported pass. Governing live executor sources are `~/.claude/skills/sc-implement-protocol/refs/qa.md` (Managed FINAL review, Subagent prompt, Review file format, Verdict owner), `~/.claude/skills/sc-implement-protocol/refs/ledger.md` (Managed-package extension), and `~/.claude/skills/sc-implement-protocol/refs/managed-workspace.md` (Completion: fresh FINAL, then archive). Skills resolve globally first; only if unavailable use the corresponding project `.claude/skills/sc-implement-protocol/refs/qa.md`, `.claude/skills/sc-implement-protocol/refs/ledger.md`, and `.claude/skills/sc-implement-protocol/refs/managed-workspace.md`. Read those live sources before execution; a missing source or a concrete incompatibility with the required boundary proof blocks closure, never licenses a fabricated template or a weaker gate. Keep their closed review criteria, isolation and verdict ownership unchanged. Missing positive witness or missing independent FINAL leaves repair closure blocked; no diagnostic rerun substitutes for either.


Start sha: 8ed35fd4f4641e3f8c9fdedc64b3eb360c9c09a7
Diff against the start snapshot: diff --git a/tests/swarm/test_resume_crash_recovery.py b/tests/swarm/test_resume_crash_recovery.py
index a48e7aac1..8299b41c9 100644
--- a/tests/swarm/test_resume_crash_recovery.py
+++ b/tests/swarm/test_resume_crash_recovery.py
@@ -727,3 +727,106 @@ def test_resume_no_marker_on_error(tmp_path, monkeypatch, failure):
     result = CliRunner().invoke(run_cmd, ["--resume", JOB_ID, "--output", str(out)])
     assert result.exit_code != EXIT_OK
     assert not (out / "done.json").exists()
+
+
+def _artifact_bytes(out):
+    return {str(p.relative_to(out)): p.read_bytes() for p in out.rglob("*") if p.is_file()}
+
+
+def _completed_stub_run(tmp_path, monkeypatch):
+    """Seed a genuine terminal marker through the public CLI, never a fixture marker."""
+    home = tmp_path / "home"
+    home.mkdir(exist_ok=True)
+    monkeypatch.setenv("HOME", str(home))
+    target = tmp_path / "target.md"
+    target.write_text("A local simulated review target. " * 12)
+    out = tmp_path / "out"
+    fresh = CliRunner().invoke(run_cmd, [
+        "--lens", "bare-review", "--transport", "stub", "--target", str(target),
+        "--output", str(out),
+    ])
+    assert fresh.exit_code == EXIT_OK, fresh.output
+    assert (out / "done.json").is_file()
+    job_id = json.loads((out / "manifest.json").read_text())["job_id"]
+    return out, job_id
+
+
+def _retry_one(out):
+    meta = sorted(out.glob("*.meta.json"))[0]
+    data = json.loads(meta.read_text())
+    data["status"] = "timeout"
+    meta.write_text(json.dumps(data))
+
+
+def _completion_policy(monkeypatch, enabled):
+    import superclaude.cli.swarm.preflight as preflight
+
+    real = preflight.resume_mode
+
+    def rehydrate(*args, **kwargs):
+        spec = real(*args, **kwargs)
+        spec.runtime.on_completion.write_done_sentinel = enabled
+        return spec
+
+    monkeypatch.setattr(preflight, "resume_mode", rehydrate)
+
+
+@pytest.mark.parametrize("enabled", [True, False])
+def test_stale_marker_absent_at_accepted_dispatch(tmp_path, monkeypatch, enabled):
+    import superclaude.cli.swarm.dispatch as dispatch
+
+    out, job_id = _completed_stub_run(tmp_path, monkeypatch)
+    marker = out / "done.json"
+    old = marker.read_bytes()
+    _retry_one(out)
+    _completion_policy(monkeypatch, enabled)
+    real_dispatch = dispatch.dispatch_wave1
+    seen = []
+
+    def observe(*args, **kwargs):
+        seen.append(marker.exists())
+        return real_dispatch(*args, **kwargs)
+
+    monkeypatch.setattr(dispatch, "dispatch_wave1", observe)
+    result = CliRunner().invoke(run_cmd, ["--resume", job_id, "--output", str(out)])
+    print(f"dispatch-entry enabled={enabled} marker_exists={seen}; "
+          f"exit={result.exit_code}; final_marker={marker.exists()}; "
+          f"old_bytes_equal={marker.read_bytes() == old if marker.exists() else False}")
+    assert result.exit_code == EXIT_OK, result.output
+    assert seen == [False], "previous completion marker visible at accepted dispatch"
+    assert marker.exists() is enabled
+
+
+def test_overlapping_resume_preserves_active_fresh_artifacts(tmp_path, monkeypatch):
+    import superclaude.cli.swarm.dispatch as dispatch
+
+    home = tmp_path / "home"
+    home.mkdir()
+    monkeypatch.setenv("HOME", str(home))
+    target = tmp_path / "target.md"
+    target.write_text("Local overlap witness. " * 12)
+    out = tmp_path / "out"
+    real_dispatch = dispatch.dispatch_wave1
+    nested = []
+    entered = False
+
+    def observe(*args, **kwargs):
+        nonlocal entered
+        if not entered:
+            entered = True
+            job_id = json.loads((out / "manifest.json").read_text())["job_id"]
+            before = _artifact_bytes(out)
+            inner = CliRunner().invoke(run_cmd, ["--resume", job_id, "--output", str(out)])
+            nested.append((inner.exit_code, before == _artifact_bytes(out)))
+        return real_dispatch(*args, **kwargs)
+
+    monkeypatch.setattr(dispatch, "dispatch_wave1", observe)
+    result = CliRunner().invoke(run_cmd, [
+        "--lens", "bare-review", "--transport", "stub", "--target", str(target),
+        "--output", str(out),
+    ])
+    print(f"overlapping_resume result={nested}; fresh_exit={result.exit_code}")
+    assert result.exit_code == EXIT_OK, result.output
+    assert len(nested) == 1
+    assert nested[0][0] != EXIT_OK, "overlapping resume was accepted"
+    assert nested[0][1], "rejected overlap changed active invocation artifacts"

NEW FILE .dev/tasks/to-do/TASK-WF-createACheckedRe-20261126-161407/artifacts/t1-red.txt
Purpose: pre-production expected-red acceptance evidence, not an unintended regression.
Baseline HEAD: a98d7b4280363f2bb506d7af5fb4eb1551953c41
Production commands.py unchanged at this run.
Command: PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src uv run --no-project /opt/uv/tools/superclaude/bin/python -m pytest tests/swarm/test_resume_crash_recovery.py -k 'stale_marker or overlapping_resume' -vv -s
================================================= test session starts ==================================================
platform linux -- Python 3.13.5, pytest-9.2.0, pluggy-1.7.0 -- /opt/uv/tools/superclaude/bin/python
cachedir: .pytest_cache
SuperClaude: 6.1.0
rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-540-resume-marker
configfile: pyproject.toml
plugins: anyio-4.16.0, superclaude-6.1.0
collecting ... collected 43 items / 40 deselected / 3 selected

tests/swarm/test_resume_crash_recovery.py::test_stale_marker_absent_at_accepted_dispatch[True] dispatch-entry enabled=True marker_exists=[True]; exit=0; final_marker=True; old_bytes_equal=True
FAILED
tests/swarm/test_resume_crash_recovery.py::test_stale_marker_absent_at_accepted_dispatch[False] dispatch-entry enabled=False marker_exists=[True]; exit=0; final_marker=True; old_bytes_equal=True
FAILED
tests/swarm/test_resume_crash_recovery.py::test_overlapping_resume_preserves_active_fresh_artifacts overlapping_resume result=[(0, False)]; fresh_exit=0
FAILED

======================================================= FAILURES =======================================================
_________________________________ test_stale_marker_absent_at_accepted_dispatch[True] __________________________________
tests/swarm/test_resume_crash_recovery.py:796: in test_stale_marker_absent_at_accepted_dispatch
    assert seen == [False], "previous completion marker visible at accepted dispatch"
E   AssertionError: previous completion marker visible at accepted dispatch
E   assert [True] == [False]
E     
E     At index 0 diff: True != False
E     
E     Full diff: (-: missing in left side, +: extra in left side)
E       [
E     -     False,
E     +     True,
E       ]
_________________________________ test_stale_marker_absent_at_accepted_dispatch[False] _________________________________
tests/swarm/test_resume_crash_recovery.py:796: in test_stale_marker_absent_at_accepted_dispatch
    assert seen == [False], "previous completion marker visible at accepted dispatch"
E   AssertionError: previous completion marker visible at accepted dispatch
E   assert [True] == [False]
E     
E     At index 0 diff: True != False
E     
E     Full diff: (-: missing in left side, +: extra in left side)
E       [
E     -     False,
E     +     True,
E       ]
_______________________________ test_overlapping_resume_preserves_active_fresh_artifacts _______________________________
tests/swarm/test_resume_crash_recovery.py:831: in test_overlapping_resume_preserves_active_fresh_artifacts
    assert nested[0][0] != EXIT_OK, "overlapping resume was accepted"
E   AssertionError: overlapping resume was accepted
E   assert 0 != 0
=============================================== short test summary info ================================================
FAILED tests/swarm/test_resume_crash_recovery.py::test_stale_marker_absent_at_accepted_dispatch[True] - AssertionError: previous completion marker visible at accepted dispatch
assert [True] == [False]
  
  At index 0 diff: True != False
  
  Full diff: (-: missing in left side, +: extra in left side)
    [
  -     False,
  +     True,
    ]
FAILED tests/swarm/test_resume_crash_recovery.py::test_stale_marker_absent_at_accepted_dispatch[False] - AssertionError: previous completion marker visible at accepted dispatch
assert [True] == [False]
  
  At index 0 diff: True != False
  
  Full diff: (-: missing in left side, +: extra in left side)
    [
  -     False,
  +     True,
    ]
FAILED tests/swarm/test_resume_crash_recovery.py::test_overlapping_resume_preserves_active_fresh_artifacts - AssertionError: overlapping resume was accepted
assert 0 != 0
=========================================== 3 failed, 40 deselected in 0.75s ===========================================

exit_code=1

NEW FILE .dev/tasks/to-do/TASK-WF-createACheckedRe-20261126-161407/artifacts/t1-acceptance.txt
Expected-red acceptance verification
Raw failures retained unchanged in t1-red.txt; expected test outcome is intentional failure before production repair.
PASS: expected pre-repair red verified mechanically: 3 selected behavior assertions failed, both policies observed old marker, disabled completion retained old bytes, overlap accepted and mutated artifacts; production unchanged.

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
