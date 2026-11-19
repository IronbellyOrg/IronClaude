# Invariant Probe Results

## Round 2.5: Fault-Finder Analysis (independent agent, reflect-reviewer class, model alias opus; every cited line re-read by the agent)

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | A bare re-claim of an issue already launched at worktree does not get escalated to full, and the return contract reports that correctly | UNADDRESSED (reporting only) | LOW | orca_worktree.py:770-777 keeps the prompt; :1705-1721 returns already_launched whatever the level; the launch entry stores the level (:1626) but Task 4's `pipeline_level: full` (SKILL.md:124) would misreport it |
| INV-002 | interaction_effects | The launch record stops a second agent from starting in a worktree the coordinator owns | UNADDRESSED | MEDIUM | a coordinator-started worker writes only a pending nonce (orca_worktree.py:1515-1523); only cmd_launch writes a `launch` entry (:1619-1631) and already_launched reads only that (:1703-1708); re-claim by the same login is allowed (claim.md:43) and Wave 7 reuses the issue-<N> worktree (claim.md:95); a person's bare claim on a coordinator-owned issue therefore starts a second agent, at full after this plan, without the plan approval Plan B needs (docs/designs/issue-watcher.md:43) |
| INV-003 | guard_conditions | The model resolves `<L>` the same way at Wave 5 and Wave 8 | UNADDRESSED | LOW | Task 4 defines the default only at claim.md:82; Wave 8 (claim.md:120) and SKILL.md:92 use `<L>` undefined; the guard enforces only the record (launch-level-guard.sh:788-805), so a mismatch fails toward refusing |
| INV-004 | guard_conditions | No hook or script treats a missing level as full (A-002) | ADDRESSED | LOW | `--level` required, choices worktree or full (orca_worktree.py:1873, :1883); guard takes the level from the record and maps an invalid word to worktree (launch-level-guard.sh:265-268); launch-level-pre-push.sh never names the levels |
| INV-005 | sufficiency_challenge | Keeping the E-SUBMIT rule text verbatim keeps a bare --submit stopped | UNADDRESSED (consensus partly wrong) | MEDIUM | the rule says "without `--pipeline full`" (issue.md:57, SKILL.md:154, commands.md:371); once the table says "Omitted means `full`" a model that resolves the default first reads the rule as satisfied; the script checks only the resolved level (orca_worktree.py:1900-1901); the design record says "or no `--pipeline`" (flag.md:85) |
| INV-006 | sufficiency_challenge | Tasks 1 and 2 make the simple-feature next steps start without brainstorm | UNADDRESSED | LOW | the chain row is only the suggested route and /sc:recommend makes the final pick (chains.md:7, claim.md:79); tests pin chains.md only |
| INV-007 | sufficiency_challenge | Tasks 3-9 plus the consensus reach every place that states the default | UNADDRESSED | LOW | sc-issue-command.md:44 (B17 "`worktree` (default, ...)") still missed; issue-watcher.md:41, :48 and issue-watcher-setup.md:575 are dated history and can stay |
| INV-008 | count_divergence | Counts the tests pin stay consistent | ADDRESSED (counts); UNADDRESSED (version) | LOW | 6 rows (test_issue_protocol.py:655) and 3 to 2 brainstorm steps (:662) are right; the command version stays 1.1.0 (test_issue_command.py:80-81) although the design bumped it when claim behaviour changed (flag.md:89) |
| INV-009 | collection_boundaries | Edge cases of the two-step row and of a claim with no worktree | ADDRESSED | LOW | K=1 under claim.md:81; full ignores the boundary (launch-prompt.md:26); a failed Wave 7 means no launch (claim.md:118) |
| INV-010 | interaction_effects | full by default changes only "also implements" | ADDRESSED (existing ship gate) | LOW | at level F the guard also allows scheduled turns and IMPL (launch-level-guard.sh:789, :791), covered by OB-H1 item 5 (issue.md:16); the Task 9 mirror copy must be redone after rebasing onto claim-handoff-planb, not hand-merged |

## Summary

- **Total findings**: 10
- **ADDRESSED**: 4 (INV-004, INV-009, INV-010, and INV-008 counts)
- **UNADDRESSED**: 6 (one of them, INV-008, in part)
  - HIGH: 0
  - MEDIUM: 2 (INV-002, INV-005)
  - LOW: 4 (INV-001, INV-003, INV-006, INV-007)

Gate: no HIGH UNADDRESSED item, so convergence is not blocked by invariants. The two MEDIUM items are warnings and carry into the merged verdict.
