"""Contract tests for the routing guide's two machine-read blocks.

The guide (src/superclaude/core/HOW-WE-WORK.md) carries two marker-delimited
blocks that other files read: the level table (printed by /sc:help, copied into
core/CLAUDE.md) and the routing table (read by /sc:recommend). Consumers find
the blocks by marker, never by line number, so these tests pin the markers,
the column contract, and every command, skill, flag and section the table names.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[2]
_GUIDE = _REPO / "src/superclaude/core/HOW-WE-WORK.md"
_COMMANDS = _REPO / "src/superclaude/commands"
_SKILLS = _REPO / "src/superclaude/skills"

_LEVEL_BEGIN, _LEVEL_END = "<!-- level-table:v1 -->", "<!-- /level-table -->"
_ROUTE_BEGIN, _ROUTE_END = "<!-- routing-table:v1 -->", "<!-- /routing-table -->"
_OTHER_BEGIN, _OTHER_END = "<!-- other-commands:v1 -->", "<!-- /other-commands -->"

# Spec section 4 row 10: commands the guide must route through "Other commands".
_OTHER_COMMANDS = {
    "sc:build",
    "sc:git",
    "sc:spawn",
    "sc:index-repo",
    "sc:agent",
    "sc:pm",
    "sc:save",
    "sc:load",
    "sc:cli-eval",
    "sc:post-release",
    "sc:review-translation",
    "sc:validate-tests",
    "sc:init-lite",
}

_COLUMNS = [
    "id",
    "intent",
    "level",
    "steps",
    "mandatory_flags",
    "changes_files",
    "section",
    "notes",
]
_LEVEL_HEADER = ["Level", "Use this when", "What you run", "What you end up with"]

# Row ids are stable keys: /sc:recommend cites them and the live run uses them.
# A row may be added; none of these may be renamed or removed.
_EXPECTED_IDS = {
    "ask",
    "small-change",
    "simple-plan",
    "task-file",
    "feature-existing",
    "research-first",
    "full-spec",
    "shape-idea",
    "bug",
    "external-research",
    "module-health",
    "compare-options",
    "critique-spec",
    "business-strategy",
    "multi-model-review",
    "cleanup",
    "tests",
    "document-built",
    "check-plan",
    "confirm-built",
    "review-pr",
    "resume",
    "unsure",
}

# Claude Code built-in slash commands the guide may name without a source file.
_BUILTINS = {"code-review", "security-review"}

# A command or skill token: a backtick immediately followed by a slash. Anchoring
# on the backtick avoids path fragments such as `.dev/tasks/to-do`.
_TOKEN_RE = re.compile(r"`/([a-z][a-z0-9:-]*)")
_FLAG_RE = re.compile(r"--[a-z][a-z0-9-]*")
_SPAN_RE = re.compile(r"`([^`]*)`")
_STEP_RE = re.compile(r"^(\d+[a-z]?)\.\s")
_HEADING_RE = re.compile(r"^#{2,3} (\d+(?:\.\d+)?)[.\s]", re.M)


def _text() -> str:
    return _GUIDE.read_text(encoding="utf-8")


def _block(text: str, begin: str, end: str) -> str:
    start = text.index(begin) + len(begin)
    return text[start : text.index(end, start)]


def _cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _table_rows(block: str) -> list[str]:
    return [ln for ln in block.splitlines() if ln.strip().startswith("|")]


def _routing_rows() -> list[dict[str, str]]:
    rows = _table_rows(_block(_text(), _ROUTE_BEGIN, _ROUTE_END))
    return [dict(zip(_COLUMNS, _cells(r), strict=True)) for r in rows[2:]]


def _steps(row: dict[str, str]) -> dict[str, str]:
    out = {}
    for part in row["steps"].split("<br>"):
        m = _STEP_RE.match(part.strip())
        assert m, f"{row['id']}: step without a label: {part!r}"
        out[m.group(1)] = part.strip()
    return out


def _command_text(token: str) -> str | None:
    """Return the source text for a /sc:<name> command or a /<skill>; None for a built-in."""
    if token.startswith("sc:"):
        path = _COMMANDS / f"{token[3:]}.md"
        assert path.is_file(), f"/{token} has no {path.relative_to(_REPO)}"
        return path.read_text(encoding="utf-8")
    if token in _BUILTINS:
        return None
    path = _SKILLS / token / "SKILL.md"
    assert path.is_file(), (
        f"/{token} is neither a built-in nor a skill under src/superclaude/skills/"
    )
    return path.read_text(encoding="utf-8")


@pytest.mark.parametrize("marker", [_LEVEL_BEGIN, _LEVEL_END, _ROUTE_BEGIN, _ROUTE_END])
def test_each_marker_appears_exactly_once(marker):
    assert _text().count(marker) == 1


def test_markers_are_ordered():
    t = _text()
    assert (
        t.index(_LEVEL_BEGIN)
        < t.index(_LEVEL_END)
        < t.index(_ROUTE_BEGIN)
        < t.index(_ROUTE_END)
    )


def test_level_table_block():
    block = _block(_text(), _LEVEL_BEGIN, _LEVEL_END)
    rows = _table_rows(block)
    assert _cells(rows[0]) == _LEVEL_HEADER
    assert set(rows[1].replace("|", "").strip()) <= {"-", " "}
    data = rows[2:]
    assert len(data) == 6
    for n, row in enumerate(data, 1):
        cells = _cells(row)
        assert len(cells) == 4, row
        assert cells[0].startswith(f"**{n}. "), row
    assert "**Hard limit:**" in block


def test_routing_header_and_separator():
    rows = _table_rows(_block(_text(), _ROUTE_BEGIN, _ROUTE_END))
    assert _cells(rows[0]) == _COLUMNS
    assert _cells(rows[1]) == ["---"] * 8


def test_every_row_has_eight_cells_and_no_pipe_in_a_cell():
    rows = _table_rows(_block(_text(), _ROUTE_BEGIN, _ROUTE_END))
    for row in rows:
        assert "\\|" not in row, f"escaped pipe: {row[:60]}"
        assert len(_cells(row)) == 8, f"{len(_cells(row))} cells: {row[:60]}"
        assert row.isascii(), f"non-ASCII: {row[:60]}"


def test_ids_unique_kebab_and_stable():
    ids = [r["id"] for r in _routing_rows()]
    assert len(ids) == len(set(ids))
    assert all(re.fullmatch(r"[a-z][a-z0-9-]*", i) for i in ids), ids
    assert _EXPECTED_IDS <= set(ids), _EXPECTED_IDS - set(ids)


def test_level_and_changes_files_vocabulary():
    for r in _routing_rows():
        assert re.fullmatch(r"[1-6]|-", r["level"]), r["id"]
        assert r["changes_files"] in {"no", "yes", "asks first"}, r["id"]


def test_every_command_and_skill_token_exists():
    for r in _routing_rows():
        for col in ("steps", "notes"):
            for token in _TOKEN_RE.findall(r[col]):
                _command_text(token)


def _non_slash_command_spans(clause: str) -> list[tuple[int, int]]:
    """Code spans that start with a non-slash command word, e.g. `git log --oneline`.

    Their flags belong to that shell command, not to a slash command or skill.
    """
    spans = []
    for m in _SPAN_RE.finditer(clause):
        first = m.group(1).strip().split(" ", 1)[0]
        if first and not first.startswith(("/", "--", "<")):
            spans.append((m.start(), m.end()))
    return spans


def _notes_flag_errors(row_id: str, notes: str, step_sources: list[str]) -> list[str]:
    """Check every slash-command flag in a notes cell; return the problems found.

    Notes are split into clauses on `;`. A flag must exist in the nearest
    `/command` token before it in the same clause; when the clause names none,
    the flag must exist in at least one of the row's step commands (notes such
    as "add `--spec <path>` to step 1"). Flags inside a code span that starts
    with a non-slash command (such as `git log --oneline`) are not checked.
    """
    errors = []
    for clause in notes.split(";"):
        skip = _non_slash_command_spans(clause)
        for m in _FLAG_RE.finditer(clause):
            if any(a <= m.start() < b for a, b in skip):
                continue
            flag = m.group(0)
            before = _TOKEN_RE.findall(clause[: m.start()])
            if before:
                source = _command_text(before[-1])
                if source is not None and flag not in source:
                    errors.append(f"{row_id}: notes {flag} not in /{before[-1]}")
            elif not any(flag in s for s in step_sources):
                errors.append(f"{row_id}: notes {flag} not in any step command")
    return errors


def test_every_notes_flag_exists_in_its_command():
    """A slash-command flag in `notes` must exist in the command it belongs to."""
    for r in _routing_rows():
        notes = r["notes"]
        if notes == "-":
            continue
        step_sources = [
            src
            for tok in _TOKEN_RE.findall(r["steps"])
            if (src := _command_text(tok)) is not None
        ]
        errors = _notes_flag_errors(r["id"], notes, step_sources)
        assert not errors, errors


def test_notes_flag_check_still_rejects_unknown_slash_command_flags():
    notes = "re-run `/sc:reflect --mode post --no-such-flag`"
    assert _notes_flag_errors("probe", notes, []) == [
        "probe: notes --no-such-flag not in /sc:reflect"
    ]
    assert _notes_flag_errors("probe", "add `--no-such-flag` to step 1", []) == [
        "probe: notes --no-such-flag not in any step command"
    ]


def test_notes_flag_check_ignores_flags_of_non_slash_commands():
    notes = "find that commit with `git log --oneline`; add `--no-promote`"
    reflect = _command_text("sc:reflect")
    assert reflect is not None
    assert _notes_flag_errors("probe", notes, [reflect]) == []


def test_other_commands_block_names_spec_row_10_commands():
    t = _text()
    assert t.count(_OTHER_BEGIN) == 1 and t.count(_OTHER_END) == 1
    assert t.index(_LEVEL_END) < t.index(_OTHER_BEGIN) < t.index(_ROUTE_BEGIN)
    block = _block(t, _OTHER_BEGIN, _OTHER_END)
    named = set(_TOKEN_RE.findall(block))
    assert _OTHER_COMMANDS <= named, _OTHER_COMMANDS - named
    for token in named:
        _command_text(token)


def test_mandatory_flags_name_real_steps_and_real_flags():
    for r in _routing_rows():
        if r["mandatory_flags"] == "-":
            continue
        steps = _steps(r)
        for entry in r["mandatory_flags"].split(";"):
            label, _, flags = entry.strip().partition(":")
            assert label in steps, (
                f"{r['id']}: mandatory flag for unknown step {label!r}"
            )
            found = _FLAG_RE.findall(flags)
            assert found, f"{r['id']}: step {label} entry has no flag"
            tokens = _TOKEN_RE.findall(steps[label])
            assert tokens, f"{r['id']}: step {label} names no command"
            source = _command_text(tokens[0])
            if source is None:
                continue
            for flag in found:
                assert flag in source, f"{r['id']}: {flag} not in /{tokens[0]} source"


def test_every_section_reference_is_a_heading():
    headings = set(_HEADING_RE.findall(_text()))
    for r in _routing_rows():
        for ref in (s.strip() for s in r["section"].split(",")):
            assert ref in headings, f"{r['id']}: section {ref} has no heading"


def test_guide_is_ascii_except_the_ruling_example():
    # GUIDE G8: the /sc:implement ruling example must keep real em dashes
    # (ledger regex in sc-implement-protocol/refs/ledger.md); nothing else may.
    for n, line in enumerate(_text().splitlines(), 1):
        if not line.isascii():
            assert "Ruling:" in line, f"line {n} is not ASCII: {line[:60]}"


def test_guide_is_not_an_at_import_anywhere():
    roots = [_REPO / "src/superclaude", _REPO / "plugins/superclaude"]
    files = [p for root in roots for p in root.rglob("*.md")]
    files += [_REPO / "CLAUDE.md", _REPO / "AGENTS.md"]
    for path in files:
        if path.is_file():
            assert not re.search(
                r"^\s*@\S*HOW-WE-WORK", path.read_text(encoding="utf-8"), re.M
            ), path


# Spec 3.2 (line 63): when the guide names a required flag for a step, the
# recommendation must include it. Each row that steps through one of these commands
# lists the flag as mandatory on that step, so /sc:recommend always emits it.
_MANDATORY_FLAGS = {
    "/sc:auggie-review": "--no-post-pr",
    "/sc:pr-submit": "--monitor 3",
    "/sc:reflect --mode post": "--no-promote",
}


@pytest.mark.parametrize("command,flag", sorted(_MANDATORY_FLAGS.items()))
def test_named_mandatory_flags_are_on_their_steps(command, flag):
    checked = 0
    for row in _routing_rows():
        if row["id"] not in ("review-pr", "confirm-built"):
            continue
        for label, step in _steps(row).items():
            if f"`{command}" not in step:
                continue
            checked += 1
            assert f"{label}: `{flag}`" in row["mandatory_flags"], (
                f"{row['id']} step {label}: {flag} not mandatory"
            )
    assert checked, f"no review-pr or confirm-built step runs {command}"
