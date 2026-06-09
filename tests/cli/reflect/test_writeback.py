"""Unit tests for the FR-6 frontmatter write-back + FR-7 sidecar.

Case 7: atomic write-back success preserves the markdown body byte-for-byte and
emits the §6 structured ``reflect_post`` block. Case 8: a concurrent edit
(compare-mismatch) bails to ``frontmatter-stale`` without overwriting, and the
sidecar still records the stale status.
"""

from __future__ import annotations

import re
from pathlib import Path
from unittest.mock import patch

import yaml

from superclaude.cli.reflect.models import ReflectResult, Verdict
from superclaude.cli.reflect.runner import write_reflect_post, write_sidecar

_FM_RE = re.compile(r"^---[ \t]*\n(.*?)\n---[ \t]*$", re.MULTILINE | re.DOTALL)

_TASKLIST = """\
---
id: "TASK-WB-0001"
title: "Write-back test"
status: "🟠 Doing"
start_commit: "abc123"
reflect_post: ""
spec_path: ""
---

# Write-back test

Body paragraph one — must be byte-identical after write-back.

- a list item
- another item
"""


def _pass_result() -> ReflectResult:
    return ReflectResult(
        verdict=Verdict.PASS,
        status="success",
        tier_reached=2,
        reason="pass",
        report_path="/tmp/reflect-out/REPORT.md",
        contract_path="/tmp/reflect-out/return-contract.yaml",
        deviations={"authorized": 0, "necessary": 0, "drift": 0, "regression": 0},
        child_exit_code=0,
        write_status="",
    )


def _body_after_frontmatter(text: str) -> str:
    m = _FM_RE.search(text)
    assert m is not None
    return text[m.end() :]


def test_writeback_success_preserves_body(tmp_path) -> None:
    """Case 7: write-back injects the §6 block and leaves the body unchanged."""
    path = tmp_path / "TASK-WB-0001.md"
    path.write_text(_TASKLIST, encoding="utf-8")
    original_body = _body_after_frontmatter(_TASKLIST)

    status = write_reflect_post(
        path, _pass_result(), head="deadbeef", reviewed_at="2026-06-09T00:00:00Z"
    )
    assert status == "written"

    new_text = path.read_text(encoding="utf-8")
    # Body bytes preserved exactly.
    assert _body_after_frontmatter(new_text) == original_body

    # The §6 structured block is present with all fields.
    fm = yaml.safe_load(_FM_RE.search(new_text).group(1))
    block = fm["reflect_post"]
    assert isinstance(block, dict)
    for key in (
        "verdict",
        "status",
        "run_id",
        "tier_reached",
        "report",
        "contract",
        "reason",
        "deviations",
        "head",
        "reviewed_at",
    ):
        assert key in block, f"missing reflect_post field: {key}"
    assert block["verdict"] == "pass"
    assert block["head"] == "deadbeef"
    assert block["deviations"] == {
        "authorized": 0,
        "necessary": 0,
        "drift": 0,
        "regression": 0,
    }
    # Sibling frontmatter keys are preserved.
    assert fm["id"] == "TASK-WB-0001"
    assert fm["title"] == "Write-back test"


def test_writeback_compare_mismatch_bails_and_sidecars(tmp_path) -> None:
    """Case 8: a concurrent edit -> frontmatter-stale, no overwrite, sidecar written."""
    path = tmp_path / "TASK-WB-0001.md"
    path.write_text(_TASKLIST, encoding="utf-8")
    orig_bytes = _TASKLIST.encode("utf-8")
    result = _pass_result()

    # read_bytes is called twice in write_reflect_post: capture, then compare.
    # Return a different value on the compare to simulate a concurrent edit.
    with patch.object(
        Path, "read_bytes", side_effect=[orig_bytes, b"DIFFERENT CONCURRENT EDIT"]
    ):
        status = write_reflect_post(
            path, result, head="deadbeef", reviewed_at="2026-06-09T00:00:00Z"
        )
    assert status == "frontmatter-stale"

    # The file was NOT overwritten (still the original content).
    assert path.read_text(encoding="utf-8") == _TASKLIST

    # The sidecar is written with the stale write_status.
    out_dir = tmp_path / "out"
    sidecar = write_sidecar(out_dir, result, env_alias_count=0, write_status=status)
    assert sidecar.exists()
    data = yaml.safe_load(sidecar.read_text(encoding="utf-8"))
    assert data["write_status"] == "frontmatter-stale"
    # The caller would exit non-zero on a stale write (fail-closed).
    assert result.verdict.exit_code == 0  # the verdict itself is pass...
    # ...but the runner downgrades it to blocked on stale; that downgrade is
    # exercised end-to-end in
    # test_runner_e2e.test_e2e_frontmatter_stale_downgrades_pass_to_blocked.
