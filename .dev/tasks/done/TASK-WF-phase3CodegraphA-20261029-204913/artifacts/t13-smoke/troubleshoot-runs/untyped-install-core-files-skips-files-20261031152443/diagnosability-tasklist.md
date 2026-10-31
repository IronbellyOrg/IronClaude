# Diagnosability Tasklist
**Issue**: install_core_files skips files
**Verdict**: partial  **Complexity**: trivial  **failing_component**: src/superclaude/cli/install_core.py
**Round**: 1 of 3
**re-run permitted**: unknown  **discriminator-required**: yes  **capability-verdict**: n/a
**branch**: feat/codegraph-adoption  **repro-venue-id**: install_core_files skips files (no repro command supplied)
## Emitter search
emitters-found: 1
already-read-files: 4
usable-capture-routes: 1
Emitter: src/superclaude/cli/main.py:179 echoes the function's message. The function returns its message at install_core.py:101; it contains skipped filenames from lines 83-88. Parent read implementation, caller, test and installation-options document. Eligible route: original CLI terminal transcript or original caller's returned tuple, with command and force argument. It captures the actual skipped list without production edits. No original transcript or log path supplied. No new run authorized: re-run permitted=unknown, OBSERVE-VIA=nobody. Static source and preservation test excluded as failing-run capture channels.
## Discriminator rows
core-rows=2, pack-rows=0, total-rows=2; comparator=none.
No producer base pairs: no exact observed token/menu supplied.
| ID | Role | Claim and observable | True prediction | False prediction | Mapping | Provenance / state |
|---|---|---|---|---|---|---|
| capture | core | Skip branch handled reported file; original command, force value and returned message | File appears under skipped and force=False, per install_core.py:66-68,83-88 | Unknown: other failure mechanisms not identified | Matching inputs/message: consistent, not proof; force=True plus skipped message from same function/run: refuted; missing capture: inconclusive | Original reported run, no command/arm supplied; pending, unobservable transport and unknown permission |
| control | core | Same producer executes in an identified passing arm | Unknown: no passing arm identified | Unknown: no passing arm identified | Inconclusive until a real passing arm and execution proof are supplied | CONTROL-PROOF=unknown; pending, no comparator |
## Bracket
Not triggered: no numeric limit supplied.
## Fix candidate
No causal fix established. No production edits proposed.
## Hard Constraints
Invocation sites only. Additive and reversible. Instrumentation, if later authorized, carries `# Diagnosability-tasklist instrumentation: revert after defect closed.` No execution or overwrite authorized in this run.
## Implementation tasks
### Preserve the original invocation result
Type 4: telemetry/artifact capture at src/superclaude/cli/main.py:178-179, currently `core_success, core_message = install_core_files(force=force)` followed by `click.echo(core_message)`. Linked measurement: capture. Supply the existing original command and unabridged message, or caller's arguments and returned tuple; do not rerun or change production source. If a later authorized dev harness is needed, add capture only there with the required annotation. Verification: actual names and arguments from one identified run, not expected values. Rollback: no instrumentation has been applied.
## Verification
The report stays `partial` until capture contains a provenance-bound original command, force value and complete result sufficient to distinguish expected preservation from a different failure. Control is pending, not an invented passing run. No rows executed.
## Rollback
No changes applied. Remove only any later authorized invocation-site instrumentation after diagnosis.
## Patch-round counter
Authoritative store: .dev/troubleshoot/diagnosability-rounds.json. Branch and venue are the header identity. Locked atomic update returned diagnosability_round=1; same-run snapshot: diagnosability-rounds.json. Incremented once; cap not reached.
