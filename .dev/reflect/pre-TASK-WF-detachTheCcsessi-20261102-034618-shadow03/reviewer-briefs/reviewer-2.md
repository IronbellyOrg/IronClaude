# Reviewer 2 brief (persona: qa)

Mode UC-1 (pre-execution). You are read-only: return findings, run nothing, edit nothing.
Persona: qa. Audit the plan for defects that would make a task fail, an acceptance criterion unmeetable, or a step contradict a constraint. The package was already executed and archived (progress.md FINAL: pass); the fix is in HEAD. Judge the PLAN as a plan, using HEAD only to verify the plan's anchors and claims.

## T1 card excerpt

## Coverage map (Wave 1B)

Pass 1 (regex R-/REQ-/SPEC-/T-\d+): 0 IDs in spec, 0 in tasklist. parsed_count=0.
Pass 2 (inference, quote-pinned):
- INF-001 "Detach the ccsession gateway shim from the terminal that starts it" (source.md:1) -> Task 3 + Task 4 (containment: goal sentence words appear in Goal/task titles). match_method: containment.
- INF-002 "as specified in .dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/remediation-source.md" (source.md:1) -> Constraints + all tasks cite remediation-source.md ACs. match_method: containment.
Union: coverage_pct_union 1.0000 (2/2), coverage_pct null (parsed-only), coverage_degraded: parsed-sparse (2 inferred > 0 parsed; T1-stop pre-filter; tier pinned to 2 regardless). unmapped_requirements [], unmapped_requirements_union []. S_dev_density (union) 0.00.

Advisory manual map (not a contract field): remediation-source.md required changes 1-4 -> Tasks 3,4 (change 1), Task 3 (change 2), Tasks 1-2 (change 3a/3b), Task 5 (change 4); AC1 -> T1.AC2/T2.AC1; AC2 -> T4.AC1/T5.AC2; AC3 -> T4.AC3; AC4 -> T5.AC2; AC5 -> Constraints tasklist:20; AC6 -> Constraints tasklist:21. No uncovered item found.

End your card with a ## Findings block fenced findings-v2 block (lens: reflect-pre, citations with roles plan and spec) and a reviewer_model_self_report line stating the model you are running as in one line.
Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-12T23:22Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/done/TASK-WF-detachTheCcsessi-20261102-034618/source.md:1 (WHOLE SPEC)

```markdown
Detach the ccsession gateway shim from the terminal that starts it, as specified in .dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/remediation-source.md (diagnosis: REPORT.md in the same directory; issue #341). Code: src/superclaude/skills/ccsession-tag/ccsession (setup_shim start statement lines 797-804), src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py (__main__), tests/unit/test_ccsession_tiers.py, CHANGELOG.md.
```

### .dev/troubleshoot/deployment-ccsession-proxy-4114-stalls-20261102031709/remediation-source.md:9-27 (required changes + ACs)

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

### /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/done/TASK-WF-detachTheCcsessi-20261102-034618/TASK-WF-detachTheCcsessi-20261102-034618.md:25-46 (Phase 1 tasks)

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

## Phase 2: Start the shim in its own session
```

### /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/done/TASK-WF-detachTheCcsessi-20261102-034618/TASK-WF-detachTheCcsessi-20261102-034618.md:74-82 (Phase 4 task)

```markdown
## Task 5: Add the CHANGELOG entry

Depends on: Task 4

In `CHANGELOG.md` under `## [Unreleased]`, add a `### ccsession: shim survives its launching terminal (#341)` section with a `#### Fixed` bullet in plain words: the shared gateway shim was started inside the terminal that first launched it, so closing that terminal (Orca kills its descendants) cut every other session's reply and refused new ones until a later launch started a new shim; ccsession now starts it from a subshell and the shim starts its own session, so it keeps running until stopped (`pkill -f local-gateway-alias-proxy.py`).

Acceptance criteria:
- The new section sits directly under `## [Unreleased]`, references #341, and names no file outside the scope.
- Every test file that reads the edited files (found with `grep -rlE "local-gateway-alias-proxy|ccsession-tag" tests/` and listed in ./artifacts/t5-checks.log) passes, and `make lint` and `make verify-sync` pass, with commands and results in ./artifacts/t5-checks.log.
```

### /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/done/TASK-WF-detachTheCcsessi-20261102-034618/artifacts/t5-checks.log:1-40 (prior-run evidence)

```text
$ grep -rlE "local-gateway-alias-proxy|ccsession-tag" tests/
tests/cli/test_update_command.py
tests/cli/test_install_hooks.py
tests/unit/test_install_ccsession.py
tests/unit/test_ccsession_tag.py
tests/unit/test_cli_doctor.py
tests/unit/test_cli_install.py
tests/unit/test_ccsession_tiers.py
(CHANGELOG.md: tests/roadmap/test_spec_parser.py and tests/audit/test_full_docs_audit.py mention "CHANGELOG" only in fixture strings; neither reads the repo CHANGELOG.md)
$ PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/cli/test_update_command.py tests/cli/test_install_hooks.py tests/unit/test_install_ccsession.py tests/unit/test_ccsession_tag.py tests/unit/test_cli_doctor.py tests/unit/test_cli_install.py tests/unit/test_ccsession_tiers.py -q -p no:cacheprovider
======================= 457 passed in 172.61s (0:02:52) ========================
rc=0
$ pgrep -af "[p]ytest-of-.*/shim-under-test.py"
pgrep: none running
$ make lint
  Errors:   0
  Warnings: 5
  ✅ PASS — architecture policy compliant (5 warning(s))
Running linter...
uv run ruff check .
All checks passed!
rc=0
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

### tests/unit/test_ccsession_tiers.py:1933-1945 (landed T1 test head)

```python
def test_shim_outlives_the_terminal_that_started_it(tmp_path: Path) -> None:
    """Issue #341: closing the terminal that launched the shim must not stop it.

    Orca closes a terminal by sending SIGTERM, then SIGKILL, to every
    descendant of the terminal's shell. A shim started by ccsession in that
    terminal is shared by other sessions, so it must not be one of them.
    """
    shim_copy = tmp_path / "shim-under-test.py"
    shim_copy.write_text((SKILL_DIR / "local-gateway-alias-proxy.py").read_text())
    fake = tmp_path / "bin" / "claude"
    fake.parent.mkdir()
    fake.write_text(
        '#!/bin/sh\necho "$ANTHROPIC_BASE_URL" > "$SEEN_FILE"\nexec sleep 60\n'
```

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|---|---|---|---|
| INF-001 goal | - | covered | source.md:1 |
| INF-002 pointer | - | covered | source.md:1 |
| (advisory) remediation changes 1-4, AC1-AC6 | - | covered | t1-card.md advisory map |
