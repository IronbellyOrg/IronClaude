"""Tests for the DM-006 ``HomeIsolation`` frozen dataclass (Task T02.04).

Owns the unit surface of the four-field record:

* ``eval_id: str``           — re-validated via FR-SCH2 :func:`validate_eval_id`
* ``home_root: Path``        — scratch root path stored verbatim
* ``session_id: str``        — value for ``CLAUDE_SESSION_ID`` env stamp
* ``time_offset_sec: int=0`` — optional simulated wall-clock offset

Cross-links:

* DM-006 (roadmap row 26) — the field contract this file enforces.
* COMP-006 ``HomeIsolation`` extension (T02.07/T02.11) — consumer site.
* FR-SCH2 :func:`validate_eval_id` (T01.05) — the validator this dataclass
  re-applies in ``__post_init__``.
* DOC-OQ8 (T06.03) — gates ``CLAUDE_FAKE_TIME_OFFSET`` semantics; the
  dataclass keeps the field regardless so the record contract is stable.
"""

from __future__ import annotations

import dataclasses
from pathlib import Path

import pytest

from superclaude.cli.eval import HomeIsolation, InvalidEvalId


def _build(**overrides) -> HomeIsolation:
    """Helper: build a HomeIsolation with defaults, allowing per-test overrides."""

    defaults: dict[str, object] = {
        "eval_id": "E1",
        "home_root": Path("/tmp/eval-runs"),
        "session_id": "sess-001",
    }
    defaults.update(overrides)
    return HomeIsolation(**defaults)  # type: ignore[arg-type]


# --- field contract --------------------------------------------------------


def test_home_isolation_has_four_fields() -> None:
    """DM-006 names exactly four fields; field order must match the spec."""

    field_names = tuple(f.name for f in dataclasses.fields(HomeIsolation))
    assert field_names == ("eval_id", "home_root", "session_id", "time_offset_sec")


def test_home_isolation_field_types() -> None:
    """Annotations match DM-006: str / Path / str / int."""

    annotations = {f.name: f.type for f in dataclasses.fields(HomeIsolation)}
    assert annotations["eval_id"] == "str"
    assert annotations["home_root"] == "Path"
    assert annotations["session_id"] == "str"
    assert annotations["time_offset_sec"] == "int"


def test_home_isolation_default_time_offset_is_zero() -> None:
    """DM-006 specifies ``time_offset_sec:int=0``; the default must match."""

    record = _build()
    assert record.time_offset_sec == 0


def test_home_isolation_accepts_explicit_time_offset() -> None:
    """Caller-supplied offsets must round-trip unchanged."""

    record = _build(time_offset_sec=42)
    assert record.time_offset_sec == 42


def test_home_isolation_stores_home_root_verbatim() -> None:
    """home_root is stored as-is; containment is FR-ISO2's responsibility."""

    path = Path("/tmp/eval-runs/run-abc/E1")
    record = _build(home_root=path)
    assert record.home_root == path
    # Identity isn't required, but no path manipulation must happen at construction time.
    assert isinstance(record.home_root, Path)


# --- frozen invariant ------------------------------------------------------


@pytest.mark.parametrize(
    "field_name,value",
    [
        ("eval_id", "E2"),
        ("home_root", Path("/tmp/other")),
        ("session_id", "sess-002"),
        ("time_offset_sec", 7),
    ],
)
def test_home_isolation_is_frozen(field_name: str, value: object) -> None:
    """Mutation of any field must raise FrozenInstanceError."""

    record = _build()
    with pytest.raises(dataclasses.FrozenInstanceError):
        setattr(record, field_name, value)


def test_home_isolation_is_hashable() -> None:
    """frozen dataclasses are hashable, which makes them safe as dict keys
    inside the orchestrator's per-eval bookkeeping."""

    record = _build()
    assert hash(record) == hash(_build())


# --- FR-SCH2 re-validation in __post_init__ --------------------------------


@pytest.mark.parametrize(
    "bad_id",
    [
        "../home",
        "/etc",
        "..",
        "",
        "1E",  # leading digit
        "e1",  # lowercase start
        "E1/x",
        "E1\x00",
        "{{prefix}}",
        "E-1",
        "E_1",
    ],
)
def test_home_isolation_rejects_unsafe_eval_id(bad_id: str) -> None:
    """Construction with an unsafe eval_id must raise ``InvalidEvalId``."""

    with pytest.raises(InvalidEvalId):
        _build(eval_id=bad_id)


@pytest.mark.parametrize("eval_id", ["E1", "E2.1", "D15", "A", "Test1", "ABC123"])
def test_home_isolation_accepts_valid_eval_ids(eval_id: str) -> None:
    """All FR-SCH2-valid ids must construct cleanly."""

    record = _build(eval_id=eval_id)
    assert record.eval_id == eval_id


def test_home_isolation_rejects_non_string_eval_id() -> None:
    """validate_eval_id rejects non-strings; the dataclass inherits that."""

    with pytest.raises(InvalidEvalId):
        _build(eval_id=1)  # type: ignore[arg-type]


def test_home_isolation_rejects_post_expansion_unsafe_id() -> None:
    """Parameterize expansion can leak an unsubstituted template token; the
    record must reject the resulting id even though it looks plausible."""

    with pytest.raises(InvalidEvalId):
        _build(eval_id="E2.{{prefix}}")


# --- structural equality ---------------------------------------------------


def test_home_isolation_equal_when_fields_match() -> None:
    """Structural equality across all four fields (dataclass __eq__)."""

    assert _build() == _build()


def test_home_isolation_unequal_when_field_differs() -> None:
    assert _build() != _build(session_id="sess-002")
    assert _build() != _build(time_offset_sec=1)
    assert _build() != _build(home_root=Path("/tmp/other"))
    assert _build() != _build(eval_id="E2")


# --- package re-export -----------------------------------------------------


def test_home_isolation_importable_from_package() -> None:
    """``from superclaude.cli.eval import HomeIsolation`` must work."""

    import superclaude.cli.eval as pkg

    assert pkg.HomeIsolation is HomeIsolation
    assert "HomeIsolation" in pkg.__all__
