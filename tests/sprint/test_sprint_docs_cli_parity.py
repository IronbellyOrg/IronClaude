"""Doc⇆CLI parity guard for ``superclaude sprint run``.

Why this exists: PR #160 shipped five review comments that all reduced to the
same root cause — docs asserting CLI facts (which flags exist, what their
defaults are) that had drifted from the Click command. Prose drifts silently;
this test makes those facts *executably verified*. The **Click command is the
single source of truth**; the sprint CLI guide must match it.

Adaptation vs the reflect template (``tests/cli/reflect/test_docs_cli_parity.py``):

* This file lives at ``tests/sprint/<file>`` → ``parents[2]`` is the repo root
  (the reflect template is one level deeper at ``tests/cli/reflect/`` →
  ``parents[3]``).
* The sprint ``run`` guide curates its ``### Key options`` to the day-to-day
  operator surface and intentionally omits advanced/operational and internal
  plumbing flags (and hidden flags never appear in ``--help`` at all). Those are
  enumerated in :data:`_UNDOCUMENTED_BY_DESIGN` so the ``missing`` assertion
  still REQUIRES any operator-facing flag — notably the 429-recovery
  ``--max-session-resets`` — to be documented, while not forcing the guide to
  grow an entry for every internal tuning knob. The ``phantom`` direction stays
  strict: the guide may never document a flag that does not exist.
"""

from __future__ import annotations

import re
from pathlib import Path

import click

from superclaude.cli.sprint.commands import run

# tests/sprint/<file>  ->  parents[2] == repo root
_GUIDE_PATH = (
    Path(__file__).resolve().parents[2]
    / "docs"
    / "guides"
    / "sprint-cli-tools-release-guide.md"
)
_FLAG_RE = re.compile(r"--[a-z][a-z0-9-]*")
_OPTION_BULLET_RE = re.compile(r"^\s*-\s+`--")  # an option-definition bullet line

# Visible ``run`` flags the guide's curated "Key options" intentionally omits:
# advanced/operational tuning + internal plumbing not part of the day-to-day
# operator surface. Explicit so a NEW operator-facing flag (e.g.
# ``--max-session-resets``) is still required to be documented by the missing
# assertion below.
_UNDOCUMENTED_BY_DESIGN = {
    "--debug",
    "--force-fidelity",
    "--handoff",
    "--no-handoff",
    "--release-dir",
    "--resume",
    "--shadow-gates",
    "--stall-action",
    "--stall-timeout",
    "--startup-stall-timeout",
    "--state-dir",
    "--task-parallelism",
}


def _cli_long_flags(*, include_hidden: bool) -> set[str]:
    """Every ``--long`` flag the Click ``run`` command exposes (excluding ``--help``).

    ``include_hidden=False`` drops hidden options (e.g. ``--tmux-session-name``)
    which never appear in ``--help`` and are not part of the documented surface.
    """
    flags: set[str] = set()
    for param in run.params:
        if not isinstance(param, click.Option):
            continue
        if not include_hidden and getattr(param, "hidden", False):
            continue
        for opt in (*param.opts, *param.secondary_opts):
            if opt.startswith("--") and opt != "--help":
                flags.add(opt)
    return flags


def _option(name: str) -> click.Option:
    for param in run.params:
        if isinstance(param, click.Option) and param.name == name:
            return param
    raise AssertionError(f"no such sprint-run option: {name!r}")


def _guide_text() -> str:
    return _GUIDE_PATH.read_text(encoding="utf-8")


def _key_options_section() -> str:
    """The ``### Key options`` block only — bounded by the next ``##``/``###`` heading."""
    text = _guide_text()
    marker = "### Key options"
    assert marker in text, f"guide is missing the '{marker}' section"
    rest = text[text.index(marker) + len(marker) :]
    nxt = re.search(r"\n#{2,3} ", rest)
    return rest[: nxt.start()] if nxt else rest


def _documented_flags() -> set[str]:
    """Flags named in the guide's option-definition bullets (ignores prose)."""
    flags: set[str] = set()
    for line in _key_options_section().splitlines():
        if _OPTION_BULLET_RE.match(line):
            flags.update(_FLAG_RE.findall(line))
    return flags


def test_documented_flags_match_cli_flags() -> None:
    """Guide option bullets must be drift-free against the Click flag surface.

    phantom (documented but non-existent) is forbidden outright; missing
    (operator-facing CLI flag absent from the guide) is forbidden EXCEPT for the
    advanced/internal flags the guide intentionally curates out.
    """
    documented = _documented_flags()
    phantom = documented - _cli_long_flags(include_hidden=True)
    assert not phantom, f"guide documents non-existent CLI flags: {sorted(phantom)}"

    expected = _cli_long_flags(include_hidden=False) - _UNDOCUMENTED_BY_DESIGN
    missing = expected - documented
    assert not missing, (
        f"operator-facing CLI flags absent from the guide's Key options: "
        f"{sorted(missing)}"
    )


def test_documented_defaults_match_cli_defaults() -> None:
    """The guide's stated ``Default:`` for ``--max-session-resets`` must match Click.

    The Click default is the source of truth (spec §7 P5: default 8). This fails
    if the guide states a different default or drops the entry entirely.
    """
    opt = _option("max_session_resets")
    assert opt.default == 8
    assert f"Default: `{opt.default}`" in _guide_text(), (
        f"--max-session-resets Click default={opt.default!r} is not stated as "
        f"Default: `{opt.default}` in the guide"
    )
