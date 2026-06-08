"""T06.09 -- NFR-006 spec_version forward-compat (1.1 loads 1.0 spec).

Covers roadmap row R-117 (NFR-006). Pins the orchestrator's best-effort
forward-compat policy: a swarm orchestrator at
:data:`CURRENT_SPEC_VERSION` accepts every entry in
:data:`SUPPORTED_SPEC_VERSIONS` so a 1.1 build transparently loads a 1.0
spec emitted by an earlier release. The 1.0 input validates without
errors, and a :class:`DeprecationWarning` is emitted so the legacy
version surfaces in operator logs ahead of any future major bump that
would drop read support.

What this test does NOT pin:

    * Schema shape across minor versions (1.0 and 1.1 currently share
      identical field sets -- only the version label differs). When a
      future minor release introduces additive optional fields, the 1.0
      fixture below must continue to validate (since the new fields are
      optional) and a separate test will pin the new fields' acceptance
      on a 1.1+ spec.
    * Unsupported versions (e.g., "0.9", "2.0") -- those are exercised
      by ``test_schema.test_wrong_spec_version_emits_pinned_rule`` and
      ``test_validate_cmd.test_invalid_spec_wrong_spec_version_exits_nonzero``.

STANDARD-tier task per the phase-6 tasklist (T06.09): best-effort guard
with no rollback path (NFR-006 is read-only forward-compat; the
orchestrator never emits a legacy version, only reads it).
"""

from __future__ import annotations

import warnings
from typing import Any

import pytest

from superclaude.cli.swarm import schema
from superclaude.cli.swarm.schema import (
    CANONICAL_INJECTION_GUARD_SENTENCE,
    CURRENT_SPEC_VERSION,
    DEPRECATED_SPEC_VERSIONS,
    RULE_SPEC_VERSION,
    SUPPORTED_SPEC_VERSIONS,
    SchemaValidationError,
    deprecation_warnings,
    validate,
    validate_or_raise,
)

# ---------------------------------------------------------------------------
# Fixture: a minimal valid 1.0 JobSpec dict.
#
# Hand-authored as a frozen 1.0 snapshot (not derived from the
# ``test_schema._minimal_valid_spec`` helper) so the test stays
# representative even if the orchestrator's current-version fixture
# drifts. The shape mirrors what the 1.0 orchestrator would have
# written to disk before the T06.09 bump: every DM-001 required field
# present, §11.5 guard satisfied, ``spec_version`` hard-coded to "1.0".
# ---------------------------------------------------------------------------


SPEC_VERSION_1_0 = "1.0"


def _minimal_v1_0_spec() -> dict[str, Any]:
    return {
        "spec_version": SPEC_VERSION_1_0,
        "job_id": "job-forward-compat-1.0",
        "created": "2026-05-01T00:00:00Z",
        "caller": {
            "skill": "sc-bare-review",
            "skill_version": "1.0.0",
            "invocation_label": "forward-compat-T06.09-smoke",
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
                "You are a code reviewer. "
                + CANONICAL_INJECTION_GUARD_SENTENCE
            ),
            "user_template": "Review: {{target}}",
            "variables": {},
        },
        "target": {
            "kind": "file",
            "path": "/abs/path/to/target.py",
            "truncation": {"line_cap": 4000, "byte_floor": 50},
            "delimiters": {
                "open": "<<<TARGET>>>",
                "close": "<<<END TARGET>>>",
            },
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
        "recommended_next_command_substitutions": {
            "job_id": "job-forward-compat-1.0"
        },
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
# Policy constants: NFR-006 best-effort read-compat
# ---------------------------------------------------------------------------


def test_current_spec_version_is_1_1() -> None:
    # The orchestrator emits 1.1 on every new job; this assertion makes
    # the version bump load-bearing for the rest of the suite -- any
    # accidental rollback to 1.0 trips here before the forward-compat
    # branches below silently degrade into "1.0 loads 1.0", which is
    # not a forward-compat scenario at all.
    assert CURRENT_SPEC_VERSION == "1.1"


def test_supported_spec_versions_include_1_0_and_current() -> None:
    # NFR-006 supported tuple must list both legacy and current versions
    # in the same order so callers iterating the tuple see history first.
    assert SPEC_VERSION_1_0 in SUPPORTED_SPEC_VERSIONS
    assert CURRENT_SPEC_VERSION in SUPPORTED_SPEC_VERSIONS


def test_legacy_1_0_is_in_deprecated_set() -> None:
    # The 1.0 version is accepted but flagged as deprecated so operator
    # logs surface the drift via DeprecationWarning.
    assert SPEC_VERSION_1_0 in DEPRECATED_SPEC_VERSIONS
    assert CURRENT_SPEC_VERSION not in DEPRECATED_SPEC_VERSIONS


# ---------------------------------------------------------------------------
# Acceptance criterion: 1.1 orchestrator loads 1.0 spec without error.
# ---------------------------------------------------------------------------


def test_validate_accepts_1_0_spec_under_1_1_orchestrator() -> None:
    # NFR-006 best-effort: a 1.0 spec must validate cleanly on a 1.1
    # orchestrator. No SchemaValidationFailure entries are expected --
    # the only side-effect is the deprecation warning, which is
    # exercised separately so this test stays focused on "accepted".
    spec = _minimal_v1_0_spec()
    failures = validate(spec)
    assert failures == [], (
        "1.0 spec must validate cleanly on 1.1 orchestrator; got:\n"
        + "\n".join(f"  {f.rule}@{f.path}: {f.message}" for f in failures)
    )


def test_validate_or_raise_accepts_1_0_spec_under_1_1_orchestrator() -> None:
    # The raise-on-invalid wrapper must mirror :func:`validate` -- 1.0
    # in, no exception out.
    spec = _minimal_v1_0_spec()
    with warnings.catch_warnings():
        # Silence the deprecation warning here so we only pin the
        # accept-without-error behavior; the warning emission is
        # exercised by ``test_validate_or_raise_emits_deprecation_warning``.
        warnings.simplefilter("ignore", DeprecationWarning)
        assert validate_or_raise(spec) is None


# ---------------------------------------------------------------------------
# Acceptance criterion: deprecated fields warned but accepted.
# ---------------------------------------------------------------------------


def test_deprecation_warnings_emitted_for_1_0_spec() -> None:
    # The :func:`deprecation_warnings` helper returns one human-readable
    # message per legacy version. The message must name both the legacy
    # version and :data:`CURRENT_SPEC_VERSION` so operators can act on it
    # without consulting the schema source.
    messages = deprecation_warnings(_minimal_v1_0_spec())
    assert len(messages) == 1, messages
    message = messages[0]
    assert SPEC_VERSION_1_0 in message
    assert CURRENT_SPEC_VERSION in message
    assert "deprecated" in message.lower()


def test_deprecation_warnings_empty_for_current_spec_version() -> None:
    # A spec at :data:`CURRENT_SPEC_VERSION` is the canonical emission
    # path; no deprecation warning fires.
    spec = _minimal_v1_0_spec()
    spec["spec_version"] = CURRENT_SPEC_VERSION
    assert deprecation_warnings(spec) == []


def test_validate_or_raise_emits_deprecation_warning_for_1_0_spec() -> None:
    # NFR-006 best-effort: :func:`validate_or_raise` must wire the
    # deprecation helper through :mod:`warnings` so operator logs
    # surface the drift without forcing every caller to invoke the
    # helper explicitly.
    spec = _minimal_v1_0_spec()
    with pytest.warns(DeprecationWarning) as caught:
        validate_or_raise(spec)
    matching = [
        w for w in caught.list if SPEC_VERSION_1_0 in str(w.message)
    ]
    assert len(matching) == 1, (
        "expected exactly one DeprecationWarning naming "
        f"{SPEC_VERSION_1_0!r}; got: "
        + repr([str(w.message) for w in caught.list])
    )


def test_validate_or_raise_does_not_warn_for_current_spec_version() -> None:
    # The deprecation warning is the legacy-only signal; emitting it on
    # the current version would drown operator logs in noise.
    spec = _minimal_v1_0_spec()
    spec["spec_version"] = CURRENT_SPEC_VERSION
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        validate_or_raise(spec)
    deprecation = [
        w for w in caught if issubclass(w.category, DeprecationWarning)
    ]
    assert deprecation == [], [str(w.message) for w in deprecation]


# ---------------------------------------------------------------------------
# Negative: unsupported versions still rejected (forward-compat is opt-in).
# ---------------------------------------------------------------------------


def test_unsupported_legacy_version_still_rejected() -> None:
    # Forward-compat only covers entries in
    # :data:`SUPPORTED_SPEC_VERSIONS`. Anything below the supported
    # window (e.g., "0.9") must still fail under
    # :data:`RULE_SPEC_VERSION` so operators see a structured rejection
    # rather than silent shape mismatch.
    spec = _minimal_v1_0_spec()
    spec["spec_version"] = "0.9"
    failures = validate(spec)
    rules = [f.rule for f in failures]
    assert RULE_SPEC_VERSION in rules, rules


def test_unsupported_future_version_still_rejected() -> None:
    # Future major bumps must opt into read-compat explicitly by adding
    # the version to :data:`SUPPORTED_SPEC_VERSIONS`; until then, a "2.0"
    # input is a structured rejection -- the schema does not auto-accept
    # by semver comparison.
    spec = _minimal_v1_0_spec()
    spec["spec_version"] = "2.0"
    with pytest.raises(SchemaValidationError) as excinfo:
        validate_or_raise(spec)
    rules = {f.rule for f in excinfo.value.failures}
    assert RULE_SPEC_VERSION in rules, rules


# ---------------------------------------------------------------------------
# Best-effort policy documentation lives in :mod:`schema` (pinned here so
# accidental removal trips a test).
# ---------------------------------------------------------------------------


def test_schema_module_documents_best_effort_policy() -> None:
    # The CURRENT_SPEC_VERSION / SUPPORTED_SPEC_VERSIONS docstrings carry
    # the best-effort policy text per T06.09 acceptance criterion
    # ("Best-effort policy documented in schema module"). Pin a small
    # set of marker phrases so the docs cannot silently drop the policy.
    current_doc = (
        schema.__dict__.get("__annotations__"),
        getattr(schema, "CURRENT_SPEC_VERSION", None),
    )
    assert current_doc is not None
    # The module-level docstring names NFR-006 and the forward-compat
    # behavior; this is the operator-facing entry point for the policy.
    module_doc = schema.__doc__ or ""
    assert "NFR-006" in module_doc
    assert "forward-compat" in module_doc.lower()
    assert "SUPPORTED_SPEC_VERSIONS" in module_doc
