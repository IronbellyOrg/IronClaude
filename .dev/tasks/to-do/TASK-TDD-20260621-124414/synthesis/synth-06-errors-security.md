# Synthesis 06 — Sections 12 (Error Handling & Edge Cases) + 13 (Security Considerations)

**Task:** TASK-TDD-20260621-124414 (FR-DRS Deterministic Runtime-Surface Sweep)
**Target TDD sections:** 12. Error Handling & Edge Cases · 13. Security Considerations
**Source research:** `01-runtime-surface-algorithm.md`, `05-reuse-and-boundaries.md`, `02-product-path-integration.md`, `00-prd-extraction.md`, `web-01-ast-ripgrep.md`, `web-02-lsp-referrers.md`

> **Authoring note:** §12 is the CENTRAL section of this design. The sweep's entire safety value is its
> handling of uncertainty: every reachability ambiguity collapses to a deterministic `DEGRADE → §10.6
> Grounding Gap` rather than a silent PASS or a silent Regression. §13 is intentionally LIGHT — the module
> is a local-only, network-free, secrets-free filesystem writer.

---

## 12. Error Handling & Edge Cases

### 12.1 Governing posture — fail-loud asymmetric cost

The sweep is `[UNVERIFIED — spec-only]` greenfield code (`runtime-surface.md` is a SPEC to build; no
implementation exists in `src/superclaude/cli/reflect/` — research 01 §0, research 02). Its single governing
rule for every error and edge case:

| Posture rule | Meaning | Forbidden opposite |
|---|---|---|
| **Never silently PASS an untested surface** | A tagged runtime surface whose reachability cannot be soundly decided MUST NOT be emitted as clean/REACHED | Emitting `REACHED`/clean on uncertainty |
| **Never silently Regression an idiomatic dynamic entrypoint** | A decorator-/registry-/reflection-/packaging-wired symbol that static analysis cannot prove MUST NOT be reported as a blocking Regression | Incrementing `deviation_count_by_class.regression` on an idiomatic dynamic surface |
| **Every uncertainty → `DEGRADE → §10.6 Grounding Gap`** | All four uncertainty categories, all tool failures, all classification gaps collapse to one deterministic outcome | `UNREACHED` or "treat as production" on incompleteness |
| **Never STOP / never global-abort** | The sweep degrades the affected EDGE and continues over the remaining edges | Halting the whole audit on one bad edge |

`DEGRADE` sets `runtime_surface_degraded: true`, routes the finding to **§10.6 Grounding Gaps**, and
**never** increments `regression` and **never** blocks (research 01 §3, RS:L36–L47).

### 12.2 The degrade oracle — 4 categories (a–d) as the error/edge-case table

Rationale (RS:L36, web-01 Finding 6, web-02): static referrer analysis is **semi-decidable** for runtime
wiring — even Meta's Pysa misses `importlib`/`getattr`/`eval`. Matching ANY row below yields `DEGRADE`. The
oracle runs BEFORE any `UNREACHED` can be emitted (precedence in §12.6).

| Cat | Uncertainty source | Deterministic match predicate (what the sweep detects) | Web-research trigger | Outcome |
|---|---|---|---|---|
| **(a)** | **Decorator routes / command decorators** | Tagged/adjacent hunk carries route/command decorators: `@app.route`, router route decorators, `@click.command`, `@click.group`, `@*.command`, Typer command/callback decorators | `flatten_attr`→`None` (unresolvable dotted decorator); decorator aliasing `r = app.route; @r(...)` (web-01 F2/F3/F6) | `DEGRADE → §10.6` |
| **(b)** | **Packaging entrypoints** | Tagged symbol named by `[project.scripts]`, `[project.entry-points.*]`, console-scripts-equivalent metadata, or equivalent packaging entrypoint declarations | `[project.scripts]` metadata (e.g. `superclaude = "superclaude.cli.main:main"`) — `[CODE-VERIFIED]` against `pyproject.toml` (research 01 §3) | `DEGRADE → §10.6` |
| **(c)** | **Registry / DI / string dispatch** | Tagged symbol appears as the registered object or string value/key in a registry assignment/call, DI-container binding, command map, plugin table, or string-dispatch table in the hunk/adjacent metadata | dispatch tables `funcs[name]()`, `REGISTRY[key]()`, string-keyed dispatch (web-01 F6; research 05 §5 reachability mismatch) | `DEGRADE → §10.6` |
| **(d)** | **Reflection / dynamic import** | Tagged symbol reached via visible reflection/dynamic-import: `importlib.import_module(...)`, `__import__(...)`, `getattr(<module>, "<symbol>")`, entry-point/plugin `load()`, name-based lookup where symbol/module is data | `getattr`/`setattr`, `importlib.import_module`/`__import__`, `eval`/`exec`, `from x import *` (web-01 F6, Recommendation 4) | `DEGRADE → §10.6` |

> **CRITICAL:** Category (a) overlaps the §1 surface tagger — a decorator that *qualifies* a symbol as a
> surface is simultaneously a *degrade* trigger, because static analysis cannot prove the decorator-registered
> route is wired at runtime. The 7-step order (tag at Step 1 → oracle at Step 4) resolves this: tagging must
> NOT suppress the later degrade (research 01 §3 port implication, Gap 5).

### 12.3 Edge-case table — every uncertainty → deterministic outcome

| Scenario / uncertainty | Source of incompleteness | Expected deterministic behavior | Test case |
|---|---|---|---|
| Dynamic dispatch / reflection (`getattr`/`importlib`/`eval`/`__import__`) | Oracle cat (d) — irresolvable by `ast`+`rg` in principle (web-01 F6) | `DEGRADE → §10.6`; `runtime_surface_degraded: true`; `regression` NOT incremented | Hunk with `getattr(mod, "h")()` → degraded true, regression 0 |
| Registry / DI / string-dispatch table membership | Oracle cat (c) | `DEGRADE → §10.6`; not UNREACHED, not Regression | `REGISTRY["x"] = handler` adjacent → degraded true |
| Decorator-aliasing / unresolvable dotted decorator | Oracle cat (a); `flatten_attr`→`None` (web-01 F2/F3) | `DEGRADE → §10.6` | `r = app.route; @r("/x")` → degraded true |
| Packaging entrypoint (`[project.scripts]`/entry-points) | Oracle cat (b) | `DEGRADE → §10.6`; never UNREACHED solely for missing static caller | `superclaude = "...:main"` console script → degraded true |
| `star-import` (`from m import *`) in scope | Oracle cat (d) referrer-invisibility (web-01 F6) | `DEGRADE → §10.6` | Module with `from x import *` referencing surface → degraded true |
| **Unknown / ambiguous file type** | §2 language table miss (lang ∉ {py,ts,js,rust,go}) | `DEGRADE` — **never** UNREACHED, **never** "treat as production" (RS:L21, research 05 §3 inverted default: audit's UNKNOWN→SOURCE does NOT transfer) | A `.kt`/`.rb` referrer → degraded true |
| **'Other' language candidate the tagger cannot classify** | §1 allowlist miss — unclassifiable surface | `DEGRADE` via language-table/default oracle; **never silently skip a possible surface** (RS:L15) | Surface in unsupported lang → degraded true, not dropped |
| Ambiguous comment-vs-test classification | §2 partition cannot decide an axis | `DEGRADE` (never UNREACHED, never production) (RS:L21) | Doc-comment-only ref that could be a call → degraded true |
| **Partial rootwalk enumeration** (root errors / skipped / unenumerable) | §4 rootwalk step 5 — incompleteness | `DEGRADE`, **never** `UNREACHED` (RS:L57, research 05 §5) | One runtime root errors during enum → degraded true |
| **Depth bound (=1) hit before resolution** | §4 rootwalk — incompleteness distinct from "walked, found nothing" | `DEGRADE` (step 5), NOT `UNREACHED` (step 4) | Candidate beyond depth-1 from all roots → degraded true |
| **LSP / language-server unavailable** (binary absent / no `referencesProvider` / handshake error / `null` / cold-start partial subset / timeout) | OQ-DRS.1 optional overlay (web-02 F5/F6/F7) — availability is multi-valued | `DEGRADE` to ripgrep/AST floor; emit explicit auditable "degraded: LSP unavailable, fell back to floor" marker; floor verdict still reproducible | LSP returns same-file-only subset → degrade-to-floor marker emitted |
| Backend `none` / chain-degraded availability / Serena down / `find_referencing_symbols` failure | Wave-0 §0.5d availability surface (research 01 backend-availability) | Degrade affected edge to §10.6; `runtime_surface_degraded: true`; append `"runtime-surface:backend_unavailable"` to `degraded_components`; continue, NO global abort | `backend: none` → edge degraded, sweep continues |
| Python source unparseable (`SyntaxError`/`OSError`/`UnicodeDecodeError`) | AST parse failure (research 05 §1 `_safe_parse` fail-soft pattern) | Return-`None` fail-soft → affected symbol DEGRADE, never silent-skip | Malformed `.py` hunk → degraded true |
| ripgrep non-UTF-8 referrer (base64 `bytes` key) or `line_number == null` | rg `--json` wire schema (web-01 F4) | Parser tolerates `bytes` fallback + null line numbers; do not silently drop a possible referrer → degrade if undecidable | Binary-ish match line → handled, not dropped |
| Kind-resolution failure on a diff-hunk symbol | Step 1 TAG cannot resolve symbol kind/decorator | `DEGRADE` (FR-RSR.3/8 → §10.6), **never** silent-skip (SKILL:L487) | Hunk symbol with unresolved kind → degraded true |
| **Non-surface diff (fast path)** | No tagged surface at all | `runtime_surface_requirements: []`, `runtime_surface_sweep_ran: false`, **zero** added cost — short-circuit before any referrer work (RS:L17) | Pure-docs diff → sweep_ran false, no ledger rows |
| `--mode pre` invocation | Sweep is UC-2-only | Sweep does NOT run (`runtime_surface_sweep_ran: false`); never on `--mode pre` (SKILL:L487) | `--mode pre` → no sweep |

### 12.4 Determinism guarantees (error-avoidance by construction)

| Lever | Rule | Source |
|---|---|---|
| ripgrep ordering | Always invoke `rg --json --sort path` — default rg is multi-threaded / non-deterministic; `--sort path` implies `--threads=1`, lexicographic order (`--sort-files` is deprecated) | web-01 F5, Rec 3/5 |
| Golden-file determinism test | Golden-file the `--json --sort path` output; assert byte-identical across repeated runs in CI (AC-2: pass across ≥3 runs, no variance) | web-01 Rec 5, prd §6 AC-2 |
| AST decorator resolver | Branch on `Name`/`Attribute`/`Call`; never read `.id` without an `isinstance` guard; match `ast.FunctionDef` AND `ast.AsyncFunctionDef`; `flatten_attr`→`None` is the DEGRADE signal | web-01 F2/F3, Rec 1/2 |
| LSP overlay is never load-bearing | Floor (ripgrep/AST) = ground truth; LSP may only *prune* false positives, never *required* to reach a verdict or flip a PASS/FAIL non-reproducibly | web-02 Rec 5, OQ-DRS.1 conclusion |

### 12.5 Per-symbol reduction precedence (edge-case resolution rule)

When a symbol has N edge-rows (the ledger is **per-edge**; counts are **per-symbol** — research 01 §5.4),
collapse to one per-symbol verdict by taking the highest-precedence status present:

```text
DEGRADE-on-any-incompleteness  >  UNREACHED  >  REACHED
```

| Reduction rule | Outcome |
|---|---|
| **ANY** single degraded edge | Whole symbol → `DEGRADE`; sets `runtime_surface_degraded: true`; routes §10.6; **NOT** added to `unreached_surfaces` |
| No degrade, ≥1 UNREACHED edge, no REACHED rescue | Symbol → `UNREACHED`; `+1` to `runtime_surface_unreached`; `+1` entry in `unreached_surfaces` |
| Otherwise (REACHED rescue, incl. zero direct referrers but root-reachable at depth 1) | Symbol → `REACHED`; no increment; no list entry |

> **Worked example (RS:L97):** a symbol with N test-only/comment-only referrers contributes **N ledger rows**
> but exactly **1** to `runtime_surface_unreached` — *only if* all edges are non-production AND none degrade.
> Any one degraded edge dominates → the symbol is DEGRADE, not UNREACHED.

**Count invariant (hard post-condition, AC-3):** `len(unreached_surfaces) == runtime_surface_unreached` MUST
hold **by construction** (computed, never asserted on LLM output). DEGRADE symbols are excluded from
`unreached_surfaces`, so they do not perturb the invariant (research 01 §5.4, prd AC-3).

### 12.6 Step ordering that enforces the asymmetric posture

The 7-step sweep order is itself the error-handling control flow (research 01 §6): **tag → find-referrers →
partition → degrade-oracle → rootwalk → reduce → emit**. The two ordering guarantees that prevent a silent
wrong verdict:

1. **Degrade-oracle (Step 4) MUST be consulted before any `UNREACHED` is emitted** (RS:L36, SKILL:L489).
2. **Rootwalk (Step 5) MUST run on every candidate-`UNREACHED` before `UNREACHED` is final** — it is the last
   gate that can rescue to `REACHED` or escalate to `DEGRADE` (RS:L51).

### 12.7 Retry & recovery strategy

| Failure | Strategy | Rationale |
|---|---|---|
| LSP cold-start partial / timeout | **No retry** — degrade-to-floor immediately | Floor is deterministic + always available; retry would reintroduce index-warmth nondeterminism (web-02 F5/F6) |
| ripgrep transient failure | Degrade affected edge; continue | Asymmetric-cost: a missing scan result is an incompleteness, not a clean PASS |
| AST parse failure | Fail-soft return-`None` → symbol DEGRADE | Mirrors `_safe_parse` pattern (research 05 §1) |
| Partial root enumeration | Degrade edge; **no** re-enumeration | Step 5 is definitional: partial enum ≡ DEGRADE (RS:L57) |

There is no network, no rate-limit, and no remote service in this module, so the template's
network-timeout/5xx/backoff rows do not apply (see §13).

---

## 13. Security Considerations

> **LIGHT section.** FR-DRS is a local-only, deterministic, pure-Python module. It performs no network I/O,
> fronts no production service, processes no credentials/PII, and exposes no API. Its only side effect is
> writing two local files under the run's `<output>/` directory. The standard web-app threat surfaces
> (authn/authz, CSRF, XSS, SQLi, data-residency) are **not applicable**.

### 13.1 Threat Model

| Threat | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Path traversal / write outside `<output>/` | L | L | All writes scoped to `<output>/return-contract.yaml` (merge) and `<output>/artifacts/runtime-surface-ledger.yaml` (sibling), resolved via `ReflectConfig.contract_path` + a parallel `ledger_path` property — single pinned location, no user-supplied path joined unsanitized (research 02) |
| Partial / corrupt file on concurrent runs | L | L | Atomic writes via `_atomic_write_text` (randomized same-dir temp + `os.replace`); parallel-session last-write-wins (research 02, research 05 §6) |
| Untrusted referrer/AST content executed | L | L | The sweep **parses** source via `ast.parse` and scans via ripgrep — it **never** `eval`/`exec`/imports the audited code; reflection patterns are *detected as DEGRADE triggers*, never invoked (web-01 F6) |
| Secret leakage into ledger/contract | L | L | Ledger rows carry only `symbol`, `edge`, `status`, `file:line` referrers, and `evidence_ref` paths — no env/secret material; no network egress to exfiltrate to |
| Supply-chain via new dependency | L | L | No new runtime dependency: stdlib `ast` + the already-present ripgrep binary; reuse-by-import/copy stays intra-repo (research 05 §7 — reflect→audit boundary is the only coupling question, and is mechanically legal) |

### 13.2 Security posture summary

| Property | Value |
|---|---|
| **Network access** | None — no HTTP, no remote service, no MCP egress required (LSP overlay is local + optional) |
| **Production service exposure** | None — dev/CI-time reflect-audit tool only |
| **Secrets / credentials handled** | None |
| **PII / sensitive data** | None — operates on the diff under audit + the work-tree source already on disk |
| **Persisted output** | Two local files, atomic, scoped to `<output>/` (contract merge + `artifacts/` ledger) |
| **Code execution of audited source** | None — static parse/scan only; dynamic constructs are detected, never run |
| **Input validation** | Fail-soft parse (`_safe_parse` pattern); tolerant ripgrep `--json` parsing (base64 `bytes` / null line-number guards, web-01 F4); unknown/ambiguous → DEGRADE, never trusted |

### 13.3 Data Governance & Compliance

Not applicable. No regulated data (GDPR/CCPA/HIPAA/PCI-DSS), no data residency constraints, no retention
obligations — the module reads local source and writes local run artifacts that follow the existing reflect
output lifecycle. No new compliance surface is introduced by FR-DRS.

---

## Coverage confirmation

**All 4 degrade-oracle categories captured** in §12.2 and §12.3:

- **(a)** Decorator routes / command decorators → DEGRADE
- **(b)** Packaging entrypoints (`[project.scripts]` / entry-points) → DEGRADE
- **(c)** Registry / DI / string dispatch → DEGRADE
- **(d)** Reflection / dynamic import (`getattr`/`importlib`/`eval`/`__import__`) → DEGRADE

Plus the additional uncertainty rows required by the brief: unknown/ambiguous file type, 'other' language,
partial rootwalk enumeration, depth-bound-hit, and LSP/server-unavailable — all mapping to
`DEGRADE → §10.6 Grounding Gap`, under the asymmetric fail-loud posture (never silently PASS an untested
surface; never silently Regression an idiomatic dynamic/registry/decorator/reflection/packaging entrypoint).
Per-symbol reduction precedence (`DEGRADE > UNREACHED > REACHED`) included as the edge-case resolution rule
with the `len(unreached_surfaces) == runtime_surface_unreached` invariant. Web-research determinism triggers
(`--sort path`; LSP-unavailable→DEGRADE; `getattr`/`importlib`/`eval`/`star-import`/decorator-aliasing→DEGRADE)
incorporated.
