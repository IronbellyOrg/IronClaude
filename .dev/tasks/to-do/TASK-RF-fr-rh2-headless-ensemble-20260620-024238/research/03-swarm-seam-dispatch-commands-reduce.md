# R3: Swarm Seam — Data Flow Tracer (dispatch / commands / reduce / merge / models)

**Status: Complete**
**Date: 2026-06-20**
**Scope:** `src/superclaude/cli/swarm/{dispatch,commands,reduce,merge,models}.py`
**Focus:** Exact current signatures + data records the new `cli/reflect/ensemble.py` will IMPORT and compose. Zero-trust line anchors.

---

## 1. `dispatch.py::dispatch_wave1` — VERBATIM SIGNATURE

File length: 508 lines. Function `def dispatch_wave1` at **dispatch.py:334**; body ends at **dispatch.py:508** (`return results`).

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
(dispatch.py:334–343)

Keyword-only params after `transport`: `transport_for_slot`, `prompt`, `parallel_executor`, `worker_spec`, `logger` (the `*` is at **dispatch.py:337**).

**Return contract** — `list[WorkerResult]` of length N (`workers_requested`), sorted by slot `index` 0..N-1 (docstring dispatch.py:404–407; positional alignment loop dispatch.py:485–490).

**`transport_for_slot` precedence over `transport`** — when supplied, it is invoked once per slot and **takes precedence**; falls back to the single shared `transport` only when the factory is `None`:
```python
slot_transport = (
    transport_for_slot(slot_index)
    if transport_for_slot is not None
    else transport
)
```
(dispatch.py:453–457)

**Synthesized `proxy_error` backstop** (guarantees exactly one `WorkerResult` per slot even if `ParallelExecutor` returns `None` for a slot):
```python
results: list[WorkerResult] = []
for index in range(workers_requested):
    outcome = raw_results.get(f"worker-{index:02d}")
    if isinstance(outcome, WorkerResult):
        results.append(outcome)
    else:
        results.append(WorkerResult(index=index, status="proxy_error", attempts=1))
```
(dispatch.py:484–490)

**Early-exit conditions:**
- Both transports `None` → `return []` — `if transport is None and transport_for_slot is None: return []` (dispatch.py:409–410).
- `workers_requested <= 0` → `return []` (dispatch.py:412–414). N is read from `preflight_result.manifest.preflight.workers_requested` (dispatch.py:412).

**Single-writer / FR-1 quiet line:**
```python
executor = parallel_executor or ParallelExecutor(max_workers=workers_requested)
executor.quiet = True  # FR-1: swarm dispatch path is silent; workers emit to files.
```
(dispatch.py:424–425)

Routing note: dispatch builds `Task(...)` objects and calls `executor.plan(tasks)` then `executor.execute(plan)` (dispatch.py:464–475) — never instantiates `ThreadPoolExecutor` directly (AC-004/NFR-001, docstring dispatch.py:346–351).

---

## 2. `commands.py::_resolve_run_transport_factory` — VERBATIM SIGNATURE (PRIVATE)

File length: 3806 lines. Function at **commands.py:612**; body ends at **commands.py:707** (the `raise ValueError(...)` for unknown kind, 704–707).

```python
def _resolve_run_transport_factory(
    transport_kind: str,
    *,
    models: Optional[list[str]] = None,
    env: Optional[Mapping[str, str]] = None,
    workers_requested: Optional[int] = None,
) -> Callable[[int], Any]:
```
(commands.py:612–618)

**CONFIRMED PRIVATE** — leading underscore `_resolve_run_transport_factory` (commands.py:612). This is the Q7 coupling smell: the ensemble must import a module-private symbol (or the run path must expose a public wrapper). Return type is `Callable[[int], Any]` (a per-slot factory `(slot_index) -> Transport`).

**openai_compat branch** (commands.py:674–703):
```python
if transport_kind == "openai_compat":
    from superclaude.cli.swarm.transports.openai_compat import (
        OpenAICompatTransport,
        read_env,
    )

    config = read_env(env)  # eager: raises TransportEnvError if incomplete
    pool = [m for m in config.models if m]
    if not pool:  # defensive -- read_env raises before reaching here
        raise ValueError("swarm run: openai_compat model pool is empty")
    # D2 guard ...
    if workers_requested is not None and len(pool) < workers_requested:
        raise ModelPoolTooSmallError(len(pool), workers_requested)
    cache: dict[str, Any] = {}

    def _factory(slot_index: int) -> Any:
        model = pool[slot_index % len(pool)]
        transport = cache.get(model)
        if transport is None:
            transport = OpenAICompatTransport(
                base_url=config.base_url,
                api_key=config.api_key,
                model=model,
            )
            cache[model] = transport
        return transport

    return _factory
```
- `read_env(env)` at commands.py:680 (eager — raises `TransportEnvError` here, before dispatch).
- `pool = [m for m in config.models if m]` at commands.py:681.
- Pool guard `if workers_requested is not None and len(pool) < workers_requested: raise ModelPoolTooSmallError(...)` at commands.py:687–688.
- Slot binding rule `pool[slot_index % len(pool)]` at commands.py:692; per-model client cache at commands.py:689,693–700 (one `OpenAICompatTransport` per unique model, reused across repeated slots).

**stub branch** (commands.py:670–673) — one shared `StubTransport` for every slot:
```python
if transport_kind == "stub":
    # Single shared stub for every slot (single-model behaviour preserved).
    shared = _resolve_run_transport("stub", models=models, env=env)
    return lambda _slot: shared
```
The shared stub comes from the sibling `_resolve_run_transport("stub", ...)` (commands.py:567–570 builds `StubTransport(model_id=model_id)`).

Unknown kind → `raise ValueError(...)` (commands.py:704–707).

---

## 3. `commands.py::ModelPoolTooSmallError`

Class definition at **commands.py:589** (`class ModelPoolTooSmallError(RuntimeError):`). Body ends commands.py:609.

```python
class ModelPoolTooSmallError(RuntimeError):
    ...
    def __init__(self, pool_size: int, workers_requested: int) -> None:
        self.pool_size = pool_size
        self.workers_requested = workers_requested
        super().__init__( ... )
```
(class commands.py:589; `__init__` commands.py:601–609)

**Two args carried:** `pool_size` (stored `self.pool_size`, commands.py:602) and `workers_requested` (stored `self.workers_requested`, commands.py:603).

**Where it raises eagerly:** inside `_resolve_run_transport_factory`, openai_compat branch, **before any slot is dispatched** — `raise ModelPoolTooSmallError(len(pool), workers_requested)` at **commands.py:688** (guarded by `len(pool) < workers_requested`). Subclasses `RuntimeError`.

The run path supplies `workers_requested` from preflight: `_resolve_run_transport_factory(..., workers_requested=preflight_result.manifest.preflight.workers_requested)` at **commands.py:1833–1838** (and resume path commands.py:2086).

---

## 4. `reduce.py::reduce_wave3` — VERBATIM SIGNATURE

File length: 724 lines. Function at **reduce.py:555**; body ends **reduce.py:724** (`return contract`).

```python
def reduce_wave3(
    worker_results: list[WorkerResult],
    mode: AmalgamationMode = "normalize+merge",
    *,
    output_dir: Optional[Path] = None,
    workers_requested: Optional[int] = None,
    status_policy: Optional[StatusPolicy] = None,
    job_id: str = "",
    started: str = "",
    finished: str = "",
    elapsed_ms: int = 0,
    caller: Optional[CallerInfo] = None,
    caller_metadata: Optional[CallerMetadata] = None,
    lens: str = "",
    lens_source: str = "",
    target: Optional[ContractTarget] = None,
    artifacts: Optional[Artifacts] = None,
    recommended_next_command_template: str = "",
    recommended_next_command_substitutions: Optional[Mapping[str, str]] = None,
    merge_callable: Optional[MergeCallable] = None,
    emit_to_disk: Optional[bool] = None,
    resume: bool = False,
) -> ResultContract:
```
(reduce.py:555–577) — all params after `mode` are keyword-only (`*` at reduce.py:558).

**M = workers_succeeded** computed line: `workers_succeeded = sum(1 for w in worker_results if w.status == "success")` (**reduce.py:648**). `workers_failed = sum(1 for w in worker_results if w.status != "success")` (reduce.py:649).

**N = effective_n** computation:
```python
effective_n = (
    int(workers_requested) if workers_requested is not None
    else len(worker_results)
)
```
(**reduce.py:650–653**) — defaults to `len(worker_results)` when `workers_requested` not passed.

**`determine_status`** at **reduce.py:158** (signature `determine_status(workers_succeeded, workers_requested, policy=None) -> ResultStatus`, reduce.py:158–162). Called from reduce_wave3 at reduce.py:654–658. IMM-5 defaults from `StatusPolicy()` — `floor=2`, `success_first=True`, `partial_threshold=2` (docstring reduce.py:177–178; read at reduce.py:198–200). Matrix logic:
- success_first tie-break `m == n == 2` → `"success"` (reduce.py:205–206)
- `m >= n and n > 0` → `"success"` (reduce.py:208–209)
- partial window `m >= max(floor, partial_threshold) and m < n` → `"partial"` (reduce.py:213–214)
- else → `"failed"` (reduce.py:216)

**AmalgamationMode dispatch** — `reducer = select_mode(mode)` (reduce.py:661); `merged_body = reducer(worker_results, merge_callable=..., workers_succeeded=..., policy=...)` (reduce.py:662–667). The three modes map via `_MODE_DISPATCH` (reduce.py:269–274): `raw`→`_reducer_raw`, `normalize`→`_reducer_normalize`, `normalize+merge`→`_reducer_normalize_merge`. The `normalize+merge` reducer calls `mechanical_merge` only when `M >= floor`: `if workers_succeeded < policy.floor: return None` (reduce.py:263) — the merge gate (reduce.py:252–267, mirrors "merged_path is null when workers_succeeded < 2").

**Emit conditions** — disk emission resolved at reduce.py:671–673:
```python
should_emit = (
    emit_to_disk if emit_to_disk is not None else output_dir is not None
)
```
- `merged.md` written when `merged_body is not None and output_dir is not None and should_emit` (reduce.py:686–689; `MERGED_FILENAME`).
- `return-contract.yaml` written when `should_emit and output_dir is not None`: `emit_contract(contract, Path(output_dir))` (**reduce.py:721–722**). `emit_contract` (reduce.py:369) writes `output_dir / "return-contract.yaml"` (`CONTRACT_FILENAME = "return-contract.yaml"`, reduce.py:139) via `to_dict` + `yaml.safe_dump(..., sort_keys=False)` (reduce.py:390–393).

**done.json caveat (line-anchor drift vs TDD):** `reduce_wave3` does **NOT** itself emit `done.json`. The done-sentinel emitter is a SEPARATE function `emit_done_sentinel(terminal_status, contract_path)` at **reduce.py:402** (writes `done.json` = `DONE_SENTINEL_FILENAME`, reduce.py:140; target `contract.parent / "done.json"`, reduce.py:456; via `DoneSentinel(...)` reduce.py:451–453 then `_atomic_write_bytes` reduce.py:458). The executor/run path calls `emit_done_sentinel` after `reduce_wave3` returns — `reduce_wave3` only emits `merged.md` + `return-contract.yaml`. If the TDD claims `reduce_wave3` emits both `return-contract.yaml` AND `done.json`, that is a drift: done.json is emitted by `emit_done_sentinel`, not inside `reduce_wave3`.

---

## 5. `merge.py::mechanical_merge`

File length: **57 lines total**. Function `def mechanical_merge` at **merge.py:50**; body is **merge.py:50–57** → **8 LOC** (signature + 7-line body), well under the NFR-008 <=30 LOC ceiling (T05.08).

```python
def mechanical_merge(worker_results: list[WorkerResult]) -> str:
    sections: list[str] = []
    for wr in sorted(worker_results, key=lambda w: w.index):
        path = Path(wr.final_path) if wr.final_path else None
        body = path.read_text(encoding="utf-8") if path and path.is_file() else ""
        header = f"## From {wr.model_label} ({wr.elapsed_ms}ms)"
        sections.append(f"{header}\n\n{body.rstrip()}\n")
    return "\n".join(sections)
```
(merge.py:50–57)

**Confirmed behaviour:** reads each worker's `final_path` (merge.py:53–54), orders by slot `index` via `sorted(..., key=lambda w: w.index)` (merge.py:52), prepends a one-line provenance header `## From {model_label} ({elapsed_ms}ms)` (merge.py:55). Verbatim concat with `"\n".join` (merge.py:57). Empty body when `final_path` missing/not a file (merge.py:54).

**DISALLOWED-operations enumeration** (module docstring merge.py:18–26) — the boundary FR-RH2.3 must NOT cross:
> * sort / rank / score / judge findings
> * dedup / filter / drop sections
> * rewrite / paraphrase / reformat content
> * reorder content *within* a worker section
> * cross-worker synthesis or alignment
> * frontmatter / YAML rewriting beyond verbatim passthrough

ALLOWED set (merge.py:11–16): verbatim concat of `final_path` contents; ordering by `index` (structural section ordering, NOT semantic ranking); prepend the one provenance header. Docstring explicitly: "Scoring, ranking, and adversarial merge live in `/sc:adversarial`; this module is intentionally too small to host any of them." (merge.py:28–29). Note merge.py:13 sorts by `index` (NOT `score`) — the `sort` in `sorted(...)` is structural slot ordering, not a ranking sort.

---

## 6. `models.py` data records

File length: 1884 lines. `WorkerStatus` and `ResultStatus` are **`Literal` type aliases, NOT enum classes**:
- `ResultStatus = Literal["success", "partial", "failed"]` (**models.py:68**)
- `WorkerStatus = Literal["success", "timeout", "parse_error", "proxy_error"]` (**models.py:69**)

### 6a. `WorkerResult` (DM-013)
`@dataclass` at models.py:1026; `class WorkerResult:` at **models.py:1027**. Fields **models.py:1117–1128** (12 fields, in order):
```python
index: int = 0                       # 1117
path: str = ""                       # 1118
raw_path: str = ""                   # 1119
meta_path: str = ""                  # 1120
final_path: str = ""                 # 1121
model_id: str = ""                   # 1122
model_label: str = ""                # 1123
bytes: int = 0                       # 1124
status: WorkerStatus = "success"     # 1125  (Literal, not enum)
http_code: Optional[int] = None      # 1126
attempts: int = 1                    # 1127
elapsed_ms: int = 0                  # 1128
```
`__post_init__` guard (models.py:1130–1136): `status` must be in `typing.get_args(WorkerStatus)` else `ValueError`.

### 6b. `ResultContract` (DM-012) — FROZEN
`@dataclass(frozen=True)` at **models.py:876**; `class ResultContract:` at **models.py:877**. Fields **models.py:997–1015** (19 fields, in declaration order):
```python
contract_version: str = "1.0"                                                  # 997
status: ResultStatus = "success"                                               # 998
job_id: str = ""                                                               # 999
started: str = ""                                                              # 1000
finished: str = ""                                                             # 1001
elapsed_ms: int = 0                                                            # 1002
caller: "CallerInfo" = field(default_factory=lambda: CallerInfo())            # 1003
lens: str = ""                                                                 # 1004
lens_source: str = ""                                                          # 1005
target: "ContractTarget" = field(default_factory=lambda: ContractTarget())    # 1006
workers_requested: int = 0                                                      # 1007
workers_succeeded: int = 0                                                      # 1008
workers_failed: int = 0                                                         # 1009
output_files: list["WorkerResult"] = field(default_factory=list)              # 1010
amalgamation_mode: AmalgamationMode = "normalize+merge"                        # 1011
merged_path: Optional[str] = None                                             # 1012
caller_metadata: "CallerMetadata" = field(default_factory=lambda: CallerMetadata())  # 1013
recommended_next_command: str = ""                                            # 1014
artifacts: "Artifacts" = field(default_factory=lambda: Artifacts())          # 1015
```
`__post_init__` guard (models.py:1017–1023): `status` ∈ `typing.get_args(ResultStatus)` else `ValueError`. All requested fields present: workers_requested/workers_succeeded/workers_failed (1007–1009), output_files (1010), amalgamation_mode (1011), merged_path (1012), caller_metadata (1013), recommended_next_command (1014), status (998).

### 6c. `DoneSentinel` (DM-017) — FROZEN
`@dataclass(frozen=True)` at models.py:1423; `class DoneSentinel:` at **models.py:1424**. Fields **models.py:1479–1481** (3 fields):
```python
atomic_write: bool = True               # 1479
terminal_status: ResultStatus = "success"  # 1480
contract_path: str = ""                 # 1481
```
`__post_init__` (models.py:1483–1489): `terminal_status` ∈ `typing.get_args(ResultStatus)` else `ValueError`.

### 6d. `LensEntry` (DM-010)
`@dataclass` at models.py:636; `class LensEntry:` at **models.py:637**. Fields **models.py:707–720** (14 fields, in order):
```python
name: str = ""                                       # 707
description: str = ""                                 # 708
system_prompt_fragment: str = ""                      # 709
user_template: str = ""                               # 710
output_template_path: str = ""                        # 711
recipe_name: str = ""                                 # 712
normalizer_strategy: str = ""                         # 713
default_workers: int = 3                               # 714
default_target_line_cap: int = 4000                   # 715
suspect: bool = False                                 # 716
tier: str = ""                                        # 717
recommended_next_command_template: str = ""           # 718
acceptance_notes: str = ""                            # 719
stability: Stability = "stable"                       # 720
```
`__post_init__` (models.py:722–728): `stability` ∈ `typing.get_args(Stability)` else `ValueError`. All task-named load-bearing fields present: name(707), system_prompt_fragment(709), user_template(710), output_template_path(711), recipe_name(712), normalizer_strategy(713), default_workers(714), suspect(716), tier(717), recommended_next_command_template(718), stability(720).

---

## 7. OI-1 CONFIRMATION — reflect verdict-driver fields are ABSENT from the swarm seam

Grep across all five files (`dispatch.py`, `commands.py`, `reduce.py`, `merge.py`, `models.py`):
```
grep -nE "tier_reached|merge_method|t2_model_class_diversity|t2_vendor_diversity|reviewer_count|adversarial_convergence_score" <5 files>
→ EXIT 1 (zero matches)
```
**CONFIRMED:** NONE of `tier_reached`, `merge_method`, `t2_model_class_diversity`, `t2_vendor_diversity`, `reviewer_count`, `adversarial_convergence_score` appear anywhere in the swarm seam. The TDD claim that they are ALL absent from `ResultContract` is correct.

The only shared key name between `ResultContract` and the reflect return-contract is **`status`** (`ResultContract.status: ResultStatus = Literal["success","partial","failed"]`, models.py:998). Its semantics are the IMM-5 worker-count verdict (M/N success/partial/failed), NOT a reflect deviation-taxonomy verdict — same key name, different domain. The new `ensemble.py` therefore composes swarm dispatch as a transport/fan-out mechanism only; it cannot read any reflect-domain verdict field off the swarm `ResultContract` and must derive reflect verdict drivers itself from worker outputs (i.e., FR-RH2.3 must NOT add scoring into `mechanical_merge`).

---

## SUMMARY

### (a) The three verbatim signatures the ensemble must reproduce/compose

1. `dispatch_wave1(preflight_result, transport=None, *, transport_for_slot=None, prompt="", parallel_executor=None, worker_spec=None, logger=None) -> list[WorkerResult]` — dispatch.py:334–343. Returns one `WorkerResult` per slot (length N), backstopped to `proxy_error` so the per-slot invariant always holds.
2. `_resolve_run_transport_factory(transport_kind, *, models=None, env=None, workers_requested=None) -> Callable[[int], Any]` — commands.py:612–618. **PRIVATE** (Q7 coupling smell). openai_compat binds slot `i`→`pool[i % len(pool)]` with a per-model transport cache; raises `ModelPoolTooSmallError` eagerly when the env pool < `workers_requested`.
3. `reduce_wave3(worker_results, mode="normalize+merge", *, output_dir=None, workers_requested=None, status_policy=None, job_id="", started="", finished="", elapsed_ms=0, caller=None, caller_metadata=None, lens="", lens_source="", target=None, artifacts=None, recommended_next_command_template="", recommended_next_command_substitutions=None, merge_callable=None, emit_to_disk=None, resume=False) -> ResultContract` — reduce.py:555–577. M=`workers_succeeded` (reduce.py:648), N=`effective_n` (reduce.py:650–653), IMM-5 via `determine_status` (floor=2/success_first=True/partial_threshold=2). Emits `return-contract.yaml` via `emit_contract` (reduce.py:721–722) + `merged.md` when M>=floor.

`mechanical_merge(worker_results: list[WorkerResult]) -> str` — merge.py:50–57 (8 LOC) — verbatim concat of `final_path` bodies ordered by `index`, one provenance header each. The DISALLOWED list (merge.py:18–26: sort/rank/score/judge/dedup/filter/rewrite/synthesis) is the boundary FR-RH2.3 must NOT add scoring to.

### (b) OI-1 confirmation — which reflect fields are ABSENT from ResultContract

CONFIRMED ABSENT (grep exit 1, zero hits across all 5 files): `tier_reached`, `merge_method`, `t2_model_class_diversity`, `t2_vendor_diversity`, `reviewer_count`, `adversarial_convergence_score`. The TDD claim is accurate. `ResultContract`'s 19 fields (models.py:997–1015) are pure swarm-domain (contract_version, status, job_id, started, finished, elapsed_ms, caller, lens, lens_source, target, workers_requested, workers_succeeded, workers_failed, output_files, amalgamation_mode, merged_path, caller_metadata, recommended_next_command, artifacts). The ONLY shared key name with the reflect return-contract is `status` (models.py:998) — same key, different semantics (IMM-5 worker-count verdict, not reflect deviation taxonomy). The ensemble therefore uses swarm only as a fan-out/transport mechanism and must derive all reflect verdict drivers itself.

### (c) Line-anchor drift vs the TDD

1. **done.json is NOT emitted by `reduce_wave3`.** `reduce_wave3` emits only `merged.md` + `return-contract.yaml` (reduce.py:686–689, 721–722). `done.json` is written by a SEPARATE function `emit_done_sentinel(terminal_status, contract_path)` at reduce.py:402 (called by the run/executor path after `reduce_wave3` returns). If the TDD attributes done.json emission to `reduce_wave3`, correct it: the emitter is `emit_done_sentinel`.
2. **`WorkerStatus`/`ResultStatus` are `Literal` type aliases, not enum classes** (models.py:68–69). The task brief and DM-013 row spell `status:enum`; the implementation is a `Literal[...]` validated by `__post_init__` via `typing.get_args(...)`. Functionally an enum-constraint, but not an `enum.Enum`. Task items reproducing the type annotation must use `WorkerStatus`/`ResultStatus` (the Literal aliases), not an Enum.
3. **`LensEntry` has 14 fields, not the 11 named in the brief.** The brief's "load-bearing" list omits `description` (models.py:708), `default_target_line_cap` (715), `acceptance_notes` (719) — all three are present. Full field list models.py:707–720.
4. **`ResultContract` carries 19 top-level fields** (models.py:997–1015), confirmed (the docstring at models.py:894–899 notes the phase-tasklist "18 keys" was an off-by-one; the field-completeness test pins 19).

No other anchor drift detected. All cited line numbers verified by direct Read of the worktree files on 2026-06-20.
