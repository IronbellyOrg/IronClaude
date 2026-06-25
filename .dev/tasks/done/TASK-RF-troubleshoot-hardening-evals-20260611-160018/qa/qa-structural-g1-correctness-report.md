# QA Report — Task Integrity (Structural Lens: G1 Checkout-Target Correctness)

**Topic:** G1 checkout-target correctness in the Phase 2 git-replay helper
**Date:** 2026-06-12
**Phase:** task-integrity (G1 structural correctness lens)
**Fix cycle:** N/A
**Fix authorization:** false (report-only — no source file modified)
**Stance:** Adversarial. Assumed >=5 G1 errors existed; hunted each row, each sha, each caret.

---

## Overall Verdict: PASS

The adversarial premise (>=5 G1 errors) was NOT borne out. Every one of the four
required checks verified clean against both the task-brief expectations and the
authoritative research/08 table. No row, sha, caret, or docstring discrepancy was
found. Per the "0-issues-is-suspect" principle, the evidence trail below cites the
exact tool output backing each PASS so the verdict is auditable, not asserted.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | `REPLAY_ESCAPES` stores bare pre-fix PARENT shas; NO `^` anywhere in module | PASS | `git_replay.py:49-53` — E1=`94d5baa0`, E2=`10723863`, E3=`e97aa4fd`, E4=`1b0264f1`, E5=`d878bc6d` (3rd field of each row). `grep '\^'` over the module returns only docstring/comment lines (`:8-13`, `:34`, `:45`, `:80`) — all are hazard-rule prose, NONE in executable code. |
| 2 | Runtime checkout never applies caret arithmetic; `commitish` passed through unchanged | PASS | `git_replay.py:102` — `["git", "worktree", "add", "--detach", str(wt), commitish]`; `commitish` is the raw parameter (`:76`), never re-derived, sliced, or suffixed. Docstring `:79`/`:86` confirms "passed through UNCHANGED"/"verbatim". No `_resolve_prefix_parent` / `+ "^"` / f-string-with-caret anywhere. |
| 3 | Each `(escape_id, fix_sha, prefix_parent_sha, wave)` row matches research/08 EXACTLY; no fabricated sha | PASS | See per-row table below. All 5 rows byte-match `git_replay.py:49-53` ⇄ research/08 table (`research/08...md:56-60`) ⇄ replay-table.md (`:10-14`) ⇄ task brief. |
| 4 | Module docstring states the no-caret double-decrement hazard rule | PASS | `git_replay.py:8-13` — "G1 CHECKOUT RULE (load-bearing)... with NO `^` suffix, EVER... applying `^` again double-decrements (e.g. `94d5baa0^` -> `ac80f176`)... Never apply `^` at runtime." Matches research/08 EXPLICIT RULE (`research/08...md:68-72`). |

### Per-row cross-validation (Check 3 detail)

| Row | Module (`git_replay.py:49-53`) | research/08 table (`:56-60`) | Brief expectation | Match |
|-----|-------------------------------|------------------------------|-------------------|-------|
| E1 | `7601ad25` / `94d5baa0` / `H1` | `7601ad25` / `94d5baa0` / `H1` | `7601ad25` / `94d5baa0` / `H1` | EXACT |
| E2 | `e97aa4fd` / `10723863` / `H3` | `e97aa4fd` / `10723863` / `H3` | `e97aa4fd` / `10723863` / `H3` | EXACT |
| E3 | `eb9a2633` / `e97aa4fd` / `H3` | `eb9a2633` / `e97aa4fd` / `H3` | `eb9a2633` / `e97aa4fd` / `H3` | EXACT |
| E4 | `b97c9960` / `1b0264f1` / `H2` | `b97c9960` (UNMERGED) / `1b0264f1` / `H2` | `b97c9960` / `1b0264f1` / `H2` | EXACT |
| E5 | `10723863` / `d878bc6d` / `H4` | `10723863` / `d878bc6d` / `H4` | `10723863` / `d878bc6d` / `H4` | EXACT |

Chain-note cross-check (`git_replay.py:45-47` ⇄ research/08 `:64`): E5's fix `10723863`
IS E2's checkout parent (`:50` 3rd field), and E2's fix `e97aa4fd` (`:50` 2nd field) IS
E3's checkout parent (`:51` 3rd field). The module's interleave note is internally
consistent and matches the authoritative chain note. No sha appears in the module that
is absent from research/08's table — no fabrication.

## Summary

- Checks passed: 4 / 4
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (report-only lens, fix_authorization: false)

## Issues Found

None. (Adversarial premise of >=5 errors not substantiated. The G1 surface is correct:
parent shas stored bare, caret confined to hazard-documentation prose, runtime
pass-through verbatim, all 5 rows byte-exact against the authoritative table.)

## Adversarial probes that could have failed but did NOT

| Probe | What a failure would look like | Result |
|-------|-------------------------------|--------|
| Caret leaking into runtime | `commitish + "^"`, `f"{sha}^"`, or `_resolve_prefix_parent(...)` at `:102` | Absent — `:102` uses raw `commitish` |
| Caret in a stored row literal | any `"...^"` in `:49-53` | Absent — all 8-char hex, no suffix |
| Off-by-one row swap (E2/E3 share parents) | E3 parent = `10723863` instead of `e97aa4fd` | Correct — E3 parent=`e97aa4fd` (`:51`) |
| E4 pointed at HEAD/heal commit `20693bb8` not parent `1b0264f1` | E4 3rd field = `20693bb8` | Correct — `1b0264f1` (`:52`); UNMERGED caveat noted |
| Fix-sha used as checkout target (the file-03 bug) | checkout uses `fix_sha` field not `prefix_parent_sha` | `prefix_parent_sha` (3rd field) is the documented checkout target; fix_sha is audit-only (`:33`) |
| Wave drift | any wave value differing from research/08 | All 5 waves (H1/H3/H3/H2/H4) match |

## Recommendations

- None blocking. G1 checkout-target correctness is verified PASS.
- (Non-G1, out of scope for this lens, noted not flagged) Checks 2-4 confirm the
  runtime/docstring surface; G2 skip-guard and G3 teardown live in research/08 but
  were not in this lens's 4-item mandate.

## Confidence

**Confidence:** Verified: 4/4 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 4 | Grep: 3 | Glob: 0 | Bash: 3

All 4 checklist items marked [x] VERIFIED with cited tool output (Read of all 3 source
files + this report + 3 grep/bash passes targeting caret presence, row literals, and
checkout-call shape). Tool-call count exceeds the 4-item checklist minimum — not padded;
each call mapped to a specific check. No UNCHECKED, no UNVERIFIABLE items.

## QA Complete
