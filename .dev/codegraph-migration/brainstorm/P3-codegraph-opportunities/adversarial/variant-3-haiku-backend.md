# Variant 3 — BACKEND: codegraph v1.6.2 beyond 1:1 Serena replacement

Persona: backend (data integrity, API contracts, idempotency, fault tolerance, operations).
Scope: `src/superclaude/{skills,commands,agents,core,hooks}` guidance text, `tools:`/`allowed-tools` allowlists, return-contract values, and new primitives. Planning only. Ground truth: `.dev/codegraph-migration/research/codegraph-evaluation.md` (EVAL); no capability is claimed outside it.

## 1. Summary

- **Treat codegraph as a dependency with a contract, not a tool list.** Every adoption below is expressed as: status probe → call → verify → degrade. The single highest-leverage artifact is one shared contract ref (I-01) that all consumers load; per-primitive inline steps would drift and duplicate the same fail-open prose six times.
- **Access splits by primitive class, and the split is enforceable today.** Bash-capable orchestrators (workflow, implement, troubleshoot, pr-submit, auggie-review, cleanup-audit) use the CLI — no allowlist change, no `CODEGRAPH_MCP_TOOLS` dependency. Read-only agents (reuse-auditor, troubleshoot-analyst, reflect-reviewer) cannot run the CLI; they get value only if the registration sets `CODEGRAPH_MCP_TOOLS`, which the planned registration (EVAL §7 step 5) does not. Until that changes, graph work in those agents stays in the Bash-capable parent.
- **`codegraph affected` (CLI-only) is the clearest net win**: it converts pr-submit VG-1 and implement Q6 from a hand-named "changed area" to a derived test-file list, with a machine-checkable output contract and a heuristic fallback that is exactly today's behavior.
- **The definition-line gap is a data-integrity boundary, not a footnote.** Caller rows cite the caller's definition line, never the call site (EVAL §5.5). Therefore codegraph output may name *who* calls, but never *where*; every cited `file:line` must be re-Read, and call-site discovery stays Grep.
- **Zero callers is not zero references.** The graph is call edges only; imports, string references, dynamic dispatch and config mentions are invisible to `callers`/`impact`. Cleanup-audit's grep proof of zero references remains the DELETE gate; codegraph is corroboration only.
- **`codegraph_explore` is not a token saving** (one call returned 24,913 characters and two unrelated `install` functions, EVAL §5.6). It is admitted only with `maxFiles ≤ 5` and a single-symbol query, never as a default grounding step.
- **Hooks need nothing from codegraph.** All codegraph tools are read-only (`readOnlyHint`, EVAL §3), so the freshness edit gate never gains a codegraph matcher; Phase 1 only *removes* the four Serena edit names from `hooks.json` and `freshness-pre-edit.sh` (1:1 work, listed here only to bound it).
- **Idempotency and rollback are free by construction** if we hold one rule: primitives never run `init`, `index`, `sync`, `uninit`, or `unlock`. Those are installer/owner mutations; a primitive that mutates index state cannot be safely re-run or rolled back.

**Nine-vector coverage map** (where each vector's value comes from; every vector is covered by at least one idea in §3):

| Vector | Primary ideas | Net position |
|---|---|---|
| Token cost | I-02, I-13, I-12; explore banned (FR-08) | Neutral-to-positive; the win is fewer Read/Grep tours, not graph payloads |
| Accuracy of citations | I-03, I-04, C-4, FR-03/FR-04 | Positive, but only *through* the mandatory re-Read; raw graph rows are never citation-grade |
| Impact analysis before edits | I-11, C-2, I-04 | Positive and novel — no primitive computes blast radius today (enrichment observation 3) |
| Review scoping | I-08, I-09 | Positive but bounded: context blocks and test scope, never evidence or gates that bypass the in-hunk downgrade rule |
| Test selection | I-09, I-10, C-3 | The clearest measurable win; `affected` is CLI-only, which the Bash-capable callers already satisfy |
| Troubleshooting Tier 1 | I-02, I-03, C-4 | Positive; the existing Glob/Grep fallback exit criteria make this the lowest-risk adoption |
| Planning/workflow | I-11, I-10 | Positive; planning has Bash in its allowlist but no MCP names, so CLI is the only path |
| Reflection/audit | I-04, I-05, I-06, I-07 | Largest surface (reflect is the heaviest Serena consumer) and the most contract coordination |
| Onboarding | I-12, I-13, C-4 | Modest; index-repo's current Glob flow already meets its token claim, so additions are opportunistic |

## 2. Access model and prerequisites

| Primitive class | Examples | Access path | Why |
|---|---|---|---|
| Bash-capable skill orchestrators | sc-workflow-protocol, sc-implement-protocol, sc-troubleshoot-protocol, sc-pr-submit-protocol, sc-auggie-review-protocol, sc-cleanup-audit-protocol (orchestrator) | CLI via Bash (`codegraph status`, `query`, `callers`, `impact`, `affected --stdin --json`) | No allowlist change beyond adding `Bash(codegraph *)` patterns where the allowlist enumerates Bash (cleanup-audit `:8` enumerates `Bash(git *)` etc. and has no codegraph pattern today). `affected` exists only in the CLI. Cost: ~290-300 ms per CLI query vs 3-15 ms per MCP callers call (EVAL §5) — acceptable for once-per-wave orchestrator steps. |
| Read-only agents | agents/reuse-auditor.md, troubleshoot-analyst, reflect-reviewer, evidence-validator, audit-* | MCP only (`mcp__codegraph__search`, `__callers`, `__node`, `__status` names in `tools:`) | No Bash in roster. **Blocker:** Claude Code can only call *listed* tools, and only `codegraph_explore` is listed by default; the other 7 need `CODEGRAPH_MCP_TOOLS=explore,node,search,callers,callees,impact,files,status` in the server env. The planned registration sets only `CODEGRAPH_TELEMETRY=0`, `CODEGRAPH_NO_UPDATE_CHECK=1` (EVAL §3, §7 step 5). |
| Plain commands (no enforced allowlist) | commands/index-repo.md, commands/explain.md, commands/load.md | CLI via Bash preferred; MCP as a bonus tier | Commands run in the main session, which has Bash. CLI avoids the listing blocker entirely. |
| Hooks | hooks/hooks.json, hooks/scripts/freshness-*.sh | None | codegraph is read-only; no edit-tool matcher is needed. Only the Serena-name removal is in scope (Phase 1 EDIT job). |

Prerequisites and owners:

1. **Tool listing env** (`CODEGRAPH_MCP_TOOLS`) — owner: installer phase (EVAL §7 step 5 currently omits it). Blocks every read-only-agent idea (I-06 and the reflect reviewer-facing calls). Until set, those ideas ship in their fallback shape only.
2. **Per-worktree `codegraph init`** — owner: unassigned (EVAL §4, §7 open follow-ups). IronClaude worktrees live as siblings (`~/workspaces/worktrees/<repo>/<branch>`), which are "not initialized" until `init` runs there; nested worktrees answer from the parent index *with a warning*. Every consumer must treat "not initialized" and "different working tree" as `graph=unavailable`, never as an answer.
3. **Freshness/daemon lock** — owner: codegraph itself, consumer contract here. The watcher runs only while an MCP client is connected; `codegraph sync` fails on the writer lock while a daemon runs (EVAL §4, §5.7). Primitives must never call `sync`; staleness is detected via `codegraph status` (pending-sync section / staleness banner) and recorded as a degraded value.
4. **Definition-line caller rows** — owner: upstream (single maintainer). Consumers own the mitigation: re-Read + Grep for call sites. This is a permanent contract assumption, not a temporary one.
5. **Version pin** — owner: installer (IronClaude pin v1.6.2 + SHA-256 table, EVAL §7). Primitives never assume a version or invoke `codegraph upgrade`.

**The primitive↔codegraph contract** (what I-01 materializes as text; every consumer step conforms to this sequence):

```text
1. PROBE  (once per run, before any graph call)
   CLI:  codegraph status            → maps to one of:
   MCP:  codegraph_status
     • "✓ Index is up to date"                      → graph: available
     • "⚠ Not initialized … Run codegraph init"     → graph: unavailable   (latch; no retry)
     • "⚠ This CodeGraph index belongs to a different git working tree"
                                                    → graph: unavailable   (latch; never partial trust)
     • staleness banner / pending-sync section      → graph: available, stale: true
     • command not found / tool not listed          → graph: unavailable   (latch)
2. CALL   only the read-only five: status, query/search, node, callers/callees, impact, affected.
         One call per symbol per wave; results cached for the run (FR-07).
3. VERIFY every file:line the result will feed into an artifact is re-Read at that exact line
         (FR-03). A row that fails re-Read is dropped with reason `unverified`, never repaired
         by guessing an offset. Caller rows are caller identity only (FR-04).
4. DEGRADE on any failure at steps 1-3: run the named native fallback, append the degraded
         key to the return contract (e.g. degraded: ["test-scope:codegraph_stale"]),
         continue the run. Never STOP, never retry the probe, never mutate index state.
```

This sequence is the idempotency and fail-open story in one place: steps 1-2 are pure reads (safe to replay), step 3 is the freshness-system-compatible bridge (Read is the only citation-grade accessor), step 4 is the observable degradation that downstream consumers and telemetry read.

## 3. Ideas

| ID | Idea | Vector(s) | Target primitive(s) | codegraph mechanism | Expected value | Effort | Risk | Native fallback |
|---|---|---|---|---|---|---|---|---|
| I-01 | Shared graph-contract ref + protocol skill: one status probe per run, tool-selection table, degraded-value vocabulary, re-Read rule, fallback map | all (enabler) | new `skills/sc-graph-protocol/` (see C-1); consumed by every idea below | `codegraph status` (CLI) or `codegraph_status` (MCP) as the single probe | One auditable contract instead of six divergent inline copies; makes degradation observable in return contracts | S | Low; ref could go stale vs EVAL — pin a "ground truth: EVAL" header | Each consumer step already names its own fallback today |
| I-02 | Troubleshoot Wave 1 Tier-1 grounding: replace Serena overview/find_symbol rows | troubleshooting, token cost | `skills/sc-troubleshoot-protocol/SKILL.md` (:4 allowlist, :183-216), `commands/troubleshoot.md` | `codegraph_node {file, symbolsOnly:true}` per candidate file + `codegraph_search {query, kind}` for the symbol | Keeps the ≤2k-token Tier-1 budget (Wave 1.5 :256); outline+symbol in 2 cheap MCP calls (3-15 ms class) or 2 CLI calls | S | Listing blocker for the MCP path in-session is none (skill has Bash → CLI works today) | Existing Glob/Grep fallback already accepted by the Wave-1 exit criteria (:216) |
| I-03 | Wave 1.6 "immediate callers" of the failing component as a structured list, not prose | troubleshooting, citation accuracy | `skills/sc-troubleshoot-protocol/SKILL.md` (:286 Branch A) | `codegraph callers <symbol> --limit 20` (CLI); caller identity only, call sites via Grep | Replaces an auggie prose answer with an enumerated caller set the audit log can cite; definition-line caveat handled by contract | S | Call graph misses non-call references — callers list is a floor, not exhaustive | auggie query + Grep (current path) |
| I-04 | Reflect Step 1B.3: derive touched symbols from task diff hunks | reflection/audit, accuracy | `skills/sc-reflect-protocol/SKILL.md` (:342, 6 LB SYM rows) | `codegraph_search` + `codegraph_node {symbol, includeCode:true}` to resolve hunk symbols; `codegraph_node {symbol}` replaces `find_declaration` anchoring (:340) | Removes the heaviest Serena consumer's symbol dependency; node returns definition + body to anchor overlap edges | M | Ambiguous symbols return every overload — pin with `file`; name-path addressing (`Class/method`) does not exist, so derivation works at file+symbol granularity | Read of the hunk + Grep for the def site |
| I-05 | Reflect overlap-edge shared-vs-collision test | reflection/audit | `skills/sc-reflect-protocol/SKILL.md` (:344, :514) | `codegraph callers <symbol> --limit 100` (or MCP `codegraph_callers {symbol, file, limit≤100}`) | Deterministic shared-use signal replacing `find_referencing_symbols`; the "Showing N of M" count feeds the severity rule | M | Count is *callers*, not call sites — the HIGH >5 / MEDIUM 2-5 / LOW 1 rule must be re-worded to caller count (contract change, coordinate with reflect CLI owner) | Grep the symbol name across src; treat ≥2 files as shared |
| I-06 | Reuse-auditor auggie-down fallback tier: Serena find_symbol+ripgrep → codegraph search+ripgrep | reflection/audit | `agents/reuse-auditor.md` (:5, :126, :131) | `mcp__codegraph__search`, `mcp__codegraph__node` in `tools:` | Cheaper, name-agnostic structure signal on the fallback path; keeps findings capped at advisory (unchanged) | S | **Blocked** by listing env (read-only agent, no Bash); until then the fallback stays ripgrep-only and records `neighbour-search:codegraph_unlisted` | ripgrep skeleton grep (already the floor) |
| I-07 | Cleanup-audit DELETE corroboration: grep proof stays the gate; graph adds an independent "zero inbound call edges" signal | reflection/audit | `skills/sc-cleanup-audit-protocol/SKILL.md` (:75, :83, :86, :151) | orchestrator-only: `codegraph impact <symbol> --depth 2` per DELETE candidate; add `Bash(codegraph status *;codegraph impact *;codegraph callers *)` to the allowlist | Second independent evidence source for the riskiest classification; reduces false DELETEs from grep blind spots inverting (grep misses ≠ graph misses) | M | Must never *lower* the bar: impact>0 → upgrade to REVIEW; impact=0 proves nothing (call graph only) | Grep proof alone (today's gate, unchanged) |
| I-08 | Auggie-review blast-radius context block for reviewers | review scoping | `skills/sc-auggie-review-protocol/SKILL.md` (:126-138 inputs, :218 in-hunk rule) | per top changed symbol: `codegraph callers <sym> --limit 20` / `impact --depth 2`; append a "callers of changed symbols" block to the auggie prompt file | Reviewer sees who depends on the change without spending reviewer turns on retrieval; context only — never evidence (in-hunk downgrade rule untouched) | M | Prompt size growth on wide diffs; cap at top-5 changed symbols by churn | No block appended; reviewers work from the diff (today) |
| I-09 | pr-submit VG-1 test selection from the graph | test selection, review scoping | `skills/sc-pr-submit-protocol/SKILL.md` (:206 VG-1) | `git diff --name-only <pre>..<head> \| codegraph affected --stdin --json --quiet` once per validation cycle | Replaces the hand-named `<changed-area>` with a derived test-file list; deterministic, replayable, recorded in the run-log next to the VAL gates | S-M | `affected` maps to test files only, no diff-to-symbol mapping (EVAL §6.1); empty result on a src diff must NOT skip tests — fall back, never silence | Existing changed-area heuristic, then VG-2 `make test` escalation (unchanged) |
| I-10 | Implement Q6 extras: scope `uv run pytest` to the task's touched files via affected | test selection, planning | `skills/sc-implement-protocol/SKILL.md` (:121, Q6 :129-146) | `git diff --name-only "$start" -- <touched> \| codegraph affected --stdin --json` | Cheapest-command-scoped-to-task rule (SKILL :146) gets a real derivation instead of filename guessing; `unrelated-red` classification becomes path-exact | S | Same empty-result rule as I-09; extras are never the gate (unchanged) | Current detection heuristics in the Extras table |
| I-11 | Workflow/tasklist structural risk note per task | planning, impact before edits | `skills/sc-workflow-protocol/SKILL.md`, `skills/sc-tasklist-protocol/SKILL.md` | planning Bash is available (:4 allowlist includes Bash): `codegraph impact <symbol> --depth 1` for tasks that rename/delete a named symbol; record `affects_n_callers` in the task's risk field | Plans stop proposing blind renames; the tasklist carries a measured blast radius the implementer and reviewer both see | M | Planner runs pre-implementation on symbols that may not exist yet — no-match is recorded, not treated as zero | No risk note (today); risk field stays qualitative |
| I-12 | index-repo: graph-derived metadata sections | onboarding, token cost | `commands/index-repo.md` (:12-19, :72) | `codegraph status` (counts, languages, node kinds) + `codegraph_files {format:"tree"}` + `codegraph query <entry> --json --limit 1` for entry points | Phase-2 metadata (entry points, API surface, key modules) from the index instead of Read-ing files; keeps the 58K→3K claim honest | M | Uninitialized repo → whole addition skipped; status text output has no documented JSON form (UNVERIFIED) — parse loosely or omit counts | The existing 5 parallel Globs (unchanged floor) |
| I-13 | explain: precise who-calls/what-does-X-call answers | onboarding, citation accuracy | `commands/explain.md` (:6, :48) | `codegraph callers/callees <symbol>` then mandatory re-Read of each cited line | "Who calls X" answered by enumeration instead of a Read/Grep tour; accuracy of the answer goes up and tokens down | S | Same definition-line caveat; ambiguous names need a `file` pin | Read/Grep/Glob (current) |

## 4. Ranked list

Method: **risk-discounted value/effort**, with an explicit bonus for being a prerequisite of other ideas and a penalty for depending on an unowned blocker. Value = measured delta (tokens, correctness of scope, citation integrity) from EVAL §5; effort from the S/M/L above; risk discount for blocker dependence and contract-change coordination.

1. **I-01 shared contract** — S effort, de-risks all 12 others; without it every idea re-invents its own degradation prose and drift is guaranteed.
2. **I-09 pr-submit affected test selection** — small effort, CLI-only (no blocker), converts a heuristic gate into a derived, logged one; direct fault-tolerance win for the push pipeline.
3. **I-02 troubleshoot Tier-1 grounding** — S effort, the load-bearing SYM rows keep a cheap grounding path and the existing fail-open exit criteria already accept the fallback.
4. **I-04 reflect touched-symbol derivation** — heaviest Serena consumer (6 LB SYM rows); M effort justified by removing the densest dependency; ambiguity handled by file-pinning.
5. **I-10 implement Q6 test scoping** — S effort, reuses I-09's mechanism and output contract verbatim; marginal cost near zero after I-09.
6. **I-05 reflect overlap shared-vs-collision** — pairs with I-04; ranked below it only because it changes the severity-rule wording (caller count vs call-site count), which needs reflect-CLI-owner coordination.
7. **I-11 workflow structural risk note** — cheap, novel capability (plans currently have no impact step at all); ranked mid because its value is preventive, not measured.
8. **I-03 troubleshoot Wave 1.6 callers list** — S effort, real but narrow; auggie+Grep already answers it adequately.
9. **I-08 auggie-review blast radius** — M effort, indirect value (context, not evidence); capped usefulness on small diffs.
10. **I-13 explain callers/callees** — S effort, user-facing nicety; no pipeline depends on it.
11. **I-07 cleanup-audit DELETE corroboration** — M effort, corroboration-only by design (cannot raise the bar's strength), so its value is bounded; still worth doing for the false-DELETE tail.
12. **I-06 reuse-auditor fallback tier** — real but hard-blocked on the listing env; ships as its own fallback until the installer changes.
13. **I-12 index-repo graph sections** — lowest: UNVERIFIED machine-readable status output, and the current Glob flow already meets its token claim.

Sequencing note: I-01 first (NFR-07), then the two unblocked pipeline wins (I-09, I-10) and the low-risk grounding swaps (I-02, I-04, I-05), then the context-layer additions (I-11, I-08, I-03, I-13, I-07), with I-06 and I-12 last since both wait on external owners.

## 5. Dropped ideas

- **`codegraph_explore` as a default grounding step** (troubleshoot Tier 1, explain, onboarding): one measured call returned 24,913 characters (~6K tokens) and pulled two unrelated `install` functions (EVAL §5.6). Against free server-side auggie plus targeted Read, it is a net token loss except for single-symbol queries with `maxFiles ≤ 5`; that narrow case is folded into the contract (FR-08) rather than made an idea.
- **`codegraph_node` file mode as a Read replacement anywhere**: the freshness system keys on the Read tool (`hooks/scripts/freshness-post-read.sh` matcher is `Read`); substituting node file mode would silently bypass edit-freshness gating and the evidence re-Read discipline. Read stays the only citation-grade file accessor.
- **Rewriting `/sc:load` around codegraph**: load is memory/activation (MEM/ACT jobs, INV §4); codegraph has no memories and no activation concept (EVAL §6.2). Its replacement is a native-file store decision, not a graph decision.
- **Giving the evidence-validator codegraph tools**: its job is verifying cited `file:line` against disk — exactly Read. Adding a second, unverified source to the independent last gate would weaken it, not strengthen it.
- **Adopting `prompt-hook` or `codegraph install`**: both rejected upstream pieces (EVAL §5.9, §7); prompt-hook injects an explore payload into every prompt and `codegraph install`'s CLAUDE.md block is erased by `superclaude install`.
- **Any primitive running `codegraph sync`**: fails on the writer lock while a daemon runs (EVAL §5.7); the daemon owns sync. Primitives read status, they never repair the index.
- **Replacing cleanup-audit's grep-proof DELETE gate with `impact == 0`**: the graph is call edges only; imports, strings, config and dynamic references are invisible. Graph can add evidence, never replace the gate (inverse of I-07).
- **Direct SQLite queries against `.codegraph/codegraph.db`**: schema UNVERIFIED and explicitly out of bounds (seed constraint).
- **`codegraph context <task…>` as a planning input**: listed in the CLI surface but its behavior is undocumented in EVAL; no claim may rest on it.
- **codegraph-based test selection for cleanup-audit's `/dev` verification**: the audit is read-only by charter (`READ-ONLY AUDIT — NO REPOSITORY MODIFICATIONS`) and runs no tests; adding a test-run path would change its charter for marginal value.
- **Graph-derived entry-point/route discovery for `sc-recommend` routing**: `codegraph_search {kind:"route"}` exists but IronClaude primitives are markdown, not routed code; the recommendation router's question is about work intent, not call topology.
- **Splitting `/sc:impact` and `/sc:test-scope` into per-skill private scripts**: the whole point of C-2/C-3 is one contract with one fallback map; six private copies would recreate the drift I-01 exists to remove (open question 7 keeps a future merge on the table).

## 6. Candidate new commands or skills

| # | Name | Kind | Purpose | Interface | Called by | codegraph tools | Fallback | Effort |
|---|---|---|---|---|---|---|---|---|
| C-1 | `sc-graph-protocol` (skill, with `refs/codegraph-contract.md`) | skill | The single contract every consumer loads: status probe recipe, CLI-vs-MCP selection table, degraded-value vocabulary, definition-line/re-Read rules, fallback map, explore budget | Skill invocation `> Skill sc-graph-protocol` (no args); ref is pure guidance, no output of its own; defines the shared `graph: {available, worktree, stale}` degraded keys consumers copy into their contracts | sc-troubleshoot, sc-reflect, sc-cleanup-audit, sc-auggie-review, sc-implement, sc-workflow, /sc:impact, /sc:test-scope | `codegraph status` / `codegraph_status` only | Consumers' existing named fallbacks | S |
| C-2 | `/sc:impact` | command | Operator- and planner-facing blast radius for one symbol or file: definition, callers, callees, inbound impact depth 2, affected tests | args: `<symbol> [--file <path>] [--depth 1-3] [--tests]`; output contract fields: `{symbol, resolved: bool, definition: file:line, callers: [{name, file:line, verified: bool}], caller_count, total_count, impact: [...], tests: [paths], graph: degraded-keys[]}`; every `file:line` re-Read before emission, `verified: false` rows dropped | sc-workflow (I-11 risk note), sc-implement (pre-edit check), sc-troubleshoot (Tier 1/1.6), direct operator use | `codegraph query`, `callers`, `callees`, `impact --depth`, `affected --stdin --json` (CLI) | Grep for call sites; Read for the definition; `graph: unavailable` + empty result sets | M |
| C-3 | `/sc:test-scope` | command | Derive the test command for a change set: changed files → affected test files → pytest invocation, with an explicit provenance field | args: `[--base <ref>] [--files <paths...>] [--stdin]`; output contract: `{tests: [repo-relative paths], command: string, source: graph\|heuristic\|none, degraded: []}`; `source: none` + non-empty src diff → caller must escalate, never skip | sc-pr-submit VG-1 (I-09), sc-implement Q6 (I-10), operator | `codegraph affected --stdin --json --quiet` (CLI-only subcommand) | Path-heuristic test selection (current behavior, `source: heuristic`) | S |
| C-4 | `/sc:ground` | command | Ground a structural claim set: given symbol/file claims, return verified `file:line` citations — graph locates, Read verifies, unverified rows are returned as dropped with reasons | args: `<claims...> [--json]`; output: `{grounded: [{claim, ref: file:line, snippet}], dropped: [{claim, reason: no_match\|unverified\|ambiguous}], graph: degraded-keys[]}` | sc-troubleshoot (Tier-1 exit criteria), sc-reflect (hallucination contract :42), /sc:explain, /sc:impact (internal) | `codegraph search`, `node {symbol}`, `query --json` | Grep+Glob resolution with `graph: unavailable`; identical output shape | S-M |

All four respect the installed-path rule: they reference the skill/command by name and look up peers via the dual-surface rule (project `.claude/` first, then `~/.claude/`), never a `src/superclaude/...` path.

**Composition.** C-1 is guidance only (no graph calls beyond the probe). C-2 and C-3 are the only two places that translate graph rows into operator-facing artifacts; C-4 is the shared verify layer both of them call internally, which is what keeps FR-03 enforceable in one place rather than four. Callers adopt them by name, so a fix to the contract (say, a new degraded key for the nested-worktree warning) lands once and every consumer inherits it on its next run — the same property that motivates I-01.

## 7. Requirements

Binding inputs to these requirements: EVAL (ground truth), INV §1/§4 (load-bearing rows), the seed brief's fail-open, citation and installed-path constraints, and the enrichment observations (Bash-capable vs read-only split; every target primitive already has a degraded/fallback vocabulary).

Functional:

- **FR-01** Every primitive step that names a codegraph tool MUST, in the same step, (a) name its native fallback and (b) name the degraded-value key it records (e.g. `degraded: ["grounding:codegraph_uninitialized"]`). Test: grep each edited primitive for `codegraph` — every hit line is within N lines of a fallback name and a `degraded` key.
- **FR-02** One status probe per run, before the first graph call: `codegraph status` (CLI) or `codegraph_status` (MCP). "Not initialized" and "index belongs to a different git working tree" both map to `graph: unavailable` for the whole run; the run then uses fallbacks exclusively and never retries the probe. Test: reading the primitive shows exactly one probe step and a run-scoped latch.
- **FR-03** Citation integrity: no `file:line` originating from codegraph output may appear in a report, return contract, or tasklist without a Read of that exact line in the same run. Caller rows additionally never present the definition line as a call site. Test: spot-check audit logs — every graph-sourced citation has a matching Read in the log.
- **FR-04** Caller semantics: `callers` output is used only as caller *identity* and *count*; locating the call site is an explicit Grep step in the consuming primitive. Test: primitives that consume callers contain the Grep step.
- **FR-05** `/sc:test-scope` contract: on `source: graph`, `tests` is exactly the parsed `affected --json` list; empty `tests` with a non-empty source-file diff forces `source: heuristic` (never a silent empty test run); the chosen `command` string is recorded verbatim by the caller (pr-submit run-log, implement ledger `test=` row). Test: contract fixture cases for graph-hit, graph-empty, graph-unavailable.
- **FR-06** Mutation exclusion: no primitive text contains `codegraph init`, `codegraph index`, `codegraph sync`, `codegraph uninit`, `codegraph unlock`, `codegraph upgrade`, or `codegraph install`. Test: `grep -rnE 'codegraph (init|index|sync|uninit|unlock|upgrade|install)' src/superclaude/{skills,commands,agents,core,hooks}` returns 0 hits.
- **FR-07** Idempotency: every codegraph call site is a read that may be re-run with identical results within a run; graph outputs are cached per run (one affected computation per validation cycle; one callers list per symbol per wave). Test: re-running a wave produces no duplicate graph calls in the audit log.
- **FR-08** Explore budget: `codegraph_explore` appears only with `maxFiles` between 1 and 5 and a single-symbol query; it is never a default grounding step. Test: grep for `codegraph_explore` — every hit shows a bounded `maxFiles`.
- **FR-09** Read-only agents gain `mcp__codegraph__*` names in `tools:` only when their body actually calls them, and each such addition ships together with the parent-side CLI alternative for environments where the tools are unlisted. Test: agent allowlist diff matches body call sites one-to-one.
- **FR-10** Allowlist plumbing: cleanup-audit (and any other enumerating allowlist) adds explicit `Bash(codegraph status *)`, `Bash(codegraph callers *)`, `Bash(codegraph impact *)`, `Bash(codegraph query *)`, `Bash(codegraph affected *)` patterns — no bare `Bash(codegraph *)` beyond the read-only five. Test: allowlist diff shows only those five verbs.

Non-functional:

- **NFR-01** Fail-open: codegraph absent, uninitialized, stale, or unlisted never changes a run's terminal status; the only observable effect is a degraded-value entry and the fallback path. Test: dry-run each edited primitive with the tool unavailable — outcome equals today's.
- **NFR-02** Token budget: Tier-1 troubleshoot keeps its ≤2k-token budget; no graph output block may exceed ~1k tokens (explore effectively banned per FR-08; callers lists capped at 20). Test: budget lines unchanged in the skill text; caps present at each call site.
- **NFR-03** Installed-path rule: no `src/superclaude/` path in any new or edited primitive; peer lookups use the dual-surface rule. Test: existing `grep -rn 'src/superclaude'` pre-commit check stays clean.
- **NFR-04** Additive contracts: new return-contract keys (`graph:`, `degraded:` entries) are additive; `contract_version` bumps are minor; existing consumers reading prior fields are unaffected. Test: reflect/pr-submit contract fixtures unchanged for legacy fields.
- **NFR-05** Rollback: deleting every codegraph step and name from a primitive must leave it fully functional on its fallback path with no dangling references. Test: revert-diff review per primitive; no orphaned `graph:` keys in required (non-degraded) positions.
- **NFR-06** Observability: each run records probe outcome, per-call latencies where cheap to note, and degraded keys in its existing audit log / run-log; no new telemetry channel. Test: audit-log schema check lists the `graph:` block.
- **NFR-07** Rollout ordering: I-01 (contract) lands before any consumer idea; blocked ideas (I-06) land as fallback-plus-degraded-key only, activated when the listing env ships. Test: commit order in the migration branch.

## 8. Risks, invariants and edge cases

- **Stale index**: the watcher runs only while an MCP client is connected; edits made between sessions are caught up at connect time via `(size, mtime)` + hash (EVAL §4). Invariant: FR-03's re-Read makes stale rows harmless — a stale `file:line` fails re-Read and is dropped, never silently cited. A stale *count* (caller_count) can still skew reflect severity; mitigate by recording `graph.stale: true` when status shows pending files and letting reflect treat HIGH as MEDIUM when stale.
- **Uninitialized sibling worktree** (the standard IronClaude layout): every graph call fails "not initialized". Invariant: FR-02's run-scoped latch — one probe, then fallbacks; the run never nags. Do not auto-run `init` (FR-06): index creation is a user/installer decision with disk cost (~70 KB/file).
- **Nested worktree answered from the parent index with a warning**: this is the dangerous case — results *look* local but describe another tree. Invariant: the probe treats the "different git working tree" warning as `graph: unavailable`, full stop; no partial trust.
- **Empty results**: zero callers ≠ zero references (call edges only; imports/strings/config invisible). Invariant: empty graph results never weaken a safety gate (cleanup-audit DELETE stays grep-gated; VG-1 never skips to "no tests" — FR-05).
- **Ambiguous symbols**: `node` returns every overload; `search` matches by partial name with no regex. Invariant: consumers pin with `file` (callers/node accept it); unresolved ambiguity is recorded as `dropped: ambiguous`, not guessed.
- **Explore noise and size**: 24,913-character responses with unrelated symbol matches are the documented failure mode. Invariant: FR-08; consumers prefer `search`+`node`+`callers` composition over `explore`.
- **Writer lock / daemon**: `sync` fails while a daemon holds the lock; a daemon may outlive the client up to its 300 s idle timeout. Invariant: FR-06 — primitives never sync; staleness is read, not repaired.
- **Single-maintainer upstream, pinned version**: behavior changes across releases are unreviewable by us at scale. Invariant: all claims pinned to EVAL against v1.6.2; the installer owns the version gate; primitives never assume a version or feature-detect beyond the status probe.
- **Rollback**: NFR-05 — every idea is additive guidance with its fallback intact; removing codegraph text restores today's behavior byte-for-byte on the fallback path.
- **Repo hygiene**: `init` writes a self-ignoring `.codegraph/.gitignore`, so only `.codegraph/.gitignore` shows untracked — acceptable; no primitive edits `.gitignore` for it.

Edge cases the contract must name explicitly (each maps to a probe outcome or a FR above):

| Edge case | Observed behavior (EVAL) | Contract response |
|---|---|---|
| Worktree sibling, no init | `status` → "⚠ Not initialized" | `graph: unavailable`, latch, fallback path, degraded key recorded |
| Nested worktree, no init | answered from parent index **with warning** | `graph: unavailable` — the warning is treated as a hard no, because rows describe another tree's line numbers |
| Daemon holds writer lock | `sync` fails with "database is locked by another process (PID …)" | Never called by primitives (FR-06); nothing to handle |
| Symbol exists in tests and src (e.g. `install`) | explore pulled `eval/signal_handler.py` and `cleanup_audit/process.py` unrelated matches | Pin with `file`; ambiguity → `dropped: ambiguous` (FR-04 companion) |
| Caller list truncated ("Showing 20 of 23") | callers caps at 100; CLI defaults to 20 with a `pass --limit to widen` hint | Record `total_count` separately from the returned rows; consumers display the truncation, never present 20 as the whole set |
| Diff touches only non-code files (docs/config) | `affected` has no symbols to map | `tests: []` is legitimate here; FR-05's escalation rule keys on *source-file* diffs, so a docs-only diff may honestly yield no tests |
| Sub-300ms budget-sensitive call sites | CLI ~290-300 ms vs MCP 3-15 ms | Orchestrator waves use either; per-hunk loops (reflect Step 1B.3 over ≥3 tasks × hunks) prefer MCP when listed, else batch CLI calls and accept the latency |
| First call after connect on a repo edited while no server ran | connect-time `(size, mtime)` + hash catch-up | Treat the first status probe as authoritative for the run; if it reports pending, set `stale: true` rather than waiting |

## 9. Open questions

1. Does the installer phase set `CODEGRAPH_MCP_TOOLS` in the registration env (EVAL §7 step 5 currently omits it)? This single env var gates I-06 and all read-only-agent value; who owns the decision — installer phase or this migration?
2. Who owns per-worktree `codegraph init` (Coder template hook vs git post-checkout vs manual)? Until owned, FR-02's latch is the whole story in worktrees — is that acceptable long-term for reflect, whose heaviest consumer base runs in worktrees?
3. Will the reflect severity rule accept *caller count* as the proxy for *call-site count* (I-05), and does that require a reflect CLI owner coordination bump beyond a text edit?
4. Is there a machine-readable `codegraph status` (JSON flag undocumented in EVAL)? If yes, I-12's index-repo sections get cheaper and the FR-02 probe gets a parseable latch source.
5. Does `codegraph affected` scale and stay correct on repos far larger than the 500-file sample, and is its test-file mapping convention (path/name matching) stable enough to bind VG-1 to it?
6. Plugin mirror (`plugins/superclaude/`) — which of these edits must be mirrored there, and does `test_routing_plugin_parity.py` or the HOW-WE-WORK byte-copy rule pull in any of the new primitives (C-1 in particular)?
7. Should `/sc:impact` and `/sc:test-scope` eventually merge (one command, `--tests` mode), or stay separate because their callers (planner vs push pipeline) need different output contracts?
8. Should the `graph:` degraded keys live inside each skill's existing `degraded_components`-style list (reflect already has one, INV CONTRACT job) rather than a new top-level field, so downstream parsers need no change?
