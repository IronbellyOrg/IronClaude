# Diagnosability Context Card

**Issue**: Verified Codex finding on PR #360: a user's "ponytail@ponytail": false opt-out is not carried to "ponytail@ironclaude", so the next install re-enables Ponytail
**failing_component**: src/superclaude/cli/install_user_setup.py (apply_settings_defaults)
**Verdict**: partial
**Complexity**: trivial (score 0: single file, deterministic, no intermittent/perf/security signals)
**Hard-stop fired**: false
**Round**: 0 of 3 (discriminator-required: no; counter not consumed)
**Captured bytes (failing run)**: n/a (audit-time only; the repro stdout is in tier1-observation.md)

## 3-W's coverage

| W | Answerable | Evidence |
|---|------------|----------|
| When  | yes | deterministic: every install/update run; repro in tier1-observation.md |
| Where | yes | the "added" message names enabledPlugins.ponytail@ironclaude (install_user_setup.py:186), reaches stdout (main.py:237, :405) |
| Why   | partial | the message does not mention the existing ponytail@ponytail: false; the repro shows both values side by side |

## Branch A — Log-call inventory

Total: 15 (condensed to 9 in wave1_6-branch-A.md). Types: return-message/print 11, exception_handler 4 (rich 2, minimal 1, silent 1). No logging module. `degraded`: true.

## Branch B — Log-config reachability

Effective level: none (unconditional click.echo). Source: main.py:236-237, :404-405. reaches_sink: 1, filtered_out: 0, unknown: 0. `degraded`: true.

## Sufficiency rubric application

Row fired: none of S1-S3 (no exception); S4 shape (2 yes + 1 partial, reaches_sink) gives sufficient, capped to partial because both branches ran degraded (auggie unavailable). S14 does not apply: the disputed datum (ponytail@ironclaude: true next to ponytail@ponytail: false) is directly observed in tier1-observation.md.

## Implication for diagnosis confidence

Existing signal: the defaults message lists each added key and always reaches stdout.
Gap: it does not show that the plugin was already disabled under its old id.
Consequence: none for this diagnosis; the local repro observed the exact failing state.
Next step: proceed to hypothesis formation; no instrumentation needed.

## Tasklist reference

diagnosability-tasklist.md (informational, verdict=partial; no pending measurement).
