9e1bd201cc639fd2eb86e8cb0d59336e2c8969f4
Review one task for spec compliance.

Task brief: ## Task 2: Update the tests and the reference doc that pin issue-worker-t3

Depends on: Task 1

Edit `tests/skills/test_issue_worker_agents.py` line 22 so the pin entry is `("claude-gw-tier2b", "tier2b")` and check lines 71 to 80 for assertions that depend on the old pin. Edit `tests/skills/test_model_alias_policy.py` line 30 so `src/superclaude/agents/issue-worker-t3.md` maps to `claude-gw-tier2b`; leave lines 229 to 241 as they are. Edit `docs/reference/model-aliases.md` line 16 so `issue-worker-t3` pins `claude-gw-tier2b` and the `effort: low` reason is stated without the claim that Tier 3's first model is the one that rejects `medium` (say the tier's first model, as in the agent file). Check line 17 and the rest of that file for another `claude-gw-tier3` mention tied to the worker.

Acceptance criteria:
- `uv run pytest tests/skills/test_issue_worker_agents.py tests/skills/test_model_alias_policy.py -q` passes.
- `docs/reference/model-aliases.md` no longer says `issue-worker-t3` pins `claude-gw-tier3`, and the three export lines pinned by `test_mapping_document_states_the_exports_and_tiers_exist` are untouched.
Global constraints: 
- Master already holds the tier layout (`ccsession-models.json` tier2b, tier3, tier4; review-tiers file; MODEL-TIERS.md rows). Do not change those lists, slots or windows, and do not edit `ccsession-models.json` (so no version bump).
- Do not touch ccsession alias code (`ccsession`, `models.py`, `local-gateway-alias-proxy.py`) or `tests/skills/test_model_alias_policy.py` lines 229-241 (the `haiku` alias stays on its current tier).
- Do not add a Terra-specific 429 rule and do not edit `docs/designs/sc-issue-command.md` or any file under `docs/testing/v5.0.0/sysop/`.
- Edit only `src/` and `plugins/` sources, tests, docs and CHANGELOG; the `.claude/` copies come from `make sync-dev` and are never staged. Installed primitives must not gain any `src/superclaude/...` path.
- Docs follow the writing rules of the repo: plain words, no em dashes.
Start sha: 9e1bd201cc639fd2eb86e8cb0d59336e2c8969f4
Diff against the start snapshot: diff --git a/docs/reference/model-aliases.md b/docs/reference/model-aliases.md
index fd2ab9f48..b24e435d7 100644
--- a/docs/reference/model-aliases.md
+++ b/docs/reference/model-aliases.md
@@ -13,7 +13,7 @@ Checks in `tests/skills/test_model_alias_policy.py` that read model names includ
 
 ### Allow-list
 
-- `issue-worker-t3` pins `claude-gw-tier3`, `issue-worker-t2` pins `claude-gw-tier2` and `issue-worker-t1` pins `claude-gw-tier1b`, each on line 6 of its file under `src/superclaude/agents/`. `issue-worker-t3` also carries `effort: low` because its tier's first model returns an HTTP 400 for the default `medium` effort.
+- `issue-worker-t3` pins `claude-gw-tier2b`, `issue-worker-t2` pins `claude-gw-tier2` and `issue-worker-t1` pins `claude-gw-tier1b`, each on line 6 of its file under `src/superclaude/agents/`. The worker name `issue-worker-t3` is a label: since the owner decision of 2026-11-12 (issue 488) it runs on ccsession Tier 2b (GPT-6.1 Terra first), the order it had before Tier 3 was cut to GLM-5.3 and Qwen3.8 Max. `issue-worker-t3` also carries `effort: low` because the first model of the tier it used to be pinned to returns an HTTP 400 for the default `medium` effort; it is not known that Tier 2b's first model accepts `medium`, so the line stays.
 - The pins are on purpose: when a spawn fails because the picker id is not served, for example outside a ccsession tier workspace, the issue protocol stops with `E-TIER-UNAVAILABLE`, and there is no alias fallback (`src/superclaude/skills/sc-issue-protocol/refs/tiers.md` lines 34 and 40).
 - `TIER_TEXT_ALLOWED` lets the three pinned files, `src/superclaude/skills/sc-issue-protocol/` and `src/superclaude/skills/ccsession-tag/` contain the text `claude-gw-tier` (test lines 36-40).
 
diff --git a/tests/skills/test_issue_worker_agents.py b/tests/skills/test_issue_worker_agents.py
index 9d3db8478..7cd108f0e 100644
--- a/tests/skills/test_issue_worker_agents.py
+++ b/tests/skills/test_issue_worker_agents.py
@@ -19,7 +19,8 @@ ROOT = Path(__file__).resolve().parents[2]
 AGENTS = ROOT / "src/superclaude/agents"
 MODELS = ROOT / "src/superclaude/skills/ccsession-tag/ccsession-models.json"
 WORKERS = {
-    "issue-worker-t3": ("claude-gw-tier3", "tier3"),
+    # Pinned to Tier 2b (Terra first) by the owner on 2026-11-12, issue 488.
+    "issue-worker-t3": ("claude-gw-tier2b", "tier2b"),
     "issue-worker-t2": ("claude-gw-tier2", "tier2"),
     "issue-worker-t1": ("claude-gw-tier1b", "tier1b"),
 }
diff --git a/tests/skills/test_model_alias_policy.py b/tests/skills/test_model_alias_policy.py
index 2df97f142..b7123504e 100644
--- a/tests/skills/test_model_alias_policy.py
+++ b/tests/skills/test_model_alias_policy.py
@@ -27,7 +27,7 @@ ALIASES = {"opus", "sonnet", "haiku", "inherit"}
 # E-TIER-UNAVAILABLE outside a ccsession tier workspace (see
 # src/superclaude/skills/sc-issue-protocol/refs/tiers.md).
 ISSUE_WORKER_PINS = {
-    "src/superclaude/agents/issue-worker-t3.md": "claude-gw-tier3",
+    "src/superclaude/agents/issue-worker-t3.md": "claude-gw-tier2b",
     "src/superclaude/agents/issue-worker-t2.md": "claude-gw-tier2",
     "src/superclaude/agents/issue-worker-t1.md": "claude-gw-tier1b",
 }
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
