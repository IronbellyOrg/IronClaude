cccce2bd79ecb8ae35817e8ebfc3990c7b5f6c2b
Review one task for spec compliance.

Task brief: ## Task 4: Select the default through a pointer file instead of a hard-coded file name

Depends on: Task 2, Task 3

Add `src/superclaude/cli/review/data/review-default.json` with content `{"schema": "review-default/1", "template": "wonsol"}`. In `load_panel` of `src/superclaude/cli/review/panel.py` (the `else _default("review-panel.default.json")` branch, line 459 at planning time) replace the hard-coded file name with a new function `default_template_name()` that reads the pointer file through `_default`, checks `schema` and that `template` matches `_PACKAGED_NAME`, and returns that name as a string; `load_panel` calls `packaged_panel(name)` on it and validates the result with `validate_panel`, as the `@name` branch does (finding F4: one return contract for `default_template_name()`, the name string). A pointer with a bad schema, a bad name or a name with no packaged template raises `ValueError` that names the pointer file. The lookup order of `find_path` stays untouched: explicit path, `SUPERCLAUDE_REVIEW_PANEL`, `.superclaude/review-panel.json` of the project, then of the home directory, then the packaged default. Callers that must keep working: `resolve_cmd` in `src/superclaude/cli/review/panel_cmd.py`, `scripts/reflect_shadow_exit.py` (it uses `load_tiers`, so it needs no code change but its tests must pass), and the `load_panel` callers in `tests/review/test_review_panel.py`, `tests/review/test_review_panel_live7.py` and `tests/review/test_review_reflect_templates.py`.

Acceptance criteria (ids):
T4.AC1: With no flag, no environment variable and no `.superclaude/review-panel.json`, `pnl.load_panel()["template_id"] == "wonsol"` and the file `src/superclaude/cli/review/data/review-default.json` is the only place that names it; changing its `template` to `classic` makes `pnl.load_panel()["template_id"] == "classic"` with no code change.
T4.AC2: A pointer naming an unknown template, a malformed name or a wrong schema raises `ValueError` mentioning `review-default.json`.
T4.AC3: `find_path` precedence is unchanged: a project `review-panel.json`, a home one, `SUPERCLAUDE_REVIEW_PANEL` and an explicit path still override the pointer (`test_template_lookup_precedence` keeps its order of assertions).
T4.AC4: `uv run superclaude review panel resolve --run-id t1 --env anthropic-only` prints three reviewers (Sonnet plus two Haiku stand-ins); with `--env gateway` it prints the three wonsol models.
Global constraints: ## Constraints

- Work on a new branch cut from `origin/master`, never on the evaluation branch that holds the answer key; open the PR only with `/sc:pr-submit --monitor 3` against `IronbellyOrg/IronClaude`; never stage anything under `.claude/`.
- Edit only under `src/superclaude/cli/review/`, `src/superclaude/skills/`, `src/superclaude/rules/`, `tests/` and `docs/`; run `make sync-dev` after skill or rule edits.
- The product panel chooses models only. The seat lenses, table caps and briefs of the evaluation harness (S = wonder with lenses C5 C6 C8 C2 and cap 8; L1 = sol; L2 = ember) are not part of this change, so only the model mix transfers. The confirming test did not meet its registered bar (found fraction +0.099 and +0.109, lower bounds -0.004 and -0.006; 1.56 times the control's panel time); the owner has ordered the default change as provisional, and the plan must say so in the docs it touches.
- `validate_panel` in `src/superclaude/cli/review/panel.py` already allows 1 to 8 reviewers and requires exactly one `fixed` slot; do not change those rules. A template id must not start with `reflect-` (that prefix turns on the reflect profile).
- Keep the strategy and tier-name rules: tier names match `^tier[0-9]{1,2}[a-z]?$`.
Start sha: cccce2bd79ecb8ae35817e8ebfc3990c7b5f6c2b
Diff against the start snapshot: diff --git a/src/superclaude/cli/review/panel.py b/src/superclaude/cli/review/panel.py
index e99d26d0f..7f576d84a 100644
--- a/src/superclaude/cli/review/panel.py
+++ b/src/superclaude/cli/review/panel.py
@@ -444,6 +444,23 @@ def packaged_panel(name: str) -> dict:
         ) from exc
 
 
+def default_template_name() -> str:
+    """Name of the packaged panel template the pointer file review-default.json selects as the default."""
+    ptr = _default("review-default.json")
+    name = ptr.get("template") if isinstance(ptr, dict) else None
+    if (
+        not isinstance(ptr, dict)
+        or ptr.get("schema") != "review-default/1"
+        or not isinstance(name, str)
+        or not _PACKAGED_NAME.match(name)
+    ):
+        raise ValueError(
+            "invalid review-default.json: need schema 'review-default/1' and a 'template' "
+            f"packaged-panel name (got {ptr!r})"
+        )
+    return name
+
+
 def load_panel(path: str | None = None) -> dict:
     ref = path or os.environ.get("SUPERCLAUDE_REVIEW_PANEL") or ""
     if ref.startswith("@"):
@@ -453,11 +470,14 @@ def load_panel(path: str | None = None) -> dict:
             raise ValueError(f"invalid packaged panel {ref}: " + "; ".join(errors))
         return obj
     found = find_path("panel", path)
-    obj = (
-        json.loads(found.read_text(encoding="utf-8"))
-        if found
-        else _default("review-panel.default.json")
-    )
+    if found:
+        obj = json.loads(found.read_text(encoding="utf-8"))
+    else:
+        name = default_template_name()
+        try:
+            obj = packaged_panel(name)
+        except ValueError as exc:
+            raise ValueError(f"review-default.json names '{name}': {exc}") from exc
     errors = validate_panel(obj)
     if errors:
         raise ValueError(

--- new untracked file src/superclaude/cli/review/data/review-default.json ---
{"schema": "review-default/1", "template": "wonsol"}


Codegraph context: index_state: fresh, checked_at: 2026-11-17T21:16:22Z, worktree_root: /home/coder/workspaces/worktrees/IronClaude/wonsol-default, projectPath: same. Call codegraph only when index_state: fresh, never to widen scope. Q2b dependents of load_panel (signature unchanged, behaviour of the no-argument default changed) not in the touched set: resolve_cmd (src/superclaude/cli/review/panel_cmd.py:64), tests/review/test_review_panel.py (test_template_lookup_precedence, tpl fixture), tests/review/test_review_panel_live7.py, tests/review/test_review_reflect_templates.py; these test files are edited by Task 5, not this task.
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
