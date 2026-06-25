---
title: QA Report — Structural Seam + Worktree Teardown (git_replay.py)
type: qa-report
phase: structural-seam-teardown
fix_authorization: false
---

# QA Report — Structural Seam + Worktree Teardown

**Target:** `tests/troubleshoot/backtest/git_replay.py` (Phase 2 git-replay helper)
**Reference seam:** `src/superclaude/cli/sprint/process.py`
**Research basis:** `.../research/03-git-replay-helpers.md`
**Date:** 2026-06-12
**Stance:** Adversarial (report-only; NO source modified)

---

## Overall Verdict: FAIL

The four *explicit* VERIFY items each pass their literal mechanical assertion, but the
adversarial sweep of the subprocess-mock seam and worktree-teardown surfaced **3
correctness defects** — two of which directly falsify VERIFY item 3's own stated guarantees
("teardown ALWAYS runs" and "a failed remove never masks the real exception"). Any issue = FAIL.

---

## Items Reviewed (the 4 explicit VERIFY checks)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | `import subprocess as _subprocess` at module top (patchable seam) | PASS | `git_replay.py:19` exact match; mirrors `process.py:17`. Patch target `tests.troubleshoot.backtest.git_replay._subprocess.run` is valid. |
| 2 | `git worktree add --detach <path> <commitish>` with path-BEFORE-commitish | PASS | `git_replay.py:102` — `["git","worktree","add","--detach", str(wt), commitish]`. Order correct, matches research §3.1. |
| 3 | `finally` ALWAYS runs remove(check=False) + rmtree(ignore_errors) + prune(check=False); teardown survives body exception; failed remove never masks real exception | **FAIL** | Block present at `git_replay.py:109-126`, but the guarantee is **defeated by `timeout=` on the teardown subprocess calls** — see Issue #1. `check=False` does NOT suppress `TimeoutExpired`/`FileNotFoundError`. |
| 4 | Teardown never mutates live tree; `scratch_root` never rmtree's a caller-owned dir (unique subdir minted) | PASS (with caveat) | `git_replay.py:94-95` mints `Path(scratch_root)/f"replay-{uuid…}"`; `rmtree(base)` at :118 targets the minted subdir, never `scratch_root` itself. Live tree untouched (no `-C`/cwd mutation of the main checkout). Caveat: see Issue #2 (cwd-anchoring) which is an isolation/robustness gap, not a live-tree mutation. |

All 5 parent pins independently re-verified against live git: each `prefix_parent_sha == fix_sha^`
(E1–E5 all OK). The G1 "bare parent, no `^` at runtime" contract holds — `commitish` is passed
through verbatim at `:102`.

---

## Summary

- Explicit VERIFY checks passed: 3 / 4 (item 3 FAILS)
- Defects found: 3 (1 CRITICAL, 1 IMPORTANT, 1 MINOR)
- Confidence: Verified: 4/4 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
- Tool engagement: Read: 3 | Grep: 3 | Glob: 0 | Bash: 5

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | CRITICAL | `git_replay.py:111-117` (remove) and `:120-126` (prune); claim at `:80-81`, `:110` | **`timeout=120` on the teardown subprocess calls breaks the "always runs / never masks" guarantee.** `subprocess.run` raises `TimeoutExpired` on timeout and `FileNotFoundError` if `git` is absent — **regardless of `check=`**. `check=False` only suppresses `CalledProcessError` from a non-zero exit; it does nothing for these two. If the `remove` call (`:111`) times out or git is missing, the raised exception (a) propagates out of the `finally`, **masking any real exception raised in the `with` body** — the exact failure mode the inline comment at `:110` and docstring at `:80-81` claim is prevented — and (b) skips the subsequent `shutil.rmtree` (`:118`) **and** the MANDATORY `git worktree prune` (`:120`), leaking the `.git/worktrees/<name>/` admin record that `:119` calls out as non-reapable by `rmtree`. VERIFY item 3 is therefore false as written. | Wrap each teardown `_subprocess.run` in its own `try/except (_subprocess.TimeoutExpired, FileNotFoundError, OSError): pass`, OR drop `timeout=` on the teardown calls and catch broadly. The research prescription itself (§5.1, `git_replay-helpers.md:209-219`) omits a guard too, so the bug traces to the source pattern — but the helper's own docstring promises the stronger guarantee, so it must deliver it. |
| 2 | IMPORTANT | `git_replay.py:67-72`, `:101-107`, `:111-126` (no `cwd=`/`-C` anywhere) | **No repo anchoring: every `git` call resolves the repo from the process CWD, not from `wt`/`base`.** `worktree add/remove/prune` and `worktree_list_porcelain` all run with no `cwd=` and no `git -C`. Research §2 (`…helpers.md:108-111`) and §5 explicitly recommend `git -C <dir>` targeting (drift.py prior art) precisely so the helper is robust to CWD. As written, if a test (or caller) runs from a directory outside the intended repo, `worktree add` registers against — and `prune` reaps from — *whatever repo the CWD discovers*. For the unit (mocked) path this is invisible; for the integration/real-git path it is a real isolation hazard and a teardown-targets-wrong-repo risk. | Add `cwd=<repo root>` (or `["git","-C",<common-dir>, …]`) to all four `_subprocess.run` git invocations, or document + assert the required CWD invariant. At minimum `prune`/`remove` should be anchored to the same repo `add` used. |
| 3 | MINOR | `git_replay.py:97-98` | **Redundant `base.mkdir(...)` on the `mkdtemp` branch.** When `scratch_root is None`, `tempfile.mkdtemp` (`:97`) already creates the directory; the unconditional `base.mkdir(parents=True, exist_ok=True)` at `:98` is a redundant no-op on that branch (harmless due to `exist_ok=True`, but dead on the temp path). Only the `scratch_root`-provided branch (`:94-95`) actually needs the `mkdir`. Not a correctness failure — flagged for cleanliness and to show the branch was scrutinized. | Move `base.mkdir(...)` inside the `if scratch_root is not None:` branch, or leave as-is and annotate intent. |

---

## Verification Notes (what was checked and how)

- **Item 1 seam:** `grep -n` confirmed `import subprocess as _subprocess` at `:19` and `_subprocess.run` at all three call sites (`:67`, `:101`, `:111`, `:120`). No bare `subprocess.run`. Patch target is module-attribute-patchable.
- **Item 2 arg order:** Read `:102` — `--detach`, then `str(wt)` (path), then `commitish`. Correct.
- **Item 3 teardown (the FAIL):** Read `:109-126`. Confirmed via `python3 help(subprocess.run)` + Python contract that `TimeoutExpired` and `FileNotFoundError` are raised independently of `check`. The `timeout=120` kwargs at `:106`, `:116`, `:125` therefore make the teardown calls capable of raising despite `check=False`, defeating both the "always runs" and "never masks" guarantees.
- **Item 4 scratch safety:** Read `:94-98`, `:118`. `rmtree` targets the minted `base` (`replay-<uuid>` subdir), never the caller's `scratch_root`. Live-tree non-mutation confirmed: helper issues no `-C`/cwd against the main checkout and only touches the throwaway `wt`.
- **Parent-pin cross-check (beyond the 4 items):** Bash-verified all 5 `prefix_parent_sha == fix_sha^` (E1–E5 OK) against live git — the chain note at `:44-47` and reading-(a) semantics from research §4 hold.

---

## Recommendations (report-only; no fixes applied)

1. Fix Issue #1 before this helper is relied on for real-git replay — it is the difference between
   "guaranteed teardown" and "teardown that silently leaks worktree admin records and swallows the
   real test failure." This is the single defect that flips item 3.
2. Address Issue #2 to make the integration variant CWD-robust (research already prescribes the fix).
3. Issue #3 is cosmetic; bundle with the above.

## QA Complete
