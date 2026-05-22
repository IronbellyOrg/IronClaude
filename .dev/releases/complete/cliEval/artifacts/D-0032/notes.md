# D-0032 — Implementation notes (Task T02.11)

## Why T02.11 is a *test-only* deliverable

The COMP-006 method surface (`setup` / `env` / `teardown` / `state_path`)
was already implemented by T02.07 (D-0028) and hardened by T02.08
(D-0029); the FR-ISO2 containment guard already sits inside `setup`.
T02.11's deliverable text — "Full HomeIsolation implementation module
integrating FR-ISO1, FR-ISO2, and the install_hooks adapter" — is the
**finalization gate** that confirms the integrated contract round-trips
correctly as a unit, mapped to the four T02.11 AC bullets.

No code change to `src/superclaude/cli/eval/isolation.py` is required.
The install_hooks adapter (T02.14 / D-0034) consumes only the public
`HomeIsolation.home_path` property and does not extend the COMP-006
class surface — it is a separate module (`hook_adapter.py`) that takes
`home_path: Path` as input.

## Test design — integration vs. per-method coverage

`test_home_isolation_extend.py` (T02.07) and `test_path_containment.py`
(T02.08) already exhaustively cover per-method and per-check behavior
(83 + 45 = 128 tests). Repeating that coverage in `test_home_isolation.py`
would be duplicative and would obscure what T02.11 actually tests.

The new module focuses on the **integrated lifecycle**:

1. The four method signatures via `inspect.signature` introspection
   (so a future refactor that drops a method or changes a keyword-only
   parameter into positional surfaces here, not just downstream).
2. `state_path` anchored against `home_root` — the T02.11 AC explicitly
   names `is_relative_to(home_root)` (the orchestrator's declared
   scratch root), not just `home_path` (the per-eval HOME). The new
   test asserts BOTH so reporters that consume `home_root` directly
   stay correct.
3. End-to-end round-trip `setup → env → state_path → teardown`, plus
   re-setup-after-teardown.
4. Parallel siblings — 8-way `ThreadPoolExecutor` re-confirms
   concurrency safety at the COMP-006 level (T02.07 already proves it
   at the `setup` level).
5. DM-006 invariant survival across the integrated lifecycle.

## `state_path` AC — `is_relative_to(home_root)` ambiguity

The T02.11 AC text reads:

> `state_path(suffix)` returns paths exclusively under the per-eval HOME
> (verified by `is_relative_to(home_root)` assertion).

`home_root` is the scratch root (per DM-006); `home_path` is the
per-eval HOME (created by `setup`). The two predicates are equivalent
in the happy path because `home_path.parent == home_root`. The T02.11
test asserts BOTH so neither interpretation is left ambiguous and the
strictest possible reading of the AC is satisfied (see
`TestStatePathIsAnchoredUnderHomeRoot::test_state_path_is_relative_to_home_root`
and `…::test_state_path_is_also_relative_to_home_path`).

## Containment-guard re-confirmation

The T02.08 / D-0029 suite already proves every guard check rigorously.
T02.11 re-runs only two assertions at the COMP-006 entry point:

* `scratch_root_allowlist` is hit through `HomeIsolation.setup`
  (not direct `containment_guard` invocation), so a regression that
  bypasses the guard inside `setup` would surface.
* `setup()` without an explicit `config=` raises `TypeError` — the
  D-0029 refusal-before-side-effects contract.

These two are sufficient because the per-check enumeration lives in
the dedicated module and T02.11's job is integration confidence, not
attack-vector exhaustiveness.

## Concurrency test choice

8 parallel siblings via `ThreadPoolExecutor(max_workers=8)` mirrors the
upstream `test_parallel_setup_does_not_collide` from T02.07 but takes
the additional step of running the full lifecycle on each thread
(`setup → state_path → env → teardown`). Eight is enough to expose any
shared-state defect; the NFR-PERF1 baseline at 15-eval parallel lives
in T02.15 / D-0035 (benchmark, not correctness).

## Decisions

1. **No new module under `src/`** — T02.11 is a finalization gate,
   not a refactor. Keeping the per-eval primitive in
   `isolation.py` avoids splitting concerns the dataclass already
   binds together. If the install_hooks adapter (T02.14) were to land
   first, no edit to `isolation.py` would be needed; the adapter
   reads `iso.home_path` and does its own filesystem write.
2. **No probe re-import** — the T02.05 IsolationLayers probe is
   re-verified in T02.07 (D-0028 module). Re-running it here would
   add an import-time coupling without adding signal.
3. **`config: EvalConfig | None` is rejected at the type level** —
   T02.11 reaffirms D-0029's stance by asserting `TypeError` on
   `setup()` called without the keyword. Any future refactor that
   re-introduces a `None` default surfaces here.

## What deliberately does NOT live in this module

* `setup_failed` artifact-tag assertions — owned by T02.13 / D-0033.
* `deploy_hooks_to` idempotency — owned by T02.14 / D-0034.
* Sub-1.4s p50 perf at 15-eval parallel — owned by T02.15 / D-0035.
* NFR-SEC2 attack-matrix exhaustiveness — owned by T02.09 / D-0030.
* NFR-SEC3 real-`~/.claude/` refusal — owned by T02.10 / D-0031.

Cross-deliverable separation keeps each test file small enough to
pinpoint a failure to a single COMP/FR/NFR row in the roadmap.
