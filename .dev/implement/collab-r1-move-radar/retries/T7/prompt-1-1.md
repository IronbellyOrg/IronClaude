78930ede7a7ee767148a9b727bc4eec0479ac169
Review one task for spec compliance.

Task brief: T7 (source: .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/DESIGN.md section 6.5 AC-1; task grouping in .dev/implement/collab-r1-move-radar/tasks.md). Run and complete the unit and fault-injection test suite of the design.
T7.AC1: `uv run pytest .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests -q` exits 0 with T-1..T-19 and F-1..F-14 collected and passed (no skips). DESIGN.md section 6.1 lists T-1..T-19 with their module names (T-1 test_catalogue.py, T-2 test_index.py, T-3 test_classify.py, T-4 test_order.py, T-5 test_hook_schedule.py, T-6 test_hook_finish.py, T-7 test_hook_seal.py, T-8 test_hook_errors.py, T-9 test_validate.py, T-10 test_settings_and_cmd.py (plus the gate-order part in test_launch.py), T-11 test_h2.py, T-12 test_values.py, T-13 test_runner_retry.py, T-14 test_anon.py, T-15 test_judge_path.py, T-16 test_results.py, T-17 test_collab_summary.py, T-18 test_alarms.py, T-19 test_cleanup.py); section 6.2 lists F-1..F-14. Work done in this task: the missing T-1 module tests/test_catalogue.py was written (the diff below); everything else was built and reviewed under T1-T6. Evidence logs saved by the executor: /tmp/collab-r1/t7-pytest.log (full run: 138 passed, rc 0, no skips) and /tmp/collab-r1/t7-collect.txt (collected tests per module).
Global constraints: Orchestrator constraints (global): create and edit files only under .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/ (plus .dev/implement/collab-r1-move-radar/ and scratch under /tmp/evalsb-collab-r1/ and /tmp/collab-r1/); do not edit src/, tests/, .claude/, .dev/tasks/, the 20261111-a1 eval folder or any other redesign's folder; do not stage, commit or push; python only through uv; models allowed muse-ember-1.0, gpt-6-luna, claude-haiku-5-5, claude-sonnet-5-5, grok-4.7, Opus only as the blind judge, never Qwen or glm; NOFALLBACK=1; no full panel runs; at most 3 reviewer or judge sessions at once.
Start sha: 78930ede7a7ee767148a9b727bc4eec0479ac169
Diff against the start snapshot: diff --git a/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_catalogue.py b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_catalogue.py
new file mode 100644
index 000000000..631c117ca
--- /dev/null
+++ b/.dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests/test_catalogue.py
@@ -0,0 +1,66 @@
+"""T-1: the frozen catalogue (DESIGN.md 6.1 T-1, R-07)."""
+
+import hashlib
+import json
+import re
+
+from conftest import A1DIR, FIX, R1, REPO, TOOLS, jload, run
+
+SRCREQ = REPO / ".dev/brainstorms/20261113-163248-panel-collaboration/merged-requirements.md"
+PKGS = ["TASK-WF-designSpec-20261107-075614", "TASK-WF-makeTheAliasOnly-20261105-051649", "TASK-WF-design-20261108-041415"]
+CAT = R1 / "config" / "catalogue.json"
+
+
+def src_moves():
+    """Move texts from the 'Move (text sent to a reviewer)' column of SRCREQ section 2.0 (the table at lines 184-193)."""
+    lines = SRCREQ.read_text().splitlines()[183:193]
+    rows = {}
+    for ln in lines:
+        m = re.match(r"^\| (M\d+) \| (.+?) \| (?:search|reading|either)", ln)
+        if m:
+            rows[m.group(1)] = m.group(2)
+    return rows
+
+
+def catcheck(cat, gts):
+    r = run(["uv", "run", "python", str(TOOLS / "collab_summary.py"), "catcheck", str(cat), *map(str, gts)])
+    return r.returncode, json.loads(r.stdout)
+
+
+def test_texts_equal_the_source_column():
+    cat, src = jload(CAT), src_moves()
+    assert sorted(src, key=lambda m: int(m[1:])) == [f"M{i}" for i in range(1, 11)]
+    assert cat["moves"] == src
+
+
+def test_observable_set_and_rendered_length():
+    cat = jload(CAT)
+    assert cat["observable"] == ["M1", "M2", "M4", "M7"]
+    for mid, text in cat["moves"].items():
+        rendered = text + (cat["observable_suffix"] if mid in cat["observable"] else "")
+        assert len(rendered) <= 300, mid
+    assert len(cat["src_text"]) <= 300 and len(cat["finish_text"]) <= 300
+
+
+def test_pin_matches_catalogue_sha256():
+    want = (R1 / "config" / "catalogue.sha256").read_text().split()[0]
+    assert hashlib.sha256(CAT.read_bytes()).hexdigest() == want
+    assert jload(R1 / "manifest.json")["catalogue_sha256"] == want
+
+
+def test_r07_detects_a_planted_plan_quote(tmp_path):
+    gt = jload(FIX / "ground-truth.json")
+    quote = next(i["plan_quote"] for i in gt["items"] if len(i.get("plan_quote", "")) >= 12)
+    cat = jload(CAT)
+    cat["moves"]["M3"] += " " + quote[:20]  # a 12-char window of a quote must be caught
+    planted = tmp_path / "planted.json"
+    planted.write_text(json.dumps(cat))
+    rc, out = catcheck(planted, [FIX / "ground-truth.json"])
+    assert rc == 1 and out["pass"] is False and out["hits"]
+
+
+def test_r07_real_catalogue_has_zero_ground_truth_hits():
+    gts = [A1DIR / p / "ground-truth.json" for p in PKGS]
+    assert all(g.exists() for g in gts)
+    rc, out = catcheck(CAT, gts)
+    assert rc == 0 and out == {"ground_truth_files": 3, "hits": [], "pass": True}

Codegraph context: index_state: fresh; checked_at: 2026-11-13T22:17:42Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel; projectPath: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel. call codegraph only when index_state: fresh, never to widen scope. Q2b dependents: none outside the diff (shell, markdown and untracked test files are not indexed; Grep floor used).
Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): Saved evidence for T7.AC1: /tmp/collab-r1/t7-pytest.log, /tmp/collab-r1/t7-collect.txt. Reproduce with: uv run pytest .dev/eval-workspaces/tasklist-review-panel/20261113-collab/r1-move-radar/tests -q -rs -p no:cacheprovider


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