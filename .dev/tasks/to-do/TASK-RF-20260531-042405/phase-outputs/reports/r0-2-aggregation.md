# R0.2 Aggregation Report — Anti-Instinct Allowlist (Contract #10)

**Phase:** 3 Phase Gate (PG3.1)
**Commit:** `f41ea931` on `refactor/roadmap-pipeline-r0-r1-rewrite`
**Worktree:** `/config/workspace/IronClaude-RoadmapRewrite/`

## Phase-output files (with sizes + one-line summary)

| File | Size | Summary |
|---|---|---|
| `phase-outputs/discovery/multimodelswarm-fp-seeds.md` | 6.7 KB | Step 3.1 — verbatim enumeration of the 6 MultiModelSwarm FP instances at roadmap.md L207/L211/L213, each mapped to a SCAFFOLD-term match + Layer that fired + proposed allowlist entry. |
| `phase-outputs/plans/r0-2-allowlist-design.md` | 8.7 KB | Step 3.2 — design rationale for the NEW `_ALLOWLIST_PHRASES` mechanism (chosen over extending `_DESCRIPTOR_NOUNS` / `_DEMOTED_H3_SUBSECTIONS`), integration point in `scan_obligations`, planned tests, non-widening confirmation, R1.3 forward-compatibility note. |
| `phase-outputs/test-results/r0-2-pytest-output.txt` | 18 KB | Step 3.6 — raw pytest output for the 5-file obligation_scanner suite. |
| `phase-outputs/test-results/r0-2-pytest-summary.md` | 6.2 KB | Step 3.6 — structured summary: 134 passed / 1 skipped / 0 failed. 7 new Contract #10 tests all PASS. 12 wider-suite failures confirmed pre-existing (unrelated). |
| `phase-outputs/test-results/r0-2-lint-format-summary.md` | 1.3 KB | Step 3.7 — ruff check + format clean (1 I001 import-order auto-fixed). |
| `phase-outputs/test-results/r0-2-multimodelswarm-rerun.txt` | 252 B | Step 3.8 — direct scanner re-run output on verbatim pre-fix MultiModelSwarm M3 content. Result: `undischarged_count=0`. |
| `phase-outputs/test-results/r0-2-multimodelswarm-summary.md` | 5.3 KB | Step 3.8 — Acceptance gate #5 mapping, resume-command failure noted as non-anti-instinct (state-file discovery), test-level Contract #10 invariant proves the fix independently. |

## New files (source + tests + fixtures)

| Path | Role |
|---|---|
| `tests/roadmap/test_anti_instinct_recurrence.py` | Contract #10 lint test suite — 7 tests (3 parametrised FP + 1 anti-regression + 1 provenance + 2 helper-contract). |
| `tests/roadmap/fixtures/recurrence/anti_instinct/multimodelswarm_fp_case.md` + `.expected.json` | FP fixture 1: `stub transport` + `deterministic stub for tests` (MultiModelSwarm L207, L211). |
| `tests/roadmap/fixtures/recurrence/anti_instinct/stub_worker_parallelism_fp_case.md` + `.expected.json` | FP fixture 2: `stub-worker parallelism test` (MultiModelSwarm L213). |
| `tests/roadmap/fixtures/recurrence/anti_instinct/module_path_fp_case.md` + `.expected.json` | FP fixture 3: module path `transports/stub.py`. |
| `tests/roadmap/fixtures/recurrence/anti_instinct/valid_obligation_case.md` + `.expected.json` | Anti-regression fixture: `Build stub authentication module` MUST still emit HIGH. |

## Modified files

| Path | Change |
|---|---|
| `src/superclaude/cli/roadmap/obligation_scanner.py` | Added `_ALLOWLIST_PHRASES: frozenset[str]` constant (5 entries) with provenance comment block; added `_is_allowlisted(line)` helper; added Layer 6 short-circuit in `scan_obligations` immediately after `_get_context_line`. |
| `tests/roadmap/test_obligation_scanner.py` | 3 pre-existing fixtures (Layer 5 H3-context + Fix 1 tail-section) retargeted from `Stub transport` → `Stub handler` to preserve their original demotion contracts under Layer 6 precedence. |

## Test result summary (from r0-2-pytest-summary.md)

- 5-file obligation_scanner suite: **134 passed, 1 skipped, 0 failed**.
- Wider `tests/roadmap/` suite: 1734 passed, 13 skipped, 12 failed — all 12 failures **pre-existing** on this branch (confirmed via stash-and-rerun); none reference `obligation_scanner`, `_ALLOWLIST_PHRASES`, Layer 6, or Contract #10.

## Lint/format summary (from r0-2-lint-format-summary.md)

- `ruff check`: PASS (zero issues after auto-fixing 1 I001 import-order finding).
- `ruff format --check`: PASS (3 files already formatted).

## MultiModelSwarm live re-run result (from r0-2-multimodelswarm-summary.md)

- **PASS** via two independent paths:
  1. `test_multimodelswarm_fp_demoted` parametrised test (3 FP cases) — all PASS.
  2. Direct `scan_obligations()` re-run on verbatim pre-fix MultiModelSwarm M3 content — `undischarged_count=0`.
- Full `roadmap run --resume` invocation failed for non-anti-instinct reasons (state-file discovery: no `.roadmap-state.json` at the release directory path). Documented in r0-2-multimodelswarm-summary.md per task spec ("If the resume command fails for non-anti-instinct reasons, log the failure as a blocker BUT note that the test-level Contract #10 invariant already proves the fix").
- Historical 2026-05-31 18:07 UTC audit re-run already reports `undischarged_obligations: 0` (post-manual-rename); Phase 3 locks the fix in as a Contract #10 CI invariant so future releases need not depend on case-by-case roadmap edits.

## Contract #10 satisfaction (assertion)

- [x] **≥3 known-false-positive fixtures from documented historical recurrences** — 3 FP fixtures sourced verbatim from MultiModelSwarm halt + BUILD-REQUEST §R0 item 2.
- [x] **1 valid-obligation guard** — proves no over-broadening; `Build stub authentication module` still emits HIGH undischarged.
- [x] **Provenance comment block** enforced by `test_allowlist_provenance` — references BUILD-REQUEST §R0 item 2, Contract #10, master:§Recurrence #6.
- [x] **Layer 1-5 cascade preserved** — every non-allowlisted match takes the original code path.
- [x] **Zero new `return True` fragility stubs** — Contract #5 unaffected.
- [x] **PRESERVE targets byte-identical** — commands.py / structural_checkers.py / convergence.py / cosmetic_remediator.py untouched (verified by `git diff --quiet`).

## Status

R0.2 deliverables landed in commit `f41ea931`. Ready for PG3.2 (rf-qa task-integrity verification).
