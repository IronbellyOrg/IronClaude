# Merge Log: Q17

## Metadata

- Pipeline step: /sc:adversarial Step 5 (merge execution)
- Merge date: 2026-11-14
- Base: Variant 2 (proposal-B.md; byte-identical to adversarial/variant-2-original.md, checked with `cmp`)
- Plan: adversarial/refactor-plan.md (4 planned changes, all additive, all Low risk; approved auto, non-interactive)
- Output: merged-proposal.md
- Supporting sources read: proposal-A.md, proposal-C.md, adversarial/round1-advocate-1.md
- Citation checks: merged-requirements.md line 200 read directly (SW-11 row names V2-04 "if v2 reads stored sweep facts"); ADJ line 81 taken from the plan as allowed (also cited the same way by advocates 1 and 3 and the debate transcript)

## Changes Applied

### Change #1: Written re-ask trigger

- Status: Applied
- Source: round1-advocate-1.md "Suggested merge"; round1-advocate-2.md "Concessions" 1; round1-advocate-3.md "Overall" (base weakness U-002)
- Target: "What happens next if the owner picks it", appended as the last bullet
- Before: section ended with the contract-note (XC-05) bullet; no re-ask trigger anywhere in the document
- After: new bullet "The ledger also records a re-ask trigger: ask Q17 again when Q19 (which reviewer ask comes first) picks Decision Desk or OB-09 is scheduled, and only after PR #539 has merged."
- Provenance tag: `<!-- Source: round1-advocate-1, round1-advocate-2 and round1-advocate-3 (shared suggestion for base weakness U-002), merged per Change #1 -->`
- Validation: wording matches the plan's integration point; no new citations. Introduces a conflict with the unchanged base bullet in "What it costs or risks" (see Post-Merge Validation, item C-1).

### Change #2: Freshness gap recorded for any later yes

- Status: Applied
- Source: Variant 1 (proposal-A) "What it costs or risks" bullet 4; diff points U-001, C-005
- Target: "What happens next if the owner picks it", placed directly after the contract-note (XC-05) bullet and before the Change #1 bullet
- Before: contract-note bullet covered only the verbatim-words and report-age rule (ADJ line 253)
- After: new bullet "The contract note also records that sweep facts are always older than live Orca rows (the coordinator sweep is capped at once per 5 minutes, a cap and not a schedule, ADJ line 81), so any later panel must show the report age prominently."
- Provenance tag: `<!-- Source: Variant 1 (proposal-A), "What it costs or risks" bullet 4 (diff points U-001, C-005), merged per Change #2 -->`
- Validation: wording matches the plan; ADJ line 81 is a citation the plan permits. Consistent with the existing verbatim-words and report-age rule.

### Change #3: Leave room in Decision Desk

- Status: Applied
- Source: round1-advocate-1.md "Steelman of Variant 2" critique and "Suggested merge" ("add one sentence to OB-09 asking the Decision Desk layout to leave room for a sweep-facts area")
- Target: "What it costs or risks", layout-rework bullet, after "adding them later may mean reworking its layout"
- Before: "The question comes back later; if Decision Desk is designed first without sweep facts, adding them later may mean reworking its layout."
- After: same sentence, followed by "Mitigation: one sentence in OB-09 asks the Decision Desk layout to leave room for a possible sweep-facts area."
- Provenance tag: `<!-- Source: Variant 1 advocate (round1-advocate-1, "Steelman of Variant 2" critique and "Suggested merge"), final sentence merged per Change #3 -->` (plus the section tag marking the section as Base (original, modified))
- Validation: the plan gave no exact text; the sentence follows advocate 1's suggested wording. No citation added. Checked against "OB-09 condition (3) is settled for now as snapshot v1 only": a layout reservation adds no data dependency, so no contradiction.

### Change #4: Possible home for a joined view

- Status: Applied
- Source: Variant 3 (proposal-C) "What happens next" bullet 4 and "What stays unresolved"; diff point C-004 (advocate 3)
- Target: "What stays unresolved", appended as a new bullet
- Before: two bullets (whether the observer should ever show sweep facts; Q9 left at its default)
- After: new bullet "Where a person sees Orca state and sweep classes together, if anywhere. A possible home is Orchestrator v2, which is linked to sweep facts through SW-11 (merged-requirements.md line 200) but is unbuilt."
- Provenance tag: `<!-- Source: Variant 3 (proposal-C), "What happens next" bullet 4 and "What stays unresolved" (diff point C-004), merged per Change #4 -->`
- Validation: states that v2 is unbuilt, as the plan requires; merged-requirements.md line 200 confirmed by direct read (SW-11 row lists V2-04 as a dependent).

## Post-Merge Validation

### Structure

- Heading hierarchy: one H1 (title) and five H2 sections (Answer; What happens next if the owner picks it; What it unlocks; What it costs or risks; What stays unresolved), same order and levels as the base. PASS.
- Base preservation: a diff of the merged text (provenance comments removed) against the base shows exactly three added bullets and one extended bullet, matching Changes #1 to #4; no other line changed. PASS.
- Dashes: no em dashes or en dashes in the merged file. PASS.
- Provenance: header block present; a Source tag precedes every section and every inserted block. PASS.

### Internal references

- Line citations in the merged file: merged-requirements.md lines 257, 708 (base); ADJ line 779 (base); ADJ line 253 (base); ADJ line 81 (Change #2, allowed by the plan); ADJ line 361 (base); merged-requirements.md line 200 (Change #4, allowed by the plan). No other citation added. PASS.
- IDs referenced by the new text (Q17, Q19, OB-09, PR #539, XC-05, SW-11, Decision Desk, v2) all already appear in the base or in the plan. PASS.

### Contradiction re-scan against the base

- C-1 (FLAGGED, not fixed): the base bullet in "What it costs or risks", "'Not now' has no trigger written down; it may drift into 'never' without a decision.", is now contradicted by the Change #1 bullet, which writes a trigger into the ledger. The plan lists no change to this bullet, so it was left as the base has it. Escalated to the orchestrator: a follow-up plan item should either remove that bullet or reword it (for example, to say the trigger depends on Q19 and PR #539, which may never happen).
- No other contradiction found: Change #2 extends the existing report-age rule; Change #3 adds no data dependency to OB-09; Change #4 is consistent with "Whether the observer should ever show sweep facts" staying open and with the base's statement that the sweep JSON is a carrier for v2 (ADJ line 361).

## Summary

- Planned changes: 4. Applied: 4. Skipped: 0. Failed: 0.
- Structural checks and reference checks passed.
- One contradiction (C-1) introduced between Change #1 and an unchanged base bullet; left in place because the plan does not cover it, and escalated.
- Overall status: partial (all planned changes applied; contradiction C-1 needs an orchestrator decision before the merged proposal is fully consistent).

## Orchestrator resolution of C-1 (added after the merge)

- Action: the orchestrating session reworded the conflicting base bullet in merged-proposal.md to: "'Not now' could drift into 'never' without a decision; the re-ask trigger recorded in the ledger (above) is what prevents that, so the trigger must actually be written down when Q17 is answered." A provenance tag marks it as an orchestrator edit.
- Result: no remaining contradiction. Final status: success (with this recorded post-merge edit).
