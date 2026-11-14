# Should a "reclaimable" worker count as running, finished, or neither?

## Question in one sentence
When Orca says an agent worker is `reclaimable`, should our dashboards treat it as still running, as finished (history), or as a separate state of its own?

## Why you are being asked
The note that defines shared words between the dashboard and the sweep report needs one row for this word, and the dashboard's next PR (the one that turns on its coordinator-questions panel) cannot open until that row exists.

## Background you need
- Orca is the local app that runs agent workers. It reports each worker's state; one of them is `reclaimable`. No file we have explains exactly what Orca means by it.
- The dashboard (`superclaude observe`) hides finished workers (`released`, `retained`) unless you press `h`. It does not hide `reclaimable` ones, so they fill the screen: at one check there were 27 reclaimable workers and 0 active.
- A recorded sample shows reclaimable workers had finished their task but still held resources that had not been released, and Orca could not tell whether the session was still alive.

## Your options

### 1. Its own state, for now; settle it with one read-only check (recommended)
- If you pick this: the dashboards show the word `reclaimable` and never call it running or finished. The planned read-only Orca check adds one look at what `reclaimable` means; then you choose between options 2 and 3.
- Upside: never wrong, no code change, decided on evidence later.
- Downside: the screen stays crowded with finished workers until then.

### 2. Finished: hide it with the other finished workers
- If you pick this: a small dashboard change hides reclaimable workers by default (`h` shows them).
- Upside: the default screen shows only working agents.
- Downside: if a reclaimable worker can still be running, the dashboard hides it; the meaning is guessed.

### 3. Not finished: keep it visible as "awaiting release"
- If you pick this: no code change; the row stays on screen, labelled as waiting for release.
- Upside: a reminder to clean up held resources stays visible.
- Downside: the screen stays crowded; wrong if Orca releases them on its own.

## What the debate found
- Three advocates; 8 of 9 points agreed; option 1 won 2 of 3 overall votes.
- Even the advocate for "finished" chose option 1 now, because the dashboard's hide rule ignores whether a worker is alive.
- The sample shows the task finished but the session's end was not confirmed.

## Recommendation and confidence
Option 1, about 75 percent.

## If you do not answer
Option 1 applies by default: "its own state". The dashboard keeps showing reclaimable workers as it does today.

## What this answer does not authorize
No code change, no Orca command beyond the already-planned read-only capture, and nothing sent to any worker.

## How to answer
Type: "Q23: option 1" (or "Q23: option 2", "Q23: option 3").
