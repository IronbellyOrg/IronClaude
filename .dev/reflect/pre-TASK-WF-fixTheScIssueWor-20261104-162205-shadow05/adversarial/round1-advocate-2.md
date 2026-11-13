# Round 1 — Advocate for Variant 2 (qa/haiku)

## Position summary

I am the coverage lens. My card's value is not depth on the stale-text axis — that axis is conceded to R3 — but that it is the only card auditing three surfaces nobody else touched: the coverage matrix as a record (F1), per-span verifiability of a bundled row (F2), and citation sufficiency of the red-run evidence (F3). The merged verdict should adopt R3's stale-text finding as canonical, keep R1/R3's "authorized expansion" classification, and absorb my two uniques as additive rows, because dropping my card deletes the panel's only matrix-integrity and evidence-sufficiency checks.

## Steelman of opponents

**R1 (analyzer, 0.66):** Its root-cause lens caught the stale-text finding directly (F1, plan:26 + plan:45 both quoting `summary.md`), correctly scoped it as documentation-level given the archived package, and its F2 classified the SKILL.md/early-section additions as an authorized expansion with the spec four-file list vs plan:20 — textbook deviation-taxonomy discipline. Its F3 even invited its own calibrator's correction, showing precise AC-wording engagement.

**R3 (refactorer, 0.82):** The only card grounded on disk: `tests/skills/test_issue_worker_agents.py:228/253` prove the plan's byte-exact `summary.md` text no longer matches the test constants' `issue-summary.md`, upgrading stale-text from docs drift to "would fail pinned tests if executed" (F1 MAJOR, F2 unpassable-AC). Its F4 five-copy duplication finding (U-003) names the structural mechanism that made the stale text possible — the duplication already bit once. Four findings, widest lens, highest calibration, deservedly.

## Strengths claimed

1. **Only card that audits the coverage matrix itself (F1).** INF-003 is mapped to Tasks 1-2 and records neither Task 3's SKILL.md edit nor Task 1's early section (citations: source.md:1 four-file list; plan:20). The matrix is the reflect-pre deliverable; an authorized expansion absent from the matrix misleads the next reader even though the expansion itself is fine.
2. **Only per-span verification finding (F2 / U-001, Medium).** INF-001 bundles three distinct spec spans — rationale, consumers (`gh --body-file`, `/sc:recommend`), failure marker `E-WORKER-NO-OUTPUT` (source.md:1) — into one row, while plan:45's AC only lists the paragraph's file names. No AC asserts the spans individually, so "row covered" silently becomes "span verified." It generalizes R3's F2: both are AC-to-evidence mismatch, mine names the class, R3's the instance.
3. **Only evidence-sufficiency finding (F3 / U-002).** The cited excerpt names one spawn-rule failure; the SKILL.md negative test and T2 evidence are not visible, so "a reviewer cannot confirm the per-file red failures or the SKILL.md negative test from the cited lines alone" — the panel's only finding upholding the evidence-validator gate. Two-sided: it affirms T1.AC2 holds (rc=1 recorded) before flagging the excerpt.
4. **Additive, not duplicative.** Both my findings the diff analysis could not cluster into anyone else's (U-001, U-002 are the R2-only rows). Merging my card adds coverage axes at zero redundancy cost.

## Weaknesses conceded

- Calibrated lowest (0.55 vs 0.66 / 0.82); I do not dispute the ranking.
- **No fix guidance in any finding**: all three name gaps, none names remedies.
- **Weakest grounding of the panel**: every citation is source.md or plan; my card cites zero on-disk files. R3's test-file citations are the grounding standard.
- **C-001 miss conceded**: I never surfaced the stale text — my F2 cited plan:45 containing `summary.md` yet used it for bundling, a lens-boundary error (I checked span-to-row mapping, not span-content-vs-disk agreement).
- F3 deflates its own severity to INFO; defensible, but it is why U-002 is valued Low.

## A-001 response

QUALIFY — valid for the unanimous non-blocking call on an archived done/ package, but "never re-executed" is unproven: the package remains the input to any future remediation or template reuse (R3 F1's failure mode), so the merged verdict must state the assumption, not rely on it silently.

## Per-point recommendations

- **C-001:** Concede the miss — winner R3 F1+F2 (disk-grounded at test:228/253), severity MAJOR, non-blocking retained.
- **C-002:** Merge — R1 F2/R3 F3 win the deviation classification (Authorized expansion, INFO); retain my F1 as an additive matrix-record fix ("add a spec-less row for Task 3's SKILL.md edit"), since the classification and the missing row are different defects.
- **U-001:** Keep in the merged verdict as a MINOR coverage-gap row (my F2, Medium value, panel-unique; generalizes R3 F2's AC-to-evidence mismatch into a per-span verification rule).
- **U-002:** Keep as INFO (my F3) but require the fix my card omitted: name the missing citations (per-file t1-red.log lines and the SKILL.md negative-test output) before merge.

Not checked: I did not re-verify any citation against the on-disk task package or test file — the three cards and diff-analysis.md are my entire evidence base, so quotes are as-written, not re-grounded.
