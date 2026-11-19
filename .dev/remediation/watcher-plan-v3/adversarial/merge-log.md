# Merge Execution Log

## Metadata
- Base: Variant 2 (opus:architect), `adversarial/variant-2-opus-architect.md`
- Executor: merge-executor agent
- Merged output: `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/remediation/watcher-plan-v3/remediation-proposal.md`
- Changes applied: 24 of 24 planned (8 V rows, 8 S rows, 5 K rows, 3 T rows)
- Status: success
- Timestamp: 2026-11-19

## Changes Applied

Validation key: Structure = heading and ordering intact; Refs = every cited line either read this session or marked carried; Contra = no new contradiction.

### Change V-1: Self-approval, warn-first
- **Status**: Applied
- **Source**: Variant 1 Q-1 Part B, softened by Round 2 verdict 1
- **Target**: Q-1 "Self-approval, Part B"; Decision 3; residual risks
- **Before**: Base residual risk 1 only
- **After**: `excluded_ids` default empty, one config key, warning in `check-config` and Task 17 report, generator rule, tamper-list caveat
- **Provenance tag**: `<!-- Source: Base (Variant 2 Q-1), modified by V-6 ... -->` on Q-1
- **Validation**: Structure ok | Refs ok (predicates.py:185, 216-223; cycle.py:58-69, 883, 998; cli.py:185-198 read; source.md:64 carried) | Contra ok. Judgment: V-1 assigned to Task 6 because `cycle.py` is edited there; the plan did not assign it.

### Change V-2: Reason order in `_revalidate`
- **Status**: Applied
- **Source**: Variant 1 Q-4
- **Target**: Q-4 (replaces the base "time check runs first" sentence)
- **After**: approval reread, then time rule, then equality
- **Validation**: Structure ok | Refs ok (cycle.py:1007-1016 read) | Contra ok

### Change V-3: Ship gate constant plus coupling test
- **Status**: Applied
- **Source**: Variant 2 Q-2 Option A, Variant 1 coupling test
- **Target**: Q-2; Decision 1
- **Validation**: Structure ok | Refs ok (launch.py, cycle.py:1026-1028, audit.py:26,71-80, test_launch_level_observations.py:79-84 read; design:201 carried) | Contra ok

### Change V-4: Field-value times, unreadable voids
- **Status**: Applied
- **Source**: Variant 2 Q-3 Option C, Variant 1 (unreadable voids), Variant 3 (same-second)
- **Target**: Q-3; Task 3a; Decision 2
- **Validation**: Structure ok | Refs ok (github.py:88-103, predicates.py:112-118, 257 read) | Contra ok. Docs fact on `updatedAt` kept as carried and listed in Not verified.

### Change V-5: `complete.run` alternative
- **Status**: Applied (weak row, marked best-effort and in Decision 6)
- **Source**: Advocate 1 proposal
- **Target**: Q-1 code item 4
- **Validation**: Structure ok | Refs ok (guard:444 read) | Contra ok

### Change V-6: Blocked class covers issue, label, project
- **Status**: Applied
- **Source**: Variant 2 Q-1 catch-all, Variant 1 label/project scope
- **Target**: Q-1 code items 1 to 3
- **Validation**: Structure ok | Refs ok (guard:646-655, 786-806 read) | Contra ok. Correction: the `for LL_C in` list is at guard:786, not 788 as the debate cited.

### Change V-7: Seven test files into Task 6
- **Status**: Applied
- **Source**: Variant 2 Q-7, Variant 1 tip
- **Target**: Q-7; task list table
- **Validation**: Structure ok | Refs ok (launch.py:33, 92, 101 read; per-file counts carried) | Contra ok

### Change V-8: Per-run result marker
- **Status**: Applied (weak row, in Decision 6)
- **Source**: Variant 1 Q-6 idea, key changed to approval event id
- **Target**: Q-6
- **Validation**: Structure ok | Refs ok (record.py:545-547, predicates.py:14, 253-255 read) | Contra ok

### Change S-1: Narrow coordinator pattern keeps pytest allowed
- **Status**: Applied | **Target**: Q-1 item 4 and must-allow tests | **Validation**: ok

### Change S-2: Guard version stamp to 2
- **Status**: Applied | **Target**: Q-1 item 5 | **Validation**: ok (guard:10, plugin mirror line 10, orca_worktree.py:839, the three test pins all read)

### Change S-3: Compare-and-set on Status
- **Status**: Applied | **Target**: Q-5 | **Validation**: ok

### Change S-4: DF-14 restated
- **Status**: Applied | **Target**: Q-8 | **Validation**: ok (test_security_invariants.py:919 read; DF-14 text carried)

### Change S-5: No config key as gate switch
- **Status**: Applied | **Target**: Q-2 | **Validation**: ok (guard:763-765 read)

### Change S-6: plan:23 scope wording
- **Status**: Applied | **Target**: Q-1 plan edits, Decision 6 | **Validation**: ok

### Change S-7: Governed sessions documented, unbound test
- **Status**: Applied | **Target**: Q-1 plan edits, Q-9 | **Validation**: ok (guard:153-154, 391 read; guard:257-268 and claim.md:118 carried)

### Change S-8: Ordering and push sentence
- **Status**: Applied | **Target**: Q-10 | **Validation**: ok (WORKER-CONTRACT.md:245 read)

### Changes K-1 to K-5
- **Status**: Applied (K-1 loop entry in Q-1 item 2; K-2 allow rows in item 1; K-3 hyphen alternative in item 4 and tests; K-4 in the header edit rule; K-5 as Decision 4)
- **Validation**: ok

### Changes T-1 to T-3
- **Status**: Applied (T-1 in Q-3 plan edit for plan:70; T-2 outcome table in Task 3a text; T-3 ranked impact and rollback lines in residual risks)
- **Validation**: ok

## Invariant coverage
I-1 to I-17 mapped: I-3, I-4, I-5, I-6, I-12, I-13, I-14, I-16, I-17 addressed in text; I-7 lifted by the Q-1 message text and tests; I-1, I-2, I-8, I-9, I-11, I-15 carry their declared limits in Q-1, Q-3, Q-9; I-10 stays open as Decision 4.

## Post-Merge Validation

### Structural Integrity
- Heading hierarchy: ok (H1, H2 per section, H3 inside Decisions)
- Section ordering: ok (decisions, task list changes, Q-1 to Q-10, residual risks, not verified)
- Document flow: ok

### Internal References
- Total references: about 70 file:line citations
- Resolved: all read this session except those listed under Not verified and marked carried
- Broken: 0. One debate citation corrected (guard:788 to guard:786).

### Contradiction Re-Scan
- New contradictions introduced: 0
- Note: refactor-plan row V-1 cites plan:24 and plan:209 for edits; plan:24 is the approval constraint and plan:209 the Task 15 body, both confirmed.

## Summary
- Total changes planned: 24
- Successfully applied: 24
- Failed: 0
- Skipped: 0
- Post-merge validation: PASS
- Constraint check: only three files written; the plan package and the repo are untouched.
