# Invariant Probe Results — Phase 13 Pre-Validation (Round 2.5 fault-finder)

Probing the emerging consensus (mostly-KEEP-with-REFACTORs) against the 6-category checklist.

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | sufficiency_challenge | "13.5 zero-failures bar is achievable" — does running the suite ALONE green it? | UNADDRESSED→addressed-by-REFACTOR | HIGH | Verified: `uv run pytest tests/roadmap/ -k default_agents` → 3 FAILED (haiku vs sonnet), pre-existing + out-of-scope. Suite is NOT green at parent. REFACTOR to baseline-delta neutralizes. |
| INV-002 | collection_boundaries | "every RECURRENT row maps to a dispatchable component in 13.3" | UNADDRESSED→addressed-by-REFACTOR | HIGH | Rows #2,#5,#10,#12,#15,#16,#17,#21,#22 have no entry in 13.3's 6-class dispatch map. 13.3 demands "no fixture silently skipped" — contradiction unless dispatch is extensible + skip/xfail registry. |
| INV-003 | guard_conditions | "Gate #4 (≥1 fixture per row) is satisfiable for ALL 18 rows" | UNADDRESSED→addressed-by-REFACTOR | MEDIUM | Row #17 (OOM/context-window) is a runtime resource failure not resolvable by a scanner-fixture; row #21 (sprint executor) is OUT of scope per BUILD-REQUEST §Scope. DEFERRED-with-stub honors the count without fabricating scanner inputs. |
| INV-004 | state_variables | "live 38-spec run fits disk/cost budget" (13.6) | UNADDRESSED→addressed-by-REFACTOR | MEDIUM | Worktree 72% full (34G free); session hit ENOSPC; R1.3 Option B now runs real certify LLM subprocess. M5 4h/spec cap absent from 13.6 text. REFACTOR adds time+disk+cost guards + sampling fallback. |
| INV-005 | interaction_effects | "`.dev/releases/Current/` output is unambiguous" (13.6) | UNADDRESSED | LOW | Both `.dev/releases/Current` AND `.dev/releases/current` exist on disk — case-collision hazard on case-insensitive FS. REFACTOR disambiguates path. |
| INV-006 | count_divergence | "15 NEW fixtures" arithmetic | ADDRESSED | LOW | 18 RECURRENT (Gate #4) − 3 already-created (#4,#6,#9) = 15. Correct. |
| INV-007 | guard_conditions | "Contract #1 fail-pre/pass-post is verifiable in 13.3" | UNADDRESSED→addressed-by-REFACTOR | MEDIUM | No pre-fix checkout in Phase 13; fixes already landed R0/R1. The fail/pass property must be attested per-class at the landing phase; 13.3 asserts steady-state PASS + no-skip only. |
| INV-008 | sufficiency_challenge | "13.4 wires 10 contracts" — are any already wired? | ADDRESSED-by-REFACTOR | MEDIUM | Verified already-wired: Contract #5/#8 (Makefile Check 11), #2 (test_dispatch_reachability.py), #9 (test_spec_roadmap_id_containment.py), #10 (test_anti_instinct_recurrence.py), #3 (tool-write schemas). 13.4 must be "verify + fill gaps", not greenfield. |

## Summary
- Total findings: 8
- ADDRESSED: 2 (INV-006, INV-008 via REFACTOR)
- UNADDRESSED (resolved by proposed REFACTORs): 5 — INV-001(HIGH), INV-002(HIGH), INV-003(MED), INV-004(MED), INV-007(MED)
- UNADDRESSED (residual LOW): 1 — INV-005
- HIGH-severity UNADDRESSED after REFACTOR applied: 0 → convergence permitted.

The two HIGH findings (INV-001 zero-failures bar; INV-002 dispatch coverage) are the load-bearing reasons 13.5 and 13.3 are REFACTOR not KEEP.
