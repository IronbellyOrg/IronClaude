# Refactoring Plan: Merge into Base (Variant 1)

## Overview
- Base: Variant 1 (sonnet:analyzer) = `variant-1-original.md`
- Incorporating strengths from: Variant 2 (haiku:qa) = `variant-2-original.md`; Round 2.5 invariant probe (`invariant-probe.md`)
- Planned changes: 17 (revision 2, after the analytical review FAIL of revision 1: B-1, B-2, B-3 and minor notes fixed; see Review Status)
- Risk level: Medium overall (findings change severity and classification; no source text outside the card is edited)
- Output: `adversarial/merged-output.md` (the merged reviewer verdict). Every finding keeps its original id; new rows get `M-n`. Every section carries a provenance comment. The merged header states the debate status `BLOCKED_BY_INVARIANTS (INV-001)` and the unresolved point X-001.

## Planned Changes

### Change 1: Raise R1-4 to HIGH and merge R2-5 (from Variant 2)
- **Source**: V2 §Findings R2-5
- **Target**: Base §3 row R1-4 (replace)
- **Rationale**: C-005 V2 95%; V1 conceded in R1 and R2 (new evidence 1: an agentless setup terminal also matches plan :53's count/agent guard, so `result.setup`/`result.defaultTabs` are the only discriminator).
- **Integration point**: R1-4 becomes HIGH; add the `created_scene()` "opaque, not json" (test_issue_orca_worktree.py:376) and FO-11 `warning is None` (:552-561) conflict, the valid-reply fixture, list failure/malformed/zero-terminal tests; mark "Agrees F5; merged R2-5".
- **Risk**: Low

### Change 2: Add repository-identity guard finding (from Variant 2, at MEDIUM)
- **Source**: V2 R2-6
- **Target**: Base §3, new row M-1 after R1-4 (insert)
- **Rationale**: U-001 and X-002 merged: identity before any close, MEDIUM (V2 conceded severity in R2 item 4).
- **Integration point**: Evidence orca_worktree.py:507-513 vs :618-645; remedy: close only after the git-common-dir check, foreign-repo fixture → failed/stale, zero close calls.
- **Risk**: Low

### Change 3: Gate a close inside `finish()` on status `created` (from invariant probe)
- **Source**: invariant-probe.md INV-004
- **Target**: M-1 remedy (append)
- **Rationale**: `finish` is shared with `reuse_record` and the reused path (orca_worktree.py:494-552, :575).
- **Risk**: Low

### Change 4: Add INV-001 as a HIGH finding (from invariant probe)
- **Source**: INV-001
- **Target**: Base §3, new row M-2 (insert, top of HIGH rows)
- **Rationale**: Gate-blocking HIGH UNADDRESSED; orchestrator re-read orca_worktree.py:198-206, :232-235: `min(..., key=WARNING_ORDER.index)` raises `ValueError` for a code not in the list, so `W-FIRST-TAB-LEFT` as the only note on a created worktree crashes the script before it prints JSON.
- **Integration point**: Remedy: Task 3 adds `W-FIRST-TAB-LEFT` to `WARNING_ORDER` at a stated rank, and to the worktree-warning enumeration at SKILL.md:149 as well as the claim.md Wave 7 table; tests where it is the only note AND where it appears alongside another note (e.g. `W-WORKTREE-COPY-FAILED`, orca_worktree.py:526), since the `min` runs over every note code (analytical review, check 5).
- **Risk**: Low

### Change 5: Add the other MEDIUM UNADDRESSED probe items (from invariant probe)
- **Source**: INV-002, INV-003, INV-006, INV-007, INV-010, INV-012
- **Target**: Base §3, new rows M-3 to M-8 (insert, MEDIUM)
- **Rationale**: Warnings from the invariant gate; not covered by either card. INV-005 folds into R1-3/R1-5 (close effectiveness, `--tab`) and Task 8 live check; INV-008/INV-009 already in R1-2; INV-011 already in R1-11; INV-014 folds into R1-9; INV-013 becomes LOW row M-11.
- **Integration point (remedies are the orchestrator's minimal proposals; the probe supplied assumptions only)**:
  - M-3 (INV-002): state in Task 3 which post-create paths (list failure → reused record, AMBIGUOUS, not listed, not on disk) leave the plain tab, report `W-FIRST-TAB-LEFT` on each, and say a re-run's reused match does not close.
  - M-4 (INV-003): state what happens when the copy or record write fails after the close (no tab, no agent) and give its remedy line; this is in open tension with M-1's "close before the copy" placement — the plan must choose: close after a successful copy (keeps the tab on failure) or before (as now) with this consequence accepted.
  - M-5 (INV-006): the hook's block message and CLAUDE.md example must not combine `--agent` with `--activate` or hooks unless verified not to seed a plain terminal (REPORT.md:51); add to Task 8 live checks.
  - M-6 (INV-007): list `bash -c`, `sh -c`, `eval`, `ssh host '…'`, `cat <<EOF | bash` as known ceilings in the hook header and t8-delivery.md.
  - M-7 (INV-010): t8-delivery.md "not covered" section (merge with R1-12).
  - M-8 (INV-012): state who reads `worktree_warning` in unattended runs (the `/sc:issue` Final output must print it) and add a pin that it is printed.
- **Risk**: Low

### Change 6: Merge R2-1 test cases into R1-1 (from Variant 2)
- **Source**: V2 R2-1
- **Target**: Base R1-1 recommended change (append)
- **Rationale**: C-001 merged; V2 adds backticks, comments/newlines, both command orders, nested substitution; INV-007's quoted-execution forms go in the ceilings list.
- **Risk**: Low

### Change 7: Add R2-2 fail-open and full-message tests (from Variant 2)
- **Source**: V2 R2-2
- **Target**: Base R1-2 (append as second half)
- **Rationale**: C-002 disjoint halves, 95%.
- **Risk**: Low

### Change 8: Replace R1-13 remedy with the executable test (from Variant 2)
- **Source**: V2 R2-3
- **Target**: Base R1-13 (replace remedy; raise to MEDIUM)
- **Rationale**: C-003 V2 95%; V1 conceded.
- **Risk**: Low

### Change 9: Correct R1-6 line list and merge R2-7, R2-8 (from Variant 2)
- **Source**: V2 R2-7, R2-8; diff analysis C-007/X-004
- **Target**: Base R1-6 (replace line list) + new row M-9 for R2-8
- **Rationale**: "Union minus verified-not-stale lines" (X-004 90%, C-007 95%). Drop SKILL.md :89, :92 (already conditioned), SKILL.md:150 (already says no launch for `none`, re-read by the analytical review) and issue.md:64 (example invocation, verified not stale in C-007); add SKILL.md :90-91. Final list: SKILL.md :17, :90-91, :170 and the return-contract block (four worktree fields null for `none`, ten keys kept); claim.md :93, :131-136. Plus user guide commands.md :367, :379, :394 (re-read, stale) and HOW-WE-WORK.md:329 + plugin mirror (U-002; :329 to be re-read by the evidence validator).
- **Risk**: Low

### Change 10: Merge R2-9 into R1-7 (from Variant 2)
- **Source**: V2 R2-9
- **Target**: Base R1-7 (append)
- **Rationale**: C-008 merged 95%.
- **Risk**: Low

### Change 11: Correct R1-11 misattribution
- **Source**: diff analysis U-014; V1 R1 concession
- **Target**: Base R1-11 (modify)
- **Rationale**: Plan :19 does not claim the policy is enforced; finding becomes "say explicitly that only the `--agent` half is enforced" without the misattribution.
- **Risk**: Low

### Change 12: Move the Task 3/5 departure out of the class table into a Grounding Gap
- **Source**: debate X-001 (unresolved, 50%), A-005 (V2 85%), reflect taxonomy §10.4-§10.6 (SKILL.md:1026-1093)
- **Target**: Base §4 rows 1, 2 and 3 (the create → copy → launch departure, the first-tab close, D2/FO-18 staying) and base §2 row (2) "Covered by documented deviation" (replace all four), plus a new "Grounding Gaps" section and new row M-10 (decision).
- **Rationale**: Drift withdrawn by both. V1 argues Necessary (inline rationale, real ordering constraint); V2 argues source.md:1 states an explicit restriction ("keep `agent launch` only for an already existing worktree") that the plan contradicts, which §10.5 says rationale cannot authorize (Regression signal). V1 conceded "only way to meet the intent" overreaches (R2 response 1; A-005). The deciding fact, owner approval of plan :20, is not in any debate artifact (A-003 records it as unverified). §10.6 has no `unknown` class, so the departure leaves the class table and goes to a Grounding Gap row.
- **Integration point**:
  - §4: remove rows 1-3; add one line "Rows for the Task 3/5 departure, the first-tab close and D2/FO-18 are not classified; see Grounding Gaps (G-1)." §2 row (2): "Departs from the source; classification pending G-1".
  - New "Grounding Gaps" section with G-1: `hunk_ref: plan :20, :53, :75 (Tasks 3, 5)`; `evidence_missing: recorded owner approval of the plan :20 departure (plan says only "stated to the owner before planning")`; `why_not_classifiable: Necessary if approved or genuinely forced; Regression under §10.5 if it contradicts the source's explicit restriction without approval; neither can be decided without the owner's answer`; `next_evidence_needed: ask the owner whether the bare create → copy → agent launch + first-tab close replacement is approved`; `owner: user`; `decision_needed_by_user: true`.
  - Header note: a non-empty Grounding Gaps section means `needs_human_decision: true` and the forced non-success status that §10.6 (SKILL.md:1089) and the report template require for the reflect report.
  - Also reword the base's other "deviation" phrases so none reads as a justification: line 9 ("documented and mostly justified" → "documented; classification pending G-1"), line 22 (out-of-scope "documented deviation" → "plan departure, see G-1"), line 46 ("covered only through the Constraints deviation" → "covered only through the plan :20 departure, see G-1").
  - M-5's REPORT.md:51 is `.dev/troubleshoot/bug-agents-run-orca-worktree-create-20261108015205/REPORT.md:51` (to be confirmed by the evidence validator).
  - M-10 remedy: record the owner's answer in plan Constraints before Tasks 3 and 5 run; if rejected, a redesign must keep "failed copy = no agent" (V2 R2 item 5) and weigh alternatives (A-005: e.g. publishing the nonce before the create, an absolute-path prompt), none verified. Severity: orchestrator's choice of HIGH (gates two tasks), not a debate award.
  - Orchestrator observation (not debate evidence): a search of this session's transcript found no recorded approval.
- **Risk**: Medium (changes the headline classification)

### Change 13: Add V2's per-task acceptance table and T1 rulings (from Variant 2)
- **Source**: V2 §Per-task acceptance review, §Other T1 findings checked
- **Target**: Base, new §2a after §2 (insert) and §3a (insert)
- **Rationale**: S-003 V2 90%; S-005 V2 85%; C-011 F2 ruling (keep Orca prerequisite, record the decision), F8, F9 caveat.
- **Risk**: Low

### Change 14: Update grade, verdict and confidence
- **Source**: debate C-010, S-007; calibrations
- **Target**: Base §1 and §5 (replace)
- **Rationale**: Both advocates at 3/5; verdict "revise before execution; record the owner decision first". Report calibrated card scores (V1 0.83, V2 0.89: rubric means dominated by citation grounding, i.e. how well each card's claims held, not the probability the plan works) and V2's own revised self-report 0.75; no new self-report.
- **Risk**: Low

### Change 15: Carry the F3 line-range ruling (from Variant 2)
- **Source**: V2 R2-7 refutation; matrix C-012 (V2 70%)
- **Target**: Base §3a (new T1 rulings section, Change 13)
- **Rationale**: Plan's 105-134 holds the return fields (:121-134); only the prose line :136 lies outside.
- **Risk**: Low

### Change 16: Note that agreement with T1 is anchored (from Variant 2)
- **Source**: matrix A-004 (V2 85%)
- **Target**: Base §3 closing line (append)
- **Rationale**: The "Agrees Fn" markers record agreement after seeing T1; each finding stands on its own cited evidence, not on the count of cards agreeing.
- **Risk**: Low

### Change 17: Add the re-read-before-editing caveat (merge)
- **Source**: matrix A-007 (Merge 95%)
- **Target**: Base §5 (append)
- **Rationale**: Plan anchors are approximate (e.g. `:614-640` vs the new-row block ending at :646); the executor re-reads `cmd_worktree`, `finish`, `Outcome.as_dict` and the cited tests before editing.
- **Risk**: Low

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|------------|-------------------|---------------------------|
| X-001 | V2 "Drift" label | Withdrawn by V2 in R2 item 1 (§10.3 requires a silent change). |
| X-002 | V2 R2-6 at HIGH | V2 conceded MEDIUM (R2 item 4). |
| C-004 | V2 "restore agent-on-create" as co-equal default remedy | V2 conceded it loses "failed copy = no agent" (R2 item 5); kept only as one option under the owner decision. |
| C-010 | V2 grade 2/5 | V2 revised to 3/5. |
| S-007 | V2 confidence 0.91 | V2 revised to 0.75; calibrated 0.89 reported alongside. |
| X-001 (V1 side) | Base "Necessary deviation" for §4 rows 1-3 | Not kept as a class: V1 conceded "only way to meet the intent" overreaches (R2 response 1); A-005 to V2; class moved to Grounding Gap G-1 (Change 12). |
| X-001 (V2 side) | "Prospective Regression" class | Not adopted as a class either: it holds only if the owner did not approve, which is the open fact (G-1). |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 12 | Medium | Headline class misreported | Restore the base §4 rows only after the owner approves in G-1; keep M-10 |
| 1-11, 13-17 | Low | A finding mis-merged | Revert the affected row to its base or V2 text |

## Review Status
- Auto-approved (default; not interactive), gated on the analytical review.
- Review round 1 (sonnet analytical agent, 2026-11-08T04:14Z): FAIL. Blocking: B-1 (Change 12 fixed only §4 row 1; rows 2-3 and §2 row (2) kept the withdrawn premise), B-2 (pseudo-class "Grounding Gap" in the class table; required §10.6 fields missing; transcript search presented as debate evidence), B-3 (Change 9 kept non-stale issue.md:64 and SKILL.md:150). Minor: Change 5 had no remedies, M-1/M-4 tension unstated, Change 14 confidence wording, M-10 severity provenance, unnumbered LOW row, SKILL.md:149 enumeration, header status, INV-001 test should cover "with another note"; missing V2/merge awards C-012, A-004, A-007.
- Revision 2 (this file): all three blocking findings and every minor note addressed (Changes 4, 5, 9, 12, 14 revised; Changes 15-17 added; NOT-made table extended).
- Review round 2 (same analytical agent, re-read the revised file, 2026-11-08T04:16Z): PASS. B-1, B-2, B-3 resolved; no new blocking defect. Minor notes 1-4 applied (Change 12 rewording of base lines 9, 22, 46; forced status; rollback wording); note 5 resolved by giving REPORT.md's full path; note 6 is this entry.
- Approved by: auto (after review round 2 PASS)
- Approval timestamp: 2026-11-08T04:17:30Z
