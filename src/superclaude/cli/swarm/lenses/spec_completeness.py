"""``spec-completeness`` lens entry (COMP-027 / R-052).

"What's missing or under-specified in this spec?" Experimental
T2-spec tier, 3 workers, suspect:false.

Field provenance (roadmap COMP-027 row, line 22)::

    spec_completeness lens | "What's missing in this spec?";
    tier:T2-spec; workers:3 | lenses/spec_completeness.py |
    entry passes validator.
"""

from __future__ import annotations

from pathlib import Path

from superclaude.cli.swarm.models import LensEntry
from superclaude.cli.swarm.schema import CANONICAL_INJECTION_GUARD_SENTENCE

__all__ = ["LENS"]


_TEMPLATE_PATH = str(
    (Path(__file__).parent / "templates" / "spec-completeness-output.md").resolve()
)


LENS: LensEntry = LensEntry(
    name="spec-completeness",
    description=(
        "Identify gaps and under-specified sections in the target "
        "specification (COMP-027)."
    ),
    system_prompt_fragment=(
        "You are auditing the target specification for completeness. "
        "Surface missing sections, ambiguous requirements, and "
        "under-specified contracts with section references. "
        + CANONICAL_INJECTION_GUARD_SENTENCE
    ),
    user_template=(
        "Audit the following specification for completeness. Produce "
        "a gap table: section, gap, why it matters, suggested "
        "addition.\n\n<<<TARGET>>>\n{target_content}\n<<<END TARGET>>>"
    ),
    output_template_path=_TEMPLATE_PATH,
    recipe_name="verdict_only_v1",
    normalizer_strategy="verdict_only_v1",
    default_workers=3,
    default_target_line_cap=4000,
    suspect=False,
    tier="T2-spec",
    recommended_next_command_template=("/sc:reflect --merge {compare_files}"),
    acceptance_notes="Experimental lens (spec §3.3).",
    stability="experimental",
)
