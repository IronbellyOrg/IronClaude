# QA Report — Task Integrity (Phase 2, F-3 Remediation)

**Topic:** v4.3.5 sprint auto-resume DriftAssessor — Finding F-3 (same-ID material edit silently resumed)
**Date:** 2026-06-03
**Phase:** task-integrity (adversarial)
**Fix cycle:** 1
**Fix authorization:** true

---

## Overall Verdict: PASS

The principled WS-normalized-hash fix is implemented exactly as designed across all four code/test files, RED→GREEN evidence is genuine, and the design amendment matches the code. Four MINOR documentation defects (stale `executor.py` line citations in `design.md` that predated the F-3 additions and no longer covered the new `tasklist_sha256_ws` field) were found and FIXED in-place. No code, test, or behavioral defects found.

## Acceptance Checks (each verified, file:line)

| # | Acceptance check | Result | Evidence |
|---|------------------|--------|----------|
| 1 | Principled, not a bare branch flip | PASS | `drift.py:186-219` — fall-through reads `_recorded_sha_ws`/`_current_sha_ws`, keeps 0.9/cosmetic ONLY when `recorded_ws and current_ws and recorded_ws == current_ws` (`:188`), else `confidence=0.5, cosmetic_only=False` (`:200-219`). NOT a blanket `<0.8` — the AC-4 cosmetic path is preserved by the equality gate. |
| 2 | AC-4 provably non-regressed | PASS | `test_drift_trailing_whitespace_high_conf` asserts `>=0.8` + `cosmetic_only is True` + `tier != "hash"` (`test_resume.py:259-267`). `_build_task_interrupted` co-edit persists `rj["tasklist_sha256_ws"]` of the recorded body (`test_resume.py:217`) so the WS-missing fallback does NOT fire. Direct-exec confirmed `_normalize_whitespace("_P3") == _normalize_whitespace("_P3" + "   \n")` is True, and realistic body+trailing-ws case equal. |
| 3 | AC-5 same-ID material edit now <0.8 | PASS | `test_drift_same_id_material_body_edit_low_conf` (`test_resume.py:286-307`) asserts `<0.8` + `cosmetic_only is False`. Direct-exec confirmed the CG-2 deliverable-block edit's WS-normalized hash DIFFERS from recorded `_P3` WS hash (True), so the `<0.8` branch genuinely fires. |
| 4 | Backward-compatibility | PASS | `_recorded_sha_ws` returns None on absent field via `payload.get("tasklist_sha256_ws")` + `(OSError, ValueError)` catch (`drift.py:324-343`); None ⇒ `if recorded_ws and ...` False ⇒ `confidence=0.5` branch, no crash. `test_drift_missing_recorded_hash_no_crash` PASSES (`test_resume.py:319-325`). |
| 5 | NFR-3 — git NEVER gates | PASS | `_annotate_git` (`drift.py:259-306`) mutates ONLY `changed_paths` (`:302`) and `tier` (`:305`); `.confidence` does NOT appear in the function body (direct source-string check True). F-3 decision is entirely in deterministic Tier-0/1. |
| 6 | CG-2 RED-then-GREEN | PASS | `cg2-red.txt:18` shows `AssertionError: assert 0.9 < 0.8` (`confidence=0.9, cosmetic_only=True` — the exact F-3 defect). `cg2-green.txt:14` shows the same test PASSED (6 passed). Genuine RED→GREEN. |
| 7 | Design amendment matches code | PASS (after fix) | §2 note (`design.md:95-106`) and §5 DD-4 amendment (`design.md:251-262`) describe `tasklist_sha256_ws` exactly as implemented. Field semantics correct, no fabrication. FOUR stale `executor.py` line citations were the only defect — FIXED. |

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | `rerun_tasks.py` new helpers | PASS | `_normalize_whitespace` (`:704-718`) collapses intra-line ws via `" ".join(line.split())`, drops trailing blank lines, preserves interior blanks. `_content_sha256_ws_excluding_rerun_block` (`:721-738`) reuses `_split_rerun_block` then hashes normalized content. Both adjacent to existing `_content_sha256_excluding_rerun_block` (`:688-701`). |
| 2 | `executor.py` persists `tasklist_sha256_ws` | PASS | `_write_phase_result_json` (`:2053-2095`); payload dict (`:2079-2090`) emits `tasklist_sha256` (`:2087`) and `tasklist_sha256_ws` (`:2089`) via imported helpers (`:2074-2077`). Atomic tmp+replace write preserved (`:2093-2095`). |
| 3 | `drift.py` rewritten fall-through + readers | PASS | Fall-through (`:177-219`) WS-hash-gated; `_current_sha_ws` (`:241-248`) and `_recorded_sha_ws` (`:324-343`) added; both use the same writer fn. Tier-0 (`:46-55`) and `_annotate_git` (`:259-306`) untouched in semantics. |
| 4 | `test_resume.py` CG-2 test + builder co-edit + import | PASS | New import (`:24-27`); `_build_task_interrupted` co-edit persists `tasklist_sha256_ws` (`:217`); CG-2 test `test_drift_same_id_material_body_edit_low_conf` (`:286-307`). |
| 5 | f3-test-summary.md + raw outputs | PASS | Summary matches actual pytest output (6 passed, RED→GREEN narrative accurate). `cg2-red.txt`/`cg2-green.txt` present and consistent. |
| 6 | design.md §2 + §5 DD-4 amendment | FIXED | Field semantics correct; 4 stale `executor.py` line citations corrected in-place. |
| 7 | Independent suite re-run (UV) | PASS | `TestDriftAssessor` 6/6; full `test_resume.py` 18/18; ruff clean; `make verify-sync` clean. |

## Summary

- Acceptance checks passed: 7 / 7 (check 7 after in-place fix)
- Items reviewed passed: 7 / 7
- Critical issues: 0
- Important issues: 0
- Minor issues: 4 (all stale doc line citations) — ALL FIXED in-place
- Issues fixed in-place: 4

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | MINOR | `design.md:96` (§2 hash-fields note) | Cited `executor.py:2053-2072` for `_write_phase_result_json`; function is actually `2053-2095` and the new `tasklist_sha256_ws` field is at `:2089`, OUTSIDE the cited range — a reader following the citation would not find the field. | Update to `2053-2095`, payload `2079-2090`, with field anchors `:2087`/`:2089`. |
| 2 | MINOR | `design.md:243` (§5 DD-4 storage note) | Cited `executor.py:2053-2072` + payload `:2059-2067`; both stale. | Update to `2053-2095` + payload `2079-2090`. |
| 3 | MINOR | `design.md:136` (control-flow pseudocode) | Result-JSON schema cited as `executor.py:2059-2067`; stale. | Update to `2079-2090`. |
| 4 | MINOR | `design.md:153` and `:385` (evidence-trail refs) | Result-JSON schema/writer cited as `executor.py:2053-2072`; stale. | Update both to `2053-2095`. |

Note: these are citation-accuracy defects only. The field's NAME, SEMANTICS, persistence-alongside behavior, and absence⇒<0.8 fallback are all described correctly in the prose — no fabrication of behavior (acceptance check 7). They were the *only* defects found in the entire F-3 remediation.

## Actions Taken (fix-authorized)

- Fixed `design.md:96` — citation `executor.py:2053-2072` → `2053-2095` (payload `2079-2090`, fields `:2087`/`:2089`). Verified by `grep` of the actual function span (`def` at 2053, closing `}` at 2090, function end 2095).
- Fixed `design.md:243` — `2053-2072` + `2059-2067` → `2053-2095` + `2079-2090`.
- Fixed `design.md:136` — schema citation `2059-2067` → `2079-2090`.
- Fixed `design.md:153` and `:385` — `2053-2072` → `2053-2095`.
- Re-verified post-fix: `grep -n "2053-2072\|2059-2067"` over `design.md` returns no matches (zero stale citations remain).
- Re-ran `TestDriftAssessor` after doc edits: 6/6 PASS (docs-only edits, no test impact, as expected).

## Adversarial probes that did NOT surface defects (anti-rubber-stamp evidence)

- Confirmed the fix is principled, not a bare branch flip — the 0.9 cosmetic path survives via the WS-hash equality gate; a naive blanket `<0.8` would have regressed AC-4 but was NOT done (`drift.py:188`).
- Independently recomputed both WS hashes (not trusting the test): CG-2 edited body DIFFERS from baseline (so `<0.8` fires), AC-4 trailing-ws body MATCHES baseline (so 0.9 kept). Test assertions are not vacuous.
- Confirmed the AC-4 builder co-edit is load-bearing: without persisting `tasklist_sha256_ws` of the recorded body, AC-4 would hit the WS-missing fallback and fail — the test summary's claim is correct.
- Confirmed `_annotate_git` cannot influence the verdict (`.confidence` absent from its body) — NFR-3 holds; no git dependency leaked into the F-3 decision.
- Confirmed backward-compat None path scores `0.5` (conservative <0.8), never crashes — verified the guard logic, not just the test name.
- Confirmed RED transcript shows the EXACT defect signature (`0.9 < 0.8`, `cosmetic_only=True`) — the RED was real, not a contrived failure.

## Confidence

**Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

**Tool engagement:** Read: 9 | Grep: 1 | Glob: 0 | Bash: 8

All 7 acceptance checks and all 7 reviewed items carry tool-cited evidence (Read of every file in scope + independent Bash exec of `_normalize_whitespace`/WS-hash semantics + independent UV suite re-run + ruff + verify-sync). No unverifiable or unchecked items. No web research performed (entirely source-truth-local). Tool-call count (18) exceeds the 7-item checklist minimum.

## Recommendations

- Phase 2 F-3 remediation is sound and may proceed. No follow-up required.
- The 4 fixed doc citations are committed as part of this QA pass; no further doc work needed.

## QA Complete

---

VERDICT: PASS

FIXES APPLIED:
- `design.md:96` — `executor.py` citation `2053-2072` → `2053-2095` (payload `2079-2090`, fields `:2087`/`:2089`)
- `design.md:243` — `2053-2072` + payload `2059-2067` → `2053-2095` + `2079-2090`
- `design.md:136` — result-JSON schema citation `2059-2067` → `2079-2090`
- `design.md:153` + `design.md:385` — `2053-2072` → `2053-2095`
