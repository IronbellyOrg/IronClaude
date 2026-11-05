# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2 (Round 1 parallel, Round 2 sequential) + Round 2.5 invariant probe; Round 3 not run (depth standard)
- Convergence achieved: 100% on diff points (26/26); status BLOCKED_BY_INVARIANTS (3 HIGH UNADDRESSED: INV-002, INV-003, INV-011)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 3 (A: architect; B: security + analyzer; C: backend + qa)

## Round 1: Advocate Statements

### Variant A Advocate (default:architect)

**Position**: Variant A gets the access model right. Interactive symbol, caller and impact lookups should go through the eight read-only MCP tools, and the four read-only agents should get MCP names in place of their Serena names. That is the smallest change that keeps the measured speed and the documented parameters. A is not complete by itself, though. It needs C's readiness labels, fallback rules and mutation grep test, which makes the result "A as base, plus C's guard rails."

**Steelman of Variant B**: B has no dependency on Phase 2. It works where MCP is missing, and the one documented case is background subagents (`sc-cleanup-audit-protocol/SKILL.md:86`, CTX). Agent `tools:` lines stay unchanged, so read-only is guaranteed without proof (FR-11). Its artifacts follow existing patterns (`sc-troubleshoot-protocol/SKILL.md:281`, `sc-reflect-protocol/SKILL.md:355`, BR §1) and are reproducible (NFR-03). It also refuses to make a global listing decision before the always-loaded schema overhead is measured (D-28, NFR-06). That is disciplined deferral.

**Steelman of Variant C**: C keeps A's 1:1 name swap and adds what A leaves out: an explicit fallback when the Phase 2 env line is missing (U-007); one readiness check per run that works over MCP or CLI (U-008); a grep test over every primitive that forbids mutating verbs; and artifacts only where a brief already uses them. On correctness and failure behaviour, C beats A.

**Key strengths claimed**:
1. Latency. MCP calls take 3-15 ms after a 220 ms init; CLI calls take 290-297 ms (EVAL §5.6, §5.5). For 30 symbols that is about 0.5 s against about 9 s (arithmetic from EVAL §5.5, not a measurement).
2. Documented inputs. The MCP tools document `file`, `line`, `limit`, `symbolsOnly` and `depth` (EVAL §3). On the CLI, `callers --file`, `symbolsOnly` and a machine-readable `status` are UNVERIFIED (BR B11, E-2; BR §8.2).
3. Safety by construction. Every MCP tool is `readOnlyHint: true` (EVAL §3). The CLI puts `install` next to the read verbs, and `install` edits Claude config (EVAL §2, §5.9).
4. Telemetry. The MCP entry carries `CODEGRAPH_TELEMETRY=0` (EVAL §7 step 5); Bash CLI calls do not inherit it (BR B9, INV-005).
5. Smallest Phase 3 change. Each Serena name maps to one codegraph name; Phase 1 already edits the roster test (A-005).
6. Agents can ask follow-up questions; B's own brainstorm deferred reuse-auditor work (D-08) because "candidates the agent finds cannot be precomputed".

**Weaknesses identified in Variant B**:
1. Freshness: INV-001 is HIGH; CLI `status` without a daemon was never observed (BR §2.3). Under E-1 Outcome B, whole runs are `stale`.
2. Size and fragility: probe, parsers, golden fixtures and artifacts (C-012); text output can change between releases (BR B7, §8.2; 8 releases in about 3 months, EVAL §1).
3. Allowlist matching with env prefixes and `~` paths is UNVERIFIED (E-3, INV-019, INV-020) for every closed-Bash orchestrator.
4. Agents lose follow-up lookups (D-08).

**Weaknesses identified in Variant C**:
1. Whether `codegraph_status` over MCP shows the "different git working tree" warning in the same form as CLI `status` (EVAL §5.8) is UNVERIFIED.
2. CLI `status` in scripts adds a second allowlisted subcommand and the E-3 risk.
3. No rule for explore, despite the 24,913-character sample (EVAL §5.6).
4. Two mechanisms per agent (artifact plus MCP names) to document and test.

**Concessions**:
- A has no readiness or provenance check (C-005), no mutation grep test although it keeps CLI `init` (C-004), and no stated behaviour when the env line is missing or codegraph is absent (C-006, C-007). C fixes all four.
- A's freshness strength is overstated: the `alwaysLoad` server starts the daemon in every interactive session, whichever path primitives use (BR §2.1 line 69; EVAL §5.7).
- Foreground-agent MCP access is UNVERIFIED (OQ-9); one live smoke test is needed before roster edits ship.
- Schema overhead of eight listed tools is unmeasured (NFR-06).
- X-005 self-contradiction conceded.
- B's explore ban (FR-10) is better supported than A's `maxFiles` allowance; EVAL never measured `maxFiles`.

**Shared assumptions**:
- A-001 QUALIFY: freshness depends on whether the session has an MCP client, not on the path a primitive uses (EVAL §4, §5.7).
- A-002 REJECT: an explicit list without `explore` blocks it (EVAL §3, `tools.ts:2926-2929`); amend A to seven tools.
- A-003 QUALIFY: pre-approval via settings (EVAL §7 step 6); whether `allowed-tools` restricts MCP tools is UNVERIFIED; if so add names there.
- A-004 REJECT: the no-MCP session set is not known; only background subagents are documented.
- A-005 REJECT: Phase 1 edits the same `tools:` lines; the roster edit is not option-specific.
- A-006 QUALIFY: outputs are Markdown (EVAL §5.6); "structured" holds for inputs only.

**Per-point verdicts**: S-001 B; S-002 B; S-003 B; C-001 A=C; C-002 A (A-003 caveat); C-003 A; C-004 C (B equal); C-005 C; C-006 C; C-007 C; C-008 C; C-009 A=C; C-010 A=C (adopt NFR-06 as a check, not a deferral gate); C-011 A=C; C-012 A; X-001 A (pending OQ-9); X-002 A=C with explore omitted and overhead measured; X-003 B; X-004 tie (all overstate); X-005 C.

### Variant B Advocate (default:security+analyzer)

**Position**: Variant B (CLI-first, with the orchestrator computing graph results and handing agents a file path) is the safest and most correct v1. It keeps every read-only agent's tool list unchanged, needs nothing from Phase 2, and is the only variant with a fully specified readiness and worktree-provenance contract (BR FR-01..FR-05). Its costs are real: CLI latency, parsing plain-text output, unverified allowlist matching, telemetry, and a larger Phase 3. Variant C beats it on speed for the interactive main session, but only once schema overhead is measured.

**Steelman of Variant A**: Smallest Phase 3 change; 3-15 ms against about 300 ms (EVAL §5.5, §5.6); all eight tools read-only (EVAL §3); documented inputs while several CLI flags are not (BR B7, B11); agents keep follow-up ability with no shell.

**Steelman of Variant C**: Keeps A's swap and latency and adopts B's safety machinery (mutation grep test, readiness labels, artifacts where a brief already uses them), plus the degrade rule A lacks (U-007).

**Key strengths claimed**:
1. Least privilege: no read-only agent's `tools:` line changes (FR-11); evidence-validator byte-identical (D-11); reflect reviewers denied Bash (reflect `:658`); existing artifact patterns (troubleshoot `:281`, reflect `:355`).
2. Testable mutation boundary: per-subcommand patterns (FR-04) plus grep test (FR-23); `Bash(codegraph *)` would pre-approve `install` (EVAL §2, §5.9).
3. Worktree correctness: five-state probe; FR-03 rejects nested-worktree answers from the parent index (EVAL §5.8); FR-05 stale = leads; FR-07 empty never proves absence.
4. Works for every primitive class; no Phase 2 dependency; background subagents lack MCP (`SKILL.md:86`).
5. Reviewable and capped: byte-identical artifacts (NFR-03); 2K tokens per run (NFR-06); 40 rows and 6 KB per brief (FR-10).
6. Measured MCP re-entry trigger instead of a speculative global change (BR §2.1; rule 7).
7. Same freshness as A/C in interactive sessions: daemon is installer-owned (BR §2.1 line 69; EVAL §5.7). Whether `alwaysLoad` spawns the server at session start is UNVERIFIED.

**Weaknesses identified in Variant A**:
1. Keeps CLI `affected` and `init` without a mutation guard (C-004); `init` is a 34 MB, about 1 GB RSS write (EVAL §5.4); X-005.
2. No provenance check; nested worktrees answer from the parent with only a warning (EVAL §5.8).
3. Agent MCP names depend on UNVERIFIED foreground access (OQ-9) with no stated fallback (C-006, C-007).
4. Explore left usable with only `maxFiles` guidance (EVAL §5.6; D-01).
5. "Structured" overstated: MCP output is Markdown (EVAL §5.6).

**Weaknesses identified in Variant C**:
1. Two access paths: two parsers, two fixture sets, two failure modes in the capability map.
2. User-scope registration changes the listing in every project; overhead unmeasured (D-28, NFR-06).
3. Keeps explore listed with no ban (X-003), against FR-10 and FR-21.
4. "Removes most of INV-001" credits the access path (A-001).
5. Foreground-agent MCP access UNVERIFIED (OQ-9).

**Concessions**:
- About 300 ms per CLI call; about 9 s for 30 symbols by arithmetic (NFR-01).
- INV-001 still HIGH; headless sessions hurt A and C equally.
- No documented `--json` for `callers`, `impact`, `status` (B7).
- Allowlist matching UNVERIFIED (E-3, INV-019, INV-020).
- CLI calls do not inherit `CODEGRAPH_TELEMETRY=0` (B9, INV-005).
- Agents cannot ask follow-ups (D-08).
- Largest Phase 3 change.

**Shared assumptions**:
- A-001 QUALIFY: freshness belongs to the session; session-start spawning UNVERIFIED; headless sessions lack a watcher under every option.
- A-002 REJECT: omit explore from any explicit list (EVAL §3), including B's deferred MCP stage.
- A-003 QUALIFY: settings pre-approval (EVAL §7 step 6); `allowed-tools` restriction UNVERIFIED.
- A-004 REJECT: only background subagents documented; headless and sprint unmeasured; favours explicit fallbacks.
- A-005 REJECT: Phase 1 changes the same roster; narrows B's size disadvantage.
- A-006 REJECT: MCP output is Markdown; CLI documents `--json` for `query` and `affected`; parse fragility about equal.

**Per-point verdicts**: S-001 tie; S-002 B; S-003 B; C-001 C if NFR-06 acceptable, else B; C-002 C if A-003 holds, else B; C-003 C; C-004 B=C; C-005 B; C-006 B (C second); C-007 B=C; C-008 B; C-009 A=C; C-010 B; C-011 A=C; C-012 A; X-001 B; X-002 B for v1; X-003 B; X-004 BR §2.1 position (cancels A/C's edge); X-005 B.

### Variant C Advocate (default:backend+qa)

**Position**: Variant C is the best base. It uses MCP for symbol, caller and impact lookups and the CLI only for `affected`, scripted `status` and the user-typed `init`, and it keeps B's discipline: the mutation grep test, the readiness label and a fallback to Grep/Read when codegraph is unusable. Two changes would make it stronger: drop `explore` from the tool list, and stop claiming freshness as an MCP-only advantage.

**Steelman of Variant A**: Smallest correct change; no agent gains Bash; documented MCP inputs (EVAL §3); 3-15 ms vs about 300 ms (EVAL §5.5, §5.6); matches rule 7.

**Steelman of Variant B**: No Phase 2 dependency and no always-loaded schemas; the listing is global and an explicit list blocks unnamed tools (EVAL §3; D-28); overhead unmeasured (NFR-06); pure agent rosters; reproducible artifacts (NFR-03); works where MCP is documented unavailable (`SKILL.md:86`).

**Key strengths claimed**:
1. Documented inputs where they matter: MCP `callers`/`node` take `file` and `line` (EVAL §3); CLI equivalents UNVERIFIED until E-2 (BR B11, §8.2). Avoids B's parser and fixture machinery for lookups (B7, NFR-04).
2. Telemetry stays off for lookups: MCP inherits `CODEGRAPH_TELEMETRY=0` (EVAL §7 step 5); CLI does not (B9, INV-005).
3. Explicit failure behaviour: env line missing = "codegraph absent" (U-007), satisfying FR-02 and NFR-07.
4. Safety: all MCP tools read-only (EVAL §3); exact read CLI patterns; keeps the FR-23 grep test A drops.
5. Agent follow-up removes D-08's reason for deferral; artifacts kept where briefs already use them (troubleshoot `:281`, reflect `:355`).
6. Provenance check per run over MCP or CLI catches nested-worktree and not-initialized states (EVAL §5.8; FR-03; U-008).

**Weaknesses identified in Variant A**:
1. No mutation guard (C-004; FR-23).
2. No readiness or provenance step; FR-03 left to chance.
3. Failure behaviour unstated (C-006, C-007), conflicting with FR-02 and NFR-07.
4. Allows explore against D-01, D-27, FR-10 (EVAL §5.6).
5. X-005 self-contradiction.

**Weaknesses identified in Variant B**:
1. Lookups rely on undocumented CLI flags and text parsing (B7, B11); fixes add Phase 3 size (C-012).
2. Allowlist matching UNVERIFIED (B12, INV-019, INV-020) in three closed-Bash orchestrators.
3. CLI telemetry accepted risk (INV-005).
4. No agent follow-ups (D-08).
5. Latency: about 9 s for 30 symbols by arithmetic; the 15 s budget with resolution at risk (INV-011).

**Concessions**:
- Freshness does not depend on the access path where the `alwaysLoad` server connects (BR §2.1; EVAL §5.7); "removes most of INV-001" is overstated.
- Foreground-agent MCP access UNVERIFIED (OQ-9); needs a live smoke test before any `tools:` change; if it fails, agents fall back to B's artifacts.
- B's five-value vocabulary is better specified; C should adopt it.
- B's rule to measure schema overhead before the env change (NFR-06) is sound; adopt as a precondition.
- Two access paths cost documentation; FR-21 caps the routing block at 12 lines.

**Shared assumptions**:
- A-001 REJECT: the `alwaysLoad` server starts the daemon whichever path a primitive uses; freshness differs only in no-MCP sessions, which need the label under every option.
- A-002 REJECT: `CODEGRAPH_MCP_TOOLS=node,search,callers,callees,impact,files,status` blocks explore (EVAL §3, `tools.ts:2926-2929`) and enforces FR-10 mechanically.
- A-003 QUALIFY: settings pre-approval; `allowed-tools` behaviour UNVERIFIED; test it or add names to `allowed-tools`.
- A-004 QUALIFY: only background subagents documented; headless and sprint UNVERIFIED; C's CLI `status` fallback covers unknowns.
- A-005 ACCEPT: Phase 1 changes `test_diagnostic_worker_contract.py:17-26` under every option.
- A-006 QUALIFY: outputs Markdown on both paths; inputs still differ (MCP `file`/`line` pin documented, CLI not, B11).

**Per-point verdicts**: S-001 tie; S-002 B; S-003 B; C-001 A=C; C-002 A (C close second); C-003 C; C-004 B=C; C-005 B (C should adopt); C-006 C; C-007 C; C-008 C; C-009 A=C (conditional on OQ-9); C-010 B; C-011 A=C; C-012 A; X-001 C (gated on OQ-9 smoke test); X-002 C amended (explore omitted); X-003 B; X-004 B; X-005 C.

## Round 2: Rebuttals

### Variant A Rebuttal

**Response to criticisms**
1. No mutation grep test: CONCEDED. A keeps CLI `init` and `affected`, so FR-23's grep test belongs in A unchanged (single exception `commands/graph.md`). One test, no design change.
2. No readiness or provenance check: CONCEDED. FR-03 cannot depend on the model noticing a warning; adopt one check per run (FR-01). The MCP server "re-checks per call" (EVAL §4), so a per-call warning is at least emitted; its exact MCP text is UNVERIFIED (EVAL §5.8 captured only the CLI form).
3. Foreground-agent MCP access (OQ-9): CONCEDED. One live smoke test before any `tools:` edit; if it fails, agents get B's artifact path.
4. Explore allowance: CONCEDED, with a stronger fix: omit explore from the explicit list, which blocks it mechanically (EVAL §3, `tools.ts:2926-2929`).
5. "Structured" overstated: CONCEDED for outputs (Markdown, EVAL §5.6); still true for inputs (MCP `callers` documents `file`, `limit` max 100, EVAL §3; CLI `--file` UNVERIFIED, B11, BR §8.2).
6. X-005: CONCEDED. Restated as "one exact Bash pattern (`affected`), only in orchestrators that need it."

**Updated assessment**: C is A plus the guard rails A lacked; amended C is the merge base. B's contract (five-state vocabulary, FR-03..FR-08) is the best-specified part of the debate and should be kept whole; B's transport (CLI for every lookup) is worse on latency, telemetry (B9, INV-005), undocumented flags (B7, B11) and Phase 3 size.

**New evidence**
1. B does not avoid always-loaded schema cost: explore is listed by default with `_meta.anthropic/alwaysLoad: true` (EVAL §3), and Phase 2 registers with `alwaysLoad` under every option (CTX). NFR-06 itself says "measure the always-loaded explore schema overhead"; FR-21 says the model "may call [explore] unprompted". Under B the 24,913-character risk (EVAL §5.6) stays open in every main session; FR-10's grep covers primitive text only. A seven-tool explicit list without explore is the only mechanical closure. Net schema change from 1 to 7 tools: UNVERIFIED.
2. The daemon outlived its client, idle timeout 300 s (EVAL §5.7): freshness is a property of the session and daemon.
3. `sync` fails on the writer lock while a daemon runs (EVAL §5.7): no primitive runs `sync` under any option (FR-05).
4. Approval is not availability: `mcp__codegraph__*` is a permission rule (EVAL §3, §7 step 6). Whether a skill's `allowed-tools` hides MCP tools is UNVERIFIED (A-003); fix by adding exact MCP names to closed-Bash orchestrators' `allowed-tools`.

**Final per-point positions**: S-001 tie (changed); S-002 B; S-003 B; C-001 A=C; C-002 A with exact MCP names in `allowed-tools`; C-003 A; C-004 B=C; C-005 B's vocabulary over C's dual path (changed); C-006 C; C-007 C; C-008 C; C-009 A=C gated on OQ-9; C-010 B on measure-first: run NFR-06 before the env line ships, reject the 100-call trigger (changed); C-011 A=C; C-012 A; X-001 C with A's exact subsets (U-001), gated on OQ-9 smoke test with artifact fallback (changed); X-002 C amended: 7 tools, explore omitted, after NFR-06 (changed); X-003 B's ban enforced by omission; X-004 B (changed); X-005 B=C (changed); A-001 QUALIFY; A-002 REJECT; A-003 QUALIFY; A-004 REJECT; A-005 REJECT; A-006 QUALIFY.

### Variant B Rebuttal

**Response to criticisms**
1. Undocumented flags and text parsing: PARTLY CONCEDED. `query --json` and `affected --json` are documented (EVAL §3). Callers, impact and status are text on the CLI, and MCP output is also Markdown (EVAL §5.6), so parsing is needed on both paths. MCP's documented `file` pin (EVAL §3) is a real advantage over CLI B11. The size cost stands (C-012).
2. Allowlist matching UNVERIFIED: CONCEDED, but not B-only: amended C still uses CLI `affected` and `status` in closed-Bash orchestrators and needs E-3 too; A and C carry the parallel unknown A-003.
3. Telemetry: CONCEDED. MCP inherits `CODEGRAPH_TELEMETRY=0` (EVAL §7 step 5); CLI does not (B9). C's CLI calls leak the same way, so the FR-22 installer handoff is needed under every option.
4. No follow-up lookups: CONCEDED (D-08); closing it depends on the OQ-9 smoke test.
5. Latency: CONCEDED for lookups (30 × 297 ms ≈ 8.9 s by arithmetic, EVAL §5.5). Part of INV-011 is path-independent: the FR-06 resolver runs CLI `query --json` per cited row; cost UNVERIFIED (E-4).
6. Freshness: REJECTED as B-specific. Headless sessions have no MCP client under any option (E-1 Outcome B hits A, B and C alike); interactive sessions get the `alwaysLoad` daemon whichever path is used (BR §2.1 line 69; EVAL §5.7).
7. 100-call trigger: CONCEDED. Measure NFR-06 first; drop the call count as a gate (INV-025 already says the count is evidence, not a switch).

**Response to A's new evidence 1**: CONCEDED, decisive. `codegraph_explore` is listed by default with `_meta.anthropic/alwaysLoad: true` (EVAL §3) and FR-21 says the model may call it unprompted. B's "no always-loaded schema cost" strength is false: B carries one schema plus the 24,913-character risk (EVAL §5.6) in every main session. Closing it mechanically needs an explicit list without explore (`tools.ts:2926-2929`), which is a Phase 2 env line. B is not free of Phase 2 either.

**Updated assessment**: Amended C is the merge base (seven tools, explore omitted, NFR-06 measured before the env line ships, OQ-9 smoke test before any `tools:` edit, B's artifacts as fallback). B's contract carries over whole: K-1 probe with five states, FR-03..FR-08, FR-23, FR-10 enforced by omission. Security conditions for the merge: (a) evidence-validator byte-identical (D-11); (b) exact MCP names in `tools:` and `allowed-tools`, never `mcp__codegraph__*` in a primitive; (c) CLI only for `affected`, `status` and the user-typed `init`; (d) FR-22 telemetry handoff.

**New evidence**
1. An explicit `CODEGRAPH_MCP_TOOLS` list is a server-side allowlist (unlisted tools blocked, `tools.ts:2926-2929`); in default mode unlisted tools still answer a raw `tools/call` (EVAL §3, §5.6), so the default listing is not a boundary. Strongest least-privilege argument for amended C.
2. `codegraph_node` file mode is a Read equivalent (EVAL §3); `hooks.json:59` counts only `Read` (D-10). Primitives must not use node file mode as a Read substitute; add the phrase to the FR-23/FR-10 grep test. Whether node output satisfies the freshness hook is UNVERIFIED.
3. Every MCP tool accepts optional `projectPath` (nearest `.codegraph/` at or above it, EVAL §3). Primitives should pass the worktree root's realpath, or FR-03 can be bypassed. The MCP form of the "different git working tree" warning is UNVERIFIED (EVAL §5.8 captured the CLI form).

**Final per-point positions**: S-001 tie; S-002 B; S-003 B; C-001 C with NFR-06 first (changed); C-002 C with exact MCP names in `allowed-tools` plus E-3 for `affected` (changed); C-003 C; C-004 B=C; C-005 B's vocabulary inside C with `projectPath` pinned; C-006 C (changed); C-007 B=C; C-008 C with B's artifacts as fallback (changed); C-009 A=C gated on OQ-9; C-010 measure NFR-06 first, drop the trigger (changed); C-011 A=C; C-012 A; X-001 C with A's subsets, gated on OQ-9, artifact fallback, evidence-validator excluded (changed); X-002 amended C, seven tools, explore omitted, after NFR-06 (changed); X-003 B's ban by omission; X-004 B; X-005 B=C (changed); A-001 QUALIFY; A-002 REJECT (strengthened); A-003 QUALIFY; A-004 REJECT; A-005 REJECT; A-006 QUALIFY (changed).

### Variant C Rebuttal

**Response to criticisms**
1. Two paths: PARTLY CONCEDED. Parsing is needed on both paths anyway (MCP Markdown, EVAL §5.6; CLI `callers`/`impact`/`status` text, B7). Under C the CLI covers only `affected` (documented `--json`, EVAL §3) and `status` text, which B parses too. Net: one extra fixture set (MCP Markdown), not a doubled design.
2. Global listing: CONCEDED; run NFR-06 before the env line ships. Counter-evidence: explore is already always-loaded under every option (EVAL §3 `_meta.anthropic/alwaysLoad`); the real change is 1 tool to 7 with explore removed; net cost UNVERIFIED.
3. Explore: CONCEDED; omit it from the explicit list (`tools.ts:2926-2929`).
4. INV-001 overclaim: CONCEDED (BR §2.1 line 69; EVAL §5.7).
5. OQ-9: CONCEDED; one smoke test before any `tools:` edit; on failure agents get B's artifacts.
6. MCP form of the warning: CONCEDED as UNVERIFIED. Fix: add one step to E-1 capturing `codegraph_status` over MCP in a nested and a sibling worktree (effort S). Until then provenance comes from CLI `status` where Bash allows it; otherwise rows are `provenance_unproven`, leads only (FR-03).
7. CLI `status` allowlist: REJECTED in part. Closed-Bash orchestrators run in the main session and get readiness from `codegraph_status` over MCP, so they need no `status` pattern. CLI `status` is needed only where MCP is absent (headless or scripted runs in unrestricted-Bash orchestrators). The only new closed-Bash pattern is `affected`; E-3 still applies (conceded).

**Position on B's merge conditions**
- (a) evidence-validator byte-identical: ACCEPT (D-11, FR-06).
- (b) exact MCP names in `tools:` and `allowed-tools`, never the wildcard in a primitive: ACCEPT; the wildcard stays only in the settings permission rule (EVAL §7 step 6).
- (c) CLI only for `affected`, `status`, user-typed `init`: QUALIFY. The FR-06 resolver runs CLI `codegraph query <caller> --json` per cited row. Either add `query` as a fourth read verb or move the resolver to MCP `codegraph_search` / `codegraph_node {symbol, file}`; whether those return `startLine`/`endLine` spans is UNVERIFIED. Until E-2 or an MCP capture settles it, prefer adding `query`.
- (d) FR-22 telemetry handoff: ACCEPT.
- Evidence 2 (no node file mode as Read substitute): QUALIFY. `codegraph_node {file, symbolsOnly:true}` is the stated equivalent of Serena's `get_symbols_overview` (EVAL §6.2), which the three agents carry today; ban file mode without `symbolsOnly:true`, allow the outline form.
- Evidence 3 (pin `projectPath`): ACCEPT, not sufficient alone. `projectPath` resolves to the nearest `.codegraph/` at or above it (EVAL §3); a nested worktree without init still gets the parent index (EVAL §4, §5.8). The provenance check stays mandatory.

**Remaining disagreements**: the `query` verb under (c); the `symbolsOnly` outline exception to evidence 2.

**New evidence**
1. MCP lookups never touch the Bash allowlist; all 8 tools `readOnlyHint: true` (EVAL §3); the server-side explicit list is a stronger fence than per-subcommand patterns whose matching is UNVERIFIED (B12, INV-019, INV-020).
2. The MCP server re-checks the index per call (EVAL §4): after `/sc:graph init`, MCP lookups pick up the new index without restart; whether the watcher starts for it is UNVERIFIED (OQ-3).
3. This checkout is a sibling worktree and reads "not initialized" (EVAL §5.8; BR B2): the U-007 fallback is exercised here before any `init`, a useful first live test.

**Final per-point positions**: S-001 tie; S-002 B; S-003 B; C-001 C after NFR-06 (changed); C-002 C with exact MCP names in `allowed-tools` plus one `affected` pattern (changed); C-003 C plus `query` for the resolver (changed); C-004 B=C; C-005 B's vocabulary inside C with `projectPath` pinned (changed); C-006 C; C-007 B=C (changed); C-008 C with B's artifacts as fallback; C-009 A=C gated on OQ-9; C-010 measure NFR-06 first, drop the trigger (changed); C-011 A=C; C-012 A; X-001 C with A's subsets (U-001), gated on OQ-9, evidence-validator excluded (changed); X-002 amended C, seven tools, explore omitted, after NFR-06 (changed); X-003 B's ban by omission (changed); X-004 B; X-005 B=C (changed); A-001 QUALIFY (changed); A-002 REJECT; A-003 QUALIFY; A-004 REJECT (changed); A-005 REJECT (changed, wording); A-006 QUALIFY.

## Post-Round-2 Convergence Check (orchestrator)

- Per-point tracking: all 26 diff points (S 3, C 12, X 5, A 6) have unanimous or 2/3-majority agreement after Round 2 (see Scoring Matrix).
- Taxonomy coverage: L1 3/3 points addressed; L2 14/14; L3 9/9. Gate passed.
- New points raised in Round 2 outside the diff list: N-001 (`query` as a fourth CLI read verb for the FR-06 resolver) and N-002 (`symbolsOnly` outline exception to the node-file-mode ban). Raised by C only; A and B did not respond. Not in the convergence denominator; carried as unresolved.
- Round 2.5 invariant probe dispatched next (depth standard).

## Round 2.5: Invariant Probe (summary)

The fault-finder ran on the amended-C consensus. It returned 15 findings: 1 ADDRESSED, 14 UNADDRESSED (3 HIGH, 10 MEDIUM, 1 LOW). Full table: `invariant-probe.md`. The 3 HIGH UNADDRESSED items block convergence:
- INV-002: the version and pin cannot be read over MCP alone in closed-Bash orchestrators.
- INV-003: agents that call MCP directly do not receive the orchestrator's readiness state.
- INV-011: one smoke test does not cover every spawn mode, permission scope or version.

## Round 3

Not run: Round 3 requires depth deep, and this run is depth standard.

## Scoring Matrix

Winner = the variant whose approach the advocates agreed is superior after Round 2. "Shared" points count 0.5 for each named variant in the tiebreaker. A-NNN rows record agreement on the assumption, not a variant win.

| Diff Point | Level | Winner | Confidence | Evidence Summary |
|------------|-------|--------|------------|-----------------|
| S-001 | L1 | tie | 90% | Same three-section shape; all three advocates call it cosmetic |
| S-002 | L1 | B | 90% | Fullest self-critique (6 weaknesses); unanimous |
| S-003 | L1 | B | 90% | Cites BR IDs directly; unanimous |
| C-001 | L2 | C (A shared) | 85% | MCP for lookups, 3-15 ms vs about 300 ms (EVAL §5.5-5.6); B conceded, conditional on NFR-06 |
| C-002 | L2 | C | 80% | Exact MCP names in `allowed-tools` plus one `affected` pattern; A's position merged into it |
| C-003 | L2 | C | 75% | Narrow CLI scope; open sub-point N-001 (`query` verb) |
| C-004 | L3 | B=C (shared) | 95% | Mutation grep test; A conceded |
| C-005 | L3 | B content in C transport (shared) | 90% | B's state vocabulary delivered over MCP or CLI; unanimous |
| C-006 | L3 | C | 90% | Explicit degrade rule when the env line is missing; B conceded that B also needs an env line to block explore |
| C-007 | L3 | C | 85% | Fallback plus labels |
| C-008 | L2 | C | 85% | Artifacts where briefs already use them; B's artifacts as fallback |
| C-009 | L2 | A=C (shared) | 85% | Follow-up lookups, gated on OQ-9; B conceded (D-08) |
| C-010 | L2 | B (modified) | 85% | Measure NFR-06 before the env line ships; drop the 100-call trigger; unanimous |
| C-011 | L2 | A=C (shared) | 95% | Measured latency (EVAL §5.6) |
| C-012 | L2 | A | 90% | Smallest change; unanimous |
| X-001 | L3 | C | 80% | MCP names with A's subsets, gated on the OQ-9 smoke test, artifact fallback, evidence-validator excluded |
| X-002 | L2 | C (amended) | 85% | Seven tools, explore omitted, after NFR-06; unanimous |
| X-003 | L2 | B | 95% | Explore ban enforced by leaving it out of the list (EVAL §3, `tools.ts:2926-2929`); unanimous |
| X-004 | L3 | B | 90% | Freshness belongs to the session (BR §2.1 line 69; EVAL §5.7); A and C conceded |
| X-005 | L2 | B=C (shared) | 95% | A conceded its self-contradiction |
| A-001 | L3 | QUALIFY (all) | 90% | Freshness depends on whether the session has an MCP client; session-start spawn is UNVERIFIED |
| A-002 | L3 | REJECT (all) | 95% | An explicit list without explore blocks it |
| A-003 | L2 | QUALIFY (all) | 85% | Approval is not availability; add exact names to `allowed-tools` |
| A-004 | L3 | REJECT (all) | 85% | The set of sessions without MCP is unknown; detect MCP at runtime |
| A-005 | L2 | REJECT (all) | 90% | Phase 1 changes the roster test under every option |
| A-006 | L2 | QUALIFY (all) | 85% | Outputs are Markdown on both paths; MCP inputs are documented |

Diff points won (tiebreaker input): A 2.0, B 6.5, C 10.5.

## Convergence Assessment
- Points resolved: 26 of 26 (S 3, C 12, X 5, A 6)
- Alignment: 100%
- Threshold: 80%
- Taxonomy coverage: L1 3, L2 14, L3 9 (all levels covered)
- Invariant gate: BLOCKED (INV-002, INV-003, INV-011 HIGH UNADDRESSED); 10 MEDIUM warnings
- Status: BLOCKED_BY_INVARIANTS. Depth standard has no Round 3, so the three HIGH items are carried as accepted risks with explicit closure rules in the merge (refactor-plan Changes #9-#11).
- Unresolved points: none among the diff points. New Round 2 sub-points N-001 (`query --json` as a CLI read verb for the FR-06 resolver) and N-002 (`symbolsOnly` outline exception to the node-file-mode ban) were raised by C only. The orchestrator settles both on evidence in the refactor plan (Changes #7 and #8) and flags them for user review.
