"""T02.01 -- ``cli/swarm/schema.py`` JSON Schema + cross-field validators.

Covers roadmap row R-030 (COMP-005). Pins:

1. The schema module exposes :data:`JOB_SPEC_SCHEMA`,
   :data:`CURRENT_SPEC_VERSION`, :data:`CANONICAL_INJECTION_GUARD_SENTENCE`,
   :class:`SchemaValidationFailure`, :class:`SchemaValidationError`,
   :func:`validate`, :func:`validate_or_raise`.
2. A round-trip-friendly minimal valid spec passes both ``validate`` and
   ``validate_or_raise``.
3. Negative-case fixtures (missing required field, wrong type,
   out-of-enum, ``spec_version`` drift, missing §11.5 substring, empty
   ``required_substring`` with guard enabled, unknown field) each fail
   with the expected rule identifier.
4. ``validate_or_raise`` bundles every failure in the raised
   :class:`SchemaValidationError`.
5. Disabled injection guard bypasses the §11.5 cross-field rule.

T02.03 adds ``custom_prompt_dir`` requires ``lens == 'custom'``;
that rule is exercised in detail by
``tests/swarm/test_schema_injection_substring.py``. Here we only pin
the public surface (``RULE_CUSTOM_PROMPT_DIR_REQUIRES_CUSTOM_LENS`` /
``CUSTOM_LENS_NAME`` exports) so accidental removal trips this test.

STRICT-tier task per §4.11 (security-critical §11.5 enforcement).
"""

from __future__ import annotations

import copy
from typing import Any

import pytest

from superclaude.cli.swarm import schema
from superclaude.cli.swarm.schema import (
    CANONICAL_INJECTION_GUARD_SENTENCE,
    CURRENT_SPEC_VERSION,
    JOB_SPEC_SCHEMA,
    RULE_INJECTION_REQUIRED,
    RULE_INJECTION_SUBSTRING,
    RULE_SCHEMA,
    RULE_SPEC_VERSION,
    SchemaValidationError,
    SchemaValidationFailure,
    validate,
    validate_or_raise,
)

# ---------------------------------------------------------------------------
# Fixture: a minimal valid JobSpec dict.
#
# Kept literal (no construction from JobSpec dataclass) so the schema
# layer is exercised end-to-end without coupling tests to the dataclass
# defaults. Every required field is present; the §11.5 cross-field rule
# is satisfied (prompt.system contains the canonical substring).
# ---------------------------------------------------------------------------


def _minimal_valid_spec() -> dict[str, Any]:
    return {
        "spec_version": CURRENT_SPEC_VERSION,
        "job_id": "job-abc",
        "created": "2026-06-01T00:00:00Z",
        "caller": {
            "skill": "sc-bare-review",
            "skill_version": "1.0.0",
            "invocation_label": "bare-review-T02.01-smoke",
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
        "recommended_next_command_substitutions": {"job_id": "job-abc"},
        "runtime": {
            "mode": "inline",
            "log_level": "info",
            "on_completion": {
                "write_done_sentinel": True,
                "print_contract_to_stdout": True,
            },
        },
    }


# ---------------------------------------------------------------------------
# Module surface
# ---------------------------------------------------------------------------


def test_schema_constants_are_strings() -> None:
    assert isinstance(CURRENT_SPEC_VERSION, str) and CURRENT_SPEC_VERSION
    assert (
        isinstance(CANONICAL_INJECTION_GUARD_SENTENCE, str)
        and CANONICAL_INJECTION_GUARD_SENTENCE
    )


def test_job_spec_schema_is_draft7() -> None:
    assert JOB_SPEC_SCHEMA["$schema"] == "http://json-schema.org/draft-07/schema#"
    # The schema must list every DM-001 top-level field. The dataclass
    # carries 17 fields total; one (``custom_prompt_dir``) is optional,
    # so the schema's ``required`` list is the 16 mandatory fields.
    assert len(JOB_SPEC_SCHEMA["required"]) == 16


def test_spec_version_pinned_to_supported_versions() -> None:
    # After T06.09 (NFR-006 forward-compat) ``spec_version`` uses an
    # ``enum`` keyed off :data:`SUPPORTED_SPEC_VERSIONS`. The orchestrator
    # still emits :data:`CURRENT_SPEC_VERSION`, but legacy versions in
    # the supported tuple are accepted on input so resume / replay paths
    # survive across point releases.
    spec_version_entry = JOB_SPEC_SCHEMA["properties"]["spec_version"]
    assert spec_version_entry["enum"] == list(schema.SUPPORTED_SPEC_VERSIONS)
    assert CURRENT_SPEC_VERSION in schema.SUPPORTED_SPEC_VERSIONS


def test_public_surface() -> None:
    assert set(schema.__all__) == {
        "CANONICAL_INJECTION_GUARD_SENTENCE",
        "CURRENT_SPEC_VERSION",
        "CUSTOM_LENS_NAME",
        "DEPRECATED_SPEC_VERSIONS",
        "JOB_SPEC_SCHEMA",
        "RULE_CUSTOM_PROMPT_DIR_REQUIRES_CUSTOM_LENS",
        "RULE_INJECTION_REQUIRED",
        "RULE_INJECTION_SUBSTRING",
        "RULE_SCHEMA",
        "RULE_SPEC_VERSION",
        "SUPPORTED_SPEC_VERSIONS",
        "SchemaValidationError",
        "SchemaValidationFailure",
        "contains_required_substring",
        "deprecation_warnings",
        "validate",
        "validate_or_raise",
    }


# ---------------------------------------------------------------------------
# Valid-spec path
# ---------------------------------------------------------------------------


def test_minimal_valid_spec_passes_validate() -> None:
    failures = validate(_minimal_valid_spec())
    assert failures == [], "minimal valid spec produced failures:\n" + "\n".join(
        f"  {f.rule}@{f.path}: {f.message}" for f in failures
    )


def test_minimal_valid_spec_passes_validate_or_raise() -> None:
    # Should return None without raising.
    assert validate_or_raise(_minimal_valid_spec()) is None


def test_validate_returns_empty_list_when_custom_prompt_dir_omitted() -> None:
    # ``custom_prompt_dir`` is optional per DM-001; a spec without it
    # must still validate.
    spec = _minimal_valid_spec()
    del spec["custom_prompt_dir"]
    assert validate(spec) == []


# ---------------------------------------------------------------------------
# spec_version drift
# ---------------------------------------------------------------------------


def test_wrong_spec_version_emits_pinned_rule() -> None:
    spec = _minimal_valid_spec()
    spec["spec_version"] = "0.9"
    failures = validate(spec)
    rules = [f.rule for f in failures]
    assert RULE_SPEC_VERSION in rules, rules
    pinned = next(f for f in failures if f.rule == RULE_SPEC_VERSION)
    assert pinned.path == "spec_version"
    assert pinned.value == "0.9"


# ---------------------------------------------------------------------------
# §11.5 cross-field rule
# ---------------------------------------------------------------------------


def test_missing_injection_substring_in_prompt_system_is_rejected() -> None:
    spec = _minimal_valid_spec()
    # Drop the canonical sentence from prompt.system but keep the
    # required_substring populated -- this is the §11.5 violation
    # T02.03 / T02.07 must reject.
    spec["prompt"]["system"] = "You are a code reviewer."
    failures = validate(spec)
    rules = [f.rule for f in failures]
    assert RULE_INJECTION_SUBSTRING in rules, rules
    failure = next(f for f in failures if f.rule == RULE_INJECTION_SUBSTRING)
    assert failure.path == "prompt.system"
    # The failure surfaces the missing substring so operators can
    # paste it into prompt.system.
    assert CANONICAL_INJECTION_GUARD_SENTENCE in failure.message


def test_empty_required_substring_with_guard_enabled_is_rejected() -> None:
    spec = _minimal_valid_spec()
    spec["target"]["injection_guard"]["required_substring"] = ""
    failures = validate(spec)
    rules = [f.rule for f in failures]
    assert RULE_INJECTION_REQUIRED in rules, rules
    # When the required_substring is empty we do not also emit the
    # downstream "missing in prompt.system" failure -- the missing
    # substring is itself the root cause.
    assert RULE_INJECTION_SUBSTRING not in rules


def test_disabled_injection_guard_skips_cross_field_rule() -> None:
    spec = _minimal_valid_spec()
    spec["target"]["injection_guard"]["enabled"] = False
    spec["target"]["injection_guard"]["required_substring"] = ""
    spec["prompt"]["system"] = "You are a code reviewer."
    # Disabling the guard opts out of §11.5; the schema layer does not
    # second-guess that choice (T02.07 may layer its own policy).
    failures = validate(spec)
    rules = [f.rule for f in failures]
    assert RULE_INJECTION_REQUIRED not in rules
    assert RULE_INJECTION_SUBSTRING not in rules


# ---------------------------------------------------------------------------
# Schema-level negative cases
# ---------------------------------------------------------------------------


def test_missing_required_top_level_field_is_rejected() -> None:
    spec = _minimal_valid_spec()
    del spec["transport"]
    failures = validate(spec)
    assert any(f.rule == RULE_SCHEMA for f in failures), [f.rule for f in failures]


def test_wrong_type_is_rejected() -> None:
    spec = _minimal_valid_spec()
    spec["workers"]["count"] = "three"
    failures = validate(spec)
    schema_failures = [f for f in failures if f.rule == RULE_SCHEMA]
    assert schema_failures, [f.rule for f in failures]
    # Path locates the offending field for the operator.
    assert any("workers.count" in f.path for f in schema_failures)


def test_out_of_enum_amalgamation_mode_is_rejected() -> None:
    spec = _minimal_valid_spec()
    spec["amalgamation_mode"] = "bogus"
    failures = validate(spec)
    assert any(f.rule == RULE_SCHEMA for f in failures)


def test_unknown_top_level_field_is_rejected() -> None:
    # ``additionalProperties: False`` catches typos.
    spec = _minimal_valid_spec()
    spec["unknown_field"] = "oops"
    failures = validate(spec)
    assert any(f.rule == RULE_SCHEMA for f in failures)


# ---------------------------------------------------------------------------
# validate_or_raise / SchemaValidationError contract
# ---------------------------------------------------------------------------


def test_validate_or_raise_bundles_every_failure() -> None:
    spec = _minimal_valid_spec()
    spec["spec_version"] = "0.9"
    spec["prompt"]["system"] = "no guard sentence here"
    with pytest.raises(SchemaValidationError) as excinfo:
        validate_or_raise(spec)
    rules = [f.rule for f in excinfo.value.failures]
    assert RULE_SPEC_VERSION in rules
    assert RULE_INJECTION_SUBSTRING in rules
    # The exception message must name the failing rules so terminal
    # output is actionable.
    msg = str(excinfo.value)
    assert RULE_SPEC_VERSION in msg
    assert RULE_INJECTION_SUBSTRING in msg


def test_schema_validation_failure_is_frozen() -> None:
    failure = SchemaValidationFailure(
        rule=RULE_SCHEMA,
        path="prompt.system",
        message="...",
        value=None,
    )
    with pytest.raises(Exception):
        # frozen dataclass: attribute assignment raises FrozenInstanceError.
        failure.rule = "other"  # type: ignore[misc]


def test_schema_validation_error_requires_at_least_one_failure() -> None:
    with pytest.raises(ValueError):
        SchemaValidationError([])


# ---------------------------------------------------------------------------
# Edge inputs
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("non_dict", [None, 42, "spec", [], (1, 2)])
def test_non_dict_spec_is_rejected(non_dict: Any) -> None:
    failures = validate(non_dict)
    assert failures
    assert any(f.rule == RULE_SCHEMA for f in failures)


def test_validate_does_not_mutate_input() -> None:
    spec = _minimal_valid_spec()
    snapshot = copy.deepcopy(spec)
    validate(spec)
    assert spec == snapshot
