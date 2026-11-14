# Proposal C: no `/sc:pr-submit` on PR #539 at any level; the author does everything by hand

## Answer

`/sc:pr-submit` is never run on PR #539: the #539 author handles every review finding, failing check, push, reply and resolve by hand until the owner merges.

## What happens next if the owner picks it

1. The #539 author applies SW-02 and SW-03 and pushes by hand, staging named paths, each under its push grant; thread resolves under their own grants.
2. New Augment or Codex findings after those pushes are read and fixed by hand, with a written plan where the hard limit requires one.
3. The author refreshes the merge reference by a hand push (SW-05 (1)) and the owner merges.
4. The ledger records "no pr-submit on #539 (Q28 default)".

## What it unlocks

- No automated write of any kind on the PR that carries the open INV-008 security thread; nothing can design, push or resolve an INV-008 change except a person.
- No grant row for the tool is needed, so no risk of an unlisted write.

## What it costs or risks

- Every later finding and red check on a 1003-file PR is handled by hand; the merge state is UNSTABLE today (read 2026-11-14).
- The project's review loop (verification against real code, deduplication, one fix commit per cycle, re-trigger) is not used, so a finding can be missed or fixed without verification.
- A Codex security review that lands after a clean code review must be noticed by a person.

## What stays unresolved

- Nothing about the tool; only the hand workload.
