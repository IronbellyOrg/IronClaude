"""Shared compiled regexes and filename construction helpers for prd CLI
Stage B artifacts.

Used by ``prompts.py`` when writing artifacts (filename construction) and by
``executor.py`` when detecting them on disk for resume-skip. Keeping the
patterns in one module ensures the writing side and the detection side cannot
drift apart — a rename only has to happen here.
"""

from __future__ import annotations

import re

# Detection regexes — match a bare filename (``Path.name``), not a full path.
INVESTIGATION_FILENAME_RE = re.compile(r"^\d{2}-.+\.md$")
WEB_RESEARCH_FILENAME_RE = re.compile(r"^web-\d{2}-.+\.md$")
SYNTHESIS_FILENAME_RE = re.compile(r"^synth-\d{2}-.+\.md$")


def investigation_filename(idx: int, slug: str) -> str:
    """Return the canonical investigation research filename."""
    return f"{idx:02d}-{slug}.md"


def web_research_filename(idx: int, slug: str) -> str:
    """Return the canonical web-research filename."""
    return f"web-{idx:02d}-{slug}.md"


def synthesis_filename(entry_synth_file: str) -> str:
    """Return the synthesis filename.

    Identity helper: the synthesis mapping already provides names in
    ``synth-NN-*.md`` form. Routing the call site through this helper gives a
    single grep-able choke point so the writing side stays coupled to
    ``SYNTHESIS_FILENAME_RE``.
    """
    return entry_synth_file
