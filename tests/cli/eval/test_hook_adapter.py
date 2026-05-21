"""COMP-014 hook adapter tests (Task T02.14 / D-0034).

The adapter at ``src/superclaude/cli/eval/hook_adapter.py`` wraps
:func:`superclaude.cli.install_hooks.install_hooks` so the cliEval
harness can deploy SuperClaude hooks into a per-eval ``HOME`` without
touching the user's real ``~/.claude/``. These tests pin the four T02.14
acceptance criteria as executable assertions:

1. ``deploy_hooks_to(home_path)`` exists, calls ``install_hooks`` with
   ``target_path=home_path/.claude/settings.json``, and raises
   :class:`HookDeployFailed` with an ``error_tag`` when the underlying
   installer fails.
2. Re-invocation on the same ``home_path`` produces identical filesystem
   state. ``<home_path>/.claude/hooks.json`` is byte-identical (SHA256)
   to the source ``src/superclaude/hooks/hooks.json``.
3. The adapter never writes to the real ``~/.claude/`` directory. The
   mtime of the real HOME (if it exists) MUST NOT change across the
   test run.
4. The error-tag surface is structured: each failure mode carries a
   kebab-case ``error_tag`` the orchestrator can route into
   ``EvalRunner.outcome.artifacts`` without parsing strings.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import pytest

from superclaude.cli.eval import (
    HookDeployFailed,
    deploy_hooks_to,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _source_hooks_json() -> Path:
    """Resolve src/superclaude/hooks/hooks.json the same way the adapter does."""

    # tests/cli/eval/test_hook_adapter.py is at <repo>/tests/cli/eval/.
    # The source file is at <repo>/src/superclaude/hooks/hooks.json.
    repo_root = Path(__file__).resolve().parents[3]
    return repo_root / "src" / "superclaude" / "hooks" / "hooks.json"


def _snapshot_real_home_mtime() -> float | None:
    """Snapshot mtime of the real ``~/.claude/`` directory if it exists.

    Returns ``None`` when the directory is absent (CI hosts without a
    user Claude install). Callers compare against
    :func:`_real_home_mtime_unchanged` to assert no writes leaked.
    """

    real = Path.home() / ".claude"
    if not real.exists():
        return None
    return real.stat().st_mtime


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def per_eval_home(tmp_path: Path) -> Path:
    """Per-test scratch directory mirroring the per-eval HOME shape."""

    home = tmp_path / "eval-home"
    home.mkdir()
    return home


@pytest.fixture
def real_home_mtime_guard() -> float | None:
    """Capture mtime of real ``~/.claude/`` at fixture entry."""

    return _snapshot_real_home_mtime()


# ---------------------------------------------------------------------------
# AC1 — deploy_hooks_to exists with the documented signature
# ---------------------------------------------------------------------------


def test_deploy_hooks_to_writes_settings_json_under_home_path(
    per_eval_home: Path,
) -> None:
    """``install_hooks`` is invoked with ``target_path`` under the per-eval HOME."""

    deploy_hooks_to(per_eval_home)

    settings_path = per_eval_home / ".claude" / "settings.json"
    assert settings_path.exists(), "settings.json must be created under per-eval HOME"

    payload = json.loads(settings_path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    # The merge must have populated the hooks key with the source events.
    assert "hooks" in payload
    assert "SessionStart" in payload["hooks"]


def test_deploy_hooks_to_copies_hook_scripts(per_eval_home: Path) -> None:
    """Hook scripts are deployed to ``<home>/.claude/hooks/``."""

    deploy_hooks_to(per_eval_home)

    scripts_dir = per_eval_home / ".claude" / "hooks"
    assert scripts_dir.is_dir()
    # At least one freshness script must be present (signals install_hooks ran).
    assert any(scripts_dir.glob("freshness-*.sh"))


# ---------------------------------------------------------------------------
# AC2 — verbatim hooks.json copy (SHA256 equality)
# ---------------------------------------------------------------------------


def test_hooks_json_is_byte_identical_to_source(per_eval_home: Path) -> None:
    """``<home>/.claude/hooks.json`` SHA256-matches the source file."""

    deploy_hooks_to(per_eval_home)

    dest = per_eval_home / ".claude" / "hooks.json"
    source = _source_hooks_json()
    assert dest.exists(), "verbatim hooks.json must land under per-eval HOME"
    assert _sha256_of(dest) == _sha256_of(source), (
        f"deployed hooks.json must be byte-identical to {source} (SHA256 mismatch)"
    )


# ---------------------------------------------------------------------------
# AC3 — idempotency (re-invocation produces identical state)
# ---------------------------------------------------------------------------


def test_re_invocation_is_idempotent(per_eval_home: Path) -> None:
    """Calling ``deploy_hooks_to`` twice produces identical FS state."""

    deploy_hooks_to(per_eval_home)

    claude_dir = per_eval_home / ".claude"
    # Snapshot byte-content of the three artefacts the adapter materializes.
    settings_first = (claude_dir / "settings.json").read_bytes()
    hooks_json_first = (claude_dir / "hooks.json").read_bytes()
    script_names_first = sorted(p.name for p in (claude_dir / "hooks").iterdir())

    deploy_hooks_to(per_eval_home)

    settings_second = (claude_dir / "settings.json").read_bytes()
    hooks_json_second = (claude_dir / "hooks.json").read_bytes()
    script_names_second = sorted(p.name for p in (claude_dir / "hooks").iterdir())

    assert settings_first == settings_second
    assert hooks_json_first == hooks_json_second
    assert script_names_first == script_names_second


# ---------------------------------------------------------------------------
# AC4 — never writes to real ~/.claude/
# ---------------------------------------------------------------------------


def test_real_user_claude_dir_is_untouched(
    per_eval_home: Path, real_home_mtime_guard: float | None
) -> None:
    """Mtime of real ``~/.claude/`` is unchanged by a successful deploy."""

    deploy_hooks_to(per_eval_home)

    post_mtime = _snapshot_real_home_mtime()
    assert post_mtime == real_home_mtime_guard, (
        "deploy_hooks_to must never touch the real ~/.claude/ "
        f"(mtime before={real_home_mtime_guard} after={post_mtime})"
    )


def test_refuses_when_home_path_is_real_user_claude_dir(per_eval_home: Path) -> None:
    """``HookDeployFailed`` with ``refused-real-home`` when ``home_path`` is real ~/.claude/."""

    real_claude = Path.home() / ".claude"
    # The defense-in-depth guard compares the resolved ``home_path`` against
    # the resolved real Claude dir; passing the *parent* of that dir as
    # ``home_path`` would cause `install_hooks` to land settings.json under
    # the real `~/.claude/`. Assert refusal happens first.
    with pytest.raises(HookDeployFailed) as exc_info:
        deploy_hooks_to(real_claude.parent)  # i.e., $HOME itself
    assert exc_info.value.error_tag == "refused-real-home"
    assert exc_info.value.home_path == real_claude.parent


def test_refuses_when_home_path_is_descendant_of_real_user_claude_dir(
    tmp_path: Path,
) -> None:
    """Refusal also fires when ``home_path`` lives under real ~/.claude/."""

    # Synthesize a fake ``Path.home()`` so the test never actually has to
    # touch the operator's real $HOME. The adapter's guard resolves
    # ``Path.home() / .claude``, so monkeypatching ``Path.home`` makes the
    # whole comparison deterministic on any CI host.
    fake_home = tmp_path / "fake-home"
    fake_claude = fake_home / ".claude"
    fake_claude.mkdir(parents=True)
    nested = fake_claude / "nested"
    nested.mkdir()

    with patch("superclaude.cli.eval.hook_adapter.Path.home", return_value=fake_home):
        with pytest.raises(HookDeployFailed) as exc_info:
            deploy_hooks_to(nested)
    assert exc_info.value.error_tag == "refused-real-home"


# ---------------------------------------------------------------------------
# Error contract — HookDeployFailed surfaces structured error_tag
# ---------------------------------------------------------------------------


def test_install_hooks_failure_propagates_as_hook_deploy_failed(
    per_eval_home: Path,
) -> None:
    """When ``install_hooks`` returns ``(False, msg)`` the adapter raises with
    ``error_tag='install-hooks-failed'`` and the installer message in ``detail``."""

    installer_msg = "❌ simulated installer failure for AC1 propagation"
    with patch(
        "superclaude.cli.eval.hook_adapter.install_hooks",
        return_value=(False, installer_msg),
    ):
        with pytest.raises(HookDeployFailed) as exc_info:
            deploy_hooks_to(per_eval_home)
    assert exc_info.value.error_tag == "install-hooks-failed"
    assert installer_msg in exc_info.value.detail
    assert exc_info.value.home_path == per_eval_home


def test_missing_source_hooks_json_raises_hook_deploy_failed(
    per_eval_home: Path, tmp_path: Path
) -> None:
    """Absent source ``hooks.json`` produces ``source-hooks-json-missing``."""

    nonexistent = tmp_path / "absent" / "hooks.json"
    with patch(
        "superclaude.cli.eval.hook_adapter._source_hooks_json",
        return_value=nonexistent,
    ):
        with pytest.raises(HookDeployFailed) as exc_info:
            deploy_hooks_to(per_eval_home)
    assert exc_info.value.error_tag == "source-hooks-json-missing"
    assert str(nonexistent) in exc_info.value.detail


def test_hooks_json_copy_failure_raises_hook_deploy_failed(
    per_eval_home: Path,
) -> None:
    """``OSError`` during the verbatim copy is wrapped as
    ``hooks-json-copy-failed`` with the OS error in ``detail``."""

    # Let the install_hooks step succeed, then induce a failure inside the
    # verbatim copy. Patch the dedicated `_copy_hooks_json_verbatim`
    # seam so the patch scope is precise — patching the shared
    # ``shutil.copy2`` global would also break install_hooks's own
    # script-copy pipeline.
    def boom(*_args, **_kwargs):
        raise OSError("simulated EIO during verbatim copy")

    with patch(
        "superclaude.cli.eval.hook_adapter._copy_hooks_json_verbatim",
        side_effect=boom,
    ):
        with pytest.raises(HookDeployFailed) as exc_info:
            deploy_hooks_to(per_eval_home)
    assert exc_info.value.error_tag == "hooks-json-copy-failed"
    assert "simulated EIO during verbatim copy" in exc_info.value.detail
    assert isinstance(exc_info.value.__cause__, OSError)


def test_error_tags_are_kebab_case_strings() -> None:
    """All ``HookDeployFailed.error_tag`` values follow kebab-case so
    orchestrator routing can rely on a stable shape."""

    sample = HookDeployFailed(
        error_tag="install-hooks-failed",
        home_path=Path("/tmp/unused"),
        detail="probe",
    )
    assert sample.error_tag.islower()
    # No underscores; only dashes between lowercase tokens.
    assert "_" not in sample.error_tag
    assert all(part.isalnum() for part in sample.error_tag.split("-"))


# ---------------------------------------------------------------------------
# AC5 — settings.json points the freshness scripts at the per-eval HOME
#       via the install_hooks merge surface
# ---------------------------------------------------------------------------


def test_settings_json_merge_uses_per_eval_target_path(per_eval_home: Path) -> None:
    """``install_hooks`` is invoked with ``target_path=<home>/.claude/settings.json``."""

    captured: dict[str, object] = {}

    real_install_hooks = (
        # Re-import inside the patch to call through to the real installer.
        __import__(
            "superclaude.cli.install_hooks", fromlist=["install_hooks"]
        ).install_hooks
    )

    def spy(target_path: Path | None = None, force: bool = False):
        captured["target_path"] = target_path
        captured["force"] = force
        return real_install_hooks(target_path=target_path, force=force)

    with patch("superclaude.cli.eval.hook_adapter.install_hooks", side_effect=spy):
        deploy_hooks_to(per_eval_home)

    assert captured["target_path"] == per_eval_home / ".claude" / "settings.json"
    assert captured["force"] is False
