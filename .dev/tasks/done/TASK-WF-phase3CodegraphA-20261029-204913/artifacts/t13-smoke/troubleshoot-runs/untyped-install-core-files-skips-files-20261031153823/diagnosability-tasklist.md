# Diagnosability Tasklist
**Issue**: install_core_files skips files
**Verdict**: partial  **Complexity**: trivial  **failing_component**: src/superclaude/cli/install_core.py
**Round**: update unavailable (prior 1 of 3)  **re-run permitted**: unknown  **discriminator-required**: yes  **capability-verdict**: n/a
**branch**: feat/codegraph-adoption  **repro-venue-id**: install_core_files skips files (no repro command supplied)

## Emitter search
emitter-search: n/a (no captured single-expression predicate; actual missing evidence is the incident invocation and result).
emitters-found: 2 direct console sinks, main.py:179 and main.py:366; seven message append sites in install_core.py:79,81,84,88,91,93,98 are construction sites, not independent sinks.
already-read-files: 16 distinct successfully read non-output source/reference files: protocol SKILL.md; triage-checklist.md; troubleshoot-analyst.md; CODEGRAPH.md checkout fallback; install_core.py; doc-discovery.md; test_how_we_work_install.py; main.py; environment-deltas.md; diagnosability-audit.md; installation.md; primitive-differential.md; hypothesis-card-template.md; escalation-rubric.md; report-template.md; agent-assertions.md. Counter store and generated output files excluded from this source/reference count.
usable-capture-routes: 1 technical route: an invocation-site wrapper can preserve the actual returned (success,message) tuple and input force value for the caller's destination without altering production logic. Existing captured incident artifacts could supply the same evidence, but none were supplied.
Production emitters are not eligible edit targets. Existing test invocation at tests/cli/test_how_we_work_install.py:66 is an eligible future harness location, not proof about the incident. Sink access is technically available, but transport to the actual incident and re-run permission are unknown. No capability failure asserted. Emit `preservation-input=unobserved` on absent/error input, never an assumed value.

## Discriminator rows
comparator=none
core-rows=2, pack-rows=0, total-rows=2
No surviving categorical producer rows: no exact/reference producer pair invented. No optional packs.
| ID | Role | Claim | Observable and probe | Value if claim true | Value if false | Outcome mapping | Provenance / state |
|---|---|---|---|---|---|---|---|
| input-policy | core measurement | Reported skip follows the existing-destination / force=False guard | Preserve actual invocation arguments and pre-call destination existence, then reduce conjunction to boolean only if all inputs known | true, from install_core.py:66-68 | unknown: other causes may share the inputs | true: consistent, not confirmed; false: refutes this narrow guard explanation; missing/error: inconclusive | Actual failing venue required; pending, no capture and no transport authorization |
| control | core control | A known-good arm executes the same production call | Supply captured command and verified execution site for a separate known-good arm | unknown: no control provided | unknown: no control provided | Either value alone inconclusive; absent input unobserved | CONTROL-PROOF: unknown; pending, no reference run |
No discriminating falsifier established for the entire incident until actual inputs and returned message are captured. No literal reference-context form is asserted.

## Hard Constraints
Invocation sites only, additive only, reversible. Proposed instrumentation carries `# Diagnosability-tasklist instrumentation: revert after defect closed.` No production edits or automatic execution.

## Implementation tasks
### Preserve actual invocation evidence
Type 2, fixture wrapper, proposal only. Invocation site: tests/cli/test_how_we_work_install.py:66, current code `ok, message = install_core.install_core_files(target_path=target, force=False)`. A future additive harness wrapper may preserve input-policy inputs and the real returned tuple, with the revert annotation. This local harness does not establish the original incident environment; incident access is still required. Linked rows: input-policy, control. Verify capture records real arguments, destination observation errors as unobserved, and the returned tuple without substituting expected output. No task has been applied.

## Verification
Both core rows remain pending. Original incident output, exact command or API call, destination and force value are required. No observation or passing test is claimed. Counter update and execution transport must be available before any counted probe execution.

## Rollback
No instrumentation applied. If the proposed wrapper is later authorized, remove only its added annotated instrumentation after preserving captured evidence. No production file changes.

## Patch-round counter
Authoritative store: .dev/troubleshoot/diagnosability-rounds.json. Read existing branch/venue value 1. Attempted atomic locked update through update-counter.py was denied before execution by session permissions. No increment or snapshot is claimed; prior value remains the last observed value, not this run's round. Existing issue-based venue key retained because no exact repro venue was supplied. Counter transport unavailable: protocol status blocked, skip automatic execution and Waves 1.7-4.5. This is not a rerun refusal and does not set blocked-on-authorization.
