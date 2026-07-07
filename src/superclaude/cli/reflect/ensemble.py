"""FR-RH2 Tier-2 ensemble driver.

The Tier-2 audit path invokes the swarm run surface
(``dispatch_wave1`` / ``_resolve_run_transport_factory``); no in-process
agent fan-out is introduced in ``runner.py`` or this driver. A
``depth=standard|deep`` run binds each worker slot to a distinct external
model (``T2Model0N``) via the per-slot factory.

``t2_model_class_diversity == "full"`` is computed over the distinct
``model_id`` values of the M succeeded workers, NOT over the N requested
slots.

# Phase C -> Phase D: adversarial verdict -> reflect return-contract.yaml
# (shape PRESERVED)
phase_c_to_d:
  required_fields:
    tier_reached: 2
    merge_method: "<adversarial>"
    reviewer_count: "M (succeeded workers); >=2 for pass"
    t2_model_class_diversity: "full"
    adversarial_convergence_score: "<float; recorded TELEMETRY at tier 2>"
  consumed_by: [contract.derive_verdict, runner.write_reflect_post]
  verdict_map_unchanged: {pass: 0, halted: 10, degraded: 11, blocked: 2}
"""

from __future__ import annotations

import dataclasses
import re
import shlex
import time
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any

import yaml

from superclaude.cli.pipeline.process import ClaudeProcess
from superclaude.cli.reflect.contract import parse_contract
from superclaude.cli.reflect.models import ReflectConfig
from superclaude.cli.swarm.commands import _resolve_run_transport_factory
from superclaude.cli.swarm.config import T1_MODEL_MAX_SLOTS
from superclaude.cli.swarm.dispatch import dispatch_wave1
from superclaude.cli.swarm.lenses.reflect_review import (
    LENS as _REFLECT_REVIEW_LENS_ENTRY,
)
from superclaude.cli.swarm.models import (
    CallerInfo,
    CallerMetadata,
    Manifest,
    PreflightSummary,
    SwarmState,
    WorkerResult,
    WorkerSpec,
)
from superclaude.cli.swarm.normalize import normalize_wave2
from superclaude.cli.swarm.preflight import PreflightResult
from superclaude.cli.swarm.reduce import emit_done_sentinel, reduce_wave3
from superclaude.cli.swarm.transports import Transport
from superclaude.cli.swarm.transports.openai_compat import TransportEnvError
from superclaude.cli.swarm.transports.stub import StubTransport

from ._diversity import (  # noqa: F401
    _vendor_from_model_id,
    compute_model_class_diversity,
    compute_vendor_diversity,
)
from .fallback import (
    FallbackTransportFactory,
    make_fallback_slot_factory,
    run_fallback_ladder,
)

REFLECT_CONTRACT_VERSION = "1.0"
REFLECT_REVIEW_LENS = "reflect-review"
# Reviewer normalize recipe. `passthrough` preserves the full reviewer body
# verbatim; `bare-review-v1` (code-review findings-table shape) would discard
# free-form reflection reviews down to a ~911-byte stub (300-char verdict cap +
# findings-table-only extraction), starving the adversarial scorer of content.
REFLECT_REVIEW_RECIPE = "passthrough"
SWARM_SUBRUN_DIR = "t2-swarm"
ADVERSARIAL_SUBRUN_DIR = "t2-adversarial"
CONTRACT_FILENAME = "return-contract.yaml"
MZERO_CONTRACT_MISSING_SLUG = "contract-missing"


@dataclasses.dataclass
class AdversarialResult:
    """Result object returned by the Tier-2 adversarial seam.

    Widens the seam beyond a bare convergence float so real deviation/regression
    signal can flow into ``build_reflect_contract``. Today only
    ``convergence_score`` + ``report_path`` are LIVE (sourced from the score-only
    ``/sc:adversarial`` Mode-A child); the three deviation booleans + per-class
    counts default CLEAN until a producer-extension emits them (OQ-PRODUCER).

    Load-bearing booleans (``regression_present``, ``unauthorized_deviation_present``,
    ``needs_human_decision``) MUST be genuine Python ``bool`` — a non-bool routes
    BLOCKED ``malformed-contract-boolean`` in ``contract.py``.
    """

    convergence_score: float | None
    regression_present: bool = False
    unauthorized_deviation_present: bool = False
    needs_human_decision: bool = False
    deviation_count_by_class: dict[str, int] = dataclasses.field(
        default_factory=lambda: {
            "authorized": 0,
            "necessary": 0,
            "drift": 0,
            "regression": 0,
        }
    )
    report_path: str | None = None
    # The parsed adversarial sub-contract status (success/partial/failed);
    # ``None`` = no status parsed / child failed.
    status: str | None = None


TransportFactory = Callable[[int], Transport]
AdversarialScoreFn = Callable[[list[str], Path], AdversarialResult | None]

# Vendor-distinct stub model pool so a credit-free ``--transport stub`` run is
# genuinely PASS-eligible: each slot binds a DISTINCT model_id from a DISTINCT
# vendor family, so both model-class diversity AND vendor diversity are
# satisfied (mirrors a real heterogeneous T2Model0N pool).
_STUB_VENDOR_POOL = ("qwen", "deepseek", "gpt", "mistral")


def stub_model_id(slot_index: int) -> str:
    """Deterministic vendor-distinct stub ``model_id`` for slot ``slot_index``."""
    vendor = _STUB_VENDOR_POOL[slot_index % len(_STUB_VENDOR_POOL)]
    return f"{vendor}-stub-{slot_index:02d}"


def build_preflight_result(*, reviewers: int, transport: str) -> PreflightResult:
    """Build the minimal swarm preflight shape dispatch reads."""
    manifest = Manifest(
        job_id="reflect-ensemble",
        preflight=PreflightSummary(
            target_checksum="",
            workers_requested=reviewers,
            transport_kind=transport,
        ),
        caller_metadata=CallerMetadata(suspect=True, tier="T2"),
    )
    return PreflightResult(
        manifest=manifest,
        state=SwarmState(state="preflight_ok", job_id=manifest.job_id),
        caller_metadata=manifest.caller_metadata,
    )


def resolve_t2_transport_factory(
    transport: str,
    *,
    reviewers: int,
    models: list[str] | None = None,
    env: Mapping[str, str] | None = None,
) -> TransportFactory:
    """Resolve the per-slot transport binding for the Tier-2 ensemble.

    The live path delegates to the swarm factory so the T2 proxy pool guard
    raises eagerly. The stub path intentionally builds one stub per slot with a
    distinct, vendor-distinct ``model_id`` (`stub_model_id`); the swarm factory's
    shared-stub branch would collapse all slots onto one model and make the
    diversity proof impossible.
    """
    if transport == "stub":

        def _stub_factory(slot_index: int) -> Transport:
            return StubTransport(model_id=stub_model_id(slot_index))

        return _stub_factory

    factory = _resolve_run_transport_factory(
        transport,
        models=models,
        env=env,
        workers_requested=reviewers,
    )
    return factory


# needs_human_decision gate (§7.3): the dedicated T1 proxy binding
# (``T1ProxyUrl`` / ``T1ProxyKey`` / ``T1Model0N``). CONFIRMED and enabled in Phase 5
# after the read-only env-var-NAME presence check + explicit operator sign-off
# (see phase-outputs/plans/t1-proxy-binding-decision.md). Only env-var NAME strings
# appear here -- never a proxy key/url VALUE. This supersedes the design §7.3
# T2-reuse default. When set, the ``openai_compat`` fallback arm resolves the REAL
# T1 pool via ``read_env_for_pool`` (lazily, so an incomplete env still degrades to
# ``fallback_config_missing`` at dispatch rather than crashing the run).
_T1_PROXY_BINDING: dict | None = {
    "model_prefix": "T1Model0",
    "proxy_url_env": "T1ProxyUrl",
    "proxy_key_env": "T1ProxyKey",
    "max_slots": T1_MODEL_MAX_SLOTS,
}


def resolve_t1_fallback_factory(
    transport: str,
    *,
    ladder: tuple[str, ...],
    env: Mapping[str, str] | None = None,
) -> FallbackTransportFactory:
    """Resolve the slot-NAME-keyed T1 fallback transport factory (GAP-2 sibling).

    Mirrors :func:`resolve_t2_transport_factory` but keyed by ladder-slot NAME
    (``"T1Model01"`` / ``"T1Model02"``) rather than a positional slot index (F1),
    and resolves the T1 pool/creds from ``env`` INTERNALLY (the ensemble seam has
    no ``SwarmConfig``). The ``stub`` arm is fully functional; the ``openai_compat``
    arm is gated behind the :data:`_T1_PROXY_BINDING` needs_human_decision sentinel
    until Phase 5 confirms the dedicated T1 proxy contract.
    """
    if transport == "stub":
        # One shared, vendor-distinct stub across every fallback slot. The stub
        # ``model_id`` classifies to a vendor family (via ``_vendor_from_model_id``)
        # that differs from the T2 stub pool, so a credit-free fallback certifies.
        shared = StubTransport(model_id="gemini-t1fallback-stub")

        def _stub_factory(_slot_name: str) -> Transport:
            return shared

        return _stub_factory

    # openai_compat: gated behind the needs_human_decision sentinel. While
    # unconfirmed, the factory raises TransportEnvError when invoked, which
    # run_fallback_ladder folds into terminal_reason: fallback_config_missing.
    if _T1_PROXY_BINDING is None:

        def _gated_factory(_slot_name: str) -> Transport:
            raise TransportEnvError(("T1ProxyUrl", "T1ProxyKey", "T1Model01"))

        return _gated_factory

    # _T1_PROXY_BINDING confirmed (set only by the Phase 5 needs_human_decision
    # HALT). Read the DEDICATED T1 pool + creds INTERNALLY via read_env_for_pool
    # (mirrors the T2 path; F3) and bind each ladder slot NAME to a DISTINCT pool
    # model by ladder position (F1) via make_fallback_slot_factory. The env read is
    # deferred INTO the returned factory (LAZY) so a TransportEnvError (env
    # incomplete) or ModelPoolTooSmallError (pool < ladder position) is raised when
    # the controller CALLS the factory -- inside run_fallback_ladder's catch, which
    # folds it into terminal_reason: fallback_config_missing -- rather than eagerly
    # at resolve time (which would escape the catch and crash run_tier2_ensemble).
    # The proxy creds live only inside the build_transport closure, never surfaced
    # (AC #12). The resolved slot factory is memoized after the first successful read.
    binding = _T1_PROXY_BINDING
    resolved: dict[str, FallbackTransportFactory] = {}

    def _lazy_openai_factory(slot_name: str) -> Transport:
        from superclaude.cli.swarm.transports.openai_compat import (
            OpenAICompatTransport,
            read_env_for_pool,
        )

        inner = resolved.get("factory")
        if inner is None:
            pool_config = read_env_for_pool(
                model_prefix=binding["model_prefix"],
                max_slots=binding["max_slots"],
                proxy_url_env=binding["proxy_url_env"],
                proxy_key_env=binding["proxy_key_env"],
                env=env,
            )
            pool = tuple(model for model in pool_config.models if model)
            transport_cache: dict[str, Transport] = {}

            def _build_transport(model_id: str) -> Transport:
                cached = transport_cache.get(model_id)
                if cached is None:
                    cached = OpenAICompatTransport(
                        base_url=pool_config.base_url,
                        api_key=pool_config.api_key,
                        model=model_id,
                    )
                    transport_cache[model_id] = cached
                return cached

            inner = make_fallback_slot_factory(
                pool=pool, ladder=ladder, build_transport=_build_transport
            )
            resolved["factory"] = inner
        return inner(slot_name)

    return _lazy_openai_factory


def run_tier2_ensemble(
    config: ReflectConfig,
    *,
    prompt: str = "",
    transport_for_slot: TransportFactory | None = None,
    adversarial_convergence_score: float | None = None,
    adversarial_score_fn: AdversarialScoreFn | None = None,
    adversarial_unavailable: bool = False,
    env: Mapping[str, str] | None = None,
) -> dict[str, Any] | None:
    """Run the in-process swarm fan-out and emit the reflect contract.

    The returned mapping is the exact top-level reflect contract written to
    ``config.contract_path``. When M==0, the resolved Q6 default maps the case
    to the existing ``contract-missing`` branch by leaving the top-level reflect
    contract absent; the swarm sub-run contract and ``done.json`` still land in
    ``output_dir/t2-swarm`` for diagnosis.

    FR-RH2.2: each external worker receives the ``reflect-review`` lens brief
    (``system_prompt_fragment`` + ``user_template`` over the review target), NOT
    a Claude-Code ``/sc:reflect`` slash command. ``prompt`` overrides the
    lens-built brief only when explicitly supplied (tests / advanced callers).
    """
    reviewers = int(config.reviewers)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    swarm_output_dir = output_dir / SWARM_SUBRUN_DIR
    swarm_output_dir.mkdir(parents=True, exist_ok=True)

    # F4 (§7.4): capture the shared run deadline ONCE, before primary dispatch.
    # The in-process Tier-2 route has no outer ClaudeProcess timeout, so this is
    # the single wall-clock bound the sequential fallback ladder honors. None when
    # no timeout is configured (the bound is inert; max_attempts still applies).
    deadline = (
        time.monotonic() + config.timeout_seconds if config.timeout_seconds else None
    )

    preflight = build_preflight_result(reviewers=reviewers, transport=config.transport)
    factory = transport_for_slot or resolve_t2_transport_factory(
        config.transport,
        reviewers=reviewers,
        env=env,
    )
    worker_prompt = prompt or build_worker_prompt(config)
    worker_spec = WorkerSpec(
        count=reviewers, models=[], timeout_sec=config.timeout_seconds
    )
    worker_results = dispatch_wave1(
        preflight,
        transport_for_slot=factory,
        prompt=worker_prompt,
        worker_spec=worker_spec,
    )
    stamped_workers = _stamp_worker_paths(worker_results, swarm_output_dir)
    normalized_workers = normalize_wave2(
        stamped_workers,
        REFLECT_REVIEW_RECIPE,
        recipe_args={
            "target": str(config.tasklist_path),
            "target_checksum": "",
            "caller_label": "reflect-ensemble",
        },
    )
    # §2 seam: after primary normalize, before anything reads normalized_workers,
    # run the bounded T1 fallback ladder so fallback successes flow through the
    # SAME reduce_wave3 / adversarial scorer / contract builder as primaries. Gated
    # on config.tier2_fallback_enabled (default-OFF for stub via resolve_config);
    # when disabled the path is byte-equivalent to today (t2_fallback=None).
    fallback_metadata: dict | None = None
    if config.tier2_fallback_enabled:
        fb_factory = resolve_t1_fallback_factory(
            config.transport,
            ladder=tuple(config.tier2_fallback_ladder),
            env=env,
        )
        ladder_outcome = run_fallback_ladder(
            primaries=normalized_workers,
            config=config,
            transport_for_fallback_slot=fb_factory,
            prompt=worker_prompt,
            swarm_output_dir=swarm_output_dir,
            stamp=_stamp_worker_paths,
            deadline_monotonic=deadline,
            env=env,
        )
        normalized_workers = ladder_outcome.contributing_workers
        fallback_metadata = ladder_outcome.metadata
    succeeded_final_paths = [
        worker.final_path
        for worker in normalized_workers
        if worker.status == "success" and worker.final_path
    ]
    next_substitutions = {
        "suspect_files": ",".join(succeeded_final_paths)
        if succeeded_final_paths
        else "<no-reflect-review-files>",
        "compare_files": ",".join(
            ["<existing-reflect-report>", *succeeded_final_paths]
        ),
    }
    swarm_contract = reduce_wave3(
        normalized_workers,
        mode="normalize+merge",
        output_dir=swarm_output_dir,
        workers_requested=reviewers,
        job_id=preflight.manifest.job_id,
        caller=CallerInfo(invocation_label="reflect-ensemble", kind="cli"),
        caller_metadata=preflight.caller_metadata,
        lens=REFLECT_REVIEW_LENS,
        lens_source="registry",
        recommended_next_command_template=(
            "/sc:adversarial --compare {compare_files} --suspect-source {suspect_files}"
        ),
        recommended_next_command_substitutions=next_substitutions,
        emit_to_disk=True,
    )
    swarm_contract_path = swarm_output_dir / CONTRACT_FILENAME
    emit_done_sentinel(swarm_contract.status, swarm_contract_path)

    adversarial_result: AdversarialResult | None = None
    if adversarial_convergence_score is None and len(succeeded_final_paths) >= 2:
        if adversarial_score_fn is None:
            adversarial_result = run_adversarial_scorer(
                succeeded_final_paths,
                output_dir / ADVERSARIAL_SUBRUN_DIR,
                config=config,
            )
        else:
            adversarial_result = adversarial_score_fn(
                succeeded_final_paths,
                output_dir / ADVERSARIAL_SUBRUN_DIR,
            )
        # A ``None`` result (child failure) leaves ``adversarial_convergence_score``
        # at ``None`` so the null-convergence DEGRADE fallback is preserved; a
        # pre-supplied score short-circuits the seam (this branch never runs).
        if adversarial_result is not None:
            adversarial_convergence_score = adversarial_result.convergence_score

    # Destructure the seam result into contract-bound locals. Clean defaults apply
    # when no seam ran (pre-supplied score / <2 survivors) OR the child failed
    # (``adversarial_result is None``) — so a genuinely clean Tier-2 run still
    # routes PASS (NFR-RH2.6 backward-compat).
    regression_present = (
        adversarial_result.regression_present
        if adversarial_result is not None
        else False
    )
    unauthorized_deviation_present = (
        adversarial_result.unauthorized_deviation_present
        if adversarial_result is not None
        else False
    )
    needs_human_decision = (
        adversarial_result.needs_human_decision
        if adversarial_result is not None
        else False
    )
    deviation_count_by_class = (
        adversarial_result.deviation_count_by_class
        if adversarial_result is not None
        else None
    )
    adversarial_report_path = (
        adversarial_result.report_path if adversarial_result is not None else None
    )
    adversarial_status = (
        adversarial_result.status if adversarial_result is not None else None
    )

    contract = build_reflect_contract(
        normalized_workers,
        swarm_merged_path=swarm_contract.merged_path,
        # Forward the STRING VALUE of the swarm status (a ``ResultStatus`` Literal /
        # plain ``str`` today) via ``getattr(..., "value", ...)`` so ``_worst_status``
        # always receives a real ``str`` -- the status axis was previously severed
        # (only ``.merged_path`` was forwarded). Robust if ``.status`` is promoted to
        # a real enum.
        swarm_status=getattr(swarm_contract.status, "value", swarm_contract.status),
        adversarial_status=adversarial_status,
        adversarial_convergence_score=adversarial_convergence_score,
        adversarial_unavailable=adversarial_unavailable,
        regression_present=regression_present,
        unauthorized_deviation_present=unauthorized_deviation_present,
        needs_human_decision=needs_human_decision,
        deviation_count_by_class=deviation_count_by_class,
        adversarial_report_path=adversarial_report_path,
        # L2 telemetry: reaching here means launch happened (the STOP path never
        # builds a contract). "snapshot-children-only" iff a snapshot was created:
        # only the ClaudeProcess review children (Tier-1 audit child + adversarial
        # scorer) are snapshot-`cwd`-grounded; the text-in/out swarm workers still
        # read the live tasklist path (D1 telemetry-honesty fix — was the overclaiming
        # "snapshot"). "disabled" otherwise (the default flag-off path).
        reviewer_isolation=(
            "snapshot-children-only" if config.reviewer_grounding_root else "disabled"
        ),
        audit_tree_dirty=config.audit_tree_dirty,
        reviewer_grounding_root=(
            str(config.reviewer_grounding_root)
            if config.reviewer_grounding_root
            else None
        ),
        # FX7: thread the REQUESTED count so the builder can surface a reviewer shortfall
        # (reviewer_count < requested) via reviewers_verified + a visible degraded_components token.
        reviewers_requested=reviewers,
        t2_fallback=fallback_metadata,
    )
    _emit_reflect_contract(config.contract_path, contract)
    return contract


def run_adversarial_scorer(
    final_paths: list[str],
    output_dir: Path,
    *,
    config: ReflectConfig,
) -> AdversarialResult | None:
    """Launch the selected Mode-A scorer and wrap its output in an ``AdversarialResult``.

    The downstream merge step consumes swarm's per-reviewer ``final_path``
    artifacts (suspect-aware). No scoring, ranking, or dedup logic is added to
    ``swarm/merge.py``. The adversarial merge produces a convergence score
    recorded on the reflect contract.

    Only ``convergence_score`` + ``report_path`` are populated LIVE here (the
    score-only Mode-A child cannot supply reviewer-deviation signal); the three
    deviation booleans + per-class counts default CLEAN on ``AdversarialResult``
    (GAP-2 scope fork). A child-launch/parse failure still returns ``None`` so the
    null-convergence DEGRADE fallback is preserved. ``regression_present`` is
    NEVER auto-derived from a low/None convergence score (GAP-4 non-conflation:
    low convergence is reviewer DISAGREEMENT → DEGRADE, not a regression).
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    prompt = build_adversarial_prompt(final_paths, output_dir)
    proc = ClaudeProcess(
        prompt=prompt,
        output_file=output_dir / "adversarial-stdout.json",
        error_file=output_dir / "adversarial-stderr.log",
        model=config.model,
        timeout_seconds=config.timeout_seconds,
        max_turns=config.max_turns,
        output_format="stream-json",
        # L1b (design (a)): the Mode-A adversarial scorer is a REVIEW-class child
        # (it reads reviewer artifacts + writes a contract); it runs under the
        # restricted reviewer profile so it cannot mutate the repo under audit.
        reviewer_profile=True,
        # L2: ground the scorer in the snapshot worktree when reviewer isolation is
        # active (None otherwise -> live CWD, today's behavior).
        cwd=config.reviewer_grounding_root,
    )
    proc.start()
    if proc.wait() != 0:
        return None
    parsed = parse_adversarial_contract(output_dir)
    return AdversarialResult(
        convergence_score=extract_convergence_score(parsed),
        report_path=_extract_adversarial_report_path(parsed),
        status=extract_adversarial_status(parsed),
    )


def parse_adversarial_contract(output_dir: Path) -> dict[str, Any] | None:
    """Locate + parse the ``/sc:adversarial`` return contract under ``output_dir``.

    ``/sc:adversarial`` writes its return contract into its ``artifacts_dir`` —
    ``<output>/adversarial/return-contract.yaml`` — NOT ``<output>/return-
    contract.yaml``. We try the artifacts-dir path first (the skill's
    convention), then fall back to the output root for forward-compatibility.
    """
    for candidate in (
        output_dir / "adversarial" / CONTRACT_FILENAME,
        output_dir / CONTRACT_FILENAME,
    ):
        parsed = parse_contract(candidate)
        if parsed is not None:
            return parsed
    return None


def build_adversarial_prompt(final_paths: list[str], output_dir: Path) -> str:
    """Build the literal sc:adversarial Mode-A invocation.

    The comma-joined path list and ``output_dir`` are shell-quoted so a path
    containing spaces (or other shell metacharacters) stays a single argument
    instead of being split into several. The comma remains the ``--compare`` /
    ``--suspect-source`` list delimiter, so a path containing a literal comma is
    still ambiguous by construction — an accepted limitation of the
    comma-delimited contract.
    """
    compare_files = ",".join(final_paths)
    return (
        "/sc:adversarial "
        f"--compare {shlex.quote(compare_files)} "
        f"--suspect-source {shlex.quote(compare_files)} "
        f"--output {shlex.quote(str(output_dir))}"
    )


def build_worker_prompt(config: ReflectConfig) -> str:
    """Compose the per-reviewer ``reflect-review`` lens brief (FR-RH2.2).

    Mirrors swarm ``commands._assemble_prompt``: the lens
    ``system_prompt_fragment`` (carrying the injection guard) is prepended to the
    ``user_template`` with ``{target_content}`` filled by the review target. The
    target is the tasklist under audit plus a base-ref header; full git-diff
    materialization is a rollout refinement (logged follow-up).
    """
    lens = _REFLECT_REVIEW_LENS_ENTRY
    target_content = _load_review_target(config)
    user_prompt = (lens.user_template or "").replace("{target_content}", target_content)
    fragment = lens.system_prompt_fragment or ""
    if fragment and user_prompt:
        return f"{fragment}\n\n{user_prompt}"
    return fragment or user_prompt


def _load_review_target(config: ReflectConfig) -> str:
    """Read the reflect review target (tasklist body + base-ref header)."""
    header = (
        "# Reflect Tier-2 review target\n"
        f"Base ref: {config.base}\n"
        f"Tasklist: {config.tasklist_path}\n\n"
    )
    try:
        body = Path(config.tasklist_path).read_text(encoding="utf-8")
    except OSError:
        body = ""
    return header + body


def extract_convergence_score(contract: dict[str, Any] | None) -> float | None:
    """Extract and normalize the adversarial return-contract score.

    ``/sc:adversarial`` nests its fields under a top-level ``return_contract:``
    key (``return_contract:\n  convergence_score: 0.33``); unwrap it before
    reading. A direct (un-nested) ``convergence_score`` is also tolerated.
    """
    if not contract:
        return None
    inner = contract.get("return_contract")
    if isinstance(inner, dict):
        contract = inner
    raw_score = contract.get("convergence_score")
    if raw_score is None:
        raw_score = contract.get("adversarial_convergence_score")
    try:
        score = float(raw_score)
    except (TypeError, ValueError):
        return None
    if 0.0 <= score <= 1.0:
        return score
    return None


def extract_adversarial_status(contract: dict[str, Any] | None) -> str | None:
    """Extract the adversarial return-contract status (success/partial/failed).

    Mirrors ``extract_convergence_score``'s ``return_contract:`` unwrap: the
    Mode-A child nests its fields under a top-level ``return_contract:`` key
    (the incident child emitted ``return_contract.status: "partial"``). A direct
    (un-nested) ``status`` is also tolerated. The value is normalized (stripped +
    lowercased) so a formatting/case variant of a real status (e.g. ``"Partial "``,
    ``"FAILED"``) still matches the exact-membership degrade gate
    (``adversarial_subrun_status in ("partial", "failed")``) instead of silently
    slipping past it. Returns ``None`` when the contract is falsy, absent, or the
    status is not a non-empty string.
    """
    if not contract:
        return None
    inner = contract.get("return_contract")
    if isinstance(inner, dict):
        contract = inner
    value = contract.get("status")
    if not isinstance(value, str):
        return None
    normalized = value.strip().lower()
    return normalized or None


def _extract_adversarial_report_path(contract: dict[str, Any] | None) -> str | None:
    """Extract the merged report path from the adversarial return contract.

    Mirrors ``extract_convergence_score``'s ``return_contract:`` unwrap. The
    Mode-A child emits ``merged_output_path`` (string|null, schema research 02
    §3); surface it as the adversarial ``report_path`` so the contract can prefer
    it over the swarm ``merged.md`` subrun fallback. Returns ``None`` when absent
    or non-string.
    """
    if not contract:
        return None
    inner = contract.get("return_contract")
    if isinstance(inner, dict):
        contract = inner
    value = contract.get("merged_output_path")
    return value if isinstance(value, str) and value else None


_STATUS_RANK = {"success": 0, "partial": 1, "failed": 2}


def _worst_status(*statuses: str | None) -> str:
    """Return the worst (highest-rank) status under ``failed > partial > success``.

    Coerces each argument to its string form via ``getattr(s, "value", s)`` -- a
    no-op for the current ``ResultStatus = Literal["success", "partial", "failed"]``
    (a plain ``str`` at runtime) but robust if ``swarm_contract.status`` is ever
    promoted to a real enum, so a non-``str`` status can never silently fall through
    ``_STATUS_RANK.get(...)`` to rank 0 and mis-rank as ``success``. Unknown / ``None``
    default to rank 0; returns ``"success"`` when none is worse. Pure and total --
    never raises on ``None``/unknown (this is the telemetry-only worst-of).
    """
    worst = "success"
    for status in statuses:
        status = getattr(status, "value", status)
        if status and _STATUS_RANK.get(status, 0) > _STATUS_RANK[worst]:
            worst = status
    return worst


def build_reflect_contract(
    workers: list[WorkerResult],
    *,
    swarm_merged_path: str | None = None,
    adversarial_convergence_score: float | None = None,
    adversarial_unavailable: bool = False,
    regression_present: bool = False,
    unauthorized_deviation_present: bool = False,
    needs_human_decision: bool = False,
    deviation_count_by_class: dict[str, int] | None = None,
    adversarial_report_path: str | None = None,
    reviewer_isolation: str = "disabled",
    audit_tree_dirty: bool = False,
    reviewer_grounding_root: str | None = None,
    swarm_status: str = "success",
    adversarial_status: str | None = None,
    reviewers_requested: int | None = None,
    t2_fallback: dict | None = None,
) -> dict[str, Any] | None:
    """Map swarm worker facts onto the reflect return-contract namespace.

    The deviation/regression signal (``regression_present``,
    ``unauthorized_deviation_present``, ``needs_human_decision``,
    ``deviation_count_by_class``) is threaded from the adversarial seam result;
    all four default CLEAN so a direct call or a seam-less Tier-2 run still emits
    an all-zero, regression-free contract that routes PASS. Load-bearing booleans
    are forwarded as genuine Python ``bool`` (never ``"true"``/``1``).
    """
    succeeded = [worker for worker in workers if worker.status == "success"]
    reviewer_count = len(succeeded)
    if reviewer_count == 0:
        return None

    # FX7 honest-accounting (additive/visible). ``reviewers_requested`` is None for
    # direct/test calls that omit the kwarg → verification is treated as vacuously
    # satisfied (never ``reviewer_count >= None``, which would raise). On a genuine
    # shortfall (requested known and fewer survived) surface a VISIBLE ``reviewer-shortfall``
    # token in ``degraded_components``. The token is BENIGN — it is intentionally NOT a
    # ``_DEGRADED_COMPONENTS_HALT_SET`` member (contract.py:31-33), so it does NOT flip the
    # verdict: a 2-of-3 shortfall stays PASS-eligible per the deliberate FR-RH2.9 design
    # (test_i3). The verdict-DEGRADE-on-shortfall is DEFERRED as a needs_human_decision
    # PENDING (fx7-degrade-on-reviewer-shortfall-DECISION.md) because degrading it would
    # reverse FR-RH2.9 non-additively (parallel to the deferred degrade-on-unverified vs R2-F2).
    reviewers_verified = (
        True if reviewers_requested is None else reviewer_count >= reviewers_requested
    )
    degraded_components: list[str] = []
    if reviewers_requested is not None and reviewer_count < reviewers_requested:
        degraded_components.append("reviewer-shortfall")

    tier_reached = 2 if reviewer_count >= 2 else 1
    merge_method = "adversarial" if reviewer_count >= 2 else "single-reviewer-fallback"
    report_path = _select_report_path(
        succeeded,
        swarm_merged_path,
        adversarial_report_path=adversarial_report_path,
    )
    if deviation_count_by_class is None:
        deviation_count_by_class = {
            "authorized": 0,
            "necessary": 0,
            "drift": 0,
            "regression": 0,
        }

    contract = {
        "contract_version": REFLECT_CONTRACT_VERSION,
        "status": "success",
        # Telemetry worst-of (includes swarm) -- observability ONLY, never gated.
        "subrun_status": _worst_status(swarm_status, adversarial_status),
        # The adversarial child's status verbatim -- the DEGRADE gate signal.
        "adversarial_subrun_status": adversarial_status,
        # Telemetry bool derived from the worst-of -- observability ONLY.
        "subrun_status_partial": _worst_status(swarm_status, adversarial_status)
        != "success",
        "mode": "post",
        "tier_reached": tier_reached,
        "reviewer_count": reviewer_count,
        "report_path": report_path,
        "audit_log_path": None,
        "deviation_count_by_class": deviation_count_by_class,
        "t2_model_class_diversity": compute_model_class_diversity(succeeded),
        "t2_vendor_diversity": compute_vendor_diversity(succeeded),
        "adversarial_unavailable": adversarial_unavailable,
        "merge_method": merge_method,
        "adversarial_convergence_score": adversarial_convergence_score,
        "verification_ran": False,
        "verification_skip_reason": "no-verification-stage",
        # FX7 additive visibility siblings — make the vacuity/shortfall observable to a
        # downstream reader WITHOUT repurposing existing routing (driving-plan §3.4).
        # verification_verified/regression_verified are always False here (the headless
        # seam runs no verification triangle); reviewers_verified is None-guarded above.
        "verification_verified": False,
        "reviewers_verified": reviewers_verified,
        "regression_verified": False,
        "citations_dropped": 0,
        "citations_dropped_extrapolated": 0,
        "input_drift_detected": False,
        "regression_present": regression_present,
        "unauthorized_deviation_present": unauthorized_deviation_present,
        "needs_human_decision": needs_human_decision,
        "user_decision_required": False,  # seam emits no user-decision signal; honest default (R2-F3, supersedes R6 Step 2.5 mirror mandate)
        "serena_summary_corroboration": "unavailable",
        "degraded_components": degraded_components,
        # L2 reviewer-isolation telemetry (pure telemetry; not verdict-bearing —
        # the STOP happens in the runner before derive_verdict, so audit_tree_dirty
        # is NOT registered in _LOAD_BEARING_BOOL_FIELDS). Defaulted CLEAN so a
        # seam-less Tier-2 run or a direct call still emits a valid contract.
        "reviewer_isolation": reviewer_isolation,
        "audit_tree_dirty": audit_tree_dirty,
        "reviewer_grounding_root": reviewer_grounding_root,
    }
    if t2_fallback is not None:
        contract["t2_fallback"] = t2_fallback
    return contract


def _stamp_worker_paths(
    workers: list[WorkerResult],
    output_dir: Path,
) -> list[WorkerResult]:
    """Populate raw/meta/final artifact paths before Wave 2 normalization."""
    stamped: list[WorkerResult] = []
    for worker in workers:
        slug = _slugify_model(worker.model_label or worker.model_id, worker.index)
        base = f"{REFLECT_REVIEW_LENS}-{worker.index:02d}-{slug}"
        replaced = dataclasses.replace(
            worker,
            path=str(output_dir / f"{base}.final.md"),
            raw_path=str(output_dir / f"{base}.raw.md"),
            meta_path=str(output_dir / f"{base}.meta.json"),
            final_path=str(output_dir / f"{base}.final.md"),
        )
        body = getattr(worker, "body", None)
        if body is not None:
            replaced.body = body
        stamped.append(replaced)
    return stamped


def _slugify_model(value: str, index: int) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip()).strip("-._")
    return slug.lower() if slug else f"slot{index:02d}"


def _select_report_path(
    succeeded: list[WorkerResult],
    swarm_merged_path: str | None,
    *,
    adversarial_report_path: str | None = None,
) -> str | None:
    # Prefer the adversarial merged report when present (QA CRITICAL #2: keep the
    # swarm ``merged.md`` only as a subrun-artifact fallback). When no adversarial
    # report path is available the existing chain (swarm → worker final_path →
    # None) is preserved unchanged, so current swarm-path assertions stay green.
    if adversarial_report_path:
        return adversarial_report_path
    if swarm_merged_path:
        return swarm_merged_path
    for worker in succeeded:
        if worker.final_path:
            return worker.final_path
    return None


def _emit_reflect_contract(path: Path, contract: dict[str, Any] | None) -> None:
    if contract is None:
        try:
            path.unlink()
        except FileNotFoundError:
            pass
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    text = yaml.safe_dump(contract, sort_keys=False, allow_unicode=True)
    path.write_text(text, encoding="utf-8")
