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

# Additional operations and explicit coordination, not an Other-only namespace.
_OTHER_COMMANDS = {
    "sc:build",
    "sc:git",
    "sc:graph",
    "sc:impact",
    "sc:spawn",
    "sc:index",
    "sc:index-repo",
    "sc:agent",
    "sc:pm",
    "sc:save",
    "sc:load",
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
    "installed-inventory",
    "focused-design",
    "technical-design-document",
    "cleanup-audit-only",
    "contained-improve",
    "auggie-review-only",
    "localization-review",
    "context-audit",
    "cli-eval-create",
    "cli-eval-run",
    "cli-portification-spec",
    "release-boundary",
    "post-release",
    "roadmap-artifacts",
    "sprint-tasklist-bundle",
    "roadmap-fidelity",
    "tier-validation",
}

# Claude Code built-in slash commands the guide may name without a source file.
_BUILTINS = {"code-review", "rename", "security-review"}

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


def test_other_commands_membership_and_live_references():
    t = _text()
    assert t.count(_OTHER_BEGIN) == 1 and t.count(_OTHER_END) == 1
    assert t.index(_LEVEL_END) < t.index(_OTHER_BEGIN) < t.index(_ROUTE_BEGIN)
    block = _block(t, _OTHER_BEGIN, _OTHER_END)
    members = {_TOKEN_RE.findall(_cells(line)[0])[0] for line in _table_rows(block)[2:]}
    assert members == _OTHER_COMMANDS
    assert "entries can be referenced by outcome routes" in t
    assert not members & {
        "sc:help",
        "sc:cli-eval",
        "sc:cli-portify",
        "sc:init-lite",
        "sc:post-release",
        "sc:review-translation",
        "sc:tdd",
        "sc:validate-roadmap",
        "sc:validate-tests",
    }
    for token in set(_TOKEN_RE.findall(block)):
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
            mandatory = {
                entry.partition(":")[0].strip(): entry.partition(":")[2]
                for entry in row["mandatory_flags"].split(";")
            }
            assert flag in _FLAG_RE.findall(mandatory.get(label, "")), (
                f"{row['id']} step {label}: {flag} not mandatory"
            )
    assert checked, f"no review-pr or confirm-built step runs {command}"


def test_direct_change_threshold_and_written_plan_requirement():
    """T01/T02: static contract for a three-edit rename versus eight blocks."""
    block = _block(_text(), _LEVEL_BEGIN, _LEVEL_END)
    direct = _cells(_table_rows(block)[3])
    assert "one source file (plus its test file)" in direct[1]
    assert "five edits or fewer" in direct[1]
    assert "already know exactly" in direct[1]
    assert "/sc:task" in direct[2]
    assert "more than 5 edits or touches more than one source file" in block
    assert "one block of consecutive changed lines" in block
    assert "8 places is 8 edits and requires a written plan" in block
    assert "Direct command selection does not waive" in block


@pytest.mark.parametrize(
    "row_id", ["simple-plan", "feature-existing", "research-first"]
)
def test_ordinary_routes_plan_with_workflow_then_implement(row_id):
    """T03/T06/T07: static route contract, not generated recommendations."""
    row = next(r for r in _routing_rows() if r["id"] == row_id)
    commands = _TOKEN_RE.findall(row["steps"])
    assert commands.index("sc:workflow") < commands.index("sc:implement")
    assert not {"task-builder", "task"} & set(commands)
    assert "--depth quick" not in row["mandatory_flags"]
    if row_id != "research-first":
        assert row["level"] == "3"
    else:
        assert "research-only requests stop after step 1" in row["notes"]


@pytest.mark.parametrize(
    "reason",
    [
        "File count",
        "multiple sessions",
        "existing spec/PRD/TDD",
        "risk",
        "auditability",
        "drift concerns",
        "resume",
    ],
)
def test_mdtm_cannot_be_selected_by_a_proxy_alone(reason):
    """T03/T06/T07/T08: size, specs, sessions and assurance are not MDTM gates."""
    block = _block(_text(), _LEVEL_BEGIN, _LEVEL_END)
    exclusion = next(
        line for line in block.splitlines() if line.startswith("File count")
    )
    assert reason in exclusion
    assert "alone never select level 4" in exclusion
    assert "twelve-file feature across several sessions still uses level 3" in exclusion
    ordinary = _cells(_table_rows(block)[4])
    assert "Ordinary implementation" in ordinary[1]
    assert "many files or several sessions" in ordinary[1]
    assert "with or without an existing spec" in ordinary[1]
    assert "few files" not in ordinary[1]
    assert "one or two sessions" not in ordinary[1]


def test_explicit_mdtm_creation_or_existing_task_execution_is_preserved():
    """T04: MDTM remains available for explicit or exceptional machinery needs."""
    row = next(r for r in _routing_rows() if r["id"] == "task-file")
    assert row["level"] == "4"
    assert "explicit MDTM" in row["intent"]
    assert "exceptionally complex long-running" in row["intent"]
    assert "research/checklist/phase-panel machinery need" in row["intent"]
    steps = _steps(row)
    assert "task-builder" in _TOKEN_RE.findall(steps["1a"])
    assert "existing MDTM task" in steps["1b"]
    assert "without rebuilding" in steps["1b"]
    assert _TOKEN_RE.findall(steps["3"]) == ["task"]
    assert "only when execution is requested" in steps["3"]


def test_existing_approved_plan_and_explicit_executor_keep_their_identity():
    """T05/T10/T11: resume and explicit implement do not become MDTM execution."""
    block = _block(_text(), _LEVEL_BEGIN, _LEVEL_END)
    assert (
        "adequate approved plan already exists, use its existing executor directly"
        in block
    )
    assert "do not rebuild it" in block
    assert "Managed workflow packages use `/sc:implement`" in block
    assert "existing MDTM execution uses `/task`" in block
    assert (
        "Explicit `/sc:implement` selection retains that executor's own semantics"
        in block
    )
    assert (
        "not MDTM checklist/phase execution, even if the source resembles MDTM" in block
    )
    resume = next(r for r in _routing_rows() if r["id"] == "resume")
    assert "rerun the same command" in resume["steps"]
    assert "sc:implement" in _TOKEN_RE.findall(resume["steps"])
    assert "task-builder" not in _TOKEN_RE.findall(resume["steps"])


def test_inspection_breadth_does_not_require_an_implementation_plan():
    """T12: reading thirty files for a report is not a thirty-file source edit."""
    block = _block(_text(), _LEVEL_BEGIN, _LEVEL_END)
    assert "Inspection breadth is not mutation breadth" in block
    assert (
        "reading thirty files for an explanation or report does not require an implementation plan"
        in block
    )
    ask = next(r for r in _routing_rows() if r["id"] == "ask")
    assert ask["changes_files"] == "no"
    assert not {"sc:workflow", "task-builder"} & set(_TOKEN_RE.findall(ask["steps"]))


def test_contained_cleanup_exception_retains_safeguards_not_structural_migration():
    """T13: the folder exception preserves its checkpoint and diff boundary."""
    block = _block(_text(), _LEVEL_BEGIN, _LEVEL_END)
    assert "contained `/sc:cleanup` and `/sc:improve` work on a folder" in block
    assert "commit first and review `git diff` afterwards" in block
    assert "This exception does not cover structural migrations" in block
    cleanup = _block(_text(), "### 3.7 ", "### 3.8 ")
    assert "Commit first" in cleanup
    assert "Review `git diff`" in cleanup
    assert (
        "Structural refactors or work outside the contained-folder exception" in cleanup
    )
    assert "`/sc:workflow <spec path>`" in cleanup
    assert "`/sc:implement <printed plan path>`" in cleanup
    assert "exception does not cover an architectural migration" in cleanup


def test_full_spec_ordinary_post_document_planning_is_workflow_first():
    """S18: static full-spec branch contract; no model-generation run implied."""
    row = next(r for r in _routing_rows() if r["id"] == "full-spec")
    steps = _steps(row)
    assert "only for requested ordinary planning" in steps["7a"]
    assert _TOKEN_RE.findall(steps["7a"]) == ["sc:workflow"]
    assert "accepted PRD/TDD paths and constraints" in steps["7a"]
    assert _TOKEN_RE.findall(steps["8a"]) == ["sc:implement"]
    assert "only for requested execution of 7a" in steps["8a"]
    assert "new components and existing specs do not justify MDTM" in row["notes"]
    section = _block(_text(), "### 3.1 ", "### 3.2 ")
    assert "Ordinary post-document planning uses workflow" in section
    assert "--depth standard --handoff none" in section


def test_document_only_full_spec_stops_without_downstream_planning():
    """T09/S19: static document-only stop, preserving document-owned machinery."""
    row = next(r for r in _routing_rows() if r["id"] == "full-spec")
    assert (
        "documents-only requests stop after the requested documents and reviews"
        in row["notes"]
    )
    assert "without a roadmap or phase tasks" in row["notes"]
    section = _block(_text(), "### 3.1 ", "### 3.2 ")
    stop = section.index(
        "For documents only, stop after the requested documents and reviews"
    )
    assert stop < section.index("1. **Shape the idea")
    assert "do not append a roadmap, phase tasks, implementation or shipping" in section
    assert "PRD and TDD skills keep their own document-generation machinery" in section


def test_explicit_roadmap_preserves_its_composer_and_phase_task_outputs():
    """S20: static explicit-roadmap branch, not a substitute for generation evals."""
    row = next(r for r in _routing_rows() if r["id"] == "full-spec")
    steps = _steps(row)
    assert (
        "only for explicit composer selection or exceptional level-4 machinery needs"
        in steps["7b"]
    )
    assert _TOKEN_RE.findall(steps["7b"]) == ["roadmap"]
    assert "supplied documents" in steps["7b"]
    assert _TOKEN_RE.findall(steps["8b"]) == ["task"]
    assert "only for requested execution" in steps["8b"]
    assert "uses task-builder/task internally" in row["notes"]
    assert "full setting creates phase task files" in row["notes"]
    section = _block(_text(), "### 3.1 ", "### 3.2 ")
    assert "exceptionally complex, long-running phased program" in section
    assert "composer internally uses `/task-builder` and `/task`" in section
    assert "not permission to implement product phases" in section


def test_standard_planning_default_and_conditional_quick_are_consistent():
    block = _block(_text(), _LEVEL_BEGIN, _LEVEL_END)
    assert "--depth standard --handoff none" in block
    assert "Standard is the default; use quick for smaller checked plans" in block
    simple = next(r for r in _routing_rows() if r["id"] == "simple-plan")
    assert simple["mandatory_flags"] == "-"
    assert "quick is conditional for smaller checked plans" in simple["notes"]
    section = _block(_text(), "### 3.3 ", "### 3.4 ")
    assert "Standard is the ordinary planning default" in section
    assert "for this smaller checked plan, quick is appropriate" in section


def test_bug_planning_and_brainstorm_follow_on_do_not_use_size_to_choose_mdtm():
    bug = next(r for r in _routing_rows() if r["id"] == "bug")
    steps = _steps(bug)
    assert _TOKEN_RE.findall(steps["3b"]) == ["sc:workflow", "sc:implement"]
    assert "only explicit or exceptionally justified MDTM" in steps["3c"]
    assert "--depth quick" not in bug["mandatory_flags"]
    assert (
        "deep diagnosis without fix can feed separate ordinary workflow planning"
        in bug["notes"]
    )
    shape = next(r for r in _routing_rows() if r["id"] == "shape-idea")
    assert "stop at merged requirements" in shape["notes"]
    assert "no automatic task-file handoff" in shape["notes"]
    assert "--handoff task" not in _text()


@pytest.mark.parametrize(
    "stale_policy",
    [
        "fits in one or two sessions",
        "level 4 for anything larger, longer, or riskier",
        "Use the second pair for many files, multi-session work",
        "Add `--handoff task` to go straight to a task file",
        "For work that changes code, prefer `/task-builder`",
    ],
)
def test_old_size_based_mdtm_policy_is_not_retained(stale_policy):
    assert stale_policy not in _text()


@pytest.mark.parametrize(
    "case,row_id,targets,inputs,boundaries",
    [
        (
            "S01",
            "installed-inventory",
            {"sc:help"},
            ["live inventory"],
            ["no install repair"],
        ),
        (
            "S02",
            "focused-design",
            {"sc:design"},
            ["<target>", "type/format"],
            ["code format is design guidance", "no declared output flag"],
        ),
        (
            "S03",
            "technical-design-document",
            {"tdd", "sc:tdd"},
            ["supplied PRD/stub", "code paths", "output", "tier"],
            [
                "Technical Design Document",
                "document-owned MDTM machinery",
                "verify template/agents/tools",
            ],
        ),
        (
            "S04",
            "cleanup-audit-only",
            {"sc:cleanup-audit"},
            ["<target>", "pass/focus/batch-size"],
            [
                "exclusion floor",
                "hidden-only targets are not exhaustively covered",
                "no cleanup, improve or commit",
            ],
        ),
        (
            "S05",
            "contained-improve",
            {"sc:improve"},
            ["<target>", "type/safe/interactive"],
            [
                "automatic edits",
                "no compulsory cleanup/deletions",
                "structural migration stays planned",
            ],
        ),
        (
            "S06",
            "auggie-review-only",
            {"sc:auggie-review"},
            ["resolved target", "supported controls"],
            [
                "--no-post-pr --no-remediation-offer",
                "internal reviewer only",
                "default prism-b",
            ],
        ),
        (
            "S07",
            "localization-review",
            {"sc:review-translation"},
            ["<source-file>", "<translation-files...>"],
            [
                "confirm context before review",
                "separate consent",
                "not runtime troubleshooting",
            ],
        ),
        (
            "S08",
            "context-audit",
            {"sc:init-lite"},
            ["--context-optimized", "project-root/output"],
            ["dry-run` writes nothing", "scaffold` is opt-in", "never context inputs"],
        ),
        (
            "S09",
            "cli-eval-create",
            {"sc:cli-eval"},
            ["create", "supplied name/from/agents"],
            ["schema-validated suite", "no automatic suite run"],
        ),
        (
            "S10",
            "cli-eval-run",
            {"sc:cli-eval"},
            ["run", "supplied suite/eval selectors"],
            [
                "confirm exact invocation/safety",
                "real execution and artifact writes",
                "no invented resume",
            ],
        ),
        (
            "S11",
            "cli-portification-spec",
            {"sc:cli-portify"},
            ["--workflow <skill-name-or-path>", "name/output/dry-run"],
            [
                "Phase 0-2",
                "no full spec synthesis or panel artifacts",
                "no-direct-code-files",
                "contract gap/unavailable",
            ],
        ),
        (
            "S12",
            "release-boundary",
            {"sc:release-split"},
            ["<release-artifact>", "supplied controls"],
            [
                "--no-split --resume-from <validated proposal>",
                "no-split is valid",
                "no product execution or Git",
            ],
        ),
        (
            "S13",
            "post-release",
            {"sc:post-release"},
            ["<existing release tag>", "supplied output"],
            [
                "tagged commit",
                "consolidated-plan gate",
                "separate outward-action approval",
                "never fabricated success",
            ],
        ),
        (
            "S14",
            "roadmap-artifacts",
            {"sc:roadmap"},
            ["supplied documents", "requested controls"],
            ["contract gap", "no combined interface", "not MDTM roadmap substitution"],
        ),
        (
            "S15",
            "sprint-tasklist-bundle",
            {"sc:tasklist"},
            ["<roadmap-path>", "supplied spec/output"],
            [
                "readable non-empty roadmap",
                "writable output parent",
                "no unsupported source flag",
                "no automatic Sprint/task execution",
            ],
        ),
        (
            "S16",
            "roadmap-fidelity",
            {"sc:validate-roadmap"},
            ["roadmap/spec sources", "supplied output directory"],
            [
                "command/protocol contract gap",
                "explicitly denies CLI equivalence",
                "exit zero is not clean validation",
            ],
        ),
        (
            "S17",
            "tier-validation",
            {"sc:validate-tests"},
            ["YAML file/directory", "<verified target>"],
            [
                "default is absent",
                "report missing prerequisite",
                "no code/config repairs or fabricated counts",
            ],
        ),
    ],
    ids=lambda value: (
        value if isinstance(value, str) and re.fullmatch(r"S\d+", value) else None
    ),
)
def test_specialist_static_targets_inputs_and_stops(
    case, row_id, targets, inputs, boundaries
):
    """Static S01-S17 contracts; these are not model-generation evaluations."""
    row = next(r for r in _routing_rows() if r["id"] == row_id)
    assert targets <= set(_TOKEN_RE.findall(row["steps"])), case
    assert "3.13" in row["section"].split(", "), case
    for retained in inputs:
        assert retained in row["steps"], (case, retained)
    for boundary in boundaries:
        assert boundary in row["steps"] + " " + row["notes"], (case, boundary)
    assert not {"sc:workflow", "sc:implement", "task-builder", "task"} & set(
        _TOKEN_RE.findall(row["steps"])
    ), f"{case}: specialist deliverable acquired generic implementation"


def test_specialist_matching_and_unavailable_contract_are_shared_not_keyword_first():
    """T14-T22/T42/T45: outcome, authority and availability precede broad words."""
    guide = _text()
    routing = _block(guide, "## Routing table", _ROUTE_BEGIN)
    assert (
        "Match the whole requested outcome, explicit selection, supplied artifact and authority ceiling"
        in routing
    )
    assert (
        "Specialist objectives outrank generic review/error/tasklist/no-changes wording"
        in routing
    )
    assert "Resolve conditions before emitting steps" in routing
    assert "only the selected branch contributes mandatory flags" in routing
    assert "without appending execution or shipping to report-only goals" in routing
    section = _block(guide, "### 3.13 ", "### 3.14 ")
    assert "missing plugin capability is **unavailable**" in section
    assert "actual callable command/skill and relevant dependencies" in section
    assert "contract gap**, not a union of both interfaces" in section
    assert "new suite or a supervised existing-suite run" in section
    assert (
        "checked workflow plan, an MDTM checklist and a roadmap-to-Sprint bundle"
        in section
    )
    unsure = next(r for r in _routing_rows() if r["id"] == "unsure")
    assert "one useful clarification" in unsure["steps"]
    assert "sc:recommend" not in _TOKEN_RE.findall(unsure["steps"])
    assert "never recommend recommend to itself" in unsure["notes"]


def test_reports_keep_specialist_objective_instead_of_generic_competitor():
    """T15-T17/S07/S29: artifact labels and errors do not determine the objective."""
    rows = {r["id"]: r for r in _routing_rows()}
    business = rows["business-strategy"]
    assert "even when input is a PRD" in business["intent"]
    assert "document-or-inline-content" in business["steps"]
    assert "--mode <discussion/debate/socratic/adaptive>" in business["notes"]
    assert "--synthesis-only" in business["notes"]
    critique = rows["critique-spec"]
    assert critique["mandatory_flags"] == "-"
    assert "without a supported explicit mode" in critique["notes"]
    assert "discussion/socratic" in critique["notes"]
    assert "target-release clarification" in critique["notes"]
    assert "consent before input edits" in critique["notes"]
    assert "not raw PRD/TDD authoring, business viability" in critique["notes"]
    locale = rows["localization-review"]
    assert locale["changes_files"] == "no"
    assert "not runtime troubleshooting" in locale["notes"]
    assert not {"sc:troubleshoot", "sc:analyze"} & set(
        _TOKEN_RE.findall(locale["steps"])
    )


def test_requested_analysis_research_explain_modes_are_not_forced_defaults():
    """T22/T32/T33/S28: retain explicit controls and broad-analysis scope."""
    rows = {r["id"]: r for r in _routing_rows()}
    assert rows["module-health"]["mandatory_flags"] == "-"
    assert "no forced focus" in rows["module-health"]["notes"]
    assert (
        "--focus <area> --depth <quick/deep> --format <text/json/report>"
        in rows["module-health"]["notes"]
    )
    assert rows["external-research"]["mandatory_flags"] == "-"
    assert "quick/standard/deep/exhaustive" in rows["external-research"]["notes"]
    assert "not forced deep" in rows["external-research"]["notes"]
    assert (
        "--level <basic/intermediate/advanced> --format <text/examples/interactive> --context <domain>"
        in rows["ask"]["notes"]
    )
    assert rows["ask"]["changes_files"] == "no"


def test_adversarial_generation_comparison_and_pipeline_remain_exclusive():
    """S22: static required inputs and owned continuation, not single-file compare."""
    row = next(r for r in _routing_rows() if r["id"] == "compare-options")
    steps = _steps(row)
    assert "2-10 readable files" in steps["1a"]
    assert "--compare" in steps["1a"] and "--source" not in steps["1a"]
    assert all(flag in steps["1b"] for flag in ("--source", "--generate", "--agents"))
    assert all(
        flag in steps["1c"] for flag in ("--pipeline", "--pipeline-resume", "--output")
    )
    assert not {"--compare", "--source", "--generate", "--agents"} & set(
        _FLAG_RE.findall(steps["1c"])
    )
    assert "mutually exclusive" in row["notes"]
    assert "no one-file comparison or product execution" in row["notes"]


def test_cleanup_audit_and_improvement_have_separate_authority_boundaries():
    """S04/S05: reporting cannot acquire deletion, improvement or a commit."""
    rows = {r["id"]: r for r in _routing_rows()}
    audit = rows["cleanup-audit-only"]
    assert audit["changes_files"] == "no"
    assert _TOKEN_RE.findall(audit["steps"]) == ["sc:cleanup-audit"]
    assert "commit" not in audit["steps"]
    assert "default surface, not forced all" in audit["notes"]
    assert "later passes need earlier context" in audit["notes"]
    assert "hidden/BMAD paths are an unremovable exclusion floor" in audit["notes"]
    improve = rows["contained-improve"]
    assert _TOKEN_RE.findall(improve["steps"]) == ["sc:improve"]
    assert "checkpoint commit" in improve["steps"] and "git diff" in improve["steps"]
    assert "sc:cleanup" not in _TOKEN_RE.findall(improve["steps"])
    assert "sc:improve" not in _TOKEN_RE.findall(rows["cleanup"]["steps"])


def test_previews_documentation_and_suite_runs_disclose_actual_writes():
    """T34-T39: preview artifacts, document forms and real runs stay distinct."""
    rows = {r["id"]: r for r in _routing_rows()}
    section = _block(_text(), "### 3.6 ", "### 3.7 ")
    assert "brainstorm dry run can write preparatory artifacts" in section
    portify = rows["cli-portification-spec"]["notes"]
    assert "dry-run writes Phase 0-2 artifacts" in portify
    assert "no full spec synthesis or panel artifacts" in portify
    context = rows["context-audit"]
    assert "--context-optimized" in context["mandatory_flags"]
    assert "dry-run` writes nothing and creates no output directory" in context["notes"]
    assert (
        "force` is limited to owned artifacts, never context inputs" in context["notes"]
    )
    tests = rows["tests"]
    assert tests["mandatory_flags"] == "-"
    assert "watch never adds fix" in tests["notes"]
    assert "needs explicit repair intent" in tests["notes"]
    assert "new tests are authoring, YAML tier validation is separate" in tests["notes"]
    docs = rows["document-built"]
    assert {
        "sc:document",
        "sc:index",
        "tech-reference",
        "operational-guide",
        "readme",
    } <= set(_TOKEN_RE.findall(docs["steps"]))
    assert (
        "--type <inline/external/api/guide> --style <brief/detailed>" in docs["notes"]
    )
    assert (
        "inline source changes retain direct-change limits or workflow planning"
        in docs["notes"]
    )
    assert "real execution and artifact writes" in rows["cli-eval-run"]["notes"]
    assert "no automatic suite run" in rows["cli-eval-create"]["notes"]


def test_diagnosis_reflection_and_review_preserve_remediation_coupling():
    """T23-T27/T59-T62/S06: depth is not unrequested execution authority."""
    rows = {r["id"]: r for r in _routing_rows()}
    bug = rows["bug"]
    assert "diagnosis-only stops after step 2" in bug["notes"]
    assert (
        "no speculative fix for an unconfirmed, failed or blocked result"
        in bug["notes"]
    )
    assert "standard `/sc:troubleshoot --fix` offers workflow planning" in bug["notes"]
    assert "after supported diagnosis and acceptance" in bug["notes"]
    assert "--depth quick --fix` is invalid" in bug["notes"]
    assert "--depth deep --fix` couples to MDTM" in bug["notes"]
    assert (
        "deep diagnosis without fix can feed separate ordinary workflow planning"
        in bug["notes"]
    )
    reflect = rows["confirm-built"]["notes"]
    assert (
        "standard `/sc:reflect --remediate` offers workflow after acceptance" in reflect
    )
    assert "explicit deep remediation couples to MDTM" in reflect
    assert "--tier 2 --depth standard --remediate" in reflect
    assert "legacy task analyze/validate aliases remain supported" in reflect
    assert "no headless auto-fix substitution" in reflect
    section = _block(_text(), "### 3.10 ", "### 3.11 ")
    assert "Deep alone does not remediate" in section
    assert "carried hardening blockers" in section
    assert "consume it rather than repeat it" in section
    review = rows["auggie-review-only"]["notes"]
    assert "accepted deep offer currently selects MDTM" in review
    assert "ordinary review offer uses workflow" in review
    assert (
        "deep plus ordinary later planning suppresses offer and plans separately"
        in review
    )
    assert "undeclared design referral gap" in review
    assert "no-post-pr --no-remediation-offer" in review


def test_reflect_optional_inputs_and_report_only_post_flags():
    """T28-T31: pre needs a spec; post accepts diff-only or log-only."""
    rows = {r["id"]: r for r in _routing_rows()}
    pre = rows["check-plan"]
    pre_step = _steps(pre)["2"]
    assert "--mode pre --spec <spec>" in pre_step
    assert "--tasklist" not in pre_step
    assert "spec is required, tasklist optional" in pre["notes"]
    post = rows["confirm-built"]
    steps = _steps(post)
    assert "--diff <ref-or-path>" in steps["1a"]
    assert "--task-log" not in steps["1a"]
    assert "--task-log <log-path>" in steps["1b"]
    assert "--diff" not in steps["1b"]
    for label in ("1a", "1b"):
        assert not {"--spec", "--tasklist"} & set(_FLAG_RE.findall(steps[label]))
        assert "--no-promote" in steps[label]
        assert f"{label}: `--no-promote`" in post["mandatory_flags"]
    assert post["changes_files"] == "no"
    assert "not mandatory together" in post["notes"]


def test_pr_monitor_ceiling_is_conditional_and_each_branch_has_one_exact_value():
    """T63: keep the full-loop default while respecting lower authority ceilings."""
    row = next(r for r in _routing_rows() if r["id"] == "review-pr")
    steps = _steps(row)
    mandatory = {
        entry.partition(":")[0].strip(): entry.partition(":")[2].strip(" `")
        for entry in row["mandatory_flags"].split(";")
    }
    expected = {
        "6a": ("0", "creation-only or review App absent/uncertain"),
        "6b": ("1", "proposals without source edits"),
        "6c": ("2", "local fixes without publication"),
        "6d": ("3", "requested/authorized full loop"),
    }
    for label, (ordinal, condition) in expected.items():
        assert condition in steps[label]
        assert re.findall(r"--monitor\s+(\d+)", steps[label]) == [ordinal]
        assert mandatory[label] == f"--monitor {ordinal}"
        assert _TOKEN_RE.findall(steps[label]) == ["sc:pr-submit"]
    assert "6" not in mandatory, "No unconditional monitor ceiling on all branches"
    assert "--no-post-pr" in mandatory["4"]
    assert "--no-remediation-offer" in mandatory["4"]
    assert "choose exactly one 6 branch and one monitor ordinal" in row["notes"]
    assert "3 is the current command default" in row["notes"]
    assert "can commit/push/retrigger/reply/resolve" in row["notes"]
    assert "stronger-project-policy conflict" in row["notes"]
    assert "never silently increased" in row["notes"]
    assert "Always pass `--monitor 3`" not in _text()


def test_pr_attachment_monitor_log_resume_and_silence_are_not_new_shipping():
    """T64-T66: PR identity, logged ceiling and terminal failures stay explicit."""
    rows = {r["id"]: r for r in _routing_rows()}
    shipping = rows["review-pr"]["notes"]
    assert "--pr <number>" in shipping
    assert "not another creation" in shipping
    assert "origin repo, PR head and bounded cycle-fix push range" in shipping
    assert "head/CI prerequisites" in shipping
    assert "attended in-session, not daemon" in shipping
    assert "silence/timeout is not clean" in shipping
    assert "recommendation executes no Git/GitHub actions" in shipping
    resume = rows["resume"]
    steps = _steps(resume)
    assert _TOKEN_RE.findall(steps["1a"]) == ["sc:pr-submit"]
    assert "--resume <run-log.jsonl>" in steps["1a"]
    assert "--pr <number>" in steps["1b"]
    assert "recorded ceiling, not task execution or PR recreation" in resume["notes"]
    assert "no task-builder rebuild from resume alone" in resume["notes"]
    local = rows["auggie-review-only"]["notes"]
    assert "PR posting defaults on, local-only uses" in local
    assert "--no-post-pr --no-remediation-offer" in local
    assert "review-pr" not in rows["auggie-review-only"]["steps"]


def test_other_operations_preserve_requested_authority_and_owned_state():
    """S23-S27/T19/T72: utility operations are not generic implementation."""
    other = _block(_text(), _OTHER_BEGIN, _OTHER_END)
    assert "Status-only stays inspection" in other
    assert "a commit needs authorization" in other
    assert "Do not append push, merge or PR creation" in other
    assert "Compile/package existing code" in other
    assert "not new-feature implementation" in other
    assert "Broken compilation needs diagnosis" in other
    assert "mode=quick or mode=update" in other
    assert "PROJECT_INDEX.md and PROJECT_INDEX.json" in other
    assert "Coordinated project docs/API/structure/README" in other
    assert "needs no MCP server" in other
    assert ".superclaude/memory/" in other
    assert "writes memory; not durable task execution state" in other
    assert "Not executor resume" in other
    assert "inspect status, orient, then wait" in other
    assert "self-contained, not a missing protocol" in other
    assert "Not a default planner, automatic-start guarantee" in other
    assert "critical stop is a task hierarchy only" in other
    assert "no source edits or downstream implementation" in other
    assert "Branch tracing is limited" in other


def test_lifecycle_and_contract_gaps_do_not_certify_stale_or_mixed_interfaces():
    """T44-T51/T60/T74: keep known limits, without resurrecting retired targets."""
    guide = _text()
    limits = _block(guide, "### 3.14 ", "## 4. ")
    for retired in ("estimate", "the sc dispatcher", "select-tool", "task-mcp"):
        assert retired in limits
    assert "not current runnable framework targets" in limits
    assert "readable installed remnants survive" in limits
    assert "Explicit deprecated metadata and verified canonical retirement" in limits
    assert (
        "Answer retirement questions with the underlying intent and a current "
        "independently verified alternative" in limits
    )
    assert (
        "Independently authored installed-only/custom commands remain eligible"
        in limits
    )
    assert "uncertain ownership of a same-name override needs clarification" in limits
    assert "Do not delete, update or reinstall anything automatically" in limits
    for row in _routing_rows():
        assert not {"sc:estimate", "sc:sc", "sc:select-tool", "sc:task-mcp"} & set(
            _TOKEN_RE.findall(row["steps"] + row["notes"])
        )
    rows = {r["id"]: r for r in _routing_rows()}
    for row_id in ("roadmap-artifacts", "roadmap-fidelity"):
        assert "contract gap" in rows[row_id]["steps"]
        assert "asks first" == rows[row_id]["changes_files"]
        assert not {"--specs", "--agents", "--template", "--depth"} & set(
            _FLAG_RE.findall(rows[row_id]["steps"])
        ), "No runnable union of the conflicting command/protocol interfaces"
    assert (
        "Command and protocol disagree on missing-proxy STOP versus stub fallback"
        in guide
    )
    assert "Startup status messages do not prove agent/PM activation" in limits
    assert (
        "static routing assertions, generated recommendation results" in limits.lower()
    )
    assert (
        "Do not report fabricated quality scores, timing, savings or test counts"
        in limits
    )


def test_swarm_settings_help_retains_inputs_without_inferred_real_launch():
    """S21: settings help is specialized preparation, not real-model permission."""
    row = next(r for r in _routing_rows() if r["id"] == "multi-model-review")
    assert "swarm settings help" in row["intent"]
    assert _TOKEN_RE.findall(_steps(row)["1"]) == ["sc:swarm-wizard"]
    assert "supplied goal/target" in row["steps"]
    assert "stop at settings/preparation" in row["steps"]
    assert "explicitly authorized and prerequisites pass" in row["steps"]
    assert "keep goal, target and output" in row["notes"]
    assert "interview missing inputs or ambiguous lens" in row["notes"]
    assert "50 non-whitespace bytes" in row["notes"]
    assert "T2ProxyUrl/T2ProxyKey/T2Model01" in row["notes"]
    assert "confirmation after a passing stub dry run" in row["notes"]
    assert "contract gap on missing-proxy STOP versus fallback" in row["notes"]
    assert not {"sc:spec-panel", "sc:explain", "task-builder"} & set(
        _TOKEN_RE.findall(row["steps"])
    )


def test_explicit_cleanup_controls_and_pr_attachment_do_not_gain_default_actions():
    """T22/T64: defaults apply only after preserving explicit operation intent."""
    rows = {r["id"]: r for r in _routing_rows()}
    cleanup = rows["cleanup"]
    assert cleanup["mandatory_flags"] == "-"
    assert "--type <code/imports/files/all>" in cleanup["notes"]
    assert "never overwrite supported explicit choices" in cleanup["notes"]
    assert "attachment skips shipping steps 1-5" in rows["review-pr"]["notes"]


def test_grouped_required_flags_still_use_exact_flag_tokens():
    """Grouping two required controls cannot hide a missing or lookalike flag."""
    row = next(r for r in _routing_rows() if r["id"] == "review-pr")
    entry = next(
        item for item in row["mandatory_flags"].split(";") if item.startswith("4:")
    )
    required = _FLAG_RE.findall(entry.partition(":")[2])
    assert required == ["--no-post-pr", "--no-remediation-offer"]
    source = _command_text("sc:auggie-review")
    assert source is not None
    assert all(flag in source for flag in required)
    assert "--no-post-pr" not in _FLAG_RE.findall("--no-post-pr-lookalike")


def test_task_and_implement_verification_claims_are_not_universal_test_guarantees():
    """T73: static route claims distinguish manual checks, sanity and extras."""
    small = next(r for r in _routing_rows() if r["id"] == "small-change")
    assert "run the related test if it has not run" in small["steps"]
    assert (
        "STANDARD permits affected tests or documented manual verification"
        in small["notes"]
    )
    assert "LIGHT includes scope/sanity checks" in small["notes"]
    assert "manual verification as an observed test pass" in small["notes"]
    level_block = _block(_text(), _LEVEL_BEGIN, _LEVEL_END)
    direct = _cells(_table_rows(level_block)[3])
    assert (
        "STANDARD permits affected tests or documented manual verification" in direct[2]
    )
    assert "LIGHT includes scope/sanity checks" in direct[2]
    assert "Run the related test if it has not run" in direct[2]
    assert "it runs the affected tests itself" not in direct[2]
    assert "it skipped checking" not in direct[2]
    assert "observed related-test result when available" in direct[3]
    implementation = _block(_text(), "### 3.3 ", "### 3.4 ")
    assert (
        "tests as extras; compliance with the acceptance criteria is the task verdict"
        in implementation
    )
    assert "not every task uses an independent agent" in implementation
    assert "managed package's final review is independent" in implementation
