# QA Report — Reworked-Test-Integrity Lens (Phase Gate 5)

**Topic:** sc-bare-review M8/M9 migration — reworked-test integrity of `tests/swarm/test_recipe_bare_review.py` (Step 5.2) + research G-1
**Date:** 2026-06-16
**Phase:** report-validation (structural QA — reworked-test-integrity lens)
**Fix cycle:** N/A
**Fix authorization:** FALSE (report only)
**Adversarial stance:** Assumed the reworked test still hard-fails on legacy absence OR silently dropped its legacy-independent coverage. Verified independently with grep + a live pytest run against a tree where the legacy script is already deleted.

---

## Overall Verdict: PASS

The reworked `test_recipe_bare_review.py` has NO remaining runtime dependency on the legacy `t2_normalize.py` script, retains every legacy-independent test named in the verification criteria, and passes cleanly (11 passed, 0 skipped, 0 errored) on a tree where the legacy script is already deleted. The rework approach is documented in the module docstring.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | No `assert LEGACY_SCRIPT.exists()` / no `LEGACY_SCRIPT` constant | PASS | `grep -n "LEGACY_SCRIPT"` → exit 1, ZERO matches. The constant and its `assert` are fully removed. |
| 2 | No `importlib` runtime load of `t2_normalize.py` | PASS | `grep -n "importlib"` → ONLY line 18, inside the module docstring (lines 1-24): "...via importlib) is now provided by the permanent...". Prose, not executable. |
| 3 | No `spec_from_file` load | PASS | `grep -n "spec_from_file"` → exit 1, ZERO matches. |
| 4 | No `scripts/t2_*` runtime dependency | PASS | `grep -n "scripts/"` → exit 1, ZERO matches. `grep -n "t2_"` → lines 4, 18 (docstring) and line 52 (comment `# what ``t2_dispatch`` would have stamped...`). All three are docstring/comment prose; none executable. |
| 5 | `t2_normalize` references are prose-only | PASS | `grep -n "t2_normalize"` → lines 4 and 18, both inside the module docstring block. No import, no `sys.argv`, no `main()` invocation anywhere. |
| 6 | REGISTRY-surface tests present | PASS | `test_registry_resolves_bare_review_v1_to_recipe` (line 118), `test_registry_bare_review_v1_protocol_callable` (line 126) both present and PASSED. |
| 7 | Dispatcher-integration tests present | PASS | `test_dispatcher_routes_success_worker_through_bare_review_v1` (168), `test_dispatcher_promotes_parse_error_via_salvage_flag` (202), `test_dispatcher_keeps_parse_error_when_body_is_unrecoverable` (231) all present and PASSED. |
| 8 | Salvage-flag semantics test present | PASS | `test_recipe_salvage_flag_matches_status_transition` (line 95), parametrized over 5 fixtures, all 5 PASSED. |
| 9 | Duplicates / AC-011 boundary test present | PASS | `test_recipe_preserves_all_findings_including_duplicates` (line 268) present and PASSED. |
| 10 | File passes WITHOUT legacy script present, none SKIPPED | PASS | `ls .../scripts/t2_normalize.py` → "No such file or directory" (script already deleted). `uv run pytest ... -v` → **11 passed in 0.20s**, 0 skipped, 0 errored. Run did not error on the script's absence. |
| 11 | No module-level `pytestmark` skipif (would have hidden coverage) | PASS | `grep -n "pytestmark"` returns nothing relevant; the run reports all 11 tests RUN and PASSED — coverage is live, not skip-masked. |
| 12 | Rework approach documented in module docstring | PASS | Docstring lines 1-24 explain the legacy-independent rework: byte-identity A/B parity (formerly `test_legacy_vs_recipe_byte_identical` via importlib) is now provided by the CLI-vs-frozen-golden gate in `tests/swarm/test_bare_review_parity.py`, "so this file no longer depends on it at run time" (lines 16-23). |
| 13 | Research G-1 disposition matches the actual rework | PASS | G-1 (`research/06-gap-fill-round1.md:9-72`) flagged the hard `assert LEGACY_SCRIPT.exists()` at old line 89 and recommended convert-to-frozen-golden OR delete the legacy-coupled portion. The reworked file took the documented frozen-golden/parity-gate path: the legacy-coupled `test_legacy_vs_recipe_byte_identical` + `_load_legacy` + `_run_legacy` are gone; legacy-independent tests (REGISTRY, dispatcher, AC-011, salvage) remain — exactly the disposition G-1 prescribed. |

---

## Summary

- Checks passed: 13 / 13
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: FALSE)

---

## Confidence

**Verified:** 13/13 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

- Tool engagement: Read: 2 | Grep: 6 (via Bash grep -n) | Glob: 0 | Bash: 3
- Every checklist item maps to a specific grep result, a Read of the named line range, or a line in the captured pytest summary. No UNCHECKED items. No UNVERIFIABLE items. No web research required (all claims are local source-truth).

---

## Issues Found

None.

Adversarial probes that came up clean:
- Hypothesis "the legacy assert was merely converted to a skipif, hiding the coverage": REFUTED — no `pytestmark`, no `skipif`, all 11 tests RUN (not skipped).
- Hypothesis "legacy-independent tests were dropped during rework": REFUTED — all 7 named tests (8 test functions counting the 5-way parametrization) present and passing.
- Hypothesis "a stray `t2_*` runtime reference survives in executable code": REFUTED — the only surviving `t2_`/`importlib`/`t2_normalize` tokens are at lines 4, 18, 52, all in the docstring/comment band; `LEGACY_SCRIPT`, `spec_from_file`, and `scripts/` have ZERO matches.
- Hypothesis "the run errors on the deleted script": REFUTED — `t2_normalize.py` confirmed absent on disk, run completed 11 passed in 0.20s with no collection/import error.

---

## Raw Evidence

### Grep (all run against `tests/swarm/test_recipe_bare_review.py`)

```
grep -n "LEGACY_SCRIPT"   → exit 1 (NO matches)
grep -n "spec_from_file"  → exit 1 (NO matches)
grep -n "scripts/"        → exit 1 (NO matches)
grep -n "importlib"       → 18:``t2_normalize.py`` via importlib) is now provided by the permanent   [docstring]
grep -n "t2_normalize"    → 4:legacy ``t2_normalize.py``):                                          [docstring]
                            18:``t2_normalize.py`` via importlib) is now provided by the permanent   [docstring]
grep -n "t2_"             → 4 (docstring), 18 (docstring), 52 (# comment `t2_dispatch`)
```

### Legacy script absence

```
ls -la src/superclaude/skills/sc-bare-review/scripts/t2_normalize.py
→ ls: cannot access ...: No such file or directory   (exit 2)
```

### Pytest summary

```
uv run pytest tests/swarm/test_recipe_bare_review.py -v
collected 11 items
test_recipe_salvage_flag_matches_status_transition[basic_findings.raw.txt-success]  PASSED
test_recipe_salvage_flag_matches_status_transition[salvage.raw.txt-parse_error]     PASSED
test_recipe_salvage_flag_matches_status_transition[verdict_only.raw.txt-success]    PASSED
test_recipe_salvage_flag_matches_status_transition[freeform_fallback.raw.txt-success] PASSED
test_recipe_salvage_flag_matches_status_transition[odd_cites.raw.txt-success]       PASSED
test_registry_resolves_bare_review_v1_to_recipe                                     PASSED
test_registry_bare_review_v1_protocol_callable                                      PASSED
test_dispatcher_routes_success_worker_through_bare_review_v1                        PASSED
test_dispatcher_promotes_parse_error_via_salvage_flag                               PASSED
test_dispatcher_keeps_parse_error_when_body_is_unrecoverable                        PASSED
test_recipe_preserves_all_findings_including_duplicates                             PASSED
============================== 11 passed in 0.20s ==============================
```

0 skipped. 0 errored. 0 xfailed.

---

## Recommendations

None blocking. The reworked test is integrity-clean for Phase Gate 5: legacy-runtime-independent, fully retains its legacy-independent coverage surface, and is self-documenting. Green light to proceed.

## QA Complete
