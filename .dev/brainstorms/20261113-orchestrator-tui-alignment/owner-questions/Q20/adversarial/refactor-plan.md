# Refactoring Plan: Merge into Base (Variant 2, proposal-B)

## Overview
- Base: Variant 2 (proposal-B, named person owns)
- Incorporating strengths from: Variant 1 (proposal-A), Variant 3 (proposal-C), advocate findings
- Planned changes: 6
- Risk level: Low (additive, one wording refinement)

## Planned Changes

### Change 1: Cleanup rule gates the schedule, not FU-1 (from Variant 1)
- **Source**: Variant 1 "What happens next" bullet 4 (U-001); round1-advocate-1.md "Concessions" 1 and "Overall"; round1-advocate-2.md "Concessions"; round1-advocate-3.md "Overall"
- **Target**: Base, "What happens next" (append)
- **Integration point**: bullet: "Before the watcher's schedule is enabled (WA-05), a written rule says who closes watcher sessions and by when. FU-1 itself launches one session on one test issue (merged-requirements.md line 306), so it does not wait for that rule."
- **Risk**: Low.

### Change 2: The confirmed day cap (A-001)
- **Source**: round1-advocate-1.md and -2.md "Shared assumptions" A-001; `src/superclaude/cli/issue_watch/cycle.py` lines 33 and 36; `docs/designs/issue-watcher-setup.md` line 238
- **Target**: Base, "Answer" (wording refinement)
- **Integration point**: replace "up to 6 watcher sessions a day" with "up to the confirmed day cap of watcher sessions a day (default 6)"; add to "What happens next": "The day cap is a code constant (`DAY_CAP = 6`) that the design lists as a proposal for you to confirm after the shadow run; lowering it is a small code change, not a configuration edit."
- **Risk**: Low.

### Change 3: Review cadence and absence fallback (from advocates 2 and 3)
- **Source**: round1-advocate-2.md "Concessions" (single point of failure); round1-advocate-3.md "Overall" (review cadence)
- **Target**: Base, "What happens next", the ledger bullet (extend)
- **Integration point**: append: "The ledger also records how often that person looks at the open sessions, and either a named substitute or the rule that the schedule is disabled while the owner is away."
- **Risk**: Low.

### Change 4: What "owns" covers (from advocate 1)
- **Source**: round1-advocate-1.md "Strengths claimed" 3; `docs/designs/issue-watcher-setup.md` line 309
- **Target**: Base, "What it costs or risks", first bullet (extend)
- **Integration point**: append: "Orca's creator rule covers the agent made when the worktree is created; the watcher starts later sessions itself, so the named person is their owner by this decision and their reviewer, not by Orca's record (whether Orca attributes them to the creator is UNVERIFIED). The runbook gives no command to end a running session; it is closed by hand in Orca."
- **Risk**: Low.

### Change 5: Read-only count in the coordinator's check (from Variant 3, narrow form)
- **Source**: Variant 3 "What happens next" bullet 3 (U-003); round1-advocate-2.md "Concessions" (count without transcripts)
- **Target**: Base, "What it unlocks" (append)
- **Integration point**: bullet: "Optionally, the coordinator's recurring check may report a read-only count of open sessions in `issue-watch`, without reading their transcripts and without owning them, so the named person gets a reminder."
- **Risk**: Low; must not imply ownership.

### Change 6: Second-agent ownership if Q2 keeps the default (A-002)
- **Source**: all three advocates, A-002
- **Target**: Base, "What stays unresolved" (append)
- **Integration point**: bullet: "If Q2 keeps the default claim level, each claim also starts a second agent in its own `issue-<N>` worktree; you would also name who owns those agents. Under Q2's recommended `--pipeline none` there is no second agent."
- **Risk**: Low.

## Changes NOT Being Made

| Diff Point | Non-Base Approach | Rationale |
|---|---|---|
| C-001, X-001, X-002 | Coordinator owns the agent and sessions (V3) | The coordinator's loop is scoped to its Run (WORKER-CONTRACT.md line 288); sessions read outsider-written text; its own advocate judged V2 better |
| C-003, X-003 | Hold FU-1 (V1) | FU-1 is one session; the hold is circular; its own advocate judged V2 better |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|---|---|---|---|
| 1 to 6 | Low | None beyond the base | Restore base text |

## Review Status
- Approved by: auto (non-interactive)
- Approval timestamp: 2026-11-14
