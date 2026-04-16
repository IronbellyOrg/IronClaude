# Roadmap Pipeline Compression Refactor — Design Document

**Date**: 2026-04-15
**Status**: DESIGN (no code changes yet)
**Target**: `src/superclaude/cli/roadmap/` (commands.py, executor.py, prompts.py, gates.py, models.py)
**Depends on**: [compressed-markdown-dsl-primer.md](./compressed-markdown-dsl-primer.md) — strategy details live there, not here
**Upstream validation**: [adversarial-roadmap-formats-20260415/adversarial/return-contract.yaml](./adversarial-roadmap-formats-20260415/adversarial/return-contract.yaml) — convergence 0.80, status `partial`, 3 HIGH UNADDRESSED invariants

---

## 1. Goal

Insert Compact Markdown DSL compression at **three natural points** in the `superclaude roadmap run` pipeline so that every agent subprocess (extract, generate×2, diff, debate, score, merge, test-strategy, spec-fidelity, etc.) reads a token-reduced form of its inputs without paying an accuracy tax. The three points:

| # | Point | What is compressed | When | Primary win |
|---|-------|--------------------|------|-------------|
| **C1** | **Ingest** | `spec_file`, `tdd_file`, `prd_file` | Once, before `extract` | Every downstream step that embeds the source pays a lower token bill |
| **C2** | **Mid-pipeline** | `roadmap-{agent_a}.md`, `roadmap-{agent_b}.md` | After `generate-*`, before `diff`/`debate`/`score`/`merge` | The four adversarial steps are the single largest consumer of variant bytes; compressing there has the largest multiplier |
| **C3** | **Output** | `roadmap.md` (merged) | After `merge`, before persistence | Emitted artifact is consumed by `sc:tasklist`, `sc:pm`, `sc:validate-roadmap`, CI, human reviewers; every future read inherits the saving |

All three are **opt-in behind flags** and **gated by a fidelity checksum** that can roll back to the uncompressed original if the compressed form fails validation.

---

## 2. Non-Goals

- **Not** inventing a new file format. Compact MD DSL is standard CommonMark — see primer §1.
- **Not** changing the pipeline step count or DAG shape. Compression is a **pre-step** on specific Step inputs, not a new phase in the state machine.
- **Not** touching `sc:adversarial` itself. The validated recommendation already emerged from that pipeline; this design applies the recommendation inside the sibling `superclaude roadmap run` CLI.
- **Not** compressing Haiku-consumed paths until INV-5 clears (see §8).
- **Not** compressing the `spec_file` input to `spec-fidelity` / `wiring-verification` / `deviation-analysis` / `anti-instinct` — those steps compare against **the original spec as the ground truth**. Compressing the reference would poison those gates. See §5.2.

---

## 3. Current Pipeline Reference (for diff-readability)

From `src/superclaude/cli/roadmap/executor.py::_build_steps` (executor.py:1299-1488):

```
extract                         inputs: [spec_file, tdd_file?, prd_file?]
├─ generate-{agent_a}  (parallel)  inputs: [extraction, tdd_file?, prd_file?]
└─ generate-{agent_b}  (parallel)  inputs: [extraction, tdd_file?, prd_file?]
diff                            inputs: [roadmap_a, roadmap_b]
debate                          inputs: [diff_file, roadmap_a, roadmap_b]
score                           inputs: [debate_file, roadmap_a, roadmap_b, tdd_file?, prd_file?]
merge                           inputs: [score_file, roadmap_a, roadmap_b, debate_file, tdd_file?, prd_file?]
anti-instinct                   inputs: [spec_file, merge_file]           ← MUST read original spec
test-strategy                   inputs: [merge_file, extraction, tdd_file?, prd_file?]
spec-fidelity                   inputs: [spec_file, merge_file, tdd_file?, prd_file?]  ← MUST read original spec
wiring-verification             inputs: [merge_file, spec_fidelity_file]  ← MUST read original spec (via fidelity)
deviation-analysis              inputs: [spec_fidelity_file, merge_file]
remediate                       inputs: [deviation_file, spec_fidelity_file, merge_file]
certify (dynamic)               inputs: [remediation_file, ...]
```

The three compression points attach as follows:

```
                  ┌──[C1: compress spec/tdd/prd]──┐
                  │                               │
                  ▼                               │
               extract                            │
                  │                               │
                  ▼                               │
         ┌─ generate-a                            │
         └─ generate-b                            │
                  │                               │
         ┌──[C2: compress variant_a, variant_b]   │
         │                                        │
         ▼                                        │
               diff                               │
               debate                             │
               score                              │
               merge ──[produces roadmap.md]      │
                  │                               │
                  ▼                               │
               anti-instinct  ←── reads raw spec_file (NOT C1)
               test-strategy                      │
               spec-fidelity  ←── reads raw spec_file (NOT C1)
               wiring-verif                       │
               deviation-analysis                 │
               remediate                          │
                  │                               │
                  ▼                               │
         ┌──[C3: compress roadmap.md → roadmap.cmd.md]
         │     (optional; roadmap.md retained as ground truth)
         ▼
             certify
```

Key insight: **C1 substitutes inputs for LLM-only steps (extract, generate, test-strategy)**, **C2 substitutes inputs for adversarial steps (diff/debate/score/merge)**, and **C3 emits an additional artifact** without replacing the canonical `roadmap.md`.

---

## 4. Architectural Changes

### 4.1 New module: `src/superclaude/cli/roadmap/compression/`

```
compression/
├── __init__.py          # Public API: compress(), decompress(), fidelity_check()
├── strategies.py        # Approach1RuleBased, Approach2ASTAware, Approach3LLMAssisted
├── conventions.py       # ConventionsHeader builder, abbrev resolver, serializer
├── fidelity.py          # Semantic-equivalence check + tiktoken delta measurement
├── registry.py          # document_type → strategy selection (matrix from primer §5)
└── models.py            # CompressionResult, CompressionManifest, FidelityReport
```

The three strategies are named after the primer's three approaches (§4 of primer):
- `Approach1RuleBased` — textual, regex-driven, whitespace/decorative/preamble stripping. Deterministic. ~12-18% ceiling.
- `Approach2ASTAware` — parses via `markdown-it-py`, operates on the token stream, handles tables/lists/code-fences semantically. Deterministic. ~25-33% ceiling (matches V-B's measured -33.4%).
- `Approach3LLMAssisted` — calls an auditor agent with a "rewrite for minimum tokens, preserve all assertions" prompt. Non-deterministic. ~35-50% ceiling. **Requires a fidelity auditor pass** before being accepted.

### 4.2 Public API

```python
# compression/__init__.py
def compress(
    source: Path,
    document_type: Literal["roadmap", "prd", "spec", "tdd", "tasklist"],
    strategy: Literal["auto", "rule", "ast", "llm"] = "auto",
    target_model: Literal["opus", "sonnet", "haiku"] = "opus",
    output: Path | None = None,
) -> CompressionResult: ...

def fidelity_check(
    original: Path,
    compressed: Path,
    checks: list[Literal["token_delta", "heading_set", "ref_set", "table_rows", "code_fences", "claim_sample"]],
) -> FidelityReport: ...

def decompress(compressed: Path, conventions: ConventionsHeader) -> str:
    """Reversible textual expansion for human review or rollback."""
```

`CompressionResult` includes:
- `output_path`, `strategy_used`, `conventions_header_tokens`
- `tokens_before`, `tokens_after`, `delta_pct` (measured via `tiktoken` **and** `anthropic.messages.count_tokens` when available — see INV-1 in §8)
- `fidelity_report` (always attached)
- `rollback_to` (original path, retained even on success)

### 4.3 `CompressionManifest` — provenance record

Every compressed artifact writes a sidecar `{name}.compression.json`:

```json
{
  "source": "spec.md",
  "output": "spec.cmd.md",
  "strategy": "ast",
  "target_model": "opus",
  "tokens_before_tiktoken": 14820,
  "tokens_after_tiktoken": 9874,
  "delta_pct_tiktoken": -33.4,
  "tokens_before_claude_native": null,
  "tokens_after_claude_native": null,
  "conventions_header_sha256": "ab12…",
  "fidelity_checks": {
    "heading_set": "PASS",
    "ref_set": "PASS",
    "table_rows": "PASS",
    "code_fences": "PASS",
    "claim_sample": "PASS (20/20 sampled assertions recoverable)"
  },
  "produced_at": "2026-04-15T18:07:22Z",
  "produced_by": "compression.strategies.Approach2ASTAware@v1",
  "rollback_to": "spec.md"
}
```

The manifest is the audit trail for INV-1 and INV-5 — it records which tokenizer produced each number and whether a Claude-native re-measurement has been populated.

### 4.4 `RoadmapConfig` additions (models.py)

```python
@dataclass
class RoadmapConfig(PipelineConfig):
    # ... existing fields ...

    # --- Compression (new) ---
    compress_ingest: bool = False           # C1 flag
    compress_variants: bool = False         # C2 flag
    compress_output: bool = False           # C3 flag
    compression_strategy: Literal["auto", "rule", "ast", "llm"] = "auto"
    compression_fidelity_floor: float = 0.99   # reject compression if fidelity < 99%
    compression_min_delta_pct: float = -5.0    # reject if savings < 5% (not worth the risk)
    compression_target_model: Literal["opus", "sonnet", "haiku"] = "opus"
```

CLI equivalent on `commands.py::run`:

```python
@click.option("--compress-ingest", is_flag=True, default=False,
    help="Apply Compact MD DSL compression to spec/TDD/PRD before extract. "
         "Gated by fidelity check; falls back to uncompressed on failure.")
@click.option("--compress-variants", is_flag=True, default=False,
    help="Compress generated variant roadmaps before diff/debate/score/merge.")
@click.option("--compress-output", is_flag=True, default=False,
    help="Emit an additional roadmap.cmd.md alongside roadmap.md. Canonical "
         "roadmap.md is never replaced (consumer-DAG safety, INV-3).")
@click.option("--compression-strategy",
    type=click.Choice(["auto", "rule", "ast", "llm"]), default="auto",
    help="Override document-type strategy selection.")
@click.option("--compress-all", is_flag=True, default=False,
    help="Shortcut for --compress-ingest --compress-variants --compress-output.")
```

### 4.5 New deterministic Steps — C1, C2, C3 as first-class pipeline members

The pipeline already has non-LLM deterministic steps (anti-instinct, deviation-analysis, remediate) so compression fits the existing Step contract. Each compression point is a `Step` with `prompt=""` and a custom `runner` hook (to be added to `execute_roadmap`).

```python
# Injected by _build_steps when flags are set

# C1 — ingest (runs before extract; no gate change on extract)
Step(
    id="compress-ingest",
    prompt="",
    output_file=out / ".compression/ingest-manifest.json",
    gate=COMPRESS_INGEST_GATE,
    timeout_seconds=60,
    inputs=[config.spec_file] + ([config.tdd_file] if config.tdd_file else []) + ([config.prd_file] if config.prd_file else []),
    retry_limit=0,
),

# C2 — variants (runs after both generate-* complete; in front of diff)
Step(
    id="compress-variants",
    prompt="",
    output_file=out / ".compression/variants-manifest.json",
    gate=COMPRESS_VARIANTS_GATE,
    timeout_seconds=60,
    inputs=[roadmap_a, roadmap_b],
    retry_limit=0,
),

# C3 — output (runs after merge, before certify)
Step(
    id="compress-output",
    prompt="",
    output_file=out / ".compression/output-manifest.json",
    gate=COMPRESS_OUTPUT_GATE,
    timeout_seconds=60,
    inputs=[merge_file],
    retry_limit=0,
),
```

### 4.6 How compression changes downstream Step `inputs`

Rather than mutating the files in place, C1/C2 **write compressed siblings** and the subsequent Steps read the sibling when the flag is set:

```python
# _build_steps selects the effective input path
eff_spec    = out / "spec.cmd.md"   if config.compress_ingest  else config.spec_file
eff_tdd     = out / "tdd.cmd.md"    if config.compress_ingest and config.tdd_file else config.tdd_file
eff_prd     = out / "prd.cmd.md"    if config.compress_ingest and config.prd_file else config.prd_file
eff_road_a  = out / f"roadmap-{agent_a.id}.cmd.md" if config.compress_variants else roadmap_a
eff_road_b  = out / f"roadmap-{agent_b.id}.cmd.md" if config.compress_variants else roadmap_b
```

Then:
- `extract` reads `eff_spec`, `eff_tdd`, `eff_prd`
- `generate-*` read `extraction` (unchanged — extraction output is re-authored by the model)
- `diff`/`debate`/`score`/`merge` read `eff_road_a`, `eff_road_b`
- **BUT** `anti-instinct`, `spec-fidelity`, `wiring-verification` **always** read `config.spec_file` (never `eff_spec`) — this is the fidelity firebreak described in §5.2

The original files are never deleted, so `--resume`, `accept-spec-change`, and the state-hash machinery continue to work against the authoritative sources.

---

## 5. Fidelity Gates and Firebreaks

### 5.1 `COMPRESS_*_GATE` definitions (gates.py additions)

Each compression gate runs **after** the compression produces its artifact and **before** downstream consumers run:

```python
COMPRESS_INGEST_GATE = Gate(
    required_sections=[],         # not a markdown gate
    structural_checks=[
        check_compression_manifest_exists,
        check_compression_fidelity_floor,    # >= config.compression_fidelity_floor
        check_compression_delta_threshold,   # delta_pct <= config.compression_min_delta_pct
        check_conventions_header_valid,
        check_heading_set_preserved,
        check_internal_refs_preserved,
    ],
    on_fail="ROLLBACK_TO_ORIGINAL",  # new gate disposition (see 5.3)
)
```

**On gate failure**, instead of HALTing the pipeline (the default for extract/generate/etc.), the compression gate:

1. Logs a WARNING with the failed check
2. Rewrites the effective path mapping to point at the original uncompressed file
3. Annotates the manifest with `status: "fell_back"` and the reason
4. Marks the Step `PASS` (not `FAIL`) with a `rollback=True` flag
5. Continues the pipeline

This keeps compression **strictly opt-in and strictly non-blocking** — a compression bug can never prevent a roadmap from being produced.

### 5.2 The spec-fidelity firebreak (critical)

Compressing the spec and then running `spec-fidelity` against the compressed spec would create a tautology: the fidelity audit would be comparing the merged roadmap against an already-transformed reference. Any assertion dropped by compression would be invisibly dropped from the fidelity ground truth.

**Design rule**: `anti-instinct`, `spec-fidelity`, `wiring-verification`, and `deviation-analysis` **always** receive `config.spec_file` (the raw original). This is enforced at `_build_steps` construction time and audit-logged. `test-strategy` and `extract`/`generate` are LLM synthesis steps — they can safely read `eff_spec`.

### 5.3 New gate disposition: `ROLLBACK_TO_ORIGINAL`

Extend `gates.py::GateMode` (or introduce `GateDisposition`) with `ROLLBACK_TO_ORIGINAL`. Current dispositions include `BLOCKING`, `TRAILING`; the new one is used exclusively by compression gates. The executor's gate evaluator checks the disposition and, on failure, calls back into `compression.__init__.rollback(manifest)` to restore effective paths.

This avoids overloading existing semantics of `retry_limit` or `fail_hard`.

### 5.4 Claim-sample fidelity check

The strongest gate check. For a compressed document:
1. Parse the original into sentences/bullets/table rows → sample N assertions (default 20, stratified across sections)
2. For each assertion, ask a **separate auditor LLM call** (fast model, no context pollution): "Is this assertion preserved in the compressed text?" with both documents attached
3. Require ≥95% preservation rate (configurable)
4. Fail the gate if any **HIGH-severity** assertion (headings, acceptance criteria, gate conditions, invariants) is missing

This is the only gate that costs LLM tokens. It is **mandatory for Approach 3 (LLM-assisted)**, **optional for Approach 2 (AST)**, and **skipped for Approach 1 (rule-based)** — because rule-based transforms are provably lossless by construction.

---

## 6. Document-Type Routing

The strategy selection matches the primer's §5 matrix:

| Document | Strategy | Flags | Expected delta | Fidelity floor |
|----------|----------|-------|----------------|----------------|
| `spec` | Approach 1 only | `--compress-ingest` | 10-15% | 0.999 (near-lossless required) |
| `prd` | Approach 1 → Approach 3 (LLM audit) | `--compress-ingest` | 35-45% | 0.99 + claim-sample |
| `tdd` | Approach 1 → Approach 2 (code-fence-aware) | `--compress-ingest` | 15-25% | 0.999 |
| `roadmap` (variant, C2) | Approach 2 + auto-conventions-header | `--compress-variants` | 25-33% | 0.99 + claim-sample |
| `roadmap` (merged, C3) | Approach 2 | `--compress-output` | 25-33% | Emit both raw + compressed |

This table is implemented in `compression/registry.py`. `--compression-strategy` overrides it.

---

## 7. Cost Model (why the flag is off by default)

| Compression cost | Approach 1 | Approach 2 | Approach 3 |
|------------------|-----------|-----------|-----------|
| Wall-clock added | <1s | 1-3s | 15-60s (LLM call) |
| Tokens added (auditor) | 0 | 0 or 500 (claim-sample) | 2-5k (rewriter) + 500 (auditor) |
| Risk of fidelity fail | ~0% | <1% | 2-5% |
| Rollback cost | 0 | 0 | 0 |

For a typical roadmap run (extract + 2×generate + 4 adversarial + 5 audit steps), C1 alone reduces downstream read cost by roughly:

```
savings_per_step ≈ delta_pct × read_fraction_of_spec
total_savings    ≈ savings_per_step × steps_that_read_spec
```

With 6 steps reading the spec and `-15%` on Approach 1, the absolute saving is about **90% of one spec-read** per pipeline. At -33% on C2 variants across 4 adversarial steps, the saving is about **132% of one variant-read** per pipeline. The compression step itself costs ~1s of wall clock — the ROI is clearly positive, but only once INV-1 (tokenizer) confirms the tiktoken numbers translate to Claude-native numbers within tolerance.

**Default**: all three flags OFF. Opt-in until INV-1/INV-5 clear.

---

## 8. Production Prerequisites — UNADDRESSED Invariants Carry-Forward

The adversarial validation flagged 3 HIGH-severity blind spots that this refactor **must address before production rollout**. Each is a hard prerequisite on a flag, not an advisory note.

### INV-1 — Tokenizer measurement (`cl100k_base` vs Claude native)

**Assumption**: tiktoken `cl100k_base` delta approximates Claude 4.6's native tokenization.
**Risk to this design**: the `-33.4%` that justified Approach 2 was measured on `cl100k_base`. Claude-native tokenization of the same slice could differ materially.
**Prerequisite**: Re-run the Phase 2 slice measurement using Anthropic's `messages.count_tokens` endpoint against `claude-opus-4-6` and `claude-haiku-4-5`. Accept Approach 2's compression ceiling only if relative delta stays within ±3pp of the `cl100k_base` number.
**Enforcement**: `CompressionResult.tokens_before_claude_native` / `tokens_after_claude_native` are `null` by default. The gate `check_compression_delta_threshold` evaluates against `tiktoken` now and **must** evaluate against `claude_native` when `--compression-target-model=opus|sonnet|haiku` is set once the SDK is wired up. Until then, log a WARNING per run containing `delta measured with cl100k_base; Claude-native unverified`.

### INV-3 — Consumer DAG enumeration

**Assumption**: roadmap files are consumed primarily by one pipeline stage with a dominant read pattern.
**Risk to this design**: if the final `roadmap.md` is also consumed by `sc:tasklist`, `sc:pm`, `sc:validate-roadmap`, `sc:adversarial`, CI, human reviewers, then C3 **cannot replace** `roadmap.md` in place — each consumer has a different tolerance for compressed form (humans want the uncompressed one; LLM consumers want the compressed one; CI grep may want raw ASCII).
**Prerequisite before merging**: Enumerate the consumer DAG. Populate `claudedocs/roadmap-consumer-dag.md` with the list of all tools/scripts/gates/agents/humans that read `roadmap.md` and their read patterns (whole-file / phase-scoped / field-scoped).
**Enforcement in this design**: C3 **never replaces** `roadmap.md`. It writes `roadmap.cmd.md` alongside, and the manifest records which consumer should read which form. The default remains that `roadmap.md` is canonical; downstream consumers must explicitly opt in by reading `roadmap.cmd.md`. This is the least-disruption default until the DAG audit completes.

### INV-5 — Haiku accuracy A/B untested on candidate formats

**Assumption**: webmaster-ramos's single Haiku data point (69.6% MD, 75.3% JSON, 74.8% TOON) generalizes to the candidate formats.
**Risk to this design**: Compressed Markdown DSL has not been A/B-tested on Haiku 4.5 specifically. If Haiku accuracy drops >3pp on compact-form roadmaps, compressing variants before any Haiku-consumed step would silently degrade quality.
**Prerequisite**: Run a Haiku-specific A/B against `Approach1RuleBased` and `Approach2ASTAware` outputs using ≥20 retrieval prompts on the same Phase 2 slice. Block Haiku path adoption if accuracy drops >3pp below plain Markdown.
**Enforcement in this design**:
- `compression_target_model` defaults to `opus`
- If `--compression-target-model=haiku` is passed **and** the A/B report is missing (`claudedocs/haiku-compression-ab-results.md` not present), the CLI **refuses to apply compression to Haiku-consumed Steps** and logs a clear error: `Haiku compression path is gated until INV-5 A/B completes. See claudedocs/roadmap-pipeline-compression-design.md §8.`
- Since the default `RoadmapConfig.agents` is `[opus:architect, haiku:architect]`, enabling `--compress-variants` with the default agent set will **only compress the opus variant** and leave the haiku variant uncompressed until INV-5 clears. The diff/debate/score/merge Steps then read a mixed pair, and the manifest explicitly records this asymmetry.

---

## 9. Migration Path

Shipped in 4 phases. Each phase is independently revertible.

### Phase 0 — Scaffolding (no behavior change)
- Create `compression/` module skeleton with stubs that raise `NotImplementedError`
- Add `RoadmapConfig` fields with defaults `False`
- Add CLI flags as inert options
- Add `COMPRESS_*_GATE` definitions that always pass
- Acceptance: `superclaude roadmap run spec.md` runs identically to before

### Phase 1 — Approach 1 only, C1 only
- Implement `Approach1RuleBased` (whitespace + decorative + preamble stripping)
- Wire C1 Step behind `--compress-ingest`
- Enforce spec-fidelity firebreak
- Acceptance: on a golden spec, `diff roadmap.md roadmap-uncompressed.md` is empty (within stochastic noise); extract + generate token count drops ~10%

### Phase 2 — Approach 2, C1 + C2
- Implement `Approach2ASTAware` using `markdown-it-py`
- Wire C2 Step behind `--compress-variants`
- Implement claim-sample fidelity gate
- Acceptance: measured variant compression ≥25% on 3 reference roadmaps; no `spec-fidelity` regressions across 5 test pipelines; rollback path exercised in tests

### Phase 3 — C3 + consumer-DAG routing + INV carry-forward
- Implement C3 (emit both raw and compressed)
- Populate `claudedocs/roadmap-consumer-dag.md` (closes INV-3)
- Wire `anthropic.messages.count_tokens` into manifest (closes INV-1 measurement side)
- Block Haiku path without A/B results (blocks INV-5 until A/B runs)
- Acceptance: `superclaude roadmap run spec.md --compress-all` produces raw + compressed artifacts with fidelity gate passing, rollback paths tested, manifest shows both tokenizer measurements

### Phase 4 — Approach 3 (LLM-assisted) — optional, PRD-only
- Only if Phase 3 is stable
- Restricted to PRD compression; never applied to spec or roadmap variants
- Mandatory claim-sample gate with 0.99 floor
- Acceptance: 35%+ PRD compression with no lost high-severity assertions across 3 reference PRDs

---

## 10. Testing Strategy

| Test | Layer | Covers |
|------|-------|--------|
| `test_approach1_idempotent` | unit | Running Approach 1 twice yields byte-identical output |
| `test_approach1_lossless_claims` | unit | Every sentence in input recoverable from output |
| `test_approach2_ast_preserves_tables` | unit | Tables, code fences, nested lists pass through untouched |
| `test_conventions_header_roundtrip` | unit | `decompress(compress(x)) == x` for N sample documents |
| `test_fidelity_gate_rollback` | integration | A deliberately broken strategy triggers rollback without failing the pipeline |
| `test_spec_fidelity_firebreak` | integration | `spec-fidelity` receives original spec even when `--compress-ingest` is on |
| `test_haiku_gate_refusal` | integration | `--compression-target-model=haiku` without A/B file fails fast with clear error |
| `test_c3_both_artifacts_present` | integration | Both `roadmap.md` and `roadmap.cmd.md` exist after `--compress-output` |
| `test_resume_after_compression` | integration | `--resume` works when compression manifests are already present |
| `test_consumer_dag_routing` | integration | `sc:tasklist` reads raw `roadmap.md` by default; compressed form only when opted in |
| `test_tiktoken_vs_native_tolerance` | integration (INV-1) | Manifest records both numbers; delta within ±3pp |

---

## 11. Open Questions

1. **Should C2 compress the `diff_file`/`debate_file`/`score_file` intermediates too?** These are re-generated every run and are the largest secondary artifacts. Not included in initial scope to keep the change surface small; candidate for Phase 5.
2. **Should `extraction.md` be compressed?** `extract` writes it, many downstream steps read it. This would be another high-ROI spot. Deferred to Phase 5 because the extraction format is brittle to regex stripping (it is partially machine-readable).
3. **Caching**: Compressing the same spec twice is wasteful. A content-addressed cache keyed on `(sha256(source), strategy, target_model)` would make compression free on `--resume`. Not in initial scope.
4. **Who owns the conventions header?** Shared across all artifacts in a run, or per-artifact? Leaning toward **run-scoped** (one header in `.compression/conventions.md`) so C1, C2, C3 can share abbreviations and amortize the preamble over more read operations. Needs validation on a real run.
5. **Does C2 asymmetry (opus compressed, haiku not) bias `diff`?** The diff agent sees one compressed variant and one raw variant — the structural diff signal will be contaminated by format differences. Mitigation: when `--compress-variants` would produce an asymmetric pair, **either compress both or neither**. Under current INV-5 gate this means C2 is effectively disabled on the default agent set until the Haiku A/B completes.

Question #5 is the most significant design pressure point — it may mean that **C2 is entirely blocked on INV-5** rather than just the Haiku side. Flagged for the Phase 2 design review.

---

## 12. Summary

| Point | Flag | Default | Strategy | Savings target | Blocked by |
|-------|------|---------|----------|----------------|------------|
| C1 ingest | `--compress-ingest` | OFF | Per-doc-type (primer §5) | 10-45% depending on doc | INV-1 (measurement) |
| C2 variants | `--compress-variants` | OFF | Approach 2 | 25-33% | INV-5 (Haiku A/B) + Q5 (asymmetry) |
| C3 output | `--compress-output` | OFF | Approach 2 | 25-33% | INV-3 (consumer DAG) |

All three are **additive**, **opt-in**, **rollback-safe**, and **carry every UNADDRESSED invariant as a hard prerequisite**. None of them change the existing 12-step state machine; they attach as pre-steps with their own deterministic gates and fall back to the uncompressed path on any fidelity failure.

The canonical `roadmap.md`, `spec.md`, and variant files are **never deleted or replaced in place**. Every compressed form is a sibling with a manifest trail. This guarantees `--resume`, the state hash machinery, and all human/CI consumers continue to work unchanged against the authoritative sources, while opt-in consumers get the token savings when they ask for them.

**Next step**: Phase 0 scaffolding PR. Does not change any behavior; establishes the module, flags, and no-op gates so Phase 1 (Approach 1 + C1) can land as a small, reviewable change.
