"""Mocked end-to-end tests for ``ReflectRunner.run`` (launch->parse->verdict->writeback).

Drives the real runner with ``ClaudeProcess`` patched to the Idiom-B factory (it
writes a chosen fixture contract into the output dir from ``.wait()`` and returns
the rc). Covers the §6 verdict matrix end-to-end plus the G1 max_turns threading
and the G2 resume short-circuit.
"""

from __future__ import annotations

import re
from unittest.mock import patch

import yaml

from superclaude.cli.reflect.config import resolve_config
from superclaude.cli.reflect.models import Verdict
from superclaude.cli.reflect.runner import ReflectRunner

from .conftest import _FAKE_HEAD

_PATCH_TARGET = "superclaude.cli.reflect.runner.ClaudeProcess"
_FM_RE = re.compile(r"^---[ \t]*\n(.*?)\n---[ \t]*$", re.MULTILINE | re.DOTALL)


def _read_reflect_post(path) -> dict | None:
    text = path.read_text(encoding="utf-8")
    fm = yaml.safe_load(_FM_RE.search(text).group(1))
    block = fm.get("reflect_post")
    return block if isinstance(block, dict) else None


def _config(tasklist, **overrides):
    params = dict(depth="standard", model="test-model")
    params.update(overrides)
    return resolve_config(str(tasklist), **params)


def test_e2e_pass(
    temp_tasklist, patch_git, patch_runner_env, make_claude_process_stub
) -> None:
    config = _config(temp_tasklist)
    factory = make_claude_process_stub("pass.yaml", rc=0)
    with patch(_PATCH_TARGET, side_effect=factory) as mock_cls:
        result = ReflectRunner(config).run()
    assert result.verdict is Verdict.PASS
    assert result.verdict.exit_code == 0
    mock_cls.assert_called_once()
    # G1: max_turns threaded explicitly (default 250, never the primitive's 100).
    assert mock_cls.call_args.kwargs["max_turns"] == config.max_turns == 250
    assert _read_reflect_post(temp_tasklist)["verdict"] == "pass"


def test_e2e_halted(
    temp_tasklist, patch_git, patch_runner_env, make_claude_process_stub
) -> None:
    config = _config(temp_tasklist)
    factory = make_claude_process_stub("halted_regression.yaml", rc=0)
    with patch(_PATCH_TARGET, side_effect=factory) as mock_cls:
        result = ReflectRunner(config).run()
    assert result.verdict is Verdict.HALTED
    assert result.verdict.exit_code == 10
    mock_cls.assert_called_once()
    assert _read_reflect_post(temp_tasklist)["verdict"] == "halted"


def test_e2e_degraded(
    temp_tasklist, patch_git, patch_runner_env, make_claude_process_stub
) -> None:
    config = _config(temp_tasklist)
    factory = make_claude_process_stub("degraded_serena.yaml", rc=0)
    with patch(_PATCH_TARGET, side_effect=factory) as mock_cls:
        result = ReflectRunner(config).run()
    assert result.verdict is Verdict.DEGRADED
    assert result.verdict.exit_code == 11
    mock_cls.assert_called_once()
    assert _read_reflect_post(temp_tasklist)["verdict"] == "degraded"


def test_e2e_blocked_no_contract(
    temp_tasklist, patch_git, patch_runner_env, make_claude_process_stub
) -> None:
    config = _config(temp_tasklist)
    factory = make_claude_process_stub(None, rc=0, write_contract=False)
    with patch(_PATCH_TARGET, side_effect=factory) as mock_cls:
        result = ReflectRunner(config).run()
    assert result.verdict is Verdict.BLOCKED
    assert result.verdict.exit_code == 2
    mock_cls.assert_called_once()


def test_e2e_blocked_timeout(
    temp_tasklist, patch_git, patch_runner_env, make_claude_process_stub
) -> None:
    config = _config(temp_tasklist)
    factory = make_claude_process_stub(None, rc=124, write_contract=False)
    with patch(_PATCH_TARGET, side_effect=factory) as mock_cls:
        result = ReflectRunner(config).run()
    assert result.verdict is Verdict.BLOCKED
    assert result.verdict.exit_code == 2
    assert result.reason == "timeout"
    mock_cls.assert_called_once()


def test_e2e_blocked_child_crash(
    temp_tasklist, patch_git, patch_runner_env, make_claude_process_stub
) -> None:
    config = _config(temp_tasklist)
    factory = make_claude_process_stub(None, rc=1, write_contract=False)
    with patch(_PATCH_TARGET, side_effect=factory) as mock_cls:
        result = ReflectRunner(config).run()
    assert result.verdict is Verdict.BLOCKED
    assert result.verdict.exit_code == 2
    mock_cls.assert_called_once()


_RESUME_TASKLIST = """\
---
id: "TASK-RESUME-0001"
title: "Resume test"
status: "🟠 Doing"
start_commit: "1111111111111111111111111111111111111111"
spec_path: ""
reflect_post:
  verdict: pass
  status: success
  tier_reached: 2
  head: "{head}"
  deviations:
    authorized: 0
    necessary: 0
    drift: 0
    regression: 0
---

# Resume test

Body.
"""


def test_e2e_resume_clean_head_skips_launch(
    tmp_path, patch_git, patch_runner_env, make_claude_process_stub
) -> None:
    """G2: prior reflect_post pass on the current HEAD -> skip launch, exit 0."""
    path = tmp_path / "TASK-RESUME-0001.md"
    path.write_text(_RESUME_TASKLIST.format(head=_FAKE_HEAD), encoding="utf-8")
    config = _config(path, resume=True)
    factory = make_claude_process_stub("pass.yaml", rc=0)
    with patch(_PATCH_TARGET, side_effect=factory) as mock_cls:
        result = ReflectRunner(config).run()
    assert result.verdict is Verdict.PASS
    assert result.verdict.exit_code == 0
    assert result.reason == "resume-clean-head"
    mock_cls.assert_not_called()


def test_e2e_resume_stale_head_launches(
    tmp_path, patch_git, patch_runner_env, make_claude_process_stub
) -> None:
    """G2: prior reflect_post head != current HEAD -> normal launch runs."""
    path = tmp_path / "TASK-RESUME-0002.md"
    path.write_text(
        _RESUME_TASKLIST.format(head="0000000000000000000000000000000000000000"),
        encoding="utf-8",
    )
    config = _config(path, resume=True)
    factory = make_claude_process_stub("pass.yaml", rc=0)
    with patch(_PATCH_TARGET, side_effect=factory) as mock_cls:
        result = ReflectRunner(config).run()
    assert result.verdict is Verdict.PASS
    mock_cls.assert_called_once()


def test_e2e_frontmatter_stale_downgrades_pass_to_blocked(
    temp_tasklist, patch_git, patch_runner_env, make_claude_process_stub
) -> None:
    """FR-6 fail-closed: a clean PASS contract whose write-back hits a concurrent
    edit (frontmatter-stale) MUST downgrade to BLOCKED / exit 2 -- the
    load-bearing race-safe write-back defense (runner.py downgrade branch). A
    pass audit that could not be durably recorded must NOT leak as a green gate.
    """
    config = _config(temp_tasklist)
    factory = make_claude_process_stub("pass.yaml", rc=0)
    with (
        patch(_PATCH_TARGET, side_effect=factory) as mock_cls,
        patch(
            "superclaude.cli.reflect.runner.write_reflect_post",
            return_value="frontmatter-stale",
        ),
    ):
        result = ReflectRunner(config).run()
    mock_cls.assert_called_once()
    # The contract itself derived PASS, but the unwritable frontmatter forces
    # a fail-closed downgrade so the gate never greens on an unrecorded audit.
    assert result.verdict is Verdict.BLOCKED
    assert result.verdict.exit_code == 2
    assert result.reason == "frontmatter-stale"
    assert result.write_status == "frontmatter-stale"


def test_e2e_frontmatter_missing_downgrades_pass_to_blocked(
    temp_tasklist, patch_git, patch_runner_env, make_claude_process_stub
) -> None:
    """FR-6 fail-closed: a PASS contract whose tasklist has no parseable
    frontmatter block downgrades to BLOCKED / exit 2 (no silent green gate)."""
    config = _config(temp_tasklist)
    factory = make_claude_process_stub("pass.yaml", rc=0)
    with (
        patch(_PATCH_TARGET, side_effect=factory) as mock_cls,
        patch(
            "superclaude.cli.reflect.runner.write_reflect_post",
            return_value="frontmatter-missing",
        ),
    ):
        result = ReflectRunner(config).run()
    mock_cls.assert_called_once()
    assert result.verdict is Verdict.BLOCKED
    assert result.verdict.exit_code == 2
    assert result.reason == "frontmatter-missing"
