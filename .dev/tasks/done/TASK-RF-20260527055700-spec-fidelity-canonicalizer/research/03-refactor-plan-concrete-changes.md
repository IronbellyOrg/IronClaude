# Refactoring Plan

## Overview

- **Base**: Variant 5 (fix-5: Tier 1 code + property-based + flatline-halt tests)
- **Incorporated variants**: fix-3 (helper signature design + docstring on future upstream relocation), fix-2 (docstring tagging id_schema_drift as a fixability instance)
- **Total changes planned**: 4 (3 base + 1 incorporated)
- **Total changes rejected**: 4 (full upstream relocation from fix-3, full fixability scaffolding from fix-2, ADVISORY severity tier from fix-4, CLI lane from fix-4)
- **Risk**: Low overall (single production file, < 30% per-patch diff, test additions exempt from production guard)

## Planned Changes

### Change 1 — Add `_canonicalize_requirement_id` helper (from base fix-5 Layer A; influenced by fix-3 and fix-2)

- **Source**: fix-5 (code identical to fix-1)
- **Target location**: `src/superclaude/cli/roadmap/structural_checkers.py`, near `_make_finding` (around line 260)
- **Integration approach**: Append helper definition + module-level docstring
- **Rationale (citing debate evidence)**:
  - debate-transcript.md Round 1 (all 5 variants endorse canonicalization)
  - INV-006 (mechanical sufficiency confirmed)
  - C-001 winner: fix-3's argument for upstream is structurally elegant BUT the minimal version breaks `roadmap_quote` (X-001 contradiction); choosing checker-side preserves `Finding.roadmap_quote` semantics
- **Integration approach**:
  ```python
  def _canonicalize_requirement_id(family: str, raw: str) -> str:
      """Canonicalize a requirement ID to enable drift-tolerant comparison.

      Mirrors the precedent in integration_contracts.py:445 (_canonicalize_identifiers,
      KNOWLEDGE.md 2026-05-25 "Fix B Merged"). Strips leading zeros within the
      numeric tail while preserving family prefix and any sub-ID structure.

      Examples:
          D01     -> D1
          D-01    -> D1
          FR-7    -> FR-7   (idempotent)
          FR-7.1  -> FR-7.1 (sub-ID preserved)
          NFR-02  -> NFR-2

      Note: this helper is intentionally a pure (family, raw) -> str transformation
      with no shared state. A future refactor MAY relocate this helper into
      spec_parser.extract_requirement_ids so canonical IDs flow downstream by
      construction (refactoring-expert framing in fix-3 of the adversarial debate).
      For now it lives in the checker because relocation would alter the
      Finding.roadmap_quote semantics at structural_checkers.py:389.

      Note (forward-looking): this fix demotes "canonical form matches but surface
      form differs" findings to MEDIUM with rule_id="id_schema_drift". This is a
      specific instance of a broader "fixability" concept (fix-2 framing in the
      adversarial debate): findings should declare whether they are reachable by
      an additive roadmap edit. The full fixability classifier is deferred pending
      calibration of the CLASS_DRIFT count threshold (INV-003 of the invariant probe).
      """
      ...
  ```
- **Risk level**: Low (pure function, no shared state, well-defined family-aware transformation)

### Change 2 — Modify the `phantom_id` block in `check_signatures` (from base fix-5 Layer A; identical to fix-1)

- **Source**: fix-5 / fix-1
- **Target location**: `src/superclaude/cli/roadmap/structural_checkers.py:372-391`
- **Integration approach**: Replace the current set-difference with canonicalized set-difference + classification:
  ```python
  # Compute both raw and canonical sets
  spec_canon = {_canonicalize_requirement_id("D" if p.startswith("D") else family, p): p
                for family, ids in spec_parsed.requirement_ids.items() for p in ids}
  roadmap_canon = {_canonicalize_requirement_id(family if p in ids else "?", p): p
                   for family, ids in roadmap_parsed.requirement_ids.items() for p in ids}

  drift_findings  = []  # MEDIUM id_schema_drift
  phantom_findings = []  # HIGH phantom_id (current behavior)
  for canon, raw in roadmap_canon.items():
      if canon in spec_canon:
          if raw == spec_canon[canon]:
              continue  # exact match — no finding
          drift_findings.append(_make_finding(
              dimension="signatures", mismatch_type="id_schema_drift",
              description=f"Roadmap ID '{raw}' canonicalizes to spec ID '{spec_canon[canon]}' "
                          f"(surface form differs). Does not block convergence.",
              location=f"roadmap:{raw}", spec_quote=spec_canon[canon], roadmap_quote=raw,
          ))
      else:
          phantom_findings.append(_make_finding(  # current HIGH behavior
              dimension="signatures", mismatch_type="phantom_id",
              description=f"Roadmap references ID '{raw}' not found in spec",
              location=f"roadmap:{raw}", spec_quote="[MISSING]", roadmap_quote=raw,
          ))
  findings.extend(phantom_findings); findings.extend(drift_findings)
  ```
- **Also required**: Add `("signatures", "id_schema_drift"): "MEDIUM"` to `SEVERITY_RULES` (around line 42-67). Add a templated `id_schema_drift` entry to `FIX_GUIDANCE_TEMPLATES` (around line 155-176): `"Spec uses '{spec_quote}' form; roadmap uses '{roadmap_quote}' form. Either normalize roadmap IDs to the spec form OR rely on the canonicalized comparator — this finding does not block convergence."`
- **Rationale**: addresses the root cause documented at `structural_checkers.py:380` (raw set difference). Drops 54 HIGHs to 0 HIGHs + 54 MEDIUMs (which the convergence gate ignores per `get_active_high_count` at `convergence.py:242`).
- **Risk level**: Low (additive edit; preserves existing genuine-phantom behavior for IDs whose canonical form is not in spec)

### Change 3 — Add 5 golden-fixture asymmetric-ID tests (from base fix-5 Layer B(1))

- **Source**: fix-5 Layer B(1)
- **Target location**: `tests/cli/roadmap/test_structural_checkers.py` (or `tests/roadmap/test_structural_checkers.py` per repo convention)
- **Integration approach**: Add 5 tests as siblings to existing `test_detects_phantom_id`:
  - `test_phantom_id_canonicalizes_zero_padded_d_ids` — spec={D1,D3,D5} roadmap={D01,D03,D05} → 0 HIGH, 3 MEDIUM `id_schema_drift`
  - `test_phantom_id_genuine_phantom_still_emits_high` — spec={D1,D3} roadmap={D01,D99} → 1 HIGH (D99), 1 MEDIUM (D01↔D1)
  - `test_phantom_id_canonicalizes_fr_subids` — `FR-7.1` vs `FR-7.1` identity, plus `FR-07.1` vs `FR-7.1` drift
  - `test_phantom_id_canonicalizes_nfr_padding` — `NFR-02` vs `NFR-2` drift
  - `test_phantom_id_idempotent_on_unpadded` — `D1, D3, D5` everywhere → 0 findings
- **Rationale**: closes the example-based test gap identified in fix-5's evidence (`test_structural_checkers.py:152, 258`).
- **Risk level**: Low (test additions, no production impact)

### Change 4 — Add property-based test + flatline-halt + cross-cutting integration test (from base fix-5 Layer B(2-4))

- **Source**: fix-5 Layer B(2), B(3), B(4)
- **Target locations**:
  - NEW `tests/cli/roadmap/test_structural_checkers_properties.py` (or repo convention path) — property-based test gated by `pytest.importorskip("hypothesis")` per the precedent at `tests/sprint/test_property_based.py`
  - `tests/cli/roadmap/test_convergence.py` — `test_flatline_halt_emits_structural_verdict` (sibling to `test_convergence_loop_three_runs:911`)
  - `tests/cli/roadmap/test_remediate_executor.py` — `test_loop_reports_structural_when_all_remediations_exceed_diff_guard` (sibling to `test_large_change_rejected:708`)
- **Integration approach**:
  - Property-based test: `@given(id_form_pairs())` strategy yielding `(canonical, surface_variants)`; assert 0 HIGH for canonical-form matches.
  - Flatline-halt test: driver returns 58 findings on n=1, 54 on n=2, 54 on n=3 (TUIBBS shape). Assert NOT passed AND halt-reason text contains a structural-unfixability marker. After Change 2 lands, the same fixture passes on Run 1 (regression lock).
  - Cross-cutting integration test: registry where every active finding's only candidate patch exceeds 30% guard; assert terminal verdict identifies the structural ceiling, not budget exhaustion.
- **Rationale**: closes 3 coverage gaps identified in fix-5 (Layer B description) and provides property-based protection against the NEXT family that surfaces canonical-form drift.
- **Risk level**: Low (test additions; `importorskip` handles hypothesis dep posture)

## Changes NOT Being Made

### From fix-2 (Tier 2 / root-cause-analyst, "scaffolded")
- **Rejected**: Full `_classify_fixability` + `FIXABILITY_GUIDANCE_TEMPLATES` + modified `_make_finding` scaffolding (~30 LOC of new abstraction).
- **Rationale**: INV-003 (HIGH UNADDRESSED in the invariant probe) — the `CLASS_DRIFT` count threshold is undefined, making the classifier non-deterministic. Without a defined threshold the scaffolding is unsafe to ship. The CONCEPT is endorsed: docstring on `_canonicalize_requirement_id` flags `id_schema_drift` as a specific instance of the broader fixability framing for future generalization.
- **What was preserved instead**: docstring forward-reference (see Change 1).

### From fix-3 (Tier 2 / refactoring-expert, "upstream")
- **Rejected**: Move canonicalization into `spec_parser.extract_requirement_ids` so canonical IDs flow downstream by construction.
- **Rationale**: The minimal-LOC framing breaks `Finding.roadmap_quote` at `structural_checkers.py:389` (which expects the source form for human-readable reports). The full version (value-object refactor with both canonical and raw forms) exceeds the ~12 LOC budget and turns into a multi-module refactor. The seam-elimination INSIGHT is preserved as future work.
- **What was preserved instead**: helper signature `(family: str, raw: str) -> str` is identical to what would live in `spec_parser.py`, so a future refactor can MOVE the helper without rewriting it. Documented in the helper's docstring (see Change 1).

### From fix-4 (Tier 2 / system-architect, "architectural")
- **Rejected**: New `ADVISORY` severity tier in `Finding.severity` + new CLI flags `--allow-advisory-drift` / `--strict-no-advisory` + downstream-consumer audit.
- **Rationale**: The new severity tier introduces ongoing audit burden on every `Finding.severity` consumer (report formatter, audit log emitter, release-readiness scorer, etc.) and a permanent CLI API surface. The architectural cleanliness IS valuable but only justified when 2+ drift classes need taxonomic distinction. Currently 1 (ID-schema). Defer the ADVISORY tier proposal pending a second drift class.
- **What was preserved instead**: nothing in this fix; explicitly documented as a follow-up consideration for the next release.

### Common spec-side path
- **Rejected**: Spec-side normalization (e.g., "the team should update the spec to use D01..D54"). 
- **Rationale**: A-001 of the diff-analysis (UNSTATED shared assumption: "the spec must be treated as immutable input"). None of the 5 proposals consider spec-side normalization as a valid outcome path. The right answer in some projects MAY be a spec edit; that's a human decision, surfaced in the return contract's unresolved-conflicts.

## Risk Summary

| Change | Risk | Mitigation |
|---|---|---|
| 1 (helper) | Low | Pure function, no shared state, 5-family-aware. Property-based test in Change 4 validates correctness across families. |
| 2 (phantom_id block) | Low | Additive edit; preserves existing genuine-phantom behavior. Tests in Change 3 lock both pass and fail conditions. |
| 3 (golden-fixture tests) | None | Test additions only. |
| 4 (property-based + flatline + integration) | Low | `importorskip` handles `hypothesis` dep posture; flatline test asserts on stable halt-reason markers (refactor risk noted in fix-5's risks). |

**Per-patch 30% diff guard compliance**: All production changes (Changes 1-2) fit in `structural_checkers.py` — ~20 LOC added + ~20 LOC modified in a 700+ line file ≈ ~6%. Well under the 30% per-patch threshold.

## Review Status

- Approval: auto-approved (non-interactive mode)
- Timestamp: 2026-05-27T05:55:30Z
