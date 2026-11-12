6fa89667b24f567b5ef77d5b5ee61dfc65f5b137
Review one task for spec compliance.

Task brief: ## Task 8: Add a test that ties review-tiers.default.json to the ccsession slot counts

Edit `tests/review/test_review_panel_live7.py`: add one test that loads `src/superclaude/cli/review/data/review-tiers.default.json` and `src/superclaude/skills/ccsession-tag/ccsession-models.json` and asserts, for `tier2b`, `tier3` and `tier4`, that the number of models in the review tier list equals the number of `models_env` slots in the JSON, and that the first model of `tier2b` is `gpt-6.1-terra` and of `tier3` is `glm-5.3`. Reuse the fixtures and path helpers already in that file. Also run `uv run pytest tests/review -q` and confirm the existing tests that cover the filled `tier2b` (`test_packaged_tier2b_has_the_owner_supplied_models_in_order`, `test_gateway_resolves_all_seven_with_the_packaged_tier2b`, the `anthropic-only` stand-in tests) pass without edits; if one fails, fix the cause in the review data or code rather than the test.

Acceptance criteria:
- The new test fails when a model is dropped from `tier2b` in the review tier file (checked once by hand-editing a temporary copy or via monkeypatch inside the test) and passes on the real files.
- `uv run pytest tests/review -q` passes with no failures, showing the live7 panel and the `anthropic-only` stand-in still resolve and the gateway environment does not fail closed on `tier2b`.
Global constraints: 
- Master already holds the tier layout (`ccsession-models.json` tier2b, tier3, tier4; review-tiers file; MODEL-TIERS.md rows). Do not change those lists, slots or windows, and do not edit `ccsession-models.json` (so no version bump).
- Do not touch ccsession alias code (`ccsession`, `models.py`, `local-gateway-alias-proxy.py`) or `tests/skills/test_model_alias_policy.py` lines 229-241 (the `haiku` alias stays on its current tier).
- Do not add a Terra-specific 429 rule and do not edit `docs/designs/sc-issue-command.md` or any file under `docs/testing/v5.0.0/sysop/`.
- Edit only `src/` and `plugins/` sources, tests, docs and CHANGELOG; the `.claude/` copies come from `make sync-dev` and are never staged. Installed primitives must not gain any `src/superclaude/...` path.
- Docs follow the writing rules of the repo: plain words, no em dashes.
Start sha: 6fa89667b24f567b5ef77d5b5ee61dfc65f5b137
Diff against the start snapshot: diff --git a/tests/review/test_review_panel_live7.py b/tests/review/test_review_panel_live7.py
index c69506c69..1dbf65e1d 100644
--- a/tests/review/test_review_panel_live7.py
+++ b/tests/review/test_review_panel_live7.py
@@ -4,6 +4,7 @@ from __future__ import annotations
 
 import copy
 import json
+from pathlib import Path
 
 import pytest
 from click.testing import CliRunner
@@ -82,6 +83,29 @@ def test_packaged_tier2b_has_the_owner_supplied_models_in_order(tiers):
     assert all(m in tiers["names"] for m in tiers["aliases"]["tier2b"]["models"])
 
 
+CCSESSION_MODELS = (
+    Path(__file__).resolve().parents[2]
+    / "src/superclaude/skills/ccsession-tag/ccsession-models.json"
+)
+
+
+def _assert_tiers_match_ccsession_slots(tiers):
+    slots = json.loads(CCSESSION_MODELS.read_text(encoding="utf-8"))["tiers"]
+    for tier in ("tier2b", "tier3", "tier4"):
+        listed = tiers["aliases"][tier]["models"]
+        assert len(listed) == len(slots[tier]["models_env"]), tier
+    assert tiers["aliases"]["tier2b"]["models"][0] == "gpt-6.1-terra"
+    assert tiers["aliases"]["tier3"]["models"][0] == "glm-5.3"
+
+
+def test_review_tier_lists_match_the_ccsession_slot_counts(tiers):
+    _assert_tiers_match_ccsession_slots(tiers)
+    dropped = copy.deepcopy(tiers)
+    dropped["aliases"]["tier2b"]["models"].pop()
+    with pytest.raises(AssertionError):
+        _assert_tiers_match_ccsession_slots(dropped)
+
+
 def test_gateway_resolves_all_seven_with_the_packaged_tier2b(tiers, live7):
     out = pnl.resolve(live7, tiers, "gateway", "run-a")
     got = {r["reviewer_id"]: r for r in out["reviewers"]}
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
