# Proposal B: owner confirms authorship in one dated sentence; a records-only pull request copies the files verbatim now

## Answer

The owner writes one dated sentence in the ledger confirming that the existing pass record and the 2026-11-08 and 2026-11-12 decision records are theirs, and authorizes a records-only pull request, opened now and separate from the switch-on, that copies the sibling-only records to master byte for byte, with no edits, for the owner to review and merge.

## What happens next if the owner picks it

- The owner's sentence and date go into the ledger (XC-01). Its scope: the named files exactly as they stand in the sibling on that date (checked by a byte comparison in the PR).
- A session the owner names copies `owner-pass-record-20261112.md`, `owner-decisions-20261108.md`, `owner-decisions-20261112.md`, `live-test-guide.md` and `tuibbs-review/` to a fresh branch from `origin/master`, staging those named paths only, and opens the PR through `/sc:pr-submit` on the fork, under a permission row for that item and action.
- The owner merges it. The switch-on PR (OB-06) later cites the pass record by its master path instead of committing it.
- The sibling can be cleaned once the merge is verified.

## What it unlocks

- Every owner record is reviewable on master in days, independent of whether the questions read is ever switched on (OB-06 is gated on tests that need live Orca, Q24 and Q30).
- OB-08 (the #409 correction pass) can cite master paths early.
- Smallest owner effort: one sentence plus one merge.
- The pass record already states "Written by the owner." on its first lines (sibling file, read 2026-11-14); a dated confirmation adds an explicit owner statement without retyping.

## What it costs or risks

- An agent session performs the copy and the commit; this sits close to the rule "agents may cite, never write" an owner record (sibling `release-gates.md:22`). Verbatim copying with a byte check is not writing, but a reviewer may read it as the agent being the committer of owner text.
- Changes OB-06 prerequisite (d) from "committed in this PR" to "already on master and cited"; the spec (`merged-requirements.md:254`) and ADJ (line 191, "The guard-flip PR itself must commit the owner's pass record") would need that one condition reworded.
- Commits a pass record that names one Run for a switch-on that may never happen; if the owner later rewrites it, there are two versions on master.

## What stays unresolved

Whether the program's rules allow an agent-made commit of owner text with an owner confirmation; which session makes the copy; whether `handoff-mvp-brainstorm.md` is included.
