"""Spec & roadmap parser — structured data extraction from markdown documents.

Implements FR-2: Extracts YAML frontmatter, markdown tables, fenced code blocks,
requirement IDs, function signatures, Literal enum values, numeric thresholds,
and file paths from spec/roadmap markdown.

All extraction functions return structured objects and collect ParseWarning
instances for graceful degradation on malformed input.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ParseWarning:
    """Warning produced during parsing for malformed or irregular input."""

    category: str  # e.g. "yaml", "table", "code_block"
    message: str
    location: str = ""  # e.g. line number or section heading


@dataclass
class CodeBlock:
    """A fenced code block extracted from markdown."""

    language: str  # empty string if no language tag
    content: str
    start_line: int
    end_line: int


@dataclass
class TableRow:
    """A single row from a markdown table."""

    cells: list[str]


@dataclass
class MarkdownTable:
    """A markdown table extracted from a document, keyed by heading path."""

    heading_path: str
    headers: list[str]
    rows: list[TableRow]
    start_line: int
    end_line: int


@dataclass
class FunctionSignature:
    """A Python function signature extracted from a fenced code block."""

    name: str
    params: str
    return_type: str  # empty string if no return annotation


@dataclass
class ThresholdExpression:
    """A numeric threshold extracted from text (e.g. '< 5s', '>= 90%')."""

    operator: str  # '<', '<=', '>', '>=', '==', 'minimum', 'maximum', 'at least', 'at most'
    value: str  # raw numeric string including unit
    raw: str  # original matched text


@dataclass
class SpecSection:
    """A section of a spec document split by heading level.

    Implements FR-5: Sectional splitting for checker routing.
    """

    heading: str
    heading_path: str  # e.g. "FR-1/FR-1.1/Acceptance Criteria"
    level: int  # 0 = frontmatter/preamble, 1-6 = heading levels
    content: str
    start_line: int
    end_line: int


@dataclass
class ParseResult:
    """Aggregated parse result from a spec or roadmap document."""

    frontmatter: dict[str, Any] = field(default_factory=dict)
    tables: list[MarkdownTable] = field(default_factory=list)
    code_blocks: list[CodeBlock] = field(default_factory=list)
    requirement_ids: dict[str, list[str]] = field(default_factory=dict)
    function_signatures: list[FunctionSignature] = field(default_factory=list)
    literal_values: list[list[str]] = field(default_factory=list)
    thresholds: list[ThresholdExpression] = field(default_factory=list)
    file_paths: list[str] = field(default_factory=list)
    sections: list[SpecSection] = field(default_factory=list)
    warnings: list[ParseWarning] = field(default_factory=list)


# ---------- YAML Frontmatter ----------

def parse_frontmatter(text: str, warnings: list[ParseWarning]) -> dict[str, Any]:
    """Extract YAML frontmatter from document text.

    Returns parsed dict. On malformed YAML, returns partial parse via
    line-by-line key: value extraction and appends ParseWarning.
    """
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', text, re.DOTALL)
    if not match:
        return {}

    yaml_text = match.group(1)

    # Try proper YAML parsing first
    try:
        import yaml
        result = yaml.safe_load(yaml_text)
        if isinstance(result, dict):
            return result
    except Exception:
        pass

    # Fallback: line-by-line extraction
    warnings.append(ParseWarning(
        category="yaml",
        message="Malformed YAML frontmatter; falling back to line-by-line extraction",
        location="lines 1-*",
    ))
    result: dict[str, Any] = {}
    current_key = ""
    current_list: list[str] = []
    in_list = False

    for line in yaml_text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        # List item continuation
        if stripped.startswith("- ") and in_list:
            current_list.append(stripped[2:].strip().strip('"').strip("'"))
            continue

        # Save previous list if we were in one
        if in_list and current_key:
            result[current_key] = current_list
            in_list = False
            current_list = []

        # Key: value pair
        colon_idx = stripped.find(":")
        if colon_idx > 0:
            key = stripped[:colon_idx].strip()
            value = stripped[colon_idx + 1:].strip()
            current_key = key

            if not value:
                # Could be start of a list or multi-line value
                in_list = True
                current_list = []
            else:
                result[key] = value.strip('"').strip("'")

    if in_list and current_key:
        result[current_key] = current_list

    return result


# ---------- Markdown Tables ----------

def extract_tables(text: str, warnings: list[ParseWarning]) -> list[MarkdownTable]:
    """Extract markdown tables keyed by preceding heading path."""
    lines = text.splitlines()
    tables: list[MarkdownTable] = []
    heading_stack: list[tuple[int, str]] = []

    i = 0
    while i < len(lines):
        line = lines[i]

        # Track headings for heading_path
        heading_match = re.match(r'^(#{1,6})\s+(.+)', line)
        if heading_match:
            level = len(heading_match.group(1))
            title = heading_match.group(2).strip()
            # Pop stack to current level
            heading_stack = [(l, h) for l, h in heading_stack if l < level]
            heading_stack.append((level, title))
            i += 1
            continue

        # Detect table: line with pipes
        if '|' in line and line.strip().startswith('|'):
            table_start = i
            header_line = line
            headers = _parse_table_row(header_line)

            # Check for separator line
            if i + 1 < len(lines) and re.match(r'^\s*\|[\s\-:|]+\|', lines[i + 1]):
                i += 2  # skip header + separator
            else:
                # Irregular table - no separator
                warnings.append(ParseWarning(
                    category="table",
                    message="Table missing separator line",
                    location=f"line {i + 1}",
                ))
                i += 1

            # Collect data rows
            rows: list[TableRow] = []
            while i < len(lines) and '|' in lines[i] and lines[i].strip().startswith('|'):
                cells = _parse_table_row(lines[i])
                if len(cells) != len(headers):
                    warnings.append(ParseWarning(
                        category="table",
                        message=f"Row has {len(cells)} columns, header has {len(headers)}",
                        location=f"line {i + 1}",
                    ))
                rows.append(TableRow(cells=cells))
                i += 1

            heading_path = "/".join(h for _, h in heading_stack) if heading_stack else ""
            tables.append(MarkdownTable(
                heading_path=heading_path,
                headers=headers,
                rows=rows,
                start_line=table_start + 1,
                end_line=i,
            ))
            continue

        i += 1

    return tables


def _parse_table_row(line: str) -> list[str]:
    """Parse a markdown table row into cells."""
    stripped = line.strip()
    if stripped.startswith('|'):
        stripped = stripped[1:]
    if stripped.endswith('|'):
        stripped = stripped[:-1]
    return [cell.strip() for cell in stripped.split('|')]


# ---------- Fenced Code Blocks ----------

def extract_code_blocks(text: str, warnings: list[ParseWarning]) -> list[CodeBlock]:
    """Extract fenced code blocks with language annotation."""
    lines = text.splitlines()
    blocks: list[CodeBlock] = []
    i = 0

    while i < len(lines):
        match = re.match(r'^(`{3,}|~{3,})\s*(.*)', lines[i])
        if match:
            fence_char = match.group(1)[0]
            fence_len = len(match.group(1))
            language = match.group(2).strip()
            start = i

            if not language:
                warnings.append(ParseWarning(
                    category="code_block",
                    message="Fenced code block missing language tag",
                    location=f"line {i + 1}",
                ))

            # Find closing fence
            i += 1
            content_lines: list[str] = []
            while i < len(lines):
                close_match = re.match(r'^' + re.escape(fence_char) + r'{' + str(fence_len) + r',}\s*$', lines[i])
                if close_match:
                    break
                content_lines.append(lines[i])
                i += 1

            blocks.append(CodeBlock(
                language=language,
                content="\n".join(content_lines),
                start_line=start + 1,
                end_line=i + 1,
            ))
        i += 1

    return blocks


# ---------- Requirement IDs ----------

_REQUIREMENT_PATTERNS: dict[str, re.Pattern[str]] = {
    "FR": re.compile(r'\bFR-\d+(?:\.\d+)?\b'),
    "NFR": re.compile(r'\bNFR-\d+(?:\.\d+)?\b'),
    "SC": re.compile(r'\bSC-\d+\b'),
    "G": re.compile(r'\bG-\d+\b'),
    "D": re.compile(r'\bD-?\d+\b'),
}


def extract_requirement_ids(text: str) -> dict[str, list[str]]:
    """Extract requirement ID families via regex.

    Returns dict keyed by family prefix (FR, NFR, SC, G, D)
    with sorted unique ID lists.
    """
    result: dict[str, list[str]] = {}
    for family, pattern in _REQUIREMENT_PATTERNS.items():
        ids = sorted(set(pattern.findall(text)))
        if ids:
            result[family] = ids
    return result


# ---------- Function Signatures ----------

_FUNC_SIG_RE = re.compile(
    r'def\s+(\w+)\s*\(([^)]*)\)\s*(?:->\s*(.+?))?:'
)


def extract_function_signatures(code_blocks: list[CodeBlock]) -> list[FunctionSignature]:
    """Extract Python function signatures from fenced code blocks."""
    signatures: list[FunctionSignature] = []
    for block in code_blocks:
        if block.language and block.language.lower() not in ("python", "py", ""):
            continue
        for match in _FUNC_SIG_RE.finditer(block.content):
            signatures.append(FunctionSignature(
                name=match.group(1),
                params=match.group(2).strip(),
                return_type=(match.group(3) or "").strip(),
            ))
    return signatures


# ---------- Literal Values ----------

_LITERAL_RE = re.compile(r'Literal\[([^\]]+)\]')


def extract_literal_values(code_blocks: list[CodeBlock]) -> list[list[str]]:
    """Extract Literal[...] enum values from code blocks."""
    results: list[list[str]] = []
    for block in code_blocks:
        for match in _LITERAL_RE.finditer(block.content):
            values = [v.strip().strip('"').strip("'") for v in match.group(1).split(",")]
            results.append(values)
    return results


# ---------- Numeric Thresholds ----------

_THRESHOLD_RE = re.compile(
    r'(?:'
    r'([<>]=?|==)\s*(\d+(?:\.\d+)?[%smhKMGT]*\w*)'
    r'|'
    r'(minimum|maximum|at\s+least|at\s+most)\s+(\d+(?:\.\d+)?[%smhKMGT]*\w*)'
    r')',
    re.IGNORECASE,
)


def extract_thresholds(text: str) -> list[ThresholdExpression]:
    """Extract numeric threshold expressions from text."""
    thresholds: list[ThresholdExpression] = []
    seen: set[str] = set()
    for match in _THRESHOLD_RE.finditer(text):
        raw = match.group(0).strip()
        if raw in seen:
            continue
        seen.add(raw)
        if match.group(1):
            thresholds.append(ThresholdExpression(
                operator=match.group(1),
                value=match.group(2),
                raw=raw,
            ))
        else:
            thresholds.append(ThresholdExpression(
                operator=match.group(3).lower(),
                value=match.group(4),
                raw=raw,
            ))
    return thresholds


# ---------- File Paths ----------

_FILE_PATH_RE = re.compile(
    r'`((?:src/|tests/|docs/|scripts/|\./)[^\s`]+)`'
)


def extract_file_paths(text: str) -> list[str]:
    """Extract file paths from text (backtick-quoted, starting with known prefixes)."""
    return sorted(set(_FILE_PATH_RE.findall(text)))


def extract_file_paths_from_tables(tables: list[MarkdownTable]) -> list[str]:
    """Extract file paths from manifest tables (columns containing paths)."""
    paths: set[str] = set()
    path_like = re.compile(r'(?:src/|tests/|docs/|scripts/|\./)\S+')
    for table in tables:
        for row in table.rows:
            for cell in row.cells:
                for match in path_like.finditer(cell):
                    # Strip backticks and trailing punctuation
                    p = match.group(0).strip('`').rstrip('.,;:)')
                    paths.add(p)
    return sorted(paths)


# ---------- Section Splitting (FR-5) ----------

_HEADING_RE = re.compile(r'^(#{1,6})\s+(.+)', re.MULTILINE)


def split_into_sections(text: str) -> list[SpecSection]:
    """Split document into sections by heading level.

    Handles YAML frontmatter as level=0 section and preamble
    (content before first heading) as level=0 section.
    """
    lines = text.splitlines(keepends=True)
    sections: list[SpecSection] = []
    heading_stack: list[tuple[int, str]] = []

    # Handle YAML frontmatter
    fm_match = re.match(r'^---\s*\n(.*?\n)---\s*\n', text, re.DOTALL)
    content_start = 0
    if fm_match:
        fm_end = text[:fm_match.end()].count('\n')
        sections.append(SpecSection(
            heading="frontmatter",
            heading_path="frontmatter",
            level=0,
            content=fm_match.group(0),
            start_line=1,
            end_line=fm_end,
        ))
        content_start = fm_end

    # Find all headings with their line positions
    heading_positions: list[tuple[int, int, str]] = []  # (line_idx, level, title)
    for i, line in enumerate(lines):
        if i < content_start:
            continue
        m = re.match(r'^(#{1,6})\s+(.+)', line)
        if m:
            heading_positions.append((i, len(m.group(1)), m.group(2).strip()))

    # Handle preamble (content between frontmatter and first heading)
    if heading_positions:
        first_heading_line = heading_positions[0][0]
        if first_heading_line > content_start:
            preamble = "".join(lines[content_start:first_heading_line])
            if preamble.strip():
                sections.append(SpecSection(
                    heading="preamble",
                    heading_path="preamble",
                    level=0,
                    content=preamble,
                    start_line=content_start + 1,
                    end_line=first_heading_line,
                ))
    elif content_start < len(lines):
        # No headings at all - entire content is preamble
        preamble = "".join(lines[content_start:])
        if preamble.strip():
            sections.append(SpecSection(
                heading="preamble",
                heading_path="preamble",
                level=0,
                content=preamble,
                start_line=content_start + 1,
                end_line=len(lines),
            ))

    # Process each heading section
    for idx, (line_idx, level, title) in enumerate(heading_positions):
        # Update heading stack
        heading_stack = [(l, h) for l, h in heading_stack if l < level]
        heading_stack.append((level, title))
        heading_path = "/".join(h for _, h in heading_stack)

        # Determine section end
        if idx + 1 < len(heading_positions):
            end_idx = heading_positions[idx + 1][0]
        else:
            end_idx = len(lines)

        content = "".join(lines[line_idx:end_idx])
        sections.append(SpecSection(
            heading=title,
            heading_path=heading_path,
            level=level,
            content=content,
            start_line=line_idx + 1,
            end_line=end_idx,
        ))

    return sections


# ---------- Dimension Mapping (FR-5) ----------

DIMENSION_SECTION_MAP: dict[str, list[str]] = {
    "signatures": ["FR-1", "FR-2", "3. Functional Requirements"],
    "data_models": ["4.1", "4.2", "4.3", "4. File Manifest"],
    "gates": ["FR-7", "FR-8", "5.1"],
    "cli": ["5.1", "CLI", "Commands"],
    "nfrs": ["6.", "NFR", "Non-Functional"],
}


# ---------- Full Parse ----------

def parse_document(text: str) -> ParseResult:
    """Parse a spec or roadmap document, extracting all structured data.

    Returns a ParseResult with all extraction types populated.
    Collects ParseWarning instances for any graceful degradation.
    """
    warnings: list[ParseWarning] = []

    frontmatter = parse_frontmatter(text, warnings)
    tables = extract_tables(text, warnings)
    code_blocks = extract_code_blocks(text, warnings)
    requirement_ids = extract_requirement_ids(text)
    function_signatures = extract_function_signatures(code_blocks)
    literal_values = extract_literal_values(code_blocks)
    thresholds = extract_thresholds(text)
    file_paths = extract_file_paths(text)
    file_paths_from_tables = extract_file_paths_from_tables(tables)
    all_file_paths = sorted(set(file_paths + file_paths_from_tables))
    sections = split_into_sections(text)

    return ParseResult(
        frontmatter=frontmatter,
        tables=tables,
        code_blocks=code_blocks,
        requirement_ids=requirement_ids,
        function_signatures=function_signatures,
        literal_values=literal_values,
        thresholds=thresholds,
        file_paths=all_file_paths,
        sections=sections,
        warnings=warnings,
    )
