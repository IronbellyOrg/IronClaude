# QA Report — Report/Harness Validation (lens 3: evidence-quality / collision-boundary)

**Topic:** troubleshoot-hardening-evals backtest harness — final structural QA
**Date:** 2026-06-12
**Phase:** report-validation (Phase 6 parallel rf-qa, lens 3)
**Fix cycle:** N/A
**Fix authorization:** false (report-only — NO file modified)

---

## Overall Verdict: PASS

ADVERSARIAL STANCE applied: assumed ≥5 evidence-quality/collision-boundary errors and hunted
each of the 4 assigned claims with independent tool evidence (git status, recursive grep,
full-file Reads). Zero defects found on this lens. The absence is corroborated by `git status`
(only `tests/troubleshoot/` + the task dir are new) and by the harness's own in-tree negative
guards (no-caret asserts, no-`docs/` asserts, `parents[3]` pin test).

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Every harness file lives ONLY under `tests/troubleshoot/backtest/` (sole exception: authorized parent `tests/troubleshoot/__init__.py` per Step 1.5) | PASS | `find tests/troubleshoot -maxdepth 1 -type f` (non-pycache) → only `tests/troubleshoot/__init__.py`. All other source/test/schema/fixture files are under `tests/troubleshoot/backtest/`. The parent `__init__.py` is the task-authorized Step 1.5 file (1 line). |
| 2 | NO edit/create under skill/command/`.claude/`/impl-owned test paths (per `git status`) | PASS | `git status --porcelain` → only `?? .dev/tasks/.../`, `?? .dev/troubleshoot-meta/`, `?? tests/troubleshoot/`. `git status --porcelain` of `src/superclaude/skills/sc-troubleshoot-protocol/`, `src/superclaude/commands/troubleshoot.md`, `.claude/`, and impl-owned `tests/troubleshoot/test_hardening_*.py` + `e2e-backtest-scenarios.md` → empty (no changes). `git diff --stat HEAD` over those paths → empty. |
| 3 | G1 no-caret holds (REPLAY_ESCAPES bare parent shas; runtime checkout never applies `^`) | PASS | `git_replay.py:48-56` stores bare `prefix_parent_sha` (E1=`94d5baa0`, E2=`10723863`, E3=`e97aa4fd`, E4=`1b0264f1`, E5=`d878bc6d`) — no `^`. Runtime checkout `git_replay.py:188` passes `commitish` verbatim to `git worktree add --detach`; `checkout_worktree` docstring (`git_replay.py:160-161`) confirms pass-through. `run_prefix_replay_snippet` (`replay_executor.py:218`) passes `parent_sha` verbatim. All `^` matches in harness are (a) doc/no-caret rules (`git_replay.py:8-13,34,45,161`), (b) `git cat-file -e <sha>^{commit}` object-existence peel (`git_replay.py:103`, `test_git_replay_integration.py:45`) — NOT a checkout decrement, (c) regex `^E[0-9]+$` (`catch_rate.schema.json:82`, `test_catch_rate_schema.py:124`), (d) no-caret ASSERTIONS (`test_git_replay_unit.py:41,77`). No string concatenation adds `^` to any sha at a call site (grep returned none). |
| 4 | E4 pinned to `1b0264f1` (NOT HEAD) | PASS | `git_replay.py:52-54` `ReplayEscape("E4","b97c9960","1b0264f1","H2")` — `1b0264f1` is the checkout target; `b97c9960` is the UNMERGED fix (provenance only). `test_backtest_e4.py:34-45` skipif + replay both key on `_E4.prefix_parent_sha` (== `1b0264f1`); explicit HEAD-DRIFT note (`test_backtest_e4.py:14-16,42-43,76`) documents HEAD is already healed via `20693bb8` and pins to the parent, NOT HEAD. `test_git_replay_unit.py:73,84` asserts `escape_by_id("E4").prefix_parent_sha == "1b0264f1"`. No checkout site uses HEAD or `b97c9960` as the E4 target. |

## Summary
- Checks passed: 4 / 4
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (report-only)

## Issues Found
None on this lens.

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| — | — | — | (no findings) | — |

## Supplementary collision-boundary verifications (adversarial, beyond the 4 claims)
- **Off-limits write targets inside harness:** the only references to `sc-troubleshoot-protocol`/`.claude`/`test_hardening_` are READ-only existence probes (`_impl_guard.py:21-30,49-51` uses `.exists()` only; no write) or nodeid-distinctness notes (`test_git_replay_unit.py:6`, `test_waiver_regreen.py:31`). No write/open(w) targets any off-limits path.
- **All filesystem writes are tmp-scoped:** E1 `_spec` (`test_backtest_e1.py:42-44`) and E3 `_f` (`test_backtest_e3.py:48-50`) write under `tempfile.mkdtemp()` inside the replayed subprocess; `conftest.py:32-33,48-49` uses `tempfile.gettempdir()` + `tmp_path`; `catch_rate_report.py:156-166` writes only to the required `output_dir` arg (no `docs/` default) with a top-guard + docstring forbidding `docs/`. `test_catch_rate_aggregation.py:174`, `test_catch_rate_schema.py:271-275` write under `tmp_path`. Harness asserts output is NOT under `docs/` (`test_catch_rate_schema.py:335`).
- **REPO_ROOT depth pin:** `_impl_guard.py:21` uses `parents[3]`; `test_path_resolution.py:11-18` asserts it lands on the pyproject-bearing root and is not `tests`/`troubleshoot`/`backtest` — collision-safe ref resolution.

## Actions Taken
None (fix_authorization: false; report-only).

## Recommendations
- Lens 3 (evidence-quality/collision-boundary) is GREEN — no blocker to proceeding.
- Final verdict is the AND of all parallel lenses; merge with lens 1 (template-conformance) and lens 2 (internal-consistency) reports before declaring the harness gate PASS.

## Confidence
**Verified:** 4/4 | **Unverifiable:** 0 | **Unchecked:** 0 | **Confidence:** 100.0%
**Tool engagement:** Read: 6 | Grep: 6 | Glob: 0 | Bash: 8

[PARTITION NOTE: This is the single lens-3 instance; cross-lens (template + internal-consistency) checks are out of scope for this report and are covered by the sibling parallel rf-qa instances.]

## QA Complete
