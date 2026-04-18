"""Markdown document compression using strategy stacks from compression research.

Applies per-document-type compression strategies (roadmap, spec, tasklist)
as defined in UNIFIED-compression-strategies.md. All transforms are
fence-aware (never modify content inside ``` blocks). Lossy strategies
are off by default; enable with `aggressive=True`.

This module is the importable home of the compression pipeline. The
``scripts/compress.py`` CLI wrapper re-exports from here.

High-level API:
    run_pipeline(text, doc_type, aggressive=False) -> (compressed, stats)
    compress_file(input_path, doc_type, output_path, aggressive=False) -> stats
"""
from __future__ import annotations

import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


# ============================================================================
# Section 1: Fence-aware infrastructure
# ============================================================================

def split_fenced_regions(text: str) -> list[tuple[str, bool]]:
    """Split text into alternating (content, is_fenced) regions.

    Uses character-position tracking for exact round-trip:
    ''.join(r[0] for r in split_fenced_regions(text)) == text
    """
    regions: list[tuple[str, bool]] = []
    fence_re = re.compile(r"^(\s*(`{3,}|~{3,}))(.*?)$", re.MULTILINE)

    in_fence = False
    fence_char = ""
    fence_len = 0
    last_pos = 0

    for m in fence_re.finditer(text):
        delimiter = m.group(2)
        rest = m.group(3)
        d_char = delimiter[0]
        d_len = len(delimiter)

        if not in_fence:
            if m.start() > last_pos:
                regions.append((text[last_pos : m.start()], False))
            in_fence = True
            fence_char = d_char
            fence_len = d_len
            last_pos = m.start()
        elif d_char == fence_char and d_len >= fence_len and rest.strip() == "":
            line_end = m.end()
            if line_end < len(text) and text[line_end] == "\n":
                line_end += 1
            regions.append((text[last_pos:line_end], True))
            last_pos = line_end
            in_fence = False
            fence_char = ""
            fence_len = 0

    if last_pos < len(text):
        regions.append((text[last_pos:], in_fence))
    elif last_pos == 0 and not regions:
        regions.append((text, False))

    return regions


def apply_outside_fences(text: str, transform: Callable[[str], str]) -> str:
    """Apply a transform function only to non-fenced regions."""
    regions = split_fenced_regions(text)
    parts = []
    for content, is_fenced in regions:
        parts.append(content if is_fenced else transform(content))
    return "".join(parts)


# ============================================================================
# Section 2: Data structures
# ============================================================================

@dataclass
class StrategyEntry:
    """A compression strategy with metadata."""
    id: str
    name: str
    fn: Callable[[str], str]
    lossy: bool = False


@dataclass
class StrategyStat:
    """Per-strategy savings measurement."""
    id: str
    name: str
    bytes_before: int
    bytes_after: int

    @property
    def bytes_saved(self) -> int:
        return self.bytes_before - self.bytes_after

    @property
    def pct_saved(self) -> float:
        if self.bytes_before == 0:
            return 0.0
        return (self.bytes_saved / self.bytes_before) * 100


@dataclass
class ParsedTable:
    """A parsed pipe table from the document."""
    start_line: int
    end_line: int
    headers: list[str]
    separator: str
    rows: list[list[str]]
    raw: str


# ============================================================================
# Section 3: Shared helpers
# ============================================================================

def _find_header_end(text: str) -> int:
    end = 0
    for hdr_match in re.finditer(r"<!--.*?-->", text, re.DOTALL):
        gap = text[end:hdr_match.start()]
        if gap.strip() == "":
            end = hdr_match.end()
            if end < len(text) and text[end] == "\n":
                end += 1
        else:
            break
    return end


def _upsert_conventions_header(
    text: str, new_entries: dict[str, str], section: str = "CONV"
) -> str:
    pattern = rf"<!-- {section}:(.*?)-->"
    match = re.search(pattern, text, re.DOTALL)
    formatted = ", ".join(f"{k}={v}" for k, v in new_entries.items())

    if match:
        existing = match.group(1).strip()
        combined = f"{existing}, {formatted}"
        return (
            text[: match.start()]
            + f"<!-- {section}: {combined} -->"
            + text[match.end() :]
        )
    else:
        header = f"<!-- {section}: {formatted} -->\n"
        return header + text


def _generate_alias(token: str, existing_aliases: set[str]) -> str:
    parts = re.split(r"[_\-/.]", token)
    parts = [p for p in parts if p]
    if len(parts) >= 2:
        alias = "".join(p[0].upper() for p in parts)
        if len(alias) >= 2 and alias not in existing_aliases:
            return alias

    consonants = [c for c in token.upper() if c in "BCDFGHJKLMNPQRSTVWXYZ"]
    if len(consonants) >= 2:
        alias = "".join(consonants[:3])
        if alias not in existing_aliases:
            return alias

    base = token[:2].upper()
    for i in range(1, 100):
        alias = f"{base}{i}"
        if alias not in existing_aliases:
            return alias

    return token[:4].upper()


def parse_pipe_tables(text: str) -> list[ParsedTable]:
    tables: list[ParsedTable] = []
    lines = text.split("\n")
    i = 0

    while i < len(lines):
        line = lines[i]
        if "|" in line and line.strip().startswith("|"):
            if i + 1 < len(lines) and re.match(
                r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]
            ):
                header_line = line
                sep_line = lines[i + 1]

                headers = [
                    c.strip()
                    for c in header_line.strip().strip("|").split("|")
                ]

                rows: list[list[str]] = []
                start = i
                j = i + 2
                while j < len(lines) and lines[j].strip().startswith("|"):
                    cells = [
                        c.strip()
                        for c in lines[j].strip().strip("|").split("|")
                    ]
                    rows.append(cells)
                    j += 1

                raw = "\n".join(lines[start:j])
                tables.append(
                    ParsedTable(
                        start_line=start,
                        end_line=j - 1,
                        headers=headers,
                        separator=sep_line,
                        rows=rows,
                        raw=raw,
                    )
                )
                i = j
                continue
        i += 1

    return tables


def _is_in_frontmatter(text: str, pos: int) -> bool:
    if not text.startswith("---"):
        return False
    end = text.find("\n---", 3)
    if end == -1:
        return False
    return pos < end + 4


# ============================================================================
# Section 4: Strategy functions
# ============================================================================

def s01_whitespace_collapse(text: str) -> str:
    def _collapse(chunk: str) -> str:
        return re.sub(r"\n{3,}", "\n\n", chunk)
    return apply_outside_fences(text, _collapse)


def s01_whitespace_collapse_with_hr(text: str) -> str:
    def _collapse_and_remove_hr(chunk: str) -> str:
        lines = chunk.split("\n")
        result: list[str] = []
        for idx, line in enumerate(lines):
            if re.match(r"^-{3,}\s*$", line) or re.match(r"^\*{3,}\s*$", line) or re.match(r"^_{3,}\s*$", line):
                prev_heading = False
                next_heading = False
                for p in range(idx - 1, -1, -1):
                    if lines[p].strip():
                        prev_heading = bool(re.match(r"^#{1,6}\s", lines[p]))
                        break
                for n in range(idx + 1, len(lines)):
                    if lines[n].strip():
                        next_heading = bool(re.match(r"^#{1,6}\s", lines[n]))
                        break
                if prev_heading or next_heading:
                    continue
            result.append(line)
        chunk = "\n".join(result)
        return re.sub(r"\n{3,}", "\n\n", chunk)
    return apply_outside_fences(text, _collapse_and_remove_hr)


def s02_trailing_whitespace_strip(text: str) -> str:
    def _strip(chunk: str) -> str:
        return re.sub(r"[ \t]+$", "", chunk, flags=re.MULTILINE)
    return apply_outside_fences(text, _strip)


def s03_decorative_hr_removal(text: str) -> str:
    def _remove_hr(chunk: str) -> str:
        lines = chunk.split("\n")
        result: list[str] = []
        for idx, line in enumerate(lines):
            if re.match(r"^-{3,}\s*$", line) or re.match(r"^\*{3,}\s*$", line) or re.match(r"^_{3,}\s*$", line):
                if idx == 0 and chunk == text[:len(chunk)]:
                    result.append(line)
                    continue

                prev_heading = False
                next_heading = False
                for p in range(idx - 1, -1, -1):
                    if lines[p].strip():
                        prev_heading = bool(re.match(r"^#{1,6}\s", lines[p]))
                        break
                for n in range(idx + 1, len(lines)):
                    if lines[n].strip():
                        next_heading = bool(re.match(r"^#{1,6}\s", lines[n]))
                        break
                if prev_heading or next_heading:
                    continue
            result.append(line)
        return "\n".join(result)
    return apply_outside_fences(text, _remove_hr)


def s04_pipe_table_padding_collapse(text: str) -> str:
    def _collapse_padding(chunk: str) -> str:
        lines = chunk.split("\n")
        result: list[str] = []
        for line in lines:
            if line.strip().startswith("|") and "|" in line.strip()[1:]:
                if re.match(r"^\s*\|[\s:|-]+\|\s*$", line):
                    cells = line.strip().strip("|").split("|")
                    collapsed = []
                    for cell in cells:
                        cell = cell.strip()
                        if re.match(r"^:?-+:?$", cell):
                            collapsed.append(cell)
                        else:
                            collapsed.append(cell)
                    result.append("|" + "|".join(collapsed) + "|")
                else:
                    cells = line.strip().strip("|").split("|")
                    collapsed = [c.strip() for c in cells]
                    result.append("|" + "|".join(collapsed) + "|")
            else:
                result.append(line)
        return "\n".join(result)
    return apply_outside_fences(text, _collapse_padding)


def s07_html_comment_removal(text: str, preserve_count: int = 3) -> str:
    def _remove_comments(chunk: str) -> str:
        comments = list(re.finditer(r"<!--.*?-->", chunk, re.DOTALL))
        if not comments:
            return chunk

        to_remove = comments[preserve_count:]
        if not to_remove:
            return chunk

        result = chunk
        for m in reversed(to_remove):
            start = m.start()
            end = m.end()
            before = result[:start].rstrip(" \t")
            after = result[end:].lstrip(" \t")
            if before.endswith("\n") and after.startswith("\n"):
                result = before + after
            else:
                result = before + after
        return result
    return apply_outside_fences(text, _remove_comments)


_CONVENTIONS_PROTECTED_TOKENS: frozenset[str] = frozenset(
    {
        # Template placeholder sentinel used by the roadmap pipeline. Downstream
        # gates and tooling match the literal string ``SC_PLACEHOLDER``; aliasing
        # it to a short form would silently break placeholder detection.
        "SC_PLACEHOLDER",
    }
)


def s09_conventions_header(text: str, mode: str = "identifiers") -> str:
    regions = split_fenced_regions(text)
    non_fenced = "".join(content for content, is_fenced in regions if not is_fenced)

    if mode == "identifiers":
        candidates = re.findall(
            r"(?:[A-Za-z_][A-Za-z0-9_.-]*(?:/[A-Za-z0-9_.-]+)+)"
            r"|(?:[A-Za-z_][A-Za-z0-9_-]{7,})",
            non_fenced,
        )
    else:
        candidates = re.findall(r"\*\*([A-Z][A-Za-z ]{2,})\*\*:", non_fenced)

    counter = Counter(candidates)

    existing_aliases: set[str] = set()
    conv_match = re.search(r"<!-- CONV:\s*(.*?)\s*-->", text)
    if conv_match:
        for entry in conv_match.group(1).split(","):
            entry = entry.strip()
            if "=" in entry:
                alias_part = entry.split("=", 1)[1].strip()
                existing_aliases.add(alias_part)

    eligible = [
        (token, count)
        for token, count in counter.items()
        if count >= 5
        and len(token) >= 6
        and token not in _CONVENTIONS_PROTECTED_TOKENS
        and not all(w in existing_aliases for w in token.split())
    ]

    eligible.sort(key=lambda x: x[1] * len(x[0]), reverse=True)
    eligible = eligible[:20]

    if not eligible:
        return text

    alias_map: dict[str, str] = {}

    for token, _count in eligible:
        alias = _generate_alias(token, existing_aliases)
        header_cost = len(alias) + 1 + len(token) + 2
        savings_per_use = len(token) - len(alias)
        if savings_per_use * _count > header_cost:
            alias_map[token] = alias
            existing_aliases.add(alias)

    if not alias_map:
        return text

    text = _upsert_conventions_header(text, alias_map, section="CONV")

    def _substitute(chunk: str) -> str:
        result = chunk
        for token, alias in sorted(
            alias_map.items(), key=lambda x: len(x[0]), reverse=True
        ):
            escaped = re.escape(token)
            result = re.sub(rf"(?<!\w){escaped}(?!\w)", alias, result)
        return result

    header_end = _find_header_end(text)
    if header_end > 0:
        header_part = text[:header_end]
        rest = text[header_end:]
        rest = apply_outside_fences(rest, _substitute)
        return header_part + rest

    return apply_outside_fences(text, _substitute)


def s10_labels_only_abbreviation(text: str) -> str:
    return s09_conventions_header(text, mode="labels")


def s13_multi_paragraph_bullet_compaction(text: str) -> str:
    def _compact(chunk: str) -> str:
        lines = chunk.split("\n")
        result: list[str] = []
        i = 0
        while i < len(lines):
            line = lines[i]
            bullet_match = re.match(r"^(\s*[-*+]\s+)", line)
            if bullet_match:
                indent = len(bullet_match.group(1))
                bullet_lines = [line]
                j = i + 1
                while j < len(lines):
                    if lines[j].strip() == "":
                        k = j + 1
                        while k < len(lines) and lines[k].strip() == "":
                            k += 1
                        if k < len(lines) and len(lines[k]) > indent and lines[k][:indent].strip() == "":
                            j = k
                            bullet_lines.append(lines[j].strip())
                            j += 1
                        else:
                            break
                    elif len(line) > indent and lines[j][:indent].strip() == "" and lines[j].strip():
                        bullet_lines.append(lines[j].strip())
                        j += 1
                    else:
                        break
                if len(bullet_lines) > 1:
                    result.append(bullet_lines[0].rstrip() + " " + " ".join(bullet_lines[1:]))
                else:
                    result.append(line)
                i = j
            else:
                result.append(line)
                i += 1
        return "\n".join(result)
    return apply_outside_fences(text, _compact)


def s14_table_default_row_hoisting(text: str) -> str:
    regions = split_fenced_regions(text)

    all_text = "".join(content for content, _ in regions)
    tables = parse_pipe_tables(all_text)

    field_value_tables = [
        t for t in tables
        if len(t.headers) == 2 and len(t.rows) >= 2
    ]

    if len(field_value_tables) < 3:
        return text

    field_value_counter: dict[str, Counter[str]] = defaultdict(Counter)
    for table in field_value_tables:
        for row in table.rows:
            if len(row) >= 2:
                field_name = row[0].strip()
                field_value = row[1].strip()
                field_value_counter[field_name][field_value] += 1

    n_tables = len(field_value_tables)
    defaults: dict[str, str] = {}
    for field_name, value_counts in field_value_counter.items():
        if value_counts:
            most_common_value, count = value_counts.most_common(1)[0]
            if count > n_tables * 0.5:
                defaults[field_name] = most_common_value

    if not defaults:
        return text

    defaults_parts = [f"{k}={v}" for k, v in defaults.items()]
    defaults_block = "> **Defaults**: " + " | ".join(defaults_parts) + "\n"

    lines = text.split("\n")
    result_lines: list[str] = []
    defaults_inserted = False
    i = 0

    while i < len(lines):
        line = lines[i]

        if (
            line.strip().startswith("|")
            and i + 1 < len(lines)
            and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1])
        ):
            headers = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(headers) == 2:
                if not defaults_inserted:
                    result_lines.append(defaults_block)
                    defaults_inserted = True

                result_lines.append(line)
                result_lines.append(lines[i + 1])
                j = i + 2

                while j < len(lines) and lines[j].strip().startswith("|"):
                    cells = [
                        c.strip()
                        for c in lines[j].strip().strip("|").split("|")
                    ]
                    if len(cells) >= 2:
                        fname = cells[0].strip()
                        fval = cells[1].strip()
                        if defaults.get(fname) == fval:
                            j += 1
                            continue
                    result_lines.append(lines[j])
                    j += 1
                i = j
                continue

        result_lines.append(line)
        i += 1

    return "\n".join(result_lines)


def s15_executive_summary_dedup(text: str) -> str:
    def _dedup(chunk: str) -> str:
        match = re.search(
            r"(^#{1,3}\s+.*(?:Executive|Summary|Overview).*$)",
            chunk,
            re.MULTILINE | re.IGNORECASE,
        )
        if not match:
            return chunk

        summary_start = match.start()
        heading_level = match.group(1).count("#")
        rest = chunk[match.end():]
        next_heading = re.search(
            rf"^#{{1,{heading_level}}}\s", rest, re.MULTILINE
        )
        if next_heading:
            summary_end = match.end() + next_heading.start()
        else:
            return chunk

        summary_text = chunk[summary_start:summary_end]
        body_text = chunk[summary_end:]

        summary_body = summary_text[match.end() - summary_start:]
        sentences = re.split(r"(?<=[.!?])\s+", summary_body.strip())

        body_normalized = re.sub(r"\s+", " ", body_text.lower())

        kept = []
        for sentence in sentences:
            normalized = re.sub(r"\s+", " ", sentence.strip().lower())
            if len(normalized) < 20:
                kept.append(sentence)
            elif normalized not in body_normalized:
                kept.append(sentence)

        if len(kept) == len(sentences):
            return chunk

        new_summary = chunk[summary_start:match.end()] + "\n" + " ".join(kept) + "\n"
        return chunk[:summary_start] + new_summary + chunk[summary_end:]

    return apply_outside_fences(text, _dedup)


def s16_fr_id_range_condensation(text: str) -> str:
    def _condense(chunk: str) -> str:
        prefixes = ["FR", "NFR", "SC", "OQ"]
        for prefix in prefixes:
            pattern = rf"({prefix}-(\d{{3}})(?:,\s*{prefix}-(\d{{3}}))+)"
            for m in re.finditer(pattern, chunk):
                full_match = m.group(0)
                ids = re.findall(rf"{prefix}-(\d{{3}})", full_match)
                nums = [int(x) for x in ids]

                ranges: list[str] = []
                run_start = nums[0]
                run_end = nums[0]
                for n in nums[1:]:
                    if n == run_end + 1:
                        run_end = n
                    else:
                        if run_end - run_start >= 2:
                            ranges.append(f"{prefix}-{run_start:03d}..{run_end:03d}")
                        else:
                            for x in range(run_start, run_end + 1):
                                ranges.append(f"{prefix}-{x:03d}")
                        run_start = n
                        run_end = n
                if run_end - run_start >= 2:
                    ranges.append(f"{prefix}-{run_start:03d}..{run_end:03d}")
                else:
                    for x in range(run_start, run_end + 1):
                        ranges.append(f"{prefix}-{x:03d}")

                replacement = ", ".join(ranges)
                if replacement != full_match:
                    chunk = chunk.replace(full_match, replacement, 1)
        return chunk

    return apply_outside_fences(text, _condense)


def s17_artifact_path_macro(text: str) -> str:
    regions = split_fenced_regions(text)
    non_fenced = "".join(content for content, is_fenced in regions if not is_fenced)

    paths = re.findall(r"[A-Za-z0-9_./-]{5,}(?:/[A-Za-z0-9_./-]+)+", non_fenced)
    if not paths:
        return text

    prefix_counter: Counter[str] = Counter()
    for path in paths:
        parts = path.split("/")
        for depth in range(2, len(parts)):
            prefix = "/".join(parts[:depth]) + "/"
            prefix_counter[prefix] += 1

    eligible = [
        (prefix, count)
        for prefix, count in prefix_counter.items()
        if count >= 5
    ]
    if not eligible:
        return text

    eligible.sort(key=lambda x: x[1] * len(x[0]), reverse=True)
    best_prefix, best_count = eligible[0]

    macro = "$ART"
    savings_per_use = len(best_prefix) - len(macro)
    header_cost = len(f"$ART={best_prefix}, ")
    if savings_per_use * best_count <= header_cost:
        return text

    text = _upsert_conventions_header(text, {macro: best_prefix}, section="MACRO")

    def _replace_paths(chunk: str) -> str:
        return chunk.replace(best_prefix, macro)

    header_end = _find_header_end(text)
    if header_end > 0:
        header_part = text[:header_end]
        rest = text[header_end:]
        rest = apply_outside_fences(rest, _replace_paths)
        return header_part + rest

    return apply_outside_fences(text, _replace_paths)


_TAG_MAP: dict[str, str] = {
    "[PLANNING]": "[P]",
    "[EXECUTION]": "[E]",
    "[VERIFICATION]": "[V]",
    "[COMPLETION]": "[C]",
    "[INTEGRATION]": "[I]",
    "[TESTING]": "[T]",
    "[REVIEW]": "[R]",
}


def s18_step_tag_abbreviation(text: str) -> str:
    regions = split_fenced_regions(text)
    non_fenced = "".join(content for content, is_fenced in regions if not is_fenced)

    present_tags = {tag: abbr for tag, abbr in _TAG_MAP.items() if tag in non_fenced}
    if not present_tags:
        return text

    legend = {abbr: tag.strip("[]") for tag, abbr in present_tags.items()}
    text = _upsert_conventions_header(text, legend, section="TAGS")

    def _abbreviate(chunk: str) -> str:
        result = chunk
        for tag, abbr in present_tags.items():
            result = result.replace(tag, abbr)
        return result

    header_end = _find_header_end(text)
    if header_end > 0:
        return text[:header_end] + apply_outside_fences(text[header_end:], _abbreviate)

    return apply_outside_fences(text, _abbreviate)


def s19_checkpoint_block_dedup(text: str) -> str:
    def _dedup(chunk: str) -> str:
        checkpoint_pattern = re.compile(
            r"^(#{2,4}\s+.*[Cc]heckpoint.*$)", re.MULTILINE
        )
        matches = list(checkpoint_pattern.finditer(chunk))
        if len(matches) < 2:
            return chunk

        blocks: list[tuple[int, int, str, str]] = []
        for idx, m in enumerate(matches):
            heading = m.group(1)
            level = len(heading.split()[0])
            start = m.start()

            if idx + 1 < len(matches):
                end = matches[idx + 1].start()
            else:
                next_h = re.search(
                    rf"^#{{1,{level}}}\s",
                    chunk[m.end():],
                    re.MULTILINE,
                )
                end = m.end() + next_h.start() if next_h else len(chunk)

            body = chunk[m.end():end].strip()
            blocks.append((start, end, heading, body))

        seen: dict[str, int] = {}
        to_replace: list[tuple[int, int, str]] = []

        for i, (start, end, heading, body) in enumerate(blocks):
            normalized = re.sub(r"\s+", " ", body.strip())
            if normalized in seen:
                replacement = f"{heading}\n\n> See checkpoint template above.\n"
                to_replace.append((start, end, replacement))
            else:
                seen[normalized] = i

        if not to_replace:
            return chunk

        result = chunk
        for start, end, replacement in reversed(to_replace):
            result = result[:start] + replacement + result[end:]

        return result

    return apply_outside_fences(text, _dedup)


def s20_template_block_externalization(text: str) -> str:
    def _externalize(chunk: str) -> str:
        template_pattern = re.compile(
            r"^(#{2,4}\s+.*[Tt]emplate.*$)", re.MULTILINE
        )
        matches = list(template_pattern.finditer(chunk))
        if len(matches) < 2:
            return chunk

        templates: list[tuple[int, int, str, str]] = []
        for idx, m in enumerate(matches):
            heading = m.group(1)
            level = len(heading.split()[0])
            start = m.start()

            if idx + 1 < len(matches):
                end = matches[idx + 1].start()
            else:
                next_h = re.search(
                    rf"^#{{1,{level}}}\s",
                    chunk[m.end():],
                    re.MULTILINE,
                )
                end = m.end() + next_h.start() if next_h else len(chunk)

            body = chunk[m.end():end]
            templates.append((start, end, heading, body))

        body_map: dict[str, list[int]] = defaultdict(list)
        for i, (_, _, _, body) in enumerate(templates):
            normalized = re.sub(r"\s+", " ", body.strip())
            body_map[normalized].append(i)

        to_externalize: list[int] = []
        for indices in body_map.values():
            if len(indices) >= 2:
                to_externalize.extend(indices[1:])

        if not to_externalize:
            return chunk

        result = chunk
        for i in sorted(to_externalize, reverse=True):
            start, end, heading, _ = templates[i]
            ref = f"{heading}\n\n> See template definition above.\n"
            result = result[:start] + ref + result[end:]

        return result

    return apply_outside_fences(text, _externalize)


def s22_preamble_elision(text: str) -> str:
    def _elide(chunk: str) -> str:
        pattern = re.compile(
            r"\*\*File\*\*:\s*(.+?)\n"
            r"\*\*Line\*\*:\s*(.+?)\n"
            r"\*\*Risk\*\*:\s*(.+?)\n",
            re.MULTILINE,
        )
        matches = list(pattern.finditer(chunk))
        if len(matches) < 2:
            return chunk

        def _replace(m: re.Match) -> str:
            file_val = m.group(1).strip()
            line_val = m.group(2).strip()
            risk_val = m.group(3).strip()
            return f"File: {file_val} | Line: {line_val} | Risk: {risk_val}\n"

        return pattern.sub(_replace, chunk)

    return apply_outside_fences(text, _elide)


def s23_reference_style_citations(text: str) -> str:
    def _convert(chunk: str) -> str:
        inline_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
        all_links = inline_pattern.findall(chunk)

        url_counter: Counter[str] = Counter(url for _, url in all_links)

        duplicate_urls = {url for url, count in url_counter.items() if count >= 2}
        if not duplicate_urls:
            return chunk

        ref_map: dict[str, str] = {}
        ref_defs: list[str] = []
        ref_id = 1
        for url in sorted(duplicate_urls):
            ref_key = f"ref-{ref_id}"
            ref_map[url] = ref_key
            ref_defs.append(f"[{ref_key}]: {url}")
            ref_id += 1

        def _replace_link(m: re.Match) -> str:
            link_text = m.group(1)
            url = m.group(2)
            if url in ref_map:
                return f"[{link_text}][{ref_map[url]}]"
            return m.group(0)

        result = inline_pattern.sub(_replace_link, chunk)

        if ref_defs:
            result = result.rstrip() + "\n\n" + "\n".join(ref_defs) + "\n"

        return result

    return apply_outside_fences(text, _convert)


def s24_heading_decorative_suffix_drop(text: str) -> str:
    def _drop_suffix(chunk: str) -> str:
        heading_pattern = re.compile(
            r"^(#{1,6}\s+.+?)\s*"
            r"([\U0001F300-\U0001F9FF\U00002600-\U000027BF\U0001FA00-\U0001FA6F"
            r"\U0001FA70-\U0001FAFF\U00002702-\U000027B0]+"
            r"|[-=]{3,}|[*]{3,})\s*$",
            re.MULTILINE,
        )
        return heading_pattern.sub(r"\1", chunk)

    return apply_outside_fences(text, _drop_suffix)


def s25_validation_narrative_compaction(text: str) -> str:
    def _compact(chunk: str) -> str:
        val_pattern = re.compile(
            r"^(#{2,4}\s+.*[Vv]alidat(?:ion|e).*$)", re.MULTILINE
        )
        matches = list(val_pattern.finditer(chunk))
        if not matches:
            return chunk

        result = chunk
        for m in reversed(matches):
            heading = m.group(1)
            level = len(heading.split()[0])
            start = m.end()

            next_h = re.search(rf"^#{{1,{level}}}\s", chunk[start:], re.MULTILINE)
            end = start + next_h.start() if next_h else len(chunk)

            section_body = chunk[start:end]

            paragraphs = re.split(r"\n\n+", section_body.strip())
            if len(paragraphs) <= 1:
                continue

            bullets = []
            for para in paragraphs:
                para = para.strip()
                if not para or para.startswith("-") or para.startswith("*"):
                    bullets.append(para)
                else:
                    first_sentence = re.split(r"(?<=[.!?])\s", para)[0]
                    bullets.append(f"- {first_sentence}")

            new_section = "\n".join(bullets) + "\n"
            result = result[:start] + "\n" + new_section + result[end:]

        return result

    return apply_outside_fences(text, _compact)


# ============================================================================
# Section 5: Pipeline definitions
# ============================================================================

ROADMAP_PIPELINE: list[StrategyEntry] = [
    StrategyEntry("S-01", "Whitespace/blank-line collapse", s01_whitespace_collapse),
    StrategyEntry("S-02", "Trailing-whitespace strip", s02_trailing_whitespace_strip),
    StrategyEntry("S-03", "Decorative HR removal", s03_decorative_hr_removal),
    StrategyEntry("S-04", "Pipe-table padding collapse", s04_pipe_table_padding_collapse),
    StrategyEntry("S-07", "HTML comment removal", s07_html_comment_removal),
    StrategyEntry("S-22", "Per-change preamble elision", s22_preamble_elision),
    StrategyEntry(
        "S-09",
        "Conventions-header abbreviation",
        lambda t: s09_conventions_header(t, mode="identifiers"),
    ),
    StrategyEntry("S-16", "FR-ID range condensation", s16_fr_id_range_condensation),
    StrategyEntry("S-14", "Table default-row hoisting", s14_table_default_row_hoisting),
    StrategyEntry(
        "S-13", "Multi-paragraph bullet compaction",
        s13_multi_paragraph_bullet_compaction, lossy=True,
    ),
    StrategyEntry(
        "S-15", "Executive-summary prose dedup",
        s15_executive_summary_dedup, lossy=True,
    ),
    StrategyEntry(
        "S-25", "Validation-narrative compaction",
        s25_validation_narrative_compaction, lossy=True,
    ),
]

SPEC_PIPELINE: list[StrategyEntry] = [
    StrategyEntry("S-01", "Whitespace/blank-line collapse", s01_whitespace_collapse),
    StrategyEntry("S-02", "Trailing-whitespace strip", s02_trailing_whitespace_strip),
    StrategyEntry("S-03", "Decorative HR removal", s03_decorative_hr_removal),
    StrategyEntry("S-04", "Pipe-table padding collapse", s04_pipe_table_padding_collapse),
    StrategyEntry("S-07", "HTML comment removal", s07_html_comment_removal),
    StrategyEntry("S-10", "Conventions-header LABELS-ONLY", s10_labels_only_abbreviation),
    StrategyEntry(
        "S-23", "Reference-style citation shortcuts", s23_reference_style_citations,
    ),
]

TASKLIST_PIPELINE: list[StrategyEntry] = [
    StrategyEntry(
        "S-01", "Whitespace collapse + HR removal",
        s01_whitespace_collapse_with_hr,
    ),
    StrategyEntry("S-02", "Trailing-whitespace strip", s02_trailing_whitespace_strip),
    StrategyEntry("S-04", "Pipe-table padding collapse", s04_pipe_table_padding_collapse),
    StrategyEntry(
        "S-09", "Conventions-header (field labels)",
        lambda t: s09_conventions_header(t, mode="identifiers"),
    ),
    StrategyEntry("S-17", "Artifact-path template macro", s17_artifact_path_macro),
    StrategyEntry("S-18", "Step-tag abbreviation", s18_step_tag_abbreviation),
    StrategyEntry("S-10", "Section-label abbreviation", s10_labels_only_abbreviation),
    StrategyEntry("S-14", "Table default-row hoisting", s14_table_default_row_hoisting),
    StrategyEntry("S-19", "Checkpoint block template dedup", s19_checkpoint_block_dedup),
    StrategyEntry("S-20", "Template-block externalization", s20_template_block_externalization),
    StrategyEntry(
        "S-13", "Multi-paragraph bullet compaction",
        s13_multi_paragraph_bullet_compaction, lossy=True,
    ),
    StrategyEntry(
        "S-24", "Heading decorative suffix drop",
        s24_heading_decorative_suffix_drop, lossy=True,
    ),
]

PIPELINES: dict[str, list[StrategyEntry]] = {
    "roadmap": ROADMAP_PIPELINE,
    "spec": SPEC_PIPELINE,
    "tasklist": TASKLIST_PIPELINE,
}


# ============================================================================
# Section 6: Pipeline runner + high-level helpers
# ============================================================================

def run_pipeline(
    text: str,
    doc_type: str,
    aggressive: bool = False,
) -> tuple[str, list[StrategyStat]]:
    """Run the strategy pipeline for a document type.

    Returns (compressed_text, per_strategy_stats).
    """
    pipeline = PIPELINES[doc_type]
    stats: list[StrategyStat] = []
    current = text

    for entry in pipeline:
        if entry.lossy and not aggressive:
            continue
        before_bytes = len(current.encode("utf-8"))
        current = entry.fn(current)
        after_bytes = len(current.encode("utf-8"))
        stats.append(
            StrategyStat(
                id=entry.id,
                name=entry.name,
                bytes_before=before_bytes,
                bytes_after=after_bytes,
            )
        )

    return current, stats


def compress_file(
    input_path: Path,
    doc_type: str,
    output_path: Path,
    aggressive: bool = False,
) -> list[StrategyStat]:
    """Read input_path, compress with the doc_type pipeline, write output_path.

    Returns the per-strategy stats list. Raises FileNotFoundError if
    input_path does not exist or KeyError if doc_type is unknown.
    """
    text = input_path.read_text(encoding="utf-8")
    compressed, stats = run_pipeline(text, doc_type, aggressive=aggressive)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(compressed, encoding="utf-8")
    return stats
