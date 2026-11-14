# Proposal A: refuse and report (F2), fail closed, all six channels

## Answer

(a2) Fix by refusing: any worktree where an in-scope channel names a program that the sweep's `git status` could run is not scanned and is reported as an `unscanned` source row with its reason; no JSON key is added. (b) All six channels are in scope (`core.fsmonitor`, `filter.<driver>.clean`, `filter.<driver>.process`, `include.path`/`includeIf`, per-worktree config, `GIT_CONFIG_*` and other inherited environment), stated by outcome, and anything the check cannot classify is treated as unsafe.

## What happens next if the owner picks it

1. The owner posts the ruling on the Codex security thread on PR #539 (SW-01): fix shape F2, the six channels as a minimum, the premise (worst-case configuration, `SECURITY.md:168-170`), and authority for the allow-list edit for this purpose only.
2. The #539 author implements it (SW-02) with a regression test that reproduces the 2026-11-13 probe and fails if a worktree using any in-scope channel is scanned instead of reported `unscanned`.
3. The ruling states how a program counts: only when it could run for that worktree's `git status`; a filter that the system config defines (the host's git-lfs filter, `/etc/gitconfig`) counts only in a worktree whose attributes select it, so not every worktree on this host becomes `unscanned`.

## What it unlocks

- The strongest guarantee: the sweep never runs a configured program, including through a channel nobody listed, because doubt means "do not scan".
- No dependency on git honouring every override; nothing is neutralised, so nothing can be neutralised wrongly.
- Status results are never altered: a worktree is either scanned normally or honestly reported as not scanned.

## What it costs or risks

- Less information for the coordinator: worktrees that use LFS, fsmonitor or included config show `unscanned` instead of their git state. How many of the 29 listed worktrees that is, is UNVERIFIED.
- The rule for "could run for this worktree" must itself be right; if it is too broad (any defined filter, or any `GIT_CONFIG_*` variable), every worktree on this host is refused, because the system config defines a git-lfs filter and the session environment carries `GIT_CONFIG_*` credential keys.
- An inherited-environment hit affects the whole run, not one worktree.

## What stays unresolved

- Whether any listed worktree actually selects a filter today (how much is lost).
- Whether the owner wants a named trusted program (for example the system git-lfs filter) excepted later.
