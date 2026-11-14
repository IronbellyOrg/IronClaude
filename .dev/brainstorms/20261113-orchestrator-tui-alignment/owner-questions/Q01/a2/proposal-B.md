# Proposal B: the #539 author and the owner pick F1 or F2 at implementation time; all six channels in scope

## Answer

(a2) Rule only the outcome: no program that git configuration or the inherited environment names may run during the sweep's `git status`; the #539 author chooses neutralising (F1) or refusing and reporting `unscanned` (F2), or both, when implementing, and records the choice and its reason in the PR. (b) All six channels are in scope as a minimum, and the ruling names any channel it leaves out.

## What happens next if the owner picks it

1. The owner posts the ruling on the Codex security thread (SW-01): outcome, six channels, premise (worst-case configuration, `SECURITY.md:168-170`), allow-list edit authorised for this purpose only.
2. The #539 author picks the shape, implements it (SW-02), and writes the reason in the PR description; the regression test reproduces the 2026-11-13 probe and covers every in-scope channel.
3. The owner reviews the shape in the PR before merge (SW-05).

## What it unlocks

- The person closest to the code makes the engineering choice with the code in front of them, which is how the spec and ADJ framed it ("The design of the fix belongs to the #539 author and the owner", ADJ line 206).
- No owner time spent on a choice that depends on details only implementation shows (for example how the host's system git-lfs filter interacts with either shape).
- Matches the spec's recommended answer ("F1 or F2"; "yes to all").

## What it costs or risks

- The owner gives up the decision that most affects what the coordinator sees (scanned with programs disabled, or `unscanned`).
- The choice is made inside a 1003-file PR; the reason must be easy to find for review.
- If the author picks F1, a filter that is disabled may change what `status` reports in a repository that uses it (UNVERIFIED); if F2, a too-broad refusal rule could mark every worktree `unscanned` on this host (system git-lfs filter; session `GIT_CONFIG_*` keys).

## What stays unresolved

- The fix shape itself, until the PR.
- Who the #539 author is (Q33).
