# QA Report — Phase 3 (Production Code Change 2)

**Topic:** Phase 3 — phantom_id block + SEVERITY_RULES + FIX_GUIDANCE_TEMPLATES
**Date:** 2026-05-27
**Phase:** task-integrity (production-code phase gate)
**Fix cycle:** 1 (no fixes required)
**Target file:** `/config/workspace/IronClaude/src/superclaude/cli/roadmap/structural_checkers.py`

---

## Overall Verdict: PASS

All 13 acceptance criteria (A1–A3, B1–B4, C1–C6) verified directly against the source file. No fixes required.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| A1 | `("signatures", "id_schema_drift"): "MEDIUM"` exists in SEVERITY_RULES | PASS | Read line 34: `("signatures", "id_schema_drift"): "MEDIUM",` |
| A2 | Placed adjacent to `("signatures", "phantom_id"): "HIGH"` | PASS | Read lines 33–34: phantom_id immediately precedes id_schema_drift |
| A3 | Exactly 1 line added; no other SEVERITY_RULES entries modified | PASS | Lines 31–57 — only the new entry added at line 34; all 19 other entries match the pre-edit baseline character-for-character |
| B1 | `id_schema_drift` key exists in FIX_GUIDANCE_TEMPLATES dict | PASS | Read line 120: `"id_schema_drift": (` |
| B2 | Template body matches verbatim from research/02-merged-fix-spec.md §"Change 2" | PASS | Lines 121–123. Confirmed em dash is U+2014 via `grep -P "comparator [—]"` (matched in both code AND spec at research file line 53). Byte-level comparison via Python repr: `"Spec uses '{spec_quote}' form; roadmap uses '{roadmap_quote}' form. Either normalize roadmap IDs to the spec form OR rely on the canonicalized comparator — this finding does not block convergence."` — exact match. |
| B3 | Placeholders `{spec_quote}` and `{roadmap_quote}` present | PASS | Line 121 contains both placeholders |
| B4 | No other FIX_GUIDANCE_TEMPLATES entries modified | PASS | Read lines 99–183. All 19 pre-existing template entries (`file_missing`, `path_prefix_mismatch`, `enum_uncovered`, `field_missing`, `phantom_id`, `function_missing`, `param_arity_mismatch`, `param_type_mismatch`, `frontmatter_field_missing`, `step_param_missing`, `ordering_violated`, `semantic_check_missing`, `mode_uncovered`, `default_mismatch`, `threshold_contradicted`, `security_missing`, `dep_direction_violated`, `coverage_mismatch`, `dep_rule_missing`) intact. Only `id_schema_drift` was inserted between `phantom_id` and `function_missing` at lines 120–124. |
| C1 | Block builds `spec_canon: dict[str, str]` and `roadmap_canon: dict[str, str]` via `_canonicalize_requirement_id(family, raw)` | PASS | Lines 424–437 declare both maps with explicit type annotations and populate via the canonicalizer with family + raw from `requirement_ids` |
| C2 | Iterates roadmap_canon with 3-way partition (exact / canonical-match-surface-differs / canonical-not-in-spec) | PASS | Lines 441–470: (a) exact `raw == spec_canon[canon]` → `continue` (no finding) line 444–445; (b) canonical match, surface differs → MEDIUM `id_schema_drift` finding with mismatch_type, dimension, spec_quote=spec_canon[canon], roadmap_quote=raw lines 446–459; (c) canonical not in spec → HIGH `phantom_id` via `_make_finding` lines 461–470. Severity inheritance comes from SEVERITY_RULES via `_make_finding` (no override). |
| C3 | `findings.extend(phantom_findings)` AND `findings.extend(drift_findings)` both happen | PASS | Lines 471–472: both extends present, in that order |
| C4 | Original raw set-difference `phantom_ids = roadmap_ids - spec_ids` is GONE | PASS | `grep -n "roadmap_ids - spec_ids"` returned no matches in the file |
| C5 | Surrounding code in `check_signatures` (function_missing, param_arity, param_type) NOT modified | PASS | Lines 474–533 — all three sub-checks (`function_missing`, `param_arity_mismatch`, `param_type_mismatch`) bytewise identical to pre-edit baseline; `_route_findings(findings, roadmap_path)` call at line 535 unchanged |
| C6 | Per-patch diff for structural_checkers.py < 30% of total file LOC | PASS | `git diff --numstat` reports 97 added / 16 removed on a 1069-LOC file → 10.57% churn (added+removed)/total. Well under 30%. |

## Summary

- Checks passed: 13 / 13
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (no fixes needed)

## Issues Found

None.

## Actions Taken

None — no fixes required.

## Confidence

- **Verified:** 13/13 | **Unverifiable:** 0 | **Unchecked:** 0 | **Confidence:** 100.0%
- **Tool engagement:** Read: 1 (structural_checkers.py full) | Grep: 3 (id_schema_drift positions, em dash match, raw set-difference removal) | Glob: 0 | Bash: 4 (numstat+wc, grep verifications, em dash byte-check, mkdir+ls)
- All 13 criteria verified with direct tool evidence cited to specific line numbers or grep results. No reliance on agent claims — every assertion was read from the source file or computed from `git diff`.

## Adversarial Spot-Checks (beyond literal criteria)

Performed three additional probes hunting for hidden defects:

1. **Severity inheritance correctness** — `_make_finding` calls in the drift branch (lines 446–459) do NOT pass `severity_override`, so severity flows from `SEVERITY_RULES[("signatures", "id_schema_drift")] = "MEDIUM"` via `get_severity` (line 60, 276). Correct.
2. **Determinism** — iteration order is `sorted(roadmap_canon)` at line 441 (deterministic). `spec_canon` and `roadmap_canon` use "first-seen wins" on canon collisions (lines 429, 436), but iteration of `requirement_ids[family]` and the family list itself is not explicitly sorted at this layer. **Note (non-blocking):** if `spec_parsed.requirement_ids` returns a dict with non-deterministic family order or non-deterministic per-family `ids` iteration order, the first-seen raw on collision could vary across runs. This is not in scope for the Phase 3 acceptance criteria (which call only for canonical-map construction and partition logic), and the spec/research did not flag this. Surfacing as MINOR observation, not a FAIL — would warrant a follow-up if the convergence loop later trips a flaky-determinism gate.
3. **Routing table compatibility** — `("signatures", "id_schema_drift")` is NOT present in `MISMATCH_FILE_ROUTING` (lines 75–95). In `_route_findings` (line 204) `MISMATCH_FILE_ROUTING.get(...)` returns `None` → no `files_affected` set on drift findings → fix_guidance template interpolation still runs (line 211) because that check is independent. **Note (non-blocking):** the drift finding's `files_affected` will be empty unless a downstream layer (Finding constructor default, post-processor) populates it. The Phase 3 acceptance criteria do not require routing-table coverage for `id_schema_drift`; if subsequent phases discover the empty `files_affected` matters for the convergence comparator, a one-line addition to MISMATCH_FILE_ROUTING would resolve it. Surfacing as MINOR observation.

Neither spot-check produces a Phase 3 FAIL — they are forward-looking caveats for future phases.

## Recommendations

- Proceed to Phase 4. Phase 3 is structurally complete.
- (Optional follow-up, not blocking Phase 3) Consider whether `id_schema_drift` should be added to `MISMATCH_FILE_ROUTING` if downstream phases require `files_affected` to be set. Defer until a downstream gate flags it.
- (Optional follow-up, not blocking Phase 3) Consider stabilizing iteration order of `requirement_ids[family]` at the spec_parser layer if convergence determinism becomes a concern.

## QA Complete
