---
variant: 2
persona: analyzer
type: spec
topic: p3-codegraph-opportunities
source_brief: .dev/codegraph-migration/brainstorm/P3-codegraph-opportunities/seed-brief.md
generated: 2026-10-29
---

# Variant 2 (analyzer): where beyond 1:1 Serena replacement should IronClaude use codegraph v1.6.2

Notation. EVAL = `.dev/codegraph-migration/research/codegraph-evaluation.md`. INV = `.dev/codegraph-migration/inventory/primitive-usage.md`. Primitive paths are relative to `src/superclaude/` and I cite `path:line` only for lines I read. "UNVERIFIED" means EVAL did not measure it. Value classes used for ranking: **M** = measured gap and measured mechanism; **P** = gap shown in primitive text, mechanism measured, benefit size unmeasured (spike-gated); **A** = benefit rests on an unmeasured codegraph behaviour (dropped).

## 1. Summary

- **Root cause split.** codegraph answers "which symbols/files/tests are connected" (callers, impact, affected: set membership). It cannot answer "where exactly" (caller rows give the caller's definition line, `main.py:46` not `:255`, EVAL §5.5) or "is there none" (no text search, no dynamic/string refs, EVAL §6.1). Every adopted idea therefore uses the graph for scoping and leads, uses Read for any cited line, and never lets an empty result convict (FR-06, FR-07).
- **Access model: CLI-first, orchestrator-computed artifacts, pasted or path-referenced into read-only agent briefs.** The repo already works this way (`skills/sc-troubleshoot-protocol/SKILL.md:281` pastes the producers table into every brief; `skills/sc-reflect-protocol/SKILL.md:355` has reviewers audit only pre-computed hunks). This removes the `CODEGRAPH_MCP_TOOLS` blocker for agents, avoids MCP schema overhead (size UNVERIFIED), and works where MCP is unavailable (`skills/sc-cleanup-audit-protocol/SKILL.md:86`). Allowlists must be per-subcommand: the CLI includes `install`, `uninstall`, `upgrade`, `unlock`, `telemetry` (EVAL §3) while every MCP tool is read-only.
- **Top ranked:** I-01 readiness/provenance probe (enabler), I-02 call-site resolver plus citation contract (enabler, restores what the 1:1 swap loses), I-03 routing and token guard (explore ban in budgeted waves), I-05 reflect parity-plus (prod-only caller counts), I-04 blast-radius artifact for review scoping.
- **Parity hazard the 1:1 plan misses.** Replacing `find_referencing_symbols` with callers loses the per-reference snippet and, in the one measured sample (23 callers reported), only 2 were production callers (`install_mcp_server`, `install`) and the rest were test functions. Reflect's severity rule "HIGH if >5 referencing call sites" (`skills/sc-reflect-protocol/SKILL.md:347`) would trip on tests alone.
- **Token cost is a regression risk, not a saving, for `explore`.** One `codegraph_explore` returned 24,913 characters (about 6K tokens at 4 chars/token, an estimate) against a Tier 1 budget of about 3K Claude tokens (`skills/sc-troubleshoot-protocol/SKILL.md:218`). Auggie's value here is free server-side retrieval; codegraph output lands in Claude context. Use targeted callers, never explore, inside budgeted waves.
- **Test selection (`affected`) was never run in EVAL.** Ship it advisory-only (print the delta against `<changed-area>`), union into VG-1 only after a backtest passes (NFR-08). It can add tests, never remove them.
- **Dropped:** cleanup-audit graph DELETE check, tasklist, workflow touch-set preview, reuse-auditor co-caller search, hook-based impact gate or init, `explore` as Tier 1 replacement, `node` file mode as Read replacement (12 drops, section 5).
- **Three candidates:** `sc-codegraph-probe` (skill, bundles citation contract and call-site script), `sc-blast-radius` (skill and `/sc:blast-radius`), `sc-structure-brief` (skill). Each has a named fallback and no `src/superclaude` path.

## 2. Access model and prerequisites

### 2.1 Access path per primitive class

| Primitive class | Evidence of current tools | Default path | Why |
|---|---|---|---|
| Orchestrator skills with Bash: troubleshoot, reflect, tasklist, workflow, implement | troubleshoot `:4` has Bash; reflect `:5` lists Bash; workflow `:4`, implement `:4`, tasklist `:6` list Bash | CLI via Bash, narrow patterns, writes an artifact | 290-300 ms per CLI call (EVAL §5.5) is irrelevant at 30-60 calls; no listing blocker |
| Orchestrators with a closed Bash set: pr-submit, auggie-review, cleanup-audit | pr-submit `:4` `Bash(gh *) git uv make jq`; auggie-review `:4` `Bash(auggie *) gh git jq ...`; cleanup-audit `:8` `Bash(git *) wc find du` | Add per-subcommand patterns, e.g. `Bash(codegraph callers *)`; never `Bash(codegraph *)` | Wildcard would pre-approve `install`/`upgrade`/`uninit`/`unlock`/`telemetry` (EVAL §3, §2: `install` edits Claude config) |
| Read-only agents: reflect-reviewer, troubleshoot-analyst, reuse-auditor, evidence-validator, audit-* | `tools:` lines at `agents/*.md:4-5`, no Bash; reflect `:658` forbids Bash/Edit/Write/Task for reviewers | Artifact in brief (path to a file the agent Reads) | Same pattern as the producers table; agents need no `mcp__codegraph__*` names |
| evidence-validator | `agents/evidence-validator.md:5` = `Read, Grep, Glob` | None. Must stay Read-only | Its independence is the citation gate (FR-06) |
| Interactive commands: explain, index-repo, load | no `allowed-tools` field in the three files I read | CLI for briefs; MCP `explore` is allowed here only (FR-10) | One user-driven call, budget is the user's |
| Hooks | `hooks/hooks.json:47-70` | No change (D-03, D-04) | `freshness-pre-edit.sh` timeout is 1 s (`hooks.json:52`) |

MCP's remaining role is installer-owned: a connected server starts the shared daemon and watcher that keep the index fresh (EVAL §4, §5.7). In CLI-only sessions (headless workers, sprint runs) nothing watches, so the probe must check freshness every time (I-01).

### 2.2 Blockers and owners

| # | Blocker | Evidence | Owner | This spec's stance |
|---|---|---|---|---|
| B1 | Only `codegraph_explore` is listed; the other 7 need `CODEGRAPH_MCP_TOOLS` in the server env; planned registration sets only telemetry and update-check vars (EVAL §3, §7 step 5) | Claude Code can only call listed tools | Installer phase (Phase 2) | Do not set it in v1. If an interactive need is later proven, set `env.CODEGRAPH_MCP_TOOLS=explore,node,search,callers,impact,status` in the `add-json` (drop `callees`, `files`: Glob and CLI cover them). Measure schema overhead first (NFR-06) |
| B2 | Per-worktree init has no owner; sibling worktree is "not initialized", nested worktree answers from the parent with a warning (EVAL §4, §5.8) | This worktree layout is sibling (`~/workspaces/worktrees/...`) | Coder template or git `post-checkout` (EVAL §4); primitive-level fallback `/sc:load --index` (I-09) | Probe never inits; state `uninitialized` or `foreign-index` degrades (FR-03) |
| B3 | Freshness and lock: `codegraph sync` fails on the writer lock while a daemon runs (EVAL §5.7); watcher debounce 2000 ms; only runs with an MCP client | Measured | Probe skill | No primitive calls `sync`; probe reads `status` and flags pending files (FR-05) |
| B4 | Caller rows cite the definition line (EVAL §5.5) | Measured | I-02 | Leads only until resolved and Read (FR-06) |
| B5 | Caller list truncates at 20 by default (EVAL §5.5: "Showing 20 of 23"; MCP limit max 100) | Measured | Blast-radius skill | Record shown/total (FR-08) |
| B6 | Allowlist edits in 8+ primitives | section 3 targets | Phase 3 authors | Per-subcommand patterns (FR-04) |
| B7 | Text output has no documented `--json` for `callers`/`impact`/`status`; only `query` and `affected` list `--json` (EVAL §3) | EVAL §3 | Probe and blast-radius parsers | Golden fixtures plus `parse_failed` degrade (NFR-04) |
| B8 | Version pin and drift | EVAL §7 | `superclaude doctor` | Probe records version only (NFR-09) |

## 3. Ideas

Effort S/M/L. Risk L/M/H. Fallbacks are the primitive's own native path (Read/Grep/Glob, auggie) plus a `degraded` entry.

| ID | Idea | Vector(s) | Target primitive(s) | codegraph mechanism | Expected value (evidence) | Eff | Risk | Native fallback |
|---|---|---|---|---|---|---|---|---|
| I-01 | Readiness, provenance and freshness probe shared by all consumers; returns `ready/stale/uninitialized/foreign-index/absent/error` | citation accuracy, all | new `skills/sc-codegraph-probe/SKILL.md`; one Step-0 line in each consumer | `codegraph version`; `codegraph status` (parse "Not initialized", "different git working tree", "Index is up to date", pending list); compare `git rev-parse --show-toplevel` to the reported index root | Class M. Prevents silent answers from another checkout (EVAL §5.8 nested warning), stale reads in CLI-only runs (§5.7), and a repeat of the Auggie stale-index fabrication lesson (`skills/sc-auggie-review-protocol/SKILL.md:189`) | M | L | `state=absent`, `degraded: [codegraph:<state>]`, continue natively |
| I-02 | Call-site resolver and graph-lead citation contract | citation accuracy, reflect, troubleshoot | `skills/sc-codegraph-probe/refs/citation-contract.md` and `scripts/resolve-callsite.sh`; referenced from `skills/sc-reflect-protocol/SKILL.md:42`, `skills/sc-troubleshoot-protocol/SKILL.md` Wave 5, `skills/sc-auggie-review-protocol/SKILL.md:216-219`, `agents/reuse-auditor.md:132` | `codegraph query <caller> --json --limit 5` gives `startLine`/`endLine` (measured, EVAL §5.5); Grep `-n '\bCALLEE\b'` on that file filtered to the span; then Read | Class M. Closes the measured gap (`main.py:46` vs `:255`). Also restores the call-site snippet Serena `find_referencing_symbols` returned, which the 1:1 swap drops (EVAL §6.2: "no per-reference snippet") | S | M (aliases, attribute calls, strings: hence mandatory Read) | Grep the callee name across the file, Read |
| I-03 | Routing and token guard: CLI-first artifact passing, per-subcommand allowlists, `explore` banned in budgeted waves and subagents, 12-line routing block in core guidance | token cost, safety | `core/CLAUDE.md` (routing block, W4 step 6), `skills/sc-troubleshoot-protocol/SKILL.md:218` and `commands/troubleshoot.md`, allowlist lines of consumers | Policy; when `explore` is used interactively, `maxFiles` 5 or less (parameter exists, 1-20, EVAL §3) | Class M. Explore = 24,913 chars and pulled 2 unrelated `install` functions (EVAL §5.6) vs a 3K-token Wave 1 budget. Block is loaded every session, so size is itself a cost | S | L | Existing auggie/Grep routing |
| I-04 | Blast-radius artifact for review scoping, plus a `dependent-impact` finding class | review scoping, impact | `skills/sc-auggie-review-protocol/SKILL.md` Wave 1 (new step after `:126-138`) and Wave 3 (`:216-219`), its `refs/auggie-prompts.md`; reused by `skills/sc-pr-submit-protocol/SKILL.md` Wave 3 context | Changed symbols from `diff.patch` hunks, then `codegraph callers <sym> --limit 100`, `codegraph impact <sym> --depth 2`, partition prod/test | Class P. Wave 1 chunks by directory (`:135-138`) so cross-directory callers are invisible per chunk, and Wave 3 drops or downgrades findings outside diff hunks (`:218`), so a broken caller can never surface today. Benefit size UNVERIFIED | M | M (prompt bloat; Python-regex symbol extraction is best-effort) | Files-only scope from `git diff --name-only`; `unmapped_files[]` recorded |
| I-05 | Reflect parity-plus: prod-only caller counts for severity and runtime-surface sweep, `impact --depth 2` for top-30 hotspots | reflection, citation accuracy | `skills/sc-reflect-protocol/SKILL.md` Step 1B.3 (`:338-349`) and chain 4/4b (`:514-516`), `skills/sc-reflect-protocol/refs/runtime-surface.md` (reuse its prod/test table `:25-28`) | `codegraph callers <sym> --limit 100`; `codegraph impact <sym> --depth 2`; partition by the existing runtime-surface test globs | Class M for the hazard (2 production callers among 23 reported, one sample); P for benefit. Without it the 1:1 swap inflates severity (`:347`) | M | M (2045-line skill, CLI-parsed contract; v1 adds no fields, only `degraded_components` entries) | Grep-based referrer sweep already in 4b |
| I-06 | Troubleshoot Tier 1 structural grounding: frame to enclosing symbol to immediate callers, artifact `tier1-callers.md` pasted into Wave 1.6 Branch A | troubleshooting | `skills/sc-troubleshoot-protocol/SKILL.md` Wave 1 step 1 (`:191-194`), exit criteria (`:216`), S1.6.2 Branch A (`:286`); `commands/troubleshoot.md:88-96` | `codegraph query <symbol> --json`; `codegraph callers <symbol> --limit 20` for the failing component (cap 40 rows) | Class P. Branch A's "failing_component and immediate callers" is auggie/Grep today (`:286`); callers take 3-15 ms over MCP and about 300 ms CLI. Benefit on diagnosis quality UNVERIFIED | M | L | Glob/Grep fallback already accepted (`:194`, `:216`) |
| I-07 | Implement: untouched-dependents advisory block in the reviewer package | impact before verdict | `skills/sc-implement-protocol/SKILL.md` Q2/Q3 (`:120-123`), `skills/sc-implement-protocol/refs/qa.md` (package definition `:9`) | After Q1: changed symbols to `codegraph callers`; keep prod callers whose files are outside the touched set | Class P. QA input is the task brief and the diff only (`refs/qa.md:9`), so signature changes cannot be judged against callers. Benefit UNVERIFIED | M | M (QA scope creep; block is context-only) | No block; review unchanged |
| I-08 | Test selection: `affected` as advisory delta, later a union into VG-1 and implement extras | test selection | `skills/sc-pr-submit-protocol/SKILL.md:206-207` (VG-1/VG-2), `:4`; `skills/sc-implement-protocol/SKILL.md:129,144` (Q6 extras) | `codegraph affected <files…> --depth 2 --json --quiet` (files from `git diff --name-only`, passed as args or `--stdin` from a file) | Class P-minus. `affected` returns test files only (EVAL §6.1) and was not run in EVAL (UNVERIFIED accuracy, exit codes, output size). Union can only add tests | S advisory, M union | M (runaway set; false confidence) | `uv run pytest <changed-area>` then VG-2 `make test` as today |
| I-09 | `/sc:load --index`: the only primitive that may run `codegraph init --yes`; plus `status` in `--analyze` | onboarding | `commands/load.md` (`:6`, `:27-43`; file is Serena-based and is rewritten by Phase 3 anyway) | `codegraph init --yes` (4.5 s, about 34 MB for 500 files, peak about 1 GB RSS, EVAL §5.4); `codegraph init -i` for a nested worktree (EVAL §5.8 warning text) | Class P. Gives B2 a primitive-level owner outside Coder. Cost measured, frequency of need UNVERIFIED | S | M (mutating step in a context command; explicit flag only) | Print the exact `codegraph init --yes` line for the user |
| I-10 | Structure brief for onboarding: graph-filled Phase 2 of index-repo; relationship grounding for `/sc:explain` on a symbol or file | onboarding, token cost | `commands/index-repo.md` Phase 2 (`:61-68`), `commands/explain.md` (`:46-50`) | `codegraph status` (files by language, node kinds: measured, EVAL §5.4); `codegraph files --format flat` (measured, §5.8); `codegraph callers/callees <symbol>` | Class P. The "58K to 3K" figure in `commands/index-repo.md:13` is the primitive's own unmeasured claim; creation cost and entry-point heuristics (zero-prod-caller symbols) UNVERIFIED | S-M | L | Current 5-Glob flow unchanged |

## 4. Ranked list

Method. Enablers first (every other idea cites them). Then score = V x C / E, where V (1-5) is the structural gap closed, judged from cited primitive text; C is evidence confidence (M=1.0, P=0.6, P-minus=0.3); E is effort weight (S=1, M=2, L=4). Ties: measured hazard first, then measured mechanism, then lower risk. Ideas in class A are not ranked (section 5).

| Rank | ID | V x C / E | Rationale |
|---|---|---|---|
| 1 | I-01 | enabler | Every consumer needs provenance and freshness; failure mode is a silent wrong-checkout answer (EVAL §5.8) |
| 2 | I-02 | enabler | Closes the one measured accuracy gap and restores snippet parity lost by the 1:1 swap |
| 3 | I-03 | 3x1.0/1 = 3.0 | Cheapest, measured: explore size vs stated budgets; also bounds the guidance block that loads every session |
| 4 | I-05 | 4x0.6/2 = 1.2 | Hazard measured (callers are mostly tests); required for a correct 1:1 swap; wins the tie with I-04 on that basis |
| 5 | I-04 | 4x0.6/2 = 1.2 | Real blind spot (chunking plus out-of-hunk rule); benefit unmeasured |
| 6 | I-06 | 3x0.6/2 = 0.9 | Mechanism measured; fits the paste-a-table precedent; wins tie with I-08 on measured mechanism |
| 7 | I-08 | 3x0.3/1 = 0.9 | Advisory stage is nearly free; gate change waits for backtest |
| 8 | I-09 | 2x0.6/2 = 0.6 | Fallback owner for B2; wins tie with I-10 on measured init cost |
| 9 | I-10 | 2x0.3/1 = 0.6 | Token claim unmeasured; low risk |
| 10 | I-07 | 3x0.3/2 = 0.45 | Gap real, benefit speculative, touches QA semantics |

Sequencing: I-01 and I-02 land with or before any consumer; I-03 lands with the first consumer; I-04 and I-05 share `sc-blast-radius` (N-2); I-08 advisory ships with N-2.

Vector coverage check (each of the nine has at least one ranked idea or an explicit drop):

- Token cost: I-03, I-10; D-01. Citation accuracy: I-01, I-02, I-05.
- Impact before edits: I-04, I-07; D-02. Review scoping: I-04 (auggie-review, pr-submit), I-05 (reflect).
- Test selection: I-08. Troubleshooting Tier 1: I-06; D-09.
- Planning and workflow: I-07 (implement); D-06, D-07 (tasklist, workflow).
- Reflection and audit: I-05, I-02; D-05, D-08 (cleanup-audit, reuse-auditor).
- Onboarding: I-09, I-10 (load, index-repo, explain).

## 5. Dropped ideas

| ID | Dropped idea | Reason |
|---|---|---|
| D-01 | `codegraph_explore` as the single Tier 1 grounding call replacing auggie plus Serena | 24,913 chars (EVAL §5.6) against a 3K-token Wave 1 budget (`skills/sc-troubleshoot-protocol/SKILL.md:218`); pulled 2 unrelated functions; auggie offloads cost, explore adds it |
| D-02 | `PreToolUse` hook that runs impact before every Edit | `freshness-pre-edit.sh` has a 1 s timeout (`hooks/hooks.json:52`); CLI query is about 290-300 ms plus process start; a hook cannot know which symbol an Edit changes; fires on every Edit/Write |
| D-03 | `SessionStart` hook that runs `codegraph init` or prints index state | `init` is a 4.5 s, about 1 GB RSS write (EVAL §5.4) inside other projects; a one-line status adds nothing the probe does not already give on demand; more hook failure surface (`hooks/scripts/freshness-session-start.sh` already branches on MCP config at `:135`) |
| D-04 | `prompt-hook` or `codegraph install` guidance | Already rejected: injects an explore payload per prompt (EVAL §5.9); its CLAUDE.md block is erased by `superclaude install` (EVAL §2) |
| D-05 | cleanup-audit graph check on DELETE candidates | Grep sees every static reference the graph sees, so the graph cannot tighten DELETE (`:75`, `:151`); neither sees dynamic loading. Only benefit is reclassifying noisy KEEPs, which "conservative escalation" leaves for humans. The audit is READ-ONLY (`:155`) and `init` writes `.codegraph/`; MCP is unavailable to background subagents (`:86`) |
| D-06 | sc-tasklist-protocol graph input | Deterministic roadmap-to-tasklist generator; its "blast radius" is requirement-level (`skills/sc-tasklist-protocol/SKILL.md:1658,1670`); a live index would break determinism |
| D-07 | Workflow Wave 1 "touch-set preview" (impact and affected for files named in the spec) | Class A: spec text to symbol is a judgement step, named files are often not yet created, and an empty result reads as "no dependents" in a plan that reflect then grades (`skills/sc-workflow-protocol/SKILL.md:58-60`) |
| D-08 | Reuse-auditor co-caller neighbour search (callees of a candidate, then callers of those helpers) | Class A: codegraph callers/callees timing is measured but similarity quality is not; popular helpers add noise; contradicts "do not let names decide" only if misused. Spike instead (OQ-5). 1:1 fallback swap for `find_symbol` stays Phase 3's |
| D-09 | codegraph for troubleshoot producer enumeration (S1.6.0b) | That step is text/token search (`:277`); codegraph has no text search (EVAL §6.1) |
| D-10 | `codegraph_node` file mode as a Read replacement | Token saving unmeasured; breaks the freshness chain (`hooks.json:59` counts only `Read`), so Edit would be blocked or nagged; keep Read |
| D-11 | codegraph tools in evidence-validator `tools:` | Its independence is the gate; graph rows are leads, not evidence (FR-06) |
| D-12 | Direct SQLite queries of `.codegraph/codegraph.db`, or any data-flow/cross-service/Cypher use | Schema UNVERIFIED (EVAL §6.1); no such codegraph capability. Memory/NUDGE/ACT jobs (INV §4) are not graph jobs |

## 6. Candidate new commands or skills

All installed paths use `~/.claude/skills/<name>/...` (project copy `.claude/skills/<name>/...`); no `src/superclaude` path appears in any candidate's text.

### N-1 `sc-codegraph-probe` (skill; no slash command)

- Purpose: single readiness, provenance and freshness check; owns the citation contract and call-site script (I-01, I-02).
- Interface: args `[--project-path <abs>] [--max-pending N]`. Output (YAML in the caller's audit log or return contract): `codegraph_state` (`ready`, `stale`, `uninitialized`, `foreign-index`, `absent`, `error`), `access` (`cli`, `none`), `version`, `worktree_root`, `index_root`, `pending_files` (int or `unknown`), `degraded` (list of `codegraph:<state>`). Bundled: `refs/citation-contract.md`; `scripts/resolve-callsite.sh --caller <name> --callee <name> [--file <path>]` printing `caller_file`, `start`, `end`, and candidate `file:line:text` rows, status always `lead-unverified`.
- Callers: auggie-review (Wave 0), pr-submit (before VG-1), reflect (Wave 0, beside the Serena-removal replacement of Step 0.5c at `skills/sc-reflect-protocol/SKILL.md:252`), troubleshoot (Wave 0 header `mcps_available`, `:168`), implement (Wave 0 step 8, `:67`), load, index-repo, explain, and N-2, N-3.
- Tools: CLI `codegraph version`, `codegraph status`, `codegraph query --json`; `git rev-parse`; Grep/Read.
- Fallback: `codegraph_state=absent` with `degraded`; callers continue natively.
- Effort: M.

### N-2 `sc-blast-radius` (skill plus `/sc:blast-radius`)

- Purpose: given a diff or symbol list, produce the dependents and affected-tests artifact consumed by review, validation, implement and reflect (I-04, I-05, I-07, I-08).
- Interface: `/sc:blast-radius [--base <ref>] [--symbols a,b] [--files f…] [--depth 1..2] [--limit N<=100] [--output <dir>]`. Output `blast-radius.md` with YAML header: `graph_state`, `changed_symbols[]` (`name`, `file`, `start`, `end`, `mapped_by: hunk/name`), `dependents.prod[]` and `dependents.test[]` (`caller`, `file`, `def_line`, `call_site_line` or null, `call_site_status: resolved/unresolved`), `affected_tests[]` or `unknown`, `truncated{symbol: shown/total}`, `ambiguous[]`, `unmapped_files[]`, `degraded[]`. Rows sorted, capped (FR-10).
- Callers: `skills/sc-auggie-review-protocol`, `skills/sc-pr-submit-protocol`, `skills/sc-implement-protocol`, `skills/sc-reflect-protocol` (Step 1B.3 and 4b), humans via the command.
- Tools: CLI `codegraph query --json`, `callers`, `impact`, `affected`; probe; resolver script.
- Fallback: files-only scope from `git diff --name-only`; `affected_tests: unknown`; `degraded` entry.
- Effort: L.

### N-3 `sc-structure-brief` (skill)

- Purpose: graph-filled project or symbol brief for onboarding (I-10), with a status line for `/sc:load --analyze` (I-09).
- Interface: args `[target path or symbol] [--level overview/module/symbol]`. Output `structure-brief.md`: file and language counts, per-module top symbols, for a symbol its prod callers and callees (rows capped), entry-point candidates tagged `heuristic`, `graph_state`.
- Callers: `commands/index-repo.md`, `commands/explain.md`, `commands/load.md`.
- Tools: CLI `codegraph status`, `files --format flat`, `query --json`, `callers`, `callees`; probe.
- Fallback: the existing Glob/Read flow in each command.
- Effort: M.

## 7. Requirements

### Functional

- **FR-01** Each consuming primitive MUST run N-1 once per run before any other codegraph call and log `codegraph_state`, `access`, `degraded`. Test: grep each target for the probe step; a run with `codegraph` off PATH logs `absent`.
- **FR-02** No codegraph step may STOP or fail a run. Every step names a native fallback and records `degraded: [codegraph:<reason>]`.
- **FR-03** Results are used only when `index_root` equals the realpath of the worktree root. The nested-worktree warning ("belongs to a different git working tree", EVAL §5.8) maps to `foreign-index`, handled as `uninitialized`.
- **FR-04** CLI use is limited to `version`, `status`, `query`, `callers`, `callees`, `impact`, `affected`, `files`. Allowlist lines use one pattern per subcommand. `init`, `index`, `sync`, `uninit`, `install`, `uninstall`, `upgrade`, `unlock`, `telemetry` are forbidden in every primitive except `init` in `/sc:load --index` (FR-17).
- **FR-05** If `status` reports pending files or not up to date, results carry `stale: true` and are leads only. No "no dependents/no callers/no tests" conclusion may be drawn from stale, foreign or error states.
- **FR-06** A `file:line` derived from codegraph MUST NOT appear in a report, finding or contract unless re-Read in the same run. Caller rows carry `def_line`; `call_site_line` is set only by the resolver and confirmed by Read. `evidence-validator` keeps `tools: Read, Grep, Glob`.
- **FR-07** Asymmetric evidence: a positive graph result may clear a suspect (a production caller exists); an empty result MUST NOT establish UNREACHED, dead code, DELETE, or "no tests". Reflect's rootwalk before `UNREACHED` (`skills/sc-reflect-protocol/refs/runtime-surface.md:61`) is unchanged.
- **FR-08** Record `shown/total` for every caller list. If `total > shown` and `total <= 100`, re-query once with a wider `--limit`; above 100, set `truncated: true`.
- **FR-09** Prod/test partition uses reflect's runtime-surface table (`skills/sc-reflect-protocol/refs/runtime-surface.md:25-28`) as the single definition; severity thresholds at `skills/sc-reflect-protocol/SKILL.md:347` count distinct production caller symbols only.
- **FR-10** `codegraph_explore`, `codegraph explore` and `codegraph context` are forbidden in troubleshoot Wave 1, in any wave with a budget under 8K tokens, and in every subagent. Interactive use sets `maxFiles` to 5 or less and logs the size. Any artifact pasted into a brief has at most 40 rows and 6 KB.
- **FR-11** In v1 no `tools:` line of a read-only agent gains `mcp__codegraph__*`; agents get artifacts by path.
- **FR-12** auggie-review: when `ready`, Wave 1 writes `inputs/blast-radius.md`; the Auggie prompt receives dependent names and files only. Wave 3 adds finding class `dependent-impact`, exempt from the out-of-hunk downgrade (`:218`) only when its caller call-site line is Read-verified; otherwise it is downgraded as today.
- **FR-13** pr-submit VG-1: advisory stage prints `affected_tests` not covered by `<changed-area>` and leaves the gate unchanged. The union stage is enabled only after NFR-08 passes, never removes tests, and above 200 files escalates to VG-2.
- **FR-14** Reflect: Step 1B.3 and chain 4/4b read prod-only counts from N-2; no new contract field in v1, only `degraded_components` entries `graph:<state>`.
- **FR-15** Troubleshoot Wave 1 writes `tier1-callers.md` when a symbol or frame resolves and `access != none`; Wave 1.6 Branch A briefs paste it; exit criteria accept "graph artifact, or Glob/Grep fallback noted".
- **FR-16** Implement Q2 adds `untouched_dependents` (at most 20 rows, context only) to the reviewer package; it cannot create a blocking finding by itself and does not change touched-file rules.
- **FR-17** `/sc:load --index` is the only primitive path that may run `codegraph init --yes`; it requires the explicit flag, reports time and size, and uses `init -i` for a nested worktree.
- **FR-18** `index-repo` Phase 2 uses N-3 when `ready`, records `graph_state` in `PROJECT_INDEX.md`, and otherwise runs today's flow unchanged.
- **FR-19** No new hooks. Graph output never satisfies freshness-before-edit; `hooks.json:59` stays `Read` only.
- **FR-20** Installed-path rule: no `src/superclaude/...` path in any edited or new primitive; lookups name both `~/.claude/...` and project `.claude/...`.
- **FR-21** The routing block in `core/CLAUDE.md` is at most 12 lines: call-graph question to callers/impact, semantic to auggie, text to Grep; explore rules; fail-open sentence. No `@` import.

### Non-functional

- **NFR-01** Probe p95 under 1 s and a 30-symbol blast-radius under 15 s on a 500-file index (query is 290-300 ms, EVAL §5.5; `status` timing UNVERIFIED, measure).
- **NFR-02** Generated query batches obey `BASH_INSPECTION_POLICY.md`: at most 15 commands per chunk, 30 s aggregate, 100 KiB output, per-command timeout, `BEGIN/OK/NO_MATCH/FAIL` markers. Codegraph mutations are never batched.
- **NFR-03** Same index and inputs give byte-identical artifacts (sorted rows).
- **NFR-04** Parsers tolerate extra lines; golden fixtures of v1.6.2 `status`, `callers`, `impact`, `affected`, `query --json` outputs are tested; a mismatch yields `codegraph:parse_failed`, not an error.
- **NFR-05** Probe and blast-radius write only under the caller's output directory (`git status` unchanged apart from the self-ignored `.codegraph/`).
- **NFR-06** Graph text entering Claude-visible context per orchestrator run is 2K tokens or less (artifacts stay on disk, summaries inline). Measure `alwaysLoad` explore-schema overhead per session before any `CODEGRAPH_MCP_TOOLS` change.
- **NFR-07** With `codegraph` absent, every target primitive's behaviour equals its native fallback path; one test per primitive.
- **NFR-08** `affected` backtest on at least 20 recent merged changes: recall of tests that actually failed or were touched is at least that of `<changed-area>`, and median affected-set is 25 test files or fewer; otherwise stay advisory.
- **NFR-09** Probe records `codegraph --version` and notes a mismatch with the pin; it never blocks (`doctor` owns the gate, EVAL §7).

## 8. Risks, invariants and edge cases

- **Stale index.** Debounce 2000 ms and no watcher without an MCP client (EVAL §4). A PR that adds files can have unindexed symbols: they land in `unmapped_files[]`, and absence of dependents is not reported. Re-run `status` immediately before the queries (I-01), not once per session.
- **Uninitialized or nested worktree.** Sibling worktree: "not initialized" (this checkout is one). Nested: answers come from the parent tree's code. Invariant: `index_root == worktree_root` or the result is discarded (FR-03).
- **Empty results.** Never evidence of absence (FR-07). Report "0 graph callers, state=<s>" and keep the native grep proof where a rule demands it (cleanup-audit `:75`).
- **Ambiguous symbols.** `query` on `install_codebase_memory_mcp` also returned a `variable` whose string matched (EVAL §5.5); `node` returns every overload. Resolve via `query --json` and require a unique kind/file match, else `ambiguous[]` and file-level scope. CLI `callers` has no documented file argument (UNVERIFIED); MCP `callers` does.
- **Caller-count semantics.** Rows are per caller symbol; whether two call sites in one caller give one row or two is UNVERIFIED. Reflect thresholds are restated as "distinct production caller symbols" (FR-09), so the calibration changes from Serena's per-reference counts; flag it in the reflect change note.
- **Explore noise and size.** 24,913 chars and unrelated matches (EVAL §5.6): fenced by FR-10.
- **Output format drift and single-maintainer upstream.** Text outputs can change between releases (30 releases, 8 in about 3 months, EVAL §1). Pin is v1.6.2 (EVAL §7); golden fixtures (NFR-04) catch drift in CI; parse failure degrades rather than errors.
- **Allowlist blast radius.** One broad `Bash(codegraph *)` would pre-approve `install`, which edits `~/.claude` config and adds a prompt hook (EVAL §2, §5.9). Enforced by FR-04.
- **QA and review scope creep.** Dependents are context. Implement's drive-by rule (`skills/sc-implement-protocol/SKILL.md:119`) and auggie-review's out-of-hunk rule keep their meaning except for the single verified class in FR-12.
- **Read-only audits.** `init` writes `.codegraph/` (EVAL §4), so read-only skills (cleanup-audit, reflect, review) must never init; the probe has no init mode.
- **Rollback.** Remove the probe step and the consumer lines, or simply uninstall the binary: FR-02 and NFR-07 make absence equal to today's native path. No contract field is added, so reflect's CLI parser and pr-submit's FSM are untouched.
- **Policy interplay.** Many serial known-target CLI queries fit `BASH_INSPECTION_POLICY.md`; ad hoc loops with command substitution do not and must go through the bundled script (NFR-02).

## 9. Open questions

1. **MCP listing.** Does any interactive flow need MCP `callers`/`impact` at 3-15 ms enough to justify setting `CODEGRAPH_MCP_TOOLS` and paying 7 extra always-loaded schemas (size UNVERIFIED)? Default answer here: no. Owner: installer phase.
2. **`affected` quality.** What are its recall, set size, exit codes and output format on this repo? Needs the NFR-08 backtest before the union stage.
3. **`status` format.** Is there a stable machine-readable form (EVAL §3 lists `--json` only for `query` and `affected`)? Determines parser fragility (B7).
4. **Daemon on init.** After `codegraph init` in a worktree with a live MCP session, does the watcher start for the new index without restart? EVAL §4 says queries are picked up per call, not that the watcher starts (UNVERIFIED).
5. **Reuse-auditor.** Does the co-caller idea (D-08) separate `_bind_specs` from `_inject_*`-style duplicates better than auggie? A one-hour spike on the motivating case (`agents/reuse-auditor.md:22`) would reclassify it from A to P.
6. **Skill-to-skill invocation cost.** Is a probe skill better as a shared ref copied into each consumer's `refs/` (no Skill call) or a separate skill? Dual-surface rules favour the skill; per-run latency of the Skill call is UNVERIFIED.
7. **Non-Python changed-symbol extraction.** I-04/I-07 map hunks to symbols with a Python regex. Do the other indexed languages need their own rule, or file-level scope only?
8. **Pin ownership for primitives.** Primitives run in other projects and cannot read IronClaude's pin; is "record version, `doctor` enforces" enough?
