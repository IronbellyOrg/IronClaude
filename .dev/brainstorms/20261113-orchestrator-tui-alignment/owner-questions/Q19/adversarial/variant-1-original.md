# Proposal A: the plain-English summary and named steps first, built in the sweep

## Answer

The first ask is the plain-English summary with named steps, built as a deterministic Phase 2 addition to the sweep's report (the task's title from its brief, its command list, and each step's state from the worker's own handoff files). Issue and PR links, Fleet Quilt and Decision Desk come later.

## What happens next if the owner picks it

- The ledger records "Q19: summary and named steps first, in the sweep (Phase 2)" with the date.
- A row for this follow-up is added to #534 (the issue tracking the sweep's Phase 1 follow-ups) after PR #539 merges, using review 01's deterministic options: a bounded task title (the first line of the Orca Task brief, which the sweep already reads) and the `Command:` list, plus `steps: [{name, state}]` read from `<report-dir>/handoff/` with state words taken from `worker_status`, never from colour or elapsed time (variant-1-original.md lines 84 and 86, F-08 and F-10).
- Links to issues and PRs are left out of this first step, because they need a GitHub read the sweep does not make and a new allow-list entry (F-09, line 85).
- OB-09 (observer release 3) stays deferred behind QUESTION-LINK; it is no longer the vehicle for the first ask.

## What it unlocks

- The one ask that has a known, deterministic data source today; no new external read and no language model (review 01: "Anything richer needs an LLM, which #409's AC forbids").
- Does not wait on QUESTION-LINK, the questions-read switch-on (OB-06) or the owner's AC-S record (OB-02), which all gate release 3.
- A person reading the coordinator's report sees what each worker is doing in words, which serves the reviewer's need even before any dashboard change.

## What it costs or risks

- Goes against the spec's recommendation and review 05's ordering, which put Fleet Quilt and Decision Desk first "in the order the reviewer values" (variant-5-original.md line 252).
- The summary appears in the sweep's report, not on the dashboard the reviewer looked at; showing it on the dashboard would need Q17 = yes.
- Changes the sweep after Phase 1: a new report field and a new file read (handoff files), each needing its own review; the sweep must stay read-only and must still "recommend nothing" (WC-16).
- Depends on PR #539 merging first.

## What stays unresolved

- Where issue and PR links live (sweep with a GitHub read, or the observer).
- When Fleet Quilt and Decision Desk are built.
