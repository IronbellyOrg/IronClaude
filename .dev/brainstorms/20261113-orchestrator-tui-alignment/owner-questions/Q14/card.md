# When Orchestrator v2 may start (owner question 14)

## Question in one sentence
Issue #423 (Orchestrator v2) says it starts "after #339 is complete": what exactly must be finished first?

## Why you are being asked
The words can be read several ways, so the start gate cannot be checked as written. Your answer sets the #423 rewrite's sequencing sentence and decides whether a small sweep code change becomes a prerequisite.

## Background you need
- #339 is Orchestrator mode. Its Phase 1 is the read-only sweep (`/sc:sweep`), open as PR #539. Later phases (`/sc:close`, resume, a trust layer) are not built.
- #423 is v2: a planned advisory knowledge layer that reports to a person or the coordinator session. Nothing of it exists.
- The sweep sorts sessions into classes. Its `working` class is switched off today, because the exact names Orca uses for "live" and "waiting" were never recorded, so working sessions show as "could not determine".
- A planned one-time read-only "shared capture" of live Orca values (tracked in issue #534) would record those names. Restoring the `working` class afterwards is a separate small code PR.

## Your options
1. **PR #539 merged plus the capture recorded** (recommended)
   - If you pick this: v2 waits for the sweep merge and the capture record; the gate entry also says whether the recorded values are enough to switch the `working` class on; the code fix stays a follow-up. Optionally you set a date after which v2 may start without the capture, marking those fields pending.
   - Upside: v2 is designed with real Orca values; the gate is two checkable records; matches the plan as written.
   - Downside: still waits on a live Orca session (unreachable on 2026-11-13); v2 may launch while the sweep still says "could not determine" for working sessions.
2. **PR #539 merged, capture recorded, and the `working` class restored in code**
   - If you pick this: a small sweep PR (with its own review and your grant) must merge before v2 starts.
   - Upside: proved by a passing test; v2 sits on a sweep that can say "working".
   - Downside: slowest; puts a code change on a planning gate; if Orca does not expose what the rule needs, v2 waits on a sweep redesign.
3. **PR #539 merged only**
   - If you pick this: v2 design starts at the merge; fields that need live values are marked pending until the capture.
   - Upside: fastest; cannot be stalled by Orca being unavailable.
   - Downside: likely rework when the capture arrives; the list of "live-value fields" does not exist yet.
- In all three, `/sc:close`, resume and the trust layer come first only if v2 decides to send messages to agents, not just report to a person.

## What the debate found
- All three advocates, asked what they would pick if unassigned, picked option 1.
- The capture is a record; restoring the class is code. The plan already treats them separately.
- Option 2's best point (check the values are enough) and option 3's best point (a fallback if Orca stays down) were folded into option 1.

## Recommendation and confidence
Option 1, 80 percent.

## If you do not answer
The plan uses option 1 as its default, labelled "default" in the #423 rewrite.

## What this answer does not authorize
It does not authorize editing issue #423, running the live capture, any sweep code change, or starting v2 work; each needs its own grant or answer.

## How to answer
Type: "Q14: option 1" (optionally "with fallback date YYYY-MM-DD"), or "Q14: option 2" or "Q14: option 3".
