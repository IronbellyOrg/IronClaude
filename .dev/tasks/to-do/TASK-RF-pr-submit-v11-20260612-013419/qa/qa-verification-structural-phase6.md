# Phase 6 — Structural Verification (fix_authorization: false, verify-only)

**Agent:** rf-qa structural lens
**Stance:** adversarial; no fixes applied; no files modified.
**Scope:** confirm the 3 ACTIONABLE Phase 6 fixes (F1/F2/F3) landed correctly and F4–F7 are documented as deferred, with no new issue and no boundary weakening.

---

## OVERALL VERDICT: PASS

---

## Items Reviewed

| # | Check | Result | Evidence (file:line) |
|---|-------|--------|----------------------|
| a | F1: T-1115 BINDS flags to option-table rows, not loose substring | PASS | `tests/pr_submit/test_static_grep.py:256-259` loops `("--depth","--remediation-offer","--auggie-model")` and asserts ``f"| `{flag}`" in cmd`` (real `| \`--flag\`` table row). `:261-264` pulls the `--depth` row via `ln.strip().startswith("| \`--depth\`")` and asserts `"quick" in depth_row`. `:266-272` pulls the `--auggie-model` row and asserts `"claude-sonnet-4-6" in model_row`. This is row-bound, not document-wide `in cmd`. |
| a' | The bound rows actually exist in the command file | PASS | `src/superclaude/commands/auggie-review.md:49` `| \`--depth\` | \`standard\` | \`quick\` (...)` (carries `quick`); `:52` `| \`--remediation-offer\` | ...`; `:55` `| \`--auggie-model\` | (auggie default) | ...\`--auggie-model claude-sonnet-4-6\`)` (carries `claude-sonnet-4-6`). All three `startswith("| \`--flag\`")` predicates resolve to a real row. |
| a'' | F1 still asserts the byte-exact invocation + the no-`--no-post-pr` guard (not weakened) | PASS | `test_static_grep.py:251-253` keeps `flag_string = "--depth quick --remediation-offer --auggie-model claude-sonnet-4-6"` asserted `in fallback`; `:276-281` still guards the `> Skill sc:auggie-review-protocol` invocation line against `--no-post-pr`. The strengthening is additive. |
| b | F2: retrigger-review.sh `--pr` has `[ $# -ge 2 ] || die ... 2` guard BEFORE `shift 2` → missing value exits 2 | PASS | `scripts/retrigger-review.sh:24` `--pr) [ $# -ge 2 ] || die "missing value for --pr <N>" 2; PR="$2"; shift 2 ;;` — guard is the first clause, ahead of `PR="$2"; shift 2`, so under `set -u` (`:17`) a bare `--pr` short-circuits to `die(…, 2)`. Runtime confirm: `bash retrigger-review.sh --pr` → `exit=2`. |
| c | F3: SKILL.md Wave 6b names `effective_max_rounds` | PASS | `SKILL.md:94` Wave 6b: `clamp the effective budget \`effective_max_rounds := min(effective_max_rounds, 1)\` (the \`clamp_max_rounds\` helper, recorded once via the \`max_rounds_clamped\` event — INV-R3 monotone)`. Names `effective_max_rounds` AND the `max_rounds_clamped` event, matching the ref/core. |
| d | F4–F7 documented as deferred/no-fix (not silently dropped) | PASS | Consolidated findings `qa-consolidated-findings-phase6.md:25-28` carry F4 (NO-FIX documented), F5 (NO-FIX documented), F6 (NO-FIX), F7 (NO-FIX documented) each with rationale. Fix-applied `qa-fix-applied-phase6.md:11-16` "Deferred / no-fix" section restates F4–F7 with the same dispositions. Both files agree; nothing dropped. |
| e1 | No new issue introduced (test suite green) | PASS | `uv run pytest tests/pr_submit/test_static_grep.py -q` → **9 passed in 0.03s**. T-1115 strengthened and still green; no other gate regressed. |
| e2 | Fork-pin never weakened | PASS | `test_t104` / `test_t1101` / `test_t105` fork-pin asserts unchanged (`test_static_grep.py:97-106, 210-227, 159-197`); `_fork_scoped` (`:92-94`) still requires `IronbellyOrg/IronClaude` / `--repo` / `graphql`. retrigger-review.sh gh api path still `repos/IronbellyOrg/IronClaude/...` (`:35`). F2's guard is arg-parsing only; it does not touch the gh surface. |
| e3 | No `.claude/` path staged; src↔mirror synced | PASS | `diff -rq src/.../sc-pr-submit-protocol/ .claude/.../sc-pr-submit-protocol/` → empty (exit 0): the F2/F3 `src/` touches were propagated via sync, mirror is identical. Fix-applied log (`:22-23`) explicitly records `make sync-dev` + "No `.claude/` path staged". Verify-only here: I modified nothing. |

---

## Summary
- Checks passed: 10 / 10
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (verify-only, fix_authorization: false)

## Issues Found
None. (Adversarial probes that could have failed but did not: (1) F1 could have remained a document-wide `in cmd` substring — it does not, rows are bound via `startswith`; (2) the `--depth`/`--auggie-model` table rows could have lacked the asserted values — both carry them at auggie-review.md:49 and :55; (3) the F2 guard could have been placed after `shift 2` — it is the first clause at line 24; (4) the mirror could have drifted — diff is empty.)

## Commands Run (read-only / non-mutating)
- `uv run pytest tests/pr_submit/test_static_grep.py -q` → 9 passed.
- `bash retrigger-review.sh --pr; echo exit=$?` → `missing value for --pr <N>` / `exit=2`.
- `diff -rq src/.../sc-pr-submit-protocol/ .claude/.../sc-pr-submit-protocol/` → empty, exit 0.

## Confidence
Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

## Tool engagement
Read: 5 | Grep: 1 | Glob: 0 | Bash: 3

## QA Complete

VERDICT: PASS
