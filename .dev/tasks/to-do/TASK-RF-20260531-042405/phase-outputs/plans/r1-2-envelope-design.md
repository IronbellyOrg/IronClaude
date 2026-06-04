# R1.2 — PipelineEnvelope Design Document

**Phase:** 7 (R1.2 — PipelineEnvelope Dataclass + Sidecar JSON + Dual-Write Migration)
**Authoring step:** Step 7.1
**Date:** 2026-06-01
**Worktree of execution:** `/config/workspace/IronClaude-RoadmapRewrite/` on `refactor/roadmap-pipeline-r0-r1-rewrite`, parent `daa10416`
**Source authority:** BUILD-REQUEST `§R1.2` (line 170) + `§MVR §1` (lines 84-103) + master:§Flaw 3 + R0.1 `id_registry.py` precedent
**Pre-execution audit:** sc:reflect UC-1 audit (2026-06-01) — REPORT at `.dev/reflect/r1-2-uc1-validation/REPORT.md`; 4 adjustments embedded into this task before this design was authored

---

## 1. Chosen envelope module path

**`src/superclaude/cli/roadmap/envelope.py`** (new file).

Rationale: BUILD-REQUEST §MVR §1 explicitly cites this path (line 87). Keeping the envelope adjacent to `executor.py`, `gates.py`, `convergence.py`, and `id_registry.py` mirrors the rest of the roadmap-pipeline state machinery. `cli/pipeline/models.py` is the wrong home — that module hosts the *substrate* dataclasses (`SemanticCheck`, `GateCriteria`, `Step`, `StepResult`) consumed by every CLI pipeline (sprint, validate, roadmap), whereas `PipelineEnvelope` is roadmap-specific cross-step state. Per research/01 §A.8 L210-216, `models.py` (under `cli/roadmap/`) holds *RoadmapConfig* (inputs/flags, no cross-step state); the envelope is precisely the cross-step-state cousin that belongs in its own module.

## 2. `PipelineEnvelope` dataclass — field list verbatim from §MVR §1

The canonical 8-field shape per BUILD-REQUEST §MVR §1 lines 89-99 is:

| # | Field | Type (§MVR §1 literal) | Bound type (this design) | Notes |
|---|---|---|---|---|
| 1 | `release_id` | `str` | `str` | Release identifier (matches `<release>` in `.<release>/envelope.json` path) |
| 2 | `spec_hash` | `str` | `str` | SHA-256 of spec content; matches R0.1 `SpecIdRegistry.spec_hash` (16-char prefix) for consistency |
| 3 | `spec_ids` | `SpecIdRegistry` | `SpecIdRegistry` (imported from `id_registry.py`) | Absorbs R0.1 sidecar — see §6 below |
| 4 | `artifacts` | `dict[StepId, ArtifactRef]` | `dict[str, ArtifactRef]` | `StepId` is a phantom type (§MVR §1 names it but no `StepId` class exists in the codebase); using `str` keyed on the literal step id values verified at research/02 §1.1 (extract, generate-{agent}, diff, debate, score, merge, anti-instinct, test-strategy, spec-fidelity, wiring-verification, deviation-analysis, remediate, certify). `ArtifactRef` is a new supporting dataclass defined here. |
| 5 | `findings` | `list[Finding]` | `list[Finding]` (imported from `cli/roadmap/models.py:21`) | Typed, additive across steps |
| 6 | `counts` | `dict[str, int]` | `dict[str, int]` | Gate-pass signals — **written by Python only, NEVER by an LLM** (master:§Flaw 3 invariant) |
| 7 | `convergence` | `ConvergenceState \| None` | **`ConvergenceResult \| None`** (imported from `cli/roadmap/convergence.py:321`) | **sc:reflect UC-1 finding (2026-06-01):** §MVR §1 literally names `ConvergenceState` but the codebase has `RunMetadata` (L75) and `ConvergenceResult` (L321) and **no `ConvergenceState` class**. Recommended binding is `ConvergenceResult` (the terminal convergence verdict — `passed`, `run_count`, `final_high_count`, `regression_detected`, `halt_reason`). `RunMetadata` is per-run metadata (orthogonal to convergence outcome). The envelope's `convergence` slot should hold the terminal verdict, populated post-convergence step; `None` when convergence step has not yet run or is disabled. PG7.1 (a) "matches §MVR §1 verbatim" is evaluated against this explicit binding rather than the literal §MVR string. |
| 8 | `accepted_deviations` | `list[AcceptedDeviation]` | `list[AcceptedDeviation]` | `AcceptedDeviation` is a new supporting dataclass defined here (per §MVR §1 the type is named but not defined) |

Decorator: `@dataclass(frozen=True)` per §MVR §1 line 88.

### Supporting dataclasses (new, defined in `envelope.py`)

```python
@dataclass(frozen=True)
class ArtifactRef:
    """Reference to a step's artifact on disk + a content hash for drift detection."""
    path: Path            # absolute or relative to envelope.json's parent
    content_hash: str     # SHA-256 hex digest (16-char prefix, matches spec_hash convention)


@dataclass(frozen=True)
class AcceptedDeviation:
    """Per-pipeline accepted deviation record, absorbed from accept-spec-change flow."""
    id: str               # e.g. "D-7"
    reason: str           # human-authored rationale
    timestamp: str        # ISO-8601 string (matches the timestamp shape used elsewhere)
```

Both are `frozen=True` for hashability + safe-to-pass-across-pipeline-boundaries (matching R0.1's `SpecIdRegistry` precedent).

### Module helpers (also in `envelope.py`)

- `def load_envelope(path: Path) -> PipelineEnvelope` — atomic read; deserializes from JSON.
- `def save_envelope(envelope: PipelineEnvelope, path: Path) -> None` — **atomic write** via tmpfile + `os.replace` (matches `convergence.py:315-317` precedent in the codebase).
- `POST_EXTRACTORS: dict[str, Callable[[Path, PipelineEnvelope], PipelineEnvelope]]` — dispatch map populated in Step 7.3.

### Dispatch-extractor signature (Step 7.3 contract)

```python
def extract_<step_id>_envelope_fields(artifact_path: Path, envelope: PipelineEnvelope) -> PipelineEnvelope:
    """Parse the step's artifact deterministically (via existing spec_parser helpers — Contract #6:
    no new parsers) and return an envelope updated with that step's canonical fields (counts,
    findings, artifact ref + content_hash). Pure function; envelope is immutable (frozen=True) so
    returns a new instance via dataclasses.replace."""
```

### Field-set conformance test (sc:reflect UC-1 / G3)

Step 7.4 will assert:

```python
{f.name for f in dataclasses.fields(PipelineEnvelope)} == {
    "release_id", "spec_hash", "spec_ids", "artifacts",
    "findings", "counts", "convergence", "accepted_deviations",
}
```

Catches any future field-drift from §MVR §1.

## 3. Sidecar JSON path convention

**`<output_dir>/envelope.json`** — replaces the R0.1 proto-sidecar `<output_dir>/spec_id_registry.json`.

- `<output_dir>` resolves to the release directory (`.<release>/`) per §MVR §1 line 101.
- During the dual-write phase (§4), both files persist; consumers of `spec_id_registry.json` continue to read it until R1.6.
- JSON shape is the dataclass tree serialized via a custom `to_dict()` (mirrors R0.1 precedent at `id_registry.py:106-122`); Path values render as strings.

## 4. Post-step extractor pattern

Per §MVR §1 line 101: *"every step reads the envelope, writes its artifact, and a deterministic Python post-step extracts canonical fields into the envelope. LLM never writes gate-pass counts directly."*

### Mechanics

1. After every LLM step (`extract`, `generate-A`, `generate-B`, `diff`, `debate`, `score`, `merge`, `test-strategy`, `spec-fidelity`, `remediate`, `certify`) and every non-LLM step (`anti-instinct`, `wiring-verification`, `deviation-analysis`), the dispatch site at `executor.roadmap_run_step` (**L1021 in RoadmapRewrite HEAD `daa10416`** — note: tasklist preamble cites L955 from BareReview pre-R0.1/R1.1 state) invokes `POST_EXTRACTORS[step.id]` with the step's artifact path and the current envelope.
2. The extractor parses the artifact using **existing `spec_parser` helpers only** — no new parsers added (Contract #6 anti-duplication).
3. The extractor returns an updated `PipelineEnvelope` (immutable; via `dataclasses.replace`). The orchestrator persists it to `envelope.json` via the atomic `save_envelope` helper.

### 14-step dispatch map (matches research/02 §1.1 verified step IDs + `build_certify_step`)

| # | Step ID | Source | R1.2 extractor mode |
|---|---|---|---|
| 1 | `extract` | executor.py:_build_steps L2004 | full (writes spec_hash + initial findings) |
| 2 | `generate-A` (e.g. `generate-{agent_a.id}`) | L2031 | minimal (artifact ref + content hash; LLM-prose dominant — R1.4 makes counts trivial) |
| 3 | `generate-B` (e.g. `generate-{agent_b.id}`) | L2049 | minimal (same) |
| 4 | `diff` | L2069 | minimal |
| 5 | `debate` | L2079 | minimal |
| 6 | `score` | L2089 | partial (extract convergence score → `counts`) |
| 7 | `merge` | L2108 | full (extract roadmap_ids via `id_registry.extract_roadmap_ids` for the §9 Contract test surface) |
| 8 | `anti-instinct` | L2131 (non-LLM) | full (extract HIGH counts) |
| 9 | `test-strategy` | L2141 | minimal |
| 10 | `spec-fidelity` | L2159 | full (extract FR-resolution counts → `counts`) |
| 11 | `wiring-verification` | L2176 (non-LLM, TRAILING) | full (extract wired-symbol counts) |
| 12 | `deviation-analysis` | L2187 (non-LLM) | full (extract accepted-deviation IDs → `accepted_deviations`) |
| 13 | `remediate` | L2197 (non-LLM) | full (extract remediation result counts) |
| 14 | `certify` | executor.py:build_certify_step L1977 (in RoadmapRewrite; tasklist cites L1899 from BareReview) | full (extract terminal convergence + status) |

For steps where the LLM-prose artifact format is unstable (R1.2 has no tool-write yet), the extractor is a **no-op stub** that records only `artifacts[step.id] = ArtifactRef(path, content_hash)` with a `# TODO: R1.4 tool-write makes this trivial` comment (per Step 7.3 task instruction).

### Master:§Flaw 3 invariant — LLM never writes counts

`envelope.counts` and `envelope.findings` are populated ONLY by:
- The 14 Python post-extractors above.
- Direct Python assignments from `executor.py` (e.g., gate-pass result wiring).

There is **no codepath** where LLM output flows directly into `envelope.counts`. The substrate inversion is achieved by:
1. LLM steps write markdown artifacts (the prompt response).
2. Python post-extractors read those artifacts and *derive* counts deterministically.
3. The envelope is the only state passed to the next step's gate evaluator.

This **kills master:§Flaw 3** at the substrate layer.

## 5. Dual-write migration strategy

Per BUILD-REQUEST §R1.2 line 170: *"Dual-write with markdown for one release cycle, then markdown becomes render-only."*

### Cutover criterion: **1 release cycle** (Vector A precedent; explicit verbatim trigger)

A "release cycle" is one end-to-end `superclaude roadmap run` against a real spec in `.dev/releases/Current/<release>/` that:

1. Completes all 14 pipeline steps without halting.
2. Produces both the markdown artifacts (per the current pipeline) AND an `envelope.json` whose `counts`/`findings` reconcile with the markdown.
3. Passes all 10 Contract gates (post Phase 13 final acceptance).

After one such cycle passes, **R1.6** (Phase 11) is unblocked to delete the markdown-as-substrate code paths. R1.2 itself does NOT delete markdown — markdown remains the consumed substrate during the dual-write phase.

### Concretely, during the dual-write phase

| Concern | Behavior |
|---|---|
| Markdown artifacts | Still written by every step (no change to existing prompt outputs). |
| Markdown-consuming gates | Still consume markdown; gates do NOT read the envelope yet (R1.3 wires the first `code_assertions` to use the envelope). |
| Envelope writes | Every step appends to `envelope.json` via the atomic `save_envelope` helper. |
| Envelope reads | Only for Step 7.4 round-trip tests and Step 7.3 dispatch verification. The pipeline itself does NOT route logic through the envelope yet — that's R1.3+. |
| R0.1 `spec_id_registry.json` | Still written (no change to R0.1 wiring); the envelope's `spec_ids` field mirrors the same data for downstream R1.3+ consumers. |
| Failure modes | If `save_envelope` fails for any reason, the markdown pipeline is unaffected — log the failure to `_save_state`'s existing audit path, continue. Envelope writes are best-effort during dual-write. |

### Verifiability

PG7.1 (f) explicitly verifies dual-write preserves existing markdown — by diffing markdown output before/after a sample roadmap run with envelope writes enabled. The reflect-added (i)/(j) sub-bullets verify dispatch reachability + field-set conformance.

## 6. `migrate_id_registry_to_envelope` plan — R0.1 absorption

### Current R0.1 state (HEAD `daa10416`)

R0.1 ships `id_registry.py` with `SpecIdRegistry` (8 fields, frozen+hashable, `to_dict()`-serializable). The extract step's success path persists `<output_dir>/spec_id_registry.json`. The MERGE_GATE SemanticCheck reads that JSON to enforce Contract #9.

### R1.2 absorption

1. **Envelope creation point.** The extract step's post-extractor (Step 7.3) calls `id_registry.build_id_registry()` (the existing R0.1 entry point), then sets:
   ```python
   envelope = dataclasses.replace(
       envelope,
       spec_ids=registry,
       spec_hash=registry.spec_hash,
   )
   ```
2. **Sidecar writes during dual-write.** Both `spec_id_registry.json` (R0.1 path) AND `envelope.json` (R1.2 path) are written. Their `spec_ids` content is identical (the envelope JSON serializes `SpecIdRegistry` via its existing `to_dict()`).
3. **R0.1 consumers unaffected.** `gates.py`'s MERGE_GATE SemanticCheck continues to read `spec_id_registry.json` until R1.3 wires the first `code_assertions` to read from `envelope.json` directly. R1.6 then deletes `spec_id_registry.json` writes.
4. **TODO marker.** `envelope.py` carries a `# TODO: R1.6 — delete spec_id_registry.json writes (envelope.spec_ids supersedes)` comment at the `spec_ids` field site so the deletion target is visible.

### Preservation guarantee

During the entire dual-write phase (1+ release cycles), `spec_id_registry.json` and `envelope.json` MUST agree on `spec_ids` content. Step 7.4 tests assert: `load_envelope(path).spec_ids == load_id_registry(path.parent / "spec_id_registry.json")`.

## 7. Step 7.4 test surface (informed by §6.4 of sc:reflect REPORT)

Tests required by Step 7.4:

| Test | Source | Purpose |
|---|---|---|
| `test_envelope_round_trip` | original | `save_envelope` → `load_envelope` equality, AND explicit assertions that `list[Finding]` and `list[AcceptedDeviation]` survive as `list` not `tuple` post-deserialize (addresses Phase 6 OQ-2) |
| `test_envelope_atomic_write` | original | No partial-write file present on simulated interrupt; tmpfile pattern |
| `test_post_extractors_dispatch_complete` | original | Every step in `_build_steps()` has a `POST_EXTRACTORS` entry |
| `test_post_extractors_dispatch_reachable` | **sc:reflect UC-1 G1 (Contract #2)** | AST walk asserting every `POST_EXTRACTORS[step_id]` call is reachable from `executor.roadmap_run_step` — map-completeness alone is necessary but not sufficient |
| `test_envelope_field_set_conformance` | **sc:reflect UC-1 G3** | `{f.name for f in dataclasses.fields(PipelineEnvelope)} == <§MVR §1 canonical 8-field set>`; catches future drift from §MVR §1 |
| `test_dual_write_preserves_markdown` | original (PG7.1 (f)) | Sample roadmap run with envelope enabled produces byte-identical markdown vs without |
| `test_r0_1_consumer_preserved` | §6 above | `spec_id_registry.json` and `envelope.json` agree on `spec_ids` content |

## 8. Out-of-scope for R1.2 (deferred)

- **Gate logic consumes envelope.** R1.3 wires the first `code_assertions` to read from the envelope; R1.2 only produces it.
- **Markdown deletion.** R1.6 (Phase 11) deletes markdown-as-substrate code paths after dual-write cycle passes.
- **Tool-write at LLM steps.** R1.4 (Phase 9) rewrites 9 LLM steps as tool-write; R1.2's no-op stubs for unstable artifact formats are placeholders until then.
- **`verify-implementation` terminal step.** R1.5 (Phase 10) — separate phase.

## 9. Acceptance against §MVR §1 (verbatim check)

A direct mapping from §MVR §1 lines 84-103 to this design:

| §MVR §1 mandate | This design honors it via |
|---|---|
| New file `src/superclaude/cli/roadmap/envelope.py` | §1 |
| `@dataclass(frozen=True) class PipelineEnvelope` | §2 |
| 8 fields exact (`release_id`, `spec_hash`, `spec_ids`, `artifacts`, `findings`, `counts`, `convergence`, `accepted_deviations`) | §2 table; only deviation from literal §MVR is the `convergence` type binding (`ConvergenceResult` instead of literal `ConvergenceState`) documented explicitly per sc:reflect UC-1 finding |
| "Persisted as `.<release>/envelope.json`" | §3 |
| "every step reads the envelope, writes its artifact, and a deterministic Python post-step extracts canonical fields" | §4 |
| "LLM never writes gate-pass counts directly" | §4 invariant section |
| "Kills master:§Flaw 3" | §4 invariant section |
| Dual-write strategy 1 release cycle | §5 (explicit cutover criterion named "1 release cycle") |
| R0.1 `spec_id_registry.json` absorbed into `spec_ids` field | §6 |

PG7.1 (a) will audit against this table.

---

**End of Step 7.1 design document.**
