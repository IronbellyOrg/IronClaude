# Coordinator ledger steps for the S1 ledger arm (issue 346, theme ledger)

Owner ruling (2026-11-08): every script write (`init`, `find`, `answer`, `begin` with its scripted spec revert, `verify`, `close`, `sweep`) is done by a separate ledger step that the coordinator runs between the S1 brief tasks, itself or as an inserted dispatch, with the brief templates in this folder. The verbatim S1 review and reviser briefs (`../`) allow their sessions to write only their own output files, so those sessions never run a call that writes a file: they read files the script wrote (`ledger.json`, `plan-r<k>.md`, a `close` tail), may run only `status`, `verdict` and `--dry-run` calls (Option A ruling; these write no file), and hand their rows over in one fenced `ledger-input` block inside their own report (a reviser: inside its own disposition file). No template here asks a review or reviser session to run anything.

Placeholders in the templates: `<repo root>` (the replicate's worktree), `<rep>` (the replicate name, for example `led-r1`), `<seq>` (the `seq` the previous call printed), `<k>` (the review number), `<skill base>` (the installed `~/.claude/skills/sc-review-ledger`, else the project `.claude/skills/sc-review-ledger`), `<disposition file>`, `<review output file>`, `<last review report>`.

## Dispatch order

1. `L0-init.txt`
2. T05 (review 1, `../T05-R1-reviewer-L11-699ae853.txt`)
3. `L-find-close.txt`
4. T06 (revise 1, `../T06-R1-reviser-L10-3bb70411.txt`)
5. `L-begin.txt` (review 2 starts: snapshot r2, diff, auto-claim, scripted revert with the flag copied from T07)
6. T07 (review 2, `../T07-R2-reviewer-L11-aff19d65.txt`)
7. `L-verify-close.txt`
8. T08 (revise 2, `../T08-R2-reviser-L10-66468bab.txt`)
9. `L-begin.txt` (review 3 starts; flag copied from T09)
10. T09 (review 3, `../T09-R3-reviewer-L11-1c9a7ec8.txt`)
11. `L-verify-close.txt`
12. The sweep route (below). T10 is not dispatched: review 3 always ends the loop.

**Skip rule.** After any `close` whose `verdict` exits 12 (the loop is terminal at review 1 or 2: PASS or ESCALATE), the remaining T06 to T09 dispatches and their ledger steps are skipped and the sweep route runs next. A review-1 PASS is swept too; the sweep is never skipped. Exit 10 means CONTINUE: dispatch the next reviser.

## Sweep route

The sweep runs once after the terminal `close`, in a context that never opens the ledger folder, on the copy `sweep --prepare` prints.

- **Smoke check, recorded before replicate 1.** Dispatch one throwaway worker with the ledger-step wrapper of `L-sweep-subagent.txt`; it must spawn an Agent-tool subagent whose run lasts longer than 5 minutes, while the worker keeps sending its 5-minute heartbeat the whole time. Record the result (spawned yes/no, heartbeats seen during the subagent run, subagent run time) before replicate 1.
- **Subagent route** (only when the smoke check passed): `L-sweep-subagent.txt`, one dispatch, still 5 S1 dispatches in all.
- **Fallback route** (when the smoke check failed or was not run): `L-sweep-prepare.txt`, then `../T09b-sweep-dispatch.txt` with the printed copy path filled in, then `L-sweep-ingest.txt`. T09b is a sixth dispatch, declared as a deviation.

After the sweep, `verdict` exits 0 (delivery PASS) or 11 (delivery ESCALATE).

## Recovery

- **`E-REPORT-EDITED`** from `begin` (a review report no longer ends with the tail `close` appended): run `close --report <that report>` with the next `--expect-seq`; it re-appends the stored tail without a new decision. Then run `begin` again (`L-begin.txt` says this).
- **Any other refusal** stops the step; the step escalates with the script's JSON output and never retries with a changed input or edits the ledger by hand.
- **Rerun of an aborted replicate:** `L0-init.txt` with `--archive-existing` (renames the old ledger folder; never a manual delete).
