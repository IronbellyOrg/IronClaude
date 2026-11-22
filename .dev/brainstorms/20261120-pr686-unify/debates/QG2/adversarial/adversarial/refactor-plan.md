# Refactoring Plan: Merge into Base (Variant A, OURS)

## Overview
- Base: Variant A (`/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG2/adversarial/adversarial/variant-1-original.md`)
- Incorporating strengths from: Variant B (`variant-2-original.md`)
- Planned changes: 5
- Risk level: Low (all additive or corrective text)

## Planned Changes

### Change 1: Visible mask marker and fenced paths (from Variant B)
- **Source**: Variant B, "Cited facts" 4 and "What it risks"; Variant A advocate steelman
- **Target**: Base, "Claim" OD-4 and "What it risks" (insert)
- **Rationale**: C-003, debate point 72%: B's objection that a mask edits text without saying so is valid; INV-013 shows paths such as `.claude/settings.json` hit the deny list
- **Integration point**: In OD-4 say the mask is a visible marker such as "[name removed by naming rule]", the original match is kept in the log, and the escalation template fences paths, shas and numbers so the scan skips them
- **Risk**: Low, additive; template fencing is UNVERIFIED against the real template

### Change 2: Offline template and fixture scan, scope-independent (from Variant B)
- **Source**: Variant B, "Mechanism" and fact 8; D:847
- **Target**: Base, "Mechanism" OD-3 (append)
- **Rationale**: X-002 HYBRID 65%: the scan of every template, fixture and end-to-end body does not depend on the scope
- **Integration point**: Keep scope B for the live writers; keep the offline scan and the fake `launch.effective` test
- **Risk**: Low

### Change 3: Escalation shape rules (from Variant B)
- **Source**: Variant B, "What it gets right"; D:825 item 2, D:686
- **Target**: Base, "Claim" OD-5 (append)
- **Rationale**: U-004: one escalation per PR, warnings never reach the person, entry always written, a cap never drops an entry
- **Integration point**: State them as rules of the entry-lines channel
- **Risk**: Low

### Change 4: Reserved notice for AU4a, AU4c, AU5 (from Variant B)
- **Source**: Variant B, OD-5 claim; both advocates' C-004 HYBRID
- **Target**: Base, "What it risks" and "What it gets right" (replace the "add the notice step when a delivery path is tested" line)
- **Rationale**: A-003: entry lines are enough for held items but not for post-merge hits (INV-014); both advocates agree
- **Integration point**: Trigger list: owner says in chat a push is wanted and the cap number; a sender is tested; row 8 can be used without ruling on the other eight rows (UNVERIFIED)
- **Risk**: Medium, depends on an unbuilt sender

### Change 5: Correct the cap and ruling-source statements (from the debate)
- **Source**: Orchestrator check of D:686, D:877, D:1170, D:1177; A-002
- **Target**: Base, "Cited facts" 8 and 3 (modify)
- **Rationale**: Both texts sit in D:1177; the design says settled (ruling 39) but the ruling is Clay's; code default 0
- **Integration point**: Restate: settled by Clay's ruling 39, design default 5 (D:877), parser default 0 (`repos.py:262-269`); not an owner ruling
- **Risk**: Low

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|------------|-------------------|---------------------------|
| C-001 / C-002 | Scope A with the D:841 handoff line | No check can scan a worker body (D:847); 25 of 30 PR bodies, 8 of 9 owner PR bodies carry the line; ruling 15 is Clay's (A-002); owner decides in chat |
| C-003 | Fail closed (refusal, nothing written) | INV-013 silent failure; D:692 |
| C-004 | Notice step as part of the first build | Sender unbuilt (UNVERIFIED), nine rows and cap are not the owner's rulings |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1 | Low | Mask marker not wired | Keep plain log-only mask |
| 2 | Low | Extra test | Drop the test |
| 3 | Low | Text only | Remove lines |
| 4 | Medium | Reserved step stalls | Entry lines remain |
| 5 | Low | Text only | Revert |

## Review Status
- [x] Auto-approved (default)
- Approved by: auto
- Approval timestamp: 2026-11-20
