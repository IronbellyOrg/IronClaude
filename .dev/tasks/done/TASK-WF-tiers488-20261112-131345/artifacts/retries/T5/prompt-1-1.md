de5d808ac8c6e94ffa036adc804221cfb67e88cd
Review one task for spec compliance.

Task brief: ## Task 5: Describe the 429 fallback in the README tier section

Edit `src/superclaude/skills/ccsession-tag/README.md` in the tier section (the paragraph at lines 444 to 449 and the Failover row of the table at line 453). Add a short plain-words paragraph under the tier list: when a model answers 429 (too many requests), the first two 429s for that model are handed back to Claude Code, which retries the request; the third 429 parks that model for a while and the same request moves to the next eligible model in the tier. State that this is not an immediate retry on the next model, that it applies to every tier, and that Tier 2b has no Terra-specific rule (GPT-6.1 Terra's 429s follow the same count, then the next model is GLM-5.3). Do not change the Failover row facts.

Acceptance criteria:
- README.md contains the paragraph, with the words "first two" and "third" and no claim of an immediate retry, and no em dash.
- The statement matches the Failover row of the same file (408, 429, 500 and related replies count per model; first two go back, third switches).
Global constraints: 
- Master already holds the tier layout (`ccsession-models.json` tier2b, tier3, tier4; review-tiers file; MODEL-TIERS.md rows). Do not change those lists, slots or windows, and do not edit `ccsession-models.json` (so no version bump).
- Do not touch ccsession alias code (`ccsession`, `models.py`, `local-gateway-alias-proxy.py`) or `tests/skills/test_model_alias_policy.py` lines 229-241 (the `haiku` alias stays on its current tier).
- Do not add a Terra-specific 429 rule and do not edit `docs/designs/sc-issue-command.md` or any file under `docs/testing/v5.0.0/sysop/`.
- Edit only `src/` and `plugins/` sources, tests, docs and CHANGELOG; the `.claude/` copies come from `make sync-dev` and are never staged. Installed primitives must not gain any `src/superclaude/...` path.
- Docs follow the writing rules of the repo: plain words, no em dashes.
Start sha: de5d808ac8c6e94ffa036adc804221cfb67e88cd
Diff against the start snapshot: diff --git a/src/superclaude/skills/ccsession-tag/README.md b/src/superclaude/skills/ccsession-tag/README.md
index d7dc3f667..5fa99c64d 100644
--- a/src/superclaude/skills/ccsession-tag/README.md
+++ b/src/superclaude/skills/ccsession-tag/README.md
@@ -447,6 +447,14 @@ GPT-6.1 Terra, GLM-5.3, Qwen3.8 Max and Muse Wonder 1.0. A tier whose slots the
 workspace env file does not set stops tier-mode launches, so the env file must carry
 a tier before this data names it (see `MODEL-TIERS.md`, "How to update this page").
 
+What a 429 (too many requests) does, in every tier: it is not retried straight away on the
+next model. The first two 429s from a model go back to Claude Code, which retries the
+request on the same model. The third 429 parks that model for a while (see the Cooldown
+row below), and the same request then moves to the next eligible model in the tier. Tier 2b
+has no rule of its own for GPT-6.1 Terra: Terra's 429s follow this same count, and the next
+model after Terra in the list is GLM-5.3 (owner decision of 2026-11-12, issue 488; the
+behavior comes from the failover change merged earlier).
+
 | | What happens |
 |---|---|
 | Picker (`/model`) | Shows the tiers (Tier 0, Tier 1a, ...), each with its models; with `+models` in the owner's rule, also each model on its own, in `CCSESSION_MODEL_ORDER` order |
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
