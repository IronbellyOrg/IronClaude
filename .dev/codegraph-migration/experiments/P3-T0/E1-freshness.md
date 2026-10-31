# E1-freshness (Phase 3 Task 2, prerequisite experiment E-1)

Date: 2026-10-31, codegraph 1.6.2, Claude Code 2.1.316. Scratch worktree `.dev/worktrees/cg-sandbox` (branch `tmp/cg-sandbox` from `e4b7d131`), nested inside the indexed worktree `.dev/worktrees/codegraph-adoption`; removed at the end of Task 2. Procedure: the 8 steps of `BS` §2.3 (`.dev/codegraph-migration/brainstorm/P3-codegraph-opportunities/merged-requirements.md` lines 92-104), plus MCP `codegraph_status` in a nested and a sibling worktree (access decision §6.1). Every CLI `codegraph status` ran only after `pgrep -f 'codegraph\.js (init|index)'` printed nothing (standing rule 7). The probe edits went into the sandbox's copy of `src/superclaude/cli/install_core.py` and a new sandbox file, never into this worktree.

## Result

- **Outcome A.** Without any daemon or MCP client on the sandbox, CLI `codegraph status` lists pending files right after a write: it printed `Pending Changes: Added: 1 files / Modified: 1 files` 0.45 s after a new file was written (step 4b below), and `codegraph status --json` carries the same counts as `"pendingChanges":{"added":0,"modified":1,"removed":0}`. So the FR-05 run-state rule stands: a CLI-only session can see that its index is behind and label rows `stale`.
- Without a daemon the index itself does not catch up (node count unchanged after 5 s, `codegraph query` finds no new symbol): reads stay stale until something syncs. With a `serve --mcp` process running on the sandbox, the new function was indexed within 4 s (node count 8,824 → 8,825 → 8,826; `codegraph query _e1_probe_daemon` found it). `CODEGRAPH_NO_DAEMON=1` behaves like the no-daemon case.
- `.codegraph/daemon.sock` never existed in 1.6.2, with or without a running `serve --mcp` (steps 0-7): socket presence is not a usable "daemon live" signal. A live watcher shows only as a `codegraph.js serve --mcp --path <worktree>` process.
- Nested worktree before its own init: CLI and MCP status both answer from the parent index with the warning "This CodeGraph index belongs to a different git working tree … Run "codegraph init -i" in this worktree for a worktree-local index." (CLI step 0; MCP below). `codegraph init --yes` run inside the nested worktree created its own `.codegraph/` (step 1), so plain `init --yes` is enough for a worktree-local index in 1.6.2; `codegraph init --help` lists `-i, --index` as "Deprecated: indexing now runs by default; flag accepted for backward compatibility" (see `E2-help.md`).
- Sibling worktree (`/tmp/cg-sibling-p3t0`, no `.codegraph/` above it): MCP `codegraph_status` answers "isn't indexed with codegraph (no .codegraph/ directory found walking up from it) … Indexing is the user's decision" — that is `index_state: not_initialized`.
- MCP `codegraph_status` on the sandbox after the no-daemon write reported `Changes since index: 0 added, 0 modified, 0 removed` and 972 files: the MCP call opened the project and synced it (`Latest file indexed` moved to the call time).

## Transcript (script `e1.sh`, CLI status output cut to the first 14 lines per call)

```text
## Step 0: nested worktree before its own init (13:42:57)
$ codegraph status   (in /home/coder/workspaces/IronClaude/.dev/worktrees/codegraph-adoption/.dev/worktrees/cg-sandbox, nested inside the indexed worktree /home/coder/workspaces/IronClaude/.dev/worktrees/codegraph-adoption)

CodeGraph Status

Project: /home/coder/workspaces/IronClaude/.dev/worktrees/codegraph-adoption
⚠ This CodeGraph index belongs to a different git working tree.
  Running in: /home/coder/workspaces/IronClaude/.dev/worktrees/codegraph-adoption/.dev/worktrees/cg-sandbox
  Index from: /home/coder/workspaces/IronClaude/.dev/worktrees/codegraph-adoption
Results reflect that tree's code (often a different branch), not this worktree — symbols changed only here are missing. Run "codegraph init -i" in this worktree for a worktree-local index.

Index Statistics:
  Files:     971
  Nodes:     8,824
ls: cannot access '/home/coder/workspaces/IronClaude/.dev/worktrees/codegraph-adoption/.dev/worktrees/cg-sandbox/.codegraph': No such file or directory
serve processes for sandbox path: 0
daemon.sock: absent

## Step 1: codegraph init --yes in the nested sandbox (13:42:57)
◆  Indexed 971 files
│
●  8,824 nodes, 19,695 edges in 1.2s
│
└  Done

exit=0
/home/coder/workspaces/IronClaude/.dev/worktrees/codegraph-adoption/.dev/worktrees/cg-sandbox/.codegraph
## Step 2 (13:43:02)
$  codegraph status

CodeGraph Status

Project: /home/coder/workspaces/IronClaude/.dev/worktrees/codegraph-adoption/.dev/worktrees/cg-sandbox

Index Statistics:
  Files:     971
  Nodes:     8,824
  Edges:     19,695
  DB Size:   30.47 MB
  Backend:   node:sqlite — built-in (full WAL)
  Journal:   wal

Nodes by Kind:
daemon.sock: absent

## Step 3: append a function (13:43:03)
## Step 4: status at once (13:43:03)
$  codegraph status

CodeGraph Status

Project: /home/coder/workspaces/IronClaude/.dev/worktrees/codegraph-adoption/.dev/worktrees/cg-sandbox

Index Statistics:
  Files:     971
  Nodes:     8,824
  Edges:     19,695
  DB Size:   30.47 MB
  Backend:   node:sqlite — built-in (full WAL)
  Journal:   wal

Nodes by Kind:
## Step 4: status after 5 s (13:43:08)
$  codegraph status

CodeGraph Status

Project: /home/coder/workspaces/IronClaude/.dev/worktrees/codegraph-adoption/.dev/worktrees/cg-sandbox

Index Statistics:
  Files:     971
  Nodes:     8,824
  Edges:     19,695
  DB Size:   30.47 MB
  Backend:   node:sqlite — built-in (full WAL)
  Journal:   wal

Nodes by Kind:
ℹ No results found for "_e1_probe_nodaemon"
daemon.sock: absent

## Step 5: with a daemon running (13:43:09)
serve processes for sandbox path: 2
daemon.sock: absent
## Step 5: status at once (13:43:13)
$  codegraph status

CodeGraph Status

Project: /home/coder/workspaces/IronClaude/.dev/worktrees/codegraph-adoption/.dev/worktrees/cg-sandbox

Index Statistics:
  Files:     971
  Nodes:     8,825
  Edges:     19,696
  DB Size:   30.73 MB
  WAL Size:  0.73 MB
  Backend:   node:sqlite — built-in (full WAL)
  Journal:   wal

## Step 5: status after 5 s (13:43:18)
$  codegraph status

CodeGraph Status

Project: /home/coder/workspaces/IronClaude/.dev/worktrees/codegraph-adoption/.dev/worktrees/cg-sandbox

Index Statistics:
  Files:     971
  Nodes:     8,826
  Edges:     19,697
  DB Size:   30.73 MB
  WAL Size:  0.72 MB
  Backend:   node:sqlite — built-in (full WAL)
  Journal:   wal


Search Results for "_e1_probe_daemon":

function    _e1_probe_daemon
  src/superclaude/cli/install_core.py:159
  ()
daemon.sock: absent
Terminated
after stopping the daemon:
daemon.sock: absent

## Step 6: CODEGRAPH_NO_DAEMON=1 (13:43:56)
## Step 6: status at once
$ CODEGRAPH_NO_DAEMON=1 codegraph status

CodeGraph Status

Project: /home/coder/workspaces/IronClaude/.dev/worktrees/codegraph-adoption/.dev/worktrees/cg-sandbox

Index Statistics:
  Files:     971
  Nodes:     8,826
  Edges:     19,697
  DB Size:   30.73 MB
  Backend:   node:sqlite — built-in (full WAL)
  Journal:   wal

Nodes by Kind:
## Step 6: status after 5 s (13:44:01)
$ CODEGRAPH_NO_DAEMON=1 codegraph status

CodeGraph Status

Project: /home/coder/workspaces/IronClaude/.dev/worktrees/codegraph-adoption/.dev/worktrees/cg-sandbox

Index Statistics:
  Files:     971
  Nodes:     8,826
  Edges:     19,697
  DB Size:   30.73 MB
  Backend:   node:sqlite — built-in (full WAL)
  Journal:   wal

Nodes by Kind:
ℹ No results found for "_e1_probe_nodaemon_env"

## Step 7: daemon.sock at the end (13:44:02)
daemon.sock: absent
```

### Step 4b: pending list right after a write, full `status` tail (no daemon)

```text
$ printf '\n\ndef _e1_probe_immediate():\n    return 4\n' >> src/superclaude/policy_probe_e1.py   # 13:44:13.742
$ codegraph status | sed -n '/Pending/,$p'                                                    # 13:44:14.187
Pending Changes:
  Added:     1 files
  Modified:  1 files
ℹ Run "codegraph sync" to update the index
$ codegraph status --json   (same moment, before the write above; excerpt)
"pendingChanges":{"added":0,"modified":1,"removed":0},"worktreeMismatch":null
```

### MCP `codegraph_status`, nested and sibling worktrees

```text
projectPath=.../cg-sandbox/.dev/worktrees/cg-nested   (nested, no own init)
> ⚠ This CodeGraph index belongs to a different git working tree.
>   Running in: /home/coder/workspaces/IronClaude/.dev/worktrees/codegraph-adoption/.dev/worktrees/cg-sandbox/.dev/worktrees/cg-nested
>   Index from: /home/coder/workspaces/IronClaude/.dev/worktrees/codegraph-adoption/.dev/worktrees/cg-sandbox
> Results reflect that tree's code (often a different branch), not this worktree — symbols changed only here are missing. Run "codegraph init -i" in this worktree for a worktree-local index.
**Files indexed:** 972 … **Changes since index:** 0 added, 0 modified, 0 removed

projectPath=/tmp/cg-sibling-p3t0   (sibling, no index above it)
The project at /tmp/cg-sibling-p3t0 isn't indexed with codegraph (no .codegraph/ directory found walking up from it), so codegraph cannot query it. Use your built-in tools (Read/Grep/Glob) for that codebase instead, and don't call codegraph for it again this session. Indexing is the user's decision — they can run 'codegraph init' in that project to enable it.

projectPath=.../cg-sandbox   (nested, own index after step 1)
**Files indexed:** 972 … **Changes since index:** 0 added, 0 modified, 0 removed   (no worktree warning)
```

Outcome: A

## Cleanup

At the end of Task 2: `git worktree remove --force` for `cg-sandbox/.dev/worktrees/cg-nested`, `/tmp/cg-sibling-p3t0` and `.dev/worktrees/cg-sandbox` (`--force` because the sandbox held the probe edits), then `git branch -D tmp/cg-sandbox tmp/cg-nested tmp/cg-sibling`. One `codegraph.js serve --mcp --path …/cg-sandbox` process (parent pid 1, left by an E-6 headless session) was still running after the removal and was stopped with `kill`.
