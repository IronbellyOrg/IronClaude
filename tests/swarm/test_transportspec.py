"""T01.16 -- DM-004 ``TransportSpec`` field set + round-trip + validation.

Covers roadmap row R-014 / DM-004. TransportSpec configures the transport
endpoint (kind + env-var names for base URL and API key resolution).
This suite pins:

1. Every field listed in the roadmap DM-004 row is present on
   TransportSpec (kind, base_url_env, api_key_env).
2. ``kind`` is typed as :data:`TransportKind` =
   ``Literal['openai_compat','stub']`` (T01.16 acceptance).
3. Defaults match FR-SPEC-004 / AC-017: kind=openai_compat,
   base_url_env=T2ProxyUrl, api_key_env=T2ProxyKey.
4. JSON round-trip is lossless for default and populated instances.
5. ``__post_init__`` validation rejects invalid ``kind`` values
   (T01.16 acceptance: ``kind="bogus"`` raises).
6. ``__post_init__`` validation rejects empty env-var names
   (T01.16 acceptance: env-var name validation rejects empty strings).

STANDARD-tier task per phase-1-tasklist.md T01.16.
"""

from __future__ import annotations

import dataclasses
import typing

import pytest

from superclaude.cli.swarm.models import (
    TransportKind,
    TransportSpec,
    from_dict,
    from_json,
    to_dict,
    to_json,
)


# Roadmap DM-004 row (.dev/releases/Current/MultiModelSwarm/roadmap.md L91)
# names exactly these fields.
EXPECTED_FIELDS: tuple[str, ...] = (
    "kind",
    "base_url_env",
    "api_key_env",
)


# ---------------------------------------------------------------------------
# Field-completeness.
# ---------------------------------------------------------------------------


def test_transportspec_is_a_dataclass() -> None:
    assert dataclasses.is_dataclass(TransportSpec)


def test_transportspec_declares_every_dm004_field() -> None:
    """No field drift vs roadmap DM-004 row."""
    declared = tuple(f.name for f in dataclasses.fields(TransportSpec))
    assert declared == EXPECTED_FIELDS, (
        f"TransportSpec field set diverged from DM-004 row.\n"
        f"  declared: {declared}\n"
        f"  expected: {EXPECTED_FIELDS}"
    )


def test_transportspec_field_count_matches_dm004() -> None:
    """Sanity gate so accidental field additions/removals fail loudly."""
    assert len(dataclasses.fields(TransportSpec)) == len(EXPECTED_FIELDS)


def test_kind_is_typed_as_transport_kind_literal() -> None:
    """T01.16 acceptance: ``kind`` is a Literal['openai_compat','stub']."""
    hints = typing.get_type_hints(TransportSpec)
    assert hints["kind"] is TransportKind


def test_transport_kind_literal_values() -> None:
    """The Literal enumerates exactly the two allowed transports."""
    assert typing.get_args(TransportKind) == ("openai_compat", "stub")


def test_base_url_env_is_typed_as_str() -> None:
    hints = typing.get_type_hints(TransportSpec)
    assert hints["base_url_env"] is str


def test_api_key_env_is_typed_as_str() -> None:
    hints = typing.get_type_hints(TransportSpec)
    assert hints["api_key_env"] is str


# ---------------------------------------------------------------------------
# Default values (T01.16 + FR-SPEC-004 / AC-017 spec defaults).
# ---------------------------------------------------------------------------


def test_default_kind_is_openai_compat() -> None:
    """FR-SPEC-004: Phase-1 reference transport is openai_compat."""
    assert TransportSpec().kind == "openai_compat"


def test_default_base_url_env_is_t2_proxy_url() -> None:
    """AC-017 / FR-SPEC-004: base_url_env=T2ProxyUrl."""
    assert TransportSpec().base_url_env == "T2ProxyUrl"


def test_default_api_key_env_is_t2_proxy_key() -> None:
    """AC-017 / FR-SPEC-004: api_key_env=T2ProxyKey."""
    assert TransportSpec().api_key_env == "T2ProxyKey"


# ---------------------------------------------------------------------------
# Validation (T01.16 acceptance criteria).
# ---------------------------------------------------------------------------


def test_invalid_kind_raises_value_error() -> None:
    """T01.16 acceptance: construction with ``kind="bogus"`` raises."""
    with pytest.raises(ValueError, match="kind"):
        TransportSpec(kind="bogus")  # type: ignore[arg-type]


def test_kind_openai_compat_is_accepted() -> None:
    """Sanity: the canonical Phase-1 kind constructs without error."""
    spec = TransportSpec(kind="openai_compat")
    assert spec.kind == "openai_compat"


def test_kind_stub_is_accepted() -> None:
    """Sanity: the deterministic CI stub kind constructs without error."""
    spec = TransportSpec(kind="stub")
    assert spec.kind == "stub"


def test_empty_base_url_env_raises_value_error() -> None:
    """T01.16 acceptance: env-var name validation rejects empty strings."""
    with pytest.raises(ValueError, match="base_url_env"):
        TransportSpec(base_url_env="")


def test_empty_api_key_env_raises_value_error() -> None:
    """T01.16 acceptance: env-var name validation rejects empty strings."""
    with pytest.raises(ValueError, match="api_key_env"):
        TransportSpec(api_key_env="")


# ---------------------------------------------------------------------------
# Round-trip contracts.
# ---------------------------------------------------------------------------


def test_default_instance_round_trips_via_dict() -> None:
    instance = TransportSpec()
    restored = from_dict(TransportSpec, to_dict(instance))
    assert restored == instance


def test_default_instance_round_trips_via_json() -> None:
    instance = TransportSpec()
    restored = from_json(TransportSpec, to_json(instance))
    assert restored == instance


def test_populated_instance_round_trips_via_json() -> None:
    instance = TransportSpec(
        kind="stub",
        base_url_env="CustomProxyUrl",
        api_key_env="CustomProxyKey",
    )
    restored = from_json(TransportSpec, to_json(instance))
    assert restored == instance


def test_round_trip_diff_is_empty() -> None:
    """Acceptance criterion: round-trip lossless."""
    instance = TransportSpec(
        kind="openai_compat",
        base_url_env="T2ProxyUrl",
        api_key_env="T2ProxyKey",
    )
    payload_before = to_dict(instance)
    restored = from_dict(TransportSpec, payload_before)
    payload_after = to_dict(restored)
    assert payload_before == payload_after
