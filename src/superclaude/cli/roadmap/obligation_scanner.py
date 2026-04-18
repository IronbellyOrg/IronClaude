"""Obligation scanner -- detects undischarged scaffolding obligations in roadmaps.

Scans roadmap content for scaffolding terms (mock, stub, skeleton, placeholder,
scaffold, temporary, hardcoded) that create implicit obligations, then verifies
each obligation has a corresponding discharge term (replace, wire, integrate,
connect, implement real, remove mock, swap) in a later phase.

Pure function: content in, findings out. No I/O.

Implements FR-MOD1.1 through FR-MOD1.8.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


# --- FR-MOD1.1: Obligation vocabulary (11 scaffold terms) ---

SCAFFOLD_TERMS = [
    r"\bmock(?:ed|s)?\b",
    r"\bstub(?:bed|s)?\b",
    r"\bskeleton\b",
    r"\bplaceholder\b",
    r"\bscaffold(?:ing|ed)?\b",
    r"\btemporary\b",
    r"\bhardcoded\b",
    r"\bhardwired\b",
    r"\bno-?op\b",
    r"\bdummy\b",
    r"\bfake\b",
]

# Terms that DISCHARGE an obligation (something fulfilled)
DISCHARGE_TERMS = [
    r"\breplace\b",
    r"\bwire\s+(?:up|in|into)\b",
    r"\bintegrat(?:e|ing|ed)\b",
    r"\bconnect\b",
    r"\bswap\s+(?:out|in)\b",
    r"\bremove\s+(?:mock|stub|placeholder|scaffold)\b",
    r"\bimplement\s+real\b",
    r"\bfill\s+in\b",
    r"\bcomplete\s+(?:the\s+)?(?:skeleton|scaffold)\b",
]

# Compile patterns
_SCAFFOLD_RE = re.compile("|".join(SCAFFOLD_TERMS), re.IGNORECASE)
_DISCHARGE_RE = re.compile("|".join(DISCHARGE_TERMS), re.IGNORECASE)

# FR-MOD1.7: Exempt comment pattern (OQ-003 resolution: per-line scope)
_EXEMPT_COMMENT_RE = re.compile(r"#\s*obligation-exempt", re.IGNORECASE)

# FR-MOD1.8: Code block detection for severity demotion (OQ-004 resolution)
_CODE_BLOCK_RE = re.compile(r"```[\s\S]*?```")


# --- FR-MOD1.6: Dataclasses ---


@dataclass
class Obligation:
    """A detected scaffolding obligation."""

    phase: str  # e.g., "M2", "2.3"
    term: str  # the matched scaffold term
    component: str  # nearby component context
    context: str  # surrounding sentence/line
    line_number: int
    severity: str  # "HIGH" or "MEDIUM" (FR-MOD1.8)
    discharged: bool  # True if a matching discharge was found in a later milestone
    exempt: bool  # True if line has # obligation-exempt (FR-MOD1.7)
    discharge_phase: str | None  # milestone where discharge was found
    discharge_context: str | None


@dataclass
class ObligationReport:
    """Result of obligation scanning."""

    total_obligations: int
    discharged: int
    undischarged: int
    obligations: list[Obligation]

    @property
    def undischarged_count(self) -> int:
        """Count of undischarged obligations excluding MEDIUM severity and exempt.

        Per OQ-004: MEDIUM severity obligations (code-block context) are excluded.
        Per OQ-003: Exempt obligations are excluded.
        """
        return sum(
            1
            for o in self.obligations
            if not o.discharged and not o.exempt and o.severity != "MEDIUM"
        )

    @property
    def has_undischarged(self) -> bool:
        return self.undischarged_count > 0


def scan_obligations(content: str) -> ObligationReport:
    """Scan roadmap content for scaffolding obligations and discharge status.

    Algorithm:
    1. Parse content into phase-delimited sections (FR-MOD1.2: H2/H3 fallback).
    2. For each section, find all scaffold terms (FR-MOD1.1).
    3. For each scaffold term, extract component context (FR-MOD1.4).
    4. Search ALL subsequent sections for discharge (FR-MOD1.3, FR-MOD1.5).
    5. Check for exempt comments (FR-MOD1.7) and code-block demotion (FR-MOD1.8).
    6. Report undischarged obligations.

    Returns an ObligationReport with all findings.
    """
    # Pre-compute code block ranges for severity demotion
    code_block_ranges = _get_code_block_ranges(content)

    sections = _split_into_phases(content)
    obligations: list[Obligation] = []

    for i, (phase_id, phase_content, start_line) in enumerate(sections):
        for match in _SCAFFOLD_RE.finditer(phase_content):
            term = match.group()
            context_line = _get_context_line(phase_content, match.start())
            abs_line = start_line + phase_content[: match.start()].count("\n")

            # Skip markdown headings — section titles are document structure,
            # not scaffolding obligations. Also skip table header/separator lines.
            # IMPORTANT: Only skip lines that look like actual markdown headings
            # (## or ### followed by space), NOT Python comments (# comment)
            # which may appear inside code blocks.
            stripped_context = context_line.lstrip()
            if (
                (stripped_context.startswith("## ") or stripped_context.startswith("### "))
                or stripped_context.startswith("|")
            ):
                continue

            # Skip phase objective paragraphs — these are declarative
            # descriptions of phase goals (e.g., "**Objective:** ...scaffold
            # orchestrator interfaces..."), not prescriptive scaffolding
            # actions that create discharge obligations.
            if stripped_context.startswith("**Objective:"):
                continue

            # Skip scaffold terms that appear in purely descriptive/configuration
            # contexts rather than indicating temporary implementations needing
            # replacement. Rich roadmaps (TDD+PRD enriched) use these words
            # descriptively far more than simple spec-only roadmaps.
            ctx_lower = context_line.lower()

            # "skeleton" in a phase objective as a noun phrase (e.g., "layered
            # service skeleton", "project skeleton") is descriptive architecture,
            # not a temporary implementation. Only flag when used as a direct
            # object of an imperative verb (e.g., "Build skeleton", "Create
            # skeleton") which suggests intentional scaffolding work.
            if term.lower() == "skeleton":
                # Check for imperative verb before "skeleton" suggesting action
                imperative_before = re.search(
                    r"\b(?:build|create|set\s+up|generate|write|add)\s+\w*\s*"
                    + re.escape(term),
                    context_line,
                    re.IGNORECASE,
                )
                if not imperative_before:
                    continue

            # "hardcoded" describing a deliberate config value (e.g.,
            # "bcrypt cost factor (12)" or "hardcoded default") is not an obligation.
            if term.lower().startswith("hardcod"):
                if any(
                    w in ctx_lower
                    for w in (
                        "cost factor",
                        "configuration",
                        "config",
                        "default",
                        "cost",
                        "environment",
                        "setting",
                        "static",
                        "constant",
                    )
                ):
                    continue

            # FR-MOD1.4: Extract component context (60-char, backtick-priority)
            component = _extract_component_context(phase_content, match.start())

            # FR-MOD1.7: Check for exempt comment on the same line (OQ-003)
            exempt = bool(_EXEMPT_COMMENT_RE.search(context_line))

            # FR-MOD1.8: Determine severity (OQ-004)
            # Calculate absolute position in original content for code-block check
            abs_pos = _get_absolute_position(content, sections, i, match.start())
            severity = _determine_severity(abs_pos, code_block_ranges)

            # FR-MOD1.3: Cross-phase discharge search
            discharged = False
            discharge_phase = None
            discharge_context = None

            for j in range(i + 1, len(sections)):
                later_phase_id, later_content, _ = sections[j]
                # FR-MOD1.5: Dual-condition discharge (term + component)
                if _has_discharge(later_content, component):
                    discharged = True
                    discharge_phase = later_phase_id
                    discharge_match = _DISCHARGE_RE.search(later_content)
                    if discharge_match:
                        discharge_context = _get_context_line(
                            later_content, discharge_match.start()
                        )
                    break

            obligations.append(
                Obligation(
                    phase=phase_id,
                    term=term,
                    component=component,
                    context=context_line,
                    line_number=abs_line,
                    severity=severity,
                    discharged=discharged,
                    exempt=exempt,
                    discharge_phase=discharge_phase,
                    discharge_context=discharge_context,
                )
            )

    undischarged_count = sum(1 for o in obligations if not o.discharged)
    return ObligationReport(
        total_obligations=len(obligations),
        discharged=len(obligations) - undischarged_count,
        undischarged=undischarged_count,
        obligations=obligations,
    )


# --- FR-MOD1.2: Milestone-section parser with H2/H3 fallback ---


def _split_into_phases(content: str) -> list[tuple[str, str, int]]:
    """Split content into (phase_id, text, start_line_number) tuples.

    Splits on H2/H3 headings containing milestone-like patterns:
    "## M2: Title", "## Phase 2", "### 2.3 Executor", "## Step 4", etc.
    Falls back to any H2/H3 heading if no milestone-pattern headings found.
    """
    phase_pattern = re.compile(
        r"^(#{2,3})\s+((?:(?:Phase|Step|Stage|Milestone)\s+|M)\d+[\w.]*.*?)$",
        re.MULTILINE | re.IGNORECASE,
    )
    matches = list(phase_pattern.finditer(content))

    if not matches:
        # Fallback: split on any H2/H3 heading
        fallback_pattern = re.compile(r"^(#{2,3})\s+(.+?)$", re.MULTILINE)
        matches = list(fallback_pattern.finditer(content))

    if not matches:
        # Final fallback: treat whole content as one section
        return [("entire-document", content, 1)]

    sections: list[tuple[str, str, int]] = []
    for i, m in enumerate(matches):
        phase_id = m.group(2).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        start_line = content[: m.start()].count("\n") + 1
        sections.append((phase_id, content[start:end], start_line))

    return sections


# --- FR-MOD1.4: Component context extraction (60-char, backtick-priority) ---


def _extract_component_context(text: str, pos: int) -> str:
    """Extract likely component name near a scaffold term.

    Uses a 60-char window. Prioritizes backtick-delimited terms,
    falls back to capitalized multi-word terms, then to the line context.
    """
    window_start = max(0, pos - 60)
    window_end = min(len(text), pos + 60)
    window = text[window_start:window_end]

    # Priority 1: backtick-delimited terms
    code_terms = re.findall(r"`([^`]+)`", window)
    if code_terms:
        return code_terms[0].lower()

    # Priority 2: capitalized multi-word terms (e.g., "Executor Skeleton")
    cap_terms = re.findall(r"[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*", window)
    if cap_terms:
        return cap_terms[0].lower()

    # Fallback: the whole line context
    return _get_context_line(text, pos).lower()


def _get_context_line(text: str, pos: int) -> str:
    """Extract the line containing position `pos`."""
    start = text.rfind("\n", 0, pos) + 1
    end = text.find("\n", pos)
    if end == -1:
        end = len(text)
    return text[start:end].strip()


# --- FR-MOD1.5: Dual-condition discharge matching ---


def _has_discharge(content: str, component: str) -> bool:
    """Check if content contains a discharge term referencing the component.

    Dual-condition: requires both a discharge verb AND a reference to the
    component name. If no component context is available, falls back to
    checking for any discharge term.
    """
    if not component:
        return bool(_DISCHARGE_RE.search(content))

    has_discharge = bool(_DISCHARGE_RE.search(content))
    has_component = component.lower() in content.lower()
    return has_discharge and has_component


# --- FR-MOD1.8: Code-block severity demotion ---


def _get_code_block_ranges(content: str) -> list[tuple[int, int]]:
    """Return list of (start, end) positions for code blocks in content."""
    return [(m.start(), m.end()) for m in _CODE_BLOCK_RE.finditer(content)]


def _determine_severity(
    abs_pos: int, code_block_ranges: list[tuple[int, int]]
) -> str:
    """Determine severity based on whether position is inside a code block.

    Per OQ-004: scaffold terms inside code blocks are MEDIUM severity.
    """
    for start, end in code_block_ranges:
        if start <= abs_pos <= end:
            return "MEDIUM"
    return "HIGH"


def _get_absolute_position(
    content: str,
    sections: list[tuple[str, str, int]],
    section_idx: int,
    relative_pos: int,
) -> int:
    """Convert a relative position within a section to absolute content position."""
    _, section_text, _ = sections[section_idx]
    # Find where this section's text starts in the original content
    section_start = content.find(section_text)
    if section_start == -1:
        return relative_pos  # fallback
    return section_start + relative_pos
