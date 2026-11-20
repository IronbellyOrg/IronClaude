# Codegraph grounding (plan TASK-WF-planIssue691Part-20261120-204103)

## Run state

- index_state: fresh (codegraph_status: 3519 files, 0 added, 0 modified, 0 removed; latest file indexed 2026-11-20T20:34:39Z)
- access: mcp (status tool listed; lookup tools listed)
- worktree_root: the issue-691-part-b worktree
- Languages indexed: python, javascript, typescript, yaml, liquid. Bash is not indexed, so every lookup into the `.sh` files and the runbook used the floor (Grep, Read). Token: `graph:empty` for the shell files (no symbols exist for them).
- Python symbols in `orca_worktree.py` were read directly with Read (verified line numbers), not through graph rows.

## Resolved symbols

- `write_launch_result` src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:244 (Read)
- `LAUNCH_RESULT_NAME` same file line 241; copy skip at line 477 (Read)
- `cmd_launch` line 1707, inner `finish` line 1711 (writes the file); `already_launched` branch `emit` at line 1730 (no write) (Read)
- `launch_result` line 1657 (field list); `session_report` line 1456 (release text, `<session id>` with a space at line 1482, `inode number` text at line 1473) (Read)
- session-gov.sh: `claim_send` 118, `claim_has` 148, `launch_real` 155, `release_session` 193, `inode_record` 263, `preflight_refusal` 239, `run_b` 277, `run_c` 341, `run_d` 370, `run_e` 433 (Read, master 1a6c8723f)

## Dependents

- Readers of the claim text in `.dev/issues/442/`: only `session-gov.sh` (Grep for `CLAIM_`, `claim-T`, `terminal list`, `L1 guard`, `rm"`; `setup-github.sh` has its own `--pipeline none` claim wait and never reaches `cmd_launch`).
- `evidence.sh` reads the gov-log record ids (`b-inode`, `b-<case>-claim|pending|no-mirror|no-record`, `b-ctx-released`); none of those ids change. The `$sub-terminal` record id is removed and no reader uses it.
- Callers of `release_session`: run_b line 330, run_c 353, run_d 382, run_e 467. Callers of `claim_send`: `launch_real` (163) and `preflight_refusal` (241). Callers of `launch_real`: run_b 298, run_c 344, run_d 374, run_e 437. Callers of `claim_has`: `launch_real` 168 and `preflight_refusal` 243.
- Runbook citations of session-gov.sh lines: 767 (421, 423), 769 (195, 209), 846 (2), 856 (82). `runbook-selftest.sh` checks each quote against its cited line; its anchors are lines 228, 505, 520, 536, 698. `session-gov-selftest.sh` reads runbook lines 536 to 697.
- Outside `.dev/issues/442/`: Grep for `session-gov|observation-runbook|442/scripts` finds only packages under `.dev/tasks/done/` (history). No `tests/` or `docs/` file reads these scripts.

## Pre-check

Checked by Read/Grep (shell files are not indexed): every `session-gov.sh` line the plan cites (82, 118, 148, 155, 163, 168, 181, 193, 195, 209, 241, 243, 252, 298, 330, 344, 353, 374, 382, 421, 423, 437, 467) holds the text the plan says; every `orca_worktree.py` line it cites (244, 477, 1473, 1482, 1711, 1730) holds the stated code. Dependents the plan did not name: none found (no `tests/`, `docs/` or `src/` reader of these scripts). 0 of 7 tasks name a missing file or symbol.
