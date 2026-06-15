# QA Report — Task Integrity (Scoped Graft Re-Verification)

**Topic:** Differential Backtest/Eval Harness — surgical graft of Waiver re-green meta-scenario (Step 4.7b) + E2 digit-heading CAVEAT (Step 4.4)
**Date:** 2026-06-11
**Phase:** task-integrity (structural lens, scoped to grafted items ONLY)
**Fix authorization:** false (report-only)
**Lens:** structural — verify the 5 changed items did not break invariants
**Stance:** ADVERSARIAL (assumed ≥3 structural defects on entry)

Scope of re-verification (changed items only):
1. Step 4.4 (E2 runner) — inserted digit-heading-trap CRITICAL FIXTURE CAVEAT
2. Step 4.7b (NEW) — Waiver re-green meta-scenario runner
3. Step 4.8 (aggregation) — waiver-exclusion clause
4. Phase 4 heading — "(E1-E5 + Waiver re-green)"
5. OQ-3 — waiver exclusion documentation

NOT re-verified: the other 73 previously-validated items (out of scope per spawn instruction).

---

## Overall Verdict: PASS (with 1 MINOR graft-completeness gap — non-blocking)

---

## Items Reviewed

| # | Structural check | Result | Evidence |
|---|------------------|--------|----------|
| 1 | B2 self-containment — Step 4.4 (post-edit) | PASS | L336: single self-contained item. Context (read `research/05-replay-targets.md` E2 + replay-table + git_replay + _impl_guard, with rationale), Action (create `test_backtest_e2.py` with OLD=MISS test (a) + NEW=CATCH proxy (b) + inserted digit-heading CAVEAT), Output (`tests/troubleshoot/backtest/test_backtest_e2.py`), Verification (`from __future__` first, OLD=MISS impl-independent, NEW=CATCH skip-guarded, bare sha, distinct fn names, 1:1 §8.3 E2), Completion gate present. CAVEAT did NOT split the item across checkboxes. |
| 2 | B2 self-containment — Step 4.7b (NEW) | PASS | L352: single self-contained item. Context (read deepdive §5.4/§4.5 + FR-12 + NFR-4 + §8.3 row + guard module, with rationale), Action (create `test_waiver_regreen.py` with one guarded test + DESIGN NOTE), Output (`tests/troubleshoot/backtest/test_waiver_regreen.py`), Verification (`from __future__` first, `requires_impl_ref`-guarded NOT importorskip/xfail/try-except, distinct fn name, 1:1 §8.3 waiver row + FR-12), Completion gate present. All five facets present. |
| 3 | Placeholder scan (TB-Add-1) | PASS | grep over changed lines 320,334-336,350-356,524-528 for TBD/TODO/FIXME/{UPPER}/XXX → NO matches. Both 4.4 and 4.7b have full bodies (no title-only items). |
| 4 | No `^` caret on any parent sha | PASS | grep `[0-9a-f]{7,}\^` / `\^[0-9]` over 334-336,350-356 → none. Step 4.4 states "bare parent sha"; 4.7b has no parent sha (verdict-state assertion, no replay locus). G1 intact. |
| 5 | Skip-guard correctness (4.7b) | PASS | L352 names importorskip/xfail/try-except ONLY in the prohibition. Mechanism = `requires_impl_ref("hardening-output-contract.md")`. Helper EXISTS: Step 4.1 (L324) item (5) defines `requires_impl_ref(ref_filename)` in `_impl_guard.py`. Order 4.1 < 4.7b — defined before use. |
| 6 | Numbering / DAG | PASS | Step 4.8 (L356) refs "the 5 per-escape runners" + "EXACTLY the five E1-E5 records" — waiver excluded, no contradiction. Step 4.QA.2 (§8.3 mapping, L367) scopes to "each of E1-E5". Heading (L320) → "(E1-E5 + Waiver re-green)". Overview bullet #4 (L78) "one per escape, E1-E5" unchanged & correct. No broken reference. |
| 7 | Invariant non-regression (catch_rate / total_escapes==5) | PASS | Model (Step 3.2 L280 / 3.QA.2 L284): `CatchRateReport` + `_derive_backtest_status` over E1-E5. Step 4.8 (L356): waiver "EXCLUDED … `total_escapes == 5`, model and invariant unchanged". OQ-3 (L528): "denominator stays `total_escapes == 5`". grep for "6 escape / total_escapes == 6 / all 6" → NONE. No item implies 6 records feed the report. |
| 8 | Collision boundary intact | PASS | grep `test_waiver_regreen.py` = 1 (only 4.7b). grep `test_waiver_latch_one_way_blocks_downstream_regreen` = 1 (unique fn). `test_hardening_verdict.py` appears only as the impl-side collision note; no backtest item writes it (`Create.*test_hardening_verdict` = 0). Backtest under `tests/troubleshoot/backtest/`; impl owns `tests/troubleshoot/`. No overlap. |
| 9 | CAVEAT factual accuracy (independent source check) | PASS | `git show 10723863:src/superclaude/cli/prd/gates.py`: `_check_parallel_instructions` L197, regex `Phase\s+(\d+)` L207, `int(m.group(1)) >= 2` L212, `if not later_phases: return True`. CAVEAT claims ("~L207", digit-only, literal `Phase N` never matches → returns True → OLD=MISS goes RED) are exact. Fixture prescription (digit ≥2 final phase w/o keyword, preceded by an earlier phase WITH a keyword) is correct against the first-miss-returns loop semantics. |

---

## Summary

- Structural checks passed: 9 / 9
- Structural checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 1 (graft-completeness gap in the Phase 4 QA gate inventory — see below)
- Issues fixed in-place: 0 (fix_authorization: false — report-only)

All 7 spawn-prompt structural checks PASS. The 3 adversarially-assumed defects were NOT found; the graft is structurally sound. One MINOR completeness gap surfaced that is adjacent to the graft (the inventory enumeration was not extended), documented below — it does not break any invariant and does not block.

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | MINOR | Step 4.QA.1, L362 (Phase 4 QA gate inventory) | The inventory item enumerates Phase 4 deliverables as `_impl_guard.py, test_path_resolution.py, test_backtest_e1.py … test_backtest_e5.py, test_catch_rate_aggregation.py` and its completion criterion is "ensuring all 5 per-escape runners + the guard + path + aggregation files are included". The grafted Step 4.7b deliverable `test_waiver_regreen.py` is NOT in this enumeration, and "If a Phase 4 file is missing" would not trip for it. The "Use Glob to find all" phrasing means a directory glob would physically discover the file, but the explicit completeness assertion does not require it — so the waiver runner could be silently omitted from the inventory record. Note this is the inventory lens only; Steps 4.QA.2/4.QA.4 (§8.3 mapping, aggregation) are CORRECTLY scoped to E1-E5 and intentionally exclude the waiver, so no contradiction exists there. | Add `.../test_waiver_regreen.py` to the L362 enumeration and append "+ the waiver re-green meta-scenario runner (Step 4.7b, single `requires_impl_ref`-guarded test, EXCLUDED from catch_rate)" to the completion criterion. OPTIONAL/non-blocking: the graft author may have deliberately left the inventory E1-E5-scoped; if so, no action needed. Cosmetic completeness only — does not affect any invariant or the green-now DOD. |

## Actions Taken

None — `fix_authorization: false`. Report-only.

## Recommendations

- The graft is structurally sound; PROCEED is warranted on the structural lens.
- OPTIONAL (MINOR, non-blocking): extend the Step 4.QA.1 inventory enumeration (L362) to name `test_waiver_regreen.py` so the Phase 4 inventory record is complete. This is the only graft-adjacent loose end; it does not gate execution.
- No skip-guard, collision, caret, denominator, or DAG defect was found. The digit-heading CAVEAT is factually correct against the live parent source at `10723863`.

---

## Confidence

- **Confidence:** "Verified: 9/9 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%"
- **Tool engagement:** "Read: 4 | Grep: 6 | Glob: 0 | Bash: 6"
- No UNCHECKED items. No UNVERIFIABLE items. Each check maps to a specific tool action (Read of the changed item lines; Grep for placeholders/carets/collision/denominator; `git show` of the parent commit for the CAVEAT). Tool-call count (≥10 verification actions) exceeds the 9 structural checks — engagement minimum satisfied, no padding.
- No web research was required (all claims verified against local source + git history; source-truth-first per Principle 6).

## QA Complete

**VERDICT: PASS** — graft is structurally sound; all 7 spawn checks PASS; 1 MINOR non-blocking inventory-completeness gap documented (Step 4.QA.1 enumeration omits `test_waiver_regreen.py`).
