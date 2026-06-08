---
artifact: r5-remediation-decision
phase: 3
gate: r5-decision
verdict_source: phase-2-reproduction
decision: PROCEED
scope: MD-FAMILY-PLUS-ALLOWLIST
---

# R5 Remediation Decision

## Decision: **PROCEED** (path b) — scope **MD-FAMILY-PLUS-ALLOWLIST**

The milestone-prefixed `M{n}-D{nn}` ID false-positive **genuinely reproduces on the current branch**. Phase 4 (the R5 implementation subtree) **EXECUTES IN FULL**, including the allowlist port (item 4.4).

## Evidence (from Phase 2, QA-verified PASS in `reviews/qa-phase-2-report.md`)

1. **Current-tree premise confirmed** (`r5-current-state.md`): `contracts.ID_PATTERNS` has FR/NFR/SC/G/D only — no MD family; no `md_ids` anywhere; no Explicit-non-references allowlist subsystem.
2. **Tokenizer FP confirmed** (`r5-current-state.md` §Tokenizer FP Probe): `extract_requirement_ids('...M1-D01, M1-D02, M2-D01...')` → `{'D': ['D01', 'D02']}`. The `M{n}-` prefix is discarded; `M1-D01` and `M2-D01` collide into one bare `D01`.
3. **Structural FP reproduced** (`r5-reproduction.md`, `test-results/r5-repro-output.txt`): asymmetric milestone fixture (spec `M1-D01,M2-D01,M3-D01` vs roadmap `M1-D01,M1-D02,M2-D03`) → **2 HIGH `phantom_id`** for `D02`,`D03` with `spec_quote='[MISSING]'`. These are legitimate milestone deliverables (`M1-D02`, `M2-D03`) wrongly flagged — the exact class of PR #111's 51-HIGH incident.
4. **Scope forced to PLUS-ALLOWLIST** (`r5-scope-determination.md`): PR #111's oracle test #1 `test_phantom_id_honors_explicit_non_references_for_milestone_d_ids` (the canonical v1-MVP bug-trigger shape, at commit `861047c2`) uses `_write_md_fixture_with_allowlist` and its roadmap body carries standalone bare-`D` `D01..D05` indices exempted only by the `**Explicit non-references (do not resolve against spec):**` annotation. The MD family alone cannot make that test pass; the allowlist is required. Tests #2/#3 use the plain `_write_id_fixture` and already pass on this branch.

## Mandatory Phase 4 carry-forward (ALL items in scope under MD-FAMILY-PLUS-ALLOWLIST)

| Phase 4 item | Action | In scope? |
|---|---|---|
| 4.1 | Add anchor-free `MD` body to `contracts.ID_PATTERNS` (before `D`, sourced from SoT, never inlined) | ✅ YES |
| 4.2 | `_MD_TRAILING_D_RE` + dedup in `spec_parser.extract_requirement_ids` | ✅ YES |
| 4.3 | MD canonicalizer branch in `structural_checkers._canonicalize_requirement_id` (distinct `M1-D1` vs `M2-D1`) | ✅ YES |
| 4.4 | **Explicit non-references allowlist port** in `structural_checkers` | ✅ YES (scope = PLUS-ALLOWLIST) |
| 4.5 | `md_ids` field on `SpecIdRegistry` + the 2 extra `SpecIdRegistry(` sites (`envelope.py::envelope_from_dict`, `test_pipeline_envelope.py::sample_envelope`) with `.get("md_ids", ())` round-trip | ✅ YES |
| 4.6 | `md_ids` in `SpecIdRegistry.union_of_known()` | ✅ YES |
| 4.7 | `md_ids` in `SpecIdRegistry.to_dict()` | ✅ YES |
| 4.8 | `md_ids` in `build_id_registry` | ✅ YES |
| 4.9 | `md_ids` in gates Contract #9 sidecar read (`_roadmap_ids_within_spec`) | ✅ YES |
| 4.10 | schema-test updates for `md_ids` | ✅ YES |
| 4.11 | conftest sidecar `md_ids` | ✅ YES |
| 4.12 | Port PR #111's 3 oracle tests + `_write_md_fixture_with_allowlist` helper (from `861047c2`) | ✅ YES |
| 4.13 | Disk-backed `M{n}-D{nn}` fixture | ✅ YES |
| 4.14 | Run R5 test surfaces incl. `test_pipeline_envelope.py` | ✅ YES |
| 4.15 | Confirm `make lint-architecture` green (MD body only in SoT) | ✅ YES |

## PR #111 disposition
Once path-b lands and the 3 oracle tests pass on this branch, PR #111 (`fix/roadmap-md-family-tokenizer-canonicalizer`) is superseded by the contracts-SoT-sourced port and may be **closed as superseded** by the operator (outward-facing action — surface `gh pr close 111 --repo IronbellyOrg/IronClaude` to the operator at task end; do not auto-close).
