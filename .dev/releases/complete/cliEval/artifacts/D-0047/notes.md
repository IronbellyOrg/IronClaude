# D-0047 — EvalContext implementation notes

## Design decisions

### Frozen dataclass + MappingProxyType for mapping fields

T03.03 explicitly says "(immutable view)" and the AC enumerates "EvalContext instances reject mutation (FrozenInstanceError on attempted set)". `@dataclass(frozen=True)` covers attribute assignment but does *not* block method calls on field values — `ctx.env["HOME"] = "..."` would silently succeed on a plain dict. Three options were considered:

1. **Plain frozen dataclass + plain `dict` fields.** Rejected — the "immutable view" wording in DM-010 + the threading rationale (an `EvalContext` shared across ExpectCallables) means the mapping contents must not be mutable either.
2. **`Mapping[str, str]` annotation only.** Rejected — `Mapping` is a *type* hint, not a runtime guard. Callers can still pass a `dict` and mutate it.
3. **`MappingProxyType` wrapping in `__post_init__` and the factory** (chosen). The `types.MappingProxyType` is the standard-library read-only proxy; assignments raise `TypeError`. We wrap in two places:
   - `__post_init__` so direct `EvalContext(...)` construction (used in test ergonomics) still wraps the mappings.
   - `from_runner_state` so the factory shallow-copies the caller's mapping into a fresh `dict`, then proxies it. The shallow copy is what isolates the context from later caller mutation (covered by `test_eval_context_factory_isolates_env_from_caller_mutation`).

The combination gives a record where neither `ctx.foo = bar` nor `ctx.env["foo"] = bar` succeeds.

### `home` and `home_path` as two separate fields

DM-010 lists both `home` and `home_path`. The pair is intentional:

- `home` is the `HomeIsolation` instance — primitives that need `home.env()` (e.g. `Expect.settings_json` traversing `~/.claude/settings.json`) or `home.state_path(...)` (helpers that join a suffix safely) call it directly.
- `home_path` is a `Path` — primitives that only need the directory avoid the `home.home_path` property indirection *and* the `RuntimeError` it raises when setup has not run (by the time the factory builds the context, setup has already completed and dereferencing the property always succeeds).

The factory enforces `home.home_path == home_path` as an invariant so the two never drift.

### Factory keyword-only arguments

`from_runner_state` is defined with `*` before the first parameter so every argument must be passed by keyword. Rationale: future field additions (e.g. when DM-010 grows a 16th field for OQ-8 wall-clock plumbing) would silently re-bind positional callers if we did not enforce this. The cost is a slightly longer call site in `EvalRunner` (T03.04); the benefit is that any test or runner that constructs a context fails loudly the moment the schema changes. Covered by `test_from_runner_state_keyword_only_arguments`.

### Factory raises through `home.home_path` rather than building a half-valid context

`HomeIsolation.home_path` raises `RuntimeError("HomeIsolation.setup() must be called before accessing home_path")` when setup has not run. Two options:

1. **Catch the `RuntimeError` and fabricate a placeholder** (e.g. `Path("/")`). Rejected — half-valid contexts are worse than no context. An ExpectCallable that read the placeholder would silently produce garbage assertions.
2. **Let the `RuntimeError` propagate** (chosen). The factory call site (`EvalRunner.run`) is the right place to fail loudly — by the time the runner builds the context the setup step is supposed to have completed, so a propagation here is a runner-internal bug, not a user-facing error. Covered by `test_from_runner_state_raises_when_home_not_setup`.

### Why no `to_dict()` for `EvalContext`

DM-001 (`EvalOutcome`) and DM-003 (`EvalResult`) have `to_dict()` because they flow into JSON artifacts (`summary.json`). DM-010 (`EvalContext`) is consumed in-process by ExpectCallables; none of the downstream Reporter paths serialise it. Adding `to_dict()` for symmetry would be dead code today and would force us to define serialisation for `EvalSpec` and `HomeIsolation`, both of which carry richer state than what the Reporter needs. The `_EVAL_CONTEXT_FIELDS` constant is still in place so a future `to_dict()` can iterate in DM-010 order if the need arises.

### Module-level vs. delayed `HomeIsolation` import

`HomeIsolation` is imported from `.isolation`, which itself imports from `.loader` (for `validate_eval_id`) and `.config` (for `EvalConfig`). To avoid the import cycle that would land if `models.py` imported `isolation.py` eagerly, the `HomeIsolation` import is guarded by `TYPE_CHECKING` and the dataclass field uses a forward-string annotation (`"HomeIsolation"`). Runtime construction works because the factory accepts the instance as a keyword argument and never has to introspect the class.

## Future work touchpoints

- **T03.04 / T03.05 (EvalRunner)** — primary construction site for `EvalContext`. The runner will call `EvalContext.from_runner_state(...)` after the `observe` lifecycle step has captured stdout/stderr/exit_code, then pass the context to each `Expect.*` callable in the `assert` step.
- **T04.01..T04.07 (Expect primitives)** — every primitive is a function from `EvalContext` to `ExpectResult`. The 15-field contract is the surface they read; primitives that need helpers (`home.state_path`, `home.env`) call them off the `home` field.
- **OQ-8 (DOC-OQ8 / T06.03)** — when wall-clock offset semantics resolve, the runner may need to thread an additional field through the context; `_EVAL_CONTEXT_FIELDS` provides the canonical insertion point.
