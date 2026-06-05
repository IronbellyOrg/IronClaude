"""T02.10 -- INV-005 worker-count vs model-pool guard.

Covers both branches of the OQ-007 resolution recorded in
``docs/swarm/oq-resolutions.md``:

    * V1 ``warn-on-exceed-with-defaults`` -- ``pool_policy="warn"``
      (the project default). Preflight logs a WARNING and clamps
      ``workers.count`` down to the pool size; no
      :class:`PreflightError` is raised.
    * V2 ``STOP-before-dispatch`` -- ``pool_policy="stop"``. Preflight
      emits :data:`preflight.RULE_WORKERS_EXCEED_POOL` and aborts
      Wave 0.

The helper-level tests pin :func:`workers_exceed_pool` (detection-only)
and :func:`check_pool_size` (policy-aware emission) so a mutation of
either function is caught without an end-to-end run; the
``run_preflight`` tests then pin the wiring -- clamping, logging, and
manifest stamping for warn mode; structured failure for stop mode.
"""

from __future__ import annotations

import logging
from typing import Any

import pytest

# INV-005 worker-vs-pool guard (T08.03 / NFR-007). Module-level marker
# so every test in this file is selected by ``pytest -m inv``.
pytestmark = pytest.mark.inv

from superclaude.cli.swarm.models import LensEntry
from superclaude.cli.swarm.preflight import (
    DEFAULT_POOL_POLICY,
    RULE_WORKERS_EXCEED_POOL,
    PreflightError,
    check_pool_size,
    run_preflight,
    set_lens_resolver,
    workers_exceed_pool,
)
from superclaude.cli.swarm.schema import (
    CANONICAL_INJECTION_GUARD_SENTENCE,
    CURRENT_SPEC_VERSION,
)

# ---------------------------------------------------------------------------
# Fixtures -- mirror the minimal valid spec used in test_preflight.py so a
# fixture mutation there is mirrored automatically (one source of truth via
# explicit duplication would be ideal but the existing pattern keeps the
# spec dict inline per test module).
# ---------------------------------------------------------------------------


def _minimal_valid_spec() -> dict[str, Any]:
    return {
        "spec_version": CURRENT_SPEC_VERSION,
        "job_id": "job-inv005-001",
        "created": "2026-06-01T00:00:00Z",
        "caller": {
            "skill": "sc-bare-review",
            "skill_version": "1.0.0",
            "invocation_label": "inv005-pool-guard",
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
        "recommended_next_command_substitutions": {"job_id": "job-inv005-001"},
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


@pytest.fixture
def target_loader():
    return lambda _path: b"x" * 120


# ---------------------------------------------------------------------------
# Project default -- pinned so a flip away from V1 warn is loud.
# ---------------------------------------------------------------------------


def test_default_pool_policy_is_warn() -> None:
    assert DEFAULT_POOL_POLICY == "warn"


# ---------------------------------------------------------------------------
# workers_exceed_pool (detection-only)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("workers_count", "pool", "expected"),
    [
        (3, ["a", "b", "c"], False),  # equal
        (2, ["a", "b", "c"], False),  # under
        (4, ["a", "b", "c"], True),  # over
        (5, [], False),  # empty pool -> INV-007 territory
        (1, ["solo"], False),  # singleton equal
        (2, ["solo"], True),  # singleton over
        (2, ["a", "", "b"], False),  # filtered pool size 2 vs 2
        (3, ["a", "", "b", "c"], False),  # filtered pool size 3 vs 3
        (4, ["a", "", "b", "c"], True),  # filtered pool size 3 vs 4
    ],
)
def test_workers_exceed_pool_detection(
    workers_count: int, pool: list[str], expected: bool
) -> None:
    assert workers_exceed_pool(workers_count, pool) is expected


# ---------------------------------------------------------------------------
# check_pool_size -- policy branches
# ---------------------------------------------------------------------------


def test_check_pool_size_stop_emits_failure_on_overage() -> None:
    failures = check_pool_size(5, ["a", "b", "c"], policy="stop")
    assert len(failures) == 1
    assert failures[0].rule == RULE_WORKERS_EXCEED_POOL
    assert failures[0].reason == "workers-exceed-pool"
    assert failures[0].path == "workers.count"
    assert "5" in failures[0].message
    assert "3" in failures[0].message


def test_check_pool_size_warn_returns_empty_on_overage() -> None:
    # Detection-only contract: helper returns [] under warn mode; clamp
    # + warning happen in run_preflight.
    failures = check_pool_size(5, ["a", "b", "c"], policy="warn")
    assert failures == []


def test_check_pool_size_default_policy_is_stop() -> None:
    # Direct callers (tests, validation scripts) get strict-by-default.
    failures = check_pool_size(5, ["a", "b", "c"])
    assert len(failures) == 1
    assert failures[0].rule == RULE_WORKERS_EXCEED_POOL


def test_check_pool_size_passes_when_equal_under_both_policies() -> None:
    assert check_pool_size(3, ["a", "b", "c"], policy="warn") == []
    assert check_pool_size(3, ["a", "b", "c"], policy="stop") == []


def test_check_pool_size_skips_empty_pool_under_both_policies() -> None:
    # INV-007 reports empty pool; INV-005 stays silent regardless of policy.
    assert check_pool_size(5, [], policy="warn") == []
    assert check_pool_size(5, [], policy="stop") == []


def test_check_pool_size_rejects_unknown_policy() -> None:
    with pytest.raises(ValueError, match="must be 'warn' or 'stop'"):
        check_pool_size(5, ["a", "b", "c"], policy="bogus")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# run_preflight wiring -- end-to-end OQ-007 branches.
# ---------------------------------------------------------------------------


def test_run_preflight_warn_mode_clamps_and_logs(
    lens_resolver_stub, target_loader, caplog: pytest.LogCaptureFixture
) -> None:
    spec = _minimal_valid_spec()
    spec["workers"]["count"] = 7  # pool size 3
    with caplog.at_level(
        logging.WARNING, logger="superclaude.cli.swarm.preflight"
    ):
        result = run_preflight(
            spec, target_loader=target_loader, pool_policy="warn"
        )

    # No PreflightError raised -- success path.
    assert result.state.state == "preflight_ok"

    # Manifest reports the clamped count (post-clamp workers_requested).
    assert result.manifest.preflight.workers_requested == 3

    # Warning emitted with the canonical INV-005 / OQ-007 phrasing.
    warnings = [
        rec
        for rec in caplog.records
        if rec.levelno == logging.WARNING
        and "INV-005" in rec.getMessage()
    ]
    assert len(warnings) == 1
    msg = warnings[0].getMessage()
    assert "OQ-007" in msg
    assert "warn-with-defaults" in msg
    assert "7" in msg  # original
    assert "3" in msg  # pool size + clamped value


def test_run_preflight_default_policy_warns_not_stops(
    lens_resolver_stub, target_loader, caplog: pytest.LogCaptureFixture
) -> None:
    # Pinning V1 warn-with-defaults as the project-default behavior:
    # callers that do not pass ``pool_policy`` get the clamp + warning,
    # not a PreflightError.
    spec = _minimal_valid_spec()
    spec["workers"]["count"] = 5  # pool size 3
    with caplog.at_level(
        logging.WARNING, logger="superclaude.cli.swarm.preflight"
    ):
        result = run_preflight(spec, target_loader=target_loader)
    assert result.state.state == "preflight_ok"
    assert result.manifest.preflight.workers_requested == 3


def test_run_preflight_stop_mode_raises_with_inv005(
    lens_resolver_stub, target_loader
) -> None:
    spec = _minimal_valid_spec()
    spec["workers"]["count"] = 5
    with pytest.raises(PreflightError) as excinfo:
        run_preflight(spec, target_loader=target_loader, pool_policy="stop")
    rules = {f.rule for f in excinfo.value.failures}
    assert RULE_WORKERS_EXCEED_POOL in rules
    failure = next(
        f
        for f in excinfo.value.failures
        if f.rule == RULE_WORKERS_EXCEED_POOL
    )
    assert failure.reason == "workers-exceed-pool"
    assert failure.path == "workers.count"


def test_run_preflight_warn_mode_silent_when_within_pool(
    lens_resolver_stub, target_loader, caplog: pytest.LogCaptureFixture
) -> None:
    spec = _minimal_valid_spec()
    spec["workers"]["count"] = 3  # equal to pool size
    with caplog.at_level(
        logging.WARNING, logger="superclaude.cli.swarm.preflight"
    ):
        result = run_preflight(
            spec, target_loader=target_loader, pool_policy="warn"
        )
    assert result.manifest.preflight.workers_requested == 3
    assert not any(
        "INV-005" in rec.getMessage() for rec in caplog.records
    )


def test_run_preflight_stop_mode_silent_when_within_pool(
    lens_resolver_stub, target_loader
) -> None:
    spec = _minimal_valid_spec()
    spec["workers"]["count"] = 2  # under pool size
    result = run_preflight(
        spec, target_loader=target_loader, pool_policy="stop"
    )
    assert result.state.state == "preflight_ok"
    assert result.manifest.preflight.workers_requested == 2
