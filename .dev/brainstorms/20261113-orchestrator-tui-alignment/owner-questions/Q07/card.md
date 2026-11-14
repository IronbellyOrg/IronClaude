# Saving your own decision records before a side workspace is deleted (Q7)

## Question in one sentence
Will you confirm that your 2026-11-12 approval record is your own text, and get it and your other decision records out of the side workspace where they are the only copies?

## Why you are being asked
Several of your records exist only in one side checkout on this machine (untracked files and local commits never pushed). If that checkout is cleaned up or the disk fails, they are gone. The work that switches on the dashboard's questions panel must cite your approval record, and the project rule is that agents may quote your records but never write them, so only you can vouch for them.

## Background you need
- The side checkout is `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp`.
- At risk (checked 2026-11-14): your approval ("pass") record and your 2026-11-12 decision record (in two unpushed commits), and the untracked `owner-decisions-20261108.md`, `live-test-guide.md`, `tuibbs-review/` and `handoff-mvp-brainstorm.md`.
- The approval record says "Written by the owner." at the top, but the commits holding it were made by an agent session, so git cannot prove who typed it.
- The current plan saves the approval record only inside the switch-on change, which may never happen.

## Your options
1. Freeze today, then save everything now (recommended)
   - If you pick this: today a dated "do not clean" note names every file at risk; you re-read the files, write one dated line saying they are yours, and commit them unchanged to the main branch in a small records-only change (or name an archive). An agent session copies them for you only if you write that this is acceptable. The switch-on change later points to the saved copy.
   - Upside: nothing can be lost, whether or not the panel is ever switched on; reviewers can read the records.
   - Downside: about one sitting of your time; one written condition of the plan ("the approval record is committed in the switch-on change") must be reworded.
2. Do it yourself, on the plan's original schedule
   - If you pick this: you commit the decision records in the next batch of work; the approval record goes in with the switch-on change.
   - Upside: matches the plan exactly; no rewording.
   - Downside: the approval record stays a single copy until the switch-on happens, and the side checkout could be cleaned before then.
3. Not now; freeze the side checkout and ask later
   - If you pick this: a dated "do not clean" note only; nothing is saved; asked again when the switch-on is scheduled.
   - Upside: no effort now.
   - Downside: single copies for an open-ended time; the note is not a lock; correcting the dashboard's issue text stays blocked.

## What the debate found
- Two of three advocates chose option 1's core; the third chose option 2 plus the freeze. All three agreed the approval record must be saved before any cleanup, not only with the switch-on.
- All three agreed you should re-read the files first, because git cannot show who typed them.
- The open split is whether an agent may make the copy; the recommendation defaults to you.

## Recommendation and confidence
Option 1, 65 percent. It is the only option where no record can be lost whatever happens to the switch-on.

## If you do not answer
The side checkout must not be cleaned, the switch-on change cannot open, and the records stay single copies.

## What this answer does not authorize
It does not switch the panel on, does not choose which work sessions the panel may read, and does not let any agent edit or write your records. A copy by an agent session happens only if you say so in writing.

## How to answer
Type: "Q7: option 1, I will commit them myself" (or "Q7: option 1, a named session may copy", "Q7: option 2", "Q7: option 3"), and say whether to save `handoff-mvp-brainstorm.md`.
