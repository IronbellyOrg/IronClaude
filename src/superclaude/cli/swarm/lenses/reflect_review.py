"""``reflect-review`` lens entry for reflect Tier-2 reviewer fan-out.

Frames each external swarm worker as a heterogeneous Tier-2 reflection
reviewer whose normalized artifact is suspect-aware input to the downstream
adversarial scorer.

FR-RH2.2 acceptance bullets:

- ``reflect-review`` is registered and passes the swarm lens validator (same
  gate as ``bare-review``).
- The lens emits ``suspect: true`` and a ``recommended_next_command_template``
  containing ``/sc:adversarial`` with ``{suspect_files}`` substitution.
- ``default_workers`` is in ``[2,4]``; the lens does not hard-code a Claude
  model (models come from the ``T2Model0N`` env pool, not
  ``spec.workers.models``).
"""

from __future__ import annotations

from pathlib import Path

from superclaude.cli.swarm.models import LensEntry
from superclaude.cli.swarm.schema import CANONICAL_INJECTION_GUARD_SENTENCE

__all__ = ["LENS"]


_TEMPLATE_PATH = str(
    (Path(__file__).parent / "templates" / "reflect-review-output.md").resolve()
)


LENS: LensEntry = LensEntry(
    name="reflect-review",
    description=(
        "Heterogeneous Tier-2 reflection review with suspect-source "
        "framing for the headless reflect ensemble."
    ),
    system_prompt_fragment=(
        "You are one reviewer in a heterogeneous Tier-2 reflection ensemble. "
        "Independently audit the target for regressions, drift, missing "
        "verification, and unresolved decisions. Produce concrete findings "
        "with file:line evidence and label high-confidence suspect-source "
        "files for downstream adversarial scoring. "
        + CANONICAL_INJECTION_GUARD_SENTENCE
    ),
    user_template=(
        "Review the following reflect target as an independent Tier-2 "
        "reviewer. Focus on evidence-backed findings, pass/fail signals, "
        "and suspect-source files that the adversarial scorer should treat "
        "with extra scrutiny.\n\n<<<TARGET>>>\n{target_content}\n<<<END TARGET>>>"
    ),
    output_template_path=_TEMPLATE_PATH,
    # `passthrough` preserves the full free-form reviewer body (the bare-review
    # findings-table recipe would truncate reflection reviews to a ~911-byte
    # stub). Keeps the lens config consistent with the ensemble runtime recipe.
    recipe_name="passthrough",
    normalizer_strategy="passthrough",
    default_workers=3,
    default_target_line_cap=4000,
    suspect=True,
    tier="T2",
    recommended_next_command_template=(
        "/sc:adversarial --compare {compare_files} --suspect-source {suspect_files}"
    ),
    acceptance_notes=(
        "Stable reflect-review lens for the FR-RH2 headless ensemble. "
        "Keep {suspect_files} in the next-command template so the "
        "COMP-023 suspect coupling remains satisfied."
    ),
    stability="stable",
)
