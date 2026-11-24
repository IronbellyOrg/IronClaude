e2faccf0530162bd7f15fc361e457afc64b094eb
Review one task for spec compliance.

Task brief: ## Task 2: Retry first_run for a failed, disabled config in run_sweep

Depends on: Task 1

In `src/superclaude/cli/issue_watch/dispatch.py`, add a module constant `RETRY_AFTER_S = 3600.0`, import `failed_step` from `.first_run` (next to the existing `first_run` import at line 45) and add `timedelta` to the `from datetime import ...` line (line 40). In `run_sweep`, immediately before `enabled = _enabled(config_path)` (line 428, after the generate branch that ends at line 427), add: when `not dry_run`, `_enabled(config_path) is False`, and `failed_step(config_path)` returns `(step, written_at)`, call `first_run(config_path, defaults, runner, deps_factory)` once when `step == "config"`, or when `since - written_at >= timedelta(seconds=RETRY_AFTER_S)` for any other step (`since` is the sweep start already computed at the top of `run_sweep`). Then fall through to the existing `_enabled` read, so a successful retry continues to the precheck and the child, and a failed retry is reported as `not_enabled`. A repo whose config was just generated in this same sweep is not retried a second time. Source requirements 1, 2, 3 and 5.

Acceptance criteria:
- T2.AC1: A config that is `enabled: false` with a report `first-run: failed config: worktree_invalid` and a now-valid worktree is enabled by the next non-dry sweep and its child starts in that sweep.
- T2.AC2: A failed retry leaves the config disabled, is skipped as `not_enabled`, and calls `first_run` exactly once in that sweep.
- T2.AC3: A failure at a step other than `config` is retried only when the report is at least 3600 seconds older than the sweep start.
- T2.AC4: A disabled config with no report or a `first-run: passed` report, and any config in a dry-run sweep, produces no `first_run` call and no file write.
- T2.AC5: `grep -n "ensure_trigger_label\|init_state\|gh " src/superclaude/cli/issue_watch/dispatch.py` shows no new GitHub or store call in `dispatch.py`.
Global constraints: ## Constraints

- Reuse the existing `first_run` function as the only setup path; do not add GitHub writes, label creation or store creation to `dispatch.py` or `cycle.py` (the boundary pinned by `tests/issue_watch/test_security_invariants.py` stays intact).
- Do not change the config schema (`_TOP_KEYS` in `src/superclaude/cli/issue_watch/cycle.py`) and do not change `ensure_config` in `src/superclaude/cli/issue_watch/generate.py`.
- A config with no first-run report, or whose report starts with `first-run: passed`, is never retried.
- A dry-run sweep makes no `first_run` call and writes no file.
- Do not edit anything under `.claude/`; change `src/` and `tests/` only.
Start sha: e2faccf0530162bd7f15fc361e457afc64b094eb
Diff against the start snapshot: 
```diff
diff --git a/src/superclaude/cli/issue_watch/dispatch.py b/src/superclaude/cli/issue_watch/dispatch.py
index 33465706f..22bd264db 100644
--- a/src/superclaude/cli/issue_watch/dispatch.py
+++ b/src/superclaude/cli/issue_watch/dispatch.py
@@ -37,12 +37,12 @@ import time
 from collections.abc import Callable, Iterator
 from contextlib import contextmanager
 from dataclasses import dataclass, field, replace
-from datetime import datetime, timezone
+from datetime import datetime, timedelta, timezone
 from pathlib import Path
 
 from . import cycle, record, repo_init
 from .defaults import Defaults
-from .first_run import first_run
+from .first_run import failed_step, first_run
 from .generate import Base, _projects, ensure_config
 from .launch import check_origin
 from .predicates import format_utc, parse_utc
@@ -52,6 +52,7 @@ from .runner import Runner
 LOOP_CAP_S = 270.0
 CHILD_TIMEOUT_S = 255.0
 GIT_TIMEOUT_S = 15.0
+RETRY_AFTER_S = 3600.0  # a failed first run past the config step is retried after this long
 ROTATION_FILE = "rotation.json"
 RATE_WAIT_FILE = "account-rate-wait.json"
 LOCK_FILE = "run-all.lock"
@@ -425,6 +426,20 @@ def run_sweep(
             if outcome.status == "generated":
                 generated.append(repo.name)
                 first_run(config_path, defaults, runner, deps_factory)
+        if (
+            not dry_run
+            and repo.name not in generated
+            and _enabled(config_path) is False
+        ):
+            # A config left disabled by a failed first run is retried: a config-step failure (the
+            # worktree was not there yet) every sweep, a later step (GitHub calls, dry-run cycles)
+            # only once RETRY_AFTER_S has passed. No failed report means the owner disabled it.
+            failed = failed_step(config_path)
+            if failed is not None and (
+                failed[0] == "config"
+                or since - failed[1] >= timedelta(seconds=RETRY_AFTER_S)
+            ):
+                first_run(config_path, defaults, runner, deps_factory)
         enabled = _enabled(config_path)
         if enabled is not True:
             skipped.append(
```

Codegraph context
index_state: fresh
checked_at: 2026-11-24T02:39:04Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-751
projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-751
call codegraph only when index_state: fresh, never to widen scope
Dependents not in the diff (Q2b): run_sweep callers: run_all_command (cli.py:508,511), tests/issue_watch/test_dispatch.py sweep() (:152); signature and SweepResult unchanged; new call sites of first_run and failed_step are inside run_sweep only; no GitHub or store call added to dispatch.py (grep ensure_trigger_label|init_state in dispatch.py: none). Task 1 (failed_step) is already complete and not part of this diff.

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
