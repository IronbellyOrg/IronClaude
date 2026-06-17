# OPS-004 Tabletop Rehearsal Sign-Off — PENDING (needs_human_decision HALT)

**Status: PENDING — HUMAN ACTION REQUIRED (never auto-stamped)**
**Date recorded:** 2026-06-16

## What is blocked
The OPS-004 tabletop rehearsal **sign-off** (the stamped Date / Rehearser / Outcome row in the `## Tabletop Rehearsal Sign-Off` appendix of `docs/swarm/rollback-procedure.md`) is a genuine `needs_human_decision` HALT. The rehearsal is a human EXECUTION step; per the project's "human-decision items must HALT" discipline (memory `feedback_human_decision_items_must_halt`) the sign-off MUST NOT be auto-stamped, defaulted, or fabricated by the executor.

## What a human operator must do to clear it
1. **Execute the rollback rehearsal** against a scratch / fixture swarm environment, exercising the rollback steps documented in `docs/swarm/rollback-procedure.md` (Option A `git revert 2355bfe1` and/or Option B surgical `git checkout <sha> -- <legacy paths>`), including the artifact-preservation step.
2. **Record the outcome** in the `## Tabletop Rehearsal Sign-Off` appendix of `docs/swarm/rollback-procedure.md`: Date, Rehearser, Scenarios exercised (T1-T4), Rollback option exercised (A/B), Outcome (PASS/FAIL), Lessons learned.

## Scope of the HALT (precise)
- **HARD-BLOCKED on the human:** the sign-off STAMP itself. The appendix remains explicitly **UNSTAMPED** (verified present-and-empty at `docs/swarm/rollback-procedure.md:162-169`).
- **NOT blocked:** the rest of WS-D and the migration. The rollback DOCUMENT already exists (Step 6.5); this HALT concerns only the human-decision artifact (the stamp), not the surrounding doc-authoring work. The task proceeds; the sign-off is tracked as an open HIGH-priority follow-up for a human.

## Confirmation
The executor did NOT fill in, stamp, or fabricate any rehearsal outcome. The appendix is UNSTAMPED. This PENDING record + a HIGH-priority entry in the task's "Follow-Up Items Identified" section satisfy Step 6.6.
