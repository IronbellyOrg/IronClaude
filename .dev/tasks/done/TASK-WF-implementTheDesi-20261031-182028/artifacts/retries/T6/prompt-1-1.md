34fd8d6edc8a8dd61af89b505c43e87793ad120f
Review one task for spec compliance.

Task brief: ## Task 6: Add the reviewer adapter table and the Codex priority parser

Depends on: Task 2

Create src/superclaude/pr_submit/reviewers.py per design sections 4, 7 and 14 with: `REVIEWERS = ("augment", "codex")`, `reviewer_identities(contract, reviewer)`, `retrigger_phrase(contract, reviewer)` (Augment: first `accepted_trigger_phrases` entry, i.e. "auggie review"; Codex: `codex_retrigger_phrase`), `reviewer_activity(payload, contract)`, `parse_codex_priority(body)` (exactly one `![P<n> Badge](https://img.shields.io/badge/P<m>-...)` with n == m in 0-3 on the first non-blank line, colour ignored, else None) and `codex_severity_hint(priority)` (P0 critical, P1 high, P2 medium, P3 low, None → None). No gh or git tokens.

Acceptance criteria:
- `parse_codex_priority` returns "P0".."P3" for the four badges and None for no badge, two badges, P4, and alt/URL mismatch.
- `route(remap_severity(finding_from_comment(root)))` for roots carrying the mapped hint gives `--depth deep --fix` for P0 and P1, `--fix` for P2, report-only for P3, and `--fix` (Medium fail-safe) for a malformed badge.
Global constraints: 
- The design file .dev/pr-submit-codex/design/pr-submit-codex-design.md is the specification; do not add behaviour it does not describe.
- Keep the deterministic core src/superclaude/pr_submit/ free of gh and git command tokens (NFR-6, checked by tests/pr_submit/test_static_grep.py).
- Augment-only behaviour must stay identical apart from the added reviewer_absent event and reviewer fields (design sections 5 and 6); existing tests in tests/pr_submit/ keep passing.
- Never hardcode src/superclaude/ paths inside installed primitives (command, skill, refs, scripts); keep script file names unchanged.
- plugins/superclaude/ has no pr-submit twin (design section 3), so no mirror edit is needed; do not create one.
- Edit src/superclaude/ only, then run make sync-dev; never edit or stage .claude/ copies.
- Run pytest only on named files or tests/pr_submit, never the full suite or tests/cli/eval/ as a directory; use uv run.
- .dev/tasks/ is always staged (git add .dev/tasks), including this package and its artifacts/.
Start sha: 34fd8d6edc8a8dd61af89b505c43e87793ad120f
Diff against the start snapshot: diff --git a/src/superclaude/pr_submit/reviewers.py b/src/superclaude/pr_submit/reviewers.py
new file mode 100644
index 00000000..b857f459
--- /dev/null
+++ b/src/superclaude/pr_submit/reviewers.py
@@ -0,0 +1,82 @@
+"""Reviewer adapters for the ``sc:pr-submit`` core: Augment and Codex.
+
+One reviewer-agnostic path with a small per-reviewer adapter: who the author is,
+how completion is proven, how severity is read, and which comment asks for a
+re-review. Everything after a normalized ``Finding`` is shared. Values come from
+the detection contract, so a local override can change or blank them; an empty
+identity set disables that reviewer.
+
+Core purity (NFR-6): pure functions over an already-fetched snapshot; no shell or
+version-control command tokens.
+"""
+
+from __future__ import annotations
+
+import re
+from typing import Any
+
+from .classifier import _augment_identities, has_augment_activity, has_reviewer_activity
+
+REVIEWERS = ("augment", "codex")
+
+_CODEX_HINTS = {"P0": "critical", "P1": "high", "P2": "medium", "P3": "low"}
+_BADGE = re.compile(r"!\[P(\d) Badge\]\(https://img\.shields\.io/badge/P(\d)-[^)\s]*\)")
+
+
+def reviewer_identities(contract: Any, reviewer: str) -> set[str]:
+    """The non-empty author identities of ``reviewer`` (empty set = disabled)."""
+    if reviewer == "augment":
+        return _augment_identities(contract)
+    if reviewer == "codex":
+        return {
+            identity
+            for identity in (
+                getattr(contract, "codex_bot_login", None),
+                getattr(contract, "codex_app_slug", None),
+            )
+            if isinstance(identity, str) and identity
+        }
+    raise ValueError(f"unknown reviewer: {reviewer!r}")
+
+
+def retrigger_phrase(contract: Any, reviewer: str) -> str:
+    """The comment body that asks ``reviewer`` for a re-review."""
+    if reviewer == "augment":
+        phrases = getattr(contract, "accepted_trigger_phrases", None) or []
+        return phrases[0] if phrases else "auggie review"
+    if reviewer == "codex":
+        return getattr(contract, "codex_retrigger_phrase", None) or "@codex review"
+    raise ValueError(f"unknown reviewer: {reviewer!r}")
+
+
+def reviewer_activity(payload: dict, contract: Any) -> dict[str, bool]:
+    """Presence per reviewer. Augment keeps its silence predicate unchanged."""
+    return {
+        "augment": has_augment_activity(payload, contract),
+        "codex": has_reviewer_activity(payload, reviewer_identities(contract, "codex")),
+    }
+
+
+def parse_codex_priority(body: Any) -> str | None:
+    """``"P0".."P3"`` from the one Codex badge on the first non-blank line, else None.
+
+    The body must hold exactly one ``![P<n> Badge](https://img.shields.io/badge/P<m>-...)``
+    image with ``n == m`` in 0-3, on the first non-blank line. Colour is ignored.
+    """
+    if not isinstance(body, str):
+        return None
+    badges = _BADGE.findall(body)
+    if len(badges) != 1:
+        return None
+    alt, url = badges[0]
+    if alt != url or alt not in "0123":
+        return None
+    first = next((line for line in body.splitlines() if line.strip()), "")
+    if not _BADGE.search(first):
+        return None
+    return f"P{alt}"
+
+
+def codex_severity_hint(priority: str | None) -> str | None:
+    """Map a Codex priority onto the existing severity hints (P0 critical .. P3 low)."""
+    return _CODEX_HINTS.get(priority) if isinstance(priority, str) else None
diff --git a/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t6-check.py b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t6-check.py
new file mode 100644
index 00000000..50a80c39
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t6-check.py
@@ -0,0 +1,30 @@
+from superclaude.pr_submit import DetectionContract, finding_from_comment, remap_severity, route
+from superclaude.pr_submit.reviewers import (REVIEWERS, codex_severity_hint, parse_codex_priority,
+    retrigger_phrase, reviewer_activity, reviewer_identities)
+
+def badge(alt, url, title="Fix it"):
+    return (f"**<sub><sub>![{alt} Badge](https://img.shields.io/badge/{url}-yellow?style=flat)"
+            f"</sub></sub>  {title}**\n\nBody text.\n\n<!-- codex-code-review-finding:v1 -->")
+
+cases = {"P0": badge("P0", "P0"), "P1": badge("P1", "P1"), "P2": badge("P2", "P2"), "P3": badge("P3", "P3"),
+         "no badge": "**Fix it**\n\nBody.", "two badges": badge("P1", "P1") + "\n" + badge("P2", "P2"),
+         "P4": badge("P4", "P4"), "alt/url mismatch": badge("P1", "P2"),
+         "badge not on first line": "Intro line\n" + badge("P2", "P2")}
+expected = {"P0": "P0", "P1": "P1", "P2": "P2", "P3": "P3"}
+ok = True
+for name, body in cases.items():
+    got = parse_codex_priority(body)
+    want = expected.get(name)
+    ok &= got == want
+    hint = codex_severity_hint(got)
+    r = route(remap_severity(finding_from_comment({"path": "a.py", "line": 1, "body": body,
+                                                   "reviewer": "codex", "severity_hint": hint})))
+    print(f"{name:24} priority={got} hint={hint} route={r}")
+shipped = DetectionContract.load()
+print("REVIEWERS", REVIEWERS)
+print("codex identities", sorted(reviewer_identities(shipped, "codex")), "augment", sorted(reviewer_identities(shipped, "augment")))
+print("phrases", retrigger_phrase(shipped, "augment"), "|", retrigger_phrase(shipped, "codex"))
+print("bare contract codex identities", reviewer_identities(DetectionContract(), "codex"))
+p = {"reviews": [], "comments": [{"user": {"login": "chatgpt-codex-connector[bot]"}, "body": "x"}]}
+print("activity", reviewer_activity(p, shipped))
+raise SystemExit(0 if ok else 1)
diff --git a/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t6-check.log b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t6-check.log
new file mode 100644
index 00000000..66a0a286
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t6-check.log
@@ -0,0 +1,15 @@
+P0                       priority=P0 hint=critical route=--depth deep --fix
+P1                       priority=P1 hint=high route=--depth deep --fix
+P2                       priority=P2 hint=medium route=--fix
+P3                       priority=P3 hint=low route=report-only
+no badge                 priority=None hint=None route=--fix
+two badges               priority=None hint=None route=--fix
+P4                       priority=None hint=None route=--fix
+alt/url mismatch         priority=None hint=None route=--fix
+badge not on first line  priority=None hint=None route=--fix
+REVIEWERS ('augment', 'codex')
+codex identities ['chatgpt-codex-connector', 'chatgpt-codex-connector[bot]'] augment ['augmentcode', 'augmentcode[bot]']
+phrases auggie review | @codex review
+bare contract codex identities set()
+activity {'augment': False, 'codex': True}
+rc=0
diff --git a/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t6-test.log b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t6-test.log
new file mode 100644
index 00000000..cc5fccbc
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t6-test.log
@@ -0,0 +1,14 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 4.3.5
+benchmark: 5.3.0 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
+rootdir: /home/coder/workspaces/IronClaude/.dev/worktrees/pr-submit-codex
+configfile: pyproject.toml
+plugins: superclaude-4.3.5, benchmark-5.3.0, anyio-4.15.1, cov-7.1.0
+collected 47 items
+
+tests/pr_submit/test_static_grep.py ...................                  [ 40%]
+tests/pr_submit/test_severity_router.py ............................     [100%]
+
+============================== 47 passed in 0.60s ==============================
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
