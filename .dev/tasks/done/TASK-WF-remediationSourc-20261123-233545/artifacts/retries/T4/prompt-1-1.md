ffa799f65173efefa019c434993e17b378f13a29
Review one task for spec compliance.

Task brief: ## Task 4: Test failed_step in test_first_run.py

Depends on: Task 1

In `tests/issue_watch/test_first_run.py`, add tests for `failed_step` using the existing harness helpers (the class around lines 100-140 that builds a config and a state directory under `tmp_path`): a failed `config` report in `state_dir`, a `passed` report, no report, a symlinked report, a non-UTF-8 first line, and a relative `state_dir` with the report beside the config as `<stem>-first-run.txt` (follow the existing pin at lines 347-356).

Acceptance criteria:
- T4.AC1: Each case above has its own test and the new tests fail if `failed_step` is removed.
- T4.AC2: `uv run pytest tests/issue_watch/test_first_run.py -q` passes.
Global constraints: ## Constraints

- Reuse the existing `first_run` function as the only setup path; do not add GitHub writes, label creation or store creation to `dispatch.py` or `cycle.py` (the boundary pinned by `tests/issue_watch/test_security_invariants.py` stays intact).
- Do not change the config schema (`_TOP_KEYS` in `src/superclaude/cli/issue_watch/cycle.py`) and do not change `ensure_config` in `src/superclaude/cli/issue_watch/generate.py`.
- A config with no first-run report, or whose report starts with `first-run: passed`, is never retried.
- A dry-run sweep makes no `first_run` call and writes no file.
- Do not edit anything under `.claude/`; change `src/` and `tests/` only.
Start sha: ffa799f65173efefa019c434993e17b378f13a29
Diff against the start snapshot: 
```diff
diff --git a/tests/issue_watch/test_first_run.py b/tests/issue_watch/test_first_run.py
index a026b5340..e6704e661 100644
--- a/tests/issue_watch/test_first_run.py
+++ b/tests/issue_watch/test_first_run.py
@@ -356,3 +356,92 @@ def test_an_unreadable_config_reports_next_to_itself_under_its_own_name(
     assert out.report_path == path.parent / "Broken-first-run.txt"
     assert "config_invalid" in out.report_path.read_text()
     assert os.path.exists(path) and path.read_text() == "not json"
+
+
+# --- failed_step: the read-only check dispatch uses to retry a failed first run --------------
+
+
+def _plain_config(tmp_path: Path, **raw) -> Path:
+    path = tmp_path / "cfg" / "Plain.json"
+    path.parent.mkdir(parents=True, exist_ok=True)
+    path.write_text(json.dumps(raw))
+    return path
+
+
+def test_failed_step_names_the_step_of_a_real_failed_first_run(tmp_path) -> None:
+    h = Harness(tmp_path, worktree=False)
+    assert h.run().status == "failed"
+    found = first_run.failed_step(h.path)
+    assert found is not None and found[0] == "config"
+    assert found[1].tzinfo is not None
+    assert abs(found[1].timestamp() - h.report.stat().st_mtime) < 1
+
+
+def test_failed_step_reads_the_step_after_failed_up_to_the_colon(tmp_path) -> None:
+    state = tmp_path / "state"
+    state.mkdir()
+    path = _plain_config(tmp_path, state_dir=str(state))
+    (state / first_run.REPORT_FILE).write_text(
+        "first-run: failed dry_run: origin_mismatch\nship_gate: closed\n"
+    )
+    found = first_run.failed_step(path)
+    assert found is not None and found[0] == "dry_run"
+
+
+def test_failed_step_is_none_for_a_passed_report(tmp_path) -> None:
+    h = Harness(tmp_path)
+    assert h.run().status == "enabled"
+    assert first_run.failed_step(h.path) is None
+
+
+def test_failed_step_is_none_when_there_is_no_report(tmp_path) -> None:
+    h = Harness(tmp_path)
+    assert not h.report.exists()
+    assert first_run.failed_step(h.path) is None
+
+
+def test_failed_step_does_not_follow_a_symlinked_report(tmp_path) -> None:
+    state = tmp_path / "state"
+    state.mkdir()
+    path = _plain_config(tmp_path, state_dir=str(state))
+    real = tmp_path / "real.txt"
+    real.write_text("first-run: failed config: worktree_invalid\n")
+    os.symlink(real, state / first_run.REPORT_FILE)
+    assert first_run.failed_step(path) is None
+
+
+def test_failed_step_is_none_for_a_non_utf8_first_line(tmp_path) -> None:
+    state = tmp_path / "state"
+    state.mkdir()
+    path = _plain_config(tmp_path, state_dir=str(state))
+    (state / first_run.REPORT_FILE).write_bytes(b"first-run: failed \xff\xfe: x\n")
+    assert first_run.failed_step(path) is None
+
+
+def test_failed_step_finds_the_report_beside_a_config_with_a_relative_state_dir(
+    tmp_path,
+) -> None:
+    path = _plain_config(tmp_path, state_dir="relative/state")
+    (path.parent / f"Plain-{first_run.REPORT_FILE}").write_text(
+        "first-run: failed config: config_invalid\n"
+    )
+    found = first_run.failed_step(path)
+    assert found is not None and found[0] == "config"
+
+
+def test_failed_step_finds_the_report_of_an_unreadable_config(tmp_path) -> None:
+    path = tmp_path / "cfg" / "Broken.json"
+    path.parent.mkdir()
+    path.write_text("not json")
+    h = Harness(tmp_path)  # only for its router and factory
+    first_run.first_run(path, DEFAULTS, h.router, h.factory)
+    found = first_run.failed_step(path)
+    assert found is not None and found[0] == "config"
+
+
+def test_failed_step_writes_nothing(tmp_path) -> None:
+    h = Harness(tmp_path, worktree=False)
+    h.run()
+    before = sorted(str(p) for p in tmp_path.rglob("*"))
+    first_run.failed_step(h.path)
+    assert sorted(str(p) for p in tmp_path.rglob("*")) == before
```

Codegraph context
index_state: fresh
checked_at: 2026-11-24T02:39:04Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-751
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-751
call codegraph only when index_state: fresh, never to widen scope
Dependents not in the diff (Q2b): Test-only addition appended to tests/issue_watch/test_first_run.py; no production file in this diff; failed_step (first_run.py) was delivered by Task 1.

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
