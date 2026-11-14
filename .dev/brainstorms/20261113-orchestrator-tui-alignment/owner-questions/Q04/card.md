# What you meant by "TUI Panel" on the Coder workspace-listener issue

## Question in one sentence
In your 2026-11-13 comment on Coder#477, "Ensure this aligns with Orchestrator and TUI Panel", what is the "TUI Panel"?

## Why you are being asked
The reply to Coder#477 must say in one line what it is aligning with. Nobody can tell from the files: the phrase appears in nothing you wrote elsewhere. The answer also affects whether that issue should be narrowed or closed (Q3) and whether a copy of dashboard data should go to another host (Q18).

## Background you need
- `superclaude observe` is the read-only terminal dashboard of Orca workers (the local agent-orchestration app), built for IronClaude issue #409 and merged. Today it reads one host only.
- Its planned later releases include one for answering coordinator questions (may or may not write; not established) and one that reads a remote fleet.
- TUIBBS is your separate TUI platform on another host. Your 2026-11-08 note said the dashboard "may become a TUIBBS module", marked "Background, not deciding".
- On 2026-11-08 you also replaced #409's Go direction with Python plus Rich.
- Reviewers rate "the #409 dashboard" as the likely meaning (about 70 to 75 percent) and a TUIBBS screen at about 15 percent.

## Your options
1. **The #409 dashboard, with today's properties only** (the host-neutral proposal, with today's verified facts added). Reply line: "TUI Panel = `superclaude observe` (the #409 dashboard); single-host and read-only today; later readers, including a possible TUIBBS screen, not decided."
   - If you pick this: the line is shown to you, then posted; the copy-to-another-host question stays at "not yet"; the narrow-or-close question is decided on its own.
   - Upside: true today and stays true when later releases ship.
   - Downside: a reader of the Coder issue does not learn whether one host or several must be served.
2. **The #409 dashboard, single-host and read-only (the spec's original line).**
   - If you pick this: the line "TUI Panel = `superclaude observe`; single-host; read-only" is posted.
   - Upside: shortest, firmest statement.
   - Downside: reads as a lasting limit that the planned remote-fleet release would contradict; pushes the Coder issue toward closing.
3. **Both: the dashboard now, and a TUIBBS screen reading its data as the plan.**
   - If you pick this: you are stating a TUIBBS screen is planned; the copy-to-TUIBBS work can be scoped now.
   - Upside: gives the Coder issue a real future consumer.
   - Downside: commits to cross-host work with no plan or task yet, and moves worker data off the host.

## What the debate found
- Unmodified, two of three advocates picked option 2 and one a host-neutral version; all three then agreed on option 1's line.
- "Single-host" today cannot answer whether the dashboard "stays" single-host, which is what the narrow-or-close decision needs.
- Nothing in the files shows a TUIBBS screen is planned.

## Recommendation and confidence
Option 1, 64 percent. This partly matches the spec's recommended answer: same meaning, but "single-host" and "read-only" are scoped to "today".

## If you do not answer
The working reading (the #409 dashboard) is used until you say otherwise; the Coder reply still waits for the narrow-or-close answer.

## What this answer does not authorize
Posting the reply (that needs its own permission row); any copy of dashboard data to another host; any TUIBBS work.

## How to answer
Type, for example: "Q4: option 1" (or "Q4: option 2" / "Q4: option 3, a TUIBBS screen is planned" / "Q4: I meant <something else>").
