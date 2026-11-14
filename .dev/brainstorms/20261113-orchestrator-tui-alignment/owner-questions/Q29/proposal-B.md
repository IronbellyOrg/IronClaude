# Proposal B: the Coder template update

## Answer

The sweep reaches this host through the Coder template: after PR #539 merges, the Coder repository's daily monitor opens its pin-bump PR, which is merged, the image rebuilt, the template pushed and this workspace updated.

## What happens next if the owner picks it

1. After SW-05 (the merge), the next daily run of `ironclaude-upstream-monitor.yml` opens "chore(deps): bump IronClaude pin to <sha>" in the Coder repository (or the owner runs it by hand with `workflow_dispatch`).
2. The bump PR is reviewed and merged; the image is rebuilt and the template pushed; the owner updates this workspace.
3. The coordinator checks `superclaude sweep --help` exits 0 and `/sc:sweep` produces one report (SWEEP-RUNNABLE), recorded with its date.
4. XC-04 is scheduled after that.

## What it unlocks

- One delivery path for every workspace, as the owner stated it; every engineer runs the same pinned CLI.
- No exception to record and no host drift.

## What it costs or risks

- Slower: up to a day for the monitor, plus a Coder PR, an image build and a workspace update.
- A workspace update may restart the workspace and end running sessions, including the coordinator and Orca (UNVERIFIED).
- On this host, the user-level install at `~/.local/bin/superclaude` (revision `d2d8a2d16`) comes before the image's `/usr/local/bin/superclaude` on `PATH` (observed 2026-11-14). Unless that user-level install is removed, the template update changes nothing the coordinator runs, and SWEEP-RUNNABLE still fails.

## What stays unresolved

- Who removes the shadowing user-level install, and whether it returns after a rebuild (whether `/home/coder` persists is UNVERIFIED).
