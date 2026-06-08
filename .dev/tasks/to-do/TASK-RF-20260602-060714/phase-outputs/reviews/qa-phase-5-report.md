# QA Report — Task Integrity (Phase 5 Gate)

**Topic:** R1, R2, R4, R3 remediations (Steps 5.1-5.12)
**Date:** 2026-06-02
**Phase:** task-integrity (phase-gate verification)
**Fix cycle:** N/A (initial pass)

---

## Overall Verdict: PASS

All six acceptance criteria independently verified by reading the actual source/test
files AND re-running every zero-trust command. 329 tests pass. arch_lint PASS (exit 0).
Shell-correctness behavior re-derived empirically across BOTH caller branches
(git ls-files + find). No defects found; no fixes required.

---

## Items Reviewed

| # | Check (AC) | Result | Evidence |
|---|-----------|--------|----------|
| 1 | R1 stale-comment removal (comment-only) | PASS | `grep -n "will hoist\|TODO comment below" id_registry.py` → CLEAN (no match). Read confirms docstring L22-25 now says "R0.3 hoisted ... this module now sources" (factual past-tense); no behavior change — only the module docstring text differs. |
| 2 | R2 resume-aware helper + placement + invariants | PASS | `_reset_id_registry_sidecar_hint` at executor.py L3399-3429: fresh run → `set_id_registry_sidecar_path(None)`; `--resume` AND sidecar exists → re-point at `<output_dir>/spec_id_registry.json` (L3426-3429). Called at L3532 — AFTER dry-run guard (L3525-3527 `return`) and BEFORE `execute_pipeline` (L3577). Helper touches only the module-level hint; fail-shut branches and `Callable[[str], bool\|str]` signature untouched (only imports `set_id_registry_sidecar_path`). |
| 3 | R2 regression test single-body, fail-before/pass-after | PASS | `test_r2_run_start_reset_closes_stale_sidecar_leak` (test_spec_roadmap_id_containment.py L182-235): ONE body, two sequential simulated runs (run1 sets sidecar A; run2 fresh → asserts fail-shut `isinstance(leaked,str)` + "Contract #9"; then resume-aware re-point asserts `is True`). Imports the new helper (L196) → fail-before (import error pre-fix). Docstring explicitly documents the autouse-reset-between-bodies hazard. |
| 4 | R4 shell-correctness (malformed fires, exit-1 legit, exit-2 fatal, POSIX) | PASS | See "ZERO-TRUST RE-RUNS" below. Both caller branches guard via `if FILE_LIST=$(...); then :; else rc=$?; [ "$rc" -ge 2 ] && diag+exit 1`. `apply_scope` maps grep {0,1}→`return 0`, ≥2→`return "$rc"` (L43-44). Empirically: malformed EXCLUDE → exit 1 + stderr naming SCOPE.md (both git & find branches); all-filtered → exit 0 "Total files: 0"; valid/absent EXCLUDE → exit 0. `#!/bin/sh`, no bashisms. |
| 5 | R4 src↔.claude parity, nothing staged | PASS | `make verify-sync` → "✅ All components in sync." `diff -q` src vs .claude repo-inventory.sh → PARITY_OK. `git status --porcelain .claude/` (minus `??` and settings.json) → NO_STAGED_CLAUDE_CHANGES. |
| 6 | R3 docstring skip in Rule 2; real literal still flags; Rules 1&3+marker untouched; walker 0 violations | PASS | arch_lint.py L141-159 precomputes `docstring_node_ids` (Module/ClassDef/FunctionDef/AsyncFunctionDef first-stmt Expr→str Constant); L192-193 skips those ids in Rule 2 only. Tests: `test_docstring_with_verbatim_pattern_body_not_flagged` (module/class/function positions) + `test_docstring_skip_does_not_mask_real_literal` (real assignment STILL flags exactly once). Rules 1 (name-rebind) & 3 (class-redef, UnaddressedInvariant, allow-marker) test coverage intact. Walker over `src/superclaude/cli/` → PASS exit 0. |

---

## Summary

- Checks passed: 6 / 6 acceptance criteria
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (none needed)

---

## ZERO-TRUST RE-RUNS (executed by QA, UV-only)

| Command | Result |
|---------|--------|
| `grep -n "will hoist\|TODO comment below" .../id_registry.py` | **CLEAN** (no output) |
| `uv run pytest <4 suites> -q` | **329 passed in 0.49s** |
| `uv run python -m superclaude.tools.arch_lint --check-contracts ... --scan-paths src/superclaude/cli/` | **PASS, exit 0** ("no contract-constant duplications detected") |
| `sh -n repo-inventory.sh` | **SYNTAX_OK** |
| R4 malformed EXCLUDE `[unbalanced` (find branch, temp dir) | exit **1** + stderr `ERROR: invalid exclusion regex ... in .claude-audit/SCOPE.md` (NOT exit-0 "Total files: 0") |
| R4 malformed EXCLUDE (git ls-files branch, scoped subdir of real repo) | exit **1** + same SCOPE.md-naming diagnostic |
| R4 valid EXCLUDE `^vendor/` | exit **0**, "Total files: 2" |
| R4 absent/comment-only EXCLUDE | exit **0** |
| R4 all-files-filtered (grep -v exits 1, legitimate empty) | exit **0**, "Total files: 0" (exit-1 correctly treated as success) |
| grep exit-code probe: malformed ERE → **2**; no-match → **1** | confirms the {0,1}→success / ≥2→fatal mapping is correct |
| bashism scan (`pipefail`, `[[`, `<<<`, array subscripts, `function`) | **NO_BASHISMS** |
| `make verify-sync` | **✅ All components in sync** |
| `git status --porcelain .claude/` (excl. ??/settings.json) | **NO_STAGED_CLAUDE_CHANGES** |
| `diff -q` src vs .claude repo-inventory.sh | **PARITY_OK** |

---

## Adversarial Probes (looked for defects, found none)

1. **R2 fail-shut bypass risk** — Confirmed the helper clears to `None` on a fresh run
   (run2 with no own sidecar), so a fresh second in-process run CANNOT inherit run-1's
   stale registry. The regression test asserts the leaked call returns a failure STRING,
   not `True`. No bypass.
2. **R2 placement risk** — Confirmed the helper is called AFTER `if config.dry_run: ... return`
   (so `--dry-run` does not mutate gate state) and BEFORE `_apply_resume` / `execute_pipeline`.
   Ordering correct.
3. **R4 `set -e` command-substitution abort** — The known trap is that a non-zero
   command-substitution assignment under `set -e` aborts AT the assignment line before any
   `rc=$?`/`exit 1` diagnostic. Both callers correctly place the substitution inside an
   `if ...; then :; else` guard (the one context where `set -e` is suppressed for a
   non-zero substitution). Empirically verified the diagnostic fires in BOTH branches.
4. **R4 exit-1 vs exit-2 disambiguation** — Verified grep returns 2 on a malformed ERE and
   1 on a clean no-match. `apply_scope`'s `[ "${rc:-0}" -le 1 ] && return 0` collapses
   exactly {0,1} to success and propagates ≥2. The "all files filtered" case (grep -v exit 1)
   correctly yields exit-0 "Total files: 0" — legitimate-empty is NOT treated as fatal.
5. **R3 over-broad skip risk** — Confirmed only `id(node)` of structurally-identified
   docstring Constants is skipped; a real `PATTERN = '<body>'` assignment of the same body
   in the same file STILL flags exactly once (contrast test). Rules 1 & 3 and the
   allow-marker path are unmodified. Skip is scoped to Rule 2 docstrings only.

---

## Confidence Gate

- **Confidence:** "Verified: 6/6 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%"
- **Tool engagement:** "Read: 5 | Grep: 4 | Glob: 0 | Bash: 8" (each Read/Grep/Bash mapped
  to a specific AC; tool-call count ≥ 6 checklist items — not suspect)
- No web research performed (all claims local/source-truth).
- UNCHECKED items: none.
- UNVERIFIABLE items: none.

---

## Actions Taken

None — no defects found. No in-place fixes required.

## Recommendations

- Green light to proceed past the Phase 5 gate. All R1/R2/R3/R4 remediations are correct,
  test-backed, POSIX-clean, in sync, and leave the documented fail-shut/signature/allow-marker
  invariants untouched.

## QA Complete
