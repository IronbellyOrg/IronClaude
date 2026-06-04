<!-- Provenance: produced by /sc:adversarial Mode B (inline), Round 2.5 -->

# Invariant Probe Results — Phase 10 (R1.5)

## Round 2.5 — Fault-Finder Analysis

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | guard_conditions | verify-implementation's FR→AST assertion can run at production runtime | UNADDRESSED | HIGH | Step 10.2 routes resolution through `fidelity_checker._scan_codebase` (source-tree rglob) + `importlib`; `gate_passed` dispatches code_assertions with `repo_root` (pipeline/gates.py:99-100); pipx package has no `src/` and CWD-fallback (`executor.py:1615-1619`) points at the user's project. R1.3 merged-rec INV-001 establishes source-tree assertions are CI-only. |
| INV-002 | sufficiency_challenge | Adding verify-implementation ALONE closes Flaw 1's evidence chain at runtime | UNADDRESSED | HIGH | Downstream gate that falsifies sufficiency: the envelope-None shim (pipeline/gates.py:93-98) returns PASS when a code_assertion-only gate is dispatched without envelope/repo_root. If verify-implementation is wired like every current call site (no envelope plumbed), its gate silently PASSES at runtime → Flaw 1 not closed, only relocated. Sufficiency requires the assertion be runtime-artifact-grounded AND the live gate path actually plumb envelope. |
| INV-003 | state_variables | `envelope.spec_ids[FR]` yields an FR's spec state | UNADDRESSED | HIGH | `SpecIdRegistry` (id_registry.py:43-90) exposes `fr_ids: tuple[str,...]`, no `__getitem__`. Subscript raises TypeError. Correct binding is `envelope.spec_ids.fr_ids`. |
| INV-004 | collection_boundaries | empty `fr_ids` is handled | UNADDRESSED | MEDIUM | If a spec declares zero FRs, the assertion's for-loop is empty → returns no Finding → gate PASSES (silent PASS on empty target). Contract #4 (PG10.1 check e: "no silent PASS on empty FRs") requires an explicit empty-FR guard. Step 10.3 has no `test_empty_fr_set` case. |
| INV-005 | count_divergence | line citations in 10.1/10.2 match current source | UNADDRESSED | MEDIUM | Task cites `fidelity_checker.py:287-303` / `314-337` and `executor.py:2167`/`2176`; actual fail-open is L302/L320, `gate=None` bypass is L2579, wiring-verification step is L2588. ~3-12 line drift. A verbatim-following worker edits wrong lines. |
| INV-006 | interaction_effects | consolidating wiring-verification to hold budget ≤14 has no side effects | ADDRESSED | LOW | Step 10.2 explicitly migrates the consolidated step's tests; certify preserved (carries R1.3 runtime semantic_checks). Interaction handled by design step 10.1. |
| INV-007 | guard_conditions | sequencing prereq (ship after/with Step 11.4) is enforced | ADDRESSED | LOW | Task L603 H2-fix note already binds the ordering; PG10.2 proceeds to Phase 11. |

## Summary
- Total findings: 7
- ADDRESSED: 2 (INV-006, INV-007)
- UNADDRESSED: 5
  - HIGH: 3 (INV-001, INV-002, INV-003)
  - MEDIUM: 2 (INV-004, INV-005)
  - LOW: 0

## Gate verdict
3 HIGH UNADDRESSED invariants. Per AD-1 these would BLOCK convergence on a *consensus fix proposal*. Here, the debate's consensus IS that these three faults define the mandatory REFACTOR scope for Step 10.2 (substrate swap + correct subscript + plumb-or-classify), so they are surfaced as the verdict's required-replacement content rather than blocking the verdict itself. INV-002 (sufficiency) is the deepest: verify-implementation only kills Flaw 1 if BOTH (a) its assertion is runtime-artifact-grounded AND (b) the live gate path actually plumbs envelope so it isn't shim-skipped — Phase 10 as written guarantees neither.
