# Refactoring Plan (merge of the three reviewer cards into one verdict)

## Overview
- Base: variant 3 (reviewer 3, opus). Incorporated: variants 1 and 2, and the Round 2.5 probe.
- Output: `.dev/reflect/pre-refactorScIssueC-20261118042013/adversarial/merged-verdict.yaml` (the merged review verdict), with provenance comments.
- Changes planned: 9. Changes not made: 4. Overall risk: Low (document merge).

## Planned Changes
| # | Change | Source | Target in base | Rationale (debate evidence) | Risk |
|---|--------|--------|----------------|----------------------------|------|
| 1 | Replace V3 F1 "owner decision" by a definite plan change: keep the E-SUBMIT-NEEDS-FULL rule, change Tasks 3, 4, 5, 7, and copy the design-record wording "or no `--pipeline`" into issue.md:57, SKILL.md:154 and commands.md:371 | V3 Round 2 P2; probe INV-005 | findings, F1 | all three advocates agreed to keep the rule (R2: V1 0.85, V2 0.95, V3 0.8); INV-005 shows the verbatim rule becomes ambiguous once the default is stated | Low |
| 2 | Grade it BLOCKING (Safety: a bare `--submit` would commit, push and open a PR, which the spec never authorized; flag.md:85 records the opposite rule) | style rule on safety grading; V1 F1, V3 F1 | F1 severity | reviewers graded medium; the grade follows consequence, not label | Low |
| 3 | Add finding: restrict the "waits; run the printed implement command" sentence of claim.md:142 to worktree, plus a test; common grade medium | V1 F2, V2 F1 (downgraded), V3 F6 | new finding | R2 P1: V1 0.7, V2 0.85, V3 0.85 | Low |
| 4 | Add finding: Task 10 staging omits .dev/tasks (CLAUDE.md:35-37) | V2 Round 2 P3, V3 P3 | new finding | agreed 0.9 to 0.95 | Low |
| 5 | Add findings: architecture reference (Task 7), design-record lines 66, 78, 87 and a superseded line at sc-issue-command.md:238 plus :44 (Task 8) | V3 F2 to F4, V1 F5, probe INV-007 | findings F2 to F4 | agreed by V1 and V3 | Low |
| 6 | Add finding: coordinator-owned issue re-claimed bare starts a second agent at full (record as a known risk or add one sentence to Task 3 or 4) | probe INV-002 | new finding, medium | uncontested evidence at orca_worktree.py:1515-1523, :1619-1631, :1703-1708 | Low |
| 7 | Add LOW items: INV-001 pipeline_level for already_launched, INV-003 Wave 8 `<L>` wording, INV-006 plan goal wording, INV-008 version note | probe | notes | uncontested | Low |
| 8 | Record out of scope: worker-brief.txt:17-19 and the owner test-launch rows issue-watcher-setup.md:616-619; mark A-004 CONTRADICTED | V3 P4, V1 P4, V2 P4 | out_of_scope | agreed | Low |
| 9 | Correct tags: V3 F5 and F6 grounded | V3 concession, calibrator | tags | agreed | Low |

## Changes NOT Being Made
- V1 F3 (stricter gate for a bare claim): withdrawn by V1 after re-reading issue.md:16; both levels already need OB-H1 item 1.
- V2 F1 blocking grade for claim.md:142: withdrawn by V2; the text is ambiguous, not observed wrong, and the defect already affects explicit full claims.
- V2 F2 as written (accept a bare --submit): withdrawn by V2; replaced by pinning that a bare --submit stops.
- Treating V3 F1 as an owner question only: replaced by change 1 (a definite plan change), because the owner approved a default change only.

## Review Status
Auto-approved (non-interactive).
