# Merge Log: D11 observability recommendation

## Metadata

- Base variant: Variant 2 (opus:analyzer, CLAY position paper), `variant-2-original.md`
- Other variant (source of incorporated strengths): Variant 1 (opus:architect, OURS), `variant-1-original.md`
- Executor: merge-executor
- Refactoring plan: `refactor-plan.md` (10 planned changes, 6 rejected alternatives)
- Changes planned: 10
- Changes applied: 10
- Changes skipped: 0
- Changes failed: 0
- Status: COMPLETE
- Timestamp: 2026-11-20
- Merged artifact: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D11/adversarial/merged-d11-observability-recommendation.md`

## Changes Applied

### Change 1: Replace the claim paragraph
- Status: APPLIED
- Before: Base claim said the report is the work-item layer and the sweep and observer "feed or read it"; the report was kept ahead of any contract note.
- After: The sweep JSON v1 is the one source of session facts, the observer the one screen, the report the one plain-English report and work-item layer that meets issue 409 asks today; features adopted per the adoption table; "do not hold the working report behind unwritten design" kept. Three one-line reasons cite C-003, X-001 and C-002.
- Provenance tag: `<!-- Source: Variant 1 (opus:architect), Section The claim - merged per Change #1 ... -->`
- Validation: PASS. One sentence was added that the plan did not list: it points to rule 9 (the observer questions panel as the open exception to "one data source"). It adds no new fact; it keeps the claim from contradicting INV-005. Flag for the orchestrator.

### Change 2: Replace "The mechanism" with a three-layer data flow
- Status: APPLIED
- Before: Three numbered items (entry files, join and gate, nine rows and cap).
- After: A three-layer table (facts, work items, screen), the data direction (sweep to report, report to observer), base items 1 to 3 kept as "Layer 2 in detail" plus the C-001 session split, a notice-step paragraph, and an "Order of work" paragraph (X-002).
- Provenance tags: Variant 1 "The mechanism" per Change #2, and Base (original, modified) for the kept entry-file, join and gate text.
- Validation: PASS.

### Change 3: Add the section "Testable rules for the spec"
- Status: APPLIED
- Before: No such section.
- After: 12 numbered rules, each naming its finding id: 1 INV-003, 2 INV-003, 3 INV-006, 4 INV-007, 5 INV-001 (HIGH), 6 INV-002 (HIGH), 7 INV-004, 8 INV-010, 9 INV-005, 10 INV-009, 11 INV-008, 12 INV-012. Evidence paths are from the probe. UNVERIFIED items kept (which map covers more; sanitize.py on arbitrary text).
- Provenance tag: `<!-- Source: Debate evidence (invariant-probe.md, Round 2.5, INV-001 to INV-012) - merged per Change #3 -->`. This is not one of the three tag forms in the brief, because the source is the probe and not a variant.
- Validation: PASS.

### Change 4: Read-only and "recommend nothing" rules
- Status: APPLIED
- Before: Base listed the DM and commit as a risk only.
- After: Section "Read-only and recommend-nothing rules": sweep and observer carry no Options, Recommendation or write; those belong to the report or orchestrator session; observer showing entry text stays an owner decision (UNVERIFIED).
- Provenance tag: Variant 1 Section Cited facts item 3, per Change #4.
- Validation: PASS.

### Change 5: Person-specific values and naming
- Status: APPLIED
- Before: Base cost lines named the one-person config and the naming drift.
- After: Section "Person-specific values and naming": per-user config for person, time zone, ClickUp user and token and DM channel; owner naming and layout; D08 settles the name; `$AWR_ROOT` or `orchestrator_repo` still needed, so not zero-setup (A-004).
- Provenance tags: Variant 1 Section Cited facts item 4 per Change #5; Base (original, modified).
- Validation: PASS.

### Change 6: Nine-row table
- Status: APPLIED
- Before: Base: "one table of nine rows says what may reach the person".
- After: Adopted with "the person"; notice step only; sweep and observer never pick a row but may show a recorded row number; "exactly nine rows" test kept; rows 1 to 7 never low-stakes.
- Provenance tag: Variant 1 per Change #6 and #7 (shared section).
- Validation: PASS.

### Change 7: Cap of 5 notices a day
- Status: APPLIED
- Before: Base: cap "settled by ruling 39" (cited fact 6).
- After: PROPOSED default of 5 per repo per 24 hours, notices only, entries never dropped; not settled (ruling 39 is Clay's by implication, AD-B4 "not ruled on; open", parser returns 0 for an absent key, `escalate` and `asks.json` do not exist); no generator writes a value until the owner records a ruling (INV-011).
- Provenance tag: as Change 6.
- Validation: PASS. The base's "settled" claim is removed from the merged file.

### Change 8: Living report and status words
- Status: APPLIED
- Before: Base kept the living report with a fixed state path (`.dev/coordinator/orchestrated/`) and its own six status words.
- After: Section "The living report and the status words": per-user, configurable state path, model-free `refresh`; six words for work items only; session state on screen is the sweep class word for word; entry files store only `session_id`.
- Provenance tag: Base (original, modified), citing C-009, C-008 and INV-008.
- Validation: PASS.

### Change 9: Adoption table for Clay's features
- Status: APPLIED
- Before: No such table (base had a bare "adopt" statement).
- After: Six rows: living report (adopt with change), nine rows (adopt with change), cap of 5 (adopt as a proposal, not settled), silent-loss check (adopt as is, report layer), plain-English item template (adopt with change), `check.py` gate (adopt as is).
- Provenance tag: Variant 2 (CLAY) Section Final recommended merge (d), per Change #9.
- Validation: PASS.

### Change 10: Keep and extend costs and risks; add open decisions
- Status: APPLIED
- Before: Base costs (3 items) and risks (2 items, no mitigations).
- After: Costs: base items kept, plus the JSON field and golden-test edit, the two-map coverage check, the observer questions exception, the cap ruling, the contract note, the saved JSON file, the three-outputs cost. Risks: base risks kept, each with a mitigation from the plan or debate; added risks for the golden test, INV-001, INV-002, INV-004, INV-005, the cap, rule quality, and duplicate or unsafe text. New section "Open decisions for the owner": 4 questions (cap value and who rules; observer showing entry text; questions panel as exception or sweep block; where the sweep JSON lives), each with what each answer does. Cited facts merged and de-duplicated into 16 numbered items, each with its source; the two position papers' corrections (join key not in JSON, cap not settled) replace the base's cited facts 6.
- Provenance tags: Base (original, modified) and Variant 1 per Change #10.
- Validation: PASS. The consequence lines under each owner answer are restatements of plan and probe text; none adds a new fact.

## Post-Merge Validation

### Structural integrity
- Heading levels: one H1 (the title) and 12 H2 sections; no H3 or deeper, so no skipped levels. PASS.
- Section order: claim, mechanism, rules, read-only, person values, notice step, living report, adoption table, cited facts, costs, risks, open decisions, what the merge gets right. No gaps. PASS.
- Provenance: header has the three required comments; 15 `<!-- Source: ... -->` tags, at least one per section. PASS.
- Dashes: 0 em dashes and 0 en dashes in the merged file. PASS.

### Internal references
- Total references checked: 66 (26 "F N" fact references, all within the 16 facts; 25 "rule N" references, all within rules 1 to 12; 5 "open decision N" references, all within decisions 1 to 4; 10 section-name references to 7 distinct headings, all present).
- Resolved: 66
- Broken: 0

### Contradiction re-scan
- New contradictions introduced: none found.
- Points checked: the claim says "one source of session facts" and names the questions panel as the open exception (rule 9); the cap is "proposed" everywhere (claim, mechanism, notice step, adoption table, risks, owner decision 1), never "settled"; the state path is "today `.dev/coordinator/orchestrated/`" in the mechanism and `.dev/coordinators/` in the naming section, which is current state versus target, not a conflict; the six work-item words appear only for work items (section "The living report" and risks).
- Not checked: whether any cited path or line still matches the master export. The merge copies citations from the inputs and does not re-read the source tree.

### Rule checks
- All 12 rules cite their finding id: PASS (1 INV-003, 2 INV-003, 3 INV-006, 4 INV-007, 5 INV-001, 6 INV-002, 7 INV-004, 8 INV-010, 9 INV-005, 10 INV-009, 11 INV-008, 12 INV-012).
- INV-001 and INV-002 appear as rules 5 and 6, both marked HIGH: PASS.
- INV-011 is covered in the section "The notice step: nine rows and the cap" and in owner decision 1: PASS.

## Deviations to report

1. Change 1: one cross-reference sentence about the questions-panel exception was added to the claim (see Change 1).
2. Change 3: the provenance tag names the invariant probe, not a variant, because the rules come from the probe.
3. Changes 4 to 8 each became their own short H2 section, because the brief's suggested section list had no place for them. Content is the plan text only.

## Summary

- Planned: 10
- Applied: 10
- Failed: 0
- Skipped: 0
- Rejected alternatives (6) honored: none of the six non-base approaches appears in the merged file as a recommendation.
