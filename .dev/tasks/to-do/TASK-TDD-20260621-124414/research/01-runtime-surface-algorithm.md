# Research 01 — Runtime-Surface Algorithm (port target)

**Status: Complete**

**Topic:** The deterministic 7-step runtime-surface sweep algorithm and the ledger data model.
**Investigation type:** Architecture Analyst / Code Tracer.
**Component root (target module location):** `src/superclaude/cli/reflect/` — the module to be ported will live here.

## Verification posture (read first)

`refs/runtime-surface.md` is a **refs / source-of-truth specification document** describing *intended* behavior for FR-RSR. As of this investigation, **no runtime-surface implementation exists** in `src/superclaude/cli/reflect/`. Confirmed by grepping every file in that directory (`models.py`, `runner.py`, `commands.py`, `contract.py`, `ensemble.py`, `config.py`, `__init__.py`) for `runtime_surface`, `RuntimeSurface`, `rootwalk`, `unreached_surfaces`, `ledger`, `RuntimeSurfaceLedger` — **zero matches**.

Therefore:

- `[UNVERIFIED — spec-only]` is the **expected and correct** tag for nearly every structural claim here. It does NOT mean "stale documentation" — it means the algorithm is a **SPEC to build**, not a description of existing code. The distinction matters: a spec-only tag is a legitimate forward-looking design contract, whereas a stale-code tag would indicate the docs diverged from a real implementation. This module has no implementation to diverge from yet.
- `[CODE-VERIFIED]` is reserved for claims I could confirm against an existing artifact (e.g. the `pyproject.toml` `[project.scripts]` entries the spec cites as a concrete in-repo case).

Citations below reference `src/superclaude/skills/sc-reflect-protocol/refs/runtime-surface.md` by line number (abbreviated `RS:Lnn`) and `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (abbreviated `SKILL:Lnn`).

---

## §1 — Surface allowlist (OQ-RSR.1) `[UNVERIFIED — spec-only]`

Source: RS:L5–L17.

The tagger is **UC-2-only**, **symbol-anchored**, and **LLM-free / deterministic**. It keys off the *resolved diff-hunk symbol kind/decorator*, **not** off a `requirement_id` (RS:L7). `requirement_id` is optional and may stay `null`; a surface hunk with no mapped requirement is still tagged and still swept (RS:L7).

Per-language surface symbols in scope and the deterministic tagger signal (RS:L9–L15):

| Language / family | Surface symbols/decorators in scope | Deterministic tagger signal |
|---|---|---|
| **Python** | CLI command symbols, HTTP route handlers, public endpoint handlers, Click/Typer command callbacks, decorator-registered routes | Resolved function/class symbol kind + decorators: `@app.route`, router route decorators, `@click.command`, `@click.group`, `@*.command`, Typer command/callback decorators |
| **TypeScript / JavaScript** | Route handlers, command handlers, exported endpoint handlers, framework/controller methods | Resolved function/method/export kind + route/handler/controller decorators or call sites naming the symbol as endpoint/handler |
| **Rust** | Command handlers, HTTP/endpoint handlers, runtime-handler exports | Resolved function/item kind + route/handler attributes or command-dispatch registration visible in the hunk |
| **Go** | HTTP handlers, CLI command handlers, exported runtime endpoint functions | Resolved function/method kind + handler registration idioms visible in the hunk |
| **Other / unknown** | Any candidate the tagger cannot classify soundly | `DEGRADE` via the language-table/default oracle; **never silently skip a possible surface** (RS:L15) |

**Allowlist set for the port:** `{py, ts, js, rust, go}` are classifiable; everything else → `DEGRADE` (the `Other / unknown` row, RS:L15). This is the fail-loud asymmetric-cost posture: an unclassifiable candidate is never dropped.

**Non-surface fast path (RS:L17):** a non-surface diff emits `runtime_surface_requirements: []`, `runtime_surface_sweep_ran: false`, and adds **zero** runtime-surface sweep cost. This is the cheap exit the port must short-circuit to before any referrer work.

---

## §2 — Language table (OQ-RSR.2) `[UNVERIFIED — spec-only]`

Source: RS:L19–L32.

Purpose: partition `find_referencing_symbols` results into **production referrers** vs **test/comment evidence** (RS:L21). Unknown languages or ambiguous comment/test classification yield `DEGRADE` — **never** `UNREACHED` and **never** "treat as production" (RS:L21).

| Language | Path / test markers | Inline test markers | Comment syntax to exclude as non-production evidence |
|---|---|---|---|
| `py` | `tests/`, `test_*.py`, `*_test.py`, `conftest.py` | `class Test*`, `def test_*`, `pytest` fixtures/marks in enclosing scope | `#`, triple-quoted docstrings used only as documentation/examples |
| `rust` | `tests/`, `*_test.rs` | `#[cfg(test)]`, `mod tests`, `#[test]` | `//`, `///`, `//!`, `/* ... */` |
| `ts` | `tests/`, `__tests__/`, `*.test.ts`, `*.spec.ts` | `describe(`, `it(`, `test(` in enclosing scope | `//`, `/* ... */`, JSDoc-only references |
| `js` | `tests/`, `__tests__/`, `*.test.js`, `*.spec.js` | `describe(`, `it(`, `test(` in enclosing scope | `//`, `/* ... */`, JSDoc-only references |
| `go` | `*_test.go` | `func Test*`, `func Benchmark*`, `func Example*` | `//`, `/* ... */`, doc-comment-only references |
| unknown / unsupported | n/a | n/a | Classification is incomplete → `DEGRADE` |

Two load-bearing classification rules (RS:L32):

1. **Inline test modules count as test even inside a production-path file.** Example: a Rust `#[cfg(test)] mod tests` block living in `src/foo.rs` (a production path) is still test evidence, not a production caller. The port cannot rely on file-path classification alone; it must inspect the *enclosing scope* markers (column "Inline test markers").
2. **Comment-only and documentation-only references do not count as production callers.** A symbol named only inside a `#`/`//`/docstring/JSDoc reference is not a production referrer.

**Port implication:** classification is a two-axis decision — (path marker OR inline-test-scope marker) ⇒ test; (comment/doc-only) ⇒ excluded; otherwise ⇒ production. Any axis that cannot be evaluated (unknown language) collapses the whole symbol to `DEGRADE`.

---

## §3 — Degrade oracle (FR-RSR.3) `[UNVERIFIED — spec-only]` (with one `[CODE-VERIFIED]` data point)

Source: RS:L34–L47.

Rationale (RS:L36): static referrer analysis is **semi-decidable** for runtime wiring. Matching ANY row below yields `status: DEGRADE`, routes the finding to **§10.6 Grounding Gaps**, and **never** increments `deviation_count_by_class.regression` and **never** produces a blocking Regression.

The four categories, each with its deterministic match predicate (RS:L38–L43):

| # | Category | Deterministic match predicate | Verdict |
|---|---|---|---|
| **(a)** | Decorator routes / command decorators | Tagged symbol or adjacent hunk carries route/command decorators: `@app.route`, router route decorators, `@click.command`, `@click.group`, `@*.command`, Typer command/callback decorators | `DEGRADE` |
| **(b)** | Packaging entrypoints | Tagged symbol is named by `[project.scripts]`, `[project.entry-points.*]`, console-scripts-equivalent metadata, or equivalent packaging entrypoint declarations | `DEGRADE` |
| **(c)** | Registry / dependency-injection / string dispatch | Tagged symbol appears as the registered object or string value/key in a registry assignment/call, DI-container binding, command map, plugin table, or string-dispatch table visible in the hunk or adjacent metadata | `DEGRADE` |
| **(d)** | Reflection / dynamic import | Tagged symbol reached via a visible reflection/dynamic-import expression: `importlib.import_module(...)`, `__import__(...)`, `getattr(<module>, "<symbol>")`, entry-point/plugin `load()`, or equivalent name-based lookup where the symbol name or module path is data | `DEGRADE` |

**Concrete in-repo packaging case (RS:L45) — `[CODE-VERIFIED]`:** the spec cites `pyproject.toml` `[project.scripts]` entries `superclaude = "superclaude.cli.main:main"` and `ic = "superclaude.cli.ic:main"`. I verified `pyproject.toml` L67–L69 contains exactly these two entries (plus the `[project.entry-points.pytest11]` block at L72–L73, which is category (b)/(c) wiring as well). These console-script entrypoints **MUST** degrade (category b); they are **never** `UNREACHED` and **never** a Regression solely because no static production caller appears.

**Default rule (RS:L47):** every reachability uncertainty maps to `DEGRADE → §10.6 Grounding Gap`. The safe asymmetric-cost posture is fail-loud:
- never silently PASS an untested surface, AND
- never silently Regression an idiomatic dynamic/registry/decorator/reflection/packaging entrypoint.

**Port implication:** the oracle is a pure predicate over (tagged symbol, hunk text, adjacent metadata incl. `pyproject.toml`). It runs BEFORE any `UNREACHED` can be emitted (see §4 and the precedence in §5). Note category (a) overlaps the §1 tagger signals — a decorator that *qualifies* a symbol as a surface is simultaneously a *degrade* trigger, because static analysis cannot prove the decorator-registered route is actually wired at runtime.

---

## §4 — Entrypoint-rootwalk algorithm (OQ-RSR.3 / FR-RSR.4) `[UNVERIFIED — spec-only]`

Source: RS:L49–L59.

**Gating rule (RS:L51):** the production-caller sweep MUST invoke the rootwalk on **every** candidate-`UNREACHED` verdict *before* emitting `UNREACHED`. The rootwalk is the last gate that can rescue a symbol to `REACHED` (or escalate it to `DEGRADE`).

The 5-step rootwalk (RS:L53–L57):

1. **Enumerate runtime roots** available to the run: packaging entrypoints (incl. `[project.scripts]`), command roots, route/router roots, and other runtime entrypoint roots visible to the protocol.
2. **Walk from each root toward the candidate symbol with depth bound = 1**, mirroring the §4.0 link-following depth convention. (`depth=1` semantics: only roots that reach the candidate within a *single* link hop count; this is a shallow, deliberately bounded walk, not a full transitive reachability search.)
3. **REACHED rescue:** if the candidate is reachable from *any* enumerated root within the depth bound, reduce the symbol to `REACHED` — **even with zero direct production referrers**.
4. **UNREACHED only when:** all roots enumerated successfully AND no root reaches the candidate AND the degrade oracle did not match. Only then may the candidate reduce to `UNREACHED`.
5. **DEGRADE on partial enumeration:** if any root errors, is skipped, cannot be enumerated, OR the depth bound is hit before resolution → enumeration is partial → verdict is `DEGRADE`, **never** `UNREACHED`.

**depth=1 subtlety (RS:L59):** a symbol called only by *other unreached production code* is **not** automatically `REACHED`. The rootwalk anchors `REACHED` to an actual *runtime root*, not to an arbitrary production caller. Partial rootwalk is incompleteness and follows the default degrade doctrine.

**Port implication — the three rootwalk outcomes:**
- root reaches candidate within depth 1 ⇒ **REACHED** (overrides zero-referrer UNREACHED candidacy).
- complete enumeration, no root reaches, oracle clean ⇒ **UNREACHED**.
- any enumeration failure / skip / depth-bound-hit ⇒ **DEGRADE**.

The depth bound = 1 is a hard constant the port should encode as a named constant (mirrors §4.0 convention). Reaching the depth bound *before* resolving is itself an incompleteness signal → DEGRADE (step 5), distinct from "completed the walk and found nothing" → UNREACHED (step 4).

---

## §5 — `runtime-surface-ledger.yaml` schema + data model (FR-RSR) `[UNVERIFIED — spec-only]`

Source: RS:L61–L101.

### 5.1 Artifact location and granularity

The sweep writes `<output>/artifacts/runtime-surface-ledger.yaml` as a **per-run artifact** (RS:L63). It is **one row per evaluated EDGE**, not one row per symbol (RS:L63). This per-edge-vs-per-symbol split is the single most error-prone aspect of the data model and drives the count invariant in §5.4.

### 5.2 YAML row shape (RS:L65–L72)

```yaml
- requirement_id: <str | null>          # null is valid; tagger is symbol-anchored
  symbol: <str>                          # tagged surface symbol name-path
  edge: <str>                            # "<symbol> -> <referrer-or-entrypoint-root>"
  status: REACHED | UNREACHED | DEGRADE
  production_referrers: [<file:line>]    # surviving non-test/non-comment referrers; [] for UNREACHED
  evidence_ref: <file:line-or-artifact>  # evidence backing the verdict; re-Read by evidence-validator
```

### 5.3 `RuntimeSurfaceLedgerRow` TypedDict — field by field (RS:L77–L84)

```python
class RuntimeSurfaceLedgerRow(TypedDict):
    requirement_id: str | None
    symbol: str
    edge: str
    status: Literal["REACHED", "UNREACHED", "DEGRADE"]
    production_referrers: list[str]
    evidence_ref: str
```

| Field | Type | Meaning / port notes |
|---|---|---|
| `requirement_id` | `str \| None` | Optional. `None`/`null` is valid because the tagger is symbol-anchored, not requirement-anchored (RS:L7, L66). |
| `symbol` | `str` | The tagged surface symbol **name-path** (e.g. `MyClass/my_handler`). Stable join key for the per-symbol reduction. |
| `edge` | `str` | Formatted `"<symbol> -> <referrer-or-entrypoint-root>"` (RS:L68). One ledger row = one such edge. |
| `status` | `Literal["REACHED","UNREACHED","DEGRADE"]` | Per-EDGE status (the per-symbol verdict is derived by reduction, §5.4). |
| `production_referrers` | `list[str]` | Surviving non-test / non-comment referrers as `file:line`. **`[]` for UNREACHED** (RS:L70). |
| `evidence_ref` | `str` | `file:line` or artifact path; **re-Read by the evidence-validator** downstream (RS:L71) — so it must point at something re-readable. |

### 5.4 Per-symbol reduction precedence + count invariant

**Reduction precedence (RS:L86–L90):**

```text
DEGRADE-on-any-incompleteness > UNREACHED > REACHED
```

Read as: collapse a symbol's N edge-rows into one per-symbol verdict by taking the highest-precedence status present. **Any** single degraded edge ⇒ the whole symbol is `DEGRADE` (RS:L98). If no degrade but at least one UNREACHED edge and no REACHED rescue ⇒ `UNREACHED`. Otherwise `REACHED`.

**Count semantics (RS:L92–L98):**

- The ledger is **per-edge**; contract counts are **per-symbol** (RS:L94).
- `runtime_surface_unreached` counts **symbols** reduced to `UNREACHED`, **never edges** (RS:L95).
- **Invariant (RS:L96):** `len(unreached_surfaces) == runtime_surface_unreached` MUST hold. The list `unreached_surfaces` and the integer counter are two views of the same per-symbol UNREACHED set; the port must keep them in lockstep.
- Worked example (RS:L97): a symbol with N test-only/comment-only referrers contributes **N ledger rows** but exactly **1** to `runtime_surface_unreached` — *if* all edges are non-production AND none degrade.
- Degrade dominance (RS:L98): any degraded edge for a symbol reduces that symbol to `DEGRADE`, which sets `runtime_surface_degraded: true` and routes through **§10.6 Grounding Gaps** rather than the deviation ledger. A DEGRADE symbol is therefore **NOT** added to `unreached_surfaces` (so it does not count toward the invariant).

**Guard note (RS:L100):** the silent-no-op risk is mitigated by the asymmetric-cost default — if the sweep cannot decide (language classification, backend/tooling, root enumeration, or dynamic wiring incomplete) it MUST emit `DEGRADE` and preserve evidence rather than silently emit PASS or Regression.

**Port implication — data-model layering:**
1. Producer emits per-EDGE `RuntimeSurfaceLedgerRow[]` to YAML.
2. A reducer groups rows by `symbol`, applies `DEGRADE > UNREACHED > REACHED`, yielding a per-symbol verdict map.
3. The contract emitter derives the six `runtime_surface_*` fields (§6) from the per-symbol map, maintaining `len(unreached_surfaces) == runtime_surface_unreached` as a checkable post-condition / test assertion.

---

## §6 — The deterministic 7-step sweep, step by step `[UNVERIFIED — spec-only]`

Sources: SKILL:L465–L491 (steps 4b'/4b), RS §1–§5. The sweep is the union of two SKILL chain steps — **4b' (tagger)** and **4b (production-caller sweep)** — which together decompose into 7 deterministic stages. It runs in **UC-2 only** (never `--mode pre`) and is **LLM-free / deterministic** (SKILL:L487). It **extends** the already-fetched step-4 `find_referencing_symbols` result; it does **not** add a second referrer-fetch call (SKILL:L489).

### Step 1 — TAG (SKILL step 4b', FR-RSR.1) `[UNVERIFIED — spec-only]`

- **Inputs:** diff-hunk symbols with resolved kind/decorator from chain steps 2/2a/3; the §1 surface allowlist.
- **Decision logic:** classify each diff-hunk symbol by resolved symbol kind/decorator against the §1 allowlist (RS:L9–L15). Surface ⇒ tag it. Kind-resolution failure ⇒ `DEGRADE` (FR-RSR.3/8 → §10.6), **never** silent-skip (SKILL:L487).
- **Outputs:** `runtime_surface_requirements: [<ids>]` when mapped ids exist; a surface hunk with no mapped requirement is still tagged with `requirement_id: null` and the sweep still runs (SKILL:L487). Non-surface diff ⇒ `runtime_surface_requirements: []`, `runtime_surface_sweep_ran: false`, zero added cost (the fast path). Emits one `audit.log` row `{wave: 1, step: "4b'", timestamp, outcome, evidence_ref}` (SKILL:L487).

### Step 2 — FIND-REFERRERS (reuse step-4 result) `[UNVERIFIED — spec-only]`

- **Inputs:** the already-fetched step-4 `find_referencing_symbols <symbol> include_info:true` result for each tagged symbol (SKILL:L464, L489).
- **Decision logic:** **no new fetch.** The sweep extends the existing referrer set; `include_info:true` already carries each referrer's signature/docstring used for classification.
- **Outputs:** the candidate referrer set per tagged symbol (production-vs-test partition deferred to Step 3).

### Step 3 — PARTITION (production vs test/comment) `[UNVERIFIED — spec-only]`

- **Inputs:** the referrer set from Step 2; the §2 language table.
- **Decision logic (RS:L21–L32, SKILL:L489):** for each referrer, classify via §2 — path/test markers OR inline-test-scope markers ⇒ **test**; comment/doc-only ⇒ **excluded**; otherwise ⇒ **production**. Inline test modules count as test even in a production-path file (e.g. Rust `#[cfg(test)]`, in-file `Test*`). Unknown language / ambiguous comment-vs-test ⇒ `DEGRADE` (never UNREACHED, never "treat as production").
- **Outputs:** per symbol, the surviving `production_referrers` list and a per-edge classification.

### Step 4 — DEGRADE-ORACLE (RS §3, FR-RSR.3) `[UNVERIFIED — spec-only]`

- **Inputs:** tagged symbol, hunk text + adjacent metadata (incl. `pyproject.toml`), the §3 categories a–d.
- **Decision logic:** if ANY oracle row matches (decorator route / packaging entrypoint / registry-DI-string-dispatch / reflection-dynamic-import) ⇒ edge/symbol `DEGRADE` (RS:L36–L43). MUST be consulted before any `UNREACHED` (SKILL:L489).
- **Outputs:** DEGRADE verdict + §10.6 Grounding Gap routing for matched symbols; never increments `regression`; never blocks.

### Step 5 — ROOTWALK (RS §4, FR-RSR.4) `[UNVERIFIED — spec-only]`

- **Inputs:** every **candidate-UNREACHED** symbol (zero surviving production referrers AND oracle clean); the enumerable runtime roots.
- **Decision logic (RS:L51–L57):** enumerate roots → walk each toward candidate at depth bound 1 → reachable ⇒ `REACHED` (even with zero direct referrers); fully enumerated + unreached + oracle-clean ⇒ `UNREACHED`; any root error/skip/unenumerable/depth-bound-hit ⇒ `DEGRADE`. MUST run before emitting any `UNREACHED` (SKILL:L489, RS:L51).
- **Outputs:** final per-edge status for candidate-UNREACHED symbols (REACHED rescue, confirmed UNREACHED, or DEGRADE).

### Step 6 — REDUCE (per-symbol verdict) `[UNVERIFIED — spec-only]`

- **Inputs:** all per-edge statuses for a symbol.
- **Decision logic (RS:L86–L98):** collapse edges by precedence `DEGRADE-on-any-incompleteness > UNREACHED > REACHED`. Any degraded edge ⇒ symbol DEGRADE. Else any UNREACHED edge (no REACHED rescue) ⇒ symbol UNREACHED. Else REACHED.
- **Outputs:** one per-symbol verdict; the per-symbol UNREACHED set feeds `unreached_surfaces`; degraded symbols set `runtime_surface_degraded: true` and are NOT added to `unreached_surfaces`.

### Step 7 — EMIT (ledger + contract + audit) `[UNVERIFIED — spec-only]`

- **Inputs:** per-edge rows + per-symbol verdicts.
- **Decision logic / outputs:**
  - Write `<output>/artifacts/runtime-surface-ledger.yaml` — one `RuntimeSurfaceLedgerRow` per evaluated edge (RS:L63–L72, SKILL:L489).
  - Emit the SIX name-exact contract fields (§6 below) on EVERY path when `runtime_surface_sweep_ran: true`, including fully-REACHED runs (SKILL §9.1 MANDATORY EMISSION comment, SKILL.md:L721–L730).
  - Preserve `len(unreached_surfaces) == runtime_surface_unreached` (RS:L96, SKILL:L489).
  - Emit one `audit.log` row `{wave: 1, step: "4b", timestamp, outcome, evidence_ref}` (SKILL:L489).
  - Writes only under `<output>/`; never a clean PASS for a tagged surface whose reachability could not be evaluated; never STOPs (SKILL:L489).

### Contract field discipline (FR-RSR.7, SKILL §9.1 MANDATORY EMISSION comment, SKILL.md:L721–L730) `[UNVERIFIED — spec-only]`

When the sweep ran, the §9.1 contract MUST carry ALL SIX `runtime_surface_*` fields by exact name on every path. Per-symbol verdict → fields mapping:

| Per-symbol verdict | `runtime_surface_unreached` | `runtime_surface_degraded` | `unreached_surfaces` |
|---|---|---|---|
| REACHED | `0` (no increment) | `false` | `[]` (no entry) |
| UNREACHED | `+1` increment | `false` | `+1` entry |
| DEGRADE | no increment | `true` + §10.6 Grounding Gap | **NOT added** |

Forbidden improvised keys (SKILL §9.1 MANDATORY EMISSION comment, SKILL.md:L721–L730): `runtime_surface_reachable`, `reachability_path`, `static_caller_absent_is_expected`, bespoke `reachable: true` — all invisible to the §9.3 consumer map and break the contract. A confidently-traced dynamic path is still `runtime_surface_degraded: true` + Grounding Gap (static reachability cannot soundly prove it).

### Backend-availability / fail-open behavior (SKILL:L489) `[UNVERIFIED — spec-only]`

The sweep reads the Wave-0 §0.5d availability surface rather than re-probing. `backend: none`, a chain-degraded availability report, Serena unavailable, or a `find_referencing_symbols` failure → degrade the affected edge to §10.6 Grounding Gap, set `runtime_surface_degraded: true`, append `"runtime-surface:backend_unavailable"` to `degraded_components`, continue over remaining edges with no global abort, NEVER STOP.

---

## Gaps and Questions

1. **Six contract fields — only five are named in `refs/runtime-surface.md`.** SKILL:L489/L491 assert "ALL SIX `runtime_surface_*` fields" but the refs document explicitly names only: `runtime_surface_requirements`, `runtime_surface_sweep_ran`, `runtime_surface_unreached`, `runtime_surface_degraded`, and `unreached_surfaces` (the latter is the list, not prefixed `runtime_surface_`). The sixth field is not enumerated in either source read. **The port must obtain the canonical six-field list from the §9.1 contract spec** (likely in SKILL.md §9 or `contract.py`), not from `refs/runtime-surface.md` alone. Note `unreached_surfaces` does not carry the `runtime_surface_` prefix yet participates in the invariant — naming is not uniform.
2. **`edge` string format is loosely specified.** RS:L68 gives `"<symbol> -> <referrer-or-entrypoint-root>"` but does not fix delimiter spacing, how entrypoint roots are rendered vs `file:line` referrers, or uniqueness/dedup rules across edges. The port needs a canonical formatter + a test, since the per-edge→per-symbol grouping joins on `symbol`, not `edge`.
3. **depth=1 "§4.0 link-following depth convention" is an external reference.** RS:L54 and L2 of step 2 defer to "the §4.0 link-following depth convention" in SKILL.md, not quoted here. The port should read SKILL §4.0 to confirm whether depth=1 means "one referrer hop" vs "one file hop" vs "one symbol-edge hop" before encoding the constant.
4. **Root enumeration source is unbounded in the spec.** RS:L53 lists root *categories* (packaging entrypoints, command roots, route/router roots, "other runtime entrypoint roots visible to the protocol") but not a concrete enumeration mechanism. For Python the `[project.scripts]` table is concrete (`pyproject.toml`); for ts/js/rust/go the "command roots / route roots" enumeration is undefined — likely a per-language degrade until a concrete enumerator exists.
5. **Tagger vs oracle overlap is intentional but needs ordering in code.** Decorator-routes are both a §1 tag signal AND a §3(a) degrade trigger. The 7-step order (tag → ... → oracle at Step 4) resolves this: a decorated symbol is tagged as surface, then the oracle degrades it. The port must not let Step 1's tagging suppress Step 4's degrade.
6. **No existing `models.py` types to extend.** The reflect `models.py` defines `Verdict`, `ReflectConfig`, `ReflectResult` (enum/dataclasses) but no TypedDict and no runtime-surface types. The port introduces `RuntimeSurfaceLedgerRow` as new surface; decide whether it lands in `models.py` or a new `runtime_surface.py` module under `src/superclaude/cli/reflect/`.
7. **`evidence_ref` re-readability contract.** RS:L71 says the evidence-validator re-Reads `evidence_ref`. The port must guarantee it is always a resolvable `file:line` or an on-disk artifact path under `<output>/`, never a transient/in-memory handle.

## Stale Documentation Found

**None — and this is expected.** `refs/runtime-surface.md` is a forward-looking SPEC for a module that does not yet exist (`src/superclaude/cli/reflect/` has zero runtime-surface code, grep-confirmed across all seven files). There is no implementation for the docs to have drifted from, so no claim is "stale code." Every structural claim is legitimately `[UNVERIFIED — spec-only]`.

The single `[CODE-VERIFIED]` data point — the `pyproject.toml` `[project.scripts]` entries `superclaude = "superclaude.cli.main:main"` and `ic = "superclaude.cli.ic:main"` (RS:L45 ↔ `pyproject.toml` L67–L69) — **matches the live file exactly**; no staleness there either. (The file also carries `[project.entry-points.pytest11]` at L72–L73, consistent with the spec's category-(b) packaging-entrypoint examples.)

## Summary

The runtime-surface algorithm is a deterministic, LLM-free, UC-2-only sweep that decomposes into **7 stages** — tag, find-referrers (reuse step-4), partition, degrade-oracle, rootwalk, reduce, emit — built atop five spec sections in `refs/runtime-surface.md` and SKILL §6.1 steps 4b'/4b (SKILL:L465–L491). Its governing posture is **fail-loud asymmetric cost**: never silently PASS an untested surface, never silently Regression an idiomatic dynamic/registry/decorator/packaging/reflection entrypoint; every uncertainty maps to `DEGRADE → §10.6 Grounding Gap`.

Data model: a **per-edge** `runtime-surface-ledger.yaml` (`RuntimeSurfaceLedgerRow` TypedDict, 6 fields) reduced to a **per-symbol** verdict under precedence `DEGRADE > UNREACHED > REACHED`, surfaced through name-exact contract fields with the hard invariant `len(unreached_surfaces) == runtime_surface_unreached`. The degrade oracle (4 categories a–d), the §2 language partition table (py/rust/ts/js/go + unknown→DEGRADE), and the depth-1 entrypoint-rootwalk are the three decision engines feeding the reduction.

**Build status:** greenfield. No runtime-surface implementation exists in `src/superclaude/cli/reflect/`; existing `models.py` has no TypedDicts. The port introduces all of this as new surface. Primary open items before coding: (1) obtain the canonical SIXTH contract field from the §9.1 contract spec / `contract.py`, (2) pin the §4.0 depth=1 convention, (3) define a canonical `edge` formatter, and (4) define concrete root-enumeration for non-Python languages (likely degrade-by-default until built).

**Sections:** 9 — §1 allowlist, §2 language table, §3 degrade oracle, §4 rootwalk, §5 ledger/data model, §6 7-step algorithm + contract discipline, Gaps and Questions, Stale Documentation Found, Summary.

---

**Status: Complete**
