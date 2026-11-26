# Diff Analysis: spec Comparison (Run ledger script)

## Metadata
- Generated: 2026-11-26T17:40:00Z
- Variants compared: 2 (V1 = sonnet:architect, V2 = sonnet:refactorer)
- Total differences found: 16
- Categories: structural (2), content (11), contradictions (0), unique (3), shared assumptions (3)
- Extra evidence (read-only probe /tmp/runledger-probe.py, 2026-11-26, real Orca): 62 non-legacy Runs, 22 live worktrees. Rule "live worktree" admits 3 Runs (Coordinator worktree, Coder issue-516, and `run_93bfa00cae2b` because it used the main checkout /home/coder/workspaces/IronClaude, which Orca always lists). Rule "unfinished task" (status not in completed/failed/cancelled) admits 9 Runs: 6 hold a single old `ready` task, `run_93bfa00cae2b` holds 15 `blocked` + 2 `ready`. Union = 10 Runs. A full rebuild with no short-circuit took 26.1 s.

## Structural Differences
| # | Area | V1 | V2 | Severity |
|---|------|----|----|----------|
| S-001 | Code layout | Package `src/superclaude/cli/run_ledger/` with `orca.py`, `rules.py` (pure `decide()`), `store.py`, `commands.py` | One file `src/superclaude/cli/run_ledger.py` (~150 lines) | Medium |
| S-002 | Command surface | Group `superclaude run-ledger` with `build`, `add`, `show`, `path` | One command `superclaude run-ledger` (flags `--ledger`, `--dry-run`, `--json`, `--accept-empty`) | Medium |

## Content Differences
| # | Topic | V1 | V2 | Severity |
|---|-------|----|----|----------|
| C-001 | Hook | Ship PostToolUse hook `run-ledger-record.sh` + `add` subcommand; drop only if run-create output lacks the id | Drop the hook; coordinator runs the build itself after run-create | High |
| C-002 | Concurrency | `flock` on a lock file, build merges under lock so a hook add during a build survives; 10 s lock timeout, exit 3 | No lock (single writer); atomic temp + `os.replace` only | Medium |
| C-003 | Ledger path | `~/.superclaude/run-ledger/ledger.json` (env override) | `${XDG_STATE_HOME:-~/.local/state}/superclaude/run-ledger.json` (env override); sweep already uses XDG_STATE_HOME | Low |
| C-004 | Sweep consumption | New `--ledger PATH` and `--no-ledger` flags on `sweep run`; default reads ledger when no `--run` | No new flag; fallback to ledger when no `--run` and no bound Run; env var for tests | Low |
| C-005 | New-Run rule with no previous ledger | `created_at` > now minus 24 h | Rule skipped (else all 62 would be "new") | Medium |
| C-006 | Plausibility guards | exit 4 on: 0 Runs, 0 worktrees, 0 included while a Run was active in 24 h, and shrink to under 20% when old included >= 5; `--force` bypasses the last two | exit 1 on: Orca failure, 0 worktrees, 0 Runs with old ledger, 0 included while old >= 1 and a non-legacy Run exists; `--accept-empty` overrides the last | High |
| C-007 | Exit codes | 0 ok, 1 Orca, 2 usage, 3 lock timeout, 4 implausible | 0 ok, 1 Orca or implausible, 2 usage | Low |
| C-008 | Schedule | Crontab `*/45` with `flock -n`, shipped as `src/superclaude/templates/run-ledger.cron.example` | Crontab `17,47`, shipped as `docs/user-guide/run-ledger-cron.md` or in `--help` | Low |
| C-009 | Tests | About 40 named tests in 5 files (rules, build, store, sweep, hook) | 10 named tests (some parametrised) in one file | Low |
| C-010 | Worker-list paging cap | Cap 20 pages | Cap 50 pages plus repeated-cursor FAIL | Low |
| C-011 | Ledger schema | `reasons`, `source`, `added_at`, `last_seen_active`, `build_ok`, counts | `reasons`, `live_worktree_ids`, `unfinished_task_count`, short `objective`, counts; `generated_at` captured before the first Orca call | Low |

## Contradictions
None found. The variants disagree on design, not on facts. Both verified the same Orca shapes (worker `resource.worktreeId` equals `worktree list` id string `<repoId>::<abs path>`; task statuses seen: completed 644, failed 60, blocked 18, ready 12).

## Unique Contributions
| # | Variant | Contribution | Value |
|---|---------|--------------|-------|
| U-001 | V1 | Verified `worker-list --run <unknown>` returns ok with zero workers while `task-list --run <unknown>` returns `run_not_found`; so use `run-list` as the universe. Prints count of blocked-only Runs in build output. | Medium |
| U-002 | V1 | Hook-entry expiry (24 h) and a fixture-based hook test; `--timeout` aggregate; `show` and `path` helpers | Low |
| U-003 | V2 | `generated_at` taken before the first Orca call so a Run created mid-build is not missed; explicit statement of what was deleted and why; fallback "coordinator runs the build after run-create" | Medium |

## Shared Assumptions
| # | Assumption | Source agreement | Impact | Status |
|---|------------|------------------|--------|--------|
| A-001 | The scheduled process can reach the Orca server from cron (PATH, socket, auth) the way an Orca terminal can | Both pick system crontab | High (a schedule that cannot call Orca never builds; sweep then reads a stale or missing ledger) | UNSTATED (both mark only the PATH as UNVERIFIED) [SHARED-ASSUMPTION] |
| A-002 | A listed worktree means active work, and a non-terminal Task means unfinished work. Probe: `run_93bfa00cae2b` is permanently IN because it used the main checkout, which Orca always lists, and it holds 15 stale `blocked` tasks; 6 more Runs are IN on one old `ready` task | Both use the same two rules | High (rule 1 and rule 2 never expire, so the ledger can only grow toward the 62 Runs) | UNSTATED [SHARED-ASSUMPTION] |
| A-003 | One rebuild is a consistent snapshot: Runs, tasks, workers and worktrees are read over about 26 s while workers start and worktrees are removed | Both read sequentially without a snapshot | Medium (a Run can flip between reads; the next build repairs it) | UNSTATED [SHARED-ASSUMPTION] |

## Summary
- Total structural differences: 2
- Total content differences: 11
- Total contradictions: 0
- Total unique contributions: 3
- Total shared assumptions surfaced: 3 (UNSTATED: 3, STATED: 0, CONTRADICTED: 0)
- Highest-severity items: C-001, C-006, A-001, A-002
