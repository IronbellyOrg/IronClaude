# QA Report — Flag-Translation-Accuracy Lens (Phase 5)

**Topic:** TFEP diagnostic backend migration — §4.5 Step 3 dispatch + Step 4 retry/escalate flag translation
**Date:** 2026-06-16
**Phase:** structural (flag-translation-accuracy lens)
**Fix cycle:** N/A
**Fix authorization:** false (REPORT ONLY)
**Stance:** ADVERSARIAL — assumed ≥3 wrong/stale flags; searched for them.

---

## Overall Verdict: PASS

All translated flags in the §4.5 Step 3 dispatch and the Step 4 retry/escalate branches resolve to flags `/sc:troubleshoot` actually accepts. No forensic-only tokens (`--tier`, `--intent`, `--depth quick`) survive in the in-scope dispatch. The adversarial hypothesis of ≥3 wrong/stale flags was NOT substantiated for the in-scope surface.

---

## Source-of-Truth Flag Surface (troubleshoot.md)

Verified troubleshoot accepts (Options table lines 50-60 + argument-hint line 8):
`--type`, `--depth` (values `quick|standard|deep`), `--scope`, `--no-escalate`, `--fix`, `--models`, `--output-dir`, `--no-doc-discovery`, `--no-mcp`, `--context`, `--caller`.

There is NO `--tier`, NO `--intent`, NO `--output` (it is `--output-dir`).

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | `--caller` exists in troubleshoot surface | PASS | troubleshoot.md line 60 (Options) + line 8 (argument-hint). Used in dispatch line 215. |
| 2 | `--context` exists | PASS | troubleshoot.md line 59 + line 8. Used in dispatch line 215. |
| 3 | `--output-dir` exists | PASS | troubleshoot.md line 56 + line 8. Used in dispatch line 215. |
| 4 | `--depth` exists | PASS | troubleshoot.md line 51 + line 8 (values `quick|standard|deep`). Used in dispatch line 215. |
| 5 | `--tier` GONE from Step 3 dispatch | PASS | grep for `--tier` in SKILL.md returns only lines 265-266 (deferred budget block, out of scope). Not present in line 215 or 225-226. |
| 6 | `--intent` GONE from Step 3 dispatch | PASS | grep for `--intent` returns only lines 265-266 (deferred). Absent from dispatch + Step 4 branches. |
| 7 | `--depth quick` GONE from dispatch; uses standard/deep | PASS | Line 215 prose resolves `{depth}` to "`--depth standard`" / "`--depth deep`". Lines 210-212 map triggers → standard/deep only. No `quick` anywhere in §4.5 invocation. |
| 8 | `--output-dir` used, NOT `--output` | PASS | grep `--output` matches only `--output-dir` occurrences (lines 215, plus `{output_dir}` placeholders). No bare `--output` flag. |
| 9 | NO `--fix` in §4.5 dispatch | PASS | Line 215 explicitly: "Pass NO `--fix`". Line 236 reaffirms "NO --fix". grep `--fix` in §4.5 returns only these negative-assertion mentions, never as an emitted flag. |
| 10 | Step 4 retry branch invokes `/sc:troubleshoot` | PASS | Line 225: `recommended_escalation == "retry"` → "re-run `/sc:troubleshoot` once at the SAME `--depth`." Not `/sc:forensic`. |
| 11 | Step 4 escalate_depth branch invokes `/sc:troubleshoot` | PASS | Line 226: `recommended_escalation == "escalate_depth"` → "re-invoke `/sc:troubleshoot` at `--depth deep`." Not `/sc:forensic`. |
| 12 | Deferred budget block (265-266) correctly OUT OF SCOPE | PASS (noted) | Lines 265-266 still contain `/sc:forensic --tier light --intent triage` and `/sc:forensic --tier standard`. Per spawn instructions this is DEFERRED to Phase 6 Step 6.4 — NOT failed here. Flagged for downstream awareness only. |

---

## Summary

- Checks passed: 12 / 12
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (report-only)

## Issues Found

None in scope.

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| — | (deferred, not a finding) | SKILL.md:265-266 | `/sc:forensic --tier/--intent` persists in Escalation Budget block | Deferred to Phase 6 Step 6.4 per task scope — NOT this lens's responsibility. Recorded so it is not lost. |

## Actions Taken

None (fix_authorization: false).

## Adversarial Self-Audit

The prompt asserted "at least 3 wrong or stale flags." I searched the entire SKILL.md flag surface via grep (not just the cited line ranges) for every forensic-era token. The only surviving `--tier`/`--intent`/`--forensic` references are the two deferred budget lines (265-266), which the spawn prompt explicitly placed out of scope. Within the in-scope Step 3 dispatch (line 215) and Step 4 branches (lines 225-226), every flag cross-checks against troubleshoot.md's real Options table. I cannot manufacture an in-scope failure that does not exist; reporting a false FAIL would be worse than a true PASS. The adversarial premise does not hold for the in-scope surface.

## Confidence

Verified: 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

## Tool engagement

Read: 2 | Grep: 1 | Glob: 0 | Bash: 1 (grep)
(No web research required — all claims are local-file-bound, verified against source-of-truth files directly per Principle 6.)

## Recommendations

- Green light from the flag-translation lens for the §4.5 Step 3 dispatch + Step 4 branches.
- Downstream: ensure Phase 6 Step 6.4 retires the deferred `/sc:forensic --tier/--intent` budget block (lines 265-266) so the migration is complete.

## QA Complete
