5117a49085fa46a8a4c24dc6fd24ddfee692c2c6
Review one task for spec compliance.

Task brief: ## Task 2: Export the three variables in the tier-mode branch of the ccsession launcher

Depends on: Task 1

In `src/superclaude/skills/ccsession-tag/ccsession`, inside the `if [ "$TIER_MODE" = 1 ]; then` branch (anchor: the block that sets `TIER_MODE=0`, runs `python3 "$CCSESSION_MODELS" tier-mode` and then, in tier mode, rejects `--profile` and sets `USE_SHIM=1`), add these three lines right after `USE_SHIM=1`, with the same indentation as that line:

```bash
  export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a
  export ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b
  export ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2
```

Do not add them to any `elif` or `else` branch. Confirm by reading the launcher that nothing after the block unsets or overwrites the three variables (a grep for `ANTHROPIC_DEFAULT_` in the `ccsession-tag` folder found none before the edit).

Acceptance criteria:
- `uv run pytest tests/unit/test_ccsession_tiers.py -k alias_variables -v` passes both tests; save the output to `./artifacts/t2-green.log`.
- `uv run pytest tests/unit/test_ccsession_tag.py tests/unit/test_ccsession_tiers.py tests/skills/test_model_alias_policy.py` passes in full.
- `git diff` of `src/superclaude/skills/ccsession-tag/` shows exactly the three added lines in `ccsession` and no other file.

AC ids (in source order):
T2.AC1: `uv run pytest tests/unit/test_ccsession_tiers.py -k alias_variables -v` passes both tests; save the output to `./artifacts/t2-green.log`.
T2.AC2: `uv run pytest tests/unit/test_ccsession_tag.py tests/unit/test_ccsession_tiers.py tests/skills/test_model_alias_policy.py` passes in full.
T2.AC3: `git diff` of `src/superclaude/skills/ccsession-tag/` shows exactly the three added lines in `ccsession` and no other file.
Global constraints: ## Constraints

- Only `src/superclaude/skills/ccsession-tag/ccsession` changes under `src/superclaude/skills/ccsession-tag/`; `ccsession-orca` stays untouched.
- Re-verify every line number in the source against the code on the working branch before editing: the source numbers are at base commit 38eb3c58 and the #315 change edits the same files.
- Do not stage `.claude/`. Edit only under `src/`, `tests/`, `docs/` and `CHANGELOG.md`.
- Docs say only what the code and the two probe records show: the probe record is `.dev/issues/384/analysis/probe-alias-remap.md` (opus and haiku) and `.dev/issues/384/analysis/probe-sonnet-alias.md` (sonnet).
Start sha: 5117a49085fa46a8a4c24dc6fd24ddfee692c2c6
Diff against the start snapshot: diff --git a/src/superclaude/skills/ccsession-tag/ccsession b/src/superclaude/skills/ccsession-tag/ccsession
index f85b1b2a..677ab73e 100755
--- a/src/superclaude/skills/ccsession-tag/ccsession
+++ b/src/superclaude/skills/ccsession-tag/ccsession
@@ -865,6 +865,9 @@ if [ "$TIER_MODE" = 1 ]; then
     exit 2
   fi
   USE_SHIM=1
+  export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a
+  export ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b
+  export ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2
 elif [ -n "$TIER_ARG" ]; then
   echo "ccsession: --tier needs tier settings (T<N>_WINDOW) from the workspace env; none found" >&2
   exit 2

diff --git a/.dev/tasks/to-do/TASK-WF-launcherFollowup-20261105-131531/artifacts/t2-green.log b/.dev/tasks/to-do/TASK-WF-launcherFollowup-20261105-131531/artifacts/t2-green.log
new file mode 100644
index 00000000..9fc11ac9
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-launcherFollowup-20261105-131531/artifacts/t2-green.log
@@ -0,0 +1,13 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0 -- /home/coder/workspaces/worktrees/IronClaude/issue-384-launcher-tier-aliases/.venv/bin/python
+SuperClaude: 5.0.0
+benchmark: 5.3.1 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
+rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-384-launcher-tier-aliases
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, benchmark-5.3.1, anyio-4.16.0, cov-7.1.0
+collecting ... collected 133 items / 131 deselected / 2 selected
+
+tests/unit/test_ccsession_tiers.py::test_tier_launch_exports_the_alias_variables PASSED [ 50%]
+tests/unit/test_ccsession_tiers.py::test_non_tier_launch_leaves_the_alias_variables_unset PASSED [100%]
+
+====================== 2 passed, 131 deselected in 1.06s =======================

diff --git a/.dev/tasks/to-do/TASK-WF-launcherFollowup-20261105-131531/artifacts/t2-full.log b/.dev/tasks/to-do/TASK-WF-launcherFollowup-20261105-131531/artifacts/t2-full.log
new file mode 100644
index 00000000..7f773515
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-launcherFollowup-20261105-131531/artifacts/t2-full.log
@@ -0,0 +1,20 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 5.0.0
+benchmark: 5.3.1 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
+rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-384-launcher-tier-aliases
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, benchmark-5.3.1, anyio-4.16.0, cov-7.1.0
+collected 404 items
+
+tests/unit/test_ccsession_tag.py ....................................... [  9%]
+........................................................................ [ 27%]
+........................................................................ [ 45%]
+........................................................................ [ 63%]
+...                                                                      [ 63%]
+tests/unit/test_ccsession_tiers.py ..................................... [ 73%]
+........................................................................ [ 90%]
+........................                                                 [ 96%]
+tests/skills/test_model_alias_policy.py .............                    [100%]
+
+======================= 404 passed in 250.25s (0:04:10) ========================

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
