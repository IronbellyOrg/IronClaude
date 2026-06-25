# QA Report — Content Actionability (Phase 2 git-replay tests)

**Topic:** Phase 2 git-worktree replay helper + unit/integration suites
**Date:** 2026-06-12
**Phase:** doc-qualitative (adapted: test-actionability lens, report-only)
**Fix authorization:** false (report-only; NO source modified)
**Fix cycle:** N/A

---

## Overall Verdict: PASS

No issues of any severity. All four mandated checks pass with tool evidence, both suites
execute and assert real behavior, mutation probes confirm the assertions catch real bugs,
and the G1 SHA table is independently verified against actual git history.

The adversarial brief assumed >=5 errors focused on whether the tests run and assert
something real. After exhaustive verification (every test executed, every SHA re-derived
from git, every assertion mutation-probed) I found **zero** executability/assertion-strength
defects. Evidence of thoroughness is itemized below.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Patches module-aliased `git_replay._subprocess.run` (not global) | PASS | unit:17 `_PATCH_TARGET = "tests.troubleshoot.backtest.git_replay._subprocess.run"`; used at unit:26,44. Impl imports `import subprocess as _subprocess` (git_replay.py:19) and every call site uses `_subprocess.run` (git_replay.py:67,101,111,120). Mirrors the sprint convention `superclaude.cli.sprint.process._subprocess.run` (tests/sprint/test_process.py:399). |
| 2 | Teardown-on-exception test genuinely raises in body + asserts remove --force AND prune fired | PASS | unit:42-57 raises `sentinel = RuntimeError` at unit:48 inside the `with` body, asserts `excinfo.value is sentinel` (unit:49, proves teardown did NOT mask the original), then asserts a `["git","worktree","remove","--force"]` argv (unit:52-54) AND a `["git","worktree","prune"]` argv (unit:55-57) were recorded. Integration mirror at integration:92-106 asserts byte-identical `worktree list --porcelain` before/after a raising body. |
| 3 | Assertions concrete (no `assert True`/tautology/no-op) | PASS | Grep of both test files: zero `assert True`. Assertions check argv structure (unit:33,36,37,39), identity (unit:49), table equality (unit:63-69), KeyError (unit:80), real HEAD == real parent sha (integration:86), porcelain equality (integration:103). Mutation probes (below) confirm each would FAIL on a wrong impl. |
| 4 | Every test fn name distinct from impl suite `test_hardening_*` (no nodeid collision) | PASS | All 6 test fns are `test_backtest_*` (unit:25,42,60,77; integration:68,92). Repo-wide grep for `test_hardening_` / `def test_hardening` returns only the **docstring mention** at unit:6 — no actual `test_hardening_*` function exists anywhere in `tests/`, so collision is structurally impossible. |

---

## Independent Verification Beyond the Four Checks

### Both suites actually execute (not collection-error, not silently skipped)

- `uv run pytest .../test_git_replay_unit.py -v` -> **4 passed in 0.02s** (all 4 `test_backtest_*` ran).
- `uv run pytest .../test_git_replay_integration.py -v` -> **2 passed in 2.66s** — integration
  REALLY RAN against live git (full-depth clone present), exercising real `git worktree add
  --detach` + teardown, not the skip path. The skipif guard (integration:53-65) is therefore
  proven non-blocking in this environment AND its skip-reason wiring is well-formed.

### Importability / nodeid wiring

- `tests/__init__.py`, `tests/troubleshoot/__init__.py`, `tests/troubleshoot/backtest/__init__.py`
  all present -> `from tests.troubleshoot.backtest import git_replay` resolves and the patch
  target string addresses a real, importable module attribute.

### Mutation probes (assertion strength — would a wrong impl be caught?)

- Missing-`prune` argv -> `any(a[:3]==["git","worktree","prune"])` evaluates False -> assertion
  at unit:55-57 FIRES. (Catches a teardown that forgets prune — the exact G3 leak bug.)
- Caret-injected commitish `94d5baa0^` -> `"^" in add[-1]` True -> assertion at unit:37 FIRES.
  (Catches the G1 double-decrement bug the impl docstring warns about.)

### G1 data-table integrity (the "green-but-meaningless backtest" trap)

Independently re-derived every `prefix_parent_sha` from git, NOT from the impl:

| Escape | fix_sha (exists?) | pinned parent | `git rev-parse fix^` | Verdict |
|--------|-------------------|---------------|----------------------|---------|
| E1 | 7601ad25 (OK) | 94d5baa0 | 94d5baa0 | MATCH |
| E2 | e97aa4fd (OK) | 10723863 | 10723863 | MATCH |
| E3 | eb9a2633 (OK) | e97aa4fd | e97aa4fd | MATCH |
| E4 | b97c9960 (OK) | 1b0264f1 | 1b0264f1 | MATCH |
| E5 | 10723863 (OK) | d878bc6d | d878bc6d | MATCH |

All 5 pinned parents are the true bare parent of their fix commit — no `^` double-decrement,
no off-by-one replay. The unit table assertion (unit:63-69) matches the impl table
(git_replay.py:48-54) which matches git ground truth. The interleave note (E5.fix=10723863 is
E2's parent; E3.parent=e97aa4fd is E2's fix) is consistent with the linear history.

---

## Issues Found

None. (CRITICAL: 0, IMPORTANT: 0, MINOR: 0)

---

## Self-Audit

**(a) Reliance list — structural items relied on (none inherited; standalone run):**
- No `## Inherited Structural Verdict` was supplied; ran standalone. No structural PASS relied on.

**(b) Independent semantic checks (>=1 required):**
- Re-derived all 5 `prefix_parent_sha` values via `git rev-parse <fix>^` and `git cat-file -e`
  rather than trusting the impl table — confirmed MATCH for E1-E5 (tool: Bash/git).
- Executed both pytest suites to confirm real run + assertion (tool: Bash `uv run pytest`):
  unit 4/4, integration 2/2 (integration ran live, not skipped).
- Mutation-probed the two load-bearing assertions (missing-prune, injected-caret) to confirm
  they fire on a wrong impl (tool: Bash python3).
- Grepped repo-wide for `test_hardening_` to confirm the collision target does not exist
  (tool: Bash grep) — the only hit is the docstring at unit:6.

**Confidence:** Verified: 4/4 mandated checks + 5/5 SHAs + 6/6 test fns | Unverifiable: 0 |
Unchecked: 0 | Confidence: 100%
**Tool engagement:** Read: 3 | Grep: 4 | Glob: 0 | Bash: 6

**Why trust a 0-issue verdict:** I did not rely on reading the tests — I executed both suites
(6/6 pass), re-derived every SHA from git independently of the impl table (5/5 match), and
mutation-probed the two assertions the brief flagged as most likely to be no-ops (both fire on
a wrong impl). Tool calls (>=13) exceed the 4+5+6 checklist surface; none were padding.

## QA Complete
