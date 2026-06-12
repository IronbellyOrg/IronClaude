# Reflect Report — UC-2 Post-Execution Deviation Audit

- Run ID: post-troubleshoot-hardening-evals-20260612031044
- Mode: post (UC-2 deviation audit) | Tier reached: 2 (escalated §5.3 rule 4) | Status: success
- Calibrated confidence: 0.81 (blind-calibrated, -0.04 vs reviewer self-report mean 0.85)
- Verdict: pass_with_findings — 0 Drift, 0 Regression. 1 Authorized expansion + 1 Necessary deviation.
- Executor: opus (EXCLUDED from reviewer panel — panel executor-disjoint)
- Diff base: 8cefefde (= git merge-base HEAD origin/master; harness files staged)

## Header metrics
- tasklist_completion_pct: 0.974 (76/78 checklist items)
- Deviations authorized/necessary/drift/regression: 1 / 1 / 0 / 0
- Verification: pytest 42 passed, 11 skipped (by-design), 0 failed; ruff exit 0
- verification_regressions_detected: 0
- citations total/revalidated/dropped/inferred: 14 / 14 / 0 / 0
- evidence_validator_ran: true (zero-drop-flag: true — §11.2 meta-eval marker)
- input_drift_detected: false (28-file harness set stable)
- Reviewer panel: sonnet/analyzer + haiku/qa (executor-disjoint; opus excluded)
- t2 model/vendor diversity: full / multi (claude+openai+qwen); calibrator_diversity: full (opus disjoint)

## What was audited
Differential backtest/eval harness (28 tracked files under tests/troubleshoot/backtest/) replaying
the 5 canonical pipeline escapes E1-E5 against pre-fix PARENT commits (OLD=MISS witnesses) + skip-
guarded NEW=CATCH documentation-presence proxies, emitting a catch-rate report driving backtest_status
(not_run|partial|complete) per RELEASE-SPEC NFR-1. Partial-by-design: OLD=MISS green now, NEW=CATCH
skip-guarded pending sibling impl branch refs.

## Deviation classification (4-category taxonomy)

### 1. Authorized expansion — NEW=CATCH skip-guarding (_impl_guard.py:25-40)
NEW=CATCH proxies gated by pytest.mark.skipif keyed on impl-ref FILE EXISTENCE (self-clearing, not
dead). Spec-sanctioned: NFR-1 holds signoff advisory until E1-E5 complete; backtest_status defaults
not_run until impl refs land. Tasklist explicitly authorizes the split. NOT Drift.

### 2. Necessary deviation — E4 heal-commit re-citation (test_backtest_e4.py:14-19)
Spec/research cited E4 HEAD-heal as 20693bb8; verified merged heal is acd5631f (#158). Harness
documents the discrepancy inline and pins replay base to pre-fix parent 1b0264f1 (where the bug IS
present), NOT HEAD. Forced by on-disk reality, documented inline, contradicts no acceptance criterion
("replay at pre-fix parent" satisfied by 1b0264f1). Both SHAs real; acd5631f/#158 merged, b97c9960
(spec's E4 fix) UNMERGED. Executor's own final QA caught + corrected this in-cycle
(qa/qa-final-consolidated-findings.md). Both reviewers + blind calibrator concur: Necessary, not Drift.

### Drift: none. Regression: none.
No silent unauthorized changes, no spec-criterion contradiction, no predicate inversion, no broken
previously-passing test. Scope strictly tests/-only (no src/superclaude/ or .claude/ edits —
out-of-scope-pre-approval respected).

## Advisory note (non-blocking)
S-1 (haiku, MEDIUM->adjudicated LOW): "_impl_guard.py prose 'OLD=MISS runs UNCONDITIONALLY' is precise
relative to the impl-ref dependency but not absolute — module-level pytestmark skipif
(test_backtest_e4.py:41) also gates OLD=MISS when the pre-fix parent is absent on shallow CI."
Contradicts NO criterion (spec MANDATES the CI skip-guard). Doc-precision only; suggested reword:
"runs without an impl-ref dependency."

## Anti-vacuity verification (differential is REAL)
- OLD=MISS = genuine pre-fix subprocess replay (detached worktree, fresh sys.path), not a mock.
- backtest_status MUST equal the anti-vacuity derivation; a CATCH count alone never earns complete
  (catch_rate.py:189-195).
- null card_path hard-blocks complete (catch_rate.py:109-115, :196-205).
- proxy_limitation minLength:1 + schema-required (schema:17,:66) + runtime ValueError
  (catch_rate.py:170-173) — proxy caveat cannot be dropped/oversold.
- All 5 escapes runnable, git-verified pre-fix PARENT SHAs, no double-decrement ^ bug:
  E1=94d5baa0 E2=10723863 E3=e97aa4fd E4=1b0264f1 E5=d878bc6d.

## Promotion (Wave 7)
promotion_action: skipped / promotion_skip_reason: gate-failed. Correct + expected. §14.5.2 gate fails:
cond 3 (completion 0.974 != 1.0 — the 2 terminal items incl THIS reflect gate not yet checked); cond 5b
(frontmatter status "Doing" != "done"). By design: the terminal items are exactly what this self-run
check unblocks. Reflect does NOT move the work-unit to done/; the operator completes the terminal items.

## Tier 3 remediation (--remediate)
0 Regression, 0 Drift => no remediation MDTM task warranted. The single advisory (S-1) is a one-line
doc-precision reword, not a task-builder handoff. No remediation task recommended.

## Bottom line
The harness faithfully implements RELEASE-SPEC NFR-1: a real non-vacuous OLD=MISS vs NEW=CATCH
differential, tight anti-vacuity invariants, honest skip-guarding, correct pre-fix-parent pinning.
The only spec-vs-disk divergence (E4 heal-commit SHA) was correctly handled as Necessary and already
caught by the executor's own QA. Verdict: pass_with_findings, calibrated confidence 0.81.
