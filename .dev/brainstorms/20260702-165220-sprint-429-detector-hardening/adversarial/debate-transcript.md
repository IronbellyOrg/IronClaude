# Adversarial Debate Transcript (blind)

## Metadata
- Depth: deep · Rounds completed: 2 + Round 2.5 invariant probe (Round 3 skipped: converged)
- Convergence achieved: 0.90 · Threshold: 0.75
- Focus: All · Advocates: 3 (blind A/B/C)
- Taxonomy coverage: L1 (minimal) · L2 (contract boundary, helper-vs-inline) · L3 (predicate, regex capture, FP guard, timeout interaction) — all covered

## Round 1: Advocate statements (summarized)
- **A (architect):** Frame the defect as coupling, not regex. Invert the brittle structured-field gatekeeper into a text-primary semantic contract keyed on the durable `rate_limit_error` token; demote `api_error_status` to first-evaluated fast-path so `old_match ⊆ new_match` proves Shape-1 regression-freedom by construction. Name the detection contract as a boundary with two consumers; make the shape-variant table its executable spec + drift tripwire.
- **B (refactorer):** True mandated surface = 2 hunks in one file (regex loosen + gate widen). INLINE the disjunct — reject helper/registry/strategy ceremony. Reject nested-JSON unescaping (adds a crash mode violating C6); use `"rate_limit_error" in body`. Ship the 9-item "CHANGES NOT MAKING" ledger. Demote timeout branch to a watch-item and PROVE it stays unreachable for 429s.
- **C (qa):** Size by the false-confidence surface. Centerpiece = ~12-row parametrized contract table (api_error_status × via-provider × prefix), every cell acknowledged (empty = explicit xfail). Assert `resolved_model` per row incl. `None`. Close the untested live/offline seam with 4 parity tests incl. the PASS_RECOVERED intercept. Synthesize a Shape-2 single-account breakpoint for OQ2.

## Round 2: Rebuttals (on the 3 contested points)
- **C-002 (timeout):** B's unreachability proof (every `is_error` 429 returns inside the 429 block before `:335`) is accepted as the reason the branch stays byte-unchanged; A's debt-ledger note and C's matrix-row-T1 pin are complementary guards, not competitors. Resolution: keep unchanged, add F5 unreachability test + T1 row + debt note. All harvested.
- **C-005 (Shape-2 single-account):** B's "reject speculation" and C's "synthesized fixture" reconcile: a clearly-named `_SYNTHESIZED` breakpoint documents the assumption as an executable test row (not a speculative production path), satisfying B's concern. Adopted.
- **C-003 (helper vs inline):** Uncontested — inline wins (B), no counter-argument.

## Round 2.5: Invariant probe
See `invariant-probe.md`. 6 findings, all ADDRESSED, 0 HIGH-unaddressed. Promoted assumptions A-002 (sufficiency) and A-003 (C5 scoping) yielded the two highest-value findings: INV-005 sufficiency branch-trace and INV-004 elevating C5 to load-bearing.

## Scoring matrix (per contested point)
| Diff point | Winner | Confidence | Evidence |
|---|---|---|---|
| C-001 sizing | merge (two-axis) | 90% | complementary framings; no conflict |
| C-002 timeout | merge (all 3) | 85% | B's proof + A's ledger + C's row are orthogonal guards |
| C-003 inline | B | 88% | uncontested anti-ceremony argument |
| C-004 OQ1 | B | 90% | crash-mode/C6 rationale strongest |
| C-005 OQ2 | C (+B constraint) | 82% | synthesized-as-breakpoint satisfies both |
| C-006 back-compat | A | 90% | formal old ⊆ new proof |
| C-007 table | C | 92% | concrete matrix, xfail cells |
| C-008 parity | C | 88% | names the untested seam |

## Convergence assessment
- Points resolved: 8 of 8 · Alignment: 0.90 · Threshold: 0.75 · Status: **CONVERGED**
- Unresolved points: none. No HIGH-severity unaddressed invariants (gate not blocked).
