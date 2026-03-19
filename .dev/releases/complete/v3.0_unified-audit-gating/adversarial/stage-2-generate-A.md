---
stage: 2
stage_name: generate-A
depth: quick
gate: GENERATE_A_GATE
verdict: ADEQUATE
---

# Stage 2: generate-A -- Adversarial Review

## Q1: Meaningful Output

The eval spec will produce meaningful output at this stage. The extraction from stage 1 gives generate-A a spec with 6 functional requirements, 3 NFRs, a MEDIUM complexity class, and identifiable domains (backend/CLI, testing, observability). This is sufficient material for a roadmap generator to produce a multi-phase implementation plan with milestones, risk mitigations, and timeline estimates.

The GENERATE_A_GATE will not trivially pass. It requires:
- 3 frontmatter fields: `spec_source`, `complexity_score`, `primary_persona`
- min_lines=100
- 2 semantic checks: `frontmatter_values_non_empty`, `has_actionable_content`

The min_lines=100 threshold is the meaningful constraint here. A MEDIUM-complexity spec with 6 FRs should comfortably produce 100+ lines of roadmap, but a degenerate or truncated LLM response could fail this. The `has_actionable_content` check (regex for `^\s*(?:[-*]|\d+\.)\s+\S`) will pass for any roadmap containing a single bulleted or numbered list item -- this is a low bar but prevents completely prose-only outputs.

**Risk of trivial pass**: low-to-moderate. The 3 required frontmatter fields are explicitly named in the generate prompt (`spec_source`, `complexity_score`, `primary_persona`), and the prompt instruction `primary_persona: {agent.persona}` effectively hardcodes the value. The `frontmatter_values_non_empty` check catches empty values but not semantic correctness. A roadmap that emits `complexity_score: 0.99` for a MEDIUM spec still passes.

## Q2: v3.0 Changes

The GENERATE_A_GATE definition is identical between master and v3.0. The `build_generate_prompt()` function signature and body are unchanged. The step construction for generate-A in `_build_steps()` is unchanged.

Indirect v3.0 changes that affect this stage:

1. **Output sanitization**: Same as stage 1. `_sanitize_output()` strips preamble before `---`, increasing effective gate pass rate. On master, an LLM response starting with "Here is your roadmap:\n---\n..." would fail frontmatter parsing. In v3.0, the preamble is stripped and the gate sees clean frontmatter.

2. **Embed size limit**: The extraction output from stage 1 is embedded inline in the generate prompt. v3.0's higher embed limit (~120KB vs 100KB) means slightly larger extractions can be inlined. For the eval spec's MEDIUM-complexity extraction (~2-5KB expected), this is irrelevant.

3. **AgentSpec import**: v3.0 imports `AgentSpec` in the executor module (previously it was only imported transitively). This is a code hygiene change with no behavioral impact on generate-A.

4. **Downstream awareness**: Generate-A does not know about the new v3.0 stages (spec-fidelity, wiring-verification, remediate, certify). The generate prompt asks for a "comprehensive project roadmap" including "success criteria and validation approach." Whether the generated roadmap mentions progress reporting concepts (the eval spec's subject) is LLM-dependent and not gate-validated.

## Q3: Artifact Verification

**Artifact**: `{output_dir}/roadmap-{agent_id}.md` (e.g., `roadmap-opus-architect.md`)

| Check | Method | Automated? |
|-------|--------|------------|
| Frontmatter fields present | Parse YAML, verify `spec_source`, `complexity_score`, `primary_persona` | Yes (gate) |
| Frontmatter values non-empty | All values have content | Yes (semantic check) |
| Actionable content exists | At least one bulleted/numbered list item | Yes (semantic check) |
| Minimum length | >= 100 lines | Yes (gate) |
| Spec source traceability | `spec_source` references the eval spec filename | Manual |
| Complexity score propagation | `complexity_score` matches extraction's value | Manual |
| Persona application | Content reflects the agent's persona perspective | Manual |
| Requirement coverage | Roadmap addresses all 6 FRs from extraction | Manual |
| Phase structure | Roadmap has phased plan with milestones | Manual |

The gate provides structural validation (fields present, non-empty, content exists, minimum length). Semantic quality -- whether the roadmap is *good* -- is not gate-verified. This is by design: quality is assessed downstream in diff/debate/score stages.

## Q4: Most Likely Failure Mode

**Insufficient line count (< 100 lines).** While unlikely for a MEDIUM-complexity spec, this is the binding constraint. The 3 required frontmatter fields are named in the prompt and reliably produced. The semantic checks are low-bar. The 100-line minimum is the only check that depends on LLM output volume.

Failure scenarios:
- LLM produces a terse "executive summary" roadmap without expanding into phases
- LLM includes extensive frontmatter or metadata that inflates perceived output but the body is thin
- Output truncation due to token limits (less likely with modern models)

The second most likely failure is `frontmatter_values_non_empty` failing because `complexity_score` is emitted as an empty string or `primary_persona` is missing. The prompt hardcodes `primary_persona: {agent.persona}` in the instruction, but LLMs occasionally omit fields even when explicitly told to include them.

## Q5: Eval Spec Coverage

v3.0 does not change the generate-A stage. The eval spec does not need to exercise any new generate-A behavior.

The eval spec's progress-reporting focus means it cares about *whether* generate-A passes/fails and *how long* it takes (FR-EVAL-001.1: duration_ms in progress.json). The gate criteria are unchanged, so the eval spec correctly treats this stage as a pass-through that produces a progress entry.

Specific coverage considerations:

1. **Parallel execution**: Generate-A and generate-B run in parallel. FR-EVAL-001.1 requires "parallel steps (generate-A, generate-B) produce independent entries with correct timing." The eval spec correctly identifies this as a verification target. The parallel execution mechanism is unchanged in v3.0.

2. **Gate verdict recording**: FR-EVAL-001.1 requires `gate_verdict` in each progress entry. The GENERATE_A_GATE's verdict (pass/fail) must be captured by the progress reporter. The gate definition is unchanged, so the eval spec does not need to account for new gate behavior.

3. **Output file path**: FR-EVAL-001.1 requires `output_file` in each progress entry. The generate-A output path (`roadmap-{agent_id}.md`) is constructed by the executor and must be recorded. This path construction is unchanged in v3.0.

**Coverage assessment**: The eval spec adequately exercises stage 2. The parallel execution testing requirement (FR-EVAL-001.1) is the most relevant eval concern for this stage, and it is explicitly called out.

## Verdict

**ADEQUATE.** The eval spec produces valid input for stage 2, the gate is meaningful but not onerous for a MEDIUM-complexity spec, and v3.0 introduces no changes to this stage that require eval adaptation. The eval spec's explicit mention of parallel step timing (generate-A + generate-B) demonstrates awareness of the key testing challenge at this stage. No revision needed.
