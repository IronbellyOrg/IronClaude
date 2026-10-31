"""Drift guards for /sc:impact and sc:impact-protocol (issue #323, Phase 3).

`/sc:impact` lists the dependents of symbols from the code graph and never stops its
caller. These tests pin the command frontmatter and activation, the skill's exact
allowlist (per-verb CLI patterns, never a wildcard), the absence of build or write
verbs and of explore, the outline-only file mode, the guide and runtime-surface
lookups, every contract field and failure row, the closed token list, the impact.md
layout, the call-site budget, the advisory rule and the status-only CLI transport.
CI-safe: pure file-content assertions.
"""

import re
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[2]
_COMMAND = _REPO / "src" / "superclaude" / "commands" / "impact.md"
_SKILL = _REPO / "src" / "superclaude" / "skills" / "sc-impact-protocol" / "SKILL.md"

_SKILL_TOOLS = {
    "Read",
    "Grep",
    "Glob",
    "Write",
    "Bash(printenv SUPERCLAUDE_CODEGRAPH_PRIMITIVES)",
    "Bash(pgrep -f *)",
    "Bash(git rev-parse *)",
    "Bash(realpath *)",
    "Bash(git diff *)",
    "Bash(codegraph --version)",
    "Bash(codegraph status)",
    "Bash(codegraph query *)",
    "Bash(codegraph node *)",
    "Bash(codegraph callers *)",
    "Bash(codegraph impact *)",
    "Bash(codegraph affected *)",
    "mcp__codegraph__codegraph_status",
    "mcp__codegraph__codegraph_search",
    "mcp__codegraph__codegraph_node",
    "mcp__codegraph__codegraph_callers",
    "mcp__codegraph__codegraph_impact",
}
_TOKENS = {
    "graph:absent",
    "graph:unlisted",
    "graph:disabled",
    "graph:not_initialized",
    "graph:foreign_index",
    "graph:stale",
    "graph:version_mismatch",
    "graph:provenance_unproven",
    "graph:empty",
    "graph:ambiguous",
    "graph:truncated",
    "graph:parse_failed",
    "graph:unresolved",
    "graph:telemetry_on",
}
_MUTATING = re.compile(
    r"codegraph (?:init|index|sync|uninit|unlock|upgrade|install|uninstall|telemetry (?:on|off))"
)
_CONTRACT_FIELDS = [
    "schema_version",
    "command",
    "status",
    "caller",
    "output_dir",
    "report_path",
    "contract_path",
    "input.mode",
    "input.symbols",
    "input.diff_base",
    "input.changed_files",
    "input.depth",
    "input.limit",
    "input.tests",
    "input.test_depth",
    "readiness",
    "advisory",
    "degraded",
    "symbols[]",
    "ambiguous[]",
    "unmapped_files[]",
    "dependents[]",
    "dependents_omitted",
    "call_sites",
    "tests[]",
    "selection_source",
    "errors[]",
]
_FAILURES = [
    ("codegraph absent", "graph:absent"),
    ("lookup tools unlisted", "graph:unlisted"),
    ("switched off", "graph:disabled"),
    ("not initialized", "graph:not_initialized"),
    ("foreign index", "graph:foreign_index"),
    ("stale", "graph:stale"),
    ("version mismatch", "graph:version_mismatch"),
    ("truncated", "graph:truncated"),
    ("parse failure", "graph:parse_failed"),
    ("ambiguous name", "graph:ambiguous"),
    ("empty result", "graph:empty"),
    ("budget-limited rows", "graph:unresolved"),
    ("bad flags", "blocked"),
    ("output dir unwritable", "failed"),
]
_HEADINGS = [
    "## Summary",
    "## How to read this",
    "## Readiness",
    "## Input",
    "## Definitions",
    "## Production dependents",
    "## Test dependents",
    "## Unclassified dependents",
    "## Tests (advisory)",
    "## Unmapped files",
    "## Limits",
    "## Degraded and fallbacks",
]


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


def test_impact_command_frontmatter():
    fm = _frontmatter(_COMMAND)
    assert fm["name"] == "impact"
    assert "codegraph" in fm["mcp-servers"]
    for flag in (
        "--diff",
        "--depth",
        "--limit",
        "--tests",
        "--test-depth",
        "--output-dir",
        "--caller",
    ):
        assert flag in fm["argument-hint"], flag


def test_impact_command_invokes_protocol_skill():
    assert "> Skill sc:impact-protocol" in _section(_text(_COMMAND), "## Activation")


def test_impact_skill_name():
    assert _frontmatter(_SKILL)["name"] == "sc:impact-protocol"


def test_impact_allowed_tools_exact():
    assert _allowed(_SKILL) == _SKILL_TOOLS


def test_impact_no_wildcards():
    for path in (_COMMAND, _SKILL):
        text = _text(path)
        for banned in ("Bash(codegraph *)", "mcp__codegraph__*", "Bash(codegraph)"):
            assert banned not in text, f"{path.name} names {banned}"


def test_impact_no_mutating_verbs():
    for path in (_COMMAND, _SKILL):
        assert not _MUTATING.findall(_text(path)), path.name


def test_impact_no_explore():
    for path in (_COMMAND, _SKILL):
        text = _text(path)
        for banned in ("codegraph_explore", "codegraph explore", "codegraph context"):
            assert banned not in text, f"{path.name} names {banned}"


def test_impact_node_file_mode_has_symbols_only():
    for line in _text(_SKILL).splitlines():
        if "codegraph_node" in line and '"file"' in line:
            assert '"symbolsOnly": true' in line, line


@pytest.mark.parametrize("path", [_COMMAND, _SKILL], ids=lambda p: p.name)
def test_impact_guide_lookup_line(path):
    text = _text(path)
    assert "~/.claude/CODEGRAPH.md" in text
    for match in re.finditer(r"src/superclaude/[^\s`)]*", text):
        assert match.group(0) == "src/superclaude/core/CODEGRAPH.md", match.group(0)


def test_impact_runtime_surface_dual_surface():
    text = _text(_SKILL)
    installed = text.index(
        "~/.claude/skills/sc-reflect-protocol/refs/runtime-surface.md"
    )
    project = text.index("`.claude/skills/sc-reflect-protocol/refs/runtime-surface.md`")
    assert installed < project


@pytest.mark.parametrize("field", _CONTRACT_FIELDS)
def test_impact_contract_fields_documented(field):
    contract = _section(_text(_SKILL), "## 5. `return-contract.yaml`")
    assert field in contract, field


def test_impact_status_enum():
    contract = _section(_text(_SKILL), "## 5. `return-contract.yaml`")
    for value in ("success", "partial", "blocked", "failed"):
        assert f"`{value}`" in contract
    assert "failed > blocked > partial > success" in contract


def test_impact_tokens_closed_vocabulary():
    found = set(re.findall(r"graph:[a-z_]+", _text(_SKILL)))
    assert found <= _TOKENS, found - _TOKENS


@pytest.mark.parametrize("condition,token", _FAILURES)
def test_impact_failure_table_rows(condition, token):
    table = _section(_text(_SKILL), "## 7. Failure behaviour")
    row = next((ln for ln in table.splitlines() if ln.startswith(f"| {condition}")), "")
    assert row, f"no failure row for {condition}"
    assert token in row


def test_impact_md_sections_in_order():
    layout = _section(_text(_SKILL), "## 6. `impact.md` layout")
    positions = [layout.index(f"`{h}`") for h in _HEADINGS]
    assert positions == sorted(positions)


def test_impact_call_site_budget():
    text = _text(_SKILL)
    assert "5 per symbol" in text and "20 per run" in text
    for value in ("call-site-verified", "def-line", "unresolved"):
        assert value in text


def test_impact_advisory_rule():
    advisory = _section(_text(_SKILL), "## 3. Advisory rule")
    assert "`advisory`" in advisory
    assert "no consumer may change a severity, gate or verdict" in advisory


def test_impact_status_only_cli_transport_before_grep_fallback():
    steps = _section(_text(_SKILL), "## 2. Step sequence")
    cli = steps.index("Status-only branch transport")
    grep = steps.index("| 9 | Grep fallback")
    assert cli < grep
    for form in (
        "codegraph query",
        "codegraph node",
        "codegraph callers",
        "codegraph impact",
    ):
        assert form in steps[cli:grep], form


def test_impact_example_uses_placeholders_only():
    text = _text(_SKILL)
    assert "install_codebase_memory_mcp" not in text


_SKILLS = _REPO / "src" / "superclaude" / "skills"

# (caller file, its --caller value): every caller that invokes sc:impact-protocol.
_IMPACT_CALLERS = [
    ("sc-reflect-protocol/SKILL.md", "sc-reflect-protocol"),
    ("sc-implement-protocol/SKILL.md", "sc-implement-protocol"),
    ("sc-pr-submit-protocol/SKILL.md", "sc-pr-submit-protocol"),
    ("sc-pr-submit-protocol/refs/troubleshoot-dispatch.md", "sc-pr-submit-protocol"),
    ("sc-troubleshoot-protocol/SKILL.md", "sc-troubleshoot-protocol"),
    ("sc-auggie-review-protocol/SKILL.md", "sc-auggie-review-protocol"),
    ("sc-task-protocol/SKILL.md", "sc-task-protocol"),
]


@pytest.mark.parametrize(("rel", "caller"), _IMPACT_CALLERS)
def test_impact_callers_wired(rel, caller):
    text = _text(_SKILLS / rel)
    assert "Skill sc:impact-protocol" in text, rel
    assert f"--caller {caller}" in text, rel
    # Every caller treats a blocked or failed run like graph:absent.
    assert "`status: blocked|failed` counts as `graph:absent`" in text, rel


def test_impact_troubleshoot_wave1_does_not_call_impact():
    text = _text(_SKILLS / "sc-troubleshoot-protocol" / "SKILL.md")
    wave1 = text.split("### Wave 1: Tier 1", 1)[1].split("\n### Wave 6:", 1)[0]
    assert "sc:impact-protocol" not in wave1
    wave6 = text.split("\n### Wave 6:", 1)[1].split("\n## ", 1)[0]
    assert "Skill sc:impact-protocol" in wave6


@pytest.mark.parametrize(
    "rel",
    [
        "sc-task-protocol/SKILL.md",
        "sc-pr-submit-protocol/SKILL.md",
        "sc-troubleshoot-protocol/SKILL.md",
        "sc-auggie-review-protocol/SKILL.md",
        "sc-implement-protocol/SKILL.md",
        "sc-reflect-protocol/SKILL.md",
    ],
)
def test_impact_callers_may_invoke_skill(rel):
    fm = _frontmatter(_SKILLS / rel)
    tools = {t.strip() for t in fm.get("allowed-tools", "").split(",")}
    if fm.get("allowed-tools"):
        assert "Skill" in tools, rel
