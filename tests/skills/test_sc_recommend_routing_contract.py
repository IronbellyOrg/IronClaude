"""Regression tests for the routing contract in the sc-recommend SKILL.md.

Spec 3.2 asks /sc:recommend to read the routing guide first, let the guide's
levels override native-first answers, emit ordered workflows with every
mandatory flag, allow the two Claude Code built-ins, fall back cleanly when the
guide is missing, and keep the uv cache step optional. These tests pin the
SKILL.md text that carries each requirement, so a later edit cannot drop one
silently.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

from superclaude.cli.recommend.prompts import (
    CLASSIFICATION_KEYS,
    CLASSIFIER_PROMPT,
    COLD_PATH_RUNBOOK,
)

_REPO = Path(__file__).resolve().parents[2]
_SKILL = _REPO / "src/superclaude/skills/sc-recommend/SKILL.md"
_HELP = _REPO / "src/superclaude/commands/help.md"
_COMMAND = _REPO / "src/superclaude/commands/recommend.md"
_HOOK = _REPO / "src/superclaude/hooks/scripts/sc-recommend-phase0.sh"
_TDD_TEMPLATE = _REPO / "src/superclaude/skills/tdd/refs/build-request-template.md"

_NOT_FOUND = (
    "Routing guide not found. pipx/pip install: run superclaude update. "
    "Plugin install: update the SuperClaude plugin. Until then, recommendations "
    "do not use the routing guide."
)


def _text() -> str:
    return _SKILL.read_text(encoding="utf-8")


def _section(text: str, start: str, end: str) -> str:
    begin = text.index(start)
    return text[begin : text.index(end, begin + len(start))]


def test_step_0_comes_before_the_hot_path():
    text = _text()
    assert text.index("## Step 0") < text.index("## Hot-Path Cache Lookup")


def test_guide_locations_are_listed_in_order():
    step0 = _section(_text(), "## Step 0", "## Hot-Path Cache Lookup")
    paths = [
        "`~/.claude/HOW-WE-WORK.md`",
        "`${CLAUDE_SKILL_DIR}/refs/HOW-WE-WORK.md`",
        "`${CLAUDE_PLUGIN_ROOT}/skills/sc-recommend/refs/HOW-WE-WORK.md`",
        "`src/superclaude/core/HOW-WE-WORK.md`",
    ]
    positions = [step0.index(p) for p in paths]
    assert positions == sorted(positions), positions


def test_guide_not_found_line_is_shared_with_help():
    assert _NOT_FOUND in _text()
    assert _NOT_FOUND in _HELP.read_text(encoding="utf-8")


def test_hard_limit_overrides_native_first():
    text = _text()
    assert "hard limit overrides native first" in text
    assert "more than 5 edits or touches more than one source file" in text


def test_mandatory_flags_rule_is_present():
    assert "Every flag listed in the row's `mandatory_flags`" in _text()


def test_builtins_allowed_in_r2_and_r4():
    text = _text()
    r2 = _section(text, "### Rule R2", "### Rule R3")
    r4 = _section(text, "### Rule R4", "## Return Contract")
    for rule in (r2, r4):
        assert "/code-review" in rule and "/security-review" in rule


def test_uv_cache_step_is_gated():
    hot = _section(_text(), "## Hot-Path Cache Lookup", "## Phase 0")
    assert "**Availability gate" in hot
    assert "test -f src/superclaude/cli/recommend/prompts.py" in hot
    assert "uv run superclaude recommend --help" in hot
    assert "recommend CLI unavailable; cache skipped" in hot


def test_match_uses_the_whole_objective_and_preserves_explicit_selection():
    step0 = _section(_text(), "## Step 0", "## Hot-Path Cache Lookup")
    for rule in (
        "whole requested outcome",
        "authorization ceiling",
        "existing artifact",
        "Intent phrases are discovery hints",
        "Preserve explicit command/executor selection",
        "never a candidate that sends the user back",
        "ask one clarifying question",
    ):
        assert rule in step0
    assert "take the row with the higher" not in step0
    assert "at least one of its `intent` phrases" not in step0


def test_ordered_output_resolves_branches_before_emitting_steps():
    ordered = _section(_text(), "### Ordered-workflow template", "## Phase 3")
    for rule in (
        "Select exactly one alternative branch",
        "report-only or plan-only request stops",
        "Supported explicit choices outrank ordinary defaults",
        "stronger project rule conflicts",
        "never silently increase authority",
        "missing required input needs clarification",
        "Report-only is not automatically zero-write",
    ):
        assert rule in ordered
    assert "Emit every step of the row" not in ordered


def test_interface_evidence_accepts_declarations_not_conflicting_examples():
    rule = _section(_text(), "### Rule R1", "### Rule R2")
    reference = (_SKILL.parent / "refs/surface-enumeration.md").read_text()
    for text in (rule, reference):
        assert "formal Usage" in text
        assert "keyword" in text
        assert "mode=update" in text and "mode=quick" in text
        assert "example-only" in text
        assert "conflicting" in text
    for unsupported in ("--validate", "--preview", "--output"):
        assert unsupported in rule


def test_verification_follows_actual_activation_and_relevant_dependencies():
    source = _text()
    candidate = _section(source, "### Step C", "### Graceful degradation")
    reference = (_SKILL.parent / "refs/surface-enumeration.md").read_text()
    for text in (candidate, reference):
        assert "self-contained" in text
        assert "Skill Invocation" in text
        assert "backing skill" in text
        assert "tdd" in text
        assert "contract gap" in text.lower()
        assert "not installed" in text
    assert "Commands are thin dispatchers" not in source
    assert "skills/<name>/SKILL.md` first" in reference
    assert "project `.claude/agents/<name>.md` first" in reference
    assert "source/active-copy disagreement" in source
    assert "including a cached hint" in candidate


def test_retirement_checks_provenance_without_excluding_custom_commands():
    reference = (_SKILL.parent / "refs/surface-enumeration.md").read_text()
    for rule in (
        "deprecated: true",
        "Source absence alone is not retirement evidence",
        "installed-only/custom extensions remain eligible",
        "Uncertain same-name custom ownership needs clarification",
        "not blanket rejection/deletion",
        "Verify replacements independently",
    ):
        assert rule in reference
    r2 = _section(_text(), "### Rule R2", "### Rule R3")
    assert "readable file" in r2
    assert "retired targets" in r2
    assert "custom extensions" in r2


def test_missing_requested_targets_stay_visible_while_irrelevant_ghosts_drop():
    # FR-06: a missing plugin capability stays visibly unavailable.
    row = next(
        line
        for line in _text().splitlines()
        if line.startswith("| Candidate source missing |")
    )
    assert "Drop an irrelevant candidate without noise" in row
    assert "`not installed: <name>`, never runnable" in row
    for selected in (
        "a matched routing row's step",
        "an explicitly named command",
        "the guide's Other commands entry selects for this request",
    ):
        assert selected in row
    assert "Do not surface it." not in row
    assert "a matched or selected requested step remains visible" in _text()


def test_live_and_no_guide_fallbacks_keep_workflow_first_policy():
    phase1 = _section(_text(), "## Phase 1", "## Phase 2")
    rubric = (_SKILL.parent / "refs/delegation-vs-native-heuristics.md").read_text()
    for text in (phase1, rubric):
        assert "level 3" in text
        assert "explicit MDTM" in text
        assert "long-running" in text
        assert "standard" in text.lower()
        assert "quick" in text.lower()
        assert "structural migrations" in text
        assert "for anything larger, longer, or riskier" not in text
    assert "**No guide:** skip cache helpers" in phase1
    assert "Reading many files" in phase1
    assert "existing plan goes straight to its executor" in phase1


def test_cache_hit_is_a_reverified_request_specific_hint():
    hot = _section(_text(), "## Hot-Path Cache Lookup", "## Phase 0")
    for rule in (
        "a hit is only a hint",
        "actual callable copy",
        "lifecycle guidance",
        "reconstruct the handoff",
        "current request's verified paths/inputs/mode/output",
        "Never emit a saved envelope verbatim",
        "@{inputs}",
        "miss_validation_stale",
        "miss_budget_exceeded",
        "no-guide, unavailable-helper and non-checkout handling remain live-only",
    ):
        assert rule in hot
    assert "emit `recommendation` **verbatim**" not in hot
    assert "hand-off envelope unchanged" not in hot
    assert "- If the hint is incompatible," in hot
    rejection = hot.split("- If the hint is incompatible,", 1)[1].split(
        '- `outcome: "native"`', 1
    )[0]
    for rule in (
        "retired",
        "unavailable",
        "contradictory",
        "reject it and use live Phase 0-2 discovery",
        "miss_validation_stale",
        "Do not log a hit for a rejected hint",
    ):
        assert rule in rejection


def test_cold_worker_preserves_verification_and_implementation_boundaries():
    cold = " ".join(COLD_PATH_RUNBOOK.split()).casefold()
    for rule in (
        "whole requested outcome",
        "authority ceiling",
        "actual callable copy",
        "skills prefer installed then project",
        "formal usage",
        "mode=update and mode=quick",
        "skill invocation",
        "deprecated: true",
        "source absence alone does not reject",
        "contract gap",
        "decision-relevant dependencies",
        "level 3",
        "explicit mdtm intent",
        "file count",
        "structural migrations",
        "current-request",
        "cache_update=null",
    ):
        assert rule in cold
    assert "larger, longer, or riskier" not in cold
    assert "parent surfaces your output verbatim" not in cold


def test_classifier_keys_do_not_force_ordinary_planning_into_mdtm():
    assert CLASSIFICATION_KEYS == (
        "spec-generation",
        "codebase-research",
        "task-file-generation",
        "parallel-agent-fanout",
        "roadmap-generation",
        "adversarial-review",
        "cleanup-audit",
        "troubleshoot-debug",
        "web-research",
        "cli-portify",
    )
    classifier = " ".join(CLASSIFIER_PROMPT.split())
    for rule in (
        "explicit MDTM generation",
        "exceptionally complex, long-running",
        "ordinary twelve-file feature over several sessions -> unknown",
        "existing workflow package -> unknown",
        "artifact type is unclear, return unknown",
        "populated-document derivation is different",
    ):
        assert rule in classifier
    assert "turn a spec, report, or build request into a task file" not in classifier
    assert "review-only /sc:spec-panel" not in classifier


def test_optional_cache_insertion_never_bypasses_parent_validation():
    cold = _section(_text(), "## Cold-Path Write-Back", "## Output Constraints")
    for rule in (
        "classifier's existing key",
        "relevant lifecycle guidance",
        "resolved reference paths",
        "Parent validates an optional cache_update",
        "no insertion or row evaluation",
        "Only after successful row insertion",
        "A hit, native result, null payload or failed cache write",
        "Recheck the worker result",
        "never surface worker text unconditionally verbatim",
    ):
        assert rule in cold
    assert "Surface the recommendation verbatim" not in cold


def test_tdd_followup_offers_workflow_and_task_only_for_existing_mdtm():
    line = next(
        line
        for line in _TDD_TEMPLATE.read_text(encoding="utf-8").splitlines()
        if "Suggest downstream workflow" in line
    )
    assert "/sc:workflow docs/[domain]/TDD_[COMPONENT-NAME].md" in line
    assert "/sc:implement" in line
    assert "only executes an MDTM task file that already exists" in line
    assert "create implementation tasks using the `/task` skill" not in line
    assert "invoke the task skill" not in line


def test_recommend_command_summary_is_accurate_and_flags_unchanged():
    text = _COMMAND.read_text(encoding="utf-8")
    assert (
        'argument-hint: "<goal description> [--plugin] [--eval <mode>] [--minstar <N>]"'
        in text
    )
    assert "`--plugin`, `--eval`, and `--minstar` are the only flags." in text
    assert "Default **500**" in text and "**Opt-in**" in text
    summary = _section(text, "## Behavioral Summary", "## Activation")
    for rule in (
        "whole requested outcome",
        "exactly one selected alternative",
        "stop at the requested deliverable",
        "a cache hit is only a hint",
        "never emitted verbatim",
        "copy that would actually run",
        "backing skill",
        "lifecycle guidance",
        "not installed: <name>",
        "contract gap",
        "`/sc:workflow`, then `/sc:implement`",
    ):
        assert rule in summary
    # Plugin mode replaces every local routing step, including guide levels.
    assert "With `--plugin`, steps 1-4 are replaced" in summary
    assert "no local routing row, guide level or `/sc:workflow` step" in summary
    activation = _section(text, "## Activation", "## Examples")
    assert "advisory and fail-open" in activation
    assert "cannot be silently skipped" not in text
    assert "defense-in-depths" not in text


def test_hook_reminder_matches_branches_and_stays_advisory():
    script = _HOOK.read_text(encoding="utf-8")
    assert "sc-recommend|sc:recommend|sc-recommend-protocol) ;;" in script
    exits = {
        line.strip() for line in script.splitlines() if line.strip().startswith("exit ")
    }
    assert exits == {"exit 0"}
    reminder = " ".join(
        _section(script, "<sc-recommend-phase0-reminder", "</sc-recommend").split()
    )
    for rule in (
        "Advisory reminder from a fail-open hook",
        "With --plugin: skip steps 0-4",
        "whole requested outcome",
        "- matched: no cache, no auggie query",
        "- no_match:",
        "- absent (no guide found): no cache helpers",
        "a hit is a hint",
        "never emit the cached text or its paths",
        "Unless matched, issue ONE",
        "copy that would actually run",
        "contract gap",
        "Auggie unavailable — ranking falls back to literal Glob+Read",
    ):
        assert rule in reminder
    assert "MANDATORY" not in reminder
    assert "not optional guidance" not in reminder


@pytest.mark.skipif(
    not (shutil.which("bash") and shutil.which("jq")),
    reason="hook behavior check needs bash and jq on PATH",
)
@pytest.mark.parametrize(
    ("payload", "reminds"),
    [
        ({"tool_name": "Skill", "tool_input": {"skill": "sc-recommend"}}, True),
        ({"tool_name": "Skill", "tool_input": {"skill": "sc:recommend"}}, True),
        (
            {"tool_name": "Skill", "tool_input": {"skill": "sc-recommend-protocol"}},
            True,
        ),
        ({"tool_name": "Skill", "tool_input": {"skill": "sc-workflow"}}, False),
        ({"tool_name": "Bash", "tool_input": {"command": "sc-recommend"}}, False),
        ("not json sc-recommend", False),
    ],
)
def test_hook_is_fail_open_and_matches_only_recommend(payload, reminds):
    stdin = payload if isinstance(payload, str) else json.dumps(payload)
    result = subprocess.run(
        ["bash", str(_HOOK)],
        input=stdin,
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )
    assert result.returncode == 0
    assert ("<sc-recommend-phase0-reminder" in result.stdout) is reminds
    if not reminds:
        assert result.stdout == ""
