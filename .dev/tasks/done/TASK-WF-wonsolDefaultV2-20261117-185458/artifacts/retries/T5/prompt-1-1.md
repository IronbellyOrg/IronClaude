2e369c11fa47e22565e17e02724992fd9768a680
Review one task for spec compliance.

Task brief: ## Task 5: Update the tests and golden files that pin the old default and add the regression tests

Depends on: Task 4

Edit these existing tests: `tests/review/test_review_panel.py` (the `assert pnl.load_panel()["template_id"] == "default"` line of `test_template_lookup_precedence` becomes `"wonsol"`; `test_packaged_defaults_are_read_through_importlib_resources` checks the pointer file and the tier file instead of `review-panel.default.json`; finding F2: the `tpl` fixture at lines 19-21 (`return pnl.load_panel()`) becomes `pnl.load_panel("@classic")`, so the tests that pin the 4-slot shape and the Sonnet anchor at lines 38, 217-226, 237-240, 257, 272, 288-290 and 306 keep their meaning), `tests/review/test_review_cli.py` (finding F2: lines 52-62 and 76 pin the ids `t1b-1, t2-1, t3-1, t3-2` and the re-review anchor `t1b-1`, so they call `resolve --template @classic`), `tests/review/test_review_panel_live7.py` (`test_default_panel_is_unchanged_by_live7` becomes a test that the default is `wonsol` with 3 reviewers and that `@classic` still has 4 reviewers and `live7` still has 7), and settle the golden consumers (finding F1): `tests/review/test_review_panel_exclusion.py` (lines 58-63) and `tests/review/test_review_panel_reflect_profile.py` (lines 77-79) call `pnl.packaged_panel(name)` for the name `default`; both get one shared helper that returns the frozen fixture `tests/review/fixtures/review-panel.default.frozen.json` for `default` and `pnl.packaged_panel(name)` for `live7`. With that, `tests/review/fixtures/panel-golden-default-live7.json` stays byte-identical (its values keep `"template_id":"default"` and the old `template_sha256`), and the frozen-tier copy `tests/review/fixtures/review-tiers.frozen-1.0.0.json` stays byte-identical, so `tests/review/test_review_panel_exclusion.py` still proves that the old resolutions did not move; only `tests/review/fixtures/panel-golden-packaged-tiers.json` is re-pinned, and only for the `tiers_sha256` change of the Task 1 bump. Add `tests/review/test_review_default_template.py` with these tests: the default resolves to a template by reference (`default_template_name()` returns the pointer's value); a three-reviewer default resolves in `anthropic-only` and in `gateway`; a pointer edited in a temporary copy of the data folder switches the default to `classic` with no code change; a bad pointer is rejected. Check that `tests/review/test_review_panel_reflect_profile.py`, `tests/review/test_review_reflect_templates.py` and `tests/cli/reflect/test_shadow_skill_contract.py` still pass (they read `load_tiers` and `classes`; the new `classes` entry for ember must not break the reflect profile rules).

Acceptance criteria (ids):
T5.AC1: `uv run pytest tests/review tests/cli/reflect tests/unit/test_ccsession_tiers.py tests/skills/test_review_severity_rule.py -q` passes (the last file is added after PR 605 of the blocker-classification program, which pins the reflect reviewer in that test; it also scans tracked primitives for "any severity" wording, so new docs text must not use it) with no test skipped for this change; `tests/unit/test_ccsession_tiers.py` is run only to show it is not affected (it matched a search for `muse-ember-1.0`; if it reads `review-tiers.default.json`, update it in this task).
T5.AC2: The new test file fails if `load_panel` goes back to a hard-coded file name (the pointer-switch test is the check) and if the default is changed to a template with 4 reviewers while the 3-reviewer assertion remains.
T5.AC3: `git diff --stat` shows no change to `tests/review/fixtures/review-tiers.frozen-1.0.0.json`.

Explicit operator instruction on this task (the plan text above predates it; it is part of the task, not extra scope): in tests/review/test_review_cli.py add `--template @classic` to all four default-panel `resolve` calls (the calls at the file's lines 53, 64-74, 77-79 and 206-208 on the start tree) so they keep resolving the 4-reviewer panel; the `resolve` calls at lines 86 and 92 of the start tree stay on the default (they assert only the environment and a failing exit).
Known note: the Task 1 version bump also changes `tiers_version` (1.0.0 to 1.1.0) inside the re-pinned values of tests/review/fixtures/panel-golden-packaged-tiers.json, not only `tiers_sha256`.
Global constraints: ## Constraints

- Work on a new branch cut from `origin/master`, never on the evaluation branch that holds the answer key; open the PR only with `/sc:pr-submit --monitor 3` against `IronbellyOrg/IronClaude`; never stage anything under `.claude/`.
- Edit only under `src/superclaude/cli/review/`, `src/superclaude/skills/`, `src/superclaude/rules/`, `tests/` and `docs/`; run `make sync-dev` after skill or rule edits.
- The product panel chooses models only. The seat lenses, table caps and briefs of the evaluation harness (S = wonder with lenses C5 C6 C8 C2 and cap 8; L1 = sol; L2 = ember) are not part of this change, so only the model mix transfers. The confirming test did not meet its registered bar (found fraction +0.099 and +0.109, lower bounds -0.004 and -0.006; 1.56 times the control's panel time); the owner has ordered the default change as provisional, and the plan must say so in the docs it touches.
- `validate_panel` in `src/superclaude/cli/review/panel.py` already allows 1 to 8 reviewers and requires exactly one `fixed` slot; do not change those rules. A template id must not start with `reflect-` (that prefix turns on the reflect profile).
- Keep the strategy and tier-name rules: tier names match `^tier[0-9]{1,2}[a-z]?$`.
Start sha: 2e369c11fa47e22565e17e02724992fd9768a680
Diff against the start snapshot: diff --git a/tests/review/fixtures/panel-golden-packaged-tiers.json b/tests/review/fixtures/panel-golden-packaged-tiers.json
index 305cd911b..6c997b1f4 100644
--- a/tests/review/fixtures/panel-golden-packaged-tiers.json
+++ b/tests/review/fixtures/panel-golden-packaged-tiers.json
@@ -1,5 +1,5 @@
 {
- "default|anthropic-only|first": "{\"environment\":\"anthropic-only\",\"review_kind\":\"first\",\"reviewers\":[{\"alias\":\"claude-gw-tier1b[1m]\",\"fallback_depth\":0,\"fallbacks\":[],\"launch\":\"sonnet\",\"model\":\"claude-sonnet-5-5\",\"model_name\":\"Claude Sonnet 5.5\",\"reviewer_id\":\"t1b-1\",\"seed\":null,\"slot_id\":\"t1b\",\"stand_in\":false,\"strategy\":\"fixed\",\"tier\":\"tier1b\"},{\"alias\":\"claude-gw-tier2[1m]\",\"fallback_depth\":0,\"fallbacks\":[],\"launch\":\"haiku\",\"model\":\"claude-haiku-5-5\",\"model_name\":\"Claude Haiku 5.5\",\"reviewer_id\":\"t2-1\",\"seed\":\"1228767805|t2|1\",\"slot_id\":\"t2\",\"stand_in\":true,\"strategy\":\"random\",\"tier\":\"tier2\"},{\"alias\":\"claude-gw-tier3[1m]\",\"fallback_depth\":0,\"fallbacks\":[],\"launch\":\"haiku\",\"model\":\"claude-haiku-5-5\",\"model_name\":\"Claude Haiku 5.5\",\"reviewer_id\":\"t3-1\",\"seed\":\"1228767805|t3|1\",\"slot_id\":\"t3\",\"stand_in\":true,\"strategy\":\"random\",\"tier\":\"tier3\"},{\"alias\":\"claude-gw-tier3[1m]\",\"fallback_depth\":0,\"fallbacks\":[],\"launch\":\"haiku\",\"model\":\"claude-haiku-5-5\",\"model_name\":\"Claude Haiku 5.5\",\"reviewer_id\":\"t3-2\",\"seed\":\"1228767805|t3|2\",\"slot_id\":\"t3\",\"stand_in\":true,\"strategy\":\"random\",\"tier\":\"tier3\"}],\"run_id\":\"golden-run\",\"schema\":\"review-panel-resolution/1\",\"template_id\":\"default\",\"template_sha256\":\"fd2ef963a5c5e6dab3f405ebe980523101bca51802fe372fc019927a787146ba\",\"template_version\":\"1.0.0\",\"tiers_sha256\":\"a35908fa6d4019ea3f01d7842b2090ac6432d40a36cdeb9a08c6f0b1f50f05be\",\"tiers_version\":\"1.0.0\"}",
- "live7|anthropic-only|first": "{\"environment\":\"anthropic-only\",\"review_kind\":\"first\",\"reviewers\":[{\"alias\":\"claude-gw-tier1b[1m]\",\"fallback_depth\":0,\"fallbacks\":[],\"launch\":\"sonnet\",\"model\":\"claude-sonnet-5-5\",\"model_name\":\"Claude Sonnet 5.5\",\"reviewer_id\":\"t1b-1\",\"seed\":null,\"slot_id\":\"t1b\",\"stand_in\":false,\"strategy\":\"fixed\",\"tier\":\"tier1b\"},{\"alias\":\"claude-gw-tier2[1m]\",\"fallback_depth\":0,\"fallbacks\":[],\"launch\":\"haiku\",\"model\":\"claude-haiku-5-5\",\"model_name\":\"Claude Haiku 5.5\",\"reviewer_id\":\"t2-1\",\"seed\":\"1228767805|t2|1\",\"slot_id\":\"t2\",\"stand_in\":true,\"strategy\":\"random\",\"tier\":\"tier2\"},{\"alias\":\"claude-gw-tier2b[1m]\",\"fallback_depth\":0,\"fallbacks\":[],\"launch\":\"haiku\",\"model\":\"claude-haiku-5-5\",\"model_name\":\"Claude Haiku 5.5\",\"reviewer_id\":\"t2b-1\",\"seed\":\"1228767805|t2b|1\",\"slot_id\":\"t2b\",\"stand_in\":true,\"strategy\":\"random\",\"tier\":\"tier2b\"},{\"alias\":\"claude-gw-tier3[1m]\",\"fallback_depth\":0,\"fallbacks\":[],\"launch\":\"haiku\",\"model\":\"claude-haiku-5-5\",\"model_name\":\"Claude Haiku 5.5\",\"reviewer_id\":\"t3-1\",\"seed\":\"1228767805|t3|1\",\"slot_id\":\"t3\",\"stand_in\":true,\"strategy\":\"random\",\"tier\":\"tier3\"},{\"alias\":\"claude-gw-tier3[1m]\",\"fallback_depth\":0,\"fallbacks\":[],\"launch\":\"haiku\",\"model\":\"claude-haiku-5-5\",\"model_name\":\"Claude Haiku 5.5\",\"reviewer_id\":\"t3-2\",\"seed\":\"1228767805|t3|2\",\"slot_id\":\"t3\",\"stand_in\":true,\"strategy\":\"random\",\"tier\":\"tier3\"},{\"alias\":\"claude-gw-tier4[1m]\",\"fallback_depth\":1,\"fallbacks\":[],\"launch\":\"haiku\",\"model\":\"claude-haiku-5-5\",\"model_name\":\"Claude Haiku 5.5\",\"reviewer_id\":\"t4-1\",\"seed\":\"1228767805|t4|1\",\"slot_id\":\"t4\",\"stand_in\":false,\"strategy\":\"random\",\"tier\":\"tier4\"},{\"alias\":\"claude-gw-tier4[1m]\",\"fallback_depth\":1,\"fallbacks\":[],\"launch\":\"haiku\",\"model\":\"claude-haiku-5-5\",\"model_name\":\"Claude Haiku 5.5\",\"reviewer_id\":\"t4-2\",\"seed\":\"1228767805|t4|2\",\"slot_id\":\"t4\",\"stand_in\":false,\"strategy\":\"random\",\"tier\":\"tier4\"}],\"run_id\":\"golden-run\",\"schema\":\"review-panel-resolution/1\",\"template_id\":\"live7\",\"template_sha256\":\"191ea47fb9c5617b24e132c81e173fb0f67896c22be122736ffb9e4bc463a848\",\"template_version\":\"1.0.0\",\"tiers_sha256\":\"a35908fa6d4019ea3f01d7842b2090ac6432d40a36cdeb9a08c6f0b1f50f05be\",\"tiers_version\":\"1.0.0\"}",
- "tiers_sha256": "a35908fa6d4019ea3f01d7842b2090ac6432d40a36cdeb9a08c6f0b1f50f05be"
+ "default|anthropic-only|first": "{\"environment\":\"anthropic-only\",\"review_kind\":\"first\",\"reviewers\":[{\"alias\":\"claude-gw-tier1b[1m]\",\"fallback_depth\":0,\"fallbacks\":[],\"launch\":\"sonnet\",\"model\":\"claude-sonnet-5-5\",\"model_name\":\"Claude Sonnet 5.5\",\"reviewer_id\":\"t1b-1\",\"seed\":null,\"slot_id\":\"t1b\",\"stand_in\":false,\"strategy\":\"fixed\",\"tier\":\"tier1b\"},{\"alias\":\"claude-gw-tier2[1m]\",\"fallback_depth\":0,\"fallbacks\":[],\"launch\":\"haiku\",\"model\":\"claude-haiku-5-5\",\"model_name\":\"Claude Haiku 5.5\",\"reviewer_id\":\"t2-1\",\"seed\":\"1228767805|t2|1\",\"slot_id\":\"t2\",\"stand_in\":true,\"strategy\":\"random\",\"tier\":\"tier2\"},{\"alias\":\"claude-gw-tier3[1m]\",\"fallback_depth\":0,\"fallbacks\":[],\"launch\":\"haiku\",\"model\":\"claude-haiku-5-5\",\"model_name\":\"Claude Haiku 5.5\",\"reviewer_id\":\"t3-1\",\"seed\":\"1228767805|t3|1\",\"slot_id\":\"t3\",\"stand_in\":true,\"strategy\":\"random\",\"tier\":\"tier3\"},{\"alias\":\"claude-gw-tier3[1m]\",\"fallback_depth\":0,\"fallbacks\":[],\"launch\":\"haiku\",\"model\":\"claude-haiku-5-5\",\"model_name\":\"Claude Haiku 5.5\",\"reviewer_id\":\"t3-2\",\"seed\":\"1228767805|t3|2\",\"slot_id\":\"t3\",\"stand_in\":true,\"strategy\":\"random\",\"tier\":\"tier3\"}],\"run_id\":\"golden-run\",\"schema\":\"review-panel-resolution/1\",\"template_id\":\"default\",\"template_sha256\":\"fd2ef963a5c5e6dab3f405ebe980523101bca51802fe372fc019927a787146ba\",\"template_version\":\"1.0.0\",\"tiers_sha256\":\"66a55376777d02d60cf10fb86fe47295bc67cca8910c608c9f29d999077e845b\",\"tiers_version\":\"1.1.0\"}",
+ "live7|anthropic-only|first": "{\"environment\":\"anthropic-only\",\"review_kind\":\"first\",\"reviewers\":[{\"alias\":\"claude-gw-tier1b[1m]\",\"fallback_depth\":0,\"fallbacks\":[],\"launch\":\"sonnet\",\"model\":\"claude-sonnet-5-5\",\"model_name\":\"Claude Sonnet 5.5\",\"reviewer_id\":\"t1b-1\",\"seed\":null,\"slot_id\":\"t1b\",\"stand_in\":false,\"strategy\":\"fixed\",\"tier\":\"tier1b\"},{\"alias\":\"claude-gw-tier2[1m]\",\"fallback_depth\":0,\"fallbacks\":[],\"launch\":\"haiku\",\"model\":\"claude-haiku-5-5\",\"model_name\":\"Claude Haiku 5.5\",\"reviewer_id\":\"t2-1\",\"seed\":\"1228767805|t2|1\",\"slot_id\":\"t2\",\"stand_in\":true,\"strategy\":\"random\",\"tier\":\"tier2\"},{\"alias\":\"claude-gw-tier2b[1m]\",\"fallback_depth\":0,\"fallbacks\":[],\"launch\":\"haiku\",\"model\":\"claude-haiku-5-5\",\"model_name\":\"Claude Haiku 5.5\",\"reviewer_id\":\"t2b-1\",\"seed\":\"1228767805|t2b|1\",\"slot_id\":\"t2b\",\"stand_in\":true,\"strategy\":\"random\",\"tier\":\"tier2b\"},{\"alias\":\"claude-gw-tier3[1m]\",\"fallback_depth\":0,\"fallbacks\":[],\"launch\":\"haiku\",\"model\":\"claude-haiku-5-5\",\"model_name\":\"Claude Haiku 5.5\",\"reviewer_id\":\"t3-1\",\"seed\":\"1228767805|t3|1\",\"slot_id\":\"t3\",\"stand_in\":true,\"strategy\":\"random\",\"tier\":\"tier3\"},{\"alias\":\"claude-gw-tier3[1m]\",\"fallback_depth\":0,\"fallbacks\":[],\"launch\":\"haiku\",\"model\":\"claude-haiku-5-5\",\"model_name\":\"Claude Haiku 5.5\",\"reviewer_id\":\"t3-2\",\"seed\":\"1228767805|t3|2\",\"slot_id\":\"t3\",\"stand_in\":true,\"strategy\":\"random\",\"tier\":\"tier3\"},{\"alias\":\"claude-gw-tier4[1m]\",\"fallback_depth\":1,\"fallbacks\":[],\"launch\":\"haiku\",\"model\":\"claude-haiku-5-5\",\"model_name\":\"Claude Haiku 5.5\",\"reviewer_id\":\"t4-1\",\"seed\":\"1228767805|t4|1\",\"slot_id\":\"t4\",\"stand_in\":false,\"strategy\":\"random\",\"tier\":\"tier4\"},{\"alias\":\"claude-gw-tier4[1m]\",\"fallback_depth\":1,\"fallbacks\":[],\"launch\":\"haiku\",\"model\":\"claude-haiku-5-5\",\"model_name\":\"Claude Haiku 5.5\",\"reviewer_id\":\"t4-2\",\"seed\":\"1228767805|t4|2\",\"slot_id\":\"t4\",\"stand_in\":false,\"strategy\":\"random\",\"tier\":\"tier4\"}],\"run_id\":\"golden-run\",\"schema\":\"review-panel-resolution/1\",\"template_id\":\"live7\",\"template_sha256\":\"191ea47fb9c5617b24e132c81e173fb0f67896c22be122736ffb9e4bc463a848\",\"template_version\":\"1.0.0\",\"tiers_sha256\":\"66a55376777d02d60cf10fb86fe47295bc67cca8910c608c9f29d999077e845b\",\"tiers_version\":\"1.1.0\"}",
+ "tiers_sha256": "66a55376777d02d60cf10fb86fe47295bc67cca8910c608c9f29d999077e845b"
 }
diff --git a/tests/review/test_review_cli.py b/tests/review/test_review_cli.py
index 047fe9ca7..e23148a47 100644
--- a/tests/review/test_review_cli.py
+++ b/tests/review/test_review_cli.py
@@ -50,7 +50,17 @@ def test_review_help_lists_the_subcommands():
 
 
 def test_panel_resolve_prints_json():
-    res = run("review", "panel", "resolve", "--env", "anthropic-only", "--run-id", "x")
+    res = run(
+        "review",
+        "panel",
+        "resolve",
+        "--template",
+        "@classic",
+        "--env",
+        "anthropic-only",
+        "--run-id",
+        "x",
+    )
     assert res.exit_code == 0, res.output
     out = json.loads(res.output)
     assert [r["reviewer_id"] for r in out["reviewers"]] == [
@@ -65,6 +75,8 @@ def test_panel_resolve_prints_json():
             "review",
             "panel",
             "resolve",
+            "--template",
+            "@classic",
             "--env",
             "anthropic-only",
             "--run-id",
@@ -75,7 +87,15 @@ def test_panel_resolve_prints_json():
     )
     assert [r["reviewer_id"] for r in rr["reviewers"]] == ["t1b-1"]
     again = run(
-        "review", "panel", "resolve", "--env", "anthropic-only", "--run-id", "x"
+        "review",
+        "panel",
+        "resolve",
+        "--template",
+        "@classic",
+        "--env",
+        "anthropic-only",
+        "--run-id",
+        "x",
     )
     assert again.output == res.output
 
@@ -204,7 +224,15 @@ def test_merge_revise_verdict_round_trip(tmp_path):
     resolution = tmp_path / "panel.json"
     resolution.write_text(
         run(
-            "review", "panel", "resolve", "--env", "anthropic-only", "--run-id", "x"
+            "review",
+            "panel",
+            "resolve",
+            "--template",
+            "@classic",
+            "--env",
+            "anthropic-only",
+            "--run-id",
+            "x",
         ).output
     )
     out1 = tmp_path / "review" / "round1.md"
diff --git a/tests/review/test_review_panel.py b/tests/review/test_review_panel.py
index c7a18f65e..43d0235fd 100644
--- a/tests/review/test_review_panel.py
+++ b/tests/review/test_review_panel.py
@@ -18,7 +18,7 @@ def tiers():
 
 @pytest.fixture
 def tpl():
-    return pnl.load_panel()
+    return pnl.load_panel("@classic")
 
 
 def test_default_files_validate(tiers, tpl):
@@ -357,7 +357,7 @@ def test_template_lookup_precedence(tmp_path, monkeypatch):
     monkeypatch.setenv("HOME", str(home))
     monkeypatch.delenv("SUPERCLAUDE_REVIEW_PANEL", raising=False)
     monkeypatch.chdir(proj)
-    assert pnl.load_panel()["template_id"] == "default"
+    assert pnl.load_panel()["template_id"] == "wonsol"
     write(home / ".superclaude" / "review-panel.json", "from-user")
     assert pnl.load_panel()["template_id"] == "from-user"
     write(proj / ".superclaude" / "review-panel.json", "from-project")
@@ -398,7 +398,7 @@ def test_invalid_template_file_is_rejected(tmp_path):
 
 def test_packaged_defaults_are_read_through_importlib_resources():
     root = Path(pnl.__file__).parent / "data"
-    assert (root / "review-panel.default.json").is_file()
+    assert (root / "review-default.json").is_file()
     assert (root / "review-tiers.default.json").is_file()
 
 
diff --git a/tests/review/test_review_panel_exclusion.py b/tests/review/test_review_panel_exclusion.py
index 92ff78b00..fa59f183f 100644
--- a/tests/review/test_review_panel_exclusion.py
+++ b/tests/review/test_review_panel_exclusion.py
@@ -11,6 +11,7 @@ import json
 from pathlib import Path
 
 import pytest
+from review_panel_golden import golden_panel
 
 from superclaude.cli.review import panel as pnl
 
@@ -59,7 +60,7 @@ def test_no_exclusion_is_byte_identical_to_golden(frozen_tiers, key, explicit):
     name, env, kind = key.split("|")
     extra = {"hard_exclude": (), "strict_distinct": False} if explicit else {}
     res = pnl.resolve(
-        pnl.packaged_panel(name),
+        golden_panel(name),
         frozen_tiers,
         env,
         "golden-run",
diff --git a/tests/review/test_review_panel_live7.py b/tests/review/test_review_panel_live7.py
index 1dbf65e1d..c1dc7333a 100644
--- a/tests/review/test_review_panel_live7.py
+++ b/tests/review/test_review_panel_live7.py
@@ -39,10 +39,12 @@ def test_live7_is_valid_and_has_seven_reviewers(tiers, live7):
     }
 
 
-def test_default_panel_is_unchanged_by_live7(tiers):
+def test_default_is_wonsol_and_classic_and_live7_keep_their_size(tiers):
     default = pnl.load_panel()
-    assert default["template_id"] == "default"
-    assert sum(s["count"] for s in default["slots"]) == 4
+    assert default["template_id"] == "wonsol"
+    assert sum(s["count"] for s in default["slots"]) == 3
+    assert sum(s["count"] for s in pnl.load_panel("@classic")["slots"]) == 4
+    assert sum(s["count"] for s in pnl.load_panel("@live7")["slots"]) == 7
 
 
 def test_anthropic_only_resolves_to_one_sonnet_and_six_haiku(tiers, live7):
diff --git a/tests/review/test_review_panel_reflect_profile.py b/tests/review/test_review_panel_reflect_profile.py
index 99a80b969..1abbd06c3 100644
--- a/tests/review/test_review_panel_reflect_profile.py
+++ b/tests/review/test_review_panel_reflect_profile.py
@@ -14,6 +14,7 @@ from pathlib import Path
 
 import pytest
 from click.testing import CliRunner
+from review_panel_golden import golden_panel
 
 from superclaude.cli.review import panel as pnl
 from superclaude.cli.review import panel_cmd
@@ -76,7 +77,7 @@ def test_packaged_tiers_hash_and_resolutions_are_pinned(tiers):
     assert pnl.sha256_json(tiers) == golden["tiers_sha256"]
     for name in ("default", "live7"):
         res = pnl.resolve(
-            pnl.packaged_panel(name),
+            golden_panel(name),
             tiers,
             "anthropic-only",
             "golden-run",

--- new untracked file tests/review/review_panel_golden.py ---
"""Shared loader for the golden-resolution tests.

The goldens were taken when the packaged default template had the id `default`. That template now
lives on as `@classic` and the default is chosen by `review-default.json`, so the name `default`
is served from the frozen byte copy `fixtures/review-panel.default.frozen.json` and every other
name (such as `live7`) from the packaged templates.
"""

from __future__ import annotations

import json
from pathlib import Path

from superclaude.cli.review import panel as pnl

FROZEN_DEFAULT = Path(__file__).parent / "fixtures" / "review-panel.default.frozen.json"


def golden_panel(name: str) -> dict:
    if name == "default":
        return json.loads(FROZEN_DEFAULT.read_text(encoding="utf-8"))
    return pnl.packaged_panel(name)

--- new untracked file tests/review/test_review_default_template.py ---
"""The default review panel is chosen by the pointer file review-default.json, not by a file name in code."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from superclaude.cli.review import panel as pnl

DATA = Path(pnl.__file__).parent / "data"


@pytest.fixture(autouse=True)
def _no_user_overrides(tmp_path, monkeypatch):
    """No project or home review-panel.json and no environment variable can shadow the packaged default."""
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.delenv("SUPERCLAUDE_REVIEW_PANEL", raising=False)
    monkeypatch.chdir(tmp_path)


@pytest.fixture
def data_copy(tmp_path, monkeypatch):
    """A temporary copy of the packaged data folder that the loader reads instead of the real one."""
    root = tmp_path / "pkg"
    shutil.copytree(DATA, root / "data")
    monkeypatch.setattr(pnl.resources, "files", lambda _package: root)
    return root / "data"


def _point(data_copy, **fields):
    ptr = {"schema": "review-default/1", "template": "wonsol", **fields}
    (data_copy / "review-default.json").write_text(json.dumps(ptr))


def test_default_resolves_to_a_template_by_reference():
    name = json.loads((DATA / "review-default.json").read_text())["template"]
    assert pnl.default_template_name() == name
    assert pnl.load_panel()["template_id"] == name == "wonsol"


@pytest.mark.parametrize(
    "env, models, stand_ins",
    [
        (
            "anthropic-only",
            ["claude-sonnet-5-5", "claude-haiku-5-5", "claude-haiku-5-5"],
            [False, True, True],
        ),
        (
            "gateway",
            ["muse-wonder-1.0", "gpt-6.1-sol", "muse-ember-1.0"],
            [False, False, False],
        ),
    ],
)
def test_three_reviewer_default_resolves_in_both_environments(env, models, stand_ins):
    panel = pnl.load_panel()
    assert sum(s["count"] for s in panel["slots"]) == 3
    for run_id in ("t1", "t2", "t3"):
        out = pnl.resolve(panel, pnl.load_tiers(), env, run_id)
        assert [r["reviewer_id"] for r in out["reviewers"]] == [
            "t5a-1",
            "t5b-1",
            "t5c-1",
        ]
        assert [r["model"] for r in out["reviewers"]] == models
        assert [r["stand_in"] for r in out["reviewers"]] == stand_ins


def test_editing_the_pointer_switches_the_default_with_no_code_change(data_copy):
    assert pnl.load_panel()["template_id"] == "wonsol"
    _point(data_copy, template="classic")
    panel = pnl.load_panel()
    assert panel["template_id"] == "classic"
    assert sum(s["count"] for s in panel["slots"]) == 4


@pytest.mark.parametrize(
    "fields",
    [
        {"template": "no-such-template"},
        {"template": "Bad Name"},
        {"template": 5},
        {"schema": "review-default/2"},
    ],
)
def test_a_bad_pointer_is_rejected_and_names_the_pointer_file(data_copy, fields):
    _point(data_copy, **fields)
    with pytest.raises(ValueError, match="review-default.json"):
        pnl.load_panel()


def test_a_project_panel_file_still_overrides_the_pointer(tmp_path):
    (tmp_path / ".superclaude").mkdir()
    own = pnl.load_panel("@live7")
    own["template_id"] = "from-project"
    (tmp_path / ".superclaude" / "review-panel.json").write_text(json.dumps(own))
    assert pnl.load_panel()["template_id"] == "from-project"


Codegraph context: index_state: fresh, checked_at: 2026-11-17T21:16:22Z, worktree_root: /home/coder/workspaces/worktrees/IronClaude/wonsol-default, projectPath: same. Call codegraph only when index_state: fresh, never to widen scope. Q2b: this task edits tests only; no production dependents changed.
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
