# Research 05 — Reuse & Import Boundaries (Reuse Scout)

**Task:** TASK-TDD-20260621-124414 (FR-DRS Deterministic Runtime-Surface Sweep)
**Date:** 2026-06-21
**Investigation type:** Reuse Scout (re-confirm + refresh)
**Inputs read first:** `research/reuse-audit.yaml` (machine verdicts), `research-notes.md` `## REUSE_AUDIT`.
**Method:** Every verdict backed by a `[CODE-VERIFIED]` file:line neighbour read from actual source under
`/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/`.

**Scope:** prior-art neighbours for all 6 proposed components of the new `cli/reflect/runtime_surface.py`
module (surface-tagger, referrer-finder, partitioner, degrade-oracle, entrypoint-rootwalk, ledger-writer)
+ the reflect→audit import boundary.

**Verdict outcome (re-confirmed, unchanged from `reuse-audit.yaml`):** no proposed component is a
confident-duplicate. 5 of 6 are `distinct`; entrypoint-rootwalk is `reuse-by-import` (strongest overlap,
S_reuse 0.81) but shape-divergent and must be adapted, never dropped in.

| # | Component | Tier | Verdict | Disposition |
|---|-----------|------|---------|-------------|
| 1 | surface-tagger | distinct | distinct | reflect-local; reuse language constants only |
| 2 | referrer-finder | maybe-related (shape-divergent) | distinct | mirror fail-open tiering; symbol-level local impl |
| 3 | partitioner | distinct | distinct | reflect-local; reuse marker LISTS, invert default |
| 4 | degrade-oracle | maybe-related | distinct | reuse dynamic-import regex DATA; 4-cat oracle local |
| 5 | entrypoint-rootwalk | maybe-related (shape-divergent) | **reuse-by-import** | adapt `_bfs_reachable`: depth=1 + DEGRADE-on-partial |
| 6 | ledger-writer | distinct | distinct | reflect-local; reuse `IndentDumper` + `_atomic_write_text` only |

---

## 1. Surface symbol tagger → `distinct` (S_reuse 0.37)

**Capability:** classify diff-hunk symbols as runtime surfaces by language-specific symbol kind +
decorator/registration evidence.

**Nearest prior art (CODE-VERIFIED):**
- `src/superclaude/cli/audit/wiring_gate.py:164` `_safe_parse(file_path) -> ast.Module | None` — Python-only
  `ast.parse` with `SyntaxError`/`OSError`/`UnicodeDecodeError` → `None` fail-soft. [CODE-VERIFIED]
- `src/superclaude/cli/audit/filetype_rules.py:1-13` — file-type table doc lists source set
  `.py,.ts,.js,.jsx,.tsx,.go,.rs,.java`; this is a FILE-extension table, not a symbol-kind classifier. [CODE-VERIFIED]
- `src/superclaude/cli/audit/dead_code.py:37-49` `_FRAMEWORK_HOOK_PATTERNS` — name-substring heuristics
  (`pytest_`, `conftest`, `plugin`, `middleware`, `hook`, `signal`, `celery`, `task`, `command`) for
  framework-exported symbols. [CODE-VERIFIED]

**Similarity tier:** distinct. **Verdict:** distinct. **S_reuse:** 0.37 (confirmed).

**Why distinct:** `_safe_parse` returns a whole-module AST and is Python-only; it neither slices diff hunks,
resolves hunk-local symbols, nor detects Click/Typer/registry decorators. `dead_code` hook-patterns match on
filename/symbol-NAME substrings, not on decorator AST or registration-call evidence. The audit code has no
multi-language symbol-kind notion. The tagger must parse a *diff/patch*, map changed lines back to enclosing
symbols across py/ts/js/rust/go, and read decorator/registration evidence — none of which exists in audit.

**Disposition:** implement reflect-local in `runtime_surface.py`. Optionally lift the small language-extension
constants from `filetype_rules.py` after reconciling semantics; reuse `_safe_parse`'s fail-soft *pattern*
(return-None-on-parse-error) but not the function (it is wiring-gate-scoped).

---

## 2. Referrer finder → `distinct` (maybe-related, shape-divergent, S_reuse 0.67)

**Capability:** find symbol referrers across the repo with structured analysis when available + fail-open grep
evidence on tool loss.

**Nearest prior art (CODE-VERIFIED):**
- `src/superclaude/cli/audit/dependency_graph.py:1-14` — module docstring: "3-tier dependency graph with
  confidence labels from static and grep evidence." [CODE-VERIFIED]
- `src/superclaude/cli/audit/dependency_graph.py:5-8` — Tier-A = AST-resolved imports (high confidence),
  Tier-B = grep string references (medium), Tier-C = co-occurrence/naming (low). [CODE-VERIFIED]
- `src/superclaude/cli/audit/dependency_graph.py:27-39` `EdgeTier` enum + `TIER_CONFIDENCE` map
  (A=0.90, B=0.65, C=0.35) — the fail-open confidence-tiering primitive worth mirroring. [CODE-VERIFIED]
- Imports `FileAnalysis` from `tool_orchestrator` (`dependency_graph.py:24`) — the graph is built over
  per-FILE analyses, confirming file-level granularity. [CODE-VERIFIED]

**Similarity tier:** maybe-related. **Verdict:** distinct (shape-divergent). **S_reuse:** 0.67 (confirmed).

**Why distinct despite high overlap:** the audit graph is **FILE-level** import/reference graphing keyed on
`FileAnalysis` — its edges connect files, not symbols. The referrer-finder must resolve *symbol*-level
referrers (callers of a specific function/class) and then partition them production/test/comment. The
fail-open static→grep tiering (Tier-A AST / Tier-B grep, with confidence labels) is the right *shape* to
mirror, but the audit implementation cannot be imported as a symbol finder: its granularity, its
`FileAnalysis` dependency, and its DELETE-classification policy (`dependency_graph.py:10` "Tier-C edges never
promote to DELETE") are all cleanup-audit semantics that do not transfer.

**Disposition:** mirror-shape the tier model (AST-high / grep-medium, confidence-labelled, grep is the
fail-open floor) but implement a SYMBOL-level finder locally. Do NOT drop-in `dependency_graph`.

---

## 3. Production-vs-test partitioner → `distinct` (S_reuse 0.57)

**Capability:** classify referrer evidence production/test/inline-test/comment via per-language path+syntax
rules.

**Nearest prior art (CODE-VERIFIED):**
- `src/superclaude/cli/audit/filetype_rules.py:105-107` `_TEST_PREFIXES = ("test_", "spec_")`,
  `_TEST_INFIXES = (".test.", ".spec.", "_test.", "_spec.")` — the reusable filename-marker LISTS. [CODE-VERIFIED]
- `src/superclaude/cli/audit/filetype_rules.py:110-131` `classify_file_type()` — test detection first
  (prefix, infix, then `/tests/` `/test/` path containment), highest priority over extension. [CODE-VERIFIED]
- `src/superclaude/cli/audit/filetype_rules.py:143-144` — **"Default to source for unknown" → `return
  FileType.SOURCE`.** This is the inverted-default that does NOT transfer. [CODE-VERIFIED]

**Similarity tier:** distinct. **Verdict:** distinct. **S_reuse:** 0.57 (confirmed).

**Why distinct — the semantic inversion:** the audit classifier defaults UNKNOWN/ambiguous → SOURCE
(`filetype_rules.py:144`). The runtime-surface partitioner requires the OPPOSITE asymmetric-cost default:
unknown/ambiguous → DEGRADE (never silently treat an unclassifiable referrer as production-proving SOURCE).
Reusing `classify_file_type` directly would import the wrong default and could let an ambiguous referrer
falsely satisfy production-reachability. The audit classifier also has no notion of (a) inline-test scope
(test code inside a production file), or (b) comment/docstring exclusion — both required by
`runtime-surface.md` §2.

**Disposition:** reuse the `_TEST_PREFIXES`/`_TEST_INFIXES` marker LISTS (and the path-containment markers)
as DATA only, after reconciling semantics. Re-implement classification with unknown→DEGRADE default +
inline-test + comment/docstring exclusion locally.

---

## 4. Degrade oracle → `distinct` (maybe-related, S_reuse 0.68)

**Capability:** turn static incompleteness + dynamic/runtime registration evidence into a DEGRADE verdict
(not an unsafe pass / not a Regression).

**Nearest prior art (CODE-VERIFIED):**
- `src/superclaude/cli/audit/dynamic_imports.py:1-13` — docstring: "Dynamic-import-safe classification policy
  with **KEEP:monitor default** … Files referenced via dynamic imports receive KEEP:monitor, never DELETE."
  [CODE-VERIFIED]
- `src/superclaude/cli/audit/dynamic_imports.py:24-39` `_DYNAMIC_PATTERNS` — the reusable regex pattern DATA
  (`js_dynamic_import`, `js_require_variable`, `py_import_builtin` `__import__`, `py_importlib`
  `importlib.import_module`, `py_importlib_util`, `glob_import`, `webpack_require_context`). [CODE-VERIFIED]
- `src/superclaude/cli/audit/dead_code.py:30-35` `_ENTRY_POINT_FILENAMES` (`__init__.py`, `index.js`,
  `server.js`, …) + `dead_code.py:155-163` entrypoint exclusion ("Exclusion: entry points → excluded with
  reason `entry_point`"). [CODE-VERIFIED]

**Similarity tier:** maybe-related. **Verdict:** distinct. **S_reuse:** 0.68 (confirmed).

**Why distinct — the verdict mapping differs:** `dynamic_imports` maps a dynamic-import match to cleanup's
**KEEP:monitor**, not to runtime-surface's **DEGRADE**. The regex *detector* is reusable as pattern data; the
4-category oracle (a–d in `runtime-surface.md` §3) that turns matches into DEGRADE is a separate decision
surface. Likewise, audit entrypoint detection is **filename-pattern** based (`dead_code.py:30-35`), whereas
the runtime-surface oracle resolves `[project.scripts]`/entry-point *metadata* (e.g.
`superclaude = "superclaude.cli.main:main"` per `runtime-surface.md:45`) — a richer, packaging-aware notion.

**Disposition:** reuse the `_DYNAMIC_PATTERNS` regex DATA where convenient; implement the 4-category DEGRADE
oracle separately with its own verdict mapping. Do not import the KEEP:monitor classifier.

---

## 5. Entrypoint rootwalk (depth=1) → `reuse-by-import` — STRONGEST overlap (S_reuse 0.81)

**Capability:** enumerate runtime roots + bounded static walk toward a candidate symbol; emit
REACHED/UNREACHED/DEGRADE with fail-open.

**Nearest prior art (CODE-VERIFIED):**
- `src/superclaude/cli/audit/reachability.py:1-12` — module docstring: "AST call-chain reachability analyzer
  for wiring manifest validation … BFS from the entry-point function to compute the full reachable set."
  [CODE-VERIFIED]
- `src/superclaude/cli/audit/reachability.py:374` `class ReachabilityAnalyzer` — AST call-graph + BFS,
  manifest-driven (`__init__` loads `entry_points, targets` from a wiring manifest, `:385-388`). [CODE-VERIFIED]
- `src/superclaude/cli/audit/reachability.py:591-624` `_bfs_reachable(graph, start, target) -> (bool,
  call_chain)` — pure BFS over a resolved `dict[str, set[str]]` call graph, returns reachability + path.
  This internal is the strongest reuse target. [CODE-VERIFIED]

**Two confirmed domain mismatches (both CODE-VERIFIED):**
1. **Dynamic-dispatch → UNREACHABLE, not DEGRADE.** `reachability.py:26-33` documents that calls via
   `getattr()`, `**kwargs`, string-based dispatch / registry lookups (`REGISTRY[key]()`) are invisible to
   static AST and "The analyzer will report these targets as **UNREACHABLE** even if they execute at
   runtime." Runtime-surface requires such uncertainty to **DEGRADE**, never UNREACHED
   (`runtime-surface.md:47,57`). [CODE-VERIFIED both sides]
2. **depth>50 guard vs contract depth=1.** `reachability.py:460` uses `if depth > 50: … return` for
   recursive module parsing. The rootwalk contract is a depth bound of **1** (`runtime-surface.md:54`:
   "with a depth bound of **1**"). [CODE-VERIFIED both sides]
   Additionally: `_bfs_reachable` itself is **unbounded** (it BFSes the whole resolved graph until target or
   queue-exhaustion, `reachability.py:607-624`) — there is no depth parameter on the BFS at all, so depth=1
   must be enforced by the caller/graph construction, not by the BFS internal.

Further: reachability is **Python-only + wiring-manifest-required** (`:385-388` loads a manifest); the
rootwalk is **multi-language + symbol-anchored** with roots enumerated from packaging entrypoints /
command roots / route roots (`runtime-surface.md:53`). And critically, on partial enumeration
(`runtime-surface.md:57`: "If any root errors, is skipped, cannot be enumerated, or the depth bound is hit
before resolution … the verdict is `DEGRADE`, never `UNREACHED`") the rootwalk must DEGRADE — reachability
has no such partial-enumeration→DEGRADE doctrine; it reports a binary reachable/unreachable.

**Similarity tier:** maybe-related (shape-divergent). **Verdict:** **reuse-by-import** (strongest, S_reuse
0.81). **Adapt — do NOT drop-in.**

**Disposition:** the `_bfs_reachable` BFS skeleton (deque, visited-set, path accumulation) is small, stable,
and directly applicable. EITHER reuse-by-import the BFS internal OR copy/adapt the ~30-line skeleton — but in
both cases the adaptation MUST (a) enforce depth=1 at the call site, and (b) convert every partial-enumeration
/ dynamic-dispatch uncertainty into DEGRADE rather than UNREACHED. If reused long-term by import, the boundary
risk below applies (it couples reflect's product path to cleanup-audit). Preferred long-term shape: extract a
boundary-neutral BFS helper (see §7 Option B).

---

## 6. Ledger writer + contract-scalar computer → `distinct` (S_reuse 0.56)

**Capability:** emit the per-edge runtime-surface YAML ledger + reduce rows into the 6 return-contract scalars
with the count invariant.

**Nearest prior art (CODE-VERIFIED):**
- `src/superclaude/cli/reflect/ensemble.py:500-509` `_emit_reflect_contract(path, contract)` — a simple,
  reflect-LOCAL YAML artifact writer (`yaml.safe_dump(..., sort_keys=False)`, mkdir parent, unlink-on-None).
  Generic boilerplate, not a behavioural duplicate. [CODE-VERIFIED]
- `src/superclaude/cli/reflect/contract.py:65-71` `parse_contract(path) -> dict | None` — defensive
  return-contract.yaml reader (None on missing/unparseable; tolerates unknown top-level fields). The CONSUMER
  side, not a writer duplicate. [CODE-VERIFIED]
- `src/superclaude/cli/reflect/runner.py:58-67` `_IndentDumper(yaml.SafeDumper)` overriding `increase_indent`
  for yamllint-conformant block sequences (`indent-sequences: true`), and `runner.py:70` `_atomic_write_text`
  (randomized same-dir temp + `os.replace`, parallel-session-safe). [CODE-VERIFIED]

**Similarity tier:** distinct. **Verdict:** distinct. **S_reuse:** 0.56 (confirmed).

**Why distinct:** the ledger row type (`RuntimeSurfaceLedgerRow`, `runtime-surface.md:77-84`), the per-symbol
reduction precedence (`DEGRADE-on-any-incompleteness > UNREACHED > REACHED`, `runtime-surface.md:55-59`), and
the 6-scalar computation with the `len(unreached_surfaces) == runtime_surface_unreached` count invariant are
all FR-DRS-specific behaviour absent from any neighbour. `_emit_reflect_contract` is a one-liner YAML dump;
`parse_contract` reads, it does not compute scalars. None reduce ledger rows.

**Disposition:** implement the row type + per-symbol reduction + 6-scalar computation directly from
`runtime-surface.md`. Reuse ONLY the generic YAML *style*: the `_IndentDumper` (yamllint-safe sequences; see
`mem:reference_yamllint_indent_sequences_pyyaml`) and `_atomic_write_text` for overwrite-atomicity. These are
already reflect-local (same package) so reuse here carries no cross-package boundary cost.

---

## 7. Reflect → audit import-boundary decision (THREE options for the TDD to weigh)

**The mechanical fact (CODE-VERIFIED — confirmed across all four reflect modules):**
- `runner.py:8-9` (in "Isolation guardrails"): "No imports from `superclaude.cli.sprint` or
  `superclaude.cli.roadmap`." [CODE-VERIFIED]
- `config.py:7-10`: same two-package ban + "Imports nothing from `commands.py`/`runner.py`/`contract.py`."
  [CODE-VERIFIED]
- `models.py:8-12`: same `sprint`/`roadmap` ban (NFR-1 thinness) + types-only intra-package rule.
  [CODE-VERIFIED]
- `__init__.py:1-30`: lists only intra-`reflect` imports; no audit reference either way. [CODE-VERIFIED]

**Conclusion:** the documented import ban names **`cli/sprint` and `cli/roadmap` ONLY**. There is **no ban on
`cli/audit`** in any reflect module docstring. Therefore importing `superclaude.cli.audit.*` from
`runtime_surface.py` is **mechanically legal** — it violates no stated guardrail and no lint/structure gate.
The decision is a *coupling-quality* judgement, not a legality one.

The TDD (§6.4 Key Design Decisions / §21 Alternatives / §22 Open Questions) must weigh THREE options:

### Option A — import `cli/audit` directly
`from superclaude.cli.audit.reachability import ReachabilityAnalyzer` (or the `_bfs_reachable` internal).
- **Pro:** zero new code for the BFS; single source of truth for the algorithm; lowest immediate LOC.
- **Con (the core tradeoff):** **mechanically legal but couples reflect's PRODUCT path to cleanup-audit
  semantics.** `cli/audit` is the `sc:cleanup-audit` heuristic surface — its defaults (UNKNOWN→SOURCE,
  dynamic→KEEP:monitor, dynamic-dispatch→UNREACHABLE, depth>50) are the OPPOSITE of runtime-surface's
  asymmetric-cost doctrine (unknown→DEGRADE, dynamic→DEGRADE, partial→DEGRADE, depth=1). A future change to
  audit heuristics (driven by cleanup needs) would silently alter reflect's gating behaviour. Reaching into a
  private internal (`_bfs_reachable`) also depends on an unexported symbol.

### Option B — extract a boundary-neutral shared helper
Move the pure BFS skeleton into a neutral location (e.g. `superclaude.cli.pipeline.*` or a small
`graph_bfs` util) that BOTH audit and reflect import; keep all DEGRADE/depth semantics in the respective
callers.
- **Pro:** one BFS implementation, no product↔cleanup coupling; the neutral helper carries no policy. Matches
  the established reflect decoupling pattern (callable interfaces, e.g. sprint executor avoids `TurnLedger`
  import via a callable — `research-notes.md` PATTERNS_AND_CONVENTIONS).
- **Con:** a refactor touching `cli/audit` (extract + re-point `reachability.py`), larger diff, needs its own
  regression coverage; arguably over-engineering for a ~30-line BFS.

### Option C — reflect-local copy
Copy/adapt the ~30-line BFS skeleton into `runtime_surface.py` with depth=1 + DEGRADE-on-partial baked in.
- **Pro:** zero cross-package coupling; reflect owns its semantics entirely; smallest blast radius; mirrors
  how `runner.py:14-17` already copies `_IndentDumper` locally rather than importing the private symbol from
  `recommend.cache` ("lower coupling than importing the private symbol"). [CODE-VERIFIED precedent]
- **Con:** ~30 lines of BFS duplicated; the two copies could drift (low risk — BFS is stable).

**Recommended option (for the TDD to ratify, not a silent choice): Option C (reflect-local copy)** for v1,
with Option B noted as the clean long-term shape if a second reflect consumer of graph-BFS appears. Rationale:
(1) the in-repo precedent at `runner.py:14-17` already chose copy-over-import for exactly this
"private-symbol-coupling" reason; (2) the semantic divergence (depth=1, DEGRADE-on-partial,
dynamic-dispatch→DEGRADE) is large enough that the adapted BFS is barely the same function — importing the
audit version then overriding its defaults is more fragile than owning ~30 lines; (3) it keeps reflect's
product/gating path fully decoupled from cleanup-audit heuristic drift, honouring the asymmetric-cost
posture. Option A is the one to AVOID despite being the lowest-LOC path, precisely because the coupling is
silent and semantics-inverted.

---

## Gaps and Questions

- **G1 (TDD §6.4/§21/§22):** the import-boundary decision (Option A/B/C above) is the single most load-bearing
  design choice and must be surfaced as an explicit Key Design Decision + Alternative + Open Question, never a
  silent pick. Recommended: Option C; Option B as long-term.
- **G2:** whether to lift the `_DYNAMIC_PATTERNS` regexes and `_TEST_PREFIXES`/`_TEST_INFIXES` marker lists as
  *shared constants* (a small `audit`-side import of DATA only) vs copy them into reflect. These are pure
  data, not behaviour — but importing them still creates a reflect→audit edge. Recommend copy (data is tiny,
  keeps the boundary clean); flag for TDD §18 Dependencies.
- **G3 (deferred to research 02, OQ-DRS.1):** the referrer engine's structured-analysis tier (Serena/LSP vs
  AST) is an engine choice, not a reuse choice — out of scope here; the reuse verdict (mirror fail-open
  tiering, symbol-level local) holds regardless of which structured engine is chosen.
- **G4:** `_bfs_reachable` is a private (underscore) symbol; Option A would import an unexported internal,
  which is a stability risk independent of the coupling concern. Reinforces Option C/B over A.

## Stale Documentation Found

- None. All six `reuse-audit.yaml` neighbour citations and the `research-notes.md` `## REUSE_AUDIT` summary
  re-verified against current source with matching file:line evidence. Two minor refinements (not staleness,
  added precision):
  - `reuse-audit.yaml` cites `reachability.py:591` for `_bfs_reachable`; confirmed the BFS body spans
    `:591-624` and is **unbounded** (no depth parameter) — depth=1 must be enforced by the caller, a nuance
    worth carrying into the TDD beyond the line cited.
  - `reuse-audit.yaml` cites `filetype_rules.py:110` for `classify_file_type`; the load-bearing inverted
    default is specifically `:143-144` ("Default to source for unknown"), now pinned exactly.
- The reflect import-ban docstrings (`runner.py:8-9`, `config.py:7-10`, `models.py:8-12`) are current and
  consistent; `__init__.py` carries no ban statement (it is a re-export surface) — consistent with the
  guardrails living in the module docstrings, not the package init.

## Summary

Re-confirmed all six verdicts against live source; none changed. **surface-tagger = distinct** (0.37),
**referrer-finder = distinct** (maybe-related, shape-divergent, 0.67), **partitioner = distinct** (0.57),
**degrade-oracle = distinct** (maybe-related, 0.68), **entrypoint-rootwalk = reuse-by-import** (STRONGEST,
0.81; adapt `_bfs_reachable` with depth=1 + DEGRADE-on-partial), **ledger-writer = distinct** (0.56). No
confident-duplicate exists.

The reflect→audit import is **mechanically legal** — reflect's documented import ban names `cli/sprint` and
`cli/roadmap` ONLY (verified in `runner.py`, `config.py`, `models.py` docstrings; `__init__.py` carries no
ban). Importing `cli/audit` violates no guardrail but couples reflect's product/gating path to cleanup-audit
heuristic semantics whose defaults are the inverse of runtime-surface's asymmetric-cost doctrine. Presented as
three weighable options (A import directly / B extract boundary-neutral helper / C reflect-local copy);
**recommended: Option C** for v1 (matches the in-repo `_IndentDumper` copy-over-import precedent at
`runner.py:14-17`, keeps the boundary decoupled), with Option B as the clean long-term shape and **Option A to
be avoided** despite lowest LOC.
