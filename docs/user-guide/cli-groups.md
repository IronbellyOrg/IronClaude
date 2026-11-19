# The `superclaude` command groups (6.0.0)

This page lists every `superclaude` command group that 6.0.0 ships, what it is for, and where it is documented. Every description comes from the command's own `--help` text; run `superclaude <group> --help` for the full list of options. The slash commands (`/sc:...`) are in the [commands reference](commands.md).

## The groups

| Group | What it does | More |
|-------|--------------|------|
| `install`, `update`, `install-skill` | Copy the framework into `~/.claude/` (`install`), refresh it (`update`), or install one skill (`install-skill <name>`). | [Installation](../getting-started/installation.md), [Upgrading](../getting-started/upgrading.md) |
| `doctor` | Check the installation health. | [Installation](../getting-started/installation.md#-verification) |
| `version` (and `--version`) | Show the version. | |
| `mcp` | Install and manage MCP servers for Claude Code. | [MCP installation](mcp-installation.md) |
| `init-lite` | Safely audit project-local SuperClaude context surfaces. | [commands reference](commands.md) (`/sc:init-lite`) |
| `eval` | Run and inspect the cliEval real-eval harness (`list`, `describe`, `doctor`, `run`). | [Eval pipeline](eval-pipeline.md) |
| `reflect` | Run the post-execution reflect gate as a top-level subprocess. | [commands reference](commands.md) (`superclaude reflect run`) |
| `swarm` | Orchestrate multi-model swarm execution. | [Swarm guide](../swarm/README.md) |
| `recommend` | Deterministic helpers behind the `sc-recommend` skill (lookup cache, telemetry, eval). | [commands reference](commands.md) (`/sc:recommend`) |
| `sweep` | Read-only sweep of Orca Runs, worktrees and sessions. | [below](#superclaude-sweep) and `/sc:sweep` in the [commands reference](commands.md) |
| `observe` | Read-only terminal observer for Orca workers. | [below](#superclaude-observe) |
| `issue-watch` | Poll GitHub for approved issues and start one Orca claim session each. | [below](#superclaude-issue-watch), [design](../designs/issue-watcher.md) |
| `review` | Deterministic helpers for document review loops. | [below](#superclaude-review), [review panel](../reference/review-panel-live7.md) |

The groups `prd`, `cleanup-audit`, `cli-portify`, `roadmap`, `tasklist` and `sprint` were removed in 6.0.0. `superclaude <group>` now answers "No such command"; see the [6.0.0 release notes](../releases/v6.0.0.md#command-line-groups-and-their-flags) for the replacements.

`sweep`, `observe`, `issue-watch` and `review` are new since 5.0.0. The `issue-pipeline` group (the plan-approval gate) was removed with issue 655.

## `superclaude sweep`

`superclaude sweep run` collects, classifies and publishes one read-only report and prints one JSON object. It reads Orca Runs, the worktrees of the checkout and the Claude Code sessions in an activity window; it changes nothing in Orca, in git or in any worktree. The report is one dated file under `.dev/sweeps/`.

| Option | Meaning |
|--------|---------|
| `--run TEXT` | Orca Run id to read; repeat for several. Default: the Run bound to this terminal. |
| `--window TEXT` | Activity window, `<N>h` or `<N>d`, at most `720h` or `30d`. Default `6h`. |
| `--root TEXT` | Checkout root. Default: found from the current folder. |
| `--output TEXT` | Report folder, `<root>/.dev/sweeps/` or below. Default `<root>/.dev/sweeps/`. |

`/sc:sweep` runs it once, reads the report and prints the session counts and the report path.

## `superclaude observe`

A read-only terminal observer for Orca workers. It shows the worker ledger Orca reports for its workers (the next-action kind as Orca gives it, freshness, collected and reported counts) and can write a plain-text record and a versioned JSON snapshot. It never writes to Orca: no key and no option maps to an Orca call.

| Option | Meaning |
|--------|---------|
| `--once` | Read once, print the plain-text record to standard output and exit. |
| `--width 160\|116\|80` | Bind the output to 160, 116 or 80 columns. With `--once` it prints the screen text instead of the record. |
| `--ascii` | Use ASCII only (also chosen for a terminal that is not UTF-8). |
| `--fixture TEXT` | Replay a synthetic fixture variant instead of calling Orca (for example `base`). |
| `--run TEXT` | Read one Run only (an Orca run id). |
| `--snapshot FILE` | Write the JSON snapshot to this file. Default in live mode: the per-user state directory. |
| `--questions` | List the coordinator questions (messages of type `question`) of the one Run named by `--run`. Needs `--run` and a live source. |

The observer polls Orca once every 15 seconds with at most 5 calls per read. The caps are per observer process, so several observers running at once multiply the load on Orca. With `--questions` it never runs `run-use` and never binds to a Run: start it from the terminal that already holds the Run. The question list is best effort: coverage is unknown and bursts of more than 100 rows between reads may be lost.

## `superclaude issue-watch`

Polls GitHub for approved issues and starts one Orca claim session for each. Run `once` from a timer. The configuration file defaults to `~/.config/superclaude/issue-watch.json` (`--config PATH` on every subcommand).

| Subcommand | What it does |
|------------|--------------|
| `check-config` | Validates the configuration, the worktree and the approvers file; writes nothing. |
| `init-state` | Creates the state directory, store and lock; refuses if a store exists. |
| `once` | Runs one poll cycle and exits with its code. `--dry-run` reads and decides but writes no store and never calls Orca. |
| `status` | Reports health, counts, stale entries and retry commands (read-only). `--json` prints JSON. |
| `reset` | Forfeits the launch guarantee of one issue (`reset ISSUE --forfeit-guarantee`, only for an abandoned or unknown issue) or clears the rate limit (`reset --rate-limit`). Never both, never neither. |

A first run looks like this (all from the command's own examples):

```bash
superclaude issue-watch check-config
superclaude issue-watch init-state
superclaude issue-watch once --dry-run
superclaude issue-watch status --json
```

The design and the setup steps are in [issue-watcher.md](../designs/issue-watcher.md) and [issue-watcher-setup.md](../designs/issue-watcher-setup.md).

## `superclaude review`

`review` has its own subcommands; `superclaude review <subcommand> --help` shows the options of each.

- `review` holds deterministic helpers for document review loops. Its subcommands are `cluster`, `fixcheck`, `ledger`, `manifest`, `merge`, `panel`, `safety-scan`, `telemetry` and `verify-citations`. The reviewer panel it resolves is described in [review-panel-live7.md](../reference/review-panel-live7.md).
