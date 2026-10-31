"""Drift guards for /sc:graph and sc:graph-protocol (issue #323, Phase 3).

`/sc:graph` reports codegraph index readiness and is the only primitive that runs
`codegraph init`, and only when the user types it. These tests pin the exact
allowlists, the single init exception in the command body, the user-typed guard,
the nested-worktree and running-init refusals, the closed enums and contract fields
of the protocol skill, the primitive switch name, the guide lookup line, and that
no other skill calls the protocol. CI-safe: pure file-content assertions.
"""

import re
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[2]
_COMMAND = _REPO / "src" / "superclaude" / "commands" / "graph.md"
_SKILL = _REPO / "src" / "superclaude" / "skills" / "sc-graph-protocol" / "SKILL.md"
_SKILLS_DIR = _REPO / "src" / "superclaude" / "skills"

_MUTATING = re.compile(
    r"codegraph (?:init|index|sync|uninit|unlock|upgrade|install|uninstall|telemetry (?:on|off))"
)
_SKILL_TOOLS = {
    "Read",
    "Write",
    "Edit",
    "Bash(codegraph --version)",
    "Bash(codegraph status)",
    "Bash(codegraph telemetry status)",
    "Bash(git rev-parse --show-toplevel)",
    "Bash(realpath *)",
    "Bash(pgrep -f *)",
    "Bash(printenv SUPERCLAUDE_CODEGRAPH_PRIMITIVES)",
    "mcp__codegraph__codegraph_status",
}
_INDEX_STATES = ["fresh", "stale", "not_initialized", "foreign_index", "absent", "disabled", "error"]
_RELATIONS = ["own", "parent", "none", "unknown"]
_NEXT_ACTIONS = [
    "none",
    "run_graph_init",
    "run_graph_init_worktree_local",
    "install_codegraph",
    "enable_codegraph",
    "status_only_branch",
    "align_version",
    "wait_for_sync",
    "check_codegraph_error",
]
_CONTRACT_FIELDS = [
    "schema_version", "command", "subcommand", "status", "contract_path", "output_dir",
    "checked_at", "access", "index_state", "worktree_root", "worktree_relation", "cli_version",
    "pin", "pin_match", "mcp_tools_listed", "counts", "pending", "telemetry",
    "telemetry_opt_out", "kill_switch", "next_action", "degraded", "init.requested",
    "init.form", "init.ran", "init.exit_code", "init.refused_reason",
]
_GUIDE_LINE = (
    "Codegraph usage rules: read `~/.claude/CODEGRAPH.md` (in a dev checkout without an install, "
    "the labelled fallback is `src/superclaude/core/CODEGRAPH.md`)."
)


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _frontmatter(path: Path) -> dict:
    block = _text(path).split("---", 2)[1]
    return {
        k.strip(): v.strip()
        for k, _, v in (ln.partition(":") for ln in block.splitlines() if ":" in ln)
    }


def _allowed(path: Path) -> set:
    return {t.strip() for t in _frontmatter(path)["allowed-tools"].split(", ")}


def _section(text: str, heading: str) -> str:
    return text.split(heading, 1)[1].split("\n## ", 1)[0]


def test_graph_command_frontmatter():
    fm = _frontmatter(_COMMAND)
    assert fm["name"] == "graph"
    assert "codegraph" in fm["mcp-servers"]
    for token in ("status", "init", "--worktree-local", "--output-dir"):
        assert token in fm["argument-hint"]
    assert "--caller" not in fm["argument-hint"]


def test_graph_command_invokes_protocol_skill():
    assert "> Skill sc:graph-protocol" in _text(_COMMAND)


def test_graph_command_allowed_tools_exact():
    assert _allowed(_COMMAND) == {"Skill", "Bash(codegraph init --yes *)", "Bash(codegraph init -i)"}


def test_graph_skill_allowed_tools_exact():
    tools = _allowed(_SKILL)
    assert tools == _SKILL_TOOLS
    assert not [t for t in tools if "init" in t]


def test_graph_init_only_in_command():
    assert not _MUTATING.findall(_text(_SKILL)), "the skill must never name a build or write verb"
    hits = _MUTATING.findall(_text(_COMMAND))
    assert hits and all(h == "codegraph init" for h in hits)


def test_graph_init_user_typed_guard():
    init = _section(_text(_COMMAND), "## Init (user-typed only)")
    assert "/sc:graph init" in init
    assert "user's own message starts with `/sc:graph init`" in init


def test_graph_nested_worktree_refusal():
    text = _text(_SKILL)
    for token in ("nested_worktree", "--worktree-local", "worktree_local_not_nested"):
        assert token in text


def test_graph_init_preflight_refuses_running_init():
    preflight = _section(_text(_SKILL), "## `init`")
    assert "pgrep -f 'codegraph\\.js (init|index)'" in preflight
    assert "init_running" in preflight


def test_graph_no_sync_or_explore():
    for path in (_COMMAND, _SKILL):
        text = _text(path)
        for banned in ("codegraph sync", "codegraph_explore", "Bash(codegraph *)"):
            assert banned not in text, f"{path.name} names {banned}"


def test_graph_index_state_enum():
    text = _text(_SKILL)
    for value in _INDEX_STATES + _RELATIONS:
        assert f"`{value}`" in text, value


@pytest.mark.parametrize("action", _NEXT_ACTIONS)
def test_graph_next_action_enum(action):
    assert f"`{action}`" in _text(_SKILL)


@pytest.mark.parametrize("field", _CONTRACT_FIELDS)
def test_graph_contract_fields_documented(field):
    contract = _section(_text(_SKILL), "## `return-contract.yaml`")
    assert f"`{field}`" in contract or f"`{field}`," in contract or field in contract


def test_graph_telemetry_opt_out_and_switch():
    text = _text(_SKILL)
    assert "CODEGRAPH_TELEMETRY=0" in text and "DO_NOT_TRACK=1" in text
    assert "SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off" in text
    for path in (_COMMAND, _SKILL):
        assert "IRONCLAUDE_CODEGRAPH" not in _text(path)


@pytest.mark.parametrize("path", [_COMMAND, _SKILL], ids=lambda p: p.name)
def test_graph_guide_lookup_line(path):
    text = _text(path)
    assert _GUIDE_LINE in text
    for match in re.finditer(r"src/superclaude/[^\s`)]*", text):
        assert match.group(0) == "src/superclaude/core/CODEGRAPH.md", match.group(0)


def test_graph_no_skill_callers():
    callers = [
        p for p in _SKILLS_DIR.glob("*/SKILL.md")
        if p.parent.name != "sc-graph-protocol" and "sc:graph-protocol" in _text(p)
    ]
    assert not callers, f"skills must not call sc:graph-protocol: {callers}"
