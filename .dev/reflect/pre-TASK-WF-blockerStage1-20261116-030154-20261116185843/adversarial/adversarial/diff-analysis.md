# Diff Analysis: reviewer-card comparison (third review of the stage 1 plan)

## Metadata

- Generated: 2026-11-16T19:25Z
- Variants compared: 3 (variant 1 = reviewer 1 analyzer/sonnet; variant 2 = reviewer 2 qa/haiku; variant 3 = reviewer 3 refactorer/opus). Variant 1 numbered its findings R3-Fk by mistake; they are cited here as R1-Fk.
- Source of truth for every claim: the plan `.dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md` (`PLAN:n`), the spec `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md` (`SPEC:n`), the stage 2 plan (`STAGE2:n`) and stage 4 plan (`STAGE4:n`).
- Grading rule used by all reviewers: blocking = a requirement or check cannot be met, a wrong or missing result, or data loss; non-blocking = wording, format or a real but harmless weakness.
- Total differences: structural 3, content 13, contradictions 5, unique contributions 6, shared assumptions 4 (UNSTATED 3, STATED 1).

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|---|---|---|---|---|
| S-001 | Card layout | findings blocks with `consequence`, `evidence`, `repair`; then earlier-finding check; then "Other checks"; then verdict | findings blocks, plus a Deviations table and an Adherence summary in the deviation-taxonomy shape | findings blocks, "Checked and found clean" list, earlier-finding check, verdict | Low |
| S-002 | Verdict form | NEEDS-REVISION with a stated alternative ("PASS with notes if R1-F1 is read as non-blocking", confidence 0.6 / 0.7) | single NEEDS-REVISION, confidence 0.87 | single PASS, confidence 0.8 | Medium |
| S-003 | Finding ids | R1 used `R3-Fk` ids (a numbering slip, noted in its card) | `R2-Fk` | `R3-Fk` | Low |

## Content Differences

| # | Topic | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|---|---|---|---|---|
| C-001 | Task 3 gives no outcome values for the `lens-scale` labels (CRITICAL, IMPORTANT, MINOR); stage 2 Task 2 reads them to set row tiers (PLAN:62, PLAN:71, PLAN:151, STAGE2:57, SPEC:211, SPEC:737, SPEC:744) | R1-F1, blocking (closest call), repair `CRITICAL=Blocking; IMPORTANT=Medium; MINOR=Note` | not raised | R3-F4, non-blocking, repair `CRITICAL=Blocking; IMPORTANT=Blocking; MINOR=Medium`, cites REQ-02 | High |
| C-002 | Task 9 takes the scale-map family key "from the `origin` of the ledger row" but `origin` is a protocol name plus finding id (PLAN:151, PLAN:62, PLAN:192, SPEC:353, SPEC:355) | partly: R1-F4 says Task 12 never names where the family key comes from | R2-F1, blocking | R3-F3, non-blocking, repair a `reviewers` column in the scale map | Medium |
| C-003 | SHOW_USER gives the `unsettled` tag (SPEC:369, SPEC:439, SPEC:596) but Task 12 only writes the `classifier` column (PLAN:192) | not raised | R2-F2, blocking | not raised | Medium |
| C-004 | Task 10 supplies the NA marker for M only; C has no NA supplier, so REQ-18 lifts almost every verdict to SHOW_USER (PLAN:166, SPEC:528, SPEC:543) | R1-F2, non-blocking | not raised | not raised | Medium |
| C-005 | Consent binding (REQ-11) and the Offers table have no code owner, yet T8 tests "a resume asks again" and "a changed set is filed without new consent" (PLAN:137, PLAN:124, SPEC:375, SPEC:421-428, SPEC:923) | R1-F3, non-blocking | not raised | not raised | Medium |
| C-006 | Task 12 names no inputs for its command (findings file layout, judge-answers format, deliverable and kind, ledger path, expected revision) (PLAN:192, PLAN:166) | R1-F4, non-blocking | not raised | not raised | Low |
| C-007 | `earlier_decisions` test names a `pending` row but `pending` is not an item state (PLAN:124, SPEC:375, SPEC:381-390) | R1-F5, non-blocking | not raised | confirmed in the earlier-findings check (M-F3 line) | Low |
| C-008 | Stage 2 text quotes stage 1 text that no longer exists (STAGE2:27) and says `__init__.py` "registers nine subcommand modules today" (STAGE2:57) | R1-F6, non-blocking | not raised | R3-F6, non-blocking | Low |
| C-009 | Task 14 may put the literal fence text into `doctor.py`, which T2 in Task 15 then flags (PLAN:222, PLAN:234, PLAN:238, STAGE4:114) | not raised | not raised | R3-F1, non-blocking | Medium |
| C-010 | Task 15 names `STRICT_T2` but never says what it changes; stage 4 says stage 1 "did not name the switch" (PLAN:234, STAGE4:114, STAGE4:119) | not raised | not raised | R3-F2, non-blocking | Low |
| C-011 | New skill text is not checked against the banned-phrase scans of `tests/skills/test_review_severity_rule.py` during stage 1 (test lines 28, 36-51, 117, 172-176; PLAN:66; STAGE2:88, STAGE2:102) | not raised | not raised | R3-F5, non-blocking | Low |
| C-012 | The orchestrator's coverage matrix has no Pass 2 rows for source lines 51 and 52 and for the threshold-name part of line 53 | not raised | R2-F3, non-blocking (audit artifact, not a plan defect) | not raised | Low |
| C-013 | Are the first-review F1-F9 and second-review M-F1-M-F10 fixes real? | all fixed, with live lines | all fixed, with live lines | all fixed, with live lines | Low |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Variant 3 Position | Impact |
|---|---|---|---|---|---|
| X-001 | Grade of C-001 | blocking: stage 2 gets no tier for any row if the executor writes `Conditional` | not raised | non-blocking: the spec text (SPEC:211, SPEC:744) lets the executor fill IMPORTANT=Blocking; fix is cheap | High |
| X-002 | Grade of C-002 | non-blocking (only a gap in the Task 12 inputs) | blocking: a valid ledger row looks like an unknown family and returns UNSET | non-blocking: unit tests with direct keys pass, stage 2 hard-codes the lens-scale row | High |
| X-003 | Grade of C-003 | not raised | blocking: acceptance tests can pass while SHOW_USER rows stay ordinary follow-ups | not raised (R3 lists `unsettled` nowhere) | Medium |
| X-004 | Overall verdict | NEEDS-REVISION (1 blocking) | NEEDS-REVISION (2 blocking) | PASS (0 blocking) | High |
| X-005 | Internal consistency of variant 2 | n/a | R2-F1 is "blocking: yes" but the card's own Deviations table rates it MEDIUM (calibrator note) | n/a | Low |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | 1 | Consent binding has no code owner (C-005) and the NA-for-C consequence (C-004) | High |
| U-002 | 1 | Task 12 interface inputs gap and `FixtureJudge` file format used by stage 2 (C-006) | Medium |
| U-003 | 2 | `unsettled` tag production unassigned (C-003) | Medium |
| U-004 | 2 | Audit-artifact omission in the coverage matrix (C-012) | Medium |
| U-005 | 3 | doctor/T2 literal, `STRICT_T2` effect and the banned-phrase scan gap (C-009, C-010, C-011) | Medium |
| U-006 | 3 | Scale-map `reviewers` column proposal and a fixed lens-scale value set citing REQ-02 (C-002, C-001 repair) | High |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|---|---|---|---|---|
| A-001 | An executor follows the plan literally and does not fill interface gaps from the spec or from the stage 2 plan | all three cards grade "what an executor would write" without a rule for how far an executor may infer | decides whether C-001, C-002, C-003, C-004, C-005 are blocking | UNSTATED, promoted |
| A-002 | The stage 2 plan is consumed as it stands today (its text may change after its own revision) | R1-F1 and R3-F4 rely on STAGE2:57; R1-F6 and R3-F6 on STAGE2:27 | decides whether cross-stage gaps belong to this plan or to the stage 2 plan | UNSTATED, promoted |
| A-003 | A static read of the plan can show that its acceptance checks "can pass" on the current repository | all three cards say "can be met" after greps and reads, not test runs | decides how far the "checks can be met" claims are trusted | UNSTATED, promoted |
| A-004 | The review is advisory and reads the stage 1 plan as written on 2026-11-16 (input tree hash `8ed58ea3...`) | named in each brief | scope of the review | STATED |

## Summary

- Total structural differences: 3
- Total content differences: 13
- Total contradictions: 5
- Total unique contributions: 6
- Total shared assumptions surfaced: 4 (UNSTATED: 3, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: C-001, C-002, X-001, X-002, X-004
- Debate points (S + C + X + A): 25
