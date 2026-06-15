---
title: QA Structural Report — G2 (CI skip-guard) + G3 (no-leaked-worktree)
type: qa-report
phase: report-validation (structural lens, read-only)
fix_authorization: false
---

## QA Report — Structural G2 + G3 Verification

**Topic:** Phase 2 integration test — G2 CI shallow-clone skip-guard + G3 no-leaked-worktree post-condition
**Date:** 2026-06-12
**Phase:** report-validation (structural lens)
**Fix cycle:** N/A
**Stance:** Adversarial (assumed ≥5 errors; hunted for them)

---

## Overall Verdict: PASS

All 5 verification criteria hold under tool-verified evidence. The adversarial premise of "≥5 errors in G2/G3" did NOT survive verification: the integration suite runs green, the f-string `^{commit}` peel is byte-correct, the `rev-parse` guard short-circuits first, all 5 parent shas are probed, and a real body-raises run leaves zero leaked worktree stanzas. Per Principle 9 / Rule 9, a false FAIL is as harmful as a false PASS — I am not manufacturing defects to satisfy the framing. Residual robustness observations are logged below as MINOR/OBSERVATIONAL (not contract violations); none gate the PASS.

---

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Module-level `skipif` probes ALL 5 targets AND `git rev-parse --is-inside-work-tree` guards FIRST | PASS | `test_git_replay_integration.py:50` computes `_GIT_UNAVAILABLE` first; `:51` short-circuits `_MISSING = [] if _GIT_UNAVAILABLE else _missing_replay_shas()` so cat-file probes run ONLY inside a work-tree. `:40` `_missing_replay_shas` loops `git_replay.REPLAY_ESCAPES` = all 5 (verified `len==5` in `git_replay.py:48-54` and `test_git_replay_unit.py:60-61`). Live: `git rev-parse --is-inside-work-tree` → `true`. |
| 2 | `cat-file` probe uses `^{commit}` with f-string-escaped `{{`/`}}`, NOT bare `cat-file -e <sha>` | PASS | `test_git_replay_integration.py:42` → `f"{esc.prefix_parent_sha}^{{commit}}"`. Python eval confirmed: produces literal `94d5baa0^{commit}`. Not a bare `-e <sha>`. Rationale documented `:36-37`. |
| 3 | Skip reason names missing shas AND `fetch-depth: 0` un-skip trigger AND is self-clearing | PASS | `:59-62` interpolates `{_MISSING}` (the missing `(escape_id, sha)` tuples) and states "Set `fetch-depth: 0` on the checkout step to enable". Self-clearing: `_MISSING` recomputed at every import (`:51`); when all 5 present `bool(_MISSING)` is False (`:54`) → no skip. Live probe: all 5 shas PRESENT locally → suite runs (2 passed). |
| 4 | No-leak test captures `worktree list --porcelain` baseline, asserts `after == baseline` AFTER try/finally `remove --force` + `prune`, AND proves teardown fires on body-raises path | PASS | `:94` baseline; `:97-100` `with pytest.raises(RuntimeError): ... raise RuntimeError(...)` — body raises AFTER `yield wt`, so `worktree add` DID run (teardown is real, not a no-op). Teardown lives in `git_replay.py:109-126` finally: `remove --force` (`:111-117`) + `shutil.rmtree` (`:118`) + `prune` (`:120-126`). `:102-103` asserts `after == baseline`. Live run: `test_backtest_replay_leaves_no_leaked_worktree PASSED`; post-run `git worktree list --porcelain` shows ZERO `backtest-replay-*`/`replay-wt` stanzas. |
| 5 | Live working-tree HEAD never mutated (checkouts are detached worktrees under tmp dirs) | PASS | `git_replay.py:97` `tempfile.mkdtemp(prefix="backtest-replay-")` (or `scratch_root`); `:102` `git worktree add --detach <wt> <commitish>` — detached, separate dir, never `git checkout` on the live tree. `:108` yields the worktree path, body inspects `git -C <wt>`. Live HEAD after run unchanged: `8cefefdee...` on `feat/troubleshoot-hardening-evals`. |

## Summary
- Checks passed: 5 / 5
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (read-only, `fix_authorization: false`)

## Confidence
**Confidence:** Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 4 | Grep: 1 | Glob: 0 | Bash: 4

Tool-call count (9) ≥ checklist items (5): not suspect. Each Bash call mapped to a specific criterion (f-string eval → #2; rev-parse + 5 probes → #1/#3; pytest run + worktree-list → #4/#5; teardown-failure-path probe + pytestmark grep → #1/#4 robustness).

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | OBSERVATIONAL | `git_replay.py:118` | Teardown ordering is `remove --force` → `shutil.rmtree(base)` → `prune`. If `worktree add` partially fails leaving an admin stanza but no checkout dir, `remove --force` on a non-existent work-tree exits 128 (verified live: `fatal: '...' is not a working tree`). `check=False` (`:114`) correctly swallows it, and the subsequent unconditional `prune` (`:120`) reaps the orphan stanza — so the leak is still cleaned. No contract violation; the `prune`-always design is exactly what makes the failure path safe. No fix required. |
| 2 | OBSERVATIONAL | `test_git_replay_integration.py:94,102` | `worktree_list_porcelain()` uses `check=True` (`git_replay.py:65-72`). If a concurrent worktree op in the shared common-dir mutated the list mid-test, `after == baseline` could flake. This is a pre-existing concurrency property of the shared common-dir, not a G2/G3 defect; the test's own checkout is detached + uniquely named (`uuid4().hex[:12]`, `git_replay.py:95`) so it cannot self-collide. No fix required. |
| 3 | OBSERVATIONAL | `test_git_replay_integration.py:40` | The probe iterates `REPLAY_ESCAPES` and reads `esc.prefix_parent_sha` (the parent), correctly matching research/08 G2(b)'s `REPLAY_CHECKOUT_TARGETS` set {94d5baa0,10723863,e97aa4fd,1b0264f1,d878bc6d}. Note E3's parent (`e97aa4fd`) equals E2's `fix_sha` and E5's `fix_sha` (`10723863`) equals E2's parent — interleaved history. The probe set is the 5 distinct *parents*, which is correct; no fix. |

No CRITICAL, IMPORTANT, or MINOR contract violations found. All three rows are robustness notes that the implementation already handles correctly.

## Cross-check vs research/08 reconciliation
- G2(b) spec (research/08:115-177) requires: module-level `skipif`, `cat-file -e <sha>^{commit}` per escape, `rev-parse --is-inside-work-tree` first-line guard, reason naming `fetch-depth: 0`. **Test matches all four** (`:42,50-65`). The note's literal `^{commit}` + `{{`/`}}` rationale (`:175`) is reproduced verbatim in the test docstring (`:36-37`).
- G3 spec (research/08:181-239) requires: baseline capture, try/finally `remove --force` + `prune`, `after == baseline` equality (not substring/count), `prune` mandatory because admin records live in common-dir. **Implementation matches** (`git_replay.py:109-126`, `test:94-106`). Equality assertion used (`:103`), not a heuristic — correctly proving teardown on the raise path.

## Actions Taken
None — read-only structural lens, `fix_authorization: false`, NO source file modified.

## Recommendations
- None blocking. The 3 observational notes are already handled correctly by the `check=False` + always-`prune` design; no remediation needed.
- Optional (non-gating): a one-line comment at `git_replay.py:111` noting that `remove --force` may exit 128 on the partial-add path and that the unconditional `prune` is the real reaper would aid future readers — purely cosmetic.

## QA Complete
