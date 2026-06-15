# Phase 2 QA — Consolidated Findings

**Consolidated verdict: FAIL** (1 of 6 lens agents reported issues; FAIL if ANY agent reports ANY issue of ANY severity).

## Lens verdicts (6 lens agents)

| Lens | Agent | Report | Verdict |
|------|-------|--------|---------|
| Structural — G1 no-caret correctness | rf-qa | `qa-structural-g1-correctness-report.md` | PASS |
| Structural — subprocess seam + teardown integrity | rf-qa | `qa-structural-seam-teardown-report.md` | **FAIL** (3 issues) |
| Structural — G2 skip-guard + G3 no-leak | rf-qa | `qa-structural-g2-g3-report.md` | PASS |
| Content — actionability/executability | rf-qa-qualitative | `qa-content-actionability-report.md` | PASS |
| Content — collision-boundary + path discipline | rf-qa-qualitative | `qa-content-collision-boundary-report.md` | PASS |
| Domain — git-replay differential semantics | rf-qa-qualitative | `qa-domain-replay-semantics-report.md` | PASS |

## Deduplicated issues (all from the seam-teardown lens; no overlap from other lenses)

| # | Severity | Location | Issue | Required fix | Originating lens |
|---|----------|----------|-------|--------------|------------------|
| P2-1 | CRITICAL | `git_replay.py` teardown calls (remove + prune, currently `timeout=120`, `check=False`) | `timeout=` on the `finally` teardown `_subprocess.run` calls breaks the "teardown always runs / never masks the body exception" guarantee: `subprocess.run` raises `TimeoutExpired` (on timeout) and `FileNotFoundError` (if git absent) REGARDLESS of `check=False` (which only suppresses `CalledProcessError`). A raise in the `remove` call propagates out of `finally` — masking any body exception AND skipping `rmtree` + the MANDATORY `prune` (leaking the `.git/worktrees/<name>/` admin record). | Wrap each teardown `_subprocess.run` in its own `try/except (_subprocess.TimeoutExpired, FileNotFoundError, OSError): pass` (mirroring the `process.py` seam which catches exactly these), so each teardown step runs independently and none can mask the body exception or skip `prune`. | seam-teardown |
| P2-2 | IMPORTANT | `git_replay.py` — all `git` calls lack `cwd=`/`-C` | No repo anchoring: `worktree add/remove/prune` + `worktree_list_porcelain` resolve the repo from process CWD. For the real-git integration path this is an isolation hazard (teardown could target the wrong repo if CWD differs). Research §2 prescribes `git -C <dir>` targeting. | Anchor the git invocations to the repo (e.g. resolve `git rev-parse --git-common-dir` / pass `cwd`), at minimum so `remove`/`prune` target the same repo `add` used; OR document + assert the required-CWD invariant. | seam-teardown |
| P2-3 | MINOR | `git_replay.py` — `base.mkdir(...)` on the `mkdtemp` branch | When `scratch_root is None`, `tempfile.mkdtemp` already creates the dir, so the unconditional `base.mkdir(parents=True, exist_ok=True)` is a redundant no-op on that branch (harmless). | Move `base.mkdir(...)` inside the `if scratch_root is not None:` branch (or annotate intent). | seam-teardown |

## Fix routing

All 3 issues are confined to `tests/troubleshoot/backtest/git_replay.py`. Per I20 serialized-fix protocol, exactly ONE rf-qa fix agent (Step 2.QA.9) applies all CRITICAL + IMPORTANT findings (P2-1, P2-2) and SHOULD also apply the MINOR (P2-3) for cleanliness, touching ONLY files under `tests/troubleshoot/backtest/`. The G1 no-caret rule and collision boundary must be preserved.
