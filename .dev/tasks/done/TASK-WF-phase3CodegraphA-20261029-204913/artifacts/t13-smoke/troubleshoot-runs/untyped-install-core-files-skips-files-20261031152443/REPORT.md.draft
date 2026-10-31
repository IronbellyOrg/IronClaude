# Troubleshoot Report
**Target**: install_core_files skips files
**Type**: auto
**Tier reached**: 1
**Confidence**: 0.30 (conditional incident explanation; not confidence in source transcription)
**Status**: partial
**Escalation reason**: none (quick depth caps actual escalation)
**Test is wrong**: false
**Behavior is documented**: false (incident not observed)
**Doc context card**: .dev/troubleshoot/untyped-install-core-files-skips-files-20261031152443/doc-context.md
**Date**: 2026-10-31T15:24:43Z
## Summary
No unique cause is established for the reported run: no command, skipped filenames, force argument or output was supplied. The source explicitly preserves existing targets when force is false. Obtain the original invocation and complete result before treating this as a defect or authorizing overwrite.
## Documentation Context
- docs/getting-started/installation.md:263 documents force as overwrite.
- tests/cli/test_how_we_work_install.py:53-75 pins preservation without force (read, not run).
- No restrictions overridden; no edits proposed.
- Card: doc-context.md. Discovery degraded: native fallback, workers unavailable.
## Diagnosability Context
Verdict: partial. Complexity: trivial. Captured failing-run bytes: n/a.
The returned message lists skipped names and the CLI echoes it, but no original capture is available. Full card: diagnosability-context.md. Pending measurements: diagnosability-tasklist.md (round 1 of 3).
Execution locus: execution-locus.md. Original process/host unknown; OBSERVE-VIA=nobody; re-run permitted=unknown. No probe executed; verdict_source=null.
## Diagnosis
**Root cause**: UNDETERMINED — producer menu unavailable.
**Cause class**: Other: intentional preservation branch is a conditional explanation, not a proven incident cause.
**Falsifiers**:
- Core capture: pending, no original command/arm or readable run transport. True prediction: reported file appears under skipped with force=False, consistent with the branch, not confirmation. False prediction: unknown because alternatives are not identified. Same-run force=True plus this function's skipped message refutes the branch explanation; incomplete data is inconclusive.
- Core control: pending, no passing arm or execution proof. True/false predictions unknown because no passing arm is identified; mapping inconclusive. comparator=none.
No rows ran this round. Source inspection is not a failing-run observation. root_cause_summary is empty.
## Evidence
1. src/superclaude/cli/install_core.py:29: `target_path: Path = None, force: bool = False`.
2. src/superclaude/cli/install_core.py:66-68: `if dest_file.exists() and not force:` appends the name to skipped and continues.
3. src/superclaude/cli/install_core.py:83-88: message identifies existing-file skips and lists their names.
4. src/superclaude/cli/install_core.py:100: `success = len(failed) == 0`; skipping alone is not failure.
5. src/superclaude/cli/main.py:178-179: install passes force and echoes the returned message; main.py:365 passes force=True for update.
6. tests/cli/test_how_we_work_install.py:53-75: existing-file preservation regression test, execution state not-run.
7. docs/getting-started/installation.md:263: force is documented as overwrite existing files.
## Proposed Fix
No causal fix established. Obtain the original command, arguments, complete skipped-files output and one affected filename. Do not change the default protection or apply overwrite merely to silence this message. No implementation or remediation chain authorized.
## Risk + Rollback
No production changes, installer runs or tests performed. Overwrite can discard customized files; original user content must be reviewed and preserved before any separately authorized overwrite. No production rollback needed.
## Grounding Gaps
- No provenance-bound failing-run output; observation_paths is empty. No unique incident cause, test defect or documentation defect established.
- Auggie connection failed; native definition/caller/documentation searches used instead.
- Selected project diagnostic worker has tools beyond the loaded protocol's closed roster; documentation and observability branches unavailable. No branch results fabricated; parent fallback only.
- Hypothesis formed inline; independent calibration and evidence validation are separate gates.
- Producer enumeration has zero rows because no exact emitted value was supplied; no invented producer menu.
- No external primitive-behavior claim used as incident proof; local defining source body read directly.
## Next Steps
- Core capture: supply the existing original command, force argument and complete result, linked to one run and affected filename. Matching false-force/skipped output is consistent only; true-force/skipped output refutes this branch explanation; absent/incomplete output stays inconclusive. The report stays `partial` until capture provides enough provenance-bound data to distinguish the relevant explanations.
- Core control: retain pending, no identified passing arm or execution proof; predictions and mapping remain unknown/inconclusive. No new run is requested or authorized.
- Linked enabling task: preserve the original returned message or terminal transcript at the invocation site, without editing production logic. Verify actual names/arguments, not expected values; no instrumentation applied and no rollback needed.
## Audit
Hypothesis: tier1-hypothesis.md. Calibration: tier1-calibration.md. Observation record: tier1-observation.md (no captured output). Producer inventory: producers.md. Evidence validation: evidence-validation.md. Audit log: audit.log. Tier 2 and remediation not invoked; quick depth is the escalation ceiling.
## Pipeline Hardening Closure
Applicable: false. Closure verdict: not_applicable. Waiver status: none. Backtest status: not_run. Off-path review: not_required.
No pipeline escape or boundary change has been established or proposed. This is not a runtime correctness or pipeline-health signoff.
| boundary_type | producer | transformers | consumer | evidence_source | risk | decision | rationale |
|---|---|---|---|---|---|---|---|
| CLI/subprocess | install_core_files | returned message | install CLI echo | src/superclaude/cli/main.py:178-179 | Source explanation could be mistaken for actual run evidence | not_applicable | No subprocess defect or caller/return mismatch observed; report retains unknown cause and requires original output |
| file-stdin-prompt | source Markdown | explicit preserve/copy branch | target files | src/superclaude/cli/install_core.py:54-74 | Assuming copied contents without execution | not_applicable | No delivery escape or boundary change established; preservation condition only read, no runtime or remediation claim |
No hardening evidence cards emitted; known_escapes_caught=[]; no authorization refusal claimed.
