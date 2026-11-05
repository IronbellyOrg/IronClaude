"""Alias-only model selection policy (issue #384, owner decision: option A).

These tests check, at the points each test names, that the agent, command and
skill files and the Python package under ``src/superclaude`` use the plain aliases
``opus``, ``sonnet`` and ``haiku`` (or ``inherit`` in frontmatter), apart from the
allow-lists below. In tier mode the launcher sets each ``ANTHROPIC_DEFAULT_*_MODEL``
for a tier the owner may use, so those aliases map to tier models inside a
ccsession tier workspace; otherwise the workspace defaults file's real model ids
apply. See ``docs/reference/model-aliases.md``.

Enforcement type: STATIC (file text and ast). The allow-lists below are the
documented exceptions; every entry carries its reason.
"""

import ast
import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src" / "superclaude"
ALIASES = {"opus", "sonnet", "haiku", "inherit"}

# Allow-list 1: agents that pin a ccsession picker id on purpose. They stop with
# E-TIER-UNAVAILABLE outside a ccsession tier workspace (see
# src/superclaude/skills/sc-issue-protocol/refs/tiers.md).
ISSUE_WORKER_PINS = {
    "src/superclaude/agents/issue-worker-t3.md": "claude-gw-tier3",
    "src/superclaude/agents/issue-worker-t2.md": "claude-gw-tier2",
    "src/superclaude/agents/issue-worker-t1.md": "claude-gw-tier1a",
}

# Allow-list 2: paths that may contain the text "claude-gw-tier". The issue
# workers and their protocol pin tier ids on purpose; ccsession-tag is the
# launcher package (owned by issue #315, read-only for this policy).
TIER_TEXT_ALLOWED = (
    *ISSUE_WORKER_PINS,
    "src/superclaude/skills/sc-issue-protocol/",
    "src/superclaude/skills/ccsession-tag/",
)

# Residual allow-list for full model ids in Python string constants:
# path -> reason. Empty: the only hit when this test was written was fixed.
RESIDUAL_FULL_IDS: dict[str, str] = {}

TIER_TEXT_DIRS = ("agents", "commands", "skills", "cli", "hooks", "core")
TEXT_SUFFIXES = {".md", ".py", ".json", ".yaml", ".yml", ".sh", ".txt", ".toml"}
FULL_ID = re.compile(r"^claude-(opus|sonnet|haiku|fable)-\d")
MODEL_FLAG_WITH_FULL_ID = re.compile(
    r"--models?[ =]+`?claude-(opus|sonnet|haiku|fable)-\d"
)


def _rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _frontmatter_model(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    head = text[4:].split("\n---\n", 1)[0]
    for line in head.splitlines():
        key, _, value = line.partition(":")
        if key.strip() == "model":
            return value.strip().strip("\"'")
    return None


def _markdown_under(*dirs: str) -> list[Path]:
    found = []
    for name in dirs:
        for path in sorted((SRC / name).rglob("*.md")):
            if "skills/ccsession-tag/" not in path.as_posix():
                found.append(path)
    return found


def test_frontmatter_model_is_an_alias_when_present() -> None:
    """A frontmatter ``model:`` is an alias or ``inherit``; issue workers are pinned."""
    files = [
        *sorted((SRC / "agents").glob("*.md")),
        *sorted((SRC / "skills").glob("*/SKILL.md")),
        *sorted((SRC / "commands").glob("*.md")),
    ]
    bad = []
    for path in files:
        model = _frontmatter_model(path)
        if model is None:
            continue
        pin = ISSUE_WORKER_PINS.get(_rel(path))
        if pin is not None:
            if model != pin:
                bad.append(f"{_rel(path)}: {model!r} (pinned {pin!r})")
        elif model not in ALIASES:
            bad.append(f"{_rel(path)}: {model!r}")
    assert bad == []


def test_tier_ids_appear_only_in_allowed_paths() -> None:
    """The text ``claude-gw-tier`` stays inside the documented allow-list."""
    bad = []
    for name in TIER_TEXT_DIRS:
        base = SRC / name
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
                continue
            rel = _rel(path)
            if rel.startswith(TIER_TEXT_ALLOWED):
                continue
            if "claude-gw-tier" in path.read_text(encoding="utf-8", errors="ignore"):
                bad.append(rel)
    assert bad == []


def _docstring_ids(tree: ast.AST) -> set[int]:
    ids = set()
    for node in ast.walk(tree):
        if isinstance(
            node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
        ):
            body = node.body
            if (
                body
                and isinstance(body[0], ast.Expr)
                and isinstance(body[0].value, ast.Constant)
                and isinstance(body[0].value.value, str)
            ):
                ids.add(id(body[0].value))
    return ids


def test_python_selection_constants_are_not_full_model_ids() -> None:
    """No Python string constant selects a model by a full (dated) model id."""
    bad = []
    for path in sorted(SRC.rglob("*.py")):
        rel = _rel(path)
        if rel.startswith("src/superclaude/skills/ccsession-tag/"):
            continue
        if rel in RESIDUAL_FULL_IDS:
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        docstrings = _docstring_ids(tree)
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Constant)
                and isinstance(node.value, str)
                and id(node) not in docstrings
                and FULL_ID.match(node.value)
            ):
                bad.append(f"{rel}:{node.lineno}: {node.value!r}")
    assert bad == []


def test_markdown_does_not_pass_full_model_ids_to_model_flags() -> None:
    """No agent, command or skill text hands a full model id to --model/--models."""
    bad = []
    for path in _markdown_under("agents", "commands", "skills"):
        for number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            if MODEL_FLAG_WITH_FULL_ID.search(line):
                bad.append(f"{_rel(path)}:{number}")
    assert bad == []


def test_reflect_default_model_is_an_alias() -> None:
    """The reflect CLI falls back to the plain alias, not a dated model id."""
    from superclaude.cli.reflect import commands

    assert commands._DEFAULT_MODEL in ALIASES


def test_d12_manual_test_does_not_pin_the_old_reflect_model() -> None:
    """The D12 validation script expects the alias default, not claude-opus-4-8."""
    text = (ROOT / "docs/testing/v5.0.0/user/D12-reflect.md").read_text(
        encoding="utf-8"
    )
    assert "claude-opus-4-8" not in text


def test_issue_chains_use_the_default_brainstorm_models() -> None:
    """The /sc:issue chains pass no --models flag to /sc:brainstorm."""
    text = (SRC / "skills/sc-issue-protocol/refs/chains.md").read_text(encoding="utf-8")
    steps = re.findall(r"`(/sc:brainstorm[^`]*)`", text)
    assert len(steps) >= 3
    assert [step for step in steps if "--models" in step] == []


def test_cleanup_audit_docs_match_the_audit_scanner_pin() -> None:
    """audit-scanner pins sonnet, so the cleanup-audit docs do not say Haiku."""
    assert _frontmatter_model(SRC / "agents/audit-scanner.md") == "sonnet"
    files = [
        *sorted((SRC / "skills/sc-cleanup-audit-protocol").rglob("*.md")),
        SRC / "commands/cleanup-audit.md",
    ]
    assert [_rel(p) for p in files if "Haiku" in p.read_text(encoding="utf-8")] == []


RETRY_REFS = (
    "src/superclaude/skills/sc-implement-protocol/refs/retry.md",
    "src/superclaude/skills/sc-implement-protocol/refs/ledger.md",
    "plugins/superclaude/skills/sc-implement-protocol/refs/retry.md",
    "plugins/superclaude/skills/sc-implement-protocol/refs/ledger.md",
)


def test_retry_ladder_uses_the_variable_names_the_workspace_exports() -> None:
    """The retry ladder names exported slot variables, not underscore spellings."""
    retired = re.compile(r"T[0-4]_Model")
    bad = [
        rel
        for rel in RETRY_REFS
        if retired.search((ROOT / rel).read_text(encoding="utf-8"))
    ]
    assert bad == []
    retry = (ROOT / RETRY_REFS[0]).read_text(encoding="utf-8")
    for name in ("T3Model01", "T2Model02", "T1Model02", "T1Model01"):
        assert name in retry


def test_mapping_document_states_the_exports_and_tiers_exist() -> None:
    """The reference page spells the three exports; the tiers are real."""
    doc = (ROOT / "docs/reference/model-aliases.md").read_text(encoding="utf-8")
    for line in (
        "ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a",
        "ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b",
        "ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2",
    ):
        assert line in doc
    models = json.loads(
        (SRC / "skills/ccsession-tag/ccsession-models.json").read_text(encoding="utf-8")
    )
    assert {"tier1a", "tier1b", "tier2"} <= set(models["tiers"])


@pytest.mark.parametrize("pin", sorted(ISSUE_WORKER_PINS))
def test_issue_worker_allow_list_entries_exist(pin: str) -> None:
    """Every allow-listed issue worker file exists (the list cannot go stale)."""
    assert (ROOT / pin).is_file()
