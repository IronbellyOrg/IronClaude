c53fca7cfde4286666fed2670362f63dec87f492
Review one task for spec compliance.

Task brief: ## Task 1: Point issue-worker-t3 and its protocol references at claude-gw-tier2b

Edit `src/superclaude/agents/issue-worker-t3.md`: change the `model:` line 6 from `claude-gw-tier3` to `claude-gw-tier2b`, and the provenance sentence on line 12 so it names `model: claude-gw-tier2b` (keep `effort: low` and the agent name `issue-worker-t3`; adjust the sentence about the tier's first model so it stays true for Tier 2b, whose first model is GPT-6.1 Terra, without claiming facts not verified). Edit `src/superclaude/skills/sc-issue-protocol/refs/tiers.md`: the T3 table row (line 13) and the E-TIER-UNAVAILABLE example (around line 49) name `claude-gw-tier2b`; check lines 7 to 46 of that file for any other statement about T3's model and keep them consistent. Edit `src/superclaude/skills/sc-issue-protocol/SKILL.md` line 60 table row to `claude-gw-tier2b`; check the E-TIER-UNAVAILABLE row at line 163 for a tier name to update. Use Grep for `claude-gw-tier3` across `src/superclaude/skills/sc-issue-protocol/` and `src/superclaude/agents/` and update every remaining hit that refers to this worker (the Tier 3 tier itself stays defined and unchanged).

Acceptance criteria:
- `grep -rn 'claude-gw-tier3' src/superclaude/agents src/superclaude/skills/sc-issue-protocol` prints no line that refers to `issue-worker-t3`.
- `src/superclaude/agents/issue-worker-t3.md` line 6 reads `model: claude-gw-tier2b`, `effort: low` is still present, and the file name and `name:` field are unchanged.
Global constraints: 
- Master already holds the tier layout (`ccsession-models.json` tier2b, tier3, tier4; review-tiers file; MODEL-TIERS.md rows). Do not change those lists, slots or windows, and do not edit `ccsession-models.json` (so no version bump).
- Do not touch ccsession alias code (`ccsession`, `models.py`, `local-gateway-alias-proxy.py`) or `tests/skills/test_model_alias_policy.py` lines 229-241 (the `haiku` alias stays on its current tier).
- Do not add a Terra-specific 429 rule and do not edit `docs/designs/sc-issue-command.md` or any file under `docs/testing/v5.0.0/sysop/`.
- Edit only `src/` and `plugins/` sources, tests, docs and CHANGELOG; the `.claude/` copies come from `make sync-dev` and are never staged. Installed primitives must not gain any `src/superclaude/...` path.
- Docs follow the writing rules of the repo: plain words, no em dashes.
Start sha: c53fca7cfde4286666fed2670362f63dec87f492
Diff against the start snapshot: diff --git a/src/superclaude/agents/issue-worker-t3.md b/src/superclaude/agents/issue-worker-t3.md
index 07a163ac7..482d62e59 100644
--- a/src/superclaude/agents/issue-worker-t3.md
+++ b/src/superclaude/agents/issue-worker-t3.md
@@ -3,13 +3,13 @@ name: issue-worker-t3
 description: Tier-3 lookup worker for /sc:issue. Runs the first GitHub lookup of every claim and create (scout.md) and drafts the quick-depth issue body. Read-only on GitHub and code; writes only under .dev/issues/; returns the path of the file it wrote.
 category: analysis
 tools: Read, Grep, Glob, Write, Bash
-model: claude-gw-tier3
+model: claude-gw-tier2b
 effort: low
 ---
 
 # Issue Worker (tier 3)
 
-Spawned only by the `sc:issue-protocol` skill (`~/.claude/skills/sc-issue-protocol/SKILL.md`), with `subagent_type: issue-worker-t3` and no `model` parameter, so the `model: claude-gw-tier3` pin above is the model that serves you. The `effort: low` line is required because the tier's first model rejects the default `medium` effort with an HTTP 400; do not remove it or raise it to `medium`.
+Spawned only by the `sc:issue-protocol` skill (`~/.claude/skills/sc-issue-protocol/SKILL.md`), with `subagent_type: issue-worker-t3` and no `model` parameter, so the `model: claude-gw-tier2b` pin above is the model that serves you. The pin is Tier 2b (GPT-6.1 Terra first), not Tier 3: the owner kept this worker on the model order it had before Tier 3 was cut to GLM-5.3 and Qwen3.8 Max (issue 488, 2026-11-12). The `effort: low` line stays: the first model of the tier this worker used to be pinned to rejected the default `medium` effort with an HTTP 400, and it is not known that Tier 2b's first model accepts `medium`; do not remove it or raise it to `medium`.
 
 ## Your files are tool inputs, not reports
 
diff --git a/src/superclaude/skills/sc-issue-protocol/SKILL.md b/src/superclaude/skills/sc-issue-protocol/SKILL.md
index 829ebca51..e635a128f 100644
--- a/src/superclaude/skills/sc-issue-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-issue-protocol/SKILL.md
@@ -57,7 +57,7 @@ Spawn workers with `subagent_type: issue-worker-t<N>` and never pass the `model`
 
 | Agent | Picker ID (frontmatter `model:`) | Installed file |
 |---|---|---|
-| `issue-worker-t3` | `claude-gw-tier3` | `~/.claude/agents/issue-worker-t3.md` |
+| `issue-worker-t3` | `claude-gw-tier2b` | `~/.claude/agents/issue-worker-t3.md` |
 | `issue-worker-t2` | `claude-gw-tier2` | `~/.claude/agents/issue-worker-t2.md` |
 | `issue-worker-t1` | `claude-gw-tier1b` | `~/.claude/agents/issue-worker-t1.md` |
 
diff --git a/src/superclaude/skills/sc-issue-protocol/refs/tiers.md b/src/superclaude/skills/sc-issue-protocol/refs/tiers.md
index b3d71ace0..4282f2f2f 100644
--- a/src/superclaude/skills/sc-issue-protocol/refs/tiers.md
+++ b/src/superclaude/skills/sc-issue-protocol/refs/tiers.md
@@ -10,11 +10,11 @@ Workers are the agent files `~/.claude/agents/issue-worker-t3.md`, `~/.claude/ag
 
 | Tier | Picker ID pinned in agent frontmatter | Agent | Used for |
 |---|---|---|---|
-| T3 | `claude-gw-tier3` | `issue-worker-t3` | the first lookup on every claim and create (B13); quick-depth issue body |
+| T3 | `claude-gw-tier2b` | `issue-worker-t3` | the first lookup on every claim and create (B13); quick-depth issue body |
 | T2 | `claude-gw-tier2` | `issue-worker-t2` | accuracy check and summary on simple and medium claims; flag choice at quick depth when a flag is missing; validation of user-given flags at standard depth; standard-depth body. Next-step chains for simple work (B14) |
 | T1 | `claude-gw-tier1b` | `issue-worker-t1` | accuracy check and summary on complex claims; flag choice at standard and deep depth when a flag is missing; the independent flag variant for the deep adversarial check; deep body. Next-step chains for medium and complex work (B14) |
 
-Picker IDs are written without the `[1m]` context suffix (default D19).
+Picker IDs are written without the `[1m]` context suffix (default D19). The worker name `issue-worker-t3` is a label, not the ccsession tier: since the 2026-11-12 owner decision (issue 488) it is pinned to ccsession Tier 2b (GPT-6.1 Terra first), the model order it had before Tier 3 was cut to GLM-5.3 and Qwen3.8 Max.
 
 ## Why the pin lives in frontmatter
 
@@ -46,7 +46,7 @@ In claim mode the line is also shown in the posted accuracy-check comment (optio
 If a spawn of `issue-worker-t3` or `issue-worker-t2` fails because its picker ID is not served (for example, outside a ccsession tier workspace), or the T2 fallback run itself is not served, STOP `E-TIER-UNAVAILABLE`, naming the agent file and the picker ID, for example:
 
 ```text
-E-TIER-UNAVAILABLE: ~/.claude/agents/issue-worker-t3.md pins claude-gw-tier3, which this session cannot serve.
+E-TIER-UNAVAILABLE: ~/.claude/agents/issue-worker-t3.md pins claude-gw-tier2b, which this session cannot serve.
 ```
 
 There is no alias fallback (no retry with the `haiku`, `sonnet` or `opus` alias): a fallback to `haiku` follows `ANTHROPIC_DEFAULT_HAIKU_MODEL` and can land on a model of another tier or family than the pin, which defeats B13.
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
