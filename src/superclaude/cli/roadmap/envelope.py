"""PipelineEnvelope — typed cross-step state for the roadmap pipeline.

This module implements the **PipelineEnvelope** mandated by
BUILD-REQUEST §R1.2 (line 170) + §MVR §1 (lines 84-103). It eliminates
master:§Flaw 3 (state-in-markdown substrate) at the substrate layer by
inverting the relationship between markdown artifacts and gate-pass state:

- **Before R1.2**: every step's markdown artifact carries the canonical
  gate-pass counts (frontmatter, body, summary tables). Gates re-parse
  markdown each step. The LLM that wrote the markdown determines the
  counts the gate observes.
- **After R1.2**: every step's markdown artifact is just a render. The
  ``envelope.json`` sidecar carries canonical counts / findings /
  convergence. Python post-step extractors registered in
  :data:`POST_EXTRACTORS` read the markdown and *derive* counts
  deterministically. **LLMs never write gate-pass counts directly into
  the envelope** — this is the master:§Flaw 3 invariant.

**Dual-write phase (R1.2):** during the dual-write phase (1 release cycle
per BUILD-REQUEST §R1.2), markdown is still written and consumed by gates;
the envelope is also written but not yet read by gate logic. R1.3 wires
``code_assertions`` to read from the envelope; R1.6 deletes the markdown-
as-substrate code paths.

**R0.1 absorption:** The R0.1 ``spec_id_registry.json`` sidecar continues
to be written during dual-write; the envelope's ``spec_ids`` field
mirrors the same :class:`SpecIdRegistry` shape. The MERGE_GATE
SemanticCheck continues to read ``spec_id_registry.json`` until R1.3+
migrates it to envelope reads. See the TODO at the ``spec_ids`` field
site for the R1.6 deletion target.

**Sidecar location:** ``<release_dir>/envelope.json``. Persistence uses an
atomic tmpfile + ``os.replace`` pattern, mirroring
``convergence.py:315-317`` (POSIX rename atomicity).

**ConvergenceResult binding (sc:reflect UC-1, 2026-06-01):** §MVR §1
literally names the convergence field type ``ConvergenceState`` but no
such class exists in the codebase. The closest existing types are
``RunMetadata`` (convergence.py:75 — per-run metadata, orthogonal to
convergence outcome) and ``ConvergenceResult`` (convergence.py:321 — the
terminal convergence verdict). This module binds the envelope's
``convergence`` field to ``ConvergenceResult | None``. See
``r1-2-envelope-design.md`` §2 row 7 for the full rationale; PG7.1 (a)
audits the envelope against the design's documented binding.

**Design doc:** see ``.dev/tasks/to-do/TASK-RF-20260531-042405/phase-
outputs/plans/r1-2-envelope-design.md`` for the architectural rationale,
the 14-step dispatch table, and the PG7.1 audit conformance map.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, replace
from hashlib import sha256
from pathlib import Path
from typing import Callable, Optional

from superclaude.cli.roadmap.convergence import ConvergenceResult
from superclaude.cli.roadmap.id_registry import SpecIdRegistry
from superclaude.cli.roadmap.models import Finding

# ---------------------------------------------------------------------------
# Supporting dataclasses
#
# §MVR §1 names ``ArtifactRef`` and ``AcceptedDeviation`` but does not
# define their fields. Defined here, both frozen + hashable for safe
# pass-across-pipeline-boundaries (mirrors the R0.1 ``SpecIdRegistry``
# precedent in ``id_registry.py``).
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ArtifactRef:
    """Reference to a step's on-disk artifact + content hash for drift detection.

    Stored in :attr:`PipelineEnvelope.artifacts`, keyed by ``step.id``.
    Hashable (frozen=True) so the envelope can be safely passed across
    pipeline boundaries.

    Parameters
    ----------
    path:
        Path to the step's artifact (typically a markdown file under the
        release directory). Stored as a :class:`Path`; serialized as a
        string in the JSON sidecar.
    content_hash:
        First 16 hex chars of the SHA-256 of the artifact's UTF-8 bytes.
        16-char prefix matches the R0.1 ``spec_hash`` convention
        (``id_registry.py:154``).
    """

    path: Path
    content_hash: str


@dataclass(frozen=True)
class AcceptedDeviation:
    """Per-pipeline accepted-deviation record (absorbed from accept-spec-change flow).

    Distinct from :attr:`SpecIdRegistry.accepted_deviation_ids` (which
    carries only the IDs); this carries the full record (id, reason,
    timestamp) for envelope-resident audit.

    Parameters
    ----------
    id:
        Deviation ID (e.g. ``"D-7"``).
    reason:
        Human-authored rationale captured at accept-spec-change time.
    timestamp:
        ISO-8601 timestamp string (matches the format used by
        ``spec_patch.scan_accepted_deviation_records``).
    """

    id: str
    reason: str
    timestamp: str


# ---------------------------------------------------------------------------
# PipelineEnvelope — §MVR §1 canonical 8-field shape
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PipelineEnvelope:
    """Typed cross-step state for the roadmap pipeline (§MVR §1 lines 84-103).

    Substrate inversion: this object is the source of truth for cross-step
    state — markdown is render-only after the dual-write cutover (R1.6).

    **Master:§Flaw 3 invariant:** the :attr:`counts` and :attr:`findings`
    fields are populated ONLY by:

    1. The Python post-step extractors registered in
       :data:`POST_EXTRACTORS` (populated by Step 7.3).
    2. Direct Python assignments in ``executor.py``.

    There is **no code path** where LLM output flows directly into these
    fields. Post-extractors *derive* counts deterministically from markdown
    via existing ``spec_parser`` helpers — Contract #6 forbids new
    parsers.

    **R0.1 ``spec_id_registry.json`` absorption:** the :attr:`spec_ids`
    field carries the full :class:`SpecIdRegistry` built by R0.1's
    ``build_id_registry()``. During the dual-write phase, both
    ``<release>/spec_id_registry.json`` and ``<release>/envelope.json``
    are written; their ``spec_ids`` content is identical. The duplicate
    sidecar is deleted in R1.6 — see the TODO at the field site.

    Parameters
    ----------
    release_id:
        Release identifier (matches the ``<release>`` segment in
        ``<release>/envelope.json``).
    spec_hash:
        SHA-256 of spec content at extract time (16-char hex prefix;
        matches the :attr:`SpecIdRegistry.spec_hash` convention for
        downstream-consistency assertions).
    spec_ids:
        Full :class:`SpecIdRegistry` (R0.1) absorbed by R1.2.

        .. todo::
           R1.6 — delete ``<release>/spec_id_registry.json`` writes once
           gate logic reads ``envelope.spec_ids`` directly (R1.3+ wires
           the first ``code_assertions`` consumer).
    artifacts:
        Per-step artifact references with content hashes, keyed by
        ``step.id``. §MVR §1 names the type ``dict[StepId, ArtifactRef]``
        but no ``StepId`` class exists in the codebase; using ``str``
        keyed on the verified step id literals from research/02 §1.1
        (extract, generate-{agent}, diff, debate, score, merge,
        anti-instinct, test-strategy, spec-fidelity, wiring-verification,
        deviation-analysis, remediate, certify).
    findings:
        Typed :class:`Finding` records, additive across steps. Populated
        by post-extractors only (master:§Flaw 3 invariant).
    counts:
        Gate-pass signals (e.g. ``"merge.roadmap_id_count": 47``).
        Populated by post-extractors only (master:§Flaw 3 invariant).
    convergence:
        Terminal convergence verdict (:class:`ConvergenceResult` or
        ``None`` when convergence has not yet run / is disabled).
        sc:reflect UC-1 binding: §MVR §1 names this ``ConvergenceState |
        None`` but no ``ConvergenceState`` class exists; bound to
        ``ConvergenceResult | None`` per the design doc rationale.
    accepted_deviations:
        Full :class:`AcceptedDeviation` records (id + reason + timestamp)
        for envelope-resident audit. Distinct from
        ``spec_ids.accepted_deviation_ids`` which carries only the IDs.
    """

    release_id: str
    spec_hash: str
    spec_ids: SpecIdRegistry
    artifacts: dict[str, ArtifactRef]
    findings: list[Finding]
    counts: dict[str, int]
    convergence: Optional[ConvergenceResult]
    accepted_deviations: list[AcceptedDeviation]

    @staticmethod
    def empty(
        release_id: str,
        spec_hash: str,
        spec_ids: SpecIdRegistry,
    ) -> PipelineEnvelope:
        """Build a fresh envelope at pipeline start (typically after the extract step).

        Convenience constructor for the common case of starting a new
        pipeline run: pass the release identifier, the spec hash, and the
        registry built by R0.1's ``build_id_registry()``. Mutable
        collections start empty; ``convergence`` starts ``None``.
        """
        return PipelineEnvelope(
            release_id=release_id,
            spec_hash=spec_hash,
            spec_ids=spec_ids,
            artifacts={},
            findings=[],
            counts={},
            convergence=None,
            accepted_deviations=[],
        )


# ---------------------------------------------------------------------------
# Serialization helpers (JSON sidecar round-trip)
#
# Mirrors R0.1 ``SpecIdRegistry.to_dict()`` precedent (id_registry.py:106-122)
# in spirit but uses module-level helpers (rather than methods) because
# ``Finding`` and ``ConvergenceResult`` live outside this module — we cannot
# add ``to_dict`` to them without modifying source-of-truth modules
# (``convergence.py`` is on the PRESERVE list per BUILD-REQUEST §MVR §3).
# ---------------------------------------------------------------------------


def _artifact_ref_to_dict(ref: ArtifactRef) -> dict[str, str]:
    return {"path": str(ref.path), "content_hash": ref.content_hash}


def _artifact_ref_from_dict(d: dict) -> ArtifactRef:
    return ArtifactRef(path=Path(d["path"]), content_hash=d["content_hash"])


def _accepted_deviation_to_dict(dev: AcceptedDeviation) -> dict[str, str]:
    return {"id": dev.id, "reason": dev.reason, "timestamp": dev.timestamp}


def _accepted_deviation_from_dict(d: dict) -> AcceptedDeviation:
    return AcceptedDeviation(id=d["id"], reason=d["reason"], timestamp=d["timestamp"])


def _finding_to_dict(f: Finding) -> dict:
    """Serialize a :class:`Finding` to a JSON-safe dict.

    Enumerates every field explicitly (rather than using
    ``dataclasses.asdict``) so the JSON shape is stable against future
    field additions to :class:`Finding` — those would become opt-in via an
    explicit map update here, NOT silently leak into the sidecar.
    """
    return {
        "id": f.id,
        "severity": f.severity,
        "dimension": f.dimension,
        "description": f.description,
        "location": f.location,
        "evidence": f.evidence,
        "fix_guidance": f.fix_guidance,
        "files_affected": list(f.files_affected),
        "status": f.status,
        "agreement_category": f.agreement_category,
        "deviation_class": f.deviation_class,
        "source_layer": f.source_layer,
        "rule_id": f.rule_id,
        "spec_quote": f.spec_quote,
        "roadmap_quote": f.roadmap_quote,
        "stable_id": f.stable_id,
    }


def _finding_from_dict(d: dict) -> Finding:
    """Reconstruct a :class:`Finding` from its JSON-safe dict shape.

    Uses ``.get`` with defaults for the v3.05-extension fields
    (``rule_id``, ``spec_quote``, ``roadmap_quote``, ``stable_id``) and
    the post-init-validated enums (``status``, ``deviation_class``,
    ``source_layer``) so older sidecars still round-trip.
    """
    return Finding(
        id=d["id"],
        severity=d["severity"],
        dimension=d["dimension"],
        description=d["description"],
        location=d["location"],
        evidence=d["evidence"],
        fix_guidance=d["fix_guidance"],
        files_affected=list(d.get("files_affected", [])),
        status=d.get("status", "PENDING"),
        agreement_category=d.get("agreement_category", ""),
        deviation_class=d.get("deviation_class", "UNCLASSIFIED"),
        source_layer=d.get("source_layer", "structural"),
        rule_id=d.get("rule_id", ""),
        spec_quote=d.get("spec_quote", ""),
        roadmap_quote=d.get("roadmap_quote", ""),
        stable_id=d.get("stable_id", ""),
    )


def _convergence_to_dict(c: ConvergenceResult) -> dict:
    """Serialize a :class:`ConvergenceResult` to a JSON-safe dict.

    Enumerates fields explicitly — ``convergence.py`` is on the PRESERVE
    list (BUILD-REQUEST §MVR §3), so we cannot add a ``to_dict`` method
    there; the serialization contract is owned by this module.
    """
    return {
        "passed": c.passed,
        "run_count": c.run_count,
        "final_high_count": c.final_high_count,
        "structural_progress_log": list(c.structural_progress_log),
        "semantic_fluctuation_log": list(c.semantic_fluctuation_log),
        "regression_detected": c.regression_detected,
        "halt_reason": c.halt_reason,
    }


def _convergence_from_dict(d: dict) -> ConvergenceResult:
    return ConvergenceResult(
        passed=d["passed"],
        run_count=d["run_count"],
        final_high_count=d["final_high_count"],
        structural_progress_log=list(d.get("structural_progress_log", [])),
        semantic_fluctuation_log=list(d.get("semantic_fluctuation_log", [])),
        regression_detected=d.get("regression_detected", False),
        halt_reason=d.get("halt_reason"),
    )


def envelope_to_dict(envelope: PipelineEnvelope) -> dict:
    """Serialize a :class:`PipelineEnvelope` to a JSON-safe dict.

    The dict shape is the on-disk sidecar format. Field ordering follows
    the §MVR §1 canonical 8-field order, then any future extensions
    appended at the end (none at v1).
    """
    return {
        "release_id": envelope.release_id,
        "spec_hash": envelope.spec_hash,
        "spec_ids": envelope.spec_ids.to_dict(),
        "artifacts": {
            k: _artifact_ref_to_dict(v) for k, v in envelope.artifacts.items()
        },
        "findings": [_finding_to_dict(f) for f in envelope.findings],
        "counts": dict(envelope.counts),
        "convergence": (
            _convergence_to_dict(envelope.convergence)
            if envelope.convergence is not None
            else None
        ),
        "accepted_deviations": [
            _accepted_deviation_to_dict(d) for d in envelope.accepted_deviations
        ],
    }


def envelope_from_dict(d: dict) -> PipelineEnvelope:
    """Deserialize a :class:`PipelineEnvelope` from its JSON-safe dict shape.

    Reverses :func:`envelope_to_dict`. Reconstructs the embedded
    :class:`SpecIdRegistry` via its tuple fields (preserving the R0.1
    hashability invariant). Round-trip stability is exercised by the
    Step 7.4 ``test_envelope_round_trip`` test, including explicit
    assertions that ``list[Finding]`` and ``list[AcceptedDeviation]``
    survive as ``list`` (not ``tuple``) post-deserialize — addresses
    Phase 6 OQ-2.
    """
    spec_ids_d = d["spec_ids"]
    spec_ids = SpecIdRegistry(
        fr_ids=tuple(spec_ids_d.get("fr_ids", ())),
        nfr_ids=tuple(spec_ids_d.get("nfr_ids", ())),
        sc_ids=tuple(spec_ids_d.get("sc_ids", ())),
        g_ids=tuple(spec_ids_d.get("g_ids", ())),
        d_ids=tuple(spec_ids_d.get("d_ids", ())),
        # R5: .get(..., ()) so OLD envelope dicts lacking md_ids round-trip to empty.
        md_ids=tuple(spec_ids_d.get("md_ids", ())),
        accepted_deviation_ids=tuple(spec_ids_d.get("accepted_deviation_ids", ())),
        spec_hash=spec_ids_d["spec_hash"],
        spec_path=Path(spec_ids_d["spec_path"]),
    )
    conv_d = d.get("convergence")
    return PipelineEnvelope(
        release_id=d["release_id"],
        spec_hash=d["spec_hash"],
        spec_ids=spec_ids,
        artifacts={
            k: _artifact_ref_from_dict(v) for k, v in d.get("artifacts", {}).items()
        },
        findings=[_finding_from_dict(f) for f in d.get("findings", [])],
        counts=dict(d.get("counts", {})),
        convergence=(_convergence_from_dict(conv_d) if conv_d is not None else None),
        accepted_deviations=[
            _accepted_deviation_from_dict(x) for x in d.get("accepted_deviations", [])
        ],
    )


# ---------------------------------------------------------------------------
# Atomic sidecar I/O
#
# Mirrors the convergence-result write pattern at
# ``convergence.py:315-317`` (tmpfile.write_text + os.replace = POSIX-
# atomic rename). The dual-write phase relies on these helpers being
# best-effort: if an envelope write fails, the markdown pipeline is
# unaffected (gates still consume markdown), but the failure should be
# logged via ``executor.py``'s existing audit path.
# ---------------------------------------------------------------------------


def save_envelope(envelope: PipelineEnvelope, path: Path) -> None:
    """Atomically persist ``envelope`` to ``path``.

    Writes to ``<path>.tmp`` first, then uses ``os.replace`` (POSIX-atomic
    rename) to swap the final file into place. Creates parent directories
    as needed.

    Failure modes:

    - Disk full / permission denied: raises :class:`OSError`. The caller
      is responsible for logging via the executor's audit path; the
      existing markdown pipeline is unaffected because dual-write gates
      consume markdown, not the envelope (until R1.3+).
    - Mid-write process kill: the ``.tmp`` file may be orphaned but the
      final ``envelope.json`` is never partially written.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text(json.dumps(envelope_to_dict(envelope), indent=2))
    os.replace(str(tmp_path), str(path))


def load_envelope(path: Path) -> PipelineEnvelope:
    """Read an envelope from ``path``. Raises :class:`FileNotFoundError` if missing."""
    text = path.read_text(encoding="utf-8")
    return envelope_from_dict(json.loads(text))


# ---------------------------------------------------------------------------
# POST_EXTRACTORS dispatch map (populated by Step 7.3)
#
# Each registered extractor receives ``(artifact_path, current_envelope)``
# and returns the updated envelope. Because :class:`PipelineEnvelope` is
# ``frozen=True``, extractors MUST construct the updated envelope via
# ``dataclasses.replace(envelope, ...)`` — they cannot mutate in place.
#
# Population happens in Step 7.3 with one entry per step.id verified
# against research/02 §1.1. Until then, this map is empty; envelope
# writes are still functional via direct ``executor.py`` assignments.
# ---------------------------------------------------------------------------


PostExtractor = Callable[[Path, PipelineEnvelope], PipelineEnvelope]
"""Signature for a post-step extractor: (artifact_path, envelope) -> envelope."""


def _minimal_extractor(
    artifact_path: Path,
    envelope: PipelineEnvelope,
    step_id: str,
) -> PipelineEnvelope:
    """R1.2 baseline extractor: hash the artifact + record an :class:`ArtifactRef`.

    Used as the default body for every per-step extractor in this module.
    Each named extractor is a thin wrapper around this helper, registered
    in :data:`POST_EXTRACTORS` under its step ID. Subsequent phases
    (R1.3+) may extend specific extractors to derive counts/findings from
    the markdown artifact via existing ``spec_parser`` helpers — for R1.2
    dual-write, gates do not yet read the envelope, so artifact-ref
    recording is sufficient to satisfy the §MVR §1 substrate-inversion
    contract.

    Contract #6 compliance: this helper introduces no new parser. It
    reads bytes for hashing only.

    Returns the envelope unchanged if ``artifact_path`` does not exist
    (the step failed or its artifact was never written).
    """
    if not artifact_path.exists():
        return envelope
    content_hash = sha256(artifact_path.read_bytes()).hexdigest()[:16]
    ref = ArtifactRef(path=artifact_path, content_hash=content_hash)
    return replace(envelope, artifacts={**envelope.artifacts, step_id: ref})


# ---------------------------------------------------------------------------
# 14 named post-extractors (research/02 §1.1 verified step IDs)
#
# Each function has a stable name so PG7.1 (b) can audit "every step has a
# post-extractor" by symbol-table walk. The bodies are minimal — they all
# delegate to ``_minimal_extractor`` — because R1.2 dual-write only needs
# artifact-ref recording. R1.3+ may extend specific extractors to derive
# counts/findings as gate logic migrates to envelope reads.
#
# ``# TODO: R1.4 tool-write makes this trivial`` markers track the LLM-
# prose-unstable steps where tool-write rewrites in R1.4 will make
# substantive extraction mechanical (the JSON tool output IS the
# canonical state, no markdown re-parsing needed).
# ---------------------------------------------------------------------------


def extract_extract_envelope_fields(
    artifact_path: Path, envelope: PipelineEnvelope
) -> PipelineEnvelope:
    """Extractor for the ``extract`` step (research/02 §1.1, executor.py:2004).

    The R0.1 extract-step wiring already populates ``envelope.spec_ids``
    via ``build_id_registry()`` on the success path; this extractor only
    records the artifact ref to round out the envelope's bookkeeping.
    """
    return _minimal_extractor(artifact_path, envelope, "extract")


def extract_generate_envelope_fields(
    artifact_path: Path, envelope: PipelineEnvelope
) -> PipelineEnvelope:
    """Extractor for the ``generate-{agent.id}`` steps (executor.py:2031, 2049).

    Handles BOTH parallel-group generate-A and generate-B by being
    registered under the ``generate`` prefix in :func:`get_post_extractor`
    (the step IDs are dynamic per ``AgentSpec.id``, e.g. ``generate-
    opus-architect``).

    # TODO: R1.4 tool-write makes this trivial.
    """
    # The step's actual id (e.g. 'generate-opus-architect') is encoded in
    # the artifact filename; we key by the artifact's stem for stability.
    return _minimal_extractor(artifact_path, envelope, artifact_path.stem)


def extract_diff_envelope_fields(
    artifact_path: Path, envelope: PipelineEnvelope
) -> PipelineEnvelope:
    """Extractor for the ``diff`` step (executor.py:2069).

    # TODO: R1.4 tool-write makes this trivial.
    """
    return _minimal_extractor(artifact_path, envelope, "diff")


def extract_debate_envelope_fields(
    artifact_path: Path, envelope: PipelineEnvelope
) -> PipelineEnvelope:
    """Extractor for the ``debate`` step (executor.py:2079).

    # TODO: R1.4 tool-write makes this trivial.
    """
    return _minimal_extractor(artifact_path, envelope, "debate")


def extract_score_envelope_fields(
    artifact_path: Path, envelope: PipelineEnvelope
) -> PipelineEnvelope:
    """Extractor for the ``score`` step (executor.py:2089).

    Future extension (R1.3+): parse convergence score from the artifact
    and populate ``envelope.counts["score.convergence_score"]``. For R1.2
    dual-write, artifact-ref recording is sufficient.

    # TODO: R1.4 tool-write makes this trivial.
    """
    return _minimal_extractor(artifact_path, envelope, "score")


def extract_merge_envelope_fields(
    artifact_path: Path, envelope: PipelineEnvelope
) -> PipelineEnvelope:
    """Extractor for the ``merge`` step (executor.py:2108).

    Future extension (R1.3+): parse roadmap ID set from the merged
    artifact via ``id_registry.extract_roadmap_ids`` and populate
    ``envelope.counts["merge.roadmap_id_count"]``. For R1.2 dual-write,
    artifact-ref recording is sufficient — the existing MERGE_GATE
    SemanticCheck continues to consume markdown directly.

    # TODO: R1.4 tool-write makes this trivial.
    """
    return _minimal_extractor(artifact_path, envelope, "merge")


def extract_anti_instinct_envelope_fields(
    artifact_path: Path, envelope: PipelineEnvelope
) -> PipelineEnvelope:
    """Extractor for the ``anti-instinct`` step (executor.py:2131, deterministic).

    Future extension (R1.3+): parse HIGH count from the audit artifact
    and populate ``envelope.counts["anti-instinct.high_count"]``. For R1.2
    dual-write, artifact-ref recording is sufficient.
    """
    return _minimal_extractor(artifact_path, envelope, "anti-instinct")


def extract_test_strategy_envelope_fields(
    artifact_path: Path, envelope: PipelineEnvelope
) -> PipelineEnvelope:
    """Extractor for the ``test-strategy`` step (executor.py:2141).

    # TODO: R1.4 tool-write makes this trivial.
    """
    return _minimal_extractor(artifact_path, envelope, "test-strategy")


def extract_spec_fidelity_envelope_fields(
    artifact_path: Path, envelope: PipelineEnvelope
) -> PipelineEnvelope:
    """Extractor for the ``spec-fidelity`` step (executor.py:2159).

    Note: in convergence mode the executor runs
    :func:`_run_convergence_spec_fidelity` instead of the LLM subprocess
    (executor.py:1062), and the resulting :class:`ConvergenceResult` is
    written into ``envelope.convergence`` by direct Python assignment in
    that path. This extractor handles only the non-convergence-mode case
    where the LLM produces a markdown artifact.

    Future extension (R1.3+): parse FR-resolution counts and populate
    ``envelope.counts["spec-fidelity.fr_resolved"]``.

    # TODO: R1.4 tool-write makes this trivial.
    """
    return _minimal_extractor(artifact_path, envelope, "spec-fidelity")


def extract_wiring_verification_envelope_fields(
    artifact_path: Path, envelope: PipelineEnvelope
) -> PipelineEnvelope:
    """Extractor for the ``wiring-verification`` step (executor.py:2176, TRAILING gate).

    Future extension (R1.3+): parse wired-symbol counts from the static-
    analysis report and populate ``envelope.counts["wiring.symbol_count"]``.
    For R1.2 dual-write, artifact-ref recording is sufficient.
    """
    return _minimal_extractor(artifact_path, envelope, "wiring-verification")


def extract_deviation_analysis_envelope_fields(
    artifact_path: Path, envelope: PipelineEnvelope
) -> PipelineEnvelope:
    """Extractor for the ``deviation-analysis`` step (executor.py:2187, deterministic).

    Future extension (R1.3+): parse accepted-deviation records from the
    analysis artifact and append to ``envelope.accepted_deviations``. For
    R1.2 dual-write, artifact-ref recording is sufficient — the existing
    deviation-analysis consumers read the markdown directly.
    """
    return _minimal_extractor(artifact_path, envelope, "deviation-analysis")


def extract_remediate_envelope_fields(
    artifact_path: Path, envelope: PipelineEnvelope
) -> PipelineEnvelope:
    """Extractor for the ``remediate`` step (executor.py:2197, deterministic remediation).

    Future extension (R1.3+): parse remediation outcome counts and
    populate ``envelope.counts["remediate.applied"]``. For R1.2
    dual-write, artifact-ref recording is sufficient.
    """
    return _minimal_extractor(artifact_path, envelope, "remediate")


def extract_certify_envelope_fields(
    artifact_path: Path, envelope: PipelineEnvelope
) -> PipelineEnvelope:
    """Extractor for the ``certify`` step (executor.py:build_certify_step).

    Future extension (R1.3+ + R1.5): parse terminal pipeline status into
    ``envelope.counts["certify.status"]`` and integrate with the
    ``verify-implementation`` terminal step (R1.5).

    # TODO: R1.4 tool-write makes this trivial.
    """
    return _minimal_extractor(artifact_path, envelope, "certify")


# ---------------------------------------------------------------------------
# Dispatch map + resolver
# ---------------------------------------------------------------------------


POST_EXTRACTORS: dict[str, PostExtractor] = {
    "extract": extract_extract_envelope_fields,
    "generate": extract_generate_envelope_fields,
    "diff": extract_diff_envelope_fields,
    "debate": extract_debate_envelope_fields,
    "score": extract_score_envelope_fields,
    "merge": extract_merge_envelope_fields,
    "anti-instinct": extract_anti_instinct_envelope_fields,
    "test-strategy": extract_test_strategy_envelope_fields,
    "spec-fidelity": extract_spec_fidelity_envelope_fields,
    "wiring-verification": extract_wiring_verification_envelope_fields,
    "deviation-analysis": extract_deviation_analysis_envelope_fields,
    "remediate": extract_remediate_envelope_fields,
    "certify": extract_certify_envelope_fields,
}
"""Step-id-keyed dispatch map of post-step extractors.

13 entries: 12 static step IDs from research/02 §1.1 + 1 dynamic-prefix
entry (``generate``) for the parallel ``generate-{agent.id}`` group.
:func:`get_post_extractor` resolves dynamic IDs via prefix-match.
"""


def get_post_extractor(step_id: str) -> Optional[PostExtractor]:
    """Resolve the post-extractor for a given step ID.

    Exact-match lookup first; falls back to the ``generate`` extractor for
    dynamic IDs of the form ``generate-{agent.id}`` (e.g.
    ``generate-opus-architect``). Returns ``None`` when no extractor is
    registered — callers (the executor wiring) MUST handle ``None`` as a
    no-op (the dual-write semantics permit a step to have no extractor).
    """
    if step_id in POST_EXTRACTORS:
        return POST_EXTRACTORS[step_id]
    if step_id.startswith("generate-"):
        return POST_EXTRACTORS.get("generate")
    return None
