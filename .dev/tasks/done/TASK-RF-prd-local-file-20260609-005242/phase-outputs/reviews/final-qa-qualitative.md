# QA Report — task-qualitative (COMBINED CONTENT lens: actionability + domain-accuracy + cross-reference-chain)

**Topic:** prd-local-file-delivery-fix (remove `--file` misuse; inline spec content)
**Date:** 2026-06-09
**Phase:** task-qualitative
**Fix cycle:** N/A
**fix_authorization:** false (report only)

---

## Overall Verdict: PASS

The change FUNCTIONS end-to-end. Every operational claim in the consolidation and
spec was verified against live execution, not just by reading. The four mandated
operational checks all hold with tool evidence below.

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Guard prevents resume-time bare `FileNotFoundError` on scope-discovery | none | PASS | Live: bare `_read_file('/nope')` raises `FileNotFoundError`; `issubclass(FileNotFoundError, MissingArtifactError) == False`, so executor.py:696 `except MissingArtifactError` would NOT catch it → crash. Guard at prompts.py:140 (`Path(p).is_file()`) skips the read. |
| 2 | `build_scope_discovery_prompt` / `build_investigation_prompt` call `_authoritative_specs_block` | none | PASS | prompts.py:267 (scope) and prompts.py:939 (`_render_investigation_prompt`, reached via build_investigation_prompt→_dual_mode_call→_derive). Block uses `_read_file` not `_read_required`, so unguarded read = bare FNF, not the catchable subclass. |
| 3 | Real specs inlined; missing paths fall back without raising | none | PASS | Live exec: real tmp file → `ZZ_MARKER_xyz` + `--- SPEC: <path> ---` header present; `/nope/missing.md` → path appears, no raise; `[]`/`None` → `''`; 50_001-byte file → `_TRUNCATION_MARKER` present. |
| 4 | 3 new inline tests exercise content/truncation/missing-no-raise | none | PASS | test_spec_flag.py:525-548 — `test_existing_spec_content_is_inlined` (UNIQUE_MARKER), `test_oversized_spec_is_truncated` (50_001 B → marker), `test_missing_spec_path_does_not_raise`. All pass. |
| 5 | 2 inverted tests assert `--file` absence via REAL `build_command()` (not deleted symbol) | none | PASS | test_spec_flag.py:485-517 — `_command()` builds a real `PrdClaudeProcess` and calls `proc.build_command()`; asserts `"--file" not in cmd`. No reference to `_build_file_args`. |
| 6 | Removal leaves headless `--spec` runs token-free (no `--file` in argv) | none | PASS | Live: `PrdClaudeProcess(..., spec_files=[A.md]).build_command()` → argv carries no `--file` and no `extra_args` (PrdClaudeProcess passes no extra_args; base defaults `[]`). |
| 7 | Zero residual `--file` plumbing / dead symbols | none | PASS | `grep '"--file"' src/.../prd/` → 0. `grep _build_file_args\|_PHASE_ALLOWED_REFS\|_FILE_SIZE_THRESHOLD\|_SPEC_FILE_STEPS` over src/ + tests/ → 0. Only 2 doc-comment mentions of the WORD `--file` remain (process.py:11,98), both negating it. |
| 8 | Baseline pytest parity (160) | none | PASS | `uv run pytest tests/cli/prd/ -q` → 160 passed (== claimed baseline). test_spec_flag.py alone → 30 passed. |
| 9 | Cross-reference chain: spec §5.2 / Decision 1 / consolidation agree with code | none | PASS | Spec §5.2 guard, research Decision 1 `is_file()` fallback, and consolidation all match prompts.py:134-158 verbatim behavior. Empty-input contract (`if not spec_paths: return ""`) preserved at prompts.py:134. |

## Summary
- Checks passed: 9 / 9
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (report-only)

## Issues Found
None of CRITICAL/IMPORTANT severity. Two MINOR observations (non-blocking, do not
affect function):

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR (observation) | test_spec_flag.py:496-517 | The two `TestSpecFileNotAttached` tests pass distinct `step_id` values (`scope-discovery`, `investigation-3`) but `build_command()` is step-independent (base class ignores step_id), so both assert the same code path. They are correct and green, just not orthogonal. Acceptable post-removal: there is no longer any per-step `--file` branch to differentiate. No action required. |
| 2 | MINOR (observation) | prompts.py:148 | Missing-path fallback emits `"- " + p` (a bullet line) while existing specs emit a `--- SPEC: <path> ---` header. Mixed formatting within one block is slightly inconsistent but intentional and harmless — the block's preamble (prompts.py:155-156) explicitly tells the agent a path-only line "must be Read from disk". No action required. |

## Adversarial findings (5-axis sweep — actively hunted, none load-bearing)
- **AX-1 drift:** Consolidation claims "160 passed (== baseline 160)" — verified live, no drift. Spec §5.2 / Decision 1 / code all cite the same line anchors and behavior; no stale citation found.
- **AX-2 contradictions:** None. The byte-identical no-spec lock (test:268-309) coexists with content-inlining because the lock's `block` is computed from a *missing* `/abs/SPEC.md` (falls back to path-only), so the with/without delta is still exactly the block. Verified test green.
- **AX-3 omissions:** Checked for an un-updated downstream consumer of the removed `extra_args`. Decision 4 claim verified: `PrdClaudeProcess.__init__` has no `extra_args` param; sole construction at executor.py:714 passes none; base defaults `[]`. No orphaned consumer.
- **AX-4 weakened criteria:** The 3 new tests use representative input (real content marker, 50_001-byte boundary, genuinely-absent path) — not stubs. The missing-path test asserts both "path appears" AND "does not raise", exercising the real guard.
- **AX-5 invented content:** No invented files/symbols. All referenced symbols (`_authoritative_specs_block`, `_read_file`, `_TRUNCATION_MARKER`, `build_command`, `MissingArtifactError`) exist and were grep/exec-verified.

## Self-Audit
1. **Factual claims independently verified against source code:** 9 checks, each via tool
   (grep + live `uv run python` exec + pytest), including the load-bearing crash-class
   proof (`issubclass(FileNotFoundError, MissingArtifactError) == False`).
2. **Files read to verify:** prompts.py, test_spec_flag.py, executor.py, process.py (prd),
   pipeline/process.py (base `build_command`), final-consolidation.md, the spec, and
   04-gap-fill-resolutions.md.
3. **Why trust the non-zero finding count vs. a bare PASS:** I did not merely confirm the
   guard exists — I proved the counterfactual: an unguarded read raises a `FileNotFoundError`
   that is provably NOT a `MissingArtifactError` subclass (one-directional subclassing), so
   the executor's single catch site would let it escape → exactly the crash the spec warns
   about. I also live-built the headless argv and confirmed empty `extra_args`. Two MINOR
   observations are surfaced rather than suppressed.
4. **Web research:** None performed (all checks local-file/exec-bound); Tavily-first N/A.

## Confidence
Verified: 9/9 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
Tool engagement: Read: 6 | Grep: 3 | Glob: 0 | Bash(exec/pytest): 6

## Recommendations
- Proceed. The change is operationally correct and token-free on the headless `--spec`
  path. The two MINOR observations are documentation/orthogonality nits, not defects, and
  require no remediation before merge.

## QA Complete

VERDICT: PASS
