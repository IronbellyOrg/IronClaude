# Pull Request

## Summary

Make failover cover temporary server errors and explicitly named models in tier mode. Preserve immediate streaming: no event look-ahead, no withheld pings, no mid-stream switching, no new body timeout. The issue and worker brief were corrected to remove the rejected streaming requirement before implementation.

## Changes

- Count consecutive 408/429/500/502/503/504 and cut-off error replies per model. Return the first two errors for Claude Code's own retries; the third parks the model and forwards the same request to the next eligible model.
- Temporary parks grow from 5 to 10, 20, 40 and 60 minutes, with a success resetting both count and duration. Existing immediate out-of-usage switches and `Retry-After` behavior remain.
- Named models use their best-position allowed tier (higher tier wins ties), requested model first, respecting context windows. Shared counts and parks apply to both request forms.
- Keep a rotating 5 MB log plus one older copy, with cross-process rotation locking, credential redaction and no request bodies. Remove raw request-URL access logs.
- Add the three failure settings and include them in shim identity. Update README, launcher help and changelog.
- Add failure-first tests and isolated scripted/live end-to-end harnesses under `.dev/issues/392/`.

## Related Issues

Closes #392

## Checklist

### Git Workflow

- [x] Topic branch: `clayphi/ccsession-failover-392`, rebased onto the fork's `origin/master` before implementation.
- [x] Submitted through `/sc:pr-submit --monitor 3 --max-rounds 3` to `IronbellyOrg/IronClaude`.
- Commit uses the conventional `fix(ccsession):` prefix and required attribution.

### Code Quality

- [x] Changes limited to failover, logs, associated documentation and tests.
- [x] Required focused suite: 7,420 passed, 12 skipped, 1 pre-existing failure.
- [x] Final full suite: 24,621 passed, 149 skipped, 2 xpassed, 1 pre-existing failure (#352).
- [x] Final tier suite: 208 passed, 1 pre-existing failure.
- [x] `ruff check .`, `ruff format --check src/ tests/`, shell syntax and `make verify-sync` pass.
- [ ] CI pending on PR creation; monitor 3 will wait for checks and reviewer findings.

### Security

- [x] Credentials read only from the environment; generated source and evidence scanned for actual environment credential values (zero matches).
- [x] Log tests cover request-body exclusion, query/header exclusion, credential echoes, rotation and unwritable paths.
- [x] Shared production shim untouched; only isolated child shims started and stopped.

### Documentation

- [x] README failover, cooldown, named fallback, settings and logging behavior updated.
- [x] `ccsession --help` no longer claims named models have no failover.
- [x] CHANGELOG describes the change and unchanged immediate streaming.

## Testing Methods

Evidence is committed under `.dev/issues/392/`:

- `red.log`: new behavior fails against the unchanged shim before implementation; unchanged forwarding and streaming guards already pass.
- `targeted.log`, `tiers-final.log`, `full-final.log`: required tests and final regression results. `baseline-terminal.log` reproduces #352 against `origin/master`'s shim.
- `full-suite.log`: retained invalid first full run. I edited the shim after pytest collection, invalidating the launch tests' cached code fingerprint and the sync assertion. The full run was repeated with source frozen; `full-final.log` has only the existing #352 failure. `frozen-source.sha256` records the tested shim/model files.
- `e2e/run.py`: runs the real `claude -p` command on separate child shim ports. Scripted tier2 calls: Sol, Sol, Sol, then GLM, with two `api_retry` events from Claude Code. Named Opus calls: Opus then Sonnet, answering OK. An initial streamed error passes unchanged and Claude retries the same model; the shim does not switch it.
- `e2e/*summary.json`, `*-calls.json`, `*-proxy.log`: answers, exact model sequence, failure counts, parks and switches.
- `e2e/live-final-run.log`: live tier2 and named GPT-6.1 Sol answered OK; shared shim identity unchanged. The separate live Opus attempt and unchanged-master comparison show the availability limitation noted below.

The first E2E harness attempt assumed JSON output was one object; the CLI returned an event array. The harness was corrected and all scripted scenarios rerun successfully; the initial failure log is retained.

## Screenshots (if applicable)

Not applicable: local HTTP proxy and CLI behavior.

## Notes

- Known pre-existing local failure: `test_shim_outlives_the_terminal_that_started_it` (#352). It fails at the same assertion with `origin/master`'s unchanged shim; see `baseline-terminal.log`. This PR does not claim the local suite is entirely green.
- The requested live Opus smoke test was attempted: both Opus and Sonnet were out of usage. Unchanged master also returned a 429 for named Opus (`e2e/baseline-live-run.log`). The scripted Opus-to-Sonnet test passed, and live tier2 plus named GPT-6.1 Sol both answered OK. Live Opus success remains unverified because of provider availability, not silently substituted.
- The shared shim on port 4078 remained PID 1601 throughout; test shims used separate ports and were stopped after each run.
- User instruction: no subagents. Local verification was performed inline, not claimed as an independent fresh-context review; the PR monitor waits for external reviews.
- Draft/ready transitions used by the default review-fix merge guard have not been verified against every configured review/workflow integration.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
