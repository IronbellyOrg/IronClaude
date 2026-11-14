# Should the dashboard's data file be copied to your TUIBBS machine? (Q18)

## Question in one sentence
Do you want a channel that copies the worker dashboard's data file from the Coder workspace to the separate machine where TUIBBS runs?

## Why you are being asked
A deferred work item (the copy channel) waits on this answer, and the reply planned for the Coder repository's workspace listener issue (Coder#477) must say whether such a channel exists or is coming. Nothing is blocked today.

## Background you need
- The observer (`superclaude observe`) is the built, read-only terminal dashboard of agent workers. Every cycle it rewrites a small JSON file (the "snapshot") in your private state folder, readable only by you (file mode 0600).
- TUIBBS is your separate terminal platform on a different SSH host. The snapshot was shaped so a TUIBBS screen could read it one day, but nothing connects the two machines today.
- Before any copy could be safe, five things are missing: how it travels, which workspace it came from, how old is too old, re-cleaning untrusted text, and who may read the copy.
- Your note of 2026-11-08 says the dashboard "may become a TUIBBS module", marked "Background, not deciding".

## Your options

### 1. Not yet; open it at dashboard release 4 or when you say a TUIBBS screen is planned (recommended)
- If you pick this: no channel now; the item stays on file with its two triggers and its five required design pieces; Coder#477 is told "no channel exists; one is deferred".
- Upside: matches your recorded "not deciding"; nothing leaves this machine; easy to change.
- Downside: if you do want TUIBBS soon, the design waits until you say so.

### 2. Yes, a TUIBBS screen is planned; design the channel now
- If you pick this: the design starts now (the five pieces), the staleness-age question (Q22) is needed now, and Coder#477 is told a read-only copy is planned.
- Upside: one deliberate design instead of an ad hoc copy later.
- Downside: a private file would leave this machine; the TUIBBS side has no design yet.

### 3. No, no TUIBBS screen is planned; drop the item
- If you pick this: the item is closed; the dashboard is stated as single-machine; this supports closing Coder#477.
- Upside: the smallest exposure, nothing to track.
- Downside: if TUIBBS returns, the design and its safety checklist start from nothing.

## What the debate found
- All three debaters, including those arguing for options 2 and 3, judged option 1 best (65 to 72 percent).
- Options 2 and 3 each need a firm "yes" or "no" from you that your notes do not contain.
- Option 1 was improved with "who may read a copy" as a required design piece.

## Recommendation and confidence
Option 1, 70 percent. If you already know your TUIBBS plans, pick option 2 or 3 instead.

## If you do not answer
The same as option 1: no channel; the item waits for dashboard release 4 or your statement.

## What this answer does not authorize
It does not authorize building any channel, any credential for another machine, closing Coder#477, or any post on that issue by itself.

## How to answer
Type: "Q18: option 1" (or "Q18: option 2, a TUIBBS screen is planned" or "Q18: option 3").
