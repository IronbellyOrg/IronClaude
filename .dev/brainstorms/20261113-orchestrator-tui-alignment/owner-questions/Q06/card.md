# When to switch on the dashboard's "coordinator questions" panel, and for which work sessions (Q6)

## Question in one sentence
Should the dashboard's switched-off panel that reads a coordinator's open questions stay off until a safety test has run, and when do you say which work sessions it may read?

## Why you are being asked
The panel is built but off. Turning it on is blocked until you say how widely it may read. Reading the wrong way could silently delete a coordinator's unanswered questions, and nobody has measured whether it does.

## Background you need
- The dashboard is `superclaude observe`, a read-only terminal view of agent work managed by Orca (the local agent-orchestration app).
- Orca groups work into Runs (one coordinated piece of work). Each Run has a mailbox; a coordinator session (the person-opened session that hands out work) gets questions there.
- The panel uses one Orca read command. Orca's help says it "does not mark read", but whether it removes messages on a live Run is unproven either way.
- The panel is switched off by one setting in the code. Switching it on is called "the flip".
- Your earlier approval (2026-11-12) names one Run, `run_93bfa00cae2b`, an old "Claim issue 375" Run. Only the terminal that holds a Run can read its questions.
- The planned safety test puts known messages in a throwaway Run's mailbox and checks they survive the panel's read. A second check tries the panel once in a real, disposable coordinator terminal.

## Your options
1. Test first, decide the scope after (recommended)
   - If you pick this: the safety test, the one real-terminal attempt and a record of the Orca version run now; you read the results, then say "this Run only" or "any Run my terminal holds"; only then is the switch-on change made. If the tests cannot run (Orca unreachable, or the tester or test Run not named), the work is parked with a date.
   - Upside: first real evidence on whether reading deletes messages; you decide on evidence; matches the spec.
   - Downside: you are asked again later; the panel stays off longer; "this Run only" covers just the old Run, so the later choice is really "any Run my terminal holds" or no switch-on.
2. Say "any Run my terminal holds" now, build the switch-on change alongside the tests
   - If you pick this: your scope is recorded now; the change is built while the tests run and merged only if they pass.
   - Upside: no second question; the panel could arrive sooner; the scope is the only one with practical use.
   - Downside: you commit before evidence; building early breaks the spec's own order and may be wasted; how the code knows which Run "my terminal holds" is not established.
3. Keep it off and do not run the tests now
   - If you pick this: nothing reads any mailbox; the tests and the switch-on are parked until you say the panel is needed.
   - Upside: zero risk; no dependence on Orca being reachable or on two more decisions.
   - Downside: the deletion question stays unanswered; the built panel stays unused; owner records it needs keep sitting in a side workspace.

## What the debate found
- Three advocates, one per option, all picked option 1 (3 of 3), mean confidence 67 percent.
- Option 2's early build conflicts with the spec's prerequisites; its advocate conceded that.
- Option 3's original re-open trigger ("when release 3 opens") could never fire, because release 3 needs the switch-on first.
- Option 2's point stands: the narrow scope covers only an old Run, and the card says so.

## Recommendation and confidence
Option 1, 67 percent. The deciding fact: whether reading deletes questions on a live Run is unproven, and the safety test is the only planned evidence.

## If you do not answer
The panel stays off and the switch-on change is not made. Nothing already built changes.

## What this answer does not authorize
It does not let the dashboard take over a Run (Orca's `run-use`) or write to any mailbox in normal use. The safety test still needs its own written permission to write test messages to a throwaway Run. It does not choose who runs the tests (a separate question) or which real Run the terminal attempt uses (another separate question).

## How to answer
Type: "Q6: option 1" (or "Q6: option 2", or "Q6: option 3").
