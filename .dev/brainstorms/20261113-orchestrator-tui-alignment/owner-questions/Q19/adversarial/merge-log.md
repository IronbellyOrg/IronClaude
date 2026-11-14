# Merge Log: Q19

## Metadata

- Base: Variant 1 (`Q19/proposal-A.md`, identical to `Q19/adversarial/variant-1-original.md`)
- Plan: `Q19/adversarial/refactor-plan.md` (6 planned changes, approved auto, 2026-11-14)
- Output: `Q19/merged-proposal.md`
- Merge date: 2026-11-14
- Executor: merge-executor (Step 5)

## Changes Applied

### Change 1: Two-part answer (screen first in the observer, summary second)
- Status: applied
- Source: Variant 3 (proposal-C), per plan text
- Target: title and "Answer" (replaced)
- Before: title "Proposal A: the plain-English summary and named steps first, built in the sweep"; Answer "The first ask is the plain-English summary with named steps, built as a deterministic Phase 2 addition to the sweep's report (...). Issue and PR links, Fleet Quilt and Decision Desk come later."
- After: title "Proposal A (merged): Fleet Quilt first in the observer; the summary and named steps second, with their data prepared by the sweep"; Answer is the plan's text verbatim ("The first ask is a screen in the observer: Fleet Quilt (suggested) or Decision Desk, ... Issue and PR links come later.")
- Provenance tag: `Variant 3 (proposal-C), merged per Change #1` (one tag for the title, one for the Answer)
- Validation: plan text copied verbatim; H1 kept; no dashes.

### Change 2: Why Fleet Quilt is the suggested pick
- Status: applied
- Source: Variant 3 (round1-advocate-3.md Concessions 1 and Overall)
- Target: "What happens next", new bullet inserted after the ledger bullet
- Before: (no such bullet)
- After: "One row is added to the observer's `release-gates.md` for the chosen screen ask with its data gate (review 05 D7). If Fleet Quilt: ... If Decision Desk: it stays behind QUESTION-LINK, OB-06 and OB-02."
- Provenance tag: `Variant 3 (proposal-C, round1-advocate-3.md Concessions 1 and Overall), merged per Change #2`
- Validation: verbatim; position is second bullet, after the ledger bullet.

### Change 3: Ledger wording follows the new answer
- Status: applied
- Source: consistency with Change 1 (plan text)
- Target: first "What happens next" bullet (replaced)
- Before: "The ledger records "Q19: summary and named steps first, in the sweep (Phase 2)" with the date."
- After: "The ledger records "Q19: <Fleet Quilt or Decision Desk> first, in the observer, after XC-07 and XC-03; summary and named steps second" with the date. OB-09 condition (2) ("Q19 names the first ask and its program") is met."
- Provenance tag: `Base (original, modified); reason: ledger wording follows the new answer, merged per Change #3`
- Validation: verbatim except the plan's inner single quotes were written as double quotes, matching the base's quoting style.

### Change 4: Absent step state shows as unknown
- Status: applied
- Source: Variant 1 (round1-advocate-1.md Concessions 4)
- Target: the base bullet describing `steps: [{name, state}]` (appended)
- Before: bullet ended "(variant-1-original.md lines 84 and 86, F-08 and F-10)."
- After: same bullet plus "A worker that crashed leaves no handoff file for its current step, so a missing state is shown as unknown, never as a colour; reading handoff files is a new read for the sweep and needs its own review and allow-list check."
- Provenance tag: combined with consistency edit E1 on the same bullet: `Base (original, modified); reason: consistency with Change #1 (...); final two clauses from Variant 1 (round1-advocate-1.md Concessions 4), merged per Change #4`
- Validation: verbatim append.

### Change 5: Re-read the reviewer's comment before recording the order
- Status: applied
- Source: Variants 1, 2 and 3 (round1-advocate-1.md, -2.md, -3.md, A-001)
- Target: "What it costs or risks" (appended as last bullet)
- Before: (no such bullet)
- After: "The order "Fleet Quilt and Decision Desk first" is review 05's reading of the reviewer's 2026-11-11 comment; no source read shows the reviewer ranking the asks. Re-read that comment on #409 before recording Q19."
- Provenance tag: `Variants 1, 2 and 3 (round1-advocate-1.md, -2.md, -3.md, A-001), merged per Change #5`
- Validation: verbatim except inner single quotes written as double quotes.

### Change 6: Costs and unresolved items follow the two-part answer
- Status: applied
- Source: Variant 3 (proposal-C "What it costs or risks"), consistency with Change 1
- Target: "What it costs or risks" bullets 1 and 2 (replaced); "What stays unresolved" (replaced)
- Before: bullet 1 "Goes against the spec's recommendation and review 05's ordering, ... (variant-5-original.md line 252)."; bullet 2 "The summary appears in the sweep's report, not on the dashboard the reviewer looked at; showing it on the dashboard would need Q17 = yes."; unresolved: "Where issue and PR links live (sweep with a GitHub read, or the observer)." and "When Fleet Quilt and Decision Desk are built."
- After: bullet 1 "Both screen candidates are slow: Fleet Quilt needs its data discovered, Decision Desk waits for QUESTION-LINK."; bullet 2 "The summary data, if prepared in the sweep, appears on the dashboard only if Q17 later says yes; until then it is in the coordinator's local report."; unresolved: three bullets "The final pick between Fleet Quilt and Decision Desk.", "Where issue and PR links live.", "Whether Orchestrator v2 (#423, not started) ever displays summaries."
- Provenance tag: `Variant 3 (proposal-C), merged per Change #6` (per bullet in costs; one tag for the unresolved section)
- Validation: plan's semicolon list split into three bullets to keep the base's bullet format; wording unchanged.

## Consistency edits

Every unchanged base sentence was re-read against the two-part answer. Six base sentences contradicted it or no longer had a clear subject and are not covered by the plan; each got the minimal edit below, tagged `Base (original, modified); reason: consistency with Change #1`.

| # | Section | Before | After | Why |
|---|---|---|---|---|
| E1 | What happens next | "A row for this follow-up is added to #534" | "A row for the second ask (the summary and named steps) is added to #534" | After Changes 1 to 3, "this follow-up" no longer pointed to the summary; the preceding bullets are about the screen ask. |
| E2 | What happens next | "left out of this first step" | "left out of the summary step" | The summary is now the second ask, not the first step. |
| E3 | What happens next | "it is no longer the vehicle for the first ask." | "it is the vehicle for the first ask only if Decision Desk is picked." | If Decision Desk is the first ask it stays in release 3 (proposal-C line 11; plan Change 2), so "no longer the vehicle" was false for that pick. |
| E4 | What it unlocks | "Does not wait on QUESTION-LINK, ... which all gate release 3." | "The summary data does not wait on QUESTION-LINK, ... which all gate release 3." | The first ask (if Decision Desk) does wait on those gates; the claim now names the part it is true for. |
| E5 | What it unlocks | "even before any dashboard change." | "even without any dashboard change." | The first ask is now a dashboard (observer) change, so the summary is no longer said to land before it. |
| E6 | What it costs or risks | "Depends on PR #539 merging first." | "The summary data depends on PR #539 merging first." | The Answer ties only the summary data to PR #539; the screen ask waits on XC-07 and XC-03. |

Checked and left unchanged: "What it unlocks" bullet 1 (still true of the summary ask; "no new external read" refers to GitHub, not to local handoff files) and "What it costs or risks" base bullet 3 (sweep change after Phase 1; still true of the summary data step).

## Post-Merge Validation

- Heading hierarchy: one H1 (title), five H2 in order: Answer; What happens next if the owner picks it; What it unlocks; What it costs or risks; What stays unresolved. No skipped levels.
- Provenance: header block present (Provenance, Base, Merge date); a Source tag before the title, every section and every changed bullet.
- Internal references: the merged text has no section cross-references. Citations kept from the base resolve outside D: `variant-1-original.md lines 84 and 86` and `line 85` match F-08, F-10 and F-09 in `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/adversarial/variant-1-original.md` (not the Q19 copy of that name). The base citation `variant-5-original.md line 252` was removed by Change 6. No new line numbers were added.
- Contradiction re-scan: done (see Consistency edits); no remaining sentence says the summary is the first ask.
- Dashes: no em dashes or en dashes in the merged file.

## Summary

- Planned changes: 6 of 6 applied, 0 skipped, 0 escalated.
- Consistency edits: 6 (E1 to E6).
- Status: success.
