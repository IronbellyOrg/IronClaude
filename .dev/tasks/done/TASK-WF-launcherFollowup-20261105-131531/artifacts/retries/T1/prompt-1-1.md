676af6b666208ce9dc0c92bf45c30454e09c43f3
Review one task for spec compliance.

Task brief: ## Task 1: Add the failing-first tests and the harness keys to tests/unit/test_ccsession_tiers.py

In `tests/unit/test_ccsession_tiers.py`, add three lines to the `json.dump` call of the fake claude inside `_launch_env`, after the `"auth_token"` line, exactly as the source section "Harness addition" gives: `"opus_model"`, `"sonnet_model"` and `"haiku_model"`, read from `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL` and `ANTHROPIC_DEFAULT_HAIKU_MODEL` with default `""`. Append the `ALIAS_VARIABLES` tuple and the two tests `test_tier_launch_exports_the_alias_variables` and `test_non_tier_launch_leaves_the_alias_variables_unset` from the source section "Failing-first test" at the end of the file. Re-verify that the helper names they use (`_launch`, `_launch_env`, `_defaults`, `_isolated`, `TIER_BLOCK`, `SKILL_DIR`) still exist with the same signatures, and adapt the call shapes only where #315 changed them.

Run `uv run pytest tests/unit/test_ccsession_tiers.py -k alias_variables -v` on the unchanged launcher and save the output to `./artifacts/t1-red.log`.

Acceptance criteria:
- `./artifacts/t1-red.log` shows `test_tier_launch_exports_the_alias_variables` failing with an AssertionError whose three values are empty strings, and `test_non_tier_launch_leaves_the_alias_variables_unset` passing.
- The three harness keys are present in `_launch_env` and no other test in `tests/unit/test_ccsession_tiers.py` changes behaviour.

AC ids (in source order):
T1.AC1: `./artifacts/t1-red.log` shows `test_tier_launch_exports_the_alias_variables` failing with an AssertionError whose three values are empty strings, and `test_non_tier_launch_leaves_the_alias_variables_unset` passing.
T1.AC2: The three harness keys are present in `_launch_env` and no other test in `tests/unit/test_ccsession_tiers.py` changes behaviour.
Global constraints: ## Constraints

- Only `src/superclaude/skills/ccsession-tag/ccsession` changes under `src/superclaude/skills/ccsession-tag/`; `ccsession-orca` stays untouched.
- Re-verify every line number in the source against the code on the working branch before editing: the source numbers are at base commit 38eb3c58 and the #315 change edits the same files.
- Do not stage `.claude/`. Edit only under `src/`, `tests/`, `docs/` and `CHANGELOG.md`.
- Docs say only what the code and the two probe records show: the probe record is `.dev/issues/384/analysis/probe-alias-remap.md` (opus and haiku) and `.dev/issues/384/analysis/probe-sonnet-alias.md` (sonnet).
Start sha: 676af6b666208ce9dc0c92bf45c30454e09c43f3
Diff against the start snapshot: diff --git a/tests/unit/test_ccsession_tiers.py b/tests/unit/test_ccsession_tiers.py
index c87d6efe..d6dbb933 100644
--- a/tests/unit/test_ccsession_tiers.py
+++ b/tests/unit/test_ccsession_tiers.py
@@ -338,6 +338,9 @@ json.dump({
     "base_url": os.environ.get("ANTHROPIC_BASE_URL", ""),
     "api_key": os.environ.get("ANTHROPIC_API_KEY", ""),
     "auth_token": os.environ.get("ANTHROPIC_AUTH_TOKEN", ""),
+    "opus_model": os.environ.get("ANTHROPIC_DEFAULT_OPUS_MODEL", ""),
+    "sonnet_model": os.environ.get("ANTHROPIC_DEFAULT_SONNET_MODEL", ""),
+    "haiku_model": os.environ.get("ANTHROPIC_DEFAULT_HAIKU_MODEL", ""),
 }, open(os.environ["SEEN_FILE"], "w"))
 """
     )
@@ -2885,3 +2888,36 @@ def test_each_owner_gets_its_own_shim(tmp_path: Path) -> None:
         for owner in ("alice", "bob")
     }
     assert len(ports) == 2
+
+
+ALIAS_VARIABLES = (
+    "ANTHROPIC_DEFAULT_OPUS_MODEL",
+    "ANTHROPIC_DEFAULT_SONNET_MODEL",
+    "ANTHROPIC_DEFAULT_HAIKU_MODEL",
+)
+
+
+def test_tier_launch_exports_the_alias_variables(
+    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
+) -> None:
+    # The harness copies os.environ and the workspace exports these three
+    # variables, so remove them first: only the launcher may set them here.
+    for name in ALIAS_VARIABLES:
+        monkeypatch.delenv(name, raising=False)
+    rc, out, err, seen = _launch(tmp_path, "work")
+    assert rc == 0, err
+    assert (seen["opus_model"], seen["sonnet_model"], seen["haiku_model"]) == (
+        "claude-gw-tier1a",
+        "claude-gw-tier1b",
+        "claude-gw-tier2",
+    )
+
+
+def test_non_tier_launch_leaves_the_alias_variables_unset(
+    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
+) -> None:
+    for name in ALIAS_VARIABLES:
+        monkeypatch.delenv(name, raising=False)
+    rc, out, err, seen = _launch(tmp_path, "work", defaults=None)
+    assert rc == 0, err
+    assert (seen["opus_model"], seen["sonnet_model"], seen["haiku_model"]) == ("", "", "")

diff --git a/.dev/tasks/to-do/TASK-WF-launcherFollowup-20261105-131531/artifacts/t1-red.log b/.dev/tasks/to-do/TASK-WF-launcherFollowup-20261105-131531/artifacts/t1-red.log
new file mode 100644
index 00000000..5fd6939b
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-launcherFollowup-20261105-131531/artifacts/t1-red.log
@@ -0,0 +1,44 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0 -- /home/coder/workspaces/worktrees/IronClaude/issue-384-launcher-tier-aliases/.venv/bin/python
+SuperClaude: 5.0.0
+benchmark: 5.3.1 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
+rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-384-launcher-tier-aliases
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, benchmark-5.3.1, anyio-4.16.0, cov-7.1.0
+collecting ... collected 133 items / 131 deselected / 2 selected
+
+tests/unit/test_ccsession_tiers.py::test_tier_launch_exports_the_alias_variables FAILED [ 50%]
+tests/unit/test_ccsession_tiers.py::test_non_tier_launch_leaves_the_alias_variables_unset PASSED [100%]
+
+=================================== FAILURES ===================================
+_________________ test_tier_launch_exports_the_alias_variables _________________
+tests/unit/test_ccsession_tiers.py:2909: in test_tier_launch_exports_the_alias_variables
+    assert (seen["opus_model"], seen["sonnet_model"], seen["haiku_model"]) == (
+E   AssertionError: assert ('', '', '') == ('claude-gw-tier1a', 'claude-gw-tier1b', 'claude-gw-tier2')
+E     
+E     At index 0 diff: '' != 'claude-gw-tier1a'
+E     
+E     Full diff: (-: missing in left side, +: extra in left side)
+E       (
+E     -     'claude-gw-tier1a',
+E     -     'claude-gw-tier1b',
+E     -     'claude-gw-tier2',
+E     +     '',
+E     +     '',
+E     +     '',
+E       )
+=========================== short test summary info ============================
+FAILED tests/unit/test_ccsession_tiers.py::test_tier_launch_exports_the_alias_variables - AssertionError: assert ('', '', '') == ('claude-gw-tier1a', 'claude-gw-tier1b', 'claude-gw-tier2')
+  
+  At index 0 diff: '' != 'claude-gw-tier1a'
+  
+  Full diff: (-: missing in left side, +: extra in left side)
+    (
+  -     'claude-gw-tier1a',
+  -     'claude-gw-tier1b',
+  -     'claude-gw-tier2',
+  +     '',
+  +     '',
+  +     '',
+    )
+================= 1 failed, 1 passed, 131 deselected in 1.25s ==================

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
