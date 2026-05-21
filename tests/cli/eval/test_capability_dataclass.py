"""Tests for ``superclaude.cli.eval.capabilities.Capability``.

Covers cliEval Phase 1 / Task T01.09 acceptance criteria (DM-007):

* Module exports a frozen ``Capability`` dataclass with fields
  ``name, check, failure_mode, skip_flag, description``.
* Mutation is rejected (frozen dataclass).
* ``failure_mode`` accepts ``"hard"``, ``"skip"``, ``"xfail"`` and rejects
  any other string with ``ValueError`` (via ``__post_init__``).
* Two instances built from the same arguments compare equal.
"""

from __future__ import annotations

import dataclasses

import pytest

from superclaude.cli.eval.capabilities import Capability


def _always_true() -> bool:  # module-level so equality across instances is stable
    return True


def test_capability_has_required_fields() -> None:
    field_names = {f.name for f in dataclasses.fields(Capability)}
    assert field_names == {
        "name",
        "check",
        "failure_mode",
        "skip_flag",
        "description",
    }


def test_capability_is_frozen() -> None:
    cap = Capability(name="binary.claude", check=_always_true, failure_mode="hard")
    with pytest.raises(dataclasses.FrozenInstanceError):
        cap.name = "binary.other"  # type: ignore[misc]


@pytest.mark.parametrize("mode", ["hard", "skip", "xfail"])
def test_capability_accepts_valid_failure_modes(mode: str) -> None:
    cap = Capability(name="x", check=_always_true, failure_mode=mode)  # type: ignore[arg-type]
    assert cap.failure_mode == mode


@pytest.mark.parametrize(
    "mode",
    ["", "HARD", "hard ", "soft", "invalid", "fail", "warn"],
)
def test_capability_rejects_invalid_failure_modes(mode: str) -> None:
    with pytest.raises(ValueError):
        Capability(name="x", check=_always_true, failure_mode=mode)  # type: ignore[arg-type]


def test_capability_optional_fields_default() -> None:
    cap = Capability(name="binary.git", check=_always_true, failure_mode="hard")
    assert cap.skip_flag is None
    assert cap.description == ""


def test_capability_deterministic_equality() -> None:
    a = Capability(
        name="mcp_server.auggie",
        check=_always_true,
        failure_mode="skip",
        skip_flag="--no-mcp",
        description="Auggie MCP server reachable via stdio",
    )
    b = Capability(
        name="mcp_server.auggie",
        check=_always_true,
        failure_mode="skip",
        skip_flag="--no-mcp",
        description="Auggie MCP server reachable via stdio",
    )
    assert a == b


def test_capability_unequal_when_field_differs() -> None:
    base = Capability(name="binary.claude", check=_always_true, failure_mode="hard")
    assert base != dataclasses.replace(base, name="binary.git")
    assert base != dataclasses.replace(base, failure_mode="skip")
    assert base != dataclasses.replace(base, skip_flag="--no-mcp")
    assert base != dataclasses.replace(base, description="something")


def test_capability_check_not_invoked_at_construction() -> None:
    invocations: list[int] = []

    def tracking_check() -> bool:
        invocations.append(1)
        return True

    Capability(name="x", check=tracking_check, failure_mode="hard")
    # Construction must not evaluate the check callable; COMP-009 evaluates it
    # later in check_all() (T01.11).
    assert invocations == []
