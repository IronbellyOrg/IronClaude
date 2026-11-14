# Q23: is `reclaimable` live, historical or its own state?

## The question, verbatim

Spec row (merged-requirements.md section 3, line 550): "Is `reclaimable` live, historical or its own state?"

Original wording (ADJ Part 7, line 793): "Is a `reclaimable` worker live, historical, or its own state?"

## Spec's recommended answer

"Its own state, shown with Orca's word, until decided (default, no debate verdict)" (merged-requirements.md line 550; ADJ line 793: "Its own state, shown with Orca's word, until you decide (default, no debate verdict)").

## Default if unanswered

"ADJ: its own state" (merged-requirements.md line 550).

## What it gates

- XC-05, the contract note between the observer and the sweep (merged-requirements.md line 453): its mapping table of shared words must include "the `reclaimable` row (Q23 default: its own state)". Dependency row 108 (line 755): Q5, Q13, Q22, Q23 feed XC-05's content.
- OB-06, the guard-flip PR that switches on the observer's coordinator-questions read (line 254), prerequisite (e): "the `reclaimable` mapping row exists in the contract note draft (XC-05) or, if the note is not yet merged, in the observer spec (INV-023, Q23)". OB-06 depends on Q23 (line 254, depends-on column).
- Wave needed by: W1.

## Facts the question depends on

| Fact | Source |
|---|---|
| Orca reports four count keys for workers: `active`, `reclaimable`, `retained`, `released`; its `worker-list --help` lists terminal states `active`, `reclaimable`, `retained`, `release_pending`, `release_unknown`, `released` (filter behaviour not run, UNVERIFIED) | `src/superclaude/cli/observe/view.py:95`; `.dev/issues/409/bmad/spec-orca-observer/unverified-register.md:58` (Orca 1.4.245-aidev02.9cfecdd30b2a) |
| The observer treats only `released` and `retained` as historical; historical rows are hidden from the default view and shown with the `h` key | `view.py:35` (`HISTORICAL_STATES = ("released", "retained")`), `view.py:363-366`, `view.py:844-848,902-903`, read 2026-11-14 |
| So `reclaimable` rows stay in the observer's default view | invariant probe INV-023 (`.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/adversarial/invariant-probe.md` line 30, MEDIUM, UNADDRESSED); ADJ line 258 |
| Live first page of Orca counts at the probe: reclaimable 27, released 41, retained 32, active 0 | INV-023; ADJ line 230 |
| The sweep derives "settled" from Orca's `outcome` (succeeded, partial or failed) and "historical" from its 6 h window, not from the terminal state | `src/superclaude/cli/sweep/classify.py:98,114-115,781-786`; ADJ line 258 |
| For a worker in state `reclaimable` with next action `release`, the sweep's "safe to close" terminal value is "could not determine" with reason "result read not observable" | `classify.py:479-481`, read 2026-11-14 |
| Mapping-table row (ADJ): "the note decides which side of 'historical' `reclaimable` is (Q23); until then show Orca's word `reclaimable` and do not call it live or historical" | ADJ line 258 |
| Exact Orca meaning of `reclaimable` is not documented in any file read here; the name and the next action `release` suggest a finished worker whose resources can be released, UNVERIFIED | negative evidence: grep of `src/`, `docs/`, `.dev/issues/409` on 2026-11-14 |
| The shared read-only Orca capture (XC-03) is planned but not run; it does not list `reclaimable` among its recordings | merged-requirements.md line 451 |
