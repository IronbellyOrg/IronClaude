# Proposal A: yes to both, done by the owner, before the sibling worktree is cleaned

## Answer

Yes: the owner personally writes (or re-reads and re-confirms in their own words) the pass record, and personally commits the records that exist only in the sibling worktree to master, or archives them in a named place of the owner's choosing, before `issue-409-mvp` is cleaned.

## What happens next if the owner picks it

- OB-01: the owner, on a fresh branch from `origin/master` (the sibling's history does not descend from master, `merged-requirements.md:234`), commits `owner-decisions-20261108.md`, the 2026-11-12 record, `live-test-guide.md` and `tuibbs-review/`, or names an archive; the ledger (XC-01, the program's decision ledger) records the path. Observe: `git ls-tree origin/master .dev/issues/409/` lists them, or the ledger names the archive (`merged-requirements.md:249`).
- The pass record stays the owner's text; it enters master inside the switch-on pull request (OB-06 prerequisite (d), `merged-requirements.md:254`).
- After OB-01 is recorded, the sibling worktree may be cleaned.

## What it unlocks

- OB-06 prerequisite (d) can be met; the flip can open once its other prerequisites pass.
- OB-08 (the #409 issue-body correction pass) can cite the records by master path (OB-01 blocks OB-08, `merged-requirements.md:249`).
- Removes the evidence-loss risk named at `merged-requirements.md:264`.
- Authorship is unambiguous: the person who typed the record is the owner, which is the only defence against "git cannot show who typed it" (ADJ INV-014).

## What it costs or risks

- Owner time: one branch, one commit, and a pull request through the project's required route (`/sc:pr-submit`), or an archive decision.
- The owner's commit route on this host is not specified in the spec (which session, which worktree); the owner must pick one.
- If the existing pass record (which already says "Written by the owner.") is simply re-confirmed rather than re-typed, the authorship evidence is the same as today.

## What stays unresolved

Whether `handoff-mvp-brainstorm.md`, also untracked in the sibling but not named by the spec, should be saved too; where an archive would live if the owner prefers archive to master.
