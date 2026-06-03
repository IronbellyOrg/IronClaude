# sc:reflect V3 — Serena Feature Adoption Matrix #1

**Scope:** Low implementation cost / complexity items with Medium-to-High value to the sc:reflect protocol's objectives (UC-1 coverage audit, UC-2 deviation classification, tiered review ensemble, adversarial merge, evidence-validator gate, per-project deviation memory).

**Posture:** sc:reflect is read-only **with respect to project source code** — it does not mutate code. It DOES write logs, audit trails, reflection cards, reviewer briefs, reports, and may run tests/linters/build commands as verification activity. This boundary is the filter applied to every row.

**Source ranking:** Implementation cost is rated relative to wiring effort inside `src/superclaude/skills/sc-reflect-protocol/SKILL.md` and `refs/*.md`. Value is rated against the specific objectives above, not generic utility.

---

## Matrix

| # | Name | Description | Implementation Cost / Complexity | Value to sc:reflect |
|---|---|---|---|---|
| 1 | **`find_implementations`** | For an interface / abstract / protocol symbol, returns all concrete implementations. | **Low.** Drop-in addition to Wave 1A chain (§6.1) immediately after `find_symbol` when symbol kind ∈ {interface, abstract}. ~10 lines in the chain spec + one new schema field on the reflection card. | **High.** Directly strengthens UC-1 coverage analysis ("spec requires handler X; are all implementations of `Handler` accounted for in the tasklist?"). Catches "interface added but no impl wired" — a recurring **Drift** deviation in the 4-category taxonomy. |
| 2 | **`find_declaration`** | Resolves a callsite to its declaration. Complements `find_symbol` which queries by name path. | **Low.** Add to §6.1 as a step between `get_symbols_overview` and `find_symbol` when starting from a diff hunk rather than a symbol name. | **Medium.** Diff-hunk → symbol resolution is currently implicit (`find_symbol` against a textual guess). Declaration-anchoring makes the Wave 1B.3 cross-task interaction scan more precise — fewer false-positive overlap edges from name collisions. |
| 3 | **`find_referencing_code_snippets`** | Compact, grouped variant of `find_referencing_symbols` returning code excerpts grouped by usage site. | **Low.** Direct substitute or supplement in §6.1 step 4. | **Medium.** Reduces token cost of Wave 1A grounding when reference counts are high (the top-30 cap currently truncates). Same signal, denser packaging — directly improves Tier 2 reviewer brief quality per `refs/reviewer-spec.md`. |
| 4 | **`find_symbol(search_deps=True)`** | Same `find_symbol` surface, but searches the project's external dependencies. v1.5.x changelog forces this when `relative_path` is an external dep identifier. | **Low.** One-flag addition to the chain, optionally fan out a second `find_symbol` against dep symbols when a spec/tasklist cites third-party APIs. | **Medium.** Catches **Necessary deviation** cases where a task description references upstream behavior (e.g. "matches FastAPI's `Depends` contract") without citing the dep version. Cheap correctness improvement for spec-referenced third-party APIs. |
| 5 | **`summarize_changes`** | Returns a Serena-generated summary of edits made since session start (or last checkpoint). | **Low.** Add to Wave 1A in UC-2 mode as a free corroboration signal vs. the user-supplied diff. | **Medium.** Independent check on what was *actually* changed vs. what the tasklist *claims* was changed. Direct lever against the **Drift** deviation class. Compact summary, low token cost. |
| 6 | **`check_onboarding_performed`** | Boolean probe of whether Serena onboarding ran for the active project. | **Low.** Plain check in Wave 0; emit `onboarding_status: <bool>` in telemetry. | **Medium.** Lets the rubric weight grounding-confidence by whether project memory was bootstrapped — a real input to `S_dev_density` calibration. Cheap signal, cheap to wire. |
| 7 | **`get_current_config`** | Returns active Serena project + context + modes + tool list. | **Low.** Single call at Wave 0. | **Medium.** Enables deterministic `degraded_components` detection and rubric calibration. sc:reflect currently probes alias env vars but not Serena's own config — a blind spot. |
| 8 | **`delete_memory` / `rename_memory` / `edit_memory`** | Memory lifecycle CRUD operations on Serena memory blobs. | **Low.** Plug into the existing §6.3 90-day TTL / 20-entry retention scheme. | **Medium.** §6.3's retention rule is specified but **not implemented** — `write_memory` currently accumulates without pruning. These three close the loop and prevent unbounded memory growth (operational hazard at 6-month horizon). |

---

## Wiring notes (shared across all items)

- **Fail-open:** §6.5 already mandates that every Serena call is fail-open. New tools inherit that posture — missing → `degraded: ["serena"]` audit entry, fall back to native `Grep`/`Glob` where applicable, continue.
- **Telemetry:** every new tool should emit a binary `<tool>_invoked: bool` field into the return contract for observability.
- **Citation freshness:** any output that lands in a `file:line` citation must still pass the CLAUDE.md S1 re-Read rule before entering the draft report (§6.2).

---

## Research expansion section

> The detailed best-practice, documentation, and sample-use-case research for each row above is appended by the parallel research agent. The header below is the boundary; everything below it is research-agent output.

<!-- BEGIN: research-agent appended content -->

### 1. `find_implementations`

**Canonical documentation:**
- [Serena Tools — find_implementations (oraios.github.io)](https://oraios.github.io/serena/01-about/035_tools.html) — "Finds symbols that implement the given symbol using the language server backend."
- [Serena CHANGELOG — v1.3.0 entry](https://github.com/oraios/serena/blob/main/CHANGELOG.md) — "LSP Backend: Add new tools: `find_declaration`, `find_implementations`, `get_diagnostics_for_file`, `get_diagnostics_for_symbol`."
- [JetBrains-backend variant `jet_brains_find_implementations`](https://oraios.github.io/serena/01-about/035_tools.html) — "Finds the implementations of a symbol using the JetBrains backend."
- context7: `/oraios/serena` retrieval surfaced a full JSON example for `Tool/apply` returning per-implementation `{kind, name_path, relative_path}` rows.

**Tool signature:**
```json
{
  "tool": "find_implementations",
  "arguments": {
    "name_path": "Tool/apply",
    "relative_path": "src/serena/tools/tools_base.py",
    "include_info": true
  }
}
```
- Parameters: `name_path` (the interface/abstract method's name path); `relative_path` (file that contains the abstract symbol declaration); `include_info` (bool — when `true`, returns hover-like signature + docstring per implementing symbol); per [llms.txt context7 retrieval](https://context7.com/oraios/serena/llms.txt).
- Returns: a JSON array of `{kind, name_path, relative_path}` rows, one per concrete implementor; with `include_info: true` each row carries an `info` field with the implementer's signature ([context7 example response](https://context7.com/oraios/serena/llms.txt)).
- Errors / known exceptions: language-server-dependent — for languages whose LSP does not implement `textDocument/implementation` (GDScript per [v1.5.0 changelog](https://github.com/oraios/serena/blob/main/CHANGELOG.md), Godot LSP "does not implement `workspace/symbol`" caveat applies analogously) the call returns an empty list or an LSP-level error rather than a partial result.

**Best-practice usage patterns:**
- Pattern 1 — *Interface contract coverage*: invoke after `find_symbol` whenever the located symbol's `kind` is interface / abstract method / Protocol / trait. The set of implementors is the surface a coverage audit must enumerate, per the [v1.3.0 release motivation](https://github.com/oraios/serena/blob/main/CHANGELOG.md).
- Pattern 2 — *Pre-refactor blast-radius scan*: per [Serena evaluation report](https://github.com/oraios/serena/blob/main/docs/04-evaluation/030_results/050_junie_plugin_on_tianshou.md), `find_implementations` complements `find_referencing_symbols` — the former finds polymorphic substitutes, the latter finds call-sites. Pair both for any change touching an abstract.
- Pattern 3 — *Cross-package monorepo discovery*: per [v1.3.0 changelog](https://github.com/oraios/serena/blob/main/CHANGELOG.md), TypeScript adds cross-package reference support via `additional_workspace_folders`; `find_implementations` benefits when the abstract is in one package and implementors live in siblings.

**Failure modes / gotchas:**
- Symbol-kind detection is LSP-driven; non-Python languages may report `Class` instead of `Interface` for traits/Protocols, so callers cannot rely on kind alone to gate the call — `include_info: true` + signature inspection is the disambiguation surface.
- Lombok-generated methods in Java are *included* as of v1.3.0 per [CHANGELOG #1432](https://github.com/oraios/serena/blob/main/CHANGELOG.md); pre-1.3 caches may be stale.
- Empty result is ambiguous: either "no implementations" or "LSP does not support". The §6.5 fail-open path in [SKILL.md:399](file:///config/workspace/IronClaude/.claude/worktrees/reflect-v3-serena-research/src/superclaude/skills/sc-reflect-protocol/SKILL.md) must distinguish via the diagnostics path or a `kind` re-check.

**Version / language-server dependencies:**
- Introduced in: Serena **v1.3.0 (2026-05-11)** per [CHANGELOG](https://github.com/oraios/serena/blob/main/CHANGELOG.md).
- Languages supported: any LSP that implements `textDocument/implementation`; degraded/absent for GDScript (Godot LSP), Lean4 stale-cache scenarios, mIRC. JetBrains backend equivalent is `jet_brains_find_implementations`.

**sc:reflect wiring (sample use case):**
- Wave: 1A (§6.1 chain extension).
- Insertion point: SKILL.md §6.1 step 3-4 boundary, between `find_symbol <relevant-symbol>` and `find_referencing_symbols <symbol>`. New conditional step: "3b. IF symbol.kind ∈ {Interface, AbstractMethod, Protocol, Trait}: `find_implementations <symbol>`."
- Concrete invocation (paste-ready):
  ```json
  {
    "tool": "mcp__serena__find_implementations",
    "arguments": {
      "name_path": "AuthHandler/handle",
      "relative_path": "src/handlers/base.py",
      "include_info": true
    }
  }
  ```
- Rubric inputs affected: `S_dev_density` (UC-1 unmapped-requirement ratio gains a new term: missing-implementor-rows count); `coverage_pct` (UC-1 — implementor coverage becomes a sub-metric of spec coverage).
- Audit-log field(s) emitted: `find_implementations_invoked: bool`, `implementations_found: <int>`, `unmapped_implementations: <int>`.
- Return-contract addition(s): under §9.1 UC-1 block — `implementation_coverage_pct: <float 0.0-1.0> | null`, `missing_implementations: [<list of {abstract_name_path, expected_count, found_count}>]`.
- Fail-open behavior: if `find_implementations` errors or returns empty AND symbol kind is `Class` (ambiguous), emit `degraded: ["find_implementations:lsp_unsupported"]` and fall back to a `Grep` for `class .* extends|implements <name>` pattern; do NOT block the chain.

**Interaction with adjacent sc:reflect mechanics:**
This composes left-to-right with the [§6.1 chain](file:///config/workspace/IronClaude/.claude/worktrees/reflect-v3-serena-research/src/superclaude/skills/sc-reflect-protocol/SKILL.md) — `get_symbols_overview` produces the structural map, `find_symbol` resolves the abstract, `find_implementations` enumerates the polymorphic surface, then `find_referencing_symbols` walks call-sites for each implementor. In Wave 1B.3 cross-task scan, an implementation found in one task that overlaps an abstract changed in another task is a HIGH-severity interaction-effects edge (the polymorphic dispatch makes the coupling load-bearing). For Tier 2 reviewer briefs (§4.3 step 3B.0), the implementations list lands in the `reviewer-scoped grounding hunks` section so each reviewer sees the polymorphic surface independently — this is exactly the "Drift" detection the matrix calls out (interface added without implementor wiring).

---

### 2. `find_declaration`

**Canonical documentation:**
- [Serena Tools — find_declaration (oraios.github.io)](https://oraios.github.io/serena/01-about/035_tools.html) — "Finds the declaration/definition of a symbol."
- [Serena CHANGELOG — v1.3.0 entry](https://github.com/oraios/serena/blob/main/CHANGELOG.md) — "LSP Backend: Add new tools: `find_declaration`."
- [External-dep two-step pattern docs](https://github.com/oraios/serena/blob/main/docs/04-evaluation/030_results/020_codex_on_jbplugin.md) — `find_declaration` + `find_symbol(search_deps=True)` chained for external symbols.
- context7: `/oraios/serena` retrieval returned a full call-site-by-regex example with `containing_symbol_name_path`.

**Tool signature:**
```json
{
  "tool": "find_declaration",
  "arguments": {
    "relative_path": "src/serena/agent.py",
    "regex": "self\\.(execute_task)\\( ",
    "containing_symbol_name_path": "SerenaAgent/health_check",
    "include_body": false,
    "include_info": true
  }
}
```
- Parameters: `relative_path` (file containing the call-site); `regex` (Python regex with **one** capture group identifying the call-site identifier — MULTILINE + DOTALL); `containing_symbol_name_path` (optional — narrows the search to a specific symbol's body); `include_body` (bool); `include_info` (bool — returns hover/signature).
- Returns: a single `{kind, name_path, relative_path, info?}` object pointing at the declaration ([context7 example](https://context7.com/oraios/serena/llms.txt)).
- Errors / known exceptions: per [context7 source](https://context7.com/oraios/serena/llms.txt), regexes with zero or multiple matches are ambiguous; the tool relies on the regex's capture-group context to disambiguate identical identifiers within the same containing symbol.

**Best-practice usage patterns:**
- Pattern 1 — *Diff-hunk → symbol resolution*: when only a `file:line` is known (typical UC-2 input), pass the hunk's surrounding text as the regex with the identifier as the capture group; per [v1.3.0 release rationale](https://github.com/oraios/serena/blob/main/CHANGELOG.md), this is the canonical entry point when starting from textual diff coordinates.
- Pattern 2 — *External-dep declaration jumping*: per [Codex-on-jbplugin eval](https://github.com/oraios/serena/blob/main/docs/04-evaluation/030_results/020_codex_on_jbplugin.md), the standard pattern is `find_declaration` to surface the external-symbol body location, then `find_symbol(relative_path=<ext:...>, search_deps=true, include_body=true)` to retrieve the body.
- Pattern 3 — *Disambiguating overloads*: per [v1.0.0 changelog](https://github.com/oraios/serena/blob/main/CHANGELOG.md), overloaded symbols get `[index]` suffix in name paths; `find_declaration` returns the specific overload that matches the regex's call-shape.

**Failure modes / gotchas:**
- Regex with zero matches → empty result. Reflect must guard against silent miss; emit `find_declaration_no_match: true` to audit so it does not look like "no declaration exists."
- `containing_symbol_name_path` mistyped → no match; per [Serena symbol-tree docs](https://context7.com/oraios/serena/llms.txt), name paths are case-sensitive and use `/` separators.
- Per the [`solidlsp` library notes](https://github.com/oraios/serena/blob/main/CHANGELOG.md) (v0.1.3), language-server termination is now reliably detected — but a mid-call LS crash still surfaces as a tool-level error, not a silent empty result.

**Version / language-server dependencies:**
- Introduced in: Serena **v1.3.0 (2026-05-11)** per [CHANGELOG](https://github.com/oraios/serena/blob/main/CHANGELOG.md).
- Languages supported: all LSP-backed languages. JetBrains backend equivalent is `jet_brains_find_declaration` per [Tools page](https://oraios.github.io/serena/01-about/035_tools.html).

**sc:reflect wiring (sample use case):**
- Wave: 1A (§6.1) AND 1B.3 (cross-task scan).
- Insertion point: SKILL.md §6.1 — new step **2a. IF input is a diff-hunk rather than a symbol-name**: `find_declaration` first to resolve the hunk's identifiers, then continue to `find_symbol`. Also §4.1 step 1B.3 sub-step 1 ("derive its touched symbols via `mcp__serena__find_symbol`") gains a `find_declaration` pre-step for diff-hunks lacking explicit symbol context.
- Concrete invocation (paste-ready):
  ```json
  {
    "tool": "mcp__serena__find_declaration",
    "arguments": {
      "relative_path": "src/auth/handler.py",
      "regex": "session\\.(authenticate)\\(",
      "containing_symbol_name_path": "LoginHandler/post",
      "include_info": true
    }
  }
  ```
- Rubric inputs affected: `S_dev_density` is computed more precisely — unmapped hunks resolve to declarations instead of being counted as "unmappable."
- Audit-log field(s) emitted: `find_declaration_invoked: bool`, `declaration_resolutions: <int>`, `find_declaration_no_match: <int>`.
- Return-contract addition(s): under §9.1 — `hunk_to_declaration_map_path: <abs path>` (UC-2 only).
- Fail-open behavior: on empty / error, fall back to `Grep` against the identifier across the project; mark `degraded: ["find_declaration"]`; the hunk remains in the un-anchored bucket.

**Interaction with adjacent sc:reflect mechanics:**
`find_declaration` is the canonical entry into the §6.1 chain when the input is a diff-hunk (UC-2's natural shape) rather than a symbol name. It eliminates the §4.1 step 1B.3 "false-positive overlap edges from name collisions" problem by anchoring each hunk to a unique symbol identity. Combined with `find_implementations` it forms a two-step "what is this called from and what implements it" pivot. Consumer-side note: the resolved declaration object can be passed directly to `find_referencing_symbols` and `find_implementations`, so the chain composes without re-querying.

---

### 3. `find_referencing_code_snippets`

**Canonical documentation:**
- [Serena CHANGELOG — 2025-04-07 entry](https://github.com/oraios/serena/blob/main/CHANGELOG.md) — "New tool: FindReferencingCodeSnippets" (the first appearance).
- [Tools page](https://oraios.github.io/serena/01-about/035_tools.html) — *NOT listed* in the current active tool inventory under the LSP/JetBrains backend tool tables.
- [Tool inventory dump from Serena startup logs (Issue #254, n=33 tools)](https://github.com/oraios/serena/discussions/254) — `find_referencing_code_snippets` does **not** appear in the loaded-tools log; only `find_referencing_symbols` is listed.
- context7: `/oraios/serena` retrieval surfaced no current API entry for `find_referencing_code_snippets` — every retrieval that named the term landed on the v0.1 changelog footnote.

**Tool signature:**
```
unknown / not surfaced — see status note below
```
- Parameters: **unknown / not surfaced** in current docs.
- Returns: **unknown / not surfaced**.
- Errors / known exceptions: **unknown / not surfaced**.

**Status note (CRITICAL).** Based on the [v1.0.0 changelog entry "Replaced `ReplaceRegexTool` with `ReplaceContentTool`"](https://github.com/oraios/serena/blob/main/CHANGELOG.md) and the [v1.5.0 entry "Extended Symbol Information"](https://github.com/oraios/serena/blob/main/news/20260111.html) which states "The find_symbol and find_referencing_symbols tools have been updated to provide more comprehensive information about symbols. These tools now return additional details including docstrings and signatures", combined with the absence of `find_referencing_code_snippets` from both the [Tools doc page](https://oraios.github.io/serena/01-about/035_tools.html) and the active-tools log in [Issue #254](https://github.com/oraios/serena/discussions/254), the tool appears to have been **absorbed into `find_referencing_symbols`** in v1.0 (the extended-info return shape covers what the standalone tool used to provide). The matrix row may be obsolete — verify against the current serena MCP tool list at adoption time.

**Best-practice usage patterns:**
- Pattern 1 — *Pre-adoption probe*: invoke `mcp__serena__find_referencing_code_snippets` once at Wave 0 with a known symbol; if the tool 404s, fall through to the v1.0 absorption story above and use `find_referencing_symbols` with `include_info: true`.
- Pattern 2 — *Migration*: if confirmed absorbed, the matrix entry's "Medium" value transfers to using `find_referencing_symbols` with the new extended-info return, since the compact grouped excerpts are now part of that tool's response shape per [v1.5 news](https://github.com/oraios/serena/blob/main/news/20260111.html).

**Failure modes / gotchas:**
- Likely **removed/absorbed**, per the inventory evidence above; the canonical adoption path is `find_referencing_symbols` with extended-info, not a separate tool.
- If the tool still exists in some Serena configurations (older clients pinned to pre-v1.0), the signature has not been documented in the current docs site — assume the v1.5 extended-info `find_referencing_symbols` is the supported surface.

**Version / language-server dependencies:**
- Introduced in: Serena **2025-04-07** development snapshot per [CHANGELOG](https://github.com/oraios/serena/blob/main/CHANGELOG.md).
- Languages supported: all LSP-backed languages (when active).
- **Status: likely deprecated / absorbed into `find_referencing_symbols` extended-info as of v1.5.0** — research thin; primary source data is contradictory.

**sc:reflect wiring (sample use case):**
- Wave: 1A (§6.1 step 4 substitute) — proposed in the matrix.
- Insertion point: SKILL.md §6.1 step 4 (`find_referencing_symbols <symbol>`). The matrix recommended substitution; given the absorption evidence, the **actual implementation path** is to add `include_info: true` to the existing `find_referencing_symbols` call instead.
- Concrete invocation (paste-ready — substituted form):
  ```json
  {
    "tool": "mcp__serena__find_referencing_symbols",
    "arguments": {
      "name_path": "AuthHandler",
      "relative_path": "src/handlers/auth.py",
      "include_info": true
    }
  }
  ```
- Rubric inputs affected: same as today; the matrix's "denser packaging" value materialises through the v1.5 extended-info return shape, not a new tool call.
- Audit-log field(s) emitted: `references_extended_info_used: bool` (replaces `find_referencing_code_snippets_invoked`).
- Return-contract addition(s): none — the substitution reuses existing fields.
- Fail-open behavior: identical to existing `find_referencing_symbols` fallback (§6.5).

**Interaction with adjacent sc:reflect mechanics:**
Given the absorption story, this matrix row reduces to a one-line change in §6.1: add `include_info: true` to the existing step-4 call. The "denser packaging" + "reduced token cost when reference counts are high" objectives transfer to that flag. The top-30 cap in [§4.1 step 1B.3](file:///config/workspace/IronClaude/.claude/worktrees/reflect-v3-serena-research/src/superclaude/skills/sc-reflect-protocol/SKILL.md) is unchanged. Recommended task-builder pre-step: emit a `serena_info` probe (per [v1.2.0 changelog](https://github.com/oraios/serena/blob/main/CHANGELOG.md)) to enumerate the current Serena tool inventory and confirm `find_referencing_code_snippets` is or is not present before merging the wiring.

---

### 4. `find_symbol(search_deps=True)`

**Canonical documentation:**
- [Serena CHANGELOG — v1.1.2 entry](https://github.com/oraios/serena/blob/main/CHANGELOG.md) — "JetBrains: `FindSymbolTool`: Force `search_deps=True` if `relative_path` pertains to external dependencies."
- [Junie-on-tianshou evaluation — Reliability & Correctness section](https://github.com/oraios/serena/blob/main/docs/04-evaluation/030_results/050_junie_plugin_on_tianshou.md) — "Serena offers an advantage in accessing symbols within installed packages via `search_deps=true`, a capability not present in built-in tools without manual navigation of virtual environments."
- [Copilot-CLI-on-ente evaluation](https://github.com/oraios/serena/blob/main/docs/04-evaluation/030_results/030_copilot_cli_on_ente.md) — Rust + TypeScript worked examples.
- context7: `/oraios/serena` retrieval surfaced the two-step external-dep pattern `find_declaration → find_symbol(search_deps=True)`.

**Tool signature:**
```json
{
  "tool": "find_symbol",
  "arguments": {
    "name_path_pattern": "ReferencesSearch/search[0]",
    "relative_path": "<ext:ReferencesSearch.class|466808a0>",
    "include_body": true,
    "search_deps": true
  }
}
```
- Parameters: `name_path_pattern`, plus all standard `find_symbol` args; `search_deps` (bool) — when `true`, searches project-external dependencies; `relative_path` (when prefixed with `<ext...>` identifier surfaced by `find_declaration`, points at an external symbol).
- Returns: same shape as `find_symbol` — `{kind, name_path, relative_path, body_location, children, info?}` per [context7](https://context7.com/oraios/serena/llms.txt).
- Errors / known exceptions: per [v1.1.2 changelog](https://github.com/oraios/serena/blob/main/CHANGELOG.md), JetBrains backend **forces** `search_deps=true` when `relative_path` is an external-dep identifier — passing `false` is silently overridden in that case. LSP backend respects the flag.

**Best-practice usage patterns:**
- Pattern 1 — *Spec-referenced library API verification*: when a UC-1 spec cites "matches FastAPI's `Depends` contract", invoke `find_symbol` with `name_path_pattern: "Depends"`, `search_deps: true` to retrieve the upstream signature and verify behavioral equivalence in the tasklist's implementation.
- Pattern 2 — *Two-step external resolution* (per [Codex-on-jbplugin eval](https://github.com/oraios/serena/blob/main/docs/04-evaluation/030_results/020_codex_on_jbplugin.md)): `find_declaration` first to get the `<ext:...>` path, then `find_symbol(relative_path=<ext...>, include_body=true, search_deps=true)`.
- Pattern 3 — *Version-pinning deviation detection*: when an upstream API has changed across the project's pinned dep version, comparing on-disk dep symbol body to the spec-cited contract reveals **Necessary deviation** candidates (pinned-version drift).

**Failure modes / gotchas:**
- LSP must have indexed the project's dependencies — for Python, this means the venv must be the active interpreter; per [Junie-on-tianshou eval](https://github.com/oraios/serena/blob/main/docs/04-evaluation/030_results/050_junie_plugin_on_tianshou.md), this works "provided the IDE has indexed the project's interpreter."
- `<ext:...|HASH>` identifiers are not stable across LS restarts; cannot persist them in memory across reflect runs — must re-resolve via `find_declaration` each time.
- For TypeScript cross-package per [v1.3.0 changelog](https://github.com/oraios/serena/blob/main/CHANGELOG.md), `additional_workspace_folders` must be configured in `project.yml`; absent that, external-dep symbols in sibling packages are not found.

**Version / language-search dependencies:**
- Introduced in: `search_deps` predates v1.0; behavior hardened in [v1.1.2 (2026-04-14)](https://github.com/oraios/serena/blob/main/CHANGELOG.md) (JetBrains force-override) and consistently exposed across backends in v1.3.0.
- Languages supported: Python, Java, TypeScript, Rust, C# (per [eval-result docs](https://github.com/oraios/serena/blob/main/docs/04-evaluation/030_results/)); language-specific via LSP `workspace/symbol` semantics.

**sc:reflect wiring (sample use case):**
- Wave: 1A optional fan-out + 1B (UC-1 spec-cited-third-party check).
- Insertion point: SKILL.md §6.1 — new conditional **step 7**: "IF tasklist OR spec cites a third-party API by name AND that name resolves via `find_declaration` to an external dep: fan out a second `find_symbol` with `search_deps: true` against the dep symbol."
- Concrete invocation (paste-ready):
  ```json
  {
    "tool": "mcp__serena__find_symbol",
    "arguments": {
      "name_path_pattern": "Depends",
      "search_deps": true,
      "include_body": true,
      "include_info": true,
      "max_matches": 1
    }
  }
  ```
- Rubric inputs affected: `S_dev_density` (UC-1 unmapped-requirement ratio improves when third-party APIs become resolvable); new flag `third_party_api_verified` feeds the §10.2 Necessary-deviation classifier.
- Audit-log field(s) emitted: `search_deps_invocations: <int>`, `external_symbols_resolved: <int>`, `external_resolution_failures: <int>`.
- Return-contract addition(s): under §9.1 — `third_party_api_grounding: [<list of {api_name, dep_version, resolution_path}>]`.
- Fail-open behavior: if external resolution fails (un-indexed venv, missing `additional_workspace_folders`), emit `degraded: ["search_deps:lsp_unindexed"]` and skip the verification step; the third-party claim remains `[INFERRED]` per §11.1.

**Interaction with adjacent sc:reflect mechanics:**
This is a Necessary-deviation booster (§10.2). Today, when a spec says "matches FastAPI's `Depends` contract" and the tasklist implements something slightly different, reflect cannot ground the divergence in upstream truth — the §10.2 detection signal "does NOT contradict any acceptance criterion in the spec" remains undecidable. With `search_deps: true`, reflect retrieves the upstream signature, anchors the divergence, and converts what was an `[INFERRED]` finding into a Grounded one. This composes naturally with [§4.1 step 1B.3](file:///config/workspace/IronClaude/.claude/worktrees/reflect-v3-serena-research/src/superclaude/skills/sc-reflect-protocol/SKILL.md)'s cross-task scan when multiple tasks depend on the same upstream API.

---

### 5. `summarize_changes`

**Canonical documentation:**
- [Serena Issue #1296 — tool inventory](https://github.com/oraios/serena/issues/1296) — "`summarize_changes`: Provides instructions for summarizing the changes made to the codebase."
- [Serena Discussion #254 — Loaded tools log (v0.1.4 era, n=33)](https://github.com/oraios/serena/discussions/254) — `summarize_changes` listed in active tools alongside `prepare_for_new_conversation`.
- [LobeHub serena-mcp-agent skill](https://lobehub.com/zh/skills/neversight-skills_feed-serena-mcp-agent) — "Pattern: End sessions with `summarize_changes → write_memory`."
- context7: `/oraios/serena` retrieval did NOT surface a verbatim API signature; the tool is *prompt-based* (provides instructions, doesn't run a computation).

**Tool signature:**
```
unknown / not surfaced — no parameters documented in primary sources
```
- Parameters: **unknown / not surfaced**. Based on the [Issue #1296 description](https://github.com/oraios/serena/issues/1296), the tool is a **prompt-provider**: it returns instructions to the LLM rather than computing a diff. No documented arguments.
- Returns: a prompt-template string instructing the LLM to summarize changes made during the session (inferred from "Provides instructions for summarizing the changes" wording in [#1296](https://github.com/oraios/serena/issues/1296)).
- Errors / known exceptions: per [v1.2.0 changelog](https://github.com/oraios/serena/blob/main/CHANGELOG.md) "Prompt provision is now session-aware (HTTP mode)" — implies the prompt content depends on session state; cross-session invocation outside an active session returns an empty/generic prompt.

**Best-practice usage patterns:**
- Pattern 1 — *End-of-session memory persistence* (per [LobeHub skill](https://lobehub.com/zh/skills/neversight-skills_feed-serena-mcp-agent)): chain `summarize_changes → write_memory` to capture session work into project memory. This is the canonical adopter pattern.
- Pattern 2 — *Pre-`prepare_for_new_conversation` snapshot*: per [Vibetools complete guide](https://vibetools.net/posts/serena-mcp-complete-guide), `summarize_changes` is the natural pre-cursor to `prepare_for_new_conversation` (clears context but preserves a summary).
- Pattern 3 — *Independent drift signal*: the matrix's proposed use — corroborate user-supplied diff with Serena's session-internal change record.

**Failure modes / gotchas:**
- **Not a computed diff** — it's a *prompt* returned to the LLM telling the LLM to summarize. Reflect must treat the output as model-generated narrative, not ground truth. The matrix's "independent check on what was *actually* changed" claim is **weaker than implied** — independent of the user-supplied diff, but still mediated by the same model orchestrating reflect.
- Session-aware per [v1.2.0 changelog](https://github.com/oraios/serena/blob/main/CHANGELOG.md): in stdio mode (the default for Claude Code), the session is the client connection; reflect must invoke it within the same MCP session as the actual edits, or the prompt has no edits to summarize.

**Version / language-server dependencies:**
- Introduced in: pre-v1.0 (visible in the 2026-03 development snapshot at [Discussion #254](https://github.com/oraios/serena/discussions/254)).
- Languages supported: language-agnostic (it's a meta-tool, not LSP-backed).

**sc:reflect wiring (sample use case):**
- Wave: 1A (UC-2 only — corroboration signal vs. supplied diff).
- Insertion point: SKILL.md §6.1 after step 6 (the re-Read), as a new step 7 (UC-2 only): "Invoke `summarize_changes` and store the prompt output alongside the user-supplied diff."
- Concrete invocation (paste-ready):
  ```json
  {
    "tool": "mcp__serena__summarize_changes",
    "arguments": {}
  }
  ```
- Rubric inputs affected: `S_dev_density` — when the Serena summary diverges from the supplied diff (named files, hunk counts), the ratio of "claimed-but-unrecorded changes" feeds upward into ambiguity scoring.
- Audit-log field(s) emitted: `summarize_changes_invoked: bool`, `summarize_changes_path: <output>/serena-change-summary.md`.
- Return-contract addition(s): under §9.1 UC-2 block — `serena_summary_corroboration: agree | partial | disagree | unavailable`.
- Fail-open behavior: if Serena was invoked across a session boundary (reflect runs in a *fresh* session vs. the edit session), the summary is generic — emit `serena_summary_corroboration: unavailable` and skip the Drift-boost logic; no degradation to the main verdict.

**Interaction with adjacent sc:reflect mechanics:**
Slots in as a cheap pre-evidence-validator signal for §10.3 Drift detection. When the Serena summary names files NOT in the supplied diff, that's a strong Drift candidate. When the diff names files NOT in the Serena summary, that's a Necessary-deviation candidate (the work may have happened outside the Serena-instrumented session). Both feed §10.5 precedence resolution. The tool does NOT replace `git diff` — it's a corroboration, not a source-of-truth. Reflect's existing reliance on `--diff` / `--commit-range` is preserved per [SKILL.md §3.1](file:///config/workspace/IronClaude/.claude/worktrees/reflect-v3-serena-research/src/superclaude/skills/sc-reflect-protocol/SKILL.md).

---

### 6. `check_onboarding_performed`

**Canonical documentation:**
- [Serena CHANGELOG — v1.5.0 entry (2026-05-18)](https://github.com/oraios/serena/blob/main/CHANGELOG.md) — **"Tools: Delete `check_onboarding_performed` tool (instead extend project activation message)"**.
- [Serena Issue #1296 — historical inventory](https://github.com/oraios/serena/issues/1296) — pre-v1.5 description: "Checks whether project onboarding was already performed."
- [Serena memories docs](https://github.com/oraios/serena/blob/main/docs/02-usage/045_memories.md) — onboarding mechanism overview.
- context7: `/oraios/serena` retrieval did NOT surface a current API for the tool; only historical references.

**Tool signature:**
```
DELETED in v1.5.0 — no signature in current Serena
```
- Parameters: **n/a — tool no longer exists**.
- Returns: **n/a**.
- Errors / known exceptions: in v1.5.0+, invoking this tool name returns an MCP "tool not found" error.

**Critical status update (BLOCKS THE MATRIX ROW AS WRITTEN).** Per the [v1.5.0 changelog](https://github.com/oraios/serena/blob/main/CHANGELOG.md) shipped 2026-05-18, `check_onboarding_performed` was **removed** in favor of extending the `activate_project` response message to carry the onboarding status. The matrix row's "Plain check in Wave 0" path is no longer available as a separate tool call. The information is still surfaced, but through `activate_project`'s message body (per [v1.2.0 changelog](https://github.com/oraios/serena/blob/main/CHANGELOG.md): "Always provide full activation message upon calling `activate_project`") and/or by inspecting whether `list_memories` returns entries seeded by the onboarding flow (the [memory_maintenance seed memory](https://oraios.github.io/serena/02-usage/045_memories.html#the-memory-maintenance-memory), new in v1.5.0).

**Best-practice usage patterns (post-v1.5):**
- Pattern 1 — *Parse activate_project response*: reflect already invokes `activate_project` at Wave 0 ([SKILL.md §4 Wave 0.7](file:///config/workspace/IronClaude/.claude/worktrees/reflect-v3-serena-research/src/superclaude/skills/sc-reflect-protocol/SKILL.md)); the v1.5 message body carries onboarding-status text. Parse for the marker.
- Pattern 2 — *list_memories seed-presence probe*: invoke `list_memories` at Wave 0 (already in `allowed-tools` per the conversation-context [§2 inventory](file:///config/workspace/IronClaude/.claude/worktrees/reflect-v3-serena-research/.dev/releases/backlog/Reflect-V3-Serena/03-conversation-context.md)) and check for the presence of the v1.5 seeded `memory_maintenance` memory; its presence is a structural proxy for "onboarding ran."

**Failure modes / gotchas:**
- The matrix row's premise is **invalidated by upstream removal**. Adopting the row as written would emit MCP tool-not-found errors against any Serena ≥ v1.5.
- The v1.5 replacement signals are *less binary*: the activation-message text is a natural-language string requiring parsing; the memory-presence proxy can yield false negatives if onboarding was skipped via the `no-onboarding` mode per [memories docs](https://github.com/oraios/serena/blob/main/docs/02-usage/045_memories.md#disabling-memories-and-onboarding).

**Version / language-server dependencies:**
- Introduced in: pre-v1.0 (visible in [Discussion #254 v0.1.4 era loaded-tools list](https://github.com/oraios/serena/discussions/254)).
- **REMOVED in: Serena v1.5.0 (2026-05-18)** per [CHANGELOG](https://github.com/oraios/serena/blob/main/CHANGELOG.md).
- Languages supported: language-agnostic.

**sc:reflect wiring (sample use case — REVISED for post-v1.5):**
- Wave: 0 — alongside the existing `activate_project` step.
- Insertion point: SKILL.md §4.0 — augment **step 0.7** "Activate Serena project + memory hydrate" to parse the activation message for the v1.5 onboarding-status marker. Do NOT introduce a new tool call.
- Concrete invocation (paste-ready — revised):
  ```python
  # Use the activate_project response we already have at Wave 0.7
  resp = mcp__serena__activate_project(project="...")
  onboarding_performed = "onboarding" in resp.lower() and "performed" in resp.lower()
  # Fallback proxy: presence of v1.5 seed memory
  memos = mcp__serena__list_memories()
  onboarding_proxy = any(m == "memory_maintenance" for m in memos)
  ```
- Rubric inputs affected: `S_dev_density` calibration — the matrix's intent ("rubric weighted by whether project memory was bootstrapped") is preserved through the activation-message parse + list_memories probe.
- Audit-log field(s) emitted: `onboarding_status: bootstrapped | not_bootstrapped | unknown`, `onboarding_status_source: activation_msg | list_memories_proxy | unknown`.
- Return-contract addition(s): under §9.2 telemetry — `onboarding_status: <string>`.
- Fail-open behavior: when neither source is conclusive, emit `onboarding_status: unknown` and DO NOT down-weight `S_dev_density`; treat as no signal.

**Interaction with adjacent sc:reflect mechanics:**
The signal-mechanism the matrix targets ("grounding-confidence by whether project memory was bootstrapped") survives the v1.5 deletion — only the *plumbing* changes. Reflect already invokes both `activate_project` and `list_memories` at Wave 0; this row becomes a parsing addition, not a new tool wiring. Task-builder note: this row's MDTM task MUST cite the v1.5.0 deletion explicitly so the implementer doesn't add a now-defunct tool to `allowed-tools`.

---

### 7. `get_current_config`

**Canonical documentation:**
- [Serena Issue #1296 — tool description](https://github.com/oraios/serena/issues/1296) — "Prints the current configuration of the agent, including the active and available projects, tools, contexts, and modes."
- [Serena Discussion #254 — active-tools log](https://github.com/oraios/serena/discussions/254) — `get_current_config` listed alongside `serena_info` and `initial_instructions`.
- [Serena Configuration page](https://oraios.github.io/serena/02-usage/050_configuration.html) — discusses what config fields exist; `get_current_config` is the runtime read of that config.
- context7: `/oraios/serena` retrieval surfaced CLI-side `serena context list` / `serena mode list` adjacent commands; the in-MCP tool returns the *runtime* view.

**Tool signature:**
```
unknown / not surfaced — parameters not documented; treated as zero-arg
```
- Parameters: **unknown / not surfaced**. Based on the [v0.1.3 changelog](https://github.com/oraios/serena/blob/main/CHANGELOG.md) Windows-hang fix entry ("Fix `ExecuteShellCommandTool` and `GetCurrentConfigTool` hanging on Windows"), the tool runs with no arguments.
- Returns: a structured (likely YAML or JSON-rendered) string describing: active project, available projects, loaded tools list, current context, current modes, and language-backend selection — per [Issue #1296 description](https://github.com/oraios/serena/issues/1296) and [Discussion #254 startup-log shape](https://github.com/oraios/serena/discussions/254) (the same fields the startup log prints).
- Errors / known exceptions: per [v0.1.3 changelog](https://github.com/oraios/serena/blob/main/CHANGELOG.md), historical Windows hang; resolved by removing asyncio dependence.

**Best-practice usage patterns:**
- Pattern 1 — *Wave-0 environment fingerprint*: invoke once at Wave 0 to capture the deterministic configuration in audit. This is the canonical "what context+modes+tool-set is reflect running against" probe.
- Pattern 2 — *Degraded-component detection*: per [§4 Wave 0 routing](file:///config/workspace/IronClaude/.claude/worktrees/reflect-v3-serena-research/src/superclaude/skills/sc-reflect-protocol/SKILL.md), reflect probes alias env vars but not Serena's own active context. `get_current_config` closes that gap — e.g., if a user accidentally launched Serena with `--context ide-assistant` (which excludes 6 tools per [Discussion #254](https://github.com/oraios/serena/discussions/254)), reflect can detect the missing tools and downgrade gracefully.
- Pattern 3 — *Reproducibility envelope*: capture into `<output>/serena-config-snapshot.yaml` for cross-run reproducibility / meta-eval.

**Failure modes / gotchas:**
- Output shape is **not stable across Serena versions** — context+modes evolved across v1.0 → v1.5 per [CHANGELOG](https://github.com/oraios/serena/blob/main/CHANGELOG.md). Parsers should defensively check field presence.
- Pre-v0.1.3 Windows hang per [CHANGELOG](https://github.com/oraios/serena/blob/main/CHANGELOG.md); not a concern post-v1.0, but minimum supported version is implicitly v1.0+.
- Some single-project contexts (`ide`, `claude-code`) **disable** the `activate_project` tool entirely per [Configuration docs](https://github.com/oraios/serena/blob/main/docs/02-usage/050_configuration.md); reflect must not blindly assume `activate_project` succeeded — `get_current_config` reveals this.

**Version / language-server dependencies:**
- Introduced in: pre-v1.0; stable as of [v1.0.0](https://github.com/oraios/serena/blob/main/CHANGELOG.md).
- Languages supported: language-agnostic (meta-tool).

**sc:reflect wiring (sample use case):**
- Wave: 0.
- Insertion point: SKILL.md §4.0 — new **step 0.5c** between alias resolution (step 0.5) and vendor heterogeneity (step 0.6): "Invoke `get_current_config`; parse the active context + modes + tool list; persist to `<output>/serena-config-snapshot.yaml`."
- Concrete invocation (paste-ready):
  ```json
  {
    "tool": "mcp__serena__get_current_config",
    "arguments": {}
  }
  ```
- Rubric inputs affected: composes into `degraded_components` (existing in §9.2). When the active context excludes tools that reflect's chain depends on (e.g., `get_diagnostics_for_file`), `degraded_components` gains `["serena:context-excluded"]` and `S_dev_density` is up-weighted.
- Audit-log field(s) emitted: `serena_context: <string>`, `serena_modes: [<list>]`, `serena_tool_count: <int>`, `serena_excluded_tools: [<list>]`.
- Return-contract addition(s): under §9.2 telemetry — `serena_config_snapshot_path: <abs path>`, `serena_active_context: <string>`, `serena_active_modes: [<list>]`.
- Fail-open behavior: if the call fails (Serena down, tool unavailable in active context), emit `degraded: ["get_current_config"]` and skip the snapshot; the rest of Wave 0 continues.

**Interaction with adjacent sc:reflect mechanics:**
This is a Wave 0 calibration tool — it informs the §4 Wave 0 alias-routing table by adding a "context-exclusion overlay" check. For instance, if alias resolution says "3 model classes available" but `get_current_config` reveals the active context excludes `find_referencing_symbols`, the §6.1 chain is structurally degraded regardless of model diversity, and `t2_model_class_diversity: full` becomes misleading. Combined with the [§14 degraded-mode envelope](file:///config/workspace/IronClaude/.claude/worktrees/reflect-v3-serena-research/src/superclaude/skills/sc-reflect-protocol/SKILL.md), reflect's "what's actually available" picture sharpens significantly.

---

### 8. `delete_memory` / `rename_memory` / `edit_memory`

**Canonical documentation:**
- [Serena Memory Tools docs](https://github.com/oraios/serena/blob/main/docs/02-usage/045_memories.md) — "file-backed memory system with tools like `write_memory`, `read_memory`, `list_memories`, `edit_memory`, `delete_memory`, and `rename_memory`."
- [Serena CHANGELOG — v1.5.0 entry (2026-05-18)](https://github.com/oraios/serena/blob/main/CHANGELOG.md) — "Memories can now reference each other using the `mem:` convention. Renames propagate to all references automatically. See the reference convention."
- [Serena CLI subcommands](https://oraios.github.io/serena/02-usage/045_memories.html#cli-subcommands) — `serena memories list / read / write / check / auto-prefix-references`.
- context7: `/oraios/serena` retrieval surfaced verbatim JSON call examples for each tool.

**Tool signatures:**

```json
// delete_memory
{
  "tool": "delete_memory",
  "arguments": { "memory_name": "project_structure" }
}

// rename_memory
{
  "tool": "rename_memory",
  "arguments": {
    "old_name": "project_structure",
    "new_name": "architecture/project_structure"
  }
}

// edit_memory
{
  "tool": "edit_memory",
  "arguments": {
    "memory_name": "project_structure",
    "needle": "- serena/cli\\.py: CLI commands",
    "repl": "- serena/cli.py: CLI commands (top-level entry: `top_level`)",
    "mode": "regex"
  }
}
```
- Parameters per [context7](https://context7.com/oraios/serena/llms.txt):
  - `delete_memory`: `memory_name` (string).
  - `rename_memory`: `old_name`, `new_name`. Per [v1.5.0 changelog](https://github.com/oraios/serena/blob/main/CHANGELOG.md), `mem:` cross-references propagate automatically.
  - `edit_memory`: `memory_name`, `needle` (literal or regex), `repl`, `mode` ∈ {`literal`, `regex`}, optional `allow_multiple_occurrences: bool` (false by default; multiple matches error out — same DSL as `replace_content`).
- Returns: status confirmation (specific shape **unknown / not surfaced**, but follows the Serena convention of returning success markers per [memory docs](https://github.com/oraios/serena/blob/main/docs/02-usage/045_memories.md)).
- Errors / known exceptions: per [v1.2.0 changelog](https://github.com/oraios/serena/blob/main/CHANGELOG.md), `".."` in memory names is **forbidden** (path-traversal guard); `read_only_memory_patterns` config option (per [v1.0.0 changelog](https://github.com/oraios/serena/blob/main/CHANGELOG.md)) makes some memories non-editable / non-deletable; `ignored_memory_patterns` excludes some from listing.

**Best-practice usage patterns:**
- Pattern 1 — *Sliding-window retention*: pair `list_memories` + filter on a slug prefix + `delete_memory` for entries older than N. This is the §6.3 "20-entry retention" mechanism the matrix calls out.
- Pattern 2 — *Mem-reference-safe migration* (per [v1.5.0 changelog](https://github.com/oraios/serena/blob/main/CHANGELOG.md)): when renaming a memory, use `rename_memory` instead of delete+write so cross-references via `mem:` propagate. Hand-rolled delete+write breaks the v1.5 reference graph.
- Pattern 3 — *Targeted append-via-edit*: `edit_memory` with regex `\\Z` and a multi-line `repl` is the canonical append (avoids full rewrite + preserves provenance).
- Pattern 4 — *Referential-integrity audit*: per [CLI subcommands](https://oraios.github.io/serena/02-usage/045_memories.html#cli-subcommands), `serena memories check` validates the `mem:` reference graph; reflect's Wave 0 hydrate path can mirror this in-process.

**Failure modes / gotchas:**
- `rename_memory` propagation behavior was introduced **only in v1.5.0** per [CHANGELOG](https://github.com/oraios/serena/blob/main/CHANGELOG.md) — on older Serena, references break silently. Reflect should check `get_current_config` for Serena version before relying on auto-propagation.
- `edit_memory` regex mode uses Python `re` semantics with MULTILINE + DOTALL (per the analogous [replace_content tool description](https://context7.com/oraios/serena/llms.txt)); the `allow_multiple_occurrences` default of `false` is a footgun — multi-match silently errors.
- Path-traversal guard per [v1.2.0 changelog](https://github.com/oraios/serena/blob/main/CHANGELOG.md): names containing `..` are rejected. Reflect's slug derivation must sanitize.
- Read-only patterns per [v1.0.0 changelog](https://github.com/oraios/serena/blob/main/CHANGELOG.md): some memories may resist deletion if matched by `read_only_memory_patterns`.

**Version / language-server dependencies:**
- Introduced in: `delete_memory` pre-v1.0; `rename_memory` + `edit_memory` + `mem:` propagation in **v1.5.0 (2026-05-18)** per [CHANGELOG](https://github.com/oraios/serena/blob/main/CHANGELOG.md).
- Languages supported: language-agnostic.

**sc:reflect wiring (sample use case):**
- Wave: 5 persist (§6.3) — currently only `write_memory`.
- Insertion point: SKILL.md §6.3 — append a retention block executed after the two existing `write_memory` calls:
  ```
  list_memories
  → filter by prefix "reflect/last-pass-{slug}/" or "reflect/deviation-patterns-{slug}/"
  → sort by recency metadata
  → IF count > 20 OR age > 90d: delete_memory(name)
  → emit retention_actions to audit
  ```
  Also §6.3 RENAME path: when project-slug-derivation rules change between releases, `rename_memory` preserves cross-references.
- Concrete invocation (paste-ready — retention sweep):
  ```python
  memos = mcp__serena__list_memories()
  slug_memos = sorted([m for m in memos if m.startswith(f"reflect/last-pass-{slug}/")])
  if len(slug_memos) > 20:
      for m in slug_memos[:-20]:
          mcp__serena__delete_memory(memory_name=m)
  # 90-day TTL sweep
  for m in slug_memos:
      if (now - memory_mtime(m)).days > 90:
          mcp__serena__delete_memory(memory_name=m)
  ```
- Rubric inputs affected: none directly; this is an operational hygiene addition.
- Audit-log field(s) emitted: `memory_retention_sweep_invoked: bool`, `memories_deleted: <int>`, `memories_renamed: <int>`, `memories_edited: <int>`.
- Return-contract addition(s): under §9.2 telemetry — `memory_retention_actions: <int>`, `memory_retention_skipped_readonly: <int>`.
- Fail-open behavior: per existing [Error Handling Matrix row "Serena `write_memory` fails at Wave 5"](file:///config/workspace/IronClaude/.claude/worktrees/reflect-v3-serena-research/src/superclaude/skills/sc-reflect-protocol/SKILL.md), memory persistence is best-effort; retention failures inherit the same posture — emit `memory_retention_failed: true`, do NOT block the report.

**Interaction with adjacent sc:reflect mechanics:**
This row closes a **specified-but-not-implemented** loop in [§6.3](file:///config/workspace/IronClaude/.claude/worktrees/reflect-v3-serena-research/src/superclaude/skills/sc-reflect-protocol/SKILL.md): "keep last 20 entries per key; expire >90 days" is currently aspirational — `write_memory` accumulates. The three CRUD tools make the retention rule enforceable. Critical interaction with the v1.5 `mem:` reference convention: if reflect ever cross-references its own memory entries (e.g., `reflect/deviation-patterns-{slug}` referencing `reflect/last-pass-{slug}`), `rename_memory` MUST be used over delete+write to avoid breaking the reference graph. Task-builder MDTM for this row should mandate the v1.5 minimum-version check in the implementer's Wave 0 step (via `get_current_config` per row 7), with a fall-back to write-only-no-retention on pre-v1.5 Serena.

---

## Cross-feature observations

**Adoption ordering recommendation.**

Recommended single-PR groupings and prerequisite chain:

1. **Phase 0 — Reclassify row 6 BEFORE wiring anything.** The matrix's `check_onboarding_performed` row is **invalidated** by the [v1.5.0 deletion](https://github.com/oraios/serena/blob/main/CHANGELOG.md). The replacement signal is an `activate_project` response-message parse + a `list_memories` seed-presence proxy. The MDTM task for this row should cite the deletion verbatim and prevent the implementer from adding a now-defunct tool name to `allowed-tools`.

2. **Phase 1 (single PR) — Symbol-chain extension: rows 1 + 2.** `find_implementations` and `find_declaration` were introduced together in [v1.3.0](https://github.com/oraios/serena/blob/main/CHANGELOG.md), share the same §6.1 Wave 1A insertion neighborhood, and share schema additions (declaration-anchor field + implementations-list field on the reflection card). They should ship together to avoid contract-version churn.

3. **Phase 2 (single PR) — Cheap diff-density signal: row 4.** `find_symbol(search_deps=True)` is a one-flag addition gated on an "is third-party API referenced" predicate; no chain restructure required. It depends on row 2 (`find_declaration` is the entry that surfaces `<ext:...>` paths), so phase 2 must follow phase 1.

4. **Phase 3 (single PR) — Memory lifecycle: row 8.** `delete_memory` + `rename_memory` + `edit_memory` close the §6.3 retention loop. This should ship before sc:reflect sees real production use; an unbounded `write_memory` accumulator is an operational hazard at the 6-month horizon. Prerequisite: a `get_current_config` (row 7) check that the active Serena is ≥ v1.5 (for `rename_memory` propagation).

5. **Phase 4 (single PR) — Wave 0 calibration: rows 6 + 7.** Both feed `S_dev_density` calibration and `degraded_components` enrichment. Row 7's `get_current_config` snapshot also gates row 8's safe-rename, so it's a structural prerequisite. Combined PR is natural — same audit-log section, same `<output>/` artifact directory.

6. **Phase 5 (low-priority) — Drift corroboration: row 5.** `summarize_changes` is independent of the chain; it's a UC-2-only signal addition. Ship last because the cost/benefit is marginal (the tool is prompt-based, not a computed diff).

7. **Defer / verify upstream — row 3.** `find_referencing_code_snippets` appears to have been **absorbed into `find_referencing_symbols` extended-info** in v1.0+. The implementation reduces to adding `include_info: true` to the existing call. Task-builder should add a Wave 0 `serena_info` probe (per [v1.2.0 changelog](https://github.com/oraios/serena/blob/main/CHANGELOG.md)) to mechanically confirm before merging.

**Overlap analysis.**

- **Single-PR clusters:** rows {1, 2}; rows {6, 7}; rows {8} (all three CRUD tools together — they share state and one MDTM task is cleaner than three).
- **Cross-row schema interactions:** rows 1 + 2 share the reflection-card extension; rows 6 + 7 share telemetry under §9.2; rows 4 + 5 both feed §10.2/10.3 deviation-classifier signals.
- **Version-gating coupling:** rows 6 + 8 both require a Serena-version check (row 6 because the old tool is gone, row 8 because `rename_memory` propagation is v1.5+). Row 7 (`get_current_config`) is the natural version-fingerprint source for both — implementing row 7 first reduces the wiring cost for both other rows.
- **Bulk contract bump:** rows 1, 2, 4, 8 each add fields to the return contract; bundling phases 1-3 into a single `contract_version: 1.1.0` minor bump (per the [§9.4 evolution policy](file:///config/workspace/IronClaude/.claude/worktrees/reflect-v3-serena-research/src/superclaude/skills/sc-reflect-protocol/SKILL.md)) is cheaper than three sequential minor bumps.

**Outstanding research gaps.**

- **Row 3 (`find_referencing_code_snippets`)**: primary-source data is thin. The [CHANGELOG](https://github.com/oraios/serena/blob/main/CHANGELOG.md) introduces it in 2025-04-07 but the [current Tools page](https://oraios.github.io/serena/01-about/035_tools.html) and [Discussion #254 active-tools log](https://github.com/oraios/serena/discussions/254) don't include it. The v1.5 [extended-info release note](https://github.com/oraios/serena/blob/main/news/20260111.html) suggests absorption. Recommended: run a runtime probe against a live Serena MCP before wiring.
- **Row 5 (`summarize_changes`)**: API signature **not surfaced** in any primary source — only the tool's *purpose* is documented. The tool is prompt-based (returns instructions, not a diff). Best-practice patterns are inferred from the [LobeHub skill recipe](https://lobehub.com/zh/skills/neversight-skills_feed-serena-mcp-agent), not authoritative docs. Recommended: pilot in `.dev/eval-workspaces/sc-reflect/` cases before promoting from Phase 5 status.
- **Row 7 (`get_current_config`)**: return-shape **not surfaced** in any current doc; inferred from the [Serena startup-log shape in Discussion #254](https://github.com/oraios/serena/discussions/254). Implementers should probe the return shape at Wave 0 of the implementing reflect run and fail-open on parse failure.

**One-sentence cross-feature ordering recommendation.** Ship `get_current_config` (row 7) first as the version-fingerprint substrate, then bundle `find_implementations` + `find_declaration` (rows 1 + 2) as a single v1.3.0-gated symbol-chain extension PR, then `find_symbol(search_deps=True)` (row 4), then the memory-lifecycle CRUD trio (row 8) gated on the v1.5 fingerprint — deferring `summarize_changes` (row 5) and the absorbed `find_referencing_code_snippets` (row 3) to a post-eval cleanup pass; the `check_onboarding_performed` row (row 6) collapses into row 7's activate-project parse rather than a separate tool call.

<!-- END: research-agent appended content -->

<!-- END: research-agent appended content -->
