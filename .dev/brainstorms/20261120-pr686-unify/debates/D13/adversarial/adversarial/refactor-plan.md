# Refactoring Plan: merge into Variant 2 (CLAY)

## Overview
- Base variant: Variant 2 (CLAY), `adversarial/variant-2-original.md`
- Incorporated from: Variant 1 (OURS), the debate transcript and one orchestrator-verified fact (WORKER-CONTRACT.md lines 236 to 237)
- Planned changes: 6; changes not made: 3
- Overall risk: Low to Medium (one change rewrites the Claim of the base)
- Output: `merged-hybrid-position.md` in the output folder

## Planned Changes

### Change 1: Rewrite the Claim to the agreed HYBRID
- Source: debate points C-001, C-002, X-001, X-002 (both advocates, HYBRID or OURS on C-001); Variant 1 Claim
- Target: base `## Claim`
- Approach: replace
- New content in substance: the three pieces are complementary and none is retired. The coordinator is the accountable owner of the whole close chain (sweep, settle, cleanup), as the owner's issue 339 comment of 2026-11-05 says. Closeout becomes a coordinator step. Removal of worktrees is performed by the nine-rule script of issue 687 (not by free judgment of a session), which the coordinator runs: the list or dry run each cycle, and the apply step only under a grant. Deleting a branch stays a local `git branch -d` inside the script; remote branch deletion stays human-only. The PR log stays an unrelated reporting tool.
- Rationale: debate transcript, per-point table (C-002 HYBRID 66%, X-001 HYBRID 64%); the weighting rule keeps the owner's "cleanup is the role's responsibility" and adopts Clay's separable mechanism.
- Risk: Medium (changes the base's central claim)

### Change 2: Add the owner's duty text as the first cited facts
- Source: Variant 1 facts 1, 2, 3 (issue 339 body; comment 2026-11-05; status review 2026-11-17)
- Target: base `## Cited facts`, new items at the top
- Approach: insert
- Rationale: U-001, U-002; both advocates accept these as the owner's definition of the duty.
- Risk: Low

### Change 3: Add the sweep and the contract facts
- Source: Variant 1 fact 4 (PR 539 and WC-16 at `WORKER-CONTRACT.md` line 289); orchestrator-verified lines 236 to 237 and line 241 of the same file (master snapshot)
- Target: base `## Cited facts`
- Approach: insert
- Content: WC-16 runs `/sc:sweep` on each wake and the coordinator "decides and performs any action"; lines 236 and 237 already let the coordinator remove a child worktree after merge-back and delete its branch, with the keep conditions quoted in line 237 (unmerged commits, an open PR, uncommitted changes, an unfinished `/sc:implement` ledger, a report not yet read); line 241 limits coordinator outward actions to those the user's instruction names.
- Rationale: C-005; the finding that the contract already has a bounded coordinator removal duty is the evidence behind X-001 HYBRID.
- Risk: Low

### Change 4: Add the unstated assumptions as open items
- Source: diff analysis A-001, A-002, A-003; both advocates answered QUALIFY on all three
- Target: new section `## Open items before adoption` after `## What it risks`
- Approach: insert
- Content: (A-001) a written mapping of "orchestrator" in issue 339, "orchestrator" in the design of PR 681 and "coordinator" in the contract; (A-002) the script counts as the coordinator's act only if the automation is opt-in and the coordinator owns schedule, grant and report; (A-003) closeout's writes need a named grant row per `WORKER-CONTRACT.md` line 241.
- Risk: Low

### Change 5: Fix the base's weaknesses found in scoring
- Source: base-selection (L4 not met, K2 not met, R3 not met)
- Target: base `## What it risks`, and the first use of each term
- Approach: modify
- Content: gloss ADD5, D18, Orca and wave 8 on first use; add a mitigation to each risk using only sources already cited: for a wrong `done`, closeout's own `unclear` escalation and `left_open` hand-back (`SKILL.md` lines 20 and 85); for missing approval of the cleanup design, the owner's decision given in chat. Use "coordinator" throughout and say that the design of PR 681 calls the same role "orchestrator".
- Risk: Low

### Change 6: Add the OURS risk
- Source: Variant 1 risks
- Target: base `## What it risks`
- Approach: append
- Content: if the coordinator (a model session) may delete worktrees on its own judgment, a defect in its checks can destroy unpushed work; issue 687's incident of 2026-11-20 shows it (two of 16 hand-removed workspaces belonged to open issues #354 and #419).
- Risk: Low

## Changes NOT Being Made
1. Variant 1's framing that Clay's pieces "must be read under 339's scope, not as a separate duty set" (C-001, X-002): kept as a statement that one coordinator owns the chain, but not as a reason to delay issue 687. Both advocates agree the pieces are not duplicates; the framing adds delay without a benefit.
2. Variant 1's implied option that the coordinator deletes worktrees and branches on its own judgment: rejected. Both advocates accept the nine-rule script as the safer mechanism, and Variant 1 itself names the risk.
3. Variant 2's rule that the orchestrator "never removes" worktrees as a blanket statement: narrowed (see Change 1), because `orchestrator.md` line 628 concerns wave 9's issue worktree only and `WORKER-CONTRACT.md` lines 236 and 237 already give the coordinator a bounded removal duty.

## Risk Summary
| Change | Risk | Impact | Rollback |
|---|---|---|---|
| 1 | Medium | Central claim changes | Restore the base Claim from variant-2-original.md |
| 2 to 6 | Low | Additive or wording | Delete the inserted lines |

## Review Status
- Approval: auto-approved (unattended run)
- Timestamp: 2026-11-20
