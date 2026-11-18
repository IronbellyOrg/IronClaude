d3cffb20d6c0f7844a8ab0bb7dbad1f2d33e561c
Review one task for spec compliance.

Task brief: ## Task 6: Update the documentation and rule text that describe the default panel

Depends on: Task 5

Edit `docs/reference/review-panel-live7.md` so it no longer says the default is the 4-reviewer panel and describes the pointer file, the `@wonsol` and `@classic` templates, the new tiers, the `anthropic-only` resolution and the provisional status with the confirming-test numbers of the Constraints section. Read `src/superclaude/skills/sc-reflect-protocol/SKILL.md`, `src/superclaude/rules/prompts/document_review_loop_prompts.md` and `tests/review/test_review_rules_text.py` for statements about the default panel size or composition (the Task 4 grep found `review panel resolve` and `review-panel.json` text there) and change only the statements that are now false; keep `tests/review/test_review_rules_text.py` passing. Do not edit `src/superclaude/rules/prompts/document_review_loop_prompts.md` or its plugin copy in this task: its sentence stays true, and the held stage 4 of the blocker-classification program edits that file family (PR 605 note), which would otherwise collide with this task. Run `make sync-dev` and `make verify-sync`.

Acceptance criteria (ids):
T6.AC1: `grep -rn "2x Tier 3\|Tier 1b is the fixed anchor\|four reviewers\|4 reviewers" src docs tests` finds no sentence that calls the 4-reviewer panel the product default.
T6.AC2: `uv run pytest tests/review/test_review_rules_text.py -q` passes and `make verify-sync` exits 0; no file under `.claude/` is staged.
T6.AC3: The sentence in `src/superclaude/rules/prompts/document_review_loop_prompts.md` that tells the review loop to run the reviewers `superclaude review panel resolve` prints (the one real consumer of the default panel found by search) stays true, and the docs of Task 6 state that the re-review reviewer is the anchor, which changes from the Tier 1b model (Sonnet) to `muse-wonder-1.0` in the `gateway` environment and stays `claude-sonnet-5-5` in `anthropic-only`.
T6.AC4: The PR description names the confirming-test result (not confirmed by the registered rule) and that the model mix, not the evaluation seat lenses, is what ships.

Orchestrator note (context, not an AC change): the implementer read src/superclaude/skills/sc-reflect-protocol/SKILL.md, src/superclaude/rules/prompts/document_review_loop_prompts.md and tests/review/test_review_rules_text.py and found no statement about the default panel's size or composition that is now false (the rules sentence says "a panel for a first review, one reviewer for a re-review by default"; the skill always passes an explicit @reflect-* template), so none of them was edited. The AC grep still lists the byte-identical frozen copy tests/review/fixtures/review-panel.default.frozen.json (required byte-for-byte by Task 3.AC3), the @classic template description and the @live7 description; judge whether any hit calls the 4-reviewer panel the CURRENT product default. The PR description (last AC) is written at PR time, which is outside this task and this run; judge it as not applicable to the diff unless the plan text makes it a deliverable of this task.
Global constraints: ## Constraints

- Work on a new branch cut from `origin/master`, never on the evaluation branch that holds the answer key; open the PR only with `/sc:pr-submit --monitor 3` against `IronbellyOrg/IronClaude`; never stage anything under `.claude/`.
- Edit only under `src/superclaude/cli/review/`, `src/superclaude/skills/`, `src/superclaude/rules/`, `tests/` and `docs/`; run `make sync-dev` after skill or rule edits.
- The product panel chooses models only. The seat lenses, table caps and briefs of the evaluation harness (S = wonder with lenses C5 C6 C8 C2 and cap 8; L1 = sol; L2 = ember) are not part of this change, so only the model mix transfers. The confirming test did not meet its registered bar (found fraction +0.099 and +0.109, lower bounds -0.004 and -0.006; 1.56 times the control's panel time); the owner has ordered the default change as provisional, and the plan must say so in the docs it touches.
- `validate_panel` in `src/superclaude/cli/review/panel.py` already allows 1 to 8 reviewers and requires exactly one `fixed` slot; do not change those rules. A template id must not start with `reflect-` (that prefix turns on the reflect profile).
- Keep the strategy and tier-name rules: tier names match `^tier[0-9]{1,2}[a-z]?$`.
Start sha: d3cffb20d6c0f7844a8ab0bb7dbad1f2d33e561c
Diff against the start snapshot: diff --git a/docs/reference/review-panel-live7.md b/docs/reference/review-panel-live7.md
index 928432a29..a317969c6 100644
--- a/docs/reference/review-panel-live7.md
+++ b/docs/reference/review-panel-live7.md
@@ -12,7 +12,25 @@ Issue #346. This page records the panel shape for the live gateway, the `tier2b`
 | `t3` | `tier3` | 2 | random | parallel reviewers |
 | `t4` | `tier4` | 2 | random | parallel reviewers drawn from GPT-6 Luna, Claude Haiku 5.5 and Grok 4.7 (`distinct_across_slots` keeps the two draws different) |
 
-Seven reviewers, one Sonnet anchor and six parallel. The file is `src/superclaude/cli/review/data/review-panel.live7.json`; the packaged default panel (4 reviewers) is unchanged.
+Seven reviewers, one Sonnet anchor and six parallel. The file is `src/superclaude/cli/review/data/review-panel.live7.json`; `@live7` is unchanged by the default-panel change described in the next section.
+
+## The default panel (`@wonsol`, provisional)
+
+With no template argument, no `SUPERCLAUDE_REVIEW_PANEL` and no `review-panel.json`, `superclaude review panel resolve` resolves the 3-reviewer `wonsol` panel. The default is chosen by reference: `src/superclaude/cli/review/data/review-default.json` (`{"schema": "review-default/1", "template": "wonsol"}`) names a packaged template, and `default_template_name()` in `src/superclaude/cli/review/panel.py` reads it. Changing `template` to `classic` switches the default back with no code change; a pointer with a wrong schema, a malformed name or a name with no packaged template fails with an error that names `review-default.json`. The lookup order is unchanged: explicit path, `SUPERCLAUDE_REVIEW_PANEL`, `.superclaude/review-panel.json` of the project, `~/.superclaude/review-panel.json`, then the pointer.
+
+| template | reviewers | what it is |
+|---|---|---|
+| `@wonsol` (the default) | 3: `t5a` anchor, `t5b`, `t5c` | `muse-wonder-1.0` (fixed anchor, falls back to `claude-sonnet-5-5`), `gpt-6.1-sol`, `muse-ember-1.0` |
+| `@classic` | 4: `t1b` anchor, `t2`, `t3` x2 | the previous production default (1x Tier 1b anchor + 1x Tier 2 + 2x Tier 3) |
+| `@live7` | 7 | the panel described above |
+
+The three `wonsol` slots use the new tiers `tier5a` (`muse-wonder-1.0`, then `claude-sonnet-5-5`), `tier5b` (`gpt-6.1-sol` only) and `tier5c` (`muse-ember-1.0` only) in `review-tiers.default.json`. Each of `tier5b` and `tier5c` lists exactly one model so that its `random` slot is deterministic.
+
+- In the `gateway` environment the default resolves to `muse-wonder-1.0`, `gpt-6.1-sol` and `muse-ember-1.0`.
+- In the `anthropic-only` environment it resolves to `claude-sonnet-5-5` for the anchor and `claude-haiku-5-5` stand-ins for the other two, so that environment runs no wonder, sol or ember model.
+- A re-review (`--kind re-review`) resolves only the anchor. That reviewer changes from the Tier 1b model (Claude Sonnet 5.5) to `muse-wonder-1.0` in the `gateway` environment and stays `claude-sonnet-5-5` in `anthropic-only`.
+
+**Status: provisional.** The owner ordered this default change although the confirming test did not meet its pre-registered bar: the found-fraction lead over the control was +0.099 and +0.109 with lower bounds -0.004 and -0.006, and the panel took 1.56 times the control's time. Only the model mix ships. The seat lenses, table caps and briefs of the evaluation harness are not part of this change, so the product panel chooses models only.
 
 ## What the experiments support
 
@@ -20,7 +38,7 @@ The experiments ran this shape with Claude Haiku 5.5 standing in for every non-S
 
 | panel | fixed per run (of 44) | weighted residual |
 |---|---|---|
-| 1 Sonnet + 3 Haiku (the default panel's shape) | 15.7 and 15.3 (two batches of 6) | 63.0 and 63.0 |
+| 1 Sonnet + 3 Haiku (the shape of the `@classic` panel, the default before `@wonsol`) | 15.7 and 15.3 (two batches of 6) | 63.0 and 63.0 |
 | 1 Sonnet + 6 Haiku (this shape) | 19.3 and 17.7 (two batches of 6) | 53.0 and 56.8 |
 
 Pooled over both batches the extra Haiku reviewers add about 3 fixed defects per run (p = 0.013); the second batch alone is +2.3 (p = 0.17). These are Haiku stand-ins: the live Tier 2, 2b and 3 models are not Haiku, and Tier 4 mixes GPT-6 Luna, Claude Haiku 5.5 and Grok 4.7 (Haiku 5.5 is a real Tier 4 model). The live-environment evals in `.dev/research/346-review-loop-experiments/p20/live-evals/` exist to measure that.


Codegraph context: index_state: fresh, checked_at: 2026-11-17T21:16:22Z, worktree_root: /home/coder/workspaces/worktrees/IronClaude/wonsol-default, projectPath: same. Call codegraph only when index_state: fresh, never to widen scope. Q2b: docs-only task; no code dependents.
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
