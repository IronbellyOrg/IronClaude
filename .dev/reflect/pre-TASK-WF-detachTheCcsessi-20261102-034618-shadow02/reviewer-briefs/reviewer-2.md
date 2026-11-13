# Reviewer brief 2 (persona: qa)

## T1 card excerpt

# Tier 1 reflection card (UC-1, pre-execution)

Mode: pre. Spec: `.dev/tasks/done/TASK-WF-detachTheCcsessi-20261102-034618/source.md` (1 line). Tasklist: `.dev/tasks/done/TASK-WF-detachTheCcsessi-20261102-034618/TASK-WF-detachTheCcsessi-20261102-034618.md` (82 lines, 5 tasks in 4 phases).
Context caveat: this checkout already contains the change (the plan sits in `done/`), so line anchors in the plan cannot be re-checked against the pre-change tree; symbol names can.

## Requirement extraction (Step 1B.0)

- Pass 1 (regex `R-|REQ-|SPEC-|T-` ids): 0 ids. The spec is one sentence with no labeled requirement.
- Pass 2 (inference): 2 rows, both quote-pinned to source.md:1.
- `inferred_count (2) > parsed_count (0)` so the parse-density guard fires: `coverage_degraded: parsed-sparse`.

| Row | Source | Verbatim quote | Citation | Containment match (stopword set below) |
|---|---|---|---|---|
| INF-001 | inferred | Detach the ccsession gateway shim from the terminal that starts it | source.md:1 | Task 5 0.8333 (Task 1/3/4 tie at 0.6667); matched |
| INF-002 | inferred | Code: src/superclaude/skills/ccsession-tag/ccsession (setup_shim start statement lines 797-804), src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py (__main__), tests/unit/test_ccsession_tiers.py, CHANGELOG.md. | source.md:1 | Task 3 0.6957 (Task 4 0.6522); matched |

Containment uses a case-folded stopword set (articles, conjunctions, prepositions, auxiliaries: a an the and or but of to in on at by for with from as is are was were be been being it its this that these those which who whom into onto than then so no not nor if else when while after before until each every any all both either neither can could may might must shall should will would do does did has have had). The ref does not list the stopwords, so a different list changes which task wins (a prior run of the same inputs mapped INF-001 to Task 4). The matched/unmatched outcome is the same either way.

Numbers: `coverage_pct` null (parsed total 0), `coverage_pct_union` 1.0 (2/2), `unmapped_requirements_union` [], `S_dev_density` 0.0, `S_scope` 5 tasks, `S_domains` 3 (code, tests, docs/config: `src/`, `tests/`, `CHANGELOG.md`).

Secondary view (not scored): the spec delegates its acceptance criteria to `remediation-source.md`. Mapping its items to tasks: required change 1 to Task 4, 2 to Task 3, 3a to Task 1, 3b to Task 2, 4 to Task 5; AC1 to Tasks 1-2 and 4; AC2 to Task 5; AC3 to Task 4; AC4 to Task 5; AC5 and AC6 to the Constraints block plus Task 4's pid check; the Pipeline Hardening line "HC5" maps to no task (finding F4).

### F1 MAJOR (blocking), unpassable-check: Task 5 requires `make verify-sync` to pass but no task runs `make sync-dev`

- Task 5 acceptance: "`make lint` and `make verify-sync` pass" (tasklist:82).
- `verify-sync` diffs every `src/superclaude/skills/<name>/` against `.claude/skills/<name>/` and exits 1 on any difference or missing directory (Makefile:166-185). Tasks 3 and 4 edit two files under `src/superclaude/skills/ccsession-tag/` (tasklist:52, 64), so the `.claude/` copy is stale after them, and a fresh worktree has no `.claude/skills/` at all.
- The plan's scope is "exactly the four files named in the source" (tasklist:19) and lists no `make sync-dev` step, so the acceptance check cannot pass as written. The run log of the executed plan shows it: `make verify-sync` failed with "Drift detected" (t5-checks.log:28-30) until an unplanned `make sync-dev` (t5-checks.log:31-34).
- Fix: add `make sync-dev` before `make verify-sync` in Task 5 and say the gitignored `.claude/` mirror is outside the four-file scope.

### F3 MINOR, unpassable-check: Task 1's leak check cannot see the leaked process it names

- The acceptance bullet says no "shim or sleep process" survives, "checked with `pgrep -f <tmp copy path>` returning nothing" (tasklist:34). The fake `claude` ends in `exec sleep 60` (tasklist:29), whose command line is `sleep 60` and does not contain the per-test shim path, so the pgrep can only prove the shim is gone, not the sleep.
- Fix: also name a check for the sleep (assert the terminal root and its descendants are gone, as the test already collects them).

### F4 MINOR, missing-requirement: the delegated spec's off-path review requirement has no task

- `remediation-source.md` Pipeline Hardening: "HC5: off-path review required (PR reviewers and /sc:reflect --mode post)." (remediation-source.md:35). No task or acceptance criterion schedules or records it.
- This is a post-implementation process step, so the plan can name it as a closing note instead of a task. Advisory.

End your card with a ## Findings block fenced findings-v2 block (lens: reflect-pre, citations with roles plan and spec) and a reviewer_model_self_report line stating the model you are running as in one line.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-12T22:18:27Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/tasks/done/TASK-WF-detachTheCcsessi-20261102-034618/source.md:1-1

```markdown
Detach the ccsession gateway shim from the terminal that starts it, as specified in .dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/remediation-source.md (diagnosis: REPORT.md in the same directory; issue #341). Code: src/superclaude/skills/ccsession-tag/ccsession (setup_shim start statement lines 797-804), src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py (__main__), tests/unit/test_ccsession_tiers.py, CHANGELOG.md.
```

### .dev/tasks/done/TASK-WF-detachTheCcsessi-20261102-034618/TASK-WF-detachTheCcsessi-20261102-034618.md:17-23

```markdown
## Constraints

- Scope is exactly the four files named in the source: `src/superclaude/skills/ccsession-tag/ccsession`, `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py`, `tests/unit/test_ccsession_tiers.py`, `CHANGELOG.md`. Diagnosis and requirements: `.dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/remediation-source.md` and `REPORT.md` in the same directory (issue #341).
- Never signal, restart or reconfigure the running shims on ports 4013 and 4114 (or whatever serves them); never edit anything under `~/.claude`, `~/.ccsession` or the running config; never run `superclaude install`, `superclaude update`, `./update.sh` or `install.sh`.
- Doc restrictions (remediation-source.md AC6; doc-context.md in the troubleshoot directory): the shim's argv keeps the script path (ccsession uses `pgrep -f -- "$CC_SHIM_SCRIPT"` at ccsession:722 and users stop shims with `pkill -f local-gateway-alias-proxy.py`); the shim inherits the launching env; no `setsid` binary (macOS has none) and only Python standard library; bash 3.2 syntax; logging stays opt-in; ccsession never stops a running shim.
- Tests: run only named test files and tests that read the edited files; never the full suite and never `tests/cli/eval/` as a directory. Use `uv run` for Python.
- Every throwaway shim or test process started while working is stopped by its exact pid; no temp files left behind.
```

### .dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/remediation-source.md:9-26

```markdown
## Required change (scope: exactly these, nothing else)

1. `src/superclaude/skills/ccsession-tag/ccsession` — wrap the shim start statement (lines 801-804) in a `( ... )` subshell so the subshell exits at once and the shim is reparented away from the launching terminal. Update the comment above it to say why. Keep bash 3.2 syntax, keep the env assignments (GW_PROXY_UPSTREAM, GW_PROXY_PORT, CCSESSION_DIR) and the `>/dev/null 2>&1` redirect.
2. `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py` — in `__main__`, before binding, call `os.setsid()` so the shim leaves the launcher's session and process group; ignore `OSError` (raised when the process already leads a process group, e.g. run by hand in an interactive shell). Add a short comment. No new imports beyond `os` (already imported), no fork, argv unchanged.
3. Regression tests in `tests/unit/test_ccsession_tiers.py` (reuse StandInGateway, `_free_port`, `_defaults`, TIER_BLOCK, `_ask_raw`, SKILL_DIR):
   a. `test_shim_outlives_the_terminal_that_started_it`: run the real `ccsession` (fake `claude` that records ANTHROPIC_BASE_URL then `exec sleep 60`) in its own session (`start_new_session=True`, an Orca-terminal stand-in) with `CC_SHIM_SCRIPT` = a per-test copy of the shim; wait for the seen file; read the shim pid from `/__ccsession_shim`; assert the shim pid is not among the terminal root's descendants (walk `ps -axo pid=,ppid=`); start a streamed tier2 request with `gateway.script["muse-spark-1.3"] = [("pause-stream", 4)]`; 1 s later SIGTERM every descendant of the root plus the root, then SIGKILL survivors; assert the reply status is 200 and ends with `message_stop`, and the health endpoint still reports the same pid. Clean up: kill the shim by pid and `pkill -f <copy path>`; close the gateway; kill the root group if still alive.
   b. `test_a_directly_started_shim_leaves_the_launchers_session`: start the shim with the existing `shim` fixture (Popen from the test process) and assert `os.getsid(<shim pid>) != os.getsid(0)` and `os.getpgid(<shim pid>) != os.getpgid(0)`; the fixture's `terminate()` must still stop it.
   Both must fail on the current code and pass after the change.
4. `CHANGELOG.md` — one Unreleased entry (Fixed) describing the fix in plain words, referencing #341.

## Acceptance criteria

- AC1: the new tests fail before the change (verified by running them against the unmodified source) and pass after.
- AC2: `uv run pytest tests/unit/test_ccsession_tiers.py tests/unit/test_ccsession_tag.py -q` passes, plus any other test file that reads the edited files (find them with `grep -rln "local-gateway-alias-proxy\|ccsession-tag/ccsession\|SKILL_DIR / \"ccsession\"" tests/`). Never run the full suite or tests/cli/eval/ as a directory.
- AC3: live check: `python3 -I .dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/live-check/orca_close_repro.py <worktree> <private scratch dir>` against the changed source prints `shim is a descendant of the terminal: False`, `stream finished: True`, and the port still answers; output saved as live-check/after.txt; the surviving throwaway shim is stopped by its exact pid.
- AC4: `make lint` and `make verify-sync` pass.
- AC5: nothing under `~/.claude`, `~/.ccsession` or the running config is edited; the live shims (ports 4013 and 4114) are never signalled; `superclaude install/update` is not run.
- AC6: the doc restrictions hold: script path stays in the shim's argv (ccsession:722 `pgrep -f`), env is inherited, no `setsid` binary is required, logging stays opt-in, no running shim is ever stopped by ccsession.
```

### .dev/tasks/done/TASK-WF-detachTheCcsessi-20261102-034618/TASK-WF-detachTheCcsessi-20261102-034618.md:25-44

```markdown
## Phase 1: Regression tests that capture the failure

## Task 1: Add a test that a launched shim survives the terminal that started it

In `tests/unit/test_ccsession_tiers.py`, add `test_shim_outlives_the_terminal_that_started_it` next to `test_a_busy_shim_is_never_stopped_by_a_new_launch` (around line 1379), reusing `StandInGateway` (line 488), `_free_port` (568), `_defaults`/`TIER_BLOCK`, `_ask_raw` (1051) and `SKILL_DIR`. Mirror `_real_launch` (1344) but start the real `SKILL_DIR / "ccsession"` with `subprocess.Popen(..., start_new_session=True)` (a stand-in for an Orca terminal) and a fake `claude` that writes `$ANTHROPIC_BASE_URL` to a seen file and then `exec sleep 60`; `CC_SHIM_SCRIPT` is a per-test copy of `local-gateway-alias-proxy.py` in `tmp_path`, `CC_SHIM_PORT` a free port. After the seen file appears: read the shim pid from `/__ccsession_shim`; compute the terminal root's descendants by walking `ps -axo pid=,ppid=`; set `gateway.script["muse-spark-1.3"] = [("pause-stream", 4)]` and start `_ask_raw(url, "claude-gw-tier2", stream=True)` in a thread; after 1 s send SIGTERM to every descendant of the root and the root, wait 0.5 s, SIGKILL survivors (this is what Orca does when it closes a terminal: remediation-source.md Summary, troubleshoot `tier1-observation.md` O8). Clean up in `finally`: kill the shim by its pid, `pkill -f` the per-test copy path, close the gateway, and kill any remaining root process.

Acceptance criteria:
- The test asserts the shim pid is not among the terminal root's descendants, the streamed reply returns status 200 and contains `b"message_stop"`, and `/__ccsession_shim` still answers with the same pid after the terminal is gone.
- Run against the unmodified source, the test fails (record the command and its failing output in ./artifacts/t1-before.log).
- No shim or sleep process from the test is left running after it finishes (checked with `pgrep -f <tmp copy path>` returning nothing).

## Task 2: Add a test that a directly started shim leaves the starter's session

Depends on: Task 1

In `tests/unit/test_ccsession_tiers.py`, add `test_a_directly_started_shim_leaves_the_launchers_session` using the existing `shim` fixture (line 574-614, which starts the shim with `subprocess.Popen` from the test process). Read the shim pid from `/__ccsession_shim` and assert `os.getsid(pid) != os.getsid(0)` and `os.getpgid(pid) != os.getpgid(0)`. The fixture's `proc.terminate()` must still stop the shim at teardown (the shim stays the Popen child).

Acceptance criteria:
- The test fails against the unmodified source (output appended to ./artifacts/t1-before.log) and needs no new fixture.
- After the fixture's teardown the shim process is gone (assert in the test or verify with `pgrep -f` that no shim from this test survives).
```

### .dev/tasks/done/TASK-WF-detachTheCcsessi-20261102-034618/TASK-WF-detachTheCcsessi-20261102-034618.md:72-82

```markdown
## Phase 4: Record and prove the change

## Task 5: Add the CHANGELOG entry

Depends on: Task 4

In `CHANGELOG.md` under `## [Unreleased]`, add a `### ccsession: shim survives its launching terminal (#341)` section with a `#### Fixed` bullet in plain words: the shared gateway shim was started inside the terminal that first launched it, so closing that terminal (Orca kills its descendants) cut every other session's reply and refused new ones until a later launch started a new shim; ccsession now starts it from a subshell and the shim starts its own session, so it keeps running until stopped (`pkill -f local-gateway-alias-proxy.py`).

Acceptance criteria:
- The new section sits directly under `## [Unreleased]`, references #341, and names no file outside the scope.
- Every test file that reads the edited files (found with `grep -rlE "local-gateway-alias-proxy|ccsession-tag" tests/` and listed in ./artifacts/t5-checks.log) passes, and `make lint` and `make verify-sync` pass, with commands and results in ./artifacts/t5-checks.log.
```

### Makefile:164-185

```makefile

# Verify src/superclaude/ and .claude/ are in sync (CI-friendly, exits 1 on drift)
verify-sync:
	@echo "🔍 Verifying src/superclaude/ ↔ .claude/ sync..."
	@drift=0; \
	echo ""; \
	echo "=== Skills ==="; \
	for skill_dir in src/superclaude/skills/*/; do \
		name=$$(basename "$$skill_dir"); \
		case "$$name" in __*) continue;; esac; \
		if [ ! -d ".claude/skills/$$name" ]; then \
			echo "  ❌ MISSING in .claude/skills/: $$name"; \
			drift=1; \
		else \
			changes=$$(diff -rq --exclude='__init__.py' --exclude='__pycache__' "$$skill_dir" ".claude/skills/$$name" 2>/dev/null); \
			if [ -n "$$changes" ]; then \
				echo "  ⚠️  DIFFERS: $$name"; \
				echo "$$changes" | sed 's/^/      /'; \
				drift=1; \
			else \
				echo "  ✅ $$name"; \
			fi; \
```

### .dev/tasks/done/TASK-WF-detachTheCcsessi-20261102-034618/artifacts/t5-checks.log:23-40

```text
$ make verify-sync

=== Hooks Cross-Consistency ===
  ✅ hooks.json matcher and auggie-flag-clear.sh case body agree on auggie prefixes

❌ Drift detected! Run 'make sync-dev' to fix, or copy .claude/ changes to src/.
make: *** [Makefile:168: verify-sync] Error 1
rc=2
$ make sync-dev   # this fresh worktree had no gitignored .claude/ dev copies; sync-dev fills the worktree .claude/ only
   Hooks:     12 files
   Templates: 52 files
rc=0
$ make verify-sync
=== Hooks Cross-Consistency ===
  ✅ hooks.json matcher and auggie-flag-clear.sh case body agree on auggie prefixes

✅ All components in sync.
rc=0
```

## Coverage slice

| Requirement | Card ID | Status | Grounding |
|---|---|---|---|
| INF-001: Detach the ccsession gateway shim from the terminal that starts it | C-001 | matched: Task 5 (0.8333; Tasks 1/3/4 at 0.6667) | source.md:1 |
| INF-002: Code: .../ccsession (setup_shim start statement lines 797-804), .../local-gateway-alias-proxy.py (__main__), tests/unit/test_ccsession_tiers.py, CHANGELOG.md. | C-002 | matched: Task 3 (0.6957; Task 4 0.6522) | source.md:1 |
