---
variant: 1
persona: architect
model: opus
type: spec
source: ../seed-brief.md
ground_truth: ../../../research/codegraph-evaluation.md (EVAL)
date: 2026-10-29
---

# Spec: where IronClaude primitives should use codegraph v1.6.2 beyond Serena replacement (architect variant)

Scope: guidance text, `tools:` / `allowed-tools:` lines, return-contract values and new primitives under `src/superclaude/{skills,commands,agents,core,hooks}`. Not in scope: the installer phase, IronClaude Python CLI code, and the 1:1 Serena SYM/REF swaps themselves (INV §4), except where this spec builds on them. Every codegraph capability below is taken from EVAL; anything else is marked UNVERIFIED. Cited `path:line` values are repo-relative to `src/superclaude/` unless they say otherwise, and were read for this spec.

## 1. Summary

- **Build one seam, not twenty inline integrations.** All codegraph use goes through one shared, installed grounding contract (`sc-graph-grounding` skill + refs: capability map, probe, citation resolution, closed degraded vocabulary). Consumers name a *capability* (callers, impact, outline, search, affected tests), not a codegraph tool. Swapping or dropping the backend (single-maintainer upstream, EVAL §1) then means editing one ref and the allowlist lines.
- **The real value is call-graph facts that no current tool gives:** inbound callers, depth-2 impact and diff-to-test mapping (`affected`). auggie has no call graph, and Grep is lexical (seed brief). Today no target primitive computes callers of changed symbols for review scope or test selection (enrichment, observation 3).
- **Citation accuracy is a net risk unless it is engineered.** Caller rows cite the caller's *definition* line (`main.py:46`, not `:255`, EVAL §5.5). The evidence-validator would flag that as `line-mismatch` (`agents/evidence-validator.md:97`). Every graph citation therefore carries a `resolution` field, and call sites are resolved with Grep plus a re-Read before they appear in a report.
- **`codegraph_explore` is token-negative for primitives:** one call returned 24,913 characters and two unrelated `install` functions (EVAL §5.6), while auggie retrieval is free on the server side. No primitive should call explore; targeted `callers`, `impact` and `node` calls replace it.
- **The highest-value consumers are:** troubleshoot Tier 1 (callers for the failing component), test selection for pr-submit VG-1 and implement as a *superset* of today's changed-area selection, reflect UC-2 regression and impact evidence, and a pre-edit impact check for symbol-changing tasks in implement and pr-submit fixes.
- **Three blockers are owned outside this phase and gate the MCP path:** (1) only `codegraph_explore` is listed by default (EVAL §3), so the registration needs `CODEGRAPH_MCP_TOOLS`; (2) per-worktree `init` has no owner; (3) CLI calls via Bash do not inherit the MCP entry's `CODEGRAPH_TELEMETRY=0`. Until those three are fixed, Bash-capable orchestrators use the CLI and read-only agents fall back to native tools.
- **Value depends on the target project's languages.** IronClaude's own primitives are Markdown. codegraph indexed Python, YAML and Liquid in the sample (EVAL §5.4), so cross-primitive references in `.md` files get nothing. The payoff is in code repositories (here, `src/superclaude/cli/`).
- **Dropped:** explore as the default retrieval step, `prompt-hook`, the tasklist tier booster, `codegraph context`, direct SQLite, graph-only DELETE proof, `node` file mode as a Read substitute, and auto-`init` from primitives (section 5).

## 2. Access model and prerequisites

### 2.1 Access path per primitive class

| Class | Members (examples) | Bash in allowlist | Default path | Second path | Change needed |
|---|---|---|---|---|---|
| A. Orchestrator skills, unrestricted Bash, enforced MCP allowlist | `skills/sc-troubleshoot-protocol` (`:4`), `skills/sc-reflect-protocol` (`:5`) | yes | MCP `mcp__codegraph__codegraph_{callers,impact,node,search,status}` when listed | CLI `codegraph callers/impact/query --json` | Add the exact MCP names to `allowed-tools`; keep Bash |
| B. Orchestrator skills, unrestricted Bash, no MCP names | `skills/sc-implement-protocol` (`:4`), `skills/sc-workflow-protocol` (`:4`), `skills/sc-tasklist-protocol` | yes | CLI | none | Body text only. workflow "Will Not … Task fan-out" (`sc-workflow-protocol/SKILL.md:74`), so it uses only the CLI inline |
| C. Orchestrator skills, scoped Bash | `skills/sc-pr-submit-protocol` (`:4` `Bash(gh *)…Bash(make *)`), `skills/sc-auggie-review-protocol` (`:4`), `skills/sc-cleanup-audit-protocol` (`:8`) | patterns only | CLI | MCP if names added | Add `Bash(codegraph *)` only where the body calls the CLI. Avoid pipelines (`git diff \| codegraph affected --stdin`): pass the files as positional args instead (`affected [files…]`, EVAL §3), because compound-command matching under scoped patterns is UNVERIFIED |
| D. Read-only agents | `agents/reuse-auditor.md:5`, `agents/troubleshoot-analyst.md:5`, `agents/reflect-reviewer.md:5`, `agents/evidence-validator.md` | no | MCP only | Read/Grep/Glob, auggie | Add the exact MCP names to `tools:`. They cannot run the CLI (seed brief constraint). Subagents do not see the MCP server instructions (EVAL §3), so the guidance must be in the agent body or in the shared ref |
| E. Commands without an allowlist | `commands/explain.md`, `commands/index-repo.md`, `commands/load.md` | session default | MCP when listed, CLI otherwise | native | Body text. `mcp-servers:` frontmatter is decorative (INV §1), so do not rely on it |
| F. Hooks | `hooks/hooks.json` | n/a (shell) | CLI `codegraph status` only | silent no-op | A new optional SessionStart status line (I-17). No change to the freshness matchers (`hooks.json:47,59`) |
| G. Core docs | `core/CLAUDE.md` | n/a | guidance | n/a | One routing row (I-18). Never the upstream `CODEGRAPH_START` block (EVAL §2) |

`affected` has no MCP tool (EVAL §3 tool table), so test selection is CLI-only in every class. Class D agents cannot select tests; that work stays with the orchestrator.

### 2.2 Blockers and owners

| ID | Blocker | Evidence | Effect if unfixed | Owner |
|---|---|---|---|---|
| B1 | Only `codegraph_explore` is listed by default; Claude Code can only call listed tools | EVAL §3 (`tools.ts:1953`) | Class A/D/E MCP path dead; A/B/C/E fall back to the CLI, D to native tools | Phase 2 registration (EVAL §7 step 5): add `"CODEGRAPH_MCP_TOOLS":"node,search,callers,callees,impact,status"` to the `env` object. Whether to also list `explore`/`files` for interactive users is Q-1 |
| B2 | A new sibling worktree is "not initialized"; nested worktrees answer from the parent index with a warning | EVAL §4, §5.8 | `graph:not_initialized` / `graph:foreign_index` degrade on every run in a fresh worktree; this repo's own `.dev/worktrees/` convention is the nested case | No owner today. Proposed: explicit `/sc:graph init` (C-4, user-invoked) plus the Coder template / `post-checkout` research (EVAL §4). Primitives never own it (FR-09) |
| B3 | The watcher runs only while an MCP client is connected; `codegraph sync` fails on the writer lock while a daemon runs | EVAL §4, §5.7 | CLI-only sessions can query a stale index; a naive `sync` step "fails" | Shared probe ref (C-1): `status` first; a lock error means the daemon owns freshness (FR-10) |
| B4 | Caller rows give the definition line, not the call site | EVAL §5.5 | Citations fail evidence-validator re-Read (`agents/evidence-validator.md:97`) | C-1 `refs/citation-resolution.md` + evidence-validator text (I-02) |
| B5 | CLI telemetry is on by default; the opt-out env lives only in the MCP entry and the Coder image | EVAL §1, §7 steps 5 and Coder image | Bash calls on a non-Coder host send telemetry | Phase 2 installer: run `codegraph telemetry off` (persists in `~/.codegraph/telemetry.json`, EVAL §2) on the fallback path. The probe records `codegraph telemetry status` and marks `graph:telemetry_on` without blocking |
| B6 | Scoped-Bash skills lack `Bash(codegraph *)`; read-only agents lack MCP names | `sc-pr-submit-protocol/SKILL.md:4`, `sc-auggie-review-protocol/SKILL.md:4`, `agents/reuse-auditor.md:5` | Step silently unavailable | This phase (allowlist edits); the test pin on `troubleshoot-analyst.md:5` (INV §1) moves with it |
| B7 | `codegraph_node` file mode is not a `Read`, so the freshness gate does not see it | `hooks.json:59` matcher `Read` → `freshness-post-read.sh` | An edit after a node-only "read" is blocked or, worse, done unread | Invariant INV-3; no hook change |

## 3. Ideas

Value: H/M/L. Effort: S (text and allowlist edits in 1-2 files), M (several files or a contract field), L (new primitive with tests). "Fallback" is the named native path; each one also records a degraded token (§7 FR-03).

| ID | Idea | Vector(s) | Target primitive(s) | codegraph mechanism | Expected value | Effort | Risk | Native fallback |
|---|---|---|---|---|---|---|---|---|
| I-01 | Shared grounding contract: capability map (capability → MCP tool / CLI subcommand / fallback), one probe per run, closed degraded vocabulary, kill switch | all | new `skills/sc-graph-grounding/` (C-1); consumers reference `~/.claude/skills/sc-graph-grounding/refs/…` then `.claude/skills/…` | `codegraph_status` / `codegraph status`, `codegraph --version` | H: one place to change, consistent fail-open, backend swap without editing consumers | M | L | the capability map's own fallback column |
| I-02 | Citation resolution: tag every graph row `resolution: def-line`; resolve the call site by Grep for the callee name inside the caller's file, after the def line, then re-Read; the validator verifies def-line rows only as definitions | accuracy | C-1 `refs/citation-resolution.md`; `agents/evidence-validator.md`; reflect hallucination contract | `codegraph_callers {symbol, file, limit}` → rows; `codegraph query <s> --json` gives `startLine`/`endLine` (EVAL §5.5) to bound the search | H: removes the main way graph data could corrupt reports | S | L | Grep `-n` + Read |
| I-03 | Allowlists: add exact `mcp__codegraph__codegraph_{callers,impact,node,search,status}` names to Class A/D lines, and `Bash(codegraph *)` to Class C where used; never `codegraph_explore` | all (enabler) | `skills/sc-troubleshoot-protocol/SKILL.md:4`, `skills/sc-reflect-protocol/SKILL.md:5`, `agents/{reuse-auditor,troubleshoot-analyst,reflect-reviewer}.md:5`, `skills/sc-pr-submit-protocol/SKILL.md:4`, `skills/sc-auggie-review-protocol/SKILL.md:4`, `skills/sc-cleanup-audit-protocol/SKILL.md:8` | n/a | H: without it, D-class use is impossible | S | M (test pins, B1 dependency) | n/a |
| I-04 | Troubleshoot Tier 1: for a named or found symbol, add `callers` (limit 10) next to auggie; Wave 1.6 Branch A "immediate callers" (`:286`) comes from callers, not Grep guesses; the producers table gets resolved call sites | troubleshooting, accuracy, token | `skills/sc-troubleshoot-protocol/SKILL.md:191-194,286`; `commands/troubleshoot.md`; `agents/troubleshoot-analyst.md` | `codegraph_search {query, kind:"function"}`, `codegraph_node {symbol, file, includeCode:true}`, `codegraph_callers {symbol, file, limit:10}` | H: exact caller set within the ≤~3k Wave 1 budget (`:218`), not grep sprawl | S | L | auggie + Glob/Grep (`:194`) |
| I-05 | Implement pre-edit impact: when a task renames, deletes or changes the signature of an existing symbol, Q1 runs impact; callers' files join the Q3 review package as read-only context; the ledger records `impact=<n callers, m files>` | impact before edits, planning | `skills/sc-implement-protocol/SKILL.md:118-122` (Q1/Q2) + `refs/qa.md` | C-2 `/sc:impact <symbol> --file <f> --depth 2` (CLI `codegraph impact <s> --depth 2`, `codegraph callers <s>`) | H: catches unupdated call sites, which spec-compliance QA cannot see | M | M (noise on hub symbols; needs a cap) | Grep for the symbol name, marked `graph:absent` |
| I-06 | Test selection superset: VG-1 runs `changed-area ∪ affected`; implement's optional test extra uses the same skill | test selection | `skills/sc-pr-submit-protocol/SKILL.md:206-207`; `skills/sc-implement-protocol/SKILL.md:9` | C-3 → `codegraph affected <files…> --json --depth 2` | M: finds tests outside the changed directory that depend on changed files; never narrows today's set | S | L | today's `<changed-area>`; VG-2 `make test` still escalates |
| I-07 | Reflect transitive impact: Step 1B.3 overlap edges and step 4 downstream impact use `callers` plus `impact depth 2`; severity counts *resolved call sites* (I-02), or labels the count `caller_functions` | reflection/audit, accuracy | `skills/sc-reflect-protocol/SKILL.md:344,347,514,516` | `codegraph_callers`, `codegraph_impact {symbol, file, depth:2}` | H: reflect is the heaviest consumer (INV §1); adds transitive reach Serena lacked | M | M (contract fields owned by the reflect CLI; changed severity semantics) | Grep reference count, `graph:absent` |
| I-08 | Reflect UC-2 regression evidence: tests mapped to touched files; flag "touched code has mapped tests that were neither changed nor run" | reflection/audit, test selection | `skills/sc-reflect-protocol/SKILL.md` (UC-2 regression category) | C-3 (`codegraph affected <touched…> --json`) | M: grounds the Regression category in a concrete artifact | S | L | path heuristic `tests/**/test_<module>*` |
| I-09 | Auggie-review blast-radius note: map diff hunks to changed symbols, get their callers, give them to the Claude validation step as context only; findings outside hunks keep today's downgrade | review scoping | `skills/sc-auggie-review-protocol/SKILL.md:126-138` (+ the out-of-hunk rule) | `codegraph_node {file, symbolsOnly:true}` × hunk ranges (IronClaude-side mapping; codegraph has no diff-to-symbol mapping, EVAL §6.1), then `codegraph_callers` | M-L: auggie already retrieves semantically; the gain is a definite list of external callers | M | M (prompt bloat; line ranges in `symbolsOnly` output UNVERIFIED) | none needed: skip the note |
| I-10 | Pre-fix impact in remediation chains: pr-submit Wave 4 (L2+, before applying edits) and the troubleshoot `--fix` handoff include the C-2 report for symbols the fix touches | impact before edits, review scoping | `skills/sc-pr-submit-protocol/SKILL.md:194`; troubleshoot Tier 3 handoff | C-2 `/sc:impact` | M: stops an auto-fix from breaking callers outside the PR diff | S | L | Grep |
| I-11 | Reuse-auditor: (a) callers of a neighbour as liveness evidence (a reuse-by-import target must be live); (b) `search {kind}` replaces Serena name-token search in the auggie-down fallback, keeping the advisory cap | reflection/audit | `agents/reuse-auditor.md:5,126,130-132` | `codegraph_callers {symbol, file, limit:5}`, `codegraph_search {query, kind, limit}` | M: stops recommending reuse of dead code | S | L | ripgrep skeleton grep (`:131`) |
| I-12 | Cleanup-audit KEEP/DELETE corroboration: in the orchestrator only, zero graph callers is extra evidence for DELETE, never a substitute for grep proof; nonzero callers give the KEEP reference citation | reflection/audit, accuracy | `skills/sc-cleanup-audit-protocol/SKILL.md:75,83,86` | `codegraph callers <s>` (CLI; Class C) | L-M: graph misses dynamic loading and string references, so it can only add confidence | S | M (false "dead" signal if misused) | grep proof (`:75`) |
| I-13 | Workflow blast-radius inputs: when the source names existing symbols, Wave 1 records the impact counts and each task's acceptance criteria name the caller files to update | planning | `skills/sc-workflow-protocol/SKILL.md` Wave 1 | `codegraph impact <s> --depth 2` (CLI) | M: plans stop missing "update callers" tasks | M | M (prompt-only sources name no symbols; skip) | none: omit the field |
| I-14 | Explain one-hop context: for a code target, show its definition, callers and callees, so the explanation covers how the code is used | onboarding, token | `commands/explain.md:48` | `codegraph_node {symbol, includeCode:true}`, `codegraph_callers`/`codegraph_callees {limit:10}` | M: replaces a whole-file Read with one symbol | S | L | Read/Grep (`:48`) |
| I-15 | Index-repo graph stats: add a "Graph" section (files, node kinds, languages) to `PROJECT_INDEX.md` | onboarding | `commands/index-repo.md:19` (Phase 1) | `codegraph status`; `codegraph_files {format:"grouped", maxDepth:2}` | L: Glob already gives the structure; no layers or hotspots (EVAL §6.1) | S | M (a persisted doc goes stale) | the 5 Globs |
| I-16 | Load graph status: `/sc:load` reports `index_state` as one line, filling the Serena ACT job | onboarding | `commands/load.md:27` | C-4 `/sc:graph status` | L-M | S | L | "graph: absent" |
| I-17 | SessionStart status line: in an indexed repo, print at most one line (`codegraph: fresh | pending N | not initialized → /sc:graph init`); silent when the CLI is absent or the repo is not a git checkout | freshness, onboarding | `hooks/hooks.json` SessionStart; new `hooks/scripts/codegraph-status.sh` | `codegraph status` (~300 ms, EVAL §5.5) | M: makes the unowned per-worktree `init` (B2) visible | S | M (latency on every start; must time out at ≤1-2 s) | silent no-op |
| I-18 | Core routing row: one row in the `core/CLAUDE.md` MCP table on when to use callers/impact (graph), auggie (semantic) and Grep (text) | token, accuracy | `core/CLAUDE.md` | guidance only | M: interactive sessions stop defaulting to explore | S | L | n/a |
| I-19 | `/sc:graph` lifecycle command (status, explicit init, sync) | freshness (enabler) | new `commands/graph.md` (C-4) | `codegraph status`, `init --yes`, `sync` | M: a named owner for B2 at user level | S | M (`init` writes 34 MB and peaks near 1 GB RSS, EVAL §5.4) | n/a |

## 4. Ranked list

Method: two layers. **Layer 0** holds hard prerequisites, ordered by dependency: other ideas cannot work without them. **Layer 1** is ranked by `score = Value × Frequency ÷ (Effort × Risk)` with V H=3, M=2, L=1 (M-L=1.5, L-M=1.5), Frequency = how often the host primitive runs (3 = level-3 path or every PR, 2 = common, 1 = occasional), Effort S=1, M=2, L=3, Risk L=1, M=1.5. Ties are broken by fewer blockers.

Layer 0:
1. **I-03 allowlists** — without exact names nothing in Class A/D can call a tool; it also forces the B1 listing decision.
2. **I-01 shared grounding contract** — the seam every consumer references; owns probe, vocabulary and kill switch.
3. **I-02 citation resolution** — ships inside I-01; without it every graph citation is a validator failure (B4).

Layer 1:
4. **I-04 troubleshoot Tier 1 callers** — 3×3/(1×1)=9: frequent, tiny edit, fixes a vague "immediate callers" step.
5. **I-06 test-selection superset** — 2×3/(1×1)=6: every PR runs VG-1, and the superset rule makes it safe.
6. **I-08 reflect regression evidence** — 2×3/(1×1)=6: reflect runs at the end of every workflow; reuses C-3.
7. **I-18 core routing row** — 2×3/(1×1)=6: cheapest way to stop explore-by-default in every session.
8. **I-10 pre-fix impact** — 2×2/(1×1)=4: small once C-2 exists; guards auto-applied fixes.
9. **I-11 reuse-auditor liveness** — 2×2/(1×1)=4: closes a real false-recommendation class.
10. **I-14 explain one-hop** — 2×2/(1×1)=4: token-positive onboarding.
11. **I-19 /sc:graph** — 2×2/(1×1)=4 at Risk L for status, but `init` is M; ranked below the read-only items.
12. **I-17 SessionStart status line** — 2×3/(1×1.5)=4: visible freshness, at the price of per-session latency.
13. **I-05 implement pre-edit impact** — 3×3/(2×1.5)=3: highest standalone value, held back by effort and hub-symbol noise.
14. **I-07 reflect transitive impact** — 3×3/(2×1.5)=3: high value, but it changes CLI-parsed contract fields owned elsewhere.
15. **I-13 workflow blast radius** — 2×3/(2×1.5)=2.
16. **I-16 load graph status** — 1.5×2/(1×1)=3 by formula, demoted to 16 because it duplicates I-17/I-19 output.
17. **I-09 auggie-review blast-radius note** — 1.5×2/(2×1.5)=1: depends on an UNVERIFIED line-range output and competes with free auggie retrieval.
18. **I-12 cleanup-audit corroboration** — 1.5×1/(1×1.5)=1: low frequency, misuse risk.
19. **I-15 index-repo stats** — 1×1/(1×1.5)=0.7: little that Glob does not already give.

## 5. Dropped ideas

| ID | Idea | Reason |
|---|---|---|
| D-01 | `codegraph_explore` as the default grounding or explain step | Token-negative: 24,913 characters per call with unrelated matches (EVAL §5.6), while auggie is free on the server side. Targeted callers/node calls give the same facts in a few hundred tokens. Not in any `tools:` line (FR-05) |
| D-02 | Upstream `prompt-hook` / `codegraph install` | Rejected in EVAL §5.9 and §7: it injects an explore payload into every prompt, and the CLAUDE.md block is erased by `superclaude install` |
| D-03 | Graph-derived blast radius in the tasklist ">2 files affected" booster (`sc-tasklist-protocol/SKILL.md:1326`) | The tasklist generator is deterministic; tiering would then depend on local index state and stop being reproducible |
| D-04 | `codegraph context <task…>` for planning | It exists in the CLI (EVAL §3), but its output size and shape were never measured. Re-propose after a measurement |
| D-05 | Direct SQLite queries for hotspots, cycles or Cypher-like analysis | Schema UNVERIFIED (EVAL §6.1); seed constraint forbids relying on it |
| D-06 | Zero graph callers as sole DELETE proof | No text search, no data flow, misses dynamic and string dispatch (EVAL §6); contradicts `sc-cleanup-audit-protocol/SKILL.md:75` |
| D-07 | `codegraph_node` file mode as a Read replacement | Not a tracked `Read` for the freshness hook (`hooks/hooks.json:59`); saves little over Read with offset/limit |
| D-08 | Primitives auto-running `codegraph init`/`index` | Mutation (34 MB, ~1 GB RSS, EVAL §5.4) inside read-only flows; violates fail-open-without-side-effects; owner is the user or image (B2) |
| D-09 | Graph-based review chunking for auggie-review (cluster per chunk) | No clusters or layers in codegraph (EVAL §6.1) |
| D-10 | Replace reflect's LSP diagnostics leg with codegraph | No diagnostics (EVAL §6.2); keep scoped tests and linters (INV §4 DIAG) |
| D-11 | Adding codegraph tools to the freshness matchers (`hooks.json:47`) | All codegraph tools are read-only (EVAL §3); nothing to gate |
| D-12 | A `graph-scout` subagent to absorb explore output | Only useful if explore is used (D-01); `sc-cleanup-audit-protocol/SKILL.md:86` also states MCP is unavailable to background subagents, which makes the design fragile |

## 6. Candidate new commands or skills

All four reference each other only through installed paths (`~/.claude/skills/<name>/…`, `~/.claude/commands/sc/<name>.md`), with the project `.claude/` copy as the dual surface. None references `src/superclaude/`.

**C-1 `sc-graph-grounding`** (kind: skill, delegate-only, no slash command; plus refs that read-only agents load by path)
- Purpose: the single seam. It owns the capability map, the probe, citation resolution and the degraded vocabulary.
- Files: `SKILL.md` (procedure for orchestrators), `refs/capability-map.md` (row per capability: `callers | impact | outline | definition | search | affected_tests | status` → MCP tool + args, CLI subcommand + args, native fallback, known gaps; header `status: enabled|disabled`, `tested_version: 1.6.2`), `refs/probe.md`, `refs/citation-resolution.md`, `refs/degraded-vocab.md`.
- Interface (Skill args): `--need <capability>[,…] --target <symbol|file> [--file <path>] [--depth 1-3] [--limit N]`.
- Output contract (`graph-facts.yaml`, or returned inline): `graph_access: mcp|cli|none`, `index_state: fresh|pending|not_initialized|foreign_index|absent|disabled`, `cli_version`, `degraded: [<vocab tokens>]`, `facts: [{capability, symbol, file, def_line, call_site_line|null, resolution: def-line|call-site-verified|unresolved, source: codegraph|grep|auggie}]`, `truncated: bool`, `query_ms`.
- Callers: sc-troubleshoot-protocol (W1, W1.6), sc-reflect-protocol (1B.3, step 4), sc-implement-protocol (Q1 through C-2), sc-pr-submit-protocol (Wave 4 through C-2, VG-1 through C-3); agents reuse-auditor, troubleshoot-analyst, reflect-reviewer read `refs/capability-map.md` + `refs/citation-resolution.md` directly.
- Tools: `codegraph_status`, `codegraph_search`, `codegraph_node`, `codegraph_callers`, `codegraph_callees`, `codegraph_impact`; CLI `status`, `query --json`, `callers`, `impact --depth`, `--version`.
- Fallback: per row in the capability map; `none` access → native facts with `source: grep|auggie`.
- Effort: M.

**C-2 `/sc:impact`** (kind: command; runs from its own file, no protocol skill)
- Purpose: pre-edit blast radius for a symbol, a file or a diff.
- Interface: `/sc:impact <symbol> [--file <path>] | --file <path> | --diff [<base>]` `[--depth 1-3 (default 2)] [--limit N (default 20, max 100)] [--tests] [--output <dir>]`.
- Output: `impact.md` + `impact.yaml`: `targets[] {symbol, file, def_line}`, `mapping: given|diff-hunk-to-symbol` (diff mode is IronClaude-side mapping, labelled, because codegraph has none), `callers[] {symbol, file, def_line, call_site_line, resolution}`, `reach {depth, symbol_count, files[]}`, `affected_tests[]` (with `--tests`, via C-3), `index_state`, `degraded[]`, `citations_verified: n/m`, `truncated`.
- Callers: sc-implement-protocol Q1 (symbol-changing tasks), sc-pr-submit-protocol Wave 4 (L2+, before applying edits), the sc-troubleshoot-protocol `--fix` handoff, sc-workflow-protocol Wave 1 (CLI form only, optional), interactive users.
- Tools: through C-1 (`callers`, `impact`, `node symbolsOnly`).
- Fallback: Grep for the symbol name → `callers[]` with `source: grep`, `reach` omitted, `degraded: [graph:absent]`.
- Effort: M.

**C-3 `sc-test-scope`** (kind: skill, delegate-only)
- Purpose: map changed files to tests as a safe superset of today's selection.
- Interface: `--files <list> | --diff <base>` `[--depth N] [--filter <glob>]`.
- Output (`test-scope.yaml`): `changed_files[]`, `heuristic_tests[]` (changed-area rule), `affected_tests[]` (`codegraph affected <files…> --json`), `selected[] = heuristic ∪ affected`, `selection_source: union|heuristic_only`, `pytest_args`, `degraded[]`, `index_state`.
- Callers: sc-pr-submit-protocol VG-1, sc-implement-protocol (optional test extra), sc-reflect-protocol UC-2 regression evidence, C-2 `--tests`.
- Tools: CLI `affected` only (it has no MCP tool).
- Fallback: `heuristic_only`.
- Effort: S-M.

**C-4 `/sc:graph`** (kind: command)
- Purpose: user-level lifecycle and an owner for the per-worktree index (B2).
- Interface: `/sc:graph [status|init|sync]` (default `status`). `init` runs only when the user typed it, and refuses with a message when the current tree is a nested worktree unless the user also passes `--worktree-local` (it then runs `codegraph init -i`, EVAL §5.8).
- Output: `cli_version`, `pin: v1.6.2`, `pin_match`, `index_state`, `worktree_relation: own|parent|none`, `files/nodes/edges`, `pending[]`, `daemon: running|absent|unknown` (inferred from a sync lock error), `listed_tools[]` (the `mcp__codegraph__*` names present in this session), `telemetry: on|off`, `next_action`.
- Callers: `/sc:load` (status), the I-17 hook text, degraded messages from C-1.
- Tools: CLI `status`, `init --yes`, `sync`, `telemetry status`, `--version`.
- Fallback: "codegraph not installed" plus the install pointer. Never STOP the caller.
- Effort: S.

## 7. Requirements

Functional:
- **FR-01** Every primitive that uses codegraph reaches it through C-1 or C-2/C-3 and names the refs by installed path then the project `.claude/` path. Test: grep the target primitives for `sc-graph-grounding`; `grep -rn 'src/superclaude'` over the new primitives returns 0.
- **FR-02** A run probes once (`status` + `--version`) and records `graph_access` and `index_state` in the host's audit log or return contract. Test: fixture run with codegraph absent records `index_state: absent`.
- **FR-03** Each codegraph step names its native fallback in the same step and emits one token from the closed vocabulary `graph:{absent,disabled,unlisted,not_initialized,foreign_index,stale,version_mismatch,telemetry_on,empty,ambiguous,truncated}`; no step STOPs or asks the user because of graph state. Test: grep each step for a fallback verb and a vocabulary token; no new STOP code mentions codegraph.
- **FR-04** Graph caller rows enter reports only with `resolution`; `def-line` rows are cited as definitions, never as call sites; `call-site-verified` rows have been re-Read in the current run. Test: evidence-validator fixture with a def-line row cited as a call site → `line-mismatch`.
- **FR-05** No `tools:`/`allowed-tools:` line and no step body names `codegraph_explore`. Test: `grep -rn codegraph_explore src/superclaude/{skills,commands,agents,core,hooks}` matches only C-1's capability map "do not use" note.
- **FR-06** Class A/D allowlists add exact names only for tools their body calls; Class C adds `Bash(codegraph *)` only where the CLI is called. Test: for each allowlist entry, the body has a matching call (and the reverse).
- **FR-07** C-3 `selected ⊇ heuristic_tests` always. Test: unit fixture where `affected` returns a disjoint set → `selected` contains both.
- **FR-08** Severity in reflect 1B.3 uses resolved call-site counts, or the contract labels the number `caller_functions`. Test: contract fixture field name.
- **FR-09** No primitive except C-4 under an explicit user `init` runs `codegraph init|index|uninit|upgrade|install`. Test: grep.
- **FR-10** A `codegraph sync` lock failure ("could not acquire the file lock", EVAL §5.7) is recorded as `daemon: running` with freshness owned by the daemon, not as an error. Test: probe ref text plus a fixture string.
- **FR-11** A foreign-index warning ("belongs to a different git working tree", EVAL §5.8) is treated as `graph:foreign_index`: no facts from it are cited and the fallback runs. Test: fixture output → fallback path.
- **FR-12** Cleanup-audit DELETE still requires grep proof (`sc-cleanup-audit-protocol/SKILL.md:75`); graph evidence appears only as corroboration. Test: text check.
- **FR-13** C-2 `--diff` labels the hunk-to-symbol mapping `mapping: diff-hunk-to-symbol` and never claims it came from codegraph.
- **FR-14** `core/CLAUDE.md` gains one routing row; no `CODEGRAPH_START` marker and no `prompt-hook` appear in `core/` or `hooks/`. Test: grep.
- **FR-15** The I-17 hook prints at most one line, is silent when `codegraph` is not on PATH or the cwd has no `.codegraph/`, and has a timeout ≤ 2 s in `hooks.json`.
- **FR-16** When `refs/capability-map.md` says `status: disabled`, every consumer takes its fallback with `graph:disabled`. Test: flip the header in a fixture and check the consumer audit line.

Non-functional:
- **NFR-01 Token budget** Per graph call: `limit ≤ 20` (callers), `depth ≤ 2` by default, `depth 3` only through explicit C-2 args. Troubleshoot Wave 1 stays within its ≤~3k target (`sc-troubleshoot-protocol/SKILL.md:218`).
- **NFR-02 Latency** One probe per run (one `status` ≈ 300 ms CLI, EVAL §5.5); MCP preferred where listed (3-15 ms per call, EVAL §5.6).
- **NFR-03 Containment** The codegraph tool and CLI names appear only in C-1 refs, C-2/C-3/C-4 bodies, allowlist lines and the named steps. Test: a count of files containing `codegraph` stays within the listed set (pinned in a test).
- **NFR-04 Mirror parity** Every edited primitive that has a `plugins/superclaude/` twin is edited the same way (INV §1); `make verify-sync` passes.
- **NFR-05 Version honesty** C-1 states `tested_version: 1.6.2`; a different `codegraph --version` gives `graph:version_mismatch` and the run continues.
- **NFR-06 Determinism** `sc-tasklist-protocol` output does not depend on graph state (D-03).
- **NFR-07 No new side effects** Apart from C-4 `init`/`sync`, codegraph use writes nothing outside the host primitive's existing output directory.
- **NFR-08 Rollback cost** Removing the codegraph registration, or setting `status: disabled`, makes every consumer degrade with no further edits.

## 8. Risks, invariants and edge cases

Invariants:
- **INV-1 Fail-open:** codegraph is never on the critical path; every capability has a native floor.
- **INV-2 Re-Read before cite:** graph output is a pointer, never evidence. This matches the evidence-validator discipline (`agents/evidence-validator.md:3`) and the reuse-auditor rule "re-Read every neighbour" (`agents/reuse-auditor.md:132`); graph data therefore never conflicts with re-Read, as long as I-02 holds.
- **INV-3 Freshness gate unchanged:** edits still need a `Read` (`hooks/hooks.json:59`); graph reads never satisfy it.
- **INV-4 Single seam:** consumers never hardcode codegraph semantics that the capability map owns.

Edge cases:
- **Stale index.** If no MCP client ran, the CLI may answer from an old index. The probe reads the `status` pending list: if files are pending, try one `sync`; a lock error means a daemon is live (FR-10); otherwise mark `graph:stale` and resolve every cited row through Grep/Read (cheap, because I-02 already requires it).
- **Uninitialized sibling worktree.** `not_initialized` → fallback, with one pointer to `/sc:graph init`. Never auto-init (D-08).
- **Nested worktree** (this repo's `.dev/worktrees/` layout). The parent index plus warning means facts describe another tree → `foreign_index`, cite nothing (FR-11).
- **Empty results.** Zero callers can mean dead code, dynamic dispatch, registries or decorators, CLI entry points, string invocation, files over 1 MB, gitignored files or unsupported languages (EVAL §4). Record `graph:empty`; never infer "unused" from it (D-06).
- **Ambiguous symbols.** There is no `Class/method` name-path addressing (EVAL §6.2). Always pass `file` when it is known. When several matches remain, record `graph:ambiguous`, disambiguate with `search {kind}` plus `file`, and otherwise fall back.
- **Hub symbols.** Impact on a widely used helper can hit `limit`. Record `truncated: true` with the total count ("Showing 20 of 23", EVAL §5.5), and do not add every caller file to the review package (I-05 cap: 10 files).
- **Explore noise.** It is excluded from primitives (D-01). If a user lists it (Q-1), interactive use stays with the user.
- **Markdown-heavy repos.** Little or no graph signal. The I-17 hook and C-4 report the counts honestly; consumers fall back without error.
- **Old daemon, new client.** Untested (EVAL §7 follow-ups) → treat any unexpected error text as `graph:absent` for the run.
- **Telemetry.** Bash CLI calls on a host without the opt-out (B5) send telemetry. The probe surfaces `telemetry: on`; this phase does not silently change user config.
- **Single-maintainer upstream** (EVAL §1). Pin v1.6.2; INV-4 limits a backend swap to C-1 refs plus allowlists. 8 releases per quarter means the capability map is re-validated on every pin bump.
- **Rollback.** All changes are text and allowlists. Revert the PR, or set `status: disabled`. Because of INV-1, removing the MCP registration alone already degrades cleanly (NFR-08).

## 9. Open questions

- **Q-1** Should the B1 listing include `explore` and `files` for interactive users, given that an explicit `CODEGRAPH_MCP_TOOLS` allowlist then blocks unlisted tools for everyone (EVAL §3)? This variant lists only `node,search,callers,callees,impact,status`.
- **Q-2** Does Claude Code's permission matching accept a pipeline under `Bash(codegraph *)` + `Bash(git *)`? Until that is verified, C-3 passes files as positional args.
- **Q-3** Does `codegraph_node {file, symbolsOnly:true}` return end lines? I-09 and C-2 `--diff` need ranges; the fallback is the next symbol's start line, or `query --json` `endLine`.
- **Q-4** Is `sc-cleanup-audit-protocol/SKILL.md:86` ("MCP tools are unavailable to background subagents") still true for foreground `Task` agents whose `tools:` list includes MCP names? reuse-auditor already relies on auggie that way. The answer decides whether Class D agents can use codegraph at all.
- **Q-5** Who owns `codegraph telemetry off` on the IronClaude fallback-install path (B5): the installer phase or `/sc:graph`?
- **Q-6** Do reflect's CLI-parsed contract fields accept a `caller_functions` vs `call_sites` distinction (FR-08), or must it collapse into `degraded_components` (INV §4 CONTRACT hint)?
- **Q-7** Should `codegraph context <task…>` be measured (size, noise) before D-04 is final?
- **Q-8** Should C-3 `affected --depth` default to 1 or 2? Depth 2 widens test runs; the right value needs a measurement on `tests/cli/`.
