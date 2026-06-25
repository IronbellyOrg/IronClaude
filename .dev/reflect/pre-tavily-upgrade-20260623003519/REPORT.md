---
mode: pre
tier_reached: 2
status: partial
spec: .dev/brainstorms/CONSOLIDATED-tavily-0.2.x-upgrade.md
reviewers: [sonnet/gpt-5.5, haiku/qwen]
coverage_pct: 0.88
best_practice_grade: 3
needs_human_decision: true
created: 2026-06-23
---

# Reflect REPORT — Pre-execution audit of the Tavily 0.2.x upgrade plan

**Verdict: SAFE-WITH-FIXES, but BLOCKED on one human decision.** The plan is structurally sound and its core technical decisions are correct, but it (a) conflicts head-on with a pre-existing tavily-upgrade plan already in this worktree, and (b) has real coverage + test-scoping gaps. Do not implement until the version-policy conflict is resolved and the fixes below are folded in.

## BLOCKING — human decision required

### B1 [Regression-class / conflict] — A conflicting tavily-upgrade plan already exists in this worktree
- **Evidence:** `.dev/brainstorms/20260622-233136-tavily-mcp-upgrade/` (untracked, created 23:31:36 — *before* this brainstorm's C1 at 23:38). Complete pipeline: `seed-brief.md`, `merged-requirements.md`, `tasklist/phase-1..4`, `validation/reflect-pre/`, `adversarial/variant-{1-opus-architect,2-opus-refactorer}`.
- **Conflict:** that plan (merged-requirements.md:15,19,41) mandates a centralized `TAVILY_MCP_PACKAGE = "tavily-mcp@latest"` token and explicitly records `0.2.20` "in tests/docs only as verified context, **not** as the installed command target." **My consolidated plan (C1) pins exact `tavily-mcp@0.2.20`.** The two prescribe opposite edits to the same lines (e.g. install_mcp.py command, mcp-servers.md:273).
- **Why it matters:** version policy is invariant X1 — the foundation everything else inherits. My 8-cluster sweep never grepped `.dev/brainstorms/` for prior work, so it planned in ignorance of an existing, already-validated plan (likely a parallel session per memory `feedback_parallel_sessions_share_index`).
- **Decision needed:** pin-exact-`0.2.20` (my plan) **vs** centralized-`@latest`-token (existing plan). They cannot both ship. This flips the direction of the mcp-servers.md:273 edit and the install_mcp.py command.

## HIGH gaps (fold into the plan once B1 is resolved)

### H1 [Drift] — `sc-recommend` skill is an uncovered Tavily tool surface
- **Evidence:** `src/superclaude/skills/sc-recommend/SKILL.md:4` declares `mcp__tavily__tavily-search` + `mcp__tavily__tavily-extract` in `allowed-tools`; prose at SKILL.md:169 and `refs/plugin-ecosystem-sources.md:24`. Confirmed by both reviewers + direct grep.
- **Gap:** the 8-cluster sweep bucketed it as "incidental" and dropped it; the C2/C6 parity test globs `tests/agents/*.md` only → it would **not** cover this skill (silent miss).
- **Fix:** parity test must glob `src/superclaude/{agents,skills}/**/*.md` and parse BOTH `tools:` and `allowed-tools:`. sc-recommend needs no content change (inherits version + DEFAULT_PARAMETERS; stays search+extract, no map/crawl).

### H2 [Drift] — `plugins/` tavily.json mirror not in the deletion plan
- **Evidence:** `plugins/superclaude/mcp/configs/tavily.json` exists (identical remote-endpoint content to the src/ one). C1 only deletes `src/superclaude/mcp/configs/tavily.json`.
- **Provenance note:** Makefile builds plugin artefacts into `dist/plugins/` via `build-plugin`; the tracked `plugins/superclaude/` tree's relationship to `src/` must be confirmed — if it's generated/synced it regenerates from src; if hand-maintained it needs its own deletion. The plan must state which.

### H3 [Regression-risk] — version-drift test will false-positive
- **Evidence:** `tavily-mcp@0.1.2` also lives in `.dev/releases/complete/v2.01-Architecture-Refactor/.../rca-agent-3-environment.md` (archived artifact) and across `.claude/worktrees/*`.
- **Fix:** `test_tavily_version_single_pin` must scope to `src/` + `docs/` only, explicitly excluding `.dev/`, `.claude/`, `dist/`, worktrees.

### H4 [Regression-risk] — stale-token test will false-positive
- **Evidence:** `mcp.tavily` appears in real test files `tests/cli/eval/test_mcp_retry_once.py`, `tests/cli/eval/test_eval_outcome.py`, AND as a **substring of the URL `mcp.tavily.com`** (in both tavily.json files + docs).
- **Fix:** `test_no_stale_mcp_tavily_token` must (a) exclude `.dev/`/`.claude/`, (b) not match `mcp.tavily.com`, (c) exclude legitimate docstring/test-example occurrences (word-boundary or AST), and run *after* the C7 docstring fix.

## MEDIUM (correctness refinements)
- **M1** DEFAULT_PARAMETERS `-e` value: use compact JSON `json.dumps(..., separators=(",",":"))` (no spaces) so it stays one argv token and the dry-run display is clean; mask the API key in any echoed command. `_run_command` already shlex-quotes, so quoting itself is safe.
- **M2** Make `capabilities.py` `_DEFAULT_CAPABILITY_SPECS` registration of `mcp_server.tavily` **mandatory** (not optional) so non-`real.yaml` suites can resolve the capability; add a regression test.
- **M3** Add missing test assertions: (a) `registry["tavily"]["default_parameters"] == {"search_depth":"basic","max_results":10}`; (b) troubleshoot SKILL.md contains `search_depth: advanced` (so it isn't "corrected" back to basic).
- **M4** Document the C5 `search_depth: advanced` troubleshoot divergence in the updated MCP_Tavily.md (X3 exception) — per-call override IS mechanically valid (agent passes search_depth as a tool arg, overriding the server DEFAULT_PARAMETERS).
- **M5** Enumerate the 6 confirmed no-change name-only/server-level mentions explicitly so an implementer neither misses nor over-edits them: `commands/{pm,recommend,review-translation}.md` (mcp-servers frontmatter), `core/{CLAUDE.md:58,COMMANDS.md:57,MODES.md:293}`, `skills/confidence-check/SKILL.md:96`. (core/CLAUDE.md:58 MCP-table row MAY optionally get the same capability broadening as FLAGS.md.)

## PROCESS finding
- **P1** The consolidated doc was written to `/config/workspace/IronClaude/.dev/brainstorms/` (main repo) instead of the worktree — worktree-discipline violation (memory `feedback_worktree_discipline`). **Fixed during this audit** (relocated into the worktree; main-repo copy removed).

## Coverage matrix (integration surfaces)
- Files with `tavily` in `src/superclaude`: 36. Assigned to a cluster or confirmed no-change: 34. **Gaps: 2** (sc-recommend SKILL+refs = H1; plugins/ mirror = H2). `docs/research/*` + `docs/analysis/*` exclusions re-verified as research artifacts (safe). coverage_pct ≈ 0.88 (integration), gaps are additive not corrective.

## What the plan got RIGHT (verified)
- `mcp_server.tavily` capability token (C7) — the highest-value original catch; confirmed against `capabilities.py` + `real.yaml`.
- `tavily.json` zero Python readers → deletion safe (C1).
- 0.2.x tool surface, DEFAULT_PARAMETERS env name, map/crawl confined to the research engine (C2), RF fleet no-change (C6) — all confirmed.
- mcp-servers.md:273 `@latest` edit target is real (C8) — though its *direction* depends on B1.

## Reviewer ensemble
- 2 heterogeneous reviewers (gpt-5.5, qwen), both independent verdict **SAFE-WITH-FIXES**. Both confirmed H1; reviewer-1 surfaced H2/M1/M2; reviewer-2 surfaced H3/H4/M3. B1 (conflicting existing plan) was found by the orchestrator's coverage cross-check + evidence-validator (reviewer-1 gestured at it via a version-contradiction citation).
- Evidence-validator: all load-bearing citations re-Read and confirmed; no citations dropped as unfounded (reviewer-1's "consolidated doc missing" was a true symptom of P1, not a false claim).
