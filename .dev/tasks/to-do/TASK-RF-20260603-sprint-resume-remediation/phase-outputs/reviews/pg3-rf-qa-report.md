# QA Report — Task Integrity Gate (PG-3, F-2 Remediation)

**Topic:** v4.3.5 sprint auto-resume BoundaryIntegrityGate — Finding F-2 (Drift, MED-HIGH): `_detect_partial()` partial-work paths dropped on the default report-only path
**Date:** 2026-06-03
**Phase:** task-integrity (Phase 3 PG-3 review)
**Fix cycle:** N/A (cycle 1)
**Stance:** Adversarial. `fix_authorization: true`.

---

## Overall Verdict: PASS

## Acceptance Checks
| # | Check | Result | Evidence (file:line) |
|---|-------|--------|----------------------|
| 1 | Option A field added & matches §2 verbatim (7 fields) | PASS | `models.py:105` `partial_paths: list[Path] = field(default_factory=list)` placed after `coherence_warnings` (`:99-101`). design.md §2 (`design.md:86-93`) now lists exactly 7 fields — `validated_last, suspects, quarantined, passed, blocking_reasons, coherence_warnings, partial_paths` — name/type/default byte-match the source. No fabrication. |
| 2 | Assignment independent of `cleanup_opted_in` | PASS | `integrity.py:64` `if partial_paths:` → `:71` `report.partial_paths = partial_paths` at the SAME indent as `:72` `if cleanup_opted_in:` (i.e. BEFORE/OUTSIDE the opt-in sub-branch). Runs on the default report-only path. `_quarantine` opt-in unchanged (`:72-73`, body `:218-300`). |
| 3 | Printer surfaces the paths | PASS | `commands.py:538-539` `for p in r.partial_paths: click.echo(...)` inside the `if decision.report is not None:` block (`:520`), beside the `quarantined`/`suspects` loops. Call sites: `commands.py:293` (dry-run) and `:441` (interactive-confirm) — both report-only. |
| 4 | Verdict unchanged (NFR-3) | PASS | `_verdict` (`integrity.py:312-320`) returns `accept_suspect or report.validated_last` — NO `partial_paths` term. `passed` assignment (`:80`) calls `_verdict` only. Field is a pure report surface. |
| 5 | CG-1 RED→GREEN | PASS | `cg1-red.txt:18` `AttributeError: 'BoundaryReport' object has no attribute 'partial_paths'` at `test_resume.py:589`. `cg1-green.txt:13` same test PASSED. Independently re-run: GREEN (4 passed). |
| 6 | `test_boundary_quarantine_nondestructive` non-regressed | PASS | `test_resume.py:552` `assert report.passed is True`, `:550` `assert report.quarantined == {}`, `:553` next_unfinished surfaced. Re-run PASSED. |
| 7 | `--yes`/CI residual documented, not silently expanded | PASS | `f2-yes-ci-residual.md` accurately states the print fix does NOT cover the `--yes`/CI proceed path. Verified against source: `commands.py:469-471` returns `action="proceed"` directly; the proceed branch at `:299-306` does NOT call `_print_resume_decision`. Conditional on CG-4 (PENDING). No unconditional `--yes`-path change made (confirmed: only call sites are `:293` + `:441`). |

## Independent Verification
- **Re-ran** `uv run pytest "tests/sprint/test_resume.py::TestInvariants" -v` → **4 passed** (0.17s). Matches `cg1-green.txt` / `f2-test-summary.md` exactly — no fabricated results.
- **Re-ran** whole module `tests/sprint/test_resume.py` → **19 passed** (0.20s). No collateral regression.
- **Grep-confirmed** `partial_paths` appears in models (`:105`), integrity (`:63,64,71,73`), commands printer (`:538`), and design §2 (`:93`) + §4(b) (`:187`).

## Adversarial Findings (probed, non-blocking)
| # | Severity | Location | Finding | Disposition |
|---|----------|----------|---------|-------------|
| 1 | MINOR (PRE-EXISTING, out of F-2 scope) | `design.md:339` (§8 signatures) | The §8 `BoundaryIntegrityGate.run()` signature lists only `accept_suspect=False` and omits `cleanup_opted_in` (which the actual gate has carried since it was built, `integrity.py:33-39`). §8 is a non-exhaustive "internal helper" sketch. NOT introduced by F-2, NOT a `partial_paths` issue, NOT in the F-2 acceptance set. | Noted only. No fix — outside F-2 scope; touching it would be scope creep. |

## Summary
- Acceptance checks passed: 7 / 7
- Adversarial probes: 1 minor pre-existing doc-drift (out of scope), 0 in-scope issues
- Critical issues: 0
- Issues fixed in-place: 0 (no in-scope defects found)

## Self-Audit
A "0 in-scope issues" verdict here is backed by: independent pytest re-runs (4 + 19 passed, not trusting the summary), line-level reads of all 7 files, grep cross-checks of the NFR-3 invariant (`_verdict` has no `partial_paths` term), and verification that the residual note's "two call sites" claim matches the actual `commands.py` control flow (the `--yes` proceed path at `:469-471`→`:299` genuinely skips the printer). The RED→GREEN transition is real (AttributeError → pass). I probed for the most likely defects (assignment gated by `cleanup_opted_in`; `partial_paths` leaking into `passed`; residual note overclaiming coverage) and found none.

## Confidence
**Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 7 | Grep: 5 | Glob: 0 | Bash: 6 (incl. 2 pytest runs)

## QA Complete

VERDICT: PASS

FIXES APPLIED: none (7/7 acceptance checks passed on first verification; the single adversarial finding is pre-existing §8 doc-shorthand outside F-2 scope, deliberately not fixed to preserve scope discipline)
