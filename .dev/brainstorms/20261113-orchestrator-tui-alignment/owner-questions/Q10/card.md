# Whether the worker-status sweep may read the coordinator's pending questions (Q10)

## Question in one sentence
May the sweep (the coordinator's read-only worker report) ever read the pending questions in Orca's message box, or should only the dashboard do that?

## Why you are being asked
The sweep may only run commands on a list you signed, and message reading is not on it. Its report also says something not proven ("pending questions cannot be read without consuming them"), and the fix waits on your answer.

## Background you need
- Orca is the local app that runs agent work. Each piece of coordinated work (a Run) has a message box; a coordinator session gets workers' questions there.
- Orca's plain "check" command removes messages it reads. Whether the "read all, questions only" form also removes them on a live Run is unknown; Orca's help says it does not.
- The coordinator already receives every question through its own waiting loop, so it is not blind today.
- The dashboard (`superclaude observe`) has a question panel, switched off until you answer the dashboard question (Q6) and a safety test passes.

## Your options
1. Dashboard only, for now; fix the sweep's wording now (recommended)
   - If you pick this: the sweep reads no messages; after its pull request merges, the one unproven sentence becomes "This command reads no messages. A plain check consumes them. Whether the read-all form consumes on a live Run is not established." The true header line stays. Any future sweep read needs your new signature. Asked again once the safety tests have results, or if the dashboard panel is shelved.
   - Upside: removes a false claim now; changes nothing you signed; costs nothing.
   - Downside: "for now" is not final; the new sentence may need one more edit after the tests.
2. Yes, later: let the sweep list questions once the safety tests pass
   - If you pick this: the wording is fixed now, and after the tests pass you sign one new command for the sweep.
   - Upside: questions appear in the report the coordinator already reads.
   - Downside: the coordinator already gets them; the tests do not cover the coordinator's own live message box, which is where the sweep would read; the sweep may not act on them anyway.
3. Never; change the wording once, after the safety test
   - If you pick this: a permanent rule; the current sentence stays until the test result is known.
   - Upside: one clear split of jobs; one wording change.
   - Downside: an unproven sentence stays in the shipped tool with no date for the test.

## What the debate found
- All three advocates, including those for options 2 and 3, chose option 1 (3 of 3), mean confidence 73 percent.
- The sweep's header line ("Messages coverage: partial") is true and stays; only the bullet changes. The plan's work item must be reworded for that.
- The coordinator's own loop already receives every question, so option 2 adds little.

## Recommendation and confidence
Option 1, 73 percent. It removes an unproven claim now without widening what the sweep may do.

## If you do not answer
The same as option 1: message reading stays off the sweep's list, and the wording is corrected after the merge.

## What this answer does not authorize
It does not add any command to the sweep's signed list, does not switch on the dashboard's question panel, and does not authorize any message writes.

## How to answer
Type: "Q10: option 1" (or "Q10: option 2", or "Q10: option 3").
