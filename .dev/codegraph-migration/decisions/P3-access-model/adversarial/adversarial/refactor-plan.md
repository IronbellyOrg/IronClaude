# Refactoring Plan: Merge into Base (Variant C)

## Overview
- Base: Variant C (`option-c.md`, hybrid; copy `variant-3-original.md`)
- Strengths come in from Variant B (`option-b.md`), Variant A (`option-a.md`), Round 2 new evidence, and the Round 2.5 invariant probe
- Planned changes: 20
- Overall risk: Medium. The output is a decision document: it adds rules and restructures the base, and it changes no code.
- Output: `../P3-access-model-merged.md` (in the `--output` directory), with provenance tags
- Ground truth for every fact: CTX = `context.md`, EVAL = `research/codegraph-evaluation.md`, BR = `brainstorm/P3-codegraph-opportunities/merged-requirements.md`. Anything they do not measure stays UNVERIFIED.

Target structure of the merged document:
1. Recommendation in one paragraph
2. Phase 2 change
3. Access path per primitive class (table)
4. Read-only agents
5. CLI use
6. Readiness, provenance and freshness contract
7. Guards
8. Fallbacks
9. Prerequisite checks before Phase 3 edits
10. Superseded brainstorm items
11. Accepted risks and invariant closures
12. Open points
13. Not adopted

## Planned Changes

### Change 1: Restructure the base into a recommendation document (base, restructure)
- **Source**: Base Proposal, Strengths and Weaknesses
- **Target**: whole document (restructure)
- **Rationale**: All three advocates backed "amended C" as the merge base in Round 2. A decision record needs a recommendation, rules and risks, not a pro/con list.
- **Integration point**: Keep each base proposal bullet as a rule in sections 2-8. Convert the base strengths into the "why" lines of section 1. Turn the base weaknesses into section 11 or 12 entries, or delete them where a change below closes them.
- **Risk**: Medium (restructure). Mitigation: provenance tags on every section.

### Change 2: Seven listed tools, explore omitted (from B, A-002)
- **Source**: B Proposal ("no primitive names it"); A-002, rejected by all three advocates; B Round 2 new evidence 1
- **Target**: section 2 (replace the base's 8-tool string)
- **Rationale**: X-003 went to B at 95%. An explicit `CODEGRAPH_MCP_TOOLS` list blocks every unnamed tool (EVAL §3, `tools.ts:2926-2929`). That closes the 24,913-character explore risk (EVAL §5.6) mechanically. It also makes the list a server-side allowlist, whereas the default listing still answers a raw `tools/call` (EVAL §3, §5.6).
- **Integration point**: The Phase 2 env value is `"CODEGRAPH_MCP_TOOLS":"node,search,callers,callees,impact,files,status"`, one key added to the registration `env` from EVAL §7 step 5. Nothing else in Phase 2 changes, and the line ships only after Change 3 passes. State that this is the only Phase 2 edit.
- **Risk**: Low

### Change 3: NFR-06 measurement before the env line ships, with a threshold and a failure branch (from B, closes INV-009 and INV-010)
- **Source**: B (measure-first, C-010 unanimous); INV-009; INV-010
- **Target**: section 9 (insert)
- **Rationale**: C-010 is unanimous: measure first and drop the 100-call trigger. INV-009: a gate needs a threshold and a failure branch. INV-010: whether the other seven tools are deferred behind tool search, and whether the server instructions still point at the blocked explore, are both UNVERIFIED.
- **Integration point**:
  - Measure the always-loaded schema delta between the default listing (explore only) and the 7-tool list, in a session that also has codebase-memory registered (INV-015).
  - Record whether the seven tools are deferred and what the server instructions say about explore.
  - Proposed pass threshold: a delta of 2K tokens or less per session. This reuses BR NFR-06's 2K figure, is proposed and not measured, and the user confirms it.
  - Failure branch: list only `status`, which keeps explore blocked. Lookups then fall back to B's CLI transport in orchestrators and to artifacts for agents.
- **Risk**: Medium (the threshold is a proposal). The section must flag this.

### Change 4: Freshness is owned by the session, detected at run time (from B, X-004; INV-012)
- **Source**: X-004 (B, 90%); A-001 QUALIFY by all three; INV-012
- **Target**: section 6 (replace the base strength "removes most of INV-001")
- **Rationale**: The daemon and watcher start when an MCP client is connected (EVAL §4, §5.7). CLI reads saw the daemon's update (EVAL §5.7). The daemon role is installer-owned (BR §2.1 line 69). Which runs lack MCP was never measured (A-004 REJECT).
- **Integration point**:
  - State that freshness does not depend on which path a primitive uses.
  - Detect MCP at run time from whether `mcp__codegraph__codegraph_status` is present in the tool list, never from the kind of run.
  - Sessions with no MCP client carry INV-001 (BR E-1); under E-1 Outcome B they are `stale` for the whole run.
- **Risk**: Low

### Change 5: B's full readiness contract, with all K-1 states and `access: mcp` (from B, C-005; INV-008, INV-013)
- **Source**: B probe and vocabulary; BR FR-01..FR-08 and K-1 fields; INV-008; INV-013
- **Target**: section 6 (replace the base "one readiness check per run")
- **Rationale**: C-005 went to "B content, C transport" (90%). INV-008 notes that K-1 has 7 `index_state` values and that `access` lacks `mcp`. INV-013 asks that the FR-05 re-check be restated.
- **Integration point**:
  - One readiness check per run (FR-01): `codegraph_status` over MCP, otherwise CLI `codegraph status`.
  - `index_state: fresh|stale|not_initialized|foreign_index|absent|disabled|error`.
  - `access: mcp|cli|none`.
  - A missing env line, so the tool is not listed, emits `graph:unlisted` and takes the absent path.
  - Keep these rules unchanged: FR-03 provenance, FR-05 re-check after in-run writes (no primitive runs `sync`), FR-06 citation contract, FR-07 empty results never prove absence, FR-08 shown/total.
  - Stale, foreign or unproven results are leads only.
  - Add from C Round 2: E-1 also captures `codegraph_status` over MCP in a nested and a sibling worktree, because the MCP form of the warning is UNVERIFIED.
- **Risk**: Low

### Change 6: Exact MCP names in `tools:` and `allowed-tools`; the wildcard only in settings (from B condition b, A-003; INV-005)
- **Source**: B Round 2 condition (b); A Round 2 new evidence 4; INV-005 (verified: troubleshoot `SKILL.md:4` and reflect `SKILL.md:5` list exact MCP names, implement and workflow `SKILL.md:4` list none)
- **Target**: section 3 (insert a rule) and section 7
- **Rationale**: Approval is not availability (A-003 QUALIFY by all three). Whether `allowed-tools` restricts MCP tools is UNVERIFIED.
- **Integration point**:
  - Every primitive that has an `allowed-tools` field and uses codegraph names the exact `mcp__codegraph__codegraph_<tool>` names it calls.
  - `mcp__codegraph__*` appears only in the settings permission rule that IronClaude writes (EVAL §7 step 6), never in a primitive.
- **Risk**: Low

### Change 7: CLI verb list per orchestrator class, settling N-001 (from C Round 2 and B; INV-014)
- **Source**: C Round 2 qualification of B (c); INV-014; BR FR-04, FR-06, FR-22, E-3
- **Target**: section 5 (replace the base CLI bullet)
- **Rationale**: The resolver needs `query --json`, which is documented and returns `startLine`/`endLine` (EVAL §3, §5.5). Whether MCP `search` or `node` return spans is UNVERIFIED, so the orchestrator decides N-001 for `query`. Scripts run only in unrestricted-Bash orchestrators until E-3 (FR-04).
- **Integration point**: a table.
  - Unrestricted-Bash orchestrators (troubleshoot, reflect, implement, workflow) may run:
    - `codegraph --version`
    - `codegraph status` (only when MCP is absent)
    - `codegraph telemetry status`
    - `codegraph query <name> --json` (FR-06 resolver)
    - `codegraph affected … --json --quiet`
  - Closed-Bash orchestrators (pr-submit, auggie-review, cleanup-audit) get one exact pattern each where needed:
    - `Bash(codegraph affected *)` for pr-submit
    - `Bash(codegraph --version)` (Change 9)
    - no `status` pattern, because readiness comes from MCP
    - no `query`, so their rows stay `unresolved`: context, never citations, until E-3 passes
  - The only `init` is the user-typed `/sc:graph init`.
  - Never `Bash(codegraph *)`.
  - Flag N-001 as decided by the orchestrator, not by the debate.
- **Risk**: Medium

### Change 8: Ban node file mode as a Read substitute, but allow the `symbolsOnly` outline, settling N-002 (from B evidence 2 and C Round 2)
- **Source**: B Round 2 new evidence 2; C Round 2 qualification; EVAL §6.2 (`get_symbols_overview` maps to `codegraph_node {file, symbolsOnly:true}`); BR D-10, FR-19
- **Target**: section 7
- **Rationale**: Three agents carry `get_symbols_overview` today (verified: `agents/troubleshoot-analyst.md:5`, `reflect-reviewer.md:5`, `reuse-auditor.md:5`), so a blanket ban breaks the swap. File mode with code is a Read substitute that bypasses `hooks.json:59`.
- **Integration point**:
  - `codegraph_node` in file mode is allowed only with `symbolsOnly:true`.
  - Graph output never satisfies freshness-before-edit (FR-19).
  - The FR-23 grep test also rejects `codegraph_node` file-mode calls without `symbolsOnly`.
  - Flag N-002 as decided by the orchestrator.
- **Risk**: Low

### Change 9: Version and provenance in closed-Bash orchestrators (closes INV-002, HIGH)
- **Source**: INV-002; BR FR-03, NFR-09
- **Target**: section 6
- **Rationale**: The pin check needs `codegraph --version`. The server version appears only in `serverInfo` (EVAL §5.6), and whether `codegraph_status` prints it is UNVERIFIED.
- **Integration point**:
  - Closed-Bash orchestrators get exactly `Bash(codegraph --version)`. It is read-only and already in the BR FR-04 verb list.
  - Until E-3 shows the pattern matches, an unknown version means `graph:provenance_unproven`, and every row is a lead only.
- **Risk**: Low

### Change 10: Readiness state handed to agents that call MCP (closes INV-003, HIGH)
- **Source**: INV-003; EVAL §3 (subagents do not see server instructions)
- **Target**: section 4
- **Rationale**: The orchestrator holds FR-01, FR-05, FR-07 and `projectPath`; an agent that calls MCP directly inherits none of them.
- **Integration point**:
  - Every brief for an agent with codegraph MCP names carries `index_state`, `checked_at`, `worktree_root` and the exact `projectPath` to pass on every call.
  - The agent Reads `refs/citation-contract.md` by installed path.
  - The agent calls codegraph only when `index_state: fresh`; otherwise it uses the artifact or Grep/Read.
  - Agent rows are leads until the orchestrator re-Reads them (FR-06).
- **Risk**: Low

### Change 11: Smoke-test matrix for agent MCP access (closes INV-011, HIGH)
- **Source**: INV-011; OQ-9; A/B/C Round 2 concessions; `sc-cleanup-audit-protocol/SKILL.md:86`
- **Target**: section 9
- **Rationale**: One smoke test cannot cover background agents, headless ClaudeProcess children, permission scope outside IronClaude, or Claude Code version drift.
- **Integration point**:
  - Test every spawn mode the four agents actually use (foreground Agent/Task call, background, headless child) in a non-IronClaude project.
  - Record whether a permission prompt appears and the Claude Code version.
  - An agent gets MCP names only for the spawn modes that pass. Every other mode keeps B's artifact path.
  - Re-run the test when the Claude Code version changes.
  - Pin both roster outcomes in `tests/troubleshoot/test_diagnostic_worker_contract.py`.
- **Risk**: Medium

### Change 12: Corrected per-agent subsets; auggie-reviewer reclassified (from A U-001, corrected by INV-006 and INV-007)
- **Source**: A Proposal (U-001); INV-006, INV-007 (verified `agents/*.md:5`); EVAL §6.2
- **Target**: section 4 (table)
- **Rationale**: Map from the Serena tools each agent carries today:
  - `find_symbol` → search + node
  - `find_referencing_symbols` → callers
  - `get_symbols_overview` → node `symbolsOnly`
  - `get_diagnostics_for_file` → none

  auggie-reviewer has Bash (`agents/auggie-reviewer.md:5`).
- **Integration point**:
  - troubleshoot-analyst and reflect-reviewer: search, node, callers, impact. Impact is new: it is the Tier-1/blast-radius use, kept from A and C. Diagnostics have no replacement.
  - reuse-auditor: search, node, callers.
  - auggie-reviewer: search, node, callers. This changes A's node, callers, callees. Classify it as a Bash agent whose brief forbids any codegraph CLI call.
  - evidence-validator: byte-identical (D-11).
  - Rosters change only after Change 11 passes. Phase 1's Serena removal already edits the same lines and the roster test (A-005).
- **Risk**: Medium

### Change 13: Pinning `projectPath`; snapshot and isolated children (from B evidence 3; INV-004)
- **Source**: B Round 2 new evidence 3; C Round 2 qualification; INV-004 (verified `sc-reflect-protocol/SKILL.md:283-288`)
- **Target**: section 6
- **Rationale**: `projectPath` resolves to the nearest `.codegraph/` at or above it (EVAL §3). Nested worktrees answer from the parent index (EVAL §4, §5.8).
- **Integration point**:
  - `projectPath` = the realpath of the caller's own `git rev-parse --show-toplevel`.
  - Reflect `_review-snapshot` children and agents in nested `.claude/worktrees/` are `foreign_index` unless they have their own `codegraph init -i`.
  - The provenance check stays mandatory.
- **Risk**: Low

### Change 14: Fallback rules extended (base, modified)
- **Source**: Base proposal bullet 1 (missing env line means codegraph absent); U-007; BR FR-02, NFR-07
- **Target**: section 8
- **Rationale**: C-006 and C-007 went to C.
- **Integration point**: one fallback table, each row naming its `graph:*` token:
  - env line missing → `graph:unlisted`
  - binary absent → `graph:absent`
  - `IRONCLAUDE_CODEGRAPH=off` → `graph:disabled`
  - not initialized → `graph:not_initialized`
  - nested or snapshot worktree → `graph:foreign_index`
  - version mismatch → `graph:version_mismatch` / `graph:provenance_unproven`
  - agent MCP unavailable → artifact
  - NFR-06 failure → Change 3 branch

  No codegraph step stops a run (FR-02).
- **Risk**: Low

### Change 15: Default state of a new worktree; necessary but not sufficient (closes INV-001, MEDIUM)
- **Source**: INV-001; EVAL §5.4, §5.8; BR B2; C Round 2 new evidence 3
- **Target**: section 11
- **Rationale**: Ten gates sit between the decision and a working call. Sibling worktrees, which is this repo's layout, are "not initialized". Markdown is not indexed.
- **Integration point**:
  - State that a new sibling worktree takes the fallback path until a user types `/sc:graph init`.
  - In Markdown-heavy repos graph answers are sparse.
  - The first live check is this checkout, which should report `not_initialized`.
- **Risk**: Low

### Change 16: Supersede the CLI-first brainstorm items (closes INV-008, INV-010 wording)
- **Source**: INV-008, INV-010; BR FR-11, D-08, D-17, D-28, §2.1 MCP-stage row, K-1 `access` field, FR-21
- **Target**: section 10 (new)
- **Rationale**: Amended C contradicts these items, and the merged decision must say so.
- **Integration point**: list each superseded item and its replacement:
  - FR-11 → Change 12 gated by Change 11.
  - D-28 → Change 2 gated by Change 3.
  - §2.1 MCP-stage row → Change 3.
  - D-08 reopens once reuse-auditor passes Change 11; it is not adopted here.
  - D-17 is unchanged: no graph-scout.
  - K-1 `access` gains `mcp`.
  - FR-21: explore is described as blocked, not "the one always-listed tool", and the routing block names codegraph for call-graph questions (INV-015).
  - Kept unchanged: FR-10 (now enforced by omission), FR-22, FR-23, FR-24, D-01, D-10 (narrowed by Change 8), D-11, D-18.
  - The draft Phase 3 spec's MCP-first map (CTX) stands, amended by this decision.
- **Risk**: Medium (cross-document). Phase 3 authors apply it.

### Change 17: Telemetry handoff and the mutation grep test (from B, conditions a and d; C-004)
- **Source**: B Proposal (grep test); B Round 2 conditions (a) and (d); BR FR-22, FR-23; B9
- **Target**: section 7
- **Rationale**: C-004 was a B=C tie. CLI calls do not inherit `CODEGRAPH_TELEMETRY=0` (B9); the MCP entry does (EVAL §7 step 5).
- **Integration point**:
  - The FR-23 grep test runs over every primitive. Its single exception is `init` in `commands/graph.md`. Extend it per Change 8.
  - The installer runs `codegraph telemetry off` on every install path (FR-22).
  - Primitives never prefix calls with env variables (INV-020).
- **Risk**: Low

### Change 18: Smallest Phase 3 change and roster-test attribution (from A, C-012; A-005)
- **Source**: A Strength 1; C-012 (A, 90%); A-005 REJECT by all three
- **Target**: section 1 ("why") and section 3
- **Rationale**: Existing primitives change by name swap in place. The roster-test edit happens in Phase 1 under every option.
- **Integration point**:
  - State that Phase 3 swaps exact names where Serena names were.
  - State that new Phase 3 machinery is limited to the readiness check (K-1), `affected`, and the brief fields from Change 10.
- **Risk**: Low

### Change 19: Remove the base's vague wording (base weakness)
- **Source**: Clarity-1 NOT MET for C in both passes ("rarely need to call", "removes most of INV-001"); Correctness-5 NOT MET (no EVAL citations)
- **Target**: all sections
- **Rationale**: Scoring evidence.
- **Integration point**: Replace the vague phrases with the rule from Change 10 and the statement from Change 4. Cite EVAL, BR or CTX for every number.
- **Risk**: Low

### Change 20: Open points and accepted risks (record)
- **Source**: Unresolved debate items; INV-010, INV-012, INV-015; BR OQ-3, OQ-9; A/B/C concessions
- **Target**: sections 11-12
- **Rationale**: These must stay visible.
- **Integration point**:
  - Accepted risks: INV-002, INV-003, INV-011 (HIGH, closed by rule but unverified until the checks run); INV-001 (BR) for sessions without MCP; telemetry on CLI paths until the FR-22 handoff lands.
  - Open: the NFR-06 threshold value (user confirms); whether server-level `alwaysLoad` defers the seven tools; whether `allowed-tools` restricts MCP tools; the MCP form of the worktree warning; whether codebase-memory stays registered (installer phase); N-001 and N-002 were decided by the orchestrator, not the debate.
- **Risk**: Low

## Changes NOT Being Made

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|------------|-------------------|---------------------------|
| C-001, X-002 | B: CLI for every lookup, no `CODEGRAPH_MCP_TOOLS` in v1 | B's advocate conceded in Round 2. CLI costs about 300 ms per call against 3-15 ms over MCP (EVAL §5.5-5.6), and CLI calls run without the telemetry opt-out (B9). Blocking explore needs an env line anyway (B Round 2). It stays only as the Change 3 failure branch. |
| X-001 | B: no codegraph tools for read-only agents (FR-11) | C at 80%. Agents keep follow-up lookups (D-08), gated by Change 11, with B's artifacts as the fallback. |
| C-010 | B: MCP stage opens at about 100 serial CLI calls per run | Unanimous: measure NFR-06 first and drop the call-count gate. BR INV-025 already calls the count evidence, not a switch. |
| X-003 | A: explore allowed for "how does this area work" with `maxFiles` | B at 95%. `maxFiles` behaviour was never measured, and the explicit list blocks explore mechanically. |
| X-005 | A: "no allowlist patterns to get wrong" | A conceded. The merge lists every pattern (Change 7). |
| INV-006 | A: auggie-reviewer gets node, callers, callees | Verified roster: its Serena tools map to search, node, callers (EVAL §6.2). |
| C-008 | B: all agent data only through artifacts | C at 85%. Artifacts are kept where briefs already use them, and as the fallback. |
| C-012 | B: probe, parsers, fixtures for CLI lookups | Only the readiness check and `affected` parsing remain (Change 18). |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1 | Medium | Section loss | Revert to base text; provenance tags show the origin of each section |
| 3 | Medium | Threshold disputed | User sets the number; the failure branch still holds |
| 7 | Medium | Wrong verb set for an orchestrator | Remove the row; FR-23 still forbids mutating verbs |
| 11, 12 | Medium | Agents lose graph access | Artifact fallback (B) |
| 16 | Medium | Brainstorm and decision disagree | This decision supersedes, as section 10 states |
| others | Low | Additive rules | Remove the inserted rule |

## Review Status
- [x] Auto-approved (default)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-10-29T18:25:00Z
