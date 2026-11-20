"""Static tests for the /sc:worktrees command file (issue 687, source section 5).

Enforcement type: STATIC (command file text).
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COMMAND = ROOT / "src/superclaude/commands/worktrees.md"

OPTION_ROWS = ["list", "archive", "retire", "prune", "--apply", "--out"]
FORBIDDEN_OPTIONS = ["--force", "--yes", "--unattended"]
STOP_SENTENCE = (
    "`/sc:worktrees` runs only inside an IronClaude checkout "
    "that has `scripts/worktree_cleanup.py`"
)
RUN_LINE = (
    "uv run --no-project python scripts/worktree_cleanup.py "
    "<verb> [<worktree>] [--apply] [--out <dir>]"
)


def _text() -> str:
    return COMMAND.read_text(encoding="utf-8")


def _frontmatter() -> dict:
    head = _text().split("\n---\n", 1)[0]
    assert head.startswith("---\n")
    fields = {}
    for line in head[4:].splitlines():
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields


def _options_first_cells() -> list[str]:
    section = _text().split("## Options", 1)[1].split("\n## ", 1)[0]
    cells = []
    for line in section.splitlines():
        if not line.startswith("| `"):
            continue
        cell = line.strip().strip("|").split("|")[0].strip().strip("`")
        cells.append(cell.split(" ")[0])
    return cells


def _section(title: str) -> str:
    text = _text()
    start = text.index(f"## {title}")
    end = text.find("\n## ", start + 1)
    return text[start:] if end == -1 else text[start:end]


def test_frontmatter_fields():
    fields = _frontmatter()
    assert fields["name"] == "worktrees"
    assert fields["version"]
    assert fields["description"]
    assert fields["category"] == "workflow"
    assert fields["complexity"]
    assert fields["mcp-servers"] == "[]"
    assert "personas" in fields
    assert (
        fields["argument-hint"]
        == '"<list|archive|retire|prune> [<worktree>] [--apply] [--out <dir>]"'
    )


def test_the_sections_of_a_thin_command_are_all_there():
    text = _text()
    for title in (
        "Triggers",
        "Usage",
        "Options",
        "STOP rules",
        "Examples",
        "Outputs",
        "Boundaries",
    ):
        assert f"\n## {title}" in text, title


def test_options_table_lists_the_four_verbs_and_the_two_options():
    assert _options_first_cells() == OPTION_ROWS


def test_no_forbidden_option_is_listed_or_offered():
    cells = _options_first_cells()
    for flag in FORBIDDEN_OPTIONS:
        assert flag not in cells
        assert flag not in _text()


def test_the_stop_sentence_for_outside_a_checkout_is_exact():
    stop = _section("STOP rules")
    assert f'print "{STOP_SENTENCE}" and stop, running nothing' in stop
    assert "git rev-parse --show-toplevel" in stop
    assert "usage block" in stop and "running nothing" in stop


def test_it_runs_the_script_with_the_typed_arguments_and_no_skill():
    runs = _section("What it runs")
    assert RUN_LINE in runs
    assert "No skill is activated" in runs
    assert "adding nothing" in runs
    assert "Skill sc:" not in _text()
    # a heading named Activation would make the architecture lint demand a skill folder
    assert not re.search(r"^#+\s*Activation", _text(), re.M)


def test_apply_is_passed_only_when_typed():
    text = _text()
    assert "Pass `--apply` only when the person typed it" in text
    assert "Add `--apply`, a force flag or any other flag of its own" in _section(
        "Boundaries"
    )
    assert "`list`, `retire` and `prune` are dry runs unless you type `--apply`" in text
    # archive is the one verb that writes without --apply (to the evidence repo only)
    assert "`archive` is the one verb that writes without it" in text


def test_no_text_says_every_verb_is_a_dry_run():
    """archive saves to the evidence repo without --apply, so "every verb is a dry run" is false."""
    files = [
        COMMAND,
        ROOT / "docs/user-guide/commands.md",
        ROOT / "src/superclaude/core/HOW-WE-WORK.md",
        ROOT / "plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md",
        ROOT / "scripts/worktree_cleanup.py",
    ]
    for path in files:
        body = path.read_text(encoding="utf-8")
        assert "Every verb is a dry run" not in body, path
        assert "every verb is a dry run" not in body, path
        assert "Verbs (a dry run unless --apply is given)" not in body, path
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    entry = changelog.split("New command: /sc:worktrees", 1)[1].split("\n### ", 1)[0]
    assert "Every verb is a dry run" not in entry
    assert "`archive` is the one verb that writes without it" in entry


def test_boundaries_and_the_worker_rule():
    text = _text()
    boundaries = _section("Boundaries")
    assert "**Will:**" in boundaries and "**Will Not:**" in boundaries
    assert "Merge anything, push to a source repo" in boundaries
    assert "Run as a dispatched worker" in boundaries
    assert "never-as-worker list in `~/.claude/WORKER-CONTRACT.md`" in text
    assert not re.search(r"^#+\s*Unattended mode", text, re.M | re.I)


def test_no_source_tree_path():
    assert "src/superclaude/" not in _text()


def test_no_em_or_en_dash():
    dashes = (chr(0x2014), chr(0x2013))  # built from code points so this file has none
    for text in (_text(), Path(__file__).read_text(encoding="utf-8")):
        assert not any(d in text for d in dashes)


def test_the_command_is_thin():
    assert len(_text().splitlines()) <= 110
