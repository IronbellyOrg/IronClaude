# Which dashboard improvement should be built first? (Q19)

## Question in one sentence
Of the four improvements a reviewer asked for on the worker dashboard, which comes first, and should the dashboard itself or the coordinator's report carry it?

## Why you are being asked
The dashboard's third release (the "Decision Desk" screen) cannot start until someone names the first improvement and where it lives. If you do not answer, that release does not start.

## Background you need
- The observer (`superclaude observe`) is the built, read-only terminal dashboard of agent workers. The sweep is a read-only report a coordinator session writes about its workers; it is a local file that is never posted, and it is still in an open pull request (#539).
- A reviewer on 2026-11-11 asked for four things, named after design pictures: Fleet Quilt, Decision Desk, Loop Detector or Mission Pulse (named steps with green, yellow, red), and a plain-English summary with issue and PR links.
- Decision Desk depends on a link between a coordinator question and a specific worker that is not established yet. What data Fleet Quilt needs is not written down anywhere.
- The summary and named steps have a known data source today: each task's brief and the progress files workers already write.
- An earlier review read the reviewer as valuing Fleet Quilt and Decision Desk most; nobody has shown the reviewer actually ranked them.

## Your options

### 1. Fleet Quilt first on the dashboard; the summary second (recommended)
- If you pick this: Fleet Quilt gets a dashboard release row, started after the shared field definitions and one recorded live check exist; its first step is writing down what data it reads. The summary and named steps are recorded as the second item; the report can prepare their data once #539 merges.
- Upside: the reviewer gets a screen where they look; it avoids the Decision Desk blocker.
- Downside: Fleet Quilt's data is unknown, so it is not quick.

### 2. The summary and named steps first, in the coordinator's report
- If you pick this: the report gains a plain task title and step states after #539 merges.
- Upside: buildable soonest, from data that already exists.
- Downside: it appears in a report the reviewer never sees, unless you later allow sweep facts on the dashboard (Q17).

### 3. Do not pick yet
- If you pick this: nothing starts until the Decision Desk link and the related records exist.
- Upside: no commitment while inputs are missing.
- Downside: the same as not answering; the reviewer gets no answer.

## What the debate found
- Two of three debaters favoured a dashboard screen first; one favoured the summary because only it can be built now.
- The earlier review that found the summary's data source itself says to choose the screen direction first.
- Nobody confirmed the reviewer's priority order.

## Recommendation and confidence
Option 1, 55 percent. Re-read the reviewer's 2026-11-11 comment on #409 first; if it says the summary matters most, choose option 2. Choose Decision Desk instead of Fleet Quilt if you prefer it; it then waits for its link to be established.

## If you do not answer
Release 3 of the dashboard does not start and none of the four improvements moves.

## What this answer does not authorize
It does not authorize any code, any change to the sweep's allowed commands, showing sweep facts on the dashboard, or any reply on #409.

## How to answer
Type: "Q19: option 1, Fleet Quilt" (or "Q19: option 1, Decision Desk", "Q19: option 2" or "Q19: option 3").
