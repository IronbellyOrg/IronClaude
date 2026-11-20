---
name: worktrees
version: "1.0.0"
description: "List the git worktrees of our repos with the reason each is kept or removable, save a finished worktree's .dev files to the evidence repo, and remove the ones whose work is safe (nothing is removed unless --apply is typed)"
category: workflow
complexity: standard
mcp-servers: []
personas: [analyzer]
argument-hint: "<list|archive|retire|prune> [<worktree>] [--apply] [--out <dir>]"
allowed-tools: Bash
---

# /sc:worktrees: Clean Up Finished Git Worktrees

`/sc:worktrees <verb>` runs the cleanup script of this checkout, `scripts/worktree_cleanup.py`, and prints its table. A worktree is removed only when all eight rules hold: it is a linked worktree of one of our repos, its own pull request is merged, nothing was added after that pull request, every issue it relates to is closed, nothing unsaved is in it, nothing but its own Orca terminals is using it, it has been idle for the idle floor, and it is not pinned. Untracked and ignored `.dev/` files are first saved to the evidence repo and checked against GitHub. If anything cannot be read or finished, the worktree is kept and the reason is shown.

`list`, `retire` and `prune` are dry runs unless you type `--apply`. `archive` is the one verb that writes without it: it saves to the evidence repo and removes nothing. `/sc:worktrees` is for a person only. It is on the never-as-worker list in `~/.claude/WORKER-CONTRACT.md`, so a dispatched worker never runs it.

## Triggers

Explicit only: a person types `/sc:worktrees <verb>`. Nothing starts it automatically.

## Usage

```text
/sc:worktrees list
/sc:worktrees archive <worktree> [--out <dir>]
/sc:worktrees retire <worktree> [--apply] [--out <dir>]
/sc:worktrees prune [--apply] [--out <dir>]
```

## Options

| Argument | Meaning |
|---|---|
| `list` | Print the table of every worktree of every repo of ours with its decision and reason; removes nothing |
| `archive <worktree>` | Run only the save step for one worktree and print `VERIFIED` when the copy matches GitHub; it writes to the evidence repo with or without `--apply` and removes nothing |
| `retire <worktree>` | Remove one worktree whose work is safe; run it from outside that worktree; takes a path or a unique folder name |
| `prune` | Apply the same decision to every worktree; with `--apply` it removes the removable ones, without it it writes the table to `<out>/prune-<UTC stamp>.md` and `.json` |
| `--apply` | Actually remove (`retire` and `prune`). Pass it only when the person typed it. Without it nothing is removed, closed or cleared |
| `--out <dir>` | The folder for the table files and the per-repo lock files; never inside a worktree (default `~/.local/state/worktree-cleanup`) |

## STOP rules (checked before anything runs)

Print the usage block and stop, running nothing, for: no verb; a verb that is not one of the four; `archive` or `retire` without a `<worktree>`; an unknown flag; a flag with no value. When `scripts/worktree_cleanup.py` does not exist at the top of the current git checkout (found with `git rev-parse --show-toplevel`), print "`/sc:worktrees` runs only inside an IronClaude checkout that has `scripts/worktree_cleanup.py`" and stop, running nothing.

## What it runs

Run this one command from the top of the current checkout, passing the person's arguments unchanged and adding nothing:

```text
uv run --no-project python scripts/worktree_cleanup.py <verb> [<worktree>] [--apply] [--out <dir>]
```

No skill is activated. Print the table and the summary line it prints. The exit code is 0 when the run completed, 64 for a usage error or a `retire` of a worktree that is not removable, and 69 when a lookup or a removal failed (the table still shows what happened).

## Examples

```text
/sc:worktrees list
/sc:worktrees archive issue-687
/sc:worktrees retire issue-687 --apply
/sc:worktrees prune
```

## Outputs

One table with a row per worktree (repo, folder, branch, in Orca, pull request, issues, idle days, size, saved copy, decision, reason), then one summary line with the counts of removed, kept and failed. `prune` also writes `prune-<UTC stamp>.md` and `.json` under `--out`; the JSON holds the same rows and the list of commands that ran. The script writes nothing inside any worktree.

## Boundaries

**Will:**

- Run the script of this checkout with the arguments the person typed and print its table
- Pass `--apply` only when the person typed it

**Will Not:**

- Add `--apply`, a force flag or any other flag of its own
- Merge anything, push to a source repo or delete a remote branch
- Remove, move or clear anything without `--apply`
- Run as a dispatched worker
- Run outside an IronClaude checkout that has `scripts/worktree_cleanup.py`

## Related Commands

| Command | Difference |
|---|---|
| `/sc:sweep` | A read-only report on Orca Runs, worktrees and sessions; it changes nothing |
| `/sc:closeout` | Settles a merged pull request and its issue; it does not touch worktrees |
