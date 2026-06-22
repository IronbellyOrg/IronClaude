"""FR-RH2.5/.6/.9 non-mocked stub-transport integration witnesses (I1-I9).

This is the LOAD-BEARING proof that the Tier-2 ensemble genuinely forms. Each
test drives the REAL ``run_tier2_ensemble`` over the REAL
``dispatch_wave1`` -> ``reduce_wave3`` -> ``derive_verdict`` path with a
network-free ``StubTransport`` per slot. The conftest ``make_claude_process_stub``
canned-fixture path is deliberately NOT used: the pass-critical signals
(``tier_reached`` / ``merge_method`` / ``reviewer_count`` /
``t2_model_class_diversity``) are COMPUTED from the real fan-out, not copied from
a fixture.

NFR-RH2.3 non-vacuity: the I1 positive assertions must FAIL for I2/I4/I5/I6.

The adversarial convergence score is the only injected value (the adversarial
Mode-A scorer is a separate top-level ``ClaudeProcess`` that needs the ``claude``
binary, so it is stubbed via the production ``adversarial_score_fn`` seam — never
by patching ``ClaudeProcess`` to fabricate a contract). I1 additionally proves no
``ClaudeProcess`` is constructed at all.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from superclaude.cli.reflect import ensemble as ensemble_mod
from superclaude.cli.reflect.config import resolve_config
from superclaude.cli.reflect.contract import derive_verdict, parse_contract
from superclaude.cli.reflect.ensemble import (
    AdversarialResult,
    run_tier2_ensemble,
    stub_model_id,
)
from superclaude.cli.reflect.models import Verdict
from superclaude.cli.swarm.models import WorkerResult
from superclaude.cli.swarm.transports.stub import StubTransport

# Deterministic adversarial convergence score injected through the production
# seam so the credit-free test never launches the adversarial ClaudeProcess.
_FIXED_SCORE = 0.86


def _const_score(_paths: list[str], _out: Path) -> AdversarialResult:
    # Clean-default result object (the widened seam shape): a non-None convergence
    # score with no deviation/regression signal, so the existing PASS/DEGRADED
    # tests that inject this stub keep their current verdicts. Booleans are genuine
    # Python ``False``. Covers all three injection sites transitively.
    return AdversarialResult(
        convergence_score=_FIXED_SCORE,
        regression_present=False,
        unauthorized_deviation_present=False,
        needs_human_decision=False,
        deviation_count_by_class={
            "authorized": 0,
            "necessary": 0,
            "drift": 0,
            "regression": 0,
        },
        report_path=None,
    )


class _FailingTransport:
    """Network-free transport whose ``send`` always reports ``proxy_error``.

    ``http_code=None`` => the §7 retry matrix's ``other`` bucket: no retry, the
    proxy_error stands, and ``reduce_wave3`` does NOT count it toward M.
    """

    def __init__(self, model_id: str) -> None:
        self._model_id = model_id

    @property
    def model(self) -> str:
        return self._model_id

    def send(self, prompt: str, timeout: int) -> WorkerResult:  # noqa: ARG002
        result = WorkerResult(
            model_id=self._model_id,
            model_label=self._model_id,
            status="proxy_error",
            http_code=None,
            attempts=1,
        )
        result.body = ""  # type: ignore[attr-defined]
        return result


def _distinct_stub(slot_index: int) -> StubTransport:
    """One StubTransport per slot with a DISTINCT, vendor-distinct model_id.

    Uses the production `stub_model_id` scheme so both model-class diversity AND
    vendor diversity are genuinely satisfiable (a real heterogeneous pool).
    """
    return StubTransport(model_id=stub_model_id(slot_index))


def _config(temp_tasklist: Path, *, reviewers: int = 3) -> object:
    return resolve_config(
        str(temp_tasklist),
        depth="deep",
        model="test-model",
        transport="stub",
        reviewers=reviewers,
    )


def _run(config, transport_for_slot) -> tuple[dict | None, object]:
    """Drive the real ensemble + derive_verdict; return (contract, ReflectResult)."""
    run_tier2_ensemble(
        config,
        transport_for_slot=transport_for_slot,
        adversarial_score_fn=_const_score,
    )
    contract = parse_contract(config.contract_path)
    result = derive_verdict(
        contract,
        expected_tier=2,
        allow_single_vendor=config.allow_single_vendor,
        child_rc=0,
    )
    return contract, result


def _i1_positive_holds(contract: dict | None) -> bool:
    """The canonical I1 positive assertion set (NFR-RH2.3 falsifier reference).

    EXACTLY: tier_reached == 2, merge_method != "single-reviewer-fallback",
    reviewer_count >= 2, t2_model_class_diversity == "full".
    """
    if not contract:
        return False
    return (
        contract.get("tier_reached") == 2
        and contract.get("merge_method") != "single-reviewer-fallback"
        and int(contract.get("reviewer_count", 0)) >= 2
        and contract.get("t2_model_class_diversity") == "full"
    )


def test_i1_positive_witness_real_fanout(temp_tasklist, patch_git) -> None:
    """I1 positive witness (FR-RH2.5).

    "A test runs the real reflect Tier-2 driver with ``--transport stub`` and
    performs no network I/O."
    "The test does **not** patch ``ClaudeProcess`` to copy a canned
    ``tier_reached:2`` fixture for the ensemble (it exercises the real fan-out ->
    reduce path)."
    """
    config = _config(temp_tasklist, reviewers=3)

    # Prove the ensemble path constructs NO ClaudeProcess: any attempt is a
    # hard failure (the opposite of the canned-fixture mock gap).
    def _boom(*_args, **_kwargs):
        raise AssertionError("ensemble must not construct ClaudeProcess in I1")

    with patch.object(ensemble_mod, "ClaudeProcess", _boom):
        contract, result = _run(config, _distinct_stub)

    assert contract is not None
    assert contract["tier_reached"] == 2
    assert contract["merge_method"] != "single-reviewer-fallback"
    assert int(contract["reviewer_count"]) >= 2
    assert contract["t2_model_class_diversity"] == "full"
    assert contract["adversarial_convergence_score"] is not None
    assert contract["adversarial_unavailable"] is False
    assert contract["status"] == "success"
    assert result.verdict is Verdict.PASS
    assert result.verdict.exit_code == 0
    # The positive assertion set holds (the NFR-RH2.3 falsifier reference).
    assert _i1_positive_holds(contract) is True


def test_i2_negative_witness_one_reviewer_degrades(temp_tasklist, patch_git) -> None:
    """I2 negative witness (FR-RH2.6).

    "A 1-reviewer stub run yields ``merge_method == "single-reviewer-fallback"``
    and/or ``tier_reached == 1`` (a non-PASS Tier-2)."
    "The same assertions used in the positive FR-RH2.5 test FAIL for the
    1-reviewer case (witness is genuinely negative)."
    """
    config = _config(temp_tasklist, reviewers=1)
    contract, result = _run(config, _distinct_stub)

    assert contract is not None
    # Degrades: single-reviewer-fallback AND/OR tier_reached == 1.
    assert (
        contract.get("merge_method") == "single-reviewer-fallback"
        or contract.get("tier_reached") == 1
    )
    assert result.verdict is not Verdict.PASS
    # NFR-RH2.3: the canonical I1 positive assertions are demonstrably falsified.
    assert _i1_positive_holds(contract) is False
    assert contract.get("tier_reached") != 2
    assert int(contract.get("reviewer_count", 0)) < 2
    assert contract.get("merge_method") == "single-reviewer-fallback"


def test_i3_partial_two_of_three_distinct_pass_eligible(
    temp_tasklist, patch_git
) -> None:
    """I3 (FR-RH2.9): one proxy_error => M==2; PASS-eligible iff 2 distinct classes.

    mn_guard_table row:
      - {condition: "M>=2 AND >=2 distinct classes", verdict: "pass-eligible", exit: 0, slug: "pass"}
    """

    def factory(slot_index: int):
        if slot_index == 2:
            return _FailingTransport("stub-model-02")
        return _distinct_stub(slot_index)

    config = _config(temp_tasklist, reviewers=3)
    contract, result = _run(config, factory)

    assert contract is not None
    assert int(contract["reviewer_count"]) == 2
    assert contract["t2_model_class_diversity"] == "full"
    assert contract["tier_reached"] == 2
    assert result.verdict is Verdict.PASS
    assert result.verdict.exit_code == 0


def test_i4_partial_two_of_three_duplicate_class_degrades(
    temp_tasklist, patch_git
) -> None:
    """I4 (FR-RH2.4): two same-class survivors do NOT count as ``full``.

    mn_guard_table row:
      - {condition: "M>=2 but <2 distinct model classes", verdict: degraded, exit: 11, slug: "degraded-model-diversity"}
    This is the DELIBERATE OPPOSITE stub config from I1/I3 (same model_id).
    """

    def factory(slot_index: int):
        if slot_index == 2:
            return _FailingTransport("stub-model-02")
        return StubTransport(model_id="stub-model-dup")

    config = _config(temp_tasklist, reviewers=3)
    contract, result = _run(config, factory)

    assert contract is not None
    assert int(contract["reviewer_count"]) == 2
    assert contract["t2_model_class_diversity"] != "full"
    assert result.verdict is Verdict.DEGRADED
    assert result.verdict.exit_code == 11
    # NFR-RH2.3: the diversity positive assertion is falsified here.
    assert _i1_positive_holds(contract) is False


def test_i5_m_one_from_three_single_reviewer_fallback(temp_tasklist, patch_git) -> None:
    """I5 (FR-RH2.9): M==1 from N>1 is the SAME path as ``--reviewers 1``.

    mn_guard_table row:
      - {condition: "M==1 (>=N-1 failed, or --reviewers 1)", verdict: degraded, exit: 11, slug: "single-reviewer-fallback"}
    """

    def factory(slot_index: int):
        if slot_index == 0:
            return _distinct_stub(0)
        return _FailingTransport(f"stub-model-{slot_index:02d}")

    config = _config(temp_tasklist, reviewers=3)
    contract, result = _run(config, factory)

    assert contract is not None
    assert (
        contract.get("merge_method") == "single-reviewer-fallback"
        or contract.get("tier_reached") == 1
    )
    assert result.verdict is not Verdict.PASS
    assert result.verdict.exit_code == 11
    # NFR-RH2.3: the canonical I1 positive assertions are falsified for M==1.
    assert _i1_positive_holds(contract) is False
    assert contract.get("tier_reached") != 2
    assert int(contract.get("reviewer_count", 0)) < 2
    assert contract.get("merge_method") == "single-reviewer-fallback"


def test_i6_m_zero_blocked_exit2(temp_tasklist, patch_git) -> None:
    """I6 (FR-RH2.9): M==0 routes ``blocked`` (exit 2), not ``degraded``.

    mn_guard_table row:
      - {condition: "M==0 (all workers failed / no artifacts)", verdict: blocked, exit: 2, slug: "ensemble-empty"}
    Q6 RESOLVED -> Option B: M==0 maps onto the EXISTING ``contract-missing``
    BLOCKED Stage-1 slug (``ensemble-empty`` is [CODE-VERIFIED] absent from
    contract.py), preserving FR-RH2.7's "derive_verdict unchanged".
    """

    def factory(slot_index: int):
        return _FailingTransport(f"stub-model-{slot_index:02d}")

    config = _config(temp_tasklist, reviewers=3)
    contract, result = _run(config, factory)

    # M==0: no trustworthy reflect contract is emitted at the top-level path.
    assert contract is None
    # NFR-RH2.3: the canonical I1 positive assertions are falsified for M==0.
    assert _i1_positive_holds(contract) is False
    assert result.verdict is Verdict.BLOCKED
    assert result.verdict.exit_code == 2
    # Q6 working-default slug (NOT the non-existent ``ensemble-empty``).
    assert result.reason == "contract-missing"


def test_i7_return_contract_shape_preserved(temp_tasklist, patch_git) -> None:
    """I7 (FR-RH2.7): the swarm-driven return-contract preserves the consumed shape.

    "``write_reflect_post`` produces the same ``reflect_post:`` field set/order;
    the sidecar keeps its fields." ``contract_version`` is asserted at MAJOR 1
    (not an exact string) per contract.py:174-176.
    """
    config = _config(temp_tasklist, reviewers=3)
    contract, _ = _run(config, _distinct_stub)

    assert contract is not None
    # MAJOR-1 compatibility, not an exact-string match.
    assert str(contract["contract_version"]).split(".")[0] == "1"
    # Every field downstream consumers parse is present (derive_verdict +
    # _make_result + the reflect_post/sidecar write-back).
    for key in (
        "status",
        "tier_reached",
        "report_path",
        "deviation_count_by_class",
        "t2_model_class_diversity",
        "t2_vendor_diversity",
        "merge_method",
        "adversarial_convergence_score",
        "adversarial_unavailable",
        "degraded_components",
    ):
        assert key in contract, f"contract missing downstream-consumed field: {key}"
    assert isinstance(contract["degraded_components"], list)
    dev = contract["deviation_count_by_class"]
    assert set(dev) >= {"authorized", "necessary", "drift", "regression"}


def test_i8_path_confinement_reflect_parses_only_toplevel(
    temp_tasklist, patch_git
) -> None:
    """I8: reflect parses ONLY ``output_dir/return-contract.yaml``.

    path_confinement:
      reflect_contract: "<output_dir>/return-contract.yaml"          # the ONLY file reflect.derive_verdict parses
      swarm_subrun_contract: "<output_dir>/t2-swarm/return-contract.yaml"  # swarm DM-012; consumed by ensemble.py only
      rule: "reflect parses output_dir/return-contract.yaml; it MUST NOT parse the t2-swarm/ subdir's contract directly"
    """
    config = _config(temp_tasklist, reviewers=3)
    run_tier2_ensemble(
        config, transport_for_slot=_distinct_stub, adversarial_score_fn=_const_score
    )

    top = Path(config.contract_path)
    swarm = Path(config.output_dir) / "t2-swarm" / "return-contract.yaml"
    assert top == Path(config.output_dir) / "return-contract.yaml"
    assert top.is_file()
    assert swarm.is_file()
    assert top.resolve() != swarm.resolve()

    # The top-level (reflect) contract carries reflect verdict drivers; the
    # swarm sub-run contract carries swarm DM-012 worker counts.
    reflect_contract = parse_contract(top)
    swarm_contract = parse_contract(swarm)
    assert "tier_reached" in reflect_contract
    assert "workers_succeeded" in swarm_contract
    assert "tier_reached" not in swarm_contract


def test_i9_done_sentinel_dm017_shape(temp_tasklist, patch_git) -> None:
    """I9 (NFR-RH2.7): the t2-swarm sub-run emits a DM-017 ``done.json`` sentinel."""
    import json

    config = _config(temp_tasklist, reviewers=3)
    run_tier2_ensemble(
        config, transport_for_slot=_distinct_stub, adversarial_score_fn=_const_score
    )

    done = Path(config.output_dir) / "t2-swarm" / "done.json"
    assert done.is_file()
    payload = json.loads(done.read_text(encoding="utf-8"))
    assert set(payload) >= {"atomic_write", "terminal_status", "contract_path"}
    assert payload["atomic_write"] is True
    assert payload["terminal_status"] in {"success", "partial", "failed"}


def test_i10_lens_brief_drives_worker_prompt(temp_tasklist, patch_git) -> None:
    """FR-RH2.2: the worker prompt is the reflect-review lens brief, not /sc:reflect.

    Proves `build_worker_prompt` composes the lens system_prompt_fragment +
    user_template over the review target, so proxy workers receive the reflect
    brief rather than a Claude-Code slash command.
    """
    # Use a tasklist whose BODY contains `/sc:reflect` so the assertion is not
    # fixture-dependent: a faithful worker prompt may quote `/sc:reflect` inside
    # the target block, but it must NEVER be the worker INSTRUCTION (the prefix).
    tasklist = temp_tasklist
    tasklist.write_text(
        tasklist.read_text(encoding="utf-8")
        + "\n\nRun `/sc:reflect --mode post` then verify.\n",
        encoding="utf-8",
    )
    config = _config(tasklist, reviewers=3)
    prompt = ensemble_mod.build_worker_prompt(config)

    # The worker INSTRUCTION (everything before the quoted target) is the lens
    # brief, NOT the `/sc:reflect` Claude-Code slash command.
    assert "<<<TARGET>>>" in prompt  # lens user_template framing
    instruction_prefix, _, target_block = prompt.partition("<<<TARGET>>>")
    assert instruction_prefix.startswith(
        "You are one reviewer in a heterogeneous Tier-2 reflection ensemble"
    )
    assert "/sc:reflect" not in instruction_prefix  # not the worker instruction
    assert "{target_content}" not in prompt  # template was substituted
    # The `/sc:reflect` reference in the tasklist body survives ONLY inside the
    # quoted target block (proving the body is delivered as review material).
    assert "/sc:reflect" in target_block


def test_i11_production_audit_once_routes_tier2_to_ensemble(
    temp_tasklist, patch_git
) -> None:
    """FR-RH2.1 production route: Tier-2 `_audit_once` drives the ensemble.

    With the real (unpatched) `ClaudeProcess`, the production identity seam holds
    (`ClaudeProcess is _ProductionClaudeProcess`), so an `expected_tier == 2`
    audit takes the ensemble branch. Spying `run_tier2_ensemble` proves the route
    and keeps the test offline; the ensemble branch and the Tier-1 ClaudeProcess
    branch are mutually exclusive, so a called spy proves no audit ClaudeProcess
    was constructed in this path.
    """
    from unittest.mock import patch

    from superclaude.cli.reflect import runner as runner_mod
    from superclaude.cli.reflect.runner import ReflectRunner

    config2 = resolve_config(
        str(temp_tasklist), depth="deep", model="test-model", transport="stub"
    )
    with patch.object(runner_mod, "run_tier2_ensemble", autospec=True) as spy_ensemble:
        ReflectRunner(config2)._audit_once()
    spy_ensemble.assert_called_once()
    # The spy received the ReflectConfig (the ensemble builds its own lens brief).
    assert spy_ensemble.call_args.args[0] is config2


def test_i11b_tier1_audit_once_does_not_call_ensemble(temp_tasklist, patch_git) -> None:
    """FR-RH2.1 negative: a Tier-1 audit (`expected_tier == 1`) does NOT route to
    the ensemble — it uses the unchanged single `ClaudeProcess` grounded pass.

    `resolve_config` floors `quick`→`standard`, so a genuine Tier-1 config is
    built by overriding `depth="quick"` directly. `ClaudeProcess` is patched (so
    no real child launches) and `run_tier2_ensemble` is spied to prove it is
    never called for Tier-1.
    """
    import dataclasses
    from unittest.mock import patch

    from superclaude.cli.reflect import runner as runner_mod
    from superclaude.cli.reflect.runner import ReflectRunner

    config = resolve_config(str(temp_tasklist), depth="deep", model="test-model")
    tier1_config = dataclasses.replace(config, depth="quick")
    with (
        patch.object(runner_mod, "run_tier2_ensemble", autospec=True) as spy_ensemble,
        patch.object(runner_mod, "ClaudeProcess") as spy_proc,
    ):
        spy_proc.return_value.wait.return_value = 0
        ReflectRunner(tier1_config)._audit_once()
    spy_ensemble.assert_not_called()
    spy_proc.assert_called_once()


def test_i12_seam_regression_does_not_pass(temp_tasklist, patch_git) -> None:
    """I12 (FR-RH2 R6): a seam-reported regression MUST NOT route PASS.

    Red-then-green acceptance: against the pre-R6 code (``build_reflect_contract``
    hard-coded ``regression_present: False``) this asserted ``Verdict.PASS`` and
    FAILED; after the seam widening the regression signal threads through to the
    contract and ``derive_verdict`` routes HALTED (exit 10, reason
    ``"regression"``) via ``_halted_reason``.

    The ensemble is kept HEALTHY (distinct vendor-survivors → ``full`` diversity)
    and ``convergence_score`` is NON-None (0.86) so the ``null-convergence``
    DEGRADE trigger does NOT fire and mask the HALT (GAP-4 non-conflation).
    """

    def _regression_score(_paths: list[str], _out: Path) -> AdversarialResult:
        # Genuine Python ``True``/``1`` (never "true") so the strict-identity
        # ``is True`` halt trigger fires instead of self-BLOCKing on a non-bool.
        return AdversarialResult(
            convergence_score=_FIXED_SCORE,
            regression_present=True,
            unauthorized_deviation_present=False,
            needs_human_decision=False,
            deviation_count_by_class={
                "authorized": 0,
                "necessary": 0,
                "drift": 0,
                "regression": 1,
            },
            report_path=None,
        )

    config = _config(temp_tasklist, reviewers=3)
    run_tier2_ensemble(
        config,
        transport_for_slot=_distinct_stub,
        adversarial_score_fn=_regression_score,
    )
    contract = parse_contract(config.contract_path)
    result = derive_verdict(
        contract,
        expected_tier=2,
        allow_single_vendor=config.allow_single_vendor,
        child_rc=0,
    )

    # HEADLINE acceptance: a reported regression does not route PASS.
    assert result.verdict is not Verdict.PASS
    # Sharpened: it routes the HALTED regression rung specifically.
    assert result.verdict is Verdict.HALTED
    assert result.verdict.exit_code == 10
    assert result.reason == "regression"
    # Provenance: the seam signal actually reached the contract (was hard-coded
    # ``False`` before R6).
    assert contract is not None
    assert contract["regression_present"] is True
    # Healthy-ensemble guard: a DEGRADE is not masking the HALT.
    assert contract["t2_model_class_diversity"] == "full"
    assert result.verdict is not Verdict.DEGRADED
