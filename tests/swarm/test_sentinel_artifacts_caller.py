"""T01.28 -- DM-017 DoneSentinel + DM-018 Artifacts + DM-019 CallerInfo.

Covers roadmap rows R-027 / R-028 / R-029 (DM-017, DM-018, DM-019 merged
per phase-1-tasklist.md T01.28). The three records are small accompanying
structs emitted together with the result contract at Wave 3 reduce
(COMP-009, M5), so the phase tasklist merges their landing into a single
STANDARD task -- this suite mirrors the merger and pins all three field
sets plus the CallerInfo.kind Literal in one place.

Per-record contract:

DM-017 DoneSentinel (3 fields)
    Terminal marker written atomically to ``done.json`` immediately
    after :class:`SwarmState.state` flips to ``terminal``. FR-029 /
    FR-014 require the sentinel so detached / tmux callers
    (``swarm attach`` / ``subprocess.run(...)`` per FR-030) can tell
    the job finished without polling.

    The roadmap row spells ``terminal_status`` as ``str``, but every
    legal value flows in from :class:`ResultContract.status` where the
    field is the :data:`ResultStatus` Literal. Carrying the Literal
    here too keeps the sentinel's type contract aligned with the
    contract it points at; this suite pins both that constraint and
    the out-of-enum guard.

DM-018 Artifacts (5 fields)
    Path-bundle struct embedded in :class:`ResultContract.artifacts`
    (DM-012) at Wave 3 reduce. Five absolute paths -- ``manifest.json``,
    ``.swarm-state.json``, ``event-log.jsonl``, ``event-log.md``,
    ``done.json`` -- one per on-disk artifact a job produces.

    Note ``done_sentinel`` is the *path* (``str``) to ``done.json``,
    not a :class:`DoneSentinel` instance -- matches the roadmap row's
    ``done_sentinel:str``.

DM-019 CallerInfo (4 fields)
    Identity block every job carries on :class:`JobSpec.caller` and
    every contract carries on :class:`ResultContract.caller`. FR-SPEC-002
    specifies the four fields; NFR-COMPAT-001 marks ``kind`` as
    informational only.

    Kind Literal :data:`CallerKind` admits exactly the three values
    from T01.28 acceptance: ``claude`` / ``cli`` / ``subprocess``.
    ``skill`` and ``skill_version`` are :data:`Optional[str]` because
    raw CLI / subprocess callers don't carry a registered skill identity.

This suite pins:

1. Every field listed in each roadmap row is present on its dataclass,
   in declaration order; no field drift.
2. Field types match the roadmap row exactly (including the Optional
   shapes for ``CallerInfo.skill`` / ``CallerInfo.skill_version`` and
   the Literal type on ``CallerInfo.kind`` / ``DoneSentinel.terminal_status``).
3. ``CallerKind`` admits exactly the values T01.28 acceptance names,
   and out-of-enum values raise ``ValueError`` at construction.
4. ``DoneSentinel.terminal_status`` reuses :data:`ResultStatus` so the
   sentinel and the contract it points at cannot drift.
5. JSON round-trip is lossless for default and populated instances of
   each record. CallerInfo populated round-trip exercises the Optional
   path (skill / skill_version both ``None`` and both set).
6. Defaults satisfy the no-arg construction contract so the
   aggregator's round-trip suite
   (``tests/swarm/test_models_round_trip.py``) keeps passing.

STANDARD-tier task per phase-1-tasklist.md T01.28.
"""

from __future__ import annotations

import dataclasses
import typing

import pytest

from superclaude.cli.swarm.models import (
    Artifacts,
    CallerInfo,
    CallerKind,
    DoneSentinel,
    ResultStatus,
    from_dict,
    from_json,
    to_dict,
    to_json,
)

# ---------------------------------------------------------------------------
# Expected field sets, drawn verbatim from the roadmap DM-### rows
# (.dev/releases/Current/MultiModelSwarm/roadmap.md L104-L106).
# ---------------------------------------------------------------------------


EXPECTED_DONE_SENTINEL_FIELDS: tuple[str, ...] = (
    "atomic_write",
    "terminal_status",
    "contract_path",
)


EXPECTED_ARTIFACTS_FIELDS: tuple[str, ...] = (
    "manifest_path",
    "state_path",
    "event_log_jsonl",
    "event_log_md",
    "done_sentinel",
)


EXPECTED_CALLER_INFO_FIELDS: tuple[str, ...] = (
    "skill",
    "skill_version",
    "invocation_label",
    "kind",
)


# ---------------------------------------------------------------------------
# DM-017 DoneSentinel -- field-completeness.
# ---------------------------------------------------------------------------


def test_done_sentinel_is_a_dataclass() -> None:
    assert dataclasses.is_dataclass(DoneSentinel)


def test_done_sentinel_declares_every_dm017_field() -> None:
    """No field drift vs roadmap DM-017 row."""
    declared = tuple(f.name for f in dataclasses.fields(DoneSentinel))
    assert declared == EXPECTED_DONE_SENTINEL_FIELDS, (
        f"DoneSentinel field set diverged from DM-017 row.\n"
        f"  declared: {declared}\n"
        f"  expected: {EXPECTED_DONE_SENTINEL_FIELDS}"
    )


def test_done_sentinel_field_count_matches_dm017() -> None:
    """T01.28 acceptance: Field-count test for DoneSentinel."""
    assert len(dataclasses.fields(DoneSentinel)) == 3


def test_done_sentinel_atomic_write_is_bool() -> None:
    hints = typing.get_type_hints(DoneSentinel)
    assert hints["atomic_write"] is bool


def test_done_sentinel_contract_path_is_str() -> None:
    hints = typing.get_type_hints(DoneSentinel)
    assert hints["contract_path"] is str


def test_done_sentinel_terminal_status_is_result_status_literal() -> None:
    """terminal_status reuses :data:`ResultStatus` so the sentinel and the
    contract it points at cannot drift."""
    hints = typing.get_type_hints(DoneSentinel)
    assert set(typing.get_args(hints["terminal_status"])) == set(
        typing.get_args(ResultStatus)
    )


# ---------------------------------------------------------------------------
# DM-017 DoneSentinel -- defaults + Literal enforcement.
# ---------------------------------------------------------------------------


def test_done_sentinel_default_atomic_write_is_true() -> None:
    """DM-017 row spells ``atomic_write:bool(true)`` -- always-on default."""
    assert DoneSentinel().atomic_write is True


def test_done_sentinel_default_terminal_status_is_success() -> None:
    assert DoneSentinel().terminal_status == "success"


def test_done_sentinel_default_contract_path_is_empty() -> None:
    assert DoneSentinel().contract_path == ""


@pytest.mark.parametrize("status", ["success", "partial", "failed"])
def test_done_sentinel_accepts_each_terminal_status_literal(status: str) -> None:
    sentinel = DoneSentinel(terminal_status=status)  # type: ignore[arg-type]
    assert sentinel.terminal_status == status


def test_done_sentinel_rejects_unknown_terminal_status() -> None:
    """A manually constructed sentinel cannot smuggle an out-of-enum
    value into ``done.json``."""
    with pytest.raises(ValueError, match="terminal_status"):
        DoneSentinel(terminal_status="bogus")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# DM-017 DoneSentinel -- round-trip.
# ---------------------------------------------------------------------------


def test_done_sentinel_default_round_trips_via_dict() -> None:
    instance = DoneSentinel()
    restored = from_dict(DoneSentinel, to_dict(instance))
    assert restored == instance


def test_done_sentinel_default_round_trips_via_json() -> None:
    instance = DoneSentinel()
    restored = from_json(DoneSentinel, to_json(instance))
    assert restored == instance


def test_done_sentinel_populated_round_trips_via_json() -> None:
    instance = DoneSentinel(
        atomic_write=True,
        terminal_status="partial",
        contract_path="/abs/path/to/return-contract.yaml",
    )
    restored = from_json(DoneSentinel, to_json(instance))
    assert restored == instance


def test_done_sentinel_round_trip_diff_is_empty() -> None:
    instance = DoneSentinel(
        atomic_write=True,
        terminal_status="failed",
        contract_path="/abs/x.yaml",
    )
    payload_before = to_dict(instance)
    restored = from_dict(DoneSentinel, payload_before)
    payload_after = to_dict(restored)
    assert payload_before == payload_after


# ---------------------------------------------------------------------------
# DM-018 Artifacts -- field-completeness.
# ---------------------------------------------------------------------------


def test_artifacts_is_a_dataclass() -> None:
    assert dataclasses.is_dataclass(Artifacts)


def test_artifacts_declares_every_dm018_field() -> None:
    """No field drift vs roadmap DM-018 row."""
    declared = tuple(f.name for f in dataclasses.fields(Artifacts))
    assert declared == EXPECTED_ARTIFACTS_FIELDS, (
        f"Artifacts field set diverged from DM-018 row.\n"
        f"  declared: {declared}\n"
        f"  expected: {EXPECTED_ARTIFACTS_FIELDS}"
    )


def test_artifacts_field_count_matches_dm018() -> None:
    """T01.28 acceptance: Field-count test for Artifacts."""
    assert len(dataclasses.fields(Artifacts)) == 5


@pytest.mark.parametrize(
    "field_name",
    list(EXPECTED_ARTIFACTS_FIELDS),
)
def test_artifacts_every_field_is_str(field_name: str) -> None:
    """All five Artifacts fields are path strings per the roadmap row.

    Note ``done_sentinel`` is the *path* to ``done.json``, not a
    :class:`DoneSentinel` instance -- matches the row's ``done_sentinel:str``.
    """
    hints = typing.get_type_hints(Artifacts)
    assert hints[field_name] is str, (
        f"Artifacts.{field_name} should be typed str (absolute path); "
        f"got {hints[field_name]!r}"
    )


# ---------------------------------------------------------------------------
# DM-018 Artifacts -- defaults.
# ---------------------------------------------------------------------------


def test_artifacts_defaults_are_empty_strings() -> None:
    """All five fields default to ``""`` so the no-arg round-trip stub
    stays valid; real instances are stamped at Wave 3 reduce."""
    artifacts = Artifacts()
    assert artifacts.manifest_path == ""
    assert artifacts.state_path == ""
    assert artifacts.event_log_jsonl == ""
    assert artifacts.event_log_md == ""
    assert artifacts.done_sentinel == ""


# ---------------------------------------------------------------------------
# DM-018 Artifacts -- round-trip.
# ---------------------------------------------------------------------------


def test_artifacts_default_round_trips_via_dict() -> None:
    instance = Artifacts()
    restored = from_dict(Artifacts, to_dict(instance))
    assert restored == instance


def test_artifacts_default_round_trips_via_json() -> None:
    instance = Artifacts()
    restored = from_json(Artifacts, to_json(instance))
    assert restored == instance


def test_artifacts_populated_round_trips_via_json() -> None:
    instance = Artifacts(
        manifest_path="/abs/job-out/manifest.json",
        state_path="/abs/job-out/.swarm-state.json",
        event_log_jsonl="/abs/job-out/event-log.jsonl",
        event_log_md="/abs/job-out/event-log.md",
        done_sentinel="/abs/job-out/done.json",
    )
    restored = from_json(Artifacts, to_json(instance))
    assert restored == instance


def test_artifacts_round_trip_diff_is_empty() -> None:
    instance = Artifacts(
        manifest_path="/a",
        state_path="/b",
        event_log_jsonl="/c",
        event_log_md="/d",
        done_sentinel="/e",
    )
    payload_before = to_dict(instance)
    restored = from_dict(Artifacts, payload_before)
    payload_after = to_dict(restored)
    assert payload_before == payload_after


# ---------------------------------------------------------------------------
# DM-019 CallerInfo -- field-completeness.
# ---------------------------------------------------------------------------


def test_caller_info_is_a_dataclass() -> None:
    assert dataclasses.is_dataclass(CallerInfo)


def test_caller_info_declares_every_dm019_field() -> None:
    """No field drift vs roadmap DM-019 row."""
    declared = tuple(f.name for f in dataclasses.fields(CallerInfo))
    assert declared == EXPECTED_CALLER_INFO_FIELDS, (
        f"CallerInfo field set diverged from DM-019 row.\n"
        f"  declared: {declared}\n"
        f"  expected: {EXPECTED_CALLER_INFO_FIELDS}"
    )


def test_caller_info_field_count_matches_dm019() -> None:
    """T01.28 acceptance: Field-count test for CallerInfo."""
    assert len(dataclasses.fields(CallerInfo)) == 4


def test_caller_info_invocation_label_is_str() -> None:
    hints = typing.get_type_hints(CallerInfo)
    assert hints["invocation_label"] is str


@pytest.mark.parametrize("field_name", ["skill", "skill_version"])
def test_caller_info_optional_str_fields(field_name: str) -> None:
    """DM-019 spells ``skill:str?`` / ``skill_version:str?`` -- both must
    accept None for raw CLI / subprocess callers."""
    hints = typing.get_type_hints(CallerInfo)
    field_type = hints[field_name]
    args = typing.get_args(field_type)
    assert type(None) in args, (
        f"CallerInfo.{field_name} must be Optional (Union[..., None]); "
        f"got {field_type!r}"
    )
    non_none = [a for a in args if a is not type(None)]
    assert non_none == [str], (
        f"CallerInfo.{field_name} Optional arm should be str; got {non_none!r}"
    )


# ---------------------------------------------------------------------------
# DM-019 CallerInfo -- kind Literal enforcement.
# ---------------------------------------------------------------------------


def test_caller_kind_literal_values() -> None:
    """T01.28 acceptance: CallerInfo.kind Literal enforced.

    Acceptance criterion names exactly {claude, cli, subprocess}.
    """
    args = typing.get_args(CallerKind)
    assert set(args) == {"claude", "cli", "subprocess"}, (
        f"CallerKind admits {set(args)}; T01.28 acceptance requires "
        "{'claude','cli','subprocess'}."
    )


def test_caller_info_default_kind_is_cli() -> None:
    """Conservative default representing direct terminal invocation."""
    assert CallerInfo().kind == "cli"


@pytest.mark.parametrize("kind", ["claude", "cli", "subprocess"])
def test_caller_info_accepts_each_kind_literal(kind: str) -> None:
    info = CallerInfo(kind=kind)  # type: ignore[arg-type]
    assert info.kind == kind


def test_caller_info_rejects_unknown_kind() -> None:
    """A manually constructed CallerInfo cannot smuggle an out-of-enum
    value into ``JobSpec.caller`` / ``ResultContract.caller``."""
    with pytest.raises(ValueError, match="kind"):
        CallerInfo(kind="bogus")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# DM-019 CallerInfo -- defaults.
# ---------------------------------------------------------------------------


def test_caller_info_defaults() -> None:
    info = CallerInfo()
    assert info.skill is None
    assert info.skill_version is None
    assert info.invocation_label == ""
    assert info.kind == "cli"


# ---------------------------------------------------------------------------
# DM-019 CallerInfo -- round-trip.
# ---------------------------------------------------------------------------


def test_caller_info_default_round_trips_via_dict() -> None:
    instance = CallerInfo()
    restored = from_dict(CallerInfo, to_dict(instance))
    assert restored == instance


def test_caller_info_default_round_trips_via_json() -> None:
    instance = CallerInfo()
    restored = from_json(CallerInfo, to_json(instance))
    assert restored == instance


def test_caller_info_skill_populated_round_trips_via_json() -> None:
    """Skill caller path: both Optional fields carry strings."""
    instance = CallerInfo(
        skill="sc-bare-review",
        skill_version="1.0.0",
        invocation_label="bare-review-after-T01.27",
        kind="claude",
    )
    restored = from_json(CallerInfo, to_json(instance))
    assert restored == instance
    assert restored.skill == "sc-bare-review"
    assert restored.skill_version == "1.0.0"


def test_caller_info_subprocess_round_trips_with_none_skill() -> None:
    """Subprocess path: raw caller, no skill identity."""
    instance = CallerInfo(
        skill=None,
        skill_version=None,
        invocation_label="cron-nightly-audit",
        kind="subprocess",
    )
    restored = from_json(CallerInfo, to_json(instance))
    assert restored == instance
    assert restored.skill is None
    assert restored.skill_version is None


def test_caller_info_round_trip_diff_is_empty() -> None:
    instance = CallerInfo(
        skill="sc-troubleshoot",
        skill_version="2.1",
        invocation_label="oncall-2026-06-01",
        kind="claude",
    )
    payload_before = to_dict(instance)
    restored = from_dict(CallerInfo, payload_before)
    payload_after = to_dict(restored)
    assert payload_before == payload_after
