---
stage: 12
stage_name: certify
depth: standard
gate: CERTIFY_GATE
verdict: NEEDS-REVISION
conditional: true
trigger_condition: remediate step completes (PASS or FAIL)
---

# Stage 12: certify -- Adversarial Review

## Q1: Meaningful Output

**This stage can only fire if stage 11 (remediate) completes.** Since remediation itself has a LOW probability of firing (see stage-11 review), certification has an even lower probability. It is doubly conditional: spec-fidelity must FAIL with HIGH findings AND remediation must execute to completion.

**If certification fires**, the output is a `certification-report.md` file. The CERTIFY_GATE (STRICT tier) requires 5 frontmatter fields (`findings_verified`, `findings_passed`, `findings_failed`, `certified`, `certification_date`) and three semantic checks:

1. `frontmatter_values_non_empty` -- all fields non-blank
2. `per_finding_table_present` -- markdown table with `Finding | Severity | Result | Justification` columns plus `F-XX` data rows
3. `certified_is_true` -- `certified` field must equal "true" (case-insensitive)

For the eval spec scenario (1 HIGH finding from FR-EVAL-001.4), the certification report would verify whether the remediation fix for the undefined schema was correctly applied. The per-finding table would have a single `F-01` row. The `certified_is_true` check means the gate only passes if remediation was fully successful -- any finding with Result=FAIL would require `certified: false`, which fails the gate.

**Risk of trivial pass**: Low. The `certified_is_true` check is a hard constraint. The `per_finding_table_present` check validates both the header format AND the presence of `F-XX` data rows, preventing empty tables from passing. However, the check does not validate that the number of table rows matches `findings_verified` -- a report could claim `findings_verified: 5` but have only 1 table row and still pass.

**Risk of trivial fail**: Moderate. The `certified_is_true` check fails if the certifying LLM agent is skeptical and sets `certified: false`. Since the certification prompt instructs the agent to "Be skeptical," there is a non-trivial chance the agent declines to certify a fix for an undefined schema, especially if the remediation agent's fix was superficial.

## Q2: v3.0 Changes

Like stage 11, stage 12 is **entirely new in v3.0**. No certification stage exists on master. The v3.0 additions are:

1. **Certification prompt builder** (`certify_prompts.py`): Four pure functions:
   - `build_certification_prompt(findings, context_sections)` -- builds a per-finding verification checklist
   - `extract_finding_context(file_content, finding)` -- extracts relevant file sections per finding location
   - `generate_certification_report(results, findings)` -- generates the report with frontmatter and per-finding table
   - `route_certification_outcome(results)` -- routes outcomes (all-pass -> certified, any-fail -> certified-with-caveats)

2. **CERTIFY_GATE** (`gates.py`): New gate definition with 5 frontmatter fields and 3 semantic checks. The `_has_per_finding_table` check uses regex to validate both the header row pattern and `F-XX` data row presence. The `_certified_is_true` check is a strict boolean validation.

3. **`build_certify_step()`** (`executor.py`): Factory function that creates a `Step` object for certification with CERTIFY_GATE, 300-second timeout, and `remediation-tasklist.md` as input. This function exists but is **never called from `execute_roadmap()`**.

4. **State model**: `build_certify_metadata()` creates a metadata dict with `findings_verified`, `findings_passed`, `findings_failed`, `certified` (boolean), `report_file`, and `timestamp`. `derive_pipeline_status()` maps certify state to `certified` or `certified-with-caveats`.

5. **Resume support**: `check_certify_resume()` verifies certification can be skipped on `--resume` by checking that `certification-report.md` exists and passes CERTIFY_GATE. This is simpler than the remediate resume check (no hash verification).

**Same critical observation as stage 11**: The certification infrastructure is fully implemented, but the wiring that invokes it is missing from `execute_roadmap()`.

## Q3: Artifact Verification

**Primary artifact**: `{output_dir}/certification-report.md`

A third party can verify quality through:

| Check | Method | Automated? |
|-------|--------|------------|
| Frontmatter completeness | Parse YAML, verify 5 required fields present | Yes (CERTIFY_GATE) |
| Non-empty values | All frontmatter values non-blank | Yes (semantic check) |
| Per-finding table present | Markdown table with correct header and F-XX rows | Yes (semantic check) |
| certified is true | `certified` field equals "true" | Yes (semantic check) |
| findings_verified count matches table | Count F-XX rows, compare to frontmatter integer | Manual (gate does not cross-validate) |
| findings_passed + findings_failed = findings_verified | Arithmetic consistency | Manual (gate does not check) |
| certification_date format | ISO 8601 date | Manual (gate only checks non-empty) |
| Per-finding justifications | Each row has non-empty Justification column | Manual |
| Cross-reference to remediation | Report references correct remediation-tasklist.md | Manual |

**Verification gaps**:

1. **Count consistency is not gated.** `findings_verified` could say 5 while the table has 1 row. `findings_passed + findings_failed` could not equal `findings_verified`. These arithmetic checks are missing from CERTIFY_GATE's semantic checks.

2. **Justification quality is not gated.** The `_has_per_finding_table` regex checks for the presence of `F-XX` patterns in table rows, but it does not validate that the Justification column contains meaningful text. An agent could emit `| F-01 | HIGH | PASS | ok |` and pass the gate.

3. **certification_date is not validated as a date.** The gate checks non-empty, but `certification_date: banana` would pass.

## Q4: Most Likely Failure Mode

**The single most likely failure mode is that this stage never fires** (same root cause as stage 11 -- the wiring gap).

**If the wiring gap is fixed and certification does fire**, the most likely failure mode is **`certified_is_true` rejecting the report.**

The certification prompt instructs the agent to "Be skeptical -- check that each fix actually addresses the original issue, not just that the file was modified." For the eval spec's FR-EVAL-001.4 finding (undefined deviation analysis sub-entry schema), remediation would need to ADD a schema definition. The certifying agent must then verify that:

1. A schema was actually added (not just a comment saying "TODO: add schema")
2. The schema is complete (covers all fields needed for deviation sub-entries)
3. The schema is correctly referenced from FR-EVAL-001.4

If the remediation agent made a superficial fix (e.g., added a vague description instead of a concrete schema), the certification agent should set `certified: false` with justification. This causes CERTIFY_GATE to fail (`_certified_is_true` returns False), halting the pipeline.

This is actually the **correct behavior** -- the gate prevents low-quality remediations from being rubber-stamped. But it means the eval spec's assumption that the pipeline runs to completion is unlikely to hold for non-trivial findings.

**Secondary failure mode**: The `_has_per_finding_table` regex is strict about column ordering (`Finding | Severity | Result | Justification`). If the certifying LLM reorders columns or uses different header names (e.g., `ID` instead of `Finding`, `Verdict` instead of `Result`), the semantic check fails even if the content is substantively correct.

## Q5: Eval Spec Coverage

The eval spec (FR-EVAL-001.5) specifies:

> Certification step entry references the remediation it validates

This is a single acceptance criterion for the certification step's progress reporting. It tests that the progress JSON entry for the certify step contains a back-reference to the remediation step.

**Coverage gaps**:

1. **The eval spec does not define what "references the remediation" means.** Does the progress entry contain `remediation_step_id: "remediate"`? A file path to `remediation-tasklist.md`? A hash? The acceptance criterion is ambiguous -- it would itself fail a spec-fidelity check for insufficient specificity.

2. **No coverage of CERTIFY_GATE behavior.** The eval spec does not test:
   - The `per_finding_table_present` semantic check (table format validation)
   - The `certified_is_true` semantic check (boolean certification gate)
   - The frontmatter count fields (`findings_verified`, `findings_passed`, `findings_failed`)
   - The certification failure path (what happens when `certified: false`)

3. **No coverage of the certification outcome router.** `route_certification_outcome()` in `certify_prompts.py` maps all-pass to `certified` and any-fail to `certified-with-caveats`. This routing logic is untested by the eval spec.

4. **No coverage of the state transition model.** `derive_pipeline_status()` maps certify outcomes to terminal states. The eval spec tests progress reporting, not state management.

5. **No coverage of the resume path.** `check_certify_resume()` verifies that certification can be skipped on `--resume`. The eval spec does not test resume behavior for conditional stages.

6. **The eval spec's own ambiguity (FR-EVAL-001.5 "significant findings") is irrelevant to certification.** The seeded ambiguity affects the remediation trigger threshold, not the certification step. Certification runs unconditionally after remediation -- it does not re-evaluate whether findings were "significant."

## Conditional Execution Analysis

**Probability this stage fires with the eval spec: VERY LOW (estimated 10-20%).**

The dependency chain is:

1. Stages 1-9 must pass (likely for a well-formed eval spec).
2. Spec-fidelity must detect HIGH findings (uncertain -- LLM-dependent severity classification).
3. The trigger wiring must exist (currently missing from `execute_roadmap()`).
4. The finding parser must exist (currently missing -- no function converts fidelity markdown to `Finding` objects).
5. Remediation must execute to completion (dependent on agent success, diff-size threshold, retry budget).
6. Only then does certification fire.

Each link in this chain reduces probability. Even if the wiring gap (items 3-4) is fixed, the non-deterministic severity classification (item 2) means certification is not guaranteed to fire in any given pipeline run.

**The eval spec provides no mitigation for this uncertainty.** It does not include a test fixture that forces the remediate-then-certify path. It does not specify a fallback for when stages 11-12 are skipped. The three acceptance criteria in FR-EVAL-001.5 that relate to certification are simply untestable when the stage does not fire.

## Verdict

**NEEDS-REVISION**

Justification:

1. **Same critical wiring gap as stage 11**: `build_certify_step()` exists but is never called from `execute_roadmap()`. The certification step is unreachable in the current codebase.

2. **Doubly conditional with no deterministic trigger**: Certification depends on remediation, which depends on spec-fidelity HIGH findings, which depends on LLM behavior. The eval spec provides no mechanism to force this chain, making the certification-related acceptance criteria untestable in practice.

3. **Eval spec tests only progress reporting**: FR-EVAL-001.5 tests a single aspect (back-reference to remediation) of the certification step's progress entry. It does not exercise the gate's semantic checks, the certification prompt, the outcome router, the state transitions, or the failure paths.

4. **Gate arithmetic gap**: CERTIFY_GATE does not validate that `findings_passed + findings_failed == findings_verified`. This is a structural gap that could allow inconsistent reports to pass the gate.

5. **Ambiguous acceptance criterion**: "References the remediation it validates" is insufficiently specified. It would itself fail spec-fidelity as an ambiguous requirement.

**Required revisions**:
- Wire the certification step into `execute_roadmap()` after remediation (prerequisite)
- Add a finding parser to convert fidelity report markdown to `Finding` objects (prerequisite)
- Add arithmetic consistency check to CERTIFY_GATE (`findings_passed + findings_failed == findings_verified`)
- Add certification_date format validation to CERTIFY_GATE (ISO 8601)
- Define what "references the remediation" means concretely in the eval spec (file path? step ID? hash?)
- Consider a deterministic trigger mechanism for the full remediate-certify chain
- Add eval coverage for CERTIFY_GATE semantic checks (especially `certified_is_true` failure path)
