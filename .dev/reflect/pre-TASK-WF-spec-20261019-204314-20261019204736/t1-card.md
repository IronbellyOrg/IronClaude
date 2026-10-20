# PRE reflection card

Mode: pre. Advisory only; no implementation, plan edits, promotion or publication authorized.
Grounding root: /config/workspace/IronClaude/.dev/worktrees/CodebaseMemoryMCP

## Coverage and findings

F1 — Coverage instrumentation warning, not 23 proven omissions. The source has no R-/REQ-/SPEC-/T- labeled requirement IDs. Quote-pinned extraction produced 102 inferred rows; deterministic unique-word containment (threshold 0.6, explicit stopwords in artifacts/coverage-matrix.yaml) matched 79 and left 23 unmapped. Parsed coverage is null; union coverage is 0.7745; coverage_degraded is parsed-sparse. Semantic inspection finds the main implementation/safety commitments represented in the seven tasks, including many lexical nonmatches. Global constraints are outside individual task matching. Do not equate lexical nonmatches with missing behavior or rewrite the plan merely to improve this score.
Source anchors: source.md:12-22,52-63,78-102,108-117,132-155. Plan anchors: TASK-WF-spec-20261019-204314.md:19-28,36-49,59-70,82-91,103-113,119-128,138-148,154-165. All source/plan paths resolve below the input work-unit in the grounding root.

F2 — Highest implementation risk is already anticipated by Task 2, not an omitted task. Existing _run_mcp_get conflates lookup errors with absence (src/superclaude/cli/install_mcp.py:546-566); command normalization flattens argv to a space-joined string (569-594); the generic install path accepts matching commands without verifying target scope (697-704), and falls back to unscoped remove on unknown scope (719-725). Source registration safety requires exact user-scope/error-aware reversible changes (source.md:102), and Task 2 explicitly requires those stronger semantics and scope-shadowing/path-space/rollback tests (plan:61-70). Reuse must not copy these unsafe generic behaviors. [INFERRED] A supported hidden-user-entry lookup/restore approach needs proof during implementation; this review has not independently established current external CLI support. Advisory target is Task 2 and its named registry tests; no plan mutation authorized.

F3 — Real upstream merge safety remains an intentionally open release gate, not implementation completion evidence. The source requires a separately authorized disposable live smoke and release block if unrelated files are overwritten (source.md:151). Task 7 includes the smoke procedure and explicitly keeps release blocked until it passes (plan:156-164). Mocked regressions cannot establish upstream merge safety. No live smoke should run in this PRE review.

F4 — Scope/order checks look aligned. Tasks 1–2 separate native acquisition from registration, Task 3 removes only canonical upstream installation with retained indexes, Task 4 integrates menu/scope/consent/dry-run, Task 5 adds the default install phase but preserves update, Task 6 authors cross-entry-point tests, Task 7 documents behavior and the pending live gate. Existing install setup/failure aggregation and flat MCP entrypoint are consistent insertion points (src/superclaude/cli/main.py:212-275). No confirmed behavior omission or spec contradiction identified by this T1 pass. This is not a statement that product code implements the proposal.

## Routing and limitations

S_scope: 7 tasks. S_domains: 3 (code, tests, docs). S_dev_density: 23/102 = 0.22549. The parsed-sparse table-wide prefilter requires Tier 2 independently of confidence; rule 4 also fires for three domains. No explicit tier/depth override. Default reviewer rotation would be sonnet/haiku/opus (Haiku alias routes to grok-4.7[1m]); executor class is unknown. All three candidate aliases leave no disjoint available calibration class, so Tier-2 calibration diversity would be degraded. No neutralisation-of-bias claim is justified.

Serena targets the main checkout and project activation/config tools are unavailable. Do not invoke relative-path Serena tools against it. Its symbol/referrer/diagnostic grounding, memory hydration/persistence and scripted think checkpoints are unavailable for this worktree. Exact worktree Reads and one focused Auggie retrieval are the grounding fallback. No tests/builds/native execution/remote install/removal performed. External CLI/upstream contracts are not independently revalidated in this PRE review; Tasks 1–2 own that implementation-time proof.

## Calibration request

Blindly score this card ONLY, using five dimensions from reflect rubric: citation grounding, coverage completeness, deviation-classification clarity (UC-1: distinguish plan gap vs implementation risk), risk surface coverage, recommendation actionability. Return arithmetic mean and caveats; do not use a sixth dimension. No self-reported confidence supplied. Required Tier-2 routing cannot be overridden by a high score.
