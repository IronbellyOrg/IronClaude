# Analyze report: src/superclaude/cli/issue_watch (architecture, quick)

Master f2894fc44, 2026-11-24. Codegraph: index_state=fresh, checked_at=2026-11-24T22:22:19Z; degraded: none

## Layout

15 modules, 6965 lines. Largest: cycle.py 1544, github.py 1158, record.py 865, dispatch.py 522, cli.py 518.
Layering: github.py (all gh argv, read-only) and runner.py (subprocess) at the bottom; record.py (store, lock, schema) and audit.py (REASON_TABLE, log lines) in the middle; cycle.py (one poll cycle, `status_report`, `slo_numbers`) above them; dispatch.py (`run-all` sweep, loop cap, account wait file) and cli.py on top; first_run.py, repo_init.py, generate.py for setup.

## Findings (all verified by Read or Grep)

| # | Severity | Finding | Evidence | Touches |
|---|---|---|---|---|
| 1 | Medium | The throttle wait is not a growing wait: `rate_limit_wait` returns Retry-After, else x-ratelimit-reset, else now + 3600 s. It has ONE production caller, `_login_step`; every other throttled read takes the fixed clamp through `_rate_stop`. No streak is stored and nothing clears `next_permitted_at` after a good cycle (only `reset --rate-limit`). | github.py:469, 511-524; cycle.py:692-697, 778-791; record.py:724-730 (callers confirmed with codegraph_callers: `_login_step` plus 3 tests) | W4 (#812) |
| 2 | Medium | The 5-minute tick is an assumption in code: LOOP_CAP_S 270 and CHILD_TIMEOUT_S 255, so a sweep can run 525 s, and `flock -n` skips the next tick. Nothing in the package holds an interval; the schedule lives only in the image's cron line (read on this host: every minute, "managed: rewritten on every boot"). | dispatch.py:54-55, 468-470; `crontab -l` | W3 (#811) |
| 3 | Medium | `status_report` returns healthy, age, disabled_since, next_permitted_at, counts, day_cap_used, stale, retry. No interval, no last_sweep_at (NFR-04 not built), and it does not read the audit log. | cycle.py:1416-1418, 1464-1473 | W3, W6, W8 |
| 4 | Low | `slo_numbers` is the only code that reads audit lines and has no production caller (5 callers, all tests). No reader of `audit.jsonl` plus the cron log exists. The three items W6, W8, W12 all need one. | cycle.py:1497; codegraph_callers slo_numbers | W6 (#814) |
| 5 | Low | Names outside REASON_TABLE appear in the cron log: `list_failed`, `list_timeout`, `unreadable_list` (repos.py:85-124) and the sweep lines `sweep: error ...`, `sweep: unhealthy` (cli.py:418-423). A scan that demands "a name from the reasons table" flags them. | repos.py:85-124; cli.py:380-425 | W6 |
| 6 | Low | Store schema is closed: StoreDoc has an exact key set and SCHEMA_VERSION 1 with an empty MIGRATIONS table, so a stored throttle streak needs a schema bump or a side file like `account-rate-wait.json`. | record.py:31, 120-131; dispatch.py:60, 243-266 | W4 |

## Architecture notes

- Read-only boundary (NG-2) holds: github.py and cycle.py write nothing to GitHub. None of the three items needs a GitHub write.
- Each of the three items adds code in a different layer: W3 in dispatch/cli (plus the Coder image), W4 in github/cycle/record, W6 as a new read-only script over audit.py outputs.

## Recommendations

1. W3: do not add an interval setting inside this package until the image cron line is the thing that reads it; report the interval in `status` only if the owner wants it.
2. W4: if built, keep the header value, add a floor of about 60 s, store a streak in a side file, clear it on a good cycle.
3. W6: build as one read-only reader shared with W8 and W12.

No source file was changed.
