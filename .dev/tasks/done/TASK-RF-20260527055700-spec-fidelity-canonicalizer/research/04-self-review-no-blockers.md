# Wave 4 Self-Review — Spec-Fidelity Convergence Fix

**Date**: 2026-05-27
**Reviewer**: Self-Review Agent
**Target**: merged-output.md + refactor-plan.md + invariant-probe.md

---

## Self-Check Question 1 — Tests for the chosen fix

**Count**: 9 new tests across 3 files (5 golden-fixture + 1 property-based + 1 flatline-halt + 1 cross-cutting + 1 idempotency).

**Adequacy**: ADEQUATE.
- 5 family-specific golden tests (FR, NFR, SC, G, D) cover both zero-pad and sub-ID drift.
- Property-based test (`hypothesis`-gated via `importorskip`) provides family-agnostic future-proofing.
- Flatline-halt regression test pins the convergence-loop behaviour on the exact TUIBBS shape (58/54/54).
- Cross-cutting integration test guards against confusing "structural ceiling" with "budget exhaustion."

**Evidence**: refactor-plan.md Changes 3 & 4; merged-output.md §"Detailed Changes" 3 & 4.

## Self-Check Question 2 — Edge cases

- **Genuine phantoms still HIGH**: COVERED by `test_phantom_id_genuine_phantom_still_emits_high` (spec={D1,D3} roadmap={D01,D99} → 1 HIGH + 1 MEDIUM).
- **FR sub-IDs (`FR-7.1`)**: COVERED by `test_phantom_id_canonicalizes_fr_subids` (idempotent + drift case).
- **Empty collections**: ADDRESSED by INV-004 (extract_requirement_ids returns `{}` cleanly; set-difference well-defined).
- **Idempotency on unpadded**: COVERED by `test_phantom_id_idempotent_on_unpadded`.
- **NOT covered**: INV-002 (intentional `D1` AND `D-01` coexisting in spec) — canonicalizer collapses them silently; no collision warning. MEDIUM, documented.
- **NOT covered**: INV-001 (new family like `TC-NNN`) — no test guards `_REQUIREMENT_PATTERNS` completeness. MEDIUM.

## Self-Check Question 3 — Satisfies original requirements

- **Unblock TUIBBS convergence**: YES. 54 HIGHs → 0 HIGHs + 54 MEDIUMs on Run 1; `get_active_high_count` (convergence.py:242) whitelist-filters HIGH, so MEDIUM `id_schema_drift` is naturally excluded from the gate (`active_high_count == 0` predicate at convergence.py:539 satisfied).
- **7 restrictions audit**: All 7 explicitly checked (module ownership, NFR-4 purity, 30% diff guard ≈4%, binary pass predicate untouched, spec immutability respected, `max_runs=3` untouched, leverages `integration_contracts.py:445` precedent). COMPLIES.
- **Recurrence vector**: PARTIALLY foreclosed. Property test catches asymmetric-form drift across all 5 families. Non-ID drift classes (e.g., `function_missing` name normalization) remain a known follow-up — explicitly tracked.

## Self-Check Question 4 — Follow-up items

1. **A-001** — Spec immutability assumption (none of 5 variants considered spec-side normalization; product decision needed).
2. **A-002** — Canonicalization direction (`D01 → D1` chosen; alternative `D1 → D01` needs team consensus).
3. **INV-001** — Add `TC-NNN`-style family additions test guard.
4. **INV-002** — Add collision warning when both `D1` and `D-01` exist in same spec.
5. **Deferred fix-2 scaffolding** — `_classify_fixability` blocked on INV-003 (CLASS_DRIFT threshold undefined). Revisit when 2nd drift class surfaces.
6. **Deferred fix-4 ADVISORY tier** — defer until 2+ drift classes justify the taxonomic tier + CLI surface.

---

## BLOCKERS

None. The fix is shippable as specified.

## CONCERNS (non-blocking)

1. **INV-002 silent collision** — if a spec ever intentionally uses both `D1` and `D-01` as distinct IDs, this fix collapses them with no warning. Low probability in practice; document in helper docstring for future readers.
2. **Flatline-halt test brittleness** — fix-5's own risks note that asserting on halt-reason marker text may break if the formatter is refactored. Recommend asserting on a stable structural field rather than a string substring.
3. **Path convention** — refactor-plan offers two test paths (`tests/cli/roadmap/` or `tests/roadmap/`); pick one consistently before commit per repo convention.
4. **MEDIUM tier suppression assumption** — verified mechanically against `convergence.py:242` whitelist but worth a single integration smoke test on a fresh fixture to confirm gate behaviour end-to-end.

---

**Verdict**: APPROVED. Ship Changes 1-4 as specified. Capture follow-up items in the return contract.
