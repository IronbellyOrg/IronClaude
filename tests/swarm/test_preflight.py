"""T02.02 -- ``cli/swarm/preflight.py`` Wave 0 entrypoint tests.

Covers the COMP-006 acceptance criteria:

    * ``run_preflight`` resolves a registered lens, materializes the
      snapshot, stamps the Manifest with ``preflight.target_checksum``,
      ``preflight.workers_requested``, ``preflight.transport_kind``,
      and sets ``SwarmState.state == "preflight_ok"``.
    * Schema validation, §11.5 guard, IMM-4 empty-target guard,
      INV-005 worker-vs-pool guard, INV-007 empty-pool guard each have
      a call site that raises :class:`PreflightError` on violation.
    * On success the returned Manifest matches the input verbatim;
      ``write_manifest`` round-trips byte-identically (INV-016).

T02.04 (FR-020 default expansion), T02.07 (central §11.5 guard across
the three prompt paths), T02.10 (OQ-007 resolution), T02.11 (OQ-008
structured failed contract), T02.13 (truncation-aware IMM-4 check) each
own a more targeted test module; T02.02 verifies only the skeleton
contract and the wiring.
"""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

import pytest

from superclaude.cli.swarm import preflight
from superclaude.cli.swarm.models import (
    LensEntry,
    Manifest,
    PreflightSummary,
    ResolvedLensEntry,
    SwarmState,
    from_json,
    to_json,
)
from superclaude.cli.swarm.preflight import (
    MIN_TARGET_NON_WHITESPACE_BYTES,
    RULE_EMPTY_POOL,
    RULE_INJECTION_GUARD,
    RULE_TARGET_TOO_SMALL,
    RULE_TARGET_UNREADABLE,
    RULE_UNKNOWN_LENS,
    RULE_WORKERS_EXCEED_POOL,
    PreflightError,
    PreflightFailure,
    PreflightResult,
    check_empty_pool,
    check_pool_size,
    enforce_injection_guard,
    guard_empty_target,
    materialize_lens_defaults,
    run_preflight,
    set_lens_resolver,
)
from superclaude.cli.swarm.schema import (
    CANONICAL_INJECTION_GUARD_SENTENCE,
    CURRENT_SPEC_VERSION,
    RULE_INJECTION_SUBSTRING,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _minimal_valid_spec() -> dict[str, Any]:
    """A schema-valid JobSpec dict; mirrors tests/swarm/test_schema.py."""
    return {
        "spec_version": CURRENT_SPEC_VERSION,
        "job_id": "job-preflight-001",
        "created": "2026-06-01T00:00:00Z",
        "caller": {
            "skill": "sc-bare-review",
            "skill_version": "1.0.0",
            "invocation_label": "preflight-T02.02-smoke",
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
        "recommended_next_command_substitutions": {"job_id": "job-preflight-001"},
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
    """A minimal LensEntry standing in for the T02.14 registry entry."""
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
    """Install a stub lens resolver for the duration of the test."""
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


@pytest.fixture
def long_target_bytes() -> bytes:
    """Payload comfortably above the IMM-4 byte floor."""
    return b"x" * (MIN_TARGET_NON_WHITESPACE_BYTES + 10)


@pytest.fixture
def target_loader(long_target_bytes):
    return lambda _path: long_target_bytes


# ---------------------------------------------------------------------------
# Module surface
# ---------------------------------------------------------------------------


def test_public_surface() -> None:
    expected = {
        "CANONICAL_FILENAME_TEMPLATE",
        "DEFAULT_CLOSE_DELIM",
        "DEFAULT_OPEN_DELIM",
        "DEFAULT_POOL_POLICY",
        "ENV_MISSING_CONTRACT_FILENAME",
        "ENV_MISSING_REASON",
        "MIN_TARGET_NON_WHITESPACE_BYTES",
        "PoolPolicy",
        "PreflightError",
        "PreflightFailure",
        "PreflightResult",
        "RULE_CUSTOM_PROMPT_DIR_META_INVALID",
        "RULE_CUSTOM_PROMPT_DIR_MISSING",
        "RULE_EMPTY_POOL",
        "RULE_INJECTION_GUARD",
        "RULE_TARGET_TOO_SMALL",
        "RULE_TARGET_UNREADABLE",
        "RULE_UNKNOWN_LENS",
        "RULE_WORKERS_EXCEED_POOL",
        "auto_inject_guard",
        "check_empty_pool",
        "check_pool_size",
        "emit_env_missing_contract",
        "emit_manifest",
        "enforce_injection_guard",
        "expand_lens_defaults",
        "guard_empty_target",
        "materialize_lens_defaults",
        "read_custom_prompt_dir",
        "resolve_caller_metadata",
        "resolve_lens",
        "resume_mode",
        "run_preflight",
        "set_lens_resolver",
        "workers_exceed_pool",
        "wrap_target_with_delimiters",
        "write_manifest",
        "truncate_target",
    }
    assert set(preflight.__all__) == expected


def test_byte_floor_constant_matches_imm4() -> None:
    assert MIN_TARGET_NON_WHITESPACE_BYTES == 50


# ---------------------------------------------------------------------------
# Wave-0 happy path
# ---------------------------------------------------------------------------


def test_run_preflight_returns_manifest_and_state(
    lens_resolver_stub, target_loader, long_target_bytes
) -> None:
    spec = _minimal_valid_spec()
    result = run_preflight(spec, target_loader=target_loader)
    assert isinstance(result, PreflightResult)
    # Manifest snapshot pinning.
    assert isinstance(result.manifest, Manifest)
    assert result.manifest.contract_version == "1.0"
    assert result.manifest.job_id == "job-preflight-001"
    assert isinstance(result.manifest.resolved_lens_entry, ResolvedLensEntry)
    assert result.manifest.resolved_lens_entry.name == "bare-review"
    # PreflightSummary triple stamped at Wave 0.
    summary = result.manifest.preflight
    assert isinstance(summary, PreflightSummary)
    assert summary.workers_requested == 3
    assert summary.transport_kind == "openai_compat"
    # sha256 of the loaded target.
    import hashlib

    assert summary.target_checksum == hashlib.sha256(long_target_bytes).hexdigest()
    # SwarmState init.
    assert isinstance(result.state, SwarmState)
    assert result.state.state == "preflight_ok"
    assert result.state.job_id == "job-preflight-001"
    # No on-disk write requested.
    assert result.manifest_path is None


def test_run_preflight_accepts_jobspec_instance(
    lens_resolver_stub, target_loader
) -> None:
    spec = _minimal_valid_spec()
    from superclaude.cli.swarm.models import JobSpec, from_dict

    job = from_dict(JobSpec, spec)
    result = run_preflight(job, target_loader=target_loader)
    assert result.state.state == "preflight_ok"


def test_run_preflight_writes_manifest_atomically(
    tmp_path, lens_resolver_stub, target_loader
) -> None:
    spec = _minimal_valid_spec()
    result = run_preflight(
        spec, target_loader=target_loader, output_dir=tmp_path
    )
    assert result.manifest_path is not None
    written = Path(result.manifest_path)
    assert written.exists()
    assert written.name == "manifest.json"
    # No leftover tmp files (atomic write cleanup).
    leftovers = [p for p in tmp_path.iterdir() if p.name.startswith(".manifest-")]
    assert leftovers == []
    # Byte-identical round-trip (INV-016).
    payload = written.read_text(encoding="utf-8")
    restored = from_json(Manifest, payload)
    assert restored == result.manifest
    assert payload == to_json(result.manifest)


# ---------------------------------------------------------------------------
# Guard call sites (one targeted test per guard)
# ---------------------------------------------------------------------------


def test_schema_failure_raises_with_propagated_rule(
    lens_resolver_stub, target_loader
) -> None:
    spec = _minimal_valid_spec()
    spec["spec_version"] = "0.9"  # wrong version
    with pytest.raises(PreflightError) as excinfo:
        run_preflight(spec, target_loader=target_loader)
    rules = {f.rule for f in excinfo.value.failures}
    assert any(rule == "spec_version.pinned" for rule in rules)
    assert all(f.reason == "schema-invalid" for f in excinfo.value.failures)


def test_schema_missing_injection_substring_is_reported(
    lens_resolver_stub, target_loader
) -> None:
    spec = _minimal_valid_spec()
    spec["prompt"]["system"] = "You are a reviewer. No guard here."
    with pytest.raises(PreflightError) as excinfo:
        run_preflight(spec, target_loader=target_loader)
    assert any(
        f.rule == RULE_INJECTION_SUBSTRING for f in excinfo.value.failures
    )


def test_unknown_lens_raises_lens_unknown(target_loader) -> None:
    spec = _minimal_valid_spec()
    spec["lens"] = "no-such-lens"
    # Use an empty registry so resolution fails.
    previous = set_lens_resolver(lambda _name: (_ for _ in ()).throw(KeyError(_name)))
    try:
        with pytest.raises(PreflightError) as excinfo:
            run_preflight(spec, target_loader=target_loader)
    finally:
        set_lens_resolver(previous)
    assert [f.rule for f in excinfo.value.failures] == [RULE_UNKNOWN_LENS]
    assert excinfo.value.failures[0].reason == "lens-unknown"


def test_empty_target_triggers_imm4(lens_resolver_stub) -> None:
    spec = _minimal_valid_spec()
    # 49 non-whitespace bytes (one below the floor).
    payload = b"a" * (MIN_TARGET_NON_WHITESPACE_BYTES - 1)
    with pytest.raises(PreflightError) as excinfo:
        run_preflight(spec, target_loader=lambda _p: payload)
    rules = [f.rule for f in excinfo.value.failures]
    assert RULE_TARGET_TOO_SMALL in rules


def test_whitespace_only_target_triggers_imm4(lens_resolver_stub) -> None:
    spec = _minimal_valid_spec()
    payload = b" \t\n" * 200  # plenty of bytes, zero non-whitespace
    with pytest.raises(PreflightError) as excinfo:
        run_preflight(spec, target_loader=lambda _p: payload)
    assert RULE_TARGET_TOO_SMALL in {f.rule for f in excinfo.value.failures}


def test_unreadable_target_path_is_structured(lens_resolver_stub) -> None:
    spec = _minimal_valid_spec()

    def loader(_path: str) -> bytes:
        raise FileNotFoundError(2, "No such file or directory", _path)

    with pytest.raises(PreflightError) as excinfo:
        run_preflight(spec, target_loader=loader)
    assert RULE_TARGET_UNREADABLE in {f.rule for f in excinfo.value.failures}


def test_workers_exceed_pool_triggers_inv005(
    lens_resolver_stub, target_loader
) -> None:
    # T02.10 / OQ-007 V2 STOP branch: ``pool_policy="stop"`` makes the
    # preflight raise on overage. The V1 ``warn`` default branch is
    # covered in tests/swarm/test_inv005_pool_guard.py.
    spec = _minimal_valid_spec()
    spec["workers"]["count"] = 5  # pool only has 3 models
    with pytest.raises(PreflightError) as excinfo:
        run_preflight(spec, target_loader=target_loader, pool_policy="stop")
    rules = {f.rule for f in excinfo.value.failures}
    assert RULE_WORKERS_EXCEED_POOL in rules
    failure = next(
        f for f in excinfo.value.failures if f.rule == RULE_WORKERS_EXCEED_POOL
    )
    assert failure.reason == "workers-exceed-pool"


def test_empty_pool_triggers_inv007(lens_resolver_stub, target_loader) -> None:
    spec = _minimal_valid_spec()
    spec["workers"]["models"] = []
    with pytest.raises(PreflightError) as excinfo:
        run_preflight(spec, target_loader=target_loader)
    rules = [f.rule for f in excinfo.value.failures]
    assert RULE_EMPTY_POOL in rules
    # INV-007 wins -- INV-005 must not double-report when pool is empty.
    assert RULE_WORKERS_EXCEED_POOL not in rules


def test_injection_guard_helper_rejects_missing_substring() -> None:
    failures = enforce_injection_guard(
        system="reviewer prompt without the marker",
        required_substring=CANONICAL_INJECTION_GUARD_SENTENCE,
    )
    assert len(failures) == 1
    assert failures[0].rule == RULE_INJECTION_GUARD
    assert failures[0].reason == "injection-guard"


def test_injection_guard_helper_skips_empty_required_substring() -> None:
    assert enforce_injection_guard(system="anything", required_substring="") == []


def test_guard_empty_target_counts_non_whitespace_only() -> None:
    # 50 non-whitespace bytes interleaved with whitespace passes.
    payload = (b"a " * MIN_TARGET_NON_WHITESPACE_BYTES).rstrip()
    assert guard_empty_target(payload) == []


def test_check_pool_size_passes_when_equal() -> None:
    assert check_pool_size(3, ["a", "b", "c"]) == []


def test_check_empty_pool_passes_with_one_model() -> None:
    assert check_empty_pool(["m1"]) == []


# ---------------------------------------------------------------------------
# Lens resolution + materialization
# ---------------------------------------------------------------------------


def test_materialize_lens_defaults_returns_resolved_snapshot() -> None:
    lens = _bare_review_lens()
    from superclaude.cli.swarm.models import JobSpec

    snapshot = materialize_lens_defaults(JobSpec(), lens)
    assert isinstance(snapshot, ResolvedLensEntry)
    assert snapshot.name == lens.name
    assert snapshot.recipe_name == lens.recipe_name
    assert snapshot.suspect is True
    assert snapshot.tier == "T2"


def test_set_lens_resolver_round_trips() -> None:
    sentinel = _bare_review_lens()

    def resolver(_name: str) -> LensEntry:
        return sentinel

    previous = set_lens_resolver(resolver)
    try:
        assert preflight.resolve_lens("anything") is sentinel
    finally:
        restored = set_lens_resolver(previous)
        assert restored is resolver


# ---------------------------------------------------------------------------
# Failure-contract shape
# ---------------------------------------------------------------------------


def test_preflight_error_requires_at_least_one_failure() -> None:
    with pytest.raises(ValueError):
        PreflightError([])


def test_preflight_failure_is_frozen() -> None:
    failure = PreflightFailure(
        rule="x", path="y", message="z", reason="q"
    )
    with pytest.raises(Exception):
        failure.rule = "renamed"  # type: ignore[misc]


def test_run_preflight_does_not_mutate_input_spec(
    lens_resolver_stub, target_loader
) -> None:
    spec = _minimal_valid_spec()
    original = copy.deepcopy(spec)
    run_preflight(spec, target_loader=target_loader)
    assert spec == original
