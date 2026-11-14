# Proposal B: after the ruling lands, level 2 only; the tool fixes locally and a person pushes

## Answer

No `/sc:pr-submit` on PR #539 before SW-02 lands the ruling; after it, a designated PR session may run `--monitor 2`, which verifies findings, applies and validates fixes in the working tree and stops before any commit, push, reply or resolve; the #539 author reviews each fix and pushes it by hand under a push grant.

## What happens next if the owner picks it

1. Until the ruling lands, SW-02 and SW-03 are pushed by hand as in the spec.
2. The owner writes a #539 grant row for `--monitor 2`: attach to #539, local edits and troubleshoot artifacts only; no push, reply, resolve, re-trigger comment or draft toggle.
3. The PR session runs `/sc:pr-submit --pr 539 --monitor 2`; each cycle ends with validated, uncommitted changes in the #539 checkout.
4. The #539 author reads the diff, commits named paths and pushes under a push grant; replies and resolves are done by hand under their own grants.

## What it unlocks

- The tool's finding verification, diagnosis and fixing on #539, while every change to a security-sensitive PR passes a person before it leaves the machine.
- No tool reply or resolve can close a thread that needs the owner's ruling, because level 2 cannot reply or resolve.
- No draft toggle question at all (level 2 never toggles).

## What it costs or risks

- Slower: each cycle waits for a person to push, and the tool cannot re-request a review after the push; the author does that by hand.
- More hand work than the project's standard (`--monitor 3`), and the push, reply and resolve grants are needed per action.
- The PR session and the #539 author must not both have live sessions in the #539 checkout at once; the hand-off between them must be explicit.

## What stays unresolved

- Whether to move to level 3 later once #539's review settles.
