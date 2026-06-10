"""AC-6: --base precedence (--base > frontmatter start_commit > merge-base) + de-range.

Exercises each precedence branch against the patch_git fixture (rev-parse HEAD ->
_FAKE_HEAD, merge-base -> _FAKE_BASE) and asserts the resolved `config.base`, plus
the F3 de-range invariant: the built `--diff` argument is a SINGLE ref (no `..`).
"""

from __future__ import annotations

from unittest.mock import patch

from superclaude.cli.reflect.config import resolve_config
from superclaude.cli.reflect.models import Verdict
from superclaude.cli.reflect.runner import ReflectRunner

from .conftest import _FAKE_BASE, _FAKE_HEAD

_EXPLICIT = "deadbeefdeadbeefdeadbeefdeadbeefdeadbeef"

_RESUME_TASKLIST = """\
---
id: "TASK-RESUME-BASE-0001"
title: "Resume + base test"
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

# Resume + base test

Body.
"""


def _config(tasklist, **overrides):
    params = dict(depth="standard", model="test-model")
    params.update(overrides)
    return resolve_config(str(tasklist), **params)


def test_base_override_beats_frontmatter(temp_tasklist, patch_git) -> None:
    """--base explicit ref wins over frontmatter start_commit."""
    config = _config(temp_tasklist, base_override=_EXPLICIT)
    assert config.base == _EXPLICIT


def test_frontmatter_start_commit_beats_merge_base(temp_tasklist, patch_git) -> None:
    """No --base -> frontmatter start_commit (_FAKE_BASE) wins over merge-base."""
    config = _config(temp_tasklist)  # temp_tasklist carries start_commit=_FAKE_BASE
    assert config.base == _FAKE_BASE


def test_merge_base_fallback(temp_tasklist, patch_git) -> None:
    """No --base AND no frontmatter start_commit -> merge-base branch (_FAKE_BASE)."""
    # Strip the frontmatter start_commit so the merge-base branch is exercised.
    text = temp_tasklist.read_text(encoding="utf-8").replace(
        f'start_commit: "{_FAKE_BASE}"', 'start_commit: ""'
    )
    temp_tasklist.write_text(text, encoding="utf-8")
    config = _config(temp_tasklist)
    assert config.base == _FAKE_BASE  # via the merge-base fake


def test_diff_arg_is_single_ref_no_range(temp_tasklist, patch_git) -> None:
    """F3 de-range: the built --diff argument is a SINGLE ref, never a `..` range."""
    config = _config(temp_tasklist, base_override=_EXPLICIT)
    prompt = ReflectRunner(config)._build_prompt()
    parts = prompt.split()
    diff_idx = parts.index("--diff")
    diff_value = parts[diff_idx + 1]
    assert diff_value == _EXPLICIT
    assert ".." not in diff_value


def test_base_override_range_value_stored_verbatim_not_split(
    temp_tasklist, patch_git
) -> None:
    """A range-looking --base value is stored VERBATIM (no split/de-range parsing)."""
    rangelike = f"{_FAKE_BASE}..HEAD"
    config = _config(temp_tasklist, base_override=rangelike)
    # Stored verbatim (the wrapper does not split ranges; corruption-prevention is
    # the generator contract's job per FR-6). This pins the no-`..`-parsing property.
    assert config.base == rangelike


def test_base_with_resume_still_short_circuits_clean_head(
    tmp_path, patch_git, patch_runner_env, make_claude_process_stub
) -> None:
    """U7: --base <ref> --resume still short-circuits on a clean matching HEAD.

    --base changes only the audit DIFF scope, not HEAD, so the resume clean-HEAD
    short-circuit (prior reflect_post.head == config.head) still fires -> no launch.
    """
    path = tmp_path / "TASK-RESUME-BASE-0001.md"
    path.write_text(_RESUME_TASKLIST.format(head=_FAKE_HEAD), encoding="utf-8")
    config = _config(path, resume=True, base_override=_EXPLICIT)
    factory = make_claude_process_stub("pass.yaml", rc=0)
    with patch(
        "superclaude.cli.reflect.runner.ClaudeProcess", side_effect=factory
    ) as mock_cls:
        result = ReflectRunner(config).run()
    assert result.verdict is Verdict.PASS
    assert result.verdict.exit_code == 0
    mock_cls.assert_not_called()  # resume short-circuit fired despite --base
