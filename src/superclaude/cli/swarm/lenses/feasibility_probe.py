"""``feasibility-probe`` lens entry (COMP-028 / R-053).

"Would this approach actually work?" Experimental T2-feas tier,
3 workers, suspect:false.

Field provenance (roadmap COMP-028 row, line 23)::

    feasibility_probe lens | "Would this approach work?";
    tier:T2-feas; workers:3 | lenses/feasibility_probe.py |
    entry passes validator.
"""

from __future__ import annotations

from pathlib import Path

from superclaude.cli.swarm.models import LensEntry
from superclaude.cli.swarm.schema import CANONICAL_INJECTION_GUARD_SENTENCE

__all__ = ["LENS"]


_TEMPLATE_PATH = str(
    (Path(__file__).parent / "templates" / "feasibility-probe-output.md").resolve()
)


LENS: LensEntry = LensEntry(
    name="feasibility-probe",
    description=(
        "Probe whether the target approach would actually work -- "
        "surface risks, unknowns, and verdicts (COMP-028)."
    ),
    system_prompt_fragment=(
        "You are probing the target approach for feasibility. Surface "
        "concrete risks, unknowns, and supporting/falsifying evidence; "
        "conclude with a feasibility verdict and confidence. "
        + CANONICAL_INJECTION_GUARD_SENTENCE
    ),
    user_template=(
        "Probe the following approach for feasibility. Produce a "
        "concerns table and a one-line verdict.\n\n"
        "<<<TARGET>>>\n{target_content}\n<<<END TARGET>>>"
    ),
    output_template_path=_TEMPLATE_PATH,
    recipe_name="verdict_only_v1",
    normalizer_strategy="verdict_only_v1",
    default_workers=3,
    default_target_line_cap=4000,
    suspect=False,
    tier="T2-feas",
    recommended_next_command_template=("/sc:research --extend {compare_files}"),
    acceptance_notes="Experimental lens (spec §3.3).",
    stability="experimental",
)
