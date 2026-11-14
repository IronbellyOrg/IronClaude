# Proposal C: not now; freeze the sibling worktree and decide when the switch-on is scheduled

## Answer

Not yet: the owner moves no records now, and instead records that the sibling worktree `issue-409-mvp` must not be cleaned until the owner commits or archives its records; the question is asked again when the switch-on pull request is actually scheduled.

## What happens next if the owner picks it

- The ledger (XC-01) gets a dated "do not clean `issue-409-mvp`" entry naming the files at risk: `owner-pass-record-20261112.md` and `owner-decisions-20261112.md` (in unpushed local commits `1ae72e1a1`, `f104ca51a`) and the untracked `owner-decisions-20261108.md`, `live-test-guide.md`, `tuibbs-review/`, `handoff-mvp-brainstorm.md` (read 2026-11-14).
- OB-01 is held; OB-06 cannot open (its prerequisite (d) fails); OB-08 (the #409 correction pass, also blocked by OB-01) waits.
- Nothing is committed and no pull request is opened.

## What it unlocks

- No owner work now; the owner spends attention on the questions that block more work (for example Q1, the security ruling that blocks the PR #539 merge).
- If the switch-on is never done (Q6 parks it), the records never need a pull request of their own.
- Matches the spec's default for an unanswered Q7 (`merged-requirements.md:534`), but makes it an explicit, dated choice.

## What it costs or risks

- The records stay on one disk only: untracked files and unpushed commits in a worktree have no copy elsewhere (no remote branch contains the commits, read 2026-11-14). A cleanup, a disk loss or a mistaken `git worktree remove` deletes them; the spec names this risk (`merged-requirements.md:264`).
- Reviewers keep citing records they cannot open on master (ADJ A-015, 83 percent).
- OB-08 (the #409 body correction) is held behind OB-01, so the #409 issue stays wrong in 23 places longer (`merged-requirements.md:240`).
- A "do not clean" ledger entry is an instruction, not a mechanical guard.

## What stays unresolved

Authorship of the pass record; where the records will finally live; when the question is re-asked.
