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

# Tail-section headings — MUST stay in sync with gates._REQUIRED_H2_SECTIONS.
# Imported at module load to avoid drift; no circular-import risk because
# gates.py does not import obligation_scanner.
from superclaude.cli.roadmap.gates import (  # noqa: E402
    _REQUIRED_H2_SECTIONS as _TAIL_SECTION_HEADINGS,
)
from superclaude.cli.roadmap.gates import (  # noqa: E402
    _normalize_heading,
)
from superclaude.cli.vocabulary import DISCHARGE_TERMS, SCAFFOLD_TERMS

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

# Layer 3 (Stage 2) — table-row classification:
# Matches markdown table SEPARATOR rows only (e.g., `|---|---|`,
# `| :--- | ---: |`, `| :---: |`). Data rows like
# `| 2.2.1 | Scaffold cmd | FR-001 |` must NOT match — they should reach
# Layer 3a/3b detectors. The old `stripped_context.startswith("|")` guard
# at scan_obligations() collapsed BOTH separator and data rows into the
# `continue` branch, killing Layer 3 reachability for table-cell fixtures.
_TABLE_SEPARATOR_RE = re.compile(r"^\s*\|(\s*:?-+:?\s*\|)+\s*$")

# Layer 4 (Fix 3): descriptor nouns adjacent to scaffold terms signal
# descriptive/historical/fallback prose, not prescriptive scaffolding.
# Used by `_is_descriptive_context` to demote scaffold-term findings sitting
# inside per-milestone Risk Assessment / Mitigation subsections, External
# Dependencies tables, etc. A line that ALSO matches discharge intent
# (`_is_discharge_intent_line`) is NOT demoted — that protects real
# obligations like "outcome: scaffold needs replacement".
_DESCRIPTOR_NOUNS = frozenset(
    {
        "outcome",
        "result",
        "behavior",
        "behaviour",
        "property",
        "mitigation",
        "fallback",
        "dependency",
        "consideration",
        "historical",
        "legacy",
        "prior",
        "existing",
    }
)
_DESCRIPTOR_ADJACENCY_RE = re.compile(
    r"\b(" + "|".join(_DESCRIPTOR_NOUNS) + r")\b",
    re.IGNORECASE,
)

# Layer 5: H3 subsection-context demotion prefixes. A scaffold-term finding
# whose containing H3 heading (lowercased, with trailing " — M{n}" stripped)
# starts with one of these prefixes is demoted from HIGH to MEDIUM, unless
# the line itself matches discharge intent. Tuple not frozenset — order is
# stable for diagnostic reproducibility and prefix-match `any(...startswith)`
# semantics make set-vs-tuple equivalent for correctness.
_DEMOTED_H3_SUBSECTIONS: tuple[str, ...] = (
    "risk assessment",
    "integration points",
    "milestone dependencies",
    "open questions",
)

# Layer 6 (R0.2 — Contract #10): Anti-instinct phrase allowlist.
# A SCAFFOLD-term match whose context line contains one of these allowlist
# phrases is SKIPPED entirely (not demoted to MEDIUM) — these phrases refer
# to named permanent test fixtures and architectural module paths, not
# scaffolding obligations.
#
# Seed authority (no fabricated entries):
#   - BUILD-REQUEST §R0 item 2 (verbatim "stub transport",
#     "stub-worker parallelism test")
#   - .dev/releases/Current/MultiModelSwarm/anti-instinct-remediation.md §1
#     (6 FP instances at roadmap.md lines 207, 211, 213 — pre-fix prose)
#   - master:§Recurrence #6 (scaffold-vocabulary FP class)
#   - Contract #10 (≥3 known-false-positive fixtures from documented
#     historical recurrences)
#
# Addition criteria — a phrase belongs here ONLY when:
#   1. It traces to a documented historical incident (no speculative entries).
#   2. A negative-test fixture (`valid_obligation_case.md`) proves the
#      allowlist did not silently mask a real obligation.
#   3. A unit test in `test_anti_instinct_recurrence.py` asserts the new
#      phrase is matched verbatim and `test_allowlist_provenance` confirms
#      this comment block still cites Contract #10.
#
# R1.3: move to superclaude.contracts.vocabulary._ANTI_INSTINCT_ALLOWLIST_PHRASES.
_ALLOWLIST_PHRASES: frozenset[str] = frozenset(
    {
        "stub transport",
        "deterministic stub for tests",
        "deterministic stub transport for tests",
        "stub-worker parallelism test",
        "transports/stub.py",
    }
)

# Layer 5: H3 / H2 boundary regexes for the pre-scan `_build_h3_index`.
# `_H3_HEADING_RE` captures the H3 heading text (non-greedy, MULTILINE-anchored
# per line); `_H2_HEADING_RE` is boundary-only (no capture) — it resets the
# current-H3 state inside `_build_h3_index` when a new milestone starts.
_H3_HEADING_RE = re.compile(r"^###\s+(.+?)$", re.MULTILINE)
_H2_HEADING_RE = re.compile(r"^##\s+.+?$", re.MULTILINE)


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
    # Pre-compute line → containing H3 index for Layer 5 subsection demotion
    h3_index = _build_h3_index(content)

    sections = _split_into_phases(content)
    obligations: list[Obligation] = []

    for i, (phase_id, phase_content, start_line) in enumerate(sections):
        for match in _SCAFFOLD_RE.finditer(phase_content):
            term = match.group()
            context_line = _get_context_line(phase_content, match.start())
            abs_line = start_line + phase_content[: match.start()].count("\n")

            # Layer 6 (R0.2 — Contract #10): Anti-instinct phrase allowlist.
            # A SCAFFOLD-term match whose context line contains a documented
            # permanent-fixture phrase (e.g. "stub transport",
            # "transports/stub.py") is SKIPPED entirely — these are named
            # architectural artifacts, not scaffolding obligations.
            # See `_ALLOWLIST_PHRASES` docstring for the seed authority
            # (BUILD-REQUEST §R0 item 2, master:§Recurrence #6) and the
            # addition criteria. Negative-test guard: every entry has a
            # paired `valid_obligation_case` test that proves no real
            # obligation is masked (Step 3.4 / Step 3.5).
            if _is_allowlisted(context_line):
                continue

            # Skip markdown headings — section titles are document structure,
            # not scaffolding obligations. Also skip table header/separator lines.
            # IMPORTANT: Only skip lines that look like actual markdown headings
            # (## or ### followed by space), NOT Python comments (# comment)
            # which may appear inside code blocks.
            stripped_context = context_line.lstrip()
            if (
                stripped_context.startswith("## ")
                or stripped_context.startswith("### ")
            ) or _TABLE_SEPARATOR_RE.match(stripped_context):
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

            # "scaffold(ing|ed)?" is often used descriptively to mean "the work
            # being done during a phase" or to describe ownership ("team owns
            # scaffolding"), not as a literal scaffold that must be wired up
            # later. Only flag when used as the direct object of an imperative
            # verb (e.g., "Build scaffolding", "Set up scaffolding", "Stand up
            # scaffolding") which indicates a deliberate temporary artifact.
            #
            # T3.3 gate-reorder: consult ``_is_meta_context`` FIRST. When the
            # term sits inside a Layer 3a table cell (`|...| Scaffold X |`),
            # a Layer 3b parenthetical phase label (`(command scaffolding)`),
            # or a shell/negation/risk meta-context, let it through to be
            # demoted to MEDIUM downstream. Only fire the imperative-verb
            # `continue` when we're outside any meta-context, which preserves
            # the original descriptive-prose suppression contract (commit
            # 4799719).
            #
            # T3.1 regex widening: the imperative regex now tolerates an
            # optional single bracket character between the verb and the
            # scaffold term so fixtures like `Build the (scaffold) component`
            # surface a HIGH obligation as Layer 3b's docstring contract at
            # `_PAREN_PHASE_LABEL_RE` (bare parenthetical) requires.
            if term.lower().startswith("scaffold"):
                line_start = phase_content.rfind("\n", 0, match.start()) + 1
                term_start_in_line = match.start() - line_start
                if not _is_meta_context(context_line, term_start_in_line):
                    imperative_before = re.search(
                        r"\b(?:build|create|set\s+up|generate|write|add|implement|stand\s+up)\s+(?:\w+\s+)?[\(\[\"'`]?"
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

            # Local fallback for compact fenced fixtures inside section slices
            if severity == "HIGH" and _is_inside_code_block(
                phase_content, match.start()
            ):
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

            # Layer 5: H3 subsection-context demotion. Scaffold-term findings
            # whose containing H3 starts with one of the demote-target prefixes
            # (Risk Assessment, Integration Points, Milestone Dependencies,
            # Open Questions) are demoted to MEDIUM. The `if severity == "HIGH"`
            # guard makes this a no-op when prior layers already demoted; the
            # `_is_discharge_intent_line` guard mirrors Layer 4 and preserves
            # genuine obligations like "stub needs replacement" inside RAM.
            if severity == "HIGH":
                h3_text = h3_index.get(abs_line, "")
                if _is_demoted_h3(h3_text) and not _is_discharge_intent_line(
                    context_line
                ):
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


# --- FR-MOD1.2: Milestone-section parser with H2/H3 fallback ---


def _find_tail_section_start(content: str, search_start: int, hard_end: int) -> int:
    """Return position of first tail-section H2 in [search_start, hard_end], else hard_end.

    Tail sections (Risk Register, Decision Summary, etc.) are template-prescribed
    H2s that appear AFTER the last milestone. Without this guard, a scaffold term
    in such a section gets absorbed into the last milestone and becomes
    structurally undischargeable (Fix 1 — fixes 5 of 6 false positives).

    The heading set is sourced from ``gates._REQUIRED_H2_SECTIONS`` to keep
    coupling tight: any rename in the template breaks BOTH gates at once.
    """
    for m in re.finditer(r"^##\s+(.+?)$", content[search_start:hard_end], re.MULTILINE):
        heading = _normalize_heading(m.group(1))
        if heading in _TAIL_SECTION_HEADINGS:
            return search_start + m.start()
    return hard_end


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
        next_milestone_end = (
            matches[i + 1].start() if i + 1 < len(matches) else len(content)
        )
        # Fix 1: terminate each milestone section at the earlier of the next
        # milestone or the first template-tail H2 (Risk Register, Decision
        # Summary, etc.). This prevents tail-section content from being
        # absorbed into the last milestone, where it would be structurally
        # undischargeable.
        tail_section_start = _find_tail_section_start(
            content, start, next_milestone_end
        )
        end = min(next_milestone_end, tail_section_start)
        start_line = content[: m.start()].count("\n") + 1
        sections.append((phase_id, content[start:end], start_line))

    return sections


# --- FR-MOD1.4: Component context extraction (60-char, backtick-priority) ---

# Field-label words that commonly begin Markdown list items or table cells
# in roadmaps. These are document metadata, not component names — a scaffold
# obligation whose component is resolved to one of these is nearly always
# impossible to discharge because the word won't reappear in later milestones'
# technical content.
_FIELD_LABELS = frozenset(
    {
        "personnel",
        "decisions",
        "external",
        "owner",
        "owners",
        "objective",
        "objectives",
        "deliverables",
        "deliverable",
        "dependencies",
        "dependency",
        "risks",
        "risk",
        "mitigation",
        "mitigations",
        "scope",
        "assumptions",
        "assumption",
        "notes",
        "note",
        "blockers",
        "blocker",
        "approvers",
        "approver",
        "stakeholders",
        "stakeholder",
    }
)

# Matches a Markdown list-item field label at the start of a line,
# after optional list markers and emphasis:  "- **Personnel:** ...",
# "* Decisions:", "Owner: ...". Captures the label word (without colon).
_FIELD_LABEL_LINE_RE = re.compile(
    r"^\s*(?:[-*>|]\s+)?\**\s*([A-Z][A-Za-z][A-Za-z ]*?)\**\s*:\s",
)


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
        if candidate not in {
            "create",
            "build",
            "add",
            "use",
            "replace",
            "wire",
            "ensure",
        }:
            return candidate

    # Priority 4: capitalized multi-word terms (e.g., "Executor Skeleton"),
    # rejecting common field-label words and the line's own label prefix
    # (e.g., the "Personnel" in "Personnel: auth-team owns scaffolding").
    # Restoring three local-variable assignments dropped by merge commit
    # 3ac7bb6 — see f336da1:src/superclaude/cli/roadmap/obligation_scanner.py
    # lines 358-360 for the original source.
    line = _get_context_line(text, pos)
    label_match = _FIELD_LABEL_LINE_RE.match(line)
    line_label = label_match.group(1).strip().lower() if label_match else None

    cap_terms = re.findall(r"[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*", window)
    for term in cap_terms:
        t = term.strip().lower()
        if not t:
            continue
        if line_label and t == line_label:
            continue
        if t in _FIELD_LABELS:
            continue
        return t

    # Fallback: the whole line context
    return line.lower()


def _get_context_line(text: str, pos: int) -> str:
    """Extract the line containing position `pos`."""
    start = text.rfind("\n", 0, pos) + 1
    end = text.find("\n", pos)
    if end == -1:
        end = len(text)
    return text[start:end].strip()


def _is_descriptive_context(line: str, term_start_in_line: int) -> bool:
    """True when a scaffold term sits within ~4 words of a descriptor noun AND
    the line does NOT signal discharge intent.

    Fix 3: catches descriptive-prose contexts like
    ``(no-op outcome)``, ``stub-tested mitigation``, ``legacy stub retained``
    that the parenthetical-phrase Layer 3b misses. The discharge-intent guard
    ensures lines like ``outcome: scaffold needs replacement`` (a real
    obligation) remain HIGH.

    Window heuristic: ~40 chars on each side of the term covers ~4 short
    English words, which matches the prose density of roadmap risk tables.
    """
    if _is_discharge_intent_line(line):
        return False
    window_start = max(0, term_start_in_line - 40)
    window_end = min(len(line), term_start_in_line + 40)
    window = line[window_start:window_end]
    return bool(_DESCRIPTOR_ADJACENCY_RE.search(window))


def _normalize_h3_for_match(h3_text: str) -> str:
    """Lowercase the H3 heading after stripping the trailing " — M{n}" suffix.

    Roadmap convention: per-milestone H3 subsections carry a ` — M{n}`
    decoration that ties them to their enclosing milestone, e.g.
    ``### Risk Assessment and Mitigation — M2``. The Layer 5 prefix match
    operates on the bare subsection name only, so this helper strips the
    decoration before lowercasing.

    Tolerates BOTH the em-dash U+2014 (the real roadmap convention) and the
    ascii hyphen-minus, and accepts the alphanumeric milestone suffix
    variants ``M8a`` / ``M8b`` via ``M\\d+\\w*``.
    """
    return re.sub(
        r"\s+[—-]\s+M\d+\w*\s*$",
        "",
        h3_text.strip(),
        flags=re.IGNORECASE,
    ).lower()


def _build_h3_index(content: str) -> dict[int, str]:
    """Return a 1-based line → containing-H3-heading-text index.

    Walks the raw markdown for H3 and H2 boundaries and builds a dense
    ``{line_no: h3_text}`` map covering every line from 1 through
    ``content.count("\\n") + 1``. The H3 scope ends at the NEXT H3 or the
    NEXT H2 — whichever comes first. Lines that sit between an H2 and the
    first H3 inside it (or in the document preamble) map to ``""``.

    Line numbers are 1-based to align with ``Obligation.line_number`` /
    the ``abs_line`` used in ``scan_obligations``. Cost is O(n) per call
    where n = number of lines, which is acceptable per the existing
    per-call cost budget for tail-section/discharge precomputes.

    Used by Layer 5 (H3 subsection-context demotion) — the scanner's
    existing ``_split_into_phases`` silently absorbs H3 subsections into
    their enclosing H2 chunk, so a separate per-line index is required.
    """
    boundaries: list[tuple[int, str, str]] = []
    for m in _H3_HEADING_RE.finditer(content):
        line_no = content[: m.start()].count("\n") + 1
        boundaries.append((line_no, "h3", m.group(1).rstrip()))
    for m in _H2_HEADING_RE.finditer(content):
        line_no = content[: m.start()].count("\n") + 1
        boundaries.append((line_no, "h2", ""))
    boundaries.sort(key=lambda b: b[0])

    total_lines = content.count("\n") + 1
    index: dict[int, str] = {}
    boundary_iter = iter(boundaries)
    next_boundary = next(boundary_iter, None)
    current_h3 = ""
    for line_no in range(1, total_lines + 1):
        while next_boundary is not None and next_boundary[0] == line_no:
            kind = next_boundary[1]
            if kind == "h2":
                current_h3 = ""
            else:  # kind == "h3"
                current_h3 = next_boundary[2]
            next_boundary = next(boundary_iter, None)
        index[line_no] = current_h3
    return index


def _is_demoted_h3(h3_text: str) -> bool:
    """Return True when an H3 heading starts with a demote-target prefix.

    Prefix-match (NOT exact equality) so heading variants like
    ``Risk Assessment and Mitigation`` still match the ``risk assessment``
    prefix. The empty-string short-circuit handles the gap between an H2
    and the first H3 inside it where ``_build_h3_index`` records ``""``.

    Demote-target prefixes are defined in ``_DEMOTED_H3_SUBSECTIONS``:
    ``risk assessment``, ``integration points``, ``milestone dependencies``,
    ``open questions``.
    """
    if not h3_text:
        return False
    normalized = _normalize_h3_for_match(h3_text)
    return any(normalized.startswith(prefix) for prefix in _DEMOTED_H3_SUBSECTIONS)


def _is_allowlisted(line: str) -> bool:
    """True when ``line`` contains a documented anti-instinct allowlist phrase.

    Layer 6 (R0.2 — Contract #10) short-circuit. SCAFFOLD-term matches whose
    context line matches a phrase in ``_ALLOWLIST_PHRASES`` are SKIPPED
    entirely by ``scan_obligations`` — they refer to named permanent test
    fixtures or architectural module paths (e.g. ``stub transport``,
    ``transports/stub.py``), not scaffolding obligations.

    Phrase match is case-insensitive substring containment. Per Contract #10
    the allowlist subtracts from FPs only — adding a phrase requires a
    documented historical incident and a negative-test fixture proving no
    real obligation is masked. See ``_ALLOWLIST_PHRASES`` docstring for the
    source-authority list and addition criteria.
    """
    lowered = line.lower()
    return any(phrase in lowered for phrase in _ALLOWLIST_PHRASES)


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

    # Layer 4 (Fix 3): Descriptor-noun adjacency — descriptive prose
    if _is_descriptive_context(line, term_start_in_line):
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
    """Return True if line clearly states discharge intent, not new scaffolding.

    Recognizes both verb and noun forms of replace/integration so a phrase
    like "needs replacement" is treated as discharge intent (used as the
    guard for Layer 4's descriptor-noun classifier).
    """
    return bool(
        re.search(
            r"\b(?:replace(?:ment|s|d)?|wire\s+(?:up|in|into)|"
            r"integrat(?:e|ing|ed|ion)|connect|swap\s+(?:out|in)|remove|"
            r"implement\s+real|fill\s+in|complete)\b",
            line,
            re.IGNORECASE,
        )
    )


def _determine_severity(abs_pos: int, code_block_ranges: list[tuple[int, int]]) -> str:
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
