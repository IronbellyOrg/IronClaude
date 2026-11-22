"""The definition file of the daily Orca automation (Task 18): text only, switched off.

Nothing here creates, runs or switches on an automation; the test reads one Markdown file.
"""

from __future__ import annotations

import re
from pathlib import Path

DEFINITION = (
    Path(__file__).resolve().parents[2] / "scripts/worktree_cleanup_orca_automation.md"
)


def text() -> str:
    return DEFINITION.read_text(encoding="utf-8")


def field(name: str) -> str:
    match = re.search(rf"^{re.escape(name)}: (.+)$", text(), re.M)
    assert match, f"no {name} line"
    return match.group(1).strip()


def command() -> str:
    section = text().split("## Command to run (precheck shape)", 1)[1]
    block = section.split("```", 2)[1]
    return block.strip()


def test_the_three_header_fields():
    assert field("Name") == "worktree-cleanup-daily"
    assert field("Trigger (UTC)") == "0 8 * * *"
    assert field("Status") == "written, not switched on"


def test_the_name_never_starts_with_coordinator():
    assert not field("Name").startswith("coordinator-")


def test_the_sections_of_the_model_file_are_all_there():
    body = text()
    for heading in (
        "## Why the name and the trigger are what they are",
        "## Command to run (precheck shape)",
        "## Rollout ladder",
        "## Environment variables (names only; no value belongs in any file)",
        "## Human steps, in order",
        "## When a run fails",
    ):
        assert heading in body, heading


def test_the_command_is_the_precheck_shape_for_prune_without_apply():
    cmd = command()
    assert cmd.startswith("bash -lc 'set -a; [ -f ~/.aienv ] && . ~/.aienv;")
    assert "[ -f ~/.env ] && . ~/.env; set +a;" in cmd
    assert (
        "setsid nohup uv run --no-project python scripts/worktree_cleanup.py prune"
        in cmd
    )
    assert "--out <out dir>" in cmd and ">> <out dir>/run.log 2>&1 < /dev/null &" in cmd
    assert re.search(r"\bprune\b", cmd)
    assert "--apply" not in cmd  # the first week reports only
    assert cmd.endswith("'; exit 1")


def test_the_trigger_notes_and_the_unverified_items_are_stated():
    body = text()
    assert "2:00 AM Central in winter" in body and "3:00 AM" in body
    assert "--timezone America/Chicago" in body
    assert body.count("UNVERIFIED") >= 2
    assert "skipped_precheck" in body


def test_the_rollout_ladder_and_the_environment_names():
    body = text()
    ladder = body.split("## Rollout ladder", 1)[1].split("\n## ", 1)[0]
    assert "first week it reports only" in ladder
    assert "adds `--apply`" in ladder
    assert "a dispatched worker does none of this" in ladder
    for name in (
        "GH_TOKEN",
        "RUN_EVIDENCE_REPO",
        "RUN_EVIDENCE_DIR",
        "WORKTREE_CLEANUP_IDLE_DAYS",
    ):
        assert f"`{name}`" in body


def test_no_token_value_appears():
    body = text()
    assert not re.search(r"(GH_TOKEN|GITHUB_TOKEN)\s*=\s*\S", body)
    # token shapes, spelled from two pieces so this file holds none itself
    shapes = [
        r"gh" + r"[pousr]_[A-Za-z0-9]{20,}",
        r"github" + r"_pat_[A-Za-z0-9_]{20,}",
    ]
    for shape in shapes:
        assert not re.search(shape, body)


def test_no_em_or_en_dash():
    dashes = (chr(0x2014), chr(0x2013))  # built from code points so this file has none
    for content in (text(), Path(__file__).read_text(encoding="utf-8")):
        assert not any(d in content for d in dashes)


def test_the_file_only_describes_it_nothing_is_created_or_run():
    body = text()
    assert "Definition only. Nothing in this file has been created in Orca" in body
    assert "leave it switched off" in body
