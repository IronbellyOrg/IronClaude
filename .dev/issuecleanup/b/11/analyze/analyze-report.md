# /sc:analyze report: src/superclaude/cli/issue_watch (focus architecture, depth quick)

Date: 2026-11-24. Master `f2894fc44`. Read-only; no source changed.
Codegraph: index_state=fresh, checked_at=2026-11-24T22:21:00Z; degraded: none

## Layout (codegraph_files, 15 Python files, 6965 lines)

`cycle.py` (1544 lines, 150 symbols) holds the config loader, `validate_approvers` (:323), the poll cycle, `status_report` (:1400) and the SLO reducer `slo_numbers` (:1497). `launch.py` (416) builds the 12-element launch argv, the retry argv and maps a launch reply to an outcome (`outcome_of` :372). `record.py` (865) is the locked store and its state transitions (`mark_unknown` :599). `generate.py` builds the approvers file. `audit.py` writes `audit.jsonl` (rotates at 5 MiB, :108).

## Findings (architecture)

| # | Severity | Finding | Evidence |
|---|---|---|---|
| 1 | Medium | Any exit-0 launch reply without a recognised operation id is classed `unknown`; both real launches on 2026-11-23 ended that way and no `launched` decision exists, so two of the four SLO numbers are empty | `launch.py:372-395`; `cycle.py:1520-1527`; live `audit.jsonl` |
| 2 | Medium | `slo_numbers` has no production caller (tests only); `status` does not read the audit log | codegraph callers of `slo_numbers`; `cycle.py:1400-1471` |
| 3 | Low | `retry_argv` is printed by `status_report` only; nothing runs it (matches AC-9) | codegraph callers of `retry_argv`; `docs/designs/issue-watcher.md:889` |
| 4 | Low | Launch argv carries no permission flag and a test pins it; the launched session's permission mode is not recorded anywhere | `launch.py:136-157`; `tests/issue_watch/test_security_invariants.py:16` |
| 5 | Low | The generated approvers file already holds every maintainer (multi-approver by design) | `generate.py:233-247` |

Dependency view: `mark_unknown` is reached by `cycle._launch` and `cycle._examine` (codegraph impact); the module is self-contained and read-only toward GitHub except `repo_init.py` (labels).

## Recommendations

Capture Orca's real launch reply and fix the id parse first (finding 1); then the SLO review and any retry follow. See the per-issue findings in `.dev/issuecleanup/b/11/818|819|820/findings.md`.
