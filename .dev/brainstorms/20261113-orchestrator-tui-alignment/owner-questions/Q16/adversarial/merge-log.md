# Merge Log: Q16 (base Variant 3, proposal-C)

## Metadata

- Pipeline step: sc:adversarial Step 5 (merge execution)
- Merge date: 2026-11-14
- Base: Variant 3, `Q16/proposal-C.md` (same as `adversarial/variant-3-original.md` except one corrected line citation: OB-09 at line 257)
- Plan: `Q16/adversarial/refactor-plan.md` (4 planned changes, all additive, approved auto, non-interactive)
- Supporting evidence read: `variant-1-original.md`, `variant-2-original.md`, `round1-advocate-2.md`, `round1-advocate-3.md`
- Output: `Q16/merged-proposal.md`
- Changes applied: 4 of 4; skipped: 0; escalated: 0

## Changes Applied

### Change #1: Re-ask checkpoint at the trust layer

- Status: APPLIED
- Source: Variant 1 (proposal-A), "What happens next" bullet 4; diff point U-001
- Target: "What happens next if the owner picks it", new last bullet
- Before: section ended with the OB-09 bullet ("Release 3 of the observer (OB-09) later audits every answer path in that vocabulary (line 257).")
- After: last bullet reads "When SW-12's Phase 4 row is opened, the owner re-confirms this narrow promise with the draft vocabulary in view. This is a checkpoint only; no work is held until then." The second sentence reflects the plan's own note (Changes NOT Being Made, row C-004) that Change 1 keeps the re-ask without Variant 1's hold.
- Provenance tag: `<!-- Source: Variant 1 (proposal-A), "What happens next" bullet 4, diff point U-001; merged per Change #1 -->`
- Validation: PASS. Bullet is the last in the section as the plan requires; no new citation added.

### Change #2: One owner and no second vocabulary

- Status: APPLIED
- Source: Variant 2 (proposal-B), "What it unlocks" bullet 2; diff point U-002 (review 03 Edit 7 idea)
- Target: "What happens next if the owner picks it", appended
- Before: no statement of a single owner or a bar on a second vocabulary or audit format
- After: "The vocabulary and the audit format have one owner, the SW-12 Phase 4 row, and no other issue defines a second vocabulary or audit format."
- Provenance tag: `<!-- Source: Variant 2 (proposal-B), "What it unlocks" bullet 2, diff point U-002; merged per Change #2 -->`
- Validation: PASS. Ordering note: Change 1 asks for a "new last bullet" and Change 2 for an "append" to the same section. To satisfy both, Change 2's bullet sits after the base bullets and directly before Change 1's bullet. Both are still appended after all base content; no base bullet moved.

### Change #3: Per-program meaning of each term

- Status: APPLIED
- Source: `round1-advocate-2.md` "Overall"; `round1-advocate-3.md` "Concessions"
- Target: "What it costs or risks", directly after the "A shared vocabulary can hide real differences" bullet
- Before: the hidden-differences risk was stated with no mitigation
- After: "Mitigation: when SW-12 Phase 4 defines the vocabulary, each term states what it actually enforces in each program, so the shared audit record does not suggest equal protection where there is none."
- Provenance tag: `<!-- Source: round1-advocate-2.md "Overall" and round1-advocate-3.md "Concessions"; merged per Change #3 -->`
- Validation: PASS. Placed at the plan's integration point; no new citation added.

### Change #4: Audit records are untrusted input

- Status: APPLIED
- Source: `round1-advocate-3.md` "Concessions" (shared injection target; TB-UNTRUSTED, merged-requirements line 632)
- Target: "What it costs or risks", new bullet at the end of the section
- Before: section ended with the relay bullet ("It does not authorize relay (merged-requirements.md line 574); v2 relay still needs its own decision.")
- After: "One shared audit format is also a shared injection target. Audit records can carry text from issues, sessions or another program, so they are untrusted input (TB-UNTRUSTED, merged-requirements.md line 632), and every program that reads them must re-sanitise them."
- Provenance tag: `<!-- Source: round1-advocate-3.md "Concessions" (shared injection target); merged per Change #4 -->`
- Validation: PASS. The only new citation (line 632) is the one named in the plan. The TB-RELAY citation (line 637) from the advocate text was not carried over, because the plan does not list it.

## Post-Merge Validation

### Structural integrity

- Heading hierarchy: PASS. One H1 (title) and the base's five H2 sections in the base order: Answer; What happens next if the owner picks it; What it unlocks; What it costs or risks; What stays unresolved. No heading levels skipped, no sections added or removed.
- Base text preserved: PASS. Removing the provenance comments and diffing against `proposal-C.md` shows only the four inserted bullets (plus the blank line after the header block). No base line was changed or deleted.
- Provenance: PASS. Header block (Provenance, Base, Merge date) present; one Source tag before the title, each of the five sections, and each of the four inserted bullets. The two modified sections carry "Base (original, modified)" with a reason.
- Style: PASS. Plain English; no em dashes or en dashes found by a character scan.

### Internal references

- Line citations in the merged file: 456, 257, 89, 574 (all from the base) and 632 (from the plan). No other new line numbers. Lines 201 and 830, allowed by the plan, were not needed and are not used.
- Identifiers used by the inserted bullets (SW-12, Phase 4, TB-UNTRUSTED) all appear in the base or in the plan's cited sources. "SW-12's Phase 4 row" and "the SW-12 Phase 4 row" refer to the same row the base names in bullet 4 ("SW-12's Phase 4 (trust layer) row in #534").
- Result: PASS. No dangling references.

### Contradiction re-scan against the base

- Change 1 vs base: the base commits the vocabulary now; the re-ask re-confirms it later and holds no work, so it does not reintroduce Variant 1's hold on V2-03, V2-04, OB-09 or SW-12 Phase 4. No contradiction.
- Change 2 vs base bullet 4: the base assigns definition of the vocabulary to the SW-12 Phase 4 row (PLAN INFERENCE); Change 2 names the same row as the single owner. Consistent. Change 2 bars a second vocabulary, not a second mechanism, so it does not conflict with the Answer ("Each consumer keeps the trust mechanism its own threat model needs").
- Change 3 vs base "What stays unresolved": the terms still wait for SW-12 Phase 4; the mitigation only sets a rule for when they are defined. Consistent.
- Change 4 vs base "What it unlocks" bullet 3 (one audit format readable side by side): Change 4 adds a reader duty to re-sanitise; it qualifies, but does not contradict, the side-by-side benefit. It also fits the base's separate poisoned-content rule (V2-04).
- Result: PASS. No new contradictions found.

## Summary

All 4 planned changes were applied to the base exactly at their integration points, each with a provenance tag. The merged proposal keeps the base's five sections and all of its original text, adds one plan-approved citation (merged-requirements.md line 632), and passes the structural, reference and contradiction checks. One ordering ambiguity between Changes 1 and 2 was resolved by keeping Change 1's bullet last, as its integration point requires. Status: success.
