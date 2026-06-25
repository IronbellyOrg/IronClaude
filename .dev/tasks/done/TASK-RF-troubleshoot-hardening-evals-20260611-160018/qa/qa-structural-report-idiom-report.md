# QA Report — Structural / run_report.py Idiom Conformance

**Topic:** catch_rate.py + catch_rate_report.py conformance to the run_report.py / models.py RunSummary idiom
**Date:** 2026-06-12
**Phase:** report-validation (structural idiom audit, report-only)
**Fix cycle:** N/A
**Fix authorization:** false (modify NO source file)

---

## Overall Verdict: FAIL

Adversarial stance held. The five required claims were each tested against the
run_report.py / models.py idiom. **3 of 5 claims pass; claim 4 FAILS** (writer
does not guard before `mkdir`), and several additional idiom deviations were
found beyond the five enumerated checks. Per "any issue = FAIL", the top-line
verdict is FAIL.

---

## Items Reviewed (the 5 required VERIFY claims)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | EscapeResult + CatchRateReport are `@dataclass(frozen=True)` with explicit `_*_FIELDS` ordering tuples | PASS | `catch_rate.py:62` `@dataclass(frozen=True)` on `EscapeResult`; `catch_rate.py:122` `@dataclass(frozen=True)` on `CatchRateReport`. Tuples: `_ESCAPE_RESULT_FIELDS` `catch_rate.py:39-46`, `_CATCH_RATE_FIELDS` `catch_rate.py:48-59`. Mirrors models.py:74/835 + `_EVAL_OUTCOME_FIELDS`/`_RUN_SUMMARY_FIELDS`. |
| 2 | `to_dict()` walks the field tuple (single serialization SoT), unwrapping nested escapes via their own `to_dict()` | PASS | `CatchRateReport.to_dict` `catch_rate.py:195-204` iterates `_CATCH_RATE_FIELDS`; `name == "escapes"` branch (`:200-201`) does `[item.to_dict() for item in value]`, calling `EscapeResult.to_dict` (`catch_rate.py:99-100`). Mirrors `RunSummary.to_dict` models.py:935-945 evals branch. |
| 3 | The renderer (`render_catch_rate_json`) calls the invariant guard (`_check`) BEFORE any `json.dumps` | PASS | `render_catch_rate_json` `catch_rate_report.py:64-70`: `_check(report)` at line 66 precedes `json.dumps(...)` at line 68. Mirrors `render_summary_json` run_report.py:244-246 (`_check_invariant` before `json.dumps`). Also holds in markdown renderer (`_check` at `:75`). |
| 4 | The writer never leaves a partial artifact on a broken invariant (guard runs before write) | **FAIL** | `write_catch_rate_report` `catch_rate_report.py:113-114` runs `out.mkdir(parents=True, exist_ok=True)` with **no top-of-writer `_check(report)` call** before it. The idiom source guards at the TOP of the writer entrypoint: `write_aggregated_report` run_report.py:438 calls `_check_invariant(summary)` BEFORE `_write_artifact_set` (which mkdirs). See Issue #1 for the partial-artifact consequence. |
| 5 | `CatchRateContractViolation` maps to exit code 2 (constant analogous to run_report.py:78) | PASS (value) / see Issue #2 (idiom deviation) | `CATCH_RATE_CONTRACT_VIOLATION_EXIT_CODE = 2` `catch_rate_report.py:23`; `CatchRateContractViolation` docstring `:36` names it. Value 2 is correct and matches `exit_codes.USAGE_ERROR = 2` (exit_codes.py:23, verified). However the constant is a **hardcoded literal**, not sourced from the canonical SoT the way run_report.py:56 does (`= _exit_codes.USAGE_ERROR`) — and is **untyped**. See Issue #2. |

---

## Summary

- Required VERIFY claims passed: 4 / 5 (claim 5 value-correct; claim 4 fails)
- Required VERIFY claims failed: 1 (claim 4)
- Additional idiom deviations found (beyond the 5): 4
- Critical issues: 1 (Issue #1 — partial-artifact / guard placement)
- Issues fixed in-place: 0 (report-only, fix_authorization: false)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | `catch_rate_report.py:113-126` (`write_catch_rate_report`) | **VERIFY-4 FAIL — guard does not run before the writer mkdirs.** The writer calls `out.mkdir(parents=True, exist_ok=True)` (`:114`) with no preceding `_check(report)`. The invariant only fires later, inside `render_catch_rate_json` (`:66`) at the moment of the first `write_text` (`:118`). The idiom (`write_aggregated_report` run_report.py:438) guards at the TOP of the writer, BEFORE `_write_artifact_set`'s `out.mkdir` (run_report.py:389). Consequence: on a broken invariant the directory is created (a side-effect/partial artifact the idiom avoids), and — more seriously — if `emit_md=True` and only the `.json` render raised, the writer is non-atomic by construction; here the json renders first so the dir+nothing is the realized partial state. The class docstring (`:106` "Guard-then-write") and module docstring (`run_report.py:366-439` mirror claim) assert guard-then-write, but the guard is write-time, not writer-entry-time. | Add `_check(report)` as the first statement of `write_catch_rate_report` (before `Path(output_dir)`/`mkdir`), mirroring run_report.py:438. |
| 2 | IMPORTANT | `catch_rate_report.py:23` | **Exit-code constant deviates from idiom (VERIFY-5 caveat).** `CATCH_RATE_CONTRACT_VIOLATION_EXIT_CODE = 2` is a **bare hardcoded literal** and is **untyped**. run_report.py:56 sources its value from the canonical SoT (`REPORTER_CONTRACT_VIOLATION_EXIT_CODE: int = _exit_codes.USAGE_ERROR`) and annotates `: int`. Hardcoding 2 silently diverges if exit_codes.py ever re-numbers USAGE_ERROR. Value is currently correct (2 == exit_codes.USAGE_ERROR, verified exit_codes.py:23). | Source from `exit_codes.USAGE_ERROR` and add `: int` annotation. (Note: catch_rate_report.py lives under `tests/`, so importing the eval exit_codes module is a cross-package coupling decision — if that import is undesirable, at minimum annotate `: int` and add a comment pinning it to `exit_codes.USAGE_ERROR`.) |
| 3 | IMPORTANT | `catch_rate_report.py:31-42` (`CatchRateContractViolation`) vs `catch_rate.py:142-177` (`CatchRateReport.__post_init__`) | **The writer's contract-violation exception is structurally UNREACHABLE — guard is redundant, not defense-in-depth as claimed.** `_check` (`:45-61`) re-validates exactly two conditions: `caught + missed == total_escapes` and `len(escapes) == total_escapes`. But `CatchRateReport.__post_init__` (`catch_rate.py:142-154`) already raises `ValueError` on BOTH of those at construction time — and the dataclass is frozen, so no field can change between construction and the write. Therefore `_check` can never raise `CatchRateContractViolation` for any constructible `CatchRateReport`. In run_report.py the analogous `_check_invariant` IS reachable because `RunSummary.__post_init__` (models.py:905-921) does NOT validate `len(evals) == expanded_n_prime` (the docstring at models.py:877-880 explicitly defers it to the writer so partial SIGINT summaries can be constructed). The catch_rate model moved that invariant INTO `__post_init__`, which makes the mirrored writer guard dead code. The `:46` docstring "defense in depth" overstates an unreachable path. | Either (a) document that `_check` is belt-and-suspenders for the frozen model (lower the "defense in depth" claim), or (b) relax the model `__post_init__` count checks to match the run_report.py division of responsibility if partial/under-construction reports are a real use-case. Not a correctness bug, but an idiom-fidelity gap that the surrounding docstrings misrepresent. |
| 4 | MINOR | `catch_rate_report.py:64-97` (renderers) vs `catch_rate.py:195-204` | **Renderer does not re-route through a serialization SoT helper the way the idiom layers it.** Minor: `render_catch_rate_json` calls `report.to_dict()` directly (fine, that IS the SoT). Flagged only because the markdown renderer (`:73-97`) hand-reads fields (`report.caught`, `e.card_path`, etc.) rather than going through `to_dict()` — consistent with run_report.py's `render_summary_markdown` (run_report.py:141-225 also hand-reads), so this is idiom-CONSISTENT and NOT a deviation. Recorded to show the markdown path was checked and cleared. | None — consistent with idiom. |
| 5 | MINOR | `catch_rate_report.py:100-126` (`write_catch_rate_report`) | **No consolidated `_write_artifact_set`-style helper / no injected-renderer seam.** run_report.py factors writing into `_write_artifact_set` (run_report.py:366-410) with injectable renderer callables so `Reporter.write` and `write_aggregated_report` share one emit layer. catch_rate_report.py inlines the two `write_text` calls directly in the writer. This is acceptable for a single-writer module (no second caller exists), so it is a scope-appropriate simplification, not a defect — but it IS a structural divergence from the cited idiom triad and the writer is consequently non-atomic (no all-or-nothing across the 2 files). | Optional: only matters if a second writer/emitter is added later. Combined with Issue #1, consider guarding once at entry so neither file is touched on a bad invariant. |

## Actions Taken

None. Report-only run (`fix_authorization: false`); no source file modified.

## Recommendations

1. **Blocking (CRITICAL):** Move the invariant guard to the first line of `write_catch_rate_report` (mirror run_report.py:438) so the directory is never created and no file is written on a broken invariant. This is the literal VERIFY-4 requirement.
2. **IMPORTANT:** Resolve the dead-guard contradiction (Issue #3) — the writer's `CatchRateContractViolation` is currently unreachable because the frozen model already enforces both checks in `__post_init__`; either soften the "defense in depth" docstring or realign the model/writer division of responsibility with run_report.py.
3. **IMPORTANT:** Annotate `CATCH_RATE_CONTRACT_VIOLATION_EXIT_CODE: int` and pin it to `exit_codes.USAGE_ERROR` (by import or comment) so the value cannot silently drift (Issue #2).

## Confidence Gate

**Confidence:** Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

All five VERIFY claims were checked with direct tool evidence (file:line), and the run_report.py idiom source + exit_codes.py SoT were read in full to ground each comparison. Each checklist item maps to a specific Read of the cited lines.

**Tool engagement:** Read: 5 | Grep: 1 | Glob: 0 | Bash: 2 (exit_codes read + grep) — total ≥ 5 required claims.

No web research performed (all claims are intrinsically local source-truth; Principle 6 / Tavily-first not triggered).

## QA Complete
