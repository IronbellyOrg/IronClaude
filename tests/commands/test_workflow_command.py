"""Guards for /sc:workflow v3: thin command + skill refs (SPEC §8).

Managed-package policy (schema 1.2, to-do root, retired --output, naming) lives
in the refs; these are STATIC protocol guards. Executable archive behavior is in
tests/skills/test_workflow_archive.py.
"""

import filecmp
import re
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
_CMD = _REPO / "src" / "superclaude" / "commands" / "workflow.md"
_SKILL = _REPO / "src" / "superclaude" / "skills" / "sc-workflow-protocol"
_TPL00 = (
    _REPO
    / "src"
    / "superclaude"
    / "templates"
    / "workflow"
    / "00_mdtm_template_simple_task.md"
)
_REFS = (
    "input-parse.md",
    "phase-templates.md",
    "overlap-routing.md",
    "quality-gates.md",
    "return-contract.md",
)


def _workflow_texts():
    yield "command", _CMD.read_text(encoding="utf-8")
    yield "skill", (_SKILL / "SKILL.md").read_text(encoding="utf-8")
    for name in _REFS:
        yield name, (_SKILL / "refs" / name).read_text(encoding="utf-8")


def _ref(name):
    return (_SKILL / "refs" / name).read_text(encoding="utf-8")


def test_activation_handoff():
    text = _CMD.read_text(encoding="utf-8")
    assert "## Activation" in text
    assert "Skill sc:workflow-protocol" in text


def test_command_has_no_execute_step():
    text = _CMD.read_text(encoding="utf-8")
    assert "**Execute**" not in text
    assert "Analyze→Plan" not in text


def test_skill_and_five_refs_exist():
    assert (_SKILL / "SKILL.md").is_file()
    for name in _REFS:
        assert (_SKILL / "refs" / name).is_file(), name


def test_mcp_servers_empty():
    text = _CMD.read_text(encoding="utf-8")
    assert "mcp-servers: []" in text
    assert "morphllm" not in text


def test_plan_uses_template_00():
    skill = (_SKILL / "SKILL.md").read_text(encoding="utf-8")
    gates = _ref("quality-gates.md")
    assert "00_mdtm_template_simple_task.md" in skill
    assert "03_project_plan_template" not in skill + gates
    for key in ("schema: workflow-plan/1.2", "version:", "priority:", "created_date:"):
        assert key in gates, key
    assert "workflow-plan/1.1" not in gates


def test_plugin_mirror_matches_src():
    plugin = _REPO / "plugins" / "superclaude" / "skills" / "sc-workflow-protocol"
    src_rels = {str(p.relative_to(_SKILL)) for p in _SKILL.rglob("*.md")}
    plugin_rels = {str(p.relative_to(plugin)) for p in plugin.rglob("*.md")}
    assert src_rels == plugin_rels, src_rels ^ plugin_rels
    _, mismatch, errors = filecmp.cmpfiles(
        _SKILL, plugin, sorted(src_rels), shallow=False
    )
    assert not mismatch and not errors, mismatch + errors
    plugin_cmd = _REPO / "plugins" / "superclaude" / "commands" / "workflow.md"
    assert filecmp.cmp(_CMD, plugin_cmd, shallow=False)


# --- managed package policy (design R1-R2) ---------------------------------------
def test_all_creation_paths_target_to_do_not_workflow_root():
    for name, text in _workflow_texts():
        assert ".dev/workflow/" not in text, name
    for name in ("input-parse.md", "return-contract.md", "overlap-routing.md"):
        assert ".dev/tasks/to-do/" in _ref(name), name
    assert ".dev/tasks/to-do/" in _CMD.read_text(encoding="utf-8")


def test_output_flag_is_retired_everywhere():
    assert "--output" not in re.search(
        r"^argument-hint:.*$", _CMD.read_text(encoding="utf-8"), re.M
    ).group(0)
    skill = (_SKILL / "SKILL.md").read_text(encoding="utf-8")
    assert "--output" not in re.search(r"^argument-hint:.*$", skill, re.M).group(0)
    for name, text in _workflow_texts():
        for line in text.splitlines():
            if "--output" in line:
                assert re.search(r"retired|E-LEGACY|Never", line), (name, line)
    parse = _ref("input-parse.md")
    assert re.search(r"`E-LEGACY`\s*\|[^|]*`--output`", parse)
    assert "E-OUTPUT-PATH" not in parse and "E-MISSING-DIR" not in parse
    # validation precedes any write
    assert "Validate every input and flag **before any write**" in parse


def test_naming_and_collision_policy_is_specified():
    parse = _ref("input-parse.md")
    for token in (
        "TASK-WF-<subject>-<YYYYMMDD>-<HHMMSS>",
        "UTC",
        "lower camelCase",
        "**max 16**",
        "truncate to **16**",
        "`plan`",
        "full directory basename + `.md`",
        "Never `plan.md`",
        "`.dev/tasks/to-do/<id>` **or** `.dev/tasks/done/<id>`",
        "`test -L`",
        "dangling symlinks",
        "`-2`",
        "`-9`",
        "never `mkdir -p`",
        "E-PACKAGE-COLLISION",
        "Regeneration never reuses",
    ):
        assert token in parse, token


def test_early_stop_creates_no_package_and_failures_are_separated():
    parse, contract = _ref("input-parse.md"), _ref("return-contract.md")
    assert re.search(r"`E-LEGACY`[^\n]*\| none \|", parse)
    assert re.search(r"`E-NO-SOURCE`[^\n]*\| none \|", parse)
    assert "no package directory, no yaml" in contract
    assert re.search(r"\| `failed` \| `null`", contract)
    assert re.search(
        r"failed.*`partial`.*stays valid and executable", contract.replace("\n", " ")
    )
    assert "never mark a valid gated plan `failed`" in contract


def test_contract_and_plan_use_stable_portable_identity():
    contract, gates = _ref("return-contract.md"), _ref("quality-gates.md")
    for token in (
        'contract_version: "1.1"',
        "slug: <id>",
        "plan_path: ./<id>.md",
        "source_path: ./source.md",
    ):
        assert token in contract, token
    for token in ("schema: workflow-plan/1.2", "source: ./source.md", "slug: <id>"):
        assert token in gates, token
    assert "never the original absolute path" in gates
    assert "plan_path: .dev/" not in contract


def test_template_00_authoring_contract():
    text = _TPL00.read_text(encoding="utf-8")
    comment = re.search(r"<!--(.*?)-->", text, re.S).group(1)
    assert "./artifacts/" in comment and "repo-relative" in comment
    assert "executor-owned" in comment
    body = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    assert not re.search(r"^\s*([-*] \[[ xX]\]|\d+[.)] )", body, re.M)
    assert not re.search(r"^status:", text, re.M)
    assert re.findall(r"^## Task \d+:", body, re.M)
    assert not re.search(r"^## Task \d+:.*\b(verify|verification)\b", body, re.M | re.I)
    for key in ("version:", "priority:", "created_date:"):
        assert re.search(rf"^{key}", text, re.M), key


def test_plugin_ships_managed_implement_protocol_and_helper():
    root = _CMD.parents[3]
    canonical = root / "src/superclaude/skills/sc-implement-protocol"
    plugin = root / "plugins/superclaude/skills/sc-implement-protocol"
    expected = {
        path.relative_to(canonical)
        for path in canonical.rglob("*")
        if path.suffix in (".md", ".py")
    }
    actual = {
        path.relative_to(plugin)
        for path in plugin.rglob("*")
        if path.suffix in (".md", ".py")
    }
    assert expected == actual
    for path in expected:
        assert (plugin / path).read_bytes() == (canonical / path).read_bytes()


def test_digit_prefix_precedes_final_subject_truncation():
    parse = _ref("input-parse.md")
    assert "Before concatenation or truncation" in parse
    assert "`1234567890123456` → `plan123456789012`" in parse


def test_final_reflect_pre_precedes_contract_and_handoff():
    skill = (_SKILL / "SKILL.md").read_text(encoding="utf-8")
    assert skill.index("## Wave 3 — Gate") < skill.index("## Wave 4 — Reflect")
    assert skill.index("## Wave 4 — Reflect") < skill.index("## Wave 5 — Contract")
    assert (
        "/sc:reflect --mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md"
        in skill
    )
    contract = _ref("return-contract.md")
    assert "reflect_status:" in contract and "reflect_report_path:" in contract
    assert "/sc:reflect --mode pre" in _CMD.read_text(encoding="utf-8")
