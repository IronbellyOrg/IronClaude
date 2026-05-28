# Merged Spec-Fidelity Convergence Fix

<!-- Provenance: produced by /sc:adversarial-protocol -->
<!-- Base: Variant 5 (fix-5: Tier 1 code + property-based + flatline-halt tests) -->
<!-- Incorporated: fix-3 (helper-signature design + upstream-relocation docstring), fix-2 (id_schema_drift-as-fixability-instance docstring) -->
<!-- Deferred: fix-2 full fixability scaffolding (INV-003 unresolved threshold); fix-3 full upstream relocation (breaks roadmap_quote); fix-4 ADVISORY tier + CLI lane (audit burden, defer pending 2nd drift class) -->
<!-- Merge date: 2026-05-27T05:55:45Z -->

## Problem Statement
<!-- Source: Base (fix-5), problem statement, with minor additions from fix-2 framing -->

The TUIBBS v1-MVP roadmap pipeline halts at the `spec-fidelity` step with `Convergence not reached after 3 runs. Remaining active HIGHs: 54. TurnLedger: available=31, consumed=46`. All 54 ACTIVE HIGHs are identical-shape `phantom_id` findings driven by an asymmetric ID extraction/comparison pattern: `spec_parser.py:329` regex `\bD-?\d+\b` matches both `D1` and `D01` leniently, but `structural_checkers.py:380` compares them via raw `set` difference. Spec has `{D1, D3, D5}`; roadmap has `{D01, …, D54}`. The set difference flags all 54 as phantoms.

This is one specific instance of a broader pattern: the spec-fidelity gate emits findings without verifying they are reachable by an additive roadmap edit within the 30% diff guard at `remediate_executor.py:309-362` (fix-2's framing). The pattern has produced a distinct failure shape in every release (v3.0: phantom FR-NNN; mid-May: 10 HIGHs with `files_affected=[]`; TUIBBS: 54 ID-schema phantoms). The minimum-viable fix addresses the immediate trigger (the comparator asymmetry) AND adds a test infrastructure that catches future shapes at construction.

## Solution Overview

| # | Change | What it does | Source |
|---|---|---|---|
| 1 | `_canonicalize_requirement_id(family, raw) → str` helper | Pure function. Strips leading zeros within the numeric tail while preserving family prefix and sub-ID structure. Mirrors `integration_contracts.py:445` precedent. | Base (fix-5) + fix-1 (code identical) |
| 2 | Modify phantom_id block in `check_signatures` | Compare canonical sets; emit drift findings as MEDIUM `id_schema_drift`; preserve HIGH `phantom_id` for genuine missing IDs (canonical form NOT in spec). | Base (fix-5) + fix-1 (code identical) |
| 3 | 5 golden-fixture asymmetric-ID tests | Cover all 5 families (FR, NFR, SC, G, D) with both zero-pad and sub-ID drift cases; regression-lock genuine-phantom detection. | fix-5 Layer B(1) |
| 4 | Property-based + flatline-halt + cross-cutting integration tests | Family-agnostic property test (gated `importorskip`); flatline-halt regression test for the convergence loop; cross-cutting integration test for the all-fixes-unfixable scenario. | fix-5 Layer B(2,3,4) |

**Expected outcome on TUIBBS v1-MVP**: 54 HIGHs → **0 HIGHs + 54 MEDIUMs** in Run 1; convergence passes (gate predicate `active_high_count == 0` at `convergence.py:539` is satisfied; MEDIUM tier excluded from gate per registry filter at `convergence.py:242`). The 4 FIXED data_models findings from the prior Run 1 remain FIXED (no regression).

**Recurrence vector partially foreclosed**: the property-based test catches asymmetric-form drift across all 5 families at construction. The flatline-halt integration test locks the convergence-loop's behavior on the specific shape. Non-ID drift classes (e.g., function-name normalization in `function_missing`) remain a known follow-up class — addressed by the deferred fix-2 fixability scaffolding once its CLASS_DRIFT threshold is calibrated.

## Detailed Changes

### Change 1 — `_canonicalize_requirement_id` helper
<!-- Source: Base (fix-5) Layer A; influenced by fix-3 (signature design) and fix-2 (docstring) -->

**File**: `src/superclaude/cli/roadmap/structural_checkers.py`
**Location**: Near `_make_finding` (around line 260)
**Lines**: ~15 LOC added

See refactor-plan.md Change 1 for the full helper definition with docstring. Key elements:
- Pure `(family: str, raw: str) -> str` transformation; no shared state.
- Strips leading zeros within the numeric tail; preserves family prefix and sub-ID structure (e.g., `D01` → `D1`; `FR-7.1` → `FR-7.1` idempotent; `NFR-02` → `NFR-2`).
- Helper signature matches what would live in `spec_parser.py` — supports a FUTURE refactor to move canonicalization upstream (fix-3 framing) without rewriting the helper. Documented in docstring.
- Docstring tags `id_schema_drift` as a SPECIFIC INSTANCE of the broader fixability framing (fix-2 framing) — records the structural insight for the deferred full scaffolding.

### Change 2 — Modify the `phantom_id` block in `check_signatures`
<!-- Source: Base (fix-5) Layer A; identical to fix-1 -->

**File**: `src/superclaude/cli/roadmap/structural_checkers.py`
**Location**: Lines 372-391
**Lines**: ~10 LOC modified; ~10 LOC added

See refactor-plan.md Change 2 for the full replacement block. Additionally:
- Add `("signatures", "id_schema_drift"): "MEDIUM"` to `SEVERITY_RULES` (line 42-67).
- Add a templated entry to `FIX_GUIDANCE_TEMPLATES` (line 155-176): `"Spec uses '{spec_quote}' form; roadmap uses '{roadmap_quote}' form. Either normalize roadmap IDs to the spec form OR rely on the canonicalized comparator — this finding does not block convergence."`

### Change 3 — 5 golden-fixture asymmetric-ID tests
<!-- Source: fix-5 Layer B(1) -->

**File**: `tests/cli/roadmap/test_structural_checkers.py` (or `tests/roadmap/test_structural_checkers.py` per repo convention)
**Lines**: ~50 LOC added

5 new tests:
- `test_phantom_id_canonicalizes_zero_padded_d_ids` — spec={D1,D3,D5} roadmap={D01,D03,D05} → 0 HIGH, 3 MEDIUM `id_schema_drift`
- `test_phantom_id_genuine_phantom_still_emits_high` — spec={D1,D3} roadmap={D01,D99} → 1 HIGH (D99) + 1 MEDIUM (D01↔D1)
- `test_phantom_id_canonicalizes_fr_subids` — FR-7.1 idempotent + FR-07.1↔FR-7.1 drift
- `test_phantom_id_canonicalizes_nfr_padding` — NFR-02↔NFR-2 drift
- `test_phantom_id_idempotent_on_unpadded` — D1,D3,D5 everywhere → 0 findings

### Change 4 — Property-based + flatline-halt + cross-cutting integration tests
<!-- Source: fix-5 Layer B(2,3,4) -->

**Files**:
- NEW `tests/cli/roadmap/test_structural_checkers_properties.py` (~40 LOC)
- `tests/cli/roadmap/test_convergence.py` (~30 LOC added; sibling to `test_convergence_loop_three_runs:911`)
- `tests/cli/roadmap/test_remediate_executor.py` (~25 LOC added; sibling to `test_large_change_rejected:708`)

3 new tests:
- `test_canonicalization_property_holds_across_families` (NEW file, `importorskip("hypothesis")` guarded) — `@given(id_form_pairs())` strategy generates `(canonical, surface_variants)` pairs across all 5 families; asserts 0 HIGH `phantom_id` whenever canonical form matches on both sides.
- `test_flatline_halt_emits_structural_verdict` (test_convergence.py) — driver returns 58 findings on n=1, 54 on n=2, 54 on n=3 (TUIBBS shape). Pre-fix: asserts the flatline pattern reaches the halt formatter. Post-fix: asserts the same fixture passes on Run 1 with 0 active HIGH and 54 MEDIUM `id_schema_drift`.
- `test_loop_reports_structural_when_all_remediations_exceed_diff_guard` (test_remediate_executor.py) — registry where every active finding's only candidate patch exceeds the 30% guard; asserts terminal verdict identifies the structural ceiling, not budget exhaustion.

## Restriction Compliance Audit
<!-- Source: synthesis across all 5 variants' compliance sections -->

1. **Module ownership** (`structural_checkers.py` owns checkers + severity per `architecture-design.md:27-33`) — COMPLIES. All production changes in `structural_checkers.py`. Test changes mirror source location. (Resolves contradiction X-001 in favor of the majority interpretation.)
2. **Pure-function contract (NFR-4)** — COMPLIES. `_canonicalize_requirement_id` is pure `(str, str) -> str`. No I/O. No shared state.
3. **30% per-patch diff guard** — COMPLIES. ~20 LOC added + ~10 LOC modified in `structural_checkers.py` (~700+ LOC file) ≈ ~4%. Test files exempt from production-patch guard.
4. **Binary pass condition `active_highs == 0`** (`convergence.py:539`) — COMPLIES, NOT MODIFIED. The drift findings emit as MEDIUM; `get_active_high_count` at `convergence.py:242` whitelist-filters HIGH only, naturally excluding MEDIUM.
5. **Spec is an input the agent cannot modify** — COMPLIES. No spec edits. The canonicalization happens in IronClaude code; the runtime agent never touches the spec.
6. **`max_runs=3` hard default** — COMPLIES. Not touched. The fix works on Run 1.
7. **Canonicalization precedent at `integration_contracts.py:445`** — LEVERAGED. Same pattern, sibling-module placement.

## Unresolved Items (carried to return contract)

| Item | Source | Why unresolved |
|---|---|---|
| A-001 (spec immutability assumption) | diff-analysis.md | None of the 5 proposals consider spec-side normalization as a valid outcome. Surfacing for product/team decision. |
| A-002 (canonicalization direction) | diff-analysis.md | "Strip leading zeros" chosen by convention; documented in helper docstring; alternative direction (`D1 → D01`) would require team consensus on sort/alignment intent. |
| A-003 (30% diff guard correctness) | diff-analysis.md | S3 from the backlog (`roadmap-spec-fidelity-fix/RANKING.md`) remains deferred. Not reopened in this debate. |
| X-002 (comparator vs fixability root) | diff-analysis.md | Partially resolved: comparator is where this fix lives; fixability framing documented as future work in Change 1's docstring; full scaffolding deferred pending CLASS_DRIFT threshold calibration (INV-003). |
| Non-ID drift classes (e.g., `function_missing` name normalization) | INV-001 follow-up | When a 2nd drift class surfaces, reconsider fix-2's fixability scaffolding and fix-4's ADVISORY tier. |

## Post-Merge Validation

- **Structural integrity**: ✅ Pass (all sections present; headings consistent).
- **Internal references**: ✅ All file:line citations verified against the source files during Wave 1 and Wave 1.5 grounding.
- **Contradiction rescan**: ✅ No new contradictions introduced by the merge. Resolved X-001 (majority interpretation, with fix-3 framing preserved for future). X-002 partially resolved. X-003 resolved against fix-4 (MEDIUM tier chosen).
