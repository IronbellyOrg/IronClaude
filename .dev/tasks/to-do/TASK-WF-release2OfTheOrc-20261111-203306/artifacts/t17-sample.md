# T17 sample on a Run the executor created (plan Task 17)

**Run named by the executor, with the owner's permission to choose one ("find and name your own run"): `run_86013b917868`, a throwaway created for this sample. It is synthetic. It says nothing about real traffic.**

## Authority and departures from the plan text

The plan says Task 17 is blocked until the owner names the Run, allows only the one non-consuming template read, and expects an argv log that shows only the template. On 2026-11-11 (about 22:34 UTC) the owner told the executor, in the executor's session (the message is not a file in the repository): "Find and name your own run, there is no reason I should be forced to name this.. evaluate your options and choose the best one." The executor therefore chose the Run itself. That departs from the plan in two ways, both a consequence of choosing a Run nobody else holds: (1) the Run was not named by the owner; (2) the executor ran `run-create` once and `send` seven times, but only on the Run it created. The argv log below separates the measured template reads from those setup commands. Nothing was sent to or read from any Run the executor did not create (the single fenced read of Run A is recorded in `q1-result.md`).

## Why this Run (options weighed)

| Option | Verdict |
|---|---|
| The coordinator's own Run `run_93bfa00cae2b` | Real traffic, but only its own terminal holds it, an observer terminal is fenced from it (Q-1 FAIL), and the only other route is `run-use`, which is forbidden. Rejected. |
| Probe Runs A and B from the gate research | Bound to the research worker's terminal, so every other terminal is fenced (Q-1). Unreadable. Rejected. |
| A new throwaway Run created from the plain terminal, seeded with synthetic questions | The terminal that creates a Run holds it, so it can read it with the exact template and no `run-use`. Nothing real is read or changed. **Chosen.** |

## What was run (plain terminal, which created and holds the Run)

1. `orchestration run-create --objective "<text>" --json` (creates and binds the Run).
2. Seeded: 5 messages `--type question` and 2 `--type status`, each `send --to run:<id>`, synthetic subject and body.
3. Template argv, twice, about 6 s apart (22:36:32Z and 22:36:38Z): `check --all --types question --run run_86013b917868 --json`.

No `--peek`, plain `check`, `--ack`, `run-use`, `reset` or `ask`. Raw output stayed in a temporary folder and is not committed.

## Measured (redacted)

| Item | Read 1 | Read 2 |
|---|---|---|
| exit status, `ok` | 0, true | 0, true |
| rows returned | 5 | 5 |
| `result.count` | 5 | 5 |
| types in the rows | only `question` (the 2 status messages were not returned) | same |
| distinct `message.id` | 5 of 5 | 5 of 5 |
| ids and order vs read 1 | | identical, same order |
| `delivered_at` | all null | all null |
| window full (exactly 100 rows) | no | no |
| row keys | `body, created_at, delivered_at, delivery_contract, from_handle, id, payload, priority, run_id, subject, thread_id, to_handle, type` (the 13 recorded keys, no more) | same |

Call latency was not measured (the timing helper `bc` is not installed on the host).

## What this shows and does not show

- Shows: the template works end to end through real Orca for a Run the reader holds; `--types question` filters on the server; `message.id` is unique within the Run; two reads 6 s apart return the same ids in the same order; no new id appeared (nothing was sent between the reads); the read left `delivered_at` null.
- Does not show: a real message rate (5 messages sent by hand); identity on real traffic; behaviour on a busy Run; non-consumption by a non-owner (Q-1: the non-owner read is refused). The rate is not proof of completeness. The label stays `bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost`.

argv log in this artifact: the measured reads are the one template shape above, twice. Setup on this Run only: one `run-create` and seven `send` calls (5 question, 2 status). No other argv was run for this task.
