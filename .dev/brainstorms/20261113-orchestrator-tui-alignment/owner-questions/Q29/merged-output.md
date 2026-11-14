<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 1 (proposal-A) -->
<!-- Merge date: 2026-11-14T02:30Z -->

# Merged answer for Q29: how the sweep command reaches this host's CLI

<!-- Source: Variant 2 (proposal-B), Answer - merged per Change 1; Base (original, modified) keeps the pinned-commit rule -->
## Answer

Through the Coder template, plus one owner-approved clean-up on this host: after PR #539 merges, the Coder pin is bumped to the merge commit (or later), the image rebuilt and this workspace updated; then the user-level install at `~/.local/bin/superclaude`, which shadows the image's copy on `PATH`, is removed once, with the owner's approval.

<!-- Source: Variants 2 and 3 - merged per Changes 2, 3, 4 -->
## What happens next

1. Until both steps below have run, the ledger records "SWEEP-RUNNABLE not met; `/sc:sweep` duty not runnable; XC-04 held".
2. After SW-05 (the merge), the owner starts the Coder monitor by hand (`workflow_dispatch` on `ironclaude-upstream-monitor.yml`) or waits for its daily run; the bump PR is reviewed and merged, the image built, the template pushed and this workspace updated (this recreates the container, so running sessions end; plan it between sessions).
3. After the update, the owner approves one removal of the user-level install (`uv tool uninstall superclaude`, which also removes its `ic` entry point; the image provides both). Doing it after the update means the host never falls back to an older revision.
4. In the coordinator's own session, `which -a superclaude` shows the image install first (not a worktree `.venv` or `~/.local` copy), `superclaude sweep --help` exits 0, and `/sc:sweep` writes one report. The result and date go in the ledger; XC-04 can then be scheduled.

## What it unlocks
The sweep for the coordinator on the same reviewed, pinned CLI every workspace gets, with this host back on the single delivery path the owner set.

## What it costs or risks
- Slower than an in-place reinstall: a Coder PR, an image build and a workspace update.
- The workspace update ends running sessions.
- Who made the user-level install (2026-11-12 22:12) is unknown; anything that relied on it is UNVERIFIED.

## What stays unresolved
- The coordinator's real `PATH` until step 4 is run in its session.
