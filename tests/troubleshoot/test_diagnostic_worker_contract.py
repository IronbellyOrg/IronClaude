"""Native diagnostic capability and parent-persistence contracts, not OS sandbox proof."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from superclaude.cli.install_agents import install_agents
from superclaude.cli.install_skills import install_all_skills

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "src/superclaude"
PROFILE = SOURCE / "agents/troubleshoot-analyst.md"
SKILL_DIR = SOURCE / "skills/sc-troubleshoot-protocol"
TOOLS = {
    "Read",
    "Grep",
    "Glob",
    "mcp__auggie__codebase-retrieval",
    "mcp__serena__find_symbol",
    "mcp__serena__find_referencing_symbols",
    "mcp__serena__get_symbols_overview",
    "mcp__serena__get_diagnostics_for_file",
}


def assert_profile(text: str) -> None:
    frontmatter = re.match(r"\A---\n(.*?)\n---(?:\n|$)", text, re.S)
    assert frontmatter, "profile frontmatter required"
    names = re.findall(r"^name:\s*(.*?)$", frontmatter[1], re.M)
    assert names == ["troubleshoot-analyst"]
    rosters = re.findall(r"^tools:[ \t]*(.*?)$", frontmatter[1], re.M)
    assert len(rosters) == 1, "exactly one explicit tools roster required"
    tools = [tool.strip() for tool in rosters[0].split(",") if tool.strip()]
    assert len(tools) == len(TOOLS) and set(tools) == TOOLS, (
        "closed read-only tools roster"
    )


def section(text: str, start: str, end: str) -> str:
    return text.split(start, 1)[1].split(end, 1)[0]


def assert_runtime_profiles(text: str) -> None:
    profiles = re.findall(r"\bsubagent_type\s*=\s*([a-z][a-z0-9-]*)", text)
    assert set(profiles) <= {
        "troubleshoot-analyst",
        "confidence-calibrator",
        "evidence-validator",
    }, "unrestricted runtime profile"


def review_fallbacks(text: str) -> list[str]:
    wave6 = section(text, "### Wave 6:", "## Tool Coordination Summary")
    plan = section(wave6, "   - **Plan route", "   - **MDTM route")
    mdtm = wave6.split("   - **MDTM route", 1)[1]
    return [
        next(
            line
            for line in plan.splitlines()
            if "`reflect_status: skipped|failed`" in line
        ),
        next(line for line in plan.splitlines() if "**Phase D" in line),
        next(line for line in mdtm.splitlines() if "**Phase D" in line),
    ]


def assert_dispatches(text: str) -> None:
    assert_runtime_profiles(text)
    contracts = [
        ("### Wave 1.5:", "### Wave 1.6:", "Spawn three discovery branches"),
        ("### Wave 1.6:", "### Wave 1.7:", "Spawn 2 audit branches"),
        ("### Wave 1.7:", "### Wave 2:", "Form one hypothesis"),
        ("### Wave 3:", "### Wave 4:", "Spawn hypothesis agents"),
        ("### Wave 4:", "### Wave 4.5:", "Sanity-check the merge"),
    ]
    for start, end, marker in contracts:
        block = section(text, start, end)
        dispatch = next(line for line in block.splitlines() if marker in line)
        assert "subagent_type=troubleshoot-analyst" in dispatch, marker
    fallback_lines = review_fallbacks(text)
    assert all("subagent_type=troubleshoot-analyst" in line for line in fallback_lines)
    assert all("lens_name=self-review" in line for line in fallback_lines)
    assert "spawn the `confidence-calibrator` agent" in text
    assert "spawn the `evidence-validator` agent" in text


def assert_persistence(text: str) -> None:
    receipts = [
        (
            "### Wave 1.5:",
            "### Wave 1.6:",
            "writes each returned result",
            "before reading each output file",
        ),
        (
            "### Wave 1.6:",
            "### Wave 1.7:",
            "writes each returned result",
            "before reading those outputs",
        ),
        (
            "### Wave 1.7:",
            "### Wave 2:",
            "writes the returned card",
            "before step 1.5 or calibration",
        ),
        (
            "### Wave 3:",
            "### Wave 4:",
            "writes each returned card",
            "before reading each card",
        ),
        (
            "### Wave 4:",
            "### Wave 4.5:",
            "writes the returned review",
            "before reading it",
        ),
    ]
    for start, end, write, consume in receipts:
        block = section(text, start, end)
        assert write in block and consume in block, start
    wave6 = section(text, "### Wave 6:", "## Tool Coordination Summary")
    assert "persists the returned review" in wave6
    assert wave6.count("persists its returned review before consuming it") == 2
    contract = section(text, "## Native diagnostic delegation", "## Required Input")
    assert "The worker returns complete data" in contract
    assert "never host-shell heredoc assembly" in contract
    assert "retain the measurement as pending; never execute unrestricted" in contract


def test_profile_has_closed_native_tools() -> None:
    assert_profile(PROFILE.read_text())


@pytest.mark.parametrize(
    "mutation",
    [
        "missing",
        "empty",
        "duplicate",
        "Bash",
        "Write",
        "Edit",
        "Task",
        "Agent",
        "Skill",
        "mcp__*",
        "mcp__serena__replace_content",
    ],
)
def test_profile_guard_rejects_capability_mutants(mutation: str) -> None:
    text = PROFILE.read_text()
    if mutation == "missing":
        text = re.sub(r"^tools:.*\n", "", text, flags=re.M)
    elif mutation == "empty":
        text = re.sub(r"^tools:.*$", "tools:", text, flags=re.M)
    elif mutation == "duplicate":
        text = text.replace("tools: Read", "tools: Read, Read", 1)
    else:
        text = text.replace("tools: Read", f"tools: {mutation}, Read", 1)
    with pytest.raises(AssertionError):
        assert_profile(text)


def test_native_dispatches_and_persistence() -> None:
    text = (SKILL_DIR / "SKILL.md").read_text()
    assert_dispatches(text)
    assert_persistence(text)
    assert ".claude/agents/troubleshoot-analyst.md" in text
    assert "~/.claude/agents/troubleshoot-analyst.md" in text
    assert "No unrestricted fallback" in text
    assert "shadowing invalid project definition" in text


@pytest.mark.parametrize(
    "start,end,marker",
    [
        ("### Wave 1.5:", "### Wave 1.6:", "Spawn three discovery branches"),
        ("### Wave 1.6:", "### Wave 1.7:", "Spawn 2 audit branches"),
        ("### Wave 1.7:", "### Wave 2:", "Form one hypothesis"),
        ("### Wave 3:", "### Wave 4:", "Spawn hypothesis agents"),
        ("### Wave 4:", "### Wave 4.5:", "Sanity-check the merge"),
    ],
)
def test_dispatch_guard_kills_unrestricted_mutants(
    start: str, end: str, marker: str
) -> None:
    text = (SKILL_DIR / "SKILL.md").read_text()
    block = section(text, start, end)
    line = next(line for line in block.splitlines() if marker in line)
    mutant = text.replace(
        line,
        line.replace(
            "subagent_type=troubleshoot-analyst", "subagent_type=quality-engineer"
        ),
        1,
    )
    with pytest.raises(AssertionError):
        assert_dispatches(mutant)


@pytest.mark.parametrize(
    "start,end,write",
    [
        ("### Wave 1.5:", "### Wave 1.6:", "writes each returned result"),
        ("### Wave 1.6:", "### Wave 1.7:", "writes each returned result"),
        ("### Wave 1.7:", "### Wave 2:", "writes the returned card"),
        ("### Wave 3:", "### Wave 4:", "writes each returned card"),
        ("### Wave 4:", "### Wave 4.5:", "writes the returned review"),
    ],
)
def test_persistence_guard_kills_lost_receipt(start: str, end: str, write: str) -> None:
    text = (SKILL_DIR / "SKILL.md").read_text()
    block = section(text, start, end)
    mutant = text.replace(block, block.replace(write, "receives data only", 1), 1)
    with pytest.raises(AssertionError):
        assert_persistence(mutant)


@pytest.mark.parametrize("index", [0, 1, 2])
def test_review_fallback_guard_kills_unrestricted_mutants(index: int) -> None:
    text = (SKILL_DIR / "SKILL.md").read_text()
    line = review_fallbacks(text)[index]
    mutant = text.replace(
        line,
        line.replace("subagent_type=troubleshoot-analyst", "subagent_type=self-review"),
        1,
    )
    with pytest.raises(AssertionError):
        assert_dispatches(mutant)


REF_RECEIPTS = {
    "doc-discovery.md": "the parent owns the `output_path` and writes it",
    "diagnosability-audit.md": "the parent owns `output_path` and writes the file before any consumer reads it",
    "triage-checklist.md": "the parent owns `output_path` and persists the card before calibration",
}


def assert_reference_contract(name: str, text: str) -> None:
    assert_runtime_profiles(text)
    assert "subagent_type=troubleshoot-analyst" in text
    if name == "remediation-handoff.md":
        lines = [line for line in text.splitlines() if "subagent_type=" in line]
        assert len(lines) == 2
        for line in lines:
            assert "subagent_type=troubleshoot-analyst" in line
            assert "lens_name=self-review" in line
            assert "persists" in line and "parent" in line
    else:
        assert REF_RECEIPTS[name] in text


@pytest.mark.parametrize("name", [*REF_RECEIPTS, "remediation-handoff.md"])
def test_reference_dispatch_and_receipt_contracts(name: str) -> None:
    assert_reference_contract(name, (SKILL_DIR / "refs" / name).read_text())


@pytest.mark.parametrize("name", [*REF_RECEIPTS, "remediation-handoff.md"])
def test_reference_guard_kills_unrestricted_mutant(name: str) -> None:
    text = (SKILL_DIR / "refs" / name).read_text()
    with pytest.raises(AssertionError):
        assert_reference_contract(
            name,
            text.replace(
                "subagent_type=troubleshoot-analyst",
                "subagent_type=quality-engineer",
                1,
            ),
        )


@pytest.mark.parametrize("name", list(REF_RECEIPTS))
def test_reference_guard_kills_lost_persistence(name: str) -> None:
    text = (SKILL_DIR / "refs" / name).read_text()
    with pytest.raises(AssertionError):
        assert_reference_contract(
            name, text.replace(REF_RECEIPTS[name], "worker receives data only", 1)
        )


@pytest.mark.parametrize("index", [0, 1])
def test_handoff_guard_checks_each_native_fallback(index: int) -> None:
    name = "remediation-handoff.md"
    text = (SKILL_DIR / "refs" / name).read_text()
    line = [line for line in text.splitlines() if "subagent_type=" in line][index]
    with pytest.raises(AssertionError):
        assert_reference_contract(
            name, text.replace(line, line.replace("persists", "receives"), 1)
        )


def test_entire_skill_tree_rejects_unapproved_explicit_profiles() -> None:
    for path in [SKILL_DIR / "SKILL.md", *sorted((SKILL_DIR / "refs").rglob("*.md"))]:
        assert_runtime_profiles(path.read_text())


@pytest.mark.parametrize(
    "profile",
    ["quality-engineer", "root-cause-analyst", "self-review", "general-purpose"],
)
def test_tree_guard_kills_stray_unrestricted_dispatch(profile: str) -> None:
    text = (
        SKILL_DIR / "SKILL.md"
    ).read_text() + f"\nSpawn extra Task with subagent_type={profile}\n"
    with pytest.raises(AssertionError):
        assert_runtime_profiles(text)


def test_document_currency_is_finalized_after_discovery() -> None:
    reference = (SKILL_DIR / "refs/doc-discovery.md").read_text()
    assert "worker returns preliminary `currency_verdict: unknown`" in reference
    assert "existing `reason` field" in reference
    assert "After receipt, the parent persists that preliminary result" in reference
    assert "writes the finalized Branch B result before" in reference
    skill = section(
        (SKILL_DIR / "SKILL.md").read_text(), "### Wave 1.5:", "### Wave 1.6:"
    )
    assert "currency mtimes are collected by the parent after discovery" in skill
    assert "writes the finalized Branch B result before step 4 synthesis" in skill


def assert_review_mapping(text: str) -> None:
    mapping = section(text, "- **Review outcome mapping:**", "- **Models and lenses:**")
    for rule in (
        "PASS maps to existing `OK` and FAIL to a documented blocker",
        "PASS maps to `OK`, FAIL with nonblocking revision findings to `Recommends refactor`",
        "FAIL with a blocker to `Blocker`",
        "do not convert a FAIL into PASS",
    ):
        assert rule in mapping


def test_review_binary_verdict_preserves_consumer_outcomes() -> None:
    text = (SKILL_DIR / "SKILL.md").read_text()
    assert_review_mapping(text)
    agent = PROFILE.read_text()
    assert "plus the existing consumer outcome requested in the brief" in agent
    assert "Template evidence kinds such as `executed_reproducer`" in agent
    assert "never permission for worker execution" in agent
    with pytest.raises(AssertionError):
        assert_review_mapping(text.replace("Recommends refactor", "OK"))


def test_specialist_lenses_and_runtime_limits_are_preserved() -> None:
    text = (SKILL_DIR / "SKILL.md").read_text()
    selection = section(text, "**Lens selection**", "**Steps**:")
    for name in (
        "root-cause-analyst",
        "quality-engineer",
        "performance-engineer",
        "security-engineer",
        "devops-architect",
        "refactoring-expert",
        "system-architect",
    ):
        assert f"`{name}`" in selection
    assert "pick 2-4 specialist lenses" in selection
    assert "`--models` overrides" in text
    agent = PROFILE.read_text()
    assert "The parent persists the returned result" in agent
    assert "Do not return only a path to a file you did not create" in agent
    assert "It is not an OS sandbox" in agent
    assert "return its source as data" in agent
    assert "retain pending measurements" in agent


def test_installation_preserves_profile_and_protocol(tmp_path: Path) -> None:
    agents = tmp_path / "agents"
    skills = tmp_path / "skills"
    ok, message = install_agents(target_path=agents)
    assert ok, message
    installed = agents / "troubleshoot-analyst.md"
    assert installed.read_bytes() == PROFILE.read_bytes()
    assert_profile(installed.read_text())
    ok, message = install_all_skills(target_path=skills)
    assert ok, message
    for name in (
        "SKILL.md",
        "refs/doc-discovery.md",
        "refs/diagnosability-audit.md",
        "refs/triage-checklist.md",
        "refs/remediation-handoff.md",
    ):
        assert (skills / "sc-troubleshoot-protocol" / name).read_bytes() == (
            SKILL_DIR / name
        ).read_bytes()
