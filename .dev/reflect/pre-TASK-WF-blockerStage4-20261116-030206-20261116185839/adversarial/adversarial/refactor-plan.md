# Refactoring plan: merge into one review card (base V1)

## Overview

- Base variant: V1 (analyzer, sonnet), selected at combined score 0.859 against V3 0.890 by tiebreaker level 1 (debate performance, 7 points won against 3).
- Incorporated variants: V3 (C-003, C-004, F6 merge-line wording, exact fix text for the cap count), V2 (C-006, C-007 as recorded decisions, C-011 note), probe (INV-003, INV-007).
- Changes planned: 12. Rejected alternatives: 4. Overall risk: Low (the merged card changes grades toward the debate's settled grades; every grade is the settled one).
- Output: `adversarial/merged-review-card.md` (the card), `adversarial/merged-verdict.yaml`, `adversarial/adversarial/merge-log.md`.

## Planned Changes

| # | Change | Source | Target in base | Rationale (debate evidence) | Risk |
|---|--------|--------|----------------|-----------------------------|------|
| 1 | Replace the verdict with "PASS: 0 blocking, 7 Medium, 4 minor" and name the dissent history | debate S-001 (3 of 3 advocates at PASS with Medium findings) | Verdict | Round 2 unanimous | Low |
| 2 | Re-grade V1-F1 (cap count) to MEDIUM and add the exact fix: state whether the old cap bullet is folded into the digest and set the expected count (2 if kept, 1 if folded) or rely on the `v2 begin` count | V1-F1, V3-F1, V2 Checked; C-001, X-001 | Findings | V3 advocate conceded blocking; all three at Medium (Round 2) | Low |
| 3 | Re-grade V1-F2 (close enough wording) to MEDIUM with V3's fix (reword the Constraints clause without the banned words) | V1-F2, V3-F2, INV-003 | Findings | probe MEDIUM adopted: two parts of one plan contradict | Low |
| 4 | Add the non-discriminating positive greps as MEDIUM | V3-F3, V2-F3; C-003, X-003 | Findings (new) | unanimous Medium; digest supplies both tokens (SPEC:199, SPEC:201) | Low |
| 5 | Add the Rule 6 heading dependency as MEDIUM | V3-F4; C-004 | Findings (new) | unanimous Medium; S3:183 checks only "that's never minor" | Low |
| 6 | Keep V1-F3 (stale premise) as minor and add the monkeypatch point | V1-F3, V3-F5, INV-005; C-005 | Findings | unanimous minor | Low |
| 7 | Re-grade V1-F4 ("CRITICAL is blocking" kept) to MEDIUM | V1-F4; C-009 | Findings | all three advocates ended at Medium | Low |
| 8 | Re-grade V1-F5 (sibling doubt and label lines) to MEDIUM and merge V3-F7 into it | V1-F5, V3-F7; C-008 | Findings | unanimous Medium after Round 2 | Low |
| 9 | Add the section 10.5 pointer exclusion as MEDIUM and the plugin-mirror decision as a minor owner-tracking note | V2-F1, V2-F2; C-006, C-007 | Findings (new) | V2 advocate withdrew blocking; BRIEF:16 and P4:23, P4:26 | Low |
| 10 | Keep V1-F6 wording gaps as minor and merge V3-F6 (merge line only in `agent_template_qa.md`) | V1-F6, V3-F6; C-010 | Findings | unanimous minor | Low |
| 11 | Add INV-007 (Kept mechanical gates section may not exist) as minor | probe | Findings (new) | LOW, unaddressed | Low |
| 12 | Replace V1's statement "Every test path ... exists (checked by Glob)" by "exists today except the three test files and the skill folder created by earlier stages"; keep V1's per-finding status of H1 to H13 as the Earlier-findings section | scorer correction, V1 Checked | Checked | re-check with `test -e` | Low |

## Changes NOT Being Made

| Diff point | Non-base approach | Why rejected |
|------------|-------------------|--------------|
| C-001 | V3's blocking grade | V3's own advocate conceded: keeping the bullet is not the only reading the text allows (P4:39 "bullets near lines 161 to 163") |
| C-006, C-007, C-009 | V2's blocking grades | V2's advocate withdrew them after reading BRIEF:11-16 and OPEN-QUESTIONS 2.3 and 3.4; the plan records each as a decision |
| C-011 | a plan finding that the coverage matrix is incomplete | a defect of this review's own record, not of the plan; the plan holds the work |
| V3 verdict NEEDS-REVISION | keep as the verdict | rests on the blocking grade that was withdrawn |

## Risk Summary

Every change is a regrade to the settled debate grade or an added finding with cited evidence; rollback = restore the base card.

## Review Status

Auto-approved (non-interactive).
