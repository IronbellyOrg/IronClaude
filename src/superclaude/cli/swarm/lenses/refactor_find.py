"""``refactor-find`` lens entry (COMP-025 / R-050).

"Smallest cleanups that improve correctness, readability, efficiency."
Experimental T2-code tier, 3 workers, suspect:false. Findings shape
mirrors :data:`recipes.STRATEGIES` ``findings_table_v1``.

Field provenance (roadmap COMP-025 row, line 20)::

    refactor_find lens | Smallest cleanups for correctness/readability/
    efficiency; tier:T2-code; workers:3 | lenses/refactor_find.py |
    entry passes validator; stability:experimental.
"""

from __future__ import annotations

from pathlib import Path

from superclaude.cli.swarm.models import LensEntry
from superclaude.cli.swarm.schema import CANONICAL_INJECTION_GUARD_SENTENCE

__all__ = ["LENS"]


_TEMPLATE_PATH = str(
    (Path(__file__).parent / "templates" / "refactor-find-output.md").resolve()
)


LENS: LensEntry = LensEntry(
    name="refactor-find",
    description=(
        "Surface the smallest cleanups that improve correctness, "
        "readability, or efficiency in the target (COMP-025)."
    ),
    system_prompt_fragment=(
        "You are reviewing the target for the smallest cleanups that "
        "improve correctness, readability, or efficiency. Surface "
        "concrete patch sketches with file:line citations. "
        + CANONICAL_INJECTION_GUARD_SENTENCE
    ),
    user_template=(
        "Surface refactor opportunities in the following target. "
        "Produce a findings table: file:line, cleanup, rationale, "
        "patch sketch.\n\n<<<TARGET>>>\n{target_content}\n<<<END TARGET>>>"
    ),
    output_template_path=_TEMPLATE_PATH,
    recipe_name="findings_table_v1",
    normalizer_strategy="findings_table_v1",
    default_workers=3,
    default_target_line_cap=4000,
    suspect=False,
    tier="T2-code",
    recommended_next_command_template=("/sc:code-review --apply {compare_files}"),
    acceptance_notes=(
        "Experimental lens; graduates to stable after a real caller "
        "wires it in production (spec §3.3)."
    ),
    stability="experimental",
)
