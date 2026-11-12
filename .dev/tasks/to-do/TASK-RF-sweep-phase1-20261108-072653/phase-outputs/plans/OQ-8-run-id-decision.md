---
needs_human_decision: true
status: RESOLVED
---

# Step 1.0a Run id request (OQ-8)

## Request

The step 1.0a read-only Orca capture needs one existing Orca Run, named by the person. Quoted from the design and from the research:

> DESIGN section 15.1, `docs/designs/orchestrator-mode.md:894`: "It runs against an existing Run that the person names. It creates no Run, Task or Dispatch; the REPORT's throwaway Run is dropped."

> research/09 Gap 3, `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/research/09-gap-fill.md:98`: "The task item should ask for one Run id with at least one Dispatch (better one live and one settled worker, so items 4 and 13 can be captured), and should note that template 1 (`run-current`) shows the bound Run if the person has none in mind."

In plain words: please name one existing Run by its id. The Run must hold at least one Dispatch row (a worker assignment). Best is a Run with one live worker and one settled worker, so capture items 4 and 13 can be recorded. If you have no Run in mind, `orca-ide orchestration run-current` (plain output, never `--json`) shows the Run bound to the current session. The capture only reads: it creates no Run, Task or Dispatch. The same Run is used by the step 1.4 live check (item 9.3, run once the CLI is registered).

How to answer: give the Run id in your own words, say how many Dispatch rows it holds (or say in your own words that it holds at least one), and the executor records your words below. A Run with zero Dispatch rows is not enough: item 7.16 step (1) would learn no Dispatch id, template 3 would never run, and the `DISPATCH_ID_RE` half of DESIGN section 17 open item 2 would stay unverified.

## Blocked work

Item 7.15 halts while `Run id:` is empty, or the record does not say the named Run has at least one Dispatch row, or `Given by:` or `Source:` is empty. This blocks item 7.16 (the step 1.0a capture), the step 1.0a items after it, and the step 1.4 live check (item 9.3).

## Run id record

Run id: run_a4723d345399
Dispatch rows: 5 (counted by the executor on 2026-11-11 with one read-only listing, `orca-ide orchestration worker-list --run run_a4723d345399 --json`: 5 worker rows, 5 distinct dispatch ids, every row dispatchStatus completed, workerState succeeded, terminalState released). No row is live, so capture items that need a live worker may be recorded UNVERIFIED in step 1.0a.
Given by: Ryan Wiancko, owner, 2026-11-11.
Source: In this session's Run-id question the owner selected "Use run_a4723d345399 (Recommended)", whose option text reads: "Issue 504, 5 parallel sessions, 5 completed Dispatch rows. Small enough for the capture to inspect each one (one worker-show per Dispatch). I record your selection as the Run id and continue with the capture (item 7.16)." The owner had earlier pasted the output of `orca-ide orchestration run-list` (ten Runs) and written "pick one, your choice"; a first record built on that delegation alone was withdrawn after review, and this selection replaces it. The other offered option was `run_58af03dbfa92`. This resolves OQ-8 only and grants nothing else.

## Executor's Dispatch counts (evidence behind the Dispatch rows line; not part of the answer)

Counted on 2026-11-11 with the same read-only listing, counts and states only:

| Run id | Dispatch rows | States |
|---|---|---|
| run_a4723d345399 | 5 | every Dispatch completed, worker succeeded, terminal released |
| run_52c9fe174991 | 1 | completed, succeeded, terminal retained |
| run_703283babf1b | 1 | completed, succeeded, terminal released |
| run_3ceb5154f1d2 | 1 | completed, succeeded, terminal released |
| run_58af03dbfa92 | at least 100 (the first page returned 100; its terminal-state counts add up to 137) | mixed: completed, failed and abandoned; terminals released, retained and reclaimable |
| run_14cfcbd8edf2, run_c1badaa6576b, run_08fc0ad8a647, run_c51a03ef71a7, run_49770af7b34a | 0 | no worker, so not usable (item 7.15 needs at least one Dispatch row) |

No listed Run has a live worker.
