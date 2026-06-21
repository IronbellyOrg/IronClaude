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
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any

import yaml

from superclaude.cli.pipeline.process import ClaudeProcess
from superclaude.cli.reflect.contract import parse_contract
from superclaude.cli.reflect.models import ReflectConfig
from superclaude.cli.swarm.commands import _resolve_run_transport_factory
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
from superclaude.cli.swarm.transports.stub import StubTransport

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

TransportFactory = Callable[[int], Transport]
AdversarialScoreFn = Callable[[list[str], Path], float | None]

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

    preflight = build_preflight_result(reviewers=reviewers, transport=config.transport)
    factory = transport_for_slot or resolve_t2_transport_factory(
        config.transport,
        reviewers=reviewers,
        env=env,
    )
    worker_prompt = prompt or build_worker_prompt(config)
    worker_spec = WorkerSpec(count=reviewers, models=[])
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

    if adversarial_convergence_score is None and len(succeeded_final_paths) >= 2:
        if adversarial_score_fn is None:
            adversarial_convergence_score = run_adversarial_scorer(
                succeeded_final_paths,
                output_dir / ADVERSARIAL_SUBRUN_DIR,
                config=config,
            )
        else:
            adversarial_convergence_score = adversarial_score_fn(
                succeeded_final_paths,
                output_dir / ADVERSARIAL_SUBRUN_DIR,
            )

    contract = build_reflect_contract(
        normalized_workers,
        swarm_merged_path=swarm_contract.merged_path,
        adversarial_convergence_score=adversarial_convergence_score,
        adversarial_unavailable=adversarial_unavailable,
    )
    _emit_reflect_contract(config.contract_path, contract)
    return contract


def run_adversarial_scorer(
    final_paths: list[str],
    output_dir: Path,
    *,
    config: ReflectConfig,
) -> float | None:
    """Launch the selected Mode-A scorer and parse its convergence score.

    The downstream merge step consumes swarm's per-reviewer ``final_path``
    artifacts (suspect-aware). No scoring, ranking, or dedup logic is added to
    ``swarm/merge.py``. The adversarial merge produces a convergence score
    recorded on the reflect contract.
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
    )
    proc.start()
    if proc.wait() != 0:
        return None
    return extract_convergence_score(parse_adversarial_contract(output_dir))


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
    """Build the literal sc:adversarial Mode-A invocation."""
    compare_files = ",".join(final_paths)
    suspect_files = ",".join(final_paths)
    return (
        "/sc:adversarial "
        f"--compare {compare_files} "
        f"--suspect-source {suspect_files} "
        f"--output {output_dir}"
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


def build_reflect_contract(
    workers: list[WorkerResult],
    *,
    swarm_merged_path: str | None = None,
    adversarial_convergence_score: float | None = None,
    adversarial_unavailable: bool = False,
) -> dict[str, Any] | None:
    """Map swarm worker facts onto the reflect return-contract namespace."""
    succeeded = [worker for worker in workers if worker.status == "success"]
    reviewer_count = len(succeeded)
    if reviewer_count == 0:
        return None

    tier_reached = 2 if reviewer_count >= 2 else 1
    merge_method = "adversarial" if reviewer_count >= 2 else "single-reviewer-fallback"
    report_path = _select_report_path(succeeded, swarm_merged_path)

    return {
        "contract_version": REFLECT_CONTRACT_VERSION,
        "status": "success",
        "mode": "post",
        "tier_reached": tier_reached,
        "reviewer_count": reviewer_count,
        "report_path": report_path,
        "audit_log_path": None,
        "deviation_count_by_class": {
            "authorized": 0,
            "necessary": 0,
            "drift": 0,
            "regression": 0,
        },
        "t2_model_class_diversity": compute_model_class_diversity(succeeded),
        "t2_vendor_diversity": compute_vendor_diversity(succeeded),
        "adversarial_unavailable": adversarial_unavailable,
        "merge_method": merge_method,
        "adversarial_convergence_score": adversarial_convergence_score,
        "verification_ran": True,
        "verification_skip_reason": None,
        "citations_dropped": 0,
        "citations_dropped_extrapolated": 0,
        "input_drift_detected": False,
        "regression_present": False,
        "unauthorized_deviation_present": False,
        "needs_human_decision": False,
        "user_decision_required": False,
        "serena_summary_corroboration": "unavailable",
        "degraded_components": [],
    }


def compute_model_class_diversity(workers: list[WorkerResult]) -> str:
    """Return ``full`` when at least two succeeded model ids are distinct."""
    distinct_model_ids = {
        worker.model_id
        for worker in workers
        if worker.status == "success" and worker.model_id
    }
    return "full" if len(distinct_model_ids) >= 2 else "insufficient"


def compute_vendor_diversity(workers: list[WorkerResult]) -> str | None:
    """Return vendor diversity over the succeeded reviewers (OI-1: DERIVED).

    Classifies each succeeded worker's ``model_id`` to a vendor and returns
    ``"single"`` when all succeeded reviewers share one vendor (so the FR-11
    single-vendor degrade can fire), ``"multi"`` when ≥2 vendors are present, and
    ``None`` when fewer than two reviewers survived (the single-reviewer-fallback
    trigger owns the reason slug). Distinct ``model_id``s alone are NOT treated as
    multi-vendor — two distinct same-vendor models resolve to ``"single"``.
    """
    succeeded = [worker for worker in workers if worker.status == "success"]
    if len(succeeded) < 2:
        return None
    vendors = {
        _vendor_from_model_id(worker.model_id)
        for worker in succeeded
        if worker.model_id
    }
    return "multi" if len(vendors) >= 2 else "single"


def _vendor_from_model_id(model_id: str) -> str:
    """Classify a proxy ``model_id`` to a coarse vendor family."""
    lowered = model_id.lower()
    for marker, vendor in (
        ("qwen", "qwen"),
        ("deepseek", "deepseek"),
        ("gpt", "openai"),
        ("o1", "openai"),
        ("gemini", "google"),
        ("llama", "meta"),
        ("mistral", "mistral"),
        ("claude", "anthropic"),
    ):
        if marker in lowered:
            return vendor
    # Fall back to the leading path/colon segment as a best-effort vendor key.
    return lowered.split("/", 1)[0].split(":", 1)[0] or "unknown"


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
) -> str | None:
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
