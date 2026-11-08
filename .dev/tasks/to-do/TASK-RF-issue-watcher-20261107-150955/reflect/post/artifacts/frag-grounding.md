### Gap G-01 (C-020)

- **Hunk ref:** tracked in merged-verdict.yaml (C-020)
- **Evidence missing:** The dead-code list (MAX_LAUNCHES_PER_CYCLE, record.disabled_present, the status_report audit argument, CommandResult.duration_s) was not re-read by the judge.
- **Why not classifiable:** judge could not re-read the evidence this run: dead code
- **Next evidence needed:** A reference search for each of the four names across src/ and tests/ to show whether any reader exists.

### Gap G-02 (C-021)

- **Hunk ref:** tracked in merged-verdict.yaml (C-021)
- **Evidence missing:** The mark_pending state-versus-launches check was not re-read line by line by the judge.
- **Why not classifiable:** judge could not re-read the evidence this run: mark_pending state check
- **Next evidence needed:** A trace showing whether any reachable document can hold state None or failed with launches 1, which would make the missing launches == 0 check matter.

### Gap G-03 (C-027)

- **Hunk ref:** tracked in merged-verdict.yaml (C-027)
- **Evidence missing:** Variant-1 did not confirm the approvers-file fstat gap; the judge did not either.
- **Why not classifiable:** judge could not re-read the evidence this run: approvers-file fstat
- **Next evidence needed:** A spec or design line that requires an fstat after the open or a parent directory mode check; without one this is advisory at most.

### Gap G-04 (C-028)

- **Hunk ref:** tracked in merged-verdict.yaml (C-028)
- **Evidence missing:** The re-approved branch at cycle.py:641 was located but its reachability was not traced.
- **Why not classifiable:** judge could not re-read the evidence this run: re-approved branch near cycle.py:641
- **Next evidence needed:** A trace of the callers of this decision path showing whether an entry with a different approval_event_id can reach it.

### Gap G-05 (C-029)

- **Hunk ref:** tracked in merged-verdict.yaml (C-029)
- **Evidence missing:** The seven DF anchors (dry-run skips, Retry-After on the user call, full retry argv, halt on any launch outcome, cwd=worktree) were not all re-read.
- **Why not classifiable:** judge could not re-read the evidence this run: seven anchored departures
- **Next evidence needed:** A re-read of each of the seven DF rows in the DF register against the code site it names.

### Gap G-06 (C-039)

- **Hunk ref:** tracked in merged-verdict.yaml (C-039)
- **Evidence missing:** The wiring and subprocess-coverage claim (only init-state and once have real-subprocess tests) was not verified by the judge.
- **Why not classifiable:** judge could not re-read the evidence this run: wiring and subprocess coverage
- **Next evidence needed:** A search of tests/issue_watch for subprocess invocations of each verb.

### Gap G-07 (RS-issue_watch_group)

- **Hunk ref:** src/superclaude/cli/issue_watch/cli.py:94
- **Evidence missing:** static reachability of Click symbol issue_watch_group cannot be decided: the degrade oracle matches (a) command decorator, and for the group also (b) [project.scripts] and (c) main.add_command registry
- **Why not classifiable:** runtime-surface DEGRADE (refs/runtime-surface.md section 3): never UNREACHED, never Regression
- **Next evidence needed:** real-process run of the verb (tests/issue_watch/test_cli_e2e.py runs only once and init-state through python -m); the registration facts are src/superclaude/cli/main.py:565 and pyproject.toml:71

### Gap G-08 (RS-once_command)

- **Hunk ref:** src/superclaude/cli/issue_watch/cli.py:111
- **Evidence missing:** static reachability of Click symbol once_command cannot be decided: the degrade oracle matches (a) command decorator, and for the group also (b) [project.scripts] and (c) main.add_command registry
- **Why not classifiable:** runtime-surface DEGRADE (refs/runtime-surface.md section 3): never UNREACHED, never Regression
- **Next evidence needed:** real-process run of the verb (tests/issue_watch/test_cli_e2e.py runs only once and init-state through python -m); the registration facts are src/superclaude/cli/main.py:565 and pyproject.toml:71

### Gap G-09 (RS-status_command)

- **Hunk ref:** src/superclaude/cli/issue_watch/cli.py:164
- **Evidence missing:** static reachability of Click symbol status_command cannot be decided: the degrade oracle matches (a) command decorator, and for the group also (b) [project.scripts] and (c) main.add_command registry
- **Why not classifiable:** runtime-surface DEGRADE (refs/runtime-surface.md section 3): never UNREACHED, never Regression
- **Next evidence needed:** real-process run of the verb (tests/issue_watch/test_cli_e2e.py runs only once and init-state through python -m); the registration facts are src/superclaude/cli/main.py:565 and pyproject.toml:71

### Gap G-10 (RS-check_config_command)

- **Hunk ref:** src/superclaude/cli/issue_watch/cli.py:185
- **Evidence missing:** static reachability of Click symbol check_config_command cannot be decided: the degrade oracle matches (a) command decorator, and for the group also (b) [project.scripts] and (c) main.add_command registry
- **Why not classifiable:** runtime-surface DEGRADE (refs/runtime-surface.md section 3): never UNREACHED, never Regression
- **Next evidence needed:** real-process run of the verb (tests/issue_watch/test_cli_e2e.py runs only once and init-state through python -m); the registration facts are src/superclaude/cli/main.py:565 and pyproject.toml:71

### Gap G-11 (RS-init_state_command)

- **Hunk ref:** src/superclaude/cli/issue_watch/cli.py:201
- **Evidence missing:** static reachability of Click symbol init_state_command cannot be decided: the degrade oracle matches (a) command decorator, and for the group also (b) [project.scripts] and (c) main.add_command registry
- **Why not classifiable:** runtime-surface DEGRADE (refs/runtime-surface.md section 3): never UNREACHED, never Regression
- **Next evidence needed:** real-process run of the verb (tests/issue_watch/test_cli_e2e.py runs only once and init-state through python -m); the registration facts are src/superclaude/cli/main.py:565 and pyproject.toml:71

### Gap G-12 (RS-reset_command)

- **Hunk ref:** src/superclaude/cli/issue_watch/cli.py:282
- **Evidence missing:** static reachability of Click symbol reset_command cannot be decided: the degrade oracle matches (a) command decorator, and for the group also (b) [project.scripts] and (c) main.add_command registry
- **Why not classifiable:** runtime-surface DEGRADE (refs/runtime-surface.md section 3): never UNREACHED, never Regression
- **Next evidence needed:** real-process run of the verb (tests/issue_watch/test_cli_e2e.py runs only once and init-state through python -m); the registration facts are src/superclaude/cli/main.py:565 and pyproject.toml:71

### Gap G-13 (RU-record.py:370)

- **Hunk ref:** record.py:370
- **Evidence missing:** reuse neighbour search ran without auggie (degraded, capped at maybe-related); verdict reuse-by-import, S_reuse 0.66
- **Why not classifiable:** maybe-related reuse finding is advisory (section 10.8); the design deliberately mirrors this across a banned import edge with a parity test where marked
- **Next evidence needed:** semantic neighbour search with auggie available; nearest neighbour src/superclaude/cli/swarm/atomic.py:14

### Gap G-14 (RU-launch.py:163)

- **Hunk ref:** launch.py:163
- **Evidence missing:** reuse neighbour search ran without auggie (degraded, capped at maybe-related); verdict mirror-shape, S_reuse 0.88
- **Why not classifiable:** maybe-related reuse finding is advisory (section 10.8); the design deliberately mirrors this across a banned import edge with a parity test where marked
- **Next evidence needed:** semantic neighbour search with auggie available; nearest neighbour src/superclaude/cli/install_user_setup.py:198

### Gap G-15 (RU-launch.py:200)

- **Hunk ref:** launch.py:200
- **Evidence missing:** reuse neighbour search ran without auggie (degraded, capped at maybe-related); verdict mirror-shape, S_reuse 0.98
- **Why not classifiable:** maybe-related reuse finding is advisory (section 10.8); the design deliberately mirrors this across a banned import edge with a parity test where marked
- **Next evidence needed:** semantic neighbour search with auggie available; nearest neighbour src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:86

### Gap G-16 (RU-predicates.py:27)

- **Hunk ref:** predicates.py:27
- **Evidence missing:** reuse neighbour search ran without auggie (degraded, capped at maybe-related); verdict mirror-shape, S_reuse 0.74
- **Why not classifiable:** maybe-related reuse finding is advisory (section 10.8); the design deliberately mirrors this across a banned import edge with a parity test where marked
- **Next evidence needed:** semantic neighbour search with auggie available; nearest neighbour src/superclaude/cli/swarm/recipes/_primitives.py:15

