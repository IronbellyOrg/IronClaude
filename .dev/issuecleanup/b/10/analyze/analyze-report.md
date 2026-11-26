# /sc:analyze report: src/superclaude/cli/issue_watch (architecture, quick)

Run 2026-11-24 on branch `ironbelly/Realign` at `f2894fc44`. Target: `src/superclaude/cli/issue_watch` (15 files, 6965 lines). Focus: architecture. Depth: quick. Read-only; no source changed.

Codegraph: index_state=fresh, checked_at=2026-11-24T22:20:08Z; degraded: none (the graph was used only for the file count; findings below were confirmed by Grep and Read)

## Layout

`cycle.py` (1544 lines) holds the poll cycle, `status_report` and `slo_numbers`; `github.py` (1158) holds the `gh` argv builders, `CallBudget` and the rate-limit parsing; `record.py` (865) is the store; `dispatch.py`, `launch.py`, `audit.py`, `cli.py`, `predicates.py`, `first_run.py`, `repo_init.py`, `repos.py`, `runner.py`, `generate.py`, `defaults.py`.

## Findings relevant to issues 815, 816 and 817

| # | Severity | Finding | Evidence |
|---|---|---|---|
| A1 | Medium | The poll has no credential seam: every `gh` call inherits the process environment and the `gh` login. A narrower token (issue 815) needs only an environment value, not a code path, unless `check-config` must verify scopes. | `runner.py:67-75` (`SubprocessRunner.run`, no `env=`); argv builders at `github.py:250,256,279,313,348` all start with `gh` |
| A2 | Medium | `status` reads only the store. The audit log has an appender and no reader, so "three bad cycles" (issue 816) has no input today. `slo_numbers` (`cycle.py:1497`) also has no production caller. | `cycle.py:1400-1422` (docstring: "`audit` is accepted for the fixed signature and not read"); `audit.py` has append and rotate only |
| A3 | Low | The existing stale rule already trips after three missed cycles. `last_completed` is set only when the cycle exit is 0 and there is no stop reason, so three failing cycles in a row push the age past `HEALTH_AGE_S = 900` and `status` exits 1. | `cycle.py:45`, `cycle.py:1233-1234`, `cli.py:182-197` |
| A4 | Low | Exit 1 is shared between "unhealthy" and "crash", and 6 means store unreadable; a new alert exit must avoid 1, 6 and 75. | `cli.py:36-40` |
| A5 | Medium | The call budget counts every call made, so a conditional read that returns 304 would still count (issue 817's "gh_calls falling" check cannot pass by itself). Reads are a mix of GraphQL (no ETag) and REST. | `github.py:49-53`, `github.py:530-560`; `github.py:256-296,313-340` |
| A6 | Low | Header-driven rate-limit waiting already exists, so W4 and W9 both touch the same reply handling. | `github.py:474-491,511-521` |

## Recommendations

1. 815: keep dormant until its trigger; first record where the launched claim session gets its token (A1).
2. 816: build one audit-log reader shared with the shadow-run check (issue 814) and the SLO review (issue 820); pick a new exit code (A4); say that the stale rule covers the common case (A3).
3. 817: rewrite its acceptance check so it does not rely on `gh_calls` falling (A5); keep it behind measured evidence together with issue 812.

## Metrics

Files 15; lines 6965; largest module `cycle.py` 1544 lines. No dynamic analysis run.
