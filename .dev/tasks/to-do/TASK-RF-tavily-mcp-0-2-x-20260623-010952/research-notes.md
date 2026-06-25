# Research Notes: Tavily MCP 0.2.x upgrade (pin 0.2.20)

**Date:** 2026-06-23
**Scenario:** A (explicit — driven by a validated consolidated plan + reflect audit)
**Depth Tier:** Deep (16+ files across 8 integration clusters + 7 test files)
**Track Count:** 1 (one cohesive upgrade; clusters are dependency-sequenced and share invariants)
**Source:** Prior research = `.dev/brainstorms/CONSOLIDATED-tavily-0.2.x-upgrade.md` + 8 per-cluster `merged-requirements.md` + reflect REPORT `.dev/reflect/pre-tavily-upgrade-20260623003519/REPORT.md`. B1 RESOLVED by user: **pin exact `tavily-mcp@0.2.20`** (current npm latest; reproducible, manual bumps — NOT floating `@latest`).

---

## EXISTING_FILES

Integration surfaces (all verified via grep + Read this session). 36 files in `src/superclaude` mention tavily; 34 covered, 2 gaps fixed by reflect (H1/H2). Full per-file change map in `research/01-change-map-by-file.md`.

- `src/superclaude/cli/install_mcp.py` — `MCP_SERVERS["tavily"]` (~L76-84): `command: "npx -y tavily-mcp@0.1.2"`, `api_key_env: "TAVILY_API_KEY"`, transport stdio. Install argv built ~L591-624 (server name before `-e`, `--` separator, `shlex.quote` per arg in `_run_command`).
- `src/superclaude/mcp/configs/tavily.json` — orphan remote `mcp-remote` config, **zero Python readers** (verified). DELETE.
- `plugins/superclaude/mcp/configs/tavily.json` — second mirror (H2), identical remote content. Provenance vs `dist/plugins/` build output must be confirmed before delete.
- `src/superclaude/cli/main.py:235` — help example (no change).
- `src/superclaude/core/RESEARCH_CONFIG.md`, `agents/deep-research.md`, `agents/deep-research-agent.md`, `mcp/MCP_Tavily.md`, `modes/MODE_DeepResearch.md`, `examples/deep_research_workflows.md` — C2 research engine.
- `commands/research.md` (C3); `commands/brainstorm.md` + `skills/sc-brainstorm-protocol/SKILL.md` (C4); `commands/troubleshoot.md` + `skills/sc-troubleshoot-protocol/SKILL.md` + `commands/reflect.md` + `skills/sc-reflect-protocol/SKILL.md` (C5); 8 `agents/rf-*.md` (C6 — no change).
- `cli/eval/suites/real.yaml` + `cli/eval/capabilities.py` + `cli/eval/models.py` (C7); `core/FLAGS.md` + `docs/user-guide/mcp-servers.md` + `docs/reference/comprehensive-features.md` + `docs/eval/retry.md` (C8).
- **H1 GAP (reflect):** `skills/sc-recommend/SKILL.md:4` (`allowed-tools` has `mcp__tavily__tavily-search`+`-extract`) + `skills/sc-recommend/refs/plugin-ecosystem-sources.md:24` — real tool surface, no content change but MUST be in the parity test scope.

## PATTERNS_AND_CONVENTIONS

- src/superclaude/ is source of truth; `.claude/` is sync-dev output (NEVER edit directly; `core/FLAGS.md` edits need `make sync-dev` + `make verify-sync`).
- UV-only Python; tests via `uv run pytest`; CI-safe (no live network/API key) — mock or capability-gate live calls.
- Agent/skill `.md` files declare a `tools:`/`allowed-tools:` allow-list that MUST match prose-referenced `mcp__tavily__*` tools (parity invariant).
- Eval capability tokens use `mcp_server.<name>` format (verified `capabilities.py` `_DEFAULT_CAPABILITY_SPECS` + `real.yaml:37-40`), NOT `mcp.tavily`.
- `claude mcp add` argv: `_run_command` shlex-quotes each arg; env pairs are separate `-e KEY=VAL` argv tokens.

## GAPS_AND_QUESTIONS

- H2: confirm whether `plugins/superclaude/` is build-generated (Makefile `build-plugin` targets `dist/plugins/`, but the tracked `plugins/` tree exists) — if generated from src, regenerates; if hand-maintained, needs explicit delete. Resolve during execution (Phase 1).
- The 233136 sprint bundle (`@latest` policy) is SUPERSEDED by B1 — do not execute it; note its supersession.

## RECOMMENDED_OUTPUTS

Per-cluster verified change map → `research/01-change-map-by-file.md`. Verified facts + citations → `research/02-verified-facts.md`. Reflect fixes (H1-H4, M1-M5) that MUST be folded in → `research/03-reflect-fixes.md`. The 7 new test files + assertions → `research/04-test-plan.md`.

## SUGGESTED_PHASES

Dependency-ordered (from consolidated plan): **P1 Install/Config/Version (C1)** → **P2 Research engine + canonical MCP_Tavily.md (C2)** → **P3 Eval capability + verification eval (C7)** → **P4 Consumers (C3/C4/C5/C6)** → **P5 Docs + sync (C8)** → **P6 Tests + drift guards + final validation**. C1 must land first (establishes version pin + DEFAULT_PARAMETERS + tavily.json deletion that everything inherits). Granular: one item per file edit + one item per test.

## TEMPLATE_NOTES

Template 02 (complex: discovery for H2 provenance, build edits, test creation, verification). Deep tier. QA gate FINAL_ONLY (the upgrade is mechanical edits validated by the new test suite + a final QA gate). POST reflect gate ENABLED (wrapper shell-out). PRE reflect already run on the driving plan; A.10.7 PRE gate will run on the built tasklist.

## AMBIGUITIES_FOR_USER

None blocking — B1 resolved (pin 0.2.20). One execution-time discovery: H2 plugins/ provenance (handled as a Phase-1 discovery item, not a user question).
