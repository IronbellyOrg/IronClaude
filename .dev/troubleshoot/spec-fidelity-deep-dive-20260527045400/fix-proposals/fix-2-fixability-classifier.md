# Fix Proposal #2 — Fixability classifier + canonicalizer as first user (Tier 2 / root-cause-analyst, deeper framing)

## Problem statement

The Tier 1 mechanical observation (D01 != D1) is correct but mis-locates the load-bearing defect. Every release of the spec-fidelity gate fails with a *different* shape (severity drift v3.0; parser noise + `files_affected=[]` mid-May; ID-schema drift TUIBBS today). This is the empirical fingerprint of a missing fixability invariant at the finding-emission boundary: `_make_finding` (`structural_checkers.py:269-286`) constructs every HIGH with an implicit, unverified contract — "this finding can be resolved by an additive roadmap edit fitting inside the 30% diff guard" — that is never checked. When violated, the convergence loop cannot distinguish a structurally-unfixable finding from agent failure and burns 3 runs producing a budget-shaped halt.

## Proposed change

ONE module: `src/superclaude/cli/roadmap/structural_checkers.py`. Two coordinated parts.

**Part A — Fixability classifier infrastructure (the generalizable layer):**

1. Add `_classify_fixability(dimension, mismatch_type, finding_count, drift_canonical_form) -> FixabilityClass` pure helper near `_make_finding` (~line 260). `FixabilityClass` ∈ `{ADDITIVE_FIXABLE, CLASS_DRIFT, SCHEMA_MIGRATION}`.

2. Add `FIXABILITY_GUIDANCE_TEMPLATES` dict (~line 98) alongside existing `FIX_GUIDANCE_TEMPLATES`.

3. Modify `_make_finding` (lines 263-286) to accept optional `fixability` arg; when present and not `ADDITIVE_FIXABLE`, override severity to `MEDIUM` and replace `fix_guidance` with class-specific template.

**Part B — Canonicalizer as first user:**

4. Add `_canonicalize_requirement_id(pid: str) -> str` helper.

5. In `check_signatures` lines 372-391, compute `phantom_ids_raw = roadmap_ids - spec_ids` and `phantom_ids_canon = {canon(p) for p in roadmap_ids} - {canon(p) for p in spec_ids}`. For each raw `pid` in `phantom_ids_raw`: if `canon(pid) in {canon(s) for s in spec_ids}` → emit through `_make_finding(fixability=CLASS_DRIFT)` (auto-demoted to MEDIUM with `id_schema_drift` template). Else → emit HIGH `phantom_id` (current behavior).

Total ~48 LOC added, ~3 modified in a ~700-line module.

## Evidence

- `src/superclaude/cli/roadmap/structural_checkers.py:269-286` — `_make_finding` lacks fixability awareness
- `src/superclaude/cli/roadmap/structural_checkers.py:380-391` — phantom_id emission emits 1 finding per drifted ID rather than 1 finding per rule-class
- `src/superclaude/cli/roadmap/convergence.py:539, 620-630` — loop has no fixability signal to distinguish agent-failure from structurally-unfixable
- `src/superclaude/cli/roadmap/integration_contracts.py:445` — canonicalization precedent (only partial; doesn't extend to fixability)
- `.dev/releases/complete/v3.0_unified-audit-gating/adversarial-design-review/fidelity-investigation/adversarial/debate-transcript.md:127` — explicit consensus that no shipped fix touched the comparator
- `historical-context.md` Pattern 2 — every prior failure shape distinct (the fingerprint of missing invariant)

## Risks

- Over-engineering risk: if no future failure shape ever surfaces, the ~30 lines of scaffolding never pay off (Tier 1 patch alone would have sufficed)
- Mis-classification: classifier could wrongly tag genuine phantom as CLASS_DRIFT (mitigated by structural check, not heuristic)
- MEDIUM-spike side effects (same as fix-1)
- Does NOT address LLM attention drift (Pattern 1 from historical-context.md)
- Does NOT resurrect S6 (left deferred)

## Test plan

- `test_phantom_id_canonicalizes_zero_padded_d_ids` (same as fix-1)
- `test_phantom_id_real_missing_still_emits_high` (regression)
- `test_fixability_classifier_class_drift_aggregation` (asserts 54 same-class IDs all share fixability=CLASS_DRIFT + rule_id=id_schema_drift)
- `test_class_drift_medium_does_not_block_pass`
- Regression for `_make_finding` backward-compat (callers without `fixability=` arg unchanged)

## Documented constraints to honor

### Restrictions
1. Module ownership — all in `structural_checkers.py`. [COMPLIES]
2. Pure-function contract — `_classify_fixability`, `_canonicalize_requirement_id`, modified `_make_finding` all pure. [COMPLIES]
3. 30% diff guard — ~48 LOC in 700-line module = ~7%. [COMPLIES]
4. Binary pass condition — NOT modified. CLASS_DRIFT auto-demotes via Part A; pass condition naturally succeeds. [COMPLIES]
5. Spec is an input. [COMPLIES — no spec edits]
6. `max_runs=3`. [COMPLIES — not touched]
7. Canonicalization precedent. [LEVERAGED — Part B mirrors `integration_contracts.py:445`. Part A also has in-module precedent at `_classify_nfr_severity` (line 309-327).]

### Re-frame signals
1. No shipped fix has touched the comparator — this fix does AND adds the missing invariant. [ADDRESSES]
2. Failure shape has shifted; surgical fix leaves next shape unguarded — fixability scaffolding addresses next-shape recurrence proactively. [ADDRESSES at structural recurrence vector level]
3. Chosen remediation surface is `structural_checkers.py`. [ALIGNED]
