# Phase 2 Requirements Gate — Consolidated Verdict

Gate item: C-007 (Phase 2 phase-gate QA). Two report-only lens agents + one fix cycle.

## Lens reports
| Lens | Agent | Report | Cycle-0 | Final |
|---|---|---|---|---|
| requirements-patch-structure | rf-qa (adversarial, report-only) | `qa/phase-2-requirements-gate-structure.md` | FAIL (F1 IMPORTANT, F2 MINOR) | **PASS** (after fix cycle 1) |
| requirements-patch-fr-rh1-semantics | rf-qa-qualitative (adversarial, report-only) | `qa/phase-2-requirements-gate-semantics.md` | PASS (1 MINOR non-blocking) | **PASS** |

## Findings and resolution
- **F1 (structural, IMPORTANT) — RESOLVED.** The amendment §6 override table covered the spec-absent prose at `merged-requirements.md:133-138` but not the two verdict-table rows `MR:93` (§3.3) and `MR:236` (§4.12), both of which list "or spec absent" as an `unproven`→Grounding-Gap + `needs_human_decision` condition — a stale R3 violation. Fix: added two override rows (AMD:96, AMD:97) explicitly superseding `:93` and `:236` under R3 (spec-and-tasklist-absent is telemetry-only). Re-verified PASS by rf-qa cycle 1.
- **F2 (structural, MINOR) — RESOLVED.** Verdict row-3 now cites AMD §6 rows `:93` and `:236`.
- **Semantic MINOR (non-blocking, ACKNOWLEDGED).** `merged-requirements.md` has no in-file `superseded-by` banner; an implementer who opens it directly bypasses the amendment. Mitigation: the authority chain runs through `FR-RH1-v1-amendment.md` (declared authoritative) and the requirements map; Phase 3 items read the amendment/map, not the raw stale artifact. Not blocking.

## Semantic confirmations (rf-qa-qualitative, against canonical REPORT)
- R1 real-boot-only Regression; NO clause permits static-binding-absence + oracle_mismatch ⇒ unreachable/Regression (that path is `unproven`). ✅
- R2/R3 telemetry-only skips (no Grounding Gap / needs_human_decision / status change). ✅
- R4 contract `1.6.0`; R8 bounded caps (no zero-cost); R9 advisory-only semantic fallback (explicit `durable_sink:`/`@sink` sole v1 trigger). ✅
- R7 invariant arithmetic present and correct. ✅
- All stale dangerous clauses exist ONLY in historical `merged-requirements.md` and are named-and-superseded by the amendment. ✅

## CONSOLIDATED VERDICT: **PASS**
Phase 3 may proceed on `FR-RH1-v1-amendment.md` (authoritative R1–R9), not on the stale `merged-requirements.md` clauses. Fix cycles used: 1 of max 3.
