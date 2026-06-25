VERDICT: PASS

# QA Report — Cross-Cluster Invariant Conformance (X1–X7)

**Topic:** Tavily MCP 0.2.x upgrade — TASK-RF-tavily-mcp-0-2-x-20260623-010952
**Date:** 2026-06-23
**Phase:** report-validation (cross-cluster invariant conformance)
**Lens:** X1–X7 cross-cluster invariants
**Fix authorization:** FALSE (report-only)
**Diff base:** 530505a066d6bfefd43963af67e253ed3070e7af
**Diff scope:** `src/ docs/ tests/` (20 files, +291/-41)

---

## Overall Verdict: PASS

All seven cross-cluster invariants conform. Verified by reading actual files, not agent
claims. One OUT-OF-SCOPE observation recorded (pre-existing test-fixture strings) — does
not affect any invariant as specified.

## Items Reviewed

| # | Invariant | Result | Evidence |
|---|-----------|--------|----------|
| X1 | version 0.2.20 everywhere | PASS | `tavily-mcp@0.2.20` pinned in install_mcp.py:81, MCP_Tavily.md:5, RESEARCH_CONFIG.md:61, docs/user-guide/mcp-servers.md:274, real.yaml:1630. No off-pin `tavily-mcp@<ver>` anywhere. `0.2.x` appears only as descriptive tool-surface label (MCP_Tavily.md:38,40; examples:417; brainstorm SKILL:388) — not a pin leak. Guard `test_tavily_version_single_pin` PASSES. |
| X2 | single config source; orphans deleted | PASS | `ls` confirms BOTH `src/superclaude/mcp/configs/tavily.json` AND `plugins/superclaude/mcp/configs/tavily.json` do NOT exist on disk. Diff shows `src/.../tavily.json \| 13 -----` (deletion). Guard `test_no_tavily_json_references` PASSES (no in-scope refs to deleted file). |
| X3 | DEFAULT_PARAMETERS root + injection + tier overrides | PASS | install_mcp.py:85 registry == `{"search_depth": "basic", "max_results": 10}` exactly. Injection install_mcp.py:561-565 uses `json.dumps(..., separators=(",",":"))` (compact JSON) emitted as `-e DEFAULT_PARAMETERS=<json>`. troubleshoot SKILL:335 overrides to `search_depth: advanced` (Tier-2). reflect SKILL:1690 explicitly states "passes no per-call overrides". |
| X4 | eval capability token = `mcp_server.tavily` | PASS | Scoped grep `mcp\.tavily([^.]\|$)` over `src/superclaude docs` returns NOTHING (EXIT 1). Registered in capabilities.py:242 inside `_DEFAULT_CAPABILITY_SPECS` tuple (closes :249), real.yaml:41 optional_capabilities, real.yaml:1624 requires. models.py:317,322 docstrings use `mcp_server.tavily` (diff confirms `mcp.tavily`→`mcp_server.tavily` migration). Guard `test_no_stale_mcp_tavily_token` PASSES; gate test 18/18 PASS. |
| X5 | map/crawl in deep-research ENGINE ONLY | PASS | `tavily-map`/`tavily-crawl` appear ONLY in: MCP_Tavily.md, RESEARCH_CONFIG.md, deep-research.md, deep-research-agent.md, examples/deep_research_workflows.md, commands/research.md (pointer). Negative grep over `agents/rf-*.md`, sc-troubleshoot-protocol, sc-reflect-protocol, sc-brainstorm-protocol returns NOTHING (EXIT 1). Whole-tree `agents/` sweep returns only the two deep-research agents. |
| X6 | docs/commands POINT, never duplicate param tables | PASS | mcp-servers.md:137, comprehensive-features.md:75,80, FLAGS.md:72 all "see MCP_Tavily.md". research.md:93 "defined by the research engine — see RESEARCH_CONFIG.md". RESEARCH_CONFIG.md:62-63 explicitly "not duplicated here". Guard `test_docs_no_default_params_duplication` PASSES (no docs/ duplicate `search_depth`/`max_results:10`). |
| X7 | frontmatter↔prose parity for every `mcp__tavily__*` id | PASS | deep-research.md: frontmatter set {search,extract,map,crawl} == prose set (search/extract :28,36,37; map :42; crawl :44). deep-research-agent.md: frontmatter set {search,extract,map,crawl} == prose set (:123,129,130,139,140,153,155). Bidirectional: no prose-only id missing from frontmatter, no frontmatter-only id absent from prose. |

## Confidence Gate

**Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 8 | Grep: 10 | Glob: 0 | Bash: 13 (incl. 3 pytest runs: doc-alignment 4/4, capability-gates 18/18)

Tool calls (31) exceed checklist items (7) — engagement minimum satisfied; no padding (each
call maps to a specific X1–X7 verification or a guard-test confirmation).

## Summary
- Invariants passed: 7 / 7
- Invariants failed: 0
- Critical issues: 0
- Out-of-scope observations: 1
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found

| # | Severity | Location | Issue | Disposition |
|---|----------|----------|-------|-------------|
| 1 | [OUT-OF-SCOPE] | tests/cli/eval/test_mcp_retry_once.py:279,290; tests/cli/eval/test_eval_outcome.py:160,161,163,164 | Literal string `mcp.tavily` (stale token form) appears as arbitrary capability-string fixtures in tests for UNRELATED machinery (RetryOncePolicy eligibility; EvalOutcome skip plumbing). | NOT an X4 violation. Explicitly outside X4's defined grep scope (`src/superclaude docs`) AND the guard test's `_ROOTS` (src/superclaude + docs only, tests/ excluded by design — test file header lines 3-7). These fixtures predate the upgrade, were NOT touched by this task's diff, and use `mcp.tavily` as a generic placeholder, not the canonical capability registry. No fix applied (out of scope; fix_authorization false anyway). Recorded for completeness only. |

## Adversarial Notes (where I checked harder)
- Did NOT trust the scoped grep alone for X4 — swept `src tests docs plugins` whole-tree for
  `mcp.tavily`, found the test-fixture residue, then traced each to confirm it is unrelated
  machinery and out of the invariant's defined scope rather than silently passing.
- Verified X4 registration is inside the live `_DEFAULT_CAPABILITY_SPECS` tuple (read :230-254),
  not a comment.
- Confirmed X3 injection is genuinely COMPACT JSON by reading the `separators=(",",":")` arg, not
  inferring from the registry dict alone.
- Confirmed X7 BOTH directions (frontmatter⊇prose AND prose⊆frontmatter) via set-equality grep,
  not a one-way spot check.
- Ran the three relevant test suites live (doc-alignment 4/4, capability-gates 18/18) rather than
  asserting they would pass.
- Confirmed `0.2.x` strings are descriptive labels, not version-pin leaks, before clearing X1.

## Recommendations
- None blocking. Green light.
- OPTIONAL (non-blocking, out of this task's scope): a future cleanup could migrate the
  `mcp.tavily` placeholder strings in the two test files to `mcp_server.tavily` for token
  consistency, but they are inert fixtures and not governed by X4.

## Verified
- X1 version single-pin 0.2.20 — install_mcp.py, MCP_Tavily.md, RESEARCH_CONFIG.md, mcp-servers.md, real.yaml
- X2 orphan configs deleted (both src/ and plugins/) — confirmed absent on disk + diff deletion
- X3 DEFAULT_PARAMETERS root, compact-JSON server-level injection, troubleshoot advanced override, reflect no-override
- X4 mcp_server.tavily registered (capabilities.py, real.yaml, models.py); zero stale token in scope
- X5 map/crawl confined to deep-research engine; absent from rf-*/troubleshoot/reflect/brainstorm
- X6 docs/commands point to MCP_Tavily.md / RESEARCH_CONFIG.md / install_mcp.py; no duplicated tables
- X7 frontmatter↔prose parity (bidirectional) for both deep-research agents
- Guard tests: test_tavily_doc_alignment.py 4/4 PASS; test_capability_gates.py 18/18 PASS

## QA Complete
