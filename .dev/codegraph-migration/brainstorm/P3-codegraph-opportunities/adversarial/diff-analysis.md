# Diff Analysis: spec comparison (P3 codegraph opportunities)

## Metadata
- Generated: 2026-10-29T16:39:25Z
- Variants compared: 3. A = `variant-1-opus-architect.md`, B = `variant-2-sonnet-analyzer.md`, C = `variant-3-haiku-backend.md`
- Source and requirements: `../seed-brief.md` (Success Criteria). Ground truth for fact checks: `../../../research/codegraph-evaluation.md` (EVAL)
- Total differences found: 88 (S + C + X + U)
- Categories: structural (11), content (33), contradictions (21, of which 5 are EVAL or source fact checks), unique (23); shared assumptions: 12 (5 promoted as [SHARED-ASSUMPTION], 1 CONTRADICTED)
- Level tags: L1 surface, L2 structural, L3 state mechanics (priority L3 > L2 > L1; default L2)
- Similarity check: 88 differences across about 60 comparable items (9 sections, 9 vectors, about 40 matched ideas). That is far above 10%, so the variants are **not** substantially identical and the debate is not skipped.

## Structural Differences

| # | Area | Variant A | Variant B | Variant C | Severity | Level |
|---|---|---|---|---|---|---|
| S-001 | Front matter | YAML (variant, persona, model, type, source, ground_truth, date) | YAML (variant, persona, type, topic, source_brief, generated) | None; H1 title plus a persona/scope paragraph | Low | L1 |
| S-002 | Section order | Same nine sections in the same order (Summary → Open questions) | Same nine | Same nine | Low | L1 |
| S-003 | Vector coverage placement | No explicit nine-vector map; vectors appear only as a column in the ideas table | Coverage check as a list inside §4 Ranked list | Nine-vector table inside §1 Summary | Medium | L2 |
| S-004 | Access-model hierarchy | §2.1 table of 7 lettered classes (A-G) + §2.2 blocker table B1-B7 with owners | §2.1 table of 6 classes + §2.2 blockers B1-B8 with owner and stance | One class table (4 classes) + numbered prerequisite list (5) + fenced 4-step contract block | Medium | L2 |
| S-005 | Evidence notation | Value/effort scale defined at the top of §3 | Evidence classes M/P/A defined in a notation paragraph before §1 | None | Medium | L2 |
| S-006 | Idea count | 19 ideas (I-01..I-19) | 10 ideas (I-01..I-10) | 13 ideas (I-01..I-13) | Medium | L2 |
| S-007 | Ranked list format | Numbered list in two layers (Layer 0, Layer 1) with the formula value per item | Table with a score column, then sequencing and coverage notes | Numbered prose list, then a sequencing note | Low | L1 |
| S-008 | Dropped ideas format | Table D-01..D-12 | Table D-01..D-12 | 12 bullets, no IDs | Low | L1 |
| S-009 | Candidate section format | One subsection per candidate (C-1..C-4), bullet fields | One `###` subsection per candidate (N-1..N-3) | One table (C-1..C-4) plus a "Composition" paragraph | Low | L1 |
| S-010 | Risks section | Split into invariants (INV-1..4) and edge-case bullets | Bullets only | Bullets plus an edge-case table (observed behaviour → contract response) | Low | L2 |
| S-011 | Requirement and question counts | FR-01..16, NFR-01..08, Q-1..Q-8 | FR-01..21, NFR-01..09, 8 numbered questions | FR-01..10, NFR-01..07, 8 numbered questions | Low | L1 |

## Content Differences

Ideas are matched by meaning, not by ID. Notation: A:I-04 = Variant A idea I-04.

| # | Topic | Variant A approach | Variant B approach | Variant C approach | Severity | Level |
|---|---|---|---|---|---|---|
| C-001 | Scope: "beyond 1:1 Serena replacement" | Explicitly excludes the 1:1 SYM/REF swaps (INV §4) | Excludes them; I-02 "restores what the 1:1 swap loses" | Several ideas are 1:1 swaps: I-02 "replace Serena overview/find_symbol rows", I-04 replaces `find_declaration`, I-05 replaces `find_referencing_symbols`, I-06 replaces the Serena fallback tier | High | L2 |
| C-002 | Default access path per class | MCP where listed for troubleshoot/reflect (Class A) and read-only agents (Class D); CLI for implement, workflow, scoped-Bash skills; native fallback for agents until listing | CLI-first everywhere; the orchestrator computes artifacts and passes them into agent briefs by path; agents get no MCP names in v1 | CLI for Bash-capable orchestrators; read-only agents MCP-only and blocked until listing; graph work stays in the parent until then | High | L2 |
| C-003 | `CODEGRAPH_MCP_TOOLS` listing | Phase 2 must add `node,search,callers,callees,impact,status` (B1); explore/files is Q-1 | Do not set it in v1; if needed later, `explore,node,search,callers,impact,status`; measure schema overhead first | Treated as an open blocker owned by the installer; quotes the full 8-tool list | Medium | L2 |
| C-004 | Bash allowlist granularity | `Bash(codegraph *)` where the body calls the CLI (Class C) | One pattern per subcommand; never `Bash(codegraph *)` (FR-04) | Five explicit read-only verbs (FR-10), but §2 says "adding `Bash(codegraph *)` patterns" and I-07 uses a `;`-joined pattern | High | L3 |
| C-005 | Shared seam | `sc-graph-grounding` skill with arguments (`--need --target --depth --limit`), capability map, probe, citation resolution, degraded vocabulary; output `graph-facts.yaml` | `sc-codegraph-probe` skill (probe + citation contract + `resolve-callsite.sh`); consumers call it as Step 0 | `sc-graph-protocol` skill, guidance only, no args, no output; 4-step PROBE→CALL→VERIFY→DEGRADE | Medium | L2 |
| C-006 | State model and degraded vocabulary | `index_state: fresh/pending/not_initialized/foreign_index/absent/disabled` + 11 closed `graph:*` tokens | `codegraph_state: ready/stale/uninitialized/foreign-index/absent/error`; foreign-index handled as uninitialized; `parse_failed` | Binary `graph: available/unavailable` + `stale`; run-scoped latch, never retried; free-form keys such as `test-scope:codegraph_stale` | Medium | L3 |
| C-007 | Probe freshness and `sync` | One probe per run; if pending, try one `sync`; a lock error means the daemon owns freshness (FR-10) | Probe never syncs; re-run `status` right before the queries; pending → `stale: true`, leads only | Never sync (FR-06); first probe is authoritative for the run; pending → `stale: true` | Medium | L3 |
| C-008 | Token cost / explore policy | Explore named in no `tools:` line and no step body (FR-05) | Explore banned in budgeted waves (<8K), troubleshoot Wave 1 and subagents; allowed interactively with `maxFiles ≤ 5`; `context` also banned (FR-10) | Explore admitted only with `maxFiles 1-5` and a single-symbol query (FR-08) | Medium | L3 |
| C-009 | Citation accuracy mechanism | `resolution: def-line/call-site-verified/unresolved` on every row; Grep after the def line, then re-Read; validator checks def-line rows as definitions | Resolver script: `query --json` start/end span, Grep inside it, Read; status `lead-unverified`; `call_site_line` only from the resolver | Callers give identity and count only; call site by an explicit Grep step; rows that fail re-Read are dropped, never repaired; `/sc:ground` verify layer | High | L3 |
| C-010 | evidence-validator role | Edited (I-02) and listed in Class D for MCP names | Stays `Read, Grep, Glob` (FR-06, D-11) | Gets no codegraph tools (drop) | Medium | L2 |
| C-011 | Impact before edits | A:I-05 implement Q1 pre-edit impact via `/sc:impact` (cap 10 files); A:I-10 pre-fix impact in pr-submit Wave 4 and troubleshoot `--fix` | B:I-07 untouched-dependents block added to the Q2/Q3 reviewer package after the edit (rank 10); PreToolUse impact hook dropped | C:I-11 risk note in workflow/tasklist; `/sc:impact` called by implement as a pre-edit check | Medium | L2 |
| C-012 | Review scoping (auggie-review) | A:I-09 caller note as context only; out-of-hunk downgrade kept; rank 17 | B:I-04 blast-radius artifact + new `dependent-impact` finding class exempt from the out-of-hunk downgrade when Read-verified (FR-12); rank 5 | C:I-08 context block, top-5 symbols by churn, in-hunk rule untouched; rank 9 | High | L3 |
| C-013 | Test selection (`affected`) | Immediate union `changed-area ∪ affected`; `selected ⊇ heuristic` (FR-07) | Advisory delta first; union only after a 20-change backtest (NFR-08); never removes tests | Replaces `<changed-area>` with the derived list; heuristic only when graph is empty or unavailable (FR-05) | High | L3 |
| C-014 | `affected` invocation shape | Positional file args; pipeline matching under scoped Bash is UNVERIFIED (Q-2) | Args, or `--stdin` from a file | `git diff --name-only … \| codegraph affected --stdin --json` | Low | L2 |
| C-015 | Troubleshoot Tier 1 | A:I-04 search + node + callers (limit 10) in Wave 1 and 1.6 Branch A; rank 4 | B:I-06 `tier1-callers.md` artifact (cap 40 rows) pasted into 1.6 briefs; rank 6 | C:I-02 node `symbolsOnly` + search for the outline (rank 3); C:I-03 callers list for 1.6 (rank 8) | Medium | L2 |
| C-016 | Planning: workflow, tasklist | A:I-13 workflow impact counts (rank 15); tasklist dropped (D-03, determinism) | Workflow touch-set preview dropped (D-07); tasklist dropped (D-06) | C:I-11 impact risk note in both workflow and tasklist (rank 7) | Medium | L2 |
| C-017 | Reflect severity semantics | Count resolved call sites, or label the number `caller_functions` (FR-08) | Count distinct production caller symbols only, using the runtime-surface prod/test table (FR-09) | Re-word the rule to caller count; when stale, treat HIGH as MEDIUM | High | L3 |
| C-018 | Reflect contract fields | May add a `caller_functions` label (Q-6) | No new field in v1; only `degraded_components` entries (FR-14) | Additive `graph:`/`degraded:` keys with a minor `contract_version` bump (NFR-04) | Medium | L3 |
| C-019 | cleanup-audit | A:I-12 zero graph callers adds DELETE confidence; nonzero gives the KEEP citation; rank 18 | Dropped entirely (D-05): read-only audit, graph adds nothing over grep | C:I-07 `impact > 0` upgrades a DELETE to REVIEW; `impact = 0` proves nothing; rank 11 | Medium | L3 |
| C-020 | reuse-auditor | A:I-11 caller liveness check + `search {kind}` fallback via MCP | Co-caller search dropped (D-08); agent gets artifacts, no MCP | C:I-06 search + node fallback tier, blocked by listing | Medium | L2 |
| C-021 | Onboarding: index-repo, explain, load | Explain one-hop (I-14), index-repo stats (I-15, last), load status line (I-16) | `/sc:load --index` (I-09) and `sc-structure-brief` for index-repo and explain (I-10) | index-repo sections (I-12, last), explain callers/callees (I-13); load rewrite dropped | Low | L2 |
| C-022 | Hooks | New SessionStart status line, ≤2 s timeout (I-17, FR-15) | No new hooks (FR-19); SessionStart status dropped (D-03) | "Hooks need nothing from codegraph" | Medium | L2 |
| C-023 | Per-worktree `init` owner | `/sc:graph init`, user-typed only; refuses in a nested worktree without `--worktree-local` | `/sc:load --index` is the only path that may run `init --yes` (FR-17) | No primitive ever runs `init` (FR-06 grep) | High | L3 |
| C-024 | Ranking method | Layer 0 prerequisites, then `V × Frequency ÷ (Effort × Risk)` | Enablers, then `V × Confidence ÷ Effort` (M=1.0, P=0.6, P-minus=0.3) | Qualitative risk-discounted value/effort with a prerequisite bonus and a blocker penalty | Medium | L2 |
| C-025 | Top five order | allowlists, contract, citation resolution, troubleshoot callers, test superset | probe, resolver, routing/token guard, reflect parity, review blast radius | contract, pr-submit `affected`, troubleshoot Tier 1, reflect touched-symbol derivation, implement Q6 | Medium | L2 |
| C-026 | Dropped set | Unique drops: graph-scout agent, cluster-based chunking, replacing LSP diagnostics, freshness matchers | Unique drops: PreToolUse impact hook, SessionStart hook, troubleshoot producer enumeration, cleanup-audit, workflow, reuse co-caller | Unique drops: load rewrite, `sync`, `sc-recommend` routes, private per-skill scripts, cleanup-audit test runs | Medium | L2 |
| C-027 | Candidate names and count | 4: `sc-graph-grounding`, `/sc:impact`, `sc-test-scope` (skill), `/sc:graph` | 3: `sc-codegraph-probe`, `sc-blast-radius` + `/sc:blast-radius`, `sc-structure-brief` | 4: `sc-graph-protocol`, `/sc:impact`, `/sc:test-scope` (command), `/sc:ground` | Medium | L2 |
| C-028 | Candidate interfaces | `/sc:impact` symbol / file / `--diff`, depth 2 default, limit 20 (max 100), `--tests`; test scope `selected = heuristic ∪ affected` | `/sc:blast-radius --base --symbols --files`, depth 1-2, prod/test split, `affected_tests` or `unknown` | `/sc:impact` symbol, depth 1-3, unverified rows dropped; `/sc:test-scope` `source: graph/heuristic/none` | Medium | L2 |
| C-029 | Candidate callers | Seam called by troubleshoot, reflect, implement, pr-submit; agents read its refs by path | Probe called by auggie-review, pr-submit, reflect, troubleshoot, implement, load, index-repo, explain | Contract called by troubleshoot, reflect, cleanup-audit, auggie-review, implement, workflow | Low | L2 |
| C-030 | Truncation and ambiguity | `truncated: true` + total; pass `file`; `graph:ambiguous` | Record shown/total; re-query once if total ≤100 (FR-08); `ambiguous[]`; notes CLI `callers` has no documented file arg | Record `total_count` apart from rows; pin with `file`; `dropped: ambiguous` | Low | L3 |
| C-031 | Requirement emphasis | Containment count, mirror parity, version honesty, kill switch | Golden fixtures, byte-identical output, backtest, BASH policy batching, 2K-token context cap | Idempotency/caching, mutation-exclusion grep, additive contracts, rollout order | Medium | L2 |
| C-032 | Risk emphasis | Telemetry on the CLI path, Markdown repos get no signal, old daemon/new client | Allowlist blast radius (`install`), caller-count semantics, output-format drift | Stale counts skew severity, docs-only diffs, per-hunk latency | Medium | L2 |
| C-033 | Rollback | Revert the PR, or set `status: disabled` (NFR-08) | Uninstall the binary; absence equals the native path | Delete the codegraph text; fallback restores today's behaviour byte for byte | Low | L2 |

## Contradictions

| # | Point of conflict | Variant A position | Variant B position | Variant C position | Impact | Level |
|---|---|---|---|---|---|---|
| X-001 | MCP names in read-only agents | "Add the exact MCP names to `tools:`" (Class D) | "In v1 no `tools:` line of a read-only agent gains `mcp__codegraph__*`" (FR-11) | Gains names "only when their body actually calls them" (FR-09) | High | L2 |
| X-002 | Wildcard Bash pattern | "Add `Bash(codegraph *)` only where the body calls the CLI" | "never `Bash(codegraph *)`"; it "would pre-approve `install`/`upgrade`/…" | FR-10 "no bare `Bash(codegraph *)`", yet §2 "adding `Bash(codegraph *)` patterns" and §1 "no allowlist change" (self-contradiction) | High | L3 |
| X-003 | Listing env in v1 | B1 owner adds `CODEGRAPH_MCP_TOOLS` | "Do not set it in v1" | Left as an open question for the installer | Medium | L2 |
| X-004 | evidence-validator | Targets `agents/evidence-validator.md` (I-02) and lists it in Class D | "keeps `tools: Read, Grep, Glob`" (FR-06) | "Giving the evidence-validator codegraph tools" dropped | Medium | L2 |
| X-005 | Who may run `init` | "No primitive except C-4 under an explicit user `init`" (FR-09) | "`/sc:load --index` is the only primitive path that may run `codegraph init --yes`" (FR-17) | "no primitive text contains `codegraph init`" (FR-06) | High | L3 |
| X-006 | `sync` from primitives | "if files are pending, try one `sync`" | "No primitive calls `sync`" | "Primitives must never call `sync`" | Medium | L3 |
| X-007 | SessionStart hook | I-17 adds a one-line status hook | "a one-line status adds nothing the probe does not already give" (D-03) | "Hooks need nothing from codegraph" | Medium | L2 |
| X-008 | VG-1 gate change | "VG-1 runs `changed-area ∪ affected`" (now) | "union into VG-1 only after a backtest passes" | "Replaces the hand-named `<changed-area>`"; `tests` "is exactly the parsed `affected --json` list" (can narrow the set) | High | L3 |
| X-009 | Out-of-hunk downgrade | "findings outside hunks keep today's downgrade" | `dependent-impact` "exempt from the out-of-hunk downgrade" when verified (FR-12) | "in-hunk downgrade rule untouched" | High | L3 |
| X-010 | Tasklist graph input | Dropped: tiering "would then depend on local index state" (D-03) | Dropped: "a live index would break determinism" (D-06) | I-11 targets `sc-tasklist-protocol/SKILL.md`, records `affects_n_callers` | Medium | L2 |
| X-011 | Workflow impact step | Adopted (I-13) | Dropped as class A (D-07) | Adopted (I-11) | Medium | L2 |
| X-012 | Meaning of zero callers in cleanup-audit | "zero graph callers is extra evidence for DELETE" | Graph "cannot tighten DELETE"; idea dropped | "impact=0 proves nothing (call graph only)" | Medium | L3 |
| X-013 | Reflect severity count | Resolved call sites, or label `caller_functions` | "distinct production caller symbols only" | "re-worded to caller count" (tests included) | Medium | L3 |
| X-014 | Explore anywhere in primitives | "no step body names `codegraph_explore`" (FR-05) | Allowed in interactive commands with `maxFiles` ≤5 | Allowed "only with `maxFiles` between 1 and 5" | Medium | L3 |
| X-015 | Tier 1 token budget | "≤~3k Wave 1 budget (`:218`)" | "about 3K Claude tokens (`:218`)" | "≤2k-token Tier-1 budget (Wave 1.5 :256)". `SKILL.md:218` sets Wave 1 at ~3k; `:256` is Wave 1.5's 2k budget, so C cites the wrong wave | Low | L1 |
| X-016 | `/sc:load` | I-16 status line | I-09 adds `--index` (runs `init`) | "Rewriting `/sc:load` around codegraph" dropped | Low | L2 |
| X-017 | EVAL check: `status` latency | "`codegraph status` (~300 ms, EVAL §5.5)"; NFR-02 the same | "`status` timing UNVERIFIED, measure" | — | Low | L2 |
| X-018 | EVAL check: MCP tool names | Uses `mcp__codegraph__codegraph_{callers,…}` | — | Uses `mcp__codegraph__search`, `__callers`, `__node`, `__status`. EVAL §3 names the tools `codegraph_search` etc., so the server-prefixed names are `mcp__codegraph__codegraph_*`. C's allowlist entries would not match | Medium | L3 |
| X-019 | EVAL check: CLI outline | — | — | I-02 uses `codegraph_node {file, symbolsOnly:true}` and claims "skill has Bash → CLI works today". EVAL §3 lists only `node [name]` for the CLI, with no file or symbolsOnly flag | Medium | L2 |
| X-020 | EVAL check: grep vs graph coverage | — | "Grep sees every static reference the graph sees" (D-05) | "grep misses ≠ graph misses" (I-07). EVAL states neither; it reports "Linking dynamic dispatch" (§5.4) and interface→impl dispatch via explore (§6.2). Both claims are UNVERIFIED | Low | L2 |
| X-021 | EVAL check: caller sample | — | "only 2 were production callers … and the rest were test functions" | — EVAL §5.5 shows 20 of 23 rows (2 production, 18 tests); the 3 hidden rows were not inspected | Low | L1 |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | A | Kill switch: `status: disabled` header in the capability map degrades every consumer (FR-16) | Medium |
| U-002 | A | Telemetry blocker: Bash CLI calls do not inherit the MCP entry's `CODEGRAPH_TELEMETRY=0` (B5) | High |
| U-003 | A | Value depends on the target repo's language; Markdown primitives get no graph signal (EVAL §5.4) | High |
| U-004 | A | `/sc:graph` lifecycle command that refuses `init` in a nested worktree unless `--worktree-local` | Medium |
| U-005 | A | Reflect UC-2 regression evidence: touched code with mapped tests that were neither changed nor run (I-08) | Medium |
| U-006 | A | Pre-fix impact in remediation chains: pr-submit Wave 4 and troubleshoot `--fix` (I-10) | Medium |
| U-007 | A | Allowlists ranked as prerequisite #1 (Layer 0) because Class A/D cannot call anything without them | Low |
| U-008 | B | Evidence-confidence classes M/P/A that weight the ranking score | Medium |
| U-009 | B | Parity hazard: a 1:1 swap to callers inflates reflect severity with test callers; partition prod/test using the runtime-surface table | High |
| U-010 | B | `affected` backtest gate (≥20 merged changes, recall ≥ changed-area, median ≤25 files) before any gate change | High |
| U-011 | B | `dependent-impact` finding class for auggie-review | Medium |
| U-012 | B | Golden fixtures of v1.6.2 text output; a parse mismatch degrades as `parse_failed` | Medium |
| U-013 | B | Provenance check: `index_root` must equal the realpath of `git rev-parse --show-toplevel` | Medium |
| U-014 | B | Listing more MCP tools adds always-loaded schema cost per session; measure first | Medium |
| U-015 | B | `sc-structure-brief` onboarding skill | Low |
| U-016 | B | Query batches follow `BASH_INSPECTION_POLICY.md` (NFR-02) | Low |
| U-017 | B | Re-query once with a wider `--limit` when total ≤100 (FR-08) | Low |
| U-018 | C | PROBE → CALL → VERIFY → DEGRADE sequence with a run-scoped latch and no retry | Medium |
| U-019 | C | `/sc:ground` command: graph locates, Read verifies, dropped rows carry reasons | Medium |
| U-020 | C | Idempotency: graph results cached per run, one computation per validation cycle (FR-07) | Low |
| U-021 | C | Stale index → reflect treats HIGH as MEDIUM | Medium |
| U-022 | C | Docs-only diffs may honestly yield no tests; escalation is keyed on source-file diffs | Medium |
| U-023 | C | Additive contract keys with a minor `contract_version` bump (NFR-04) | Low |

## Shared Assumptions

Classification: STATED = at least one variant states it explicitly and no source contradicts it; UNSTATED = no variant states it; CONTRADICTED = the seed brief, EVAL or a cited primitive contradicts it. UNSTATED rows are promoted as [SHARED-ASSUMPTION].

| # | Agreement point (all three) | Precondition | Class | Level |
|---|---|---|---|---|
| A-001 | Every codegraph step is fail-open with a named native fallback | Seed constraint; FR-02/FR-03 (A), FR-02 (B), NFR-01 (C) | STATED | L3 |
| A-002 | Graph `file:line` is re-Read before it is cited | Seed citation contract; EVAL §5.5 definition-line gap | STATED | L3 |
| A-003 | Explore is not a default grounding step | auggie is available as the free server-side alternative. The seed brief says "auggie MCP not available in this session"; when auggie is down, the fallback is Grep/Read, not auggie | CONTRADICTED | L2 |
| A-004 | Explore is token-negative | One measured explore call (24,913 chars) is typical of explore output. All three quote that single sample as the rule; none treats it as a sample of one | UNSTATED → **[SHARED-ASSUMPTION]** | L2 |
| A-005 | Targeted callers/impact/node calls are cheap in tokens | Output size of callers/impact was never measured in characters (EVAL §5.5-5.6 report latency only). A's "a few hundred tokens" and C's "~1k" caps are estimates | UNSTATED → **[SHARED-ASSUMPTION]** | L2 |
| A-006 | One probe per run is enough | Index state does not change during the run. Implement and pr-submit edit files mid-run, and in CLI-only sessions no watcher runs (EVAL §4), so post-edit queries read the pre-edit index. B partly notices this ("re-run `status` immediately before the queries") but still requires one probe per run (FR-01) | UNSTATED → **[SHARED-ASSUMPTION]** | L3 |
| A-007 | Caller lists are usable for severity and blast radius | The call graph finds all static production callers for Python. EVAL verified this for one symbol only (§5.5); all three treat empty results as non-evidence but treat non-empty lists as complete | UNSTATED → **[SHARED-ASSUMPTION]** | L3 |
| A-008 | Test selection uses `affected` in Bash orchestrators | `affected` output is correct and parseable. EVAL never ran `affected`; B states this (I-08, NFR-08), A and C do not | STATED (B only) | L3 |
| A-009 | Consumers never auto-init from read-only flows | `init` writes 34 MB and peaks near 1 GB RSS (EVAL §5.4) | STATED | L3 |
| A-010 | Foreign-index answers are discarded | EVAL §5.8 nested-worktree warning text is stable across versions; pinned to v1.6.2 | STATED | L3 |
| A-011 | Graph value reaches primitives at all | Someone initializes the index in each worktree. With no owner (EVAL §4, §7), every consumer degrades in fresh sibling worktrees; C states this (Q-2), A and B partly | STATED | L2 |
| A-012 | A shared skill or ref can be loaded by every consumer | Orchestrators can invoke a peer skill cheaply, and agents can Read its refs by installed path. B raises the Skill-call cost (Q-6); A relies on agents reading refs by path | UNSTATED → **[SHARED-ASSUMPTION]** | L2 |

Requirement coverage against the seed brief's Success Criteria: all three name target, value, effort and risk per idea; all give one ranked list and explicit drops; candidates: A 4, B 3, C 4 (all within 3-5, all with callers); blockers (listing env, per-worktree `init`, freshness) appear in all three. Traceability failures to EVAL: X-017 (A), X-018 and X-019 (C), X-020 (B and C), X-021 (B). Scope failure: C-001 (C).

## Summary
- Total structural differences: 11
- Total content differences: 33
- Total contradictions: 21 (16 between variants, 5 EVAL or source fact checks)
- Total unique contributions: 23 (A 7, B 10, C 6)
- Shared assumptions: 12 (5 promoted [SHARED-ASSUMPTION]: A-004, A-005, A-006, A-007, A-012; 1 CONTRADICTED: A-003)
- Level distribution (77 S/C/X/A rows): L3 = 28, L2 = 41, L1 = 8
- Highest-severity items: C-001, C-002, C-004, C-009, C-012, C-013, C-017, C-023, X-001, X-002, X-005, X-008, X-009; unique High: U-002, U-003, U-009, U-010
- Similarity: not substantially identical (differences far exceed 10% of comparable items); proceed to debate.
- Main debate axes: (1) agent access (MCP names vs artifacts in briefs), (2) allowlist granularity, (3) gate changes (VG-1, out-of-hunk rule, reflect severity), (4) mutation ownership (`init`, `sync`, hooks), (5) C's 1:1-swap scope drift.
