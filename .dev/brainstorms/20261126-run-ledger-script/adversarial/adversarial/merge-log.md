# Merge log

Base: variant-2-sonnet-refactorer.md. Donor: variant-1-sonnet-architect.md. Plan: refactor-plan.md. Date: 2026-11-26.
Output: /home/coder/workspaces/worktrees/IronClaude/run-ledger/.dev/brainstorms/20261126-run-ledger-script/adversarial/merged-output.md (157 lines, limit 230).

## Per-change log
| # | Change | Status | Where applied | Source |
|---|---|---|---|---|
| 1 | Hook delivered (replaces "drop it") | applied | Hook / Design | V1 Q7 |
| 2 | Hook test and drop rule, one scratch Run | applied | Hook / Payload test and drop rule; Open decisions 2 | V1 Q7 + V2 fallback |
| 3 | `superclaude sweep ledger` subcommand, `--add`, `sweep/ledger.py` | applied | Code layout; all `run-ledger` command names replaced | V2 + #895 |
| 4 | Lock and merge | applied | Concurrency and write method | V1 Q3/Q4 |
| 5 | 24 h `new` fallback | applied | Inclusion rules; test added | V1 Q5 |
| 6 | Guards, guard 4 clause, `--accept-empty`, no shrink guard, ceiling | applied | Failure rules; Risks | V2 + V1 clause |
| 7 | Exit codes 0/1/2/3 with stderr prefixes | applied | Failure rules | V2 + lock |
| 8 | Schedule and hook registration doc for Coder#545 | applied | Schedule and install notes doc | V2 + V1 + #895 |
| 9 | Cron reaches Orca, pre-install check, `find_orca` | applied | Pre-install check; Code layout; Failure rule 1 | V2 evidence |
| 10 | Stale-candidate report, no cutoff, measured 10 of 62 | applied | Inclusion rules; schema counts; Open decisions 1 | diff A-002 |
| 11 | Runs universe from `run-list` only | applied | Inclusion rules | V1 |
| 12 | Tests (10 base + 12 added) | applied | Tests | V1 test plan |
| 13 | Sweep reads ledger, 90 minute stale header | applied | Sweep consumption | V2 + #895 |
| 14 | Sweep docs and skill text, `make sync-dev` | applied | Sweep consumption (last bullet) | #895 |

"Changes NOT being made" respected: no package, show/path/--timeout/--no-ledger/sweep --ledger, no `~/.superclaude` path, no 20% guard or five exit codes, main checkout not excluded (all listed under Out of scope).

## Judgement calls (not literal plan text)
- `--add` on a missing or unreadable ledger: the plan is silent; spec says write nothing, exit 1 `implausible:`, first build catches the Run via the 24 h fallback.
- Schema: added `source`, `added_at`, `counts`, `main_checkout_only`, `stale_open_tasks_only` and reason `hook_added` as the minimum that Changes 4 and 10 need.
- `test_new_run_in` no longer says "no previous ledger skips the rule" (contradicts Change 5); a separate 24 h test was added.
- Fixture folder `tests/run_ledger/fixtures/` and the 50-page cap (V2's figure) kept; hook log name `run-ledger-hook.log` taken from the plan.
- The unshortcut rebuild time (26.1 s) replaces the base's 15-25 s estimate; the plan's "about 26 s" lock-free read phase uses it.

## Validation
1. Heading hierarchy: H1, then H2 sections, H3 only under Hook (Design, Payload test); no gaps. PASS.
2. Internal references: "see next section", "Pre-install check", "Open decisions", "Concurrency", "Failure and implausible-result rules" all resolve to existing H2 sections. PASS.
3. Contradiction re-scan: no `superclaude run-ledger` command name (only file/test/script names `run-ledger.json`, `run-ledger.lock`, `run-ledger-record.sh`, `tests/run_ledger/`); no "3 hours" (90 minutes everywhere); hook is delivered, dropped only if the id is absent. grep checked. PASS.
4. Provenance comment present on every H2 section and the header. PASS.

## Counts
Planned 14, applied 14, skipped 0, failed 0.
