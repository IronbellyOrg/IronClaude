# Web Research: Python `ast` symbol/decorator resolution + ripgrep `--json` referrer scanning

**Topic:** Deterministic LLM-free runtime-surface sweep floor (pure-Python `ast` + `rg`).
**Date:** 2026-06-21
**Status:** Complete
**Search backend:** Tavily MCP (`tavily-search` + `tavily-extract`); no fallback required.
**Persistence note:** Authored by a deep-research subagent (no Write tool); persisted verbatim by the orchestrator.

---

## Finding 1 — `ast` node types and `decorator_list` (authoritative)

- **Source:** https://docs.python.org/3/library/ast.html (Python 3.14 docs) — **reliability: official Python docs, highest.**
- **Key info:**
  - `ast.FunctionDef(name, args, body, decorator_list, returns, type_comment, type_params)` — a `def` function.
  - `ast.AsyncFunctionDef(...)` — same fields (an `async def`). **Must be matched separately** from `FunctionDef`; not a subclass for `isinstance` narrowing.
  - `ast.ClassDef(name, bases, keywords, body, decorator_list, type_params)` — `decorator_list` as in `FunctionDef`.
  - `decorator_list` is stored outermost-first.
  - `type_params` added in 3.12; do not assume presence on <3.12.
- **Relation to floor:** Confirms the node set for symbol-kind resolution: `(ast.FunctionDef, ast.AsyncFunctionDef)` → callable, `ast.ClassDef` → class. Both carry `decorator_list`.
- **Verdict:** SUPPORTS the floor design.

## Finding 2 — `ast.walk` traversal + the `.id` vs `.attr` trap

- **Source:** https://mvdwoord.github.io/exploration/2017/08/18/ast_explore.html — blog (code-verified), cross-checked vs official docs.
- **Key info:**
  - Canonical: `for node in ast.walk(tree): if isinstance(node, ast.FunctionDef): ...`. Order unspecified but deterministic per-tree.
  - **Critical trap:** decorators are not always `ast.Name`. `@my_decorator` is `ast.Name` (`.id`); `@MyClass.sub.my_deco` is `ast.Attribute` (`.attr`/`.value`, NOT `.id`) — naive `d.id` raises `AttributeError`.
- **Relation to floor:** Decorator matcher must branch on node type, never assume `.id`.
- **Verdict:** EXTENDS the floor — names the exact failure mode to guard.

## Finding 3 — Resolving `@app.route` / Click / Typer decorators (Attribute + Call)

- **Sources:** mvdwoord blog (`flatten_attr` pattern); https://github.com/pallets/click/blob/master/src/click/decorators.py (official Click); https://typer.tiangolo.com/tutorial/commands (official Typer).
- **Key info — the three decorator AST shapes:**
  1. **Bare name** `@command` → `ast.Name`, read `.id`.
  2. **Dotted attribute** `@app.command` (no call) → `ast.Attribute`, walk `.value`/`.attr`.
  3. **Call form** `@app.command()` / `@app.route("/x")` / `@click.command()` → `ast.Call`; identity in `node.func` (a `Name`/`Attribute`); args/kwargs (route path) in `node.args`/`node.keywords`.
  - Deterministic dotted-chain resolver:
    ```python
    def flatten_attr(node):
        if isinstance(node, ast.Attribute):
            return f"{flatten_attr(node.value)}.{node.attr}"
        if isinstance(node, ast.Name):
            return node.id
        return None  # unresolvable -> DEGRADE signal
    ```
  - Typer `@app.command()` registers but does NOT modify the function — the decorated `FunctionDef` keeps its `.name`.
  - Flask `@app.route` should be the outermost decorator (last in `decorator_list`).
- **Relation to floor:** All four frameworks (Click, Typer, FastAPI, Flask) reduce to the same `{Name | Attribute | Call→func}` matcher — no per-framework runtime import.
- **Verdict:** SUPPORTS + EXTENDS the floor (concrete LLM-free detection recipe).

## Finding 4 — ripgrep `--json` wire format (authoritative schema)

- **Source:** https://docs.rs/grep-printer/latest/grep_printer/struct.JSON.html — official `grep-printer` crate docs, highest for the JSON contract.
- **Key info:**
  - **JSON Lines** — one JSON object per line; parse line-by-line.
  - Envelope: `{ "type": "<begin|end|match|context>", "data": {...} }`.
  - **`match`** (the referrer event): `data.path` (path object), `data.lines.text` (matched line when valid UTF-8), `data.line_number` (1-based or `null` if line numbers not enabled — so pass `-n`/`--line-number` or rely on `--json` config), `data.absolute_offset`, `data.submatches` (`[{match:{text}, start, end}]`, byte offsets into `lines`, half-open, **sorted by start**, can be empty).
  - **Encoding rule:** valid UTF-8 → `"text"`; invalid bytes → base64 `"bytes"`. Parser must handle the `bytes` fallback or silently drop non-UTF-8 referrers.
- **Relation to floor:** Exact event schema for the referrer-scan parser: bind to `type=="match"`, read `data.path.text` + `data.line_number` + `data.lines.text` + `data.submatches[].{start,end}`; guard `bytes`-keyed objects and `line_number==null`.
- **Verdict:** SUPPORTS the floor — authoritative confirmation.

## Finding 5 — `--sort path` is the determinism lever (authoritative)

- **Sources:** https://manpages.debian.org/testing/ripgrep/rg.1.en.html (official man page); ripgrep FAQ/GUIDE (docs.rs/crate/ripgrep).
- **Key info:**
  - Default ripgrep is multi-threaded → **non-deterministic output order**. FAQ: *"The only way to make the order of results consistent is to ask ripgrep to sort the output ... `--sort path`."*
  - `--sort path` = sort by path, **implies `--threads=1`** (single-threaded, lexicographic path order).
  - `--sort-files` is **DEPRECATED → use `--sort path`**.
  - Trade-off: sorting disables parallelism (~4–10x slower), irrelevant for a determinism-required sweep.
- **Relation to floor:** `--sort path` is the single flag making the referrer scan reproducible across runs — required for determinism + golden-file tests.
- **Verdict:** SUPPORTS the floor; THE determinism lever for rg.

## Finding 6 — Static analysis cannot resolve dynamic dispatch → DEGRADE oracle justification

- **Sources:** https://raven.io/blog/why-static-analysis-falls-short-in-dynamic-programming-languages (cites Meta Pysa); https://ipsitransactions.org/journals/papers/tir/2020jul/p6.pdf (peer-reviewed Python static-analysis eval).
- **Key info — patterns provably unresolvable by `ast`+`rg` (must DEGRADE, not "unwired"):**
  - Dynamic dispatch by string: `getattr(obj, name)()`, dispatch tables `funcs[name]()`.
  - Dynamic import: `importlib.import_module(x)`, `__import__(var)` (Meta Pysa misses these).
  - Reflection / monkey-patching: `setattr`, runtime attribute assignment, metaclass registration.
  - `eval()` / `exec()`: callee generated at runtime.
  - Aliasing / star-imports / decorator aliasing: `from m import *`, `r = app.route; @r(...)`.
  - Meta's own admission: *"There are endless pathological examples of flows of data that Pysa cannot detect."*
- **Relation to floor:** Grounds the degrade-oracle: when the sweep hits any of these (`flatten_attr`→`None`, a `getattr`/`importlib`/`eval` node, `import *`), it MUST DEGRADE. A "no referrer found" result is only trustworthy in the absence of these constructs.
- **Verdict:** SUPPORTS the degrade-oracle design.

---

## Key External Findings

1. **Decorator detection reduces to a 3-shape matcher** (`Name`→`.id`; `Attribute`→recurse; `Call`→inspect `.func`), uniform across Click/Typer/FastAPI/Flask. `flatten_attr` returning `None` is the natural DEGRADE signal. `ast.AsyncFunctionDef` must be matched alongside `ast.FunctionDef`.
2. **The ripgrep `--json` schema is authoritative and stable** (grep-printer crate): JSON Lines, `{type,data}` envelope, parse `type=="match"`; handle base64 `bytes` fallback and `line_number==null`.
3. **`--sort path` is THE determinism lever** — official FAQ + man page; implies `--threads=1`; default rg is non-deterministic. `--sort-files` deprecated.
4. **Dynamic dispatch is irresolvable in principle** — even Meta's Pysa misses `importlib`/`getattr`/`eval`; literature-backed justification for DEGRADE over "unwired."

## Recommendations from External Research

1. **Symbol-kind resolver:** match `(ast.FunctionDef, ast.AsyncFunctionDef)` → callable, `ast.ClassDef` → class; iterate via `ast.walk`; treat `type_params` as optional (3.12+).
2. **Decorator resolver:** implement `flatten_attr`; branch on `Name`/`Attribute`/`Call`; for `Call`, read `node.func` + route/command string from `node.args[0]`/`node.keywords`; never read `.id` without an `isinstance` guard.
3. **rg invocation:** always `--json --sort path` (ensure line numbers); parse JSON Lines per line; bind only `type=="match"`; tolerate `line_number==null` and `bytes`-keyed objects.
4. **Degrade-oracle triggers (DEGRADE, never "unwired"):** in-scope `getattr`/`setattr`, `importlib.import_module`/`__import__`, `eval`/`exec`, `from x import *`, decorator aliasing, or any `flatten_attr`-unresolvable decorator. A negative referrer result is valid only in the absence of all these.
5. **Determinism test hook:** golden-file the `--json --sort path` output; assert byte-identical across repeated runs in CI.
6. **Codebase remains source of truth:** verify the environment's rg version supports `--sort path` over the deprecated `--sort-files`.

## Sources

| URL | Reliability |
|---|---|
| https://docs.python.org/3/library/ast.html | Official (highest) |
| https://docs.rs/grep-printer/latest/grep_printer/struct.JSON.html | Official ripgrep crate (highest) |
| https://manpages.debian.org/testing/ripgrep/rg.1.en.html | Official man page (highest) |
| https://github.com/pallets/click/blob/master/src/click/decorators.py | Official Click |
| https://typer.tiangolo.com/tutorial/commands | Official Typer |
| https://mvdwoord.github.io/exploration/2017/08/18/ast_explore.html | Blog (code-verified) |
| https://raven.io/blog/why-static-analysis-falls-short-in-dynamic-programming-languages | Blog (cites Meta Pysa) |
| https://ipsitransactions.org/journals/papers/tir/2020jul/p6.pdf | Peer-reviewed |
