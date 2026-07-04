"""FR-RH2 ensemble unit coverage accumulated across implementation phases."""

from __future__ import annotations

import inspect
from pathlib import Path

import pytest

from superclaude.cli.reflect.commands import reflect_group
from superclaude.cli.reflect.config import resolve_config
from superclaude.cli.reflect.contract import (
    _VERIFICATION_SKIP_EXEMPTIONS,
    _degraded_reason,
    derive_verdict,
)
from superclaude.cli.reflect.ensemble import (
    _vendor_from_model_id,
    build_adversarial_prompt,
    build_reflect_contract,
    compute_model_class_diversity,
    resolve_t2_transport_factory,
    stub_model_id,
)
from superclaude.cli.reflect.models import Verdict
from superclaude.cli.swarm.commands import ModelPoolTooSmallError
from superclaude.cli.swarm.lenses import LENS_NAMES, LENSES
from superclaude.cli.swarm.lenses._validate import validate_lens
from superclaude.cli.swarm.lenses.reflect_review import LENS as REFLECT_REVIEW_LENS
from superclaude.cli.swarm.merge import mechanical_merge
from superclaude.cli.swarm.models import WorkerResult

FORBIDDEN_MODEL_LITERALS = ("claude", "anthropic", "sonnet", "opus", "haiku")
T2_ENV_2 = {
    "T2ProxyUrl": "http://proxy.example/cli/v1",
    "T2ProxyKey": "sk-test",
    "T2Model01": "model-a",
    "T2Model02": "model-b",
}
T2_ENV_3 = {
    **T2_ENV_2,
    "T2Model03": "model-c",
}


def test_u1_reflect_review_lens_registered_and_valid() -> None:
    """U1: reflect-review is registered and passes the bare-review validator gate."""
    assert "reflect-review" in LENS_NAMES
    assert LENSES["reflect-review"] is REFLECT_REVIEW_LENS

    other_names = [name for name in LENS_NAMES if name != "reflect-review"]
    assert validate_lens(REFLECT_REVIEW_LENS, other_names=other_names) is None


def test_u2_reflect_review_lens_workers_and_model_pool_source() -> None:
    """U2: reflect-review uses 2-4 workers and no hard-coded model family."""
    lens = REFLECT_REVIEW_LENS
    assert 2 <= lens.default_workers <= 4
    assert lens.name == "reflect-review"
    assert lens.tier == "T2"
    assert lens.suspect is True
    assert "/sc:adversarial" in lens.recommended_next_command_template
    assert "{suspect_files}" in lens.recommended_next_command_template

    model_source_fields = {
        "name": lens.name,
        "description": lens.description,
        "system_prompt_fragment": lens.system_prompt_fragment,
        "user_template": lens.user_template,
        "recipe_name": lens.recipe_name,
        "normalizer_strategy": lens.normalizer_strategy,
        "recommended_next_command_template": lens.recommended_next_command_template,
        "acceptance_notes": lens.acceptance_notes,
        "tier": lens.tier,
    }
    offenders = [
        (name, token)
        for name, value in model_source_fields.items()
        for token in FORBIDDEN_MODEL_LITERALS
        if token in value.lower()
    ]
    assert offenders == []


def test_transport_unknown_value_rejected_at_click_parse(
    cli_runner, temp_tasklist
) -> None:
    """Transport enum rejects unknown values before config resolution or dispatch."""
    result = cli_runner.invoke(
        reflect_group,
        ["run", str(temp_tasklist), "--transport", "bogus", "--print-command"],
    )

    assert result.exit_code != 0
    assert "Invalid value for '--transport'" in result.output


def test_reviewers_one_is_preserved_before_clamp(temp_tasklist, patch_git) -> None:
    """Q8: reviewers=1 reaches the negative-witness path unclamped."""
    config = resolve_config(
        str(temp_tasklist), depth="standard", model="test-model", reviewers=1
    )
    assert config.reviewers == 1


def test_reviewers_outside_normal_range_clamp_to_two_four(
    temp_tasklist, patch_git
) -> None:
    """Normal reviewers values clamp to [2,4] after the reviewers=1 sentinel."""
    low = resolve_config(
        str(temp_tasklist), depth="standard", model="test-model", reviewers=0
    )
    high = resolve_config(
        str(temp_tasklist), depth="standard", model="test-model", reviewers=5
    )

    assert low.reviewers == 2
    assert high.reviewers == 4


def test_transport_resolves_default_and_stub(temp_tasklist, patch_git) -> None:
    """Transport defaults to openai_compat and preserves explicit stub."""
    default = resolve_config(str(temp_tasklist), depth="standard", model="test-model")
    stub = resolve_config(
        str(temp_tasklist), depth="standard", model="test-model", transport="stub"
    )

    assert default.transport == "openai_compat"
    assert stub.transport == "stub"


def test_u3_openai_and_stub_factories_bind_distinct_slot_models() -> None:
    """U3: slot i binds to distinct T2Model0N / stub model ids."""
    openai_factory = resolve_t2_transport_factory(
        "openai_compat", reviewers=3, env=T2_ENV_3
    )
    openai_models = [openai_factory(i)._model for i in range(3)]

    stub_factory = resolve_t2_transport_factory("stub", reviewers=3)
    stub_models = [stub_factory(i).model for i in range(3)]

    assert openai_models == ["model-a", "model-b", "model-c"]
    assert len(set(openai_models)) == 3
    # Stub slots bind distinct, VENDOR-distinct model ids so a stub run is
    # PASS-eligible on both model-class and vendor diversity.
    assert stub_models == [stub_model_id(0), stub_model_id(1), stub_model_id(2)]
    assert len(set(stub_models)) == 3
    assert len({_vendor_from_model_id(m) for m in stub_models}) == 3


def test_u4_model_pool_too_small_raises_eagerly() -> None:
    """U4: pool=2, reviewers=3 raises before any worker dispatch."""
    with pytest.raises(ModelPoolTooSmallError) as excinfo:
        resolve_t2_transport_factory("openai_compat", reviewers=3, env=T2_ENV_2)

    err = excinfo.value
    assert err.pool_size == 2
    assert err.workers_requested == 3
    assert "2 model(s)" in str(err) and "3 worker(s)" in str(err)


def test_u5_model_class_diversity_uses_succeeded_worker_model_ids() -> None:
    """U5: diversity counts distinct succeeded model_id values, not aliases or N."""
    workers = [
        WorkerResult(index=0, status="success", model_id="model-a"),
        WorkerResult(index=1, status="success", model_id="model-b"),
        WorkerResult(index=2, status="proxy_error", model_id="model-c"),
    ]
    duplicate_survivors = [
        WorkerResult(index=0, status="success", model_id="model-a"),
        WorkerResult(index=1, status="success", model_id="model-a"),
        WorkerResult(index=2, status="proxy_error", model_id="model-c"),
    ]

    contract = build_reflect_contract(workers, adversarial_convergence_score=0.86)

    assert compute_model_class_diversity(workers) == "full"
    assert contract is not None
    assert contract["t2_model_class_diversity"] == "full"
    assert compute_model_class_diversity(duplicate_survivors) != "full"


def test_u6_verdict_map_and_derive_ordering_are_unchanged() -> None:
    """U6: FR-RH2.7 preserves exit codes and first-match verdict ordering."""
    assert Verdict.PASS.exit_code == 0
    assert Verdict.HALTED.exit_code == 10
    assert Verdict.DEGRADED.exit_code == 11
    assert Verdict.BLOCKED.exit_code == 2

    source = inspect.getsource(derive_verdict)
    assert source.index("# -- 1. BLOCKED") < source.index("# -- 2. DEGRADED")
    assert source.index("# -- 2. DEGRADED") < source.index("# -- 3. HALTED")
    assert source.index("# -- 3. HALTED") < source.index("# -- 4. PASS")
    assert 'contract.get("status") == "success"' in source
    assert "tier_reached == expected_tier" in source

    degraded_source = inspect.getsource(_degraded_reason)
    assert degraded_source.index('contract.get("t2_model_class_diversity")') < (
        degraded_source.index('contract.get("t2_vendor_diversity")')
    )
    assert degraded_source.index('contract.get("adversarial_unavailable")') < (
        degraded_source.index('contract.get("merge_method")')
    )
    assert degraded_source.index('contract.get("merge_method")') < (
        degraded_source.index('contract.get("adversarial_convergence_score")')
    )


def test_u8_swarm_merge_stays_mechanical_and_small() -> None:
    """U8: the adversarial scorer remains outside swarm.merge."""
    source_lines, _ = inspect.getsourcelines(mechanical_merge)
    code_lines = [
        line
        for line in source_lines
        if line.strip() and not line.lstrip().startswith("#")
    ]
    source = "".join(source_lines).lower()

    assert len(code_lines) <= 30
    for token in ("score", "rank", "dedup", "filter", "judge"):
        assert token not in source


def test_u7_no_nesting_guard_extended_to_ensemble() -> None:
    """U7 (FR-RH2.8): the no-nesting guard now scans `ensemble.py`.

    Asserts the guard module exposes the `_ENSEMBLE_SRC` reader and includes it
    in the agent-surface ban set, and that the extended agent-surface test runs
    green against the live `ensemble.py` (exercising the new anchor).
    """
    import tests.cli.reflect.test_no_nesting_guard as guard

    assert guard._ENSEMBLE_SRC.name == "ensemble.py"
    assert guard._ENSEMBLE_SRC in guard._AGENT_SURFACE_SRCS
    assert guard._RUNNER_SRC in guard._AGENT_SURFACE_SRCS
    # The extended agent-surface check must pass for the live driver module.
    guard.test_layer_b_wrapper_module_has_no_agent_imports()
    guard.test_ensemble_launches_only_via_claudeprocess_no_raw_subprocess()


def test_u9_no_forbidden_proxy_literals_in_executable_code() -> None:
    """U9 (NFR-RH2.8): no forbidden host/port/path literal in `ensemble.py`.

    The base URL is built 100% from the `T2ProxyUrl` env contract inside the
    transport layer; `ensemble.py` must carry NO `:4000/v1`, NO `:8317`, and NO
    bare `/cli` literal in executable code.
    """
    import ast

    src_path = (
        Path(__file__).resolve().parents[3] / "src/superclaude/cli/reflect/ensemble.py"
    )
    tree = ast.parse(src_path.read_text(encoding="utf-8"))
    string_literals = [
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant)
        if isinstance(node.value, str)
    ]
    joined = "\n".join(string_literals)
    for forbidden in (":4000/v1", ":8317", "/cli"):
        assert forbidden not in joined, (
            f"forbidden proxy literal {forbidden!r} in ensemble.py executable code"
        )


def test_u10_adversarial_contract_parse_real_shape(tmp_path) -> None:
    """U10 (FR-RH2.3 regression): the scorer reads the REAL /sc:adversarial contract.

    /sc:adversarial writes `<output>/adversarial/return-contract.yaml` with the
    score nested under a top-level `return_contract:` key. The stub integration
    tests INJECT the score (bypassing this parse), so this exercises the real
    `parse_adversarial_contract` + `extract_convergence_score` path that a live
    run depends on. Regression for the null-convergence-from-wrong-path bug.
    """
    from superclaude.cli.reflect.ensemble import (
        extract_convergence_score,
        parse_adversarial_contract,
    )

    out = tmp_path / "t2-adversarial"
    (out / "adversarial").mkdir(parents=True)
    (out / "adversarial" / "return-contract.yaml").write_text(
        "return_contract:\n  status: partial\n  convergence_score: 0.33\n",
        encoding="utf-8",
    )

    contract = parse_adversarial_contract(out)
    assert contract is not None
    assert extract_convergence_score(contract) == 0.33

    # Un-nested direct shape is also tolerated (forward-compat).
    assert extract_convergence_score({"convergence_score": 0.86}) == 0.86
    # Wrong-path / missing contract → None (graceful null-convergence fallback).
    assert parse_adversarial_contract(tmp_path / "nope") is None
    assert extract_convergence_score(None) is None


def test_u11_build_reflect_contract_threads_regression_fields() -> None:
    """U11 (R6): the widened builder threads the deviation/regression kwargs.

    Isolates the contract-builder change from the full fan-out path: a direct call
    with the new kwargs surfaces the regression signal, while a call WITHOUT them
    keeps the clean defaults (so the clean Tier-2 path still PASSes).
    """
    workers = [
        WorkerResult(index=0, status="success", model_id="model-a"),
        WorkerResult(index=1, status="success", model_id="model-b"),
    ]

    # With the deviation kwargs: the signal threads through as genuine bool/int.
    flagged = build_reflect_contract(
        workers,
        adversarial_convergence_score=0.86,
        regression_present=True,
        deviation_count_by_class={
            "authorized": 0,
            "necessary": 0,
            "drift": 0,
            "regression": 1,
        },
    )
    assert flagged is not None
    assert flagged["regression_present"] is True
    assert flagged["deviation_count_by_class"]["regression"] == 1

    # Clean default (no deviation kwargs): regression-free, all-zero counts.
    clean = build_reflect_contract(workers, adversarial_convergence_score=0.86)
    assert clean is not None
    assert clean["regression_present"] is False
    assert clean["unauthorized_deviation_present"] is False
    assert clean["needs_human_decision"] is False
    assert clean["user_decision_required"] is False
    assert clean["deviation_count_by_class"] == {
        "authorized": 0,
        "necessary": 0,
        "drift": 0,
        "regression": 0,
    }


def test_r2f2_build_reflect_contract_emits_honest_verification_fields() -> None:
    """R2-F2 (PR#199 round-2): the Tier-2 seam emits honest verification fields.

    The headless Tier-2 ensemble runs NO grounded/serena verification triangle, so
    hard-coding ``verification_ran=True`` was factually false and made the
    ``verification-skipped`` DEGRADE structurally unreachable on every Tier-2
    contract (clean runs bypassed the verification-integrity gate). The seam now
    emits ``verification_ran=False`` with the exempt skip reason ``no-verification-stage``
    so contract.py Trigger 12 evaluates and EXEMPTS (no DEGRADE, no PASS regression).
    """
    workers = [
        WorkerResult(index=0, status="success", model_id="model-a"),
        WorkerResult(index=1, status="success", model_id="model-b"),
    ]
    contract = build_reflect_contract(workers, adversarial_convergence_score=0.86)
    assert contract is not None
    # Genuine bool via ``is`` (not ``== False``): the seam never ran verification.
    assert contract["verification_ran"] is False
    assert contract["verification_skip_reason"] == "no-verification-stage"
    # The chosen skip reason MUST be a member of the read-only exemption set so the
    # router exempts rather than degrades (read-only membership check on contract.py).
    assert "no-verification-stage" in _VERIFICATION_SKIP_EXEMPTIONS


def test_r2f3_user_decision_required_decoupled_from_needs_human_decision() -> None:
    """R2-F3 (PR#199 round-2): user_decision_required is decoupled from needs_human_decision.

    The two predicates are orthogonal per sc-reflect-protocol/SKILL.md:793-794, and
    AdversarialResult carries no user_decision_required signal for the seam to mirror.
    Previously the seam mirrored ``user_decision_required = needs_human_decision``,
    which would fabricate a false ``user-decision-required`` HALTED route
    (contract.py:321) once the producer emits ``needs_human_decision=True``. The seam
    now emits an honest ``False`` default.

    This KNOWINGLY SUPERSEDES the R6 task Step 2.5 line 212 mandate (commit 6bea38f2,
    PR #200): "the three booleans plus the ``user_decision_required`` mirror, which
    MUST mirror ``needs_human_decision``". That mandate is a drafting error — it
    conflicts with the SKILL.md:793-794 schema, the divergent fixtures
    (human_required_needs_decision.yaml = needs=true/user=false; e2e phase-01 =
    needs=false/user=true) which a mirror cannot produce, and an independent
    /sc:reflect --mode pre --depth deep validation (2026-06-22) confirming the revert.
    """
    workers = [
        WorkerResult(index=0, status="success", model_id="model-a"),
        WorkerResult(index=1, status="success", model_id="model-b"),
    ]
    contract = build_reflect_contract(
        workers,
        needs_human_decision=True,
        adversarial_convergence_score=0.86,
    )
    assert contract is not None
    # Decoupled: the seam honestly defaults user_decision_required to False even when
    # needs_human_decision is True (genuine bool via ``is``).
    assert contract["user_decision_required"] is False
    assert contract["needs_human_decision"] is True


def test_build_reflect_contract_threads_adversarial_subrun_status() -> None:
    """P0 producer honesty: build_reflect_contract threads the adversarial sub-status.

    The incident's Tier-2 ensemble severed the real adversarial child status
    (emitting a hard-coded optimistic shell), so a ``partial`` adversarial sub-run
    never reached the contract. The widened builder now accepts an
    ``adversarial_status`` kwarg and surfaces it verbatim as
    ``adversarial_subrun_status`` (the gate signal per R-002 D-C2). A clean-default
    call WITHOUT the kwarg keeps legacy callers PASS-safe.
    """
    workers = [
        WorkerResult(index=0, status="success", model_id="model-a"),
        WorkerResult(index=1, status="success", model_id="model-b"),
    ]

    # With the new kwarg: the adversarial child status threads through verbatim.
    flagged = build_reflect_contract(
        workers,
        adversarial_convergence_score=0.86,
        adversarial_status="partial",
    )
    assert flagged is not None
    assert flagged["adversarial_subrun_status"] == "partial"

    # Clean default (no adversarial_status kwarg): non-partial, PASS-safe for legacy
    # callers (absent-safe -- either the key is absent or a non-partial default).
    clean = build_reflect_contract(workers, adversarial_convergence_score=0.86)
    assert clean is not None
    assert clean.get("adversarial_subrun_status") not in ("partial", "failed")


def test_extract_adversarial_status_reads_child_status() -> None:
    """P0 producer honesty: ``extract_adversarial_status`` reads the adversarial
    child's status, mirroring ``extract_convergence_score`` (nested ``return_contract``
    unwrap + safe defaults). Closes the untested-reader gap for the incident's severed
    signal. RED pre-fix: ``extract_adversarial_status`` does not exist until Step 2.10
    (ImportError)."""
    from superclaude.cli.reflect.ensemble import extract_adversarial_status

    # Nested return_contract unwrap (the literal incident signal shape).
    assert (
        extract_adversarial_status({"return_contract": {"status": "partial"}})
        == "partial"
    )
    # Top-level status.
    assert extract_adversarial_status({"status": "success"}) == "success"
    # Safe defaults on empty / None.
    assert extract_adversarial_status({}) is None
    assert extract_adversarial_status(None) is None


def test_run_adversarial_scorer_populates_status(tmp_path, monkeypatch) -> None:
    """P0 producer honesty: ``run_adversarial_scorer`` populates
    ``AdversarialResult.status`` from the parsed adversarial sub-contract, so the
    child's real status (the incident's severed signal) reaches the result object.

    The Mode-A scorer is a top-level ``ClaudeProcess`` needing the ``claude`` binary,
    so it is stubbed (start=no-op, wait=0) and ``parse_adversarial_contract`` is
    pointed at a sub-contract carrying ``status: partial``; the real
    ``extract_adversarial_status`` then flows it into ``AdversarialResult.status``.

    RED pre-fix: ``AdversarialResult`` has no ``status`` field / it is not populated
    until Steps 2.9+2.11 -> AttributeError on ``.status``.
    """
    from types import SimpleNamespace

    import superclaude.cli.reflect.ensemble as ensemble_mod
    from superclaude.cli.reflect.ensemble import run_adversarial_scorer

    class _StubProc:
        def __init__(self, **_kwargs) -> None:
            pass

        def start(self) -> None:
            pass

        def wait(self) -> int:
            return 0

    monkeypatch.setattr(ensemble_mod, "ClaudeProcess", _StubProc)
    config = SimpleNamespace(
        model="test-model",
        timeout_seconds=60,
        max_turns=10,
        reviewer_grounding_root=None,
    )

    # Partial sub-contract (the incident shape) -> status == "partial".
    monkeypatch.setattr(
        ensemble_mod,
        "parse_adversarial_contract",
        lambda _out: {
            "return_contract": {"status": "partial", "convergence_score": 0.75}
        },
    )
    result = run_adversarial_scorer([], tmp_path / "adv", config=config)
    assert result is not None
    assert result.status == "partial"

    # Clean/success sub-contract -> status == "success".
    monkeypatch.setattr(
        ensemble_mod,
        "parse_adversarial_contract",
        lambda _out: {
            "return_contract": {"status": "success", "convergence_score": 0.9}
        },
    )
    result2 = run_adversarial_scorer([], tmp_path / "adv2", config=config)
    assert result2 is not None
    assert result2.status == "success"


def test_build_adversarial_prompt_shell_quotes_paths() -> None:
    """PR#199 F5: build_adversarial_prompt shell-quotes the path list + output_dir.

    A path containing a space must stay a single shell argument (quoted), not be
    split into several. The comma stays the --compare/--suspect-source delimiter.
    """
    prompt = build_adversarial_prompt(
        ["/tmp/a b.final.md", "/tmp/c.final.md"], Path("/tmp/out dir")
    )
    assert "--output '/tmp/out dir'" in prompt
    assert "--compare '/tmp/a b.final.md,/tmp/c.final.md'" in prompt
    assert "--suspect-source '/tmp/a b.final.md,/tmp/c.final.md'" in prompt

    # A clean path set needs no quoting (shlex.quote is a no-op).
    clean = build_adversarial_prompt(["/tmp/a.md"], Path("/tmp/out"))
    assert "--compare /tmp/a.md " in clean
    assert clean.endswith("--output /tmp/out")


def test_resolve_config_normalizes_transport_case(temp_tasklist, patch_git) -> None:
    """PR#199 F4: resolve_config lowercases transport so programmatic callers
    passing mixed-case values match the case-insensitive CLI option."""
    config = resolve_config(
        str(temp_tasklist), depth="standard", model="test-model", transport="STUB"
    )
    assert config.transport == "stub"
