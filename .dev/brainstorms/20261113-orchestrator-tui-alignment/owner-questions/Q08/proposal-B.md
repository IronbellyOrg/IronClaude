# Proposal B: amend #409's first acceptance criterion to match how the direction was actually chosen

## Answer

Amend #409's acceptance criterion 1 instead of writing a separate record: replace "A human selects the visual direction before production integration" with a criterion that names the staged selection the owner already made on 2026-11-08 and 2026-11-11 and cites those owner records as its evidence.

## What happens next if the owner picks it

- The owner supplies (or approves word for word) the replacement criterion text; an example shape: "The owner selected the staged direction on 2026-11-08 (worker ledger first, then the question ledger after QUESTION-OBSERVATION, then Decision Desk after QUESTION-LINK); evidence: the owner decision records of 2026-11-08 and 2026-11-11." The final wording is the owner's.
- OB-08 (the #409 correction pass) posts that text in place of BC-18, under its normal pin rules (re-read `updatedAt` before writing).
- OB-02 is satisfied by the amendment; the ledger records "AC 1 amended, date". OB-09 (release 3) may start once its other prerequisites hold.
- The release-gates rule for the DIRECTION-SELECTED gate (`release-gates.md:22`) is either satisfied by the cited records or amended in the same change, as the owner says.

## What it unlocks

- No new document: the evidence already exists in the owner's own 2026-11-08 record ("Staged direction chosen ('Stage it')", sibling `owner-decisions-20261108.md:5`) and 2026-11-11 record (on master).
- The issue stops measuring shipped work against a one-shot selection model the project did not follow (ADJ X-018: the direction was chosen in staged form).
- Release 3 is unblocked on this point.

## What it costs or risks

- Changes the bar after the fact: the criterion is rewritten to fit what happened, which an outside reader may see as moving the goalposts.
- The 2026-11-08 record it cites is untracked in the sibling worktree, not on master (Q7); citing it before it is saved cites a path readers cannot open.
- The gate rule at `release-gates.md:22` asks for more than the direction (fallback date, stack confirmation, command name, production-integration reading); an amended criterion does not supply those unless the owner also amends the gate.
- The owner's 2026-11-08 record says itself that whether it satisfies the gate "is for the owner to say" (line 9); this answer is the owner saying yes, and must be written as such.

## What stays unresolved

Whether the release-gates rule is amended too; the owner's reading of "production integration".
