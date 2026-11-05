4dbc1d1a24209823d68b72ac423d79376ab92c0f
Review one task for spec compliance.

Task brief: ## Task 5: Carry the reviewer name through finding normalisation

Depends on: Task 1

Edit src/superclaude/pr_submit/severity_router.py `finding_from_comment`: read an optional text `reviewer` key from the root (default "augment"; a non-text value raises `ValueError` like the other text fields) and pass it to `Finding`. No change to `remap_severity` or `route`.

Acceptance criteria:
- `finding_from_comment({...,"reviewer":"codex","severity_hint":"medium"}).reviewer == "codex"`; a root without the key gives "augment".
- tests/pr_submit/test_severity_router.py passes.
Global constraints: 
- The design file .dev/pr-submit-codex/design/pr-submit-codex-design.md is the specification; do not add behaviour it does not describe.
- Keep the deterministic core src/superclaude/pr_submit/ free of gh and git command tokens (NFR-6, checked by tests/pr_submit/test_static_grep.py).
- Augment-only behaviour must stay identical apart from the added reviewer_absent event and reviewer fields (design sections 5 and 6); existing tests in tests/pr_submit/ keep passing.
- Never hardcode src/superclaude/ paths inside installed primitives (command, skill, refs, scripts); keep script file names unchanged.
- plugins/superclaude/ has no pr-submit twin (design section 3), so no mirror edit is needed; do not create one.
- Edit src/superclaude/ only, then run make sync-dev; never edit or stage .claude/ copies.
- Run pytest only on named files or tests/pr_submit, never the full suite or tests/cli/eval/ as a directory; use uv run.
- .dev/tasks/ is always staged (git add .dev/tasks), including this package and its artifacts/.
Start sha: 4dbc1d1a24209823d68b72ac423d79376ab92c0f
Diff against the start snapshot: diff --git a/src/superclaude/pr_submit/severity_router.py b/src/superclaude/pr_submit/severity_router.py
index 963cec34..483142b4 100644
--- a/src/superclaude/pr_submit/severity_router.py
+++ b/src/superclaude/pr_submit/severity_router.py
@@ -74,7 +74,7 @@ def finding_from_comment(raw: dict) -> Finding:
     for value in (line, original):
         if value is not None and (type(value) is not int or value <= 0):
             raise ValueError("finding locations must be positive integers or null")
-    for key in ("severity_hint", "category", "confidence"):
+    for key in ("severity_hint", "category", "confidence", "reviewer"):
         if raw.get(key) is not None and not isinstance(raw[key], str):
             raise ValueError(f"finding {key} must be text")
     for key in ("in_diff", "is_outdated"):
@@ -115,6 +115,7 @@ def finding_from_comment(raw: dict) -> Finding:
         review_id=review_id,
         original_line=original,
         is_outdated=raw.get("is_outdated", False),
+        reviewer=(raw.get("reviewer") or "augment").strip() or "augment",
     )
 
 
diff --git a/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t5-check.py b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t5-check.py
new file mode 100644
index 00000000..8ae7cac6
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t5-check.py
@@ -0,0 +1,11 @@
+from superclaude.pr_submit import finding_from_comment
+base = {"path": "a.py", "line": 3, "body": "bug"}
+f = finding_from_comment({**base, "reviewer": "codex", "severity_hint": "medium"})
+print("codex reviewer:", f.reviewer, "hint:", f.severity_hint)
+print("default reviewer:", finding_from_comment(base).reviewer)
+try:
+    finding_from_comment({**base, "reviewer": 7})
+    print("non-text reviewer: accepted (unexpected)")
+except ValueError as exc:
+    print("non-text reviewer: ValueError", exc)
+assert f.reviewer == "codex" and finding_from_comment(base).reviewer == "augment"
diff --git a/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t5-check.log b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t5-check.log
new file mode 100644
index 00000000..139031a2
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t5-check.log
@@ -0,0 +1,4 @@
+codex reviewer: codex hint: medium
+default reviewer: augment
+non-text reviewer: ValueError finding reviewer must be text
+rc=0
diff --git a/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t5-test.log b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t5-test.log
new file mode 100644
index 00000000..76ee9240
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t5-test.log
@@ -0,0 +1,13 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 4.3.5
+benchmark: 5.3.0 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
+rootdir: /home/coder/workspaces/IronClaude/.dev/worktrees/pr-submit-codex
+configfile: pyproject.toml
+plugins: superclaude-4.3.5, benchmark-5.3.0, anyio-4.15.1, cov-7.1.0
+collected 28 items
+
+tests/pr_submit/test_severity_router.py ............................     [100%]
+
+============================== 28 passed in 0.07s ==============================
+rc=0
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
