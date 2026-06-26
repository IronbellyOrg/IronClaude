"""Doc⇆CLI parity guard for ``superclaude reflect run``.

Why this exists: PR #160 shipped five review comments that all reduced to the
same root cause — the docs asserted CLI facts (which flags exist, what their
defaults are) that had drifted from ``src/superclaude/cli/reflect/commands.py``.
Prose can drift silently; this test makes those facts *executably verified*. The
**Click command is the single source of truth**; the reflect CLI guide must match
it. Specifically this would have caught:

* a documented flag that does not exist (e.g. ``--executor-model``), and
* a documented default that disagrees with the Click default (e.g. ``--fix``).

The guide path is resolved relative to the repo root so the test is CWD-agnostic.
"""

from __future__ import annotations

import re
from pathlib import Path

import click

from superclaude.cli.reflect.commands import run

# tests/cli/reflect/<file>  ->  parents[3] == repo root
_GUIDE_PATH = (
    Path(__file__).resolve().parents[3]
    / "docs"
    / "guides"
    / "reflect-cli-tools-guide.md"
)
_FLAG_RE = re.compile(r"--[a-z][a-z0-9-]*")
_OPTION_BULLET_RE = re.compile(r"^\s*-\s+`--")  # an option-definition bullet line


def _cli_long_flags() -> set[str]:
    """Every ``--long`` flag the Click ``run`` command exposes (excluding ``--help``)."""
    flags: set[str] = set()
    for param in run.params:
        if not isinstance(param, click.Option):
            continue
        for opt in (*param.opts, *param.secondary_opts):
            if opt.startswith("--") and opt != "--help":
                flags.add(opt)
    return flags


def _option(name: str) -> click.Option:
    for param in run.params:
        if isinstance(param, click.Option) and param.name == name:
            return param
    raise AssertionError(f"no such reflect-run option: {name!r}")


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
    """Flags named in the guide's option-definition bullets (ignores prose / blockquotes).

    Scanning only bullet lines that start with ``- `--`` deliberately skips the
    blockquote note explaining that ``--executor-model`` is *not* a flag, so that
    note never registers as a documented flag.
    """
    flags: set[str] = set()
    for line in _key_options_section().splitlines():
        if _OPTION_BULLET_RE.match(line):
            flags.update(_FLAG_RE.findall(line))
    return flags


def test_documented_flags_match_cli_flags() -> None:
    """Guide option bullets and the Click flag surface must be the same set."""
    cli = _cli_long_flags()
    documented = _documented_flags()
    phantom = documented - cli  # documented but not real (the --executor-model class)
    missing = cli - documented  # real but undocumented
    assert not phantom, f"guide documents non-existent CLI flags: {sorted(phantom)}"
    assert not missing, (
        f"CLI flags absent from the guide's Key options: {sorted(missing)}"
    )


def test_documented_defaults_match_cli_defaults() -> None:
    """The guide's stated ``Default:`` must be derivable from the Click default.

    Covers the flags whose Click default *is* the source of truth. ``--timeout``
    and ``--output`` are intentionally excluded: their effective defaults (3600,
    the ``<task-dir>/reflect/post/<short-sha>/`` template) are applied downstream
    in ``config.py``, not as the Click default.
    """
    guide = _guide_text()

    # Boolean flag-pairs: the documented default is the *active* side.
    for opt_name in ("fix", "promote", "reachability"):
        opt = _option(opt_name)
        active = opt.opts[0] if opt.default else opt.secondary_opts[0]
        assert f"Default: `{active}`" in guide, (
            f"--{opt_name} Click default={opt.default!r} but the guide does not "
            f"state Default: `{active}`"
        )

    # Value options: the documented default is the literal value.
    for opt_name in ("max_fix_iterations", "depth"):
        value = _option(opt_name).default
        assert f"Default: `{value}`" in guide, (
            f"--{opt_name.replace('_', '-')} Click default={value!r} is not stated "
            f"as Default: `{value}` in the guide"
        )
