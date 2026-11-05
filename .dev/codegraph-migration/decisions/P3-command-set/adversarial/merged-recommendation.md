<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant C (option-c.md) -->
<!-- Merge date: 2026-10-29T18:08:24Z -->

# P3 command set: merged recommendation (two commands)

<!-- Source: Base (original, modified) — decision summary and scores added per the orchestrator brief; scores from base-selection.md, convergence from debate-transcript.md -->
Decision: Phase 3 adds exactly 2 commands, `/sc:impact` and `/sc:graph`. Each is a thin `commands/<name>.md` that invokes its protocol skill (`sc:impact-protocol`, `sc:graph-protocol`) per the callable-skill convention in CTX, and the shared rules live once in `~/.claude/CODEGRAPH.md` (SPEC §4, P3-D2). Scores: C 0.781, A 0.748, B 0.727. C won by tiebreaker level 1, because its margin over A was 3.3% (below 5%) and it won the debate on points (C 8.0, B 7.5, A 2.5). Convergence was 100% of 23 diff points at depth quick (Round 1 only; the invariant probe was not run).

<!-- Source: Base (original, modified) — "Read context.md first" kept; abbreviations defined per refactor-plan Overview -->
Read CTX first. Abbreviations: CTX = `decisions/P3-command-set/context.md`; EVAL = `research/codegraph-evaluation.md`; BRS = `brainstorm/P3-codegraph-opportunities/merged-requirements.md`; SPEC = `specs/phase-3-codegraph-adoption-spec.md` (all under `.dev/codegraph-migration/`).

## Commands

### `/sc:impact`

<!-- Source: Base (original, modified) — signature extended per Change #3; --tests per Change #2; fail-open token per Change #1; freshness per Change #6; --diff rule per Change #7; partition, truncation and call-site budget per Change #8 -->
- **Purpose:** for symbols or a diff, list definitions and their production and test dependents, and with `--tests` an advisory list of test files.
- **Signature:** `/sc:impact <symbol>... | --diff [<base>]` `[--depth 1-3, default 2] [--limit N, default 20] [--tests] [--test-depth N, default unset] [--output-dir <dir>] [--caller <name>]`.
- **Diff input:** `--diff` maps hunks to symbols on the IronClaude side through `codegraph query --json` spans, because codegraph has no diff-to-symbol mapping (EVAL §6.1). Files it cannot map go to `unmapped_files[]` and get file-level scope only. Accuracy for non-Python code is UNVERIFIED (BRS OQ-4).
- **Dependents:** split into production and test using reflect's runtime-surface table as the single definition (BRS FR-09). Every caller list records `shown/total`; if `total` is 100 or fewer it re-queries once with a wider `--limit`, otherwise it sets `truncated` (BRS FR-08).
- **Call sites:** every row carries `resolution: def-line|call-site-verified|unresolved`. Only rows that will be cited are confirmed (Grep inside the caller's span, then Read), at most 5 per symbol and 20 per run; rows that fail are dropped, never repaired (BRS FR-06). The procedure is written in the guide, not in a script.
- **Tests (`--tests`):** returns `tests[]` from `codegraph affected` plus today's path heuristic, each with `source: heuristic|affected|both`, and a `selection_source: advisory|heuristic_only`. The list is advisory: it can add tests to a caller's selection, never remove any, and it changes no gate until G-BACKTEST passes (BRS FR-13 stage 0, NFR-08). `--test-depth` applies only with `--tests` and is passed to `affected --depth`, a separate verb from `impact --depth` (EVAL §3). While unset, codegraph's own default applies (UNVERIFIED) until BRS OQ-10 is answered by G-BACKTEST.
- **Freshness:** every result carries `index_state` and `checked_at`. Until E-1 has passed, rows are advisory: they never change a severity, gate or verdict, and no "no dependents" or "no tests" conclusion is drawn from an empty, stale or foreign result (BRS FR-05, FR-07).
- **Outputs:** `<output-dir>/impact.md` (for people) and `<output-dir>/return-contract.yaml` with `status: success|partial|blocked|failed` and absolute paths (CTX).
- **Fail-open:** with no codegraph or no index it returns `status: partial` with Grep-based results and a `graph:*` token from the closed list in BRS FR-02 (for example `graph:absent`, `graph:not_initialized`, `graph:stale`, `graph:truncated`), listed in the guide. It never stops the caller.
- **Callers and mode:** see [Callers](#callers).

### `/sc:graph`

<!-- Source: Base (original, modified) — signature, status fields and nested-worktree guard per Change #4 (Variant B item 1; BRS K-4); probe paragraph replaced per Change #5; default and fail-open line from BRS K-4 to meet the per-command field list -->
- **Purpose:** readiness of this worktree's index, and the only place `codegraph init` runs.
- **Signature:** `/sc:graph [status|init] [--worktree-local] [--output-dir <dir>]`, default `status` (BRS K-4).
- **Status:** prints `cli_version`, `pin_match`, `index_state` (`fresh|stale|not_initialized|foreign_index|absent|disabled`), `worktree_relation: own|parent|none`, files/nodes/edges, `telemetry` with the opt-out the user can apply, and `next_action`.
- **Init:** runs `codegraph init --yes` only when the user typed `init`. In a nested worktree, which codegraph answers from the parent index with a warning (EVAL §5.8), it refuses unless `--worktree-local` is given, in which case it runs `codegraph init -i`. A refusal returns `status: blocked`. There is no `sync` (BRS D-18).
- **Outputs:** the report on screen; `<output-dir>/return-contract.yaml` only when `--output-dir` is given.
- **Fail-open:** with no codegraph it reports `index_state: absent` and the install pointer; it never stops a caller (BRS K-4).
- **Callers and mode:** skills never call `/sc:graph`. A calling skill that needs readiness runs the guide's readiness check (one `codegraph status` CLI call, timing UNVERIFIED per BRS NFR-01), and `/sc:impact` runs the same check itself. `/sc:graph status` is for users and is the pointer named by `/sc:load` and by the guide's `not_initialized` message.

### Shared rules

<!-- Source: Base (original, modified) — vocabulary and call-site procedure named as guide contents per Changes #1 and #8; P3-D2 cited -->
No new skill holds shared semantics. Readiness labels, the closed `graph:*` vocabulary, read-before-cite, fail-open and the call-site procedure are written once in `~/.claude/CODEGRAPH.md` (SPEC §4, P3-D2); each command's protocol skill cites it.

## Callers

<!-- Source: Base (original, modified) — restructured per Change #9 (Variant B coverage, C-008); every row cites a SPEC §2.2 rank or BRS FR -->
### Active callers of `/sc:impact`

| Caller | Step | Mode | Ground |
|---|---|---|---|
| sc-reflect-protocol | 1B.3 and chain 4/4b, production and test counts | logged only; severity rule unchanged | SPEC rank 7; BRS FR-14 |
| sc-pr-submit-protocol | Wave 4, before a fix | warning | SPEC rank 8 |
| sc-troubleshoot-protocol | `--fix` handoff | warning | SPEC rank 8 |
| sc-auggie-review-protocol | Wave 1, `--diff` | context only | SPEC rank 11; BRS FR-12 stage 1 |
| sc-pr-submit-protocol | Wave 3 | context only | SPEC rank 11 |
| sc-implement-protocol | Q1, before rename, delete or signature edits | warning; never widens Q1 edits | SPEC rank 12; BRS FR-16 |
| sc-implement-protocol | Q6, `--tests` | advisory | SPEC rank 13 |
| sc-pr-submit-protocol | VG-1, `--tests` | advisory; VG-1 gate unchanged | SPEC rank 13; BRS FR-13 stage 0 |
| sc-task-protocol | STRICT step 7 | UNVERIFIED: not in SPEC §2.2 | base list; CTX candidate list |

Troubleshoot Tier 1 (SPEC rank 10, task T4) keeps calling the codegraph CLI inline and writes `tier1-callers.md` itself (BRS FR-15); it does not invoke `/sc:impact`. `/sc:graph status` has no skill callers (see [`/sc:graph`](#scgraph)).

### Deferred callers

SPEC §2.3 defers these, so they are not wired in Phase 3:

- sc-reflect-protocol UC-2, "mapped tests neither changed nor run" (BRS I-14): reopens on E-1 Outcome A.
- sc-workflow-protocol informational impact note (BRS I-13): reopens when a consumer asks for it.
- sc-implement-protocol post-edit "untouched dependents" check (BRS I-07 post): reopens on E-1 Outcome A.

## Overlap with existing commands

<!-- Source: Variant A, Callers (`/sc:test` as a caller) — merged per Change #10; fills CTX criterion 6 -->
| Existing command | Relation |
|---|---|
| `/sc:test` | Runs tests. It may take the `--tests` list as advisory input; `/sc:impact` never runs tests. |
| `/sc:explain` | Stays a prose explainer with its own one-hop view (SPEC rank 14). It is not a caller. |
| `/sc:index-repo` | Unchanged (SPEC §2.4, D-21). `/sc:graph status` reports index counts instead. |

## Strengths

<!-- Source: Base (original, modified) — "per-run skill invocation" narrowed to the grounding skill after Change #5; spec citation made exact -->
- Smallest new surface that covers impact, test selection and index ownership: two command files and two test files.
- One contract for all dependent and test questions; callers learn one interface.
- No per-run grounding-skill invocation by every consumer and no shell parser; the guide is already decided (SPEC §4, P3-D2).

## Weaknesses

<!-- Source: Base (original) -->
- `/sc:impact` is larger (two jobs: dependents and tests).
- No dedicated resolver script: call-site confirmation is a written procedure (Grep inside the caller's span, then Read), less mechanical than a script.
- A caller that only wants tests still calls `/sc:impact --tests`.

## Not adopted

<!-- Source: Variant A, Commands item 2 and Variant B, Commands and skills item 1 — merged per Change #11, with Advocate B's fold-back proposal -->
| Unit | From | Why not | Reopen when |
|---|---|---|---|
| `/sc:test-scope` | A | Duplicates `/sc:impact --tests`; its value is unmeasured because EVAL never ran `affected` | G-BACKTEST shows benefit (BRS NFR-08) |
| `sc-graph-grounding` skill | B | SPEC §4 P3-D2 puts shared rules in a core guide and rejects a skill ref | Stays rejected unless P3-D2 is reversed |
| `resolve-callsite.sh` | B | Script allowlists are unproven (BRS INV-019); SPEC rank 5 plans a written procedure | E-3 (allowlist matching) and E-4 (resolver cost) pass and the written procedure misses call sites (BRS INV-024). It would then live inside `/sc:impact`'s own protocol skill, not as a new unit |

## Open points

<!-- Source: Base (original, modified) — new final section per Change #12 (Advocate C concession; debate Convergence Assessment) -->
- **Name conflict:** this document uses `/sc:graph` (BRS K-4); SPEC §4 says `/sc:codegraph` and `sc-codegraph-protocol`. The conflict is unresolved.
- **E-1 / G-FRESH:** until the freshness experiment passes, every graph result stays advisory (BRS INV-001, HIGH, open).
- **G-BACKTEST / BRS OQ-10:** decides whether the `--tests` list can join a real gate and what `--test-depth` defaults to.
- **E-2:** whether CLI `callers` takes a file is UNVERIFIED, so `--file <path>` input waits on it (BRS K-2).
- **E-3 / E-4:** gate the resolver script fold-back above.
- **Extra artifact:** whether reflect and pr-submit ignore the added `return-contract.yaml` is UNVERIFIED (debate A-004).
- **Per-call token cost:** the cost of a nested `/sc:impact` call compared with inline work is UNVERIFIED (debate A-005; BRS OQ-6, NFR-06).
