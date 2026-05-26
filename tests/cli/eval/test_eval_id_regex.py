"""Tests for ``superclaude.cli.eval.loader.validate_eval_id`` (FR-SCH2).

Covers cliEval Phase 1 / Task T01.05 acceptance criteria (Deliverable D-0005,
FR-SCH2). The function is the security-critical eval-id guard applied
pre-FS-write and again post-parameterize-expansion (per Validation-Order
decision). It MUST raise :class:`InvalidEvalId` for anything that does not
match ``^[A-Z][A-Za-z0-9]*([0-9]+(\\.[0-9]+)?)?$``.

This file owns the *unit* surface of FR-SCH2 (the function contract);
``tests/cli/eval/test_path_traversal.py`` (T01.08 / NFR-SEC1) is the
dedicated negative-case test set that cross-links here and to TEST-001
(T01.23).

Cross-links:
* FR-SCH2 (this task, T01.05)
* DM-011 ``evalIdString`` regex (T01.02 — same regex enforced at schema layer)
* COMP-002 SuiteLoader orchestration (T01.07 — applies guard at entry
  and again after parameterize expansion)
* NFR-SEC1 path-traversal prevention test set (T01.08)
* TEST-001 schema + ID rejection tests (T01.23)
"""

from __future__ import annotations

import pytest

from superclaude.cli.eval import (
    INVALID_EVAL_ID_EXIT_CODE,
    InvalidEvalId,
    validate_eval_id,
)
from superclaude.cli.eval.loader import EVAL_ID_REGEX

# --- regex sanity ----------------------------------------------------------


def test_eval_id_regex_is_compiled_pattern() -> None:
    """Compiled regex avoids re-parsing on every call (loader hot path)."""

    import re

    assert isinstance(EVAL_ID_REGEX, re.Pattern)
    # Single source of truth: FR-SCH2 regex literal must match design-spec.
    assert EVAL_ID_REGEX.pattern == r"^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$"


# --- positive cases (must NOT raise) ---------------------------------------


@pytest.mark.parametrize(
    "eval_id",
    [
        "E1",        # canonical eval id (design-spec example)
        "E2",
        "E15",
        "E2.1",      # parameterize-expanded id (design-spec example)
        "E2.10",
        "D15",       # design-spec example
        "A",         # minimum-length: single uppercase letter
        "Z9",
        "Test1",     # mixed-case body is allowed by the regex
        "ABC123",
        "E0.0",
        "Foo42.7",
    ],
)
def test_validate_eval_id_accepts_well_formed_ids(eval_id: str) -> None:
    # validate_eval_id is a guard (returns None on success); the contract is
    # "raises InvalidEvalId on bad input", so a no-exception call passes.
    validate_eval_id(eval_id)


# --- negative cases (MUST raise InvalidEvalId) -----------------------------
# Acceptance criteria (T01.05): rejects ../home, /etc, .., empty, leading-
# digit IDs, and template tokens inside id.


@pytest.mark.parametrize(
    "eval_id",
    [
        "../home",         # AC: path-traversal prefix
        "../../etc",       # deeper traversal
        "/etc",            # AC: absolute-path leak
        "/tmp/eval-runs",  # absolute path matching scratch allowlist
        "..",              # AC: bare traversal
        ".",               # bare current-dir
        "./foo",           # relative-with-dot
        "foo/bar",         # embedded slash
        "foo\\bar",        # embedded backslash (Windows-style)
        "E1/x",            # otherwise-valid prefix with slash suffix
        "E1\x00",          # NUL terminator (defence in depth)
        "E1\n",            # trailing newline (re.fullmatch-equivalent guard)
        "E 1",             # whitespace
        " E1",
        "E1 ",
        "\tE1",
    ],
)
def test_validate_eval_id_rejects_traversal_and_separator_patterns(
    eval_id: str,
) -> None:
    with pytest.raises(InvalidEvalId):
        validate_eval_id(eval_id)


def test_validate_eval_id_rejects_empty_string() -> None:
    # AC: empty string is one of the named rejection cases.
    with pytest.raises(InvalidEvalId):
        validate_eval_id("")


@pytest.mark.parametrize(
    "eval_id",
    [
        "1E",
        "9",
        "0E",
        "2E1",
        "1",
        "12.3",
    ],
)
def test_validate_eval_id_rejects_leading_digit_ids(eval_id: str) -> None:
    # AC: leading-digit IDs are rejected (regex anchors to ``[A-Z]``).
    with pytest.raises(InvalidEvalId):
        validate_eval_id(eval_id)


@pytest.mark.parametrize(
    "eval_id",
    [
        "{{prefix}}",         # AC: template tokens inside id
        "E{{p}}",             # partial template residue
        "E1{{n}}",
        "{prefix}",           # single-brace template (Click-style)
        "${var}",             # shell variable expansion
        "$var",
        "%name%",             # cmd-style variable
        "<id>",               # XML-ish placeholder
    ],
)
def test_validate_eval_id_rejects_template_token_patterns(eval_id: str) -> None:
    with pytest.raises(InvalidEvalId):
        validate_eval_id(eval_id)


@pytest.mark.parametrize(
    "eval_id",
    [
        "e1",           # lowercase start (regex anchors to [A-Z])
        "eval1",
        "E-1",          # hyphen not in [A-Za-z0-9]
        "E_1",          # underscore not in [A-Za-z0-9]
        "E1.",          # trailing dot with no digit suffix
        "E.1",          # dot must follow a digit run
        "E1.1.1",       # only one ".N" decimal allowed
        "E1..1",
        "E1.1.",
    ],
)
def test_validate_eval_id_rejects_misc_malformed_ids(eval_id: str) -> None:
    with pytest.raises(InvalidEvalId):
        validate_eval_id(eval_id)


# --- non-string input ------------------------------------------------------


@pytest.mark.parametrize("bad_input", [None, 1, 1.0, b"E1", ["E1"], {"id": "E1"}, ()])
def test_validate_eval_id_rejects_non_string_input(bad_input) -> None:
    # Defence in depth: the YAML loader can produce non-string scalars; the
    # guard must not accidentally accept them via duck-typing. Any non-str
    # input raises InvalidEvalId (callers must not have to pre-coerce).
    with pytest.raises(InvalidEvalId):
        validate_eval_id(bad_input)  # type: ignore[arg-type]


# --- error surface ---------------------------------------------------------


def test_invalid_eval_id_carries_offending_value() -> None:
    bad = "../home"
    with pytest.raises(InvalidEvalId) as excinfo:
        validate_eval_id(bad)
    err = excinfo.value
    # The message must name the offending value so reporters can render it.
    assert bad in str(err)
    # And expose it programmatically so downstream callers can branch on it.
    assert err.eval_id == bad


def test_invalid_eval_id_exit_code_is_two() -> None:
    # Single source of truth for the CLI mapping; design-spec §4 exit-code
    # table reserves ``2`` for "Harness error (manifest invalid, ...)".
    assert INVALID_EVAL_ID_EXIT_CODE == 2


def test_invalid_eval_id_is_exception_subclass() -> None:
    # Callers may catch (SchemaError, InvalidEvalId) so the latter must be
    # a normal Exception (not BaseException).
    assert issubclass(InvalidEvalId, Exception)


# --- post-parameterize-expansion semantics ---------------------------------
# Acceptance criteria (T01.05): "Guard is applied at SuiteLoader entry AND
# after parameterize expansion (verified by integration test that simulates
# expansion producing an unsafe id)." The SuiteLoader wiring lands in
# T01.07; here we exercise the *function* with simulated post-expansion
# values so the unit guarantee is in place before the orchestrator builds
# on it.


def test_validate_eval_id_rejects_unsafe_expanded_id() -> None:
    # Simulate parameterize expansion producing an unsafe id (e.g., a
    # template token leaked through unsubstituted).
    base = "E2"
    template_suffix = "{{prefix}}"
    expanded = f"{base}.{template_suffix}"  # "E2.{{prefix}}"
    with pytest.raises(InvalidEvalId):
        validate_eval_id(expanded)


def test_validate_eval_id_accepts_safe_expanded_id() -> None:
    # Parameterize expansion convention: base + "." + index (e.g. E2.1,
    # E2.2). All such ids must pass the guard.
    for index in range(1, 11):
        validate_eval_id(f"E2.{index}")


def test_validate_eval_id_rejects_traversal_after_substitution() -> None:
    # Defence in depth: if a parameterize substitution accidentally
    # contained a traversal payload, the post-expansion id must be
    # rejected before any FS write.
    payload = "../../../etc/passwd"
    expanded = f"E2.{payload}"
    with pytest.raises(InvalidEvalId):
        validate_eval_id(expanded)


# --- CC1 single-source-of-truth contract (OQ-1 synthesis) ------------------


def test_eval_id_pattern_single_source() -> None:
    """CC1 — EVAL_ID_PATTERN is the FR-SCH2 schema SoT in artifact_layout.py;
    loader.EVAL_ID_REGEX is an import alias for backward-compat.
    _EVAL_ID_PATH_SAFETY_PATTERN is a separate defense-in-depth layer — the
    two regexes are intentionally distinct.
    """

    from superclaude.cli.eval.artifact_layout import (
        _EVAL_ID_PATH_SAFETY_PATTERN,
        EVAL_ID_PATTERN,
    )

    # (1) Schema SoT — loader's alias IS the same compiled object (proves
    # the import-redirect, not a copy).
    assert EVAL_ID_REGEX is EVAL_ID_PATTERN

    # (2) Defense-in-depth separation — schema and path-safety are distinct
    # compiled objects, deliberately.
    assert _EVAL_ID_PATH_SAFETY_PATTERN is not EVAL_ID_PATTERN

    # (3) Semantic invariants — strict schema rejects lowercase/underscore;
    # path-safety accepts permissive ids but rejects traversal.
    assert EVAL_ID_PATTERN.match("T01.13") is not None
    assert EVAL_ID_PATTERN.match("my_eval") is None
    assert _EVAL_ID_PATH_SAFETY_PATTERN.match("my_eval-1.0") is not None
    assert _EVAL_ID_PATH_SAFETY_PATTERN.match("../etc/passwd") is None
