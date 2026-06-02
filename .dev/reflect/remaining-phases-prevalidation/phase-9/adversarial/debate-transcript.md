# Adversarial Debate Transcript — Phase 9 Unchecked Items

## Metadata
- Depth: standard (Round 1 parallel + Round 2 rebuttal + Round 2.5 invariant probe)
- Advocates: opus:architect, sonnet:analyzer, haiku:qa
- Convergence: ~100% on verdicts (3×REFACTOR, 1×KEEP); divergences additive
- Threshold: 0.80 → exceeded

## Round 1 — positions (steelmanned)
All three independently reached: 9.11 REFACTOR, 9.12 REFACTOR, PG9.1 REFACTOR(light), PG9.2 KEEP. Steelman of the DISCARD position for each item was attempted and rejected:
- **DISCARD 9.11?** Steelman: "§3 tool-write at every step is gold-plating; markdown works." Rejected: §R1 acceptance requires Contracts 1–10 CI-enforced and the generator-side constraint is the master:§Flaw 2 fix — secondary LLM steps producing IDs (certify verdicts, reflect findings) still benefit. Not gold-plating. KEEP-the-work, REFACTOR-the-text.
- **DISCARD 9.12?** Steelman: "a cutover that can't happen in-task is pure ceremony." Rejected: the *initial decision doc + deferral* is a real, needed artifact (it records the dual-write contract and prevents premature R1.6 deletion). The ceremony is only in the "track live releases" framing → REFACTOR not DISCARD.
- **DISCARD PG9.1/PG9.2?** Steelman: "interim QA after 9.5/9.10 already covers it." Rejected: terminal cumulative gate is distinct from incremental checkpoints; halt-precedence cadence wants both. KEEP gates.

## Round 2 — rebuttals
- **analyzer → architect (X-001 20-options):** The 30-option count is real but the QA-accepted precedent (8 tool-write flags landed across 9.2–9.9, passed PG8 + interim QA) establishes "additive flags ≠ violating the 20-option PRESERVE invariant." architect concedes: surface it as a NOTE, not a blocker. The invariant protects the *20 pre-existing* options' semantics, which are unchanged.
- **qa → all (remediate parity):** Reinforced C-003 with a testability proof — a file-edit prompt has no renderable artifact, so a "parity test" comparing rendered-vs-markdown is ill-defined; the only coherent parity is prompt-string byte-identity, and there is NO roadmap_ids to assert. This *strengthens* C-003: remediate is parity-only and Contract #3 does NOT apply to it. All concede.
- **architect → analyzer (4-list vs 4-list):** Agreed the body's {test_strategy,certify,reflect,remediate} vs H4's {…,parity-test} is a true contradiction; merge to a/b/c/d/e (4 migrations + 1 consolidated parity test).

## Round 2.5 — Invariant Probe (fault-finder)

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | guard_conditions | §3 roadmap_ids constraint applies to "remediate" | UNADDRESSED→now ADDRESSED | HIGH | remediate_prompts.py:17 produces file edits, no roadmap_ids; C-003 reassigns constraint to roadmap-producing remediate surface or none |
| INV-002 | count_divergence | "12 sub-steps" is the correct denominator for cutover/PG9.1 | UNADDRESSED→ADDRESSED | HIGH | as-built = 8 done + wiring-exempt + 4 secondary; only 11 carry schema+template+parity; yaml has 13 entries → reconcile to "11 genuine + wiring exempt + remediate parity-only" |
| INV-003 | interaction_effects | 9.12 can complete while depending on future release cycles | UNADDRESSED→ADDRESSED | MEDIUM | re-scope to initial-state doc + deferral; sequence after 9.11 so validation-txt glob is complete |
| INV-004 | state_variables | certify tool-write wires through _build_steps | UNADDRESSED→ADDRESSED | MEDIUM | Step 8.3 finding: certify is dynamically constructed post-remediate in execute_roadmap, NOT a _build_steps literal; tool-write must follow that path |
| INV-005 | collection_boundaries | PG9.1 check (a) handles the empty/by-design-absent schema case (wiring) | UNADDRESSED | HIGH | check (a) "12 all" has no exemption branch → false FAIL; must encode exemption |
| INV-006 | sufficiency_challenge | Does REFACTORing the item text ALONE green the phase? | ADDRESSED | — | Yes for text-level coherence; the actual migration work (9.11) and gate runs (PG9.1/2) still execute the proven mechanism. No hidden downstream gate — the parity-test + rf-qa-qualitative paths already exist and are green for 8 steps. Evidence: 256/256 regression at 9.9. |

No HIGH-severity UNADDRESSED invariants remain after the REFACTOR recommendations are applied (INV-001/002/005 are addressed *by* the REFACTORs). Convergence not blocked.

## Scoring matrix

| Item | Winner verdict | Confidence | Evidence |
|------|---------------|-----------|----------|
| 9.11 | REFACTOR | 92% | Unanimous; necessary work + 2 spec-internal contradictions (remediate meaning, 4-list) |
| 9.12 | REFACTOR | 90% | Unanimous; necessary artifact + unsatisfiable completion criterion + yaml redundancy |
| PG9.1 | REFACTOR (light) | 88% | Unanimous on check (a) false-FAIL; gate otherwise sound |
| PG9.2 | KEEP | 90% | Unanimous; standard pattern, clean once PG9.1 fixed |

## Convergence assessment
- Points resolved: 9/9 core
- Status: CONVERGED (~100% on verdicts)
- Unresolved: none (X-001/X-003/X-004 resolved as additive notes, not conflicts)
