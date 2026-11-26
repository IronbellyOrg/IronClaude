"""Static tests for the /sc:git command file (T-12: FR-001 to FR-005, FR-090, NFR-010, NFR-012).

Enforcement type: STATIC (command file text). The protocol behind the command is
pinned in tests/skills/test_git_protocol.py; the helper in tests/vcs/.
"""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
COMMAND = ROOT / "src/superclaude/commands/git.md"

# FR-003: the sections, in this order.
SECTIONS = [
    "Triggers",
    "Usage",
    "Options",
    "STOP rules (checked before Activation)",
    "Behavioral Flow",
    "Activation",
    "Examples",
    "Outputs",
    "Boundaries",
    "Related Commands",
]

# FR-002: the usage forms, exactly these and no others.
USAGE_FORMS = [
    "/sc:git [status]",
    "/sc:git add <path>...",
    '/sc:git commit [<path>...] (--message "<text>" | --smart-commit)',
    "/sc:git branch [list | create <name> | switch <name> | cleanup]",
    "/sc:git submodule [status | update <path>... [--url <path>=<url>]..."
    ' | commit-pointer <path> (--message "<text>" | --smart-commit)]',
]

# FR-001: the argument-hint lists exactly the FR-002 operations.
ARGUMENT_HINT = (
    "status | add <path>... | commit [<path>...] (--message <text> | --smart-commit)"
    " | branch [list | create <name> | switch <name> | cleanup]"
    " | submodule [status | update <path>... [--url <path>=<url>]..."
    " | commit-pointer <path> (--message <text> | --smart-commit)]"
)

NOT_OPERATIONS = ("merge", "push", "pull", "fetch")


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


def _headings() -> list[str]:
    return re.findall(r"^## (.+?)\s*$", _text(), flags=re.M)


def _section(title: str) -> str:
    text = _text()
    start = text.index(f"\n## {title}") + 1
    end = text.find("\n## ", start + 1)
    return text[start:] if end == -1 else text[start:end]


def _usage_lines() -> list[str]:
    block = re.search(r"```[a-z]*\n(.*?)```", _section("Usage"), flags=re.S)
    assert block, "the Usage section has no fenced block"
    return [ln.strip() for ln in block.group(1).splitlines() if ln.strip()]


def test_frontmatter_fields():
    fields = _frontmatter()
    assert fields["name"] == "git"
    assert fields["description"].startswith('"') and fields["description"].endswith('"')
    assert len(fields["description"]) > 2
    assert fields["category"] == "version-control"
    assert fields["complexity"] == "moderate"
    assert fields["mcp-servers"] == "[]"
    assert fields["personas"] == "[]"
    assert fields["argument-hint"] == f'"{ARGUMENT_HINT}"'


def test_frontmatter_has_no_unattended_or_worker_field():
    head = _text().split("\n---\n", 1)[0]
    assert "unattended" not in head.lower()


def test_size_budget():
    assert len(_text().splitlines()) <= 150


def test_sections_in_order():
    assert _headings() == SECTIONS


def test_no_unattended_mode_section():
    assert "## Unattended mode" not in _text()
    assert not any("unattended" in h.lower() for h in _headings())


def test_usage_lists_exactly_the_fr002_forms():
    assert _usage_lines() == USAGE_FORMS


def test_usage_names_no_merge_push_pull_or_fetch_operation():
    usage = _section("Usage").lower()
    for word in NOT_OPERATIONS:
        assert not re.search(rf"\b{word}\b", usage), word
    for line in _usage_lines():
        assert not re.match(rf"/sc:git\s+({'|'.join(NOT_OPERATIONS)})\b", line)


def test_bare_invocation_runs_status():
    assert "A bare `/sc:git` runs `status`." in _section("Usage")


def test_options_document_every_operation_and_flag():
    cells = []
    for line in _section("Options").splitlines():
        if line.startswith("| `"):
            cells.append(line.strip().strip("|").split("|")[0].strip().strip("`"))
    first_words = {c.split(" ")[0] for c in cells}
    assert {
        "status",
        "add",
        "commit",
        "--message",
        "--smart-commit",
        "branch",
        "submodule",
        "--url",
    } <= first_words
    options = _section("Options")
    for token in ("list", "create", "switch", "cleanup", "update", "commit-pointer"):
        assert re.search(rf"`[^`]*\b{token}\b", options), token


def test_stop_rules_cover_fr004():
    stop = _section("STOP rules (checked before Activation)")
    assert "Print the usage block and run nothing" in stop
    assert "an unknown operation" in stop
    assert (
        "`push`, `pull`, `fetch`, `merge`, `rebase`, `reset`, `clean`, `stash`, "
        "`tag` or `pr` as the operation"
    ) in stop
    assert "`/sc:pr-submit`" in stop
    assert "merge is not a `/sc:git` operation" in stop
    assert "neither `--message` nor `--smart-commit`" in stop
    assert "both" in stop
    assert "`commit` or `commit-pointer`" in stop
    assert "`create` or `switch` without a name" in stop
    assert "forbidden-flag list" in stop
    assert "`--unattended`" in stop
    assert "`/sc:git` never runs as a worker" in stop
    assert "not inside a git work tree" in stop


def test_behavioral_flow_order_and_hand_off():
    flow = _section("Behavioral Flow")
    labels = re.findall(r"^\d+\. \*\*(.+?)\*\*", flow, flags=re.M)
    assert labels == ["Parse", "STOP", "Hand off", "Print"]


def test_exactly_one_skill_line_in_activation():
    text = _text()
    assert text.count("> Skill sc:git-protocol") == 1
    assert (
        sum(1 for ln in text.splitlines() if ln.strip() == "> Skill sc:git-protocol")
        == 1
    )
    activation = _section("Activation")
    assert "> Skill sc:git-protocol" in activation
    assert "~/.claude/skills/sc-git-protocol/SKILL.md" in activation
    assert ".claude/skills/sc-git-protocol/SKILL.md" in activation.replace(
        "~/.claude/skills/sc-git-protocol/SKILL.md", ""
    ), "the project copy is named as the fallback"


def test_boundaries_will_not_matches_fr005():
    will_not = _section("Boundaries").split("**Will Not:**", 1)[1].lower()
    for phrase in (
        "push",
        "fetch on its own",
        "`submodule update`",
        ".gitmodules",
        "pull",
        "merge",
        "rebase",
        "pull request",
        "delete any branch",
        "force",
        "stash",
        "rewrite history",
        ".claude/",
        "settings.json",
    ):
        assert phrase in will_not, phrase


def test_related_commands_route_push_and_cleanup():
    related = _section("Related Commands")
    assert "`/sc:pr-submit`" in related
    assert "`/sc:worktrees`" in related


def test_no_installed_primitive_path_into_src():
    assert "src/superclaude/" not in _text()


def test_interactive_option_and_merge_example_are_gone():
    text = _text()
    assert "--interactive" not in text
    assert "merge feature-branch" not in text
    assert "Interactive Operations" not in text


@pytest.mark.parametrize("flag", ["--no-verify", "--amend", "SKIP=", "commit-tree"])
def test_no_text_recommends_a_banned_token(flag):
    assert flag not in _text()
