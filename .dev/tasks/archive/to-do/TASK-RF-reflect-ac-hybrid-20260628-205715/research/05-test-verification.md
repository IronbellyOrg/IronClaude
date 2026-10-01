# Research 05: Test & Verification

Status: Complete

## Scope

- `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/tests/cli/reflect`
- `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/tests/swarm`
- Makefile validation targets
- reflect no-nesting guard

## Existing reflect tests relevant to executor/source/degraded semantics

### Tier-2 ensemble/diversity/degraded behavior

- `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/tests/cli/reflect/test_ensemble_unit.py:162` defines `test_u5_model_class_diversity_uses_succeeded_worker_model_ids`, proving model-class diversity is computed from successful `WorkerResult.model_id` values. It asserts `compute_model_class_diversity(workers) == "full"`, the generated contract has `t2_model_class_diversity == "full"`, and duplicate survivors are not full at lines 175-180.
- `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/tests/cli/reflect/test_ensemble_unit.py:183` defines `test_u6_verdict_map_and_derive_ordering_are_unchanged`, pinning exit codes PASS=0, HALTED=10, DEGRADED=11, BLOCKED=2 at lines 185-188 and the blocked -> degraded -> halted -> pass ordering at lines 190-206. Any A→C degraded/waived semantics must preserve this ordering.
- `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/tests/cli/reflect/test_ensemble_stub_integration.py:141` defines `test_i1_positive_witness_real_fanout`, the positive Tier-2 witness. It asserts real stub fan-out emits `tier_reached == 2`, `merge_method != "single-reviewer-fallback"`, `reviewer_count >= 2`, `t2_model_class_diversity == "full"`, `status == "success"`, and PASS exit 0 at lines 160-171.
- `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/tests/cli/reflect/test_ensemble_stub_integration.py:174` defines `test_i2_negative_witness_one_reviewer_degrades`; it asserts a one-reviewer run degrades/non-passes, falsifies the I1 positive assertion set, has `tier_reached != 2`, `reviewer_count < 2`, and `merge_method == "single-reviewer-fallback"` at lines 185-197.
- `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/tests/cli/reflect/test_ensemble_stub_integration.py:199` defines `test_i3_partial_two_of_three_distinct_pass_eligible`; it proves two successful distinct-class survivors remain PASS-eligible with `reviewer_count == 2`, `t2_model_class_diversity == "full"`, `tier_reached == 2`, PASS exit 0 at lines 216-221.
- `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/tests/cli/reflect/test_ensemble_stub_integration.py:224` defines `test_i4_partial_two_of_three_duplicate_class_degrades`; it deliberately uses duplicate model IDs and asserts `reviewer_count == 2`, `t2_model_class_diversity != "full"`, DEGRADED exit 11, and falsified I1 positives at lines 242-248. This is the closest existing degraded unsatisfiability pattern.
- `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/tests/cli/reflect/test_ensemble_stub_integration.py:251` defines `test_i5_m_one_from_three_single_reviewer_fallback`; it asserts M==1 from N>1 routes to single-reviewer fallback/non-PASS/exit 11 and does not collapse into a Tier-2 PASS at lines 266-277.
- `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/tests/cli/reflect/test_ensemble_stub_integration.py:280` defines `test_i6_m_zero_blocked_exit2`; it asserts M==0 emits no top-level trustworthy contract and routes BLOCKED exit 2, `reason == "contract-missing"` at lines 293-303. A→C unsatisfiable exclusion must avoid this path when there are still enough successful reviewers to form a non-collapsing degraded Tier-2.
- `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/tests/cli/reflect/test_ensemble_stub_integration.py:306` defines `test_i7_return_contract_shape_preserved`; it asserts downstream-consumed fields include `t2_model_class_diversity`, `t2_vendor_diversity`, `merge_method`, `adversarial_convergence_score`, `adversarial_unavailable`, and `degraded_components` at lines 319-333. A→C should extend this shape with any new source/exclusion telemetry fields.
- `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/tests/cli/reflect/test_verdict_mapping.py:22` through line 88 covers clean PASS, HALTED regression, degraded components, tier mismatch, and single-vendor degraded/pass-with-flag. Lines 143-175 are important for A→C because they show the existing pattern for fail-open/unavailable semantics: `serena_summary_corroboration: unavailable` is not degraded at lines 143-151, an exempted verification skip is PASS at lines 154-163, and an unexempted verification skip is DEGRADED at lines 166-175.

### Source/executor reliability coverage gap

- No current test file in `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/tests/cli/reflect` or `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/tests/swarm` contains `source_reliability`, `reliable_source`, `unreliable_source`, `executor_class`, `waive`, or `waived` coverage. Existing diversity tests only reason over model IDs/vendor classes and degraded components, not over executor-class exclusion driven by source reliability.
- Existing A→C test work should therefore be additive and should not replace the current model-class/vender-diversity tests.

### Reflect no-nesting guard / banned tokens

- `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/tests/cli/reflect/test_no_nesting_guard.py:91` defines Layer A: the task-builder wrapper branch must shell out via `superclaude reflect run`, include `--depth deep`, `--fix`, `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE`, and must not contain `_NESTING_TOKENS` at lines 93-103.
- `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/tests/cli/reflect/test_no_nesting_guard.py:106` defines Layer B over both `runner.py` and `ensemble.py`; it requires `ClaudeProcess` and bans `import anthropic`, `from anthropic`, `subagent_type`, `Agent(`, and `Task(` at lines 122-135.
- `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/tests/cli/reflect/test_no_nesting_guard.py:179` asserts `ensemble.py` launches only via `ClaudeProcess` and has no raw `subprocess.run` / `Popen` import/call at lines 187-191.
- `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/tests/cli/reflect/test_ensemble_unit.py:224` defines `test_u7_no_nesting_guard_extended_to_ensemble`, asserting `ensemble.py` is in the agent-surface source set and directly invoking the guard tests at lines 231-239.

### Swarm tests relevant to executor/model-pool constraints

- `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/tests/swarm/test_model_pool_guard.py:40` defines the openai-compatible model-pool guard. It raises `ModelPoolTooSmallError` when pool size is below workers and asserts both counts in the error at lines 40-47; it also pins equal/larger pool success and per-slot distinct model binding at lines 50-67.
- `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/tests/swarm/test_model_pool_guard.py:82` is the CLI-level guard: one real model for a three-worker lens exits `EXIT_INVALID` before dispatch and prints the pool-vs-workers error at lines 82-116. A→C should not weaken this guard; reflect-side waiver applies only to unreliable exclusion source, not to an actually undersized live model pool.
- `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/tests/swarm/test_inv005_pool_guard.py:181` pins `DEFAULT_POOL_POLICY == "warn"`; `test_workers_exceed_pool_detection` at lines 191-208 covers detection of requested workers exceeding the declared model pool. This is adjacent to, but not a substitute for, reflect executor-class exclusion semantics.
- `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/tests/swarm/test_parallel_executor_routing.py:1` documents and enforces the single `ParallelExecutor` routing seam for swarm dispatch; lines 32-47 describe the functional/static assertions banning direct `ThreadPoolExecutor`/`ProcessPoolExecutor` use, with the forbidden constructor set defined at lines 97-102. A→C should not introduce new direct parallel executor construction in reflect or swarm.

## Proposed tests to add or extend

### 1. Unit-test source reliability classification and exclusion decision

Add a new unit test file:

- `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/tests/cli/reflect/test_executor_exclusion_source.py`

Recommended assertions:

1. `test_reliable_source_applies_executor_class_exclusion`
   - Build a synthetic source/pool where executor class is known from a reliable source.
   - Assert the selector excludes all candidates matching the executor class before choosing reviewers.
   - Assert selected reviewer model IDs do not include the executor class.
   - Assert telemetry records something equivalent to `executor_exclusion.status == "applied"`, `source_reliability == "reliable"`, and `excluded_executor_class == <class>`.
2. `test_unreliable_source_waives_executor_exclusion_not_fail`
   - Build a synthetic source/pool where executor class data is absent, ambiguous, stale, or otherwise classified unreliable.
   - Assert selection still returns reviewers from the normal heterogeneous pool.
   - Assert no exception/blocked result is raised solely because the source is unreliable.
   - Assert telemetry records `executor_exclusion.status == "waived"` (or equivalent), a machine-readable reason such as `source-unreliable`, and does not set degraded solely for the waived exclusion.
3. `test_reliable_source_unsatisfiable_exclusion_degrades_not_collapses`
   - Build a synthetic source/pool where reliable source says the executor class must be excluded, but excluding it leaves fewer than the required distinct classes/survivors.
   - Assert the outcome is a formed Tier-2 contract when enough reviewers ran, not `contract is None` / BLOCKED.
   - Assert the result is DEGRADED exit 11 with reason/degraded component equivalent to `executor-exclusion-unsatisfiable`.
   - Assert it does not silently fall back to `single-reviewer-fallback` unless the successful reviewer count is actually one.
4. `test_unreliable_source_never_mutates_model_pool_guard`
   - Assert an unreliable executor-source waiver does not bypass the hard live model-pool guard from swarm. If workers=3 and the live env pool has 1 model, the existing `ModelPoolTooSmallError`/EXIT_INVALID semantics must remain.

### 2. Extend real fan-out integration tests

Extend:

- `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/tests/cli/reflect/test_ensemble_stub_integration.py`

Add integration tests that drive `run_tier2_ensemble` through the existing `_run(config, transport_for_slot)` helper pattern used at lines 108-122:

1. `test_i13_reliable_executor_exclusion_real_fanout`
   - Use three stub transports/classes where one slot is tagged as executor-class and two are non-executor distinct classes.
   - Run the real ensemble path, not a canned `ClaudeProcess` fixture.
   - Assert `reviewer_count == 2`, `tier_reached == 2`, `merge_method != "single-reviewer-fallback"`, selected/succeeded reviewer model IDs exclude the executor-class model, and verdict remains PASS if diversity is still full after exclusion.
2. `test_i14_unreliable_executor_source_waives_real_fanout`
   - Simulate unreliable source via the production seam/config/env used by the implementation.
   - Assert the run completes, emits a top-level contract, records the waiver, and remains PASS-eligible when other PASS criteria are satisfied.
   - Assert `result.verdict is not Verdict.BLOCKED`; if all other criteria are healthy, assert PASS exit 0.
3. `test_i15_reliable_executor_exclusion_unsatisfiable_degrades_real_fanout`
   - Simulate reliable executor source but a pool that cannot provide two non-executor distinct successful classes.
   - Assert top-level contract exists, `tier_reached == 2` when two or more reviewers still succeeded, and `result.verdict is Verdict.DEGRADED` / exit 11.
   - Assert `result.reason` or `degraded_components` names executor-exclusion unsatisfiability.
   - Assert this is not M==0/BLOCKED and not a one-reviewer collapse unless the fixture deliberately has only one survivor.

### 3. Extend verdict mapping for new contract fields

Extend:

- `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/tests/cli/reflect/test_verdict_mapping.py`

Add direct `derive_verdict` unit tests using an in-memory copy of `pass.yaml`:

1. `test_executor_exclusion_waived_source_unreliable_not_degraded`
   - Set the new exclusion telemetry to waived/source-unreliable.
   - Assert PASS if all other pass criteria remain healthy. This mirrors the existing fail-open unavailable pattern at lines 143-163.
2. `test_executor_exclusion_unsatisfiable_is_degraded`
   - Set the new telemetry/degraded component for unsatisfiable reliable exclusion.
   - Assert DEGRADED exit 11.
3. `test_executor_exclusion_untrusted_field_shape_blocks_or_degrades_as_designed`
   - If the implementation treats malformed load-bearing exclusion fields as contract-invalid, assert BLOCKED. If it treats them as source-unreliable, assert PASS with waiver. Do not leave malformed truthy strings implicitly PASS by accident.

### 4. Extend contract shape preservation

Extend:

- `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/tests/cli/reflect/test_ensemble_stub_integration.py:306`

Update `test_i7_return_contract_shape_preserved` to include all A→C telemetry fields consumed downstream. Suggested field names if the implementation introduces them:

- `executor_exclusion`
- `executor_exclusion_status`
- `executor_exclusion_source_reliability`
- `executor_class_source`
- `excluded_executor_class`

Use the actual names chosen by implementation, but require enough stable machine-readable fields for post-run debugging and future doc parity.

### 5. Keep and extend banned-token/no-nesting verification

Extend:

- `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/tests/cli/reflect/test_no_nesting_guard.py`
- `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/tests/cli/reflect/test_ensemble_unit.py`

Requirements:

- Add any new reflect module implementing A→C executor exclusion to `_AGENT_SURFACE_SRCS` if it can launch, select, or orchestrate reviewers.
- Add any new reflect `.py` file to the package-wide thinness scans automatically via `_REFLECT_PY`; no extra work is needed if it lives in `src/superclaude/cli/reflect/*.py`.
- Continue to ban these exact strings from reflect runner/ensemble/new launcher surfaces: `import anthropic`, `from anthropic`, `subagent_type`, `Agent(`, `Task(`.
- Continue to require `ClaudeProcess` as the only sanctioned Claude launch primitive in modules that perform Claude child launches.
- Continue to ban raw `subprocess.run` / `Popen` calls in `runner.py` and `ensemble.py`; if a new launch module exists, include it in the same raw-subprocess guard.
- Add a test asserting no A→C worker prompt/instruction contains `/sc:reflect` as the worker instruction. The existing worker-prompt guard in `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/tests/cli/reflect/test_ensemble_stub_integration.py:387` already asserts the lens brief is the instruction and `/sc:reflect` only appears in the quoted target body at lines 406-417.

## Required validation commands

### Per-code-edit gate

Run after each implementation edit that touches reflect/swarm source or tests:

```bash
cd /config/workspace/IronClaude/.dev/worktrees/pr197-remediation && uv run pytest tests/cli/reflect -q
```

### Final validation commands

Run exactly these final commands from the worktree root context:

```bash
make -C /config/workspace/IronClaude/.dev/worktrees/pr197-remediation sync-dev
```

```bash
make -C /config/workspace/IronClaude/.dev/worktrees/pr197-remediation verify-sync
```

```bash
cd /config/workspace/IronClaude/.dev/worktrees/pr197-remediation && uv run pytest tests/cli/reflect tests/swarm -q
```

```bash
cd /config/workspace/IronClaude/.dev/worktrees/pr197-remediation && uv run ruff format --check src/ tests/
```

```bash
make -C /config/workspace/IronClaude/.dev/worktrees/pr197-remediation lint
```

Makefile evidence:

- `make lint` runs `uv run ruff check .` after `lint-architecture` in `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/Makefile:48` through line 50.
- `make sync-dev` syncs `src/superclaude/` to `.claude/` for local development in `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/Makefile:109` through line 158.
- `make verify-sync` is the CI-friendly drift check in `/config/workspace/IronClaude/.dev/worktrees/pr197-remediation/Makefile:166` onward.

## Summary

Existing tests already pin Tier-2 real fan-out, diversity degradation, single-reviewer fallback, M==0 BLOCKED, verdict ordering, model-pool guard behavior, and no-nesting/ban-token rules. The A→C task needs additive tests for the missing source-reliability/executor-class exclusion axis: reliable source applies exclusion, unreliable source waives instead of fails, and reliable-but-unsatisfiable exclusion forms a non-collapsing DEGRADED Tier-2 rather than BLOCKED or single-reviewer fallback. Per-edit validation should run the reflect suite; final validation must run sync/verify-sync, reflect+swarm tests, ruff format check, and lint from the absolute worktree root.
