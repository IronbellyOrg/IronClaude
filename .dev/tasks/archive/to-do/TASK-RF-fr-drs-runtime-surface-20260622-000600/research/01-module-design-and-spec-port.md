# Research: Module Design + Spec Port

Topic type: Module design + SPEC port (File Inventory + Solution/Spec)
Scope: The greenfield module's algorithm and types — port the behavior SPEC and the TDD design for `src/superclaude/cli/reflect/runtime_surface.py`.
Status: Complete
Date: 2026-06-22

Module to design: `src/superclaude/cli/reflect/runtime_surface.py` (GREENFIELD — does not exist; grep-confirmed zero matches for `runtime_surface`/`RuntimeSurface`/`rootwalk`/`unreached_surfaces`/`ledger` across all 7 files in `cli/reflect/` per TDD §6 [CODE-VERIFIED]).

Evidence tags: `[SPEC]` = forward-looking design ported from the behavior SPEC `refs/runtime-surface.md` (cited `RS:L<n>`) or the TDD (cited `§<n>`). `[CODE-VERIFIED]` = confirmed against existing source by the TDD's own research.

---

## 1. The 6 logical units (signatures, responsibility, behavior, degrade rules)

All six live in `src/superclaude/cli/reflect/runtime_surface.py`. Signatures are pinned in TDD §8.1; the SPEC behavior each ports is in `refs/runtime-surface.md`. The 7-step algorithm (tag → find-referrers → partition → degrade-oracle → rootwalk → reduce → emit) maps to 6 units because the trailing `reduce` + `emit` steps collapse into one `reduce_ledger` unit (TDD §5.1 bridge note). Builder: ONE checklist item per unit.

### Unit 1 — `tag_surfaces` (TAG, step 1)
- **Signature** [SPEC §8.1]: `tag_surfaces(diff_hunks: list[DiffHunk], allowlist: SurfaceAllowlist) -> list[TaggedSurface]`
- **Responsibility:** Classify diff-hunk symbols as runtime surfaces by resolved symbol kind + decorator/registration against the allowlist `{py, ts, js, rust, go}`. **Symbol-anchored, NOT requirement-anchored** — `requirement_id` may be `null`; a surface hunk with no mapped requirement is still tagged and swept [SPEC RS:L7].
- **Inputs:** `diff_hunks` (the changed hunks, each carrying `added_symbols`/`decorators`/`lang`), `allowlist` (kind/decorator table).
- **Outputs:** `list[TaggedSurface]` (symbol name-path + lang + kind + optional `requirement_id` + decorators).
- **Ported behavior** [SPEC RS:L5-L17, §1 allowlist table]: per-language surface signals — Python: CLI command symbols, HTTP route handlers, Click/Typer command callbacks, decorator-registered routes (`@app.route`, `@click.command`, `@click.group`, `@*.command`, Typer command/callback); TS/JS: route/command/exported endpoint handlers + route/handler/controller decorators or call sites; Rust: command/HTTP/endpoint handlers + route/handler attributes or command-dispatch registration; Go: HTTP handlers, CLI command handlers, exported runtime endpoint functions + handler-registration idioms.
- **Degrade/uncertainty rules:** A candidate the tagger cannot classify soundly → **DEGRADE through the language-table/default oracle; NEVER silently skip a possible surface** [SPEC RS:L15, TDD §12.3 "Other-language candidate" + "Kind-resolution failure" rows]. AST kind-resolution failure on a hunk symbol → DEGRADE, never silent-skip [TDD §12.3, SKILL:L487]. Note category (a): a decorator that *qualifies* the symbol as a surface is *also* a later degrade trigger; tagging at step 1 MUST NOT suppress the step-4 oracle [TDD §12.2 CRITICAL note].
- **Fast path origin:** if `diff_hunks` yield zero tagged surfaces, the orchestrator short-circuits (FR-012, see §3 below) — `tag_surfaces` returning `[]` is the trigger.

### Unit 2 — `find_referrers` (FIND-REFERRERS, step 2)
- **Signature** [SPEC §8.1]: `find_referrers(surfaces: list[TaggedSurface], *, lsp: LspOverlay | None = None) -> list[ReferrerEdge]`
- **Responsibility:** Find referrers to each tagged surface. ripgrep `--json --sort path` + AST floor as ground truth; optional LSP/Serena overlay for precision only.
- **Inputs:** `surfaces`, optional `lsp` overlay handle.
- **Outputs:** `list[ReferrerEdge]` (symbol → referrer `file:line`, `kind=None` pre-partition).
- **Ported behavior** [SPEC RS:L21 partition source; TDD §6.1 stage table; R4 covers HOW the BFS/rg sourcing is adapted from `cli/audit`]: extend the already-fetched step-4 `find_referencing_symbols` result rather than re-fetch where available; the rg/AST floor is the deterministic engine.
- **Degrade/uncertainty rules:** **LSP overlay is NEVER load-bearing** [TDD §12.4]: the floor is ground truth; the overlay may only *prune* false positives, never be *required* to reach a verdict or flip a PASS/FAIL. LSP unavailable (binary absent / no `referencesProvider` / handshake error / `null` / cold-start partial / timeout) → DEGRADE-to-floor with an explicit auditable "degraded: LSP unavailable, fell back to floor" marker; floor verdict still reproducible [TDD §12.3 LSP row, §12.7 "No retry — degrade-to-floor immediately"]. Backend `none` / Serena down / `find_referencing_symbols` failure → degrade the affected edge, append `"runtime-surface:backend_unavailable"` to `degraded_components`, continue, NO global abort [TDD §12.3, FR-010]. ripgrep transient failure → degrade affected edge, continue (a missing scan result is incompleteness, not a clean PASS) [§12.7]. rg non-UTF-8 / `line_number == null` → tolerate `bytes` fallback + null line, do NOT silently drop a possible referrer; degrade if undecidable [§12.3].

### Unit 3 — `partition_referrers` (PARTITION, step 3)
- **Signature** [SPEC §8.1]: `partition_referrers(edges: list[ReferrerEdge], lang_table: TestCommentTable) -> PartitionedReferrers`
- **Responsibility:** Split each referrer into production vs test/inline-test/comment via the per-language table.
- **Inputs:** `edges`, `lang_table` (per-language test + comment markers).
- **Outputs:** `PartitionedReferrers` with `.production`, `.test_or_comment`, `.degraded`.
- **Ported behavior** [SPEC RS:L19-L32, §2 language table]: per-language path/test markers, inline test markers, comment syntax to exclude — py (`tests/`,`test_*.py`,`*_test.py`,`conftest.py`; `class Test*`,`def test_*`,pytest marks; `#`, docstrings), rust (`tests/`,`*_test.rs`; `#[cfg(test)]`,`mod tests`,`#[test]`; `//`,`///`,`//!`,`/* */`), ts (`tests/`,`__tests__/`,`*.test.ts`,`*.spec.ts`; `describe(`,`it(`,`test(`; `//`,`/* */`,JSDoc), js (same as ts with `.js`), go (`*_test.go`; `func Test*`/`Benchmark*`/`Example*`; `//`,`/* */`, doc-comments). **Inline test modules count as test even inside a production-path file; comment-only / documentation-only references do NOT count as production callers** [SPEC RS:L32].
- **Degrade/uncertainty rules:** Unknown/unsupported language (lang ∉ {py,ts,js,rust,go}) → **DEGRADE; NEVER UNREACHED, NEVER "treat as production"** [SPEC RS:L21,L30; TDD §12.3 "Unknown/ambiguous file type" row]. Ambiguous comment-vs-test classification → DEGRADE [SPEC RS:L21; §12.3]. The audit's UNKNOWN→SOURCE default is INVERTED here (unknown→DEGRADE) — R4 covers the data-copy detail; the *semantic* is: ambiguity is never silently production [§12.3].

### Unit 4 — `degrade_oracle` (DEGRADE-ORACLE, step 4)
- **Signature** [SPEC §8.1]: `degrade_oracle(surface: TaggedSurface, partitioned: PartitionedReferrers) -> DegradeVerdict`
- **Responsibility:** Match the 4 incompleteness categories a–d → DEGRADE when reachability cannot be soundly decided. **MUST run BEFORE any UNREACHED is emitted** [SPEC RS:L51; TDD §12.6 guarantee 1].
- **Inputs:** `surface`, `partitioned`.
- **Outputs:** `DegradeVerdict` (`degraded: bool`, `category: Literal["a","b","c","d"] | None`).
- **Ported behavior:** the 4-category oracle (full predicates in §4 below) [SPEC RS:L34-L48, §3; TDD §12.2].
- **Degrade/uncertainty rules:** default rule — every reachability uncertainty maps to `DEGRADE → §10.6 Grounding Gap`; the safe asymmetric-cost posture is fail-loud [SPEC RS:L47-L48]. DEGRADE never increments `deviation_count_by_class.regression` and never produces a blocking Regression [SPEC RS:L36].

### Unit 5 — `rootwalk_entrypoints` (ROOTWALK, step 5)
- **Signature** [SPEC §8.1]: `rootwalk_entrypoints(surface: TaggedSurface, roots: list[EntrypointRoot]) -> RootwalkResult`
- **Responsibility:** For each candidate-UNREACHED symbol, walk depth=1 from the enumerated entrypoint roots. **MUST run on every candidate-UNREACHED before UNREACHED is final** — it is the last gate that can rescue to REACHED or escalate to DEGRADE [SPEC RS:L51; TDD §12.6 guarantee 2]. Adapts `cli/audit/reachability.py:_bfs_reachable` (R4 covers the adaptation).
- **Inputs:** `surface`, `roots` (the enumerated `EntrypointRoot` set; enumeration algo I2 in §1.7 below).
- **Outputs:** `RootwalkResult` (`status: Literal["REACHED","UNREACHED","partial"]`, `hit_root`, `enumeration_complete`).
- **Ported behavior** [SPEC RS:L49-L59, §4]: (1) enumerate runtime roots — packaging entrypoints incl. `[project.scripts]`, command roots, route/router roots; (2) walk from each root toward the candidate with **depth bound = 1** (mirrors §4.0 link-following depth); (3) reachable from any root within depth → reduce to **REACHED even with zero direct production referrers**; (4) all roots enumerated, no root reaches, oracle clean → may reduce to **UNREACHED**; (5) any root errors/skipped/unenumerable OR depth bound hit before resolution → enumeration partial → **DEGRADE, never UNREACHED**. A symbol called only by other *unreached* production code is NOT automatically REACHED — REACHED anchors to an actual runtime root [SPEC RS:L59].
- **Degrade/uncertainty rules:** Partial rootwalk enumeration (root errors/skipped/unenumerable) → DEGRADE [SPEC RS:L57; §12.3]. Depth-bound (=1) hit before resolution → DEGRADE (step 5), distinct from "walked, found nothing" → UNREACHED (step 4) [§12.3]. No re-enumeration on partial — step 5 is definitional: partial enum ≡ DEGRADE [§12.7].

### Unit 6 — `reduce_ledger` (REDUCE + EMIT, steps 6+7)
- **Signature** [SPEC §8.1]: `reduce_ledger(rows: list[RuntimeSurfaceLedgerRow]) -> tuple[dict[str, str], ContractScalars]`
- **Responsibility:** Collapse per-edge rows to a per-symbol verdict under `DEGRADE > UNREACHED > REACHED`, and compute the 6 contract scalars (§8.2), enforcing the §7.4 count invariant by construction.
- **Inputs:** `rows` (per-edge `RuntimeSurfaceLedgerRow[]`).
- **Outputs:** `tuple[dict[str, str], ContractScalars]` — the per-symbol verdict map + the six `runtime_surface_*` scalars dict to merge into `return-contract.yaml`.
- **Ported behavior** [SPEC RS:L86-L98, §5; TDD §7.2, §12.5]: group rows by `symbol` (NOT by `edge`), take highest-precedence status present, derive the six scalars from the per-symbol map. Per-symbol → contract effect table: REACHED → unreached 0 / degraded false / no list entry; UNREACHED → +1 unreached / +1 list entry; DEGRADE → no increment / degraded true (+§10.6) / **NOT added to `unreached_surfaces`** [§7.2].
- **Degrade/uncertainty rules:** ANY single degraded edge dominates the whole symbol → DEGRADE [§7.2, §12.5]. The count invariant `len(unreached_surfaces) == runtime_surface_unreached` holds because both views derive from the same per-symbol UNREACHED set and DEGRADE symbols are excluded (§5 below).
- **Builder note:** EMIT-side writers (ledger YAML via `_IndentDumper` + `_atomic_write_text`; the canonical `edge` formatter) are R2's product-path concern for *where* they're called, but the formatter + sort/dedup is a pure helper in this module (see §6).

### 1.7 Root-enumeration algorithm I2 (produces the `EntrypointRoot` set step 5 starts from)
[SPEC TDD §6.1 I2; RS:L53] Scan, in FIXED order, these declared-entrypoint sources in the scope work-tree:
1. `[project.scripts]` in `pyproject.toml` (e.g. `superclaude = "superclaude.cli.main:main"`) — [CODE-VERIFIED] `pyproject.toml:68-69`, same source oracle cat (b) cites.
2. `[project.entry-points.*]` groups in `pyproject.toml` (plugin/console-script entry-point tables).
3. CLI command roots registered via the project's command framework (Click/Typer group/command roots reachable from the script entrypoints in 1–2).

Each declared entrypoint → one `EntrypointRoot` (`{root_id, kind, target}`), sorted lexicographically by `root_id` for determinism (NFR-001). **Completeness check (gates REACHED vs DEGRADE-on-partial):** enumeration is "complete" only when every source scanned without error AND every declared entrypoint resolved to a `module:symbol` target. ANY source errors / unreadable / unresolvable target → `enumeration_complete = false` → candidate-UNREACHED symbol DEGRADEs (an incomplete root set could hide a real reach path). Confirmed UNREACHED ONLY on complete enumeration with no depth=1 root hit; any root hit → REACHED; any partial → DEGRADE [SPEC RS:L57; §12.3 "Partial rootwalk enumeration" row].

---

## 2. Every DESIGNED type (compact field shape + dataclass-vs-TypedDict)

All types are GREENFIELD — defined in `runtime_surface.py`; none exist in `cli/reflect/` today [TDD §6, §8.1.1 CODE-VERIFIED]. Builder: ONE checklist item per type (12 designed + 3 modeled). The TDD says "as dataclasses or TypedDicts" [§8.1.1] — recommended kind per type below; the load-bearing constraint is the field shape, not the mechanism.

### 2.1 Input types
| Type | Recommended kind | Compact shape [SPEC §8.1.1] | Notes |
|---|---|---|---|
| `DiffHunk` | dataclass (frozen) | `{ file: str, lang: str, added_symbols: list[str], hunk_text: str, decorators: list[str] }` | One changed hunk; `added_symbols` = enclosing symbol name-paths the tagger classifies. Produced by diff-acquisition step I1 (R2 owns I1). |
| `SurfaceAllowlist` | config dataclass / module-const | `{ langs: frozenset[str] = {"py","ts","js","rust","go"}, kind_decorator_table: dict[str, list[str]] }` | Static config, NOT per-run. Lang outside `langs` → DEGRADE-tag, never silent-skip [SPEC RS:L15]. |
| `TestCommentTable` | config dataclass / module-const | `{ per_lang: dict[str, {test_prefixes: tuple[str,...], test_infixes: tuple[str,...], comment_markers: tuple[str,...]}] }` | Per-language partition data; DATA-copied from audit `filetype_rules.py:106-107` (`_TEST_PREFIXES`/`_TEST_INFIXES`) with default INVERTED (unknown→DEGRADE, not SOURCE) [TDD §8.1.1; R4 owns the copy]. |
| `LspOverlay` | **opaque pass-through** | opaque handle to the Serena/LSP referrer provider | The ONLY genuine opaque type — floor never inspects internals; either returns refined referrers or is `None` → DEGRADE-to-floor [§8.1.1, §12.4 D3/R4]. Shape owned by the overlay adapter, not this module. |

### 2.2 Intermediate types
| Type | Recommended kind | Compact shape [SPEC §8.1.1] | Notes |
|---|---|---|---|
| `TaggedSurface` | dataclass | `{ symbol: str, lang: str, kind: str, requirement_id: str | None, decorators: list[str] }` | Confirmed surface (or DEGRADE-tagged); symbol-anchored so `requirement_id` may be `null` [§7.1.1]. |
| `ReferrerEdge` | dataclass | `{ symbol: str, referrer: str (file:line), kind: Literal["production","test","comment","unknown"] | None }` | One symbol→referrer edge; `kind=None` pre-partition (set by `partition_referrers`). Maps 1:1 onto a ledger `edge`. |
| `PartitionedReferrers` | dataclass | `{ production: list[ReferrerEdge], test_or_comment: list[ReferrerEdge], degraded: list[ReferrerEdge] }` | `.degraded` holds ambiguous/unclassifiable referrers — never silently treated as production. |
| `EntrypointRoot` | dataclass | `{ root_id: str, kind: Literal["project_script","entry_point","cli_command"], target: str (module:symbol) }` | One enumerated runtime root (I2, §1.7). `root_id` is the sort key + the `root:{root_id}` operand of root edges. |
| `RootwalkResult` | dataclass | `{ status: Literal["REACHED","UNREACHED","partial"], hit_root: str | None, enumeration_complete: bool }` | `partial` / `enumeration_complete == false` → DEGRADE (never UNREACHED); a root hit → REACHED. |
| `DegradeVerdict` | dataclass | `{ degraded: bool, category: Literal["a","b","c","d"] | None }` | Oracle output; `category` names which incompleteness fired (§4). |

### 2.3 Output / modeled types
| Type | Recommended kind | Compact shape | Notes |
|---|---|---|---|
| `RuntimeSurfaceLedgerRow` | **TypedDict** | `{ requirement_id: str | None, symbol: str, edge: str, status: Literal["REACHED","UNREACHED","DEGRADE"], production_referrers: list[str], evidence_ref: str }` | [SPEC RS:L77-L84; TDD §7.1.2] In-memory rep of one per-EDGE ledger row. `None ⇄` YAML `null`. `production_referrers` MUST be `[]` for UNREACHED [RS:L70]. `evidence_ref` must be re-readable `file:line`/`<output>/` artifact (NFR-006). |
| `UnreachedSurface` | TypedDict (matches contract) | `{ symbol: str, requirement_id: str | None, evidence_ref: str }` (minimum) | [SPEC TDD §7.1.3 M3] One entry per UNREACHED symbol. Minimal PINNED triple; super-shape owned by SKILL.md §9.1. Emitter keys on these EXACT names. DEGRADE-only / fully-REACHED run → `[]`. |
| `ContractScalars` | TypedDict | the six canonical fields (§7) | [SPEC §8.1.1] The reducer's emitted scalar set; merged verbatim into `return-contract.yaml`. Keyed on the EXACT six names (§7 prefix caveat). |
| `SweepResult` | **TypedDict** | `{ ledger_rows: list[RuntimeSurfaceLedgerRow], scalars: ContractScalars, ledger_path: str | None }` | [SPEC §8.1.2] `run_sweep` return value, consumed at `runner.py:445`. `ledger_path` is `None` on the non-surface fast path. |

**Mechanism guidance:** TypedDict for the YAML-mirroring rows + scalar dicts (they round-trip to/from YAML and need string keys) — `RuntimeSurfaceLedgerRow`, `UnreachedSurface`, `ContractScalars`, `SweepResult`. dataclasses for the in-memory intermediates passed between units (`DiffHunk`, `TaggedSurface`, `ReferrerEdge`, `PartitionedReferrers`, `EntrypointRoot`, `RootwalkResult`, `DegradeVerdict`) and config (`SurfaceAllowlist`, `TestCommentTable`). `LspOverlay` stays an opaque `typing` alias / Protocol. This is a recommendation [SPEC]; the pinned constraint is the field shape.

---

## 3. `run_sweep` orchestrator (signature + unit wiring + fast path)

[SPEC §8.1.2] Single entry point called by BOTH the product path (Phase 2, `runner._audit_once`) and the eval path (Phase 3, grader). Pinned signature:

```python
def run_sweep(
    diff: str,                      # unified diff/patch text of the change under audit (I1)
    base_ref: str,                  # git base the diff is computed against (reused across fix-loop re-audits)
    scope_worktree: Path,           # work-tree root supplying the referrer search space
    tasklist: Path,                 # MDTM tasklist for requirement→surface linkage (requirement_id may be null)
    output_dir: Path,               # <output>/ — ledger to <output>/artifacts/, contract merged at <output>/return-contract.yaml
    availability_surface: dict,     # Wave-0 §0.5d backend/tool availability (drives DEGRADE-to-floor; D3/R4)
    *,
    lsp: LspOverlay | None = None,  # optional precision overlay; None → rg/AST floor only
) -> "SweepResult": ...
```

**Wiring of the 6 units (fixed 7-stage order):**
1. Acquire `diff_hunks` from `diff` (diff-parse, step I1 — R2 owns the acquisition seam).
2. `tagged = tag_surfaces(diff_hunks, allowlist)`.
3. **FAST PATH (FR-012)** [SPEC RS:L17; TDD §12.3 "Non-surface diff" row]: if `tagged == []` → short-circuit BEFORE any referrer work. Return `SweepResult(ledger_rows=[], scalars={runtime_surface_requirements: [], runtime_surface_sweep_ran: False, runtime_surface_ledger_path: None, runtime_surface_unreached: 0, runtime_surface_degraded: False, unreached_surfaces: []}, ledger_path=None)`. Write NO ledger file; add ZERO referrer-analysis cost. (Also the `--mode pre` guard: sweep is UC-2-only, never runs on `--mode pre` → `sweep_ran: false` [§12.3].)
4. `edges = find_referrers(tagged, lsp=lsp)`.
5. `partitioned = partition_referrers(edges, lang_table)`.
6. For each tagged surface: `degrade_oracle(surface, partitioned)`; if not degraded AND it is candidate-UNREACHED → `rootwalk_entrypoints(surface, roots)` where `roots` come from I2 (§1.7). Build per-edge `RuntimeSurfaceLedgerRow[]` from these results (with the canonical `edge` formatter, §6).
7. `verdict_map, scalars = reduce_ledger(rows)`; set `scalars["runtime_surface_sweep_ran"] = True`, `runtime_surface_ledger_path = <output>/artifacts/runtime-surface-ledger.yaml`.
8. EMIT: write the per-edge ledger YAML (via `_IndentDumper` + `_atomic_write_text` — R2/NFR-004/005); return `SweepResult(ledger_rows=rows, scalars=scalars, ledger_path=...)`.

**Arg construction at `_audit_once` (runner.py:394-453)** [SPEC §8.1.2; R2 owns the seam detail]: `diff`/`base_ref` from `ReflectConfig` audit inputs (same `--base` reused per fix-loop re-audit, NFR-002); `scope_worktree`/`output_dir` from `ReflectConfig` (`output_dir` backs `ReflectConfig.contract_path`, models.py:96); `tasklist` from the audited task path; `availability_surface` from the Wave-0 probe on the config. Invoked post-launch / pre-`parse_contract`; `scalars` merge-overwrite the six keys before any consumer parses.

> **[CODE-CONTRADICTED by R2 / gap-fill round 1 — see research/09]:** The TDD paraphrase above is only PARTIALLY right. Verified against `models.py:57-98` and `config.py:123-256`: ONLY `base_ref`←`config.base`, `tasklist`←`config.tasklist_path`, and `output_dir`←`config.output_dir` map to actual `ReflectConfig` fields. `ReflectConfig` has **NO** `diff`-text field, **NO** `scope_worktree` field, and **NO** Wave-0 `availability_surface` probe — those three args must be CONSTRUCTED at the seam: `diff` via `git diff <config.base>` (single-ref working-tree diff, runner.py:350-356 de-range rule); `scope_worktree` via git toplevel of `config.tasklist_path.parent` (the `git_cwd` precedent, config.py:185); `availability_surface = {}` (force-floor v1) + `lsp=None` (D3/R4: rg/AST floor is ground truth, LSP optional). The original sentence is retained above for provenance; this note supersedes its arg-source claims for `diff`/`scope_worktree`/`availability_surface`.

---

## 4. Degrade-oracle — 4 categories (a–d) with deterministic match predicates

[SPEC RS:L34-L48 §3; TDD §12.2] Matching ANY row → `DEGRADE`. The oracle runs BEFORE any `UNREACHED` can be emitted (step ordering §8). Static referrer analysis is semi-decidable for runtime wiring (even Pysa misses `importlib`/`getattr`/`eval`), so these are deterministic *detections of incompleteness*, not reachability proofs.

| Cat | Name | Deterministic match predicate (what the sweep DETECTS) | Verdict |
|---|---|---|---|
| **(a)** | Decorator routes / command decorators | Tagged symbol OR adjacent hunk carries route/command decorators: `@app.route`, router route decorators, `@click.command`, `@click.group`, `@*.command`, Typer command/callback decorators. Detection triggers also include `flatten_attr`→`None` (unresolvable dotted decorator) and decorator aliasing (`r = app.route; @r(...)`) [TDD §12.2]. | DEGRADE → §10.6 |
| **(b)** | Packaging entrypoints | Tagged symbol named by `[project.scripts]`, `[project.entry-points.*]`, console-scripts-equivalent metadata, or equivalent packaging entrypoint declarations. In-repo case: `superclaude = "superclaude.cli.main:main"`, `ic = "superclaude.cli.ic:main"` [SPEC RS:L45, CODE-VERIFIED pyproject.toml]. | DEGRADE → §10.6 |
| **(c)** | Registry / DI / string dispatch | Tagged symbol appears as the registered object OR string value/key in a registry assignment/call, DI-container binding, command map, plugin table, or string-dispatch table visible in the hunk or adjacent metadata. Triggers: `funcs[name]()`, `REGISTRY[key]()`, string-keyed dispatch [TDD §12.2]. | DEGRADE → §10.6 |
| **(d)** | Reflection / dynamic import | Tagged symbol reached via visible reflection/dynamic-import: `importlib.import_module(...)`, `__import__(...)`, `getattr(<module>, "<symbol>")`, entry-point/plugin `load()`, `eval`/`exec`, `from x import *`, or name-based lookup where the symbol/module is data [SPEC RS:L43; TDD §12.2]. | DEGRADE → §10.6 |

**CRITICAL overlap** [SPEC TDD §12.2]: category (a) overlaps the §1 surface tagger — a decorator that *qualifies* a symbol as a surface is simultaneously a *degrade* trigger (static analysis cannot prove the decorator-registered route is wired at runtime). The 7-step order (tag at step 1 → oracle at step 4) resolves this: tagging MUST NOT suppress the later degrade. Default rule: every reachability uncertainty → `DEGRADE → §10.6 Grounding Gap`; `runtime_surface_degraded: true`; never increment `regression`; never block [SPEC RS:L47-L48].

---

## 5. Reduction precedence + count invariant (holds by construction)

### 5.1 Per-symbol reduction precedence [SPEC RS:L86-L90; TDD §7.2, §12.5]
Edge rows for a given `symbol` collapse to ONE per-symbol verdict by taking the **highest-precedence status present**:
```text
DEGRADE-on-any-incompleteness  >  UNREACHED  >  REACHED
```
| Condition over a symbol's N edge rows | Per-symbol verdict |
|---|---|
| ANY single edge is DEGRADE | DEGRADE (degrade dominance, RS:L98) |
| No degrade, ≥1 UNREACHED edge, no REACHED rescue | UNREACHED |
| Otherwise (root/rescue reached the symbol, incl. zero direct referrers but root-reachable at depth 1) | REACHED |

Per-symbol verdict → contract effect [SPEC §7.2; SKILL.md:727-729]: REACHED → `runtime_surface_unreached` 0, `degraded` false, NO `unreached_surfaces` entry. UNREACHED → +1 `unreached`, +1 list entry. DEGRADE → no increment, `degraded` true (+§10.6 Grounding Gap), **NOT added to `unreached_surfaces`**.

### 5.2 Count invariant [SPEC RS:L96; TDD §7.4, §12.5, AC-3]
`len(unreached_surfaces) == runtime_surface_unreached` MUST hold on every run.
**How it holds BY CONSTRUCTION:** `runtime_surface_unreached` (int) and `unreached_surfaces` (list) are TWO VIEWS of the SAME per-symbol UNREACHED set — the reducer derives both from one pass over `verdict_map` filtered to `status == UNREACHED`. The int is `len()` of that set; the list is one `UnreachedSurface` per member. DEGRADE symbols are EXCLUDED from `unreached_surfaces`, so they cannot perturb the invariant. It is *computed*, never *asserted on LLM output*. Worked example [SPEC RS:L97]: a symbol with N test-only/comment-only referrers → N ledger rows but exactly 1 to `runtime_surface_unreached`, ONLY IF all edges are non-production AND none degrade (any degraded edge dominates → DEGRADE, not UNREACHED). Eval case id 41 (`uc2-surface-test-only-ref`) hosts this assertion [TDD §4.1, FR-008]. It is a unit/contract-boundary post-condition mirroring `contract.py`'s `_LOAD_BEARING_BOOL_FIELDS` fail-closed block (contract.py:200-209) [TDD §7.4].

---

## 6. Canonical `edge` formatter + determinism levers

### 6.1 Canonical edge formatter [SPEC TDD §7.1.1a; RS:L68]
`format_edge(symbol, target) -> f"{symbol} -> {target}"` — a PURE function. Pinned rules (resolves OQ-EDGE; enables the R3/§12.4 golden-file byte-compare test):
| Rule | Specification |
|---|---|
| Delimiter | the literal ` -> ` — one ASCII space, hyphen, greater-than, one ASCII space. NO tabs, NO Unicode arrow, NO variable spacing. |
| Left operand | `symbol` — the tagged surface symbol name-path verbatim (e.g. `MyClass/my_handler`). |
| Right operand (referrer edge) | the referrer as `file:line` (POSIX-relative path, colon, 1-based line). |
| Right operand (entrypoint-root edge) | `root:{root_id}` where `root_id` = `EntrypointRoot.root_id` — distinguishes a root edge from a referrer edge unambiguously. |
| Dedup | de-duplicate on the EXACT `(symbol, target)` tuple; identical edges collapse to one row. |
| Sort | sort the final row list lexicographically by the formatted `edge` string (ASCII codepoint order) BEFORE YAML dump. |

### 6.2 Determinism levers (NFR-001) [SPEC TDD §12.4]
- **ripgrep ordering:** ALWAYS invoke `rg --json --sort path` — default rg is multi-threaded / non-deterministic; `--sort path` implies `--threads=1` + lexicographic order (`--sort-files` is deprecated).
- **Sort-before-dump:** sort the ledger rows by formatted `edge` (6.1) before YAML emit; deterministic key ordering in scalar dicts.
- **AST decorator resolver:** branch on `Name`/`Attribute`/`Call`; never read `.id` without an `isinstance` guard; match BOTH `ast.FunctionDef` AND `ast.AsyncFunctionDef`; `flatten_attr`→`None` is the DEGRADE signal.
- **LSP never load-bearing:** floor (rg/AST) = ground truth; LSP may only prune false positives, never required to reach a verdict or flip PASS/FAIL non-reproducibly.
- **No wall-clock/random/PID/env-ordering value** may enter the structured path (NFR-001). Golden-file test asserts byte-identical ledger across ≥3 runs (AC-2).

---

## 7. The six contract scalars (EXACT names) + the prefix caveat

[SPEC TDD §8.2; SKILL.md §9.1 lines 731-736] Emitted under MANDATORY-EMISSION (all six, exact names, on REACHED/DEGRADE/UNREACHED alike) when `runtime_surface_sweep_ran` is true.

| # | Field (EXACT name) | Type | Semantics |
|---|---|---|---|
| 1 | `runtime_surface_requirements` | `list[str]` | surface requirement ids tagged from symbol kind/decorator; `[]` when none. |
| 2 | `runtime_surface_sweep_ran` | `bool` | `true` ONLY when ≥1 tagged surface triggered the sweep. |
| 3 | `runtime_surface_ledger_path` | `str | null` (abs path) | `<output>/artifacts/runtime-surface-ledger.yaml`; `null` when sweep did not run. |
| 4 | `runtime_surface_unreached` | `int` (symbol count) | count of SYMBOLS reduced to UNREACHED; `0` on a fully-REACHED run. GATING via the §5.3 derivation (see below). |
| 5 | `runtime_surface_degraded` | `bool` | `true` when ≥1 symbol reduced to DEGRADE (→ §10.6 Grounding Gap); `false` on fully-REACHED. |
| 6 | `unreached_surfaces` | `list[UnreachedSurface]` | one entry per UNREACHED symbol; `[]` on REACHED and DEGRADE-only runs. Bound to field 4 by the §5.2 count invariant. |

**CRITICAL PREFIX CAVEAT** [SPEC TDD §8.2; G4]: only **5 of the 6** fields carry the literal `runtime_surface_` prefix. The 6th, **`unreached_surfaces`**, is a list with NO prefix. A naive `startswith("runtime_surface_")` filter would SILENTLY DROP it. Every consumer AND the reducer's own emit/test code MUST key on the EXACT six names, never a prefix glob.

**§5.3 pre-filter derivation note** [SPEC FR-006; SKILL.md:402/412]: the §5.3 forbid-STOP pre-filter does NOT read the integer `runtime_surface_unreached` directly — it gates on a DERIVED string field `surface_unreached`. A derivation sets `surface_unreached = "runtime_surface_unreached"` (literal string) when the sweep emits integer `runtime_surface_unreached ≥ 1` from a SUCCESSFUL sweep; REACHED/degrade-only → `surface_unreached` stays `null`. Derivation owner is R2/R3's seam (the sweep / reflect-CLI wrapper writes it alongside the six scalars at `runner._audit_once`); flagged here only so the data-model keys on the literal six and the producer/derivation boundary is explicit. R3 owns the §5.3 wiring.

---

## 8. Step ordering that enforces the asymmetric posture

[SPEC TDD §12.6; RS:L36, L51] The 7-step order IS the error-handling control flow. Two ordering guarantees prevent a silent wrong verdict:
1. **Degrade-oracle (step 4) MUST be consulted BEFORE any UNREACHED is emitted** [RS:L36, SKILL:L489].
2. **Rootwalk (step 5) MUST run on every candidate-UNREACHED before UNREACHED is final** — it is the last gate that can rescue to REACHED or escalate to DEGRADE [RS:L51].

Governing posture (preserved from FR-RSR safety logic, NOT re-derived) [SPEC TDD §12.1; RS:L47-L48]: never silently PASS an untested surface; never silently Regression an idiomatic dynamic/registry/decorator/packaging/reflection entrypoint; every uncertainty → `DEGRADE → §10.6 Grounding Gap`; never STOP / never global-abort (degrade the affected EDGE, continue over remaining edges).

---

## 9. Builder checklist-item map (granular per-unit / per-type decomposition)

Suggested granular items (the builder may split further):
- **Module scaffold:** create `src/superclaude/cli/reflect/runtime_surface.py` (UV-only, ruff-format clean — FR-013/NFR-007).
- **15 type items:** one per designed type (§2.1: `DiffHunk`, `SurfaceAllowlist`, `TestCommentTable`, `LspOverlay`; §2.2: `TaggedSurface`, `ReferrerEdge`, `PartitionedReferrers`, `EntrypointRoot`, `RootwalkResult`, `DegradeVerdict`; §2.3: `RuntimeSurfaceLedgerRow`, `UnreachedSurface`, `ContractScalars`, `SweepResult`) — `RuntimeSurfaceLedgerRow`/`UnreachedSurface` are the pre-modeled ones.
- **6 unit items:** `tag_surfaces`, `find_referrers`, `partition_referrers`, `degrade_oracle`, `rootwalk_entrypoints`, `reduce_ledger` (§1) — each item carries its degrade rules.
- **2 helper items:** `format_edge` pure formatter + dedup/sort (§6.1); root-enumeration I2 helper producing `EntrypointRoot[]` (§1.7).
- **1 orchestrator item:** `run_sweep` wiring + the FR-012 non-surface fast path (§3).
- **1 invariant item:** count-invariant post-condition assertion in `reduce_ledger` (§5.2).

**Cross-researcher boundaries (do not duplicate):** R2 owns I1 diff-acquisition + the `_audit_once` merge-overwrite seam + ledger write-call site; R3 owns the `surface_unreached` derivation + §5.3 pre-filter wiring; R4 owns the rg/AST + `_bfs_reachable` + `_TEST_*`/`_DYNAMIC_PATTERNS` sourcing & data-copy; R5 eval; R7 tests; R8 MDTM template. THIS file owns: the 6 unit WHAT, the 15 types, `run_sweep`, the oracle predicates, reduction/invariant, the formatter, the six scalars.

---

## Summary

This research delivers the complete implementable design of the greenfield, pure-Python, LLM-free module `src/superclaude/cli/reflect/runtime_surface.py`:

1. **6 logical units** with pinned signatures (§8.1), responsibilities, inputs/outputs, ported SPEC behavior, and per-unit degrade rules — `tag_surfaces`, `find_referrers`, `partition_referrers`, `degrade_oracle`, `rootwalk_entrypoints`, `reduce_ledger` (§1), plus the root-enumeration algorithm I2 (§1.7).
2. **15 designed types** with compact field shapes and dataclass-vs-TypedDict guidance (§2): 4 inputs, 6 intermediates, 4 output/modeled, + the opaque `LspOverlay`.
3. **`run_sweep` orchestrator** (§3): pinned signature, 7-stage unit wiring, and the FR-012 non-surface fast path returning the six scalars with `sweep_ran:false` and no ledger.
4. **Degrade-oracle 4 categories a–d** with deterministic match predicates and the (a)↔tagger overlap resolution (§4).
5. **Reduction precedence `DEGRADE > UNREACHED > REACHED`** + the count invariant `len(unreached_surfaces) == runtime_surface_unreached` holding by construction (two views of one per-symbol UNREACHED set, DEGRADE excluded) (§5).
6. **Canonical `edge` formatter** `f"{symbol} -> {target}"` + determinism levers (`rg --json --sort path`, dedup on `(symbol,target)`, sort-before-dump) (§6).
7. **The six contract scalars by exact name** + the CRITICAL prefix caveat (only 5/6 carry `runtime_surface_`; `unreached_surfaces` does not) (§7).
8. **Step ordering** guarantees (oracle before UNREACHED; rootwalk before final UNREACHED) (§8), and a builder checklist-item map (§9).

All claims tagged [SPEC] (forward-looking design from `refs/runtime-surface.md` RS:L line numbers + TDD §-numbers) or [CODE-VERIFIED] (the few seam facts the TDD's research confirmed against existing source: greenfield module absence, `pyproject.toml:68-69` `[project.scripts]`, `reachability.py:_bfs_reachable`, `contract.py:200-209`, `models.py:96`).

Status: Complete
