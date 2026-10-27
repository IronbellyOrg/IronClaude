---
stage: 8
stage_name: test-strategy
depth: quick
gate: TEST_STRATEGY_GATE
verdict: ADEQUATE
---

# Stage 8: test-strategy -- Adversarial Review

## Q1: Meaningful Output

The eval spec exercises TEST_STRATEGY_GATE non-trivially because its `complexity_class: MEDIUM` drives a specific deterministic expectation through the gate's semantic checks:

- **complexity_class_valid**: The eval spec's MEDIUM complexity must appear in the test-strategy frontmatter as one of LOW/MEDIUM/HIGH. This is a pass-unless-omitted check, but since the prompt explicitly instructs the LLM to pull this from extraction, it should pass.
- **interleave_ratio_consistent**: This is the highest-value check for this eval spec. MEDIUM maps to `1:2`. If the LLM produces `1:1` (HIGH) or `1:3` (LOW), the gate rejects. This is a genuinely testable constraint because LLMs sometimes default to `1:1` (the "safest" seeming ratio) regardless of complexity class.
- **milestone_counts_positive**: The LLM must count milestones from the merged roadmap and produce positive integers. For a MEDIUM-complexity spec with ~5-6 phases, realistic values are 3-6 for each. Zero or negative would fail.
- **validation_philosophy_correct**: Must be exactly `continuous-parallel` (hyphenated). The prompt instructs this verbatim, but LLMs sometimes produce `continuous_parallel` (underscore) or `continuous parallel` (space). The gate rejects non-hyphenated variants.
- **major_issue_policy_correct**: Must be exactly `stop-and-fix`. Same exact-match constraint as above.

The 9-field frontmatter requirement (spec_source, generated, generator, complexity_class, validation_philosophy, validation_milestones, work_milestones, interleave_ratio, major_issue_policy) is strict. Three of these (spec_source, generated, generator) are injected by the executor's `_inject_provenance_fields()` function rather than produced by the LLM, which means 6 fields must come from the LLM itself.

The 40-line minimum is low enough that any meaningful test strategy will clear it.

**Assessment**: Meaningful -- the interleave_ratio_consistent check creates a genuine constraint that could fail, and the exact-string checks on validation_philosophy and major_issue_policy are realistic failure points.

## Q2: v3.0 Changes

Stage 8 (test-strategy) itself is **structurally unchanged in v3.0**. The `TEST_STRATEGY_GATE` definition (9 required frontmatter fields, 40 min lines, 5 semantic checks) is identical between master and v3.0. The `build_test_strategy_prompt()` function is unchanged. The step construction is unchanged.

**v3.0 changes that indirectly affect this stage**:

1. **`_inject_provenance_fields()` -- new in v3.0**: On master, the executor did NOT inject `spec_source`, `generated`, and `generator` into test-strategy output. These fields had to come from the LLM or the gate would fail on missing frontmatter. In v3.0, the executor injects any missing provenance fields post-subprocess (lines 339-344 in executor.py). This is a significant leniency increase: on master, a test-strategy output missing `spec_source` would fail the gate; in v3.0, the executor rescues it.

2. **`_sanitize_output()` -- new in v3.0**: Same as stage 7 -- strips conversational preamble before frontmatter. Increases pass rate for LLM outputs that include preamble.

3. **`_strip_yaml_quotes()` in `_parse_frontmatter()` -- new in v3.0**: The frontmatter parser now strips matching outer YAML quotes from values before comparison. This means if the LLM produces `interleave_ratio: "1:2"` (quoted), v3.0 strips the quotes and `_interleave_ratio_consistent` sees `1:2`, which passes. On master, the raw value `"1:2"` (with quotes) would fail the exact match against `1:2`. This is another leniency increase.

**Downstream v3.0 changes**: The test-strategy output (`test-strategy.md`) is not a direct input to any subsequent stage in the pipeline (spec-fidelity reads the spec and merged roadmap, not the test strategy). So downstream v3.0 changes do not affect this stage's behavior.

**Net effect**: v3.0 makes TEST_STRATEGY_GATE materially easier to pass through three independent leniency mechanisms (provenance injection, preamble sanitization, quote stripping). The eval spec should be aware of this increased pass rate.

## Q3: Artifact Verification

**Artifact**: `{output_dir}/test-strategy.md` -- the pipeline's test strategy document.

**Third-party verification checklist**:

1. **Frontmatter completeness**: Verify all 9 required fields are present. Three (spec_source, generated, generator) may have been injected by the executor -- a third party can detect injection by checking if `generator: superclaude-roadmap-executor` appears (the injected value).
2. **complexity_class is MEDIUM**: Must match the eval spec's extraction. Deterministic check.
3. **interleave_ratio is 1:2**: The MEDIUM-to-1:2 mapping is deterministic and machine-verifiable.
4. **validation_philosophy is continuous-parallel**: Exact string match. Deterministic.
5. **major_issue_policy is stop-and-fix**: Exact string match. Deterministic.
6. **milestone counts are positive integers**: Parse `validation_milestones` and `work_milestones` as integers, verify > 0. Deterministic.
7. **Min 40 lines**: `wc -l test-strategy.md` >= 40.
8. **Content quality (subjective)**: The test strategy should reference the eval spec's functional requirements (FR-EVAL-001.1 through FR-EVAL-001.6) and propose testing approaches for each. A third party can cross-check coverage by matching FR IDs between the eval spec and the test strategy.

**Automation level**: Checks 1-7 are fully automatable and deterministic. Check 8 is subjective but can be partially automated by searching for FR-EVAL-001.X references.

## Q4: Most Likely Failure Mode

**interleave_ratio mismatch with complexity_class.**

The `_interleave_ratio_consistent` check enforces a strict mapping: MEDIUM requires exactly `1:2`. The most common failure scenario:

1. The extraction correctly identifies `complexity_class: MEDIUM` and this propagates to the test-strategy prompt.
2. The LLM reads "MEDIUM" but produces `interleave_ratio: 1:1` (defaulting to the most conservative ratio) or `interleave_ratio: 1:3` (misremembering the mapping).
3. The gate rejects the output.
4. With `retry_limit=1`, the step retries with the same prompt. The LLM may produce the same incorrect ratio.

The eval spec's MEDIUM complexity is specifically valuable here because it tests the middle mapping (1:2), which is the one LLMs are most likely to confuse with either endpoint.

**Secondary failure mode**: The LLM produces `validation_philosophy: continuous_parallel` (underscore instead of hyphen). The `_validation_philosophy_correct` check requires exact match to `continuous-parallel`. This is a common LLM substitution because underscores are more common in code identifiers than hyphens.

**v3.0 mitigation**: The `_strip_yaml_quotes()` function mitigates the specific case where the ratio is correct but quoted. It does not mitigate ratio value errors or hyphen/underscore substitution.

## Q5: Eval Spec Coverage

Since stage 8 is structurally unchanged in v3.0, the question has two parts: (a) does the eval spec exercise the existing gate, and (b) does the eval spec account for v3.0's indirect changes?

**(a) Gate exercise -- covered**:
- **complexity_class**: MEDIUM -- exercises the middle enum value, which also validates the non-trivial interleave_ratio mapping.
- **interleave_ratio**: MEDIUM-to-1:2 is the most valuable test case (neither the "obvious" 1:1 nor the widest 1:3).
- **validation_philosophy**: The prompt hardcodes "continuous-parallel"; the gate verifies exact match. The eval spec does not need special content for this -- it is prompt-driven, not spec-driven.
- **major_issue_policy**: Same as above -- prompt-driven exact match.
- **milestone_counts_positive**: The eval spec's 6 FRs organized into an implementation order (Section 4.6) should produce a roadmap with countable phases/milestones.

**(b) v3.0 indirect changes -- partially covered**:
- **Provenance injection**: The eval spec does not explicitly test that `_inject_provenance_fields()` fires correctly. However, this is an executor-level feature, not a stage-specific concern. The eval should verify that test-strategy output has spec_source/generated/generator after the pipeline runs, but it does not need to distinguish LLM-produced vs. injected values for the gate to pass. **Minor gap**: If the eval wants to verify that the injection mechanism works (not just that the gate passes), it would need to check the raw LLM output before injection, which is not preserved.
- **Quote stripping**: The eval spec does not test the scenario where the LLM produces quoted values. This is a leniency mechanism that reduces false gate failures; it does not change what the eval spec needs to exercise.
- **Preamble sanitization**: Same as stage 7 -- a general-purpose leniency increase that the eval spec does not need to specifically exercise.

**Gap assessment**: The gaps are minor and relate to verifying v3.0's leniency mechanisms themselves, not to exercising the gate's core semantic checks. The eval spec's MEDIUM complexity is well-chosen for this stage.

## Verdict

**ADEQUATE** -- The eval spec's MEDIUM complexity creates a non-trivial exercise of the interleave_ratio_consistent semantic check (the gate's highest-value constraint). The exact-string checks on validation_philosophy and major_issue_policy are genuinely exercised by any spec that reaches this stage. v3.0's indirect changes (provenance injection, quote stripping, preamble sanitization) increase the pass rate but do not alter what the eval spec must provide. No eval spec revision needed for this stage.
