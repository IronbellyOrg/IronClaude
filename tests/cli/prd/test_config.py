"""Unit tests for superclaude.cli.prd.config.

Regression coverage for FU-003 / TASK-RF-track-3-20260518-231708 — the source-
of-truth defect at ``src/superclaude/cli/prd/config.py:100`` where
``output=None`` previously defaulted to ``Path(".")`` and caused
``superclaude prd run`` invocations from the repo root to create stray
``<repo-root>/prd-<slug>/`` directories. The patched module now prefers
``<cwd>/.dev/eval-workspaces/`` when the ``.dev/`` sandbox exists, only
falling back to CWD outside a repo.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from superclaude.cli.prd.config import resolve_config


def test_resolve_config_defaults_output_to_dev_eval_workspaces(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """When ``.dev/`` exists at CWD, default output dir is ``.dev/eval-workspaces/``, not CWD.

    Pins the FU-003 source-fix: ``resolve_config(output=None, product="test product")``
    must route ``task_dir`` to ``<cwd>/.dev/eval-workspaces/prd-test-product`` rather
    than ``<cwd>/prd-test-product`` so no stray dir leaks to the simulated repo root.
    """
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".dev").mkdir()

    cfg = resolve_config(
        "make a PRD",
        product="test product",
    )

    expected_task_dir = tmp_path / ".dev" / "eval-workspaces" / "prd-test-product"
    assert cfg.task_dir == expected_task_dir, (
        f"task_dir should resolve under .dev/eval-workspaces/, got: {cfg.task_dir}"
    )

    # Pin that resolve_config actually materialises the sandbox dir — otherwise
    # a regression that stops calling sandbox.mkdir(...) would still pass the
    # path-equality check above while breaking downstream callers that assume
    # output_path exists on disk.
    sandbox_dir = tmp_path / ".dev" / "eval-workspaces"
    assert sandbox_dir.is_dir(), (
        f".dev/eval-workspaces/ should be created by resolve_config, "
        f"but {sandbox_dir} does not exist as a directory"
    )

    repo_root_names = {p.name for p in tmp_path.iterdir()}
    assert "prd-test-product" not in repo_root_names, (
        f"stray prd-test-product/ leaked to simulated repo root: {repo_root_names}"
    )
