02277363261d75eb021f9ea75d07b4a54d70e3c8
Review one task for spec compliance.

Task brief: ## Task 1: Add the three Ponytail entries to the defaults file and pin them with tests

Edit `src/superclaude/cli/user_settings_defaults.json` (FR-001..FR-003, Design 3.1): append `"ponytail@ponytail": true` to `enabledPlugins` after `understand-anything@understand-anything`; append `"ponytail": {"source": {"source": "github", "repo": "DietrichGebert/ponytail"}}` to `extraKnownMarketplaces`; append `"PONYTAIL_DEFAULT_MODE": "lite"` to `env`. No other key changes. `apply_settings_defaults` (`install_user_setup.py:150-164`, `_NESTED_KEYS` at `:36`) already fills these entry by entry, and `install_plugins` (`:251-311`) already installs every enabled default, so no Python change is needed for this.

In `tests/cli/test_install_user_setup.py`:
- T1: new `test_defaults_ship_ponytail` loads the defaults file and asserts `enabledPlugins["ponytail@ponytail"] is True`, `extraKnownMarketplaces["ponytail"]["source"] == {"source": "github", "repo": "DietrichGebert/ponytail"}`, `env["PONYTAIL_DEFAULT_MODE"] == "lite"`, and that every `enabledPlugins` key's marketplace (text after `@`) has a `source.repo` in `extraKnownMarketplaces`. It must not assert key order and must assert no `pluginConfigs` key.
- T2: extend `test_plugins_install_missing_enabled_defaults` (`:182-209`) with `["plugin", "marketplace", "add", "DietrichGebert/ponytail"] in calls` and `"ponytail@ponytail" in installs`.
- T3/T4: extend `test_settings_defaults_fill_only_missing_values` (`:73-98`) or add a sibling test with two legs. Leg 1 (existing user): settings hold the old six plugins and the two old marketplaces; after `apply_settings_defaults`, `enabledPlugins["ponytail@ponytail"] is True`, `extraKnownMarketplaces["ponytail"]` is present, `env["PONYTAIL_DEFAULT_MODE"] == "lite"`, the existing values are unchanged, and a second run returns `(True, "✅ Settings defaults: already present")`. Leg 2 (user choice kept): with `enabledPlugins["ponytail@ponytail"] = False` and `env["PONYTAIL_DEFAULT_MODE"] = "full"` in settings, both values are unchanged after apply.

Acceptance criteria:
- `user_settings_defaults.json` is valid JSON and differs from master only by the three added entries (`git diff` shows three added lines plus the needed commas/braces).
- T1, T2 and both T3/T4 legs pass under `uv run pytest tests/cli/test_install_user_setup.py -v`; T1 fails if `PONYTAIL_DEFAULT_MODE` is anything other than `lite` or if the ponytail marketplace entry is removed.
- `test_plugins_skip_already_installed` (T6) passes unchanged.

AC ids: T1.AC1,T1.AC2,T1.AC3 (in the order of the Acceptance criteria bullets)
Global constraints: ## Constraints

- Change only `src/superclaude/cli/user_settings_defaults.json`, `src/superclaude/cli/install_user_setup.py` (at most 5 changed lines, failure label only), `tests/cli/test_install_user_setup.py`, `docs/getting-started/installation.md` and `CHANGELOG.md`. No change to `main.py`, `update.sh`, `doctor.py`, output styles, rules, hooks, any skill, command or agent, or any `.claude/` file.
- Never run `superclaude install`, `superclaude update`, `./update.sh` or `claude plugin ...` against this workspace's `~/.claude`; any manual proof uses a throwaway `HOME` under `/tmp` that is removed afterwards.
- No `pluginConfigs` entry, no `statusLine` setting, no write outside `~/.claude`, no version pin, no new module, constant, flag or CLI option.
- A user's existing `enabledPlugins`, `env` and marketplace values are never changed.
- `.dev/tasks/` is always staged (`git add .dev/tasks`); never stage `.claude/` paths.
- The superseded package `.dev/tasks/to-do/TASK-WF-closeIronbellyOr-20261104-084334/` and `.dev/reflect/pre-closeIronbellyOr-20261104084538/` stay on disk untouched.
Start sha: 02277363261d75eb021f9ea75d07b4a54d70e3c8
Diff against the start snapshot: diff --git a/src/superclaude/cli/user_settings_defaults.json b/src/superclaude/cli/user_settings_defaults.json
index b095ef6e..99674c27 100644
--- a/src/superclaude/cli/user_settings_defaults.json
+++ b/src/superclaude/cli/user_settings_defaults.json
@@ -9,7 +9,8 @@
   "skipDangerousModePermissionPrompt": true,
   "env": {
     "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1",
-    "CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION": "5000"
+    "CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION": "5000",
+    "PONYTAIL_DEFAULT_MODE": "lite"
   },
   "modelSettings": {
     "gpt-6-astra": {
@@ -31,7 +32,8 @@
     "notion@claude-plugins-official": true,
     "dropbox@claude-plugins-official": true,
     "google-cloud-storage@claude-plugins-official": true,
-    "understand-anything@understand-anything": true
+    "understand-anything@understand-anything": true,
+    "ponytail@ponytail": true
   },
   "extraKnownMarketplaces": {
     "claude-plugins-official": {
@@ -45,6 +47,12 @@
         "source": "github",
         "repo": "Lum1104/Understand-Anything"
       }
+    },
+    "ponytail": {
+      "source": {
+        "source": "github",
+        "repo": "DietrichGebert/ponytail"
+      }
     }
   }
 }
diff --git a/tests/cli/test_install_user_setup.py b/tests/cli/test_install_user_setup.py
index 91c0d855..394f530d 100644
--- a/tests/cli/test_install_user_setup.py
+++ b/tests/cli/test_install_user_setup.py
@@ -98,6 +98,80 @@ def test_settings_defaults_fill_only_missing_values(tmp_path: Path) -> None:
     assert again == (True, "✅ Settings defaults: already present")
 
 
+def _defaults() -> dict:
+    return json.loads(
+        (Path(setup.__file__).parent / "user_settings_defaults.json").read_text()
+    )
+
+
+def test_defaults_ship_ponytail() -> None:
+    defaults = _defaults()
+    assert defaults["enabledPlugins"]["ponytail@ponytail"] is True
+    assert defaults["extraKnownMarketplaces"]["ponytail"]["source"] == {
+        "source": "github",
+        "repo": "DietrichGebert/ponytail",
+    }
+    assert defaults["env"]["PONYTAIL_DEFAULT_MODE"] == "lite"
+    assert "pluginConfigs" not in defaults
+    # Every default plugin's marketplace must be installable by install_plugins.
+    for plugin in defaults["enabledPlugins"]:
+        market = plugin.split("@", 1)[1]
+        assert defaults["extraKnownMarketplaces"][market]["source"]["repo"], plugin
+
+
+def test_settings_defaults_add_ponytail_for_existing_users(tmp_path: Path) -> None:
+    claude = tmp_path / ".claude"
+    claude.mkdir()
+    defaults = _defaults()
+    old_plugins = {
+        p: True for p in defaults["enabledPlugins"] if p != "ponytail@ponytail"
+    }
+    old_markets = {
+        m: v for m, v in defaults["extraKnownMarketplaces"].items() if m != "ponytail"
+    }
+    (claude / "settings.json").write_text(
+        json.dumps(
+            {
+                "env": {"CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"},
+                "enabledPlugins": old_plugins,
+                "extraKnownMarketplaces": old_markets,
+            }
+        )
+    )
+    assert setup.apply_settings_defaults(home=tmp_path)[0]
+    settings = _settings(tmp_path)
+    assert settings["enabledPlugins"]["ponytail@ponytail"] is True
+    assert settings["extraKnownMarketplaces"]["ponytail"]["source"]["repo"] == (
+        "DietrichGebert/ponytail"
+    )
+    assert settings["env"]["PONYTAIL_DEFAULT_MODE"] == "lite"
+    for plugin, value in old_plugins.items():
+        assert settings["enabledPlugins"][plugin] is value
+    for market, value in old_markets.items():
+        assert settings["extraKnownMarketplaces"][market] == value
+    assert setup.apply_settings_defaults(home=tmp_path) == (
+        True,
+        "✅ Settings defaults: already present",
+    )
+
+
+def test_settings_defaults_keep_user_ponytail_choices(tmp_path: Path) -> None:
+    claude = tmp_path / ".claude"
+    claude.mkdir()
+    (claude / "settings.json").write_text(
+        json.dumps(
+            {
+                "env": {"PONYTAIL_DEFAULT_MODE": "full"},
+                "enabledPlugins": {"ponytail@ponytail": False},
+            }
+        )
+    )
+    assert setup.apply_settings_defaults(home=tmp_path)[0]
+    settings = _settings(tmp_path)
+    assert settings["env"]["PONYTAIL_DEFAULT_MODE"] == "full"
+    assert settings["enabledPlugins"]["ponytail@ponytail"] is False
+
+
 def test_settings_defaults_refuse_malformed_file(tmp_path: Path) -> None:
     claude = tmp_path / ".claude"
     claude.mkdir()
@@ -203,10 +277,12 @@ def test_plugins_install_missing_enabled_defaults(tmp_path: Path, monkeypatch) -
         "anthropics/claude-plugins-official",
     ] in calls
     assert ["plugin", "marketplace", "add", "Lum1104/Understand-Anything"] in calls
+    assert ["plugin", "marketplace", "add", "DietrichGebert/ponytail"] in calls
     installs = [c[2] for c in calls if c[:2] == ["plugin", "install"]]
     assert "notion@claude-plugins-official" not in installs
     assert "frontend-design@claude-plugins-official" in installs
     assert "understand-anything@understand-anything" in installs
+    assert "ponytail@ponytail" in installs
 
 
 def test_plugins_skip_already_installed(tmp_path: Path, monkeypatch) -> None:

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
