e244577584ce333bd02b13785fc624b7f21a9c80
Review one task for spec compliance.

Task brief: ## Task 2: Make the launcher export each alias variable only for a usable tier

Depends on: Task 1

Covers R-001, R-002, R-003, R-004 and R-005.

In `src/superclaude/skills/ccsession-tag/ccsession`, inside the `if [ "$TIER_MODE" = 1 ]; then` branch, replace the three unconditional `export ANTHROPIC_DEFAULT_*_MODEL=...` lines that follow `USE_SHIM=1` with this block, indented like `USE_SHIM=1`:

```bash
  # Map an alias to its tier only for a tier this owner may use: the list the
  # shim, --tier and --help use (models.py tiers). A tier not on the list, or a
  # list that cannot be read, leaves the inherited variable alone.
  _usable_tiers=$'\n'"$(python3 "$CCSESSION_MODELS" tiers 2>/dev/null | cut -d$'\x1f' -f1)"$'\n'
  case "$_usable_tiers" in *$'\n'tier1a$'\n'*) export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a ;; esac
  case "$_usable_tiers" in *$'\n'tier1b$'\n'*) export ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b ;; esac
  case "$_usable_tiers" in *$'\n'tier2$'\n'*) export ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2 ;; esac
```

Keep the block inside the tier-mode branch, add nothing to the `elif` branches, and confirm `bash -n` passes on the file (it runs under `set -e`; the pipeline status is that of `cut`, so an empty list does not stop the launcher).

Acceptance criteria:
- `uv run pytest tests/unit/test_ccsession_tiers.py -k "alias_variable or limited_owner or without_tier1a" -v` passes all five tests; save the output to `./artifacts/t2-green.log`.
- `uv run pytest tests/unit/test_ccsession_tag.py tests/unit/test_ccsession_tiers.py tests/skills/test_model_alias_policy.py` passes in full; save the output to `./artifacts/t2-full.log`.
- `git diff` of `src/superclaude/skills/ccsession-tag/` against the state before this task shows changes in `ccsession` only, and in `ccsession` only the replacement of the three export lines by the block above.

AC ids (in source order):
T2.AC1: `uv run pytest tests/unit/test_ccsession_tiers.py -k "alias_variable or limited_owner or without_tier1a" -v` passes all five tests; save the output to `./artifacts/t2-green.log`.
T2.AC2: `uv run pytest tests/unit/test_ccsession_tag.py tests/unit/test_ccsession_tiers.py tests/skills/test_model_alias_policy.py` passes in full; save the output to `./artifacts/t2-full.log`.
T2.AC3: `git diff` of `src/superclaude/skills/ccsession-tag/` against the state before this task shows changes in `ccsession` only, and in `ccsession` only the replacement of the three export lines by the block above.
Global constraints: ## Constraints

- Only `src/superclaude/skills/ccsession-tag/ccsession` changes under `src/superclaude/skills/ccsession-tag/`; `models.py`, `local-gateway-alias-proxy.py` and `ccsession-orca` stay untouched (R-002).
- The three unconditional export lines from the first follow-up already sit right after `USE_SHIM=1` in the tier-mode branch of `src/superclaude/skills/ccsession-tag/ccsession` (about lines 867-870); re-read the file before editing and change only those lines (R-001).
- Do not stage `.claude/`. Edit only under `src/`, `tests/`, `docs/` and `CHANGELOG.md`.
- Docs say only what the code and the probe records show; no probe exercised the Agent-call `model` parameter.
- R-008 (the pull request body) changes no file and has no task; it is written when the pull request is opened. R-004 has no launcher-level test because a broken access entry makes the launcher exit before Claude starts (`apply_tier_selection`, `|| exit 2`).
Start sha: e244577584ce333bd02b13785fc624b7f21a9c80
Diff against the start snapshot: diff --git a/src/superclaude/skills/ccsession-tag/ccsession b/src/superclaude/skills/ccsession-tag/ccsession
index 677ab73e..2f443f04 100755
--- a/src/superclaude/skills/ccsession-tag/ccsession
+++ b/src/superclaude/skills/ccsession-tag/ccsession
@@ -865,9 +865,13 @@ if [ "$TIER_MODE" = 1 ]; then
     exit 2
   fi
   USE_SHIM=1
-  export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a
-  export ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b
-  export ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2
+  # Map an alias to its tier only for a tier this owner may use: the list the
+  # shim, --tier and --help use (models.py tiers). A tier not on the list, or a
+  # list that cannot be read, leaves the inherited variable alone.
+  _usable_tiers=$'\n'"$(python3 "$CCSESSION_MODELS" tiers 2>/dev/null | cut -d$'\x1f' -f1)"$'\n'
+  case "$_usable_tiers" in *$'\n'tier1a$'\n'*) export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a ;; esac
+  case "$_usable_tiers" in *$'\n'tier1b$'\n'*) export ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b ;; esac
+  case "$_usable_tiers" in *$'\n'tier2$'\n'*) export ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2 ;; esac
 elif [ -n "$TIER_ARG" ]; then
   echo "ccsession: --tier needs tier settings (T<N>_WINDOW) from the workspace env; none found" >&2
   exit 2

diff --git a/.dev/tasks/to-do/TASK-WF-launcherAccessAw-20261105-144815/artifacts/t2-green.log b/.dev/tasks/to-do/TASK-WF-launcherAccessAw-20261105-144815/artifacts/t2-green.log
new file mode 100644
index 00000000..285ffbd5
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-launcherAccessAw-20261105-144815/artifacts/t2-green.log
@@ -0,0 +1,16 @@
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
+tests/unit/test_ccsession_tiers.py::test_limited_owner_gets_only_the_haiku_alias_variable PASSED [ 60%]
+tests/unit/test_ccsession_tiers.py::test_limited_owner_keeps_inherited_alias_values PASSED [ 80%]
+tests/unit/test_ccsession_tiers.py::test_workspace_without_tier1a_and_tier1b_exports_only_its_tiers PASSED [100%]
+
+====================== 5 passed, 131 deselected in 3.54s =======================

diff --git a/.dev/tasks/to-do/TASK-WF-launcherAccessAw-20261105-144815/artifacts/t2-full.log b/.dev/tasks/to-do/TASK-WF-launcherAccessAw-20261105-144815/artifacts/t2-full.log
new file mode 100644
index 00000000..9e435c9f
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-launcherAccessAw-20261105-144815/artifacts/t2-full.log
@@ -0,0 +1,20 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 5.0.0
+benchmark: 5.3.1 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
+rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-384-launcher-tier-aliases
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, benchmark-5.3.1, anyio-4.16.0, cov-7.1.0
+collected 407 items
+
+tests/unit/test_ccsession_tag.py ....................................... [  9%]
+........................................................................ [ 27%]
+........................................................................ [ 44%]
+........................................................................ [ 62%]
+...                                                                      [ 63%]
+tests/unit/test_ccsession_tiers.py ..................................... [ 72%]
+........................................................................ [ 90%]
+...........................                                              [ 96%]
+tests/skills/test_model_alias_policy.py .............                    [100%]
+
+======================= 407 passed in 253.66s (0:04:13) ========================

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
