# Whether to keep the worker-status sweep's machine-readable output (Q9)

## Question in one sentence
Should the sweep's machine-readable summary, which today is only printed to the screen, ever be saved, and if so how?

## Why you are being asked
Saving it would change a rule in the sweep's design ("a sweep adds exactly one report file", pinned by two tests) or the report format, and nothing should be built for readers that do not exist yet. A later work item is parked on your answer.

## Background you need
- The sweep (`superclaude sweep run`) is a read-only check a coordinator session runs on its workers. Each run writes one dated report for people to read, then prints one machine-readable summary (JSON) on the screen; the summary is not saved.
- Nothing reads saved summaries today. Possible future readers: the planned v2 orchestrator (issue #423) or a status record for another workspace system (Coder#477).
- The reports themselves are kept only in a local folder that git ignores, and people delete old ones by hand.

## Your options
1. Not now; write down that it is not saved; decide the form when a reader asks (recommended)
   - If you pick this: one sentence now says the summary is screen-only. When a reader names its need, try in order: the caller saves the screen output; else the sweep puts the summary inside its one report (still one file); only then a separate file, which changes the one-file rule.
   - Upside: nothing changes now; the first real reader decides what to keep; the one-file rule stays intact as long as possible.
   - Downside: the question comes back later; until then, old machine facts exist only in human-readable reports that may be deleted.
2. Put the summary inside each report now
   - If you pick this: after the sweep's pull request merges, a small change adds the summary to the end section of each report.
   - Upside: every report carries its own machine facts; the one-file rule is kept.
   - Downside: built before anyone needs it; the reports are not kept long-term anyway; the first draft would have broken an existing test and needs extra protection against odd worker text.
3. Never save it
   - If you pick this: the parked work item is closed for good.
   - Upside: one less open item.
   - Downside: if v2 later needs the facts, this must be reopened as a new question; nobody can actually stop a caller saving the screen output.

## What the debate found
- All three advocates, including those for options 2 and 3, chose option 1 (3 of 3), mean confidence 73 percent.
- Option 2's idea (summary inside the one report) is kept as the second step of option 1.
- Option 3's idea (write down now that nothing is saved) is kept too.

## Recommendation and confidence
Option 1, 73 percent. No reader exists to say what should be kept, and the reports are not durable, so storing now buys nothing.

## If you do not answer
The same as option 1 without the written sentence: nothing is saved and the rule stays as it is.

## What this answer does not authorize
It does not change the sweep's code, its pull request (#539) or the "one report file" rule; any later step needs its own pull request and its own approval.

## How to answer
Type: "Q9: option 1" (or "Q9: option 2", or "Q9: option 3").
