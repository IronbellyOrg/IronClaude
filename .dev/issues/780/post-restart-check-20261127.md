# Issue 780: post-restart check and route recommendation (2026-11-27)

Author: the issue 780 agent. Read-only check; nothing in Orca was changed or restarted.
Public record: https://github.com/IronbellyOrg/IronClaude/issues/780#issuecomment-7222363136

## Verdict

The one-time override of 2026-11-26 held, but `orca worktree current --json` still reports
`github:superclaude-org/superclaude_framework` in every worktree created before the override.
Issue 780 stays open.

## Evidence (Orca 1.4.245-aidev02.5fa1a6608658, read 2026-11-27 15:40 to 15:45 UTC)

1. `orca worktree current --json` in `/home/coder/workspaces/worktrees/IronClaude/Coordinator`:
   `projectId: github:superclaude-org/superclaude_framework`.
2. Orca processes started 2026-11-27 15:05:22 UTC (`ps`), so Orca restarted after the override
   (2026-11-26 12:13 UTC). The request said about 15:35; the process start time is the
   verified one. Whether the repo Settings panel was opened afterwards is not known.
3. `orca repo show --repo id:e8e07d51-c261-4936-815e-06aeceeb5bf8 --json`: `upstream: null`,
   `gitRemoteIdentity.canonicalKey: github.com/IronbellyOrg/IronClaude`. The override persisted.
4. Orca state file `~/.config/orca/profiles/local-default/profile-state.db` (read from a copy
   in a private temp directory, deleted afterwards):
   - domain `projects`: id `github:ironbellyorg/ironclaude`, provider identity IronbellyOrg/IronClaude.
   - domain `projectHostSetups`: `projectId: github:ironbellyorg/ironclaude`.
   - both domains were last written at 2026-11-26 12:13:01 UTC, the time of the override.
   - domain `worktreeMeta` (one row per worktree, holds its own `projectId`):
     25 rows created before the override carry `github:superclaude-org/superclaude_framework`;
     4 rows created after it (issue-834-rest, issue-611, planning-protocol,
     reflect-issues-filing) carry `github:ironbellyorg/ironclaude`; 2 rows carry no id.
5. Installed CLI surface: `orca worktree set` has no project-id option; `orca repo` offers
   only list, add, show, set (worktree visibility), set-base-ref, search-refs. No command
   rewrites the project id on an existing worktree.
6. Bundle code (`/opt/Orca/resources/app.asar`, searched with grep, not fully read) shows new
   worktrees taking `projectId` from the repo's project host setup at creation, which fits
   point 4. The exact code path that serves `worktree current` is UNVERIFIED.

## Cause

Each worktree stores a copy of the project id when it is created. The override fixed the
project and host-setup records, which new worktrees copy; it never touched the copies already
stored on older worktrees, which is what `worktree current` shows for them.

## Route recommendation: (a) change Orca

Route (a): change Orca (IronOrca repo; no issue number known) so a worktree reads its project
id from its current project record instead of a stored copy, or refreshes the copy when the
project record changes. Why (a) over the alternative:

- Route (b), rewriting `projectId` on the 25 old rows in the state file, needs Orca stopped,
  which kills every agent terminal, and it fixes only today's rows. The next change to the
  project record would leave the same gap.
- Repository edits cannot help: no code in `src/` reads the project id.

If the owner prefers a quick stopgap before (a) lands, (b) is the only available way, done by
the owner with Orca stopped and a copy of the state file taken first.

## Decision owner

The decision to change Orca belongs to Clay (the owner). Later on 2026-11-27 the IronFlow
session decided for him, under his no-stop rule: do not change Orca and do not rewrite the 25
old rows (either needs another Orca restart, which kills every agent terminal). The override is
the fix this issue needs: worktrees created after it (2026-11-26 12:13 UTC) report the fork id,
and the 25 older worktrees show the old id only until `/sc:worktrees` retires them. Route (a)
stays recorded here as a recommendation, not acted on. Clay closes #780 after the pull request
merges, with a note that new worktrees report the right id.

## Not done and still open

- Project id on the 25 older worktrees: left as is by the decision above.
- The Orca link-flag ban in CLAUDE.md stays until the owner lifts it.
- CLAUDE.md Orca paragraph: updated in the pull request that carries this file (Refs #780).
