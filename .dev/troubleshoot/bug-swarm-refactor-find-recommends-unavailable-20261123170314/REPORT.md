# Troubleshoot Report

**Target**: Issue 501: swarm refactor-find suggests an unavailable follow-up
**Type**: bug
**Tier reached**: 1
**Confidence**: 0.92
**Status**: blocked
**Escalation reason**: none
**Test is wrong**: false
**Behavior is documented**: false
**Doc context card**: doc-context.md
**Duration**: 1471 seconds through final evidence review
**Date**: 2026-11-23T17:27:45Z

## Summary
Repair acceptance is NOT PROVEN because this run was explicitly diagnosis-only: no source fix, new regression test or repaired-state replay exists. The defect itself is reproduced: the fresh-run CLI emits an unavailable downstream command and a literal placeholder mixed into the real report-file list. The supported candidate for later consideration is the existing adversarial comparison command with only actual successful reports, not an automatic source-editing command. No product changes, commits, pushes, issue comments or paid reviews occurred.

## Documentation Context
- Relevant refs: docs/dev/lens-contribution-policy.md, docs/swarm/lens-catalog.md; historical post-release finding in doc-context.md.
- Documented contract requires real commands and supported arguments; the catalog repeats the defect, not overriding that rule.
- Preserve experimental status, suspect=False, report contents and suggestion-only behavior; no restrictions overridden.
- Full context: doc-context.md; raw discovery: wave1_5-branch-A.md, wave1_5-branch-B.md, wave1_5-branch-C.md.

## Diagnosability Context
**Verdict**: partial
**Complexity classification**: trivial
**Captured-bytes (failing run)**: execution-log.jsonl 1559; return-contract.yaml 4221.
The event log does not include the recommendation, but the full YAML result captures it directly; no missing disputed datum remains. No hard-stop fired and no additional instrumentation was proposed. Detailed cards: diagnosability-context.md and diagnosability-tasklist.md (informational; zero pending measurement rows).

## Diagnosis
**Root cause**: The refactor-find handoff template is stale, and the shared fresh-run file-list builder adds a literal input that the proposed consumer cannot read.
**Cause class**: Other: downstream handoff contract mismatch.
The lens defines the unavailable namespaced command. The CLI inserts an external-review placeholder before actual successful files, and reduction faithfully formats/persists that value without validating command availability or the complete argument list. A name-only replacement would leave the bad input in place. The real CLI stub run reaches generation/emission and reproduces both facts; it does not prove a repaired handoff.
The catalog duplicates the stale recommendation. Existing lens validation and the cited tests check different properties, so their passing result does not refute this defect. Independent calibration was 0.92 and stopped the investigation at its first tier, with no competing-hypothesis fan-out.

## Evidence
1. `src/superclaude/cli/swarm/lenses/refactor_find.py:53`: `recommended_next_command_template=("/sc:code-review --apply {compare_files}")`.
2. `src/superclaude/cli/swarm/commands.py:2141-2143`: compare_files defaults to `",".join(["<existing-review>", *succeeded_final_paths])`. Lines 2145-2157 pass the template and substitutions to the real reducer.
3. `src/superclaude/cli/swarm/reduce.py:672-697`: the formatter result becomes `recommended_next_command=rendered_next`; lines 701-702 emit it. The actual captured `stub-run/return-contract.yaml:64` contains the absent command, literal prefix and three absolute final report paths.
4. Captured read-only local reducer inspection: `packaged_command_exists=False`, `installed_command_exists=False`. Captured input inspection: `literal_existing_review_present=True`, `successful_report_count=3`, `all_reports_readable=True`, `candidate_input_shape_valid=True`. Exact provenance/output spans are in tier1-observation.md; original full generated command is preserved in stub-run/return-contract.yaml, not reconstructed here.
5. `src/superclaude/commands/adversarial.md:15,39` declares comma-separated 2-10 existing file inputs; installed `/home/coder/.claude/commands/sc/adversarial.md:15,39` matches. Active `/home/coder/.claude/skills/sc-adversarial-protocol/SKILL.md:60-62` requires existing readable files. This verifies the declared candidate interface, not execution of that skill.
6. `docs/dev/lens-contribution-policy.md:287-292` says the downstream command MUST exist; lines 317-334 require compatible substitutions/flags. `docs/swarm/lens-catalog.md:25,49` repeats the stale follow-up and would need a coordinated correction.
7. `src/superclaude/cli/swarm/lenses/_validate.py:603-609` enumerates six checks with no shipped-command availability check. `tests/swarm/test_bundled_lenses.py:119-122` checks nonempty template; `tests/swarm/test_reduce.py:305-314` tests interpolation using fictional /sc:foo.
8. Command: `uv run superclaude swarm run --lens refactor-find --target src/superclaude/cli/swarm/lenses/refactor_find.py --output .dev/troubleshoot/bug-swarm-refactor-find-recommends-unavailable-20261123170314/stub-run --transport stub` exited 0 and printed `swarm run: dispatched job (mode=lens, workers=3, results=3)`.
9. Command: `uv run pytest tests/swarm/test_bundled_lenses.py tests/swarm/test_reduce.py -q` exited 0: `76 passed in 0.92s`. These are existing tests, not a newly added reproducing regression.

## Proposed Fix
Diagnosis-supported proposal only, NOT an instruction to apply a fix from this blocked report. For refactor-find, use the existing adversarial comparison interface with the successful real final reports only, without the external-review placeholder. Preserve explicit caller-supplied substitutions and sibling handoffs. A default list outside the consumer's 2-10 file range must not be presented as an executable comparison. Preserve suspect=False; {suspect_files} is not a valid shortcut for this lens.
**Files that would change if separately authorized**: src/superclaude/cli/swarm/lenses/refactor_find.py (template), src/superclaude/cli/swarm/commands.py (refactor handoff arguments), docs/swarm/lens-catalog.md (duplicate text).
**Tests required before acceptance**: focused regression in existing swarm test conventions that fails on the current missing command and invalid file list, passes after repair, checks full command/flags/readable inputs/count, excludes the placeholder, preserves explicit overrides and sibling behavior, and covers too few/many default inputs. No test has been added in this diagnosis.
More than one source file is involved, so any later authorized implementation needs the guide's written-plan route. No automatic planning, implementation or repeated diagnosis is launched here.

## Risk + Rollback
A global change to the shared file list could change bare-review/reflect handoffs. The replacement compares reports; it must not silently apply source refactors. Current baseline coverage passes while the defect remains, so it is not enough for repair acceptance. There is no product patch to roll back; retain diagnostic artifacts. The environment gained a gitignored .venv and test caches during permitted local checks.

## Follow-up tasks
None proposed outside this issue. Separate resume behavior was traced to classify the shared reducer consumer, not repaired or certified.

## Grounding Gaps
- No repaired source, new failing-before/passing-after regression or positive repaired-state CLI replay. This causes the repair-closure blocker, not uncertainty about the captured stale string.
- Downstream adversarial execution, paid/model-backed review and the original reporter environment were not run. Candidate syntax/input shape only were checked.
- Failed-worker acceptance, arbitrary path quoting and override edge cases await future authorized tests; none are claimed as passing.
- Release search found no governing PRD/TDD at the requested current/complete paths; historical finding was retained. Branch C recovered two EACCES searches by direct Read and scoped Grep. Initial audit Edit was refused by the freshness hook, then retried after Read.
- No historical pipeline-escape replay suite ran; known escape coverage is not claimed.
- Independent validation skipped inapplicable assertions for absent source diff, competing-hypothesis index and reference-arm probe rows; these were not silently passed. Minor namespace/policy-path notes are preserved in evidence-validation.md, not converted into out-of-scope fixes.

## Next Steps
Review this diagnosis together as the guide's next step. The external prerequisite for repair acceptance is a separately authorized implementation with a new failing-before/passing-after regression and a positive production-entrypoint replay; this diagnosis-only run cannot provide those. Keep the hardening blocker visible in any later plan and do not treat baseline test success as repair sign-off.
The informational diagnosability tasklist has zero pending measurement/enabling rows; no instrumentation or automatic diagnostic rerun is needed. No --fix offer, automatic remediation, commit, push, issue post or PR is authorized by this report.

## Audit
Hypothesis: tier1-hypothesis.md. Independent calibration: tier1-calibration.md (0.92, STOP). Callers: tier1-callers.md. Actual evidence: tier1-observation.md and stub-run/. Discovery and observability branch reports remain on disk. Audit log: audit.log. No Tier 2 debate or Tier 3 plan was invoked.
Independent evidence validation: evidence-validation.md. Binary PASS for diagnostic evidence: seven source/artifact evidence groups verified, two command groups passed through without re-execution, zero dropped citations. No structural assertion fired; skipped inputs are explicitly recorded. Its suggested citation-check success is merged with the prior blocked repair-closure status, never replacing it.

## Pipeline Hardening Closure
**Applicable**: true
**Closure verdict**: blocked
**Waiver status**: latched (missing mandatory repaired-state proof, not a human waiver)
**Backtest status**: not_run
**Off-path review**: performed (independent validator consumed actual runtime evidence and four boundary cards)

**Wave statuses**:
- HC0 Applicability + Boundary Scan: PASS; generated command/file-list boundary applies. See hardening-applicability.md.
- HC1 Runtime-Entrypoint Verification: FAIL for repair closure; original CLI reproduced defect, but no fix-applied positive witness exists.
- HC2 Contract Enumeration: PASS for bounded discovery; live producer/transformer/consumer paths inventoried, fresh-run path observed.
- HC3 Unmask + Sweep: N/A with rationale; no generated-prose phase/status grammar is changed. Sibling source family inventoried; repaired behavioral fixtures remain unproved.
- HC4 Effective-Input Proof: N/A for indirect Git selection; explicit captured artifact paths are used and tracked source is unchanged.
- HC5 Off-Path Reviewer + Waiver: PASS for independent diagnostic review, received in evidence-validation.md. Does not clear HC1 or authorize source changes.

**Evidence cards**: runtime-entrypoint.md; contract-ledger.md; unmask-sweep.md; effective-input.md. Paths resolve next to this report.
**Known escapes caught**: None claimed.
**Closure blockers**:
- NOT PROVEN: failed hardening wave HC1.
- NOT PROVEN: mandatory repaired-state runtime proof absent.
The blocked closure verdict follows priority 2 of the governing hardening truth table; confidence and existing passing tests cannot override it. This is not blocked-on-authorization: the authorized local diagnosis ran, and no required diagnostic rerun was refused.
