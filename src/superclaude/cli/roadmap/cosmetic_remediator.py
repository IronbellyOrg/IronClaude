"""Cosmetic-failure auto-remediation lane for the roadmap pipeline.

When a roadmap step's gate fails on issues that are *purely cosmetic* (heading
shape, dash variant, whitespace, smart-quotes, table padding, frontmatter
trailing whitespace), this module deterministically rewrites the output into
a gate-passing form and lets the pipeline continue. Failures that include any
*semantic* defect (missing milestone body, missing required H2, unreplaced
``{{SC_PLACEHOLDER:*}}`` sentinel, ``OQ-xxx`` value in a deliverable ID column,
etc.) classify as non-cosmetic and the pipeline halts as before.

The classifier and transformer are pure Python (stdlib only). No LLM is
invoked. All transforms are idempotent: re-running on already-canonical
content is a no-op by construction.

Public surface (consumed by ``cli/pipeline/executor.py``):

- ``classify_gate_failure(content, gate_name, failure_reason, *, step_id)``
  returns a ``Classification`` with ``is_pure_cosmetic`` and per-violation
  evidence.
- ``apply_cosmetic_remediations(content, classification)`` returns a tuple
  ``(rewritten_content, applied_transforms)`` where the second element is a
  list of human-readable transform descriptions suitable for audit log /
  certify-prompt surfacing.

Scope (per the design's "ALL deterministic-fixable drift" decision):

- C1 heading-stem alias (``Risk Assessment`` -> ``Risk Assessment and Mitigation``)
- C2 missing ``-- M{N}`` suffix on a required milestone H3
- C3 wrong dash variant in the suffix (en-dash, ``u2014`` literal, no-break hyphen)
- C4 wrong heading level on a known stem (``##`` or ``####`` -> ``###``)
- C5 trailing whitespace on header lines
- C6 trailing whitespace on any line
- C7 collapsed blank lines (3+ consecutive blanks -> 1)
- C8 smart-quote folding (curly -> straight) outside fenced code blocks
- C9 table cell padding normalization (only on schema-matching tables)
- C10 frontmatter key/value trailing whitespace
- C11 resource-requirements subsection alias (``External Dependencies (PRD-confirmed, TDD-pinned)``
  -> ``External Dependencies``; ``Infrastructure`` -> ``Infrastructure Requirements``)
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

# The required milestone H3 stems, ordered for stable transform output.
# Mirrors ``gates._REQUIRED_MILESTONE_SUBSECTIONS`` plus the optional
# ``open questions`` stem (not gate-required, but normalized for consistency).
_REQUIRED_STEMS_ORDER: tuple[str, ...] = (
    "Integration Points",
    "Milestone Dependencies",
    "Open Questions",
    "Risk Assessment and Mitigation",
)

# Lowercase set for fast membership checks.
_REQUIRED_STEMS_LOWER: frozenset[str] = frozenset(
    s.lower() for s in _REQUIRED_STEMS_ORDER
)

# Short-form aliases that the cosmetic-remediator promotes to canonical form.
# Keyed by the lowercased short form; value is the canonical (correctly-cased)
# stem. The empty-suffix case (e.g. ``### Risk Assessment``) is handled by C2.
_STEM_ALIASES: dict[str, str] = {
    "risk assessment": "Risk Assessment and Mitigation",
    "risks": "Risk Assessment and Mitigation",
    "risk": "Risk Assessment and Mitigation",
    "mitigation": "Risk Assessment and Mitigation",
    "integration": "Integration Points",
    "dependencies": "Milestone Dependencies",
    "milestone deps": "Milestone Dependencies",
    "deps": "Milestone Dependencies",
}

# Resource Requirements and Dependencies subsection canonical names. Used by
# C11 to normalize H3s under ``## Resource Requirements and Dependencies`` to
# the exact spellings the gate requires. Keyed by lowercased substring match
# (so e.g. ``external dependencies (PRD-confirmed, TDD-pinned)`` and
# ``infrastructure`` both promote correctly). Order matters: more-specific
# entries first.
_RESOURCE_SUBSECTION_ALIASES: tuple[tuple[str, str], ...] = (
    ("external dependencies", "External Dependencies"),
    ("external deps", "External Dependencies"),
    ("infrastructure requirements", "Infrastructure Requirements"),
    ("infrastructure", "Infrastructure Requirements"),
    ("infra requirements", "Infrastructure Requirements"),
    ("infra", "Infrastructure Requirements"),
)

# Canonical names for the parent H2 the resource aliases apply under.
_RESOURCE_PARENT_NORMALIZED: str = "resource requirements and dependencies"

# Non-canonical separator characters between stem and ``M{N}``. Includes the
# corrupted ASCII literal ``u2014`` we hit on the TUIBBS run.
_NONCANONICAL_DASH_PATTERN = re.compile(r"(?:u2014|—|–|−|\xa0\-\xa0|\xa0|~)")

# Curly-quote -> straight-quote table for C8.
_SMART_QUOTE_MAP = str.maketrans(
    {
        "‘": "'",  # left single
        "’": "'",  # right single / apostrophe
        "“": '"',  # left double
        "”": '"',  # right double
        "′": "'",  # prime
        "″": '"',  # double prime
    }
)

# Semantic-violation markers. Presence of any of these in a gate failure
# (or detectable in the content) forces ``is_pure_cosmetic=False`` regardless
# of cosmetic findings. These mirror the rules a maintainer would want to
# inspect manually before any auto-fix runs.
_SEMANTIC_MARKERS: tuple[str, ...] = (
    "{{SC_PLACEHOLDER:",  # unreplaced sentinel
)

# Gate names this remediator applies to. The pipeline executor is generic;
# we narrow the remediation surface to known roadmap gates so non-roadmap
# pipelines (sprint, validate) get default halt-on-failure behavior.
_ROADMAP_GATE_NAMES: frozenset[str] = frozenset(
    {
        "template_sections_present",
        "deliverable_table_schema",
        "open_questions_placement",
        "milestone_summary_present",
        "frontmatter_required_fields",
    }
)


@dataclass
class CosmeticViolation:
    """One detected cosmetic defect with its remediation evidence."""

    klass: str  # "C1".."C10"
    description: str  # human-readable, suitable for audit log
    line_number: int | None = None  # 1-based, if locatable
    original: str | None = None  # the offending text, for diff diagnostics


@dataclass
class Classification:
    """Result of classifying a gate failure as cosmetic vs semantic."""

    is_pure_cosmetic: bool
    cosmetic_violations: list[CosmeticViolation] = field(default_factory=list)
    semantic_violations: list[str] = field(default_factory=list)
    gate_name: str = ""
    step_id: str = ""


# --- Helpers --------------------------------------------------------------


def _strip_section_numbering(text: str) -> str:
    """Remove a leading ``N.``, ``N.M.``, ``N.M.K.`` numbering prefix.

    Mirrors ``gates._normalize_heading``'s prefix logic but does not lowercase
    -- the remediator needs to preserve case for transform output.
    """
    return re.sub(r"^\s*\d+(?:\.\d+)*\.?\s+", "", text)


def _h3_stem_and_suffix(heading_text: str) -> tuple[str, str]:
    """Split an H3 heading like ``Foo Bar -- M3`` into (``Foo Bar``, ``-- M3``).

    Tries canonical separators first (``--``, em-dash, ``-``) and then
    non-canonical ones (``u2014`` literal, en-dash, etc.) so a corrupted-
    template heading like ``Foo Bar u2014 M3`` still parses into the same
    (stem, suffix) shape as a clean one. Returns (text, "") when nothing
    separator-like is detectable.
    """
    # Canonical separators first.
    for sep in (" -- ", " — ", " - "):
        if sep in heading_text:
            stem, _, rest = heading_text.partition(sep)
            return stem.strip(), f"{sep.strip()} {rest.strip()}"
    # Non-canonical fallbacks. ``u2014`` is the literal-ASCII corruption we
    # hit on the TUIBBS run; others are visually-similar dashes.
    nc = re.search(r"\s+(?:u2014|—|–|−|\xa0|~)+\s+", heading_text)
    if nc:
        stem = heading_text[: nc.start()].strip()
        rest = heading_text[nc.end() :].strip()
        return stem, f"-- {rest}"
    return heading_text.strip(), ""


def _current_milestone_id(lines: list[str], idx: int) -> str | None:
    """Walk backward from ``idx`` to find the enclosing ``## M{N}:`` H2.

    Returns the integer N as a string (e.g. "3"), or None if no milestone
    H2 precedes the given line.
    """
    h2_re = re.compile(r"^##\s+M(\d+)\s*:", re.IGNORECASE)
    for i in range(idx - 1, -1, -1):
        m = h2_re.match(lines[i])
        if m:
            return m.group(1)
        if lines[i].startswith("# "):  # H1 resets milestone scope
            return None
    return None


def _is_in_fenced_block(lines: list[str], idx: int) -> bool:
    """Return True if line ``idx`` is inside a ``` ... ``` fenced code block."""
    fence_count = 0
    for i in range(idx):
        if lines[i].lstrip().startswith("```"):
            fence_count += 1
    return fence_count % 2 == 1


# --- Classification -------------------------------------------------------


def _detect_semantic_violations(content: str) -> list[str]:
    """Return human-readable semantic violations found in ``content``.

    A non-empty return forces ``is_pure_cosmetic=False`` regardless of any
    cosmetic findings. Conservative on purpose: we'd rather halt and have a
    human look than auto-fix on top of a semantically-broken artifact.
    """
    violations: list[str] = []
    for marker in _SEMANTIC_MARKERS:
        if marker in content:
            count = content.count(marker)
            violations.append(f"unreplaced sentinel {marker!r} ({count} occurrence(s))")

    # OQ-xxx leaking into deliverable rows (ID column = OQ-###).
    oq_in_deliverable_re = re.compile(r"^\|\s*\d+\s*\|\s*OQ-\d+\s*\|", re.MULTILINE)
    oq_matches = oq_in_deliverable_re.findall(content)
    if oq_matches:
        violations.append(
            f"OQ-xxx value in deliverable ID column ({len(oq_matches)} row(s)) "
            "-- decisions are not deliverables"
        )

    return violations


def _detect_cosmetic_violations(content: str) -> list[CosmeticViolation]:
    """Walk the content and emit one CosmeticViolation per detected defect.

    Each detector emits at most one violation per offending line; transforms
    are applied at most once per detected violation in ``_apply_*``. Order is
    line-ascending for deterministic audit output.
    """
    violations: list[CosmeticViolation] = []
    lines = content.splitlines()

    for idx, line in enumerate(lines):
        line_no = idx + 1
        in_fenced = _is_in_fenced_block(lines, idx)

        # C5 trailing whitespace on header lines
        stripped = line.rstrip()
        if (line.lstrip().startswith("#")) and not in_fenced and line != stripped:
            violations.append(
                CosmeticViolation(
                    klass="C5",
                    description=f"trailing whitespace on header line {line_no}",
                    line_number=line_no,
                    original=line,
                )
            )

        # C6 trailing whitespace on any line (skip header -- already covered
        # by C5 -- and fenced-block contents to preserve intentional padding).
        if line != stripped and not in_fenced and not line.lstrip().startswith("#"):
            violations.append(
                CosmeticViolation(
                    klass="C6",
                    description=f"trailing whitespace on line {line_no}",
                    line_number=line_no,
                    original=line,
                )
            )

        # C8 smart-quotes outside fenced code blocks
        if not in_fenced and any(ch in line for ch in "‘’“”′″"):
            violations.append(
                CosmeticViolation(
                    klass="C8",
                    description=f"smart-quote(s) on line {line_no}",
                    line_number=line_no,
                    original=line,
                )
            )

        # C1-C4 milestone H3 defects
        if line.startswith("### ") and not in_fenced:
            heading_body = _strip_section_numbering(line[4:])
            stem, suffix = _h3_stem_and_suffix(heading_body)
            stem_lower = stem.lower()

            mid = _current_milestone_id(lines, idx)
            if mid is None:
                continue  # outside any ## M{N}: scope -- not a milestone H3

            # C3: stem matches a required stem but separator is non-canonical
            if (
                stem_lower in _REQUIRED_STEMS_LOWER
                and _NONCANONICAL_DASH_PATTERN.search(line)
            ):
                violations.append(
                    CosmeticViolation(
                        klass="C3",
                        description=(
                            f"non-canonical dash in milestone H3 at line {line_no}: "
                            f"{heading_body!r}"
                        ),
                        line_number=line_no,
                        original=line,
                    )
                )
                # Don't double-emit C2 for the same line.
                continue

            # C2: stem matches a required stem but no suffix
            if stem_lower in _REQUIRED_STEMS_LOWER and not suffix:
                violations.append(
                    CosmeticViolation(
                        klass="C2",
                        description=(
                            f"missing ` -- M{mid}` suffix on milestone H3 at "
                            f"line {line_no}: {heading_body!r}"
                        ),
                        line_number=line_no,
                        original=line,
                    )
                )
                continue

            # C1: stem is a known alias (e.g. "Risk Assessment" -> "Risk
            # Assessment and Mitigation"). Triggers regardless of suffix.
            if stem_lower in _STEM_ALIASES:
                canonical = _STEM_ALIASES[stem_lower]
                violations.append(
                    CosmeticViolation(
                        klass="C1",
                        description=(
                            f"alias stem {stem!r} -> {canonical!r} on milestone H3 "
                            f"at line {line_no}"
                        ),
                        line_number=line_no,
                        original=line,
                    )
                )
                continue

        # C4 wrong heading level for a known milestone stem (`##` directly
        # under a M{N}: parent, or `####`). Detect after C1-C3 to avoid double
        # emission.
        if (line.startswith("## ") or line.startswith("#### ")) and not in_fenced:
            heading_body = _strip_section_numbering(line.lstrip("#").lstrip())
            stem, _ = _h3_stem_and_suffix(heading_body)
            if stem.lower() in _REQUIRED_STEMS_LOWER:
                mid = _current_milestone_id(lines, idx)
                if mid is not None and not line.startswith("## M"):
                    violations.append(
                        CosmeticViolation(
                            klass="C4",
                            description=(
                                f"wrong heading level for required stem "
                                f"{stem!r} at line {line_no}: should be H3"
                            ),
                            line_number=line_no,
                            original=line,
                        )
                    )

    # C7 collapsed blank lines (whole-file detector, not per-line)
    if re.search(r"\n\n\n\n", content):
        violations.append(
            CosmeticViolation(
                klass="C7",
                description="3+ consecutive blank lines (will collapse to 1)",
            )
        )

    # C9 table cell padding (whole-file detector). Detects pipe-table rows
    # with no leading/trailing space inside cells. Only emits for tables that
    # look like the roadmap's known schemas (9-col deliverable, 7-col risk).
    table_row_re = re.compile(r"^\|([^\n]+)\|$", re.MULTILINE)
    for tm in table_row_re.finditer(content):
        cells = tm.group(1).split("|")
        if len(cells) in (9, 7):  # roadmap deliverable or risk schema
            irregular = any(
                cell != ""  # empty cell is fine
                and (cell[0] != " " or cell[-1] != " ")
                and "---" not in cell  # separator row exempt
                for cell in cells
            )
            if irregular:
                # Single C9 violation summarizing the whole table region is
                # enough -- the transform fixes every row.
                line_no = content[: tm.start()].count("\n") + 1
                violations.append(
                    CosmeticViolation(
                        klass="C9",
                        description=(
                            f"table cell padding irregularity near line {line_no}"
                        ),
                        line_number=line_no,
                    )
                )
                break  # only emit once

    # C10 frontmatter trailing whitespace on values
    if content.startswith("---\n"):
        end = content.find("\n---", 4)
        if end != -1:
            frontmatter = content[4:end]
            for fidx, fline in enumerate(frontmatter.splitlines(), start=2):
                # Line 1 is the opening ---; skip it.
                if ":" in fline and fline != fline.rstrip():
                    violations.append(
                        CosmeticViolation(
                            klass="C10",
                            description=f"frontmatter trailing whitespace at line {fidx}",
                            line_number=fidx,
                            original=fline,
                        )
                    )

    # C11 resource-requirements subsection alias. Under
    # ``## Resource Requirements and Dependencies``, the gate requires H3s
    # spelled exactly ``External Dependencies`` and ``Infrastructure
    # Requirements``. Detect H3s that match a longer/shorter alias and emit
    # C11 so the transformer can normalize.
    h2_re_resource = re.compile(r"^##\s+(.+?)\s*$")
    in_resource_section = False
    for idx, line in enumerate(lines):
        h2m = h2_re_resource.match(line.rstrip("\n"))
        if h2m and not line.startswith("### "):
            h2_text = _strip_section_numbering(h2m.group(1)).lower().strip()
            in_resource_section = h2_text == _RESOURCE_PARENT_NORMALIZED
            continue
        if not in_resource_section:
            continue
        if line.startswith("# "):  # H1 ends the section
            in_resource_section = False
            continue
        if not line.startswith("### "):
            continue
        if _is_in_fenced_block(lines, idx):
            continue
        h3_body = _strip_section_numbering(line[4:]).strip().lower()
        # Already canonical? Skip.
        if h3_body in ("external dependencies", "infrastructure requirements"):
            continue
        # Match against aliases (substring match; most-specific entries first).
        for alias_lower, _canonical in _RESOURCE_SUBSECTION_ALIASES:
            if alias_lower in h3_body:
                violations.append(
                    CosmeticViolation(
                        klass="C11",
                        description=(
                            f"resource-requirements H3 alias at line {idx + 1}: "
                            f"{line.rstrip()!r}"
                        ),
                        line_number=idx + 1,
                        original=line,
                    )
                )
                break

    return violations


def classify_gate_failure(
    content: str,
    gate_name: str,
    failure_reason: str,
    *,
    step_id: str,
) -> Classification:
    """Classify a gate failure as pure-cosmetic, semantic, or mixed.

    The classifier is conservative: any semantic violation forces
    ``is_pure_cosmetic=False`` regardless of cosmetic findings. The remediator
    will refuse to transform a mixed-failure artifact -- the operator should
    address the semantic defect first.

    Gates outside the roadmap domain (e.g. sprint pipeline gates) return
    ``is_pure_cosmetic=False`` immediately so the generic executor stays
    halt-on-any-failure for those pipelines.
    """
    if gate_name not in _ROADMAP_GATE_NAMES:
        return Classification(
            is_pure_cosmetic=False,
            semantic_violations=[
                f"gate {gate_name!r} not in roadmap remediation surface"
            ],
            gate_name=gate_name,
            step_id=step_id,
        )

    semantic = _detect_semantic_violations(content)
    cosmetic = _detect_cosmetic_violations(content)

    is_pure = (not semantic) and bool(cosmetic)
    return Classification(
        is_pure_cosmetic=is_pure,
        cosmetic_violations=cosmetic,
        semantic_violations=semantic,
        gate_name=gate_name,
        step_id=step_id,
    )


# --- Transforms -----------------------------------------------------------


def _apply_milestone_h3_rewrites(content: str) -> tuple[str, list[str]]:
    """Rewrite milestone H3 headings to canonical form.

    Handles C1 (stem aliases), C2 (missing suffix), C3 (dash variants), and
    C4 (wrong heading level) in one pass. Idempotent: a heading already in
    canonical form passes through unchanged.
    """
    transforms: list[str] = []
    lines = content.splitlines(keepends=True)
    h2_re = re.compile(r"^##\s+M(\d+)\s*:", re.IGNORECASE)
    current_mid: str | None = None

    for idx, line in enumerate(lines):
        # Update milestone scope
        m = h2_re.match(line.rstrip("\n"))
        if m:
            current_mid = m.group(1)
            continue
        if line.startswith("# "):
            current_mid = None
            continue
        if current_mid is None:
            continue
        if _is_in_fenced_block(lines, idx):
            continue

        # Match any ##/####/### with a recognized stem fragment. The heading
        # level is not used directly -- C4 will demote/promote anything to ###
        # below via the canonical heading we emit.
        h_match = re.match(r"^(#{2,4})\s+(.+?)\s*$", line.rstrip("\n"))
        if not h_match:
            continue
        body = h_match.group(2)
        body = _strip_section_numbering(body)
        stem, suffix = _h3_stem_and_suffix(body)
        stem_lower = stem.lower()

        canonical_stem: str | None = None
        if stem_lower in _REQUIRED_STEMS_LOWER:
            # Already canonical-spelled
            for canon in _REQUIRED_STEMS_ORDER:
                if canon.lower() == stem_lower:
                    canonical_stem = canon
                    break
        elif stem_lower in _STEM_ALIASES:
            canonical_stem = _STEM_ALIASES[stem_lower]

        if canonical_stem is None:
            continue

        new_heading = f"### {canonical_stem} -- M{current_mid}"
        normalized_line = new_heading + ("\n" if line.endswith("\n") else "")

        if line != normalized_line:
            transforms.append(
                f"H3 normalized at line {idx + 1}: {line.rstrip()!r} -> {new_heading!r}"
            )
            lines[idx] = normalized_line

    return "".join(lines), transforms


def _apply_trailing_whitespace_fix(content: str) -> tuple[str, list[str]]:
    """Strip trailing whitespace from every non-fenced line. Idempotent."""
    transforms: list[str] = []
    lines = content.splitlines(keepends=True)
    changed_lines: list[int] = []
    for idx, line in enumerate(lines):
        if _is_in_fenced_block(lines, idx):
            continue
        # Preserve final newline if present.
        if line.endswith("\n"):
            stripped = line[:-1].rstrip() + "\n"
        else:
            stripped = line.rstrip()
        if stripped != line:
            lines[idx] = stripped
            changed_lines.append(idx + 1)
    if changed_lines:
        transforms.append(
            f"trailing whitespace stripped from {len(changed_lines)} line(s): "
            f"{changed_lines[:5]}{'...' if len(changed_lines) > 5 else ''}"
        )
    return "".join(lines), transforms


def _apply_blank_line_collapse(content: str) -> tuple[str, list[str]]:
    """Collapse 3+ consecutive blank lines to exactly 1. Idempotent."""
    transforms: list[str] = []
    new_content, n = re.subn(r"\n{3,}", "\n\n", content)
    if n > 0:
        transforms.append(f"collapsed multi-blank-line run(s): {n} site(s)")
    return new_content, transforms


def _apply_smart_quote_fold(content: str) -> tuple[str, list[str]]:
    """Fold curly quotes to straight. Skips fenced code blocks."""
    transforms: list[str] = []
    lines = content.splitlines(keepends=True)
    changes = 0
    for idx, line in enumerate(lines):
        if _is_in_fenced_block(lines, idx):
            continue
        folded = line.translate(_SMART_QUOTE_MAP)
        if folded != line:
            lines[idx] = folded
            changes += 1
    if changes > 0:
        transforms.append(f"smart-quotes folded on {changes} line(s)")
    return "".join(lines), transforms


def _apply_table_padding_fix(content: str) -> tuple[str, list[str]]:
    """Normalize pipe-table cell padding on schema-matching tables.

    Only touches tables whose data rows have 9 or 7 cells (roadmap deliverable
    + risk schemas). Leaves other tables untouched so non-roadmap markdown is
    never broken.
    """
    transforms: list[str] = []
    lines = content.splitlines(keepends=True)
    changes = 0
    for idx, line in enumerate(lines):
        if not line.startswith("|"):
            continue
        if _is_in_fenced_block(lines, idx):
            continue
        # Split into cells; strip outer empty caused by leading/trailing pipes
        raw = line.rstrip("\n")
        if not raw.endswith("|"):
            continue
        cells = raw.split("|")[1:-1]
        if len(cells) not in (9, 7):
            continue
        # Separator rows (---|---|...) untouched.
        if all("---" in c or set(c.strip()) <= {"-", ":"} for c in cells):
            continue
        normalized = (
            "|" + "|".join(f" {c.strip()} " if c.strip() else "  " for c in cells) + "|"
        )
        if normalized != raw:
            lines[idx] = normalized + ("\n" if line.endswith("\n") else "")
            changes += 1
    if changes > 0:
        transforms.append(f"table cell padding normalized on {changes} row(s)")
    return "".join(lines), transforms


def _apply_frontmatter_trim(content: str) -> tuple[str, list[str]]:
    """Strip trailing whitespace inside the YAML frontmatter block. Idempotent."""
    transforms: list[str] = []
    if not content.startswith("---\n"):
        return content, transforms
    end = content.find("\n---", 4)
    if end == -1:
        return content, transforms
    fm = content[4:end]
    new_fm_lines: list[str] = []
    changed = 0
    for fline in fm.splitlines():
        rstripped = fline.rstrip()
        if rstripped != fline:
            changed += 1
        new_fm_lines.append(rstripped)
    if changed > 0:
        transforms.append(
            f"frontmatter trailing whitespace stripped on {changed} line(s)"
        )
        new_content = "---\n" + "\n".join(new_fm_lines) + content[end:]
        return new_content, transforms
    return content, transforms


def _apply_resource_subsection_rewrites(content: str) -> tuple[str, list[str]]:
    """Rewrite Resource Requirements H3s to canonical form (C11).

    Walks the document, tracks whether the current section is
    ``## Resource Requirements and Dependencies``, and rewrites any H3 that
    matches an alias (e.g. ``### External Dependencies (PRD-confirmed,
    TDD-pinned)`` -> ``### External Dependencies``; ``### Infrastructure``
    -> ``### Infrastructure Requirements``). Idempotent.
    """
    transforms: list[str] = []
    lines = content.splitlines(keepends=True)
    h2_re = re.compile(r"^##\s+(.+?)\s*$")
    in_resource = False
    for idx, line in enumerate(lines):
        h2m = h2_re.match(line.rstrip("\n"))
        if h2m and not line.startswith("### "):
            h2_text = _strip_section_numbering(h2m.group(1)).lower().strip()
            in_resource = h2_text == _RESOURCE_PARENT_NORMALIZED
            continue
        if line.startswith("# "):
            in_resource = False
            continue
        if not in_resource or not line.startswith("### "):
            continue
        if _is_in_fenced_block(lines, idx):
            continue
        h3_body = _strip_section_numbering(line[4:]).strip()
        h3_lower = h3_body.lower()
        # Already canonical -> skip
        if h3_lower in ("external dependencies", "infrastructure requirements"):
            continue
        for alias_lower, canonical in _RESOURCE_SUBSECTION_ALIASES:
            if alias_lower in h3_lower:
                new_line = f"### {canonical}" + ("\n" if line.endswith("\n") else "")
                if new_line != line:
                    transforms.append(
                        f"resource H3 normalized at line {idx + 1}: "
                        f"{line.rstrip()!r} -> '### {canonical}'"
                    )
                    lines[idx] = new_line
                break
    return "".join(lines), transforms


def apply_cosmetic_remediations(
    content: str,
    classification: Classification,
) -> tuple[str, list[str]]:
    """Apply every transform indicated by ``classification``.

    Returns ``(rewritten_content, applied_transforms)``. When the classification
    is not pure-cosmetic, returns ``(content, [])`` -- the caller is expected
    to check this and halt the pipeline.

    Transforms are applied in a stable order so the output is deterministic:
        1. Milestone H3 rewrites (C1-C4)
        2. Resource-section H3 rewrites (C11)
        3. Trailing whitespace (C5, C6)
        4. Blank-line collapse (C7)
        5. Smart-quote fold (C8)
        6. Table padding (C9)
        7. Frontmatter trim (C10)

    All transforms are idempotent. The function is safe to call twice.
    """
    if not classification.is_pure_cosmetic:
        return content, []

    klasses = {v.klass for v in classification.cosmetic_violations}
    transforms: list[str] = []
    current = content

    if klasses & {"C1", "C2", "C3", "C4"}:
        current, t = _apply_milestone_h3_rewrites(current)
        transforms.extend(t)

    if "C11" in klasses:
        current, t = _apply_resource_subsection_rewrites(current)
        transforms.extend(t)

    if klasses & {"C5", "C6"}:
        current, t = _apply_trailing_whitespace_fix(current)
        transforms.extend(t)

    if "C7" in klasses:
        current, t = _apply_blank_line_collapse(current)
        transforms.extend(t)

    if "C8" in klasses:
        current, t = _apply_smart_quote_fold(current)
        transforms.extend(t)

    if "C9" in klasses:
        current, t = _apply_table_padding_fix(current)
        transforms.extend(t)

    if "C10" in klasses:
        current, t = _apply_frontmatter_trim(current)
        transforms.extend(t)

    return current, transforms


__all__ = [
    "Classification",
    "CosmeticViolation",
    "apply_cosmetic_remediations",
    "classify_gate_failure",
]
