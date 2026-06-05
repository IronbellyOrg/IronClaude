"""T02.22 / FR-024 -- ``--auto-inject-guard`` flag tests.

Pins the acceptance criteria for the backward-compat opt-in that lets
legacy ``--custom-prompt-dir`` users migrate without an immediate hard
preflight failure:

1. :func:`preflight.auto_inject_guard` prepends the canonical §11.5
   sentence to a ``system`` string when the sentence is absent, and is
   a no-op when the sentence is already present (idempotent).
2. :func:`preflight.read_custom_prompt_dir` accepts an
   ``auto_inject_guard`` keyword. When set ``True`` and the
   ``system.txt`` lacks the canonical sentence, the reader auto-injects
   the sentence and the §11.5 substring check passes. When the flag is
   absent (default ``False``), the same fixture produces the
   :data:`preflight.RULE_INJECTION_GUARD` failure -- the absent-flag
   path **preserves** §11.5 enforcement with no silent bypass.
3. :data:`commands.auto_inject_guard_option` is a Click decorator that
   binds the operator-facing ``--auto-inject-guard`` flag to a
   ``auto_inject_guard: bool`` keyword on any subcommand it decorates.
   The flag defaults to ``False`` and is parsed as ``True`` when
   present.

The fixture pattern follows ``tests/swarm/test_custom_prompt_dir.py``
so the existing ``_write_three_files`` shape carries over and the
diagnostic surface stays uniform across the FR-021 / FR-024 test
modules.
"""

from __future__ import annotations

from pathlib import Path

import click
import pytest
from click.testing import CliRunner

from superclaude.cli.swarm.commands import auto_inject_guard_option
from superclaude.cli.swarm.preflight import (
    RULE_INJECTION_GUARD,
    PreflightError,
    auto_inject_guard,
    read_custom_prompt_dir,
)
from superclaude.cli.swarm.schema import CANONICAL_INJECTION_GUARD_SENTENCE

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


_LEGACY_SYSTEM_TXT: str = (
    "You are a careful reviewer. Inspect the target and report findings."
)
"""Legacy ``system.txt`` body without §11.5 framing.

Mirrors the typical pre-FR-024 prompt: useful reviewer instructions,
but no canonical §11.5 sentence. The auto-inject-guard flag exists to
let migrators land this exact content unchanged while preflight stamps
the canonical sentence on top.
"""


def _write_three_files(
    base: Path,
    *,
    system: str = _LEGACY_SYSTEM_TXT,
    user: str = "Review: {{target}}",
    meta: str = "variables:\n  audience: senior\n",
) -> None:
    """Write the FR-021 three-file bundle into ``base``.

    Mirrors the helper in ``test_custom_prompt_dir.py``; duplicated
    here (rather than imported) so the FR-024 module's failure
    diagnostics are isolated from any future refactor of the FR-021
    test helpers.
    """
    (base / "system.txt").write_text(system, encoding="utf-8")
    (base / "user.txt").write_text(user, encoding="utf-8")
    (base / "meta.yaml").write_text(meta, encoding="utf-8")


# ---------------------------------------------------------------------------
# :func:`preflight.auto_inject_guard` helper
# ---------------------------------------------------------------------------


def test_auto_inject_guard_prepends_canonical_when_missing() -> None:
    """Legacy system.txt + helper → canonical sentence sits at the top."""
    result = auto_inject_guard(_LEGACY_SYSTEM_TXT)

    assert result.startswith(CANONICAL_INJECTION_GUARD_SENTENCE)
    assert _LEGACY_SYSTEM_TXT in result
    # Result is canonical + separator + legacy; the legacy body is
    # preserved verbatim so callers see no normalisation.
    assert result.endswith(_LEGACY_SYSTEM_TXT)


def test_auto_inject_guard_idempotent_when_already_present() -> None:
    """Helper is a no-op when the canonical sentence is already present."""
    already = "Intro. " + CANONICAL_INJECTION_GUARD_SENTENCE + " Outro."

    assert auto_inject_guard(already) == already


def test_auto_inject_guard_idempotent_on_repeated_calls() -> None:
    """Calling the helper twice does not double-prepend."""
    once = auto_inject_guard(_LEGACY_SYSTEM_TXT)
    twice = auto_inject_guard(once)

    assert once == twice
    # Only one occurrence of the canonical sentence survives the two
    # passes -- the property the substring check downstream relies on.
    assert twice.count(CANONICAL_INJECTION_GUARD_SENTENCE) == 1


def test_auto_inject_guard_empty_system_yields_canonical_only() -> None:
    """Empty input produces just the canonical sentence (no stray whitespace)."""
    assert auto_inject_guard("") == CANONICAL_INJECTION_GUARD_SENTENCE


def test_auto_inject_guard_custom_canonical_sentence() -> None:
    """The ``canonical_sentence`` kwarg overrides the default for tests."""
    custom = "CUSTOM-SENTINEL"

    result = auto_inject_guard(_LEGACY_SYSTEM_TXT, canonical_sentence=custom)

    assert result.startswith(custom)
    assert result.endswith(_LEGACY_SYSTEM_TXT)


def test_auto_inject_guard_empty_sentence_is_passthrough() -> None:
    """Empty ``canonical_sentence`` disables the helper (returns input)."""
    assert auto_inject_guard(_LEGACY_SYSTEM_TXT, canonical_sentence="") == (
        _LEGACY_SYSTEM_TXT
    )


def test_auto_inject_guard_separator_is_blank_line() -> None:
    """Default insertion places a blank line between sentence and legacy body.

    The separator is ``\\n\\n`` so a downstream LLM reader sees the
    canonical framing as its own paragraph above the legacy prompt;
    eyeballing the rendered prompt during migration should not show a
    cramped wall-of-text.
    """
    result = auto_inject_guard(_LEGACY_SYSTEM_TXT)

    separator = CANONICAL_INJECTION_GUARD_SENTENCE + "\n\n"
    assert result.startswith(separator)


# ---------------------------------------------------------------------------
# :func:`preflight.read_custom_prompt_dir` integration (flag-on / flag-off)
# ---------------------------------------------------------------------------


def test_read_custom_prompt_dir_flag_off_rejects_legacy(tmp_path: Path) -> None:
    """Default ``auto_inject_guard=False`` preserves §11.5 enforcement.

    Acceptance criterion: "Absent flag preserves §11.5 required-substring
    enforcement (no silent bypass)." Legacy ``system.txt`` (no canonical
    sentence) → :data:`RULE_INJECTION_GUARD` failure.
    """
    _write_three_files(tmp_path)

    with pytest.raises(PreflightError) as excinfo:
        read_custom_prompt_dir(
            tmp_path,
            required_substring=CANONICAL_INJECTION_GUARD_SENTENCE,
        )

    failures = excinfo.value.failures
    assert len(failures) == 1
    assert failures[0].rule == RULE_INJECTION_GUARD
    assert failures[0].path == "custom_prompt_dir/system.txt"


def test_read_custom_prompt_dir_flag_off_default_argument(tmp_path: Path) -> None:
    """Omitting the kwarg behaves identically to ``auto_inject_guard=False``.

    Defensive check: a refactor that changed the default to ``True``
    would silently bypass §11.5 enforcement on every existing call site.
    This test pins the default.
    """
    _write_three_files(tmp_path)

    with pytest.raises(PreflightError) as excinfo:
        # No ``auto_inject_guard`` kwarg passed at all.
        read_custom_prompt_dir(
            tmp_path,
            required_substring=CANONICAL_INJECTION_GUARD_SENTENCE,
        )

    assert any(
        f.rule == RULE_INJECTION_GUARD for f in excinfo.value.failures
    )


def test_read_custom_prompt_dir_flag_on_injects_and_passes(
    tmp_path: Path,
) -> None:
    """``auto_inject_guard=True`` → canonical sentence prepended; check passes.

    Acceptance criterion: "``--auto-inject-guard`` flag prepends
    canonical §11.5 sentence on custom-prompt-dir path." The
    substring check sees the injected sentence and the reader returns
    the trio without raising.
    """
    _write_three_files(tmp_path)

    system, user, meta = read_custom_prompt_dir(
        tmp_path,
        required_substring=CANONICAL_INJECTION_GUARD_SENTENCE,
        auto_inject_guard=True,
    )

    # Canonical sentence is now visible at the top of the returned
    # ``system`` payload -- the substring check above passed because
    # the helper injected it.
    assert system.startswith(CANONICAL_INJECTION_GUARD_SENTENCE)
    # Original legacy body is preserved verbatim below the canonical
    # sentence -- migration users see their existing prompt unchanged.
    assert _LEGACY_SYSTEM_TXT in system
    # Other two files round-trip identically regardless of the flag.
    assert user == "Review: {{target}}"
    assert meta == {"variables": {"audience": "senior"}}


def test_read_custom_prompt_dir_flag_on_idempotent_when_compliant(
    tmp_path: Path,
) -> None:
    """``auto_inject_guard=True`` is a no-op when system.txt already complies.

    A migrator who has already added the canonical sentence should not
    see a duplicate prepended on top of their existing one.
    """
    compliant_system = (
        "Intro. " + CANONICAL_INJECTION_GUARD_SENTENCE + " Continue reviewing."
    )
    _write_three_files(tmp_path, system=compliant_system)

    system, _, _ = read_custom_prompt_dir(
        tmp_path,
        required_substring=CANONICAL_INJECTION_GUARD_SENTENCE,
        auto_inject_guard=True,
    )

    # One occurrence -- no double prepend.
    assert system.count(CANONICAL_INJECTION_GUARD_SENTENCE) == 1
    # Body preserved verbatim -- the helper saw the sentence and
    # returned the input unchanged.
    assert system == compliant_system


def test_read_custom_prompt_dir_flag_on_with_empty_substring(
    tmp_path: Path,
) -> None:
    """Flag on + ``required_substring=""`` → no check fires, sentence still injected.

    The reader runs the helper before the substring check; an empty
    substring (guard disabled) is decoupled from the auto-inject
    decision so callers can use the flag as a pure
    "always-prepend-canonical" preprocessor when running outside the
    schema-enforced path.
    """
    _write_three_files(tmp_path)

    system, _, _ = read_custom_prompt_dir(
        tmp_path,
        # Default empty substring -> guard disabled.
        auto_inject_guard=True,
    )

    assert system.startswith(CANONICAL_INJECTION_GUARD_SENTENCE)


def test_read_custom_prompt_dir_flag_off_compliant_system_passes(
    tmp_path: Path,
) -> None:
    """Flag off + compliant ``system.txt`` → no failure, no transform.

    Pins the orthogonality: the flag's only job is the migration
    prepend. A caller who has already done the migration sees identical
    behavior with or without the flag.
    """
    compliant = "Intro. " + CANONICAL_INJECTION_GUARD_SENTENCE
    _write_three_files(tmp_path, system=compliant)

    system, _, _ = read_custom_prompt_dir(
        tmp_path,
        required_substring=CANONICAL_INJECTION_GUARD_SENTENCE,
        auto_inject_guard=False,
    )

    assert system == compliant


# ---------------------------------------------------------------------------
# :data:`commands.auto_inject_guard_option` Click decorator
# ---------------------------------------------------------------------------


def _build_test_command():
    """Build a throwaway Click command decorated with the FR-024 flag.

    Used by the option-parsing tests so the decorator's wiring is
    exercised end-to-end through Click's argument parser without
    coupling the tests to ``swarm run`` (still a T01.08 placeholder).
    """

    @click.command()
    @auto_inject_guard_option
    def cmd(auto_inject_guard: bool) -> None:  # pragma: no cover via runner
        click.echo(f"auto_inject_guard={auto_inject_guard}")

    return cmd


def test_auto_inject_guard_option_default_is_false() -> None:
    """Absent flag → bound kwarg is ``False``."""
    runner = CliRunner()
    result = runner.invoke(_build_test_command(), [])

    assert result.exit_code == 0
    assert "auto_inject_guard=False" in result.output


def test_auto_inject_guard_option_present_binds_true() -> None:
    """``--auto-inject-guard`` flips the bound kwarg to ``True``."""
    runner = CliRunner()
    result = runner.invoke(_build_test_command(), ["--auto-inject-guard"])

    assert result.exit_code == 0
    assert "auto_inject_guard=True" in result.output


def test_auto_inject_guard_option_kwarg_name_lines_up_with_reader() -> None:
    """Click option destination matches :func:`read_custom_prompt_dir` kwarg.

    The option binds to ``auto_inject_guard`` (snake-case) so a
    subcommand can thread the bound value straight into
    ``read_custom_prompt_dir(..., auto_inject_guard=auto_inject_guard)``
    without a rename step. Verifies the decorator's parameter name was
    not accidentally renamed during refactors.
    """
    cmd = _build_test_command()

    # ``cmd.params`` is the list of Click parameter records.
    flag_param = next(
        p for p in cmd.params if isinstance(p, click.Option)
        and "--auto-inject-guard" in p.opts
    )

    assert flag_param.name == "auto_inject_guard"
    assert flag_param.is_flag is True
    assert flag_param.default is False


def test_auto_inject_guard_option_help_documents_migration() -> None:
    """``--help`` text mentions the migration / backward-compat use case.

    Operator discoverability: a user running ``swarm run --help`` should
    learn from the flag's help text that it exists for the §11.5
    custom-prompt-dir migration, not for general per-invocation prompt
    munging.
    """
    runner = CliRunner()
    result = runner.invoke(_build_test_command(), ["--help"])

    assert result.exit_code == 0
    # Documents the FR-024 backward-compat scope.
    assert "FR-024" in result.output
    # Documents the §11.5 anchor.
    assert "§11.5" in result.output
