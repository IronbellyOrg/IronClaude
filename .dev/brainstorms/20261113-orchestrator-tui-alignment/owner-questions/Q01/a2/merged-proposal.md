<!-- Provenance: produced by /sc:adversarial -->
<!-- Base: Variant 1 (proposal-A) -->
<!-- Incorporated: Variant 2 (proposal-B), Variant 3 (proposal-C), amendments agreed by all three advocates (debate-transcript.md) -->
<!-- Merge date: 2026-11-14 -->

# Proposal A: refuse and report (F2), fail closed, all six channels

## Answer
<!-- Source: Base (Variant 1, proposal-A), part (b) modified by Change 1 from Variant 2 (C-003, X-001) -->

Part (a) is already answered "fix" by the owner (owner update of 2026-11-13, relayed by the team lead; not accept, not F3). This answer covers only (a2) and (b).

(a2) Fix by refusing: any worktree where an in-scope channel names a program that the sweep's `git status` could run is not scanned and is reported as an `unscanned` source row with its reason; no JSON key is added. (b) All six channels are in scope as a minimum (`core.fsmonitor`, `filter.<driver>.clean`, `filter.<driver>.process`, `include.path`/`includeIf`, per-worktree config, `GIT_CONFIG_*` and other inherited environment), stated by outcome, and the ruling names any channel it deliberately leaves out. Anything the check cannot classify is refused and reported `unscanned` with its reason. The ruling does not claim that refusal covers channels nobody listed.

## What happens next if the owner picks it
<!-- Source: Base (Variant 1, proposal-A); step 2 replaced by Change 2 (Variant 3, U-003, C-005); step 3 extended by Change 3 (all advocates; question.md host facts); step 4 inserted by Change 4 (A-002; SW-02 (2); INV-039); step 5 inserted by Change 5 (Variant 2, U-002) -->

1. The owner posts the ruling on the Codex security thread on PR #539 (SW-01): fix shape F2, the six channels as a minimum, the premise (worst-case configuration, `SECURITY.md:168-170`), and authority for the allow-list edit for this purpose only.
2. The #539 author implements it (SW-02) with a two-sided regression test that reproduces the 2026-11-13 probe: it fails if any in-scope program runs in a scanned worktree, and it fails if a worktree that should be refused is scanned.
3. The ruling states how a program counts: only when it could run for that worktree's `git status`; a filter that the system config defines (the host's git-lfs filter, `/etc/gitconfig`) counts only in a worktree whose attributes select it, so not every worktree on this host becomes `unscanned`. An inherited-environment setting counts only when it names a program `git status` could run; the session's `credential.*` keys name none. An environment setting that does count affects the whole run, which is then reported, not partly scanned.
4. The ruling states that the git-status scope is kept separate from the contract allow-list and transcript scans, which share the same path list today, so the fix for `git status` does not change what those other reads cover.
5. The #539 author records in the PR description how the ruling was carried out and why, so the reasoning is easy to find inside the 1003-file PR, and the owner reviews it in the PR before merge (SW-05).

## What it unlocks
<!-- Source: Base (Variant 1, proposal-A); bullet 1 replaced by Change 1 (Variant 2, C-003, X-001; V1 advocate concession 1) -->

- The strongest guarantee that can be checked: the sweep never runs a program that a named channel configures for a scanned worktree, doubt means "do not scan", and any channel left out is named, so the promise is auditable.
- No dependency on git honouring every override; nothing is neutralised, so nothing can be neutralised wrongly.
- Status results are never altered: a worktree is either scanned normally or honestly reported as not scanned.

## What it costs or risks
<!-- Source: Base (Variant 1, proposal-A), unchanged -->

- Less information for the coordinator: worktrees that use LFS, fsmonitor or included config show `unscanned` instead of their git state. How many of the 29 listed worktrees that is, is UNVERIFIED.
- The rule for "could run for this worktree" must itself be right; if it is too broad (any defined filter, or any `GIT_CONFIG_*` variable), every worktree on this host is refused, because the system config defines a git-lfs filter and the session environment carries `GIT_CONFIG_*` credential keys.
- An inherited-environment hit affects the whole run, not one worktree.

## What stays unresolved
<!-- Source: Base (Variant 1, proposal-A); runner-up appended by Change 6 (Variant 3 advocate; V1 advocate concession 2) -->

- Whether any listed worktree actually selects a filter today (how much is lost).
- Whether the owner wants a named trusted program (for example the system git-lfs filter) excepted later.
- The runner-up is the combination from Variant 3 (disable programs by default, refuse only where disabling could change the answer). It would win if a count shows many worktrees that use only fsmonitor, whose git facts F2 would withhold for no security gain.
