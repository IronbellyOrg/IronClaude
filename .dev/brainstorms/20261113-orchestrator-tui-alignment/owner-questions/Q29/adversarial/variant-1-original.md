# Proposal A: an owner-approved user-level reinstall at the merge commit

## Answer

After PR #539 merges, the owner approves one user-level reinstall of the CLI on this host at the merge commit (`uv tool install --force git+https://github.com/IronbellyOrg/IronClaude@<merge sha>`), which replaces the user-level install that already shadows the image's copy; the Coder template catches up on its own schedule.

## What happens next if the owner picks it

1. After SW-05 (the merge), the owner records the approval in the ledger with the exact commit.
2. The reinstall runs once; `superclaude sweep --help` is checked to exit 0 and `/sc:sweep` produces one report (SWEEP-RUNNABLE).
3. The ledger notes that this host runs a newer CLI than the image until the Coder pin is bumped and the workspace updated.
4. XC-04 (the real-id join comparison) can be scheduled the same day.

## What it unlocks

- SWEEP-RUNNABLE within minutes of the merge, with no dependency on the Coder repository's review, image build or workspace update.
- It works with the host as it is: the user-level install at `~/.local/bin` already comes first on `PATH` (observed 2026-11-14), so only replacing it changes what the coordinator runs.

## What it costs or risks

- It goes against the owner's stated rule that IronClaude reaches workspaces only through the Coder template (owner memory, 2026-11-12); it needs an explicit exception.
- This host diverges from other workspaces until the template catches up, and the user-level install keeps shadowing future template updates until it is removed.
- A reinstall from a moving branch instead of the merge commit would install unreviewed code; the commit must be pinned.

## What stays unresolved

- When to remove the user-level install so the template becomes authoritative again.
