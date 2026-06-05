"""``bare-review`` lens entry (COMP-024 / R-049).

Ports the parent-spec ``sc-bare-review`` SKILL.md framing (v1.3.0-draft)
into the bundled swarm-lens registry: unscaffolded native-instinct
review with suspect-source framing, T2 tier, 3 workers, suspect:true.
This is the only ``stable`` entry at M2; the remaining six built-ins
ship at ``experimental`` and graduate after a real caller wires them in
production (spec §3.3 inventory + §3.4 PR-review discipline).

Field provenance (roadmap COMP-024 row, line 19 of
``.dev/releases/Current/MultiModelSwarm/roadmap.md``)::

    bare_review lens | Unscaffolded native-instinct review lens;
    suspect:true; tier:T2; workers:3 | lenses/bare_review.py |
    entry passes validator; suspect_files in next-cmd template.

The §11.5 injection-guard sentence is appended verbatim to
``system_prompt_fragment`` via
:data:`schema.CANONICAL_INJECTION_GUARD_SENTENCE` so the lens path
agrees with the JSON-Schema and ``--custom-prompt-dir`` paths
byte-for-byte (INV-003 / INV-014 parity, COMP-023 assertion 5).
"""

from __future__ import annotations

from pathlib import Path

from superclaude.cli.swarm.models import LensEntry
from superclaude.cli.swarm.schema import CANONICAL_INJECTION_GUARD_SENTENCE


__all__ = ["LENS"]


_TEMPLATE_PATH = str(
    (Path(__file__).parent / "templates" / "bare-review-output.md").resolve()
)


LENS: LensEntry = LensEntry(
    name="bare-review",
    description=(
        "Unscaffolded native-instinct review with suspect-source "
        "framing. Ports the sc-bare-review v1.3.0-draft skill into "
        "the bundled swarm-lens registry (COMP-024)."
    ),
    system_prompt_fragment=(
        "You are conducting a bare review of the target. Surface "
        "concrete findings with file:line citations and label any "
        "high-confidence suspect-source files. "
        + CANONICAL_INJECTION_GUARD_SENTENCE
    ),
    user_template=(
        "Review the following target and produce a findings table "
        "with severity, file:line, title, evidence, and suspect-source "
        "flag.\n\n<<<TARGET>>>\n{target_content}\n<<<END TARGET>>>"
    ),
    output_template_path=_TEMPLATE_PATH,
    recipe_name="bare-review-v1",
    normalizer_strategy="bare-review-v1",
    default_workers=3,
    default_target_line_cap=4000,
    suspect=True,
    tier="T2",
    recommended_next_command_template=(
        "/sc:adversarial --compare {compare_files} "
        "--suspect-source {suspect_files}"
    ),
    acceptance_notes=(
        "Stable lens. PR-review discipline (NFR-012) applies: extra "
        "scrutiny on suspect:true; ensure {suspect_files} substitution "
        "remains in the next-command template (COMP-023 assertion 3)."
    ),
    stability="stable",
)
