# QA Report — Domain Lens: Git-Replay Differential Semantics

**Topic:** Phase 2 git-replay helper + integration test — differential (OLD=MISS vs NEW=CATCH) semantics
**Date:** 2026-06-12
**Phase:** doc-qualitative (domain lens, report-only)
**Fix authorization:** false (NO source file modified)
**Lens:** Adversarial — assumed ≥3 subtly-wrong replay semantics; hunted them.

---

## Overall Verdict: PASS

All three domain concerns verified correct against live git history. No replay-semantics
defect found. Every checkout target is a genuine pre-fix locus (the bug IS present at the
checked-out tree); E4 is correctly pinned to the fix-parent `1b0264f1` rather than HEAD (where
`20693bb8` already healed the advisory bug); and the helper mints a unique, self-torn-down
worktree dir per checkout with zero cross-escape tree reuse. The adversarial pass surfaced two
NON-defects worth recording (E5 literal-vs-template grep, integration assertion scope) — neither
is an error in the replay semantics.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Each `prefix_parent_sha == fix_sha^` (bare parent, pre-fix locus) | PASS | `git rev-parse <fix>^` == claimed parent for E1/E2/E3/E5 (all 4 OK); E4 special-cased (see #4) |
| 2 | Pre-fix BUG actually present at each parent tree (not fix, not double-decrement) | PASS | E1 `--file` present(2)→0 post-fix; E2 no `completion_signals`(0)→2; E3 no `advisory`(0)→1; E4 no advisory in `_evaluate_gate`; E5 `<BASE>..HEAD` two-dot form at parent → single-ref post-fix |
| 3 | E4 base pinned to `1b0264f1` NOT HEAD (advisory bug healed via `20693bb8` on HEAD) | PASS | `b97c9960` UNMERGED (not ancestor of HEAD); `1b0264f1 == b97c9960^`; `_evaluate_gate` has NO advisory at `1b0264f1` but reads `check.advisory` at HEAD:859; `20693bb8` = "honor advisory semantic-check flag in executor._evaluate_gate" |
| 4 | No worktree reuse across escapes (unique mint + teardown per checkout) | PASS | `git_replay.py:94-99` mints `scratch_root/replay-<uuid4>` or fresh `mkdtemp`; `wt=base/"wt"`; `finally` does remove --force + rmtree(base) + prune (lines 109-126); `scratch_root` itself never removed |
| 5 | Double-decrement guard arithmetic in docstring | PASS | `94d5baa0^ == ac80f176` confirmed (`git_replay.py:12` example correct) |
| 6 | Skip-guard `^{commit}` peel correctness (G2) | PASS | `test_git_replay_integration.py:42` peels `<sha>^{commit}`; `git cat-file -e 94d5baa0^{commit}` exit 0; peel defends against prefix-collision false-skip |
| 7 | Chain-note interleave claim (per-escape pinning required) | PASS | E5 fix `10723863` IS E2 parent; E2 fix `e97aa4fd` IS E3 parent; linear-ancestor chain `d878bc6d<10723863<e97aa4fd<eb9a2633` all confirmed |
| 8 | Teardown fires on body exception, no leak | PASS | unit `test...teardown_fires_even_when_body_raises` + integration `test...leaves_no_leaked_worktree` both PASS; `git worktree list` byte-identical before/after raise; 0 stray replay worktrees |

---

## Summary
- Checks passed: 8 / 8
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (report-only lens)

---

## Concern-by-Concern Verdict (as specified in the task)

### Concern 1 — Bare-parent checkout is the correct pre-fix locus — PASS

For E1/E2/E3/E5, `prefix_parent_sha` is byte-equal to `git rev-parse <fix_sha>^` — i.e. the
bare parent of the fix, NOT the fix commit and NOT a double-decremented `<fix>^^`:

- E1: `fix 7601ad25^ = 94d5baa0` == `git_replay.py:49` ✓
- E2: `fix e97aa4fd^ = 10723863` == `git_replay.py:50` ✓
- E3: `fix eb9a2633^ = e97aa4fd` == `git_replay.py:51` ✓
- E5: `fix 10723863^ = d878bc6d` == `git_replay.py:53` ✓

And the bug is demonstrably PRESENT at each parent tree (not healed, not pre-bug):
- E1 @ `94d5baa0`: `cli/prd/process.py` contains 2× `"--file"` (local-path emission) → 0 at fix `7601ad25`.
- E2 @ `10723863`: `cli/prd/gates.py` has NO `completion_signals` (no final-phase exemption) → 2 at fix `e97aa4fd`.
- E3 @ `e97aa4fd`: `cli/pipeline/gates.py` has NO `advisory` → 1 at fix `eb9a2633`.
- E5 @ `d878bc6d`: `task-builder/SKILL.md:2195` uses `--diff <BASE>..HEAD` (two-dot range, `<BASE>=start_commit`) → single-ref `--diff <BASE>` at fix `10723863`.

The double-decrement guard documented at `git_replay.py:8-13` is real and arithmetically
correct: `94d5baa0^ = ac80f176`, so applying `^` at runtime WOULD replay one commit too early.
The helper passes `commitish` through unchanged (`git_replay.py:102`, asserted by
`test_git_replay_unit.py:36-37`).

### Concern 2 — E4 pinned to `1b0264f1`, NOT HEAD — PASS

- `b97c9960` (E4 fix) is genuinely UNMERGED: NOT an ancestor of HEAD.
- `1b0264f1` IS `b97c9960^` (the fix's parent) AND is an ancestor of HEAD.
- At `1b0264f1`: `cli/prd/executor.py::_evaluate_gate` has NO `advisory` handling; its loop is
  `if result is not True: ... return False` (`1b0264f1:executor.py:853,859`) — the bug IS present.
- At HEAD: `executor.py:856-859` reads `getattr(check, "advisory", False)` — the bug is HEALED.
- The healing commit is `20693bb8` = "fix(prd): honor advisory semantic-check flag in
  executor._evaluate_gate" (touches `executor.py`, +15/-3). This is exactly the commit the task's
  concern names. Had E4 been pinned to HEAD, the bug would be absent → green-but-meaningless.
  The `git_replay.py:52` comment ("fix UNMERGED; replay against parent") is accurate.

### Concern 3 — No cross-escape worktree reuse / tree leak — PASS

`checkout_worktree` (`git_replay.py:75-126`):
- Mints a UNIQUE `base` per call: `scratch_root / f"replay-{uuid.uuid4().hex[:12]}"` (line 95) or
  a fresh `tempfile.mkdtemp(prefix="backtest-replay-")` (line 97). UUID/mkdtemp guarantee
  uniqueness — no shared dir across escapes.
- `wt = base / "wt"` (line 99) lives inside the per-call `base`, so a caller-supplied
  `scratch_root` is never itself removed (only its `replay-<uuid>` child is) — comment at
  lines 87-89 is accurate.
- Teardown is guaranteed (`finally`, lines 109-126): `git worktree remove --force` + `shutil.rmtree(base)`
  + `git worktree prune`, all `check=False` so a failed remove never masks a body exception, and
  `prune` ALWAYS reaps the `.git/worktrees/<name>/` admin record (G3).
- No call site iterates `REPLAY_ESCAPES` reusing one worktree: the only `checkout_worktree`
  invocations are per-escape in tests (each its own `with` block).
- Proven empirically: integration `test...leaves_no_leaked_worktree` PASSES (worktree list
  byte-identical before/after a raising body); 0 stray replay worktrees after the run.

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| — | — | — | None. No replay-semantics defect found. | — |

## Non-Defects Recorded (adversarial pass — NOT failures)

These were probed under the "≥3 subtly-wrong" mandate and found to be CORRECT; recorded so the
reviewer sees they were checked, not skipped:

1. **E5 literal-grep mismatch is a grep artifact, not a doc error.** A naïve
   `grep -F 'start_commit..HEAD'` at parent `d878bc6d:SKILL.md` returns 0, which superficially
   looks like "bug absent at parent." It is not: the OLD template at line 2195 uses the
   placeholder form `--diff <BASE>..HEAD` where `<BASE>` resolves to frontmatter `start_commit`.
   The two-dot range (the bug) IS present; the fix collapses it to a single `<BASE>` ref.
   research/05-replay-targets.md:229 describes this precisely (`<BASE>..HEAD` where `<BASE>=start_commit`).
   No defect.

2. **Integration suite asserts checkout-correctness only for E1.** `test...lands_on_prefix_parent`
   (line 68-89) and the no-leak test (line 92-106) both hardcode `escape_by_id("E1")`. E2-E5
   checkout-lands-on-parent is NOT independently asserted by a real-git assertion — though the
   skip-guard `_missing_replay_shas()` (line 40) DOES probe all 5 parents, and the unit test
   `test...has_exactly_five_bare_parent_shas` locks all 5 SHA values. This is a reasonable test
   economy (the checkout mechanism is escape-agnostic; the SHA table is value-locked elsewhere),
   NOT a replay-semantics error. Flagging only as informational — not a FAIL under the three
   stated concerns.

---

## Self-Audit

**(a) Reliance list — structural items NOT re-checked (none inherited; standalone domain lens):**
- This is a standalone domain lens with no Inherited Structural Verdict block; all claims were
  verified from primary sources (live git + file reads).

**(b) Independent semantic checks (≥1 required):**
- Verified `prefix_parent_sha == fix^` for 4 escapes via `git rev-parse <fix>^` (Bash, all OK).
- Verified bug-present-at-parent for ALL 5 escapes via `git show <parent>:<file> | grep` deltas
  against `git show <fix>:<file>` (E1 --file 2→0; E2 completion_signals 0→2; E3 advisory 0→1;
  E4 advisory absent→present; E5 two-dot→single-ref).
- Verified E4 unmerged + heal-on-HEAD via `git merge-base --is-ancestor` + `git show HEAD:executor.py:859`
  + `git show --stat 20693bb8`.
- Verified worktree uniqueness/teardown by reading `git_replay.py:94-126` + running both unit
  and integration suites (6 tests, all PASS) + `git worktree list` stray-count = 0.

**Confidence:** Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
**Tool engagement:** Read: 4 | Grep: 0 (folded into Bash) | Glob: 0 | Bash: 8

If I claimed 0 issues without evidence, the user should distrust it — so every concern above
cites a concrete `git`/file evidence line, and the bug-present-at-parent delta (the load-bearing
differential) was checked for ALL FIVE escapes, not sampled.

## QA Complete
