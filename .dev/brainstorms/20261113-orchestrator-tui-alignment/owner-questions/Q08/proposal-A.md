# Proposal A: neither now; let #409 say honestly that the criterion is not met, and write the record when release 3 is next

## Answer

Do neither now: allow the #409 correction pass to post the honest status line for acceptance criterion 1 ("not met as recorded"), keep the criterion unchanged, and write the direction-selection record only when release 3 (Decision Desk) is the next piece of work.

## What happens next if the owner picks it

- OB-08 (the #409 correction pass) posts BC-18 as proposed: criterion 1 kept, with the appended status line "(Status 2026-11-13: not met as recorded. `superclaude observe` is registered in the shipped CLI; PR #503 lists the missing selection record as a known gap.)" (ADJ line 535), re-dated at posting.
- OB-02 (the record) is recorded in the ledger as "deferred by owner to release 3, date".
- OB-09 (release 3) keeps OB-02 as a prerequisite; the record is written as release 3's first step.

## What it unlocks

- No owner writing now; the owner spends attention on questions that block more work.
- #409 becomes accurate on this point at once: it stops implying a selection record exists, without inventing one.
- When the record is finally written, it can also cover release 3's own choices that the gate lists ("post-link choice or explicit deferral", "fallback date", `release-gates.md:22`), which are not known today.

## What it costs or risks

- #409 publicly states an acceptance criterion as "not met" for a shipped command, which can read as a defect in work already merged.
- The owner's 2026-11-08 statement ("Stage it") stays the only evidence, and that file is untracked in the sibling worktree, not on master (Q7).
- Release 3 gains one more step at its start.
- Differs from the spec's default, which posts OB-08 without BC-18; the owner must say BC-18 may post.

## What stays unresolved

The owner's reading of "production integration"; whether the 2026-11-08 "Stage it" decision already satisfies the gate (the record itself says that is "for the owner to say", line 9).
