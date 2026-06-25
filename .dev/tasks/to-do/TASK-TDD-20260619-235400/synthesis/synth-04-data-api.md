# synth-04 — Data Models & API Specifications (TDD §7 + §8)

> **Synthesis deliverable** for the ReflectHardening (RH) Heavyweight TDD.
> Source of truth: research files `02`, `03`, `04`, `05`, `09` (all `[CODE-VERIFIED]` against the worktree this turn) + direct re-read of `src/superclaude/cli/swarm/models.py` (`LensEntry` L637-728).
> **THE load-bearing artifact** is §8.3 — the OI-1 swarm→reflect field-correspondence table. It is called out as the BLOCKING gate (TDD §22 Q1) because it sizes the to-be-built `ensemble.py` mapping layer.
> Scope note: `ensemble.py` does **not yet exist** in the tree (`find src -name ensemble.py` → no hit, per research 03/05). The swarm and reflect contracts below are existing/stable; the mapping layer that joins them is the RH design obligation.

---

## 7. Data Models

The RH feature joins two existing, frozen contracts (swarm-side producer, reflect-side consumer) through a new in-process mapping layer. The entities below are the on-wire and in-memory records that layer reads and writes. Four are swarm-side (`WorkerResult`, `ResultContract`, `LensEntry`, `DoneSentinel`); one is reflect-side (`ReflectResult` + the parsed `return-contract.yaml` verdict fields).

**M / N convention (used throughout §7–§8):**

- **N** = `workers_requested` = requested reviewer slot count. `dispatch_wave1` returns a `list[WorkerResult]` of length **N** (one per slot, including failed/synthesized slots).
- **M** = `workers_succeeded` = `sum(1 for w in worker_results if w.status == "success")` (reduce.py L648; predicate identical to dispatch.py L496). Diversity and `reviewer_count` are measured over **M**, never N (research 03 §5, FR-RH2.4/2.9).

### 7.1 Data Entities

#### `WorkerResult` (DM-013)

Swarm per-reviewer outcome record. `@dataclass` at `models.py:1026`; field block L1117-1128; `status` enum guarded in `__post_init__` (L1130-1136). **Exactly 12 fields** (research 03 §3). One `WorkerResult` per requested slot, sorted by `index` 0..N-1. The transport populates `http_code`/`attempts`/`elapsed_ms`; the dispatch layer fills the path fields after materializing the body to disk (research 04 §1).

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| `index` | `int` | Yes | Worker slot index 0..N-1; drives `{index:02d}` filename substitution and `mechanical_merge` ordering. | Default `0`; positional correspondence with requested slots. |
| `path` | `str` | Yes | Canonical output path (post-normalize, or = `raw_path` in raw mode). | Default `""`. |
| `raw_path` | `str` | No | Per-worker raw output `*.raw.<ext>`; retained when `retain_raw=True`. | Default `""`. |
| `meta_path` | `str` | No | Per-worker meta sidecar `*.meta.json` (transport/model/attempts/http/status). | Default `""`. |
| `final_path` | `str` | Yes | **Post-normalization file consumed by Wave-3 reduce/merge AND (per RH design) by reflect.** Load-bearing per-reviewer pointer; `mechanical_merge` reads this, never `merged.md`/`raw_path`. | Default `""`; diverges from `path` only when normalization rewrites under a different filename. |
| `model_id` | `str` | Yes | Transport model id (e.g. `gpt-5-codex`, `claude-haiku-4.5`). | Default `""`; basis for diversity computation. |
| `model_label` | `str` | Yes | Human label printed in merge provenance header `## From {model_label}`. | Default `""`. |
| `bytes` | `int` | No | Output byte count. | Default `0`. |
| `status` | `WorkerStatus` enum | Yes | One of `success` / `timeout` / `parse_error` / `proxy_error`. Drives the M-count. | `__post_init__` raises `ValueError` on out-of-enum (L1130-1136). `success` only counts toward M. |
| `http_code` | `Optional[int]` | No | Transport HTTP status. | Default `None` (stub transport / no HTTP / timeout). |
| `attempts` | `int` | No | Attempt count. | Default `1`; `2` only when a 5xx was retried once (FR-017). |
| `elapsed_ms` | `int` | No | Per-worker wall-clock (ms), cumulative across attempts (backoff sleep excluded). | Default `0`; printed in provenance header. |

> **Note:** `WorkerStatus = Literal["success","timeout","parse_error","proxy_error"]` (`models.py:69`). This is a different enum from the job-level `ResultStatus` (`success`/`partial`/`failed`, `models.py:68`) used by `ResultContract`. **M = count of `WorkerResult`s with `status == "success"`** (the salvage promotion `parse_error → success` is a Wave-2/normalize concern applied upstream, not in this dataclass).
> The raw response body is stashed on the non-dataclass attribute `WorkerResult.body` so the dispatcher can materialize `raw_path` without a second `send` (research 04 §1).

#### `ResultContract` (DM-012) — the swarm `return-contract.yaml`

Swarm Wave-3 terminal contract. `@dataclass(frozen=True)` at `models.py:876`; fields L997-1015; `status` enum guarded in `__post_init__` (L1017-1023). **19 top-level keys** (after the four `target.*` sub-fields collapse into one `ContractTarget`). The on-disk `<output_dir>/return-contract.yaml` IS `to_dict(ResultContract)` dumped via `yaml.safe_dump(..., sort_keys=False)` (`emit_contract`, reduce.py L369-394), so YAML key order == declaration order below (research 05 §1.5, §3).

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| `contract_version` | `str` | Yes | §5 schema version; mirrors `Manifest.contract_version`. | Default `"1.0"`. |
| `status` | `ResultStatus` enum | Yes | IMM-5 job verdict stamped at reduce. | `success` / `partial` / `failed`; `__post_init__` rejects out-of-enum (L1017-1023). |
| `job_id` | `str` | Yes | UUID; mirrors `Manifest.job_id` / `SwarmState.job_id`. | Default `""`. |
| `started` | `str` | No | ISO 8601 start timestamp. | Default `""`. |
| `finished` | `str` | No | ISO 8601 finish timestamp. | Default `""`. |
| `elapsed_ms` | `int` | No | `finished − started` delta. | Default `0`. |
| `caller` | `CallerInfo` (DM-019) | Yes | Identity block copied verbatim from `JobSpec`. | Stub default. |
| `lens` | `str` | No | Lens name; `""` when JSON-Schema-driven (no registered lens). | Default `""`. |
| `lens_source` | `str` | No | Provenance of the lens. | `{"", "registry", "custom"}` (schema-validated at M2). |
| `target` | `ContractTarget` (nested) | Yes | Post-exec target snapshot. | `path:str`, `checksum:str` (sha256 → 12 hex), `truncated:bool=False`, `truncation_line_cap:int=4000` (L842-873). |
| `workers_requested` | `int` | Yes | **N**. | Default `0`. INV-005: `succeeded + failed == requested` (enforced at emitter, not dataclass). |
| `workers_succeeded` | `int` | Yes | **M** (success count). | Default `0`. |
| `workers_failed` | `int` | Yes | N − M (non-success). | Default `0`. Counted against `len(worker_results)` in reduce, not N (research 05 §1.1). |
| `output_files` | `list[WorkerResult]` (DM-013) | Yes | **Per-reviewer artifact list** (each carries `final_path`). | Default `[]`; full per-worker list carried verbatim (reduce.py L713). |
| `amalgamation_mode` | `AmalgamationMode` enum | Yes | Reduce mode that ran. | `raw` / `normalize` / `normalize+merge`; default `"normalize+merge"`. |
| `merged_path` | `Optional[str]` | No | Path to `merged.md`. | Default `None`; null unless mode==`normalize+merge` AND M ≥ floor(2) AND `output_dir` set. |
| `caller_metadata` | `CallerMetadata` (DM-020) | Yes | `suspect:bool` + `tier:str` (OQ-009 lens/caller precedence). | Stub default. |
| `recommended_next_command` | `str` | No | **Rendered** next-command string (contrast JobSpec's unrendered `*_template`). | Default `""`. |
| `artifacts` | `Artifacts` (DM-018) | Yes | Path bundle: `manifest_path`, `state_path`, `event_log_jsonl`, `event_log_md`, `done_sentinel` (all `str`). | Stub default; `done_sentinel` here is the path string, not a `DoneSentinel`. |

> **CRITICAL (OI-1 root cause):** None of the reflect verdict-driver fields (`tier_reached`, `merge_method`, `t2_model_class_diversity`, `t2_vendor_diversity`, `adversarial_convergence_score`, `deviation_count_by_class`, the seven load-bearing booleans, etc.) appear on this dataclass. The two `return-contract.yaml` files (swarm DM-012 vs reflect) share **only** the key name `status`, and even there the semantics differ. See §8.3.

#### `DoneSentinel` (DM-017)

Swarm completion sentinel. `@dataclass(frozen=True)` at `models.py:1423`; fields L1479-1481; `terminal_status` enum guarded in `__post_init__` (L1483-1489). Written by `emit_done_sentinel` (reduce.py L402-459) as `json.dumps(to_dict(sentinel), sort_keys=True, indent=2)` to `<contract_path>.parent/done.json` (co-located with the contract).

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| `atomic_write` | `bool` | Yes | Always-on marker; write uses tmp + fsync + `os.replace`. | Default `True`. |
| `terminal_status` | `ResultStatus` enum | Yes | IMM-5 verdict. | `success` / `partial` / `failed`; `__post_init__` enforces enum (L1483-1489). The kill path (`commands._emit_killed_done_sentinel`) bypasses the dataclass because `"killed"` is intentionally NOT in `ResultStatus`. |
| `contract_path` | `str` | Yes | Absolute path to `return-contract.yaml` (lets a poller locate the rich record). | Default `""`. |

#### `LensEntry` (DM-010)

Swarm lens registry record. `@dataclass` at `models.py:637`; fields L707-720; `stability` enum guarded in `__post_init__` (L722-728). **14 fields** (re-read directly this turn — research 09 only cited the two recipe/strategy fields). The RH `reflect-review` lens ships one of these; the COMP-023 validator's assertions 2 & 6 require `recipe_name` ∈ `REGISTRY` and `normalizer_strategy` ∈ `STRATEGIES` (research 09 §3).

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| `name` | `str` | Yes | Lens identifier; unique across `LENSES`. | Default `""`. |
| `description` | `str` | No | Human-facing registry metadata (not used at dispatch). | Default `""`. |
| `system_prompt_fragment` | `str` | Yes | System-prompt injection; §11.5 substring asserted by validator. | Default `""`. |
| `user_template` | `str` | Yes | Per-worker user prompt template. | Default `""`. |
| `output_template_path` | `str` | No | Path to output template (expanded into `NormalizationSpec` at preflight). | Default `""`. |
| `recipe_name` | `str` | Yes | M4 recipe binding. | Default `""`; validator assertion 2 requires ∈ `recipes.REGISTRY`. |
| `normalizer_strategy` | `str` | Yes | Names the prompt's expected output shape (FR-LENSREG.NS / T02.21). | Default `""`; validator assertion 6 requires resolution in `recipes.STRATEGIES` (or REGISTRY). |
| `default_workers` | `int` | No | Lens-driven default N (FR-020). | Default `3`; some lenses override to 4. Compatible with `StatusPolicy.floor=2`. |
| `default_target_line_cap` | `int` | No | Default truncation cap. | Default `4000` (mirrors `Truncation`). |
| `suspect` | `bool` | No | Triggers the §FR-020 / NFR-012 review discipline; propagates into `CallerMetadata`. | Default `False`; `bare_review` is the canonical `suspect=True` lens. |
| `tier` | `str` | No | Caller tier label (OQ-009 precedence). | Default `""`. |
| `recommended_next_command_template` | `str` | No | Unrendered next-command template; `suspect` ↔ `{suspect_files}` placeholder coupling asserted by validator. | Default `""`. |
| `acceptance_notes` | `str` | No | Free-text acceptance criteria. | Default `""`. |
| `stability` | `Stability` enum | No | Registry stability flag. | `stable` / `experimental`; default `"stable"`; `__post_init__` raises `ValueError` on out-of-enum (L722-728). |

#### `ReflectResult` + parsed verdict fields (reflect-side consumer)

Reflect-wrapper result. `@dataclass` at `reflect/models.py:94-121`. Built by `_make_result` (`reflect/contract.py:104-127`) reading the parsed reflect `return-contract.yaml` defensively (`c = contract or {}`). This is the **left column** of the OI-1 table (§8.3) — the fields `derive_verdict` actually reads. Authoritative per research 02 (D1).

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| `verdict` | `Verdict` enum | Yes | Derived verdict. | `PASS`(0) / `HALTED`(10) / `DEGRADED`(11) / `BLOCKED`(2); `is_promotable` ⇔ `PASS`. |
| `status` | `str \| None` | Yes | Raw audit completion status from contract. | `.get`, may be `None`. PASS requires `== "success"`. |
| `tier_reached` | `int \| None` | Yes | Highest reflection tier reached. | Coerced to `None` if not `int` (contract.py L116-117). PASS requires `== expected_tier`. |
| `reason` | `str` | Yes | Reason slug (e.g. `"single-reviewer-fallback"`, `"tier-mismatch"`). | Branch arg. |
| `report_path` | `str \| None` | No | Path to the reflect report. | From `contract["report_path"]`; may be `None`. |
| `contract_path` | `str \| None` | No | Pinned contract path the runner parsed. | Hard `None` in `_make_result`; runner fills (L122). |
| `deviations` | `dict[str,int]` | Yes | 4-key int dict (authorized/necessary/drift/regression). | From `_extract_deviations`; non-coercible → `0`. |
| `child_exit_code` | `int` | Yes | Child `claude` process rc. | Passthrough of `child_rc`. |
| `write_status` | `str` | No | Write-back status. | `""`; runner finalizes. |
| `remediation_task_path` | `str \| None` | No | FR-8: wrapper only READS reflect's emitted path. | Default `None`. |
| `fix_iterations` | `int` | No | Auto-fix loop bookkeeping. | Default `0`; set by runner. |
| `fix_converged` | `bool` | No | Auto-fix convergence flag. | Default `False`; set by runner. |

> `ReflectResult.outcome` (L118-121) returns `"success"` IFF `verdict is Verdict.PASS`, else `"failed"`. The full set of verdict-DRIVER fields parsed from the reflect contract (beyond what lands on `ReflectResult`) is the left column of §8.3.

---

## 8. API Specifications

This component exposes no HTTP surface. Its "API" is (a) the `reflect run` CLI flag surface, (b) the in-process swarm library functions `ensemble.py` calls, and (c) the OI-1 field-correspondence contract between the two `return-contract.yaml` schemas. Section 8.3 is the BLOCKING deliverable.

### 8.1 CLI Surface — `superclaude reflect run`

The FR-RH2 mutation surface is a three-file chain per resolved field: `ReflectConfig` dataclass field (`reflect/models.py:57-91`), `resolve_config` param + resolution + constructor kwarg (`reflect/config.py:123-240`), and the `@click.option` + `run()` signature param + `resolve_config(...)` kwarg (`reflect/commands.py:76-190`). `ReflectConfig` is defined in `models.py` (NOT `config.py`) and imported via `from .models import ReflectConfig` (`config.py:24`). New fields append at the dataclass tail after `max_fix_iterations` (research 09 §1).

| Flag | Type / Choices | Default | Status | Resolution / Semantics |
|------|----------------|---------|--------|------------------------|
| `--transport` | `Choice([openai_compat, stub])`, case-insensitive | `openai_compat` | **NET-NEW** (zero occurrences in `reflect/` today) | Mirrors the `--depth` `click.Choice` idiom. Validate in `resolve_config` against `{"openai_compat","stub"}` using the `model` non-empty `raise ValueError` pattern (`config.py:170-172`); a bad value → `ValueError` → command-body `blocked`/exit 2 (`commands.py:191-227`). `stub` selects the offline deterministic `StubTransport`; `openai_compat` selects the live `:4000/cli` proxy driver (research 04). |
| `--reviewers` | `int` | `3` | **NET-NEW** | Clamp to `[2,4]`; `1` is a sentinel selecting **negative-witness mode**. Clamp + sentinel branch live in `resolve_config` (next to the `config.py:190` depth floor), NOT a Click callback (house convention: all resolution in `config.py`). **The `1` sentinel MUST be branched BEFORE the `max(2, min(4, n))` clamp** or the clamp rewrites it to `2` and erases negative-witness mode. Maps to swarm `workers_requested` (N); diversity/`reviewer_count` then measured over M succeeded. |
| `--depth` | `Choice([standard, deep])`, case-insensitive | `standard` | **ALREADY EXISTS** — do NOT re-add | `commands.py:101-106` → `resolve_config` floor `"standard" if depth=="quick" else depth` (`config.py:190`) → `ReflectConfig.depth` (field #5, `models.py:71`). Drives `expected_tier = 2 if config.depth in {"standard","deep"} else 1` in the runner (`runner.py:403`); both depths currently collapse to tier 2. If `deep` must map to a different expected tier, `runner.py:403` is the single mutation point. |

> **Note:** There is deliberately **no `--model` flag**; the model is `os.environ.get("ANTHROPIC_MODEL","").strip() or _DEFAULT_MODEL` where `_DEFAULT_MODEL="claude-opus-4-8"` (`commands.py:31, 172`). `ReflectConfig.contract_path` is a property → `self.output_dir / "return-contract.yaml"` (`models.py:88-91`).

> **Open question (research 09 Gap):** `--reviewers` out-of-range (0, 5) — silent clamp vs hard-fail `ValueError`→exit-2? "clamp [2,4]" implies silent clamp; recommend explicit `if reviewers == 1: <negative-witness> else: reviewers = max(2, min(4, reviewers))`. The TDD must settle this (see §8.3 notes).

### 8.2 In-Process Library Interface (swarm seam `ensemble.py` consumes)

These are the existing, stable swarm functions the new `ensemble.py` calls in-process. Signatures verbatim from the worktree (research 03, 04, 05).

#### `dispatch_wave1(...)` — Wave-1 fan-out (`swarm/dispatch.py:334-343`)

```python
def dispatch_wave1(
    preflight_result: PreflightResult,
    transport: Optional[Transport] = None,
    *,
    transport_for_slot: Optional[Callable[[int], Transport]] = None,
    prompt: str = "",
    parallel_executor: Optional[ParallelExecutor] = None,
    worker_spec: Optional[WorkerSpec] = None,
    logger: Optional[Logger] = None,
) -> list[WorkerResult]:
```

- All params after `transport` are **keyword-only** (bare `*` at L337). Returns a `list[WorkerResult]` of length **N** (= `preflight_result.manifest.preflight.workers_requested`), one per slot sorted by `index`, with a synthesized `proxy_error` backstop guaranteeing one result per slot (L484-490).
- `transport_for_slot` (the shape `ensemble.py` uses for heterogeneous per-model fan-out) **takes precedence** over `transport` when supplied (L453-457).
- Early exits: both transport sources `None` → `return []` (L409-410); `workers_requested <= 0` → `return []` (L412-414). Sets `executor.quiet = True` (FR-1 single-writer, L425).

#### `_resolve_run_transport_factory(...)` — per-slot transport factory (`swarm/commands.py:612-707`)

```python
def _resolve_run_transport_factory(
    transport_kind,
    *,
    models=None,
    env=None,
    workers_requested=None,
) -> Callable[[int], Any]:
```

- Returns a `(slot_index) -> Transport` factory. `openai_compat` branch: `config = read_env(env)` eagerly at build time (L680), `pool = [m for m in config.models if m]` (L681), then the **D2 pool guard** `if workers_requested is not None and len(pool) < workers_requested: raise ModelPoolTooSmallError(len(pool), workers_requested)` (L687-688). Binding rule: slot `i` → `pool[i % len(pool)]` with a per-model client cache → each slot gets a **distinct** `T2Model0N` model.
- `stub` branch: one shared `StubTransport` for every slot (`lambda _slot: shared`, L670-673).
- `ModelPoolTooSmallError` (`commands.py:589-609`, subclass of `RuntimeError`) raises eagerly at factory-build, catching the env-pool-vs-workers gap that INV-005 (spec placeholders) cannot see. Env pool read by `read_env` from `os.environ`: `T2ProxyUrl`, `T2ProxyKey`, dense `T2Model01..T2Model09` (`config.py:48-63`); never from an `.aienv` file in-code.

#### `reduce_wave3(...)` — Wave-3 reduce + contract emission (`swarm/reduce.py:555`)

```python
def reduce_wave3(
    worker_results: list[WorkerResult],
    *,
    output_dir: Optional[Path] = None,
    mode: AmalgamationMode = "normalize+merge",
    policy: Optional[StatusPolicy] = None,
    workers_requested: Optional[int] = None,
    emit_to_disk: Optional[bool] = None,
    merge_callable: Optional[Callable[..., str]] = None,
    # ... (caller/lens/target/timestamp metadata threaded onto the emitted ResultContract)
) -> ResultContract:
```

- Computes `workers_succeeded` (M, L648), `workers_failed` (L649), `effective_n` (N = `workers_requested` if supplied else `len(worker_results)`, L650-653), then `status = determine_status(...)` (IMM-5 truth table, L158-216; defaults `floor=2, success_first=True, partial_threshold=2`).
- Dispatches by `AmalgamationMode` via `select_mode` (L276): `raw`/`normalize` → `merged_body=None`; `normalize+merge` → calls `mechanical_merge` (scoring-free, 8 LOC, reads each worker's `final_path`, orders by `index`, prepends `## From {model_label} ({elapsed_ms}ms)`) when `M >= floor`, else `None`.
- Emits `<output_dir>/return-contract.yaml` (= `to_dict(ResultContract)`, `sort_keys=False`) and co-located `done.json` only when `should_emit and output_dir is not None`. `merged_path` set only when `merged_body is not None AND output_dir is not None AND should_emit` (L686-689).

> **Signature note:** the `reduce_wave3` parameter block beyond the load-bearing args (caller/lens/target/timestamp metadata threaded onto the contract at L699-719) was summarized rather than re-transcribed field-by-field; the load-bearing args (`worker_results`, `output_dir`, `mode`, `policy`, `workers_requested`, `emit_to_disk`, `merge_callable`) and return type `ResultContract` are code-verified (research 05 §1).

### 8.3 THE OI-1 Field-Correspondence Table — swarm DM-012 → reflect verdict (BLOCKING / TDD §22 Q1)

> **CRITICAL — this is THE load-bearing deliverable.** It is the BLOCKING gate (TDD §22 Q1) because it sizes the `ensemble.py` mapping layer. The two `return-contract.yaml` files (swarm DM-012 producer vs reflect consumer) are **disjoint schemas sharing one filename**: they share **only** the key name `status`, and even there the semantics differ (swarm = IMM-5 worker verdict `success`/`partial`/`failed`; reflect = a `status == "success"`-vs-tier check). **Every other reflect verdict-driver field has NO swarm DM-012 source** and must be synthesized/defaulted in `ensemble.py`. The number of `synthesize in ensemble.py` rows below is the size of the mapping layer the RH feature must build.

**Left column** = every field `derive_verdict` reads (research 02, AUTHORITATIVE/Complete — D1). **Right column** = swarm DM-012 source (research 05 producer side — D2). `ensemble.py` does not exist yet; "synthesize in ensemble.py" is the design obligation.

| Reflect-consumed field (derive_verdict reads) | Type | Swarm-emitted source (DM-012 / WorkerResult) | Mapping / Transform | Notes |
|---|---|---|---|---|
| `status` | `str` | `ResultContract.status` (name-collision only) | **RE-MAP, not passthrough.** Swarm `status` ∈ {success,partial,failed} (IMM-5 worker verdict); reflect `status` must be the reflect audit completion status (`success` for the PASS gate, contract.py L235). `ensemble.py` must NOT forward the swarm worker verdict as the reflect `status`. | The ONLY shared key name; semantics diverge. |
| `tier_reached` | `int` (1 or 2) | **Absent** in DM-012 | **Synthesize in ensemble.py** from swarm execution facts (which/how many T2 reviewers ran; `expected_tier` is 2 for standard/deep per `runner.py:403`). | Consumed in degraded (T1 trigger L263; null-convergence L284) + PASS (tier match L235). |
| `merge_method` | `str` | **Absent.** Closest: `amalgamation_mode` + `workers_succeeded` (M) | **Synthesize/derive in ensemble.py:** `merged_path is None` (mode≠`normalize+merge` OR M<2) ⇔ no merge → reflect's `"single-reviewer-fallback"` value. | DEGRADED trigger 10 (`== "single-reviewer-fallback"` → exit 11, contract.py L280-281). |
| `reviewer_count` | `int` | `workers_succeeded` (M) | **MAP from M** = `ResultContract.workers_succeeded` (rename + re-derive over succeeded subset). NOT `workers_requested` (N), NOT `len(output_files)`. | FR-RH2.4/2.9: count over M succeeded only (research 03 §5). |
| `t2_model_class_diversity` | `str` (e.g. `"full"`) | **Absent.** Closest: distinct `output_files[].model_id`/`model_label` over the M succeeded | **Compute in ensemble.py** from the distinct model classes of the M succeeded `WorkerResult`s. | DEGRADED trigger 7 (set AND `!= "full"` → exit 11, contract.py L267-269). T1-null guard: `None` → skipped. |
| `t2_vendor_diversity` | `str` (e.g. `"single"`) | **Absent.** Closest: distinct vendor of `output_files[].model_id` over M succeeded | **Compute in ensemble.py** from the distinct vendors of the M succeeded models. | DEGRADED trigger 8 (`== "single"` AND NOT `allow_single_vendor` → exit 11, contract.py L272-273). Suppressed by `--allow-single-vendor`. |
| `degraded_components` | `list[str]` | **Absent** in DM-012 | **Synthesize in ensemble.py** (telemetry of chain-critical capability loss: serena/auggie/env-aliases/evidence-validator). Swarm transport/pool failures may seed tokens. | BLOCKED list-shape guard (contract.py L184-193); DEGRADED triggers 1-5 (exact membership of `_DEGRADED_COMPONENTS_HALT_SET`, L259-260). Non-list → BLOCKED. |
| `adversarial_unavailable` | `bool` | **Absent** | **Synthesize in ensemble.py** (whether the adversarial merge stage could run). | F2 load-bearing bool; DEGRADED trigger 9 (`is True`, L276-277). Present non-bool → BLOCKED. |
| `adversarial_convergence_score` | numeric \| `None` | **Absent** (a `/sc:adversarial` artifact, not swarm) | **From the adversarial stage, NOT swarm.** `ensemble.py` defaults `None` until adversarial runs. | DEGRADED trigger 11 (only when `tier_reached == 2` AND `is None` → `"null-convergence"`, L284-285). |
| `verification_ran` | `bool` | **Absent** | **Synthesize in ensemble.py** (whether reflect's verification executed). | F2 bool; DEGRADED trigger 12 (`is False` AND skip-reason not exempt, L288-291). |
| `verification_skip_reason` | `str` | **Absent** | **Synthesize in ensemble.py.** | Read inside trigger 12; exempt set = `{read-only-project, tool-unavailable, --no-verify}` (L289). |
| `citations_dropped` | `int` | **Absent** | **Synthesize in ensemble.py** (count, sample-count NOT extrapolated). | DEGRADED trigger 13 (`int(...) > 0`, L294-298). Absent → `0`. |
| `input_drift_detected` | `bool` | **Absent** | **Synthesize in ensemble.py** (spec/input drifted from audited state). | F2 bool; DEGRADED trigger 14 (`is True`, L301-302). |
| `regression_present` | `bool` | **Absent** | **Synthesize in ensemble.py** (reflect detected a regression). | F2 bool; HALTED (`is True` → `"regression"`, L315-316) + `classify_fix` human-required. |
| `unauthorized_deviation_present` | `bool` | **Absent** | **Synthesize in ensemble.py.** | F2 bool; HALTED (`is True`, L317-318) + `classify_fix`. |
| `needs_human_decision` | `bool` | **Absent** | **Synthesize in ensemble.py** (grounding-gaps non-empty IFF this is `True`). | F2 bool; HALTED (L319-320) + `classify_fix` human-required carve-out. |
| `user_decision_required` | `bool` | **Absent** | **Synthesize in ensemble.py.** | F2 bool; HALTED (L321-322) + `classify_fix`. |
| `deviation_count_by_class` | `dict[str,int]` | **Absent** (reflect/adversarial-side only) | **Synthesize in ensemble.py** (4-key: authorized/necessary/drift/regression). | HALTED (`regression>0`→`"regression"`, `drift>0`→`"drift"`, L323-327); also `classify_fix`. Non-dict → `{}`/`0` coercion. |
| `contract_version` | `str` | `ResultContract.contract_version` exists (`"1.0"`) but is the SWARM schema version | **Do NOT forward.** `ensemble.py` must emit the **reflect** contract version (major `1`). Swarm `contract_version` describes DM-012, not the reflect contract. | BLOCKED: absent/blank → `"contract-version-missing"`; major ≠ `"1"` → `"unknown-major-version"` (contract.py L166-181). |
| `status` (PASS conjunct) | `str` | (see `status` row) | PASS requires `status == "success"` AND `tier_reached == expected_tier` (both synthesized). | Only exit-0 path. Success-but-tier-mismatch → HALTED `"tier-mismatch"`. |
| `report_path` | `str \| None` | **Absent** | **Synthesize in ensemble.py** (path to the reflect report the wrapper surfaces). | Read into `ReflectResult.report_path` (contract.py L119); not a verdict driver but contract-emitted. |
| `remediation_task_path` | `str \| None` | **Absent** | **Synthesize in ensemble.py** (FR-8: wrapper only READS reflect's emitted path; default `None`). | Read into `ReflectResult.remediation_task_path` (contract.py L126). |
| *(call-arg)* `child_rc` | `int` | N/A — child `claude` process exit code | Supplied by the runner, not the contract. `124` → BLOCKED `"timeout"`; any other non-zero → BLOCKED `"child-crash"` (F0 veto). | Gates the BLOCKED stage AHEAD of contract parse (contract.py L148-159). |

**Sizing conclusion (the BLOCKING answer to §22 Q1):** of ~22 reflect verdict-driver fields, exactly **one** (`status`) has a swarm DM-012 key of the same name (and it needs re-mapping, not passthrough); **`reviewer_count` maps from `workers_succeeded` (M)**; `merge_method`/`t2_model_class_diversity`/`t2_vendor_diversity` are **derived/computed** from swarm raw facts (`amalgamation_mode`, `merged_path`, distinct `output_files[].model_id`); and **every remaining field is synthesized or defaulted in `ensemble.py`** with no swarm source. The swarm DM-012 contract supplies only the *raw execution facts* (`workers_succeeded`, `amalgamation_mode`, `merged_path`, `output_files[].model_id/model_label/final_path`); `ensemble.py` is the entire vocabulary-translation layer. This non-interchangeability is precisely why the OI-1 table is load-bearing.

### 8.4 Path-Confinement Contracts (swarm ↔ reflect)

Two design rules the RH feature must implement (today neither is wired — `grep -rn "t2-swarm\|final_path\|output_files" src/superclaude/cli/reflect/` returns zero hits; research 05 Gaps 1-2):

**Contract A — reflect consumes per-reviewer `output_files[].final_path`, NEVER `merged.md`.**
The swarm emits both: the per-reviewer `WorkerResult` list (each with `final_path`) AND, in `normalize+merge` mode, a single `merged.md` (path on `merged_path`). `merged.md` is the scoring-free mechanical concat (merge.py, 8 LOC, no judging). Reflect's independent adversarial ensemble requires the **separate per-reviewer bodies** — feeding it `merged.md` would collapse the per-reviewer diversity the ensemble depends on. So reflect/`ensemble.py` reads each `final_path` individually.

**Contract B — `reflect.derive_verdict` parses `<reflect output_dir>/return-contract.yaml` ONLY; it MUST NOT parse the swarm `t2-swarm/` subdir contract directly.**
`reflect/contract.py::parse_contract` (L65) takes a single pinned `path: Path` and does not walk into any `t2-swarm/` subdir (`_make_result` L120 comment: "runner fills the pinned path it parsed"). Because the two schemas are disjoint (§8.3), the swarm DM-012 `t2-swarm/return-contract.yaml` is NOT directly parseable as if it were the reflect contract — it is consumed only via the `ensemble.py` mapping layer, never fed raw into `derive_verdict`. The reflect side reads exactly `<output_dir>/return-contract.yaml`; the swarm side confines its writes to `<swarm output_dir>/return-contract.yaml` (`emit_contract`, NFR-013). `ensemble.py` reads the `t2-swarm/` subdir contract, maps it, and writes the reflect contract the runner pins.

> **M==0 interaction (research 02 takeaway 2):** if the mapping produces a missing/blank `contract_version`, a non-list `degraded_components`, or any present-but-non-bool load-bearing boolean, `derive_verdict` returns `BLOCKED` (exit 2) at stage 1 — BEFORE any degrade/halt/pass evaluation. `ensemble.py` must therefore emit a well-typed reflect contract (proper bools, list `degraded_components`, major-1 `contract_version`) or the zero-trustworthy-signal path routes to BLOCKED, never silently leaks to PASS.

---

## Cross-references

- §7 entities are the records §8.2 functions return and §8.3 maps between.
- §8.3 left column ⇐ research 02 (reflect consumer, AUTHORITATIVE); right column ⇐ research 05 (swarm producer) + research 03 (`WorkerResult`).
- §8.1 CLI surface ⇐ research 09; transport/pool semantics ⇐ research 04.
- **Outstanding for the TDD:** (1) `--reviewers` clamp-vs-reject semantics for out-of-range (research 09 Gap); (2) whether `expected_tier` is promoted to a `ReflectConfig` field or kept in `runner.py:403`; (3) Path A (reuse `bare-review-v1`) vs Path B (new `reflect-review-v1` recipe) for the lens binding (research 09 §3).

---

*Status: Complete*
