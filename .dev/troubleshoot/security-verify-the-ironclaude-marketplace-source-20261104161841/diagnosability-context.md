# Diagnosability Context Card

**Issue**: Verified Codex security finding on PR #360: install_plugins trusts a registered `ironclaude` marketplace by name and keeps installing Ponytail after a failed marketplace add/update
**failing_component**: src/superclaude/cli/install_user_setup.py (install_plugins)
**Verdict**: partial
**Complexity**: non-trivial (`--type security` override)
**Hard-stop fired**: false
**Round**: 0 of 3 (discriminator-required: no)
**Captured bytes (failing run)**: n/a (audit-time only; repro stdout in tier1-observation.md)

## 3-W's coverage

| W | Answerable | Evidence |
|---|------------|----------|
| When  | yes | deterministic; repro in tier1-observation.md |
| Where | yes | repro command list shows the skipped add (case 1) and the install after a failed add (case 2) |
| Why   | partial | the final message names failures but not the marketplace source or the claude stderr (:363-372 discard it) |

## Branch A — Log-call inventory

Total 13 (7 kept). No logging module; returned messages only; subprocess output captured and discarded. `degraded`: true.

## Branch B — Log-config reachability

Unconditional click.echo (main.py:237, :405). Final message reaches_sink: 1; claude subprocess output filtered_out: 1. `degraded`: true.

## Sufficiency rubric application

Row fired: S4 shape (2 yes + 1 partial, reaches_sink) gives sufficient, capped to partial (degraded). S14 not applicable: the disputed datum (the command list) is directly observed in the repro.

## Implication for diagnosis confidence

Existing signal: the plugin-step message reaches stdout and names failed items.
Gap: no source of the used marketplace and no claude error text.
Consequence: none for this diagnosis; the repro observed both defects directly.
Next step: proceed; naming the mismatch in the message is part of the fix.

## Tasklist reference

diagnosability-tasklist.md (informational; no pending measurement).
