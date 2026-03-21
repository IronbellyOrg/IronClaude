# BF-6: Lightweight Debate Unspecified — Solution Proposals

## Problem Statement

Architecture Sec 4.3 describes a "Two-agent debate via ClaudeProcess" for semantic HIGH validation with no prompt format, scoring criteria, round count, or token budget. It mentions "prosecutor/defender/judge" (3 roles) but calls it "2-agent". A developer cannot implement `validate_semantic_high()` without guessing.

### Constraints from Existing Spec

- FR-4: "When semantic layer assigns HIGH: pipeline pauses, spawns adversarial debate"
- Resolved Question #2: "Lighter-weight variant for regression validation (FR-8). Full adversarial protocol for FR-4 semantic HIGH validation."
- `validate_semantic_high()` returns `(verdict, transcript_reference)`
- Verdicts: `CONFIRM_HIGH` | `DOWNGRADE_TO_MEDIUM` | `DOWNGRADE_TO_LOW`
- This is the LIGHTWEIGHT variant; full `/sc:adversarial` is for FR-8 regression
- Must integrate with `DeviationRegistry.record_debate_verdict()`

---

## Solution A: Single-Round Prosecutor/Defender with Automated Judge

### Concept

Two LLM calls per finding. A prosecutor argues the finding IS HIGH severity. A defender argues it should be downgraded. A deterministic scoring rubric (no third LLM call) evaluates both arguments and produces the verdict.

### Roles

| Role | Type | Purpose |
|------|------|---------|
| Prosecutor | LLM call (ClaudeProcess) | Argues finding IS high severity with evidence |
| Defender | LLM call (ClaudeProcess) | Argues finding should be downgraded with evidence |
| Judge | Deterministic rubric (Python) | Scores both arguments, produces verdict |

### Prompt Templates

**Prosecutor Prompt** (~2KB):
```
You are a severity prosecutor in a spec-fidelity audit. Your role is to argue that the following finding IS correctly classified as HIGH severity.

## Finding Under Review
- **ID**: {{finding.stable_id}}
- **Dimension**: {{finding.dimension}}
- **Rule ID**: {{finding.rule_id}}
- **Description**: {{finding.description}}
- **Spec Quote**: {{finding.spec_quote}}
- **Roadmap Quote**: {{finding.roadmap_quote}}

## Relevant Spec Sections
{{spec_sections_text}}

## Relevant Roadmap Sections
{{roadmap_sections_text}}

## Your Task
Argue that this finding SHOULD remain HIGH severity. You must provide:

1. **Impact Argument** (1-3 sentences): What concrete harm results if this deviation ships? Be specific — name the function, data flow, or user-facing behavior affected.

2. **Evidence Citations** (1-3 items): Quote exact text from the spec and/or roadmap that supports HIGH classification. Each citation must include the section reference.

3. **Downgrade Rebuttal** (1-2 sentences): Why downgrading to MEDIUM or LOW would be incorrect. What would be missed?

Respond in this exact YAML format:
```yaml
impact_argument: "<your argument>"
evidence_citations:
  - quote: "<exact quote>"
    source: "<section reference>"
  - quote: "<exact quote>"
    source: "<section reference>"
downgrade_rebuttal: "<your rebuttal>"
confidence: <0.0-1.0>
```

Do NOT hedge. Argue the strongest case for HIGH severity.
```

**Defender Prompt** (~2KB):
```
You are a severity defender in a spec-fidelity audit. Your role is to argue that the following finding should be DOWNGRADED from HIGH to MEDIUM or LOW severity.

## Finding Under Review
- **ID**: {{finding.stable_id}}
- **Dimension**: {{finding.dimension}}
- **Rule ID**: {{finding.rule_id}}
- **Description**: {{finding.description}}
- **Spec Quote**: {{finding.spec_quote}}
- **Roadmap Quote**: {{finding.roadmap_quote}}

## Relevant Spec Sections
{{spec_sections_text}}

## Relevant Roadmap Sections
{{roadmap_sections_text}}

## Your Task
Argue that this finding should be DOWNGRADED from HIGH. You must provide:

1. **Mitigation Argument** (1-3 sentences): Why is this deviation less severe than it appears? Consider: implicit coverage, additive content, cosmetic differences, or roadmap sections that address the spirit if not the letter.

2. **Evidence Citations** (1-3 items): Quote exact text from the spec and/or roadmap that supports downgrading. Each citation must include the section reference.

3. **Recommended Level**: Either MEDIUM or LOW, with a 1-sentence justification.

4. **Concession** (1 sentence): What is the strongest argument AGAINST downgrading? (steelman the prosecutor's position)

Respond in this exact YAML format:
```yaml
mitigation_argument: "<your argument>"
evidence_citations:
  - quote: "<exact quote>"
    source: "<section reference>"
  - quote: "<exact quote>"
    source: "<section reference>"
recommended_level: "MEDIUM|LOW"
recommended_level_justification: "<justification>"
concession: "<strongest argument against downgrading>"
confidence: <0.0-1.0>
```

Do NOT hedge. Argue the strongest case for downgrading.
```

### Scoring Criteria (Automated Judge Rubric)

The judge is a deterministic Python function that scores both arguments on 4 criteria, each 0-3 points:

| Criterion | Weight | 3 (Strong) | 2 (Adequate) | 1 (Weak) | 0 (Missing) |
|-----------|--------|------------|--------------|----------|-------------|
| **Evidence Quality** | 30% | 2+ exact spec/roadmap quotes with section refs | 1 exact quote + 1 paraphrase | Only paraphrases, no exact quotes | No citations |
| **Impact Specificity** | 25% | Names specific function/data flow/behavior affected | Names general area affected | Vague "could cause issues" | No impact stated |
| **Logical Coherence** | 25% | Argument follows directly from evidence; no leaps | Mostly follows from evidence; minor gaps | Significant logical gaps | Self-contradictory |
| **Concession Handling** | 20% | Acknowledges strongest counter-point and addresses it | Acknowledges counter-point but deflects | Ignores obvious counter-points | N/A for prosecutor |

**Scoring Algorithm**:
```python
def judge_verdict(prosecutor_scores: dict, defender_scores: dict) -> str:
    """Deterministic verdict from rubric scores.

    prosecutor_scores: {evidence: 0-3, impact: 0-3, coherence: 0-3, concession: 0-3}
    defender_scores:   {evidence: 0-3, impact: 0-3, coherence: 0-3, concession: 0-3}
    """
    weights = {"evidence": 0.30, "impact": 0.25, "coherence": 0.25, "concession": 0.20}

    p_weighted = sum(prosecutor_scores[k] * weights[k] for k in weights) / 3.0  # normalize to 0-1
    d_weighted = sum(defender_scores[k] * weights[k] for k in weights) / 3.0

    margin = p_weighted - d_weighted

    if margin > 0.15:
        return "CONFIRM_HIGH"
    elif margin < -0.15:
        # Use defender's recommended level
        return f"DOWNGRADE_TO_{defender_recommended_level}"
    else:
        # Tiebreak: favor prosecutor (conservative — keep HIGH when uncertain)
        return "CONFIRM_HIGH"
```

### Round Structure

- **Round count**: 1 (single round: prosecutor argues, defender argues, judge scores)
- **Execution**: Prosecutor and defender run in parallel (independent prompts)
- **No rebuttals**: This is the lightweight variant; rebuttals are the full protocol's job

### Token Budget

| Component | Estimated Tokens |
|-----------|-----------------|
| Prosecutor prompt (input) | ~1,500 |
| Prosecutor response | ~400 |
| Defender prompt (input) | ~1,500 |
| Defender response | ~400 |
| Judge (Python, no LLM) | 0 |
| **Total per finding** | **~3,800** |

### Output Format

```yaml
debate_output:
  finding_id: "{{stable_id}}"
  verdict: "CONFIRM_HIGH|DOWNGRADE_TO_MEDIUM|DOWNGRADE_TO_LOW"
  verdict_confidence: 0.85  # margin magnitude mapped to 0-1
  prosecutor:
    impact_argument: "..."
    evidence_citations: [...]
    downgrade_rebuttal: "..."
    confidence: 0.9
    rubric_scores:
      evidence: 3
      impact: 2
      coherence: 3
      concession: 2  # always 2 for prosecutor (no concession field)
    weighted_score: 0.82
  defender:
    mitigation_argument: "..."
    evidence_citations: [...]
    recommended_level: "MEDIUM"
    concession: "..."
    confidence: 0.7
    rubric_scores:
      evidence: 2
      impact: 2
      coherence: 2
      concession: 3
    weighted_score: 0.68
  margin: 0.14
  transcript_path: "{{output_dir}}/debate-{{stable_id}}.yaml"
```

### LLM Calls Per Finding

**2** (prosecutor + defender, parallel)

### Advantages

- Fully specified: exact prompts, exact rubric, exact thresholds
- Deterministic judge: no third LLM call, reproducible verdicts from same arguments
- Fast: 2 parallel LLM calls, ~3.8K tokens total
- Conservative tiebreak: uncertain cases default to CONFIRM_HIGH

### Disadvantages

- Rubric scoring requires parsing YAML responses (fragile if LLM doesn't comply)
- Single round limits depth of argumentation
- Automated judge cannot evaluate nuance (e.g., technically correct but misleading evidence)

---

## Solution B: Reuse `/sc:adversarial --depth quick` Directly

### Concept

Reuse the existing `/sc:adversarial` protocol in `--depth quick` mode. Package the finding + evidence as two "variant" artifacts (a "HIGH severity report" and a "downgrade proposal"), then let the existing 5-step pipeline handle it. Map the base-selection outcome to a verdict.

### Roles

| Role | Type | Purpose |
|------|------|---------|
| Variant A ("Prosecutor artifact") | Generated document | Finding presented as confirmed HIGH |
| Variant B ("Defender artifact") | Generated document | Finding presented with downgrade rationale |
| Adversarial pipeline | Existing `/sc:adversarial --depth quick` | Diff, debate (1 round), score, plan, merge |

### Invocation Format

```python
def validate_semantic_high(
    finding: Finding,
    spec_sections: list[SpecSection],
    roadmap_sections: list[SpecSection],
    config: PipelineConfig,
) -> tuple[str, str]:
    """Invoke /sc:adversarial --depth quick for severity validation."""

    # 1. Generate two temporary artifacts
    prosecutor_artifact = _generate_prosecutor_artifact(finding, spec_sections, roadmap_sections)
    defender_artifact = _generate_defender_artifact(finding, spec_sections, roadmap_sections)

    # 2. Write to temp files
    output_dir = config.output_dir / "debates" / finding.stable_id
    p_path = output_dir / "variant-prosecutor.md"
    d_path = output_dir / "variant-defender.md"

    # 3. Invoke adversarial protocol
    # /sc:adversarial --compare variant-prosecutor.md,variant-defender.md \
    #   --depth quick --focus severity --output <output_dir>

    # 4. Map base-selection result to verdict
    base_selection = parse_base_selection(output_dir / "adversarial" / "base-selection.md")
    if base_selection.winner == "variant-prosecutor":
        verdict = "CONFIRM_HIGH"
    else:
        # Parse defender artifact for recommended level
        verdict = f"DOWNGRADE_TO_{defender_artifact.recommended_level}"

    return (verdict, str(output_dir))
```

**Prosecutor Artifact Template** (~1.5KB):
```markdown
# Severity Assessment: {{finding.stable_id}} — HIGH

## Finding
- **Dimension**: {{finding.dimension}}
- **Rule**: {{finding.rule_id}}
- **Description**: {{finding.description}}

## Spec Evidence
{{finding.spec_quote}}
(Source: {{spec_section_refs}})

## Roadmap Evidence
{{finding.roadmap_quote}}

## Severity Justification: HIGH
This deviation is HIGH severity because:
1. The spec explicitly requires {{spec_requirement_summary}}
2. The roadmap {{roadmap_gap_description}}
3. Impact: {{impact_description}}

## Recommendation
Maintain HIGH classification. This requires remediation before the gate can pass.
```

**Defender Artifact Template** (~1.5KB):
```markdown
# Severity Assessment: {{finding.stable_id}} — Recommend Downgrade

## Finding
- **Dimension**: {{finding.dimension}}
- **Rule**: {{finding.rule_id}}
- **Description**: {{finding.description}}

## Spec Evidence
{{finding.spec_quote}}
(Source: {{spec_section_refs}})

## Roadmap Evidence
{{finding.roadmap_quote}}

## Severity Justification: Downgrade to {{recommended_level}}
This deviation should be downgraded because:
1. The roadmap {{mitigation_description}}
2. The spec requirement is {{flexibility_argument}}
3. Impact is limited: {{limited_impact_description}}

## Recommendation
Downgrade to {{recommended_level}}. This does not block gate passage.
```

### Scoring/Verdict Criteria

Uses the existing `/sc:adversarial` scoring protocol:
- Quantitative layer (50%): 5 deterministic metrics (completeness, technical accuracy, structural quality, implementation readiness, innovation)
- Qualitative layer (50%): 25-criterion binary rubric with CEV protocol
- Base selection winner = verdict determination

### Verdict Mapping

| Base Selection Winner | Verdict |
|----------------------|---------|
| Prosecutor artifact | CONFIRM_HIGH |
| Defender artifact | DOWNGRADE_TO_{recommended_level from defender} |

### Round Structure

Per `--depth quick`:
- Step 1: Diff analysis (1 LLM call)
- Step 2: Debate — 1 round, advocate statements only (2 LLM calls, parallel)
- Step 3: Base selection with scoring (1 LLM call)
- Step 4: Refactoring plan (1 LLM call) — largely wasted for severity validation
- Step 5: Merge execution (1 LLM call) — largely wasted for severity validation

### Token Budget

| Component | Estimated Tokens |
|-----------|-----------------|
| Artifact generation (Python, no LLM) | 0 |
| Step 1: Diff analysis | ~3,000 |
| Step 2: Debate (2 advocates) | ~4,000 |
| Step 3: Base selection + scoring | ~3,000 |
| Step 4: Refactoring plan | ~2,000 |
| Step 5: Merge execution | ~2,500 |
| **Total per finding** | **~14,500** |

### Output Format

Standard `/sc:adversarial` output:
```
output_dir/debates/<stable_id>/adversarial/
  diff-analysis.md
  debate-transcript.md
  base-selection.md
  refactor-plan.md
  merge-log.md
  merged-output.md
```

Plus verdict extraction:
```yaml
debate_output:
  finding_id: "{{stable_id}}"
  verdict: "CONFIRM_HIGH|DOWNGRADE_TO_MEDIUM|DOWNGRADE_TO_LOW"
  verdict_confidence: 0.0-1.0  # from base-selection score margin
  transcript_path: "debates/{{stable_id}}/adversarial/"
```

### LLM Calls Per Finding

**6** (diff analysis + 2 advocates + base selection + refactor plan + merge)

### Advantages

- Zero new protocol design; reuses battle-tested `/sc:adversarial`
- Full artifact trail (5 standard adversarial documents per finding)
- If `/sc:adversarial` improves, this benefits automatically

### Disadvantages

- **3.8x more expensive** per finding (~14.5K vs ~3.8K tokens)
- Steps 4 and 5 (refactor plan, merge) are wasted — there is nothing to merge for a severity verdict
- Requires generating synthetic "variant" artifacts from a finding, which is a semantic mismatch (the adversarial protocol is designed for comparing alternative implementations, not arguing severity levels)
- Verdict extraction from base-selection.md requires parsing prose output
- Output is 5 files per finding — much heavier than needed for a simple verdict

---

## Evaluation Matrix

| Criterion | Weight | Solution A | Solution B |
|-----------|--------|-----------|-----------|
| **Specification Completeness** | 40% | **9/10** — Exact prompts, exact rubric, exact thresholds, exact output schema. A developer can implement from this alone. | **5/10** — Relies on existing protocol but mapping between adversarial output and verdict is underspecified. Artifact generation templates need {{placeholder}} resolution logic. Steps 4-5 are wasted work with no clear handling. |
| **Token Efficiency** | 30% | **9/10** — ~3,800 tokens per finding, 2 parallel LLM calls. Minimal waste. | **3/10** — ~14,500 tokens per finding, 6 LLM calls, Steps 4-5 produce artifacts nobody reads. |
| **Verdict Quality** | 30% | **7/10** — Deterministic rubric is reproducible but cannot evaluate argumentative nuance. Conservative tiebreak prevents false downgrades. | **7/10** — Full scoring protocol is thorough but designed for comparing implementations, not severity levels. Semantic mismatch may produce unreliable verdicts. |
| **Weighted Total** | 100% | **8.4** | **5.1** |

## Winner: Solution A

Solution A wins decisively. It is fully specified (a developer can implement it without guessing), token-efficient (3.8x cheaper than Solution B), and purpose-built for severity validation rather than repurposing a general-purpose comparison tool. The deterministic judge eliminates a third LLM call while providing reproducible verdicts.
