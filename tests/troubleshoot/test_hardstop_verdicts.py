"""T10 hard-stop verdicts — R-03 acceptance test. Harness §3 T10."""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.troubleshoot._assertions import ValidatorInputs, evaluate_validator
from tests.troubleshoot._procedures import hardstop_verdict

FIX = Path(__file__).parent / "fixtures" / "procedures" / "tasklist"


@pytest.mark.parametrize(
    "name,expect_key",
    [
        ("refused", "verdict"),
        ("authorized", "status"),
        ("no-emitter-no-file", "append_to"),
        ("source-only-read", "capability_verdict"),
    ],
    ids=["refused", "authorized", "no-emitter-no-file", "source-only-read"],
)
def test_hardstop_verdict(name: str, expect_key: str) -> None:
    """R-03: four hard-stop outcomes from the tasklist fixtures."""
    md = (FIX / f"{name}.md").read_text()
    if name == "no-emitter-no-file":
        got = hardstop_verdict(md, ["startup.sh", "out/REPORT.md"])
        assert got.get("append_to") == "out/REPORT.md", got
    elif name == "source-only-read":
        got = hardstop_verdict(md, ["startup.sh", "test-startup-boot.sh"])
        assert got.get("capability_verdict") == "blocked", got
        assert got.get("source_edit") is False, got
    elif name == "refused":
        got = hardstop_verdict(md, [])
        assert got == {
            "verdict": "blocked-on-authorization",
            "status": "blocked",
            "written": True,
        }, got
    else:
        got = hardstop_verdict(md, [])
        assert got.get("status") == "partial", got
        assert got.get("task_rows_required") is True, got
        val = evaluate_validator(ValidatorInputs(report="", tasklist_text=md))
        assert "capability_block_unproven" in val.flags, val.flags
    assert expect_key in got, got
