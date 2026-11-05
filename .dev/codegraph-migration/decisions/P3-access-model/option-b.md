# Option B: CLI-first, artifacts for agents (brainstorm recommendation)

Read `context.md` in this folder first. Source: `.dev/codegraph-migration/brainstorm/P3-codegraph-opportunities/merged-requirements.md` §2.1, FR-04, FR-11, D-28.

## Proposal

- No `CODEGRAPH_MCP_TOOLS` in v1; only explore stays listed, and no primitive names it.
- Orchestrators call the CLI through Bash: `codegraph query --json`, `callers`, `callees`, `impact`, `affected`, `status`, `files`. Allowlists use one pattern per read-only subcommand (`Bash(codegraph callers *)`), never `Bash(codegraph *)`. A grep test forbids mutating verbs in every primitive.
- Read-only agents get no codegraph tools; the orchestrator computes graph results and passes them as an artifact path in the brief (pattern already used by troubleshoot producers tables and reflect hunks).
- A shared probe runs `codegraph status` once per run and labels results `fresh|stale|not_initialized|foreign_index|absent`; stale results are leads only.
- An MCP stage is deferred until schema overhead is measured and CLI call counts exceed about 100 per run.

## Strengths

- No Phase 2 dependency; works in CLI-only sessions and where MCP is unavailable.
- Agents' rosters stay pure (no new tools), so read-only guarantees are trivially kept.
- Artifacts on disk are reviewable and reproducible; one orchestrator call serves many agents.
- No always-loaded schema cost.

## Weaknesses

- About 300 ms per call; 30-symbol batches take seconds.
- Without an MCP client there is no watcher; CLI freshness detection without a daemon is unmeasured (INV-001), so results may be stale with no way to tell.
- Several CLI flags (file pin, `symbolsOnly`, machine-readable `status`, `--json` for `callers`/`impact`) are undocumented; parsing human text output is brittle across releases.
- Every closed-Bash orchestrator needs new allowlist patterns whose matching (env prefixes, `~` paths) is unverified.
- Agents lose the ability to ask follow-up graph questions; everything must be precomputed.
- Larger Phase 3 change (probe, parsers, fixtures, artifacts) than a name swap.
