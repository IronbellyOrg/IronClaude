# Refactoring Plan: Merge into Base (D04 claim level and grants)

## Overview
- Base: Variant A (OURS, position-OURS.md copied as variant-1-original.md)
- Incorporating strengths from: Variant B (CLAY, variant-2-original.md)
- Planned changes: 9
- Risk level: Medium overall (the merged text changes the recommendation of the base from "Pipeline picks the level now" to a hybrid; facts are unchanged)
- The merged output is a unified position (the debate's resolved answer), not a third advocate paper: it states the winning rule, the conditions the invariant probe adds and the open points.

## Planned Changes

### Change 1: Live rule is a none-only claim (from Variant B)
- **Source**: Variant B, Claim and Cited fact 1; debate Round 2 (both advocates); scoring rows C-001, C-004
- **Target**: Base, Claim (replace)
- **Rationale**: Both advocates agree the only live behaviour is `--pipeline none` (R33, `launch.py:33`, `commands/issue.md:48`); confidence 90% (C-004)
- **Integration point**: Replace the opening Claim paragraph; keep the Pipeline field as the named gate-open selector
- **Risk**: Medium (changes the base's headline)

### Change 2: One supervised route for the live rule (from Variant B)
- **Source**: Variant B, Mechanism 1 and 2; Cited fact 3
- **Target**: Base, Mechanism (insert new item)
- **Rationale**: C-002, 75%: `worker-start` plus mailbox is the only route that runs; K4 (D:1226) states a one-route reason independent of the gate
- **Integration point**: New Mechanism item before the guard item
- **Risk**: Low (additive)

### Change 3: Grants split: four standing, two per PR (hybrid)
- **Source**: Variant B Mechanism 3 (list), Variant A Cited fact 6 and Decision 8; Round 2 answers (c), (d) of both advocates
- **Target**: Base, Claim last sentence and Mechanism 4 (replace)
- **Rationale**: C-006 85%, C-007 85%: `issue.assign`, `issue.comment`, `issue.body.append_plan_sections`, `issue.hold` are bounded and reversible; `pr.merge` and `issue.close` contradict contract lines 241, 245, 300 and rest on Clay's ruling R10 (D:71)
- **Integration point**: Replace "one grant row per issue" with the split; merge and close released by a chat-recorded go keyed to the PR and head sha
- **Risk**: Medium

### Change 4: Controls adopted, scoped to what they cover (from Variant B)
- **Source**: Variant B Mechanism 3, 4, 5; Cited fact 7
- **Target**: Base, Mechanism (insert new item)
- **Rationale**: C-008 75%: `answer-check`, `E-NO-GRANT`, closed `refuse(argv)`; `E-NO-GRANT` covers at most 2 of 6 entries (D:696), the owner identity must be a parameter (D:694), the gate for `pr.merge` is not tied to a gate reason (INV-004)
- **Integration point**: New Mechanism item with the four conditions of Change 8
- **Risk**: Medium

### Change 5: Gate wording keyed to what master has (resolves A vs B on "never used")
- **Source**: Round 2 answers (a) of both advocates; INV-001
- **Target**: Base, Mechanism 5 (replace)
- **Rationale**: A wanted "not used while the gate is closed"; B showed K4 (D:1226) is an independent one-route reason; INV-001 shows the constant `GOVERNED_LEVELS_ALLOWED` is not on master. The merged wording: the orchestrator launches only through `worker-start`; the watcher prompt stays pinned to `--pipeline none` (`launch.py:33`); any governed level is a later owner decision after the 12 observations, and that decision amends R9 and the K4 test in the same change
- **Integration point**: Replace Mechanism 5
- **Risk**: Medium

### Change 6: Corrections to base facts
- **Source**: Round 1 and 2 concessions (X-002, X-003, C-005)
- **Target**: Base, Cited facts 3 and 4, Costs bullet 2 and 5
- **Rationale**: fact 3 becomes "the only control that is built"; Q36 (owner-answers line 185) is approval latency, Decision 8 (line 130) is the grant row, so the "for now" sentence is removed; fact 4 is corrected: per repo `enabled` and `max_in_flight` (D:278, D:289) and per PR gate reasons (D:582) exist, but no per-issue stop after the claim
- **Integration point**: Edit in place
- **Risk**: Low

### Change 7: Flag semantics kept (base strength)
- **Source**: Base Mechanism 1; `docs/designs/sc-issue-claim-pipeline-flag.md` lines 69-89
- **Target**: Base (preserve, add the `--plan` STOP row from D:1065)
- **Rationale**: The topic asked for `/sc:issue --claim` flag semantics; variant B lacks them (criterion C1)
- **Integration point**: A "Flag semantics" section
- **Risk**: Low

### Change 8: Conditions from the invariant probe (new section)
- **Source**: invariant-probe.md INV-001 to INV-004, INV-012, INV-005, INV-009, INV-010
- **Target**: Base (new section "Conditions the spec must state")
- **Rationale**: 5 HIGH UNADDRESSED items block convergence; each becomes a condition, none changes the winner
- **Integration point**: New section after Mechanism
- **Risk**: Low

### Change 9: Open points and what the owner must decide
- **Source**: unresolved points C-001, C-002, X-001, A-001, A-003
- **Target**: Base (new section)
- **Rationale**: The merged output must not hide non-convergence (78.9%)
- **Integration point**: Final section
- **Risk**: Low

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|------------|-------------------|---------------------------|
| C-007 | Standing `pr.merge` and `issue.close` in `grants` | Contract lines 241, 245, 300; ruling R10 is Clay's (D:71), Q38 says further issues wait for G2; B conceded in Round 2 |
| C-001 | "Launch levels are never used" as a permanent rule (R9, D:81) | Would erase the owner's R25; kept as "not now, a later owner decision" |
| C-009 | Reading no Project field ever (R1, R3, D:256) | Status and Pipeline reads are a D01 question; only deferred, not dropped |
| C-006 | A per-issue grant row as a file written by the owner (Decision 8) | Conflicts with the owner's chat-only rule of 2026-11-17; A conceded in Round 2 (d) |
| C-005 | "Pipeline is the only per-issue brake" (base claim) | Other brakes exist (D:278, D:289, D:582); claim removed |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1 | Medium | Headline of the paper contradicts the debate | Restore the base Claim |
| 3 | Medium | Wrong split of grants reaches the spec | Revert to the base grant text |
| 4 | Medium | Controls described as covering more than they do | Re-check D:696 and D:588 |
| 5 | Medium | Spec names a gate that does not exist on master | Re-check with a grep of the master snapshot |
| 2, 6, 7, 8, 9 | Low | Additive or factual corrections | Remove the inserted section |

## Review Status
- [x] Auto-approved (default)
- [ ] User-approved (--interactive)
- Approved by: auto (unattended)
- Approval timestamp: 2026-11-20 (UTC)
