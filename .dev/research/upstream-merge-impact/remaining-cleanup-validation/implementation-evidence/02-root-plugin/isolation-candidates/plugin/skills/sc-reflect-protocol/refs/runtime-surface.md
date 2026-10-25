# Runtime Surface Reachability

Source-of-truth reference for FR-RSR runtime-surface tagging, reachability sweep decisions, degrade handling, rootwalk bounds, and the runtime-surface ledger schema.

## 1. Surface allowlist (OQ-RSR.1)

The runtime-surface tagger is UC-2-only and symbol-anchored: it keys off the resolved diff-hunk symbol kind/decorator, not a requirement id. `requirement_id` is optional and may remain `null`; a surface hunk with no mapped requirement is still tagged and swept.

| Language / family | Surface symbols and decorators in scope | Deterministic tagger signal |
|---|---|---|
| Python | CLI command symbols, HTTP route handlers, public endpoint handlers, Click/Typer command callbacks, decorator-registered routes | Resolved function/class symbol kind plus decorators such as `@app.route`, router route decorators, `@click.command`, `@click.group`, `@*.command`, and Typer command/callback decorators |
| TypeScript / JavaScript | Route handlers, command handlers, exported endpoint handlers, framework/controller methods | Resolved function/method/export kind plus route/handler/controller decorators or call sites naming the symbol as an endpoint/handler |
| Rust | Command handlers, HTTP/endpoint handlers, functions exported as runtime handlers | Resolved function/item kind plus route/handler attributes or command-dispatch registration visible in the hunk |
| Go | HTTP handlers, CLI command handlers, exported runtime endpoint functions, AND provider/adapter methods that implement a DECLARED runtime capability (an interface method the composition root wires and a caller invokes for a live effect — e.g. a `Subscribe`/`Dial`/`Open` seam on an injected provider) | Resolved function/method kind plus handler registration idioms visible in the hunk, OR a method whose receiver implements an interface that a composition root binds and a runtime caller invokes for its effect |
| Other / unknown | Any candidate the tagger cannot classify soundly | `DEGRADE` through the language-table/default oracle; never silently skip a possible surface |

A non-surface diff emits `runtime_surface_requirements: []`, `runtime_surface_sweep_ran: false`, and adds zero runtime-surface sweep cost.

## 2. Language table (OQ-RSR.2)

Use this table to partition `find_referencing_symbols` results into production referrers vs test/comment evidence. Unknown languages or ambiguous comment/test classification yield `DEGRADE`, never `UNREACHED` and never "treat as production."

| Language | Path/test markers | Inline test markers | Comment syntax to exclude as non-production evidence |
|---|---|---|---|
| `py` | `tests/`, `test_*.py`, `*_test.py`, `conftest.py` | `class Test*`, `def test_*`, `pytest` fixtures/marks in the enclosing scope | `#`, triple-quoted docstrings used only as documentation/examples |
| `rust` | `tests/`, `*_test.rs` | `#[cfg(test)]`, `mod tests`, `#[test]` | `//`, `///`, `//!`, `/* ... */` |
| `ts` | `tests/`, `__tests__/`, `*.test.ts`, `*.spec.ts` | `describe(`, `it(`, `test(` in the enclosing scope | `//`, `/* ... */`, JSDoc-only references |
| `js` | `tests/`, `__tests__/`, `*.test.js`, `*.spec.js` | `describe(`, `it(`, `test(` in the enclosing scope | `//`, `/* ... */`, JSDoc-only references |
| `go` | `*_test.go` | `func Test*`, `func Benchmark*`, `func Example*` | `//`, `/* ... */`, doc-comment-only references |
| unknown / unsupported | n/a | n/a | Classification is incomplete → `DEGRADE` |

Inline test modules count as test even when they live in a production-path file. Comment-only and documentation-only references do not count as production callers.

## 3. Degrade oracle (FR-RSR.3)

Static referrer analysis is semi-decidable for runtime wiring. Matching any row below yields `status: DEGRADE`, routes the finding to §10.6 Grounding Gaps, and never increments `deviation_count_by_class.regression` or produces a blocking Regression.

| Category | Deterministic match predicate | Verdict |
|---|---|---|
| (a) Decorator routes / command decorators | Tagged symbol or adjacent hunk carries route/command decorators such as `@app.route`, router route decorators, `@click.command`, `@click.group`, `@*.command`, or Typer command/callback decorators | `DEGRADE` |
| (b) Packaging entrypoints | Tagged symbol is named by `[project.scripts]`, `[project.entry-points.*]`, console-scripts-equivalent metadata, or equivalent packaging entrypoint declarations | `DEGRADE` |
| (c) Registry / dependency-injection / string dispatch | Tagged symbol appears as the registered object or string value/key in a registry assignment/call, DI-container binding, command map, plugin table, or string-dispatch table visible in the hunk or adjacent metadata | `DEGRADE` |
| (d) Reflection / dynamic import | Tagged symbol is reached through a visible reflection/dynamic-import expression such as `importlib.import_module(...)`, `__import__(...)`, `getattr(<module>, "<symbol>")`, entry-point/plugin `load()`, or equivalent name-based lookup where the symbol name or module path is data | `DEGRADE` |

Concrete in-repo packaging case: `pyproject.toml` declares `[project.scripts]` entries `superclaude = "superclaude.cli.main:main"` and `ic = "superclaude.cli.ic:main"`. Those console-script entrypoints are registry/packaging wiring and MUST degrade; they are never `UNREACHED` and never Regression solely because no static production caller appears.

Default rule: every reachability uncertainty maps to `DEGRADE → §10.6 Grounding Gap`. The safe asymmetric-cost posture is fail-loud: never silently PASS an untested surface, and never silently Regression an idiomatic dynamic/registry/decorator/reflection/packaging entrypoint.

### 3a. Behavioral reachability for provider/adapter capability seams (symbol-edge ≠ behavioral)

For a tagged **provider/adapter capability seam** (the §1 Go-row addition), a production referrer edge is **NECESSARY BUT NOT SUFFICIENT** to reduce the symbol to `REACHED`. This closes the Layers 1-2 gap the v1.4.1 WS-dial miss exposed (see the reflect-miss analysis: FR-RSR proved a `Subscribe` production referrer existed at `menu.go:663` and reduced it to `REACHED`, while one hop below the edge the caller's `err==nil` guard swallowed the sentinel and the callee returned `ErrNoStream` — the edge existed but carried no live behavior). A capability seam reduces to `REACHED` only when the sweep can show **behavioral reachability**:

1. a production (non-test) caller invokes the seam at a runtime entrypoint / composition root, **AND**
2. that caller's use of the result is **live** — the result is consumed, not discarded and not swallowed by a dead error-guard (the `if …; err == nil { … }` shape that silently no-ops on a not-implemented sentinel), **AND**
3. the callee is a **non-vacuous** implementation — not a bare sentinel body (an `ErrNoStream`-shape stub) where the caller's contract requires a live effect.

If a capability seam has a production referrer but sub-clause (2) or (3) fails (result discarded/dead-guarded, or callee is sentinel-only), it does **NOT** reduce to `REACHED` — it is a behavioral-reachability failure that maps to `reachability_unreachable ⇒ Regression` (see `deviation-taxonomy.md`), the same disposition SKILL.md's required-capability reachability pass assigns. Where the sweep cannot statically decide consumed-ness (sub-clause 2) or callee-vacuousness (sub-clause 3), it emits `DEGRADE` (never a silent `REACHED`) per the default doctrine above. Symbol-edge presence alone is never a pass for a capability seam.

## 4. Entrypoint-rootwalk algorithm (OQ-RSR.3 / FR-RSR.4)

The production-caller sweep MUST invoke the rootwalk on every candidate-`UNREACHED` verdict before emitting `UNREACHED`.

1. Enumerate runtime roots available to the run: packaging entrypoints (including `[project.scripts]`), command roots, route/router roots, and other runtime entrypoint roots visible to the protocol.
2. Walk from each enumerated root toward the candidate symbol with a depth bound of **1**, mirroring the §4.0 link-following depth convention.
3. If the candidate symbol is reachable from any enumerated root within the depth bound, reduce the symbol to `REACHED` even when it has zero direct production referrers.
4. If all roots are enumerated successfully, no root reaches the candidate, and the degrade oracle did not match, the candidate may reduce to `UNREACHED`.
5. If any root errors, is skipped, cannot be enumerated, or the depth bound is hit before resolution, enumeration is partial; the verdict is `DEGRADE`, never `UNREACHED`.

A symbol called only by other unreached production code is not automatically `REACHED`: the rootwalk anchors `REACHED` to an actual runtime root. Partial rootwalk is incompleteness and follows the default degrade doctrine.

## 5. `runtime-surface-ledger.yaml` schema

The sweep writes `<output>/artifacts/runtime-surface-ledger.yaml` as a per-run artifact. It is one row per evaluated edge, not one row per symbol.

```yaml
- requirement_id: <str | null>          # null is valid; the tagger is symbol-anchored
  symbol: <str>                         # tagged surface symbol name-path
  edge: <str>                           # "<symbol> -> <referrer-or-entrypoint-root>"
  status: REACHED | UNREACHED | DEGRADE
  production_referrers: [<file:line>]   # surviving non-test/non-comment referrers; [] for UNREACHED
  evidence_ref: <file:line-or-artifact> # evidence backing the verdict; re-Read by evidence-validator
```

Typed shape:

```python
class RuntimeSurfaceLedgerRow(TypedDict):
    requirement_id: str | None
    symbol: str
    edge: str
    status: Literal["REACHED", "UNREACHED", "DEGRADE"]
    production_referrers: list[str]
    evidence_ref: str
```

Per-symbol reduction precedence:

```text
DEGRADE-on-any-incompleteness > UNREACHED > REACHED
```

Count semantics and invariant:

- The ledger is per-edge; contract counts are per-symbol.
- `runtime_surface_unreached` counts symbols reduced to `UNREACHED`, never edges.
- `len(unreached_surfaces) == runtime_surface_unreached` MUST hold.
- A symbol with N test-only/comment-only referrers contributes N ledger rows but exactly 1 to `runtime_surface_unreached` if all edges are non-production and none degrade.
- Any degraded edge for a symbol reduces that symbol to `DEGRADE`; this records `runtime_surface_degraded: true` and routes through §10.6 Grounding Gaps rather than the deviation ledger.

Guard note: the silent-no-op risk is mitigated by the asymmetric-cost default. If the sweep cannot decide because language classification, backend/tooling, root enumeration, or dynamic wiring is incomplete, it must emit `DEGRADE` and preserve evidence instead of silently emitting PASS or Regression.
