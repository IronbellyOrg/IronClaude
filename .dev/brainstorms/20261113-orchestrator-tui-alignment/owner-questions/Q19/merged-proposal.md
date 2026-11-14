<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 1 (proposal-A) -->
<!-- Merge date: 2026-11-14 -->

<!-- Source: Variant 3 (proposal-C), merged per Change #1 (title replaced) -->
# Proposal A (merged): Fleet Quilt first in the observer; the summary and named steps second, with their data prepared by the sweep

<!-- Source: Variant 3 (proposal-C), merged per Change #1 (Answer replaced) -->
## Answer

The first ask is a screen in the observer: Fleet Quilt (suggested) or Decision Desk, named now and started only after the contract note is final (XC-07) and the shared read-only capture is recorded (XC-03). The second ask is the plain-English summary with named steps; its data has a known deterministic source (the task title and `Command:` lines from the Orca Task brief, and step states from workers' handoff files), so that data can be prepared as a sweep Phase 2 follow-up after PR #539 merges. Issue and PR links come later.

<!-- Source: Base (original, modified); each bullet is tagged below -->
## What happens next if the owner picks it

<!-- Source: Base (original, modified); reason: ledger wording follows the new answer, merged per Change #3 -->
- The ledger records "Q19: <Fleet Quilt or Decision Desk> first, in the observer, after XC-07 and XC-03; summary and named steps second" with the date. OB-09 condition (2) ("Q19 names the first ask and its program") is met.
<!-- Source: Variant 3 (proposal-C, round1-advocate-3.md Concessions 1 and Overall), merged per Change #2 -->
- One row is added to the observer's `release-gates.md` for the chosen screen ask with its data gate (review 05 D7). If Fleet Quilt: its first step is recording what data it reads, since no source records that. If Decision Desk: it stays behind QUESTION-LINK, OB-06 and OB-02.
<!-- Source: Base (original, modified); reason: consistency with Change #1 ("this follow-up" now names the second ask); final two clauses from Variant 1 (round1-advocate-1.md Concessions 4), merged per Change #4 -->
- A row for the second ask (the summary and named steps) is added to #534 (the issue tracking the sweep's Phase 1 follow-ups) after PR #539 merges, using review 01's deterministic options: a bounded task title (the first line of the Orca Task brief, which the sweep already reads) and the `Command:` list, plus `steps: [{name, state}]` read from `<report-dir>/handoff/` with state words taken from `worker_status`, never from colour or elapsed time (variant-1-original.md lines 84 and 86, F-08 and F-10). A worker that crashed leaves no handoff file for its current step, so a missing state is shown as unknown, never as a colour; reading handoff files is a new read for the sweep and needs its own review and allow-list check.
<!-- Source: Base (original, modified); reason: consistency with Change #1 -->
- Links to issues and PRs are left out of the summary step, because they need a GitHub read the sweep does not make and a new allow-list entry (F-09, line 85).
<!-- Source: Base (original, modified); reason: consistency with Change #1 -->
- OB-09 (observer release 3) stays deferred behind QUESTION-LINK; it is the vehicle for the first ask only if Decision Desk is picked.

<!-- Source: Base (original, modified); each bullet is tagged below -->
## What it unlocks

<!-- Source: Base (original) -->
- The one ask that has a known, deterministic data source today; no new external read and no language model (review 01: "Anything richer needs an LLM, which #409's AC forbids").
<!-- Source: Base (original, modified); reason: consistency with Change #1 -->
- The summary data does not wait on QUESTION-LINK, the questions-read switch-on (OB-06) or the owner's AC-S record (OB-02), which all gate release 3.
<!-- Source: Base (original, modified); reason: consistency with Change #1 -->
- A person reading the coordinator's report sees what each worker is doing in words, which serves the reviewer's need even without any dashboard change.

<!-- Source: Base (original, modified); each bullet is tagged below -->
## What it costs or risks

<!-- Source: Variant 3 (proposal-C), merged per Change #6 (replaces base bullet 1) -->
- Both screen candidates are slow: Fleet Quilt needs its data discovered, Decision Desk waits for QUESTION-LINK.
<!-- Source: Variant 3 (proposal-C), merged per Change #6 (replaces base bullet 2) -->
- The summary data, if prepared in the sweep, appears on the dashboard only if Q17 later says yes; until then it is in the coordinator's local report.
<!-- Source: Base (original) -->
- Changes the sweep after Phase 1: a new report field and a new file read (handoff files), each needing its own review; the sweep must stay read-only and must still "recommend nothing" (WC-16).
<!-- Source: Base (original, modified); reason: consistency with Change #1 -->
- The summary data depends on PR #539 merging first.
<!-- Source: Variants 1, 2 and 3 (round1-advocate-1.md, -2.md, -3.md, A-001), merged per Change #5 -->
- The order "Fleet Quilt and Decision Desk first" is review 05's reading of the reviewer's 2026-11-11 comment; no source read shows the reviewer ranking the asks. Re-read that comment on #409 before recording Q19.

<!-- Source: Variant 3 (proposal-C), merged per Change #6 (section replaced) -->
## What stays unresolved

- The final pick between Fleet Quilt and Decision Desk.
- Where issue and PR links live.
- Whether Orchestrator v2 (#423, not started) ever displays summaries.
