---
title: "Cleanup Branch — Pre-PR Triplet Verdict"
branch: "chore/repo-cleanup-pre-pr-split"
base: "ff99449 (master)"
head: "fe11bd8 (cleanup commit)"
date: "2026-05-18"
---

# Pre-PR Triplet Verdict — `chore/repo-cleanup-pre-pr-split`

## Overall Verdict: **PASS-PR-READY**

The single commit on this branch (`fe11bd8` — add defensive `.gitignore` guards) introduces ZERO new failures across the three pre-PR commands. All observed failures are pre-existing on the master baseline `ff99449`.

## Command 1 — `uv run ruff check src/ tests/`

| Field | Value |
|------|------|
| Exit code | 1 (errors reported) |
| Total errors | 49 |
| Error codes | E402, E731, F401, F821, F841, N999 |
| Output | `phase-outputs/test-results/chore-cleanup-ruff.txt` |
| **New errors introduced by THIS branch** | **0** |

Our commit modifies ONLY `.gitignore` (17 insertions, 0 deletions in a non-Python file). Ruff does not lint `.gitignore`. Therefore none of the 49 errors are attributable to this branch — they are all pre-existing on master and will be addressed by future PRs (audit suite ruff-fix happens in PR-B per Phase 6).

**Verdict: PASS — no new failures introduced.**

## Command 2 — `uv run pytest tests/ --tb=no -q`

| Field | Value |
|------|------|
| Exit code | 1 (failures reported) |
| Summary | 63 failed, 5631 passed, 105 skipped, 22 warnings, 1 error in 181.77s |
| Output | `phase-outputs/test-results/chore-cleanup-pytest.txt` |
| **New failures introduced by THIS branch** | **0** |

All 63 failures fall in `tests/sprint/...` and one error in `tests/v3.3/test_zero_files_analyzed.py`. These are the C1-C4 sprint runner regressions that the stashed src/ changes (TASK-RF-20260518-015659) will repair when applied to PR-A in Phase 5. They are pre-existing on the master baseline and out of scope for this `.gitignore`-only cleanup commit.

Cross-check: the boilerplate from R6 listed ~57 pre-existing sprint failures; the observed 63 is within drift tolerance (six additional sprint regression-gap tests added on master since R6 was authored).

**Verdict: PASS — no new failures introduced.**

## Command 3 — `make verify-sync`

| Field | Value |
|------|------|
| Exit code | 2 (drift detected) |
| Specific failure | `MISSING from _FRESHNESS_SCRIPTS: reject-workspace-writes.sh` |
| Output | `phase-outputs/test-results/chore-cleanup-verify-sync.txt` |
| **New drift introduced by THIS branch** | **0** |

The `reject-workspace-writes.sh` hook was registered in feat-branch commit `efaa33d` (OQ-3 fix) but is not yet on master. The installer registration step in `make verify-sync` notices this gap on master baseline. PR-F (hooks aux, Phase 9) will land this commit on master and clear the drift.

Our `.gitignore`-only commit cannot affect `_FRESHNESS_SCRIPTS` registration — verified by `git show fe11bd8 --stat`: only `.gitignore` modified.

**Verdict: PASS — no new drift introduced.**

## Summary

| Command | Exit | Pre-existing | New from THIS branch | Verdict |
|--------|------|--------------|----------------------|---------|
| `uv run ruff check src/ tests/` | 1 | 49 errors | 0 | PASS |
| `uv run pytest tests/ -q` | 1 | 63 failed + 1 error | 0 | PASS |
| `make verify-sync` | 2 | 1 drift (reject-workspace-writes.sh) | 0 | PASS |

**Triplet is PR-ready** — the cleanup commit can be opened as PR-0 (its own PR) OR folded into one of the other 7 PRs at the user's discretion. Either way, it does not block downstream PR work.

## Note on Pre-PR Triplet Semantics

Per CONTRIBUTING.md lines 33-35, the triplet runs before opening a PR. The semantic interpretation per BUILD_REQUEST Phase 3 Step 3.13 is "no NEW failures introduced by THIS branch" — pre-existing failures on master do not block this PR. All three commands satisfy that semantic. The actual pre-existing failures will be cleared by the downstream PR-A (sprint runner fixes) and PR-F (hooks aux + reject-workspace-writes.sh registration).
