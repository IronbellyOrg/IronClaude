# Diff Analysis: D14 final disposition (OURS vs CLAY)

## Metadata
- Generated: 2026-11-20 (UTC), by the D14 orchestrating session
- Variants compared: 2 (V1 = position-OURS, V2 = position-CLAY)
- Total differences found: 4 structural, 9 content, 4 contradictions, 7 unique, 6 shared assumptions
- Categories: structural (4), content (9), contradictions (4), unique (7), shared assumptions (6)
- Notation: "Dnn" = `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Dnn/VERDICT.md`. "Planb" = the owner's unpushed branch `ironbelly/issue-watcher-zero-setup-plan` (worktree `claim-handoff-planb`). "686" = PR 686, Clay's rewrite of the watcher. "682" = PR 682, Clay's merged deletion of `issue_pipeline`.
- Live facts checked read-only on 2026-11-20 before this analysis: master head is still `61ac2c2e6`; PR 686 head `8e5ae29ad` open and MERGEABLE; PR 690 head `f3bc77981` open and MERGEABLE; PRs 681, 682, 683, 684 merged; 687 and 689 are issues, not PRs; issue 655 (assignee clayphi) and issue 450 (assignee ironbelly) open; `master` has `protected: false`; a new owner PR 693 (issue 691, claim launch result file, opened 2026-11-20 04:15Z) touches `commands/issue.md`, `sc-issue-protocol/SKILL.md`, `refs/claim.md`, `scripts/orca_worktree.py`, which are files PR 690 also edits; PRs 686 and 690 carry comments only from augmentcode, chatgpt-codex-connector and clayphi (none from ironbelly).

## Structural Differences

| # | Area | V1 (OURS) | V2 (CLAY) | Severity |
|---|------|-----------|-----------|----------|
| S-001 | Section set | Claim, Mechanism, Cited facts, Gets right, Costs, Risks | Same six sections | Low |
| S-002 | Granularity of the answer | A five-part answer (revert, split, stamp, keep-adapt, keep/rescope); only the first two have a mechanism | One order (681, 682, 684, 686, 690) and "follow-ups" | Medium |
| S-003 | Per-item coverage | Names all nine items in the claim; no per-item table | Names 686, 690, 682, 655, 450; silent on the 681 stamp, 683, 684, 687, 689 | Medium |
| S-004 | Conditions before each step | Cites the ordering break (fact 1) but no list of pre-conditions | None | Medium |

## Content Differences

| # | Topic | V1 (OURS) | V2 (CLAY) | Severity |
|---|-------|-----------|-----------|----------|
| C-001 | PR 686 | Split into additive pieces, close the original after re-filing | Merge as is (green, mergeable), fix forward | High |
| C-002 | PR 682 | Revert first, as a new PR | Do not revert; the code never ran live | High |
| C-003 | Order of operations | Revert, then split 686, amend design, then the rest | Design order: 681, 682, 684 (done), 686, 690, then B and E | High |
| C-004 | Design doc (PR 681) | Keep the file, stamp "contested", amend to the unified rules | Keep as the single base for PRs A to E; amend after | Medium |
| C-005 | PR 690 | Keep with named adaptations | Merge after 686 as is | Medium |
| C-006 | Issues 655 and 450 | Keep 450 open, rescope 655 | Keep 655 as tracking issue, fold 450 into it ("replaces 450") | High |
| C-007 | Why merging first is safe or unsafe | Names are cheap to fix only before merge; revert plus 686 breaks the CLI; planb conflicts | `enabled: false` makes landing harmless; follow-ups are cheaper after landing | High |
| C-008 | What the 12 review rounds and green CI prove | Counted as cost of a split | Evidence of merge readiness | Medium |
| C-009 | Cost model | 4,599-line revert plus rework of a 59-file PR | Revert is churn; renames are a grep | Medium |

## Contradictions

| # | Point of conflict | V1 position | V2 position | Impact |
|---|-------------------|-------------|-------------|--------|
| X-001 | Does landing 686 first close the revert option? | Revert plus 686 merge cleanly in git but break the CLI (29 modules fail collection, D03 INV-001) | V2's own risk list admits the break, but uses it as a reason to skip the revert, not to hold 686 | High |
| X-002 | Is the approval gate dropped? | D01 rules the gate stays (R19), so 686's deletions of approval code are unwanted | V2 fact 4 quotes D03's "about 50 percent if the gate is dropped"; D01 rules the opposite, so that premise is not in force | High |
| X-003 | Does `enabled: false` hold the poll off? | Silent | V2 fact 2 relies on it. D03 recommendation 7(b): the closed ship gate (R33) is not built on master; the only hold is `cycle.py:228` `raw.get("enabled", False)`, and the owner's plan wants default-on config (R18). The brake is one config default | Medium |
| X-004 | Who gave notice to whom | No owner review on any PR; the design says "approved by the owner (Clay)" | Clay posted on issue 450 with an `@ironbelly` mention | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | V1 | Concrete ordering break: revert plus 686 gives a failing `superclaude --help` (D03 INV-001) | High |
| U-002 | V1 | Persisted wake names and the registry cost nothing to rename before merge (D08 action 8) | High |
| U-003 | V1 | 686's wake defects M1 and M2 and the blind duplicate start (D10) | High |
| U-004 | V1 | Planb collision: 225 status entries, six shared files; its 13-file patch applies to the revert tree only (D03) | High |
| U-005 | V2 | Review history, CI green and 12 rounds: real effort a split discards | Medium |
| U-006 | V2 | PR 683 already refers to `/sc:issue --plan`, which exists only once 690 lands (D13) | Medium |
| U-007 | V2 | The owner's alignment records (PRs 587 to 589) mark the handoff DEFERRED, not rejected | Low |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Classification | Impact | Status |
|-------|-----------|------------------|----------------|--------|--------|
| A-001 | The revert tree builds and its tests pass | Both weigh the PR 682 revert | UNSTATED (D03 Unverified: full suite did not finish) | High | Promoted |
| A-002 | Clay, the owner or an agent will do the re-filing work of a split | V1 split, V2 follow-up PRs | UNSTATED | Medium | Promoted |
| A-003 | `enabled: false` is a reliable brake on a poll | V2 fact 2; V1 does not contest | UNSTATED (see X-003) | Medium | Promoted |
| A-004 | The owner's chat decisions will be given and recorded before any step | Both | STATED (D01, D03, D04 actions all name chat decisions) | High | Not promoted |
| A-005 | Master does not move in a way that changes these answers | Both | STATED, verified today (head `61ac2c2e6`) | Low | Not promoted |
| A-006 | One person decides for the repository ("the owner") | Both | CONTRADICTED: the design says "the owner (Clay)", decision records say ironbelly, and the host login is shared | High | Promoted |

## Summary
- Total structural differences: 4
- Total content differences: 9
- Total contradictions: 4
- Total unique contributions: 7
- Total shared assumptions surfaced: 6 (UNSTATED: 3, STATED: 2, CONTRADICTED: 1)
- Highest-severity items: C-001, C-002, C-003, C-006, C-007, X-001, X-002, U-001 to U-004, A-001, A-006
- Diff points counted for convergence (S + C + X + promoted A): 4 + 9 + 4 + 4 = 21
