
## Taxonomy coverage gate (AD-5)
- L1 points debated: S-002, S-004, C-004, C-005 (covered)
- L2 points debated: S-001, S-003, C-003, X-001 (covered)
- L3 points debated: C-001, C-002, X-002, A-001, A-002, A-003, A-004 (covered)
- Result: all three levels covered after Round 1; no forced round.

## Scoring Matrix

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|-----------------|
| S-001 | none (count is not merit) | 90% | All three advocates in Round 2 rule that finding count is not merit; the surviving blocker C-001 came from V1 and V3. |
| S-002 | Variant 2 | 95% | All three name V2: `resolved_model: glm-5.3` records the alias resolution source.md:127 warns about. |
| S-003 | split: V1/V3 label "ordering" for C-001; V2 label "missing-test" for C-002 | 85% | Unanimous in Round 2; S-4 "false-claim" and Q-4 "weak-match" are both mislabels. |
| S-004 | Variant 3 | 95% | Reading the executor files (SKILL.md:135, qa.md:245-247, ledger.md:60) is what exposed C-001; V2 conceded its evidence was too narrow. |
| C-001 | Variant 3 (Variant 1 co-winner) | 98% | Blocking, unanimous; V2 conceded in Round 1. The plan's own ACs (plan:213, :223) require "blocked", so the task either passes silently (qa.md:83-87 with ledger.md:60) or halts (qa.md:245-247); Task 16 (plan:228-236) is gated. |
| C-002 | Variant 2 (classification); V1/V3 fix | 90% | Minor, unanimous after Round 2 (V1 and V3 conceded): section 20 is checks (source.md:465), deliverables are sections 15/16 (source.md:388-398), plan:15 claims no verification. |
| C-003 | Variant 1 | 85% | Minor, unanimous; rule exists at plan:22, Task 5 copies only "the gh commands" (plan:91). |
| C-004 | Variant 3 | 90% | Minor, unanimous; hunk-range check makes plan:178 observable; executor diffs against Q0 (SKILL.md:123). |
| C-005 | Variant 3 | 85% | Minor, unanimous; ASCII rule at test_how_we_work_routing_table.py:341-346 not stated at plan:159; V3 also adds the live-reference rule. |
| X-001 | Variant 1 / Variant 3 (FAIL) | 98% | Verdict FAIL, unanimous; V2 explicitly conceded its PASS. Basis: C-001 and A-001. |
| X-002 | Variant 2 | 90% | Minor, unanimous after V1 and V3 conceded: no section 15/16 deliverable is missing. |
| A-001 | REJECT (no card won; all missed) | 95% | Blocking (security), unanimous: plan:219 asks the user for the token and runs with it set; persisted in session records, contrary to plan:219 and source.md:296. |
| A-002 | QUALIFY, Variant 1 partial | 85% | Minor, unanimous after V1 conceded: invariant stated at plan:22, :91, :109; section 16 (source.md:390-398) asks for no static test. |
| A-003 | ACCEPT | 85% | Unanimous after V1 conceded and V2 changed: source.md:391 defines the static test as phrase presence; plan:121 matches. |
| A-004 | REJECT (as worded), minor | 80% | Minor unanimous; label REJECT by V2 and V3 (2/3), QUALIFY by V1. plan:55 conflicts twice with source.md:149. |

### Unique contributions (not in the convergence denominator)

| U-id | Ruling | Confidence | Evidence Summary |
|------|--------|------------|-----------------|
| U-001 | keep, minor | 90% | plan:49 says "unset" but forces nothing. Invariant probe INV-003 (HIGH) shows the A-001 fix makes an exported token the default, so this is folded into the A-001 recommendation. |
| U-002 | keep, minor | 90% | Bookkeeping only; coverage-matrix.json:8-15. |
| U-003 | keep, minor (relabel missing-requirement) | 90% | source.md:132 "every ref" vs plan:95, :109. INV-006 widens the fix to all five refs. |
| U-004 | reject | 90% | V2's own card says no plan change; no defect (V1, V2, V3 agree in Round 2). |
| U-005 | keep, minor | 90% | plan:209 needs a session restart and names no checkable model-evidence source. |
| U-006 | keep, minor (relabel spec-inherited, not false-claim) | 90% | plan:121 copies source.md:391; the model test reads source only (test_how_we_work_routing_table.py:19, :144). |
| U-007 | keep, minor | 90% | plan:198 greps local `master`. |
| U-008 | keep, minor | 90% | plan:209 and :230 act outside the plan:20 edit scope; worktree never removed. |

### Points won (Step 3 tiebreaker input)
- Variant 1: C-003, A-002 (partial), C-001 (half), X-001 (half) = 3.0
- Variant 2: S-002, C-002, X-002 = 3.0
- Variant 3: S-004, C-004, C-005, C-001 (half), X-001 (half) = 4.0
- Points with no variant winner: S-001, S-003 (split), A-001, A-003, A-004

## Convergence Assessment
- Points resolved: 15 of 15
- Alignment: 100%
- Threshold: 80%
- Taxonomy gate: all levels covered
- Invariant gate: CONVERGENCE BLOCKED: 3 HIGH-severity UNADDRESSED invariant(s) detected. Blocking items: INV-001, INV-002, INV-003. These are gaps in the consensus fixes for C-001 and A-001, not reversals of them. Depth is standard, so no Round 3 runs. The orchestrator carries all three into the refactor plan as required amendments to the merged recommendations, and lists them in the return contract's `unaddressed_invariants`.
- MEDIUM UNADDRESSED warnings: INV-004, INV-005, INV-007, INV-008, INV-009.
- Status: BLOCKED_BY_INVARIANTS
- Unresolved points: none
