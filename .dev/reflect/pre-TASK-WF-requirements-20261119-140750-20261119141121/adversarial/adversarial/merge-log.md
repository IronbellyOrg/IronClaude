# Merge Execution Log

## Metadata
- Base: Variant 3 (opus:refactorer), `reviewer-cards/reviewer-3-card.md`
- Executor: merge-executor agent
- Changes applied: 31 of 31 planned (R-01 to R-31 of `refactor-plan.md`); 22 become register rows P4-1 to P4-22, the other 9 are folded into rows or sections as listed below
- Status: success (every planned row applied; the pipeline status is partial because convergence was 0.784, NOT_CONVERGED, see the return contract)
- Timestamp: 2026-11-19

Merged output: `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/reflect/pre-TASK-WF-requirements-20261119-140750-20261119141121/adversarial/merged-output.md`

## Changes Applied

Register mapping (plan row to merged row; final grade from `round2-rebuttals.md` section 3).

### Change 1: R-01 cross-repo approval read (C-001)
- **Status**: Applied
- **Source**: Variant 3, B-1 (V1 and V2 did not find it)
- **Target**: Base B-1, now P4-1 Blocking (Safety); evidence cites re-read in this run (`cli.py:279,282,343-348`, `reads.py:65-67,142,148`, `github.py:37,75,89`, `WORKER-CONTRACT.md:242,298`)
- **Before**: B-1 fix "thread --repo ... or limit the dispatcher"
- **After**: fix names the files, the `repo` parameter chain, the second-repo test, the WORKER-CONTRACT.md:242 rewording and the plan:30 addition
- **Provenance tag**: `<!-- Source: Variant 3 B-1 (base) ... -->`
- **Validation**: Structural integrity OK | References OK | Contradictions OK

### Change 2: R-02 empty Pipeline (C-002)
- **Status**: Applied
- **Source**: Variant 3, B-2
- **Target**: P4-2 Blocking (Decision)
- **Before**: fix "tell no value from unreadable"
- **After**: exact Task 3 and Task 5 sentences and four acceptance rows from the plan
- **Provenance tag**: `<!-- Source: Variant 3 B-2 (base); Round 2 verdict C-002 ... -->`
- **Validation**: OK | OK | OK

### Change 3: R-03 claim-time approval check (C-003)
- **Status**: Applied
- **Source**: Variant 2, QA-2; Variant 3 located the rule (`stage_predicates.py:161-170`)
- **Target**: new P4-3 Blocking (Decision) (base card had no finding)
- **Before**: section did not exist
- **After**: evidence from `approval_record.py:313-338`, `stage_predicates.py:161-170`, `test_stage_predicates.py:281`; replacement acceptance bullet
- **Provenance tag**: `<!-- Source: Variant 2 QA-2 ... -->`
- **Validation**: OK | OK | OK

### Change 4: R-04 and R-24 guard pattern (C-004 + X-001)
- **Status**: Applied
- **Source**: Variant 2 QA-3, Variant 3 M-4 (replaced), Variant 1 M-5
- **Target**: base M-4 replaced and regraded; now P4-4 Blocking (Decision); the over-match pointer R-24 is merged into it
- **Before**: Medium, "delete the second option and anchor on the verb word"
- **After**: Blocking (Decision); anchored patterns, replacement of the bare case, unmatched string-built forms, accepted over-matches; the case-run results marked carried
- **Provenance tag**: `<!-- Source: Variant 2 QA-3, Variant 3 M-4, Variant 1 M-5; Round 2 verdict C-004 + X-001 ... -->`
- **Validation**: OK | OK | OK

### Change 5: R-05 brief levels (C-006)
- **Status**: Applied
- **Source**: Variant 3, B-3
- **Target**: P4-5 Blocking (Decision); adds `brief.py:51-74` and `:73-74` evidence
- **Provenance tag**: `<!-- Source: Variant 3 B-3 (base) ... -->`
- **Validation**: OK | OK | OK

### Change 6: R-06 R6 and R9 lifecycle (C-005)
- **Status**: Applied
- **Source**: Variant 2, QA-1; graded Medium by the arbiter (V2 argued Blocking (Missing))
- **Target**: P4-11 Medium
- **Provenance tag**: `<!-- Source: Variant 2 QA-1; Round 2 verdict C-005 ... -->`
- **Validation**: OK | OK | OK

### Change 7: R-07 retry has no stored Status (C-007)
- **Status**: Applied
- **Source**: Variant 1 M-2, Variant 3 M-2
- **Target**: P4-8 Medium (evidence `cycle.py:1308-1314`, `record.py:68-88` re-read)
- **Validation**: OK | OK | OK

### Change 8: R-08 live-item helper order (C-008)
- **Status**: Applied
- **Source**: Variant 1 M-1
- **Target**: P4-7 Medium
- **Validation**: OK | OK | OK

### Change 9: R-09 pr-submit and the guard (C-011)
- **Status**: Applied
- **Source**: Variant 3 M-3 (reworded: wrapper scripts not seen, inline forms refused)
- **Target**: P4-9 Medium; wrapper and refs lines marked carried
- **Validation**: OK | OK | OK

### Change 10: R-10 Task 19 vs Task 24 Project count (C-014)
- **Status**: Applied
- **Source**: Variant 2 QA-4
- **Target**: P4-10 Medium
- **Validation**: OK | OK | OK

### Change 11: R-11 Q-6 gap
- **Status**: Applied as a pointer
- **Source**: Variant 3 (Q-6 PARTIAL); the plan grades it Note ("see R-16")
- **Target**: merged into P4-16 Note (not a separate Medium row)
- **Validation**: OK | OK | OK

### Changes 12 to 22: Note rows R-12 to R-22
- **Status**: Applied (R-12 to R-21 as P4-15, P4-21, P4-12, P4-14, P4-16, P4-17, P4-18, P4-13, P4-19, P4-20); R-22 (keep Tasks 7 and 13 whole) is a no-fix item carried in the No-finding list
- **Source**: Variant 1 M-3, N-1, N-2; Variant 3 M-1, M-5, N-1 to N-6; X-002, X-003
- **Provenance tag**: one comment per row in the merged output
- **Validation**: OK | OK | OK

### Change 23: R-23 Task 4 is a planned halt (A-002 / I-10)
- **Status**: Applied
- **Source**: shared assumption A-002 (no card questioned it)
- **Target**: new P4-6 Medium, marked not verified against the executor (I did not read the executor's stop behaviour)
- **Validation**: OK | OK | OK

### Changes 24 to 28: pointers R-24, R-25, R-26, R-27, R-28
- **Status**: Applied (R-24 into P4-4; R-25 as P4-22 Note; R-26 and R-27 folded into P4-12; R-28 into the No-finding list and P4-1)
- **Validation**: OK | OK | OK

### Change 29: R-29 status table
- **Status**: Applied as the "Confirmed fixed" line (Q-1 PARTIAL while P4-4 is open, Q-6 and Q-10 PARTIAL at Note level, Q-3 FIXED with P4-2)
- **Validation**: OK | OK | OK

### Change 30: R-30 coverage
- **Status**: Applied in the No-finding list (R1 to R33 each map to a task; V2's partials mapped to P4-11, P4-10, P4-3 and P4-4/P4-15)

### Change 31: R-31 not checked
- **Status**: Applied as the "Not checked" list, plus a list of citations carried and not re-read in this run

## Post-Merge Validation

### Structural Integrity
- Heading hierarchy: OK. H1 title; H2 Findings, Convergence, Decisions, No-finding list, Not checked; H3 per finding and per grade group.
- Section ordering: OK. Findings ordered by grade (Blocking, Medium, Note) then plan task, as the plan states.
- Document flow: OK.

### Internal References
- Total references: 22 finding ids plus Q-1 to Q-10 mentions
- Resolved: all. P4-n ids used in the header, status line, convergence section and No-finding list each exist.
- Broken: 0

### Contradiction Re-Scan
- New contradictions introduced: 0
- One point checked: the header says "5 blocking, 6 medium, 11 notes"; the register has P4-1 to P4-5 Blocking, P4-6 to P4-11 Medium, P4-12 to P4-22 Note, which matches.

### Evidence-citation rule
- Every file:line in an Evidence line was re-read in this run, except the ones the merged output marks "carried" (cli.py:52 and :134-158, test_stage_status.py:63, predicates.py:24 and :181-182 and :205, the pr-submit wrapper and refs lines, remediation-proposal.md:132 and :205, the two doc lines of P4-18, and the case run of P4-4, which the orchestrator ran). The doc lines 1070 and 1443 did not show up in a re-grep and are stated as unconfirmed.

## Summary
- Total changes planned: 31
- Successfully applied: 31
- Failed: 0
- Skipped: 0
- Post-merge validation: PASS
- Open issue: convergence 0.784 against 0.80 (NOT_CONVERGED); C-004 / P4-4 is the one unresolved grade (arbiter: Blocking (Decision))
