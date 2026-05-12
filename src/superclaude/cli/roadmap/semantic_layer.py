"""Residual semantic layer with adversarial validation.

Implements FR-4 (semantic checking), FR-5 (chunked comparison),
and the lightweight debate protocol (BF-6 resolution).
"""
from __future__ import annotations

import json
import logging
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

import yaml

from .models import Finding

logger = logging.getLogger(__name__)


# --- Prompt Budget Constants (BF-7 / NFR-3) ---

MAX_PROMPT_BYTES = 30_720  # 30KB hard limit

# Proportional allocation (BF-7 resolution)
BUDGET_SPEC_ROADMAP_PCT = 0.60     # 60% = 18,432 bytes
BUDGET_STRUCTURAL_CTX_PCT = 0.20   # 20% = 6,144 bytes
BUDGET_PRIOR_SUMMARY_PCT = 0.15    # 15% = 4,608 bytes
BUDGET_TEMPLATE_PCT = 0.05         # 5%  = 1,536 bytes

TRUNCATION_MARKER = "[TRUNCATED: {} bytes omitted from '{}']"


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

def _truncate_to_budget(content: str, budget_bytes: int, heading: str = "content") -> str:
    """Tail-truncate content to fit within byte budget on line boundaries.

    BF-7 resolution: proportional budget allocation with tail-truncation.
    FR-4.2: truncation markers include section heading.
    """
    encoded = content.encode("utf-8")
    if len(encoded) <= budget_bytes:
        return content

    omitted = len(encoded) - budget_bytes
    marker = TRUNCATION_MARKER.format(omitted, heading)
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

    # Truncation priority (FR-4.2): prior summary first, then structural, then spec/roadmap
    # Truncate prior findings summary (least critical — cut first)
    prior_text = _truncate_to_budget(
        request.prior_findings_summary, prior_budget, heading="Prior Findings Summary",
    )

    # Truncate structural findings context (secondary)
    structural_text = "\n".join(
        f"- [{f.severity}] {f.dimension}: {f.description}"
        for f in request.structural_findings
    )
    structural_text = _truncate_to_budget(
        structural_text, structural_budget, heading="Structural Findings Context",
    )

    # Truncate spec+roadmap sections (last resort)
    spec_text = "\n\n".join(
        f"#### {s.heading}\n{s.content}" if hasattr(s, 'heading') else str(s)
        for s in request.spec_sections
    )
    roadmap_text = "\n\n".join(
        f"#### {s.heading}\n{s.content}" if hasattr(s, 'heading') else str(s)
        for s in request.roadmap_sections
    )
    combined = f"### Spec Sections\n{spec_text}\n\n### Roadmap Sections\n{roadmap_text}"
    combined = _truncate_to_budget(
        combined, spec_roadmap_budget, heading="Spec/Roadmap Sections",
    )

    prompt = (
        f"{template}"
        f"{structural_text}\n\n"
        f"### Prior Findings (for anchoring)\n{prior_text}\n\n"
        f"{combined}\n\n"
        "### Instructions\n"
        "Report only NEW semantic deviations. Assign severity: HIGH, MEDIUM, or LOW.\n"
        "Respond with ONLY a YAML document in the following format (no markdown fences, no prose):\n\n"
        "```\n"
        "findings:\n"
        "  - dimension: <dimension name>\n"
        "    description: <what is wrong>\n"
        "    severity: HIGH | MEDIUM | LOW\n"
        "    evidence: <supporting evidence from spec/roadmap>\n"
        "```\n\n"
        "If there are no deviations, respond with:\n"
        "```\n"
        "findings: []\n"
        "```\n"
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


# --- Structural dimension set (for filtering) ---

# Dimensions covered by structural checkers (from structural_checkers.CHECKER_REGISTRY keys).
# Semantic layer processes only aspects NOT in this set.
STRUCTURAL_DIMENSIONS = frozenset({"signatures", "data_models", "gates", "cli", "nfrs"})

# Semantic-only dimensions: judgment-dependent checks not covered by structural rules
SEMANTIC_DIMENSIONS = frozenset({
    "prose_sufficiency",       # Are descriptions adequate and unambiguous?
    "contradiction_detection", # Do spec sections contradict each other?
    "completeness_coverage",   # Are all spec aspects addressed in roadmap?
    "architectural_alignment", # Does the roadmap's design match spec intent?
})


# --- T04.01: run_semantic_layer() Entry Point ---

@dataclass
class SemanticLayerResult:
    """Result of running the semantic layer."""
    findings: list[Finding]
    prompts_sent: int = 0
    debates_triggered: int = 0
    debate_verdicts: dict[str, str] = field(default_factory=dict)


def run_semantic_layer(
    spec_sections: list[Any],
    roadmap_sections: list[Any],
    structural_findings: list[Finding],
    registry: Any,  # DeviationRegistry
    output_dir: Path,
    *,
    claude_process_factory: Callable | None = None,
) -> SemanticLayerResult:
    """Entry point for the residual semantic layer (FR-4).

    Receives only dimensions/aspects NOT covered by structural checkers.
    Uses per-section chunked input. Includes structural findings as context.
    Tags all findings with source_layer="semantic".
    Prior findings from registry memory included in prompt.

    Args:
        spec_sections: Parsed SpecSection objects from the spec.
        roadmap_sections: Parsed SpecSection objects from the roadmap.
        structural_findings: Findings from structural checkers (context, not re-checked).
        registry: Active DeviationRegistry for prior findings and verdict recording.
        output_dir: Directory for debate artifacts.
        claude_process_factory: Optional factory for LLM calls (enables testing).

    Returns:
        SemanticLayerResult with findings and debate metadata.
    """
    prior_summary = registry.get_prior_findings_summary(max_entries=50)
    result = SemanticLayerResult(findings=[])

    for dimension in sorted(SEMANTIC_DIMENSIONS):
        request = SemanticCheckRequest(
            dimension=dimension,
            spec_sections=spec_sections,
            roadmap_sections=roadmap_sections,
            structural_findings=structural_findings,
            prior_findings_summary=prior_summary,
        )

        prompt = build_semantic_prompt(request)
        result.prompts_sent += 1

        # Execute semantic check via LLM
        if claude_process_factory is not None:
            findings = _execute_semantic_check(
                prompt, dimension, claude_process_factory,
            )
        else:
            # Without a factory, return empty (no live LLM available)
            logger.warning(
                "No claude_process_factory provided; skipping LLM call for %s",
                dimension,
            )
            findings = []

        # Tag all findings with source_layer="semantic"
        for f in findings:
            if hasattr(f, 'source_layer'):
                object.__setattr__(f, 'source_layer', 'semantic') if hasattr(type(f), '__dataclass_fields__') else setattr(f, 'source_layer', 'semantic')

        # Trigger debate for HIGH findings (FR-4.1)
        for f in findings:
            if f.severity == "HIGH":
                result.debates_triggered += 1
                verdict = validate_semantic_high(
                    finding=f,
                    registry=registry,
                    output_dir=output_dir,
                    claude_process_factory=claude_process_factory,
                )
                result.debate_verdicts[f.stable_id] = verdict

        result.findings.extend(findings)

    return result


def _execute_semantic_check(
    prompt: str,
    dimension: str,
    claude_process_factory: Callable,
) -> list[Finding]:
    """Execute a single semantic check via LLM and parse response into Findings.

    The factory should return an object with a run(prompt) method that
    returns the LLM response string. Response is parsed as YAML.
    """
    from .convergence import compute_stable_id

    try:
        process = claude_process_factory()
        response_text = process.run(prompt)
    except Exception as exc:
        logger.error("Semantic check failed for %s: %s", dimension, exc)
        return []

    # Strip markdown fences if present (Claude often wraps YAML in ```yaml ... ```)
    import re
    cleaned = response_text.strip() if response_text else ""
    cleaned = re.sub(r"^```(?:ya?ml)?\s*\n", "", cleaned)
    cleaned = re.sub(r"\n```\s*$", "", cleaned)

    # Parse YAML response
    try:
        parsed = yaml.safe_load(cleaned)
    except (yaml.YAMLError, AttributeError):
        logger.warning("Failed to parse semantic response YAML for %s", dimension)
        return []

    if not isinstance(parsed, dict):
        return []

    findings_data = parsed.get("findings", [])
    if not isinstance(findings_data, list):
        return []

    findings: list[Finding] = []
    for entry in findings_data:
        if not isinstance(entry, dict):
            continue
        description = entry.get("description", "")
        severity = entry.get("severity", "MEDIUM")
        location = entry.get("location", f"semantic:{dimension}")
        rule_id = f"semantic_{dimension}"
        stable_id = compute_stable_id(dimension, rule_id, location, rule_id)

        findings.append(Finding(
            id=f"{dimension}-semantic-{stable_id[:8]}",
            severity=severity,
            dimension=dimension,
            description=description,
            location=location,
            evidence=entry.get("evidence", ""),
            fix_guidance=entry.get("fix_guidance", f"Review {dimension} for semantic issues"),
            status="ACTIVE",
            source_layer="semantic",
            rule_id=rule_id,
            spec_quote=entry.get("spec_quote", ""),
            roadmap_quote=entry.get("roadmap_quote", ""),
            stable_id=stable_id,
        ))

    return findings


# --- T04.03: validate_semantic_high() Debate Protocol ---

def validate_semantic_high(
    finding: Finding,
    registry: Any,  # DeviationRegistry
    output_dir: Path,
    *,
    claude_process_factory: Callable | None = None,
) -> str:
    """Orchestrate lightweight adversarial debate for a semantic HIGH finding.

    Implements FR-4.1 protocol steps 1-7:
    1. Build prosecutor + defender prompts from finding context
    2. Execute both via ClaudeProcess in parallel (2 LLM calls)
    3. Parse YAML responses; default scores to 0 on parse failure
    4. Score both via score_argument() against 4-criterion rubric
    5. Compute verdict via judge_verdict()
    6. Write debate YAML to output_dir/debates/{stable_id}/debate.yaml
    7. Call wire_debate_verdict() to update registry

    Args:
        finding: The semantic HIGH finding to validate.
        registry: Active deviation registry for verdict recording.
        output_dir: Directory for debate output artifacts.
        claude_process_factory: Optional factory for ClaudeProcess creation.

    Returns:
        Verdict string: "CONFIRM_HIGH", "DOWNGRADE_TO_MEDIUM", or "DOWNGRADE_TO_LOW".
    """
    stable_id = getattr(finding, 'stable_id', '') or ''

    # Step 1: Build prompts
    prosecutor_prompt = PROSECUTOR_TEMPLATE.format(
        dimension=finding.dimension,
        rule_id=getattr(finding, 'rule_id', ''),
        description=finding.description,
        spec_quote=getattr(finding, 'spec_quote', ''),
        roadmap_quote=getattr(finding, 'roadmap_quote', ''),
        spec_context="[Semantic finding — see description]",
        roadmap_context="[Semantic finding — see description]",
    )
    defender_prompt = DEFENDER_TEMPLATE.format(
        dimension=finding.dimension,
        rule_id=getattr(finding, 'rule_id', ''),
        description=finding.description,
        spec_quote=getattr(finding, 'spec_quote', ''),
        roadmap_quote=getattr(finding, 'roadmap_quote', ''),
        spec_context="[Semantic finding — see description]",
        roadmap_context="[Semantic finding — see description]",
    )

    # Step 2: Execute both in parallel
    prosecutor_yaml: dict = {}
    defender_yaml: dict = {}

    if claude_process_factory is not None:
        def _run_side(prompt: str) -> dict:
            try:
                process = claude_process_factory()
                response = process.run(prompt)
                parsed = yaml.safe_load(response)
                return parsed if isinstance(parsed, dict) else {}
            except Exception:
                return {}

        with ThreadPoolExecutor(max_workers=2) as pool:
            p_future = pool.submit(_run_side, prosecutor_prompt)
            d_future = pool.submit(_run_side, defender_prompt)
            prosecutor_yaml = p_future.result()
            defender_yaml = d_future.result()

    # Step 3 & 4: Score both sides (defaults to 0 on parse failure)
    prosecutor_scores = score_argument(prosecutor_yaml)
    defender_scores = score_argument(defender_yaml)

    # Extract defender recommendation
    defender_rec = defender_yaml.get("recommended_severity", "MEDIUM")
    if defender_rec not in ("MEDIUM", "LOW"):
        defender_rec = "MEDIUM"

    # Step 5: Deterministic verdict
    verdict, margin = judge_verdict(prosecutor_scores, defender_scores, defender_rec)

    # Step 6: Write debate YAML (T04.04)
    debate_dir = output_dir / "debates" / stable_id
    debate_dir.mkdir(parents=True, exist_ok=True)
    debate_yaml_path = debate_dir / "debate.yaml"

    debate_output = {
        "finding_stable_id": stable_id,
        "dimension": finding.dimension,
        "description": finding.description,
        "prosecutor": {
            "evidence_quality": prosecutor_scores.evidence_quality,
            "impact_specificity": prosecutor_scores.impact_specificity,
            "logical_coherence": prosecutor_scores.logical_coherence,
            "concession_handling": prosecutor_scores.concession_handling,
            "weighted_score": prosecutor_scores.weighted_score,
        },
        "defender": {
            "evidence_quality": defender_scores.evidence_quality,
            "impact_specificity": defender_scores.impact_specificity,
            "logical_coherence": defender_scores.logical_coherence,
            "concession_handling": defender_scores.concession_handling,
            "weighted_score": defender_scores.weighted_score,
        },
        "margin": margin,
        "verdict": verdict,
    }

    with open(debate_yaml_path, "w") as f:
        yaml.dump(debate_output, f, default_flow_style=False, sort_keys=False)

    # Step 7: Wire verdict into registry (T04.04)
    wire_debate_verdict(registry, finding, verdict, str(debate_yaml_path))

    logger.info(
        "Debate for %s: verdict=%s margin=%.3f",
        stable_id[:8], verdict, margin,
    )

    return verdict
