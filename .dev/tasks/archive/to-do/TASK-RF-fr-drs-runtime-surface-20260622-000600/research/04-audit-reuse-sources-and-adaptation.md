# Research 04 — cli/audit Reuse Sources + Adaptation Semantics (Patterns & Conventions + Doc Cross-Validator)

**Researcher:** R4 (of 8) — FR-DRS deterministic runtime-surface sweep
**Date:** 2026-06-22
**Status:** Complete
**Owns:** ONLY the cli/audit source code being copied/adapted + inversion semantics + the boundary-decision evidence. Does NOT cover module algorithm (R1), product seam (R2), contract consumer (R3), eval (R5), SKILL (R6), tests (R7), template (R8).

**Evidence tags:** `[CODE-VERIFIED]` = read in this session; line numbers re-verified 2026-06-22.

---

## TL;DR for the builder

The TDD mandates **copy/adapt, NEVER import** (§6.4 D1 = Option C; §21 Alt 3). The builder writes items that:

1. **Copy** `_bfs_reachable` (~30-line BFS skeleton) into the new reflect-local `runtime_surface.py`, with TWO inversions baked in: **(a) depth=1 enforced at the call site**, **(b) partial-enumeration / dynamic-dispatch → DEGRADE, never UNREACHED**.
2. **Copy as DATA** the test-marker LISTS and dynamic-import regex patterns, then **invert the default**: audit's `unknown→SOURCE` and `dynamic→KEEP:monitor` both become **`→DEGRADE`** in runtime-surface.
3. **Mirror the `_safe_parse` fail-soft AST pattern** (return `None` on parse error, never raise).
4. Reuse the **reflect-local** `_IndentDumper` + `_atomic_write_text` (zero boundary cost) for the ledger writer — NOT the ensemble's bare `yaml.safe_dump`.

The boundary is sound: the reflect import ban names ONLY `cli/sprint` + `cli/roadmap`, so a `cli/audit` import is *mechanically legal* but a **coupling liability** (audit defaults are the semantic inverse of runtime-surface). The in-repo `runner.py:14-17` copy-over-import precedent (`_IndentDumper`) ratifies Option C.

---

## 1. `_bfs_reachable` — full body + the depth=1 + DEGRADE-on-partial adaptation

### 1.1 Source (verbatim) — `cli/audit/reachability.py:591-635` `[CODE-VERIFIED]`

Signature (`:591-596`):

```python
def _bfs_reachable(
    self,
    graph: dict[str, set[str]],
    start: str,
    target: str,
) -> tuple[bool, list[str]]:
```

Full body (`:604-635`):

```python
        if start == target:
            return True, [start]

        visited: set[str] = set()
        # Queue entries: (current_node, path_so_far)
        queue: deque[tuple[str, list[str]]] = deque()
        queue.append((start, [start]))
        visited.add(start)

        while queue:
            current, path = queue.popleft()

            for neighbor in graph.get(current, set()):
                if neighbor in visited:
                    continue

                new_path = [*path, neighbor]

                # Exact match
                if neighbor == target:
                    return True, new_path

                # Suffix match: target "a.b.c.func" matches neighbor ...
                if self._is_target_match(neighbor, target):
                    return True, new_path

                visited.add(neighbor)
                queue.append((neighbor, new_path))

        return False, []
```

`deque` is imported at `reachability.py:49` (`from collections import deque`) `[CODE-VERIFIED]`.

### 1.2 Three load-bearing facts the adaptation MUST invert `[CODE-VERIFIED]`

| Fact | Where (audit) | Audit doctrine | Runtime-surface doctrine (required inversion) |
|------|---------------|----------------|-----------------------------------------------|
| **UNBOUNDED BFS** | `_bfs_reachable:591-635` has **NO depth parameter** — only `graph`, `start`, `target`. It walks the entire reachable closure. | walks to arbitrary depth | **depth=1 enforced at the CALL SITE** (the BFS internal cannot self-limit). §6.3 note + §21 Alt 3 Con(A): "`_bfs_reachable` is itself unbounded (no depth parameter), so depth=1 must be enforced by the caller regardless." |
| **`depth > 50` guard is NOT in the BFS** | `reachability.py:460` `if depth > 50:` lives in **`_parse_module_recursive` (`:454-462`)** — the recursive *module-import* parse, a DIFFERENT method. | bounds recursive import-following at 50 | irrelevant to the BFS; do NOT copy this guard. The rootwalk's bound is depth=1 at the call site, not a module-parse recursion cap. (Common confusion — the builder must not mistake `:460` for a BFS depth cap.) |
| **dynamic dispatch → UNREACHABLE** | docstring `reachability.py:30`: "The analyzer will report these targets as UNREACHABLE" (on dynamic dispatch the analyzer cannot resolve the edge → reports unreachable). | dynamic/unresolved → **UNREACHABLE** (binary) | dynamic/partial/unresolved → **DEGRADE** (asymmetric-cost: never escalate idiomatic-but-unresolvable wiring to a blocking UNREACHED). |

### 1.3 The reflect-local copy plan (~30 lines, depth=1 + DEGRADE-on-partial)

The reflect rootwalk is NOT a method on a class with a global graph; it is a **free function** that walks runtime roots at depth=1 for ONE candidate-UNREACHED symbol and returns a 3-state result (`REACHED | UNREACHED | DEGRADE`), NOT the audit's binary `(bool, path)`. Skeleton the builder writes (the BFS *shape* preserved; the two inversions baked in):

```python
# reflect-local copy of cli/audit/reachability.py:_bfs_reachable
# INVERSIONS: (a) depth=1 enforced here (no depth param in source);
#             (b) partial enumeration / dynamic dispatch -> DEGRADE, never UNREACHED.
def rootwalk_depth1(
    roots: list[EntrypointRoot],          # enumerated runtime roots (NOT a global call graph)
    symbol: str,
    edges: dict[str, set[str]],           # symbol -> direct referrers (depth-1 adjacency only)
    enumeration_complete: bool,           # False if root enumeration was partial/unsound
) -> Literal["REACHED", "UNREACHED", "DEGRADE"]:
    # (a) depth=1: examine ONLY direct adjacency of each root; do NOT recurse the closure.
    for root in roots:
        if symbol in edges.get(root.root_id, set()):
            return "REACHED"          # any root hit -> REACHED (mirrors audit's early-return True)
    # (b) DEGRADE-on-partial: confirmed UNREACHED ONLY on full clean enumeration.
    if not enumeration_complete:
        return "DEGRADE"              # audit would have walked deeper / reported UNREACHABLE
    return "UNREACHED"                # full enumeration, no root hit, clean oracle
```

Notes for the builder:
- The audit BFS's `visited`/`queue`/`new_path` machinery exists because it walks the **full closure**; at **depth=1** the walk collapses to a single adjacency check per root, so the deque is optional — but the TDD frames it as "adapts the BFS skeleton," so keeping the deque-shaped walk (bounded to one expansion) is acceptable and makes the provenance auditable. What is NON-negotiable is the **depth=1 bound** and the **3-state return with DEGRADE replacing both UNREACHABLE and any partial-walk outcome**.
- The `degrade-oracle` (TDD step 4, categories a–d) MUST run **before** the rootwalk emits any UNREACHED (TDD §FR-004 AC; Risk R1 mitigation). The rootwalk's own `enumeration_complete=False → DEGRADE` is the *second* DEGRADE gate; the oracle is the first.
- Counter-hygiene (Risk R1): a DEGRADE symbol is NOT appended to `unreached_surfaces`, preserving `len(unreached_surfaces) == runtime_surface_unreached`.

**TDD cross-refs:** §6.3 entrypoint-rootwalk adaptation note (line 447); Reuse Audit row `entrypoint-rootwalk` (line 1450, `reuse-by-import`, S_reuse **0.81** STRONGEST, "**Adapt — do NOT drop-in**"); §6.4 D1 (line 460); §21 Alt 3 Option C (line 1297-1311); FR-004 AC-1 (line 284); Risk R1 (line 1222); §28 source-map (line 1468).

---

## 2. The DATA-copies (marker lists + dynamic patterns) — exact current values + inversions

### 2.1 Test prefixes / infixes — `cli/audit/filetype_rules.py:106-107` `[CODE-VERIFIED]`

```python
_TEST_PREFIXES = ("test_", "spec_")
_TEST_INFIXES = (".test.", ".spec.", "_test.", "_spec.")
```

`classify_file_type` (`:110-144`) applies them, then for any unknown extension **defaults to SOURCE** (`:143-144`):

```python
    # Default to source for unknown
    return FileType.SOURCE
```

**Copy as DATA, INVERT the default** (Reuse Audit row `partitioner`, line 1448, distinct, S_reuse 0.57):

| Aspect | Audit (`classify_file_type`) | Runtime-surface partitioner (required) |
|--------|------------------------------|----------------------------------------|
| marker lists | `_TEST_PREFIXES`, `_TEST_INFIXES` (verbatim above) | **copy verbatim as DATA** |
| unknown/ambiguous default | **`→ SOURCE`** (`:143-144`) | **`→ DEGRADE`** — never "treat as production" (TDD step 3 / line 384) |
| scope | filename-level only | adds **inline-test scope** + **comment/docstring exclusion** the audit classifier lacks |

The partitioner also reuses the path heuristics (`/tests/`, `/test/` etc., `:124-131`) if convenient, but the load-bearing change is the **default inversion**: audit's "when in doubt, it's source" becomes runtime-surface's "when in doubt, **DEGRADE**" (asymmetric-cost).

The language table at `filetype_rules.py:7` (`source: .py, .ts, .js, .jsx, .tsx, .go, .rs, .java`) `[CODE-VERIFIED]` is the small lang-extension constant the **surface-tagger** may reuse (Reuse Audit row `surface-tagger`, line 1446) — but the tagger is otherwise distinct (it parses diff hunks + detects Click/Typer/registry decorators, which audit does not).

### 2.2 Dynamic-import patterns — `cli/audit/dynamic_imports.py:24-39` `[CODE-VERIFIED]`

```python
_DYNAMIC_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    # JavaScript dynamic import()
    ("js_dynamic_import", re.compile(r"import\s*\([^\"'][^)]*\)")),
    # JavaScript require with variable
    ("js_require_variable", re.compile(r"require\s*\([^\"'][^)]*\)")),
    # Python __import__
    ("py_import_builtin", re.compile(r"__import__\s*\(")),
    # Python importlib.import_module
    ("py_importlib", re.compile(r"importlib\.import_module\s*\(")),
    # Python importlib.util.find_spec
    ("py_importlib_util", re.compile(r"importlib\.util\.\w+\s*\(")),
    # Glob/wildcard imports
    ("glob_import", re.compile(r"glob\s*\.\s*glob\s*\(")),
    # require.context (webpack)
    ("webpack_require_context", re.compile(r"require\.context\s*\(")),
]
```

**Copy as DATA if convenient, INVERT the verdict mapping** (Reuse Audit row `degrade-oracle`, line 1449, maybe-related, S_reuse 0.68):

| Aspect | Audit (`dynamic_imports.py`) | Runtime-surface degrade-oracle (required) |
|--------|------------------------------|--------------------------------------------|
| regex pattern data | `_DYNAMIC_PATTERNS` (verbatim above) | **copy as DATA** (cat. d: reflection/dynamic-import) |
| match → verdict | **`KEEP:monitor`** (module docstring `:1,4,11`; `apply_keep_monitor` `:125`) | **`→ DEGRADE`** (NOT KEEP:monitor) |
| entrypoint detection | filename-pattern (audit `dead_code.py:155` exclusion) | **`[project.scripts]` / entry-point METADATA resolution** (cat. b) — NOT filename-pattern |

The oracle is one of **4 categories (a–d)**: (a) decorator routes, (b) packaging entrypoints (`[project.scripts]`), (c) registry/DI/string-dispatch, (d) reflection/dynamic-import. ONLY category (d) reuses the audit regex data; (a)–(c) are reflect-local. The whole oracle MUST run **before** any UNREACHED (Risk R1).

---

## 3. The `_safe_parse` fail-soft pattern to mirror — `cli/audit/wiring_gate.py:164-174` `[CODE-VERIFIED]`

```python
def _safe_parse(file_path: Path) -> ast.Module | None:
    """Parse a Python file, returning None on SyntaxError (R2 mitigation)."""
    try:
        source = file_path.read_text(encoding="utf-8")
        return ast.parse(source, filename=str(file_path))
    except SyntaxError as exc:
        logger.warning("SyntaxError parsing %s: %s — skipping", file_path, exc)
        return None
    except (OSError, UnicodeDecodeError) as exc:
        logger.warning("Cannot read %s: %s — skipping", file_path, exc)
        return None
```

**Mirror the PATTERN, not the function** (Reuse Audit row `surface-tagger`, line 1446 — reuse "the fail-soft `return-None-on-parse-error` *pattern*"). The surface-tagger AST-parses diff hunks; when a hunk/file fails to parse, it MUST return `None` and **DEGRADE the affected surface**, never raise and never silently drop (fail-open envelope P3). Key properties to replicate:
- catch `SyntaxError` AND `(OSError, UnicodeDecodeError)` separately,
- `logger.warning(... "— skipping")`,
- return `None` (the caller treats `None` as "cannot resolve → DEGRADE", the inversion of audit's "skip and move on").

This is a PATTERN copy (idiom), not a constant/function import — the tagger parses *diff hunks* (resolving hunk-local symbols), which `_safe_parse` (whole-file) does not do, so it cannot be reused by import.

---

## 4. Reflect import-ban confirmation + copy-over-import precedent (boundary-decision evidence)

### 4.1 The import ban names ONLY `cli/sprint` + `cli/roadmap` `[CODE-VERIFIED]`

All three reflect module docstrings were read this session:

| File | Docstring lines | Exact ban text |
|------|-----------------|----------------|
| `runner.py` | `:8-9` | "Isolation guardrails: - No imports from ``superclaude.cli.sprint`` or ``superclaude.cli.roadmap``." |
| `config.py` | `:7-10` | "Isolation guardrails: - No imports from ``superclaude.cli.sprint`` or ``superclaude.cli.roadmap``. ... - Imports nothing from ``commands.py`` / ``runner.py`` / ``contract.py``." |
| `models.py` | `:8-12` | "Isolation guardrails (NFR-1 thinness ...): - No imports from ``superclaude.cli.sprint`` or ``superclaude.cli.roadmap``." |

**`cli/audit` is NOT named in any ban.** A `from superclaude.cli.audit... import ...` is therefore **mechanically legal** (no guardrail, no `__init__.py` ban). This is exactly why the boundary decision must be made by *judgment*, not by a mechanical gate: the gate would not catch the coupling. Matches TDD §6.4 D1 (line 460): "verified in `runner.py:8-9`, `config.py:7-10`, `models.py:8-12`; `__init__.py` carries no ban."

### 4.2 Copy-over-import precedent — `runner.py:14-17` (`_IndentDumper`) `[CODE-VERIFIED]`

`runner.py:14-17` docstring:

> "The ``_IndentDumper`` is copied locally (lower coupling than importing the private symbol from ``recommend.cache``); the atomic writer uses a randomized same-dir temp name so parallel sessions never collide ..."

The class is defined reflect-local at `runner.py:58-67` `[CODE-VERIFIED]`. This is the established in-repo precedent: reflect **copies** a ~10-line private helper rather than importing it from another `cli/` package, "for exactly this private-symbol-coupling reason" (§21 Alt 3 line 1311). `_bfs_reachable` is *also* private (underscore-prefixed, unexported), so importing it would repeat the anti-pattern this precedent already rejected once.

**Boundary decision is sound:** legal-but-coupled import (Option A) is to be AVOIDED; reflect-local copy (Option C) is ratified v1; boundary-neutral extraction (Option B) is the clean long-term shape *only if a second reflect graph-BFS consumer appears* (§21 Alt 3 line 1311; §18.2 line 1165).

---

## 5. Per-Reuse-Audit-row disposition (the table the builder copies items from)

Source: TDD "Reuse & Consolidation Audit" table, lines 1440-1453 `[CODE-VERIFIED]` (re-confirmed against live source in this research). Outcome: **5 of 6 distinct; 1 reuse-by-import (rootwalk, S_reuse 0.81) but adapted-never-dropped.** No proposed component is a confident duplicate.

| # | Unit | Reuse verdict | Disposition for the builder | Audit source (line-verified) |
|---|------|---------------|------------------------------|------------------------------|
| 1 | **surface-tagger** | distinct (0.37) | **Reflect-local.** Mirror the `_safe_parse` fail-soft *pattern* (§3); reuse only the tiny lang-extension constant (`filetype_rules.py:7`). Audit helpers don't parse diff hunks / resolve hunk-local symbols / detect Click·Typer·registry decorators. | `wiring_gate.py:164` (`_safe_parse`); `filetype_rules.py:7` (lang table). Both `[CODE-VERIFIED]`. |
| 2 | **referrer-finder** | shape-divergent (0.67) | **Reflect-local, distinct.** Mirror the fail-open tier *shape* (AST-high / grep-medium, **grep is the floor**) but implement SYMBOL-level locally. Do NOT drop-in: audit graph is FILE-level, too broad for symbol referrer + comment/test partitioning. Engine choice (LSP overlay vs AST floor) is OQ-DRS.1, an engine choice not a reuse choice. | `dependency_graph.py` (3-tier static+grep); `tool_orchestrator.py:146`. (cited in table; not re-read this session — `[UNVERIFIED]` line offsets, verdict per table.) |
| 3 | **partitioner** | distinct (0.57) | **Reflect-local.** Copy `_TEST_PREFIXES`/`_TEST_INFIXES` LISTS as DATA (§2.1); **INVERT the default** unknown/ambiguous `SOURCE→DEGRADE`; add inline-test scope + comment/docstring exclusion. | `filetype_rules.py:106-107` (markers); `:110-144` (`classify_file_type`, default-to-SOURCE at `:143-144`). `[CODE-VERIFIED]`. |
| 4 | **degrade-oracle** | maybe-related (0.68) | **Reflect-local.** Copy `_DYNAMIC_PATTERNS` regex DATA if convenient (§2.2, category d); implement 4-category oracle (a–d) separately; **INVERT** dynamic `KEEP:monitor→DEGRADE`; entrypoint via `[project.scripts]` METADATA not filename-pattern. | `dynamic_imports.py:24-39` (`_DYNAMIC_PATTERNS`); docstring `:1,4,11` (KEEP:monitor); `dead_code.py:155` (entrypoint exclusion). Patterns + KEEP default `[CODE-VERIFIED]`; `dead_code.py:155` `[UNVERIFIED]` (per table). |
| 5 | **entrypoint-rootwalk** | **reuse-by-import (0.81, STRONGEST)** | **Adapt — do NOT drop-in.** Reflect-local copy (Option C / §6.4 D1) of the ~30-line BFS skeleton (§1.3) with **depth=1 at the call site** + **partial/dynamic→DEGRADE** baked in. Matches `runner.py:14-17` copy precedent. | `reachability.py:591` (`_bfs_reachable`); `:740` (`emit_reachability_report` — NOT scalar frontmatter, do not reuse). `_bfs_reachable:591-635` + `deque:49` + `depth>50` at `:460` (module-parse, NOT BFS) all `[CODE-VERIFIED]`. |
| 6 | **ledger-writer** | distinct (0.56) | **Reflect-local.** Implement `RuntimeSurfaceLedgerRow` + per-symbol reduction + 6-scalar computation directly from `runtime-surface.md`. Reuse ONLY the **reflect-local** YAML style: `_IndentDumper` (`runner.py:58-67`) + `_atomic_write_text` (`runner.py:70-89`) — both already reflect-local, **zero boundary cost**. **NOT** ensemble's bare `yaml.safe_dump` + `path.write_text`. | `ensemble.py:500` (`_emit_reflect_contract`); `contract.py:65` (`parse_contract`); `runner.py:58-67`/`:70-89` (`_IndentDumper`, `_atomic_write_text`) `[CODE-VERIFIED]`. |

### 5.1 The two MANDATORY reflect-local writer deps (§18.2 lines 1163-1164) `[CODE-VERIFIED]`

The ledger-writer item MUST cite these as non-negotiable (no boundary cost — both already reflect-local):

- **`_IndentDumper(yaml.SafeDumper)`** (`runner.py:58-67`): yamllint-safe nested block sequences (`unreached_surfaces:`, `production_referrers:`). Without it, pre-commit yamllint fails on nested sequences (`mem:reference_yamllint_indent_sequences_pyyaml`). MANDATORY — NOT ensemble's bare `yaml.safe_dump`.
- **`_atomic_write_text(path, text)`** (`runner.py:70-89`): randomized same-dir temp + `os.replace`; `mkdir(parents=True, exist_ok=True)` covers the new `<output>/artifacts/` dir; parallel-session last-write-wins safety. MANDATORY — NOT ensemble's plain `path.write_text`.

---

## 6. Builder action items (the "copy X, invert default Y" lines this research underwrites)

The builder should emit items shaped exactly as:

1. **Copy** `_bfs_reachable` (`reachability.py:591-635`) into `cli/reflect/runtime_surface.py` as `rootwalk_depth1(...)`; **enforce depth=1 at the call site** (source has no depth param); **return 3-state** with **partial-enumeration / dynamic-dispatch → DEGRADE** (audit returns binary + UNREACHABLE). Do NOT copy the `depth>50` guard (`:460`) — it is module-parse recursion, not the BFS. Run the degrade-oracle BEFORE any UNREACHED (R1).
2. **Copy** `_TEST_PREFIXES`/`_TEST_INFIXES` (`filetype_rules.py:106-107`) as DATA; **invert** `classify_file_type`'s unknown→SOURCE default (`:143-144`) to unknown/ambiguous **→DEGRADE**; add inline-test + comment/docstring exclusion.
3. **Copy** `_DYNAMIC_PATTERNS` (`dynamic_imports.py:24-39`) as DATA for oracle category (d); **invert** dynamic→KEEP:monitor to dynamic **→DEGRADE**; implement (a)–(c) reflect-local; entrypoint via `[project.scripts]` metadata.
4. **Mirror** the `_safe_parse` (`wiring_gate.py:164-174`) fail-soft `return-None-on-parse-error` pattern in the tagger; `None`→DEGRADE.
5. **Reuse** reflect-local `_IndentDumper` (`runner.py:58-67`) + `_atomic_write_text` (`runner.py:70-89`) for the ledger writer; NOT ensemble's bare dump/write.
6. **Boundary decision item:** state explicitly NO `from superclaude.cli.audit...` import (Option A AVOIDED); reflect-local copy (Option C) per §6.4 D1; cite `runner.py:14-17` precedent + the import-ban naming only sprint/roadmap as the evidence the edge stays clean.

---

## Status: Complete

**Summary:** Documented the exact cli/audit copy/adapt sources for FR-DRS with re-verified line numbers. (1) `_bfs_reachable:591-635` full body + the depth=1-at-call-site + DEGRADE-on-partial reflect-local copy plan; the `depth>50` guard at `:460` is in `_parse_module_recursive`, NOT the BFS (builder trap flagged). (2) Two DATA copies with inversions: `_TEST_PREFIXES`/`_TEST_INFIXES` (`filetype_rules.py:106-107`) invert unknown→SOURCE to →DEGRADE; `_DYNAMIC_PATTERNS` (`dynamic_imports.py:24-39`) invert dynamic→KEEP:monitor to →DEGRADE. (3) `_safe_parse` (`wiring_gate.py:164-174`) fail-soft pattern to mirror. (4) Import-ban confirmed naming ONLY cli/sprint+cli/roadmap (audit import legal-but-coupled) + the `runner.py:14-17` `_IndentDumper` copy-over-import precedent — boundary decision (Option C) sound. (5) Per-row disposition for all 6 Reuse-Audit units (5 distinct/reflect-local, 1 reuse-by-import=rootwalk adapted-never-dropped) + the two MANDATORY reflect-local writer deps. All primary claims `[CODE-VERIFIED]`; only `dependency_graph.py`/`tool_orchestrator.py`/`dead_code.py:155` line offsets are `[UNVERIFIED]` (table-sourced, not re-read — out of R4's core-copy scope).
