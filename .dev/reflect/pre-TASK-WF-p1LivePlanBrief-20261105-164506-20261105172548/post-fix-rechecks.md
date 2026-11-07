# Fix cycle 1 (revision 2 of the plan), applied in place before the plan's first task

Source: the merged debate of this run (`adversarial/`), the invariant probe (`adversarial/invariant-probe.md`) and the three reviewer cards. Correction of revision 1: its row 2 ("Task 1 compares every file", justified by "spec says every file") was wrong. The spec has no `cmp`-every-file rule (round 2, advocate 3), and the broad wording was introduced by revision 1 itself; it made the install line fail on `README.md` and `__init__.py`, which the installer never copies (`src/superclaude/cli/install_commands.py:11,40`).

| # | Finding | Sev | Fix in the plan |
|---|---|---|---|
| 1 | C-001: Task 1 install line cannot pass (README.md, `__init__.py`; `cmp` rc=2, reproduced by three advocates) | HIGH | Compare every `*.md` directly under `src/superclaude/commands/` except `README.md`, with the reason and file:line |
| 2 | C-002 and INV-001: clean-tracked-tree check fails for any plan edit | HIGH after probe | Check is `git status --porcelain -- src plugins tests`; `.dev/` edits do not matter |
| 3 | C-003: Task 23 `find` can never be empty (326 tracked contract files) | LOW | `ac13-find-before.txt` baseline and `ac13-find-diff.txt`; PASS only on an empty diff |
| 4 | C-004 quoting: whole Constraints bullet would be copied into the brief | LOW | Owner instruction is only the text between `>>>` and `<<<` markers |
| 5 | C-005: Task 25 acceptance still said "grant file" | LOW | Reworded |
| 6 | C-008: D-P1-5 cited for staging | LOW | Cites WC-9; says what D-P1-5 covers |
| 7 | U-003 and INV-010: `pgrep -af -- '--watch'` matches the executor's own shell, PIDs differ per call | MEDIUM | `ps -eo args` listing, filtered, compared without PIDs (Tasks 9 and 19) |
| 8 | U-004 and INV-011: no rule to compare the worker's report path with `<R>/return-contract.yaml` | MEDIUM | Compare after `realpath -m` |
| 9 | INV-012: a retried Task 1 would create a second Orca run | MEDIUM | Reuse an existing `live-run.json` and `status-baseline.txt` |
| 10 | U-001: `--parent-worktree active` may attach to Orca's active worktree, not the coordinator's | MEDIUM | `lc22-parent-check.txt` must show the feature worktree as parent; mismatch fails before dispatch |
| 11 | U-002: no rule that tasks run one at a time | LOW | Constraints bullet "Task order" |
| 12 | C-013: static report covers `7127c247`, not the tip | LOW | Task 25 report states both |
| 13 | INV-014: plan's revision note and provenance | LOW | Note now lists two revisions with their files |

Not changed (with reason): U-005 (skills install exclusion; no touched skill has a same-named command, three advocates ran the check), U-006 (lc13 and lc15 flags; spec 2.1 permits both), C-009 (documented at plan line 41, per task), C-010 (reflect matrix trace debt, the plan covers each span).

# Fix cycle 2 (revision 3 of the plan), applied in place before the plan's first task

Source: `recheck-1.md` (verdict: 1 blocking finding, 9 minor).

| # | Finding | Sev | Fix in the plan |
|---|---|---|---|
| 14 | B1: a Task 1 retry or a resumed live task runs in a new Orca terminal, but nothing re-attaches the run (`worker-start` is refused with `consumer_fenced`), and the AC on `coordinator_handle` cannot pass | blocking | Task 1: if the reused run's `coordinator_handle` differs from `$ORCA_TERMINAL_HANDLE`, run `orca orchestration run-use --id <run_id> --json`, save `./artifacts/run-use.json`; same rule at the start of any resumed live task (`run-use-<NN>.json`); AC accepts a matching handle or the run-use receipt |
| 15 | M1: baseline files overwritten before the keep clause is read | minor | The save sentence itself now says "only for a file that does not exist yet", for both baseline files |
| 16 | M2: help list lacks `worktree current` and `orchestration run-use` | minor | Both added to the Task 1 help list |
| 17 | M3: no AC for `lc22-parent-check.txt` | minor | Task 24 AC added (parent equals feature worktree id, else FAIL and nothing dispatched) |
| 18 | M4: `grep -v -e ps` and `-e 'bash -c'` drop real lines | minor | `grep -v -w -e grep -e shell-snapshots -e ps | sort`; exit 1 with an empty listing stated as the passing case |
| 19 | M5: lc08 has no before/after listing files | minor | `lc08-pgrep-before.txt` and `lc08-pgrep-after.txt` named in the extra and in the lc08 AC |
| 20 | M6: `find` output order not stable | minor | Both Task 23 `find` runs piped through `sort` |
| 21 | M9: "carry verdicts" vs step-5 per-condition "verdict" | minor | Wording: "check verdicts" plus a note that step-5 entries are condition results |

Not changed (optional in the recheck): M7 (indented `>>>` marker renders as a quote; the executor reads raw text, which is correct), M8 (skill diff base is local `master`; the wider compared set is harmless and all 15 files pass today).
