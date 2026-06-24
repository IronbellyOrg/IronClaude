# QA Report — Research Gate (Gap-Detection Re-Verification, Round 2)

**Topic:** Troubleshoot hardening evals — git-replay helpers / replay targets
**Date:** 2026-06-11
**Phase:** research-gate (fix-cycle re-verification)
**Fix cycle:** 2 (gap-fill round 1 re-verify)
**Lens:** gap-detection
**Fix authorization:** false (report-only)
**Stance:** ADVERSARIAL — assume gaps NOT closed until independently proven.

---

## Scope

Re-verify 3 gaps flagged FAIL in round 1 are now CLOSED in:
`research/08-gap-fill-reconciliation.md`

- G1 (IMPORTANT): checkout-target contradiction (`<sha>^` vs direct-parent)
- G2 (IMPORTANT): CI shallow-clone skip-guard
- G3 (MINOR): no-leaked-worktree post-condition

Plus: scan for NEW contradictions introduced against research/03 and research/05.

---

## Verification Log

All git claims in `08-gap-fill-reconciliation.md` were re-run independently against
`/config/workspace/IronClaude/` (full-depth clone). Results below are MY tool output,
not the note's quoted output.

### G1 — checkout-target contradiction (IMPORTANT)

**Note's authoritative pin (lines 66-89):** "The harness MUST store the PRE-FIX PARENT sha
per escape and check it out with NO `^` suffix." Explicit double-decrement warning at lines
70-72: applying `^` to a parent sha (`94d5baa0^` = `ac80f176`) double-decrements and replays
one commit too early → green-but-meaningless backtest. Recommends pinning the resolved parent
at authoring time so runtime is `git checkout <prefix_parent_sha>` with zero `^` arithmetic.
→ **Pin requirement MET.** Double-decrement warning MET (explicit, with the concrete
`94d5baa0^ → ac80f176` example).

**Independent git re-verification (my own `git rev-parse --short <fix>^`):**

| Escape | FIX     | Note claims PARENT | My `git rev-parse` | Match |
|--------|---------|--------------------|--------------------|-------|
| E1 | `7601ad25` | `94d5baa0` | `94d5baa0` | ✓ |
| E2 | `e97aa4fd` | `10723863` | `10723863` | ✓ |
| E3 | `eb9a2633` | `e97aa4fd` | `e97aa4fd` | ✓ |
| E4 | `b97c9960` | `1b0264f1` | `1b0264f1` | ✓ |
| E5 | `10723863` | `d878bc6d` | `d878bc6d` | ✓ |

All 5 parents match the task brief mapping exactly. Double-decrement hazard independently
reproduced: `git rev-parse --short '94d5baa0^'` → `ac80f176` (matches note line 43).
E4 unmerged independently confirmed: `git merge-base --is-ancestor b97c9960 master` → UNMERGED
(matches note line 46 + the `(UNMERGED)` annotation in the table). All 5 parent shas are real
commits: `git cat-file -e <sha>^{commit}` → present for all 5.

**G1 VERDICT: CLOSED.** The note authoritatively pins the bare parent sha per escape with no
`^`, warns explicitly about the double-decrement, and every sha is independently correct.

### G2 — CI shallow-clone skip-guard (IMPORTANT)

**Note's fetch-depth claim (lines 97-111):** the pytest suite runs in the `test:` job of
`.github/workflows/test.yml`; the checkout (`test.yml:20-21`) uses `actions/checkout@v4` with
NO `fetch-depth` key → defaults to shallow `fetch-depth: 1`; `fetch-depth: 0` is set only in
`contract3-generator-constraint-lint.yml:32`, `publish-pypi.yml:37`, `boundary-guard.yml:43`,
none of which run the replay.

**Independent re-verification (my own Read + grep):**
- `test.yml:11` `test:` job; `test.yml:20-21` `Checkout code` / `actions/checkout@v4` with
  **no `fetch-depth`** — confirmed by reading the file directly (lines 19-21).
- The pytest steps `Run tests` (54-56) and `Run tests with coverage` (58-61) live in that SAME
  `test:` job, after the single no-fetch-depth checkout. So the replay test genuinely runs on a
  shallow clone in CI. Confirmed.
- `grep -rn 'fetch-depth' .github/workflows/` → exactly 3 hits, all `fetch-depth: 0`:
  `publish-pypi.yml:37`, `contract3-generator-constraint-lint.yml:32`, `boundary-guard.yml:43`.
  Matches the note's list precisely; none is the test job. Confirmed.

**Skip-guard predicate (note lines 115-176):** module-level `pytest.mark.skipif` that (a) probes
`git cat-file -e <parent>^{commit}` per escape to detect commits absent on a shallow clone, and
(b) uses `git rev-parse --is-inside-work-tree` as a first-line guard so a non-git checkout
(unpacked sdist / Docker layer) skips cleanly instead of erroring. Copy-pasteable, syntactically
complete, f-string brace-escaping is correct (`{sha}^{{commit}}`), and the `^{commit}` peel
rationale (asserts object exists AND is a commit) is sound. The predicate keys off the pinned
PARENT shas from G1 (`REPLAY_CHECKOUT_TARGETS`) — consistent with the G1 resolution, NOT the
fix shas. → both required elements (cat-file -e probe per escape + is-inside-work-tree) MET.

**G2 VERDICT: CLOSED.** Actual fetch-depth identified (default shallow `1`, no key on the test
job), concrete copy-pasteable skipif predicate provided with both required probes.

### G3 — no-leaked-worktree post-condition (MINOR)

**Note's post-condition (lines 184-239):** capture `git worktree list --porcelain` baseline →
run replay in try/finally → teardown does `git worktree remove --force <dir>` then
`git worktree prune` → assert `after == baseline`. `prune` is argued mandatory because the
`.git/worktrees/<name>/` admin records live in the common-dir (`git rev-parse --git-common-dir`
→ `.git`), shared across worktrees and unaffected by `tmp_path` deletion.

**Independent re-verification:**
- `git rev-parse --git-common-dir` → `.git` (matches note line 192). Confirmed the admin-record
  rationale: tmp_path cleanup does NOT reap `.git/worktrees/<name>/`, so `prune` is genuinely
  required.
- `git worktree list --porcelain` produces blank-line-separated stanzas of
  `worktree <path>` / `HEAD <sha>` / `branch <ref>` — exactly the shape the note describes
  (line 197) and what the `after == baseline` equality compares.
- The assertion is concrete and assertable: equality (not substring/count heuristic) catches
  both a leaked checkout and a leaked admin stanza. `prune` is in `finally` (fires on the
  assertion-failure path). Both required elements (baseline==after; prune mandatory via
  common-dir) MET.

**G3 VERDICT: CLOSED.** Concrete assertable post-condition specified with mandatory prune
justified by the common-dir evidence.

### NEW-contradiction scan (note vs research/03 and research/05)

- **vs 05:** The note's per-escape parent table (E1→94d5baa0, E2→10723863, E3→e97aa4fd,
  E4→1b0264f1, E5→d878bc6d) is byte-identical to 05's "Source-of-truth confirmation" table
  (05 lines 19-25) and 05's harness assertion table (05 lines 272-278). E4 UNMERGED matches
  05. **No contradiction with 05** — the note ratifies 05.
- **vs 03:** The note explicitly declares 03 WRONG on the data shape and names 03's
  `_resolve_prefix_parent("94d5baa0") → ac80f176` example (03 lines 188-194, 225) as the
  double-decrement bug. This is a *deliberate, documented* supersession (the note states at
  line 5 it is the tie-breaker where 03 and 05 conflict), NOT a new accidental contradiction.
  03 itself flagged the ambiguity as an open question for R5 (03 lines 166-170, 292). The note
  resolves it in 05's favor with hard git evidence. Correctly handled.
- The note introduces no claim that contradicts 03's still-valid mechanics (subprocess seam,
  `git -C` targeting, try/finally teardown, `git worktree add --detach <path> <commitish>`
  arg order). It only overrides 03's parent-vs-fix data-shape reading. **No new contradiction
  introduced.**

One internal-consistency nit (NON-blocking, MINOR, not a gap): the note's worktree-add example
at line 219 uses `git worktree add --detach <dir> 94d5baa0` (correct: a parent checkout target),
whereas 03's helper example at 03:225 fed `_resolve_prefix_parent("94d5baa0")` — the note's
example is the corrected form, so this is the note fixing 03, not a contradiction.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| G1 | Checkout-target pinning (bare parent, no `^`) + double-decrement warning | PASS | Note lines 66-72, 78-89; 5 parents re-resolved via `git rev-parse --short <fix>^` all match brief; `94d5baa0^`→`ac80f176` reproduced; E4 UNMERGED reproduced |
| G2 | Actual CI fetch-depth identified + copy-pasteable skipif (cat-file -e + is-inside-work-tree) | PASS | Read `test.yml:11,20-21,54-61` (no fetch-depth on test job); `grep fetch-depth` → 3 hits all `:0`, none the test job; predicate at note lines 115-176 |
| G3 | Assertable no-leak post-condition (baseline==after, prune mandatory via common-dir) | PASS | `git rev-parse --git-common-dir`→`.git`; porcelain stanza shape confirmed; assertion at note lines 201-239 |
| NC | No new contradiction vs 03/05 | PASS | Note ratifies 05's table byte-for-byte; supersedes 03's data-shape reading deliberately (note line 5 tie-breaker); 03 mechanics untouched |

## Summary
- Checks passed: 4 / 4
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false — report-only)

## Issues Found

None blocking. One non-blocking MINOR observation (note line 219 is the *corrected* worktree-add
example; it fixes 03 rather than contradicting it — no action required).

## Confidence Gate

- All 3 gap checks + the contradiction scan were VERIFIED with independent tool output
  (git rev-parse, git cat-file, git merge-base, git rev-parse --git-common-dir,
  git worktree list --porcelain, grep, Read of test.yml). No checklist item is UNCHECKED
  or UNVERIFIABLE.
- **Confidence:** Verified: 4/4 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 4 | Grep: 0 (greps run via Bash) | Glob: 0 | Bash: 4
  (Bash calls covered the G1 sha resolution + double-decrement + E4-merge + cat-file probes,
  the G2 fetch-depth grep across workflows, and the G3 common-dir + porcelain checks; Read
  covered 08/03/05 and test.yml). Tool-call count (8) ≥ checklist items (4) — not suspect.
- No web research required (all claims are local-repo / git-bound, not external).

## Recommendations

- Green light to proceed to synthesis for this track. All 3 round-1 gaps (G1, G2, G3) are
  independently confirmed CLOSED; no new contradiction introduced against 03/05.
- Carry forward to the task-builder: the harness MUST store the resolved PRE-FIX PARENT sha
  per escape and `git checkout` it with NO `^` (the note's REPLAY_ESCAPES shape), and ship the
  module-level skipif guard so the integration replay skips (not fails) on shallow CI clones.

---

## VERDICT: PASS

All 3 previously-failed gaps (G1 IMPORTANT, G2 IMPORTANT, G3 MINOR) are independently verified
CLOSED. No new contradiction introduced against research/03 or research/05. Fix cycle 2 reduced
the open-gap count from 3 → 0 (strict monotonic decrease; no regression).

## QA Complete
