# D-0010 — Implementation notes

## Design choices

1. **Co-locate `CapabilityGates` with `Capability` / `CapabilityReport`
   in `capabilities.py`.** Design-spec §3 proposed a separate
   `capability_gates.py`, but T01.09 and T01.10 already established
   `capabilities.py` as the module home for this subsystem. Splitting
   the gate class into a sibling file would force every caller to
   import from two modules and would introduce a circular-import risk
   when `CapabilityGates._make_capability` materialises `Capability`
   instances. Keeping everything in one file makes the
   declaration → consumption flow readable top-to-bottom.

2. **`_CapabilitySpec` as a private internal helper.** The `Capability`
   dataclass (T01.09) only carries the per-capability *behaviour*
   (`name`, `check` callable, `failure_mode`, `skip_flag`,
   `description`). To probe a binary we also need the *target* string
   (`claude` vs `binary.claude`) and the *kind* tag (`binary` vs
   `mcp_server`) so the gate can pick the right probe. Stashing those
   on a private `_CapabilitySpec` keeps `Capability` itself stable for
   external callers and lets the static roster carry the extra metadata
   without polluting the public type.

3. **`mcp_probe` constructor hook for OQ-5.** Rather than wait for OQ-5
   to land before shipping T01.11, the gate accepts an optional
   `mcp_probe: Callable[[str], tuple[bool, str]]` keyword. Production
   callers leave it `None` and get the M1 PATH-presence stub; the M2
   patch (resolving OQ-5) swaps in a real handshake probe via the same
   hook without touching `CapabilityGates`. Tests also use this hook to
   simulate reachable/unreachable servers without monkeypatching
   `shutil`.

4. **`Capability.check` closures defer to gate methods.** The
   `capabilities()` accessor materialises `Capability` instances whose
   `check` closures call back into `self.which_or_skip` /
   `self.mcp_server_reachable`. This guarantees there is exactly one
   source of truth for what "passed" means — if a future patch tightens
   `which_or_skip` (e.g., to enforce `is_executable`), the closures
   automatically pick it up. The default-argument binding
   (`target: str = spec.target`) inside the closure prevents the
   classic late-binding-in-loop bug.

5. **`blocked_evals` left empty by `check_all`.** The gate has no
   knowledge of which evals depend on which capability — that mapping
   lives on the `requires:` field of each `EvalSpec` in the parsed
   suite. The SuiteLoader / runner is the layer that joins the two and
   populates `blocked_evals`. Leaving the field empty here keeps the
   single-responsibility separation clean and matches how the existing
   `PermissiveCapabilityResolver` (T01.07) defers gate semantics to the
   real implementation.

6. **`skip_flags` sorted + deduplicated.** The constructor accepts any
   iterable; the property emits a sorted tuple so two gates created
   with the same flag set in different orders produce equal reports.
   This is what gives `test_check_all_is_idempotent` its strict
   equality guarantee.

7. **Unknown-kind guard in `_probe`.** The `Literal["binary",
   "mcp_server"]` annotation on `_CapabilitySpec.kind` is a type-checker
   hint, not a runtime constraint. A typo in a downstream custom spec
   tuple (`kind="binaryy"`) would otherwise silently fall through and
   produce an always-passing row. The explicit `ValueError` raises at
   `check_all` time so the test suite catches the typo via
   `test_unknown_capability_kind_is_rejected_at_check_time`.

## Trade-offs and follow-ups

- **No `CapabilityResolver` adapter yet.** The SuiteLoader (T01.07)
  consumes the `CapabilityResolver` protocol (`resolve(eval_id,
  required)`). `CapabilityGates` does not implement that signature —
  T01.13 will wire an adapter when it threads the real gate through
  `commands.py`. Building the adapter now would be speculative: the
  loader → gate seam wants to consult `CapabilityReport.report` to map
  capability names to pass/fail, which the loader doesn't have access
  to today.
- **MCP reachability is intentionally weak.** The M1 stub treats
  "binary on PATH" as the reachability signal. This passes locally
  whenever the `auggie` CLI is installed but does NOT detect a wedged
  server, an SSE endpoint behind a firewall, or an unreachable
  gateway. OQ-5 must resolve before COMP-009 close at M2.
- **No async / no timeout.** `shutil.which` is sub-millisecond on a
  warm cache; a future MCP handshake probe will need a per-server
  timeout. The `mcp_probe` hook keeps the seam in place for that
  upgrade.
- **`capabilities()` materialises new `Capability` instances on every
  call.** This is intentional — the closures bind to the live gate
  instance so a test that calls `gate.capabilities()[0].check()` sees
  the same probe behaviour as `gate.check_all()`. The cost is trivial
  (8 dataclass constructions); memoising would force us to invalidate
  on `_mcp_probe` replacement.
