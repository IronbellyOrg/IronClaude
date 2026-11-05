1c746b15079f00b4db397b4f4cec3071a4120dfc
Review one task for spec compliance.

Task brief: ## Task 1: Add the restricted-owner tests to tests/unit/test_ccsession_tiers.py

Covers R-006 and, through its expectations, R-003 and R-005.

Append three tests after `test_non_tier_launch_leaves_the_alias_variables_unset` at the end of `tests/unit/test_ccsession_tiers.py`, using `ALIAS_VARIABLES`, `_launch`, `ACCESS_BLOCK` (the access setting that limits `bob` to tier2 and tier3) and the `_isolated` fixture, and removing the three variables first with `monkeypatch.delenv` as the existing tests do. The existing `test_tier_launch_exports_the_alias_variables` already covers an unrestricted owner and the existing non-tier test covers R-005; leave both unchanged.

- `test_limited_owner_gets_only_the_haiku_alias_variable`: launch with `defaults=ACCESS_BLOCK` and `CODER_WORKSPACE_OWNER_NAME="bob"`, all three variables unset; expect `seen["opus_model"] == ""`, `seen["sonnet_model"] == ""` and `seen["haiku_model"] == "claude-gw-tier2"`.
- `test_limited_owner_keeps_inherited_alias_values`: same launch with `monkeypatch.setenv` giving the opus and sonnet variables the sentinel values `inherited-opus` and `inherited-sonnet`; expect those two values unchanged and `seen["haiku_model"] == "claude-gw-tier2"`.
- `test_workspace_without_tier1a_and_tier1b_exports_only_its_tiers`: before launching, write `$XDG_CACHE_HOME/ccsession/models.json` (the `_isolated` fixture sets a private `XDG_CACHE_HOME`) as a copy of `src/superclaude/skills/ccsession-tag/ccsession-models.json` with the `tier1a` and `tier1b` entries removed from `tiers` and `version` set to a string that sorts above the bundled one (`models.py` `load()` takes the newest copy); launch with the unrestricted `TIER_BLOCK` and the opus and sonnet variables set to sentinel values; expect the sentinels unchanged and `seen["haiku_model"] == "claude-gw-tier2"`.

Run `uv run pytest tests/unit/test_ccsession_tiers.py -k "alias_variable or limited_owner or without_tier1a" -v` on the launcher as it stands (unconditional exports) and save the output to `./artifacts/t1-red.log`.

Acceptance criteria:
- `./artifacts/t1-red.log` shows the three new tests failing with an AssertionError (the opus and sonnet values are `claude-gw-tier1a` and `claude-gw-tier1b` where the test expects empty or sentinel values) and the two existing alias tests passing.
- `uv run ruff check tests/unit/test_ccsession_tiers.py` and `uv run ruff format --check tests/unit/test_ccsession_tiers.py` pass.

AC ids (in source order):
T1.AC1: `./artifacts/t1-red.log` shows the three new tests failing with an AssertionError (the opus and sonnet values are `claude-gw-tier1a` and `claude-gw-tier1b` where the test expects empty or sentinel values) and the two existing alias tests passing.
T1.AC2: `uv run ruff check tests/unit/test_ccsession_tiers.py` and `uv run ruff format --check tests/unit/test_ccsession_tiers.py` pass.
Global constraints: ## Constraints

- Only `src/superclaude/skills/ccsession-tag/ccsession` changes under `src/superclaude/skills/ccsession-tag/`; `models.py`, `local-gateway-alias-proxy.py` and `ccsession-orca` stay untouched (R-002).
- The three unconditional export lines from the first follow-up already sit right after `USE_SHIM=1` in the tier-mode branch of `src/superclaude/skills/ccsession-tag/ccsession` (about lines 867-870); re-read the file before editing and change only those lines (R-001).
- Do not stage `.claude/`. Edit only under `src/`, `tests/`, `docs/` and `CHANGELOG.md`.
- Docs say only what the code and the probe records show; no probe exercised the Agent-call `model` parameter.
- R-008 (the pull request body) changes no file and has no task; it is written when the pull request is opened. R-004 has no launcher-level test because a broken access entry makes the launcher exit before Claude starts (`apply_tier_selection`, `|| exit 2`).
Start sha: 1c746b15079f00b4db397b4f4cec3071a4120dfc
Diff against the start snapshot: diff --git a/tests/unit/test_ccsession_tiers.py b/tests/unit/test_ccsession_tiers.py
index 941f2d1a..df655a5d 100644
--- a/tests/unit/test_ccsession_tiers.py
+++ b/tests/unit/test_ccsession_tiers.py
@@ -2925,3 +2925,79 @@ def test_non_tier_launch_leaves_the_alias_variables_unset(
         "",
         "",
     )
+
+
+def _seen_aliases(seen) -> tuple:
+    return (seen["opus_model"], seen["sonnet_model"], seen["haiku_model"])
+
+
+def test_limited_owner_gets_only_the_haiku_alias_variable(
+    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
+) -> None:
+    # bob may use tier2 and tier3 only (ACCESS_BLOCK), so tier1a and tier1b are
+    # not his: the opus and sonnet variables are not exported.
+    for name in ALIAS_VARIABLES:
+        monkeypatch.delenv(name, raising=False)
+    rc, out, err, seen = _launch(
+        tmp_path, "work", defaults=ACCESS_BLOCK, CODER_WORKSPACE_OWNER_NAME="bob"
+    )
+    assert rc == 0, err
+    assert _seen_aliases(seen) == ("", "", "claude-gw-tier2")
+
+
+def test_limited_owner_keeps_inherited_alias_values(
+    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
+) -> None:
+    # A variable for a tier the owner may not use stays exactly as inherited;
+    # the one for a tier the owner may use is set.
+    monkeypatch.setenv("ANTHROPIC_DEFAULT_OPUS_MODEL", "inherited-opus")
+    monkeypatch.setenv("ANTHROPIC_DEFAULT_SONNET_MODEL", "inherited-sonnet")
+    monkeypatch.setenv("ANTHROPIC_DEFAULT_HAIKU_MODEL", "inherited-haiku")
+    rc, out, err, seen = _launch(
+        tmp_path, "work", defaults=ACCESS_BLOCK, CODER_WORKSPACE_OWNER_NAME="bob"
+    )
+    assert rc == 0, err
+    assert _seen_aliases(seen) == (
+        "inherited-opus",
+        "inherited-sonnet",
+        "claude-gw-tier2",
+    )
+
+
+def test_workspace_without_tier1a_and_tier1b_exports_only_its_tiers(
+    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
+) -> None:
+    # A newer cached model list without tier1a and tier1b (models.load() takes
+    # the newest copy): the workspace has no such tiers, so for any owner only
+    # the haiku variable is exported.
+    data = json.loads((SKILL_DIR / "ccsession-models.json").read_text())
+    for tier in ("tier1a", "tier1b"):
+        del data["tiers"][tier]
+    data["version"] = "2099-01-01.1"
+    cache = Path(os.environ["XDG_CACHE_HOME"]) / "ccsession"
+    cache.mkdir(parents=True, exist_ok=True)
+    (cache / "models.json").write_text(json.dumps(data))
+    loaded, source = models.load()
+    assert source == "downloaded" and "tier1a" not in loaded["tiers"]
+
+    # Inherited values unset ...
+    for name in ALIAS_VARIABLES:
+        monkeypatch.delenv(name, raising=False)
+    unset_dir = tmp_path / "unset"
+    unset_dir.mkdir()
+    rc, out, err, seen = _launch(unset_dir, "work")
+    assert rc == 0, err
+    assert _seen_aliases(seen) == ("", "", "claude-gw-tier2")
+
+    # ... and inherited values already set.
+    monkeypatch.setenv("ANTHROPIC_DEFAULT_OPUS_MODEL", "inherited-opus")
+    monkeypatch.setenv("ANTHROPIC_DEFAULT_SONNET_MODEL", "inherited-sonnet")
+    set_dir = tmp_path / "set"
+    set_dir.mkdir()
+    rc, out, err, seen = _launch(set_dir, "work")
+    assert rc == 0, err
+    assert _seen_aliases(seen) == (
+        "inherited-opus",
+        "inherited-sonnet",
+        "claude-gw-tier2",
+    )

diff --git a/.dev/tasks/to-do/TASK-WF-launcherAccessAw-20261105-144815/artifacts/t1-red.log b/.dev/tasks/to-do/TASK-WF-launcherAccessAw-20261105-144815/artifacts/t1-red.log
new file mode 100644
index 00000000..d820433e
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-launcherAccessAw-20261105-144815/artifacts/t1-red.log
@@ -0,0 +1,99 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0 -- /home/coder/workspaces/worktrees/IronClaude/issue-384-launcher-tier-aliases/.venv/bin/python
+SuperClaude: 5.0.0
+benchmark: 5.3.1 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
+rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-384-launcher-tier-aliases
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, benchmark-5.3.1, anyio-4.16.0, cov-7.1.0
+collecting ... collected 136 items / 131 deselected / 5 selected
+
+tests/unit/test_ccsession_tiers.py::test_tier_launch_exports_the_alias_variables PASSED [ 20%]
+tests/unit/test_ccsession_tiers.py::test_non_tier_launch_leaves_the_alias_variables_unset PASSED [ 40%]
+tests/unit/test_ccsession_tiers.py::test_limited_owner_gets_only_the_haiku_alias_variable FAILED [ 60%]
+tests/unit/test_ccsession_tiers.py::test_limited_owner_keeps_inherited_alias_values FAILED [ 80%]
+tests/unit/test_ccsession_tiers.py::test_workspace_without_tier1a_and_tier1b_exports_only_its_tiers FAILED [100%]
+
+=================================== FAILURES ===================================
+____________ test_limited_owner_gets_only_the_haiku_alias_variable _____________
+tests/unit/test_ccsession_tiers.py:2945: in test_limited_owner_gets_only_the_haiku_alias_variable
+    assert _seen_aliases(seen) == ("", "", "claude-gw-tier2")
+E   AssertionError: assert ('claude-gw-tier1a', 'claude-gw-tier1b', 'claude-gw-tier2') == ('', '', 'claude-gw-tier2')
+E     
+E     At index 0 diff: 'claude-gw-tier1a' != ''
+E     
+E     Full diff: (-: missing in left side, +: extra in left side)
+E       (
+E     -     '',
+E     -     '',
+E     +     'claude-gw-tier1a',
+E     +     'claude-gw-tier1b',
+E           'claude-gw-tier2',
+E       )
+_______________ test_limited_owner_keeps_inherited_alias_values ________________
+tests/unit/test_ccsession_tiers.py:2960: in test_limited_owner_keeps_inherited_alias_values
+    assert _seen_aliases(seen) == (
+E   AssertionError: assert ('claude-gw-tier1a', 'claude-gw-tier1b', 'claude-gw-tier2') == ('inherited-opus', 'inherited-sonnet', 'claude-gw-tier2')
+E     
+E     At index 0 diff: 'claude-gw-tier1a' != 'inherited-opus'
+E     
+E     Full diff: (-: missing in left side, +: extra in left side)
+E       (
+E     -     'inherited-opus',
+E     -     'inherited-sonnet',
+E     +     'claude-gw-tier1a',
+E     +     'claude-gw-tier1b',
+E           'claude-gw-tier2',
+E       )
+_______ test_workspace_without_tier1a_and_tier1b_exports_only_its_tiers ________
+tests/unit/test_ccsession_tiers.py:2990: in test_workspace_without_tier1a_and_tier1b_exports_only_its_tiers
+    assert _seen_aliases(seen) == ("", "", "claude-gw-tier2")
+E   AssertionError: assert ('claude-gw-tier1a', 'claude-gw-tier1b', 'claude-gw-tier2') == ('', '', 'claude-gw-tier2')
+E     
+E     At index 0 diff: 'claude-gw-tier1a' != ''
+E     
+E     Full diff: (-: missing in left side, +: extra in left side)
+E       (
+E     -     '',
+E     -     '',
+E     +     'claude-gw-tier1a',
+E     +     'claude-gw-tier1b',
+E           'claude-gw-tier2',
+E       )
+=========================== short test summary info ============================
+FAILED tests/unit/test_ccsession_tiers.py::test_limited_owner_gets_only_the_haiku_alias_variable - AssertionError: assert ('claude-gw-tier1a', 'claude-gw-tier1b', 'claude-gw-tier2') == ('', '', 'claude-gw-tier2')
+  
+  At index 0 diff: 'claude-gw-tier1a' != ''
+  
+  Full diff: (-: missing in left side, +: extra in left side)
+    (
+  -     '',
+  -     '',
+  +     'claude-gw-tier1a',
+  +     'claude-gw-tier1b',
+        'claude-gw-tier2',
+    )
+FAILED tests/unit/test_ccsession_tiers.py::test_limited_owner_keeps_inherited_alias_values - AssertionError: assert ('claude-gw-tier1a', 'claude-gw-tier1b', 'claude-gw-tier2') == ('inherited-opus', 'inherited-sonnet', 'claude-gw-tier2')
+  
+  At index 0 diff: 'claude-gw-tier1a' != 'inherited-opus'
+  
+  Full diff: (-: missing in left side, +: extra in left side)
+    (
+  -     'inherited-opus',
+  -     'inherited-sonnet',
+  +     'claude-gw-tier1a',
+  +     'claude-gw-tier1b',
+        'claude-gw-tier2',
+    )
+FAILED tests/unit/test_ccsession_tiers.py::test_workspace_without_tier1a_and_tier1b_exports_only_its_tiers - AssertionError: assert ('claude-gw-tier1a', 'claude-gw-tier1b', 'claude-gw-tier2') == ('', '', 'claude-gw-tier2')
+  
+  At index 0 diff: 'claude-gw-tier1a' != ''
+  
+  Full diff: (-: missing in left side, +: extra in left side)
+    (
+  -     '',
+  -     '',
+  +     'claude-gw-tier1a',
+  +     'claude-gw-tier1b',
+        'claude-gw-tier2',
+    )
+================= 3 failed, 2 passed, 131 deselected in 2.93s ==================

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
