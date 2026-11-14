# How the worker dashboard and the sweep report should fit together

## Question in one sentence
Should the worker dashboard and the sweep report stay separate programs joined by one written contract note, should the dashboard show the sweep's findings in a panel, or should the decision wait?

## Why you are being asked
Two read-only programs were built independently from the same design and never mention each other. Today they have two output files both called "v1", three sets of words for the same things, and two lists of allowed Orca commands that disagree on one command. A contract note to fix that waits on this answer.

## Background you need
- `superclaude observe` is the worker dashboard (issue #409, merged). It polls Orca (the local agent-orchestration app) every 15 seconds.
- `superclaude sweep run` is the coordinator's report about its workers (issue #339, PR #539, still open). It runs at most once every 5 minutes, writes a dated report each time, and prints its findings to the screen only.
- The #409 issue text proposes that the dashboard read the sweep's findings, so both say the same thing about a session. All five reviews advised against doing that now.
- Merging the two programs into one was rejected by every review.
- The dashboard does not show the sweep's classes today, so the two cannot visibly disagree on one screen yet.

## Your options
1. **Keep both separate, write one contract note.**
   - If you pick this: the note is drafted now on a branch from master, then landed with a test and links after PR #539 merges and one real-id comparison runs. The panel question is asked again once that comparison is recorded.
   - Upside: fixes today's confusion with no change to either program; a test catches future drift.
   - Downside: the two programs can still describe the same worker differently; the note only explains how.
2. **Add a dashboard panel that shows the sweep's findings.**
   - If you pick this: the coordinator's regular sweep output is saved, and the dashboard reads that saved copy (never runs the sweep itself). A note is still written.
   - Upside: one classification of each session on your screen, as #409 proposed.
   - Downside: sweep data up to 5 minutes old next to rows seconds old; depends on matching ids never tested on real data; empty when no coordinator is running.
3. **Write nothing yet; decide after PR #539 merges and the ids are compared.**
   - If you pick this: nothing is drafted; the question comes back later.
   - Upside: decides with more evidence.
   - Downside: today's confusion stays; the note is needed under every option anyway.

## What the debate found
- All three advocates, including those for options 2 and 3, recommended option 1.
- The panel's benefit does not exist yet, because the dashboard shows none of the sweep's classes today.
- Drafting the note now is cheap; only landing it waits for PR #539.

## Recommendation and confidence
Option 1, 75 percent. Matches the spec's recommended answer.

## If you do not answer
Work proceeds on option 1 as a provisional answer and you are asked once more later.

## What this answer does not authorize
Any change to either program's code or output; storing the sweep's output; a dashboard panel; any merge of PR #539.

## How to answer
Type, for example: "Q5: option 1" (or "Q5: option 2, I want one view on screen" / "Q5: option 3, wait").
