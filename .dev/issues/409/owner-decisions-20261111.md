# Owner decisions, 2026-11-11 (phase 2 gate)

Source: owner replies in the coordinator session after the phase 2 gate research report
(`.dev/tasks/to-do/TASK-RESEARCH-phase2-gate-20261111-200400/RESEARCH-REPORT-phase2-gate.md`).

| Decision | Owner answer | Meaning for phase 2 |
|---|---|---|
| 8: what identifies a human question | "coordinator questions only" | The list shows only messages of type `question`, labelled "coordinator questions" (not "human"). Worker completion reports and escalations are out of scope. |
| 6: permission to read that scope | "Permission granted, proceed" | The observer may read one named Run's question messages. Read scope as recommended in the report: one named Run, `--types question`, never `run-use`. The owner did not name the Run beyond that; phase 2 plan must state which Run. |

## Coordinator measurement taken after decision 6 (read-only, own Run run_93bfa00cae2b)

- `check --all --run <run>` returned 100 rows (the cap): 91 heartbeat, 8 worker_done, 1 question. A read of the whole mailbox therefore hides most questions behind heartbeats.
- `check --all --run <run> --types question` returned 41 rows. So the cap is applied after the type filter; phase 2 must pass `--types question`.
- A later consuming `check` found 0 pending: the reads did not consume. Tested as the Run's owner only.

Still UNVERIFIED: read from an unbound observer terminal (Q-1), effect of `run-use` on a live coordinator (Q-2), message rate on a Run other than this one.
