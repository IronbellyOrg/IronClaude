# D-0008 — implementation notes

## Decisions made during build

1. **Module path:** `src/superclaude/cli/eval/capabilities.py`, per the
   task step `[EXECUTION] Add Capability dataclass with frozen=True`. The
   filename matches the design-spec §11 reference (`capability_gates.py`
   in the spec is the COMP-009 site landing in T01.11; T01.09 only owns
   the descriptor type, so it lives in a sibling `capabilities.py`).

2. **`failure_mode` typed as `Literal["hard","skip","xfail"]`.** Matches
   the task acceptance criterion verbatim. A module-level
   `FailureMode = Literal[...]` alias is exported so COMP-009 callers can
   annotate their `CAPABILITIES` list with the same type without
   re-declaring the union.

3. **`__post_init__` runtime check.** Even with the `Literal` static
   type, Python does not enforce membership at runtime, so the task
   acceptance criterion `instantiation with an invalid failure_mode
   raises ValueError` requires an explicit check. Implemented via a
   `frozenset` lookup against `{"hard", "skip", "xfail"}` so adding new
   modes later is a one-line change.

4. **`check` callable is NOT invoked at construction.** Capability
   descriptors are declared at module import time (in COMP-009's static
   `CAPABILITIES` list per design-spec §11). If `check` were invoked
   eagerly, doctor output would crash on import when `claude` is missing
   instead of reporting it as a HARD failure. The test
   `test_capability_check_not_invoked_at_construction` locks this
   contract.

5. **`skip_flag: Optional[str] = None` and `description: str = ""`.**
   Matches the design-spec §11 reference signature verbatim. Defaults
   make HARD capabilities (which never need a skip flag) construct with
   3 positional args, matching the design-spec's example rows.

6. **Equality and hashability.** The dataclass-generated `__eq__`
   gives structural equality across all 5 fields, satisfying the AC
   "two instances built from the same arguments compare equal". The
   instances are hashable only when the `check` callable is hashable
   (module-level functions are; freshly-constructed lambdas are too,
   under CPython's default `id`-based hash). Callers should not rely on
   Capability as a dict key — this is documented in the module
   docstring.

## Things deliberately NOT in scope of T01.09

- Static `CAPABILITIES` table (`binary.claude`, …) — landing in T01.11.
- `which_or_skip` / `mcp_server_reachable` helpers — T01.11.
- `CapabilityReport` aggregate model — T01.10 (DM-008).
- Doctor CLI plumbing — T01.13.
- OQ-5 `mcp_server_reachable` semantics resolution — tracked in
  phase-1-tasklist notes for T01.11, not relevant to the descriptor
  type.
