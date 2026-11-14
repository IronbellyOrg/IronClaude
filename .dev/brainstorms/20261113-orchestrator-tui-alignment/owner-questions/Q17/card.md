# Should the worker dashboard also show the sweep report's facts? (Q17)

## Question in one sentence
Should the observer dashboard ever show, next to its live Orca worker list, the facts that only the coordinator's sweep report has (safe-to-close, frozen plans, waiting on a person, git state)?

## Why you are being asked
The observer's planned third release (the "Decision Desk" screen, not yet scheduled) must declare which data it reads. A "yes" also forces the separate storage question (Q9: whether the sweep's JSON is ever saved or captured) to be decided. Nothing is blocked today; this sets the direction for later work.

## Background you need
- Orca is the local app that runs agent workers. The observer (`superclaude observe`) is a built, read-only terminal dashboard that shows Orca's worker list in Orca's own words.
- The sweep (`superclaude sweep run`) is a read-only report a coordinator session makes about its workers. It is in an open pull request (#539), not merged. It writes one dated report; its JSON is printed to the screen only, not saved.
- The two programs use some of the same words with different meanings (for example "stale" means 45 seconds without a good read in the observer, but a 6 hour window in the sweep).
- The coordinator runs the sweep at most once every 5 minutes, so sweep facts are always older than the live dashboard rows.
- An earlier review judged, at 78 percent confidence, that the sweep's JSON should feed other future tools, not the observer, "now".

## Your options

### 1. Not now, with a written trigger to ask again (recommended)
- If you pick this: the dashboard stays Orca-only; release 3 plans on the dashboard's own data. The ledger records: ask again when Decision Desk is chosen or scheduled, and only after #539 merges. The rule for any later panel (show the sweep's own words and the report's age) stays on file.
- Upside: nothing waits on unmerged work; nothing changes in the sweep; easy to change later.
- Downside: a person still checks two places for now.

### 2. Yes, plan a sweep panel for release 3
- If you pick this: release 3 will read both sources; the storage question (Q9) must be decided now, likely by capturing the sweep's output each run.
- Upside: one screen with everything needed to decide whether to close or wait on a worker.
- Downside: depends on an unmerged program and an unscheduled release; old sweep facts sit next to live rows and can mislead.

### 3. Never, as a written rule
- If you pick this: the dashboard is declared Orca-only for good; any combined view would live elsewhere (perhaps the future Orchestrator v2, which is not built).
- Upside: the two programs never mix their words on one screen.
- Downside: no evidence supports "never"; reversing a written rule later costs more.

## What the debate found
- All three debaters, including those arguing for options 2 and 3, judged option 1 best (62 to 70 percent).
- Option 2 is right about what a person needs but every input it depends on is still open.
- Option 3 goes further than any evidence.
- Option 1 was improved with a re-ask trigger and a warning that sweep facts lag the live rows.

## Recommendation and confidence
Option 1, 65 percent.

## If you do not answer
The same as option 1 without the written trigger: no sweep panel, nothing changes, and the question may simply never come back.

## What this answer does not authorize
It does not authorize saving the sweep's JSON, changing the "one report file" rule, any change to the sweep or the dashboard code, or scheduling release 3.

## How to answer
Type: "Q17: option 1" (or "Q17: option 2" or "Q17: option 3").
