# What the coordinator's "static report in chat" should be (owner question 11)

## Question in one sentence
When issue #339 asks for "a static report in chat every 3 to 5 minutes", should that be the sweep's short summary, the observer dashboard's one-shot text, both, or nothing yet?

## Why you are being asked
Only you know what you meant by your issue wording. Nothing is blocked: no work item waits on this answer. It is recorded in the decision ledger (the program's list of your decisions) and sets what the coordinator session (the person-opened Claude session that supervises worker sessions) prints in chat.

## Background you need
- The sweep (`/sc:sweep`, issue #339, open PR #539) is a read-only command that writes one report file about all sessions and prints, in chat, only the session counts and that file's path. The report file already uses the #409 dashboard layout (docs/designs/orchestrator-mode.md:603).
- The observer (`superclaude observe`, issue #409, already merged) is a read-only terminal dashboard. `observe --once` prints its view once as plain text and writes no file.
- The sweep may run at most once every 5 minutes. That is a cap, not a timer: no recurring coordinator loop exists yet.
- A "contract note" between the two programs (one shared word list and how their rows match) is planned but not written.
- On 2026-11-07 you chose that the first PR delivers "a read-only `/sc:sweep` plus the static orchestrator status report on the #409 layout" (seed-brief.md:17).

## Your options
1. **Sweep summary only, until the contract note exists** (recommended)
   - If you pick this: nothing changes in code or spec; the chat shows counts plus the report path; the ledger notes that no 3-to-5-minute cadence exists yet; the observer text is reconsidered when the note is written, after a check that the observer works from the coordinator's own terminal.
   - Upside: zero edits; one set of words in chat; the #409-layout report already exists in the file it points at.
   - Downside: the chat itself shows counts, not the fleet; "every 3 minutes" is not met; the revisit has no date.
2. **Both reports, now**
   - If you pick this: the chat later shows the sweep summary plus the observer's one-shot text; the worker contract, the sweep skill and the output style would need edits that are not scheduled.
   - Upside: the fleet is visible in chat; the observer writes no file and is not capped at 5 minutes.
   - Downside: two programs' words side by side before they agree on meanings; the observer's gate test (an unbound terminal cannot read another terminal's work) failed, and the coordinator-terminal case is untested.
3. **Neither yet; park the clause**
   - If you pick this: automated chat output stays your list of open decisions only; the sweep reply appears only when someone runs `/sc:sweep`; the clause is logged as deferred in issue #534 (the sweep's follow-up list).
   - Upside: promises nothing that does not run today.
   - Downside: drops part of the scope you chose on 2026-11-07; one more deferred item.

## What the debate found
- Three advocates each argued one option; asked what they would pick if unassigned, all three picked option 1.
- The deciding fact: the #409-layout report already exists as the sweep's report file, so option 1 meets your recorded scope with no edit.
- Option 2's best point (the observer text) is kept as a later step, gated on a terminal check.
- Option 3's best point (no loop exists) is kept as a ledger note.

## Recommendation and confidence
Option 1, 85 percent.

## If you do not answer
The default is the same as option 1: sweep summary only. Nothing else changes.

## What this answer does not authorize
It does not authorize any edit to PR #539, the worker contract, the sweep skill or the output style, any new recurring timer, or any Orca or GitHub write.

## How to answer
Type: "Q11: option 1" (or "Q11: option 2" or "Q11: option 3").
