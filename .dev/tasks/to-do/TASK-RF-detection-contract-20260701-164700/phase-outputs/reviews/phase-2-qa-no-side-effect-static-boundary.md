# QA Report — Phase 2 No-Side-Effect Static Boundary

**Topic:** Detection contract setup static boundary review
**Date:** 2026-07-01
**Phase:** synthesis-gate-equivalent / task-integrity
**Fix cycle:** N/A

---

## Overall Verdict: FAIL

The read-only setup surfaces are clean, and the existing detection/classifier seams are not modified. However, `write_lock()` does **not** enforce the required single lock destination. It accepts any path whose parts contain `.dev` and `pr-monitor` and whose basename is `detection-contract.locked.md`, including nested or unrelated `.dev/pr-monitor` paths. Under the provided PASS/FAIL rule, this is a side-effect boundary failure.

## Confidence

**Confidence:** Verified: 4/4 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

**Tool engagement:** Read: 19 | Grep: 0 | Glob: 0 | Bash: 4 | tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0

No external lookup was required; this review was source-truth-only.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | `diagnose()` / `load_evidence()` / `validate_candidate()` perform no file write, no live GitHub call, no `run_skill()`, no Monitor arming | PASS | Read `diagnosis.py`: `diagnose()` only resolves paths, checks existence, reads contract/YAML/evidence hashes, and renders next-command text; no write or network APIs. Read `evidence.py`: `load_evidence()` only opens local JSON files and computes canonical SHA-256. Read `validation.py`: `validate_candidate()` calls pure `classify()` and builds `ValidationReport`; no write/network/skill/Monitor calls. `rg` side-effect-token sweep found write primitives only in `writer.py`; no live GitHub/network/subprocess/Skill/Monitor tokens in these functions. |
| 2 | `write_lock()` writes only `/config/workspace/IronClaude/.dev/pr-monitor/detection-contract.locked.md` and only after `confirmed=True` plus passing gate | FAIL | Read `writer.py` lines 63-82: `write_lock()` defaults to `.dev/pr-monitor/detection-contract.locked.md`, evaluates `LockGate`, then `mkdir` + atomic write. Read `lockgate.py` lines 161-174: `confirmed is True` is required, but `_dest_under_pr_monitor()` only checks that `.dev` and `pr-monitor` appear somewhere in `dest.parts` and basename equals `detection-contract.locked.md`; it does not compare to the single absolute allowed path. Read `writer.py` lines 93-100: `_ensure_lock_destination()` repeats the same broad containment check. |
| 3 | `DetectionContract.load()` / `for_arming()` semantics unchanged | PASS | `git diff -- ... detection.py classifier.py ...` showed no diff for `src/superclaude/pr_submit/detection.py` or `classifier.py`; only command/skill docs changed plus new `contract_setup/`. Read `detection.py` lines 147-199: `load()` still defaults to shipped ref unless `prefer_local_override=True`, and `for_arming()` remains `load(prefer_local_override=True)`. |
| 4 | `classify()` semantics unchanged | PASS | `git diff` showed no classifier changes. Read `classifier.py` lines 158-232: classifier still uses Augment identities, decline-first with watermark attributed-review exception, polling/clean/findings fall-through unchanged. |

## Summary

- Checks passed: 3 / 4
- Checks failed: 1
- Critical issues: 1
- Important issues: 0
- Minor issues: 0
- Issues fixed in-place: 0 (fix_authorization=false)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | CRITICAL | `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/lockgate.py` lines 165-174 and `/config/workspace/IronClaude/src/superclaude/pr_submit/contract_setup/writer.py` lines 63-100 | Lock destination gate is too permissive. It accepts any path containing `.dev` and `pr-monitor` with basename `detection-contract.locked.md`, not only `/config/workspace/IronClaude/.dev/pr-monitor/detection-contract.locked.md`. Examples that would pass the current structural predicate include unrelated or nested `.dev/.../pr-monitor/detection-contract.locked.md` paths. This violates the “writes only one lock file” static boundary. | Hard-pin the destination check to the exact repo-local lock path. Resolve the destination and require equality with the canonical lock path for the active repo, e.g. `Path.cwd() / _LOCAL_OVERRIDE_REL` resolved, or the absolute required path for this task. Reject nested `.dev/*/pr-monitor/...`, absolute paths outside the repo, `.claude`, and shipped `src/` refs. Prefer removing the public `dest` override unless tests need dependency injection; if retained, it must be equality-checked after resolution. |

## Actions Taken

- No fixes applied; `fix_authorization=false`.
- Verified source files directly and performed a side-effect-token sweep across assigned files and existing seams.
- Verified existing seam files have no uncommitted semantic changes via `git diff`.

## Recommendations

- Block Phase 2 promotion until the lock destination gate is narrowed to the single allowed path.
- Add a regression test for rejected destinations such as `/tmp/.dev/pr-monitor/detection-contract.locked.md`, `.dev/other/pr-monitor/detection-contract.locked.md`, `.dev/pr-monitor/nested/detection-contract.locked.md`, `.claude/...`, and `src/...`.
- After fixing, rerun this no-side-effect static-boundary QA and include a dynamic negative test proving `confirmed=False` and failing gates do not create parent directories or temp files.

## QA Complete
