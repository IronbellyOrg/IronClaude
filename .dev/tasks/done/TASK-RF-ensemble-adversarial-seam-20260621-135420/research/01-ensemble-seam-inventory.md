# Research: Ensemble Seam Inventory

- **Topic type:** File Inventory — FR-RH2 adversarial seam surface in `ensemble.py`
- **Scope:** `src/superclaude/cli/reflect/ensemble.py` (whole file, 509 lines)
- **Status:** In Progress
- **Date:** 2026-06-21
- **Repo root:** `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3`

All line anchors below are against `src/superclaude/cli/reflect/ensemble.py` unless
another path is named. File is 509 lines total.

---

## 1. `AdversarialScoreFn` type alias (the seam type to widen)

- **Definition:** line **72**
  ```python
  AdversarialScoreFn = Callable[[list[str], Path], float | None]
  ```
- Sits directly under `TransportFactory = Callable[[int], Transport]` (line 71).
- **Current contract:** takes `(final_paths: list[str], output_dir: Path)` and returns
  `float | None` — i.e. ONLY the convergence score float, NOT a result object.
- **This is the alias FR-RH2.7 must widen** to return a result object (or a
  `Tuple`/dataclass carrying `deviation_count_by_class`, `regression_present`,
  `unauthorized_deviation_present`, `needs_human_decision`, `report_path`, plus the
  score). Widening this changes the seam's public callable shape — see §8 backward-compat.

---

## 2. `run_tier2_ensemble` — signature + seam invocation block

- **Signature:** lines **136–145**
  ```python
  def run_tier2_ensemble(
      config: ReflectConfig,
      *,
      prompt: str = "",
      transport_for_slot: TransportFactory | None = None,
      adversarial_convergence_score: float | None = None,    # 141
      adversarial_score_fn: AdversarialScoreFn | None = None, # 142
      adversarial_unavailable: bool = False,                  # 143
      env: Mapping[str, str] | None = None,
  ) -> dict[str, Any] | None:
  ```
  Returns the exact top-level reflect contract dict (or `None` when M==0).

- **Seam invocation block:** lines **221–232**
  ```python
  if adversarial_convergence_score is None and len(succeeded_final_paths) >= 2:   # 221
      if adversarial_score_fn is None:                                            # 222
          adversarial_convergence_score = run_adversarial_scorer(                 # 223
              succeeded_final_paths,
              output_dir / ADVERSARIAL_SUBRUN_DIR,                                # 225
              config=config,
          )
      else:
          adversarial_convergence_score = adversarial_score_fn(                   # 229
              succeeded_final_paths,
              output_dir / ADVERSARIAL_SUBRUN_DIR,                                # 231
          )
  ```
  Gate: runs the scorer only when no score was pre-supplied AND >=2 reviewers
  succeeded. **Both branches assign ONLY a float** to
  `adversarial_convergence_score`; the deviation/regression fields are never
  captured here. This is the core wiring gap.

- **What is passed to `build_reflect_contract`:** lines **234–239**
  ```python
  contract = build_reflect_contract(
      normalized_workers,                                          # 235 (positional)
      swarm_merged_path=swarm_contract.merged_path,                # 236
      adversarial_convergence_score=adversarial_convergence_score, # 237
      adversarial_unavailable=adversarial_unavailable,             # 238
  )
  ```
  Only `swarm_merged_path`, the score float, and `adversarial_unavailable` flow
  in. No deviation counts, no regression flag, no adversarial report path.
  **FR-RH2.7 target: extend this call to forward the parsed result-object fields.**
- `_emit_reflect_contract(config.contract_path, contract)` writes it (line 240);
  the dict is also returned (line 241).
- `succeeded_final_paths` (the seam input) is built at lines **189–193** from
  `normalized_workers` where `status == "success" and final_path`.

---

## 3. `run_adversarial_scorer` (default scorer) + parse chain

- **Signature:** lines **244–249**
  ```python
  def run_adversarial_scorer(
      final_paths: list[str],
      output_dir: Path,
      *,
      config: ReflectConfig,
  ) -> float | None:
  ```
  Return type `float | None` — **same narrow shape as the seam alias**, so it
  must widen in lockstep with `AdversarialScoreFn`.

- **What it launches:** builds the Mode-A prompt via `build_adversarial_prompt`
  (line 258), runs a `ClaudeProcess` (lines 259–267) with
  `output_file=output_dir/"adversarial-stdout.json"`,
  `error_file=output_dir/"adversarial-stderr.log"`, `output_format="stream-json"`,
  model/timeout/max_turns from `config`. `proc.start()` then `proc.wait()`; on
  non-zero rc returns `None` (lines 268–270).

- **What it parses/returns:** line **271**
  ```python
  return extract_convergence_score(parse_adversarial_contract(output_dir))
  ```
  So the parse chain is `parse_adversarial_contract(output_dir)` ->
  `extract_convergence_score(...)`. **Only the score is extracted; the rest of the
  adversarial return-contract dict is discarded** at this seam. FR-RH2.7 must
  capture the full parsed dict here (or return it) and map its deviation/regression
  fields.

- **NOTE on naming:** the user's brief references a `_parse_convergence_score`
  helper. **No such symbol exists.** The actual helpers are
  `parse_adversarial_contract` (274) and `extract_convergence_score` (336) — see
  §3a/§3b. (Verified via full-file read + grep; `_parse_convergence_score` returns
  no matches.)

### 3a. `parse_adversarial_contract` (lines 274–289)
- `def parse_adversarial_contract(output_dir: Path) -> dict[str, Any] | None:`
- Tries `output_dir/"adversarial"/CONTRACT_FILENAME` first, then
  `output_dir/CONTRACT_FILENAME` (lines 282–285); returns first non-None
  `parse_contract(candidate)` (imported from `reflect.contract`, line 37), else
  `None`. **This already returns the FULL parsed dict** — the data needed for
  deviation mapping is available here; it is just thrown away downstream.

### 3b. `extract_convergence_score` (lines 336–357) — the lossy step
- `def extract_convergence_score(contract: dict[str, Any] | None) -> float | None:`
- Unwraps a top-level `return_contract:` key if present (lines 345–347), reads
  `convergence_score` (line 348) falling back to `adversarial_convergence_score`
  (line 350), `float(...)`-coerces, and returns it only if `0.0 <= score <= 1.0`.
  **Discards every other field** of the adversarial contract.

### 3c. `build_adversarial_prompt` (lines 292–301)
- `def build_adversarial_prompt(final_paths: list[str], output_dir: Path) -> str:`
- Emits the literal `/sc:adversarial --compare <paths> --suspect-source <paths>
  --output <output_dir>` Mode-A invocation (lines 296–301). compare/suspect are
  both the joined `final_paths`. (R2 owns the child output schema.)

---

## 4. `build_reflect_contract` — full field-by-field dict (HARD-CODED vs COMPUTED)

- **Signature:** lines **360–366**
  ```python
  def build_reflect_contract(
      workers: list[WorkerResult],
      *,
      swarm_merged_path: str | None = None,
      adversarial_convergence_score: float | None = None,
      adversarial_unavailable: bool = False,
  ) -> dict[str, Any] | None:
  ```
- **Early return:** `succeeded` = workers with `status == "success"` (368);
  `reviewer_count = len(succeeded)` (369); **returns `None` if `reviewer_count == 0`**
  (370–371). This is the M==0 -> `contract-missing` branch.
- Computes locally: `tier_reached` (373: `2 if >=2 else 1`),
  `merge_method` (374: `"adversarial"` if >=2 else `"single-reviewer-fallback"`),
  `report_path = _select_report_path(succeeded, swarm_merged_path)` (375).

**Returned dict (lines 377–407), field-by-field:**

| Field | Line | Source | FR-RH2.7 relevance |
|---|---|---|---|
| `contract_version` | 378 | const `REFLECT_CONTRACT_VERSION` ("1.0", L59) | unchanged |
| `status` | 379 | **HARD-CODED `"success"`** | should reflect regression/halt |
| `mode` | 380 | **HARD-CODED `"post"`** | unchanged |
| `tier_reached` | 381 | COMPUTED (`tier_reached`, L373) | unchanged |
| `reviewer_count` | 382 | COMPUTED (`reviewer_count`) | unchanged |
| `report_path` | 383 | COMPUTED (`_select_report_path`, swarm-merged) | **swarm path only; adversarial report_path NOT included** |
| `audit_log_path` | 384 | **HARD-CODED `None`** | — |
| `deviation_count_by_class` | 385–390 | **HARD-CODED all-zero** `{authorized:0, necessary:0, drift:0, regression:0}` | **MAP TARGET** from adversarial result |
| `t2_model_class_diversity` | 391 | COMPUTED (`compute_model_class_diversity`) | unchanged |
| `t2_vendor_diversity` | 392 | COMPUTED (`compute_vendor_diversity`) | unchanged |
| `adversarial_unavailable` | 393 | param passthrough | unchanged |
| `merge_method` | 394 | COMPUTED (`merge_method`, L374) | unchanged |
| `adversarial_convergence_score` | 395 | param passthrough (float/None) | already wired |
| `verification_ran` | 396 | **HARD-CODED `True`** | — |
| `verification_skip_reason` | 397 | **HARD-CODED `None`** | — |
| `citations_dropped` | 398 | **HARD-CODED `0`** | — |
| `citations_dropped_extrapolated` | 399 | **HARD-CODED `0`** | — |
| `input_drift_detected` | 400 | **HARD-CODED `False`** | — |
| `regression_present` | 401 | **HARD-CODED `False`** | **MAP TARGET** |
| `unauthorized_deviation_present` | 402 | **HARD-CODED `False`** | **MAP TARGET** |
| `needs_human_decision` | 403 | **HARD-CODED `False`** | **MAP TARGET** |
| `user_decision_required` | 404 | **HARD-CODED `False`** | **MAP TARGET** (mirror of needs_human_decision) |
| `serena_summary_corroboration` | 405 | **HARD-CODED `"unavailable"`** | — |
| `degraded_components` | 406 | **HARD-CODED `[]`** | — |

**Summary:** the five fields the track must drive from the adversarial result
(`deviation_count_by_class`, `regression_present`, `unauthorized_deviation_present`,
`needs_human_decision`, `user_decision_required`) are ALL hard-coded clean
literals today, plus `report_path` carries only the swarm-merged path and never
the adversarial report path. `status` is also a hard-coded `"success"`.

---

## 5. `_select_report_path` (lines 488–497)

```python
def _select_report_path(
    succeeded: list[WorkerResult],
    swarm_merged_path: str | None,
) -> str | None:
    if swarm_merged_path:               # 492
        return swarm_merged_path        # 493
    for worker in succeeded:            # 494
        if worker.final_path:           # 495
            return worker.final_path    # 496
    return None                         # 497
```
- **Current behavior:** returns `swarm_merged_path` when truthy, else the first
  succeeded worker's `final_path`, else `None`. **Never considers an adversarial
  report path.** If FR-RH2.7 wants `report_path` to point at the adversarial
  report, this function (or the `report_path` assignment at L383) is the place to
  thread an `adversarial_report_path` argument.

---

## 6. `ADVERSARIAL_SUBRUN_DIR` constant + child output dir construction

- **Constant:** line **67** — `ADVERSARIAL_SUBRUN_DIR = "t2-adversarial"`
  (sibling to `SWARM_SUBRUN_DIR = "t2-swarm"`, L66).
- **Child output dir constructed** as `output_dir / ADVERSARIAL_SUBRUN_DIR` at the
  seam call sites: line **225** (default `run_adversarial_scorer` branch) and line
  **231** (`adversarial_score_fn` seam branch). `output_dir = Path(config.output_dir)`
  (L160). Inside `run_adversarial_scorer`, `output_dir.mkdir(...)` (L257) creates it;
  `parse_adversarial_contract` then looks for `<dir>/adversarial/return-contract.yaml`
  or `<dir>/return-contract.yaml` (L283–284). So the adversarial child contract
  the result-object would be parsed from lives under
  `config.output_dir/t2-adversarial/[adversarial/]return-contract.yaml`.
- `CONTRACT_FILENAME = "return-contract.yaml"` (L68).

---

## 7. Existing callers/tests passing `adversarial_score_fn` (R4 owns tests)

Grep over `src/` + `tests/`:
- **Production seam declarations/uses** (in `ensemble.py`): L72 (alias), L142
  (param), L222 / L229 (branch). No production caller in `runner.py` passes
  `adversarial_score_fn` — `runner.py:425` calls `run_tier2_ensemble(config)` with
  positional config only (no kwargs), so the default scorer path is taken in prod.
- **Tests passing `adversarial_score_fn`** (R4's domain, listed for completeness):
  - `tests/cli/reflect/test_ensemble_stub_integration.py:93` —
    `adversarial_score_fn=_const_score`
  - `tests/cli/reflect/test_ensemble_stub_integration.py:331` —
    `adversarial_score_fn=_const_score`
  - `tests/cli/reflect/test_ensemble_stub_integration.py:356` —
    `adversarial_score_fn=_const_score`
  - Module docstring at `test_ensemble_stub_integration.py:16` references "the
    production `adversarial_score_fn` seam".
  - `_const_score` is the stub callable matching the CURRENT `(list[str], Path) ->
    float|None` shape; widening the alias means these stubs' return type changes.
- **`build_reflect_contract` direct test:** `tests/cli/reflect/test_ensemble_unit.py:170`
  calls `build_reflect_contract(workers, adversarial_convergence_score=0.86)`.

---

## 8. Backward-compat surface — every call site whose signature changes if `AdversarialScoreFn` is widened

If `AdversarialScoreFn` (L72) is widened to return a result object instead of
`float | None`, these surfaces must change in lockstep:

1. **`AdversarialScoreFn` alias itself** — L72. The return type changes.
2. **`run_tier2_ensemble` seam branch** — L229–232: `adversarial_score_fn(...)`
   currently assigned to `adversarial_convergence_score` (a float var). Must
   destructure/store the result object instead.
3. **`run_adversarial_scorer`** — L244–249 signature returns `float | None`; L223
   default branch assigns its return to `adversarial_convergence_score`. Must
   widen its return to the same result-object shape so BOTH branches are uniform.
4. **`run_adversarial_scorer` body** — L271 currently returns only
   `extract_convergence_score(parse_adversarial_contract(...))`; must instead
   return the result object built from the full `parse_adversarial_contract` dict.
5. **`build_reflect_contract` call** — L234–239: must gain new kwargs
   (deviation counts, regression flag, unauthorized flag, human-decision flag,
   adversarial report path) and `build_reflect_contract` (L360) signature/body
   must accept + emit them (replacing the L385–406 hard-coded literals).
6. **Test stubs** in `test_ensemble_stub_integration.py` (L93/331/356) and their
   `_const_score` helper — return shape must match the widened alias. **(R4 owns.)**

No other module imports `AdversarialScoreFn` (grep: only `ensemble.py` references
it). `run_tier2_ensemble` is imported only by `runner.py:35` and called at
`runner.py:425` WITHOUT the score-fn kwarg, so the production entrypoint is
unaffected by widening the *optional* seam param — only the seam's own internal
plumbing + tests change.

---

## Status: Complete

### Summary of key findings
- The seam alias to widen is **`AdversarialScoreFn` at L72** (`Callable[[list[str],
  Path], float | None]`). Its sibling default scorer **`run_adversarial_scorer`
  (L244)** returns the same narrow `float | None` and must widen in lockstep.
- The lossy point is **L271 / `extract_convergence_score` (L336)**: the full
  adversarial contract IS available via `parse_adversarial_contract` (L274, returns
  the whole dict) but only `convergence_score` is extracted. FR-RH2.7 should map the
  remaining fields from that already-parsed dict.
- **`build_reflect_contract` (L360)** hard-codes the five track-target fields:
  `deviation_count_by_class` (L385–390, all zero), `regression_present` (L401,
  False), `unauthorized_deviation_present` (L402, False), `needs_human_decision`
  (L403, False), `user_decision_required` (L404, False) — plus `status` (L379,
  "success"). `report_path` (L383) carries only the swarm-merged path via
  `_select_report_path` (L488), never an adversarial report path.
- The seam call site that forwards to the contract builder is **L234–239** (passes
  only swarm path + score float + unavailable bool).
- The user's brief named a `_parse_convergence_score` helper — **it does not exist**;
  the real helpers are `parse_adversarial_contract` (L274) and
  `extract_convergence_score` (L336).
- `ADVERSARIAL_SUBRUN_DIR = "t2-adversarial"` (L67); child contract parsed from
  `config.output_dir/t2-adversarial/[adversarial/]return-contract.yaml`.
- Backward-compat: only `ensemble.py` internals + the 3 stub-test call sites
  (L93/331/356) change. `runner.py:425` calls `run_tier2_ensemble(config)` with no
  score-fn kwarg, so production is insulated. R4 owns the test changes.
