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

from ..vocabulary import DISCHARGE_TERMS, SCAFFOLD_TERMS

# Compile patterns
_SCAFFOLD_RE = re.compile("|".join(SCAFFOLD_TERMS), re.IGNORECASE)
_DISCHARGE_RE = re.compile("|".join(DISCHARGE_TERMS), re.IGNORECASE)

# FR-MOD1.7: Exempt comment pattern (OQ-003 resolution: per-line scope)
_EXEMPT_COMMENT_RE = re.compile(r"#\s*obligation-exempt", re.IGNORECASE)

# FR-MOD1.8: Code block detection for severity demotion (OQ-004 resolution)
_CODE_BLOCK_RE = re.compile(r"```[\s\S]*?```")

# --- FR-MOD1.9: Meta-context classification ---

# Layer 1a: Inline code - scaffold term inside backticks (scaffold-aware)
_INLINE_CODE_SCAFFOLD_RE = re.compile(
    r"`[^`]*(?:" + "|".join(SCAFFOLD_TERMS) + r")[^`]*`",
    re.IGNORECASE,
)

# Layer 1b: Completed checklist item
_COMPLETED_CHECKLIST_RE = re.compile(r"^\s*-\s*\[x\]", re.IGNORECASE)

# Layer 2: Negation/meta-context prefix patterns
_NEGATION_PREFIX_RE = re.compile(
    r"(?:"
    r"\b(?:no|not?|never|without|ensure\s+no|verify\s+no|check\s+(?:for\s+)?no|"
    r"must\s+not|should\s+not|shall\s+not|cannot|don'?t|reject|prohibit|forbid|prevent|disallow)\b"
    r"|"
    r"\b(?:removed?|replaced?|eliminated?|deleted?|stripped?|cleaned?|purged?|"
    r"swapped\s+out|migrated\s+away\s+from)\b"
    r"|"
    r"(?:^\s*)(?:risk|warning|caution|danger|caveat|concern)\s*:"
    r"|"
    r"\b(?:verification|gate\s+criteri|check\s+(?:for|that)|validate|assert|audit)\b"
    r")",
    re.IGNORECASE,
)

# Shell command detection (Category 2)
_SHELL_CMD_RE = re.compile(
    r"(?:^\s*[$>]?\s*)?(?:grep|sed|awk|find|rg|ag|git\s+grep|xargs)\b",
    re.IGNORECASE,
)

# Risk/warning line detection
_RISK_WARNING_RE = re.compile(
    r"(?:^\s*)(?:risk|warning|caution|danger|caveat|concern)\s*:",
    re.IGNORECASE,
)

# Gate/verification criteria language
_GATE_CRITERIA_RE = re.compile(
    r"(?:no|zero|0)\s+(?:\w+\s+){0,4}(?:present|found|detected|remaining|allowed|permitted|exist)",
    re.IGNORECASE,
)

# Layer 3a: "Scaffold" as imperative verb in table cell (narrow: scaffold only)
# Matches: "| 2.2.1 | Scaffold command file..." where scaffold is first word after pipe.
# Only "scaffold" has a legitimate dual meaning (verb "create" vs noun "temporary").
# mock/stub/fake/dummy as first words in task cells are genuine obligations.
_TABLE_CELL_IMPERATIVE_RE = re.compile(
    r"^\s*\|[^|]*\|\s*scaffold\s+\w+",
    re.IGNORECASE,
)

# Layer 3b: Parenthetical phase/step label (requires multi-word content)
# Matches: "(command scaffolding)", "(Phase 2 mocking)", "(stubbed layer)" etc.
# Bare "(scaffold)" or "(mock)" stay HIGH — those are genuine qualifiers, not labels.
_PAREN_PHASE_LABEL_RE = re.compile(
    r"\(\s*\w+\s+(?:scaffold(?:ing|ed)?|mock(?:ing|ed)?|stub(?:bing|bed)?)\s*\)"
    r"|"
    r"\(\s*(?:scaffold(?:ing|ed)?|mock(?:ing|ed)?|stub(?:bing|bed)?)\s+\w+\s*\)",
    re.IGNORECASE,
)


# --- FR-MOD1.6: Dataclasses ---


@dataclass
class Obligation:
    """A detected scaffolding obligation."""

    phase: str  # e.g., "Phase 2", "2.3"
    term: str  # the matched scaffold term
    component: str  # nearby component context
    context: str  # surrounding sentence/line
    line_number: int
    severity: str  # "HIGH" or "MEDIUM" (FR-MOD1.8)
    discharged: bool  # True if a matching discharge was found in a later phase
    exempt: bool  # True if line has # obligation-exempt (FR-MOD1.7)
    discharge_phase: str | None  # phase where discharge was found
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

            # FR-MOD1.4: Extract component context (60-char, backtick-priority)
            component = _extract_component_context(phase_content, match.start())

            # FR-MOD1.7: Check for exempt comment on the same line (OQ-003)
            exempt = bool(_EXEMPT_COMMENT_RE.search(context_line))

            # FR-MOD1.8: Determine severity (OQ-004)
            # Calculate absolute position in original content for code-block check
            abs_pos = _get_absolute_position(content, sections, i, match.start())
            severity = _determine_severity(abs_pos, code_block_ranges)

            # Local fallback for compact fenced fixtures inside section slices
            if severity == "HIGH" and _is_inside_code_block(phase_content, match.start()):
                severity = "MEDIUM"

            # Layer 1a: Inline code meta-context
            if severity == "HIGH" and _INLINE_CODE_SCAFFOLD_RE.search(context_line):
                severity = "MEDIUM"
            # Layer 1b: Completed checklist meta-context
            elif severity == "HIGH" and _COMPLETED_CHECKLIST_RE.match(context_line):
                severity = "MEDIUM"
            # Layer 2: Negation/meta-context classification
            elif severity == "HIGH":
                line_start = phase_content.rfind("\n", 0, match.start()) + 1
                term_start_in_line = match.start() - line_start
                if _is_meta_context(context_line, term_start_in_line):
                    severity = "MEDIUM"

            # FR-MOD1.3: Cross-phase discharge search
            discharged = False
            discharge_phase = None
            discharge_context = None

            for j in range(i + 1, len(sections)):
                later_phase_id, later_content, _ = sections[j]
                # FR-MOD1.5: Dual-condition discharge (term + component)
                if _has_discharge(later_content, component, term):
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


# --- FR-MOD1.2: Phase-section parser with H2/H3 fallback ---


def _split_into_phases(content: str) -> list[tuple[str, str, int]]:
    """Split content into (phase_id, text, start_line_number) tuples.

    Splits on H2/H3 headings containing phase-like patterns:
    "## Phase 2", "### 2.3 Executor", "## Step 4", etc.
    Falls back to any H2/H3 heading if no phase-pattern headings found.
    """
    phase_pattern = re.compile(
        r"^(#{2,3})\s+((?:Phase|Step|Stage|Milestone)\s+\d+[\w.]*.*?)$",
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
    """Extract likely component anchor near a scaffold term.

    Uses a 60-char window. Prioritizes backtick-delimited terms,
    then noun phrase around the scaffold term, then capitalized terms,
    then line fallback.
    """
    window_start = max(0, pos - 60)
    window_end = min(len(text), pos + 60)
    window = text[window_start:window_end]

    # Priority 1: backtick-delimited terms
    code_terms = re.findall(r"`([^`]+)`", window)
    if code_terms:
        return code_terms[0].lower()

    # Priority 2: noun phrase after scaffold term (e.g., "stub handler")
    noun_after = re.search(
        r"\b(?:mock(?:ed|s)?|stub(?:bed|s)?|skeleton|placeholder|"
        r"scaffold(?:ing|ed)?|temporary|hardcoded|hardwired|no-?op|dummy|fake)\b"
        r"\s+([a-z][a-z0-9_-]{1,30})",
        window,
        re.IGNORECASE,
    )
    if noun_after:
        return noun_after.group(1).lower()

    # Priority 3: noun phrase before scaffold term (e.g., "service mock")
    noun_before = re.search(
        r"\b([a-z][a-z0-9_-]{1,30})\s+"
        r"(?:mock(?:ed|s)?|stub(?:bed|s)?|skeleton|placeholder|"
        r"scaffold(?:ing|ed)?|temporary|hardcoded|hardwired|no-?op|dummy|fake)\b",
        window,
        re.IGNORECASE,
    )
    if noun_before:
        candidate = noun_before.group(1).lower()
        if candidate not in {"create", "build", "add", "use", "replace", "wire", "ensure"}:
            return candidate

    # Priority 4: capitalized multi-word terms (e.g., "Executor Skeleton")
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


def _is_meta_context(line: str, term_start_in_line: int) -> bool:
    """Determine if a scaffold term on this line is in a meta-context.

    Returns True when the scaffold term appears in a negation, verification,
    historical, risk, shell-command, or gate-criteria context.
    """
    if _SHELL_CMD_RE.search(line):
        return True

    if _RISK_WARNING_RE.match(line):
        return True

    if _GATE_CRITERIA_RE.search(line):
        return True

    prefix = line[:term_start_in_line]
    if _NEGATION_PREFIX_RE.search(prefix):
        return True

    # Layer 3a: Scaffold term as imperative verb in table cell
    if _TABLE_CELL_IMPERATIVE_RE.search(line):
        return True

    # Layer 3b: Scaffold term in parenthetical label
    if _PAREN_PHASE_LABEL_RE.search(line):
        return True

    return False


# --- FR-MOD1.5: Dual-condition discharge matching ---


def _has_discharge(content: str, component: str, term: str = "") -> bool:
    """Check if content contains a discharge term for this obligation.

    Requires a discharge verb and either a component anchor match or a
    scaffold-term match as fallback.
    """
    has_discharge = bool(_DISCHARGE_RE.search(content))
    if not has_discharge:
        return False

    if component and component.lower() in content.lower():
        return True

    if term and re.search(re.escape(term), content, re.IGNORECASE):
        return True

    return False


# --- FR-MOD1.8: Code-block severity demotion ---


def _get_code_block_ranges(content: str) -> list[tuple[int, int]]:
    """Return list of (start, end) positions for code blocks in content."""
    return [(m.start(), m.end()) for m in _CODE_BLOCK_RE.finditer(content)]


def _is_inside_code_block(text: str, pos: int) -> bool:
    """Return True if ``pos`` is inside a fenced code block in ``text``."""
    for m in _CODE_BLOCK_RE.finditer(text):
        if m.start() <= pos <= m.end():
            return True
    return False


def _is_discharge_intent_line(line: str) -> bool:
    """Return True if line clearly states discharge intent, not new scaffolding."""
    return bool(
        re.search(
            r"\b(?:replace|wire\s+(?:up|in|into)|integrat(?:e|ing|ed)|connect|"
            r"swap\s+(?:out|in)|remove|implement\s+real|fill\s+in|complete)\b",
            line,
            re.IGNORECASE,
        )
    )


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
