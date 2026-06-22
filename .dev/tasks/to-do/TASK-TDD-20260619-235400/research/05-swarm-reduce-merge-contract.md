# 05 — Swarm Reduce + Merge-Boundary + Contract-Emission (Swarm-side of OI-1)

- **Topic:** Swarm reduce wave3, mechanical-concat merge boundary, `ResultContract` / `return-contract.yaml` (DM-012) emission — the SWARM half of the OI-1 field-correspondence table.
- **Type:** Code Tracer research
- **Scope:** `src/superclaude/cli/swarm/reduce.py` (`reduce_wave3`), `src/superclaude/cli/swarm/merge.py` (concat boundary), `src/superclaude/cli/swarm/models.py` (`ResultContract`), plus path-confinement contracts vs reflect.
- **Status:** Complete
- **Date:** 2026-06-19

> Source of truth = code read this turn. Line numbers re-verified against the worktree files.

---

## 1. `reduce_wave3` — status computation, merge trigger, contract emission

File: `src/superclaude/cli/swarm/reduce.py`. `reduce_wave3` is the single Wave-3 public entrypoint (def at **L555**, docstring "Compute status, trigger merge, emit the final ResultContract" at **L578**). `[CODE-VERIFIED]`

### 1.1 How M (success count), N, and the fail count are computed

Inside `reduce_wave3`, Step 1 (L647–658):

```python
workers_succeeded = sum(1 for w in worker_results if w.status == "success")   # L648  (= M)
workers_failed    = sum(1 for w in worker_results if w.status != "success")   # L649
effective_n = int(workers_requested) if workers_requested is not None else len(worker_results)  # L650-653 (= N)
status = determine_status(workers_succeeded=workers_succeeded, workers_requested=effective_n, policy=effective_policy)  # L654
```

- **M = `workers_succeeded`** = count of `WorkerResult` entries whose `.status == "success"` (post-Wave-2 salvage promotion; §7.4 may flip `parse_error → success` upstream, not here). `[CODE-VERIFIED]`
- **N = `effective_n`** = the caller-supplied `workers_requested` if provided, else `len(worker_results)`. Real M5 wiring passes the preflight-recorded N so retried slots count against the original N. `[CODE-VERIFIED]`
- **`workers_failed`** = `len(worker_results) - M` (every non-`success` status). Note: this counts against `len(worker_results)`, NOT against `effective_n`; if `effective_n > len(worker_results)` the INV-005 identity `succeeded + failed == requested` does not mechanically hold inside this function (the docstring assigns INV-005 enforcement to the emitter, not the dataclass — models.py L982-986). `[CODE-VERIFIED]`

### 1.2 IMM-5 status truth table — `determine_status` (L158–216)

| Condition (M=succeeded, N=requested) | Result | Code line |
|---|---|---|
| `success_first AND M == N == 2` | `success` (tie-break, evaluated FIRST) | L205-206 |
| `M >= N AND N > 0` | `success` | L208-209 |
| `M >= max(floor, partial_threshold) AND M < N` | `partial` | L213-214 |
| otherwise (M < floor) | `failed` | L216 |

Edge cases (docstring L182-191): `N == 0 → failed`; `M > N → success`; negative inputs clamped to 0 via `max(0, int(...))` (L196-197) so the function is total. Policy defaults when `policy is None`: `StatusPolicy()` = `floor=2, success_first=True, partial_threshold=2` (models.py L546-548). `[CODE-VERIFIED]`

### 1.3 Mode dispatch + merge trigger (Step 2, L660–667)

`select_mode(mode)` (L276) returns one of three reducers from `_MODE_DISPATCH` (L269-273):

| `AmalgamationMode` | reducer | merged body | per-reviewer artifact |
|---|---|---|---|
| `raw` | `_reducer_raw` (L224) | always `None` | each worker's `raw_path` |
| `normalize` | `_reducer_normalize` (L236) | always `None` | each worker's **`final_path`** |
| `normalize+merge` | `_reducer_normalize_merge` (L248) | merge string when `M >= floor`, else `None` | each worker's **`final_path`** (files remain on disk) |

The merge gate is `workers_succeeded < policy.floor → return None` (L263-264) — mirrors the §5 "merged_path null when workers_succeeded < 2" rule. When the gate passes it calls `merge_callable` or `_default_merge` (L265-266). `_default_merge` (L314) lazy-imports `superclaude.cli.swarm.merge.mechanical_merge` (L325). `[CODE-VERIFIED]`

### 1.4 merged.md write (L685–689) and contract emission (Step 3, L691–724)

- `merged_path` is set to `str(output_dir / "merged.md")` **only** when `merged_body is not None AND output_dir is not None AND should_emit` (L686-689). `MERGED_FILENAME = "merged.md"` (L138). Written via `_atomic_write_bytes` (tmp + fsync + `os.replace`, L335-361). `[CODE-VERIFIED]`
- `should_emit` = `emit_to_disk` if explicitly set, else `output_dir is not None` (L671-673). `[CODE-VERIFIED]`
- The `ResultContract` is constructed AFTER status (L699-719), then written to disk via `emit_contract(contract, output_dir)` (L721-722) only when `should_emit and output_dir is not None`. `[CODE-VERIFIED]`
- `output_files=list(worker_results)` (L713) — the full per-worker list is carried verbatim onto the contract. `[CODE-VERIFIED]`
- `recommended_next_command` is the **rendered** template (`_render_recommended_next_command`, L467) — contrast JobSpec's unrendered `*_template`. `[CODE-VERIFIED]`

### 1.5 `emit_contract` — the swarm `return-contract.yaml` (DM-012) writer (L369–394)

```python
target  = Path(output_dir) / CONTRACT_FILENAME          # CONTRACT_FILENAME = "return-contract.yaml" (L139)
payload = to_dict(contract)                              # dataclasses.asdict recursion (models.py L1692)
body    = yaml.safe_dump(payload, sort_keys=False, allow_unicode=True)   # L392 — DM-012 declaration order preserved
_atomic_write_bytes(target, body.encode("utf-8"))       # tmp + fsync + os.replace
```

So the swarm `return-contract.yaml` is literally `to_dict(ResultContract)` dumped with `sort_keys=False`. Path is always `<output_dir>/return-contract.yaml`, confined to the caller-supplied `output_dir` (NFR-013). `[CODE-VERIFIED]`

Two other reduce-emitted filenames (L138-140): `MERGED_FILENAME = "merged.md"`, `CONTRACT_FILENAME = "return-contract.yaml"`, `DONE_SENTINEL_FILENAME = "done.json"`. `emit_done_sentinel` (L402) writes `done.json` to `Path(contract_path).parent` (co-located with the contract, L456). `[CODE-VERIFIED]`

---

## 2. Mechanical-concat merge boundary — `merge.py` (the scoring-free wall)

File: `src/superclaude/cli/swarm/merge.py`. The module is 58 lines total; `mechanical_merge` body is **8 LOC** (L50–57), under the ≤30-LOC NFR-008 ceiling. `[CODE-VERIFIED]`

### 2.1 The boundary contract — quoted verbatim from the docstring (L9–29)

```text
Boundary contract (AC-011 / AC-012 -- enforced by T05.05 review):

ALLOWED operations -- the entire surface area this module may grow into:
    1. Verbatim concat of per-worker ``final_path`` file contents.
    2. Ordering by :attr:`WorkerResult.index` (slot index, 0..N-1).
       This is structural ordering of *sections*, not semantic ranking.
    3. Prepend one provenance header per section, exactly:
       ``## From {model_label} ({elapsed_ms}ms)``.

DISALLOWED operations -- any addition here is a boundary violation and
must trip T05.05 PR review, T05.08 LOC ceiling, T05.09 boundary test,
or T05.10 scoring-engine grep audit:
    * sort / rank / score / judge findings
    * dedup / filter / drop sections
    * rewrite / paraphrase / reformat content
    * reorder content *within* a worker section
    * cross-worker synthesis or alignment
    * frontmatter / YAML rewriting beyond verbatim passthrough

Scoring, ranking, and adversarial merge live in ``/sc:adversarial``;
this module is intentionally too small to host any of them.
```

The four structural guards (docstring L31-40): (1) this docstring enumeration, (2) ≤30 LOC ceiling test `tests/swarm/test_merge_loc_ceiling.py`, (3) PR-touch review check on this file path, (4) the 3-worker boundary test `tests/swarm/test_merge_mechanical_only.py` + `tests/swarm/test_merge_no_transforms.py`. `[CODE-VERIFIED]`

### 2.2 The implementation (L50–57)

```python
def mechanical_merge(worker_results: list[WorkerResult]) -> str:
    sections: list[str] = []
    for wr in sorted(worker_results, key=lambda w: w.index):          # ordering by slot index only
        path = Path(wr.final_path) if wr.final_path else None          # reads final_path, NEVER raw_path/path/merged.md
        body = path.read_text(encoding="utf-8") if path and path.is_file() else ""
        header = f"## From {wr.model_label} ({wr.elapsed_ms}ms)"
        sections.append(f"{header}\n\n{body.rstrip()}\n")
    return "\n".join(sections)
```

Reads each worker's **`final_path`** (the post-normalization per-reviewer file), sorts by `index` only, prepends the fixed provenance header, joins with `\n`. No score/rank/dedup/rewrite. Missing/empty `final_path` → empty body (no error). Scoring is deferred to `/sc:adversarial`. `[CODE-VERIFIED]`

---

## 3. `ResultContract` (DM-012) — full field table

File: `src/superclaude/cli/swarm/models.py`. `@dataclass(frozen=True)` at L876; fields L997–1015. The class docstring claims **19 top-level keys** (L897-899) after the four `target.*` sub-fields collapse into one `ContractTarget`. The DM-012 `return-contract.yaml` IS `to_dict()` of this dataclass.

| # | Field | Type | Default | Semantics |
|---|---|---|---|---|
| 1 | `contract_version` | `str` | `"1.0"` | §5 schema version; mirrors `Manifest.contract_version`. |
| 2 | `status` | `ResultStatus` Literal `success`/`partial`/`failed` | `"success"` | IMM-5 verdict stamped at reduce. `__post_init__` rejects out-of-enum (L1017-1023). |
| 3 | `job_id` | `str` | `""` | UUID; mirrors `Manifest.job_id` / `SwarmState.job_id`. |
| 4 | `started` | `str` | `""` | ISO 8601 start timestamp. |
| 5 | `finished` | `str` | `""` | ISO 8601 finish timestamp. |
| 6 | `elapsed_ms` | `int` | `0` | finished − started delta. |
| 7 | `caller` | `CallerInfo` (DM-019) | stub | identity block copied verbatim from JobSpec. |
| 8 | `lens` | `str` | `""` | lens name; `""` when JSON-Schema-driven (no registered lens). |
| 9 | `lens_source` | `str` | `""` | `{"", "registry", "custom"}` (schema-validated at M2). |
| 10 | `target` | `ContractTarget` (nested) | stub | post-exec target snapshot (path/checksum/truncated/line_cap). |
| 11 | `workers_requested` | `int` | `0` | N. INV-005: `succeeded + failed == requested`. |
| 12 | `workers_succeeded` | `int` | `0` | **M** (success count). |
| 13 | `workers_failed` | `int` | `0` | N − M (non-success). |
| 14 | `output_files` | `list[WorkerResult]` (DM-013) | `[]` | **per-reviewer artifact list** (see §4). |
| 15 | `amalgamation_mode` | `AmalgamationMode` Literal `raw`/`normalize`/`normalize+merge` | `"normalize+merge"` | mode that ran. |
| 16 | `merged_path` | `Optional[str]` | `None` | path to `merged.md`; null when mode≠`normalize+merge` OR M < 2. |
| 17 | `caller_metadata` | `CallerMetadata` (DM-020) | stub | `suspect:bool` + `tier:str` (OQ-009 lens/caller precedence). |
| 18 | `recommended_next_command` | `str` | `""` | **rendered** next-command string. |
| 19 | `artifacts` | `Artifacts` (DM-018) | stub | path bundle (manifest/state/event-logs/done_sentinel). |

Nested `ContractTarget` (DM-012 `target.*`, L842-873): `path:str`, `checksum:str` (sha256 → 12 hex), `truncated:bool=False`, `truncation_line_cap:int=4000`. `[CODE-VERIFIED]`

---

## 4. `output_files[].final_path` — per-reviewer artifact structure (DM-013 `WorkerResult`)

`@dataclass WorkerResult` (models.py L1026), fields L1117–1128. Each entry in `ResultContract.output_files` is one of these — the per-reviewer artifact record reduce/merge and reflect both consume.

| Field | Type | Default | Semantics |
|---|---|---|---|
| `index` | `int` | `0` | slot index 0..N-1; drives merge ordering + `{index:02d}` filename. |
| `path` | `str` | `""` | canonical output path (post-normalize, or = raw_path in raw mode). |
| `raw_path` | `str` | `""` | per-worker raw output `*.raw.<ext>`; retained when `retain_raw=True`. |
| `meta_path` | `str` | `""` | per-worker meta sidecar `*.meta.json` (transport/model/attempts/http/status). |
| **`final_path`** | `str` | `""` | **per-worker post-normalization file consumed by Wave-3 reduce/merge AND by reflect.** Diverges from `path` only when normalization rewrites under a different filename. |
| `model_id` | `str` | `""` | transport model id (e.g. `gpt-5-codex`, `claude-haiku-4.5`). |
| `model_label` | `str` | `""` | human label printed in merge provenance header `## From {model_label}`. |
| `bytes` | `int` | `0` | output byte count. |
| `status` | `WorkerStatus` Literal `success`/`timeout`/`parse_error`/`proxy_error` | `"success"` | drives M-count; `__post_init__` enforces enum (L1130-1136). |
| `http_code` | `Optional[int]` | `None` | transport HTTP status; `None` for stub transport / no HTTP. |
| `attempts` | `int` | `1` | 1 (no retry) or 2 (5xx retried once per FR-017). |
| `elapsed_ms` | `int` | `0` | per-worker wall-clock; printed in provenance header. |

**`final_path` is the load-bearing per-reviewer artifact pointer.** `mechanical_merge` reads `final_path` (merge.py L53); `normalize` and `normalize+merge` modes both name `final_path` as the per-reviewer artifact (reduce.py L243, L294). Reflect MUST consume `output_files[].final_path`, never `merged.md` (see §6). `[CODE-VERIFIED]`

---

## 5. `done.json` sentinel shape (DM-017 `DoneSentinel`)

`@dataclass(frozen=True) DoneSentinel` (models.py L1423), fields L1479–1481. Written by `emit_done_sentinel` (reduce.py L402-459) via `json.dumps(to_dict(sentinel), sort_keys=True, indent=2) + "\n"` (L457) to `<contract_path>.parent/done.json` (L456).

| Field | Type | Default | Semantics |
|---|---|---|---|
| `atomic_write` | `bool` | `True` | always-on; write uses tmp + fsync + `os.replace`. |
| `terminal_status` | `ResultStatus` Literal `success`/`partial`/`failed` | `"success"` | IMM-5 verdict; `__post_init__` enforces enum (L1483-1489). |
| `contract_path` | `str` | `""` | absolute path to `return-contract.yaml` (lets a poller locate the rich record). |

Sentinel JSON shape (sorted keys):
```json
{
  "atomic_write": true,
  "contract_path": "<abs path to return-contract.yaml>",
  "terminal_status": "success"
}
```

Note the kill path (`commands._emit_killed_done_sentinel`, referenced L429-432) bypasses the dataclass because `"killed"` is intentionally NOT in `ResultStatus`; the IMM-5 reduce path goes through the dataclass guard (only `success`/`partial`/`failed`). `[CODE-VERIFIED]`

`Artifacts` (DM-018, L1492) bundles the on-disk paths embedded in `ResultContract.artifacts`: `manifest_path`, `state_path`, `event_log_jsonl`, `event_log_md`, `done_sentinel` (all `str`, default `""`). `done_sentinel` here is the **path** (str), not a `DoneSentinel` instance. `[CODE-VERIFIED]`

---

## 6. The two path-confinement contracts (swarm ↔ reflect)

**Contract A — reflect consumes per-reviewer `output_files[].final_path`, NEVER `merged.md`.**
- The swarm side EMITS both: `output_files` (the per-reviewer `WorkerResult` list, each with `final_path`) AND, in `normalize+merge` mode, a single `merged.md` whose path is on `merged_path`. `[CODE-VERIFIED]`
- `merged.md` is the mechanical concat — scoring-free, no judging (merge.py §2). Reflect's job (independent adversarial review) requires the SEPARATE per-reviewer bodies, not the pre-concatenated blob; feeding `merged.md` to reflect would collapse the per-reviewer diversity that reflect's ensemble depends on. So reflect must read each `final_path` individually. This is a contract assertion grounded in the swarm-side artifact split; the reflect-side enforcement code lives in the reflect runner (synth-04 / file `01`/`02` territory) — `[UNVERIFIED]` from swarm code alone (see Gaps).

**Contract B — `reflect.derive_verdict` parses `<output_dir>/return-contract.yaml` and MUST NOT parse the `t2-swarm/` subdir contract directly.**
- There are **two distinct files both named `return-contract.yaml`** with **different schemas**:
  - **Swarm DM-012** (`<swarm-output_dir>/return-contract.yaml`) = `to_dict(ResultContract)` → keys: `contract_version, status, job_id, started, finished, elapsed_ms, caller, lens, lens_source, target, workers_requested, workers_succeeded, workers_failed, output_files, amalgamation_mode, merged_path, caller_metadata, recommended_next_command, artifacts`. (reduce.py L369-394) `[CODE-VERIFIED]`
  - **Reflect contract** (`<reflect output_dir>/return-contract.yaml`) parsed by `src/superclaude/cli/reflect/contract.py::parse_contract` (L65) → reads keys: `status`, `tier_reached` (L113/L195), `t2_model_class_diversity` (L267), `merge_method` (L280), `adversarial_convergence_score` (L284), `deviation_count_by_class` (L92), `report_path` (L119), `remediation_task_path` (L126). `[CODE-VERIFIED]`
- **These key sets barely overlap.** Only `status` is a shared key name — but even there the swarm `status` is the IMM-5 `success`/`partial`/`failed` worker verdict, while the reflect `status` feeds a different `success`-vs-tier check (`contract.py` L235). The reflect-specific fields (`tier_reached`, `t2_model_class_diversity`, `merge_method`, `adversarial_convergence_score`, `deviation_count_by_class`) are **NOT present on the swarm DM-012 `ResultContract`**. `[CODE-VERIFIED]`
- Therefore the swarm `t2-swarm/` subdir contract is NOT directly parseable by `reflect.derive_verdict` as if it were the reflect contract: the schemas are disjoint. The confinement contract is that reflect parses ITS OWN `<output_dir>/return-contract.yaml`; the swarm subdir's DM-012 contract is consumed only via a mapping/synthesis layer (`ensemble.py`), never fed raw into `derive_verdict`. `[CODE-VERIFIED]` on the schema-disjointness; the explicit "must not parse t2-swarm subdir" assertion is the design rule the OI-1 table encodes (reflect contract.py takes a single `path: Path` and does not walk into `t2-swarm/` — it parses exactly the path the runner pins, `contract.py` L65, `_make_result` L120 comment "runner fills the pinned path it parsed"). `[CODE-VERIFIED]`

---

## 7. OI-1 combined correspondence — swarm-field → reflect-field

`02-reflect-contract-verdict.md` exists but is a **stub header only** (`Status: In Progress`, no field table body yet as of this turn). The reflect-side join therefore **completes in synthesis (synth-04)**. I read `reflect/contract.py` directly to attempt the mapping rather than relying on the absent file.

The reflect verdict-driver fields and whether a swarm DM-012 field maps onto them:

| Reflect-side field (consumed by `derive_verdict`) | Swarm DM-012 source? | Mapping needed |
|---|---|---|
| `status` (`contract.py` L116/L235) | `ResultContract.status` exists, BUT semantics differ (IMM-5 worker verdict ≠ reflect tier-success). | **Re-mapping** required; not a passthrough. |
| `tier_reached` (L113/L195/L263) | **Absent** on swarm DM-012. | Must be SYNTHESIZED by an `ensemble.py`-style layer from swarm execution facts (e.g. how many T2 reviewers ran / merge mode). |
| `merge_method` (L280, value `single-reviewer-fallback`) | **Absent** on swarm DM-012. Closest swarm signal: `amalgamation_mode` (`normalize+merge` vs not) + `workers_succeeded` (M<2 → no merge). | Must be DERIVED from swarm `amalgamation_mode` + M (`merged_path is None` ⇔ no merge). |
| `t2_model_class_diversity` (L267) | **Absent** on swarm DM-012. Closest swarm signal: distinct `output_files[].model_id` / `model_label` set. | Must be COMPUTED by `ensemble.py` from the distinct model classes in `output_files`. |
| `reviewer_count` (task brief) | **Absent** as a named key; swarm equivalent = `workers_succeeded` (M) or `len(output_files)`. | Maps onto swarm `workers_succeeded` / `workers_requested`; rename + re-derive. |
| `adversarial_convergence_score` (L284) | **Absent** on swarm DM-012 entirely (a `/sc:adversarial` artifact, not a swarm artifact). | Comes from the adversarial stage, NOT from swarm. |
| `deviation_count_by_class` (L92) | **Absent** on swarm DM-012. | Reflect/adversarial-side only. |

**Conclusion:** essentially every reflect verdict field except a loose `status` name-collision requires a mapping/synthesis layer. The swarm DM-012 contract supplies the *raw execution facts* (`workers_succeeded`, `amalgamation_mode`, `merged_path`, `output_files[].model_id/model_label/final_path`); an `ensemble.py` mapping turns those into the reflect verdict vocabulary (`tier_reached`, `merge_method`, `t2_model_class_diversity`, `reviewer_count`). The OI-1 table is load-bearing precisely because the two `return-contract.yaml` schemas are NOT interchangeable. `[CODE-VERIFIED]` (swarm side); reflect-side join finalized in synth-04.

---

## Key Takeaways

1. **M (success count) computation is one line:** `workers_succeeded = sum(1 for w in worker_results if w.status == "success")` (reduce.py L648). N = `workers_requested` if supplied else `len(worker_results)` (L650-653). `workers_failed` counts non-success against `len(worker_results)`, not against N.
2. **IMM-5 status order matters:** the `success_first AND M==N==2 → success` tie-break is evaluated FIRST (L205), before the `M>=N`, partial-window, and failed checks. Defaults `floor=2, success_first=True, partial_threshold=2`.
3. **The merge boundary is a hard scoring-free wall.** `mechanical_merge` (8 LOC) reads each worker's `final_path`, sorts by `index`, prepends `## From {model_label} ({elapsed_ms}ms)`, concats. DISALLOWED: sort/rank/score/judge/dedup/filter/rewrite/synthesis. Scoring is delegated to `/sc:adversarial`. Four guards: docstring + ≤30 LOC ceiling test + PR-touch check + 3-worker boundary test.
4. **The swarm `return-contract.yaml` (DM-012) = `to_dict(ResultContract)` dumped with `sort_keys=False`** at `<output_dir>/return-contract.yaml`. 19 top-level keys. `merged_path` is null unless mode=`normalize+merge` AND M≥floor AND output_dir set.
5. **`final_path` is the per-reviewer artifact pointer** on each `WorkerResult` in `output_files`. Both merge and (per design) reflect consume `final_path` — never `merged.md`.
6. **Two files named `return-contract.yaml`, disjoint schemas.** The swarm DM-012 contract and the reflect contract share only the key name `status` (with different semantics). The reflect verdict fields (`tier_reached`, `merge_method`, `t2_model_class_diversity`, `adversarial_convergence_score`, `deviation_count_by_class`) do NOT exist on swarm DM-012. The OI-1 join requires a mapping/synthesis layer.

## Gaps and Questions

1. **`[CODE-CONTRADICTED]` — no `ensemble.py` exists.** `find src -name "*ensemble*"` returns nothing. The OI-1 mapping layer (swarm execution facts → reflect verdict vocabulary) that the task brief assumes does not yet exist in code. This is consistent with a TDD/hardening task (it is to-be-designed), but the table cannot cite a current `ensemble.py` symbol.
2. **`[CODE-CONTRADICTED]` — reflect does NOT currently consume swarm artifacts.** `grep -rn "t2-swarm\|final_path\|output_files" src/superclaude/cli/reflect/` returns zero hits. Reflect's `runner.py` parses a single pinned `config.contract_path` (L420) and never walks a `t2-swarm/` subdir. So today the swarm↔reflect wiring is NOT implemented; the path-confinement contracts (§6) describe the *intended* design, not current behavior. The "reflect consumes `final_path` not `merged.md`" and "must not parse t2-swarm subdir" rules are **design assertions to be built**, not existing enforcement.
3. **`[UNVERIFIED]` — reflect-side field table.** `02-reflect-contract-verdict.md` is a stub header only; the authoritative reflect-side field list comes from that file when complete. I sourced reflect fields directly from `reflect/contract.py` this turn, but the canonical cross-reference table is finalized in synth-04.
4. **INV-005 inside `reduce_wave3`:** `workers_failed` is computed against `len(worker_results)`, while N can be `workers_requested`. If a caller passes `workers_requested > len(worker_results)`, the emitted contract's `succeeded + failed != requested`. The dataclass does not enforce INV-005 (models.py L982-986 defers it to the emitter), and `reduce_wave3` does not re-check it. Worth flagging for the TDD as a possible invariant gap.

## Summary

The swarm Wave-3 reduce path (`reduce_wave3`, reduce.py L555) computes **M = count of `success` `WorkerResult`s** and applies the IMM-5 truth table (`determine_status`, L158) to stamp `status ∈ {success, partial, failed}`, then dispatches by `AmalgamationMode`: `raw`/`normalize` produce no `merged.md`; `normalize+merge` calls the scoring-free `mechanical_merge` (merge.py L50, 8 LOC) when M≥floor, which concats each worker's `final_path` in `index` order with a fixed provenance header and explicitly forbids any sort/rank/score/judge/dedup/rewrite (delegated to `/sc:adversarial`). The terminal artifact is the DM-012 `ResultContract` (models.py L876, 19 keys) serialized as `to_dict()` → `<output_dir>/return-contract.yaml` (`emit_contract`, L369), with per-reviewer `output_files[].final_path` records (DM-013) and a co-located `done.json` sentinel (DM-017: `atomic_write`, `terminal_status`, `contract_path`). The load-bearing OI-1 finding: the swarm DM-012 `return-contract.yaml` and the reflect `return-contract.yaml` are **two disjoint schemas sharing one filename** — reflect's verdict fields (`tier_reached`, `merge_method`, `t2_model_class_diversity`, `adversarial_convergence_score`, `deviation_count_by_class`) have no DM-012 counterparts and must be synthesized from swarm raw facts (`workers_succeeded`, `amalgamation_mode`, `merged_path`, distinct `output_files[].model_id`). That mapping layer (`ensemble.py`) and the swarm→reflect wiring do **not yet exist** in code — the path-confinement contracts in §6 are design rules for the TDD to implement, not current enforcement.

---

**Status: Complete**
