# Validation Reference

Reference document for Wave 4 (Validation). Documents the canonical CLI **gate-criteria validation** behavior, the cosmetic-gate auto-remediation lane that sits in front of every gate, and (for skill-mode operators) the inference-only `quality-engineer` / `self-review` sub-agent prompts retained as non-canonical guidance.

---

## CLI Canonical Behavior (B-6, VERIFIED)

> **CLI parity.** The roadmap CLI does **not** dispatch `quality-engineer` or `self-review` sub-agents and does **not** run a REVISE loop. Wave 4 in the CLI is a flat sequence of pipeline steps, each guarded by a deterministic `GateCriteria` instance built from required frontmatter fields, a `min_lines` floor, an enforcement tier, and pure-function semantic checks. Source: `src/superclaude/cli/roadmap/validate_gates.py:30-69` (`REFLECT_GATE`, `ADVERSARIAL_MERGE_GATE`) and `src/superclaude/cli/roadmap/gates.py` (per-step roadmap gates).

### Gate criteria shape

Every gate is a `GateCriteria` (`src/superclaude/cli/pipeline/models.py`) value with four fields:

| Field | Purpose |
|---|---|
| `required_frontmatter_fields` | List of YAML frontmatter keys (or OR-group alias tuples) that must be present in the step's output file. |
| `min_lines` | Minimum line count for the rendered output. Catches catastrophic truncation. |
| `enforcement_tier` | `STRICT` halts the pipeline on failure; `STANDARD` records the failure but allows continuation. |
| `semantic_checks` | List of `SemanticCheck(name, check_fn, failure_message)` pure functions taking `content: str` and returning `bool`. |

Gates are pure data — no LLM call, no `Task(...)` spawn, no sub-agent dispatch. Enforcement happens in `cli/pipeline/gates.py` against the file already written by the step.

### `REFLECT_GATE` — single-agent and per-agent validation

Defined at `cli/roadmap/validate_gates.py:30-45`. Used by both `_build_single_agent_steps` and the per-agent reflection steps in `_build_multi_agent_steps` (`cli/roadmap/validate_executor.py:247-338`).

| Property | Value |
|---|---|
| `required_frontmatter_fields` | `blocking_issues_count`, `warnings_count`, `tasklist_ready` |
| `min_lines` | `20` |
| `enforcement_tier` | `STRICT` |
| Semantic checks | `frontmatter_values_non_empty` — every frontmatter field has a non-empty value (`cli/roadmap/gates.py:131-139`). |

Step shape (`validate_executor.py:256-273`): `Step(id="reflect", prompt=build_reflect_prompt(...), output_file=validate_dir / "validation-report.md", gate=REFLECT_GATE, retry_limit=1)`. In multi-agent mode the step IDs are `reflect-{agent.id}` and each agent writes a `reflect-{agent.id}.md` reflection report (`validate_executor.py:298-322`).

### `ADVERSARIAL_MERGE_GATE` — multi-agent merge

Defined at `cli/roadmap/validate_gates.py:47-69`. Used by the adversarial-merge step that consumes N parallel reflection reports (`validate_executor.py:324-333`).

| Property | Value |
|---|---|
| `required_frontmatter_fields` | `blocking_issues_count`, `warnings_count`, `tasklist_ready`, `validation_mode`, `validation_agents` |
| `min_lines` | `30` |
| `enforcement_tier` | `STRICT` |
| Semantic checks | `frontmatter_values_non_empty` plus `agreement_table_present` — content must contain a markdown agreement/disagreement table (header row containing `"agree"` or `"agreement"`, separator, and at least one data row; see `_has_agreement_table` at `validate_gates.py:15-27`). |

Step shape (`validate_executor.py:324-333`): `Step(id="adversarial-merge", prompt=build_merge_prompt([...]), output_file=validate_dir / "validation-report.md", gate=ADVERSARIAL_MERGE_GATE, inputs=reflect_outputs, retry_limit=1)`.

### Routing — single-agent vs multi-agent

`execute_validate` picks between `_build_single_agent_steps` and `_build_multi_agent_steps` based on `len(config.agents)`:

- **1 agent** → one `reflect` step gated by `REFLECT_GATE`, output is `validation-report.md`.
- **N ≥ 2 agents** → N parallel `reflect-{agent.id}` steps (each gated by `REFLECT_GATE`) followed by one sequential `adversarial-merge` step gated by `ADVERSARIAL_MERGE_GATE`. The merge prompt is built by `build_merge_prompt([reflect outputs])`.

No PASS/REVISE/REJECT aggregate score is computed. A step either passes its gate or halts the pipeline.

### Wave 4 per-roadmap-step gates (B-3 context)

The CLI's flat 14-step pipeline also exposes deterministic `GateCriteria` for the post-merge roadmap-validation steps (used by `superclaude roadmap run`, not the standalone `validate` subcommand above):

| Step | Gate | Source |
|---|---|---|
| `anti-instinct` | `ANTI_INSTINCT_GATE` | `cli/roadmap/gates.py:1353-1378` |
| `test-strategy` | `TEST_STRATEGY_GATE` | `cli/roadmap/gates.py:1231-1272` |
| `spec-fidelity` | `SPEC_FIDELITY_GATE` | `cli/roadmap/gates.py:1274-1297` |
| `wiring-verification` | `WIRING_GATE` | `cli/audit/wiring_gate.py` |
| `deviation-analysis` | `DEVIATION_ANALYSIS_GATE` | `cli/roadmap/gates.py:1390-1423` |
| `remediate` | `REMEDIATE_GATE` | `cli/roadmap/gates.py:1299-1322` |
| `certify` | `CERTIFY_GATE` | `cli/roadmap/gates.py:1324-1351` |

All of these are `GateCriteria` instances — no sub-agent dispatch.

---

## Cosmetic-Gate Auto-Remediation Lane

> **Where it sits.** Between a step's output and its gate. When a gate fails, the pipeline calls `classify_gate_failure(content, gate_name, failure_reason)` (`cli/roadmap/cosmetic_remediator.py`) to decide whether the failure is *purely cosmetic* or has any *semantic* defect. Pure-cosmetic failures are auto-rewritten and the step continues; any semantic defect halts the pipeline as usual.

### Flag surface (`cli/roadmap/commands.py:153-170`)

| Flag | Default | Behavior |
|---|---|---|
| `--allow-cosmetic-remediation` / `--no-allow-cosmetic-remediation` | enabled | Auto-fix pure-cosmetic gate failures and continue. |
| `--strict-no-remediation` | off | Explicit alias for `--no-allow-cosmetic-remediation`; high-stakes runs disable the lane so any gate failure is terminal. |

### Cosmetic transforms (C1-C11)

`apply_cosmetic_remediations` (`cli/roadmap/cosmetic_remediator.py`) ships eleven deterministic Python-only transforms (no LLM call, all idempotent):

| ID | Transform |
|---|---|
| C1 | Heading-stem alias (e.g., `Risk Assessment` → `Risk Assessment and Mitigation`). |
| C2 | Missing `-- M{N}` suffix on a required milestone H3. |
| C3 | Wrong dash variant in the suffix (en-dash, `—` literal, no-break hyphen → canonical). |
| C4 | Wrong heading level on a known stem (`##` or `####` → `###`). |
| C5 | Trailing whitespace on header lines. |
| C6 | Trailing whitespace on any line. |
| C7 | Collapsed blank lines (3+ consecutive blanks → 1). |
| C8 | Smart-quote folding (curly → straight) outside fenced code blocks. |
| C9 | Table cell padding normalization (only on schema-matching tables). |
| C10 | Frontmatter key/value trailing whitespace. |
| C11 | Resource-requirements subsection alias normalization (e.g., `Infrastructure` → `Infrastructure Requirements`). |

### Behavior when the lane is active

When a gate failure classifies as `is_pure_cosmetic=True`:

1. The CLI rewrites the offending output via `apply_cosmetic_remediations` (`executor.py:3086-3091`).
2. The step result is marked `remediated`.
3. The applied transforms are surfaced in the HALT report (`executor.py:2254-2266`) so a human reviewer can decide whether the cosmetic fixes mask a deeper problem.
4. The pipeline continues to the next step.

Any *semantic* finding alongside the cosmetic ones forces `is_pure_cosmetic=False` and the pipeline halts as if the lane were disabled.

### Skill-orchestrator equivalent

Pipelines orchestrated via this skill SHOULD preserve the same cosmetic-vs-semantic distinction at the orchestrator level rather than re-running expensive LLM steps for purely cosmetic gate violations. Treat the C1-C11 catalogue above as the canonical list of defects that do NOT warrant a regeneration.

---

## Non-Canonical Inference-Only Material

> **Scope.** Everything below describes a `quality-engineer` + `self-review` sub-agent validation pattern with a REVISE loop. This pattern is **not** implemented by the CLI today (`cli/roadmap/executor.py` and `cli/roadmap/validate_executor.py` contain no `Task(`, no sub-agent dispatch, no aggregate score, no REVISE loop). It is retained here as an optional inference-only enhancement for skill-mode operators who want a richer holistic validation surface on top of the canonical gate criteria above. Do not cite anything in this section as CLI behavior. If/when sub-agent validation is added to the CLI, this material can be promoted back to canonical.
>
> **Note for orchestrators**: the SKILL.md Wave 4 instructions still reference these prompts. That is consistent with the CLI crosswalk in `SKILL.md` "CLI Step Crosswalk" → "Wave 4 (Validation)", which explicitly flags the sub-agent dispatch as inference-only and non-canonical for CLI parity. Aggregate `PASS ≥ 85% / REVISE 70-84% / REJECT < 70%` thresholds below are likewise inference-only — the CLI does not compute an aggregate validation score.

### Quality-Engineer Agent Prompt (inference-only)

Dispatch this prompt to a `quality-engineer` sub-agent. The agent runs in **read-only** mode — it does not modify any artifacts.

#### Prompt

```text
You are a quality-engineer validation agent for sc:roadmap. Your task is to validate the generated roadmap artifacts against the source specification.

INPUT FILES:
- Source spec: {spec_path}
- roadmap.md: {roadmap_path}
- extraction.md: {extraction_path}
- test-strategy.md: {test_strategy_path}

Perform the following validation checks and score each dimension 0-100:

## 1. COMPLETENESS (weight: 0.35)
- Every FR and NFR in extraction.md has a corresponding deliverable in at least one milestone in roadmap.md
- Every risk in extraction.md appears in the roadmap.md Risk Register
- Every success criterion in extraction.md is traceable to at least one milestone
- No orphaned deliverables (deliverables not traceable to any extracted requirement)
- Score: (items_covered / total_items) * 100

## 2. CONSISTENCY (weight: 0.30)
- Milestone IDs follow the M{digit} schema consistently
- Deliverable IDs follow the D{milestone}.{seq} schema
- Risk IDs follow the R-{3digits} schema
- Dependency references between milestones are valid (no references to non-existent milestones)
- Frontmatter values match body content (e.g., milestone_count in frontmatter matches actual milestone count)
- Domain distribution in frontmatter matches extraction.md domain distribution
- Complexity score in frontmatter matches extraction.md complexity score
- Score: (consistent_items / total_checked_items) * 100

## 3. TRACEABILITY (weight: 0.20)
- Every milestone traces back to at least one requirement
- Every deliverable has acceptance criteria
- Source line references in extraction.md are valid (not fabricated)
- Decision Summary entries cite specific data points (not subjective justifications)
- Score: (traceable_items / total_items) * 100

## 4. TEST STRATEGY VALIDATION (weight: 0.15)
- Interleave ratio matches complexity class:
  - LOW complexity → 1:3 ratio
  - MEDIUM complexity → 1:2 ratio
  - HIGH complexity → 1:1 ratio
- Every validation milestone references a real work milestone from roadmap.md
- Continuous parallel validation philosophy is explicitly encoded (not generic boilerplate)
- Stop-and-fix thresholds are defined for each severity level (Critical, Major, Minor, Info)
- Issue classification table is present with clear actions per severity
- Score: (criteria_met / total_criteria) * 100

OUTPUT FORMAT:
Return a structured validation report:
{
  "completeness": {"score": <0-100>, "issues": [<list of specific issues>]},
  "consistency": {"score": <0-100>, "issues": [<list of specific issues>]},
  "traceability": {"score": <0-100>, "issues": [<list of specific issues>]},
  "test_strategy": {"score": <0-100>, "issues": [<list of specific issues>]},
  "weighted_score": <computed>,
  "recommendation": "<PASS|REVISE|REJECT>",
  "improvement_recommendations": [<specific, actionable improvements if REVISE>]
}
```

### Self-Review Agent Prompt (inference-only)

Dispatch this prompt to a `self-review` sub-agent. The agent runs in **read-only** mode.

#### 4-Question Validation Protocol

```text
You are a self-review validation agent for sc:roadmap. Answer each question with evidence from the artifacts.

INPUT FILES:
- Source spec: {spec_path}
- roadmap.md: {roadmap_path}
- extraction.md: {extraction_path}
- test-strategy.md: {test_strategy_path}

Answer these 4 questions. For each, provide a score (0-100) and evidence.

## Question 1: Does the roadmap faithfully represent the spec? (weight: 0.30)
- Are all spec requirements represented in the roadmap?
- Does the milestone ordering respect the spec's implicit or explicit priorities?
- Are any spec requirements distorted, merged incorrectly, or misinterpreted?
- Score: percentage of requirements faithfully represented

## Question 2: Are the milestones achievable and well-ordered? (weight: 0.25)
- Does each milestone have clear, measurable deliverables?
- Are dependencies correctly identified (no circular dependencies, no missing prerequisites)?
- Is the milestone ordering logical (foundations before features, features before integration)?
- Score: percentage of milestones with correct ordering and achievable scope

## Question 3: Does the risk assessment match the actual risks? (weight: 0.25)
- Are high-impact risks identified with appropriate mitigations?
- Are there obvious risks NOT in the register (blind spots)?
- Do risk probabilities and impacts seem calibrated (not all "Low" or all "High")?
- Score: (identified_risks / estimated_total_risks) * calibration_quality

## Question 4: Is the test strategy actionable? (weight: 0.20)
- Can a developer follow the test strategy to validate each milestone?
- Are stop-and-fix criteria specific enough to trigger action?
- Does the validation milestone placement make sense given the roadmap structure?
- Score: percentage of validation milestones with actionable criteria

OUTPUT FORMAT:
{
  "q1_faithfulness": {"score": <0-100>, "evidence": "<specific examples>"},
  "q2_achievability": {"score": <0-100>, "evidence": "<specific examples>"},
  "q3_risk_quality": {"score": <0-100>, "evidence": "<specific examples>"},
  "q4_test_actionability": {"score": <0-100>, "evidence": "<specific examples>"},
  "weighted_score": <computed>,
  "recommendation": "<PASS|REVISE|REJECT>",
  "improvement_recommendations": [<specific, actionable improvements if REVISE>]
}
```

### Score Aggregation (inference-only)

Both agents run in **parallel** (they are independent read-only validators). Their scores are aggregated into a final validation score.

#### Aggregation formula

```text
final_score = (quality_engineer_weighted_score * 0.55) + (self_review_weighted_score * 0.45)
```

**Agent weights**: Quality-engineer (0.55) is weighted slightly higher because it performs structural validation. Self-review (0.45) provides holistic assessment.

#### Per-agent weighted score calculation

**Quality-engineer**:

```text
weighted_score = (completeness * 0.35) + (consistency * 0.30) + (traceability * 0.20) + (test_strategy * 0.15)
```

**Self-review**:

```text
weighted_score = (q1_faithfulness * 0.30) + (q2_achievability * 0.25) + (q3_risk_quality * 0.25) + (q4_test_actionability * 0.20)
```

### Decision Thresholds (inference-only)

| Score Range | Status | Action |
|-------------|--------|--------|
| >= 85% | PASS | Accept roadmap. Write `validation_status: PASS` and `validation_score: <score>` to roadmap.md frontmatter |
| 70-84% | REVISE | Enter REVISE loop (see below) |
| < 70% | REJECT | Reject roadmap. Write `validation_status: REJECT` and `validation_score: <score>`. Report all issues to user |

#### Adversarial mode additional checks (inference-only)

When adversarial mode was used (multi-spec or multi-roadmap):

- Missing adversarial artifacts (no adversarial/ directory when adversarial mode was active) → automatic REJECT
- Missing convergence score in frontmatter → automatic REVISE (regardless of score)

### REVISE Loop (inference-only)

> **CLI parity reminder.** The CLI does not execute this loop. `cli/roadmap/executor.py` and `cli/roadmap/validate_executor.py` contain zero occurrences of `REVISE` and zero re-runs of Wave 3 on the basis of validation output. The loop below applies only when an inference-mode orchestrator chooses to enact it on top of CLI output.

When the final score is 70-84% (REVISE), execute the following loop:

#### Iteration 1

1. Collect `improvement_recommendations` from both agents
2. Combine into a prioritized improvement list (highest-impact issues first)
3. Re-run Wave 3 (Generation) with the improvement list as additional input context
4. Re-run Wave 4 (Validation) on the regenerated artifacts
5. If new score >= 85%: PASS. If 70-84%: proceed to Iteration 2. If < 70%: REJECT

#### Iteration 2

1. Collect new `improvement_recommendations`
2. Re-run Wave 3 with both iteration 1 and iteration 2 recommendations
3. Re-run Wave 4
4. If new score >= 85%: PASS. If still 70-84%: accept with `validation_status: PASS_WITH_WARNINGS`. If < 70%: REJECT

#### Maximum iterations

**Hard limit**: 2 iterations. After 2 REVISE iterations without reaching PASS:

- Set `validation_status: PASS_WITH_WARNINGS`
- Set `validation_score: <final_score>`
- Append a warnings section to roadmap.md listing unresolved issues
- Report to user that roadmap passed with warnings and recommend manual review

### No-Validate Behavior

When `--no-validate` flag is set:

- Skip Wave 4 entirely
- Set `validation_status: SKIPPED`
- Set `validation_score: 0.0`
- No agents are dispatched (CLI: no validate-subcommand pipeline is built; skill-mode: no sub-agents dispatched)

This is the one Wave 4 behavior that the CLI and the inference-only material agree on verbatim.

---

## CLI parity baseline (B-6)

| Property | CLI canonical | Inference-only (non-canonical) |
|---|---|---|
| Validation mechanism | `GateCriteria` (frontmatter + min_lines + semantic checks) | `quality-engineer` + `self-review` sub-agent dispatch |
| Gates exposed | `REFLECT_GATE`, `ADVERSARIAL_MERGE_GATE` + per-step roadmap gates | (n/a) |
| Failure model | Per-step boolean: pass or halt (`STRICT`) / record (`STANDARD`) | Aggregate weighted score with PASS/REVISE/REJECT bands |
| Re-run on failure | None (one `retry_limit=1` on the step itself) | REVISE loop, max 2 iterations, re-runs Wave 3 → Wave 4 |
| Multi-agent path | N parallel `REFLECT_GATE` reflections + 1 `ADVERSARIAL_MERGE_GATE` merge | Both sub-agents always run in parallel |
| Cosmetic auto-fix | `apply_cosmetic_remediations` (C1-C11) sits in front of every gate | Not modeled |
| `--no-validate` | Skip the validate pipeline entirely | Skip Wave 4 entirely |

*Reference document for sc:roadmap v2.0.0 — loaded on-demand during Wave 4. CLI canonical behavior cited from `cli/roadmap/validate_gates.py:30-69`, `cli/roadmap/validate_executor.py:247-338`, `cli/roadmap/cosmetic_remediator.py`, and `cli/roadmap/commands.py:153-170`.*
