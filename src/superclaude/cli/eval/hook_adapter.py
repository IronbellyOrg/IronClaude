"""COMP-014 install_hooks adapter for per-eval HOME (Task T02.14 / D-0034).

This module is the single integration point between the cliEval harness's
per-eval ``HOME`` (materialized by :class:`HomeIsolation` in T02.11) and
the production hook installer at :mod:`superclaude.cli.install_hooks`.
The adapter has two jobs:

1. **Reuse, do not duplicate.** Delegate the script-copy + settings.json
   merge to the existing ``install_hooks`` so the per-eval hook surface
   is exactly the production user-install surface. A separate copy
   pipeline would drift; the COMP-014 reuse contract pins this to the
   one installer.
2. **Deploy ``hooks.json`` verbatim.** ``install_hooks`` merges hook
   registrations *into* ``settings.json`` but never copies the source
   ``hooks.json`` to the target HOME. The acceptance criteria for T02.14
   require ``<home_path>/.claude/hooks.json`` to be byte-identical to
   ``src/superclaude/hooks/hooks.json`` so post-mortem inspection and the
   FR-G* gate tests can SHA256-compare the source-of-truth registrations
   against what the per-eval HOME shipped. The adapter performs this
   second copy itself.

Defense-in-depth: a pre-flight refusal asserts ``home_path`` is not the
real ``~/.claude/`` (resolves both sides; rejects any equality or
descendant relationship). This complements but does not replace the
:class:`HomeIsolation` containment guard — the adapter MAY be invoked
directly by tests, so the guard must live here too.

Idempotency: re-invoking ``deploy_hooks_to`` against the same
``home_path`` produces identical filesystem state. ``install_hooks``
itself is idempotent (existing scripts are skipped without ``--force``;
the settings.json merge skips matcher collisions). The verbatim
``hooks.json`` copy uses ``shutil.copy2`` which overwrites with the same
bytes when the source is unchanged.

Error contract: any failure inside the adapter raises
:class:`HookDeployFailed` with an :attr:`HookDeployFailed.error_tag`
attribute the EvalRunner (T03.x) propagates into
``EvalRunner.outcome.artifacts``. The tag is a short kebab-case
identifier the orchestrator buckets ERRORED evals by without parsing
human-readable strings.

Cross-links
===========

* COMP-006 :class:`HomeIsolation` (T02.11 / D-0032) — supplies the
  ``home_path`` argument.
* NFR-ISO2 atomic-setup wrapper (T02.13 / D-0033) — invokes the
  adapter from inside ``HomeIsolation.setup``'s post-mkdtemp block in
  a future wiring task.
* :func:`superclaude.cli.install_hooks.install_hooks` — the underlying
  installer this adapter wraps.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from superclaude.cli.install_hooks import install_hooks

__all__ = [
    "HookDeployFailed",
    "deploy_hooks_to",
]


# Relative paths under the per-eval HOME that the adapter writes to.
_SETTINGS_RELPATH = (".claude", "settings.json")
_HOOKS_JSON_RELPATH = (".claude", "hooks.json")


class HookDeployFailed(Exception):
    """Raised by :func:`deploy_hooks_to` when hook deployment cannot complete.

    Carries a short kebab-case :attr:`error_tag` the orchestrator
    (:class:`EvalRunner`, T03.x) routes into
    ``EvalRunner.outcome.artifacts`` so failed evals can be bucketed
    without parsing the human-readable message.

    Attributes:
        error_tag: Short identifier for the failure mode. One of:

            * ``"refused-real-home"`` — ``home_path`` resolved to (or
              under) the real ``~/.claude/``; defense-in-depth guard
              fired BEFORE any filesystem write.
            * ``"install-hooks-failed"`` — the underlying
              :func:`install_hooks` returned ``success=False``. The
              installer's message is preserved in :attr:`detail`.
            * ``"hooks-json-copy-failed"`` — the verbatim
              ``hooks.json`` copy raised :class:`OSError`. The OS
              error message is preserved in :attr:`detail`.
            * ``"source-hooks-json-missing"`` — the source
              ``src/superclaude/hooks/hooks.json`` is not on disk.
              Should never happen in a working checkout; surfaced
              explicitly to make missing-source bugs loud.

        home_path: The per-eval HOME the adapter was asked to deploy to.
        detail: Human-readable failure detail (installer message,
            ``OSError`` rendering, etc.). Never contains the error_tag
            itself so the two surfaces stay independent.
    """

    def __init__(
        self,
        *,
        error_tag: str,
        home_path: Path,
        detail: str,
    ) -> None:
        self.error_tag = error_tag
        self.home_path = home_path
        self.detail = detail
        super().__init__(
            f"COMP-014 hook deploy failed [{error_tag}] for home_path={home_path!s}: {detail}"
        )


def _real_user_claude_dir() -> Path:
    """Resolve the user's real ``~/.claude/`` directory.

    Returns the resolved (symlinks collapsed) path. Used by the
    defense-in-depth refusal so a per-eval ``home_path`` that is a
    symlink to the real user HOME still fails the equality / descendant
    check.
    """

    return (Path.home() / ".claude").resolve(strict=False)


def _refuse_real_home(home_path: Path) -> None:
    """Reject ``home_path`` when any adapter write would land under real ``~/.claude/``.

    Two attack surfaces are caught:

    * ``home_path`` itself resolves to (or under) the real
      ``~/.claude/`` directory — every adapter write is anchored at
      ``home_path``, so this catches direct attempts.
    * ``home_path / .claude`` resolves to (or under) the real
      ``~/.claude/`` — the subtle case where the caller passes their
      own ``$HOME`` as ``home_path`` and the adapter's
      ``<home_path>/.claude/settings.json`` write would otherwise
      silently target the real configuration directory.

    Both sides are resolved with ``strict=False`` so a symlink in either
    direction is collapsed before comparison.
    """

    real = _real_user_claude_dir()
    resolved_home = home_path.resolve(strict=False)
    resolved_claude_subdir = (home_path / ".claude").resolve(strict=False)

    def _matches(candidate: Path) -> bool:
        return candidate == real or candidate.is_relative_to(real)

    if _matches(resolved_home) or _matches(resolved_claude_subdir):
        raise HookDeployFailed(
            error_tag="refused-real-home",
            home_path=home_path,
            detail=(
                f"home_path {home_path!s} (resolved={resolved_home!s}; "
                f"claude_subdir={resolved_claude_subdir!s}) intersects the "
                f"real user Claude dir {real!s}; refusing to write hooks "
                f"under the real ~/.claude/"
            ),
        )


def _source_hooks_json() -> Path:
    """Locate the canonical ``src/superclaude/hooks/hooks.json``.

    Mirrors :func:`superclaude.cli.install_hooks._get_hooks_source` so
    the adapter and the installer agree on which file is the source of
    truth. Imported via the public ``install_hooks`` to avoid coupling
    on a private helper that may move.
    """

    # ``hook_adapter.py`` lives at src/superclaude/cli/eval/hook_adapter.py.
    # Two parents up is the package root (src/superclaude/).
    package_root = Path(__file__).resolve().parent.parent.parent
    return package_root / "hooks" / "hooks.json"


def deploy_hooks_to(home_path: Path) -> None:
    """Deploy SuperClaude hooks into the per-eval HOME at ``home_path``.

    Two filesystem effects, in this order:

    1. :func:`install_hooks` is invoked with ``target_path`` resolved to
       ``<home_path>/.claude/settings.json``. This copies the hook
       scripts to ``<home_path>/.claude/hooks/`` and merges hook
       registrations into a fresh ``<home_path>/.claude/settings.json``.
    2. The source ``src/superclaude/hooks/hooks.json`` is copied
       verbatim to ``<home_path>/.claude/hooks.json`` (byte-identical
       via :func:`shutil.copy2`).

    Idempotent: re-invocation on the same ``home_path`` produces
    identical filesystem state. The installer skips already-deployed
    scripts and matcher-colliding registrations; the verbatim copy
    overwrites with the same bytes when the source is unchanged.

    Args:
        home_path: Per-eval HOME directory created by
            :class:`HomeIsolation.setup`. MUST NOT resolve to the real
            ``~/.claude/`` directory — the pre-flight guard rejects
            that case before any write happens.

    Raises:
        HookDeployFailed: Any of the failure modes documented on
            :class:`HookDeployFailed.error_tag`. Each failure mode
            carries enough detail (``home_path`` + ``detail``) for the
            orchestrator to bucket the eval and surface the underlying
            cause in operator-facing reports.
    """

    # Step 0 — defense-in-depth refusal. Must run BEFORE any write so
    # `install_hooks` never even materializes a directory under real
    # `~/.claude/`.
    _refuse_real_home(home_path)

    source_hooks_json = _source_hooks_json()
    if not source_hooks_json.exists():
        raise HookDeployFailed(
            error_tag="source-hooks-json-missing",
            home_path=home_path,
            detail=f"source hooks.json not found at {source_hooks_json!s}",
        )

    # Step 1 — delegate scripts + settings.json merge to install_hooks.
    settings_path = home_path.joinpath(*_SETTINGS_RELPATH)
    success, message = install_hooks(target_path=settings_path, force=False)
    if not success:
        raise HookDeployFailed(
            error_tag="install-hooks-failed",
            home_path=home_path,
            detail=message,
        )

    # Step 2 — verbatim hooks.json copy. Required by the AC: the
    # per-eval HOME must carry a SHA256-identical copy of the source
    # registrations so post-mortem inspection / FR-G* gate tests can
    # diff against the canonical file. Routed through the private
    # :func:`_copy_hooks_json_verbatim` helper so test patches against
    # ``shutil.copy2`` (a globally shared module attribute) cannot
    # accidentally also break ``install_hooks``'s own copy pipeline.
    dest_hooks_json = home_path.joinpath(*_HOOKS_JSON_RELPATH)
    try:
        dest_hooks_json.parent.mkdir(parents=True, exist_ok=True)
        _copy_hooks_json_verbatim(source_hooks_json, dest_hooks_json)
    except OSError as exc:
        raise HookDeployFailed(
            error_tag="hooks-json-copy-failed",
            home_path=home_path,
            detail=f"verbatim hooks.json copy from {source_hooks_json!s} "
            f"to {dest_hooks_json!s} failed: {exc}",
        ) from exc


def _copy_hooks_json_verbatim(src: Path, dest: Path) -> None:
    """Copy ``src`` to ``dest`` verbatim (byte-identical, preserving mtime).

    Wraps :func:`shutil.copy2` so the adapter's verbatim copy site is
    a dedicated, monkeypatch-friendly seam. Tests targeting the
    ``hooks-json-copy-failed`` error tag patch this function instead
    of the shared ``shutil.copy2`` global, which would also break
    :func:`install_hooks` (it copies hook scripts through the same
    ``shutil.copy2`` API).
    """

    shutil.copy2(src, dest)
