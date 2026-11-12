1e689ab873523e44111b4bd634e8bc563a119722
Review one task for spec compliance.

Task brief: ## Task 4: Update the retry-ladder tests and the family note in model-aliases.md

Depends on: Task 3

Edit `tests/skills/test_model_alias_policy.py` line 227 so the loop over names reads `("T2bModel01", "T2Model02", "T1Model02", "T1Model01")`. Edit `tests/skills/test_workflow_archive.py` line 799 so the RUNGS list starts with `"T2bModel01"` (the ledger regex accepts `[A-Za-z0-9_]+`, so no code change is needed). Edit `docs/reference/model-aliases.md` line 63 (the "Implement retry ladder" bullet): the four exported variables become `T2bModel01`, `T2Model02`, `T1Model02`, `T1Model01`, the defaults.sh line numbers are removed or marked as unverified for `T2bModel01`, and the family note states that rung 0 is Terra (GPT family) by owner decision of 2026-11-12 while `T3Model01` is glm-5.3.

Acceptance criteria:
- `uv run pytest tests/skills/test_model_alias_policy.py tests/skills/test_workflow_archive.py -q` passes.
- `grep -n 'T3Model01' docs/reference/model-aliases.md` prints no line that describes the retry ladder.
Global constraints: 
- Master already holds the tier layout (`ccsession-models.json` tier2b, tier3, tier4; review-tiers file; MODEL-TIERS.md rows). Do not change those lists, slots or windows, and do not edit `ccsession-models.json` (so no version bump).
- Do not touch ccsession alias code (`ccsession`, `models.py`, `local-gateway-alias-proxy.py`) or `tests/skills/test_model_alias_policy.py` lines 229-241 (the `haiku` alias stays on its current tier).
- Do not add a Terra-specific 429 rule and do not edit `docs/designs/sc-issue-command.md` or any file under `docs/testing/v5.0.0/sysop/`.
- Edit only `src/` and `plugins/` sources, tests, docs and CHANGELOG; the `.claude/` copies come from `make sync-dev` and are never staged. Installed primitives must not gain any `src/superclaude/...` path.
- Docs follow the writing rules of the repo: plain words, no em dashes.
Start sha: 1e689ab873523e44111b4bd634e8bc563a119722
Diff against the start snapshot: diff --git a/docs/reference/model-aliases.md b/docs/reference/model-aliases.md
index 88ed9626f..4bbf63a16 100644
--- a/docs/reference/model-aliases.md
+++ b/docs/reference/model-aliases.md
@@ -60,4 +60,4 @@ The probes covered the frontmatter path and `--model`; they did not exercise the
 - **Reflect reviewer diversity.** When the three variables hold the tier ids, `count_model_aliases` (`src/superclaude/cli/reflect/runner.py` lines 291-310) counts three distinct values. Tier 1a and tier 1b both list Claude Sonnet 5.5 (`src/superclaude/skills/ccsession-tag/MODEL-TIERS.md` lines 38-39), so the reviewers differ less than the count suggests.
 - **Sprint alternate-model suggestion.** Given the alias `opus`, `suggest_alternate_model` returns `sonnet` when the two slots hold different ids (`src/superclaude/cli/sprint/aienv.py` lines 149-152). When the three `ANTHROPIC_DEFAULT_*_MODEL` slots hold tier ids and no slot that `_load_aliases` reads, including `T2Model01` to `T2Model0N` (lines 78-82), holds a given Claude id from a cooldown message such as `claude-opus-5-5`, it returns `None` (lines 111-128).
 - **Roadmap names.** Step ids such as `generate-opus-architect` (`src/superclaude/skills/sc-roadmap-protocol/SKILL.md` line 114) and the `/sc:recommend` eval model lists (`src/superclaude/cli/recommend/eval_aggregate.py` lines 18-20) name the aliases, so this change does not rename them.
-- **Implement retry ladder.** On 2026-11-05 `/etc/aidev02/aienv.d/defaults.sh` exports `T3Model01`, `T2Model02`, `T1Model02` and `T1Model01` (lines 48, 37, 69 and 67). After Task 5 of this issue's plan, in a workspace that sets these four variables the primary ladder of `refs/retry.md` in `sc-implement-protocol` (names at lines 162, 164, 168, 169 and 172) replaces the alias fallback ladder. The Task 5 notes (`artifacts/t5-notes.md` in this issue's plan package) record that with these values rung 1 is a non-Claude model, rungs 0 and 2 are GPT models, and a claude-sonnet executor sits on no primary rung, so its tier is unknown and adviser A takes the top rung.
+- **Implement retry ladder.** On 2026-11-05 `/etc/aidev02/aienv.d/defaults.sh` exported the four rung variables of that time: the first Tier 3 slot, `T2Model02`, `T1Model02` and `T1Model01` (lines 48, 37, 69 and 67). Since the owner decision of 2026-11-12 (issue 488) rung 0 is `T2bModel01`, the first Tier 2b slot (GPT-6.1 Terra, a GPT-family model, so the family behavior of rung 0 is unchanged); the other three variables are unchanged, and the line of `T2bModel01` in `defaults.sh` is not checked here. The first Tier 3 slot now holds glm-5.3, which is in neither model family, so it is no longer a rung. After Task 5 of this issue's plan, in a workspace that sets the four rung variables the primary ladder of `refs/retry.md` in `sc-implement-protocol` (names at lines 162, 164, 168, 169 and 172) replaces the alias fallback ladder. The Task 5 notes (`artifacts/t5-notes.md` in this issue's plan package) record that with these values rung 1 is a non-Claude model, rungs 0 and 2 are GPT models, and a claude-sonnet executor sits on no primary rung, so its tier is unknown and adviser A takes the top rung.
diff --git a/tests/skills/test_model_alias_policy.py b/tests/skills/test_model_alias_policy.py
index b7123504e..b77a3cace 100644
--- a/tests/skills/test_model_alias_policy.py
+++ b/tests/skills/test_model_alias_policy.py
@@ -224,7 +224,7 @@ def test_retry_ladder_uses_the_variable_names_the_workspace_exports() -> None:
     ]
     assert bad == []
     retry = (ROOT / RETRY_REFS[0]).read_text(encoding="utf-8")
-    for name in ("T3Model01", "T2Model02", "T1Model02", "T1Model01"):
+    for name in ("T2bModel01", "T2Model02", "T1Model02", "T1Model01"):
         assert name in retry
 
 
diff --git a/tests/skills/test_workflow_archive.py b/tests/skills/test_workflow_archive.py
index cf6632bfe..5a9269acb 100644
--- a/tests/skills/test_workflow_archive.py
+++ b/tests/skills/test_workflow_archive.py
@@ -796,7 +796,7 @@ def test_directory_traversal_error_cannot_produce_final_state(p, monkeypatch):
 # --- retry / halt ledger records -------------------------------------------------
 CK = "a" * 40
 RUNGS = [
-    "T3Model01",
+    "T2bModel01",
     "T2Model02",
     "T1Model02",
     "T1Model01",
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
