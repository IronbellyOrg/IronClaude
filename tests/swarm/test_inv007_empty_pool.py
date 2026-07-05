"""T02.11 -- INV-007 / OQ-008 empty-pool failure contract.

Covers both OQ-008 branches recorded in
``docs/swarm/oq-resolutions.md``:

    * **Output dir creatable** -- ``emit_env_missing_contract`` writes
      ``<job.output.dir>/return-contract.yaml`` carrying
      ``status: "failed"`` + ``reason: "env-missing"`` and returns the
      absolute path. :func:`run_preflight` attaches that path to the
      raised :class:`PreflightError`.
    * **Output dir NOT creatable** -- ``emit_env_missing_contract``
      returns ``None`` (bare abort); no file is written. The
      :class:`PreflightError` still surfaces :data:`RULE_EMPTY_POOL`
      so callers see the failure mode.

Helper-level tests pin :func:`emit_env_missing_contract` directly
(creatable, empty ``output.dir``, mkdir-fails) so a regression of the
write logic is caught without an end-to-end preflight run. The
``run_preflight`` tests then pin the wiring -- the empty-pool path
calls the emitter and attaches the resulting path to
:class:`PreflightError.env_missing_contract_path`.
"""

# ruff: noqa: E402 -- module-level ``pytestmark`` intentionally precedes the
# superclaude imports so the marker is registered before collection.

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
import yaml

# INV-007 empty-pool failure (T08.03 / NFR-007). Module-level marker so
# every test in this file is selected by ``pytest -m inv``.
pytestmark = pytest.mark.inv

from superclaude.cli.swarm.models import JobSpec, LensEntry, from_dict
from superclaude.cli.swarm.preflight import (
    ENV_MISSING_CONTRACT_FILENAME,
    ENV_MISSING_REASON,
    RULE_EMPTY_POOL,
    RULE_WORKERS_EXCEED_POOL,
    PreflightError,
    PreflightFailure,
    check_empty_pool,
    emit_env_missing_contract,
    run_preflight,
    set_lens_resolver,
)
from superclaude.cli.swarm.schema import (
    CANONICAL_INJECTION_GUARD_SENTENCE,
    CURRENT_SPEC_VERSION,
)

# ---------------------------------------------------------------------------
# Fixtures -- mirror the minimal valid spec used in the rest of the
# preflight test suite so a fixture mutation there is mirrored
# automatically. Inline rather than shared to keep the test module
# self-contained (matches the existing pattern in test_inv005_pool_guard.py).
# ---------------------------------------------------------------------------


def _minimal_valid_spec(output_dir: str) -> dict[str, Any]:
    return {
        "spec_version": CURRENT_SPEC_VERSION,
        "job_id": "job-inv007-001",
        "created": "2026-06-01T00:00:00Z",
        "caller": {
            "skill": "sc-bare-review",
            "skill_version": "1.0.0",
            "invocation_label": "inv007-empty-pool",
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
            "dir": output_dir,
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
        "recommended_next_command_substitutions": {"job_id": "job-inv007-001"},
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
# check_empty_pool -- the detection helper.
# ---------------------------------------------------------------------------


def test_check_empty_pool_emits_env_missing_reason_on_empty() -> None:
    failures = check_empty_pool([])
    assert len(failures) == 1
    assert failures[0].rule == RULE_EMPTY_POOL
    assert failures[0].reason == ENV_MISSING_REASON
    assert failures[0].path == "workers.models"


def test_check_empty_pool_filters_empty_strings() -> None:
    # Pool of [""], [" "], etc. is treated as empty -- env-missing.
    failures = check_empty_pool(["", ""])
    assert len(failures) == 1
    assert failures[0].rule == RULE_EMPTY_POOL


def test_check_empty_pool_passes_with_one_model() -> None:
    assert check_empty_pool(["solo"]) == []


# ---------------------------------------------------------------------------
# emit_env_missing_contract -- direct helper tests covering both OQ-008
# branches without an end-to-end run.
# ---------------------------------------------------------------------------


def _build_jobspec(output_dir: str) -> JobSpec:
    return from_dict(JobSpec, _minimal_valid_spec(output_dir))


def test_emit_env_missing_contract_creates_dir_and_writes_yaml(
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "swarm-out"  # does not exist yet -- must be created
    job = _build_jobspec(str(output_dir))
    failures = check_empty_pool([])

    contract_path = emit_env_missing_contract(job, failures=failures)

    assert contract_path is not None
    assert Path(contract_path).is_file()
    assert Path(contract_path).name == ENV_MISSING_CONTRACT_FILENAME
    assert Path(contract_path).parent == output_dir.resolve()

    payload = yaml.safe_load(Path(contract_path).read_text(encoding="utf-8"))
    # Status + reason classifier -- the IMM-5 ``failed`` terminal status
    # plus the INV-007 / OQ-008 token.
    assert payload["status"] == "failed"
    assert payload["reason"] == ENV_MISSING_REASON
    # IMM-5 / DM-012 alignment.
    assert payload["contract_version"] == "1.0"
    assert payload["job_id"] == job.job_id
    assert payload["workers_requested"] == job.workers.count
    assert payload["workers_succeeded"] == 0
    assert payload["workers_failed"] == 0
    assert payload["output_files"] == []
    assert payload["merged_path"] is None
    # Caller record copied verbatim.
    assert payload["caller"]["skill"] == job.caller.skill
    assert payload["caller"]["skill_version"] == job.caller.skill_version
    # Lens record stamped.
    assert payload["lens"] == job.lens
    # PreflightFailure list embedded so callers see every failing rule.
    failure_list = payload["preflight_failures"]
    assert isinstance(failure_list, list) and len(failure_list) == 1
    assert failure_list[0]["rule"] == RULE_EMPTY_POOL
    assert failure_list[0]["reason"] == ENV_MISSING_REASON


def test_emit_env_missing_contract_returns_none_when_output_dir_empty(
    tmp_path: Path,
) -> None:
    job = _build_jobspec("")  # empty output.dir -> bare abort branch
    contract_path = emit_env_missing_contract(job, failures=check_empty_pool([]))
    assert contract_path is None
    # No stray file under tmp_path either -- bare abort is silent.
    assert list(tmp_path.iterdir()) == []


def test_emit_env_missing_contract_returns_none_when_mkdir_fails(
    tmp_path: Path,
) -> None:
    # Plant a file at the parent path so mkdir-with-parents fails on
    # NotADirectoryError -- the OQ-008 "output dir not creatable" branch.
    blocker = tmp_path / "blocker"
    blocker.write_text("not a directory", encoding="utf-8")
    uncreatable = blocker / "subdir"

    job = _build_jobspec(str(uncreatable))
    contract_path = emit_env_missing_contract(job, failures=check_empty_pool([]))
    assert contract_path is None
    # The blocker file is untouched -- bare abort writes nothing.
    assert blocker.is_file()
    assert blocker.read_text(encoding="utf-8") == "not a directory"


def test_emit_env_missing_contract_idempotent_on_existing_dir(
    tmp_path: Path,
) -> None:
    # mkdir(parents=True, exist_ok=True) must not fail when the directory
    # already exists -- otherwise resume / retry on a partially-emitted
    # job would surface the wrong failure mode.
    output_dir = tmp_path / "out"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "pre-existing.txt").write_text("keep me", encoding="utf-8")

    job = _build_jobspec(str(output_dir))
    contract_path = emit_env_missing_contract(job, failures=check_empty_pool([]))

    assert contract_path is not None
    assert (output_dir / ENV_MISSING_CONTRACT_FILENAME).is_file()
    # Pre-existing sibling files survive the contract write.
    assert (output_dir / "pre-existing.txt").read_text(encoding="utf-8") == "keep me"


def test_emit_env_missing_contract_atomic_write_no_tmp_left(
    tmp_path: Path,
) -> None:
    # The atomic write path uses write-to-tmp + os.replace; assert that no
    # ``.return-contract-*.yaml.tmp`` files are left under ``output.dir``
    # after a successful write (otherwise resume + listdir would see
    # ghost files).
    output_dir = tmp_path / "out"
    job = _build_jobspec(str(output_dir))
    contract_path = emit_env_missing_contract(job, failures=check_empty_pool([]))

    assert contract_path is not None
    leftovers = [
        p
        for p in Path(output_dir).iterdir()
        if p.name.startswith(".return-contract-") and p.name.endswith(".tmp")
    ]
    assert leftovers == []


# ---------------------------------------------------------------------------
# run_preflight wiring -- end-to-end OQ-008 branches.
# ---------------------------------------------------------------------------


def test_run_preflight_empty_pool_writes_contract_when_dir_creatable(
    lens_resolver_stub, target_loader, tmp_path: Path
) -> None:
    output_dir = tmp_path / "swarm-out"
    spec = _minimal_valid_spec(str(output_dir))
    spec["workers"]["models"] = []  # trigger INV-007

    with pytest.raises(PreflightError) as excinfo:
        run_preflight(spec, target_loader=target_loader)

    rules = {f.rule for f in excinfo.value.failures}
    assert RULE_EMPTY_POOL in rules
    # INV-005 must not double-report; the empty-pool guard wins.
    assert RULE_WORKERS_EXCEED_POOL not in rules

    # The structured contract was emitted at the expected path and
    # attached to PreflightError for diagnostics.
    contract_path = excinfo.value.env_missing_contract_path
    assert contract_path is not None
    assert Path(contract_path).is_file()
    assert Path(contract_path).name == ENV_MISSING_CONTRACT_FILENAME

    payload = yaml.safe_load(Path(contract_path).read_text(encoding="utf-8"))
    assert payload["status"] == "failed"
    assert payload["reason"] == ENV_MISSING_REASON
    assert payload["job_id"] == spec["job_id"]


def test_run_preflight_empty_pool_bare_abort_when_dir_uncreatable(
    lens_resolver_stub, target_loader, tmp_path: Path
) -> None:
    # OQ-008 bare-abort branch -- output.dir is under a file, so mkdir
    # raises NotADirectoryError and the emitter returns None.
    blocker = tmp_path / "blocker.txt"
    blocker.write_text("not a directory", encoding="utf-8")
    uncreatable = blocker / "subdir"

    spec = _minimal_valid_spec(str(uncreatable))
    spec["workers"]["models"] = []  # trigger INV-007

    with pytest.raises(PreflightError) as excinfo:
        run_preflight(spec, target_loader=target_loader)

    rules = {f.rule for f in excinfo.value.failures}
    assert RULE_EMPTY_POOL in rules
    # No contract path attached -- the bare-abort branch returns None.
    assert excinfo.value.env_missing_contract_path is None
    # The blocker file is untouched.
    assert blocker.is_file()


def test_run_preflight_non_empty_pool_skips_env_missing_emission(
    lens_resolver_stub, target_loader, tmp_path: Path
) -> None:
    # A successful preflight must not emit return-contract.yaml -- that
    # path is reserved for the failure / reduce branches. The empty-pool
    # branch is the only Wave-0 trigger for env-missing emission.
    output_dir = tmp_path / "out"
    spec = _minimal_valid_spec(str(output_dir))
    result = run_preflight(spec, target_loader=target_loader)

    assert result.state.state == "preflight_ok"
    # If output_dir does not exist, no env-missing emission happened.
    assert not (output_dir / ENV_MISSING_CONTRACT_FILENAME).exists()


def test_preflight_error_carries_no_contract_path_for_non_env_missing_failures(
    lens_resolver_stub, target_loader, tmp_path: Path
) -> None:
    # A non-INV-007 failure (e.g. IMM-4 empty target) must not trigger
    # env-missing emission; ``env_missing_contract_path`` stays None.
    output_dir = tmp_path / "out"
    spec = _minimal_valid_spec(str(output_dir))

    def short_loader(_path: str) -> bytes:
        return b"x"  # 1 non-ws byte -- below IMM-4 floor

    with pytest.raises(PreflightError) as excinfo:
        run_preflight(spec, target_loader=short_loader)

    assert excinfo.value.env_missing_contract_path is None
    # No return-contract.yaml left under output_dir either.
    if output_dir.exists():
        assert not (output_dir / ENV_MISSING_CONTRACT_FILENAME).exists()


# ---------------------------------------------------------------------------
# PreflightError shape -- back-compat for non-env-missing constructors.
# ---------------------------------------------------------------------------


def test_preflight_error_default_env_missing_contract_path_is_none() -> None:
    failure = PreflightFailure(
        rule=RULE_EMPTY_POOL,
        path="workers.models",
        message="empty",
        reason=ENV_MISSING_REASON,
    )
    err = PreflightError([failure])
    assert err.env_missing_contract_path is None
    assert err.failures == [failure]


def test_preflight_error_accepts_explicit_contract_path(
    tmp_path: Path,
) -> None:
    failure = PreflightFailure(
        rule=RULE_EMPTY_POOL,
        path="workers.models",
        message="empty",
        reason=ENV_MISSING_REASON,
    )
    contract_path = str(tmp_path / "return-contract.yaml")
    err = PreflightError([failure], env_missing_contract_path=contract_path)
    assert err.env_missing_contract_path == contract_path
