# Anchor Verification

Status: Complete

Verified: 2026-07-06 13:45 UTC

## Reflect Anchors

| File | Symbol / seam | Current line(s) | Verdict | Notes |
|---|---:|---:|---|---|
| `src/superclaude/cli/reflect/ensemble.py` | `run_tier2_ensemble` | 171 | CONFIRMED | Function signature present. |
| `src/superclaude/cli/reflect/ensemble.py` | controller insertion seam after `normalize_wave2` and before `succeeded_final_paths` | 217-226 | CONFIRMED | `normalized_workers = normalize_wave2(...)` ends before `succeeded_final_paths`. |
| `src/superclaude/cli/reflect/ensemble.py` | `build_reflect_contract` | 553-638 | CONFIRMED | Contract builder defined in `ensemble.py`; current return dict ends at line 638. |
| `src/superclaude/cli/reflect/ensemble.py` | `compute_model_class_diversity` | 641-648 | CONFIRMED | Helper still lives in `ensemble.py`. |
| `src/superclaude/cli/reflect/ensemble.py` | `compute_vendor_diversity` | 651-669 | CONFIRMED | Helper still lives in `ensemble.py`. |
| `src/superclaude/cli/reflect/ensemble.py` | `_vendor_from_model_id` | 672-688 | CONFIRMED | Private helper still lives in `ensemble.py`. |
| `src/superclaude/cli/reflect/models.py` | `ReflectConfig.reachability` | 109 | CONFIRMED | Last defaulted field is `reachability: bool = True`. |
| `src/superclaude/cli/reflect/models.py` | `ReflectConfig.contract_path` | 111-114 | CONFIRMED | Property returns `self.output_dir / "return-contract.yaml"`. |
| `src/superclaude/cli/reflect/contract.py` | `_LOAD_BEARING_BOOL_FIELDS` | 48-58 | CONFIRMED | No fallback-related member exists. |
| `src/superclaude/cli/reflect/contract.py` | `_degraded_reason` | 256-299 | CONFIRMED | T6 `degraded-tier1` lines 270-272 precedes T10 `single-reviewer-fallback` lines 287-289. |
| `src/superclaude/cli/reflect/config.py` | `resolve_config` | 238-383 | CONFIRMED | Transport/reviewer resolution remains inside this function. |
| `src/superclaude/cli/reflect/commands.py` | `run` option block | 216-319 | CONFIRMED | Click run options present; function body starts at line 320. |
| `src/superclaude/cli/reflect/commands.py` | `_build_inner_command` | 459-497 | CONFIRMED | Inner tmux reinvocation builder present. |

## Swarm Anchors

| File | Symbol / seam | Current line(s) | Verdict | Notes |
|---|---:|---:|---|---|
| `src/superclaude/cli/swarm/config.py` | T2 proxy/model constants | 51-63 | CONFIRMED | `T2ProxyUrl`, `T2ProxyKey`, `T2Model0`, max slots 9. |
| `src/superclaude/cli/swarm/config.py` | `SwarmConfig._collect_t2_models` | 178-185 | CONFIRMED | Collector still T2-specific. |
| `src/superclaude/cli/swarm/transports/openai_compat.py` | `read_env` | 159-202 | CONFIRMED | Reads T2 env names directly. |
| `src/superclaude/cli/swarm/commands.py` | `_resolve_run_transport_factory` | 612-707 | CONFIRMED | Factory still resolves `openai_compat` via `read_env` and positional `pool[slot_index % len(pool)]`. |
| `src/superclaude/cli/swarm/dispatch.py` | `dispatch_wave1` slot factory call loop | 444-472 | CONFIRMED | Per-slot callable passes numeric `slot_index` to `transport_for_slot`. |

## Summary

Every Step 1.3 anchor was found in the current worktree. No structural drift blocker was identified.
