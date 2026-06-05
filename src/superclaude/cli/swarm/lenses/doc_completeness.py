"""``doc-completeness`` lens entry (COMP-030 / R-055).

"What's missing, unclear, or out-of-date in this doc?" Experimental
T2-doc tier, 3 workers, suspect:false.

Field provenance (roadmap COMP-030 row, line 25)::

    doc_completeness lens | "What's missing in this doc?";
    tier:T2-doc; workers:3 | lenses/doc_completeness.py |
    entry passes validator.
"""

from __future__ import annotations

from pathlib import Path

from superclaude.cli.swarm.models import LensEntry
from superclaude.cli.swarm.schema import CANONICAL_INJECTION_GUARD_SENTENCE


__all__ = ["LENS"]


_TEMPLATE_PATH = str(
    (Path(__file__).parent / "templates" / "doc-completeness-output.md").resolve()
)


LENS: LensEntry = LensEntry(
    name="doc-completeness",
    description=(
        "Audit the target documentation for missing, unclear, or "
        "out-of-date content (COMP-030)."
    ),
    system_prompt_fragment=(
        "You are auditing the target documentation for completeness. "
        "Surface missing sections, unclear explanations, stale "
        "references, and broken links with section anchors. "
        + CANONICAL_INJECTION_GUARD_SENTENCE
    ),
    user_template=(
        "Audit the following documentation for completeness. Produce "
        "a gap table: section, gap kind, issue, suggested fix.\n\n"
        "<<<TARGET>>>\n{target_content}\n<<<END TARGET>>>"
    ),
    output_template_path=_TEMPLATE_PATH,
    recipe_name="findings_table_v1",
    normalizer_strategy="findings_table_v1",
    default_workers=3,
    default_target_line_cap=4000,
    suspect=False,
    tier="T2-doc",
    recommended_next_command_template=(
        "/sc:document --apply {compare_files}"
    ),
    acceptance_notes="Experimental lens (spec §3.3).",
    stability="experimental",
)
