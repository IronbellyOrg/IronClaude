# Refactoring Plan: Merge into Base (Variant 3, haiku:backend)

## Overview
- **Base variant**: Variant 3 (haiku:backend), `variant-3-haiku-backend.md`
- **Incorporating from**: Variant 1 (opus:architect), Variant 2 (sonnet:analyzer)
- **Total planned changes**: 16 (11 incorporations from debate winners, 5 required changes from HIGH-severity unaddressed invariants)
- **Overall risk level**: High. The base wins on the tiebreaker, but all three advocates recommended V1's architecture as the skeleton (debate Round 2), so Change 1 restructures the whole document around V1's organization while keeping V3's integrity rules. Five HIGH invariants (INV-005, INV-006, INV-010, INV-026, INV-028) are unaddressed in every variant and must be closed by new text, not by choosing one variant's wording.
- **Hard constraints on the merged output**: five structurally distinct, full snapshot concepts (not widget alternatives); every example uses synthetic DEMO-marked data from one shared fixture table; one default recommendation with one switch rule; UI research and design content only, no product code and no new external research.

## Planned Changes

### Change 1: Restructure the document around the layer model and V1 organization (from Variant 1)
- **Source**: Variant 1 s.1-17 (organization), s.2 Architectural Model (four layers with owns / must-never)
- **Target**: Base whole document; restructure. Order: purpose and concept set, layer model, requirements, observation and data contract (V3 s.3), integrity rules (V3 s.4), frame contract, one section per concept, comparison, default, states, overflow, evaluation, limits, risks, gates.
- **Rationale**: S-001 (majority, 70%) and S-002 (unanimous, 95%) won by V1 in Round 2; all three advocates recommended V1's skeleton in Round 2; INV-030 records that the layer model does not hide integrity fields from the renderer, so V3 s.3-4 stay as their own sections.
- **Integration approach**: restructure; keep V3 s.3 and s.4 text verbatim except where Changes 12-16 modify it.
- **Risk**: High (whole-document reorder; provenance must be tracked per section).

### Change 2: Requirements catalogue with Layer, Basis and acceptance condition together (from Variants 1 and 2)
- **Source**: Variant 1 s.3.1-3.7 (Layer column, DEC/BLK/COM/CHG/VER/COV/FMT families); Variant 2 s.3 (Basis column, evidence tags)
- **Target**: Base s.2 (R01-R16); replace with one merged table whose rows carry ID, requirement, Layer, Basis and observable acceptance condition.
- **Rationale**: S-003 is UNRESOLVED after Round 2 (50% confidence); V3 Round 2 CR-4 and INV-025 (ADDRESSED) require the three attributes stay on the same row. DEC-1 (decisions first) and DEC-3 (OLDEST line mandatory) won by V1 under C-004 (95%) and X-001 (70%).
- **Integration approach**: replace; map every R01-R16 to a merged row so no V3 requirement is lost.
- **Risk**: Medium (requirement loss if mapping is incomplete).

### Change 3: Shared report frame contract and printed legend (from Variant 1)
- **Source**: Variant 1 s.4.1-4.4 (header, footer, field rules, notation, legend, stable identity)
- **Target**: Base, new section after the integrity rules; insert.
- **Rationale**: S-004 and S-011 (95%) and S-012 (70%) won by V1 in Round 2; V3 conceded it has no frame or legend (Round 2 CR-3). Must be modified by Change 15 (qualifiers in header).
- **Integration approach**: insert; the frame applies to all five concepts.
- **Risk**: Medium.

### Change 4: Concept A, Attention Brief, as the default (from Variant 1, with Variant 3 and Variant 2 content)
- **Source**: Variant 1 s.6 (Attention Brief, oldest-decision queue); Variant 3 s.5 (Decision Brief integrity content); Variant 2 s.4.1 and s.6 (ANSWERED, NOT RESOLVED band; WATCH row; SINCE strip)
- **Target**: Base s.5; replace.
- **Rationale**: C-002 (V3 concepts not visibly distinct, 80%, V3 conceded Round 2 CR-1); X-001 won by V1 (DEC-1: no worker VERIFY row above human questions); C-011 and C-008 won by V2 (95%).
- **Integration approach**: replace; repair any V1 or V3 screen that puts a non-decision row above the decision block.
- **Risk**: Medium.

### Change 5: Concept B, Ball-Holder Board (from Variant 2)
- **Source**: Variant 2 s.4.2 (C2 Ball-Holder Board, responsibility bands)
- **Target**: Base s.6 (Run Ledger); replace, keep V3 run reconciliation content as a supporting block.
- **Rationale**: C-001 won by V2, unanimous after V3 changed its vote in Round 2 (95%); A-002 won by V3: the owner field never names the relay, and a missing owner stays unknown.
- **Integration approach**: replace; mark retained V3 content `Base (original, modified)`.
- **Risk**: Medium.

### Change 6: Concept C, Root-Blocker Tree, age-ranked (from Variant 1 with Variant 3 rules)
- **Source**: Variant 1 s.8 (tree layout); Variant 3 s.7 (age-ranked roots, `dependency conflict` for cycles, union counts)
- **Target**: Base s.7; restructure.
- **Rationale**: X-002 and C-007 won by V3 (95%); X-009 won by V3 (union footer, INV-013 ADDRESSED); INV-016 ADDRESSED (cycles). Must repeat the OLDEST frame line (DEC-3).
- **Integration approach**: restructure V3 s.7 into V1's tree layout.
- **Risk**: Low.

### Change 7: Concept D, Conversation Ledger with y/n/? ladder (from Variant 1)
- **Source**: Variant 1 s.9 and s.9.1 (y/n/? transport and resolution ladder)
- **Target**: Base s.8 (Conversation Handoffs); replace.
- **Rationale**: C-015 won by V1 (95%); C-002 distinctness.
- **Integration approach**: replace; keep V3's acting-human versus requesting-worker distinction (A-002).
- **Risk**: Low.

### Change 8: Concept E, Delta Journal repaired under DEC-1 (from Variant 1 with Variant 3 rules)
- **Source**: Variant 1 s.10 (Delta Journal, CHG-3 VANISHED); Variant 3 s.4 rules 4-5 (positive-only partial additions, `newly observed`)
- **Target**: Base s.9 (Change Journal); replace.
- **Rationale**: X-006 won by V3 (DEC-1 repair needed); X-005 won by V3; C-010 won by V1. INV-018, INV-024 and INV-027 (MEDIUM) apply: VANISHED is shown only after a full read, as last-known unresolved with the capped-read qualifier, never as a resolution; partial reads produce only `newly observed` additions; an item first seen after the cap window moves is labelled `newly observed`, not `new`.
- **Integration approach**: replace.
- **Risk**: Medium (delta semantics).

### Change 9: Shared fixture table, overflow screen and concept x state matrix (from Variant 2)
- **Source**: Variant 2 s.2.6 (fixture world), s.7.1 (19-decision overflow with arithmetic), s.8 (concepts x states)
- **Target**: Base s.10; insert fixture table before the concepts; replace overflow screen; append matrix after the four states.
- **Rationale**: S-005, S-006, S-007 won by V2 (95%); C-016 won by V2 (hard budget), with V3 whole-bundle accounting (rules 7-9). INV-011 (MEDIUM): print omitted counts in whole bundles and label observed as `observed (census unknown)`, never as a total. Fixture identifiers become DEMO-marked per C-020.
- **Integration approach**: insert / replace / append.
- **Risk**: Medium (arithmetic must match the fixture).

### Change 10: Comparison, data dependency, default and one switch rule (from Variants 1 and 2)
- **Source**: Variant 1 s.11.1-11.2 (comparison ratings, data-dependency table); Variant 2 s.6 and s.9.3 (hybrid default, switch rule)
- **Target**: Base s.10 default; replace.
- **Rationale**: S-008 won by V1 (70%); C-003 won by V2 (95%). INV-020 (MEDIUM): one reconciled switch rule only; whichever concept is default must keep the frame and OLDEST line.
- **Integration approach**: replace. Default: Concept A with the SINCE strip; switch to E only if the evaluation decision rule shows it ties on the oldest-decision task and wins on change recall.
- **Risk**: Low.

### Change 11: Evaluation, contract cases and gate table (from Variants 2 and 3)
- **Source**: Variant 2 s.9.1-9.3 (reader tasks, mechanical checks, decision rule), s.12.1 (gate table, FG-8 Cannot-ship); Variant 3 s.11 (future contract cases)
- **Target**: Base s.11-12; restructure.
- **Rationale**: S-009, C-018, S-010, C-019 won by V2; INV-029 ADDRESSED (V1 CR-9 gate semantics: gates block shipping, not design exploration).
- **Integration approach**: restructure; must apply Change 13 to MC-4.
- **Risk**: Low.

### Change 12: Classification rule with a visible fallback (required by INV-005, HIGH)
- **Source**: New text required by invariant-probe.md INV-005 (no variant addresses it); constrained by V1 COM-4, V2 R-COM-04
- **Target**: Base s.3 Logical records and requirements; insert.
- **Rationale**: A-001 promoted shared assumption; a decision misclassified as routine is hidden.
- **Integration approach**: insert a rule: a message becomes a heartbeat only when it matches an explicit routine form; anything not positively matched is shown as `unclassified` in the decision block and is eligible for OLDEST. Add an open gate for the classifier evidence.
- **Risk**: Medium (may add noise; noise is preferred to a hidden decision).

### Change 13: Remove every conditional all-clear (required by INV-006, HIGH)
- **Source**: Base V3 s.10 scope-qualified empty state (X-004 winner); modifies Variant 2 R-INT-01 and MC-4, Variant 1 COV-4
- **Target**: merged requirements, evaluation checks and every concept; replace.
- **Rationale**: X-004 won by V3; INV-006 found MC-4 still validates a conditional all-clear and COV-4 still permits one outside the default.
- **Integration approach**: no concept in any state prints a fleet-wide all-clear; the empty state reads `no attention items observed in <scope>` with coverage and census qualifiers; MC-4 is rewritten to check for the absence of any all-clear text.
- **Risk**: Low.

### Change 14: One reconciled line and column budget; truncation makes the report invalid (required by INV-010, HIGH)
- **Source**: Variant 2 R-FMT-03 (60 lines, C-016 winner), Variant 1 OVF-8 (about 40), Variant 3 rule 7 (44, yields to a complete question); INV-012 (LOW, columns)
- **Target**: merged FMT requirements and overflow section; replace.
- **Rationale**: A-003 (one paste fits the chat limit) is UNRESOLVED; budgets conflict.
- **Integration approach**: state one hard line budget and one column width with the wrap margin; the oldest complete question may exceed it (V3 rule 7, INV-014 ADDRESSED) and the report then says so; the transport limit is an open gate; a paste missing its end marker is invalid.
- **Risk**: Medium.

### Change 15: Coverage, census and omitted qualifiers in the header (required by INV-028, HIGH)
- **Source**: Variant 1 s.4.1 footer fields; Variant 3 s.10 empty state
- **Target**: frame contract from Change 3; modify.
- **Rationale**: a split, truncated or stale paste loses the footer, leaving an unqualified empty or partial report.
- **Integration approach**: move coverage, census and omitted counts into the header; the footer repeats them with an end marker; add a report sequence or as-of identity line so an older paste is recognizable (INV-003, MEDIUM).
- **Risk**: Low.

### Change 16: OLDEST is `oldest observed`, with a paging gate (required by INV-026, HIGH)
- **Source**: Base V3 s.3 source capabilities (100-message cap, census unknown); Variant 1 DEC-3 and s.4.2 OLDEST
- **Target**: frame contract and data contract; modify.
- **Rationale**: the 100-message non-consuming peek has no paging or cursor, so the true oldest decision can sit outside the window on every run.
- **Integration approach**: OLDEST is labelled `oldest observed` whenever the census is unknown; add a gate requiring paging or a cursor before any claim of the oldest decision; tie to Change 12 so unclassified items are ranked. Also define the sort position of unknown-age, `seen>=` and `clock conflict` items (INV-007, MEDIUM): they print above known-age items with their age qualifier.
- **Risk**: Medium.

### Open questions carried into the merged output (MEDIUM invariants)
The merged output must list these as open questions or explicit rules, not drop them: INV-001 (partial-read pointer and duplicate `new`), INV-002 (first-run, empty-store state), INV-004 (uncertain-identity candidates), INV-021 (whether ANSWERED NOT RESOLVED items count for DEC-1 and OLDEST), INV-022 (WATCH clock uses evidence time, not collection time), INV-023 (redaction changes meaning; tell the reader). LOW items INV-009, INV-015, INV-017 may be recorded as limits.

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|-----------|-------------------|---------------------------|
| C-005, X-007 | V1 orders by age without pinning the oldest under overrides | V3 won (95%): oldest pointer is kept on any override (rule 2), within DEC-1 ordering per X-001 |
| C-006, X-003 | V1/V2 treat a page under the cap as a complete history | V3 won: census stays `unknown` independent of worker coverage |
| C-009 | V1/V2 infer resolution from disappearance | V3 won: last-known unresolved until explicit resolution (rule 3) |
| C-012, X-004 | V1/V2 conditional fleet-wide all-clear | V3 won; reinforced by Change 13 |
| C-013 | V1/V2 summarize stale state | V3 won: full last-known bundles under a not-confirmed-current banner |
| C-014 | V1/V2 merge failure kinds | V3 won: distinct unavailable / stale / mismatched / failed labels |
| C-017 | V1/V2 allow paraphrase of questions | V3 won: exact question text with marked redaction (rule 10); INV-023 open question |
| A-002 | V2 names the relay as owner | V3 won: acting human distinct from requesting worker; missing owner stays unknown |
| A-004 | V1 assumes the latest paste is the one read | V3 won; Change 15 adds the identity line |
| S-003 | Pick one of Layer, Basis or acceptance condition | UNRESOLVED; all three kept together (Change 2) |
| A-003 | Assume one paste fits the transport limit | UNRESOLVED; open gate (Change 14) |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|-----------------|----------|
| 1 | High | Integrity rules lost or duplicated during reorder | Revert to V3 order and insert V1 sections only |
| 2 | Medium | A V3 requirement is dropped | Re-add missing R-rows from V3 s.2 |
| 3 | Medium | Concepts render inconsistent headers | Revert to per-concept headers |
| 4 | Medium | Non-decision row above decisions (violates DEC-1) | Revert screen to V1 s.6 order |
| 5 | Medium | Responsibility axis loses run reconciliation | Restore V3 s.6 as supporting block |
| 6 | Low | Cycle items lose grouping | Restore V3 s.7 text |
| 7 | Low | Ladder drops acting-human distinction | Restore V3 s.8 field |
| 8 | Medium | Partial reads emit negative deltas | Restrict E to V3 rules 4-5 only |
| 9 | Medium | Overflow arithmetic does not match fixture | Recompute from fixture table |
| 10 | Low | Two switch rules remain | Keep V2 s.9.3 rule only |
| 11 | Low | MC-4 still validates all-clear | Apply Change 13 text |
| 12 | Medium | Noise from unclassified rows | Keep rule; tune routine forms via gate |
| 13 | Low | Some screen keeps all-clear wording | Search-and-replace check in merge log |
| 14 | Medium | Budget conflicts with complete-question rule | Keep V3 rule 7 precedence statement |
| 15 | Low | Header overflows line budget | Shorten footer, keep header |
| 16 | Medium | OLDEST wording inconsistent across concepts | Frame-level definition only |

## Review Status
- [x] Auto-approved (non-interactive mode)
- **Approved by**: auto
- **Timestamp**: 2026-11-05T20:15:00Z
