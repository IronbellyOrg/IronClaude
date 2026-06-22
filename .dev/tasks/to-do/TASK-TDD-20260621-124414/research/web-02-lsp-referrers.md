# Web-02: Programmatic LSP / Serena Referrer Resolution

**Task:** TASK-TDD-20260621-124414
**Component context:** Deterministic, LLM-free runtime-surface sweep; OQ-DRS.1 referrer-engine decision.
**Research depth:** light / optional. **Status:** Complete.
**Search backend:** Tavily MCP (`tavily-search`), advanced depth.
**Persistence note:** Authored by a deep-research subagent (no Write tool); persisted verbatim by the orchestrator.

## What we already know (codebase = source of truth)

- The sweep's referrer engine **floor is ripgrep / AST** — for determinism and a no-MCP / no-language-server fallback.
- An LSP / Serena `find_referencing_symbols`-style upgrade is **OPTIONAL** and **must degrade gracefully** when unavailable.

## Findings

### F1 — The LSP referrer contract: `textDocument/references` + `ReferenceParams` + `includeDeclaration`
- **Source:** https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification (High)
- `textDocument/references`; param `ReferenceParams` extends `TextDocumentPositionParams` (`{textDocument:{uri}, position:{line,character}}`) + `context:{includeDeclaration: boolean}`. Response: `Location[]` or `null`. Gated by server `referencesProvider` capability.
- **Position-based, not name-based** — caller must first resolve a symbol's `(uri,line,character)` (via `documentSymbol`/`workspace/symbol`). Our floor is name/pattern-based, no position resolution needed.
- **Verdict:** Extends.

### F2 — LSP is intentionally not a compiler/AST model at the protocol level
- **Source:** https://learn.microsoft.com/en-us/visualstudio/extensibility/language-server-protocol (High)
- Protocol types are editor data types (document, cursor), not ASTs/resolved types. Semantic resolution happens inside the server, behind an opaque, version-dependent boundary. The floor's behavior is fully owned/reproducible by us.
- **Verdict:** Supports the floor's determinism rationale.

### F3 — Precision delta: Serena `find_referencing_symbols` (LSP) vs Grep (ripgrep), measured
- **Source:** https://oraios.github.io/serena/04-evaluation/030_results/010_cc_on_tianshou.html (High, vendor)
- Serena LSP: 63 files, code-only, categorized (import/call/type). Grep: 83 files, flat, includes README/CHANGELOG/.ipynb/comments/strings. Same recall, ~24% of grep hits were non-code surfaces.
- **Relation:** Quantifies the precision gap the floor accepts — ripgrep over-reports (conservative: won't miss a real call, but flags non-runtime mentions). AST is a middle tier.
- **Verdict:** Extends.

### F4 — Serena/LSP referrers categorize usage type (import/call/type annotation); grep cannot
- **Sources:** https://mcp.directory/skills/serena ; https://claudemarketplaces.com/mcp/oraios/serena (Med-High)
- Serena wraps LSP via `multilspy`; `find_referencing_symbols` returns references categorized by kind and grouped by file — distinguishing a `Mock(spec=authenticate)` test ref from a real call.
- **Relation:** Usage-kind categorization is the LSP-only capability most relevant to a runtime-surface oracle (real call/dispatch vs import vs test-only). Directly relevant to `uc2-surface-test-only-ref` and `uc2-surface-dynamic-dispatch`.
- **Verdict:** Extends.

### F5 — Determinism failure mode #1: cold-start indexing returns partial (same-file-only) results
- **Source:** https://github.com/typescript-language-server/typescript-language-server/discussions/1067 (High)
- First `textDocument/references` query returns a subset (often same-file) because the service is still indexing; re-running returns the full set. *"more problematic for coding agents."*
- **Relation:** A direct determinism counterexample — identical input → different output by index warmth. The floor has no warm-up state. **Strongest argument for keeping the floor as the default.**
- **Verdict:** Supports the floor; contradicts "LSP referrers are deterministic out of the box."

### F6 — Determinism failure mode #2: long/variable startup latency; missing refs until indexed
- **Sources:** https://discourse.julialang.org/t/121584 (Julia LS ~40s startup; "Missing reference" until indexed); https://code.visualstudio.com/blogs/2019/02/19/lsif (LSIF precomputes references precisely because live results are expensive/timing-sensitive). (High)
- **Verdict:** Supports the floor (determinism + bounded latency).

### F7 — Availability/handshake fragility: `didOpen` prerequisite; per-server capability deviations
- **Sources:** https://developercommunity.visualstudio.com/content/problem/832032 (clangd refuses requests without prior `didOpen`); https://www.reddit.com/r/vim/comments/b3yzq4 (servers deviate from spec; clients paper over). (Med-High)
- **Relation:** "Unavailable" is multi-valued — server-present-but-erroring, returned-null, returned-partial-subset, unmet-handshake. All must map to DEGRADE.
- **Verdict:** Supports the "must degrade gracefully" requirement.

### F8 — A library-grade programmatic LSP client exists (multilspy / Serena)
- **Sources:** https://github.com/microsoft/multilspy ; https://stackoverflow.com/questions/76756132 (author); https://dev.to/siddhantkcode/how-to-make-ai-code-edits-more-accurate-bbe (High)
- `multilspy.SyncLanguageServer`: `start_server()` context mgr, then `request_references("path", line, col)` → `Location[]`. Handles jedi (Python), rust-analyzer, gopls, JDT.LS, OmniSharp. Python ≥3.10.
- **Relation:** The OPTIONAL upgrade is feasible/Python-native — but inherits F5–F7 caveats; must be wrapped in availability-probe → DEGRADE-to-floor, plus a symbol→position resolution step.
- **Verdict:** Extends.

### F9 — AST search (ast-grep/tree-sitter) is a middle tier, not an LSP substitute
- **Source:** https://www.reddit.com/r/ClaudeAI/comments/1lefmff/ (Med)
- AST removes comment/string false positives and matches structural patterns, but does not resolve which class's method is called, type hierarchies, or overrides — those need LSP's type model. Three-tier model: ripgrep (max recall, deterministic, zero deps) < AST/tree-sitter (removes comment/string noise, deterministic, no dispatch resolution) < LSP/Serena (semantic precision, non-deterministic warm-up + availability dependence).
- **Verdict:** Supports the floor; clarifies AST's place.

## Key External Findings

1. **Contract (F1, F2):** LSP referrer upgrade = `textDocument/references` (`ReferenceParams` position + `context.includeDeclaration`) → `Location[]`, gated by `referencesProvider`. Position-based, precision behind an opaque server model.
2. **Precision win real but bounded (F3, F4, F9):** code-only + usage-kind-categorized; ~24% fewer non-code false positives (63 vs 83). AST is a middle tier.
3. **LSP referrers are NOT deterministic out of the box (F5, F6, F7):** cold-start partial subsets; tens-of-seconds startup; handshake prerequisites; LSIF exists because live results are timing-sensitive.
4. **Availability is multi-valued (F7, F8):** not just "binary missing" — also server-erroring/null/partial/unmet-handshake. All → DEGRADE.
5. **A faithful programmatic client exists (F8):** `multilspy.SyncLanguageServer.request_references` — but inherits all caveats; wrap in availability probe + fallback.

## Recommendations from External Research

1. **Keep ripgrep/AST as the determinism-safe default for OQ-DRS.1.** External primary sources confirm live LSP referrer results are not deterministic without index-warmth control. Nothing found contradicts the floor decision.
2. **Treat LSP/Serena strictly as an OPTIONAL precision overlay, never a dependency** — its win is precision (code-only + usage-kind categorization, relevant to test-only-ref / dynamic-dispatch surfaces), behind an availability gate.
3. **Define DEGRADE broadly:** force DEGRADE-to-floor on any of: server binary absent; no `referencesProvider`; `start_server`/handshake error; `references` errors/times-out/returns `null`/returns a same-file-only subset. Emit an explicit auditable "degraded: LSP unavailable, fell back to ripgrep/AST" signal.
4. **If/when built, use `multilspy.SyncLanguageServer.request_references`** + a symbol→position step + a warm-up/retry-or-degrade guard; pin the language-server version to bound determinism drift.
5. **Determinism contract:** the verdict must be reproducible from the floor alone. LSP may *refine* (prune false positives) but must never be *required* to reach a verdict or change a PASS/FAIL in a non-reproducible way. Floor = ground truth; LSP = optional overlay.

## OQ-DRS.1 conclusion
LSP/Serena referrer resolution is non-deterministic without index-warmth control and availability-dependent → the **ripgrep/AST floor remains the determinism-safe default**; the LSP upgrade stays an OPTIONAL precision overlay that must **DEGRADE to the floor on any unavailability signal** (defined broadly), emitting an explicit auditable degrade marker.
