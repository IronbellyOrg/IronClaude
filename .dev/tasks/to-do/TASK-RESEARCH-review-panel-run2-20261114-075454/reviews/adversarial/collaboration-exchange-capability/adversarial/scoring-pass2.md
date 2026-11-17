# Base Selection Scoring, Pass 2 (reverse order: Variant B first, then Variant A)

Slot C-12 (collaboration-exchange-capability). Variant A = `variant-1-original.md` (Proposal A, static kit, exchange deferred). Variant B = `variant-2-original.md` (Proposal B, dormant exchange transport built now). Scored as written; the debate is used only as evidence of which claims are right or wrong. Evidence pin: E2 tip `6c09843...`; `c44c98a77` facts are [POST-BASELINE] and not penalised.

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant B | Variant A |
|---|---|---|---|
| RC | 0.30 | 0.9333 (14/15) | 1.0000 (15/15) |
| IC | 0.25 | 0.9706 (1 - 2/68) | 0.9600 (1 - 3/75) |
| SR | 0.15 | 0.9500 (38/40) | 0.9500 (38/40) |
| DC | 0.15 | 0.9231 (12/13) | 0.9474 (18/19) |
| SC | 0.15 | 1.0000 (9 H2 / 9) | 1.0000 (9 H2 / 9) |
| **quant_score** | | **0.9536** | **0.9746** |

### Counts behind the metrics

- **RC.** Items 1-8 (position, design consequence, evidence, consistency C-01..03, invariants, test, PR/rf-qa effect, objection): B sections 1, 2, 3, 4, 5, 6, 7, 8; A sections 1, 3, 4, 2, 5, 6, 7, 8. Items 9-15 for B: 9 (3.D quote of "may beat every exchange design"), 10 (3.D, +59 percent, 281.567 s vs 179.561/174.274 s), 11 **not addressed** (B only mentions "act rate" in 4 and 6.7; no 0 to 1.0 range or probe disagreement), 12 (0), 13 (0 and 3.D), 14 (2.8, 3.B, 3.C, 5), 15 (1 and 3.C). B = 14/15. A: 9 (E1), 10 (4.2), 11 (E6: luna r2 4/5 and 5/5, r4 0 and 0.4, r5 1/5 and 3/5, ember 0/4 and 0/5), 12 (4.2 last bullet quotes and answers it), 13 (E3), 14 (E5, 4.4), 15 (3.3, E10). A = 15/15.
- **IC.** Scorable claims = numbered items plus bulleted claims plus table rows. B: 4 (section 1 claims) + 8 (section 2) + 22 (section 3 bullets A-F) + 3 (section 0 stale checks) + 3 (section 4) + 12 (section 5) + 8 (section 6) + 3 (section 7) + 5 (section 8 answers) = 68. A: 1 + 4 + 6 + 2 + 6 + 2 + 12 (E1-E12) + 7 + 5 + 1 + 12 + 7 + 3 + 7 = 75. Contradictions B (2): (1) 2.2 "registered ... in hooks.json" vs 2.2/2.4 arguments baked into per-session `--settings` and "off emits no --settings"; (2) 1 and 5 "off cost is zero by construction" vs 2.2 "one installed hook script" shipped to every install. Contradictions A (3): (1) 4.2 "no exchange arm has a matching control row" vs its own 4.3 counted rows against the same-harness baseline; (2) 3.3 and 5 "H1 reaches reflect through the brief, no call-site change, no change to `cli/reflect`" vs the fact that reflect's brief builder does not carry the spec path (INV-005, HIGH); (3) 3.4 "adding the core element changes no pinned result" and 6.4 "brief bytes with kit off equal today's brief" vs 3.4/6.5 "briefs H1 already changes" (INV-004).
- **SR.** Method: first 40 substantive sentences after the section headings in document order (lead-in lines such as "B claims four narrower things" skipped). B vague (2): 0 "Both are recorded script results, not re-run here"; 3.B "Two packages written separately agree". A vague (2): 1 "Reviewers stay independent and blind"; 2 "This proposal agrees with all three outcomes". All others carry a number, path, line cite, hash or named entity.
- **DC.** Internal references only (section refs, test numbers, E-ids, defined labels; other slots, MR requirement ids R-21..R-25 and research files are external and excluded). B: 12 internal refs (0 to 3.E/3.F/3.B, 4 to 2.5, 3.C "A above" and "B above", 3.D to 0, 5 to 2.3 and 3.C, 7 to 5, 8 to 3.D and "test 1"), all resolve, plus 1 unresolved label ("H1/H2" in section 1 is never defined in B) = 12/13. A: 18 internal refs (1 to 3.4, 2 to 3.1 item 2, 3.1 to 3.3, 3.3 to 3.4, 3.4 and 4.2 and 4.3 to section 6, 4.4 to E8 and E10, 5 to 3.4, 6.1 to "claim E2 in 4.1", 6.7/7 to Measurement 1, 7 to 3.2, 8 to 3.1 items 1 and 2 and "section 6 point 1", INV-label rows), all resolve, plus 1 unresolved label ("A1" used in 4.2 and 6.1, never defined) = 18/19.
- **SC.** `^## ` lines: B 9, A 9; max 9; both 1.0.

`quant_B = 0.30(0.9333) + 0.25(0.9706) + 0.15(0.95) + 0.15(0.9231) + 0.15(1.0) = 0.9536`
`quant_A = 0.30(1.0) + 0.25(0.96) + 0.15(0.95) + 0.15(0.9474) + 0.15(1.0) = 0.9746`

## Qualitative Scoring (50% weight)

Each cell: verdict, then the one-line CEV evidence (claim = criterion met in that variant; N = NOT MET, M = MET).

### Completeness

| # | Criterion | B | B evidence | A | A evidence |
|---|---|---|---|---|---|
| 1 | Covers all explicit requirements | N | 14/15 RC items; act-rate range across probes (item 11) absent | M | 15/15 RC items; E6 act-rate table, E1, 4.2, E3, E5 |
| 2 | Edge cases and failure scenarios | M | 6.4 fault injection (corrupt board line, missing transcript, lock timeout); 3.F r2 smoke delivered nothing | M | E7 (F7 arm not run), E8 (`phase2_timeout` 1), E9 (hang kill, quarantined row) |
| 3 | Dependencies and prerequisites | M | 2.3 and 8 last bullet depend on slot C-07 launcher; 4 needs C-08 | M | 2 table column "Dependency or residue" (C-01 INV-003, C-03 INV-006/007), 3.4 X-13 |
| 4 | Success/completion criteria | M | 6 tests 1-3 each say "B is wrong if ..."; 6.7 "fewer than half of the cells" | M | 6.1 "wrong if an exchange arm beats A2 ... right if none does"; 6.2, 6.4 |
| 5 | Out of scope | M | 1 boundary: model-authored F4/F7 writers not in core; 2.6 and 2.7 no reflect/ledger change | M | 3.2 "What the core does not build now" lists hook, board, seal, registry, alarms |
| | **Subtotal** | **4/5** | | **5/5** | |

### Correctness

| # | Criterion | B | B evidence | A | A evidence |
|---|---|---|---|---|---|
| 1 | No factual errors | N | 2.2 "registered in hooks.json" is a defect (global `PostToolUse` registry, hooks.json:136); "off cost zero" ignores the installed script | N | 4.4 "`--resume` on gateway ids is not evidenced" is stale at the pinned tip (r5 NOTES:23-30, r2 RESULTS:8-14 record S2 PASS); 8 "tens to ~150 ms" mixes unverified r4 figures |
| 2 | Feasible with stated constraints | M | 2.3-2.4 new adapter outside the pinned `ClaudeProcess` (process.py:149-152); 8 states the C-07 fallback | N | 3.3 "H1 through the reflect brief, no call-site change" is infeasible without a `cli/reflect` edit (INV-005 HIGH); H2 vs pins at test_review_findings:113,117 (INV-009 HIGH) |
| 3 | Terminology consistent | M | exchange/switch/off state, F-family kinds, A1/A2 used the same way in 1, 2.4, 5, 6 | N | "E2" means both the study and claim row E2 (6.1 "claim E2 in 4.1"); "matching control" shifts meaning between 4.2 and 4.3 |
| 4 | No internal contradictions | N | 2 found (hooks.json vs per-session settings; zero-cost vs installed script) | N | 3 found (matching control; reflect no-change vs H1; brief bytes vs H1) |
| 5 | Claims supported by evidence | M | section 3 file:line with tags; 3.B recorded lines; 3.D row ids for the +59 percent | M | 4.1 table of 12 rows with evidence and tag; 4.2 row values |
| | **Subtotal** | **3/5** | | **1/5** | |

### Structure

| # | Criterion | B | B evidence | A | A evidence |
|---|---|---|---|---|---|
| 1 | Logical ordering | M | 0 conventions, 1 position, 2 design, 3 evidence, 4 consistency, 5 invariants, 6 test, 7 effect, 8 objection (brief order) | M | 0 legend, 1 position, 2 consistency, 3 design, 4 evidence ...; forward refs "see 3.4" are minor |
| 2 | Consistent hierarchy | M | H3 only inside 3 (A-F); no orphans | M | H3 only inside 3 (3.1-3.4) and 4 (4.1-4.4) |
| 3 | Separation of concerns | M | [POST-BASELINE] isolated in 3.F; consistency 4, invariants 5, tests 6 separate | M | evidence 4, invariants 5 (preserved/endangered tables), tests 6 separate |
| 4 | Navigation aids | M | section 0 legend with `BP`/`MR` keys, "(section 3.B)", "(test 1)" cross-refs | M | E1-E12 ids, "3.1 item 2" cross-refs, section 0 key |
| 5 | Artifact conventions | M | all 8 required position-paper elements as sections 1-8; Status lines | M | all 8 required elements present (sections 1-8); Status lines |
| | **Subtotal** | **5/5** | | **5/5** | |

### Clarity

| # | Criterion | B | B evidence | A | A evidence |
|---|---|---|---|---|---|
| 1 | Unambiguous language | N | 2.1 "for example `exchange/`"; 5 "would likely cost more ... [UNVERIFIED]" | N | 6.2 "a cap the module owner states" (no number); 3.4 "first candidates for `on`" |
| 2 | Concrete not abstract | M | 600-byte cap, forbidden keys list, 8 numbered tests, file:line | M | E1-E12 with line cites, 4.2 computed means, 7 numbered measurements |
| 3 | Section purpose | M | each section maps to one brief element, named in its heading | M | same; 3.1/3.2 split "now" vs "not now" |
| 4 | Terms defined on first use | N | "H1/H2" used in section 1 without definition; "R-21..R-25" uninterpreted | M | H1-H4 defined in 1; `k` defined at 4.3; s06/r09 keyed in 0 (minor gap: "A1") |
| 5 | Actionable decision points | M | 6 tests with pass/fail conditions; 8 concession "B shrinks if C-07 yields no launcher" | M | 6 measurements; 7 "What would change this" |
| | **Subtotal** | **3/5** | | **4/5** | |

### Risk Coverage

| # | Criterion | B | B evidence | A | A evidence |
|---|---|---|---|---|---|
| 1 | At least 3 risks with probability and impact | N | 5 lists 6 endangered items with impact text but no probability assessment | N | 5 lists 4 endangered items with mitigations; no probability assessment (INV-G tagged HIGH only in the preserved table) |
| 2 | Mitigation for each risk | N | 5: INV-G read-only risk has none ("delivery to a mechanically read-only reviewer is UNVERIFIED", pushed to C-07) | M | 5: lint test for INV-G, `kit: off` for INV-L/A, `verify-sync` for INV-K, per-module cap in 6.2 for cost |
| 3 | Failure modes and recovery | M | 6.4 and 3.A: seal fails closed, review fails open; 8 fallback if no launcher | M | 3.4 `kit: off` default for pinned modules; 3.1 item 2 re-ask needs served-model check; 8 answer 2 bounded retrofit |
| 4 | External dependencies | M | 2.3/8 launcher C-07; 4 served model (C-08); 3.B gateway ids not in official docs | M | 2 table (C-01 INV-003, C-03 INV-006/007); 8 answer 2 unverified runtime facts |
| 5 | Monitoring/validation | M | 6.5 latency suite, `collab` record counts, 6.8 echo/independence alarms | M | 6.4 off-state equality, 6.5 brief lint, 6.7 hold-out control |
| | **Subtotal** | **3/5** | | **4/5** | |

### Invariant & Edge Case Coverage

| # | Criterion | B | B evidence | A | A evidence |
|---|---|---|---|---|---|
| 1 | Collection boundaries | M | 2.1 600-byte cap; 2.7 one-reviewer re-review round; 6.5 "at least 30 calls" | M | 3.1 item 2 anchor >200 / claim >300 limits; 2 re-review panel is one reviewer |
| 2 | State interactions across boundaries | M | 2.5 sidecar keyed by reviewer and finding id; 4 C-02 quorum counts over own-origin lines | M | 2 table: sidecar vs open key, `origin` name collision, clearing record free of peer influence |
| 3 | Guard condition gaps | M | 2.1 forbidden verdict keys; 3.A r2 hook lacks `agent_id` branch; seal fails closed | M | 3.1 item 6 key refused until registered; 5/6.5 brief lint for read-only lanes |
| 4 | Count divergence | N | 3.E checks the 36-test count only; no off-by-one case (600-byte boundary untested, no adversarial-anchor test) | M | 2 pins at 201/301; 4.3 test counts 103/163/89/90/82 vs reported 138/358/89/106/108 |
| 5 | Interaction effects | M | 4 and 5: exchange x C-02 quorum, x re-review rounds, x INV-L shadow, x untrusted PR anchors | M | 2 table: peer finding not an independent vote under C-03 union/quorum; kit x pinned reflect bytes (3.4, 5) |
| | **Subtotal** | **4/5** | | **5/5** | |

### Edge Case Floor

B 4/5, A 5/5; both at or above the 1/5 floor; both eligible.

### Qualitative Summary

| Dimension | Variant B | Variant A |
|---|---|---|
| Completeness | 4/5 | 5/5 |
| Correctness | 3/5 | 1/5 |
| Structure | 5/5 | 5/5 |
| Clarity | 3/5 | 4/5 |
| Risk Coverage | 3/5 | 4/5 |
| Invariant & Edge Case | 4/5 | 5/5 |
| **qual_score** | **22/30 = 0.7333** | **24/30 = 0.8000** |

A's lower Correctness subtotal is driven by two debate-established defects that appear as written: a stale evidence claim (`--resume` not evidenced) and an infeasible no-change route for H1 into reflect. B's is driven by the hooks.json wording and the "off is free" claim.

## Combined Scoring

| Variant | Quant x0.50 | Qual x0.50 | **Final** | Debate tiebreaker |
|---|---|---|---|---|
| B | 0.4768 | 0.3667 | **0.8435** | 5 of 25 points (20%) |
| A | 0.4873 | 0.4000 | **0.8873** | 12 of 25 points (48%) |

**Margin**: 0.0438 (4.38 percent), below the 5 percent threshold. **Tiebreaker applied**: yes. Level 1 (debate winner tally A 12, B 5, Merge 2, Tie 2, Unresolved 1): A won more points, and 48 percent against 20 percent is not tied, so A is selected at level 1. Level 2 is not reached; for the record, correctness count would favour B (3/5 against 1/5).

RESULT_PASS2: quant_A=0.9746 quant_B=0.9536 qual_A=24/30 qual_B=22/30 combined_A=0.8873 combined_B=0.8435 floor_A=5/5 floor_B=4/5

A: MMMMMNNNNMMMMMMNMMMMNMMMMMMMMM
B: NMMMMNMMNMMMMMMNMMNMNNMMMMMMNM
