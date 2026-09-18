"""Tests for the globally installed Bash inspection policy resource."""

from __future__ import annotations

from pathlib import Path

from superclaude.cli import install_core
from superclaude.cli.prompt_policy import (
    BASH_INSPECTION_POLICY,
    load_bash_inspection_policy,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
CORE = REPO_ROOT / "src/superclaude/core"


def test_policy_resource_contains_required_contract():
    policy = load_bash_inspection_policy()

    assert policy == BASH_INSPECTION_POLICY
    assert "five or more serial Bash inspections" in policy
    assert "Same-turn parallel tool calls are exempt" in policy
    assert "maximum 15 commands" not in policy  # wording is "Limit each chunk"
    assert "Limit each chunk to 15 commands" in policy
    assert "30 seconds aggregate runtime" in policy
    assert "100 KiB" in policy
    assert "does **not** count as a tracked Read" in " ".join(policy.split())
    assert "not a security boundary" in policy


def test_global_claude_imports_policy():
    claude_md = (CORE / "CLAUDE.md").read_text(encoding="utf-8")
    assert "@BASH_INSPECTION_POLICY.md" in claude_md


def test_core_install_and_listing_include_policy(tmp_path, monkeypatch):
    target = tmp_path / ".claude"
    ok, message = install_core.install_core_files(target_path=target, force=True)
    assert ok, message
    installed = (target / "BASH_INSPECTION_POLICY.md").read_text(encoding="utf-8")
    assert installed.strip() == BASH_INSPECTION_POLICY

    monkeypatch.setattr(install_core.Path, "home", classmethod(lambda cls: tmp_path))
    assert "BASH_INSPECTION_POLICY.md" in install_core.list_installed_core_files()
