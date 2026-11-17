# Wave 3C — blind calibration, reviewer-2 card (opus-class calibrator, disjoint from haiku reviewer)

Note: graded the condensed legacy card file as persisted at dispatch; full verbatim card persisted afterwards from the same reviewer output.

## Card scores

Citation grounding 0.70 / Coverage completeness 0.75 / Deviation-classification clarity 0.60 / Risk surface coverage 0.55 / Recommendation actionability 0.30 → **mean 0.58**.

Citation checks it performed: plan lines 31-87, 91, 94, 19 all correct; issue-summary absence confirmed; four reference agents read (reflect-reviewer.md:64, reuse-auditor.md:50, auggie-reviewer.md:79, troubleshoot-analyst.md:27) — none contains the Constraints sentence; none mentions checked_at or worktree_root (independently corroborates the wording finding).

## per_finding (shadow step 5)

```yaml
calibration:
  per_finding:
    F1: 0.85
    F2: 0.92
```

## Calibrator verdicts on self-reported confidence

F1 0.91 slightly high → 0.85 (the "diff adds only that bullet" clause limits the gap a little); F2 0.99 overstated → 0.92 (finding true and independently corroborated; card body itself gave no evidence lines).

## Classification note (feeds Wave 4)

Calibrator: F1 (weak acceptance criteria) is a coverage gap rather than a spec departure, so "Drift" is a stretch. This is a plan-quality finding, not an executor deviation — the merge debate should treat both F1/F2 as plan-fidelity findings, not UC-2 deviations (UC-1 has no executor work to deviate).
