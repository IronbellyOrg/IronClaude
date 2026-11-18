# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2 (Round 1 parallel, Round 2 sequential) plus Round 2.5 invariant probe; no Round 3 (depth standard)
- Convergence achieved: 88.9 percent (8 of 9 diff points; X-001 unresolved between the advocates after Round 2)
- Convergence threshold: 80 percent
- Focus areas: correctness, coverage, deviation-classification
- Advocate count: 2 (Variant 1 haiku:analyzer, Variant 2 opus:qa)
- Taxonomy coverage: L1 S-001; L2 C-001 to C-003, X-002, A-001, A-002; L3 X-001, A-003 (all levels covered)

Round texts (persisted verbatim by the orchestrator): `debate/round-1.md`, `debate/round-2-advocate-1.md`, `debate/round-2-advocate-2.md`. Invariant probe: `invariant-probe.md`. Omission check on shared assumptions: both advocates answered A-001 to A-003 in Round 1; no [OMISSION] flag.

## Scoring Matrix

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|------------------|
| S-001 | Variant 1 (weak) | 60% | Category plus blocking fields convey two facts; V2's advocate called it a wash (55 percent "both") |
| C-001 | Variant 2 | 85% | rf-qa.md:100 and :548, SPEC:853; :810 dropped, :796 minor |
| C-002 | Variant 2 | 90% | zero-trust test :95 still label-based; both advocates agree |
| C-003 | Variant 2 | 90% | S2:138 produces the M6 share that Task 2 does not count |
| X-001 | Variant 1 | 75% | SKILL.md:131 before :140, retry.md:109 and :158 leave the edit; V1's advocate withdrew in Round 2 (PLAN:20), V2's advocate and the fault-finder (INV-001) rejected the retreat |
| X-002 | Variant 2 | 90% | verdict pairs (lines 240 to 784) sit before `## Critical Rules` at rf-qa-qualitative.md:983; all agree |
| A-001 | QUALIFY | 80% | producers named, not executed |
| A-002 | REJECT | 90% | rf-qa.md:548 and :100 sit outside PLAN:140 and the S0:34 patterns |
| A-003 | REJECT | 85% | a halt leaves the edited source in the tree (retry.md:109, :158) |
| U-001 | Variant 1 | 75% | blocking, as X-001 |
| U-002 | Variant 1 | 85% | blocking; the fault-finder adds the reduced-panel threshold (INV-003) |
| U-003 | Variant 1 | 90% | minor |
| U-004 | Variant 2 (qualified) | 75% | minor: hook injects the old style into both arms; REQ-04 and Medium cadence in neither arm |
| U-005 | Variant 2 | 75% | minor |
| U-006 | Variant 2 (qualified) | 60% | minor: caught late at PLAN:192 |
| U-007 | Variant 2 | 60% | minor |
| U-008 | Variant 2 | 70% | minor: rf-qa.md:393 and rf-qa-qualitative.md:800 keep the rule |
| U-009 | Variant 2 | 85% | minor (M6; fault-finder adds M9, M11) |
| U-010 | Variant 2 | 85% | minor, folded into C-002 |
| U-011 | Variant 1 | 85% | end-point claim dropped; the hash-description part stays under X-002 |
| U-012 | Variant 2 | 80% | minor (fault-finder INV-012 raises the ledger-row gap to Medium) |

## Convergence Assessment
- Points resolved: 8 of 9 (S, C, X, A points; the 12 U points are keep-or-drop decisions, all settled)
- Alignment: 88.9%
- Threshold: 80%
- Status: BLOCKED_BY_INVARIANTS at the gate (2 HIGH UNADDRESSED: INV-001, INV-003), cleared by carrying both into the merged card as blocking findings F1 and F2
- Unresolved points: X-001 (advocates split; resolved by evidence for Variant 1's position)
