# QA Domain Lens — Core-Purity / Fork-Pin (Phase 6)

**Task:** pr_submit V1.1 build — Phase 6
**Lens:** core-purity / fork-pin boundary (T-N50 / T-104)
**Stance:** Adversarial. fix_authorization: false (report only). No web search.
**Date:** 2026-06-12

---

## Files Verified (Read + Grep)

- `src/superclaude/skills/sc-pr-submit-protocol/refs/auggie-fallback.md`
- `src/superclaude/skills/sc-pr-submit-protocol/refs/review-retrigger.md`
- `src/superclaude/skills/sc-pr-submit-protocol/scripts/retrigger-review.sh`
- `tests/pr_submit/test_static_grep.py`

---

## Claim Verification

### 1. auggie-fallback.md has ZERO gh/git tokens AND is in CORE_PURE_FILES — PASS

- `grep -nE '\bgh\b|\bgit\b' auggie-fallback.md` → **empty (exit 1)**. Zero shell/VCS word tokens.
  (The ref documents the `> Skill sc:auggie-review-protocol` invocation + flag table only.)
- `CORE_PURE_FILES` at `test_static_grep.py:36` now includes
  `SKILL_DIR / "refs" / "auggie-fallback.md"` — confirmed present in the zero-token set
  guarded by `test_tn50_core_pure_no_gh_git_tokens` (lines 109-120).

### 2. review-retrigger.md + retrigger-review.sh are NOT in CORE_PURE_FILES — PASS

- `CORE_PURE_FILES` (test_static_grep.py:27-40) contains exactly: state-machine.md,
  severity-routing.md, loop-guard.md, auggie-fallback.md, fsm.py, severity_router.py,
  loop_guard.py. **Neither gh-bearing file is in the list.**
- Both carry `gh` BY DESIGN (issue-comment POST surface) and are instead covered by the
  T-104 fork-pin path — explicitly by the dedicated `test_t1101_retrigger_gh_is_fork_scoped`
  (lines 210-227), which asserts both via `REVIEW_RETRIGGER_REF` + `RETRIGGER_SCRIPT`.
  This mirrors the thread-reply.md / augment-poll.md exclusion rationale (comment at lines 32-35).

### 3. Script `gh api` is fork-pinned to repos/IronbellyOrg/IronClaude — PASS

- `retrigger-review.sh:34-35`:
  `gh api --method POST "repos/IronbellyOrg/IronClaude/issues/${PR}/comments"`.
  Path-segment fork pin (gh api takes no `--repo`). Not bare, not upstream.
- No `SuperClaude-Org` or bare/upstream offender found in the file.

### 4. review-retrigger.md example `gh api` is fork-pinned — PASS

- `review-retrigger.md:25`:
  `gh api --method POST repos/IronbellyOrg/IronClaude/issues/<N>/comments -f body="auggie review"`.
  Fork-pinned. The prose at lines 28-29 additionally names a bare/upstream path as a
  "T-104-class defect" (documentation only, not an emitted command — `_command_lines`
  scans only fenced code blocks, so prose is not a false-positive offender).

---

## Adversarial Probes (negative results)

- `grep -nE 'SuperClaude-Org|repos/[^I]...'` across both gh-bearing files → **no offenders**.
- No second/unpinned `gh api` call hidden in either file (each has exactly one fenced POST).
- auggie-fallback.md fenced block (line 28) is a `> Skill ...` invocation, NOT a `gh`/`git`
  command — consistent with its zero-token classification.

## Offenders

None.

---

VERDICT: PASS
