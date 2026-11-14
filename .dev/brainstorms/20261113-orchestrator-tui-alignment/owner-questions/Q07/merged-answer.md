<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 2 (proposal B) -->
<!-- Merge date: 2026-11-14 -->
# Merged answer: freeze the sibling today; the owner re-reads and confirms authorship in one dated sentence, then commits the records verbatim in a records-only pull request now (or names an archive)

<!-- Source: Base (proposal B), modified by Change 1 (proposal A), Change 2 (proposal A) and Change 3 (proposal A) -->
## Answer

The owner reads each named file (or the byte-identical diff) first, then writes one dated sentence in the ledger that names the existing pass record and the 2026-11-08 and 2026-11-12 decision records and says they are the owner's text. The owner then personally commits the sibling-only records to master byte for byte, with no edits, in a records-only pull request opened now and separate from the switch-on, or archives them in a named place of the owner's choosing. A session the owner names makes the copy and the commit instead only if the owner writes that a verbatim, byte-checked copy of owner text by a named session is acceptable.

<!-- Source: Base (proposal B), modified by Change 4 (proposal C, new first bullet), Change 1 (proposal A), Change 2 (proposal A) and Change 3 (proposal A) -->
## What happens next if the owner picks it

- Today, the ledger (XC-01) gets a dated "do not clean `issue-409-mvp`" entry naming the files at risk: `owner-pass-record-20261112.md` and `owner-decisions-20261112.md` (in unpushed local commits `1ae72e1a1`, `f104ca51a`) and the untracked `owner-decisions-20261108.md`, `live-test-guide.md`, `tuibbs-review/`, `handoff-mvp-brainstorm.md` (read 2026-11-14). The freeze holds until the merge (or the archive) is verified. The entry also records the owner's explicit decision on `handoff-mvp-brainstorm.md`: save it with the other records, or leave it.
- The owner reads each named file (or the byte-identical diff) first, then writes the dated sentence in the ledger (XC-01). The sentence names the files and says they are the owner's text. Its scope: the named files exactly as they stand in the sibling on that date (checked by a byte comparison in the PR).
- By default the owner copies `owner-pass-record-20261112.md`, `owner-decisions-20261108.md`, `owner-decisions-20261112.md`, `live-test-guide.md` and `tuibbs-review/` (plus `handoff-mvp-brainstorm.md` if the owner chose to save it) to a fresh branch from `origin/master`, staging those named paths only, commits them, and opens the PR through `/sc:pr-submit` on the fork. Only if the owner writes that a verbatim, byte-checked copy of owner text by a named session is acceptable does that named session make the copy and the commit instead, staging the named paths only, under a permission row for that item and action.
- Alternatively, the owner names an archive of their choosing instead of master; the ledger records the archive path, and no records-only PR is opened.
- On the master route, the owner merges the PR. The switch-on PR (OB-06) later cites the pass record by its master path instead of committing it.
- The sibling can be cleaned once the merge (or the archive) is verified; that also ends the freeze.

<!-- Source: Base (proposal B), with consistency edits from Change 1, Change 2 and Change 3 -->
## What it unlocks

- On the master route, every owner record is reviewable on master in days, independent of whether the questions read is ever switched on (OB-06 is gated on tests that need live Orca, Q24 and Q30).
- OB-08 (the #409 correction pass) can cite master paths early.
- Owner effort stays small: one reading pass, one sentence, and one commit and merge (or one archive decision).
- The pass record already states "Written by the owner." on its first lines (sibling file, read 2026-11-14); a dated confirmation after the owner re-reads the files adds an explicit owner statement without retyping.

<!-- Source: Base (proposal B), first bullet modified by Change 2 (proposal A) -->
## What it costs or risks

- By default the owner makes the commit, which costs owner time: one branch, one commit and one pull request through `/sc:pr-submit`. If the owner instead rules that a named session may copy, that session performs the copy and the commit; this sits close to the rule "agents may cite, never write" an owner record (sibling `release-gates.md:22`). Verbatim copying with a byte check is not writing, but a reviewer may read it as the agent being the committer of owner text.
- Changes OB-06 prerequisite (d) from "committed in this PR" to "already on master and cited"; the spec (`merged-requirements.md:254`) and ADJ (line 191, "The guard-flip PR itself must commit the owner's pass record") would need that one condition reworded.
- Commits a pass record that names one Run for a switch-on that may never happen; if the owner later rewrites it, there are two versions on master.

<!-- Source: Base (proposal B), modified by Change 4 (proposal C), Change 2 (proposal A) and Change 3 (proposal A) -->
## What stays unresolved

Whether the program's rules allow a commit of owner text by a named session (this matters only if the owner rules that alternative); which session, if any, the owner names; where an archive would live if the owner prefers an archive to master. Whether `handoff-mvp-brainstorm.md` is saved or left is no longer open in advance: the owner decides it explicitly in today's freeze entry.
