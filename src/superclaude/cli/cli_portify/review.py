"""User review gates for the CLI Portify pipeline.

Implements:
- ReviewDecision enum (ACCEPTED, REJECTED, SKIPPED)
- REVIEW_GATE_STEPS: set of step IDs that trigger user review
- is_review_step(): identify review steps
- prompt_review(): prompt user and return decision
- review_gate(): combined check + prompt, returns (should_continue, decision)
"""

from __future__ import annotations

from enum import Enum


# ---------------------------------------------------------------------------
# ReviewDecision
# ---------------------------------------------------------------------------


class ReviewDecision(Enum):
    """Decision made at a user review gate."""

    ACCEPTED = "accepted"
    REJECTED = "rejected"
    SKIPPED = "skipped"


# ---------------------------------------------------------------------------
# REVIEW_GATE_STEPS
# ---------------------------------------------------------------------------

#: Step IDs that require a user review gate before proceeding.
REVIEW_GATE_STEPS: frozenset[str] = frozenset({
    "design-pipeline",
    "panel-review",
})


# ---------------------------------------------------------------------------
# is_review_step
# ---------------------------------------------------------------------------


def is_review_step(step_name: str) -> bool:
    """Return True if step_name requires a user review gate."""
    return step_name in REVIEW_GATE_STEPS


# ---------------------------------------------------------------------------
# prompt_review
# ---------------------------------------------------------------------------


def prompt_review(
    step_name: str,
    artifact_path: str,
    skip_review: bool = False,
) -> ReviewDecision:
    """Prompt the user to accept or reject an artifact at a review gate.

    Args:
        step_name: Name of the step whose artifact is under review.
        artifact_path: Path to the artifact file for user inspection.
        skip_review: If True, skip the prompt and return SKIPPED.

    Returns:
        ReviewDecision.SKIPPED if skip_review=True.
        ReviewDecision.ACCEPTED if user responds y/yes (case-insensitive).
        ReviewDecision.REJECTED otherwise (n, empty, EOF, KeyboardInterrupt).
    """
    if skip_review:
        return ReviewDecision.SKIPPED

    print(f"\n[Review] Step '{step_name}' produced artifact: {artifact_path}")
    print("Accept and continue? [y/N] ", end="", flush=True)

    try:
        response = input().strip().lower()
    except (EOFError, KeyboardInterrupt):
        return ReviewDecision.REJECTED

    if response in ("y", "yes"):
        return ReviewDecision.ACCEPTED
    return ReviewDecision.REJECTED


# ---------------------------------------------------------------------------
# review_gate
# ---------------------------------------------------------------------------


def review_gate(
    step_name: str,
    artifact_path: str,
    skip_review: bool = False,
) -> tuple[bool, ReviewDecision]:
    """Combined gate check: determine if review needed, prompt if so.

    Args:
        step_name: Pipeline step ID.
        artifact_path: Path to the artifact to review.
        skip_review: Bypass review prompt if True.

    Returns:
        (should_continue, ReviewDecision) — should_continue is False only
        when the user explicitly rejects the artifact.
    """
    if not is_review_step(step_name):
        return True, ReviewDecision.SKIPPED

    decision = prompt_review(step_name, artifact_path, skip_review=skip_review)
    if decision == ReviewDecision.REJECTED:
        return False, ReviewDecision.REJECTED
    return True, decision
