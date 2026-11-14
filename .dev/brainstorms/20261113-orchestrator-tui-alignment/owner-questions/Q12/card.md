# Make the observer dashboard findable in the routing guide (owner question 12)

## Question in one sentence
Should the routing guide (the file that tells people and `/sc:recommend` which tool to use) get an entry for the observer dashboard `superclaude observe`?

## Why you are being asked
The observer is built and merged, but no guide, user guide or command file mentions it, so nobody is pointed at it. One small PR (work item OB-07) is planned to fix that and waits on your yes.

## Background you need
- The observer (`superclaude observe`, issue #409, PRs #503 and #514) is a read-only terminal dashboard of Orca workers (Orca is the local agent-orchestration app). Its coordinator-questions panel is still switched off on master.
- The routing guide is `HOW-WE-WORK.md`. It has machine-read tables that tests check, and prose sections that tests do not check. A byte-for-byte copy lives in the plugin folder.
- `/sc:recommend` reads only the marked tables, not the prose sections.
- PR #539 (the open sweep PR) edits the same guide and tests, so any guide change waits for it to merge.
- Only a person or a coordinator session should run the observer, never a worker session.

## Your options
1. **One routing-table row, own small PR after #539 merges** (recommended)
   - If you pick this: after #539 merges, a worker adds one row, runs the routing tests, and names any test edit they force; the row says "Coordinator or person only, never a worker" and describes only what works today; the PR goes through `/sc:pr-submit --monitor 3`.
   - Upside: findable by people and by `/sc:recommend`; one small, revertable row.
   - Downside: a routing test may need a change; waits for #539.
2. **One sentence in the guide's prose Orca section, no table row**
   - If you pick this: same timing; a bullet beside the existing "never workers" text; no test edits.
   - Upside: verified to need no test change.
   - Downside: `/sc:recommend` will not suggest the observer, because it does not read that section.
3. **No entry for now**
   - If you pick this: nothing changes; asked again after the questions panel is switched on and the observer-sweep contract note is written.
   - Upside: no PR, no test risk, no entry to rewrite later.
   - Downside: a working tool stays invisible with no date to revisit; the "person only" rule is written nowhere.

## What the debate found
- All three advocates agreed only a table row is read by `/sc:recommend` (checked in its skill file).
- The test cost of a row is probably smaller than first thought: the tests ignore plain terminal commands, and one row already has one. Not yet run.
- Two of three advocates picked option 1 when unassigned; one picked option 2; none picked option 3.

## Recommendation and confidence
Option 1, 78 percent.

## If you do not answer
The routing-row PR does not start; the observer stays unmentioned in the guide.

## What this answer does not authorize
It does not authorize opening, pushing or merging the PR; each needs its own grant row from you. It does not authorize any change to PR #539 or to the observer's code.

## How to answer
Type: "Q12: option 1" (or "Q12: option 2" or "Q12: option 3").
