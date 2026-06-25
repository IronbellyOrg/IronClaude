# QA Report — Final Content (NFR-1 Fidelity + Proxy Honesty)

**Topic:** E1-E5 differential backtest harness — NFR-1 fidelity + proxy-honesty adversarial review
**Date:** 2026-06-12
**Phase:** task-qualitative (content/fidelity overlay)
**Fix cycle:** N/A (report-only, fix_authorization: false)

---

## Overall Verdict: **FAIL**

The four core claims (#1 separation, #2 proxy-honesty serialized, #3 E4 HEAD-drift pinned to `1b0264f1`, #4 NFR-1 catch-rate drives `not_run` today) are SUBSTANTIVELY UPHELD by the code and proven by passing/skipping tests. However, the adversarial stance surfaced **3 fidelity defects** (1 IMPORTANT, 2 MINOR). Per this phase's "any issue = FAIL / no severity exempt" rule, the verdict is FAIL. None of the defects break the replay's functional correctness — they are narrative/attribution/coverage fidelity gaps.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Signoff stays ADVISORY until `complete`; separate from run-level verdict | PASS | `catch_rate.py:207-217` — `production_signoff` returns `run_level_verdict` ONLY when `STATUS_COMPLETE`, else `"advisory"`. `test_backtest_status_separation.py:38,53` assert advisory at not_run/partial; `:68` mirrors at complete. Tests PASS (3/3). |
| 2 | NEW=CATCH proxy limitation serialized, schema-required, minLength 1, honest, not oversold | PASS (with coverage gap, see I3) | `catch_rate.py:69` field in `_CATCH_RATE_FIELDS`; `:156` serialized; `:162-166` non-empty/non-whitespace honesty guard. `schema.json:17` required, `:64-67` `minLength:1`. `catch_rate_report.py:35-42` `_PROXY_NOTE` wire text matches code (producer-asserted, NON-NULLNESS only, EXISTENCE upstream). |
| 3 | E4 HEAD-drift pinned to `1b0264f1` (NOT HEAD), bug present at base | PASS (functional) / FAIL (attribution, see I1) | `git_replay.py:53` E4 pinned bare `1b0264f1`; verified `1b0264f1` IS ancestor of HEAD; verified `_evaluate_gate` at `1b0264f1` has NO advisory branch (bug present). E4 OLD=MISS test PASSED (replay reproduced `halted_despite_advisory=True`). |
| 4 | NFR-1: catch-rate drives status; today `not_run` (refs absent); `complete` unreachable | PASS | 3 foundation/escape refs verified ABSENT under `.../refs/`. `test_catch_rate_aggregation.py:131` asserts `not_run`+`total_escapes==0`; ran (not skipped). 5 parametrized escape-collection tests SKIP at not_run. `_collect_escape_results:65` returns `[]` when no ref present. |

---

## Summary

- Checks passed: 4 / 4 core claims substantively upheld
- Checks failed: 0 core claims; **3 fidelity defects** found (1 IMPORTANT, 2 MINOR)
- Critical issues: 0
- Tests executed: aggregation+separation 5 passed / 5 skipped; E4 1 passed / 1 skipped — all green, today-state = not_run confirmed

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| I1 | IMPORTANT | `test_backtest_e4.py:14,43,76` | The load-bearing "E4 HEAD-drift" narrative asserts (3 places) "HEAD already healed via `20693bb8`". On THIS worktree's HEAD (`8cefefde`, branch `feat/troubleshoot-hardening-evals`), `20693bb8` is **NOT an ancestor** (`git merge-base --is-ancestor 20693bb8 HEAD` → false). The advisory heal actually present on HEAD was introduced by **`acd5631f`** (PR #158, "fix(prd): honor advisory checks in the executor's _evaluate_gate (live PRD path)"). `acd5631f` and `20693bb8` are distinct commits (different patch-ids: `09fd5188…` vs `397a2c54…`; different executor.py trees). The research doc §4.2 line 166 also claims `20693bb8` "IS an ancestor of HEAD" — stale for this worktree. Replay logic is UNAFFECTED (pins to `1b0264f1`, bug verified present, OLD=MISS test passes), but the fidelity claim names the wrong heal commit. | Correct the 3 comments + research §4.2 to attribute the HEAD heal to `acd5631f` (PR #158) for this branch, OR state both commits honor advisory and the branch-specific ancestor is `acd5631f` not `20693bb8`. Do not change the replay base (`1b0264f1` is correct). |
| I2 | MINOR | `git_replay.py:53`, `test_backtest_e4.py:85` | E4 wave is labeled **`H2`** (singular). Spec §3.1 traceability matrix (research line 41) binds E4 to **both `H1, H2`** ("Shared `SemanticCheck.advisory` honored by generic gate but not PRD evaluator … Closing Wave(s): H1, H2"). The harness collapses E4's dual-wave mapping to H2 only. Defensible (the E4 replay targets the H2 ledger-completeness oracle specifically), but technically diverges from the spec's 1:1 escape→wave matrix. | Either annotate E4's wave as `H1,H2` to match the spec matrix, or add an inline note that E4 is intentionally scoped to its H2 ledger oracle (the §8.3 E4 expected outcome) while H1 is covered by E1. |
| I3 | MINOR | `catch_rate.py:162-166` (guard); no test | The proxy-honesty guard rejecting empty/whitespace `proxy_limitation` (the "OVERSELL-2" enforcement central to claim #2) has **NO negative test**. No test in `tests/troubleshoot/backtest/` passes `proxy_limitation=""` or `"  "` inside `pytest.raises(ValueError)`. The guard is present and correct (read + confirmed), but its regression protection is absent — a future edit could silently weaken the honesty invariant. | Add a negative test: `pytest.raises(ValueError)` constructing a `CatchRateReport`/`build_catch_rate_report` with `proxy_limitation=""` and with `"   "`, asserting the "non-empty, non-whitespace" message. |

---

## Adversarial Findings That Did NOT Materialize (checked, cleared)

- **`import json` missing in `_E4_SNIPPET`** — NOT a bug. `replay_executor.run_prefix_replay_snippet` injects a `prelude` (`replay_executor.py:220-226`) with `import sys, json` prepended before the snippet runs in the subprocess.
- **Caret double-decrement on checkout** — Cleared. `git_replay.py:9-13` documents the G1 bare-sha rule; `checkout_worktree:155-194` passes `commitish` through unchanged (no `^`). `prefix_parent_sha` pre-resolved at authoring.
- **`complete` from CATCH count alone (vacuity)** — Cleared. `_derive_backtest_status:128` + `__post_init__:189-201` require CATCH **AND** `negative_witness` **AND** non-null `card_path` for ALL escapes; explicit `card_path is None` re-check at `:191`.
- **Card existence never enforced** — Cleared as DISCLOSED. Model enforces NON-NULLNESS only (IO-free); `_collect_escape_results:62,76` sets `card_path` only from a `.exists()`-verified ref (upstream existence); `unresolved_card_paths:262-284` is the real on-disk gate. Wire text (`_PROXY_NOTE`) matches this exactly — honest, not oversold.
- **Today silently emits `complete`/`partial`** — Cleared. Refs absent → `_collect_escape_results` returns `[]` → `not_run`; proven by `test_catch_rate_aggregation.py:131` (ran) + 5 skips at not_run.

---

## Self-Audit

**(a) Reliance list — structural items skipped (rf-qa territory, not re-checked):**
- Relied on structural QA for: JSON-schema well-formedness, field-ordering tuples, `to_dict` SoT walk, frozen-dataclass shape. Did not re-verify these as structural correctness.

**(b) Independent semantic checks (≥1 required, INV-019):**
- Git ancestry of `1b0264f1`/`b97c9960`/`20693bb8`/`acd5631f` vs worktree HEAD — verified via `git merge-base --is-ancestor` + `git patch-id` + `git log -S` (uncovered I1, the wrong-heal-commit attribution; tool evidence: `20693bb8` NOT ancestor, `acd5631f` is the `-S'advisory'` introducer).
- Bug-presence at replay base — verified `_evaluate_gate` body at `1b0264f1` via `git show 1b0264f1:…executor.py` (no advisory branch → bug present → replay meaningful).
- Today-state assertion — verified refs ABSENT via filesystem `ls` + ran the aggregation test (asserts `not_run`).
- E4 replay correctness — ran `test_backtest_e4.py` (OLD=MISS PASSED, reproduced halt-despite-advisory).
- Spec-vs-code wave mapping — cross-read research §3.1 line 41 vs `git_replay.py:53` (uncovered I2).
- Honesty-guard coverage — grepped all backtest tests for an empty/whitespace `proxy_limitation` rejection (uncovered I3, the missing negative test).

**Confidence:** Verified: 4/4 core claims + 6 semantic checks | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
**Tool engagement:** Read: 9 | Grep: 0 (folded into Bash greps) | Glob: 0 | Bash: 6

If I told the user I found 0 issues, they should NOT believe it: the adversarial git-ancestry probe directly contradicted a triple-stated narrative claim (`20693bb8` heal) and the spec-matrix cross-read found a wave narrowing — both invisible to a tests-pass-so-it's-fine reading (all tests are green despite I1/I2).

---

## Recommendations

- Resolve I1 before this harness's HEAD-drift narrative is cited as authoritative: the `20693bb8` attribution is wrong for branch `feat/troubleshoot-hardening-evals` (heal = `acd5631f` / PR #158). This is the highest-value fix — the comment actively misdirects a future maintainer choosing a replay base.
- I2 + I3 are hardening: align E4's wave label with the spec matrix (or annotate the intentional H2 scoping), and add the empty-proxy-limitation negative test to lock the OVERSELL-2 invariant.
- The replay base `1b0264f1` is CORRECT and must NOT change — verified bug-present + ancestor-of-HEAD + OLD=MISS test passes.

## QA Complete
