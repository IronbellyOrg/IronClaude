# BF-6 Resolution: Single-Round Prosecutor/Defender with Automated Judge

## Selected Solution

**Solution A**: Single-round prosecutor/defender with automated judge (deterministic rubric).

**Rationale**: Weighted score 8.4 vs 5.1 (Solution B). Solution A wins on all three criteria:

1. **Specification completeness (40%)**: Exact prompt templates, exact rubric with numeric thresholds, exact output schema. A developer can implement `validate_semantic_high()` from this document alone without guessing at any parameter.
2. **Token efficiency (30%)**: ~3,800 tokens per finding (2 parallel LLM calls) vs ~14,500 tokens (6 calls). Solution B wastes Steps 4-5 (refactor plan + merge) which produce artifacts irrelevant to severity validation.
3. **Verdict quality (30%)**: Both solutions score equally. Solution A's deterministic rubric is reproducible and conservative (tiebreak favors CONFIRM_HIGH). Solution B's general-purpose scoring protocol has a semantic mismatch — it was designed to compare implementations, not argue severity levels.

---

## Debate Protocol Specification

### Roles

| Role | Type | Count | Purpose |
|------|------|-------|---------|
| Prosecutor | LLM call (ClaudeProcess) | 1 per finding | Argues the finding IS correctly classified as HIGH severity |
| Defender | LLM call (ClaudeProcess) | 1 per finding | Argues the finding should be downgraded to MEDIUM or LOW |
| Judge | Deterministic Python function | 0 LLM calls | Scores both arguments against a fixed rubric, produces verdict |

The architecture doc's reference to "3 roles" is correct — prosecutor, defender, judge. The "2-agent" label refers to the 2 LLM calls (the judge is not an LLM agent).

### Prompt Templates

#### Prosecutor Prompt

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

#### Defender Prompt

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

### Scoring Criteria

The judge is a deterministic Python function. It scores each argument on 4 criteria, each 0-3 points:

| Criterion | Weight | 3 (Strong) | 2 (Adequate) | 1 (Weak) | 0 (Missing) |
|-----------|--------|------------|--------------|----------|-------------|
| **Evidence Quality** | 30% | 2+ exact spec/roadmap quotes with section refs | 1 exact quote + 1 paraphrase | Only paraphrases, no exact quotes | No citations |
| **Impact Specificity** | 25% | Names specific function, data flow, or behavior affected | Names general area affected | Vague "could cause issues" language | No impact stated |
| **Logical Coherence** | 25% | Argument follows directly from evidence with no logical leaps | Mostly follows from evidence with minor gaps | Significant logical gaps between evidence and conclusion | Self-contradictory or non-sequitur |
| **Concession Handling** | 20% | Prosecutor: rebuttal addresses the strongest downgrade argument directly. Defender: concession names a specific, strong counter-point | Acknowledges counter-point but deflects or generalizes | Ignores obvious counter-points | Field missing or empty |

#### Scoring Implementation

```python
import yaml
from dataclasses import dataclass
from typing import Literal

@dataclass
class RubricScores:
    evidence: int       # 0-3
    impact: int         # 0-3
    coherence: int      # 0-3
    concession: int     # 0-3

    @property
    def weighted(self) -> float:
        """Weighted score normalized to 0.0-1.0."""
        weights = {"evidence": 0.30, "impact": 0.25, "coherence": 0.25, "concession": 0.20}
        raw = (
            self.evidence * weights["evidence"]
            + self.impact * weights["impact"]
            + self.coherence * weights["coherence"]
            + self.concession * weights["concession"]
        )
        return raw / 3.0  # max raw is 3.0, so this normalizes to 0-1


def score_argument(response_yaml: dict, role: Literal["prosecutor", "defender"]) -> RubricScores:
    """Score a parsed YAML response against the rubric.

    Evidence Quality: count citations with both 'quote' and 'source' fields.
    Impact Specificity: check for named functions/data flows/behaviors in impact argument.
    Logical Coherence: check evidence supports conclusion (citations reference claim).
    Concession Handling: check rebuttal (prosecutor) or concession (defender) field.
    """
    citations = response_yaml.get("evidence_citations", [])
    valid_citations = [
        c for c in citations
        if isinstance(c, dict) and c.get("quote") and c.get("source")
    ]

    # Evidence Quality
    if len(valid_citations) >= 2:
        evidence = 3
    elif len(valid_citations) == 1:
        evidence = 2
    elif len(citations) > 0:
        evidence = 1
    else:
        evidence = 0

    # Impact Specificity
    if role == "prosecutor":
        impact_text = response_yaml.get("impact_argument", "")
    else:
        impact_text = response_yaml.get("mitigation_argument", "")

    # Heuristic: specific if contains parens (function call), dots (module path),
    # or quoted identifiers
    has_specifics = any(
        marker in impact_text
        for marker in ["()", ".", "`", "def ", "class ", "Step("]
    )
    if has_specifics and len(impact_text) > 50:
        impact = 3
    elif len(impact_text) > 30:
        impact = 2
    elif len(impact_text) > 0:
        impact = 1
    else:
        impact = 0

    # Logical Coherence: citations should reference terms from impact argument
    if evidence >= 2 and impact >= 2:
        coherence = 3
    elif evidence >= 1 and impact >= 1:
        coherence = 2
    elif evidence >= 1 or impact >= 1:
        coherence = 1
    else:
        coherence = 0

    # Concession Handling
    if role == "prosecutor":
        concession_text = response_yaml.get("downgrade_rebuttal", "")
    else:
        concession_text = response_yaml.get("concession", "")

    if concession_text and len(concession_text) > 30 and any(
        marker in concession_text for marker in ["`", "FR-", "NFR-", "spec", "require"]
    ):
        concession = 3
    elif concession_text and len(concession_text) > 15:
        concession = 2
    elif concession_text:
        concession = 1
    else:
        concession = 0

    return RubricScores(evidence=evidence, impact=impact, coherence=coherence, concession=concession)


def judge_verdict(
    prosecutor_scores: RubricScores,
    defender_scores: RubricScores,
    defender_recommended_level: str,
) -> tuple[str, float]:
    """Deterministic verdict from rubric scores.

    Returns (verdict, confidence).
    Confidence is the absolute margin mapped to 0.5-1.0 range.
    """
    p_weighted = prosecutor_scores.weighted
    d_weighted = defender_scores.weighted

    margin = p_weighted - d_weighted

    if margin > 0.15:
        verdict = "CONFIRM_HIGH"
    elif margin < -0.15:
        level = defender_recommended_level.upper()
        if level not in ("MEDIUM", "LOW"):
            level = "MEDIUM"  # safe default
        verdict = f"DOWNGRADE_TO_{level}"
    else:
        # Tiebreak: favor prosecutor (conservative)
        verdict = "CONFIRM_HIGH"

    # Confidence: map |margin| to 0.5-1.0 range (0.0 margin = 0.5 confidence, 1.0 margin = 1.0)
    confidence = 0.5 + min(abs(margin), 0.5)

    return verdict, confidence
```

### Round Structure

| Round | Participants | Execution | Purpose |
|-------|-------------|-----------|---------|
| 1 (only) | Prosecutor + Defender | **Parallel** via ClaudeProcess | Each argues their case independently |

- **Round count**: 1 (single round)
- **No rebuttals**: This is the lightweight variant. The full `/sc:adversarial` protocol handles multi-round debate for FR-8 regression validation.
- **Parallel execution**: Prosecutor and defender prompts are independent and run simultaneously, halving wall-clock time.

### Token Budget

| Component | Input Tokens | Output Tokens | Total |
|-----------|-------------|---------------|-------|
| Prosecutor prompt | ~1,500 | ~400 | ~1,900 |
| Defender prompt | ~1,500 | ~400 | ~1,900 |
| Judge (Python) | 0 | 0 | 0 |
| **Total per finding** | **~3,000** | **~800** | **~3,800** |

**Budget cap**: 5,000 tokens per finding (hard limit). If `spec_sections_text` or `roadmap_sections_text` would exceed this, truncate to the first 2 sections by byte size, preserving the section most relevant to the finding's dimension.

### Output Format

Each debate produces a single YAML file:

```yaml
# Schema: DebateOutput v1
finding_id: "a1b2c3d4e5f67890"
dimension: "signatures"
rule_id: "phantom_id"
original_severity: "HIGH"
verdict: "CONFIRM_HIGH"           # or DOWNGRADE_TO_MEDIUM, DOWNGRADE_TO_LOW
verdict_confidence: 0.82

prosecutor:
  impact_argument: "The roadmap references FR-009 which does not exist in the spec's requirement ID set. Any task implementing FR-009 will produce code with no spec backing, creating untraceable functionality that cannot be validated."
  evidence_citations:
    - quote: "requirement_ids: tuple[RequirementID, ...]"
      source: "Sec 3.1/SpecData"
    - quote: "phantom_id: HIGH  # Roadmap references ID not in spec"
      source: "Sec 4.2.2/SignatureChecker"
  downgrade_rebuttal: "A phantom ID is definitionally HIGH — it represents fabricated requirements that would pass through the pipeline unchecked."
  confidence: 0.9
  rubric_scores:
    evidence: 3
    impact: 3
    coherence: 3
    concession: 2
  weighted_score: 0.88

defender:
  mitigation_argument: "The roadmap may use FR-009 as shorthand for a requirement that exists under a different ID. Cross-referencing shows the described functionality maps to FR-1.2."
  evidence_citations:
    - quote: "Referenced IDs, function names/params in task descriptions"
      source: "Sec 3/FR-1"
  recommended_level: "MEDIUM"
  recommended_level_justification: "ID mismatch without functional gap is a labeling error, not a missing requirement."
  concession: "If FR-009 truly has no spec counterpart, the finding is correctly HIGH — phantom requirements create unvalidatable code."
  confidence: 0.6
  rubric_scores:
    evidence: 2
    impact: 2
    coherence: 2
    concession: 3
  weighted_score: 0.72

margin: 0.16
timestamp: "2026-03-19T10:00:00Z"
transcript_path: "debates/a1b2c3d4e5f67890/debate.yaml"
```

### Verdict Mapping

| Prosecutor Weighted | Defender Weighted | Margin | Verdict |
|--------------------|-------------------|--------|---------|
| > defender + 0.15 | - | > +0.15 | **CONFIRM_HIGH** |
| < defender - 0.15 | - | < -0.15 | **DOWNGRADE_TO_{defender.recommended_level}** |
| within 0.15 of defender | - | -0.15 to +0.15 | **CONFIRM_HIGH** (conservative tiebreak) |

The 0.15 margin threshold means a clear win requires roughly a 1-point advantage on a primary criterion. The conservative tiebreak ensures uncertain cases do not accidentally downgrade genuine HIGH findings.

---

## Architecture Design Change

### Addition to Section 4.3 (`semantic_layer.py`)

Replace the current `validate_semantic_high()` docstring (architecture-design.md lines 444-461) with:

```python
def validate_semantic_high(
    finding: Finding,
    spec_sections: list[SpecSection],
    roadmap_sections: list[SpecSection],
    config: PipelineConfig,
) -> tuple[str, str]:
    """Spawn lightweight adversarial debate for a semantic HIGH finding.

    Returns (verdict, transcript_reference):
        verdict: "CONFIRM_HIGH" | "DOWNGRADE_TO_MEDIUM" | "DOWNGRADE_TO_LOW"
        transcript_reference: path to debate YAML output file

    Protocol: Single-round prosecutor/defender with automated judge.
        1. Build prosecutor prompt (argues finding IS HIGH) — see PROSECUTOR_TEMPLATE
        2. Build defender prompt (argues finding should be downgraded) — see DEFENDER_TEMPLATE
        3. Execute both via ClaudeProcess in parallel (2 LLM calls)
        4. Parse YAML responses
        5. Score both against 4-criterion rubric (evidence quality 30%,
           impact specificity 25%, logical coherence 25%, concession handling 20%)
        6. Compute margin = prosecutor_weighted - defender_weighted
        7. Verdict: margin > 0.15 → CONFIRM_HIGH
                    margin < -0.15 → DOWNGRADE_TO_{defender.recommended_level}
                    else → CONFIRM_HIGH (conservative tiebreak)
        8. Write debate output YAML to config.output_dir / "debates" / finding.stable_id

    Token budget: ~3,800 per finding (hard cap: 5,000).
    LLM calls: 2 (parallel).
    Round count: 1 (no rebuttals — this is the lightweight variant).

    For full multi-round adversarial debate (FR-8 regression validation),
    use /sc:adversarial --depth quick|standard|deep.
    """
```

### New Constants in `semantic_layer.py`

```python
# Debate prompt templates
PROSECUTOR_TEMPLATE: str = """..."""  # As specified in Prompt Templates above
DEFENDER_TEMPLATE: str = """..."""    # As specified in Prompt Templates above

# Rubric weights
RUBRIC_WEIGHTS: dict[str, float] = {
    "evidence": 0.30,
    "impact": 0.25,
    "coherence": 0.25,
    "concession": 0.20,
}

# Verdict thresholds
VERDICT_MARGIN_THRESHOLD: float = 0.15
DEBATE_TOKEN_CAP: int = 5000
```

### Registry Integration

After `validate_semantic_high()` returns, the caller in `run_semantic_layer()` updates the registry:

```python
verdict, transcript_path = validate_semantic_high(finding, spec_secs, road_secs, config)
registry.record_debate_verdict(finding.stable_id, verdict, transcript_path)
if verdict.startswith("DOWNGRADE_TO_"):
    new_severity = verdict.replace("DOWNGRADE_TO_", "")
    finding.severity = new_severity
```

---

## Validation

### Unit Tests

1. **Rubric scoring determinism**: Given fixed YAML responses, `score_argument()` always returns the same `RubricScores`.
2. **Verdict thresholds**: Test all three verdict paths (CONFIRM_HIGH, DOWNGRADE, tiebreak) with boundary margin values (0.14, 0.15, 0.16, -0.14, -0.15, -0.16).
3. **YAML parse failure handling**: If prosecutor or defender response is not valid YAML, all rubric scores default to 0 for that side. This means: if prosecutor fails to produce valid YAML, defender wins (likely downgrade); if defender fails, prosecutor wins (CONFIRM_HIGH). If both fail, tiebreak applies (CONFIRM_HIGH).
4. **Token budget enforcement**: Verify that `spec_sections_text` truncation kicks in when combined prompt exceeds 5,000 tokens.

### Integration Tests

1. **Known-HIGH finding**: Feed a phantom ID finding (definitionally HIGH) through the debate. Verify verdict is CONFIRM_HIGH.
2. **Known-MEDIUM finding**: Feed a cosmetic difference finding (labeled HIGH by semantic layer). Verify verdict is DOWNGRADE_TO_MEDIUM.
3. **Registry update**: After debate, verify `registry.findings[stable_id]` has `debate_verdict` and `debate_transcript` populated.
4. **Parallel execution**: Run 3 debates simultaneously. Verify no state corruption and all produce valid output.

### Property-Based Tests

1. **Tiebreak conservative**: For any two `RubricScores` where `|margin| <= 0.15`, verdict is always CONFIRM_HIGH.
2. **Score bounds**: `weighted` property always returns a value in [0.0, 1.0].
3. **Verdict determinism**: Same (prosecutor_scores, defender_scores, recommended_level) tuple always produces the same verdict.
