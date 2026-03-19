---
stage: 11
stage_name: remediate
depth: standard
gate: REMEDIATE_GATE
verdict: NEEDS-REVISION
conditional: true
trigger_condition: spec-fidelity FAIL with high_severity_count > 0
---

# Stage 11: remediate -- Adversarial Review

## Q1: Meaningful Output

**Whether this stage produces meaningful output depends entirely on whether spec-fidelity (stage 9) detects HIGH severity findings.** The eval spec contains two seeded ambiguities:

1. **FR-EVAL-001.4** (deviation analysis sub-entry schema omission): This is a BLOCKING-class gap -- a data model (Section 4.5) cannot be validated against an undefined schema. If spec-fidelity correctly classifies this as HIGH severity, it contributes to `high_severity_count > 0` in the fidelity report frontmatter, which causes `_high_severity_count_zero` to return False, which causes `SPEC_FIDELITY_GATE` to FAIL. This failure is the prerequisite for remediation.

2. **FR-EVAL-001.5** ("significant findings" ambiguity): This should classify as MEDIUM/WARNING -- it is an undefined threshold, not a missing data model. It does not contribute to remediation triggering.

**If remediation fires**, the output is a `remediation-tasklist.md` file. The gate (REMEDIATE_GATE, STRICT tier) requires 6 frontmatter fields (`type`, `source_report`, `source_report_hash`, `total_findings`, `actionable`, `skipped`) and two semantic checks (`frontmatter_values_non_empty`, `all_actionable_have_status`). For a single HIGH finding (FR-EVAL-001.4), the tasklist will have `total_findings: 1`, `actionable: 1`, `skipped: 0`. This is minimal but structurally valid -- the gate will not trivially pass or fail. The `all_actionable_have_status` check requires the one actionable entry to have FIXED or FAILED status, which is only true after the remediation executor runs.

**If remediation does NOT fire**, this stage is skipped entirely, producing no output. This is the more likely scenario given the risk factors in Q4.

**Risk of trivial pass**: Low if the stage fires -- the `all_actionable_have_status` check requires actual execution. **Risk of trivial skip**: High -- the triggering condition requires a specific interaction between the LLM-generated fidelity report and the `_high_severity_count_zero` semantic check.

## Q2: v3.0 Changes

Stages 11-12 are **entirely new in v3.0**. They do not exist on master at all. Master's pipeline terminates after spec-fidelity (or wiring-verification in late master). The specific v3.0 additions are:

1. **Remediate executor** (`remediate_executor.py`): Full parallel agent orchestration with:
   - `.pre-remediate` snapshot creation for rollback (atomic copy via `os.replace()`)
   - File allowlist enforcement: only `roadmap.md`, `extraction.md`, `test-strategy.md` are editable
   - Parallel `ClaudeProcess` spawning per file group with `ThreadPoolExecutor`
   - Single retry on agent failure per NFR-002
   - ALL-or-nothing rollback: any single agent failure rolls back ALL files
   - Diff-size threshold (50%) to guard against excessive changes
   - Two-write tasklist model: initial creation (T03.04), then outcome update (T04.09)

2. **REMEDIATE_GATE** (`gates.py`): New gate definition with frontmatter schema and semantic checks. This is the first gate in the pipeline that validates operational outcomes (FIXED/FAILED statuses) rather than document structure.

3. **Conditional wiring**: `_get_all_step_ids()` includes "remediate" and "certify", and `check_remediate_resume()` exists for `--resume` support. However, **the actual conditional triggering logic is NOT wired into `execute_roadmap()`**. The function `_build_steps()` builds steps 1-10 only. `build_certify_step()` exists but is never called from `execute_roadmap()`. There is no `build_remediate_step()` function at all -- the remediation executor is designed to be called directly, not as a pipeline Step.

4. **Budget system** (`_check_remediation_budget()`): Limits remediation to 2 attempts, with terminal halt and manual-fix instructions if exhausted.

5. **State persistence**: `_save_state()` preserves `remediate` and `certify` metadata dicts, and `derive_pipeline_status()` includes the `remediated` and `certified`/`certified-with-caveats` terminal states.

**Critical observation**: The remediation infrastructure (executor, gates, resume checks, budget, state) is fully implemented, but the **trigger wiring** -- the code that detects `high_severity_count > 0` in the fidelity report and actually invokes remediation -- is not present in `execute_roadmap()`. This is the single most important finding of this review.

## Q3: Artifact Verification

**Primary artifact**: `{output_dir}/remediation-tasklist.md`

A third party can verify quality through:

| Check | Method | Automated? |
|-------|--------|------------|
| Frontmatter completeness | Parse YAML, verify 6 required fields present | Yes (REMEDIATE_GATE) |
| Non-empty values | All frontmatter values non-blank | Yes (semantic check) |
| Actionable status completeness | All non-SKIPPED entries have FIXED or FAILED | Yes (semantic check) |
| source_report_hash integrity | SHA-256 of spec-fidelity.md matches frontmatter hash | Manual (only checked on --resume) |
| File allowlist compliance | Verify no findings reference files outside {roadmap.md, extraction.md, test-strategy.md} | Manual |
| Rollback correctness | Compare file contents against .pre-remediate snapshots (if still present) | Manual (snapshots deleted on success) |
| Diff-size threshold | Verify no remediated file changed > 50% of its lines | Manual (checked at execution time only) |

**Secondary artifacts**: `.pre-remediate` snapshot files (deleted on success, retained on failure), per-file `remediate-{stem}.md` output files, `.err` error files.

**Verification gap**: The snapshot cleanup on success means a third party cannot independently verify that the rollback mechanism worked correctly. On failure, snapshots are retained, making rollback auditable. This asymmetry is by design but limits post-hoc quality assessment for the success path.

## Q4: Most Likely Failure Mode

**The single most likely failure mode is that this stage never fires.**

The trigger chain is: spec-fidelity LLM output -> `high_severity_count` frontmatter field -> `_high_severity_count_zero` semantic check -> SPEC_FIDELITY_GATE FAIL -> (trigger remediation).

The fragile links in this chain are:

1. **LLM severity classification is non-deterministic.** The spec-fidelity prompt instructs the LLM to classify findings by severity. The eval spec's FR-EVAL-001.4 (undefined schema) *should* be HIGH, but the LLM might classify it as MEDIUM ("schema can be inferred from examples") or even LOW. If it classifies as MEDIUM, `high_severity_count: 0` passes the gate, and remediation never fires.

2. **The trigger wiring does not exist.** Even if spec-fidelity correctly FAILs with HIGH findings, there is no code in `execute_roadmap()` that reads `high_severity_count` from the fidelity report and invokes remediation. The spec-fidelity failure currently triggers either the spec-patch auto-resume cycle (if deviation files exist) or a pipeline halt via `sys.exit(1)`. Neither path invokes the remediation executor.

3. **Finding extraction fragility.** Even if triggered, the remediation executor needs a `list[Finding]` parsed from the fidelity report. The `Finding` dataclass requires 7 non-optional fields (`id`, `severity`, `dimension`, `description`, `location`, `evidence`, `fix_guidance`). There is no parser function visible in the codebase that extracts `Finding` objects from a spec-fidelity markdown report. The `build_remediation_prompt()` function in `remediate_prompts.py` assumes it receives pre-parsed findings.

**If this stage does fire** (assuming the wiring gap is fixed), the most likely execution failure is the diff-size threshold: with only 1 HIGH finding about an undefined schema, the remediation agent might add a schema definition section to `extraction.md` or `roadmap.md` that constitutes a small change (well under 50%). This should pass. The more concerning case is if the LLM agent rewrites large sections in the process of fixing one finding -- the 50% guard catches this.

## Q5: Eval Spec Coverage

The eval spec (FR-EVAL-001.5) specifies:

> Progress entry for remediate step includes `trigger_reason` and `finding_count`

This is a progress-reporting requirement. It does NOT test the remediation execution itself -- it tests that the progress reporter correctly records WHY remediation was triggered and HOW MANY findings were involved.

**Coverage gaps**:

1. **The eval spec assumes remediation fires.** FR-EVAL-001.5 says "Entry is only written when remediation actually executes." But it provides no mechanism to ENSURE remediation fires. If the LLM at spec-fidelity classifies FR-EVAL-001.4 as MEDIUM instead of HIGH, the eval spec's remediation-related requirements become untestable dead code. The eval spec should specify an explicit control mechanism (e.g., a test fixture that forces `high_severity_count: 1` in the fidelity report).

2. **The eval spec does not test the remediation executor behavior.** The rollback mechanism, file allowlist, parallel agent execution, diff-size threshold, retry logic, and snapshot management are all v3.0-specific features that the eval spec completely ignores. FR-EVAL-001.5 only cares about progress reporting.

3. **The seeded ambiguity in FR-EVAL-001.5 ("significant findings")** is noted as intended to produce a WARNING. But this ambiguity is in the eval spec itself, not in the pipeline's remediation trigger logic. The pipeline uses `high_severity_count > 0` as the trigger, which is precisely defined. The eval spec's ambiguity might cause the *progress reporter* to use "significant" instead of "HIGH severity" in the `trigger_reason` field, but this is a cosmetic issue, not a functional one.

4. **No coverage of remediation failure paths.** The eval spec does not test: what happens if remediation fails? What does the progress entry look like? Does it record the rollback? The `_handle_failure()` path in `remediate_executor.py` marks findings as FAILED and restores snapshots, but the progress reporter's behavior on failure is unspecified.

5. **No coverage of the `all_actionable_have_status` semantic check.** This is the most meaningful semantic check in REMEDIATE_GATE -- it verifies that all non-SKIPPED findings reached terminal status (FIXED or FAILED). The eval spec does not exercise this because it only tests progress reporting, not gate behavior.

## Conditional Execution Analysis

**Probability this stage fires with the eval spec: LOW (estimated 20-30%).**

The chain of dependencies is:

1. The pipeline must reach spec-fidelity (stages 1-9 must pass). This is likely given the eval spec is well-formed.
2. The spec-fidelity LLM must detect FR-EVAL-001.4's schema omission and classify it as HIGH severity. This is uncertain -- LLMs vary in how aggressively they classify ambiguities.
3. Even if HIGH findings are detected, the fidelity report must correctly populate `high_severity_count` as an integer in frontmatter. LLMs sometimes emit prose instead of integers.
4. **Even if all of the above succeeds, the trigger wiring from fidelity-FAIL to remediation invocation does not exist in `execute_roadmap()`.** The pipeline will halt with an error message instead of triggering remediation.

The conditional execution analysis reveals a fundamental gap: the remediation infrastructure is built but not connected. The eval spec cannot exercise what is not wired.

## Verdict

**NEEDS-REVISION**

Justification:

1. **Critical wiring gap**: The remediation trigger logic is not implemented in `execute_roadmap()`. The function `_build_steps()` builds only stages 1-10. There is no code path that detects `high_severity_count > 0` and invokes the remediation executor. The `build_certify_step()` helper exists but is never called. This means stages 11-12 are unreachable in the current codebase, regardless of what the eval spec contains.

2. **Finding parser missing**: No function exists to parse `Finding` objects from a spec-fidelity markdown report. The remediation executor requires pre-parsed `Finding` objects, but the pipeline does not provide a parser for the fidelity output format.

3. **Eval spec tests progress reporting, not remediation**: FR-EVAL-001.5 only exercises the progress reporter's ability to record `trigger_reason` and `finding_count`. It does not exercise any of the v3.0-specific remediation features (rollback, allowlist, parallel execution, diff-size threshold, budget system). These features need their own eval coverage.

4. **Non-deterministic trigger**: The eval spec provides no mechanism to guarantee that spec-fidelity produces HIGH findings. The seeded ambiguity in FR-EVAL-001.4 is designed to trigger this, but LLM behavior is not deterministic.

**Required revisions**:
- Wire the remediation trigger into `execute_roadmap()` (prerequisite for any eval to work)
- Add a finding parser for spec-fidelity output
- Add eval coverage for remediation executor behavior (not just progress reporting)
- Consider a deterministic trigger mechanism (e.g., test fixture that forces fidelity failure) to make eval results reproducible
