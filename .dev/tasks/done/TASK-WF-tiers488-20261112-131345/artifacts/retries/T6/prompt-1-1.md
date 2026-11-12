645cdd79b41d7fd7e329ff5fbac8ffdcda250b8c
Review one task for spec compliance.

Task brief: ## Task 6: Fix the Tier 2b 429 wording and record the Haiku 5.5 owner exception in MODEL-TIERS.md

Depends on: Task 5

Edit `src/superclaude/skills/ccsession-tag/MODEL-TIERS.md`. In the Tier 2b row (line 42) replace "If GPT-6.1 Terra returns a 429 the request is retried on GLM-5.3 (owner, 2026-11-11)" with wording that matches the README: after repeated 429s the request moves on to GLM-5.3 (first two 429s go back to Claude Code, the third parks Terra), citing the README tier section. In section 5 "How models are placed" (the numbered rules at about lines 157 to 173; do not renumber the rules) add a short note after the list recording that Claude Haiku 5.5 is an owner exception to rules 1 and 2 with status "unscored", placed in Tier 4 by the owner on 2026-11-10 and confirmed 2026-11-12, with no score invented, to be scored later; check that the Tier 4 row, the Haiku 5.5 provider row (about line 122) and the Unscored note (about line 219) use the same status word. Update the "Tiers last changed" bullet at the top to mention the 2026-11-12 decisions (issue worker pin, retry rung 0) without changing the tier contents.

Acceptance criteria:
- `grep -n 'retried on GLM' src/superclaude/skills/ccsession-tag/MODEL-TIERS.md` prints nothing.
- Section 5 contains the owner-exception note with the word "unscored", and the three Haiku 5.5 mentions agree.
Global constraints: 
- Master already holds the tier layout (`ccsession-models.json` tier2b, tier3, tier4; review-tiers file; MODEL-TIERS.md rows). Do not change those lists, slots or windows, and do not edit `ccsession-models.json` (so no version bump).
- Do not touch ccsession alias code (`ccsession`, `models.py`, `local-gateway-alias-proxy.py`) or `tests/skills/test_model_alias_policy.py` lines 229-241 (the `haiku` alias stays on its current tier).
- Do not add a Terra-specific 429 rule and do not edit `docs/designs/sc-issue-command.md` or any file under `docs/testing/v5.0.0/sysop/`.
- Edit only `src/` and `plugins/` sources, tests, docs and CHANGELOG; the `.claude/` copies come from `make sync-dev` and are never staged. Installed primitives must not gain any `src/superclaude/...` path.
- Docs follow the writing rules of the repo: plain words, no em dashes.
Start sha: 645cdd79b41d7fd7e329ff5fbac8ffdcda250b8c
Diff against the start snapshot: diff --git a/src/superclaude/skills/ccsession-tag/MODEL-TIERS.md b/src/superclaude/skills/ccsession-tag/MODEL-TIERS.md
index a9e6db1da..15462cac8 100644
--- a/src/superclaude/skills/ccsession-tag/MODEL-TIERS.md
+++ b/src/superclaude/skills/ccsession-tag/MODEL-TIERS.md
@@ -5,6 +5,8 @@ One place to see which model sits in which tier, and the evals and prices that p
 - **Scores and prices checked:** 2026-09-30 (Muse Wonder rows: 2026-10-14).
 - **Tiers last changed:** 2026-11-11 (owner decisions of 2026-11-10 and 2026-11-11, IronClaude issue 488 and Coder
   issue 494: new Tier 2b, Tier 3 cut to GLM-5.3 and Qwen3.8 Max, Tier 4 adds Claude Haiku 5.5 and Grok 4.7).
+  On 2026-11-12 the owner confirmed Claude Haiku 5.5 in Tier 4 as an exception to the placement rules, pinned
+  `issue-worker-t3` to Tier 2b and moved retry-ladder rung 0 to `T2bModel01`; no tier contents changed that day.
   Before that 2026-10-28 (Tier 1 split into 1a and 1b, GPT-6.1 Sol added to Tier 2, GPT-6 Luna moved to Tier 4).
 - **Where tiers actually take effect:** the Coder workspace env, `IronbellyOrg/Coder` file
   `templates/VSCode-AIDev02/aienv.d/defaults.sh` (`T<N>Model0<M>` slots, for example `T1aModel01`). ccsession profiles live
@@ -39,7 +41,7 @@ individual entries): 850K for each model except Grok 4.7 (500K).
 | **Tier 1a** | Claude frontier. | Claude Opus 5.5 (`claude-opus-5-5`), Claude Sonnet 5.5 (`claude-sonnet-5-5`) | 56.0-57.6 | $2.00-4.00 / $0.20 / $10.00-20.00 | 850K | `claude` (Opus) |
 | **Tier 1b** | Frontier mix. Start tier for roles above Member. | Claude Sonnet 5.5 (`claude-sonnet-5-5`), GPT-6.1 Sol (`gpt-6.1-sol`), Muse Wonder Full 1.0 (`muse-wonder-full-1.0`) | 51.8-56.0 | $2.00 / $0.10-0.20 / $10.00; Muse Wonder Full on subscription | 850K | `gpt` (6.1 Sol), `wonderfull` |
 | **Tier 2** | Strong and cheap. Start tier for Members. | GPT-6.1 Sol (`gpt-6.1-sol`), GLM-5.3 (`glm-5.3`), Grok 4.7 (`grok-4.7`), Qwen3.8 Max (`Qwen3.8-max`), Muse Wonder 1.0 (`muse-wonder-1.0`), Muse Spark 1.3 (`muse-spark-1.3`) | 44.8-52 | $1.25-2.00 / $0.10-0.50 / $4.25-10.00; Muse Wonder on subscription | 500K | `grok`, `qwen`, `glm`, `muse`, `wonder` |
-| **Tier 2b** | Review-panel and fallback tier: the old Tier 3 list without Grok 4.7 and Muse Spark 1.3. If GPT-6.1 Terra returns a 429 the request is retried on GLM-5.3 (owner, 2026-11-11). | GPT-6.1 Terra (`gpt-6.1-terra`), GLM-5.3 (`glm-5.3`), Qwen3.8 Max (`Qwen3.8-max`), Muse Wonder 1.0 (`muse-wonder-1.0`) | 44.8-52 (GPT-6.1 Terra not scored yet) | $1.40-4.00 / $0.20-0.26 / $4.40-20.00 (Terra not priced yet); Muse Wonder on subscription | 900K | none |
+| **Tier 2b** | Review-panel and fallback tier: the old Tier 3 list without Grok 4.7 and Muse Spark 1.3. After repeated 429s from GPT-6.1 Terra the request moves on to GLM-5.3: the first two 429s go back to Claude Code to retry, the third parks Terra and the request moves to the next eligible model, with no Terra-specific rule (owner, 2026-11-12; see the README tier section). | GPT-6.1 Terra (`gpt-6.1-terra`), GLM-5.3 (`glm-5.3`), Qwen3.8 Max (`Qwen3.8-max`), Muse Wonder 1.0 (`muse-wonder-1.0`) | 44.8-52 (GPT-6.1 Terra not scored yet) | $1.40-4.00 / $0.20-0.26 / $4.40-20.00 (Terra not priced yet); Muse Wonder on subscription | 900K | none |
 | **Tier 3** | Strong and cheap, GLM-5.3 first. | GLM-5.3 (`glm-5.3`), Qwen3.8 Max (`Qwen3.8-max`) | 44.8-45.4 | $1.40-1.65 / $0.206-0.26 / $4.40-4.951 | 900K | none |
 | **Tier 4** | Budget. Bulk and low-stakes work. | GPT-6 Luna (`gpt-6-luna`), Claude Haiku 5.5 (`claude-haiku-5-5`, unscored, placed by the owner), Grok 4.7 (`grok-4.7`, last because its own window is 500K) | 38.1 (Luna); Haiku 5.5 not scored yet | $0.10 / $0.01 / $0.50 (Luna); Haiku 5.5 not priced here yet | 500K | none |
 
@@ -175,6 +177,10 @@ position, because the newer model wins on both score and price.
 7. **Gateway first.** A model goes into a tier only when the company gateway serves it; until then
    it stays a Candidate.
 
+**Owner exception: Claude Haiku 5.5.** Claude Haiku 5.5 (`claude-haiku-5-5`) is in Tier 4 by the
+owner's instruction (2026-11-10, confirmed 2026-11-12), which overrides rules 1 and 2 above: they would hold
+an unscored model back. Its status is "unscored". No score is invented for it; score it and revisit.
+
 ## 6. How to update this page
 
 1. Re-check the numbers on Artificial Analysis (intelligence, HLE, Terminal-Bench, $/task) and the
@@ -217,5 +223,5 @@ Footnotes:
   API rates, shown for comparison only. Gateway ids: `muse-wonder-full-1.0`, `muse-wonder-1.0` (each also
   has a `-contributor` copy). Both have 1M context.
 - **Unscored:** `claude-haiku-5-5` and `gpt-6.1-terra` have no scores or prices on this page yet. Claude Haiku 5.5 sits in
-  Tier 4 by the owner's decision of 2026-11-10 (an exception to placement rules 1 and 2, which would hold
-  an unscored model back); score it and revisit. Claude Haiku 4.5 stays Excluded in section 4.
+  Tier 4 by the owner's decision of 2026-11-10, confirmed 2026-11-12 (an owner exception to placement rules 1
+  and 2, which would hold an unscored model back; see section 5); score it and revisit. Claude Haiku 4.5 stays Excluded in section 4.
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
