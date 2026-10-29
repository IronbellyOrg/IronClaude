# Diff Analysis: decision-option Comparison (P3 command set)

## Metadata
- Generated: 2026-10-29T18:05:00Z
- Variants compared: 3
  - Variant A = `option-a.md` (three commands: `/sc:impact`, `/sc:test-scope`, `/sc:graph`)
  - Variant B = `option-b.md` (skill `sc-graph-grounding` + `/sc:impact` with tests + `/sc:graph`)
  - Variant C = `option-c.md` (two commands: `/sc:impact` with tests, `/sc:graph`; core guide as seam)
- Grounding sources: CTX = `decisions/P3-command-set/context.md`; EVAL = `research/codegraph-evaluation.md`; BRS = `brainstorm/P3-codegraph-opportunities/merged-requirements.md` §6-8; SPEC = `specs/phase-3-codegraph-adoption-spec.md` §4 (checked only to verify a claim Variant C makes, "the guide is already planned (spec §4)")
- Total differences found: 30 (diff points in the convergence denominator: 23 = S 4 + C 9 + X 4 + A 6)
- Categories: structural (4), content (9), contradictions (4), unique (7), shared assumptions (6)

## Structural Differences

| # | Area | Variant A | Variant B | Variant C | Severity |
|---|------|-----------|-----------|-----------|----------|
| S-001 | Heading names | "Commands", "Callers", "Strengths", "Weaknesses" | "Commands and skills", then same | "Commands", then same; plus an unheaded paragraph "No new skill for shared semantics" | Low |
| S-002 | Number and kind of new units | 3 slash commands | 1 delegate-only skill + 2 slash commands | 2 slash commands | High |
| S-003 | Callers section granularity | One bullet per command, three commands | Skill callers listed by name; `/sc:impact` "as in option A plus" test callers (refers to another document) | One bullet per command with step IDs (Q1, Q6, VG-1, 1B.3, UC-2) | Low |
| S-004 | Interface specification depth | Flags listed, no defaults, no fallback in the command line | Flags listed, no defaults; fallback lives in the skill | Defaults given (`--depth 1-3, default 2`, `--limit N, default 20`); fallback (`status: partial`) written into the command entry | Medium |

## Content Differences

| # | Topic | Variant A Approach | Variant B Approach | Variant C Approach | Severity |
|---|-------|-------------------|-------------------|-------------------|----------|
| C-001 | Where shared codegraph semantics live (the seam) | Core guide `~/.claude/CODEGRAPH.md` (readiness labels, read-before-cite, fail-open) | Skill `sc-graph-grounding` (probe, capability map, citation contract, closed `graph:*` vocabulary, resolver script), run as "Step 0" by every consumer | Core guide `~/.claude/CODEGRAPH.md`, plus the call-site rule; each protocol cites it | High |
| C-002 | Test selection | Separate `/sc:test-scope --files|--diff`: path heuristic plus `codegraph affected`, labelled an advisory superset, each test's source recorded | Folded into `/sc:impact --tests` (`codegraph affected` list) | Folded into `/sc:impact --tests` (`affected` plus the path heuristic); no advisory label | High |
| C-003 | Call-site resolution (EVAL §5.5: caller rows give the definition line) | "each cited row re-Read"; no step that finds the call-site line | `resolve-callsite.sh` script turns a definition line into Read-verified call-site lines | Written procedure: Grep inside the caller's span, then Read | Medium |
| C-004 | `/sc:impact` input modes | `<symbol> | --file <path> | --diff [<base>]` | Same as A | `<symbol>... | --diff [<base>]` (several symbols; no `--file`) | Medium |
| C-005 | Behaviour with no codegraph or no index | "fail-open" named as a guide rule; no per-command result | `graph:*` degraded token from the skill's closed vocabulary; result shape not stated | `status: partial`, Grep-based results, `degraded: [codegraph]`; "never stops the caller" | Medium |
| C-006 | Readiness probe used by callers | `/sc:graph status` is "every caller's readiness probe" | Skill probe once per run (readiness, worktree provenance, version, telemetry) | `/sc:graph status --output-dir <dir>` or "simply read the guide's one-call readiness check" | Medium |
| C-007 | `/sc:graph` machine output | `return-contract.yaml` when `--output-dir` is given | Not stated ("user-facing readiness") | `--output-dir <dir>` flag in the signature | Low |
| C-008 | Caller coverage | `/sc:test` named as a `/sc:test-scope` caller; no cleanup-audit, explain or load | Skill callers add cleanup-audit, explain, load | Only `/sc:impact` callers plus `/sc:load` as a `/sc:graph` reference | Medium |
| C-009 | Meaning of `--depth` when tests are folded in | `/sc:impact --depth 1-3` and `/sc:test-scope --depth N` are separate flags | One `--depth` on `/sc:impact`; whether it also drives `affected --depth` is not stated | One `--depth 1-3, default 2`; same gap as B | Medium |

## Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Variant C Position | Impact |
|---|-------------------|-------------------|-------------------|-------------------|--------|
| X-001 | Must every consumer run a skill-based probe? BRS FR-01: "Each consuming primitive MUST run K-1 once per run". SPEC §4 (P3-D2) decides a core doc instead | Rules in the guide, not in a skill (contradicts BRS FR-01) | Keeps FR-01 (skill is "Step 0") but concedes "the guide plus Read already enforces read-before-cite" (intra-variant tension) | No new skill (contradicts BRS FR-01; matches SPEC §4) | High |
| X-002 | Per-run invocation cost | Every caller probes via `/sc:graph status`, a command invocation, without stating its cost | Lists the per-run skill cost as a weakness (BRS OQ-6, UNVERIFIED) | Claims "No per-run skill invocation" as a strength, yet callers may probe through `/sc:graph status --output-dir`, and every caller invokes `/sc:impact` | Medium |
| X-003 | Degraded marker form | Not specified | Closed `graph:*` vocabulary (matches BRS FR-02) | `degraded: [codegraph]` (a token outside the BRS FR-02 closed set) | Medium |
| X-004 | Overlap of `--tests` and `/sc:test-scope` | Keeps `/sc:impact --tests` and `/sc:test-scope`; concedes duplication "unless it calls it" (unresolved inside A) | n/a (single home) | n/a (single home) | Low |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | A | A standalone `/sc:test-scope` that callers can use without dependents; `/sc:test` named as a caller | Medium |
| U-002 | B | `resolve-callsite.sh`, aimed at the measured definition-line gap (EVAL §5.5) | High (gap measured; the script's reliability is UNVERIFIED) |
| U-003 | B | Closed `graph:*` degraded vocabulary and a capability-map ref (BRS FR-02, K-1) | Medium |
| U-004 | B | Probe records worktree provenance, version and telemetry (BRS FR-03, FR-22, NFR-09) | Medium |
| U-005 | C | Concrete defaults (`--depth` 2, `--limit` 20), several symbols per call, and an explicit fail-open result (`status: partial` with Grep results) | High |
| U-006 | C | Call-site confirmation as a written Grep-in-span-then-Read procedure (the BRS FR-06 method without the script) | Medium |
| U-007 | A | Per-test `source` recorded and an "advisory superset" label (BRS K-3 `selection_source`, FR-13 stage 0) | Medium |

## Shared Assumptions

Agreement points scanned: all three keep `/sc:graph [status|init]` as the sole init owner; all three keep `/sc:impact` with `--diff [<base>]`; all three write `return-contract.yaml`; all three have orchestrator skills call slash commands mid-run; all three split dependents into production and test.

| # | Agreement Source | Assumption | Classification | Promoted |
|---|-----------------|------------|----------------|----------|
| A-001 | All keep `/sc:graph init` as the sole init owner | `init` is safe in every worktree layout. EVAL §5.8: a nested worktree is answered from the parent index with a warning and needs `codegraph init -i`; BRS K-4 refuses unless `--worktree-local` is passed. No variant states nested-worktree handling | UNSTATED | Yes |
| A-002 | All keep `/sc:impact --diff [<base>]` | Diff hunks can be mapped to symbols. EVAL §6.1: codegraph has "no diff-to-symbol mapping"; BRS K-2 does it IronClaude-side through `query --json` spans; BRS OQ-4 leaves non-Python open | UNSTATED | Yes |
| A-003 | All return dependents and tests as if current | The index is fresh at query time. EVAL §4: no watcher runs without an MCP client; BRS INV-001 (HIGH) and FR-05 re-check after in-run writes. Variants name "readiness" but no freshness re-check | UNSTATED | Yes |
| A-004 | All write `return-contract.yaml` | Callers with their own contracts (reflect's CLI parser, pr-submit's FSM) consume an extra artifact without a contract change (BRS §8.2 Rollback: "No contract field is added") | UNSTATED | Yes |
| A-005 | All have orchestrators invoke commands mid-run | A nested command or skill invocation costs less than the caller doing the same queries inline (CTX criterion 2). Only B states the cost, and only for its own skill (BRS OQ-6, UNVERIFIED) | UNSTATED | Yes |
| A-006 | All split dependents into production and test | One partition definition exists. BRS FR-09 makes reflect's runtime-surface table the single definition. No variant names it | UNSTATED | Yes |
| (stated) | A only | `affected` was never run in EVAL and its value is unmeasured | STATED (A) | No |
| (stated) | All | `codegraph_explore` is not used by these commands (CTX fact 4; BRS FR-10) | STATED (CTX) | No |

### Promoted shared-assumption diff points

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|-----------|-----------------|--------|--------|
| A-001 | Init is safe in nested worktrees | `/sc:graph init` sole owner | Medium | Open for debate |
| A-002 | Hunks map to symbols | `/sc:impact --diff` | High | Open for debate |
| A-003 | Index fresh at query time | All results | High | Open for debate |
| A-004 | Extra artifact needs no contract change | `return-contract.yaml` | Low | Open for debate |
| A-005 | Nested invocation is cheaper than inline | Command reuse | Medium | Open for debate |
| A-006 | One prod/test partition | Dependents split | Medium | Open for debate |

## Debate topic taxonomy (auto-tagged)

- L1 surface: S-001
- L2 structural: S-002, S-003, S-004, C-001, C-002, C-004, C-006, C-007, C-008, X-001, X-002, X-004, A-004, A-005
- L3 state mechanics: C-003, C-005, C-009, X-003, A-001, A-002, A-003, A-006

## Summary
- Total structural differences: 4
- Total content differences: 9
- Total contradictions: 4
- Total unique contributions: 7
- Total shared assumptions surfaced: 8 (UNSTATED: 6, STATED: 2, CONTRADICTED: 0)
- Highest-severity items: S-002, C-001, C-002, X-001, A-002, A-003
- Similarity check: 30 differences across 3 short variants; well above the 10% threshold, so the debate runs.
