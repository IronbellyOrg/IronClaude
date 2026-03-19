"""Residual semantic layer with adversarial validation.

Implements FR-4 (semantic checking), FR-5 (chunked comparison),
and the lightweight debate protocol (BF-6 resolution).
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .models import Finding

logger = logging.getLogger(__name__)


# --- Prompt Budget Constants (BF-7 / NFR-3) ---

MAX_PROMPT_BYTES = 30_720  # 30KB hard limit

# Proportional allocation (BF-7 resolution)
BUDGET_SPEC_ROADMAP_PCT = 0.60     # 60% = 18,432 bytes
BUDGET_STRUCTURAL_CTX_PCT = 0.20   # 20% = 6,144 bytes
BUDGET_PRIOR_SUMMARY_PCT = 0.15    # 15% = 4,608 bytes
BUDGET_TEMPLATE_PCT = 0.05         # 5%  = 1,536 bytes

TRUNCATION_MARKER = "[TRUNCATED: {} bytes omitted]"


# --- Debate Protocol Constants (BF-6 resolution) ---

DEBATE_TOKEN_CAP = 5_000  # max tokens per finding debate

# Rubric weights for deterministic judge
RUBRIC_WEIGHTS = {
    "evidence_quality": 0.30,
    "impact_specificity": 0.25,
    "logical_coherence": 0.25,
    "concession_handling": 0.20,
}

VERDICT_MARGIN_THRESHOLD = 0.15  # margin > 0.15 = clear winner


@dataclass(frozen=True)
class RubricScores:
    """Scores for one side of the debate (prosecutor or defender)."""
    evidence_quality: int = 0      # 0-3
    impact_specificity: int = 0    # 0-3
    logical_coherence: int = 0     # 0-3
    concession_handling: int = 0   # 0-3

    @property
    def weighted_score(self) -> float:
        """Compute weighted score normalized to [0.0, 1.0]."""
        raw = (
            self.evidence_quality * RUBRIC_WEIGHTS["evidence_quality"]
            + self.impact_specificity * RUBRIC_WEIGHTS["impact_specificity"]
            + self.logical_coherence * RUBRIC_WEIGHTS["logical_coherence"]
            + self.concession_handling * RUBRIC_WEIGHTS["concession_handling"]
        )
        return raw / 3.0  # Normalize: max raw per criterion is 3


# --- Prompt Templates ---

PROSECUTOR_TEMPLATE = """You are the PROSECUTOR in a severity validation debate.

## Finding Under Review
- **Dimension**: {dimension}
- **Rule ID**: {rule_id}
- **Current Severity**: HIGH
- **Description**: {description}
- **Spec Evidence**: {spec_quote}
- **Roadmap Evidence**: {roadmap_quote}

## Spec Context
{spec_context}

## Roadmap Context
{roadmap_context}

## Your Task
Argue that this finding IS correctly classified as HIGH severity.
Provide concrete evidence from the spec and roadmap.

## Response Format (YAML)
```yaml
argument: |
  <your argument>
evidence_points:
  - <point 1>
  - <point 2>
recommended_severity: HIGH
confidence: <0.0-1.0>
```"""

DEFENDER_TEMPLATE = """You are the DEFENDER in a severity validation debate.

## Finding Under Review
- **Dimension**: {dimension}
- **Rule ID**: {rule_id}
- **Current Severity**: HIGH
- **Description**: {description}
- **Spec Evidence**: {spec_quote}
- **Roadmap Evidence**: {roadmap_quote}

## Spec Context
{spec_context}

## Roadmap Context
{roadmap_context}

## Your Task
Argue that this finding should be DOWNGRADED from HIGH.
If downgrading, recommend MEDIUM or LOW with justification.

## Response Format (YAML)
```yaml
argument: |
  <your argument>
evidence_points:
  - <point 1>
  - <point 2>
recommended_severity: <MEDIUM or LOW>
confidence: <0.0-1.0>
```"""


# --- Semantic Check Request ---

@dataclass
class SemanticCheckRequest:
    """Input to the semantic LLM layer for one dimension."""
    dimension: str
    spec_sections: list[Any]       # SpecSection objects
    roadmap_sections: list[Any]    # SpecSection objects
    structural_findings: list[Finding]
    prior_findings_summary: str


# --- Core Functions ---

def _truncate_to_budget(content: str, budget_bytes: int) -> str:
    """Tail-truncate content to fit within byte budget on line boundaries.

    BF-7 resolution: proportional budget allocation with tail-truncation.
    """
    encoded = content.encode("utf-8")
    if len(encoded) <= budget_bytes:
        return content

    omitted = len(encoded) - budget_bytes
    marker = TRUNCATION_MARKER.format(omitted)
    marker_bytes = len(marker.encode("utf-8")) + 1  # +1 for newline
    target = budget_bytes - marker_bytes

    if target <= 0:
        return marker

    # Truncate on line boundary
    truncated = encoded[:target].decode("utf-8", errors="ignore")
    last_newline = truncated.rfind("\n")
    if last_newline > 0:
        truncated = truncated[:last_newline]

    return truncated + "\n" + marker


def build_semantic_prompt(request: SemanticCheckRequest) -> str:
    """Build a chunked prompt for one semantic check.

    Enforces NFR-3: prompt size <= 30KB via proportional budget
    allocation (BF-7 resolution).
    """
    template_budget = int(MAX_PROMPT_BYTES * BUDGET_TEMPLATE_PCT)
    spec_roadmap_budget = int(MAX_PROMPT_BYTES * BUDGET_SPEC_ROADMAP_PCT)
    structural_budget = int(MAX_PROMPT_BYTES * BUDGET_STRUCTURAL_CTX_PCT)
    prior_budget = int(MAX_PROMPT_BYTES * BUDGET_PRIOR_SUMMARY_PCT)

    # Build template
    template = (
        f"## Semantic Fidelity Check: {request.dimension}\n\n"
        "Analyze the following spec and roadmap sections for semantic "
        "deviations NOT already covered by structural checkers.\n\n"
        "### Already Checked (do NOT re-report)\n"
    )

    template_bytes = len(template.encode("utf-8"))
    if template_bytes > template_budget:
        raise ValueError(
            f"Template overhead ({template_bytes}B) exceeds budget ({template_budget}B)"
        )

    # Truncate spec+roadmap sections
    spec_text = "\n\n".join(
        f"#### {s.heading}\n{s.content}" if hasattr(s, 'heading') else str(s)
        for s in request.spec_sections
    )
    roadmap_text = "\n\n".join(
        f"#### {s.heading}\n{s.content}" if hasattr(s, 'heading') else str(s)
        for s in request.roadmap_sections
    )
    combined = f"### Spec Sections\n{spec_text}\n\n### Roadmap Sections\n{roadmap_text}"
    combined = _truncate_to_budget(combined, spec_roadmap_budget)

    # Truncate structural findings context
    structural_text = "\n".join(
        f"- [{f.severity}] {f.dimension}: {f.description}"
        for f in request.structural_findings
    )
    structural_text = _truncate_to_budget(structural_text, structural_budget)

    # Truncate prior findings summary
    prior_text = _truncate_to_budget(request.prior_findings_summary, prior_budget)

    prompt = (
        f"{template}"
        f"{structural_text}\n\n"
        f"### Prior Findings (for anchoring)\n{prior_text}\n\n"
        f"{combined}\n\n"
        "### Instructions\n"
        "Report only NEW semantic deviations. Assign severity: HIGH, MEDIUM, or LOW.\n"
        "For each finding, provide: dimension, description, severity, evidence.\n"
    )

    # Final enforcement assert
    prompt_size = len(prompt.encode("utf-8"))
    assert prompt_size <= MAX_PROMPT_BYTES, (
        f"Prompt size {prompt_size}B exceeds {MAX_PROMPT_BYTES}B budget"
    )

    return prompt


def score_argument(response_yaml: dict) -> RubricScores:
    """Score a debate argument using the deterministic rubric.

    BF-6 resolution: automated judge with 4-criterion rubric.
    Scores 0-3 per criterion based on evidence in the response.
    """
    evidence_points = response_yaml.get("evidence_points", [])
    argument = response_yaml.get("argument", "")
    confidence = response_yaml.get("confidence", 0.0)

    # Evidence quality: count of concrete evidence points
    eq = min(len(evidence_points), 3)

    # Impact specificity: argument length and specificity
    word_count = len(argument.split())
    if word_count >= 100:
        imp = 3
    elif word_count >= 50:
        imp = 2
    elif word_count >= 20:
        imp = 1
    else:
        imp = 0

    # Logical coherence: confidence level maps to coherence
    if confidence >= 0.8:
        lc = 3
    elif confidence >= 0.6:
        lc = 2
    elif confidence >= 0.4:
        lc = 1
    else:
        lc = 0

    # Concession handling: presence of caveats/qualifications
    concession_markers = ["however", "although", "while", "despite", "caveat", "limitation"]
    concessions = sum(1 for m in concession_markers if m in argument.lower())
    ch = min(concessions, 3)

    return RubricScores(
        evidence_quality=eq,
        impact_specificity=imp,
        logical_coherence=lc,
        concession_handling=ch,
    )


def judge_verdict(
    prosecutor_scores: RubricScores,
    defender_scores: RubricScores,
    defender_recommendation: str = "MEDIUM",
) -> tuple[str, float]:
    """Deterministic judge: compare weighted scores, apply margin threshold.

    BF-6 resolution:
    - Prosecutor margin > 0.15 -> CONFIRM_HIGH
    - Defender margin > 0.15 -> DOWNGRADE_TO_{recommendation}
    - Margin <= 0.15 (tiebreak) -> CONFIRM_HIGH (conservative)

    Returns (verdict, margin).
    """
    p_score = prosecutor_scores.weighted_score
    d_score = defender_scores.weighted_score
    margin = p_score - d_score

    if margin > VERDICT_MARGIN_THRESHOLD:
        return "CONFIRM_HIGH", margin
    elif margin < -VERDICT_MARGIN_THRESHOLD:
        return f"DOWNGRADE_TO_{defender_recommendation}", margin
    else:
        # Tiebreak: conservative -- uncertain cases stay HIGH
        return "CONFIRM_HIGH", margin


# --- Debate-Registry Wiring (Task 4.3) ---

def wire_debate_verdict(
    registry: Any,  # DeviationRegistry from convergence module
    finding: Finding,
    verdict: str,
    transcript_path: str,
) -> None:
    """Wire debate verdict into the deviation registry.

    After validate_semantic_high() returns, this updates the registry
    with the debate outcome and adjusts severity if downgraded.
    """
    stable_id = getattr(finding, 'stable_id', '')
    if not stable_id:
        logger.warning("Finding has no stable_id; cannot record verdict")
        return

    registry.record_debate_verdict(stable_id, verdict, transcript_path)

    if verdict.startswith("DOWNGRADE_TO_"):
        new_severity = verdict.replace("DOWNGRADE_TO_", "")
        logger.info(
            "Finding %s downgraded from HIGH to %s by debate verdict",
            stable_id[:8], new_severity,
        )
