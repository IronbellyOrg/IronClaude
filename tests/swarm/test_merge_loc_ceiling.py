"""T05.02 / T05.08 -- merge.py body LOC ceiling boundary test.

Enforces NFR-008 / AC-018: the body of
``src/superclaude/cli/swarm/merge.py`` must stay at or below 30 lines
of code. The intent is structural: the merge module owns the
caller-facing neutrality boundary (AC-011 / AC-012), and a small body
makes any drift into sort / score / dedup / filter / rewrite obvious
on review.

LOC counting rule (matches the phase-5 validation awk so this test
and the CLI sanity check stay in lockstep)::

    awk '/^\"\"\"/{f=!f; next} !f && NF {c++} END {print c}'

That is:

* Lines that begin (at column 1) with three double-quotes toggle an
  in-docstring flag and are themselves not counted. This means the
  module docstring is excluded.
* Every other non-blank line counts toward the ceiling, including
  imports, the ``def`` line, and the function body.
* Indented in-function docstrings would *not* toggle the flag (the
  regex anchors at column 1); the convention is to keep this module
  docstring-free below the module header.

Any expansion to merge.py that pushes the count past 30 should land
behind a deliberate spec change to NFR-008, not by relaxing this
test.
"""

from __future__ import annotations

from pathlib import Path

import superclaude.cli.swarm.merge as merge_module

LOC_CEILING = 30


def _count_body_loc(source: str) -> int:
    in_module_docstring = False
    count = 0
    for line in source.splitlines():
        if line.startswith('"""'):
            in_module_docstring = not in_module_docstring
            continue
        if in_module_docstring:
            continue
        if line.strip():
            count += 1
    return count


def test_merge_module_body_at_or_below_loc_ceiling() -> None:
    source_path = Path(merge_module.__file__)
    source = source_path.read_text(encoding="utf-8")
    loc = _count_body_loc(source)
    assert loc <= LOC_CEILING, (
        f"merge.py body LOC {loc} exceeds ceiling {LOC_CEILING}. "
        "The mechanical-merge boundary is intentionally tiny -- any growth "
        "must be deliberate and reviewed against AC-011 / AC-012 / NFR-008."
    )


def test_merge_module_loc_counter_excludes_module_docstring() -> None:
    """Sanity-check the counter against a synthetic source."""
    synthetic = (
        '"""one\n'
        'two\n'
        '"""\n'
        '\n'
        'from x import y\n'
        '\n'
        'def f():\n'
        '    return 1\n'
    )
    assert _count_body_loc(synthetic) == 3
