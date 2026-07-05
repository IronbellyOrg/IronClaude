"""``troubleshoot-hypothesis`` lens entry (COMP-029 / R-054).

"Given this failure, what's the most likely root cause?" Experimental
T2-tshoot tier, **4** workers (the second of two built-ins -- with
``edge-case-hunt`` -- that override default_workers to 4 per
COMP-029), suspect:false.

Field provenance (roadmap COMP-029 row, line 24)::

    troubleshoot_hypothesis lens | "Most likely root cause?";
    tier:T2-tshoot; workers:4 | lenses/troubleshoot_hypothesis.py |
    entry passes validator; default_workers=4.
"""

from __future__ import annotations

from pathlib import Path

from superclaude.cli.swarm.models import LensEntry
from superclaude.cli.swarm.schema import CANONICAL_INJECTION_GUARD_SENTENCE

__all__ = ["LENS"]


_TEMPLATE_PATH = str(
    (
        Path(__file__).parent / "templates" / "troubleshoot-hypothesis-output.md"
    ).resolve()
)


LENS: LensEntry = LensEntry(
    name="troubleshoot-hypothesis",
    description=(
        "Given a failure or symptom, enumerate ranked root-cause "
        "hypotheses with supporting and falsifying evidence "
        "(COMP-029)."
    ),
    system_prompt_fragment=(
        "You are enumerating root-cause hypotheses for the failure or "
        "symptom in the target. Rank by likelihood; for each, surface "
        "supporting evidence, falsifying evidence, and the next probe. "
        + CANONICAL_INJECTION_GUARD_SENTENCE
    ),
    user_template=(
        "Enumerate ranked root-cause hypotheses for the failure in the "
        "following target. Produce a hypothesis table.\n\n"
        "<<<TARGET>>>\n{target_content}\n<<<END TARGET>>>"
    ),
    output_template_path=_TEMPLATE_PATH,
    recipe_name="hypothesis_table_v1",
    normalizer_strategy="hypothesis_table_v1",
    default_workers=4,
    default_target_line_cap=4000,
    suspect=False,
    tier="T2-tshoot",
    recommended_next_command_template=(
        "/sc:troubleshoot --merge-hypotheses {compare_files}"
    ),
    acceptance_notes=(
        "Experimental lens. default_workers=4 by spec §3.3 -- broader "
        "fan-out raises hypothesis diversity."
    ),
    stability="experimental",
)
