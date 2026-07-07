# Research: reflect seam inventory

Status: Complete
Date: 2026-07-06
Scope: `src/superclaude/cli/reflect/{ensemble.py, contract.py, models.py, commands.py}`
Driving design: `.dev/brainstorms/20260706-035624-reflect-t2-fallback-ladder/design.md`

All line numbers below are the ACTUAL current lines (files were re-Read this turn).
Where the design cited a different line, the delta is called out. Repo root:
`/config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback`.

---

## 0. Line-number reconciliation vs design.md (quick delta table)

| Symbol / seam | design.md cite | ACTUAL current | delta |
|---|---|---|---|
| `run_tier2_ensemble` def | ensemble.py:171 | ensemble.py:171 | exact |
| insertion seam | between L225 and L226 | between L225 and L226 | exact |
| `_stamp_worker_paths` call | ensemble.py:216 | ensemble.py:216 | exact |
| `normalize_wave2` call | ensemble.py:217 (ends L225) | ensemble.py:217–225 | exact |
| `succeeded_final_paths` comprehension | ensemble.py:226 | ensemble.py:226–230 | exact |
| `build_reflect_contract` call site | ensemble.py:308 | ensemble.py:308–340 | exact |
| `build_reflect_contract` def | ensemble.py:552 | ensemble.py:**553** | +1 |
| `compute_model_class_diversity` call | (in builder) | ensemble.py:615 | — |
| `compute_model_class_diversity` def | ensemble.py:641 | ensemble.py:641 | exact |
| `compute_vendor_diversity` def | ensemble.py:651 | ensemble.py:651 | exact |
| `_degraded_reason` def/body | contract.py:265–293 | def **256**; body 265–351 | def is 256 |
| T6 `degraded-tier1` trigger | (T6) | contract.py:271–272 | — |
| T10 `single-reviewer-fallback` | (T10) | contract.py:288–289 | — |
| `_LOAD_BEARING_BOOL_FIELDS` | contract.py:206 (usage) | def 48–58; used 206–215 | — |
| `ReflectConfig` | models.py:57 | models.py:**58** (`@dataclass` L57) | +1 |
| reflect CLI `run` options | — | commands.py:216–319 | — |

Net: files are essentially where the design says. Only `build_reflect_contract`
def (+1), `_degraded_reason` def (256 not 265), and `ReflectConfig` (class body
starts L58) drift by ±1 line.

---

## 1. ensemble.py — `run_tier2_ensemble` + the insertion seam

### Signature — `ensemble.py:171–180`
```python
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
```
- `TransportFactory = Callable[[int], Transport]` (ensemble.py:106) — positional
  `slot_index` keyed; this is the naive-seam type the design's F1 slot-NAME
  factory must NOT reuse for fallback escalation.
- Body preamble (L194–209): resolves `reviewers`, `output_dir`, `swarm_output_dir`
  (= `output_dir / "t2-swarm"`, const `SWARM_SUBRUN_DIR` L67), builds `preflight`
  (L200), resolves `factory` (L201–205), builds `worker_prompt` (L206), builds
  `worker_spec = WorkerSpec(count=reviewers, models=[], timeout_sec=config.timeout_seconds)`
  (L207–209). Design §7.4 wants the run-level `deadline` captured here, before
  `dispatch_wave1`.

### Primary dispatch → stamp → normalize (the seam context)
```
ensemble.py:210–215   worker_results   = dispatch_wave1(preflight, transport_for_slot=factory,
                                                        prompt=worker_prompt, worker_spec=worker_spec)
ensemble.py:216       stamped_workers  = _stamp_worker_paths(worker_results, swarm_output_dir)
ensemble.py:217–225   normalized_workers = normalize_wave2(stamped_workers, REFLECT_REVIEW_RECIPE,
                                                          recipe_args={...})
──────────────────────────────────────────────────────────────  ◄── INSERT CONTROLLER (between 225 and 226)
ensemble.py:226–230   succeeded_final_paths = [worker.final_path for worker in normalized_workers
                                              if worker.status == "success" and worker.final_path]
```

- **`normalize_wave2` call: `ensemble.py:217–225`** — result assigned to
  `normalized_workers`. Args: `stamped_workers`, `REFLECT_REVIEW_RECIPE`
  (="passthrough", const L66), `recipe_args={"target","target_checksum","caller_label"}`.
- **`succeeded_final_paths` comprehension: `ensemble.py:226–230`** — filters
  `normalized_workers` on `status == "success" and worker.final_path`.
- **The F2/F1 controller insertion seam is between L225 and L226** exactly as the
  design states: after `normalized_workers` is finalized, before anything reads it.
- Note the primary order is **stamp (L216) BEFORE normalize (L217)** — design §4.3
  requires the per-fallback-attempt flow mirror this same stamp→normalize order.
- Everything below L226 consumes `normalized_workers`: `reduce_wave3` (L239–254),
  the adversarial gate (`len(succeeded_final_paths) >= 2`, L259), and
  `build_reflect_contract` (L308). So appending fallback successes to
  `normalized_workers` at the seam flows through all three unchanged.

### `build_reflect_contract` CALL SITE — `ensemble.py:308–340`
Current kwargs passed at the call (this is where the new `t2_fallback=` kwarg slots in):
```python
contract = build_reflect_contract(
    normalized_workers,                       # positional (L309)
    swarm_merged_path=swarm_contract.merged_path,           # L310
    swarm_status=getattr(swarm_contract.status, "value", swarm_contract.status),  # L316
    adversarial_status=adversarial_status,                  # L317
    adversarial_convergence_score=adversarial_convergence_score,  # L318
    adversarial_unavailable=adversarial_unavailable,        # L319
    regression_present=regression_present,                  # L320
    unauthorized_deviation_present=unauthorized_deviation_present,  # L321
    needs_human_decision=needs_human_decision,             # L322
    deviation_count_by_class=deviation_count_by_class,     # L323
    adversarial_report_path=adversarial_report_path,       # L324
    reviewer_isolation=("snapshot-children-only" if config.reviewer_grounding_root else "disabled"),  # L331–333
    audit_tree_dirty=config.audit_tree_dirty,             # L334
    reviewer_grounding_root=(str(config.reviewer_grounding_root) if config.reviewer_grounding_root else None),  # L335–339
)
```
`_emit_reflect_contract(config.contract_path, contract)` then writes it (L341);
`return contract` (L342).

---

## 2. ensemble.py — `build_reflect_contract` DEFINITION (lives HERE, not contract.py)

### Full signature (all defaulted keyword-only) — `ensemble.py:553–569`
```python
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
) -> dict[str, Any] | None:
```
The new additive `t2_fallback: dict | None = None` keyword-only param appends
here (mirrors how `reviewer_isolation`/`audit_tree_dirty` were threaded — all
defaulted so every existing call site + test stays valid).

### Body derivations (all recompute over the augmented worker list)
- `succeeded = [w for w in workers if w.status == "success"]` — **L579**
- `reviewer_count = len(succeeded)` — **L580**; early `return None` if 0 (L581–582)
- `tier_reached = 2 if reviewer_count >= 2 else 1` — **L584**
- `merge_method = "adversarial" if reviewer_count >= 2 else "single-reviewer-fallback"` — **L585**
  (this is the T10 field the design references — it is SET here, gated in contract.py)
- `report_path = _select_report_path(...)` — L586–590
- `deviation_count_by_class` default backfill — L591–597

### Returned dict keys (in emit order) — `ensemble.py:599–638`
`contract_version` (L600), `status`="success" (L601), `subrun_status` (L603),
`adversarial_subrun_status` (L605), `subrun_status_partial` (L607), `mode`="post"
(L609), `tier_reached` (L610), `reviewer_count` (L611), `report_path` (L612),
`audit_log_path` (L613), `deviation_count_by_class` (L614),
**`t2_model_class_diversity`: `compute_model_class_diversity(succeeded)` — L615**,
**`t2_vendor_diversity`: `compute_vendor_diversity(succeeded)` — L616**,
`adversarial_unavailable` (L617), `merge_method` (L618),
`adversarial_convergence_score` (L619), `verification_ran`=False (L620),
`verification_skip_reason`="no-verification-stage" (L621), `citations_dropped`=0
(L622), `citations_dropped_extrapolated`=0 (L623), `input_drift_detected`=False
(L624), `regression_present` (L625), `unauthorized_deviation_present` (L626),
`needs_human_decision` (L627), `user_decision_required`=False (L628),
`serena_summary_corroboration`="unavailable" (L629), `degraded_components`=[]
(L630), `reviewer_isolation` (L635), `audit_tree_dirty` (L636),
`reviewer_grounding_root` (L637).

- **`compute_model_class_diversity` is called at L615; `compute_vendor_diversity`
  at L616**, both over `succeeded` (the success-filtered augmented set).
- **Confirmed: `build_reflect_contract` is DEFINED in ensemble.py (L553), NOT in
  contract.py.** contract.py has no `build_reflect_contract`.
- A new top-level `t2_fallback:` key would be appended to this dict (design §6).

---

## 3. ensemble.py — the two diversity helpers fallback.py will reuse (circular-import note)

### `compute_model_class_diversity` — `ensemble.py:641–648`
```python
def compute_model_class_diversity(workers: list[WorkerResult]) -> str:
    distinct_model_ids = {
        worker.model_id
        for worker in workers
        if worker.status == "success" and worker.model_id
    }
    return "full" if len(distinct_model_ids) >= 2 else "insufficient"
```
Returns `"full"` (>=2 distinct model_ids) else `"insufficient"`.

### `compute_vendor_diversity` — `ensemble.py:651–669`
```python
def compute_vendor_diversity(workers: list[WorkerResult]) -> str | None:
    succeeded = [worker for worker in workers if worker.status == "success"]
    if len(succeeded) < 2:
        return None
    vendors = {
        _vendor_from_model_id(worker.model_id)
        for worker in succeeded
        if worker.model_id
    }
    return "multi" if len(vendors) >= 2 else "single"
```
Returns `None` (<2 successes), `"multi"` (>=2 vendors), else `"single"`.

### `_vendor_from_model_id` — `ensemble.py:672–688` (helper both reuse)
Maps model_id substrings to vendor family (qwen/deepseek/openai/google/meta/
mistral/anthropic), else leading path/colon segment fallback. `evaluate_quorum`
in fallback.py depends transitively on this too.

**Circular-import note (design §10):** these three helpers live in `ensemble.py`,
and `ensemble.py` would `import run_fallback_ladder` from `fallback.py`, while
`fallback.py` reuses these helpers → a top-level `ensemble → fallback → ensemble`
cycle. Design's preferred fix: extract the 3 helpers into a neutral
`reflect/_diversity.py` imported by both (option a), or function-local import in
`evaluate_quorum` (option b). Note `_vendor_from_model_id` (private) must move
WITH the two public helpers if option (a) is chosen, since both call it.

---

## 4. contract.py — `_degraded_reason` first-match order + `_LOAD_BEARING_BOOL_FIELDS`

### `_degraded_reason` — def `contract.py:256`, body `contract.py:265–351`
First-match-wins; returns the FIRST trigger slug in this fixed order (design's
honesty guarantee rests on T6 preceding T10):

| Order | Slug | Lines | Predicate |
|---|---|---|---|
| T1–5 | `degraded-components` | 267–268 | any token in `_DEGRADED_COMPONENTS_HALT_SET` |
| **T6** | **`degraded-tier1`** | **271–272** | `expected_tier >= 2 and tier_reached == 1` |
| T7 | `degraded-model-diversity` | 275–277 | `mcd is not None and mcd != "full"` |
| T8 | `single-vendor` | 280–281 | `t2_vendor_diversity == "single" and not allow_single_vendor` |
| T9 | `adversarial-unavailable` | 284–285 | `adversarial_unavailable is True` |
| **T10** | **`single-reviewer-fallback`** | **288–289** | `merge_method == "single-reviewer-fallback"` |
| T11 | `null-convergence` | 292–293 | `tier_reached == 2 and score is None` |
| T11a | `degraded-subrun-partial` | 299–300 | `adversarial_subrun_status in ("partial","failed")` |
| T11b | `low-convergence` | 310–319 | present score non-finite or `< 0.80` |
| T12 | `verification-skipped` | 322–338 | `verification_ran is False` (exemptions apply) |
| T13 | `citations-dropped` | 341–345 | `citations_dropped > 0` |
| T14 | `input-drift` | 348–349 | `input_drift_detected is True` |
| — | `None` | 351 | no trigger |

**CONFIRMED: T6 `degraded-tier1` (L271–272) fires BEFORE T10
`single-reviewer-fallback` (L288–289).** So for the "<2 successes" degrade shape,
the returned verdict reason is `degraded-tier1`; `merge_method ==
"single-reviewer-fallback"` is present only as a contract FIELD, never the verdict
slug in that shape (design §6 / §8 counter-case). Tests must assert
`degraded-tier1` as the reason, MAY assert `merge_method` as a field, MUST NOT
assert both as the verdict reason.

### `_LOAD_BEARING_BOOL_FIELDS` — `contract.py:48–58`
```python
_LOAD_BEARING_BOOL_FIELDS = frozenset(
    {
        "regression_present",
        "unauthorized_deviation_present",
        "needs_human_decision",
        "user_decision_required",
        "adversarial_unavailable",
        "input_drift_detected",
        "verification_ran",
    }
)
```
Used at `contract.py:206–215` (the malformed-boolean → BLOCKED guard).
**CONFIRMED: neither `merge_method`, `t2_model_class_diversity`,
`t2_vendor_diversity`, nor any `t2_fallback` field is a member** — so the design's
"no `_LOAD_BEARING_BOOL_FIELDS` member added" additive-only guarantee holds; the
new `t2_fallback:` block cannot trip the malformed-boolean gate. contract.py is
UNCHANGED by this work.

---

## 5. models.py — `ReflectConfig` last defaulted field + field-ordering comment

`@dataclass` at `models.py:57`; `class ReflectConfig` body `models.py:58–114`.

### Non-default fields (positional) — `models.py:66–86`
`tasklist_path, base, head, spec_path, depth, executor_model, output_dir, model,
timeout_seconds, max_turns, promote, allow_single_vendor, tmux, dry_run,
print_command, resume` (L66–81), then the **field-ordering comment L82–83**:
```python
# Auto-fix evolution (D1/D3/D6): appended AFTER all existing non-default
# fields to respect the dataclass field-ordering rule.
```
followed by `base_override, fix, max_fix_iterations` (L84–86, still non-default).

### Defaulted fields — `models.py:90–109`
`transport="openai_compat"` (L90), `reviewers=3` (L93),
`isolate_reviewers=False` (L100), `audit_tree_dirty=False` (L101),
`reviewer_grounding_root: Path | None = None` (L107),
**`reachability: bool = True` (L109) — THIS IS THE CURRENT LAST DEFAULTED FIELD.**

The 3 new defaulted fields (design §7.2) append **after L109, before the
`contract_path` property at L111–114**:
```python
tier2_fallback_enabled: bool = True
tier2_fallback_ladder: tuple[str, ...] = ("T1Model01", "T1Model02")
tier2_fallback_max_attempts: int = 2
```
`@property contract_path` is at L111–114 — insert the new fields BEFORE the first
`@property` (a method), i.e. immediately after L109. The ordering-rule comment at
L82–83 is the convention to cite for "append defaults at the end."

Note: `resolve_config` (in `config.py`, not in scope here) constructs
`ReflectConfig` and is invoked from commands.py:351 — the new fields will need
threading there too (out of this file's scope; flagged for the config researcher /
task builder).

---

## 6. commands.py — reflect CLI flag wiring (where `--no-tier2-fallback` slots)

The `run` subcommand is the target: `@reflect_group.command()` at
`commands.py:216`, decorated options `commands.py:217–319`, `def run(...)` at
`commands.py:320–338`.

### Existing options (decorator order) — `commands.py:221–319`
| Flag | Lines | dest / type |
|---|---|---|
| `--tmux` | 221–223 | `tmux` flag |
| `--print-command` | 224–228 | `print_command` flag |
| `--promote/--no-promote` | 229–234 | `promote` default True |
| `--reachability/--no-reachability` | 235–240 | `reachability` default True |
| `--timeout` | 241–246 | int, default None |
| `--depth` | 247–252 | Choice standard/deep |
| `--transport` | 257–262 | Choice openai_compat/stub |
| `--reviewers` | 263–268 | int default 3 |
| `--output` | 269–273 | default None |
| `--allow-single-vendor` | 274–278 | flag |
| `--dry-run` | 279–283 | flag |
| `--resume` | 284–288 | flag |
| `--fix/--no-fix` | 289–294 | `fix` default False |
| `--max-fix-iterations` | 295–300 | int default 2 |
| `--base` | 301–309 | `base_override` default None |
| `--isolate-reviewers/--no-isolate-reviewers` | 310–319 | `isolate_reviewers` default False |

### Where `--no-tier2-fallback` slots in (3 edit points in this file)
The `--reachability/--no-reachability` pair (L235–240) is the closest precedent
for a `--foo/--no-foo` default-True boolean. A new
`--tier2-fallback/--no-tier2-fallback` option (dest `tier2_fallback`, default
True) needs:
1. **New `@click.option` decorator** in the L221–319 block (e.g. after
   `--isolate-reviewers` at L319, before `def run`).
2. **New param in `def run(...)` signature** — current signature params
   `commands.py:320–338` end with `isolate_reviewers: bool` (L336) and
   `reachability: bool` (L337); add `tier2_fallback: bool` here.
3. **Forward to `resolve_config(...)`** — the call is `commands.py:351–370`;
   current kwargs end with `isolate_reviewers=isolate_reviewers` (L368),
   `reachability=reachability` (L369). Add `tier2_fallback=tier2_fallback`.
   (resolve_config lives in `config.py` — out of scope here — and must map it to
   `ReflectConfig.tier2_fallback_enabled`.)

### tmux inner-reinvocation forwarding — `commands.py:459–497`
`_build_inner_command` rebuilds the inner foreground `reflect run` argv. It
explicitly forwards `--promote/--no-promote` (L483), `--no-reachability` when off
(L484–485), `--allow-single-vendor` (L486–487), `--isolate-reviewers/
--no-isolate-reviewers` (L488–490), `--resume` (L491–492), `--base` (L495–496).
**A `--no-tier2-fallback` outer call under `--tmux` would silently re-default to
ON in the inner run unless forwarded here** — same footgun the L479–483 promote
comment documents. Add `cmd.append("--tier2-fallback" if config.tier2_fallback_enabled else "--no-tier2-fallback")`
(or emit only the `--no-` form when disabled, mirroring `--no-reachability` at
L484–485). This is a required companion edit, not optional.

Design §7.2 also notes: `--transport stub` should default fallback OFF (stub pool
already certifies). That default-coupling logic would live in `config.py`
`resolve_config` (out of scope here), not in the Click layer.

---

## Summary

All four in-scope files were re-Read this turn; line numbers are current. Key groundings:

1. **Seam is exact**: controller inserts between `ensemble.py:225` (end of
   `normalize_wave2` → `normalized_workers`) and `ensemble.py:226` (start of
   `succeeded_final_paths`). Primary order stamp(216)→normalize(217) is the
   pattern fallback per-attempt flow must mirror.
2. **`build_reflect_contract` is in ensemble.py** (def L553, call L308–340), NOT
   contract.py. New `t2_fallback=` kwarg appends to signature L553–569; new
   `t2_fallback:` dict key appends to the returned dict L599–638. Diversity
   helpers called at L615/L616.
3. **Diversity helpers to reuse**: `compute_model_class_diversity`
   (L641–648), `compute_vendor_diversity` (L651–669), plus private
   `_vendor_from_model_id` (L672–688) — circular-import risk if fallback.py
   imports from ensemble.py; extract to `reflect/_diversity.py` (helper + its
   private dependency together).
4. **contract.py UNCHANGED**: `_degraded_reason` (def L256) confirms T6
   `degraded-tier1` (L271–272) fires before T10 `single-reviewer-fallback`
   (L288–289). `_LOAD_BEARING_BOOL_FIELDS` (L48–58) contains 7 fields, none of
   which are the diversity/merge_method/t2_fallback fields → additive-only holds.
5. **models.py**: last defaulted field is `reachability: bool = True` (L109); 3
   new `tier2_fallback_*` fields append after L109, before the `contract_path`
   property (L111). Field-ordering comment at L82–83.
6. **commands.py**: `run` options block L221–319; `--no-tier2-fallback` needs
   THREE edits in this file — decorator (near L319), `def run` param (near
   L336–337), `resolve_config` forward (near L368–369) — PLUS tmux
   `_build_inner_command` forwarding (L459–497, near L484) or the flag silently
   resets ON in the inner run. `resolve_config`/`config.py` threading is out of
   this file's scope (flagged for the config/task builder).

Unverified: none — every claim above cites a re-Read line in one of the four
in-scope files. (Cross-file threading through `config.py`/`resolve_config` and
`swarm/*` is out of scope per the researcher split and only flagged, not
line-grounded here.)
