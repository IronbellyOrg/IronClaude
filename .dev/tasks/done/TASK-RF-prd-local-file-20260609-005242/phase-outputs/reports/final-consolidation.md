# Final Consolidation — TASK-RF-prd-local-file

## Executive summary
Hardened Option B implemented. Both `--file` emissions removed from `process.py`; `_build_file_args` method + `extra_args` wiring + the three dead constants (`_PHASE_ALLOWED_REFS`, `_FILE_SIZE_THRESHOLD`, `_SPEC_FILE_STEPS`) deleted; module/class docstrings de-`--file`'d. `_authoritative_specs_block` (prompts.py) upgraded to inline each EXISTING spec's content via the reused `_read_file` (50 KB cap + `_TRUNCATION_MARKER`) behind a mandatory `Path(p).is_file()` guard that falls back to a path-only line for missing/stale paths (never raises). Tests: `TestSpecFileAttach` (5 `--file` tests) → `TestSpecFileNotAttached` (2 no-`--file` argv tests) + `TestAuthoritativeSpecsBlockInline` (3 inline/truncation/missing-path tests); empty-input lock retained.

## Verification table
| Check | Verdict | Evidence |
|-------|---------|----------|
| grep `"--file"` in `src/superclaude/cli/prd/` | **0 matches = PASS** | phase5-grep-guard.md |
| `uv run pytest tests/cli/prd/ -q` | **160 passed = PASS** (== baseline 160) | phase5-pytest-summary.md |
| process.py parse+import, zero residual plumbing | **PASS** | Phase 2 inline ast.parse+import+grep |
| prompts.py functional smoke (empty/missing/inline/truncation) | **PASS** | Phase 3 inline smoke |
| git-scope (3 files + .dev/, 0 tracked .claude/) | **PASS** | git-scope-check.md |
| `make verify-sync` | DRIFT — pre-existing, unrelated (skills surface), Step 5.3(a) log+proceed | phase5-sync.md |

## Anchors / dead-code
- Anchor re-verify: all CONFIRMED, zero drift (phase1-anchor-reverify.md).
- Dead-constant grep: all 3 CONFIRMED-DEAD, refs inlined by literal name in prompts.py (phase2-deadconst-grep.md).

## Unresolved blockers
None. (One NON-BLOCKING manual acceptance — spec §8 criterion 4 headless repro — is deferred by design per spec §7.7/§9.)

## Readiness verdict
**Ready for QA gate.** Diffstat: process.py −82, prompts.py +24/−2, test_spec_flag.py +51/−28.
