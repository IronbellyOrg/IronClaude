7e9dc9027af96daee66784e943c519d1a2079a6a
Review one task for spec compliance.

Task brief: ## Task 3: Keep the current 4-reviewer default as the packaged template `classic`

Create `src/superclaude/cli/review/data/review-panel.classic.json` with the exact slots, `distinct_across_slots` and `apply_to` of the current `src/superclaude/cli/review/data/review-panel.default.json`, `template_id` `classic`, and a description saying it is the previous production default. Before the delete, copy the old template byte for byte to the test fixture `tests/review/fixtures/review-panel.default.frozen.json` (finding F1: the golden tests resolve the name `default`, and their stored values embed `"template_id":"default"` and its `template_sha256`, so a renamed template cannot reproduce them). Then delete `src/superclaude/cli/review/data/review-panel.default.json` (the default is selected by the pointer of Task 4, so no packaged template keeps the id `default`).

Acceptance criteria (ids):
T3.AC1: `pnl.load_panel("@classic")` has four reviewers (`t1b` 1, `t2` 1, `t3` 2) and resolves in `anthropic-only` to `claude-sonnet-5-5` plus three `claude-haiku-5-5`, exactly as the old default did.
T3.AC2: `grep -rn 'review-panel\.default\|("default"\|"default|' src/superclaude/cli/review tests/review docs` lists exactly these hits and no others at the end of this task (finding F1 and re-review finding N1: the file-name grep alone misses the golden consumers, and a repo-wide grep for the bare word `default` has unrelated hits): `src/superclaude/cli/review/panel.py:459` (rewritten by Task 4), `tests/review/test_review_panel.py:401` and `tests/review/test_review_panel_reflect_profile.py:77` (rewritten by Task 5), and the four `default|...` keys of `tests/review/fixtures/panel-golden-default-live7.json` plus the key of `tests/review/fixtures/panel-golden-packaged-tiers.json` (kept as they are; their consumers are settled in Task 5).
T3.AC3: `tests/review/fixtures/review-panel.default.frozen.json` is byte-identical to `git show HEAD:src/superclaude/cli/review/data/review-panel.default.json` taken before the delete.
Global constraints: ## Constraints

- Work on a new branch cut from `origin/master`, never on the evaluation branch that holds the answer key; open the PR only with `/sc:pr-submit --monitor 3` against `IronbellyOrg/IronClaude`; never stage anything under `.claude/`.
- Edit only under `src/superclaude/cli/review/`, `src/superclaude/skills/`, `src/superclaude/rules/`, `tests/` and `docs/`; run `make sync-dev` after skill or rule edits.
- The product panel chooses models only. The seat lenses, table caps and briefs of the evaluation harness (S = wonder with lenses C5 C6 C8 C2 and cap 8; L1 = sol; L2 = ember) are not part of this change, so only the model mix transfers. The confirming test did not meet its registered bar (found fraction +0.099 and +0.109, lower bounds -0.004 and -0.006; 1.56 times the control's panel time); the owner has ordered the default change as provisional, and the plan must say so in the docs it touches.
- `validate_panel` in `src/superclaude/cli/review/panel.py` already allows 1 to 8 reviewers and requires exactly one `fixed` slot; do not change those rules. A template id must not start with `reflect-` (that prefix turns on the reflect profile).
- Keep the strategy and tier-name rules: tier names match `^tier[0-9]{1,2}[a-z]?$`.
Start sha: 7e9dc9027af96daee66784e943c519d1a2079a6a
Diff against the start snapshot: diff --git a/src/superclaude/cli/review/data/review-panel.default.json b/src/superclaude/cli/review/data/review-panel.default.json
deleted file mode 100644
index 59e3e4a5f..000000000
--- a/src/superclaude/cli/review/data/review-panel.default.json
+++ /dev/null
@@ -1,13 +0,0 @@
-{
-  "schema": "review-panel/1",
-  "template_id": "default",
-  "version": "1.0.0",
-  "description": "Production review panel: 2x Tier 3 + 1x Tier 2 + 1x Tier 1b parallel independent reviewers; Tier 1b is the fixed anchor.",
-  "distinct_across_slots": true,
-  "apply_to": ["first"],
-  "slots": [
-    {"slot_id": "t1b", "tier": "tier1b", "count": 1, "strategy": "fixed"},
-    {"slot_id": "t2", "tier": "tier2", "count": 1, "strategy": "random"},
-    {"slot_id": "t3", "tier": "tier3", "count": 2, "strategy": "random"}
-  ]
-}

--- new untracked file src/superclaude/cli/review/data/review-panel.classic.json ---
{
  "schema": "review-panel/1",
  "template_id": "classic",
  "version": "1.0.0",
  "description": "Previous production review panel (the default before the wonsol panel): 2x Tier 3 + 1x Tier 2 + 1x Tier 1b parallel independent reviewers; Tier 1b is the fixed anchor.",
  "distinct_across_slots": true,
  "apply_to": ["first"],
  "slots": [
    {"slot_id": "t1b", "tier": "tier1b", "count": 1, "strategy": "fixed"},
    {"slot_id": "t2", "tier": "tier2", "count": 1, "strategy": "random"},
    {"slot_id": "t3", "tier": "tier3", "count": 2, "strategy": "random"}
  ]
}

--- new untracked file tests/review/fixtures/review-panel.default.frozen.json ---
{
  "schema": "review-panel/1",
  "template_id": "default",
  "version": "1.0.0",
  "description": "Production review panel: 2x Tier 3 + 1x Tier 2 + 1x Tier 1b parallel independent reviewers; Tier 1b is the fixed anchor.",
  "distinct_across_slots": true,
  "apply_to": ["first"],
  "slots": [
    {"slot_id": "t1b", "tier": "tier1b", "count": 1, "strategy": "fixed"},
    {"slot_id": "t2", "tier": "tier2", "count": 1, "strategy": "random"},
    {"slot_id": "t3", "tier": "tier3", "count": 2, "strategy": "random"}
  ]
}


Codegraph context: index_state: fresh, checked_at: 2026-11-17T21:16:22Z, worktree_root: /home/coder/workspaces/worktrees/IronClaude/wonsol-default, projectPath: same. Call codegraph only when index_state: fresh, never to widen scope. Q2b ran on the Grep/Read floor.
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
