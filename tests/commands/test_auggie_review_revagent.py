"""Content-contract tests for `/sc:auggie-review --revagent <model>`.

The command and protocol are Markdown, so these tests pin the literals the
behavior depends on, sliced by section so a literal in the wrong place fails.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC = REPO_ROOT / "src" / "superclaude"
CMD = (SRC / "commands" / "auggie-review.md").read_text(encoding="utf-8")
SKILL = (SRC / "skills" / "sc-auggie-review-protocol" / "SKILL.md").read_text(
    encoding="utf-8"
)
AGENT = (SRC / "agents" / "auggie-reviewer.md").read_text(encoding="utf-8")

ACCEPTED = {"opus", "sonnet", "haiku", "fable"}
MISSING_MSG = "`--revagent requires a value: one of opus, sonnet, haiku, fable.`"
UNSUPPORTED_MSG = (
    "`--revagent: unsupported value '<v>'. Supported: opus, sonnet, haiku, fable "
    "(native Agent tool model aliases). Full model IDs and backend/gateway aliases "
    "are not accepted; map them to a backend model via your Claude Code / gateway "
    "alias configuration instead.`"
)
WARN = "`WARN: --revagent <value> has no effect at --depth <d> (no internal reviewer agent)`"
EFFECT = "`revagent_effect: none (no internal reviewer at depth=<d>)`"


def _between(text: str, start: str, end: str) -> str:
    i = text.index(start)
    return text[i : text.index(end, i + len(start))]


def _line(text: str, prefix: str) -> str:
    return next(ln for ln in text.splitlines() if ln.strip().startswith(prefix))


def _accepted(text: str) -> set[str]:
    sentence = re.search(r"Accepted: (.*?)\.", text).group(1)
    return set(re.findall(r"`([^`]+)`", sentence))


WAVE0 = _between(SKILL, "### Wave 0", "### Wave 1")
WAVE2 = _between(SKILL, "### Wave 2", "### Wave 3")
STEP4 = _line(WAVE2, "4. For `--depth deep`")
STEP5 = _line(WAVE2, "5. For `--depth deep` **only**")
AUGGIE_FENCE = _between(WAVE2, "```bash\nauggie --print", "\n```")
ERRORS = _between(SKILL, "## Error Handling", "## Token Cost Profile")
OPTION_ROW = _line(CMD, "| `--revagent`")
WAVE0_BULLETS = [ln.strip() for ln in WAVE0.splitlines() if ln.strip().startswith("- ")]


def _bullet(needle: str) -> str:
    return next(b for b in WAVE0_BULLETS if needle in b)


# --- valid selection -------------------------------------------------------


def test_accepted_set_is_exactly_the_agent_tool_enum():
    assert _accepted(OPTION_ROW) == ACCEPTED
    assert _accepted(_bullet("Accepted:")) == ACCEPTED


def test_command_surface():
    hint = _line(CMD, "argument-hint:")
    assert "[--revagent opus|sonnet|haiku|fable]" in hint
    usage = _between(CMD, "## Usage", "## Options")
    assert "--revagent opus" in usage and "--revagent sonnet" in usage
    assert "`--revagent` picks the request alias" in OPTION_ROW
    assert "`--auggie-model`" in OPTION_ROW
    assert "CLAUDE_CODE_SUBAGENT_MODEL_FORCE" in OPTION_ROW
    assert "frontmatter model" in OPTION_ROW


# --- invalid and missing values -------------------------------------------


def test_unsupported_value_stop_and_examples_in_same_bullet():
    bullet = _bullet("Any other value")
    assert UNSUPPORTED_MSG in bullet
    for example in ("`connect`", "`Opus`", "`claude-sonnet-4-6`", "`inherit`"):
        assert example in bullet


def test_missing_value_stop_and_full_predicate():
    bullet = _bullet("Missing value")
    assert MISSING_MSG in bullet
    assert "no following token, or the next token starts with `--`" in bullet


def test_validation_precedes_env_check_and_is_depth_independent():
    step = WAVE0.index("1. Validate `--revagent`")
    assert step < WAVE0.index("command -v auggie")
    assert "applies at every `--depth`" in WAVE0
    assert "never falls back to the default" in WAVE0
    flow1 = _line(CMD, "1. **Parse arguments**")
    assert "`--revagent`" in flow1 and "before step 2" in flow1
    assert "missing or unsupported value STOPs" in flow1


def test_error_handling_rows():
    rows = [ln for ln in ERRORS.splitlines() if ln.startswith("| `--revagent`")]
    assert len(rows) == 2
    missing, unsupported = rows
    assert MISSING_MSG in missing and UNSUPPORTED_MSG in unsupported
    for row in rows:
        assert "STOP at Wave 0" in row and row.rstrip().endswith("| None |")


# --- quick/standard WARN ---------------------------------------------------


def test_warn_is_in_wave0_conditioned_and_audited():
    bullet = _bullet(WARN)
    assert EFFECT in bullet
    assert "`--revagent` was supplied" in bullet
    assert "`quick`" in bullet and "`standard`" in bullet and "deep" not in bullet
    assert "audit log" in bullet
    assert WARN not in STEP5 and EFFECT not in STEP5


# --- propagation -------------------------------------------------------------


def test_step5_passes_model_and_stays_deep_only():
    assert STEP5.strip().startswith("5. For `--depth deep` **only**")
    assert "model: <revagent>" in STEP5
    assert "pass no `model` argument" in STEP5
    assert "re-spawn" in STEP5 and "reuses the same `model` argument" in STEP5


def test_revagent_never_reaches_auggie():
    assert "revagent" not in STEP4
    assert "revagent" not in AUGGIE_FENCE
    assert '--model "${AUGGIE_MODEL:-prism-b}"' in AUGGIE_FENCE


def test_tool_coordination_names_only_the_reviewer_spawn():
    task = _line(CMD, "- **Task**:")
    for literal in (
        "auggie-reviewer",
        "--depth deep",
        "model",
        "--revagent",
        "Auggie CLI",
    ):
        assert literal in task
    assert "Delegate per-persona deep passes to" not in task


# --- omitted flag / default + audit -----------------------------------------


def test_frontmatter_default_unchanged():
    assert "model: opus" in AGENT.split("---")[1]


def test_audit_literals():
    header = _between(SKILL, "<!-- SC:AUGGIE-REVIEW:TARGET", "-->")
    assert "revagent: <opus|sonnet|haiku|fable|default>" in header
    audit_block = _between(SKILL, "## Audit\n", "8. Write")
    assert "- Reviewer agent model: <value|frontmatter default>" in audit_block
    step8 = _line(SKILL, "8. Write `<output-dir>/audit.log`")
    assert "model argument passed on each reviewer spawn" in step8
    assert "`frontmatter`" in step8
