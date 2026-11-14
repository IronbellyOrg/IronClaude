# Proposal C: a stated combination: neutralise by default, refuse and report where neutralising could change the answer

## Answer

(a2) Combine both shapes: every worktree is scanned with all configured programs disabled (F1), except where disabling a program could change what `git status` reports for that worktree (for example a filter the worktree's attributes select), in which case the worktree is reported `unscanned` with its reason (F2). (b) All six channels are in scope, stated by outcome, with "any channel not listed" handled the same way: disabled if that is safe, otherwise refused.

## What happens next if the owner picks it

1. The owner posts the ruling on the Codex security thread (SW-01): the combination, the six channels as a minimum, the premise (worst-case configuration, `SECURITY.md:168-170`), allow-list edit authorised for this purpose only.
2. The #539 author implements it (SW-02) with a regression test that reproduces the 2026-11-13 probe and fails if any in-scope program runs, and fails if a worktree whose result would be altered is reported as scanned.
3. The ruling notes the two host facts the shape must respect: the system config's git-lfs filter applies to every repository (so a "defines it" rule would refuse everything), and the session environment routinely carries `GIT_CONFIG_*` credential keys that name no program.

## What it unlocks

- Most worktrees keep full git facts: fsmonitor is a speed-up whose absence should not change what `status` reports; for included config and environment settings it depends on what they set (UNVERIFIED in general), which is exactly where the "could change the answer" rule refuses.
- Results are never silently wrong: where disabling could alter the answer, the worktree is honestly `unscanned`.
- Avoids F2's failure on this host (everything refused) and F1's risk (LFS repositories reported as changed when they are not).

## What it costs or risks

- Two behaviours to implement and test instead of one; more for a reviewer to check inside a 1003-file PR.
- The rule "could change the answer" must be stated precisely by the author; a wrong rule either leaks (runs a program) or over-refuses.
- It goes further than the spec's wording, which offered F1 or F2, not a combination.

## What stays unresolved

- Whether any listed worktree actually selects a filter today.
- Whether git versions other than 2.47.3 behave the same.
