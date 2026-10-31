47ac0255d1d34740b379e9d5bf06abc74de437e5
Review one task for spec compliance.

Task brief: ## Task 7: Classify Codex completion and select Codex finding roots

Depends on: Task 4, Task 5, Task 6

Add to src/superclaude/pr_submit/reviewers.py per design section 7: `codex_review_state(payload, contract, *, watermark=None, current_head_sha=None)` (exactly one Codex-authored issue comment with one bounded `<!-- codex-review-state:v1 {JSON} -->` marker, duplicate keys rejected, `code_review.status`/`commit_sha`/`has_any_findings` validated, completion time = `updated_at`, no later than `observed_at`, strictly newer than the watermark when given), `classify_codex(...)` returning polling/clean/findings by the design's Codex gate state rules (requires the payload completeness flags like the Augment gate), `codex_finding_comments(...)` (unresolved Codex-rooted threads through `_thread_findings` with the Codex identities and the marker time, each root dict gaining `reviewer: "codex"`, `codex_priority` and `severity_hint`), and `list_review_threads(payload, contract)` returning every Augment- or Codex-rooted thread (resolved or not) as `{reviewer, path, line, original_line, is_resolved, priority, severity, thread_id, comment_id}` for reports. Then run the read-only dry check: `src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh --pr 336 --repo IronbellyOrg/IronClaude` piped into `uv run python` calling `list_review_threads` with `DetectionContract.load()`, saving the output to ./artifacts/t7-dry-check-pr336.txt.

Acceptance criteria:
- A PR 334-shaped payload (completed, `has_any_findings:false`, no Codex review) classifies `clean`; a PR 336-shaped payload (three unresolved Codex roots with P2 badges) classifies `findings` with three roots carrying `reviewer == "codex"` and `severity_hint == "medium"`.
- Running status, wrong head, two summary comments, malformed or duplicate-key JSON, `updated_at` after `observed_at`, and `updated_at` not newer than the watermark each classify `polling`.
- ./artifacts/t7-dry-check-pr336.txt lists the three resolved Codex threads of PR 336 with priority P2 and severity Medium.
Global constraints: 
- The design file .dev/pr-submit-codex/design/pr-submit-codex-design.md is the specification; do not add behaviour it does not describe.
- Keep the deterministic core src/superclaude/pr_submit/ free of gh and git command tokens (NFR-6, checked by tests/pr_submit/test_static_grep.py).
- Augment-only behaviour must stay identical apart from the added reviewer_absent event and reviewer fields (design sections 5 and 6); existing tests in tests/pr_submit/ keep passing.
- Never hardcode src/superclaude/ paths inside installed primitives (command, skill, refs, scripts); keep script file names unchanged.
- plugins/superclaude/ has no pr-submit twin (design section 3), so no mirror edit is needed; do not create one.
- Edit src/superclaude/ only, then run make sync-dev; never edit or stage .claude/ copies.
- Run pytest only on named files or tests/pr_submit, never the full suite or tests/cli/eval/ as a directory; use uv run.
- .dev/tasks/ is always staged (git add .dev/tasks), including this package and its artifacts/.
Start sha: 47ac0255d1d34740b379e9d5bf06abc74de437e5
Diff against the start snapshot: --- a/src/superclaude/pr_submit/reviewers.py
+++ b/src/superclaude/pr_submit/reviewers.py
@@ -12,10 +12,29 @@
 
 from __future__ import annotations
 
+import json
 import re
 from typing import Any
 
-from .classifier import _augment_identities, has_augment_activity, has_reviewer_activity
+from .classifier import (
+    _COMPLETENESS,
+    STATE_CLEAN,
+    STATE_FINDINGS,
+    STATE_POLLING,
+    _augment_entries,
+    _augment_identities,
+    _is_newer,
+    _json_object,
+    _login_of,
+    _review_commits,
+    _sha,
+    _submission_ts,
+    _thread_findings,
+    _timestamp,
+    has_augment_activity,
+    has_reviewer_activity,
+)
+from .severity_router import finding_from_comment, remap_severity
 
 REVIEWERS = ("augment", "codex")
 
@@ -80,3 +99,215 @@
 def codex_severity_hint(priority: str | None) -> str | None:
     """Map a Codex priority onto the existing severity hints (P0 critical .. P3 low)."""
     return _CODEX_HINTS.get(priority) if isinstance(priority, str) else None
+
+
+_CODEX_TOKEN = "codex-review-state:v1"
+_CODEX_MARKER = re.compile(
+    r"<!--\s*codex-review-state:v1\s+(.{1,8192}?)\s*-->", re.DOTALL
+)
+_COMPLETED_REVIEW_STATES = ("COMMENTED", "APPROVED", "CHANGES_REQUESTED")
+
+
+def _codex_marker(comment: dict) -> dict | None:
+    """Parse the one bounded ``codex-review-state:v1`` marker; None when invalid."""
+    body = comment.get("body")
+    if not isinstance(body, str) or body.count(_CODEX_TOKEN) != 1:
+        return None
+    match = _CODEX_MARKER.search(body)
+    if not match:
+        return None
+    try:
+        marker = json.loads(match[1], object_pairs_hook=_json_object)
+    except (ValueError, RecursionError):
+        return None
+    review = marker.get("code_review") if isinstance(marker, dict) else None
+    if (
+        not isinstance(review, dict)
+        or not isinstance(review.get("status"), str)
+        or _sha(review.get("commit_sha")) is None
+        or type(review.get("has_any_findings")) is not bool
+    ):
+        return None
+    return review
+
+
+def _comment_updated_at(comment: dict) -> Any:
+    """The summary comment's update time (REST or GraphQL shape); missing -> None."""
+    return comment.get("updated_at", comment.get("updatedAt"))
+
+
+def codex_review_state(
+    payload: dict,
+    contract: Any,
+    *,
+    watermark: Any = None,
+    current_head_sha: str | None = None,
+) -> dict | None:
+    """The completed Codex code review of the expected head, or None (keep polling).
+
+    Evidence is the Codex summary comment's ``codex-review-state:v1`` marker. The
+    newest valid marker wins; two markers with the same latest time are ambiguous.
+    Completion time is the later of that comment's ``updated_at`` and the newest
+    Codex formal review submitted for the head (design section 18, A1/A3). It must
+    be no later than ``observed_at`` and, with a watermark, strictly newer than it.
+    """
+    if not isinstance(payload, dict):
+        return None
+    identities = reviewer_identities(contract, "codex")
+    head = _sha(
+        current_head_sha if current_head_sha is not None else payload.get("head_sha")
+    )
+    observed = _timestamp(payload.get("observed_at"))
+    if not identities or head is None or observed is None:
+        return None
+    candidates = []
+    for comment in _augment_entries(payload.get("comments"), identities):
+        body = comment.get("body")
+        if not isinstance(body, str) or _CODEX_TOKEN not in body:
+            continue
+        marker, updated = (
+            _codex_marker(comment),
+            _timestamp(_comment_updated_at(comment)),
+        )
+        if marker is None or updated is None:
+            return None  # recognisable but invalid evidence never falls back
+        candidates.append((updated, marker))
+    if not candidates:
+        return None
+    latest = max(updated for updated, _ in candidates)
+    newest = [marker for updated, marker in candidates if updated == latest]
+    if len(newest) != 1:
+        return None
+    marker = newest[0]
+    if marker["status"] != "completed" or _sha(marker["commit_sha"]) != head:
+        return None
+    review_times = []
+    for review in _augment_entries(payload.get("reviews"), identities):
+        if review.get("state") not in _COMPLETED_REVIEW_STATES:
+            continue
+        if not any(_sha(commit) == head for commit in _review_commits(review)):
+            continue
+        submitted = _timestamp(_submission_ts(review))
+        if submitted is None:
+            return None
+        review_times.append(submitted)
+    completed_at = max([latest, *review_times])
+    if completed_at > observed:
+        return None
+    if watermark is not None and not _is_newer(completed_at, watermark):
+        return None
+    return {
+        "completed_at": completed_at,
+        "has_any_findings": marker["has_any_findings"],
+        "head_review": bool(review_times),
+        "head_sha": head,
+    }
+
+
+def _codex_selection(
+    payload: dict, contract: Any, watermark: Any, current_head_sha: str | None
+) -> tuple[str, list[dict]]:
+    if not isinstance(payload, dict) or not all(
+        payload.get(key) is True for key in _COMPLETENESS
+    ):
+        return STATE_POLLING, []
+    state = codex_review_state(
+        payload, contract, watermark=watermark, current_head_sha=current_head_sha
+    )
+    if state is None:
+        return STATE_POLLING, []
+    roots = _thread_findings(
+        payload.get("threads"),
+        contract,
+        None,
+        reviewer_identities(contract, "codex"),
+        completed_at=state["completed_at"],
+    )
+    if roots is None:
+        return STATE_POLLING, []
+    if roots:
+        selected = []
+        for root in roots:
+            priority = parse_codex_priority(root.get("body"))
+            selected.append(
+                {
+                    **root,
+                    "reviewer": "codex",
+                    "codex_priority": priority,
+                    "severity_hint": codex_severity_hint(priority),
+                }
+            )
+        return STATE_FINDINGS, selected
+    if not state["has_any_findings"] or state["head_review"]:
+        return STATE_CLEAN, []
+    return STATE_POLLING, []  # findings promised but not yet visible
+
+
+def classify_codex(
+    payload: dict,
+    contract: Any,
+    *,
+    watermark: Any = None,
+    current_head_sha: str | None = None,
+) -> str:
+    """Codex gate state: ``polling`` / ``clean`` / ``findings`` (never ``declined``)."""
+    return _codex_selection(payload, contract, watermark, current_head_sha)[0]
+
+
+def codex_finding_comments(
+    payload: dict,
+    contract: Any,
+    *,
+    watermark: Any = None,
+    current_head_sha: str | None = None,
+) -> list[dict]:
+    """Unresolved Codex-rooted roots for a ``findings`` state, same selection rules
+    as Augment, each with ``reviewer``, ``codex_priority`` and ``severity_hint``."""
+    return _codex_selection(payload, contract, watermark, current_head_sha)[1]
+
+
+def list_review_threads(payload: dict, contract: Any) -> list[dict]:
+    """Every Augment- or Codex-rooted review thread, resolved or not, for reports."""
+    threads = payload.get("threads") if isinstance(payload, dict) else None
+    owners = {name: reviewer_identities(contract, name) for name in REVIEWERS}
+    rows = []
+    for thread in threads if isinstance(threads, list) else []:
+        connection = thread.get("comments") if isinstance(thread, dict) else None
+        nodes = connection.get("nodes") if isinstance(connection, dict) else None
+        if not isinstance(nodes, list) or not nodes or not isinstance(nodes[0], dict):
+            continue
+        root = nodes[0]
+        reviewer = next(
+            (n for n, ids in owners.items() if _login_of(root) in ids), None
+        )
+        if reviewer is None:
+            continue
+        priority = (
+            parse_codex_priority(root.get("body")) if reviewer == "codex" else None
+        )
+        raw = {
+            "path": root.get("path", thread.get("path")),
+            "line": root.get("line", thread.get("line")),
+            "original_line": root.get("originalLine", thread.get("originalLine")),
+            "body": root.get("body"),
+            "reviewer": reviewer,
+            "severity_hint": codex_severity_hint(priority),
+        }
+        try:
+            severity = remap_severity(finding_from_comment(raw)).remapped_severity.value
+        except ValueError:
+            severity = None
+        rows.append(
+            {
+                "reviewer": reviewer,
+                "path": raw["path"],
+                "line": raw["line"],
+                "original_line": raw["original_line"],
+                "is_resolved": thread.get("isResolved"),
+                "priority": priority,
+                "severity": severity,
+                "thread_id": thread.get("id"),
+                "comment_id": root.get("databaseId"),
+            }
+        )
+    return rows
diff --git a/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t7-check.py b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t7-check.py
new file mode 100644
index 00000000..0a244da9
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t7-check.py
@@ -0,0 +1,73 @@
+"""T7 check: Codex completion, gate states and roots on recorded PR 334/336 snapshots."""
+import copy, json, re, sys
+from superclaude.pr_submit import DetectionContract
+from superclaude.pr_submit.reviewers import classify_codex, codex_finding_comments, codex_review_state
+
+A = sys.argv[1]
+C = DetectionContract.load()
+s336 = json.load(open(f"{A}/t7-pr336-snapshot.json")); s334 = json.load(open(f"{A}/t7-pr334-snapshot.json"))
+
+def marker_sha(snap):
+    for c in snap["comments"]:
+        m = re.search(r'codex-review-state:v1 (\{.*?\}\}) -->', c["body"])
+        if m:
+            return json.loads(m[1])["code_review"]["commit_sha"]
+
+def at_review_head(snap, unresolve=False):
+    s = copy.deepcopy(snap); s["head_sha"] = marker_sha(s)
+    if unresolve:
+        for t in s["threads"]:
+            if t["comments"]["nodes"][0]["author"]["login"].startswith("chatgpt-codex"):
+                t["isResolved"] = False
+    return s
+
+results = []
+def check(name, got, want):
+    results.append(got == want); print(f"{'PASS' if got == want else 'FAIL'} {name}: got={got!r} want={want!r}")
+
+p334 = at_review_head(s334)
+check("PR334 shape (completed, no findings, no Codex review) -> clean", classify_codex(p334, C), "clean")
+p336 = at_review_head(s336, unresolve=True)
+check("PR336 shape (3 unresolved P2 roots) -> findings", classify_codex(p336, C), "findings")
+roots = codex_finding_comments(p336, C)
+check("PR336 roots count", len(roots), 3)
+check("PR336 roots reviewer/hint", {(r["reviewer"], r["severity_hint"], r["codex_priority"]) for r in roots}, {("codex", "medium", "P2")})
+p336r = at_review_head(s336)
+check("resolved-only threads + Codex review on head -> clean", classify_codex(p336r, C), "clean")
+check("live head (marker is for an older commit) -> polling", classify_codex(s336, C), "polling")
+
+def mutate_marker(snap, fn):
+    s = copy.deepcopy(snap)
+    for c in s["comments"]:
+        if "codex-review-state:v1" in c["body"]:
+            fn(c)
+    return s
+def set_status(c, st):
+    c["body"] = c["body"].replace('"status":"completed"', f'"status":"{st}"', 1)
+check("running status -> polling", classify_codex(mutate_marker(p336, lambda c: set_status(c, "running")), C), "polling")
+check("wrong head -> polling", classify_codex(p336, C, current_head_sha="0" * 40), "polling")
+dup = copy.deepcopy(p336); dup["comments"].append(copy.deepcopy([c for c in p336["comments"] if "codex-review-state" in c["body"]][0]))
+check("two summary markers with the same time -> polling", classify_codex(dup, C), "polling")
+newer = copy.deepcopy(dup); newer["comments"][-1]["updated_at"] = "2026-10-31T16:30:00Z"; newer["observed_at"] = "2026-10-31T23:00:00Z"
+check("A3: two markers, newest valid wins -> findings", classify_codex(newer, C), "findings")
+check("malformed JSON -> polling", classify_codex(mutate_marker(p336, lambda c: c.update(body=c["body"].replace('{"code_review"', '{"code_review" x', 1))), C), "polling")
+check("duplicate JSON key -> polling", classify_codex(mutate_marker(p336, lambda c: c.update(body=c["body"].replace('{"code_review":', '{"code_review":{},"code_review":', 1))), C), "polling")
+late = copy.deepcopy(p336); late["observed_at"] = "2026-10-31T15:59:00Z"
+check("completion after observed_at -> polling", classify_codex(late, C), "polling")
+check("completion not newer than watermark -> polling", classify_codex(p336, C, watermark="2026-10-31T23:59:59Z"), "polling")
+promised = mutate_marker(p334, lambda c: c.update(body=c["body"].replace('"has_any_findings":false', '"has_any_findings":true', 1)))
+check("has_any_findings true, no roots, no Codex review -> polling", classify_codex(promised, C), "polling")
+# A1: a root created after the marker edit but no later than the review submission is still selected.
+a1 = copy.deepcopy(p336)
+for c in a1["comments"]:
+    if "codex-review-state:v1" in c["body"]:
+        c["updated_at"] = "2026-10-31T15:57:20Z"
+st = codex_review_state(a1, C)
+check("A1: completion = later of marker and review (review 15:57:28)", st and st["completed_at"].isoformat(), "2026-10-31T15:57:28+00:00")
+for r in a1["reviews"]:
+    if r["user"]["login"].startswith("chatgpt-codex"):
+        r["submitted_at"] = "2026-10-31T15:57:40Z"
+check("A1: roots created after the marker edit still selected via the review time", classify_codex(a1, C), "findings")
+flags = copy.deepcopy(p336); flags["threads_ok"] = False
+check("incomplete snapshot -> polling", classify_codex(flags, C), "polling")
+sys.exit(0 if all(results) else 1)
diff --git a/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t7-check.log b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t7-check.log
new file mode 100644
index 00000000..70a7841b
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t7-check.log
@@ -0,0 +1,19 @@
+PASS PR334 shape (completed, no findings, no Codex review) -> clean: got='clean' want='clean'
+PASS PR336 shape (3 unresolved P2 roots) -> findings: got='findings' want='findings'
+PASS PR336 roots count: got=3 want=3
+PASS PR336 roots reviewer/hint: got={('codex', 'medium', 'P2')} want={('codex', 'medium', 'P2')}
+PASS resolved-only threads + Codex review on head -> clean: got='clean' want='clean'
+PASS live head (marker is for an older commit) -> polling: got='polling' want='polling'
+PASS running status -> polling: got='polling' want='polling'
+PASS wrong head -> polling: got='polling' want='polling'
+PASS two summary markers with the same time -> polling: got='polling' want='polling'
+PASS A3: two markers, newest valid wins -> findings: got='findings' want='findings'
+PASS malformed JSON -> polling: got='polling' want='polling'
+PASS duplicate JSON key -> polling: got='polling' want='polling'
+PASS completion after observed_at -> polling: got='polling' want='polling'
+PASS completion not newer than watermark -> polling: got='polling' want='polling'
+PASS has_any_findings true, no roots, no Codex review -> polling: got='polling' want='polling'
+PASS A1: completion = later of marker and review (review 15:57:28): got='2026-10-31T15:57:28+00:00' want='2026-10-31T15:57:28+00:00'
+PASS A1: roots created after the marker edit still selected via the review time: got='findings' want='findings'
+PASS incomplete snapshot -> polling: got='polling' want='polling'
+rc=0
diff --git a/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t7-dry-list.py b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t7-dry-list.py
new file mode 100644
index 00000000..e0ee6cd2
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t7-dry-list.py
@@ -0,0 +1,8 @@
+"""Read-only dry check: list review threads of a live poll snapshot read from stdin."""
+import json, sys
+from superclaude.pr_submit import DetectionContract
+from superclaude.pr_submit.reviewers import classify_codex, list_review_threads, reviewer_activity
+snap = json.load(sys.stdin); c = DetectionContract.load()
+print(f"PR {snap['pr']} head={snap['head_sha'][:8]} flags={snap['reviews_ok']},{snap['comments_ok']},{snap['threads_ok']} activity={reviewer_activity(snap, c)} codex_state_at_head={classify_codex(snap, c)}")
+for row in list_review_threads(snap, c):
+    print(f"  {row['reviewer']:7} {row['path']}:{row['line']}/{row['original_line']} resolved={row['is_resolved']} priority={row['priority']} severity={row['severity']} comment={row['comment_id']}")
diff --git a/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t7-dry-check-pr336.txt b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t7-dry-check-pr336.txt
new file mode 100644
index 00000000..9220c62e
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t7-dry-check-pr336.txt
@@ -0,0 +1,21 @@
+$ scripts/poll-augment-review.sh --pr 336 --repo IronbellyOrg/IronClaude | uv run python t7-dry-list.py
+PR 336 head=d40ed729 flags=True,True,True activity={'augment': True, 'codex': True} codex_state_at_head=polling
+  codex   src/superclaude/skills/sc-impact-protocol/SKILL.md:None/41 resolved=True priority=P2 severity=Medium comment=4432330726
+  codex   src/superclaude/skills/sc-impact-protocol/SKILL.md:None/48 resolved=True priority=P2 severity=Medium comment=4432330727
+  codex   src/superclaude/skills/sc-impact-protocol/SKILL.md:None/63 resolved=True priority=P2 severity=Medium comment=4432330729
+  augment src/superclaude/skills/sc-impact-protocol/SKILL.md:None/41 resolved=True priority=None severity=Medium comment=4432345484
+  augment src/superclaude/skills/sc-impact-protocol/SKILL.md:None/48 resolved=True priority=None severity=Medium comment=4432345490
+  augment src/superclaude/skills/sc-impact-protocol/SKILL.md:65/63 resolved=True priority=None severity=Medium comment=4432345493
+  augment src/superclaude/skills/sc-impact-protocol/SKILL.md:23/23 resolved=True priority=None severity=Medium comment=4432345496
+$ scripts/poll-augment-review.sh --pr 335 --repo IronbellyOrg/IronClaude | uv run python t7-dry-list.py
+PR 335 head=72c469f6 flags=True,True,True activity={'augment': True, 'codex': True} codex_state_at_head=polling
+  codex   .dev/codegraph-migration/specs/followup-codegraph-release-monitor-spec.md:None/141 resolved=True priority=P2 severity=Medium comment=4432067304
+  codex   .dev/codegraph-migration/specs/followup-codegraph-release-monitor-spec.md:None/126 resolved=True priority=P2 severity=Medium comment=4432067307
+  augment .dev/codegraph-migration/specs/followup-codegraph-release-monitor-spec.md:None/141 resolved=True priority=None severity=High comment=4432077161
+  augment .dev/codegraph-migration/specs/followup-codegraph-release-monitor-spec.md:None/122 resolved=True priority=None severity=Medium comment=4432077165
+  augment .dev/codegraph-migration/specs/followup-codegraph-release-monitor-spec.md:None/223 resolved=True priority=None severity=Medium comment=4432077168
+  augment .dev/codegraph-migration/specs/followup-codegraph-release-monitor-spec.md:None/133 resolved=True priority=None severity=High comment=4432284909
+  augment .dev/codegraph-migration/specs/followup-codegraph-release-monitor-spec.md:None/142 resolved=True priority=None severity=Medium comment=4432284914
+  augment .dev/codegraph-migration/specs/followup-codegraph-release-monitor-spec.md:None/147 resolved=True priority=None severity=High comment=4432284917
+  augment .dev/codegraph-migration/specs/followup-codegraph-release-monitor-spec.md:133/133 resolved=False priority=None severity=Low comment=4432441301
+rc=0
diff --git a/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t7-test.log b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t7-test.log
new file mode 100644
index 00000000..71903eb4
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/artifacts/t7-test.log
@@ -0,0 +1,54 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 4.3.5
+benchmark: 5.3.0 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
+rootdir: /home/coder/workspaces/IronClaude/.dev/worktrees/pr-submit-codex
+configfile: pyproject.toml
+plugins: superclaude-4.3.5, benchmark-5.3.0, anyio-4.15.1, cov-7.1.0
+collected 647 items
+
+tests/pr_submit/test_auggie_fallback.py ............                     [  1%]
+tests/pr_submit/test_augment_review_remediation.py .......               [  2%]
+tests/pr_submit/test_autonomy_gates.py .......                           [  4%]
+tests/pr_submit/test_ci_classify.py ....................                 [  7%]
+tests/pr_submit/test_contract_setup_diagnosis.py ..............          [  9%]
+tests/pr_submit/test_contract_setup_evidence.py .....................    [ 12%]
+tests/pr_submit/test_contract_setup_pr_submit_integration.py ......      [ 13%]
+tests/pr_submit/test_contract_setup_questions.py .........               [ 14%]
+tests/pr_submit/test_contract_setup_validation.py .............          [ 16%]
+tests/pr_submit/test_contract_setup_writer.py ................           [ 19%]
+tests/pr_submit/test_cosmos_poll.py .................................... [ 24%]
+...............................................................          [ 34%]
+tests/pr_submit/test_cosmos_protocol.py ...............                  [ 36%]
+tests/pr_submit/test_cosmos_review.py .................................. [ 42%]
+........................................................................ [ 53%]
+                                                                         [ 53%]
+tests/pr_submit/test_crash_recovery.py ................                  [ 55%]
+tests/pr_submit/test_detection_contract.py ............................. [ 60%]
+.....                                                                    [ 61%]
+tests/pr_submit/test_edge_cases.py ...................                   [ 63%]
+tests/pr_submit/test_finding_verify.py ...                               [ 64%]
+tests/pr_submit/test_gate_helper_coverage.py ...........                 [ 66%]
+tests/pr_submit/test_gate_helper_differentials.py ...................... [ 69%]
+                                                                         [ 69%]
+tests/pr_submit/test_idempotency.py ......                               [ 70%]
+tests/pr_submit/test_loop_guard.py .............                         [ 72%]
+tests/pr_submit/test_monitor_arm.py ...                                  [ 72%]
+tests/pr_submit/test_pre_pr_checks.py .................................. [ 78%]
+.....                                                                    [ 78%]
+tests/pr_submit/test_rate_limit.py ....                                  [ 79%]
+tests/pr_submit/test_reply_resolve.py ..........                         [ 81%]
+tests/pr_submit/test_review_retrigger.py .......                         [ 82%]
+tests/pr_submit/test_run_log.py ............                             [ 84%]
+tests/pr_submit/test_setup_questions_resolution.py ....                  [ 84%]
+tests/pr_submit/test_severity_router.py ............................     [ 89%]
+tests/pr_submit/test_silence.py .................                        [ 91%]
+tests/pr_submit/test_skill_parse.py ..............                       [ 93%]
+tests/pr_submit/test_static_grep.py ...................                  [ 96%]
+tests/pr_submit/test_timeout.py .....                                    [ 97%]
+tests/pr_submit/test_troubleshoot_seed.py ....                           [ 98%]
+tests/pr_submit/test_validated_not_verified.py ...                       [ 98%]
+tests/pr_submit/test_validation_gate.py .........                        [100%]
+
+============================= 647 passed in 14.33s =============================
+rc=0
Delta diff from the previous reviewed tree (empty on the first review): --- a/src/superclaude/pr_submit/reviewers.py
+++ b/src/superclaude/pr_submit/reviewers.py
@@ -132,10 +132,8 @@
 
 
 def _comment_updated_at(comment: dict) -> Any:
-    for key in ("updated_at", "updatedAt", "created_at", "createdAt"):
-        if key in comment:
-            return comment[key]
-    return None
+    """The summary comment's update time (REST or GraphQL shape); missing -> None."""
+    return comment.get("updated_at", comment.get("updatedAt"))
 
 
 def codex_review_state(
Earlier blocking findings of this start (empty on the first review): F1.1 sev=blocking trigger=B4 ac=scope at=src/superclaude/pr_submit/reviewers.py:135 anchor="The design file .dev/pr-submit-codex/design/pr-submit-codex-design.md is the specification; do not add behaviour it does not describe." chk=n,n,n,y family=codex-completion-time fix=read only updated_at/updatedAt; missing time stays polling first=A1 origin=new: _comment_updated_at falls back to created_at
Saved-probe re-check hit locations (may be empty): (no hits)

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
