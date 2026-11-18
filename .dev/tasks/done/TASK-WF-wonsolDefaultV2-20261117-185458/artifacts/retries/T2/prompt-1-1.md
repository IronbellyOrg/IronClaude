50dd693c59012e742f155907c7e166f16cc9400c
Review one task for spec compliance.

Task brief: ## Task 2: Add the wonsol panel template

Depends on: Task 1

Create `src/superclaude/cli/review/data/review-panel.wonsol.json` with `schema` `review-panel/1`, `template_id` `wonsol`, `version` `1.0.0`, a description that states the three models and that the choice is provisional, `distinct_across_slots` true, `apply_to` `["first"]` as in the existing default, and three slots: `t5a` (tier `tier5a`, count 1, strategy `fixed`, the anchor), `t5b` (tier `tier5b`, count 1, strategy `random`), `t5c` (tier `tier5c`, count 1, strategy `random`). It is loaded with `@wonsol` through `packaged_panel` in `src/superclaude/cli/review/panel.py`.

Acceptance criteria (ids):
T2.AC1: `pnl.load_panel("@wonsol")` returns the template and `pnl.validate_panel(it, pnl.load_tiers()) == []`; the slot counts sum to 3 and exactly one slot is `fixed`.
T2.AC2: `uv run superclaude review panel resolve --template @wonsol --run-id t1 --env anthropic-only` and `--env gateway` both exit 0 and list three reviewers with ids `t5a-1`, `t5b-1`, `t5c-1`; in `anthropic-only` the anchor is `claude-sonnet-5-5` and the other two are Haiku stand-ins (so that environment does not run wonder, sol or ember).
T2.AC3: `--kind re-review` resolves only the anchor `t5a-1`, the same rule that `live7` follows in `tests/review/test_review_panel_live7.py` (`test_re_review_resolves_only_the_anchor`).
Global constraints: ## Constraints

- Work on a new branch cut from `origin/master`, never on the evaluation branch that holds the answer key; open the PR only with `/sc:pr-submit --monitor 3` against `IronbellyOrg/IronClaude`; never stage anything under `.claude/`.
- Edit only under `src/superclaude/cli/review/`, `src/superclaude/skills/`, `src/superclaude/rules/`, `tests/` and `docs/`; run `make sync-dev` after skill or rule edits.
- The product panel chooses models only. The seat lenses, table caps and briefs of the evaluation harness (S = wonder with lenses C5 C6 C8 C2 and cap 8; L1 = sol; L2 = ember) are not part of this change, so only the model mix transfers. The confirming test did not meet its registered bar (found fraction +0.099 and +0.109, lower bounds -0.004 and -0.006; 1.56 times the control's panel time); the owner has ordered the default change as provisional, and the plan must say so in the docs it touches.
- `validate_panel` in `src/superclaude/cli/review/panel.py` already allows 1 to 8 reviewers and requires exactly one `fixed` slot; do not change those rules. A template id must not start with `reflect-` (that prefix turns on the reflect profile).
- Keep the strategy and tier-name rules: tier names match `^tier[0-9]{1,2}[a-z]?$`.
Start sha: 50dd693c59012e742f155907c7e166f16cc9400c
Diff against the start snapshot: 
--- new untracked file src/superclaude/cli/review/data/review-panel.wonsol.json ---
{
  "schema": "review-panel/1",
  "template_id": "wonsol",
  "version": "1.0.0",
  "description": "Production review panel (provisional): 3 parallel independent reviewers on muse-wonder-1.0 (fixed anchor, falls back to claude-sonnet-5-5), gpt-6.1-sol and muse-ember-1.0. The choice is provisional by owner order: the confirming test did not meet its pre-registered bar. Only the model mix ships, not the evaluation seat lenses.",
  "distinct_across_slots": true,
  "apply_to": ["first"],
  "slots": [
    {"slot_id": "t5a", "tier": "tier5a", "count": 1, "strategy": "fixed"},
    {"slot_id": "t5b", "tier": "tier5b", "count": 1, "strategy": "random"},
    {"slot_id": "t5c", "tier": "tier5c", "count": 1, "strategy": "random"}
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
