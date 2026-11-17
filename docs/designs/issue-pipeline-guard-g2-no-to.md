# Design: a bound worker passes no `--to` (closes the run-address gap of PR #591)

Grounding: index_state: fresh (checked_at 2026-11-17T14:36:00Z, codegraph_status only; the guard is a shell file and the rest was read with Read and Grep, so no lookup tool was used). Orca help read with `orca orchestration ask --help` on 2026-11-17.

## Problem

The launch-level guard (`src/superclaude/hooks/scripts/launch-level-guard.sh`, address block at lines 500-549) lets a bound worker run `orca orchestration send` and `ask` when `--to` is absent or names a `run:<id>`. It checks only the shape `run:<id>`, not that the id is the worker's own coordinator Run. A worker that learns another Run's id could write to that Run's mailbox. Augment reported this on PR #591; the shape check cannot be tightened because the hook has no trusted source for the worker's own Run id (the launch record holds only the level word).

## Decision

A bound worker may not pass `--to` at all. Orca's own help says "From an active Dispatch, a new question defaults to its owning Run mailbox" (`ask --help`), and the same default holds for `send` (`send --help`, quoted in `docs/designs/issue-pipeline-guard-g2.md` section 5). The default is the one address that is always the worker's own coordinator, so the guard needs no id and no new record. Any `--to`, `--to=...` or `--to` spelling is ESCAPE, like `--run` already is.

Rejected: storing the coordinator's Run id in the launch record. It changes the record format the hook parses (`read -N 13`, lines 262-269 and 302-307), the `pending` helper, the coordinator duties and the brief, for no gain over the Orca default.

## Risk this leaves (stated, not hidden)

If the default does not reach the coordinator for some verb (G2 note fact 3, never run against a bound worker), that verb is unusable for a bound worker and fails closed: the call is blocked and the worker reports through its screen. No live test is allowed in this change; the owner's live test of the first claimed issue is the check.

## Task 1: guard change, both copies

Edit `src/superclaude/hooks/scripts/launch-level-guard.sh`, then copy it byte for byte to `plugins/superclaude/hooks/scripts/launch-level-guard.sh`.

AC:
- Delete `LL_RE_RUN`, the `LL_WANT = to` branch, the `--to)` and `--to=*)` case arms and the `[ "$LL_WANT" = to ]` line, so `--to`, `--to=x`, `--To`, `--TO=x` and every `--to*` spelling reach the existing `--to* | --run* | ...) LL_SBAD=1` arm.
- Update the comment above the block so it says a bound worker passes no `--to`.
- `bash -n` passes and `cmp` shows the two copies identical.
- A bound worker's heartbeat, ask, `--body`, `--json` and `worker_done` commands without `--to` stay allowed.

## Task 2: tests

Edit `tests/hooks/test_launch_level_guard_worker.py`.

AC:
- The allowed list (`test_a_bound_worker_may_send_and_ask_its_coordinator`) no longer holds a command with `--to`; the four former `--to run:...` entries (lines 63, 64, 70, 71) move to the blocked list, expecting LL-ESCAPE.
- A new blocked case exists for each of: `--to run:run_93bf`, `--to=run:run_93bf`, `--To run:r1`, `--TO=run:r1`, on both HEARTBEAT and ASK.
- Existing blocked cases keep passing unchanged.
- `uv run pytest tests/hooks/test_launch_level_guard_worker.py` passes, and `uv run pytest tests/hooks -k launch_level -q` passes.

## Task 3: design note and any doc that states the rule

AC:
- `docs/designs/issue-pipeline-guard-g2.md`: section 5 rule (line 32) says the worker passes no `--to` and any `--to` is blocked; the "Known residual risk (found in the PR #591 review)" paragraph is replaced by one sentence saying the gap is closed by this rule, with the fail-closed risk of fact 3 named.
- `grep -rn "names .run:<id>\|--to. names\|run:<id>" docs/designs docs/architecture` hits are each checked; a statement of the old rule is corrected, other hits (Orca address forms, `dispatchReportMailbox`) are left.
- The design note names no new open fact beyond fact 3.

## Task 4: tell the worker not to pass `--to`

Edit `src/superclaude/core/WORKER-CONTRACT.md`, rule WC-17 (or the worker's duties for messages, whichever already lists the `ask` and heartbeat commands), then `make sync-dev`.

AC:
- One sentence says a bound worker sends and asks with no `--to` (the owning Run mailbox is the default) and that the guard blocks any `--to`.
- `tests/skills/test_worker_contract.py` has a pin for that sentence; `uv run pytest tests/skills/test_worker_contract.py` passes.
- `make verify-sync` is clean. `.claude/` files are never staged.

## Out of scope

No change to the launch record, `orca_worktree.py`, the brief, `release-worker`, or any non-worker session. No live test, commit or push.
