"""``edge-case-hunt`` lens entry (COMP-026 / R-051).

"What inputs / states break this?" Experimental T2-edge tier, **4**
workers (override -- the only built-in besides ``troubleshoot-hypothesis``
to declare default_workers=4 per COMP-026), suspect:false.

Field provenance (roadmap COMP-026 row, line 21)::

    edge_case_hunt lens | "What inputs/states break this?";
    tier:T2-edge; workers:4 | lenses/edge_case_hunt.py |
    entry passes validator; default_workers=4.
"""

from __future__ import annotations

from pathlib import Path

from superclaude.cli.swarm.models import LensEntry
from superclaude.cli.swarm.schema import CANONICAL_INJECTION_GUARD_SENTENCE

__all__ = ["LENS"]


_TEMPLATE_PATH = str(
    (Path(__file__).parent / "templates" / "edge-case-hunt-output.md").resolve()
)


LENS: LensEntry = LensEntry(
    name="edge-case-hunt",
    description=(
        "Probe the target for inputs and states that break it -- "
        "boundary, off-by-one, concurrency, error paths (COMP-026)."
    ),
    system_prompt_fragment=(
        "You are hunting for edge cases that break the target. "
        "Enumerate inputs and states with concrete file:line citations "
        "and a reproduction sketch for each. " + CANONICAL_INJECTION_GUARD_SENTENCE
    ),
    user_template=(
        "Identify edge cases that break the following target. "
        "Produce a findings table: file:line, input/state, why it "
        "breaks, repro sketch.\n\n<<<TARGET>>>\n{target_content}\n"
        "<<<END TARGET>>>"
    ),
    output_template_path=_TEMPLATE_PATH,
    recipe_name="findings_table_v1",
    normalizer_strategy="findings_table_v1",
    default_workers=4,
    default_target_line_cap=4000,
    suspect=False,
    tier="T2-edge",
    recommended_next_command_template=("/sc:adversarial --compare {compare_files}"),
    acceptance_notes=(
        "Experimental lens. default_workers=4 by spec §3.3 -- broader "
        "fan-out raises edge-case coverage."
    ),
    stability="experimental",
)
