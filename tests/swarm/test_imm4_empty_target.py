"""T02.13 -- IMM-4 empty-target guard (truncation-aware + no-dispatch).

Roadmap row R-040 (IMM-4). Covers the acceptance criteria:

    * ``preflight.guard_empty_target`` rejects targets with <50
      non-whitespace bytes (post-truncation).
    * Failed contract reason is ``target-too-small``.
    * STOP before any dispatch -- a mock dispatcher wired to fire only
      on preflight success records zero invocations for a 49-byte
      target.
    * ``Truncation.line_cap`` is applied before the count, so a target
      whose substantive content lives only past the cap is rejected
      even though the raw payload would clear the floor.
    * ``Truncation.byte_floor`` overrides the default 50-byte floor so
      callers can tighten the guard per-spec.

The skeleton non-whitespace check + IMM-4 wiring inside ``run_preflight``
landed in T02.02; this module exists specifically to lock the hardened
T02.13 semantics (truncation-aware, no-dispatch).
"""

from __future__ import annotations

from typing import Any, Callable
from unittest.mock import MagicMock

import pytest

# IMM-4 empty-target STOP (T08.03 / NFR-007). Module-level marker so
# every test in this file is selected by ``pytest -m imm``.
pytestmark = pytest.mark.imm

from superclaude.cli.swarm.preflight import (
    MIN_TARGET_NON_WHITESPACE_BYTES,
    RULE_TARGET_TOO_SMALL,
    PreflightError,
    PreflightResult,
    guard_empty_target,
    run_preflight,
    set_lens_resolver,
    truncate_target,
)
from superclaude.cli.swarm.models import LensEntry
from superclaude.cli.swarm.schema import (
    CANONICAL_INJECTION_GUARD_SENTENCE,
    CURRENT_SPEC_VERSION,
)


# ---------------------------------------------------------------------------
# Fixtures -- minimal valid spec + stub lens resolver. Mirrors
# tests/swarm/test_preflight.py so the IMM-4 surface is exercised in
# isolation from the rest of the Wave-0 guards.
# ---------------------------------------------------------------------------


def _minimal_valid_spec() -> dict[str, Any]:
    return {
        "spec_version": CURRENT_SPEC_VERSION,
        "job_id": "job-imm4-001",
        "created": "2026-06-01T00:00:00Z",
        "caller": {
            "skill": "sc-bare-review",
            "skill_version": "1.0.0",
            "invocation_label": "imm4-T02.13-smoke",
            "kind": "claude",
        },
        "lens": "bare-review",
        "custom_prompt_dir": None,
        "workers": {
            "count": 3,
            "models": ["gpt-5-codex", "claude-haiku-4.5", "gemini-1.5-pro"],
            "timeout_sec": 180,
            "temperature": 0.2,
            "retry": {
                "on_5xx": True,
                "on_5xx_backoff_sec": 2,
                "on_4xx": False,
                "on_timeout": False,
            },
        },
        "transport": {
            "kind": "openai_compat",
            "base_url_env": "T2ProxyUrl",
            "api_key_env": "T2ProxyKey",
        },
        "prompt": {
            "system": (
                "You are a code reviewer. " + CANONICAL_INJECTION_GUARD_SENTENCE
            ),
            "user_template": "Review: {{target}}",
            "variables": {},
        },
        "target": {
            "kind": "file",
            "path": "/abs/path/to/target.py",
            "truncation": {"line_cap": 4000, "byte_floor": 50},
            "delimiters": {"open": "<<<TARGET>>>", "close": "<<<END TARGET>>>"},
            "injection_guard": {
                "enabled": True,
                "required_substring": CANONICAL_INJECTION_GUARD_SENTENCE,
            },
        },
        "normalization": {
            "recipe": "bare-review-v1",
            "template_path": "/abs/path/to/template.j2",
            "schema_version": "1.0",
            "recipe_args": {},
            "on_parse_error": {"salvage": True, "retain_raw": True},
        },
        "output": {
            "dir": "/abs/path/to/output",
            "filename_template": "{lens}-{index:02d}-{model_slug}.md",
            "lens_name": "bare-review",
            "atomic_write": True,
            "emit_meta_sidecar": True,
        },
        "amalgamation_mode": "normalize+merge",
        "status_policy": {
            "floor": 2,
            "success_first": True,
            "partial_threshold": 2,
        },
        "recommended_next_command_template": "sc:reflect on {job_id}",
        "recommended_next_command_substitutions": {"job_id": "job-imm4-001"},
        "runtime": {
            "mode": "inline",
            "log_level": "info",
            "on_completion": {
                "write_done_sentinel": True,
                "print_contract_to_stdout": True,
            },
        },
    }


def _bare_review_lens() -> LensEntry:
    return LensEntry(
        name="bare-review",
        description="bare review skeleton",
        system_prompt_fragment=(
            "Review with care. " + CANONICAL_INJECTION_GUARD_SENTENCE
        ),
        user_template="Review: {{target}}",
        output_template_path="/abs/path/to/template.j2",
        recipe_name="bare-review-v1",
        default_workers=3,
        default_target_line_cap=4000,
        suspect=True,
        tier="T2",
        recommended_next_command_template="sc:reflect on {job_id} {suspect_files}",
        acceptance_notes="",
        stability="stable",
    )


@pytest.fixture
def lens_resolver_stub():
    lenses = {"bare-review": _bare_review_lens()}

    def resolver(name: str) -> LensEntry:
        if name not in lenses:
            raise KeyError(name)
        return lenses[name]

    previous = set_lens_resolver(resolver)
    try:
        yield resolver
    finally:
        set_lens_resolver(previous)


# ---------------------------------------------------------------------------
# Helper: run_preflight wrapper that only invokes a dispatcher on success.
# The mock dispatcher exposes the no-dispatch guarantee verifiable by tests.
# ---------------------------------------------------------------------------


def _preflight_then_dispatch(
    spec: dict[str, Any],
    *,
    target_loader: Callable[[str], bytes],
    dispatcher: Callable[[PreflightResult], None],
) -> PreflightResult:
    """Mimic the executor: run Wave-0 preflight, then dispatch only on success.

    The IMM-4 STOP-before-dispatch guarantee means that for a sub-floor
    target ``dispatcher`` is never reached -- ``run_preflight`` raises
    :class:`PreflightError` before the dispatch call executes.
    """
    result = run_preflight(spec, target_loader=target_loader)
    dispatcher(result)
    return result


# ---------------------------------------------------------------------------
# guard_empty_target -- direct unit tests
# ---------------------------------------------------------------------------


def test_guard_empty_target_passes_at_byte_floor() -> None:
    payload = b"a" * MIN_TARGET_NON_WHITESPACE_BYTES
    assert guard_empty_target(payload) == []


def test_guard_empty_target_rejects_49_bytes() -> None:
    payload = b"a" * (MIN_TARGET_NON_WHITESPACE_BYTES - 1)
    failures = guard_empty_target(payload)
    assert len(failures) == 1
    assert failures[0].rule == RULE_TARGET_TOO_SMALL
    assert failures[0].reason == "target-too-small"
    assert failures[0].path == "target.path"
    assert "STOP before dispatch" in failures[0].message


def test_guard_empty_target_whitespace_only_is_rejected() -> None:
    # 200 whitespace bytes contain zero non-whitespace -- IMM-4 fires.
    payload = b" \t\n\r\f\v" * 200
    failures = guard_empty_target(payload)
    assert len(failures) == 1
    assert failures[0].reason == "target-too-small"


def test_guard_empty_target_respects_custom_byte_floor() -> None:
    # 80 non-whitespace bytes clears the default floor (50) but fails
    # a tightened floor (100).
    payload = b"a" * 80
    assert guard_empty_target(payload) == []
    failures = guard_empty_target(payload, byte_floor=100)
    assert len(failures) == 1
    assert failures[0].reason == "target-too-small"
    assert "≥100" in failures[0].message


# ---------------------------------------------------------------------------
# truncate_target -- direct unit tests
# ---------------------------------------------------------------------------


def test_truncate_target_keeps_short_payload_intact() -> None:
    payload = b"line-a\nline-b\nline-c\n"
    truncated, was_truncated = truncate_target(payload, line_cap=10)
    assert truncated == payload
    assert was_truncated is False


def test_truncate_target_chops_to_line_cap() -> None:
    payload = b"".join(f"line-{i}\n".encode() for i in range(20))
    truncated, was_truncated = truncate_target(payload, line_cap=5)
    assert was_truncated is True
    assert truncated == b"line-0\nline-1\nline-2\nline-3\nline-4\n"


def test_truncate_target_zero_cap_disables_truncation() -> None:
    payload = b"line-a\nline-b\n"
    truncated, was_truncated = truncate_target(payload, line_cap=0)
    assert truncated == payload
    assert was_truncated is False


# ---------------------------------------------------------------------------
# run_preflight -- IMM-4 STOP-before-dispatch + no-dispatch guarantee
# ---------------------------------------------------------------------------


def test_49_byte_target_raises_target_too_small(lens_resolver_stub) -> None:
    spec = _minimal_valid_spec()
    payload = b"a" * (MIN_TARGET_NON_WHITESPACE_BYTES - 1)
    with pytest.raises(PreflightError) as excinfo:
        run_preflight(spec, target_loader=lambda _p: payload)
    rules = [f.rule for f in excinfo.value.failures]
    assert RULE_TARGET_TOO_SMALL in rules
    failure = next(
        f for f in excinfo.value.failures if f.rule == RULE_TARGET_TOO_SMALL
    )
    assert failure.reason == "target-too-small"


def test_49_byte_target_never_reaches_dispatcher(lens_resolver_stub) -> None:
    """IMM-4 STOP-before-dispatch: the mock dispatcher records zero calls."""
    spec = _minimal_valid_spec()
    payload = b"a" * (MIN_TARGET_NON_WHITESPACE_BYTES - 1)
    dispatcher = MagicMock()
    with pytest.raises(PreflightError):
        _preflight_then_dispatch(
            spec,
            target_loader=lambda _p: payload,
            dispatcher=dispatcher,
        )
    assert dispatcher.call_count == 0


def test_50_byte_target_reaches_dispatcher_once(lens_resolver_stub) -> None:
    """Symmetry check: at the floor, preflight succeeds and dispatch is called."""
    spec = _minimal_valid_spec()
    payload = b"a" * MIN_TARGET_NON_WHITESPACE_BYTES
    dispatcher = MagicMock()
    result = _preflight_then_dispatch(
        spec,
        target_loader=lambda _p: payload,
        dispatcher=dispatcher,
    )
    assert isinstance(result, PreflightResult)
    assert dispatcher.call_count == 1


def test_post_truncation_count_rejects_substantive_only_past_cap(
    lens_resolver_stub,
) -> None:
    """Truncation-aware: substantive content past the cap is dropped.

    The raw payload would clear the byte floor (40 lines × `a`*5 +
    abundant content on line 50). After truncation to ``line_cap=10``
    only the first 10 short lines survive, which fall below the floor.
    """
    spec = _minimal_valid_spec()
    spec["target"]["truncation"]["line_cap"] = 10
    # Lines 1..10: 1 non-whitespace byte each (10 total). Line 11+
    # carry the bulk of the payload but are dropped by truncation.
    head = b"a\n" * 10  # 10 non-ws bytes
    tail = b"a" * 5000 + b"\n"
    payload = head + tail
    # Raw payload has plenty of non-whitespace bytes...
    assert payload.count(b"a") > MIN_TARGET_NON_WHITESPACE_BYTES
    # ...but post-truncation has only 10, so IMM-4 fires.
    with pytest.raises(PreflightError) as excinfo:
        run_preflight(spec, target_loader=lambda _p: payload)
    assert RULE_TARGET_TOO_SMALL in {f.rule for f in excinfo.value.failures}


def test_custom_byte_floor_in_spec_tightens_imm4(lens_resolver_stub) -> None:
    """``target.truncation.byte_floor`` overrides the 50-byte default."""
    spec = _minimal_valid_spec()
    spec["target"]["truncation"]["byte_floor"] = 200
    # 100 non-whitespace bytes clears the default 50-byte floor but not
    # the tightened 200-byte floor stamped on this spec.
    payload = b"a" * 100
    with pytest.raises(PreflightError) as excinfo:
        run_preflight(spec, target_loader=lambda _p: payload)
    rules = [f.rule for f in excinfo.value.failures]
    assert RULE_TARGET_TOO_SMALL in rules


def test_target_checksum_is_post_truncation(lens_resolver_stub) -> None:
    """PreflightSummary semantics: checksum is computed post-truncation."""
    import hashlib

    spec = _minimal_valid_spec()
    spec["target"]["truncation"]["line_cap"] = 3
    head = (b"line\n" * 3) + (b"a" * 200)  # 3 short lines + bulk
    # Pad post-cap content so that truncating to 3 lines still clears
    # the 50-byte floor.
    head = b"line-aaaaaaaaaa-1\n" * 3 + b"trailing-bulk\n" * 50
    result = run_preflight(spec, target_loader=lambda _p: head)
    truncated_head = b"line-aaaaaaaaaa-1\n" * 3
    expected = hashlib.sha256(truncated_head).hexdigest()
    assert result.manifest.preflight.target_checksum == expected
