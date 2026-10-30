---
title: "P3 codegraph opportunities — merged requirements"
domain: architecture
generated_by: "/sc:brainstorm via /sc:adversarial (Mode B, depth standard)"
base_variant: "sonnet:analyzer"
convergence: "0.957 (67/70)"
convergence_status: "BLOCKED_BY_INVARIANTS (INV-001 accepted as risk; blocking prerequisite E-1)"
date: 2026-10-29
topic: p3-codegraph-opportunities
source_brief: .dev/codegraph-migration/brainstorm/P3-codegraph-opportunities/seed-brief.md
ground_truth: .dev/codegraph-migration/research/codegraph-evaluation.md (EVAL)
---

<!-- Provenance: This document was produced by /sc:adversarial (Mode B, depth standard) from Variant A (opus:architect), Variant B (sonnet:analyzer) and Variant C (haiku:backend). "Change #N" in Source tags refers to refactor-plan.md in this directory. -->
<!-- Base: Variant B (sonnet:analyzer) -->
<!-- Merge date: 2026-10-29T17:42:24Z -->

# P3: where IronClaude should use codegraph v1.6.2 beyond 1:1 Serena replacement

<!-- Source: Base (original, modified) — Notation paragraph extended with scope and INV definitions per Change #1 (Variant A line 13, Variant C line 4) -->
Notation. EVAL = `.dev/codegraph-migration/research/codegraph-evaluation.md`, the ground truth for every codegraph fact. INV = `.dev/codegraph-migration/inventory/primitive-usage.md`, the primitive inventory, cited as INV §N. INV-NNN = an item of the invariant probe, listed in section 8.4. Primitive paths are relative to `src/superclaude/`, and `path:line` is cited only for lines the variant authors read. UNVERIFIED = EVAL did not measure it. Evidence classes: **M** = measured gap and measured mechanism; **P** = gap shown in primitive text, mechanism measured, benefit unmeasured; **P-minus** = mechanism never run in EVAL; **A** = benefit rests on unmeasured codegraph behaviour (dropped).

Scope. The targets are guidance text, `tools:`/`allowed-tools:` lines, return-contract values and new primitives under `src/superclaude/{skills,commands,agents,core,hooks}`. Out of scope: the installer phase, the IronClaude Python CLI, and the 1:1 Serena SYM/REF swaps that Phase 3 owns (INV §4; D-22). This is a planning document only.

## 1. Summary

<!-- Source: Base (original, modified) — bullets corrected per Change #2 (EVAL facts), #4 (terminology), #8 (E-1), #15 (explore reason), #16 (staged tests), #26 (four candidates), #28 (ranking), #29 (drops) -->
- **Root cause split.** codegraph answers "which symbols, files and tests are connected" (callers, impact, affected: set membership). It cannot answer "where exactly" (caller rows give the caller's definition line, `main.py:46` not `:255`, EVAL §5.5) or "is there none" (no text search, no dynamic or string references, EVAL §6.1). Every adopted idea uses the graph for scoping and leads, uses Read for any cited line, and never lets an empty result convict (FR-06, FR-07).
- **Access model: CLI first, orchestrator-computed artifacts, passed by path into read-only agent briefs.** The repo already works this way (`skills/sc-troubleshoot-protocol/SKILL.md:281` pastes the producers table into every brief; `skills/sc-reflect-protocol/SKILL.md:355` has reviewers audit only pre-computed hunks). This avoids the `CODEGRAPH_MCP_TOOLS` blocker (B1) and works where MCP is unavailable (`skills/sc-cleanup-audit-protocol/SKILL.md:86`). Allowlists are per subcommand, because the CLI includes `install`, `uninstall`, `upgrade`, `unlock` and `telemetry` (EVAL §3). An MCP stage is deferred behind a measured trigger (section 2.1).
- **One blocking prerequisite.** INV-001 is the only HIGH open risk: EVAL never saw CLI `status` report pending files without a daemon. E-1 tests this in a sandbox. Until it has run, every freshness-dependent idea ships only in advisory or shadow form (G-FRESH, section 2.3).
- **Top ranked.** Layer 0: P-01 (E-1), P-02 (E-2), P-03 (E-3), I-01 grounding seam, I-02 call-site resolver and citation contract, I-03 allowlists and explore ban. Then by score: I-05 reflect parity, I-11 pre-fix impact, I-09 `/sc:graph` (section 4).
- **Parity hazard the 1:1 plan misses.** Replacing `find_referencing_symbols` with callers loses the per-reference snippet. EVAL §5.5 shows 20 of 23 caller rows for one symbol: 2 production (`install_mcp_server`, `install`) and 18 tests. The 3 hidden rows were not inspected, and this is one symbol only. Reflect's rule "HIGH if >5 referencing call sites" (`skills/sc-reflect-protocol/SKILL.md:347`) could trip on tests alone (I-05).
- **`explore` is a token regression risk.** One `codegraph_explore` call returned 24,913 characters (about 6K tokens at 4 characters per token, an estimate) and two unrelated `install` functions (EVAL §5.6). The troubleshoot Wave 1 budget is about 3K tokens (`skills/sc-troubleshoot-protocol/SKILL.md:218`). No primitive names explore (FR-10). When auggie is down, the fallback is Grep and Read.
- **Test selection is staged.** `affected` was never run in EVAL. It ships as an advisory delta (I-08 s0). The union with `<changed-area>` enters VG-1 only after G-FRESH and G-BACKTEST (I-08 s1). It can add tests, never remove them.
- **Dropped (29, section 5):** explore as a default step, all new hooks, any primitive `sync`, `/sc:load --index`, `sc-structure-brief`, tasklist graph input, reuse-auditor changes (deferred) and the 1:1 swaps themselves.
- **Four candidates (section 6):** K-1 `sc-graph-grounding` (skill), K-2 `/sc:impact`, K-3 `/sc:test-scope`, K-4 `/sc:graph`. Each has callers, a named fallback and no `src/superclaude` path.

<!-- Source: Variant C, §1 "Nine-vector coverage map" — merged per Change #3 (replaces base §4 vector bullets; net position adapted to the merged rules) -->
**Nine-vector coverage.** Every seed vector has at least one adopted idea or an explicit drop.

| Vector | Adopted (merged IDs) | Explicit drops | Net position |
|---|---|---|---|
| Token cost | I-03 routing and explore ban; FR-10 caps (40 rows, 6 KB); NFR-06 2K tokens | D-01 explore default; D-10 node file mode | Neutral to positive; the win is fewer Read/Grep tours, not graph payloads |
| Citation accuracy | I-01 provenance; I-02 resolver and typed rows | D-11 validator tools | Positive only through the mandatory re-Read; raw rows are never citation-grade |
| Impact before edits | I-07 implement pre-edit warning and post-edit check; I-11 pre-fix impact; K-2 `/sc:impact` | D-02 PreToolUse hook | Novel; no primitive computes dependents today |
| Review scoping (auggie-review, pr-submit, reflect) | I-04 s1 auggie-review context, plus pr-submit Wave 3 context; I-04 s2-3; I-11 pr-submit Wave 4; I-05 reflect | D-14 graph chunking | Context first; the one exemption waits on G-SHADOW-AUGGIE |
| Test selection (`affected`) | I-08 s0 advisory and I-08 s1 union; I-14 reflect UC-2 | D-26 cleanup-audit test runs | Unmeasured; advisory until G-BACKTEST |
| Troubleshoot Tier 1 | I-06 | D-09 producer enumeration | Lowest risk; the Glob/Grep fallback is already accepted |
| Planning (workflow, implement, tasklist) | I-13 workflow informational; I-07 implement; I-08 s0 implement Q6 extras | D-06 tasklist; D-07 graph numbers in acceptance criteria or tiering | Notes and warnings only; plan files stay deterministic |
| Reflection and audit (reflect, cleanup-audit, reuse-auditor) | I-05, I-14 reflect; I-12 cleanup-audit | D-08 reuse-auditor (deferred) | Largest surface; severity changes only after shadow runs |
| Onboarding (index-repo, explain, load) | I-10 explain one-hop and load status line; I-09 `/sc:graph` | D-19 `/sc:load --index`; D-20 `/sc:load` rewrite; D-21 index-repo stats and `sc-structure-brief` | Light edits only |

## 2. Access model and prerequisites

### 2.1 Access path per primitive class

<!-- Source: Base (original, modified) — rows 1 and 5 replaced, Bash column and MCP-stage row added per Change #5 (Variant A §2.1 classes A-G); row 1 latency relabelled per Change #2 -->
| Primitive class | Bash | Evidence of current tools | v1 path | Why |
|---|---|---|---|---|
| Orchestrators with unrestricted Bash: troubleshoot, reflect, implement, workflow | unrestricted | troubleshoot `:4` has Bash; reflect `:5`, workflow `:4`, implement `:4` list Bash | CLI via Bash; writes an artifact; may run bundled scripts | 290-300 ms per CLI call (EVAL §5.5). "Acceptable at 30-60 calls per run" is arithmetic from EVAL §5.5, not measured; the query count is logged (NFR-01) |
| Orchestrators with a closed Bash set: pr-submit, auggie-review, cleanup-audit | closed | pr-submit `:4` `Bash(gh *) git uv make jq`; auggie-review `:4` `Bash(auggie *) gh git jq ...`; cleanup-audit `:8` `Bash(git *) wc find du` | One pattern per read-only subcommand, e.g. `Bash(codegraph callers *)`; never `Bash(codegraph *)` (FR-04); bundled scripts only after E-3 | The wildcard would pre-approve `install`, `upgrade`, `uninit`, `unlock` and `telemetry` (EVAL §3; `install` edits Claude config, EVAL §2) |
| Read-only agents: reflect-reviewer, troubleshoot-analyst, reuse-auditor, audit-* | none | `tools:` lines at `agents/*.md:4-5`; reflect `:658` forbids Bash/Edit/Write/Task for reviewers | Artifact in the brief (a path the agent Reads); `refs/citation-contract.md` by installed path | Same pattern as the producers table; agents need no `mcp__codegraph__*` names (FR-11) |
| evidence-validator | none | `agents/evidence-validator.md:5` = `Read, Grep, Glob` | None; the file stays byte-identical | Its independence is the citation gate (FR-06, D-11) |
| Interactive commands: explain, load | session default | no `allowed-tools` field in either file | CLI for the explain one-hop and the load status line (I-10); no explore allowance (FR-10) | One user-driven call; index-repo is unchanged (D-21) |
| Hooks | n/a | `hooks/hooks.json:47-70` | No change (D-02, D-03, D-04) | `freshness-pre-edit.sh` timeout is 1 s (`hooks.json:52`) |
| MCP stage (deferred) | n/a | Only explore is listed by default (EVAL §3) | Not in v1 (D-28) | Eligible only when (1) the installer phase decides globally to set `CODEGRAPH_MCP_TOOLS` (one decision for every session, because an explicit list blocks every unlisted tool, explore included, EVAL §3), (2) the always-loaded schema overhead is measured (NFR-06), and (3) logged counts show more than about 100 serial CLI calls per run in some orchestrator (NFR-01). The count is evidence for the global decision, not a per-orchestrator switch |

<!-- Source: Base (original, modified) — freshness sentence aligned with FR-05 and E-1 per Change #8 and #10 -->
MCP's remaining role is installer-owned: a connected server starts the shared daemon and watcher that keep the index fresh (EVAL §4, §5.7). In CLI-only sessions (headless workers, sprint runs) nothing watches. The probe therefore re-checks freshness before each query batch that follows an in-run write (FR-05), and E-1 tests whether `status` can see pending files at all.

### 2.2 Blockers and owners

<!-- Source: Base (original, modified) — B1 stance aligned with the MCP-stage row (Change #5); B2 owner replaced and B9-B12 added per Change #6 (Variant A §2.2 B2, B5; INV-001, INV-019, INV-020); owners renamed per Change #7/#26 -->
| # | Blocker | Evidence | Owner | Stance |
|---|---|---|---|---|
| B1 | Only `codegraph_explore` is listed; the other 7 tools need `CODEGRAPH_MCP_TOOLS` in the server env; the planned registration sets only the telemetry and update-check vars | EVAL §3, §7 step 5 | Installer phase | Not set in v1 (D-28); reopen only through the MCP-stage trigger (section 2.1) |
| B2 | Per-worktree `init` has no owner; a sibling worktree is "not initialized", a nested one answers from the parent with a warning | EVAL §4, §5.8; this checkout is a sibling | User-typed `/sc:graph init` (K-4, I-09); a Coder template or git `post-checkout` hook stays a host-level option (EVAL §4) | The probe never inits; `not_initialized` and `foreign_index` degrade (FR-03) |
| B3 | `codegraph sync` fails on the writer lock while a daemon runs; watcher debounce 2000 ms; the watcher runs only with an MCP client | EVAL §4, §5.7 | K-1 | No primitive runs `sync` (D-18); the probe reads `status` (FR-05); see B10 |
| B4 | Caller rows cite the definition line | EVAL §5.5 | I-02 | Leads only until resolved and Read (FR-06) |
| B5 | Caller lists truncate at 20 by default ("Showing 20 of 23"; MCP limit max 100) | EVAL §3, §5.5 | K-2 `/sc:impact` | Record shown/total (FR-08) |
| B6 | Allowlist edits in 8+ primitives | section 3 targets | Phase 3 authors | Per-subcommand patterns (FR-04) |
| B7 | No documented `--json` for `callers`, `impact` or `status`; only `query` and `affected` list `--json` | EVAL §3 | K-1 and K-2 parsers | Golden fixtures plus `graph:parse_failed` (NFR-04); E-2 |
| B8 | Version pin and drift | EVAL §7 | `superclaude doctor` | The probe records the version; a mismatch degrades (FR-03, NFR-09) |
| B9 | Telemetry: Bash CLI calls do not inherit the MCP entry's `CODEGRAPH_TELEMETRY=0`, and a binary already on PATH skips the installer fallback | EVAL §1, §7 steps 2-3 | Installer phase | FR-22; accepted risk (section 8.4) |
| B10 | Freshness without a daemon: CLI `status` pending detection without a daemon was never observed (INV-001) | EVAL §4, §5.4, §5.7 | This phase | E-1; G-FRESH |
| B11 | CLI flag documentation gap: `callers`/`node` file pin, `symbolsOnly`, a machine-readable `status`; the EVAL §3 usage line is abbreviated | EVAL §3 | This phase | E-2 |
| B12 | Allowlist matching: `~` expansion, dual-surface script paths and env-prefixed commands under `Bash(codegraph <sub> *)` are UNVERIFIED (INV-019, INV-020) | INV-019, INV-020 | This phase | E-3 |

### 2.3 Prerequisite experiments and gates

<!-- Source: invariant-probe.md INV-001 closure note — merged per Change #8 (blocking prerequisite E-1, gate G-FRESH) -->
**E-1 freshness experiment (P-01; effort S; blocking).** In a sandbox worktree with no MCP client and no daemon (confirm `.codegraph/daemon.sock` is absent and no `serve --mcp` process runs):

1. Run `codegraph init --yes`.
2. Run `codegraph status`; record the output.
3. Append a function to an indexed file.
4. Run CLI `codegraph status` at once and again after 5 s; record both outputs verbatim.
5. Repeat steps 3-4 with a daemon running.
6. Repeat steps 3-4 with `CODEGRAPH_NO_DAEMON=1`.
7. Record whether `.codegraph/daemon.sock` exists only while a daemon is live.
8. Store the transcript as a golden fixture.

- **Outcome A:** `status` lists pending files without a daemon. The run-state rule in FR-05 stands as written.
- **Outcome B:** it does not. Every session without a detected live daemon gets `index_state: stale` for its whole run, and its graph sets and counts are leads only.

<!-- Source: Round 2 new evidence and invariant probe (INV-011, INV-019, INV-020) — merged per Change #9 -->
**E-2 CLI help capture (P-02; S).** Capture `codegraph callers --help`, `callees --help`, `node --help`, `impact --help`, `status --help`, `affected --help` and `query --help` for v1.6.2 into the capability map. This settles the CLI `file` pin, `symbolsOnly` and a machine-readable `status`; until then CLI `node` file or `symbolsOnly` mode and CLI `callers --file` are UNVERIFIED in both directions. Until E-2, CLI ambiguity is resolved by `query --json` matches filtered by file, and `/sc:impact --file` pinning stays off.

**E-3 allowlist matching check (P-03; S).** Test Claude Code permission matching for (a) `Bash(codegraph callers *)` against `CODEGRAPH_TELEMETRY=0 codegraph callers x`, (b) `~/`-prefixed and absolute script paths for both dual-surface locations, and (c) positional args such as `codegraph affected a b`. Until E-3 passes, closed-Bash consumers call subcommands directly with per-subcommand patterns, and bundled scripts run only in unrestricted-Bash orchestrators.

**E-4 resolver timing.** Time `resolve-callsite.sh` per row on the 500-file index and record it against NFR-01.

<!-- Source: Merged per Change #8 (G-FRESH), #17 (G-BACKTEST), #18 (G-SHADOW-REFLECT), #19 (G-SHADOW-AUGGIE), #23 (G-SPIKE) -->
| Gate | Opens when | Holds back |
|---|---|---|
| G-FRESH | E-1 has run and its outcome is written into the capability map. Under Outcome B it opens only in sessions with a detected live daemon | I-04 s2-3, I-05 severity use, I-07 post-edit check, I-08 s1, I-12, I-14 beyond advisory or shadow form |
| G-BACKTEST | NFR-08 passes | I-08 s1 union |
| G-SHADOW-REFLECT | 10 reflect runs on code changes have logged both today's count and the prod-only count, and a written review of the divergences approves the switch | I-05 severity switch |
| G-SHADOW-AUGGIE | Over 20 reviews, at least 3 shadow hits were judged true by the PR author or reviewer and the false-positive rate is 20% or less; G-FRESH is open | I-04 s3 exemption |
| G-SPIKE | A one-hour spike shows the DELETE→REVIEW upgrade fires on at least one candidate where grep did not | I-12 |

An idea is **freshness-dependent** when its output is a set or count that changes a severity, a gate, a verdict or a finding class, or when it runs after an in-run write. The freshness-independent ideas (I-01, I-02, I-03, I-04 s1 as labelled context, I-06, I-08 s0, I-09, I-10, I-11, I-13) may ship before E-1, with rows labelled `index_state` and `checked_at`. Every gated idea already ships an advisory form, so no idea depends on E-1 to exist, only to gate.

## 3. Ideas

<!-- Source: Base (original, modified) — rows rewritten per Changes #7, #13 (I-01, I-02), #15 (I-03), #19 (I-04 split), #18 (I-05), #20 (I-06), #21 (I-07), #16 (I-08 split), #25 (I-09, I-10); added I-11 (#22, Variant A I-10), I-12 (#23, Variant C I-07), I-13 (#24, Variant A I-13), I-14 (#28, Variant A I-08); single effort per row per Change #28 -->
Value H/M/L with evidence class. Effort S/M/L (one value). Risk L/M/H. Every fallback is the primitive's own native path plus a `graph:*` token (FR-02). The prerequisite experiments P-01..P-03 are in section 2.3.

| ID | Idea | Vectors | Target primitives | codegraph mechanism | Value (evidence) | Effort | Risk | Native fallback | Gates |
|---|---|---|---|---|---|---|---|---|---|
| I-01 | Grounding seam K-1: readiness, provenance, freshness, version and telemetry probe; capability map; closed `graph:*` vocabulary | citation accuracy, all | new `skills/sc-graph-grounding/`; one Step-0 line in each consumer | `codegraph --version`; `codegraph status` (parse "Not initialized", "different git working tree", "Index is up to date", pending list); `codegraph telemetry status`; `git rev-parse --show-toplevel` | H (M). Prevents silent answers from another checkout (EVAL §5.8), stale reads in CLI-only runs (EVAL §5.7) and a repeat of the Auggie stale-index lesson (`skills/sc-auggie-review-protocol/SKILL.md:189`) | M | L | `index_state: absent`, `graph:absent`, continue natively | none |
| I-02 | Call-site resolver and citation contract: typed `resolution` on every row | citation accuracy, reflect, troubleshoot | seam `refs/citation-contract.md`, `scripts/resolve-callsite.sh`; reflect `:42`, troubleshoot Wave 5, auggie-review `:216-219`, `agents/reuse-auditor.md:132` | `codegraph query <caller> --json --limit 20` gives `startLine`/`endLine` (EVAL §5.5); bind on file and `startLine == def_line`; span-bounded Grep for a call expression; Read (FR-06) | H (M). Closes the measured `main.py:46` vs `:255` gap and restores the call-site snippet Serena returned (EVAL §6.2: "no per-reference snippet") | M | M (aliases, attribute calls, strings; the strict match lowers recall) | Grep the callee name in the file, then Read | E-4 timing |
| I-03 | Allowlists, routing block and explore ban | token cost, safety | `core/CLAUDE.md` routing block; consumer allowlist lines; `skills/sc-troubleshoot-protocol/SKILL.md:218`, `commands/troubleshoot.md` | Policy: per-subcommand patterns (FR-04), no primitive names explore (FR-10), routing block of 12 lines or less (FR-21) | H (M). One explore call: 24,913 characters with unrelated matches (EVAL §5.6) vs a ~3K-token Wave 1 budget; the routing block loads every session, so its size is a cost | S | L | existing auggie/Grep routing | E-3 for scripts |
| I-04 s1 | auggie-review blast radius as context | review scoping, impact | auggie-review Wave 1 (new step after `:126-138`), `refs/auggie-prompts.md`; pr-submit Wave 3 context | `/sc:impact --diff` writes `inputs/blast-radius.md`: hunks to symbols via `query --json` spans, `callers --limit 100`, `impact --depth 2`, prod/test partition; the Auggie prompt gets names and files only | M (P). An out-of-hunk finding is downgraded to "context" or dropped by severity (`:218`); directory chunking applies only at 16-30 files or 1500-5000 diff lines (`:136-137`). Benefit UNVERIFIED | M | M (prompt bloat; hunk mapping is IronClaude-side and best-effort) | files-only scope from `git diff --name-only`; `unmapped_files[]` | none (context) |
| I-04 s2-3 | `dependent-impact` finding class: shadow first, then exemption from the out-of-hunk downgrade | review scoping | auggie-review Wave 3 (`:216-219`) | `call-site-verified` rows from I-02 (FR-12) | M (P-minus) | M | M (false exemptions) | today's downgrade | G-FRESH, G-SHADOW-AUGGIE |
| I-05 | Reflect prod-only parity for severity and the runtime-surface sweep | reflection, citation accuracy | reflect Step 1B.3 (`:338-349`), chain 4/4b (`:514-516`), `refs/runtime-surface.md` (prod/test table `:25-28`) | `/sc:impact` rows: `callers --limit 100`, `impact --depth 2` for the top-30 hotspots; partition by the runtime-surface globs; lists are floors (FR-09) | H (hazard M, benefit P). 18 of 20 shown rows were tests in the one sample; without it the 1:1 swap inflates severity (`:347`) | M | M (2045-line skill, CLI-parsed contract; no new field) | Grep-based referrer sweep in 4b | G-FRESH, G-SHADOW-REFLECT |
| I-06 | Troubleshoot Tier 1 callers | troubleshooting | troubleshoot Wave 1 step 1 (`:191-194`), exit criteria (`:216`), S1.6.2 Branch A (`:286`); `commands/troubleshoot.md:88-96` | `codegraph query <symbol> --json` and `codegraph callers <symbol> --limit 20` for the failing component, written to `tier1-callers.md` (40 rows, 6 KB) and pasted into Branch A briefs within the ~3K Wave 1 budget (`:218`; the 2K figure at `:256` is Wave 1.5) | H (P). Branch A's "immediate callers" is auggie/Grep today; callers took 3-15 ms over MCP and about 300 ms by CLI (EVAL §5.5, §5.6) | M | L | Glob/Grep fallback already accepted (`:194`, `:216`) | none (leads) |
| I-07 | Implement pre-edit warning and post-edit check | impact before edits | implement Q1-Q3 (`:118-123`), `refs/qa.md` (package definition `:9`) | Pre-edit `/sc:impact <symbol>` for rename, delete or signature tasks; post-edit `untouched_dependents` on the actual diff (FR-16) | H (P). QA input is the task brief and the diff only (`refs/qa.md:9`) | M | M (QA scope creep; context only) | Grep for the symbol name, `graph:absent`; review unchanged | post-edit: G-FRESH |
| I-08 s0 | `affected` advisory delta through `/sc:test-scope` | test selection | pr-submit VG-1 (`:206-207`); implement Q6 extras (`:129,144`) | `codegraph affected <files…> --depth 2 --json --quiet`, files as positional args from `git diff --name-only`, filtered to paths that exist | M (P-minus). `affected` returns test files only (EVAL §6.1) and was never run in EVAL | S | L | `uv run pytest <changed-area>`, then VG-2 `make test` | none (advisory) |
| I-08 s1 | `changed-area ∪ affected` union in VG-1 | test selection | pr-submit VG-1 | Union filtered by `git ls-files` and a `pytest --collect-only -q` pre-pass (FR-13) | M (P-minus) | M | M (runaway set, false block) | `<changed-area>` on any collection error | G-FRESH, G-BACKTEST |
| I-09 | `/sc:graph` lifecycle owner (K-4) | onboarding, freshness | new `commands/graph.md` | `codegraph status`; user-typed `codegraph init --yes`; `init -i` with `--worktree-local` in a nested worktree (EVAL §5.8) | M (P). Gives B2 a user-level owner; `init` costs about 4.5 s, 34 MB and peak 1 GB RSS for 500 files (EVAL §5.4) | S | M (a mutating step; explicit user command only) | print the exact `codegraph init --yes` line | none |
| I-10 | Explain one-hop and load status line | onboarding, token cost | `commands/explain.md` (`:46-50`), `commands/load.md` (`:27`) | Explain: CLI `query --json`, `callers`, `callees` (limit 10), rows re-Read; load: one read-only `index_state` line plus a pointer to `/sc:graph init` | M (P-minus). Token benefit unmeasured | S | L | current Read/Grep/Glob flow | none |
| I-11 | Pre-fix impact in remediation chains | impact before edits, review scoping | pr-submit Wave 4 (ordinal 2 or higher, before edits, `skills/sc-pr-submit-protocol/SKILL.md:194`); troubleshoot `--fix` handoff | `/sc:impact` report for the symbols the fix touches, as a warning only | M (P) | S | L | Grep for the symbol name, `graph:absent` | none (warning) |
| I-12 | Cleanup-audit asymmetric corroboration | reflection and audit | cleanup-audit `:75,:83,:86`, orchestrator only | `codegraph callers <s>`: nonzero callers move a DELETE candidate to REVIEW; zero callers prove nothing; the DELETE gate stays the grep proof (`:75`) | L-M (P-minus) | S | L | grep proof alone | G-SPIKE, G-FRESH |
| I-13 | Workflow informational impact | planning | workflow Wave 1 | `codegraph impact <s> --depth 2` only when the source names symbols that already exist; counts go to the plan notes with `index_state` and `checked_at`, never to acceptance criteria or tiering | M (P-minus) | M | L | omit the note | existing symbols only |
| I-14 | Reflect UC-2 regression evidence (advisory) | reflection, test selection | reflect UC-2 regression category | `/sc:test-scope` maps touched files to tests; flag "touched code has mapped tests that were neither changed nor run" | M (P-minus) | S | L | path heuristic `tests/**/test_<module>*` | G-FRESH |

## 4. Ranked list

<!-- Source: Variant A §4 Layer 0 + Base §4 V × C ÷ E — merged per Change #28 (replaces base §4; I-07 rescored with C=0.6) -->
Method. Layer 0 holds prerequisites and enablers in dependency order: the experiments P-01..P-03 (section 2.3), then I-01, I-02 and I-03, which every other idea cites. Every other idea is scored V × C ÷ E. V (1-5) is the structural gap closed, judged from cited primitive text. C is evidence confidence: M = 1.0, P = 0.6, P-minus = 0.3. E is effort weight: S = 1, M = 2, L = 4. Ties go to a measured hazard first, then a measured mechanism, then lower risk, then higher run frequency of the host primitive, then the base variant's prior rank. Class A ideas are not ranked (section 5). A gated idea keeps its rank but ships only as its gates allow.

| Rank | ID | Idea | Targets | Value | Effort | Risk | Score | Gates |
|---|---|---|---|---|---|---|---|---|
| 1 | P-01 | E-1 freshness experiment | sandbox only | H (unblocks G-FRESH) | S | L | Layer 0 | blocking |
| 2 | P-02 | E-2 CLI `--help` capture | seam capability map | M | S | L | Layer 0 | none |
| 3 | P-03 | E-3 allowlist matching check | closed-Bash allowlists | M | S | L | Layer 0 | none |
| 4 | I-01 | `sc-graph-grounding` seam | new skill; Step-0 line in each consumer | H | M | L | Layer 0 | none |
| 5 | I-02 | Resolver and citation contract | seam refs/scripts; reflect `:42`; troubleshoot Wave 5; auggie-review `:216-219` | H | M | M | Layer 0 | E-4 timing |
| 6 | I-03 | Allowlists, routing block, explore ban | `core/CLAUDE.md`; consumer allowlist lines | H | S | L | Layer 0 | E-3 for scripts |
| 7 | I-05 | Reflect prod-only parity | sc-reflect-protocol 1B.3, 4/4b; runtime-surface ref | H | M | M | 4×0.6/2 = 1.2 | G-FRESH, G-SHADOW-REFLECT |
| 8 | I-11 | Pre-fix impact in remediation chains | sc-pr-submit-protocol Wave 4; troubleshoot `--fix` handoff | M | S | L | 2×0.6/1 = 1.2 | none (warning) |
| 9 | I-09 | `/sc:graph` lifecycle owner | new `commands/graph.md` | M | S | M | 2×0.6/1 = 1.2 | none |
| 10 | I-06 | Troubleshoot Tier 1 callers | sc-troubleshoot-protocol Wave 1, 1.6 Branch A; `commands/troubleshoot.md` | H | M | L | 3×0.6/2 = 0.9 | none (leads) |
| 11 | I-04 s1 | auggie-review blast radius as context | sc-auggie-review-protocol Wave 1; pr-submit Wave 3 context | M | M | M | 3×0.6/2 = 0.9 | none (context) |
| 12 | I-07 | Implement pre-edit warning and post-edit check | sc-implement-protocol Q1-Q3, `refs/qa.md` | H | M | M | 3×0.6/2 = 0.9 | post-edit: G-FRESH |
| 13 | I-08 s0 | `affected` advisory delta | sc-pr-submit-protocol VG-1; implement Q6 extras | M | S | L | 3×0.3/1 = 0.9 | none (advisory) |
| 14 | I-10 | Explain one-hop and load status line | `commands/explain.md`, `commands/load.md` | M | S | L | 2×0.3/1 = 0.6 | none |
| 15 | I-12 | Cleanup-audit asymmetric corroboration | sc-cleanup-audit-protocol `:75,:83,:86` | L-M | S | L | 2×0.3/1 = 0.6 | G-SPIKE, G-FRESH |
| 16 | I-14 | Reflect UC-2 regression evidence (advisory) | sc-reflect-protocol UC-2 | M | S | L | 2×0.3/1 = 0.6 | G-FRESH |
| 17 | I-04 s2-3 | `dependent-impact` shadow, then exemption | sc-auggie-review-protocol Wave 3 `:218` | M | M | M | 3×0.3/2 = 0.45 | G-FRESH, G-SHADOW-AUGGIE |
| 18 | I-08 s1 | `changed-area ∪ affected` in VG-1 | sc-pr-submit-protocol VG-1 | M | M | M | 3×0.3/2 = 0.45 | G-FRESH, G-BACKTEST |
| 19 | I-13 | Workflow informational impact | sc-workflow-protocol Wave 1 | M | M | L | 2×0.3/2 = 0.3 | existing symbols only |

<!-- Source: Base (original, modified) — sequencing updated to K-1..K-4 per Change #26 -->
Sequencing. P-01..P-03 run first. I-01 and I-02 land with or before any consumer; I-03 lands with the first consumer. K-2 `/sc:impact` serves I-04, I-05, I-07, I-11 and I-13; K-3 `/sc:test-scope` serves I-08 and I-14. Gated ideas ship in their advisory or shadow form first (section 2.3).

## 5. Dropped ideas

<!-- Source: Base §5 D-01..D-12 (original, modified) + Variant A §5 + Variant C §5 + Round 2 deferrals — merged per Change #29; D-05 replaced per Change #2/#23; D-07 narrowed per Change #24 -->
| ID | Dropped idea | Reason |
|---|---|---|
| D-01 | `codegraph_explore` as a default or Tier 1 grounding step | One call returned 24,913 characters and pulled 2 unrelated functions (EVAL §5.6), against fixed wave budgets (about 3K tokens in troubleshoot Wave 1, `:218`). With auggie down, the fallback is Grep/Read. The evidence is one sample; reopen only after a `maxFiles` 1-5 single-symbol measurement |
| D-02 | `PreToolUse` hook that runs impact before every Edit | `freshness-pre-edit.sh` has a 1 s timeout (`hooks/hooks.json:52`); a CLI query is about 290-300 ms plus process start; a hook cannot know which symbol an Edit changes; it fires on every Edit/Write |
| D-03 | `SessionStart` hook that runs `codegraph init` or prints index state (including Variant A's status line) | `init` is a 4.5 s, about 1 GB RSS write (EVAL §5.4) inside other projects; `status` latency is unmeasured; it adds hook failure surface (`hooks/scripts/freshness-session-start.sh` already branches on MCP config at `:135`). `/sc:graph status` and the `/sc:load` line give visibility |
| D-04 | `prompt-hook` or `codegraph install` guidance | Injects an explore payload into every prompt (EVAL §5.9); its CLAUDE.md block is erased by `superclaude install` (EVAL §2) |
| D-05 | Zero graph callers as DELETE proof or as DELETE evidence | Callers are call edges only (EVAL §6.2) and codegraph has no text search (EVAL §6.1); EVAL states no coverage relation between Grep and the graph. Zero proves nothing; the DELETE gate stays grep proof (`sc-cleanup-audit-protocol/SKILL.md:75`). Only nonzero callers are used (I-12) |
| D-06 | sc-tasklist-protocol graph input | A deterministic roadmap-to-tasklist generator; its "blast radius" is requirement-level (`skills/sc-tasklist-protocol/SKILL.md:1658,1670`); a live index would make its bytes depend on machine state. Variant C conceded its tasklist risk field for this reason |
| D-07 | Graph numbers in workflow acceptance criteria or tiering | Spec text to symbol is a judgement step, named files are often not yet created, and an empty result reads as "no dependents" in a plan that reflect then grades (`skills/sc-workflow-protocol/SKILL.md:58-60`). Only the informational note survives (I-13) |
| D-08 | reuse-auditor co-caller search, liveness check and codegraph fallback tier | Deferred: agents have no MCP in v1 (FR-11), and candidates the agent finds cannot be precomputed by the orchestrator. Re-propose after the MCP stage (section 2.1) |
| D-09 | codegraph for troubleshoot producer enumeration (S1.6.0b) | That step is text and token search (`:277`); codegraph has no text search (EVAL §6.1) |
| D-10 | `codegraph_node` file mode as a Read replacement | Token saving unmeasured; it breaks the freshness chain (`hooks.json:59` counts only `Read`), so Edit would be blocked or nagged |
| D-11 | codegraph tools in the evidence-validator `tools:` line, or any edit to it | Its independence is the gate; it already rejects def-line rows cited as call sites (`agents/evidence-validator.md:62-66`); graph rows are leads (FR-06) |
| D-12 | Direct SQLite queries of `.codegraph/codegraph.db`, or any data-flow, cross-service or Cypher use | Schema UNVERIFIED (EVAL §6.1); no such codegraph capability. Memory and activation jobs (INV §4) are not graph jobs |
| D-13 | `codegraph context <task…>` for planning | It exists in the CLI (EVAL §3), but its output size and shape were never measured |
| D-14 | Graph-based review chunking for auggie-review | codegraph has no clusters or layers (EVAL §6.1) |
| D-15 | Replacing reflect's LSP diagnostics leg | codegraph has no diagnostics (EVAL §6.2) |
| D-16 | codegraph tools in the freshness matchers (`hooks.json:47`) | Every codegraph tool is read-only (EVAL §3); nothing to gate |
| D-17 | A `graph-scout` subagent | Only useful with explore (D-01); MCP is unavailable to background subagents (`sc-cleanup-audit-protocol/SKILL.md:86`) |
| D-18 | Any primitive running `sync`, including `/sc:graph sync` | `sync` fails on the writer lock while a daemon runs (EVAL §5.7) and would write inside read flows |
| D-19 | `/sc:load --index`, and any `init` outside the user-typed `/sc:graph init` | A mutation (34 MB, about 1 GB RSS, EVAL §5.4) inside a context command; one user-level owner (I-09) is enough |
| D-20 | Rewriting `/sc:load` around codegraph | Load is memory and activation (INV §4); codegraph has no memories (EVAL §6.2) |
| D-21 | `sc-structure-brief` and index-repo graph stats | Deferred: Glob already gives the structure; the "58K to 3K" figure in `commands/index-repo.md:13` is unmeasured; no layers or hotspots (EVAL §6.1) |
| D-22 | The 1:1 Serena swaps as P3 ideas | Out of scope; Phase 3 owns them (INV §4) |
| D-23 | `/sc:ground` claim-grounding command | Folded into the seam's resolver and citation contract (K-1) |
| D-24 | Private per-skill impact and test-scope scripts | One contract and one fallback map (K-2, K-3); private copies would drift |
| D-25 | Graph routes for `sc-recommend` | IronClaude primitives are Markdown, not routed code; routing is about work intent |
| D-26 | Test runs inside cleanup-audit | The audit is READ-ONLY by charter (`:155`) |
| D-27 | Interactive explore with `maxFiles` 5 or less | No consumer needs it and it adds surface (FR-10) |
| D-28 | `CODEGRAPH_MCP_TOOLS` and agent MCP names in v1 | The listing is global and blocks unlisted tools (EVAL §3); schema overhead unmeasured (NFR-06); deferred to the MCP-stage trigger (section 2.1) |
| D-29 | Treating HIGH as MEDIUM when the index is stale | Superseded by FR-09: stale, truncated or unproven counts never feed severity |

## 6. Candidate new commands and skills

<!-- Source: Variant A §6 C-1..C-4 slots with Base §6 N-1/N-2 content and Variant C C-3 fields — restructured per Change #26; K-1 per Change #7; N-3 moved to D-21 per Change #25 -->
All four name installed paths first (`~/.claude/skills/<name>/...`, `~/.claude/commands/sc/<name>.md`), then the project `.claude/` copy. None contains a `src/superclaude/` path (FR-20).

### K-1 `sc-graph-grounding` (skill, delegate-only; no slash command)

<!-- Source: Variant A §6 C-1 (capability map, refs, header switch) + Base N-1 (probe, provenance, resolver) + Variant C §2 contract sequence — merged per Change #7, #12, #13, #27 -->
- Purpose: the single seam (I-01, I-02). It owns the probe, the capability map, the citation contract, the closed vocabulary and the resolver script.
- Files: `SKILL.md`, whose body is the sequence PROBE (once per run, FR-01) → CALL (read-only subcommands only, FR-04; re-check after in-run writes, FR-05) → VERIFY (resolve and Read cited rows; drop failures, never repair, FR-06) → DEGRADE (native fallback plus a `graph:*` token, never STOP, FR-02). `refs/capability-map.md`: one row per capability (`callers | callees | impact | definition | search | affected_tests | status`) with the CLI form, the MCP tool name `mcp__codegraph__codegraph_<tool>` where one exists (EVAL §3; none for `affected`; not listed in v1), the native fallback, known gaps and the golden-fixture command; header `tested_version: 1.6.2` and `status: enabled|disabled`. `refs/citation-contract.md`; `refs/degraded-vocab.md`; `scripts/resolve-callsite.sh`.
- Interface: args `[--project-path <abs>] [--max-pending N]`. Resolver: `resolve-callsite.sh --caller <name> --callee <name> --file <path> --def-line <n>` prints `caller_file`, `start`, `end` and candidate `file:line:text` rows marked `unresolved`; the calling orchestrator's Read sets `call-site-verified`.
- Output fields: `access: cli|none`, `index_state: fresh|stale|not_initialized|foreign_index|absent|disabled|error`, `checked_at`, `version`, `pin_match`, `worktree_root`, `index_root|unknown`, `pending_files|unknown`, `daemon: live|absent|unknown`, `telemetry: on|off|unknown`, `degraded[]`.
- Callers: sc-troubleshoot-protocol (Wave 0, Wave 1, Wave 1.6), sc-reflect-protocol (Wave 0, 1B.3, chain 4/4b, UC-2), sc-implement-protocol (Wave 0, Q1, post-edit), sc-pr-submit-protocol (before VG-1, Wave 4), sc-auggie-review-protocol (Wave 1), sc-cleanup-audit-protocol (orchestrator, behind G-SPIKE), sc-workflow-protocol (Wave 1), `/sc:impact`, `/sc:test-scope`, `/sc:graph`, `/sc:explain`, `/sc:load`. Agents (reflect-reviewer, troubleshoot-analyst) read artifacts and `refs/citation-contract.md` by installed path.
- codegraph tools: CLI `codegraph --version`, `status`, `telemetry status`, `query --json`; also `git rev-parse`, `printenv IRONCLAUDE_CODEGRAPH`, Grep and Read.
- Fallback: `index_state: absent` or `disabled` with a `degraded` entry; callers continue natively.
- Effort: M.

### K-2 `/sc:impact` (command)

<!-- Source: Variant A §6 C-2 (modes, caps, callers) + Base N-2 blast-radius fields — merged per Change #26 (absorbs base `sc-blast-radius` and `/sc:blast-radius`) -->
- Purpose: dependents of a symbol, a file or a diff (I-04, I-05, I-07, I-11, I-13).
- Interface: `/sc:impact <symbol> | --file <path> | --diff [<base>]` `[--depth 1-3, default 2] [--limit N, default 20, max 100] [--tests] [--output <dir>]`. `--diff` maps hunks to symbols through `query --json` spans. `--file` pinning waits on E-2.
- Output: `blast-radius.md` with a YAML header: `changed_symbols[]` (`name`, `file`, `start`, `end`, `mapped_by: hunk|name`, labelled as IronClaude-side mapping), `dependents.prod[]` and `dependents.test[]` (`caller`, `file`, `def_line`, `call_site_line|null`, `resolution`), `truncated{symbol: shown/total}`, `ambiguous[]`, `unmapped_files[]`, `affected_tests[]|unknown` (with `--tests`, through K-3), `index_state`, `checked_at`, `degraded[]`. Rows are sorted and capped (FR-10, NFR-03).
- Callers: sc-implement-protocol Q1 and post-edit, sc-pr-submit-protocol Wave 4, the sc-troubleshoot-protocol `--fix` handoff, sc-auggie-review-protocol Wave 1, sc-reflect-protocol 1B.3 and 4b, sc-workflow-protocol Wave 1, operators.
- codegraph tools: CLI `query --json`, `callers`, `impact`; `affected` through K-3; the K-1 probe and resolver.
- Fallback: files-only scope from `git diff --name-only`, or Grep for the symbol name; `affected_tests: unknown`; a `graph:*` token.
- Effort: L.

### K-3 `/sc:test-scope` (command)

<!-- Source: Variant A §6 C-3 (interface, superset rule) + Variant C C-3 (`source` field, escalation) + Base I-08 — merged per Change #16 and #26 -->
- Purpose: map changed files to tests as a superset of today's selection (I-08, I-14).
- Interface: `/sc:test-scope --files <list> | --diff <base>` `[--depth N] [--filter <glob>]`. Inputs reach `affected` as positional args, filtered to paths that exist in the working tree.
- Output: `changed_files[]`, `heuristic_tests[]`, `affected_tests[]|unknown`, `delta[]`, `selected[]` (stage 1 only), `filtered[]` (reasons `not_tracked|zero_collect|collect_error`), `selection_source: advisory|union|heuristic_only`, `pytest_args`, `index_state`, `degraded[]`.
- Callers: sc-pr-submit-protocol VG-1, sc-implement-protocol Q6 extras, sc-reflect-protocol UC-2 (I-14), `/sc:impact --tests`.
- codegraph tools: CLI `affected` only; it has no MCP tool (EVAL §3).
- Fallback: `selection_source: heuristic_only`.
- Effort: M.

### K-4 `/sc:graph [status|init]` (command)

<!-- Source: Variant A §6 C-4 minus `sync` — merged per Change #26 (INV-022), with telemetry display per Change #12 and switch documentation per Change #27 -->
- Purpose: user-level lifecycle and the owner for the per-worktree index (B2, I-09).
- Interface: `/sc:graph [status|init] [--worktree-local]`, default `status`. `init` runs only when the user typed it. In a nested worktree it refuses unless `--worktree-local` is passed, which runs `codegraph init -i` (EVAL §5.8). There is no `sync` (D-18).
- Output: `cli_version`, `pin_match`, `index_state`, `worktree_relation: own|parent|none`, `files/nodes/edges`, `pending[]|unknown`, `daemon`, `telemetry` (with the opt-out the user can apply: `CODEGRAPH_TELEMETRY=0` or `DO_NOT_TRACK=1` in the shell profile, EVAL §1), `next_action`. It documents the `IRONCLAUDE_CODEGRAPH=off` switch (FR-24).
- Callers: users; referenced from the `/sc:load` status line (I-10) and from the seam's `graph:not_initialized` message.
- codegraph tools: CLI `--version`, `status`, `telemetry status`, `init --yes`, `init -i`.
- Fallback: "codegraph not installed" plus the install pointer; it never stops a caller.
- Effort: S.

## 7. Requirements

### Functional

<!-- Source: Base §7 FR-01..FR-21 (original, modified) — FR-01/FR-05 per Change #10; FR-02 per Change #4; FR-03 per Change #11; FR-04 per Change #14; FR-06 per Change #13; FR-07 per Change #23; FR-09 per Change #18; FR-10/FR-21 per Change #15; FR-12 per Change #19; FR-13 per Change #16; FR-16 per Change #21; FR-17/FR-18 withdrawn per Change #25; FR-22 per Change #12; FR-23 per Change #14; FR-24 per Change #27 -->
- **FR-01** Each consuming primitive MUST run K-1 once per run before any other codegraph call. Availability, provenance and version are latched for the run. The run logs `index_state`, `access`, `checked_at` and `degraded`. Test: grep each target for the probe step; a run with `codegraph` off PATH logs `index_state: absent`.
- **FR-02** No codegraph step may STOP or fail a run. Every step names a native fallback and records one token from the closed vocabulary `graph:{absent, disabled, unlisted, not_initialized, foreign_index, stale, version_mismatch, provenance_unproven, telemetry_on, empty, ambiguous, truncated, parse_failed, unresolved}` inside the host's existing `degraded` or `degraded_components` list. Consumers invent no tokens. Test: grep each step for a fallback verb and a vocabulary token.
- **FR-03** Results are used only when `index_root` equals the realpath of the worktree root. Normal `status` output prints no root, so `index_root: unknown` counts as a match only while the v1.6.2 nested-worktree warning is absent (negative evidence, INV-004). The nested-worktree warning ("belongs to a different git working tree", EVAL §5.8) maps to `foreign_index`, handled as `not_initialized`. When `codegraph --version` differs from the pin, emit `graph:version_mismatch` and `graph:provenance_unproven`: the provenance check relies on the v1.6.2 warning text, so rows are leads only (no citations, sets or counts) for the run. Test: fixtures for both warnings and a mismatched version take the fallback path.
- **FR-04** CLI use is limited to `version`/`--version`, `status`, `query`, `callers`, `callees`, `impact`, `affected`, `files` and the read `telemetry status`. Allowlists use one `Bash(codegraph <sub> *)` pattern per subcommand (for telemetry, the pattern names `status`), never `Bash(codegraph *)`. `init`, `index`, `sync`, `uninit`, `install`, `uninstall`, `upgrade`, `unlock` and `telemetry on|off` are forbidden in every primitive; only the user-typed `/sc:graph init` may run `init` (K-4). Bundled scripts get exact-path patterns in the form E-3 verifies. Test: the allowlist diff shows only these patterns.
- **FR-05** Freshness. Before every query batch that follows an in-run write, re-run `status`; the re-check invalidates cached rows. Pending files or "not up to date" make the result `stale: true`, and its rows are leads only. With a live daemon, if only files written in the last 3 s are pending, wait 3 s once and re-check once; if they are still pending, use `stale`. Under E-1 Outcome B, a session with no detected live daemon is `stale` for its whole run. Any graph number written to a ledger or reviewer package carries `index_state` and `checked_at`, and on `/sc:implement` resume it is `stale` until re-checked. No "no dependents", "no callers" or "no tests" conclusion may come from a stale, foreign, unproven or error state. No primitive runs `sync`. Test: a pending-files fixture yields stale rows.
- **FR-06** Citation contract. Every graph row carries `resolution: def-line|call-site-verified|unresolved`. The resolver runs `codegraph query <caller> --json --limit 20` and keeps only the match whose `file` equals the row's file and whose `startLine` equals the row's `def_line`; otherwise the row is `unresolved` and the run records the unresolved count. It Greps `\bCALLEE\s*\(` inside `startLine..endLine` and rejects matches inside string literals, comments or docstrings, bare-name assignments and attribute-only matches. With several matches it cites each as a candidate or cites none. It Reads the line; a failing row is dropped, never repaired. `def-line` rows are cited only as definitions. Budget: resolve only rows that will be cited, at most 5 per symbol and 20 per run; the rest stay `unresolved` and count only. In consumers whose citations bypass the evidence-validator (auggie-review, reflect), `call-site-verified` rows are context only and cannot lift a downgrade or raise a severity, except the FR-12 stage 3 exemption. evidence-validator stays byte-identical. Test: a def-line row cited as a call site fails the validator fixture.
- **FR-07** Asymmetric evidence. A positive graph result may clear a suspect (a production caller exists); an empty result MUST NOT establish UNREACHED, dead code, DELETE or "no tests". Example: in cleanup-audit, nonzero callers move a DELETE candidate to REVIEW, and zero callers leave the grep proof (`:75`) as the only gate. Reflect's rootwalk before `UNREACHED` (`skills/sc-reflect-protocol/refs/runtime-surface.md:61`) is unchanged.
- **FR-08** Record `shown/total` for every caller list. If `total > shown` and `total <= 100`, re-query once with a wider `--limit`; above 100, set `truncated: true`.
- **FR-09** The prod/test partition uses reflect's runtime-surface table (`skills/sc-reflect-protocol/refs/runtime-surface.md:25-28`) as the single definition. Caller lists are floors. Until G-SHADOW-REFLECT opens, severity uses today's count and both counts are logged; after it, the thresholds at `skills/sc-reflect-protocol/SKILL.md:347` count distinct production caller symbols only. When a list is still `truncated` after the one re-query, or is `stale` or `provenance_unproven`, severity uses the Grep-based reference count from chain 4b and the graph only labels prod/test.
- **FR-10** No `tools:` line and no step body in any primitive names `codegraph_explore`, `codegraph explore` or `codegraph context`. Test: the grep over `src/superclaude/{skills,commands,agents,core,hooks}` allows only the "do not use" notes in the capability map and in the FR-21 routing block. Any artifact pasted into a brief has at most 40 rows and 6 KB.
- **FR-11** In v1 no `tools:` line of a read-only agent gains `mcp__codegraph__*`; agents get artifacts by path.
- **FR-12** auggie-review staging. Stage 1: when the probe reports `fresh` or `stale` (rows labelled), Wave 1 writes `inputs/blast-radius.md` through `/sc:impact --diff`; the Auggie prompt receives dependent names and files only, and the out-of-hunk downgrade (`:218`) is unchanged. Stage 2 (shadow): Read-verified `dependent-impact` rows are reported as ordinary context, and the audit log counts the rows `:218` would have downgraded. Stage 3: after G-SHADOW-AUGGIE opens, `dependent-impact` rows that are `call-site-verified` under FR-06 are exempt from the downgrade; all other rows are downgraded as today.
- **FR-13** Test selection through `/sc:test-scope`. Stage 0 prints the `affected_tests` not covered by `<changed-area>` and leaves the VG-1 gate unchanged. Stage 1 (after G-FRESH and G-BACKTEST): `selected = heuristic ∪ affected`, always a superset of the heuristic; union paths are filtered by `git ls-files`; a `pytest --collect-only -q` pre-pass drops paths that collect zero tests (exit 5); any collection error from an affected-only path falls back to `<changed-area>` and is logged; above 200 files, escalate to VG-2. The escalation rule keys on source-file diffs, so a docs-only diff may honestly yield no affected tests. `affected` stays CLI-only.
- **FR-14** Reflect Step 1B.3 and chain 4/4b read prod-only counts from K-2 rows under FR-09. No new contract field in v1; only `degraded_components` entries `graph:<x>`.
- **FR-15** Troubleshoot Wave 1 writes `tier1-callers.md` when a symbol or frame resolves and `access != none`; Wave 1.6 Branch A briefs paste it; the exit criteria accept "graph artifact, or Glob/Grep fallback noted".
- **FR-16** Implement. Pre-edit: for tasks that rename, delete or change the signature of an existing symbol, Q1 runs `/sc:impact <symbol>` (cap 10 files) as a warning to the implementer and an input to the Q3 package and the ledger; it never widens Q1 edits (`skills/sc-implement-protocol/SKILL.md:118-119`). Post-edit: Q2 adds `untouched_dependents` on the actual diff (at most 20 rows, context only, behind G-FRESH). Neither can create a blocking finding by itself or change touched-file rules.
- **FR-17, FR-18** Withdrawn (D-19, D-21). The IDs are not reused.
- **FR-19** No new hooks. Graph output never satisfies freshness-before-edit; `hooks.json:59` stays `Read` only.
- **FR-20** Installed-path rule: no `src/superclaude/...` path in any edited or new primitive; lookups name both `~/.claude/...` and project `.claude/...`.
- **FR-21** The routing block in `core/CLAUDE.md` is at most 12 lines: a call-graph question goes to callers/impact, a semantic one to auggie, a text one to Grep; do not call explore (the one always-listed tool, which the model may call unprompted); one fail-open sentence. No `@` import.
- **FR-22** Telemetry. The probe records `codegraph telemetry status` and emits `graph:telemetry_on` without blocking. Primitives never run `telemetry on` or `telemetry off` and never prefix a call with `CODEGRAPH_TELEMETRY=0`, because the prefix may defeat per-subcommand matching (INV-020). `/sc:graph status` shows the state and the user opt-out. Handoff to the installer phase: run `codegraph telemetry off` on every install path, including a binary already on PATH.
- **FR-23** Mutation exclusion. `grep -rnE 'codegraph (init|index|sync|uninit|unlock|upgrade|install|uninstall|telemetry (on|off))'` over `src/superclaude/{skills,commands,agents,core,hooks}`, including every `skills/*/scripts/` body, returns 0 hits. The single exception is `init` inside `commands/graph.md`.
- **FR-24** Kill switches. (1) Release level: the capability-map header `status: disabled`, applied as a source edit plus a release, because `superclaude install --force` erases local edits (`install_skill.py:47-52`). (2) Runtime: `codegraph` absent from PATH means the native path (NFR-07); `./update.sh` undoes it (EVAL §7 steps 2-3). (3) User level, survives updates: the probe reads `IRONCLAUDE_CODEGRAPH=off` with `printenv` and emits `graph:disabled`. Test: each switch yields `graph:disabled` or `graph:absent` and the native path.

### Non-functional

<!-- Source: Base §7 NFR-01..NFR-09 (original, modified) — NFR-01 per Change #31; NFR-02 per Change #31 (INV-011); NFR-08 per Change #17; NFR-09 per Change #11; NFR-10 per Change #14; NFR-11..NFR-13 per Change #31 (Variant A NFR-04, NFR-05; Variant C FR-07) -->
- **NFR-01** Latency per phase: probe p95 under 1 s; graph queries for 30 symbols under 15 s on a 500-file index (`query` 290 ms and `callers` 297 ms measured, EVAL §5.5); resolver cost tracked separately against the FR-06 budget (E-4). Every run logs its serial query count. `status` timing stays UNVERIFIED until measured.
- **NFR-02** Known-target query batches obey `BASH_INSPECTION_POLICY.md`: at most 15 commands per chunk, 30 s aggregate, 100 KiB output, per-command timeouts, `BEGIN/OK/NO_MATCH/FAIL` markers. Resolver calls depend on earlier output and are not batched. Codegraph mutations are never batched.
- **NFR-03** The same index and inputs give byte-identical artifacts (sorted rows).
- **NFR-04** Parsers tolerate extra lines. Golden fixtures of v1.6.2 `status`, `callers`, `impact`, `affected` and `query --json` output are tested; a mismatch yields `graph:parse_failed`, not an error.
- **NFR-05** K-1 and K-2 write only under the caller's output directory (`git status` unchanged apart from the self-ignored `.codegraph/`).
- **NFR-06** Graph text entering Claude-visible context per orchestrator run is 2K tokens or less (artifacts stay on disk, summaries inline). Measure the always-loaded explore schema overhead per session before any `CODEGRAPH_MCP_TOOLS` change.
- **NFR-07** With `codegraph` absent, every target primitive behaves exactly as its native fallback path; one test per primitive.
- **NFR-08** `affected` backtest (G-BACKTEST): at least 20 merged changes that touch indexed languages (python, yaml, liquid, EVAL §5.4), excluding Markdown-only changes; each replayed against an index built at its parent commit. Benefit: the count of affected-only tests that fail on the change, or on a seeded mutation of each changed function. Costs: median affected set of 25 files or fewer, plus collection-error and zero-collect rates. The union is enabled only when the benefit is above 0 and the costs are within the caps; otherwise the stage stays advisory.
- **NFR-09** The probe records `codegraph --version` and `pin_match`; a mismatch degrades per FR-03 and never blocks (`superclaude doctor` owns the gate, EVAL §7).
- **NFR-10** Containment: files that mention `codegraph` stay within the listed set (K-1..K-4, allowlist lines and the steps named in section 3), from today's measured baseline of 0; a test pins the count.
- **NFR-11** Mirror parity: every edited primitive with a `plugins/superclaude/` twin is edited the same way; `make verify-sync` passes.
- **NFR-12** Version honesty: the capability map states `tested_version: 1.6.2`. On each pin bump the golden fixtures, including the nested-worktree warning, are re-recorded from the live binary in the E-1 sandbox, not from saved text.
- **NFR-13** Idempotency: graph results are cached per run (one callers list per symbol per wave, one `affected` per validation cycle), and the FR-05 re-check invalidates the cache. Test: re-running a wave shows no duplicate graph calls in the audit log.

## 8. Risks, invariants and edge cases

### 8.1 Invariants

<!-- Source: Variant A §8 INV-1..INV-4 — merged per Change #30 (renamed "Invariant 1-4" to avoid a clash with INV-NNN probe IDs) -->
- **Invariant 1, fail-open:** codegraph is never on the critical path; every capability has a native floor (FR-02, NFR-07).
- **Invariant 2, re-Read before cite:** graph output is a pointer, never evidence (FR-06), matching the evidence-validator discipline (`agents/evidence-validator.md:3`) and the reuse-auditor rule "re-Read every neighbour" (`agents/reuse-auditor.md:132`).
- **Invariant 3, freshness gate unchanged:** edits still need a `Read` (`hooks/hooks.json:59`); graph reads never satisfy it (FR-19).
- **Invariant 4, single seam:** consumers never hardcode codegraph semantics that the capability map owns (K-1).

### 8.2 Risks

<!-- Source: Base §8 (original, modified) — stale-index bullet per Change #10; rollback replaced per Change #27; Markdown bullet added per Change #30 (Variant A §8) -->
- **Stale index.** Debounce is 2000 ms, and no watcher runs without an MCP client (EVAL §4). A PR that adds files can have unindexed symbols: they land in `unmapped_files[]`, and absence of dependents is not reported. FR-05 re-checks before each batch after an in-run write; E-1 decides whether that re-check can see anything without a daemon.
- **Uninitialized or nested worktree.** A sibling worktree is "not initialized" (this checkout is one); a nested one answers from the parent tree's code. Invariant: `index_root == worktree_root` or the result is discarded (FR-03), with a pointer to `/sc:graph init`.
- **Empty results.** Never evidence of absence (FR-07). Report "0 graph callers, state=<s>" and keep the native grep proof where a rule demands it (cleanup-audit `:75`).
- **Ambiguous symbols.** `query` on `install_codebase_memory_mcp` also returned a `variable` whose string matched (EVAL §5.5); `node` returns every overload. Resolve via `query --json` and require a unique kind and file match, else `ambiguous[]` and file-level scope. Whether CLI `callers` takes a file argument is UNVERIFIED until E-2; MCP `callers` does.
- **Caller-count semantics.** Rows are per caller symbol; whether two call sites in one caller give one row or two is UNVERIFIED. Reflect thresholds become "distinct production caller symbols" (FR-09), which changes the calibration from Serena's per-reference counts. G-SHADOW-REFLECT measures the shift, and the reflect change note must state it.
- **Explore noise and size.** 24,913 characters and unrelated matches (EVAL §5.6), fenced by FR-10 and FR-21.
- **Output format drift and a single-maintainer upstream.** Text output can change between releases (30 releases, 8 in about 3 months, EVAL §1). The pin is v1.6.2 (EVAL §7); golden fixtures (NFR-04, NFR-12) catch drift; a parse failure degrades rather than errors.
- **Allowlist blast radius.** One broad `Bash(codegraph *)` would pre-approve `install`, which edits Claude config and adds a prompt hook (EVAL §2, §5.9). Enforced by FR-04 and FR-23.
- **QA and review scope creep.** Dependents are context. Implement's drive-by rule (`skills/sc-implement-protocol/SKILL.md:119`) and auggie-review's out-of-hunk rule keep their meaning, except for the single gated class in FR-12 stage 3.
- **Read-only audits.** `init` writes `.codegraph/` (EVAL §2), so read-only skills (cleanup-audit, reflect, review) never init; the probe has no init mode.
- **Markdown-heavy repos.** IronClaude's primitives are Markdown, which the graph did not index (python, yaml and liquid only, EVAL §5.4). The payoff is in code repositories; `/sc:graph status` reports the counts honestly and consumers fall back without error.
- **Rollback.** Three switches (FR-24): the release-level header, the runtime binary absence, and the user-level `IRONCLAUDE_CODEGRAPH=off` that survives updates. Removing the MCP registration does not disable CLI-default consumers. No contract field is added, so reflect's CLI parser and pr-submit's FSM are untouched.
- **Policy interplay.** Serial known-target CLI queries fit `BASH_INSPECTION_POLICY.md`; ad hoc loops with command substitution do not and go through the bundled script (NFR-02).

### 8.3 Edge cases

<!-- Source: Variant C §8 edge-case table — merged per Change #30, rows corrected to the merged rules -->
| Edge case | Observed behaviour (EVAL) | Contract response |
|---|---|---|
| Sibling worktree, no init | `status` → "Not initialized" (§5.8) | `not_initialized`, fallback, pointer to `/sc:graph init` |
| Nested worktree, no init | answered from the parent index with a warning (§5.8) | `foreign_index`; nothing from it is cited (FR-03) |
| Daemon holds the writer lock | `sync` fails: "database is locked by another process" (§5.7) | No primitive calls `sync` (FR-05, D-18) |
| Symbol name in tests and source | `query` also matched a test `variable` (§5.5) | Unique kind and file match, else `ambiguous[]` |
| Caller list truncated | "Showing 20 of 23; pass --limit to widen" (§5.5) | shown/total recorded; one re-query at 100 or less (FR-08) |
| Diff touches only docs or config | `affected` maps test files only (§6.1) | An empty set is legitimate; escalation keys on source-file diffs (FR-13) |
| CLI vs MCP latency | about 290-300 ms CLI vs 3-15 ms MCP (§5.5, §5.6) | CLI in v1; logged counts feed the MCP-stage trigger (section 2.1) |
| Edits made during the run | watcher debounce 2000 ms (§4) | Latch availability once; re-check `status` before each batch after a write (FR-05) |

### 8.4 Invariant probe items and accepted risks

<!-- Source: invariant-probe.md (HIGH and MEDIUM UNADDRESSED items per refactor-plan invariant ledger; LOW items per Change #30) and debate-transcript.md Convergence Assessment -->
**INV-001 accepted risk statement.** The debate ended BLOCKED_BY_INVARIANTS: convergence 0.957 (67 of 70 points), with one HIGH item unaddressed. The freshness design assumes CLI `codegraph status` reports pending files in a session with no daemon, and EVAL never observed that. If the assumption is wrong, stale caller sets and `affected` lists pass as fresh, and re-Read does not catch counts or sets. Depth standard has no Round 3, so this document carries INV-001 as an accepted risk with this mitigation: E-1 is a blocking prerequisite (rank 1, P-01), and G-FRESH keeps every freshness-dependent idea advisory or in shadow until E-1 has run. Under Outcome B, a session with no live daemon is `stale` (FR-05).

| ID | Severity | Assumption at risk | Handling |
|---|---|---|---|
| INV-001 | HIGH | `status` sees pending files without a daemon | E-1, G-FRESH, FR-05; accepted risk above |
| INV-002 | LOW | A check right after a write gives a usable answer | Debounce rule in FR-05 |
| INV-003 | LOW | Graph data lives only for one run | `index_state` and `checked_at` on persisted numbers; stale on resume (FR-05) |
| INV-004 | MEDIUM | Provenance can be checked on any version | `provenance_unproven` on mismatch (FR-03); live-binary fixtures (NFR-12) |
| INV-005 | MEDIUM | Telemetry is off wherever the CLI runs | Accepted risk: on non-Coder hosts with a user-installed binary, CLI calls send anonymous telemetry until the installer handoff lands. Mitigation: `graph:telemetry_on` and the `/sc:graph status` pointer (FR-22) |
| INV-009 | MEDIUM | Prod-only counts are complete enough for severity | Floors; native Grep count when truncated, stale or unproven (FR-09) |
| INV-010 | MEDIUM | The prod-only count is a parity fix | G-SHADOW-REFLECT before switching |
| INV-011 | MEDIUM | 30 symbols plus resolution fit 15 s | Resolve only cited rows, 5 per symbol and 20 per run (FR-06); E-4; NFR-01 per phase |
| INV-012 | LOW | The binding match is among the `query` results | Unresolved rows are recorded and never cited (FR-06) |
| INV-013 | LOW | The shadow exemption has an enable rule | Numeric thresholds in G-SHADOW-AUGGIE |
| INV-016 | LOW | The backtest sample stands for code changes | Indexed-language sample, parent-commit index (NFR-08) |
| INV-017 | LOW | `affected` inputs exist on disk | Inputs filtered to existing paths (K-3, FR-13) |
| INV-018 | MEDIUM | An absent binary is an off switch that survives updates | User-level `IRONCLAUDE_CODEGRAPH=off` (FR-24) |
| INV-019 | MEDIUM | Exact-path script allowlists are portable | E-3; scripts only in unrestricted-Bash orchestrators until then (FR-04) |
| INV-020 | MEDIUM | Env-prefixed calls match per-subcommand patterns | No env prefixes in primitives (FR-22); E-3; accepted risk shared with INV-005 |
| INV-022 | LOW | `/sc:graph` can own `sync` | No `sync` in K-4 (D-18) |
| INV-023 | MEDIUM | The backtest can show benefit | Benefit metric redesigned (NFR-08) |
| INV-024 | MEDIUM | Span-bounded Grep plus Read finds the real call | Call-expression check, string, comment and assignment rejection, multi-match rule (FR-06) |
| INV-025 | LOW | A per-run count can switch one orchestrator to MCP | The count is evidence for one global decision (section 2.1) |

## 9. Open questions

<!-- Source: Base §9 (original, modified) + Variant A §9 Q-4, Q-8 — updated per Change #32 -->
Closed by the debate: the MCP listing question (deferred behind the trigger in section 2.1; D-28), and whether the probe should be a skill or a copied ref (orchestrators invoke K-1; agents Read its refs by installed path).

- **OQ-1 `affected` quality.** What are its recall, set size, exit codes and output format on this repo? Answered by G-BACKTEST (NFR-08).
- **OQ-2 `status` format.** Is there a stable machine-readable form (EVAL §3 lists `--json` only for `query` and `affected`)? Answered by E-2; decides parser fragility (B7).
- **OQ-3 Daemon on init.** After `codegraph init` in a worktree with a live MCP session, does the watcher start for the new index without a restart? EVAL §4 says the server picks up a new index per call, not that the watcher starts. Observed in E-1 step 5.
- **OQ-4 Non-Python changed-symbol extraction.** I-04 and I-07 map hunks to symbols through `query --json` spans. Do other indexed languages need their own rule, or file-level scope only?
- **OQ-5 Pin ownership for primitives.** Primitives run in other projects and cannot read IronClaude's pin; is "record version, `superclaude doctor` enforces" enough?
- **OQ-6 Skill-call cost.** What does invoking K-1 once per run cost in latency and tokens? UNVERIFIED.
- **OQ-7 Daemon detection.** Does the presence of `.codegraph/daemon.sock` reliably mean a live daemon? Observed in E-1 step 7.
- **OQ-8 Telemetry handoff.** When does the installer phase run `codegraph telemetry off` on every install path (FR-22)?
- **OQ-9 MCP for foreground agents.** Is `sc-cleanup-audit-protocol/SKILL.md:86` ("MCP tools are unavailable to background subagents") also true for foreground agents whose `tools:` list MCP names? Relevant once the MCP stage opens.
- **OQ-10 `affected --depth` default.** Should K-3 default to depth 1 or 2? Measured in G-BACKTEST.
