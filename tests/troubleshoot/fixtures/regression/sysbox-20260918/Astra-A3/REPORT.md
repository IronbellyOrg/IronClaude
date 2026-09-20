---
status: partial
tier_reached: 1
confidence: null
calibration: not_run_diagnosability_hard_stop
diagnosability_verdict: insufficient
diagnosability_hard_stop: true
---
# Astra retry3 — internal seed runner and separate pre-live failure

2026-09-18. Actual sc:troubleshoot and mandatory sc-troubleshoot-protocol invocations used --depth deep --type deployment and this output directory. Diagnosis remains partial; no probability assigned to an unformed production hypothesis. Separate owner implementation authorization remains in force; no approval/task-builder prerequisite is asserted.

> Your hypothesis depth was constrained by insufficient evidence. No production fix or unchanged collector rerun is justified by the captured evidence.

## Summary

The known failure class is the INTERNAL seed runner's `runner-unavailable`, not an unavailable GitHub Actions runner. Several distinct setup, clock, process-identity/session, control-channel and worker-result failures collapse into this class. Existing evidence identifies neither the failed branch nor relevant child exit. Separately, DinD/blank failed the T51 invocation after disposition and collector fixtures passed; its failed row or abnormal-exit boundary was not retained.

## Documentation Context

Release grounding distinguishes non-blocking startup completion from positive public checkout. Identity-verified signals, finite fail-closed deadlines, repository preservation, no personal PAT dependency and secret-safe reporting remain mandatory. Documentation freshness limitations are recorded in doc-context.md, not upgraded to proven currency. Three independent documentation branches ran in parallel.

## Diagnosability Context

Wave1.6 verdict insufficient; non-trivial; hard-stop true; round1/3. S6: suppressed internal output has no retained branch-specific higher-level error. Uncollected streams are unknown-sized, not measured zero. Complexity: multi-file surface and concurrent supervisor/worker/watchdog/adapter timing; this is not a claim of a race root cause.

Missing internal evidence: exact setup/time/proc/ownership/handshake/result branch; relevant child exit and stage timings. Private channels are cleaned. Final enum and later DNS/HTTPS booleans cannot recover those transient facts. No verified invocation-only instrumentation currently recovers them. The tasklist records constrained capture requirements, not a working patch.

## Grounded source map

The detailed exhaustive map is in tier1-observation.md. Distinct paths include dependency/uptime parsing, temporary-directory/control-file setup, initial PID/parent/starttime identity, process-group/session handshake, go-channel creation, ongoing identity or clock failure, malformed/missing result, child/adapter failure and watchdog/cleanup interactions. Adapter exit27 maps to runner-unavailable; not every adapter failure is propagated into the final seed outcome. No exit171 exists in these production files:171 is the PR number.

The original artifact10564836537 records runner-unavailable / section8fail, later DNS/HTTPStrue, checkoutdir/toplevelfalse. These are runtime observations, not proof of any specific earlier predicate. No F08_RERUN witness exists; pre-rerun seed assertion can fail before actual startup invocation. Existing cleanup/ownership guards must not be weakened to make this pass.

## Evidence — independently validated

1. `.github/workflows/coder-ci-validate.yml:200` invokes `bash .github/contract-tests/test-51-selector-onboarding-wiring.sh >/dev/null 2>&1` under a failure branch; next line emits the generic pre-live error.
2. `/tmp/sysbox-pr171-retry2-dind-blank-failure.log:253` records disposition PASS; line258 collector-fixtures=pass at18:25:36; line259 generic pre-live error at18:36:04. This conclusively identifies the T51 invocation, not its failed assertion or timeout cause.
3. `.github/contract-tests/test-51-selector-onboarding-wiring.sh:63` defaults RESULT_FILE to `artifacts/test-51-evidence/test-51-selector-onboarding-wiring.txt`; line90 writes typed rows; lines106–118 copy/finalize on EXIT. Successful finalization in this invocation is unproven.
4. Read-only gh API run35377326118 artifact inventory returned11 unexpired artifacts. Original DinD/blank debug10561189917 and provenance10562190233 were downloaded privately. Debug zip contains only failure-diagnostics.txt83bytes; provenance zip only validation-provenance.json651bytes. Neither contains original T51 rows. No raw logs were copied to repository/public artifacts.
5. Git diff from failinga9d3af8 to current HEAD found no workflow/T51 source changes. Passing source tests on other jobs do not identify this invocation's failure or prove a new regression.

Validator abcde89049bd91643 re-read all cited source/private-log ranges;3 verified,0 dropped;3 command records passed through without re-execution. Partial retained. Detail in evidence-validation.md. Source map remains separate pre-hypothesis grounding, not a calibrated causal diagnosis.

## Next action and disposition

No source edit, commit, push or new CI run in retry3. Parent's existing revertf39f834 is preserved. No host operations/probes, sibling edits, merges, manual dispatch/rerun or raw-log upload.

Concrete missing evidence:
- A safe branch-specific witness captured DURING the original internal supervisor failure, including which identity/time/channel predicate rejected; later network probes are not a replacement.
- Original T51 failed row or abnormal-exit evidence from DinD/blank job105713899048. Its stdout/stderr and retained artifact inventory do not provide it.

Do not publish another unchanged diagnostic retry. A narrower observation change must first show how it captures these transient facts with fixed, secret-safe values and preserves process ownership/deadline/cleanup guards. No speculative production repair is offered. Fable's concurrent work may produce that new evidence; no sibling modifications performed.

## Protocol status and artifacts

Wave0/1 grounding completed; three independent Wave1.5 branches and two independent Wave1.6 branches completed. Wave1.6 stop skips hypotheses, calibration, Tier2 and debate even with depthdeep. Wave4.5 was not reached; no hardening closure claimed. Independent evidence validation completed; no Tier3 chain requested. This is an evidence gap, not an authorization gate.

Artifacts in this directory: audit.md, tier1-observation.md, wave1_5-branch-A/B/C.md, doc-context.md, wave1_6-branch-A/B.md, diagnosability-context.md, diagnosability-tasklist.md, diagnosability-rounds.json, REPORT.md.draft, REPORT.md, evidence-validation.md.
