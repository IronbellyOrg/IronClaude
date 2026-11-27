---
topic: "the best approach to the Run ledger script and its setup, as described in Coder issue 545"
domain: code
strategy: systematic
depth: quick
proposals_target: 2
handoff_target: none
created: 2026-11-26T17:30:00Z
---

# Seed Brief: run-ledger-script

> Source correction (coordinator, 2026-11-26, after Wave 3 started): the source issue is IronbellyOrg/IronClaude#895 (https://github.com/IronbellyOrg/IronClaude/issues/895); Coder#545 now covers only the 30 minute schedule and hook registration. #895 adds: preferably a `superclaude sweep` subcommand, hook file delivered by `superclaude install`, stale-ledger warning at 90 minutes, result file `.dev/issues/895/result.md`. See refactor-plan.md for how each was applied.

## Problem Statement
The coordinator's periodic sweep (`/sc:sweep`, WC-16) needs Orca Run ids via `--run` and fails with "no Run bound: pass --run <id>". Orca keeps all 63 Runs forever, has no Run delete and no open/settled status. Sweeping all Runs took 48.6 s and a 3,666-line report; one Run took 3.5 s. A date window was rejected by the owner: a Run counts only if it has active work.

## Known Context
- Dialogue answers come from Coder issue 545 (non-interactive run); no person was asked.
- Chosen approach in the issue: a deterministic script (uv run, no model) rebuilds a Run ledger from scratch every 30-60 minutes. A Run is in when one of its workers used a worktree Orca still lists, or it has an unfinished Task, or it was created since the last build. `run_legacy_local` always out. Any Orca failure or implausibly empty result keeps the old ledger and exits non-zero. The sweep reads `--run` ids from the ledger only. Plus a PostToolUse hook on `orca orchestration run-create` and `worker-start` that appends a new Run id at once.
- Measured: Orca list calls take about 0.18 s each; `worker-list` pages at 100 rows (8 pages); of 63 Runs 53 have workers, 155 worktrees ever used, 152 gone; 3 Runs have live work.
- Code facts are in `enrichment/codebase-context.md` (sweep CLI and its pinned Orca allowlist, hook pattern, CLI shapes).

## Constraints
- UV only; edit under `src/superclaude/`, then `make sync-dev`; never stage `.claude/`; no hardcoded `src/superclaude/` paths inside installed primitives.
- Do not run `orca orchestration reset`, delete a Run, edit `~/.claude/settings.json`, install a crontab or schedule anything. Hook and schedule are delivered as files plus install instructions; the owner gives a go before install.
- No Orca link flags (`--issue`, `--pr`). No commit unless the owner says so.
- Sweep skill may only run `superclaude sweep run`; sweep's Orca allowlist does not include `run-list`.

## Success Criteria
- Rebuild script with a regression test covering: live-worktree Run in, deleted-worktrees-only Run out, unfinished-Task Run in, newly created Run in, `run_legacy_local` out, Orca failure keeps the old ledger.
- Run once against real Orca: ledger written, rebuild time reported; a sweep over the ledger runs without "no Run bound" and its time is reported.
- Hook tested for what `run-create` gives it, then delivered as a file or dropped with the reason written down.
- Scheduling decision recorded; nothing installed.

## Open Questions
1. Where does the code live: a new `superclaude run-ledger` command group, or a standalone script? How is it installed and run by a schedule?
2. How does sweep consume the ledger: a new `--ledger`/default in `superclaude sweep run`, or the coordinator expanding ledger ids into `--run` args (sweep skill is restricted to one command)?
3. Where does the ledger file live: `.dev/coordinator/` in one worktree (issue's proposal) or a fixed per-user state path that a hook firing in any worktree can reach?
4. Concurrency: the hourly rebuild and the hook both write; how to keep appends from being lost (lock plus atomic rename)?
5. Exact definitions: unfinished Task statuses; matching worker `resource.worktreeId` to `worktree list` ids; what counts as an implausible empty result; pagination of worker-list.
6. Scheduling that survives a session restart: Orca automation, system crontab, or session-only cron. Which one to recommend and ship as a file?
7. What a PostToolUse hook receives from `run-create` (is the Run id in the output?). Needs a test.

## Enrichment Context
See `enrichment/codebase-context.md`. Key facts: sweep's Orca allowlist excludes `run-list` (so the builder is separate); the sweep skill may run only `superclaude sweep run`; `worktree list --json` ids look like `<repoId>::<path>`; `run-list --json` has no status field.
