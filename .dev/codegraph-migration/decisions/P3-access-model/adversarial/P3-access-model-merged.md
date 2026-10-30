<!-- Provenance: This document was produced by /sc:adversarial (Mode A, depth standard) -->
<!-- Base: Variant C (option-c.md, hybrid) -->
<!-- Merge date: 2026-10-29T18:30:00Z -->

# P3 decision: how IronClaude primitives reach codegraph (merged recommendation)

<!-- Source: adversarial pipeline metadata (base-selection.md, debate-transcript.md, invariant-probe.md) -->
**Merge metadata**

- Base: Variant C (`option-c.md`, hybrid). Scores: C 0.871, B 0.912, A 0.810. B led by 0.041, which is below the 0.05 band, so tiebreaker level 1 (debate points) chose C: C 10.5, B 6.5, A 2.0.
- Convergence: 100% (26/26 diff points). Status: BLOCKED_BY_INVARIANTS. INV-002, INV-003 and INV-011 (HIGH) are carried as accepted risks, each with a closure rule (sections 6.2, 4 and 9.2; listed in section 11).
- Artifacts: `adversarial/` next to this file (`diff-analysis.md`, `debate-transcript.md`, `invariant-probe.md`, `base-selection.md`, `refactor-plan.md`, `merge-log.md`).
- Citations: CTX = `../context.md`; EVAL §n = `.dev/codegraph-migration/research/codegraph-evaluation.md`; BR = `.dev/codegraph-migration/brainstorm/P3-codegraph-opportunities/merged-requirements.md`. Anything they do not measure is UNVERIFIED. A bare INV-0NN is an invariant-probe finding; brainstorm invariants are written BR INV-0NN.

## 1. Recommendation

<!-- Source: Base (original, modified) — Proposal bullets 2-4 condensed into one recommendation; base Strengths became the "why" lines; vague wording removed — merged per Change #1, #18, #19 -->
Use MCP for interactive symbol, caller, callee and impact lookups, and use the CLI only for jobs MCP cannot do (amended Variant C). Readiness, provenance and fallback follow Variant B's contract.

- **What Phase 2 must change:** exactly one env key, `CODEGRAPH_MCP_TOOLS=node,search,callers,callees,impact,files,status`. It ships only after the NFR-06 check in section 9.1 passes.
- **What read-only agents get:** exact MCP subsets per agent (section 4), gated on the smoke-test matrix (section 9.2), with an artifact fallback. evidence-validator is unchanged.
- **What the CLI is used for:** `codegraph affected`, `codegraph --version`, `codegraph status` only where there is no MCP, `codegraph telemetry status`, `codegraph query --json` for the FR-06 resolver in unrestricted-Bash orchestrators only, and the user-typed `/sc:graph init` (section 5).

Why:

- MCP calls take 3-15 ms after a 220 ms init; CLI calls take about 290-300 ms (EVAL §5.5, §5.6).
- The MCP entry carries `CODEGRAPH_TELEMETRY=0` (EVAL §7 step 5); CLI calls do not inherit it (BR B9).
- All 8 MCP tools are read-only (`readOnlyHint: true`, EVAL §3), and MCP lookups never touch a Bash allowlist. The explicit tool list also blocks explore on the server side (section 2).
- Phase 3 stays small: exact codegraph names replace Serena names in the same places. New Phase 3 machinery is limited to the readiness check (BR K-1), `affected` parsing, and the brief fields in section 4.

## 2. Phase 2 change

<!-- Source: Variant B (Proposal bullet 1; Round 2 new evidence 1) — replaces the base's 8-tool string in Proposal bullet 1 — merged per Change #2 -->
- The only Phase 2 edit adds one key to the registration `env` from EVAL §7 step 5: `"CODEGRAPH_MCP_TOOLS":"node,search,callers,callees,impact,files,status"`. Nothing else in Phase 2 changes.
- explore is left out on purpose. An explicit list blocks every unnamed tool (EVAL §3, `tools.ts:2926-2929`). That closes the 24,913-character explore risk (EVAL §5.6) mechanically. The explicit list is a server-side allowlist. The default listing is not a boundary: unlisted tools still answer a raw `tools/call` (EVAL §3, §5.6).
- The line ships only after section 9.1 passes. If 9.1 fails, the same key lists only `status`.
- If the line is missing, primitives take the absent path with `graph:unlisted` (section 8).

## 3. Access path per primitive class

<!-- Source: Base Proposal bullets 2-4 (original, modified) — restated as a table; exact-name rule from Variant B Round 2 condition (b) and Variant A Round 2 evidence 4; Phase 3 size from Variant A Strength 1 — merged per Change #1, #6, #18 -->
| Class | Primitives | Lookups | CLI (section 5) | Readiness (section 6) |
|---|---|---|---|---|
| Main session | interactive use | MCP | user-typed `/sc:graph init` only | `codegraph_status` over MCP |
| Unrestricted-Bash orchestrators | troubleshoot, reflect, implement, workflow (BR §2.1) | MCP | `--version`, `status` (no MCP only), `telemetry status`, `query --json`, `affected` | MCP; CLI `status` only when MCP is absent |
| Closed-Bash orchestrators | pr-submit, auggie-review, cleanup-audit (BR §2.1) | MCP | `Bash(codegraph --version)`; `Bash(codegraph affected *)` in pr-submit | `codegraph_status` over MCP; no `status` pattern |
| Read-only agents | troubleshoot-analyst, reflect-reviewer, reuse-auditor, auggie-reviewer | exact MCP subsets after section 9.2, else artifact | none | handed in the brief (section 4) |
| evidence-validator | evidence-validator | none | none | none; file stays byte-identical (BR D-11) |

- Phase 3 swaps exact names where Serena names were. The roster-test edit happens in Phase 1 under every option (A-005).
- Every primitive that has an `allowed-tools` field and uses codegraph names the exact `mcp__codegraph__codegraph_<tool>` names it calls. troubleshoot (`SKILL.md:4`) and reflect (`SKILL.md:5`) already list exact MCP names; implement and workflow (`SKILL.md:4`) list none (INV-005). Approval is not availability (A-003). Whether `allowed-tools` restricts MCP tools is UNVERIFIED, so the names go in anyway.
- `mcp__codegraph__*` appears only in the settings permission rule that IronClaude writes (EVAL §7 step 6), never in a primitive.

## 4. Read-only agents

<!-- Source: Variant A Proposal bullet 3 (U-001), corrected by invariant probe INV-006 and INV-007 — merged per Change #12; brief rule from invariant probe INV-003 — merged per Change #10; base Proposal bullet 3 artifact clause kept and "rarely need to call" replaced — merged per Change #1, #19 -->
Mapping from the Serena tools each agent carries today (EVAL §6.2): `find_symbol` → search + node (Partial); `find_referencing_symbols` → callers; `get_symbols_overview` → node with `symbolsOnly:true`; `get_diagnostics_for_file` → none.

| Agent | Serena tools today (`agents/*.md:5`) | codegraph MCP names | Notes |
|---|---|---|---|
| troubleshoot-analyst | find_symbol, find_referencing_symbols, get_symbols_overview, get_diagnostics_for_file | search, node, callers, impact | impact is new (Tier-1 and blast-radius use, kept from A and C); diagnostics have no replacement |
| reflect-reviewer | same four | search, node, callers, impact | same as troubleshoot-analyst |
| reuse-auditor | find_symbol, get_symbols_overview, find_referencing_symbols | search, node, callers | |
| auggie-reviewer | find_symbol, find_referencing_symbols, plus Bash | search, node, callers | A Bash agent; its brief forbids any codegraph CLI call. Replaces A's node, callers, callees |
| evidence-validator | none | none | byte-identical (BR D-11) |

- Names take the form `mcp__codegraph__codegraph_<tool>`. Rosters change only for spawn modes that pass section 9.2. Every other mode keeps Variant B's artifact path. Phase 1's Serena removal already edits the same `tools:` lines and the roster test (A-005).
- Artifacts stay where a brief already uses them (troubleshoot producers table, reflect hunks) and serve as the fallback.
- Every brief for an agent with codegraph MCP names carries `index_state`, `checked_at`, `worktree_root` and the exact `projectPath` to pass on every call. Subagents do not see server instructions (EVAL §3).
- The agent Reads `refs/citation-contract.md` by installed path. It calls codegraph only when `index_state: fresh`; otherwise it uses the artifact or Grep/Read.
- Agent rows are leads until the orchestrator re-Reads them (FR-06).

## 5. CLI use

<!-- Source: Base Proposal bullet 4 (original, modified) — verb list replaced by a per-class table from C Round 2 qualification (c) and Variant B; invariant probe INV-014 — merged per Change #7 -->
The CLI runs only where MCP cannot do the job or where the session has no MCP. There are six verbs (INV-014). This table describes the pass branch of section 9.1.

| Verb | Unrestricted-Bash orchestrators | Closed-Bash orchestrators | Purpose |
|---|---|---|---|
| `codegraph --version` | yes | `Bash(codegraph --version)` | pin check (section 6.2) |
| `codegraph status` | only when MCP is absent | no pattern; readiness comes from MCP | readiness (section 6.1) |
| `codegraph telemetry status` | yes | no | FR-22 probe |
| `codegraph query <name> --json` | yes (FR-06 resolver) | no; rows stay `unresolved`, context only, never citations, until E-3 passes | resolver |
| `codegraph affected … --json --quiet` | yes | `Bash(codegraph affected *)` in pr-submit | test selection; CLI only (EVAL §3, §6.1) |
| `codegraph init` | no | no | only the user-typed `/sc:graph init` |

- Never `Bash(codegraph *)`. It would pre-approve `install`, which edits Claude config (EVAL §2, §3).
- Bundled scripts, including the resolver, run only in unrestricted-Bash orchestrators until E-3 passes (BR FR-04, E-3).
- N-001 (`query` as a CLI read verb) was decided by the orchestrator on evidence, not by the debate. `query --json` is documented and returns `startLine`/`endLine` (EVAL §3, §5.5). Whether MCP `search` or `node` return spans is UNVERIFIED. Flagged for user review.

## 6. Readiness, provenance and freshness contract

### 6.1 One check per run

<!-- Source: Variant B probe and vocabulary (U-004) over the base transport (U-008) — replaces base Proposal bullet 5 — merged per Change #5 -->
- One readiness check per run (FR-01): `codegraph_status` over MCP, otherwise CLI `codegraph status`.
- `index_state: fresh|stale|not_initialized|foreign_index|absent|disabled|error` (BR K-1) and `access: mcp|cli|none`; BR K-1 gains `mcp` (section 10).
- A missing env line, so the tool is not listed, emits `graph:unlisted` and takes the absent path.
- Unchanged rules: FR-03 provenance; FR-05 re-check after in-run writes (no primitive runs `sync`); FR-06 citation contract; FR-07 empty results never prove absence; FR-08 shown/total.
- Stale, foreign or unproven results are leads only.
- E-1 also captures `codegraph_status` over MCP in a nested and a sibling worktree, because the MCP form of the "different git working tree" warning is UNVERIFIED (EVAL §5.8 captured only the CLI form).

### 6.2 Version and provenance in closed-Bash orchestrators

<!-- Source: invariant probe INV-002 (HIGH); BR FR-03, NFR-09 — merged per Change #9 -->
- The pin check needs `codegraph --version`. The server version appears only in `serverInfo` (EVAL §5.6). Whether `codegraph_status` prints it is UNVERIFIED.
- Closed-Bash orchestrators get exactly `Bash(codegraph --version)`. It is read-only and already in the BR FR-04 verb list.
- Until E-3 shows the pattern matches, an unknown version means `graph:provenance_unproven`, and every row is a lead only.

### 6.3 Pinning projectPath

<!-- Source: Variant B Round 2 new evidence 3 with C Round 2 qualification; invariant probe INV-004 — merged per Change #13 -->
- `projectPath` is the realpath of the caller's own `git rev-parse --show-toplevel`. It resolves to the nearest `.codegraph/` at or above it (EVAL §3), and nested worktrees answer from the parent index (EVAL §4, §5.8).
- Reflect `_review-snapshot` children (`sc-reflect-protocol/SKILL.md:283-288`) and agents in nested `.claude/worktrees/` are `foreign_index` unless they have their own `codegraph init -i`. Pinning is not enough on its own. The provenance check stays mandatory.

### 6.4 Freshness

<!-- Source: Variant B (X-004); A-001 QUALIFY; invariant probe INV-012 — replaces base Strength 2 ("removes most of INV-001") — merged per Change #4, #19 -->
- Freshness does not depend on which path a primitive uses. The daemon and watcher start when an MCP client is connected (EVAL §4, §5.7), CLI reads saw the daemon's update (EVAL §5.7), and the daemon role is installer-owned (BR §2.1 line 69).
- Detect MCP at run time from whether `mcp__codegraph__codegraph_status` is in the tool list, never from the kind of run. Which runs lack MCP was never measured (A-004, INV-012).
- Sessions with no MCP client carry BR INV-001 (BR E-1). Under E-1 Outcome B they are `stale` for the whole run.

## 7. Guards

<!-- Source: Base Proposal bullet 4 guard sentence (original, modified) + Variant B grep test and Round 2 conditions (a), (b), (d) and new evidence 2, with C Round 2 qualification — merged per Change #6, #8, #17 -->
- Allowed CLI verbs are exactly the six in section 5: `--version`, `status` (no MCP only), `telemetry status`, `query --json` (unrestricted-Bash only), `affected`, and `init` (user-typed only). Allowlists name exact read subcommands. Never `Bash(codegraph *)`.
- Exact MCP names go in `tools:` and `allowed-tools`. The wildcard lives only in the settings rule (section 3).
- The FR-23 grep test runs over every primitive, including `skills/*/scripts/` bodies. Its single exception is `init` in `commands/graph.md`. It also rejects `codegraph_node` file-mode calls without `symbolsOnly`.
- `codegraph_node` in file mode is allowed only with `symbolsOnly:true`. File mode with code is a Read substitute that bypasses `hooks.json:59` (BR D-10). A blanket ban would break the swap, because three agents carry `get_symbols_overview` today (`agents/troubleshoot-analyst.md:5`, `reflect-reviewer.md:5`, `reuse-auditor.md:5`).
- Graph output never satisfies freshness-before-edit (FR-19). N-002 (the `symbolsOnly` outline exception) was decided by the orchestrator, not by the debate. Flagged for user review.
- No primitive names explore (FR-10); section 2 now enforces this by omission.
- Telemetry: the installer runs `codegraph telemetry off` on every install path (FR-22 handoff). CLI calls do not inherit `CODEGRAPH_TELEMETRY=0` (BR B9); the MCP entry does (EVAL §7 step 5). Primitives never prefix calls with env variables (FR-22, BR INV-020).

## 8. Fallbacks

<!-- Source: Base Proposal bullet 1 fallback clause (original, modified) — extended into a token table with U-007, BR FR-02, NFR-07 — merged per Change #14 -->
| Condition | Token | Behaviour |
|---|---|---|
| Phase 2 env line missing | `graph:unlisted` | Grep/Read, exactly like "codegraph absent" |
| codegraph binary absent | `graph:absent` | native path (NFR-07) |
| `IRONCLAUDE_CODEGRAPH=off` | `graph:disabled` | native path (FR-24) |
| index not initialized | `graph:not_initialized` | native path until a user types `/sc:graph init` |
| nested or snapshot worktree | `graph:foreign_index` | handled as `not_initialized` (FR-03; section 6.3) |
| version differs or is unknown | `graph:version_mismatch` / `graph:provenance_unproven` | rows are leads only (FR-03; section 6.2) |
| agent MCP unavailable in a spawn mode | none (FR-02: consumers invent no tokens) | artifact in the brief (section 4) |
| NFR-06 check fails | none | the section 9.1 failure branch |

No codegraph step stops a run (FR-02).

## 9. Prerequisite checks before Phase 3 edits

### 9.1 NFR-06 schema check before the env line ships

<!-- Source: Variant B measure-first (C-010, unanimous); invariant probe INV-009, INV-010 — merged per Change #3 -->
- Measure the always-loaded schema delta between the default listing (explore only) and the 7-tool list, in a session that also has codebase-memory registered (INV-015). Record whether the seven tools are deferred behind tool search, and what the server instructions say about explore. Both are UNVERIFIED (INV-010).
- Proposed pass threshold: a delta of 2K tokens or less per session. This reuses BR NFR-06's 2K figure. It is proposed, not measured, and the user confirms it.
- Failure branch: the env key lists only `status`, which keeps explore blocked. Lookups then fall back to Variant B's CLI transport in orchestrators and to artifacts for agents. In that branch the section 5 verb list does not apply to lookups.
- The 100-call trigger is dropped (C-010). BR INV-025 already calls the count evidence, not a switch.

### 9.2 Smoke-test matrix for agent MCP access

<!-- Source: invariant probe INV-011 (HIGH); BR OQ-9; A/B/C Round 2 concessions; `sc-cleanup-audit-protocol/SKILL.md:86` — merged per Change #11 -->
- One smoke test is not enough. `sc-cleanup-audit-protocol/SKILL.md:86` says MCP is unavailable to background subagents, and foreground access is UNVERIFIED (OQ-9).
- Test every spawn mode the four agents actually use (foreground Agent/Task call, background, headless child) in a non-IronClaude project. Record whether a permission prompt appears and the Claude Code version.
- An agent gets MCP names only for the spawn modes that pass. Every other mode keeps the artifact path.
- Re-run the matrix when the Claude Code version changes. Pin both roster outcomes in `tests/troubleshoot/test_diagnostic_worker_contract.py`.

## 10. Superseded brainstorm items

<!-- Source: invariant probe INV-008, INV-010, INV-015; BR FR-11, D-08, D-17, D-28, §2.1 MCP-stage row, K-1 `access` field, FR-21 — merged per Change #16 -->
This decision supersedes the CLI-first items below. Phase 3 authors apply it.

| BR item | Brainstorm position | Replacement |
|---|---|---|
| FR-11 | no read-only agent gains `mcp__codegraph__*` | section 4 subsets, gated by section 9.2 |
| D-28 | no `CODEGRAPH_MCP_TOOLS` in v1 | section 2, gated by section 9.1 |
| §2.1 MCP-stage row | deferred until about 100 serial CLI calls per run | section 9.1 |
| D-08 | reuse-auditor codegraph tier deferred | reopens once reuse-auditor passes section 9.2; not adopted here |
| D-17 | no graph-scout | unchanged |
| K-1 `access` field | `cli\|none` | gains `mcp` |
| FR-21 | explore is "the one always-listed tool" | explore is described as blocked; the routing block names codegraph for call-graph questions (INV-015) |

- Kept unchanged: FR-10 (now enforced by omission), FR-22, FR-23, FR-24, D-01, D-10 (narrowed by section 7), D-11, D-18. The draft Phase 3 spec's MCP-first map (CTX) stands, amended by this decision.

## 11. Accepted risks and invariant closures

<!-- Source: invariant probe gate (INV-002, INV-003, INV-011) and INV-001; base Weaknesses (original, modified) mapped to closures — merged per Change #1, #15, #20 -->
| Risk | Severity | Closure rule | Unverified until |
|---|---|---|---|
| INV-002: version and pin not readable over MCP in closed-Bash orchestrators | HIGH | section 6.2 | E-3 shows `Bash(codegraph --version)` matches |
| INV-003: agents that call MCP lack the run's readiness state | HIGH | section 4 brief fields | Phase 3 briefs carry the fields and section 9.2 runs |
| INV-011: one smoke test does not cover every spawn mode | HIGH | section 9.2 matrix | the matrix runs |
| BR INV-001: sessions without MCP have no watcher | accepted | section 6.4 labels; `stale` under E-1 Outcome B | E-1 runs |
| Telemetry on CLI paths | accepted | FR-22 installer handoff (section 7) | the installer phase lands it |
| INV-001: amended C alone is necessary, not sufficient | MEDIUM | new worktree default below | first live check |

New worktree default (INV-001):

- Ten gates sit between this decision and a working call: registration, env list, listing, permission rule, `tools:`, `allowed-tools`, foreground availability, an initialized index, provenance and version.
- A new sibling worktree, which is this repo's layout, reads "not initialized" (EVAL §5.8; BR B2). It takes the fallback path until a user types `/sc:graph init`.
- Markdown is not indexed (EVAL §5.4), so graph answers are sparse in Markdown-heavy repos. The first live check is this checkout, which should report `not_initialized`.

Base weaknesses: "two access paths to document" stays an accepted cost, covered by one shared guide. "Schema overhead unmeasured" is closed by section 9.1. "Foreground agent MCP availability UNVERIFIED" is closed by section 9.2.

## 12. Open points

<!-- Source: unresolved debate items; invariant probe INV-010, INV-012, INV-015; BR OQ-3, OQ-9 — merged per Change #20 -->
- The NFR-06 threshold value: 2K tokens is proposed; the user confirms (section 9.1).
- Whether server-level `alwaysLoad` stops deferral of the seven listed tools (UNVERIFIED; EVAL §3).
- Whether `allowed-tools` restricts MCP tools (UNVERIFIED; A-003).
- The MCP form of the worktree warning (UNVERIFIED; E-1 addition in section 6.1).
- Whether codebase-memory stays registered next to codegraph (installer phase; INV-015).
- Whether the watcher starts for a new index after `/sc:graph init` without a restart (UNVERIFIED; BR OQ-3).
- Which runs have no MCP client (UNVERIFIED; INV-012). Section 6.4 detects it at run time instead.
- N-001 (section 5) and N-002 (section 7) were decided by the orchestrator, not the debate. The user reviews both.

## 13. Not adopted

<!-- Source: refactor-plan.md "Changes NOT Being Made" -->
| Diff point | Rejected approach | Reason |
|---|---|---|
| C-001, X-002 | B: CLI for every lookup, no `CODEGRAPH_MCP_TOOLS` in v1 | B conceded. About 300 ms per CLI call against 3-15 ms over MCP (EVAL §5.5-5.6); CLI runs without the telemetry opt-out (BR B9); blocking explore needs an env line anyway. Kept only as the section 9.1 failure branch |
| X-001 | B: no codegraph tools for read-only agents (FR-11) | Agents keep follow-up lookups (D-08), gated by section 9.2, with artifacts as the fallback |
| C-010 | B: MCP stage opens at about 100 serial CLI calls per run | Unanimous: measure NFR-06 first; BR INV-025 calls the count evidence, not a switch |
| X-003 | A: explore allowed with `maxFiles` | `maxFiles` was never measured; the explicit list blocks explore mechanically |
| X-005 | A: "no allowlist patterns to get wrong" | A conceded; every pattern is listed in section 5 |
| INV-006 | A: auggie-reviewer gets node, callers, callees | Its Serena tools map to search, node, callers (EVAL §6.2) |
| C-008 | B: all agent data only through artifacts | Artifacts are kept where briefs already use them, and as the fallback |
| C-012 | B: probe, parsers and fixtures for CLI lookups | Only the readiness check and `affected` parsing remain (section 1) |
