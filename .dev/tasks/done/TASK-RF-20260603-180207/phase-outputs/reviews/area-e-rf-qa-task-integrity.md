# QA Report — Task Integrity (Area E)

**Topic:** Area E — registry-writer removal (e1), remediate_parser deletion (e2), MD-family verify (e3)
**Date:** 2026-06-03
**Phase:** task-integrity
**Fix cycle:** N/A (no findings — no fix cycle entered)
**Stance:** ADVERSARIAL (assume wrongful deletion until evidence proves otherwise)
**fix_authorization:** true (no revert needed — see verdict)

---

## Overall Verdict: PASS

Every Area-E claim independently re-verified with actual `git`/`grep`/`pytest` commands (zero-trust — markers/aggregation NOT taken at face value). No wrongful deletion, no stranded reader, no removed shim, no mis-recorded prerequisite. ANY-severity finding would have forced FAIL; there are zero findings of any severity in Area E's scope.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| a1 | e1 HALTED, writer `_save_id_registry` NOT deleted | PASS | `grep` executor.py → `def _save_id_registry` at L611; persists `spec_id_registry.json` at L650; still called at L1396. Intact. |
| a2 | e1 reader `gates.py:_roadmap_ids_within_spec` NOT modified, still reads JSON sidecar | PASS | `git diff HEAD --stat -- gates.py` → EMPTY (byte-unchanged). `grep` gates.py: `_roadmap_ids_within_spec` at L996; `_id_registry_sidecar_path.read_text()` at L1021; reconstructs `SpecIdRegistry` at L1034; fail-closed at L1013-1018. |
| a3 | e1 prerequisite (reader-repoint via `verify_implementation.py` template) correctly documented | PASS | `verify_implementation.py:assert_all_frs_resolved` at L51 reads `envelope.spec_ids.fr_ids` via accessor (L95 `# ACCESSOR — never subscript`) + `accepted_deviation_ids` (L120). Matches e1 marker's cited template exactly. |
| a4 | e1 cutover counters NOT-MET ground recorded | PASS | e1 marker cites `r1-4-cutover-counters.yaml` 13 steps at 0/3 `cutover_eligible:false`. Consistent with HALT; reader is the harder of the two HALT grounds and is code-verified above. |
| b1 | e2 `remediate_parser.py` still EXISTS | PASS | `test -f` → EXISTS: YES. |
| b2 | e2 `remediate_parser.py` untouched | PASS | `git diff HEAD -- remediate_parser.py` → EMPTY. |
| b3 | e2 the 3 calling test files exist + untouched | PASS | `test -f` all 3 EXIST; `grep -l remediate_parser` matches all 3; `git diff HEAD --stat` on all 3 → EMPTY. |
| b4 | e2 zero production callers claim accurate | PASS | `grep -rn remediate_parser src/` (excl. self) → single hit `remediate.py:22` docstring bullet; no `from .remediate_parser import` / `remediate_parser.` call anywhere in `src/`. |
| c1 | e3 MD-family guard `test_all_schemas_accept_md_family` passes (4 params) | PASS | `uv run pytest -k test_all_schemas_accept_md_family` → 4 passed (extract/extract_tdd/generate/merge). |
| c2 | e3 6-file MD-family suite passes (187/1 claim) | PASS | Ran the exact 6 files → **187 passed, 1 skipped** — byte-matches e3 summary. |
| c3 | e3 back-compat `.get("md_ids", ())` shims NOT removed | PASS | `grep` gates.py:1041 `md_ids=tuple(payload.get("md_ids", ()))`; envelope.py:388 `md_ids=tuple(spec_ids_d.get("md_ids", ()))`. Both present. |
| d1 | No Area-E production-code deletion in `git status` | PASS | `git status --short`: the only deletion `D tests/integration/test_wiring_pipeline.py` is attributed to **Area A** (re-homed AST assertion in `test_wiring_gate.py` docstring: "removed in Area A"), NOT Area E. Area-E items e1/e2/e3 are verify/HALT-only. See Cross-Area Note. |
| d2 | executor.py changes are Area B (phantom-ID) + Area C (comment) only — NOT writer/reader edits | PASS | `git diff executor.py`: hunk 1 repoints generate-step source from `extraction.json`→`spec_id_registry.json` with fail-shut (Area B phantom-ID, L1273+); hunk 2 is the Area C 600s-inert comment. Neither touches `_save_id_registry` (L611) nor the reader. |

## Summary

- Checks passed: 13 / 13
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (none required)

## Cross-Area Note (informational — outside Area-E scope, NOT a finding)

The Area-E aggregation states "(iv) NO production code deleted or modified **in this phase**." `git status` shows changes the aggregation did not enumerate: `id_registry.py` (+`from_payload` classmethod, Area B — the shared registry reconstruction, with the `md_ids` `.get(..., ())` shim PRESENT at the new code), `tool_writer.py` (+`require_spec_ids` guard, Area B phantom-ID), `executor.py` (Area B+C, verified above), `tests/audit/test_wiring_gate.py` (+re-homed NFR-007 AST test), and the deletion `tests/integration/test_wiring_pipeline.py` (Area A). These are **other Areas of the same multi-area task** (A/B/C), not Area-E damage. The Area-E aggregation's "this phase" claim is scoped to Area E's own e1/e2/e3 items, which are verify/HALT-only and touched nothing — so the claim is accurate for its scope. The deleted wiring test's assertion was preserved (re-homed to `test_wiring_gate.py::test_no_pipeline_imports_in_wiring_gate`), so even that Area-A deletion is non-destructive. No action needed; flagged only for orchestrator awareness when merging cross-area reviews.

## Issues Found

None. (Adversarial hypotheses tested and refuted: writer-deletion → refuted by L611 grep; reader-stranding → refuted by empty gates.py diff; shim-removal → refuted by gates.py:1041 + envelope.py:388 grep; prerequisite mis-record → refuted by verify_implementation.py:95 accessor; parser deletion → refuted by `test -f` + empty diff.)

## Actions Taken

None. No revert required — no wrongful deletion exists. (fix_authorization was true; it went unused because the work is clean.)

## Confidence Gate

- **Confidence:** "Verified: 13/13 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%"
- **Tool engagement:** "Read: 4 | Grep: 6 | Glob: 0 | Bash: 9"
  - (Bash count includes the git-diff, git-status, grep-in-bash, test -f, and pytest invocations; each maps to a specific check row above. Tool calls ≥ checklist items — not suspect.)
- Unchecked items: none.
- Unverifiable items: none.
- Web research: none performed (all claims are local source-truth; no external lookup applicable).

## Recommendations

- Green light: Area E is clean. e1 (writer-removal) and e2 (parser-deletion) correctly remain HALTED/DEFERRED behind their cutover + reader-repoint preconditions; e3 (MD-family) is green with shims preserved.
- When the orchestrator merges cross-area reviews, fold in the Cross-Area Note so the Area-A wiring-test deletion and Area-B `from_payload`/`require_spec_ids` additions are accounted for under their own area gates (they are out of Area-E scope and verified non-destructive here).

## QA Complete
