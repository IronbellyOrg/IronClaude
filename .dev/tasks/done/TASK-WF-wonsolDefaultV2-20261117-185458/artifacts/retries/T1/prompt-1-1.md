260d574dd8db5eb808e4fac9d334e3ae2eb696ca
Review one task for spec compliance.

Task brief: ## Task 1: Add three seat tiers and the ember model to the packaged tier file

Edit `src/superclaude/cli/review/data/review-tiers.default.json`. Add three aliases: `tier5a` (gateway alias `claude-gw-tier5a[1m]`, models `muse-wonder-1.0` then `claude-sonnet-5-5`), `tier5b` (`claude-gw-tier5b[1m]`, models `["gpt-6.1-sol"]` only) and `tier5c` (`claude-gw-tier5c[1m]`, models `["muse-ember-1.0"]` only). The list shapes matter and were checked against `resolve_slot` in `src/superclaude/cli/review/panel.py`: a `fixed` slot takes the first available model of its list (so `tier5a` falls back from wonder to Sonnet), but a `random` slot picks at random among every available model of its list, so `tier5b` and `tier5c` must hold exactly one model each to make the seats deterministic (a two-model list returned the fallback model in a draft run). In the `anthropic-only` environment add `stand_ins` entries `tier5b` and `tier5c`, each `["claude-haiku-5-5"]` (that environment lists only Anthropic models, and a tier with none available raises `NoModelAvailable` without a stand-in). Add `muse-ember-1.0` to `names` ("Muse Ember 1.0") and to `classes` (class `muse`, as the other Muse models). Bump the tier file `version` by one minor step.

Acceptance criteria (ids):
T1.AC1: `validate_tiers` returns no errors for the edited file, and `pnl.load_tiers()["aliases"]` has `tier5a`, `tier5b` and `tier5c` with the models above.
T1.AC2: Resolving a draft template with the three slots of Task 2 for run ids `t1`, `t2` and `t3`: in `anthropic-only` it prints `claude-sonnet-5-5`, then two `claude-haiku-5-5` marked `stand_in` true, every time; in `gateway` it prints `muse-wonder-1.0`, `gpt-6.1-sol`, `muse-ember-1.0` every time.
T1.AC3: No existing alias (`tier1a` to `tier4`) changes its models, so `live7` and the old default resolve to the same models as before.
Global constraints: ## Constraints

- Work on a new branch cut from `origin/master`, never on the evaluation branch that holds the answer key; open the PR only with `/sc:pr-submit --monitor 3` against `IronbellyOrg/IronClaude`; never stage anything under `.claude/`.
- Edit only under `src/superclaude/cli/review/`, `src/superclaude/skills/`, `src/superclaude/rules/`, `tests/` and `docs/`; run `make sync-dev` after skill or rule edits.
- The product panel chooses models only. The seat lenses, table caps and briefs of the evaluation harness (S = wonder with lenses C5 C6 C8 C2 and cap 8; L1 = sol; L2 = ember) are not part of this change, so only the model mix transfers. The confirming test did not meet its registered bar (found fraction +0.099 and +0.109, lower bounds -0.004 and -0.006; 1.56 times the control's panel time); the owner has ordered the default change as provisional, and the plan must say so in the docs it touches.
- `validate_panel` in `src/superclaude/cli/review/panel.py` already allows 1 to 8 reviewers and requires exactly one `fixed` slot; do not change those rules. A template id must not start with `reflect-` (that prefix turns on the reflect profile).
- Keep the strategy and tier-name rules: tier names match `^tier[0-9]{1,2}[a-z]?$`.
Start sha: 260d574dd8db5eb808e4fac9d334e3ae2eb696ca
Diff against the start snapshot: diff --git a/src/superclaude/cli/review/data/review-tiers.default.json b/src/superclaude/cli/review/data/review-tiers.default.json
index 022ff46fe..1b10996a1 100644
--- a/src/superclaude/cli/review/data/review-tiers.default.json
+++ b/src/superclaude/cli/review/data/review-tiers.default.json
@@ -1,24 +1,29 @@
 {
   "schema": "review-tiers/1",
-  "version": "1.0.0",
+  "version": "1.1.0",
   "aliases": {
     "tier1a": {"alias": "claude-gw-tier1a[1m]", "models": ["claude-opus-5-5", "claude-sonnet-5-5"]},
     "tier1b": {"alias": "claude-gw-tier1b[1m]", "models": ["claude-sonnet-5-5", "gpt-6.1-sol", "muse-wonder-full-1.0"]},
     "tier2": {"alias": "claude-gw-tier2[1m]", "models": ["gpt-6.1-sol", "glm-5.3", "grok-4.7", "Qwen3.8-max", "muse-wonder-1.0", "muse-spark-1.3"]},
     "tier2b": {"alias": "claude-gw-tier2b[1m]", "models": ["gpt-6.1-terra", "glm-5.3", "Qwen3.8-max", "muse-wonder-1.0"]},
     "tier3": {"alias": "claude-gw-tier3[1m]", "models": ["glm-5.3", "Qwen3.8-max"]},
-    "tier4": {"alias": "claude-gw-tier4[1m]", "models": ["gpt-6-luna", "claude-haiku-5-5", "grok-4.7"]}
+    "tier4": {"alias": "claude-gw-tier4[1m]", "models": ["gpt-6-luna", "claude-haiku-5-5", "grok-4.7"]},
+    "tier5a": {"alias": "claude-gw-tier5a[1m]", "models": ["muse-wonder-1.0", "claude-sonnet-5-5"]},
+    "tier5b": {"alias": "claude-gw-tier5b[1m]", "models": ["gpt-6.1-sol"]},
+    "tier5c": {"alias": "claude-gw-tier5c[1m]", "models": ["muse-ember-1.0"]}
   },
   "names": {
     "claude-opus-5-5": "Claude Opus 5.5", "claude-sonnet-5-5": "Claude Sonnet 5.5", "claude-haiku-5-5": "Claude Haiku 5.5",
     "claude-fable-5-1": "Claude Fable 5.1", "gpt-6.1-sol": "GPT 6.1 Sol", "gpt-6.1-terra": "GPT 6.1 Terra", "gpt-6-luna": "GPT 6 Luna",
     "muse-wonder-full-1.0": "Muse Wonder Full 1.0", "muse-wonder-1.0": "Muse Wonder 1.0", "muse-spark-1.3": "Muse Spark 1.3",
+    "muse-ember-1.0": "Muse Ember 1.0",
     "glm-5.3": "GLM 5.3", "grok-4.7": "Grok 4.7", "Qwen3.8-max": "Qwen 3.8 Max"
   },
   "classes": {
     "claude-opus-5-5": "opus", "claude-sonnet-5-5": "sonnet", "claude-haiku-5-5": "haiku", "claude-fable-5-1": "fable",
     "gpt-6.1-sol": "gpt", "gpt-6.1-terra": "gpt", "gpt-6-luna": "gpt",
     "muse-wonder-full-1.0": "muse", "muse-wonder-1.0": "muse", "muse-spark-1.3": "muse",
+    "muse-ember-1.0": "muse",
     "glm-5.3": "glm", "grok-4.7": "grok", "Qwen3.8-max": "qwen"
   },
   "environments": {
@@ -31,7 +36,7 @@
     "anthropic-only": {
       "note": "This experiment environment. Tier 2 and Tier 3 contain no Anthropic model; owner decision 2026-11-10: Claude Haiku 5.5 stands in for both. Tier 1b resolves to Sonnet 5.5, the Stage 2 reviewer model.",
       "available": ["claude-opus-5-5", "claude-sonnet-5-5", "claude-haiku-5-5", "claude-fable-5-1"],
-      "stand_ins": {"tier2": ["claude-haiku-5-5"], "tier2b": ["claude-haiku-5-5"], "tier3": ["claude-haiku-5-5"], "tier4": ["claude-haiku-5-5"]},
+      "stand_ins": {"tier2": ["claude-haiku-5-5"], "tier2b": ["claude-haiku-5-5"], "tier3": ["claude-haiku-5-5"], "tier4": ["claude-haiku-5-5"], "tier5b": ["claude-haiku-5-5"], "tier5c": ["claude-haiku-5-5"]},
       "launch": {"claude-opus-5-5": "opus", "claude-sonnet-5-5": "sonnet", "claude-haiku-5-5": "haiku", "claude-fable-5-1": "fable"}
     }
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
