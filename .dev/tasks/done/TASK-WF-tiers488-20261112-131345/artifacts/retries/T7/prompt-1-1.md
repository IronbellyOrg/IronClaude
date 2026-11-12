80ee6e158d37fe93c5965715f435147d36e199d3
Review one task for spec compliance.

Task brief: ## Task 7: Add the CHANGELOG entries

Depends on: Task 3, Task 6

Edit `CHANGELOG.md` under `[Unreleased]`, in or next to the existing "ccsession tiers: Tier 2b, a two-model Tier 3 and a three-model Tier 4 (IronClaude issue 488)" section (line 16). Replace its last bullet ("Not in this change (open in issue 488) ...") with accurate text: the `issue-worker-t3` pin moves to `claude-gw-tier2b` (Terra first, as before); retry ladder rung 0 reads `T2bModel01`; the README describes the 429 fallback in plain words; Haiku 5.5 is recorded as an owner exception, unscored; the `haiku` alias and the historical design and testing docs are unchanged. Keep the merge-order bullet and keep it true: this change still must not merge until the Coder release carrying the T2b slots is installed in every workspace.

Acceptance criteria:
- CHANGELOG.md `[Unreleased]` names the four changes above and no longer lists the pin or the retry rung as open.
- The merge-order bullet is still present.
Global constraints: 
- Master already holds the tier layout (`ccsession-models.json` tier2b, tier3, tier4; review-tiers file; MODEL-TIERS.md rows). Do not change those lists, slots or windows, and do not edit `ccsession-models.json` (so no version bump).
- Do not touch ccsession alias code (`ccsession`, `models.py`, `local-gateway-alias-proxy.py`) or `tests/skills/test_model_alias_policy.py` lines 229-241 (the `haiku` alias stays on its current tier).
- Do not add a Terra-specific 429 rule and do not edit `docs/designs/sc-issue-command.md` or any file under `docs/testing/v5.0.0/sysop/`.
- Edit only `src/` and `plugins/` sources, tests, docs and CHANGELOG; the `.claude/` copies come from `make sync-dev` and are never staged. Installed primitives must not gain any `src/superclaude/...` path.
- Docs follow the writing rules of the repo: plain words, no em dashes.
Start sha: 80ee6e158d37fe93c5965715f435147d36e199d3
Diff against the start snapshot: diff --git a/CHANGELOG.md b/CHANGELOG.md
index e95b2463f..adc9fba37 100644
--- a/CHANGELOG.md
+++ b/CHANGELOG.md
@@ -17,7 +17,10 @@ All notable changes to IronClaude are documented in this file.
 
 - `ccsession-models.json` (2026-11-11.1) adds `tier2b` (`T2bModel01`-`T2bModel04`: GPT-6.1 Terra, GLM-5.3, Qwen3.8 Max, Muse Wonder 1.0), cuts `tier3` to `T3Model01`-`T3Model02` (GLM-5.3, Qwen3.8 Max) and grows `tier4` to `T4Model01`-`T4Model03` (GPT-6 Luna, Claude Haiku 5.5, Grok 4.7), and adds the display name "Claude Haiku 5.5". The models and windows come from the Coder env file; this is the data that names them.
 - **Merge order, do not skip:** this change must reach `master` only after Coder central defaults release `20261110-1` (Coder PR 495) is installed in every workspace, running and stopped. Every launch fetches this file from `master`, and a launch in tier mode stops when a slot the file names is unset ("T2bModel01 is not set (needed by tier2b)"). The Coder member rule gains `tier2b` only after this file is live (Coder release B); until then members' Tier 3 is GLM and Qwen only and Terra is in no member tier.
-- Not in this change (open in issue 488): the `issue-worker-t3` pin, the `haiku` alias, the retry-ladder rung that reads `T3Model01`, and the historical design docs.
+- Owner decisions of 2026-11-12 (issue 488, "accept all"): `issue-worker-t3` is pinned to `claude-gw-tier2b` (GPT-6.1 Terra first, as before the layout change; `effort: low` stays), in its agent file, the `sc-issue-protocol` skill and refs, and the pin tests.
+- Retry-ladder rung 0 in `sc-implement-protocol` `refs/retry.md` (and the `plugins/` copy) now reads `T2bModel01` (GPT-6.1 Terra) instead of `T3Model01`, which now holds glm-5.3, so rung 0 keeps its GPT-family behavior. The primary ladder is active only when all four rung variables are set, so in a workspace without `T2bModel01` the alias fallback ladder applies.
+- The README tier section now says in plain words what a 429 does: the first two go back to Claude Code to retry, the third parks the model and the request moves to the next eligible model in the tier; it is not an immediate retry, and Tier 2b has no Terra-specific rule. `MODEL-TIERS.md` repeats this and records Claude Haiku 5.5 as an owner exception to the placement rules, with status "unscored" (no score invented).
+- Unchanged on purpose: the `haiku` alias (still Tier 2), `ccsession-models.json` (so no version bump), the review-panel `tier2b` list (already filled by the 346 merge and tested), and the historical docs `docs/designs/sc-issue-command.md` and `docs/testing/v5.0.0/sysop/*`, which still describe the old Tier 3.
 
 ### ccsession: retry temporary failures, then switch; named-model fallback (#392)
 
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
