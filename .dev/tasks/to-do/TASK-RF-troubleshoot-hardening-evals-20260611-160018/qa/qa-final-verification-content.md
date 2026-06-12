# QA Report — Final Fix-Verification (Content/Semantics)

**Topic:** troubleshoot-hardening-evals backtest harness — verify serialized fix agent (I20) applied F-1/F-2/F-3/F-5 genuinely, no new vacuity, harness still faithful to spec
**Date:** 2026-06-12
**Phase:** fix-cycle (final content verification, report-only, fix_authorization: false)
**Fix cycle:** final
**Files modified by this agent:** NONE

---

## Overall Verdict: PASS

All four fixes are genuine, git-verified, and introduce no new vacuity. The harness's OLD=MISS / NEW=CATCH differential semantics are unchanged and sound. No files were modified by this agent.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | F-1: E4 HEAD-heal narrative factually accurate (`acd5631f`/#158 is the verified heal; `20693bb8` is a non-ancestor sibling) | PASS | `git merge-base --is-ancestor acd5631f HEAD` → YES; `acd5631f` = "fix(prd): honor advisory checks in the executor's `_evaluate_gate` (live PRD path) (#158)". `git merge-base --is-ancestor 20693bb8 HEAD` → NO (sibling "honor advisory semantic-check flag", not a HEAD ancestor). `b97c9960` (spec's fix) → UNMERGED. test_backtest_e4.py:14-19, :46, :79 cite this exactly. |
| 2 | F-1: replay-against-`1b0264f1` logic intact + well-justified | PASS | `acd5631f` parents = `1b0264f1` (git log `parents=%p`) — the replay base is the LITERAL pre-fix parent of the heal commit. At `1b0264f1`, `_evaluate_gate` exists (executor.py:825) with ZERO `advisory` handling (empty grep); at HEAD the advisory branch is present (executor.py:853-883, exactly as cited). `escape_by_id("E4").prefix_parent_sha == 1b0264f1`. test_backtest_e4.py:18-19 pins base, unchanged. |
| 3 | F-1: E4 OLD=MISS witness actually runs (not skip-masked) | PASS | OLD=MISS half `test_backtest_e4_old_protocol_misses_second_consumer` RAN and PASSED (replay base present locally; `git cat-file -t 1b0264f1` = commit). Only the NEW=CATCH proxy half skips (impl-ref `contract-enumeration.md` not landed yet — auto-un-skips on `feat/troubleshoot-pipeline-hardening`). |
| 4 | F-2: E5 assertion-1 now genuinely discriminating (pre-fix-only) | PASS | Action form `--diff <BASE>..HEAD`: pre-fix `d878bc6d` count=1, post-fix HEAD count=0 (isolated `grep -cF`). Mutation check: `'--diff <BASE>..HEAD' in text` → True pre-fix, False post-fix. test_backtest_e5.py:48 uses the discriminating form; bare `<BASE>..HEAD` still appears post-fix (count=1, inside the `(NOT <BASE>..HEAD)` prohibition) — confirming the prior assertion was non-discriminating and the strengthening is correct. |
| 5 | F-2: strengthening does not weaken the negative witness | PASS | Assertion-2 (test_backtest_e5.py:56, prohibition ``Do NOT use `start_commit..HEAD` `` absent pre-fix) retained; verified absent at `d878bc6d` (empty grep), present at HEAD. OLD=MISS half ran+passed. Both assertions now load-bearing instead of one. |
| 6 | F-3: new negative test exercises the proxy_limitation guard (raises on empty), not a tautology | PASS | catch_rate.py:160-168 `__post_init__` raises `ValueError` when `not self.proxy_limitation or not self.proxy_limitation.strip()`. Test (test_catch_rate_schema.py:268-286) parametrizes `["", "   ", "\t", "\n  \t"]`, asserts `pytest.raises(ValueError)`, and uses a VALID `not_run` shape (escapes=(), all counts 0) so ONLY the blank caveat can trigger the raise — correctly isolated. All 4 cases RAN and PASSED. |
| 7 | No new vacuity; OLD=MISS/NEW=CATCH differential semantics unchanged + sound | PASS | Full run: 21 passed, 2 skipped (the 2 skips are NEW=CATCH proxy halves, impl-refs not yet landed; both OLD=MISS halves ran+passed). Anti-vacuity invariants intact (catch_rate.py:121-137: `complete` requires CATCH ∧ witness ∧ card_path for ALL escapes). ruff check + `ruff format --check` clean on all three files. |
| 8 | F-5: wave-doc harmonization landed, bidirectional, breaks nothing | PASS | `git_replay.py` `ReplayEscape.wave` docstring: "H0..H5 is the FULL wave taxonomy; the E1-E5 escapes themselves only ever map to H1..H4 ... consistent, not contradictory". `catch_rate.py:79-81` mirrors reciprocally. Suite green. |

---

## Summary

- Checks passed: 8 / 8
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (report-only; fix_authorization: false)
- Test run: **21 passed, 2 skipped** (E4/E5 NEW=CATCH proxy halves, impl-ref-not-landed skip — both OLD=MISS halves ran + passed)
- Lint: ruff check + ruff format --check **clean** on all three files

## Issues Found

None.

## Actions Taken

None — report-only agent, no files modified.

## Self-Audit (MANDATORY)

1. **Factual claims independently verified against source/git:** 8 distinct claim-clusters. Git ancestry of all four commits (`acd5631f` ancestor=YES, `20693bb8` ancestor=NO, `1b0264f1` ancestor=YES + is the parent of `acd5631f`, `b97c9960` UNMERGED) verified via `git merge-base --is-ancestor` and `git log parents`. Advisory-branch presence verified at HEAD (executor.py:853-883) and ABSENCE at `1b0264f1`. E5 action-form string counts isolated pre/post fix via `grep -cF` + Python `in` mutation check. proxy_limitation guard read at catch_rate.py:160-168. Full pytest run executed (21 passed / 2 skipped). Skip reasons inspected (`-rs`). ruff check + format run.
2. **Files read to verify:** test_backtest_e4.py, test_backtest_e5.py, test_catch_rate_schema.py, catch_rate.py (model + guard), qa-final-consolidated-findings.md; plus git-object reads of executor.py and SKILL.md at HEAD, `1b0264f1`, and `d878bc6d`; ReplayEscape/EscapeResult docstrings introspected live.
3. **Why trust this verdict:** The strongest discriminators were positively demonstrated, not assumed — `acd5631f`'s parent IS `1b0264f1` (the replay base is the literal pre-fix parent of the heal), and the E5 action-form string flips True→False across the fix boundary (mutation-confirmed). The OLD=MISS witnesses for E4 and E5 actually RAN here (not skip-masked), and the F-3 negative test's 4 parametrized cases all RAN and passed against the real guard. No claim rests on documentation presence alone.
4. **Web research:** None required (all verification was local-file / git-bound). Tavily-first N/A.

## Confidence

Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

## Tool engagement

Read: 4 | Grep: 0 (git grep / grep -cF via Bash) | Glob: 0 | Bash: 6

## Recommendations

- Green light. F-1, F-2, F-3, F-5 are genuine and sound; no new vacuity introduced; harness remains faithful to the spec's OLD=MISS/NEW=CATCH differential contract.
- Non-blocking note (already tracked in consolidated findings as F-4/D-x, executor-handled doc edits — NOT harness code and out of this agent's verification scope): the `final-harness-inventory.md` headline clarification and the `ReplayEscape`/`PrefixReplayError` inventory symbol additions. These do not affect the test harness correctness verified here.

## QA Complete
