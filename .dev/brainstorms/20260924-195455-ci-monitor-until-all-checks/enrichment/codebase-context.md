# Codebase context (Wave 2A)

Source: auggie codebase-retrieval + session PR #237 run. quality_tier: primary.

## Abort paths that stop the wait

| Path | Where | Effect |
|------|--------|--------|
| `HALT_MAX_ROUNDS` | `fsm.py` `should_halt_rounds` at S2 findings; `DEFAULT_MAX_ROUNDS=2` | Wave 8 never starts (SKILL.md: CI phase only after Augment clean / REPORT_ONLY) |
| `TERMINAL_TIMEOUT` | `--timeout` default 600s | wait ends while jobs pending |
| Poller crash | `poll-ci-checks.sh` `as_array` + `--argjson` | no JSON line; Monitor cannot continue |
| False `clean` | `classify_checks`: empty checks → `clean` | if required/all parse as `[]` while jobs exist |

## Already correct

- `classify_checks`: any `bucket=pending` → `polling` (`ci.py`).
- FR-CI-11: `--required` then all.
- Head re-sample after checks (TOCTOU).
- Pending exit 8: do not `|| echo '[]'` on the same stdout.

## Live evidence (PR 237)

- Residual finding `poll-ci-checks.sh:47`: empty stdout → `as_array` empty → `--argjson` fail.
- `gh pr checks` table: several pass, Test 3.10/3.11/3.12 **pending**, exit 8.
- Monitor status: `terminal_max_rounds`, Wave 8 not started.
