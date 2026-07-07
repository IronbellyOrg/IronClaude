# Reflect pre-execution report — Reflect Tier-2 Fallback Model Ladder

Mode: `pre`  
Target: `/config/workspace/IronClaude/.dev/worktrees/ReflectModelFallback/.dev/brainstorms/20260706-035624-reflect-t2-fallback-ladder/design.md`  
Status: `partial`  
Tier reached: `2`  
Calibrated confidence: `0.74`

## Verdict

The design is directionally correct and captures the core fallback-ladder architecture, but it is **not ready for implementation without revision**. The review found several implementation-readiness gaps, including three high-severity code-grounding issues and two explicit decisions that should be resolved before `/sc:implement`.

## Coverage summary

- Estimated requirements coverage: **88%**
- Acceptance criteria coverage: **10/12 fully covered**, **2/12 partially covered**
- Main partial areas:
  - fallback wall-clock policy
  - same per-attempt retry/timeout behavior for fallback attempts
  - metadata schema alignment with the source requirement

The source acceptance criteria require fallback attempts to be bounded by both attempt count and wall-clock policy (`merged-requirements.md:633-644`), while the design still leaves the wall-clock source as an open implementation detail (`design.md:535-537`).

## Confirmed strengths

1. **Correct insertion point.** The design places fallback after primary dispatch, stamping, and normalization, before final path collection / merge / contract emission (`design.md:53-67`). This preserves the requirement that fallback happens only after retry and salvage complete.
2. **Verdict honesty is mostly preserved.** The design correctly states that fallback metadata should not change verdict semantics; final Tier-2 facts derive from the contributing successful workers (`design.md:340-352`).
3. **Attempt ledger vs contributing set distinction is sound.** The design separates full attempt audit history from the selected contributing reviewer set (`design.md:267-300`).
4. **Source-of-truth discipline is explicit.** The rollout keeps edits under `src/superclaude/` and forbids staging generated `.claude/` mirrors (`design.md:522-523`).

## Findings

### HIGH — F1: Fallback slot dispatch can accidentally reuse `T1Model01` for every attempt

The design says the fallback ladder dispatches one slot per iteration and escalates from `T1Model01` to `T1Model02` (`design.md:220-222`, `design.md:260-262`). Current dispatch passes a local `slot_index` into the transport factory (`dispatch.py:453-459`) and builds one-worker tasks from index `0..workers_requested-1` (`dispatch.py:464-471`). The existing transport resolver maps `slot_index` through `pool[slot_index % len(pool)]` (`commands.py:691-692`).

If fallback dispatch uses `WorkerSpec(count=1)` for both fallback attempts without an explicit slot/name wrapper, both attempts will call the factory with `slot_index == 0`, selecting `T1Model01` twice. That would violate the design’s escalation requirement for `T1Model02`.

**Required design revision:** specify an explicit fallback-slot resolver, e.g. `transport_for_fallback_slot(slot_name: Literal["T1Model01", "T1Model02"])`, or pass a logical slot offset/name into the one-worker dispatch. Add a test proving the second fallback attempt resolves `T1Model02`, not pool index 0 again.

### HIGH — F2: Fallback stamping/output seam is missing from the `run_fallback_ladder` interface

The current Tier-2 path stamps worker paths before normalization (`ensemble.py:216-225`). The design’s impure function signature injects `dispatch` and `normalize`, but no stamping callable or fallback output directory, and its docstring describes `dispatch -> normalize -> stamp` (`design.md:242-257`).

That ordering is inconsistent with the current driver shape and risks producing fallback workers without stable `raw_path` / `meta_path` / `final_path` artifacts before normalization and adversarial/reduce consumption.

**Required design revision:** make fallback attempt flow explicitly `dispatch -> _stamp_worker_paths(fallback_results, swarm_output_dir/<fallback-subdir>) -> normalize_wave2 -> ledger/contributing-set selection`. Add `stamp` and `fallback_output_dir` (or a callback that does both) to the impure function seam.

### HIGH — F3: T1 transport support omits the current OpenAI-compatible env reader

The design adds `T1Model0N` collection to swarm config and parameterizes `_resolve_run_transport_factory` / adds a fallback resolver (`design.md:358-380`, `design.md:397-406`). But the current OpenAI-compatible transport reader imports only T2 env constants (`openai_compat.py:98-103`) and reads only `T2ProxyUrl`, `T2ProxyKey`, and `T2Model0N` slots (`openai_compat.py:159-196`). The module change map includes `swarm/config.py` and `swarm/commands.py`, but omits `swarm/transports/openai_compat.py` (`design.md:475-477`).

If implementation relies on current `read_env`, it cannot read a T1 pool. If it bypasses `read_env`, the design’s claim that existing transport guards are inherited is incomplete.

**Required design revision:** add `src/superclaude/cli/swarm/transports/openai_compat.py` to the change map and specify whether `read_env` becomes prefix-parameterized or a new `read_env_for_pool(...)` helper is introduced. Keep proxy keys out of artifacts.

### MEDIUM — F4: Wall-clock policy is an unresolved design decision, not a coding detail

The acceptance criteria require fallback attempts to be bounded by wall-clock policy (`merged-requirements.md:633-644`). The design’s planner accepts `wall_clock_ok` (`design.md:207-224`) and includes `fallback_wall_clock_exhausted` (`design.md:327-338`), but explicitly defers the concrete budget source (`design.md:535-537`).

The in-process Tier-2 route does not have a surrounding `ClaudeProcess` timeout at the ensemble layer; it runs `run_tier2_ensemble` directly and sets `rc = 0` afterward (`runner.py:508-513` cited by reviewer). Current worker specs carry per-worker timeout only (`ensemble.py:207-215`). Sequential fallbacks can therefore extend wall time unless a remaining-budget mechanism is designed.

**Required design revision:** choose one: (a) derive a run deadline before primary dispatch and pass remaining seconds into the ladder, or (b) add a dedicated fallback time budget. Encode the chosen rule in the interface and tests.

### MEDIUM — F5: The design has a `contract.py` contradiction

The design says `build_reflect_contract` gains a new keyword-only `t2_fallback` parameter and emits a top-level key (`design.md:100-110`, `design.md:304-325`), but its module map says `src/superclaude/cli/reflect/contract.py` has no change (`design.md:474`) and then states `contract.py` should remain untouched (`design.md:480-482`).

Current `build_reflect_contract` is in `src/superclaude/cli/reflect/ensemble.py`, not `contract.py` (`ensemble.py:552-637` from prior symbol read). The design appears to mean “verdict mapping in `contract.py` remains unchanged,” not “no contract emission code changes.”

**Required design revision:** change the module map row to: `src/superclaude/cli/reflect/contract.py — no verdict mapping changes`; keep `build_reflect_contract` changes under `ensemble.py`.

### MEDIUM — F6: Degraded-reason narrative overstates multiple simultaneous verdict reasons

The design says a single surviving reviewer yields both `degraded-tier1` and `single-reviewer-fallback` (`design.md:340-345`, `design.md:440-443`). The current degraded-reason chain is first-match: if expected Tier 2 reaches Tier 1, `_degraded_reason` returns `degraded-tier1` before checking `merge_method == single-reviewer-fallback` (`contract.py:270-289`).

**Required design revision:** say the contract fields may show `merge_method: single-reviewer-fallback`, but the verdict reason slug will be first-match `degraded-tier1` in that case. Tests should not assert both as verdict reasons.

### LOW — F7: Test paths should use the current test namespace

The design proposes `tests/reflect/...` and `tests/swarm/...` (`design.md:450-458`). Existing reflect tests are under `tests/cli/reflect/`. To avoid a parallel test namespace, the rollout should place reflect tests under `tests/cli/reflect/` and swarm tests under the current swarm CLI test namespace.

## Required human/design decisions before implementation

1. **T1 proxy binding.** The design currently leaves same `T2Proxy*` versus new `T1Proxy*` open (`design.md:408-413`, `design.md:529-531`). For this project’s known proxy contract, the safe default is: use the same proxy endpoint/key and read only `T1Model0N` model slots for fallback, unless `~/.aienv` proves a separate T1 proxy contract exists.
2. **Wall-clock source.** Decide whether fallback uses a shared run deadline or a dedicated fallback budget. This should be chosen before coding, not left as an implementation guess.

## Recommended pre-implementation patch to the design

Before `/sc:implement`, update `design.md` to:

1. Add explicit fallback-slot name/offset routing so `T1Model02` is mechanically reachable.
2. Add stamping/output-dir seam to `run_fallback_ladder` and correct the dispatch-normalize-stamp ordering.
3. Add `src/superclaude/cli/swarm/transports/openai_compat.py` to the file change map.
4. Resolve wall-clock policy.
5. Clarify `contract.py` vs `ensemble.build_reflect_contract` responsibilities.
6. Align fallback metadata with source requirements, including `tier2_certification_basis` or an explicit rejection.
7. Use current test paths under `tests/cli/reflect/`.

## Confidence

Calibrated confidence: **0.74**. The core design is sound, but the high-severity implementation seams are concrete enough that this should remain `partial` until the design is revised.
