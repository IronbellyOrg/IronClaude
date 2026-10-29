# Refactoring Plan: Merge into Base (Variant C)

## Overview
- Base: Variant C (`option-c.md`, variant-3-original.md)
- Incorporating strengths from: Variant A (`option-a.md`), Variant B (`option-b.md`), plus debate outcomes on shared assumptions A-001..A-006
- Planned changes: 12
- Risk level: Low overall. Every change is additive or replaces a phrase; none changes the unit count of 2.
- Merged output: `../merged-recommendation.md`. It is a decision recommendation, so it keeps C's sections (Commands, Callers, Strengths, Weaknesses) and adds Overlap, Not adopted, and Open points.
- Grounding abbreviations used in the merged text: CTX = `decisions/P3-command-set/context.md`; EVAL = `research/codegraph-evaluation.md`; BRS = `brainstorm/P3-codegraph-opportunities/merged-requirements.md`; SPEC = `specs/phase-3-codegraph-adoption-spec.md`.

## Planned Changes

### Change 1: Closed `graph:*` degraded vocabulary (from Variant B)
- **Source**: Variant B, item 1 ("a closed `graph:*` degraded vocabulary")
- **Target**: Base, `/sc:impact` entry, sentence "returns `status: partial` … `degraded: [codegraph]`" (replace)
- **Rationale**: X-003, winner B at 95% (all three advocates); BRS FR-02 "Consumers invent no tokens". The vocabulary itself lives in the guide, not in a skill.
- **Integration point**: replace `degraded: [codegraph]` with "a `graph:*` token from the closed list in BRS FR-02 (for example `graph:absent`, `graph:not_initialized`, `graph:stale`, `graph:truncated`), listed in the guide".
- **Risk**: Low. Wording only.

### Change 2: Advisory test list with a per-test source (from Variant A)
- **Source**: Variant A, command 2 ("advisory superset with the source of each test recorded")
- **Target**: Base, `/sc:impact` `--tests` clause (replace)
- **Rationale**: C-002, winner A at 90%; C advocate conceded. BRS FR-13 stage 0; SPEC §2.2 rank 13 ("advisory"); EVAL never ran `affected` (A l.29).
- **Integration point**: `--tests` returns `tests[]` with `source: heuristic|affected|both`, `selection_source: advisory|heuristic_only`. The list is advisory: it can add tests to a caller's selection, never remove any, and it does not change a gate until G-BACKTEST (BRS NFR-08).
- **Risk**: Low.

### Change 3: Separate depth flag for test mapping (from Variant A)
- **Source**: Variant A, `/sc:test-scope [--depth N]` kept separate from `/sc:impact --depth`
- **Target**: Base, `/sc:impact` signature (insert flag)
- **Rationale**: C-009, winner A at 90%; EVAL §3 lists `impact <symbol> [--depth]` and `affected [… --depth …]` as separate verbs.
- **Integration point**: add `[--test-depth N]`, used only with `--tests` and passed to `affected --depth`. Its default is unset (codegraph's own default, UNVERIFIED) until BRS OQ-10 is answered by G-BACKTEST.
- **Risk**: Low.

### Change 4: Readiness fields and nested-worktree guard on `/sc:graph` (from Variant B and BRS K-4)
- **Source**: Variant B item 1 (probe: "readiness, worktree provenance, version, telemetry"); BRS K-4 `--worktree-local`
- **Target**: Base, `/sc:graph` entry (replace and extend)
- **Rationale**: C-006, winner B at 70%; A-001, winner B at 70% with QUALIFY from all three; EVAL §5.8 (a nested worktree is answered from the parent index with a warning; `init -i`).
- **Integration point**: signature `/sc:graph [status|init] [--worktree-local] [--output-dir <dir>]`. Status prints `cli_version`, `pin_match`, `index_state` (`fresh|stale|not_initialized|foreign_index|absent|disabled`), `worktree_relation: own|parent|none`, files/nodes/edges, `telemetry` with the user opt-out, and `next_action`. `init` refuses in a nested worktree unless `--worktree-local` is given, in which case it runs `codegraph init -i`. A refusal returns `status: blocked`. There is no `sync` (BRS D-18).
- **Risk**: Low.

### Change 5: One probe path, inline (resolves X-002 and Clarity 1)
- **Source**: debate on X-002 (winner B at 85%) and A-005 (winner B at 65%); both scoring passes flagged C's two probe paths
- **Target**: Base, `/sc:graph` paragraph "Callers use `/sc:graph status --output-dir <dir>` (or simply read the guide's one-call readiness check)" (replace)
- **Rationale**: CTX criterion 3 asks for one obvious way to call. Probing through a nested command per run has an unmeasured cost (BRS OQ-6, UNVERIFIED).
- **Integration point**: "Skills never call `/sc:graph`. A calling skill that needs readiness runs the guide's readiness check (one `codegraph status` CLI call, timing UNVERIFIED per BRS NFR-01), and `/sc:impact` runs the same check itself. `/sc:graph status` is for users and is the pointer named by `/sc:load` and by the guide's `not_initialized` message."
- **Risk**: Low.

### Change 6: Freshness label on every result (debate A-003, unanimous REJECT)
- **Source**: all three advocates (REJECT A-003); BRS FR-05; SPEC §2.1 finding 4
- **Target**: Base, `/sc:impact` entry (append)
- **Rationale**: EVAL §4: no watcher runs without an MCP client. BRS INV-001 is HIGH and open.
- **Integration point**: every result carries `index_state` and `checked_at`. Before E-1 has passed, rows are advisory (they never change a severity, gate or verdict), and no "no dependents" or "no tests" conclusion is drawn from an empty, stale or foreign result (BRS FR-07).
- **Risk**: Low.

### Change 7: `--diff` mapping rule (debate A-002)
- **Source**: A-002 (QUALIFY from A and C, REJECT from B); BRS K-2
- **Target**: Base, `/sc:impact` entry (insert)
- **Rationale**: EVAL §6.1: codegraph has "no diff-to-symbol mapping"; BRS OQ-4 is open for non-Python code.
- **Integration point**: "`--diff` maps hunks to symbols on the IronClaude side through `codegraph query --json` spans. Files it cannot map go to `unmapped_files[]` and get file-level scope only."
- **Risk**: Low.

### Change 8: Partition, truncation and call-site budget (debate A-006, scoring Invariant 4, C-003)
- **Source**: A-006 (ACCEPT ×3); both scoring passes (no variant records shown/total); C-003 (winner B at 80%, delivered as a procedure per SPEC §2.2 rank 5)
- **Target**: Base, `/sc:impact` entry (append)
- **Rationale**: BRS FR-09 (reflect's runtime-surface table is the single prod/test definition); FR-08 (shown/total, one re-query at 100 or fewer, else `truncated`); FR-06 (`resolution: def-line|call-site-verified|unresolved`, at most 5 per symbol and 20 per run, failing rows dropped).
- **Integration point**: one sentence each, citing the guide as the home of the procedure.
- **Risk**: Low.

### Change 9: Caller list aligned with SPEC §2.2 and §2.3 (base weakness; Variant B is better on coverage, C-008)
- **Source**: C-008 (winner B at 70%); SPEC §2.2 ranks 7, 8, 11, 12, 13, 14 and §2.3 deferrals; Variant A names `/sc:test`
- **Target**: Base, Callers section (restructure)
- **Rationale**: Pass 1 found step names that no brainstorm or spec table lists (for example "sc-task-protocol STRICT step 7"). SPEC §2.3 defers reflect UC-2 (I-14), the workflow note (I-13) and the implement post-edit check.
- **Integration point**: list callers per rank, with their mode (warning, context, advisory or logged). Move UC-2, workflow and post-edit to "Deferred callers". Mark sc-task-protocol STRICT step 7 as UNVERIFIED (not in SPEC §2.2). State that troubleshoot Tier 1 (rank 10, T4) keeps calling the CLI inline per BRS FR-15 rather than invoking `/sc:impact`.
- **Risk**: Medium, because it changes which skills are named. Mitigation: every row cites a SPEC rank or BRS FR.

### Change 10: Overlap section (base weakness shared by all variants; Variant A partly better, U-001)
- **Source**: both scoring passes (Completeness 1 NOT MET for all; CTX criterion 6); Variant A names `/sc:test` as a caller
- **Target**: Base, new section after Callers (insert)
- **Rationale**: CTX criterion 6 asks for overlap with `/sc:index-repo`, `/sc:test` and `/sc:explain`.
- **Integration point**: three rows. `/sc:test` runs tests and may take the `--tests` list as advisory input. `/sc:explain` stays a prose explainer with its own one-hop view (SPEC rank 14) and is not a caller. `/sc:index-repo` is unchanged (SPEC §2.4, D-21), and `/sc:graph status` reports counts instead.
- **Risk**: Low.

### Change 11: Not adopted, and a fold-back rule for the resolver (from Variants A and B)
- **Source**: Variant A (`/sc:test-scope`); Variant B (`sc-graph-grounding`, `resolve-callsite.sh`); Advocate B's fold-back proposal
- **Target**: Base, new section (insert)
- **Rationale**: S-002 (C, 90%), X-004 (B=C, 92%), X-001 (C, 88%), C-003 (B, 80%).
- **Integration point**: each rejected unit with its reopen trigger. `/sc:test-scope` reopens after G-BACKTEST shows benefit (BRS NFR-08). The grounding skill stays rejected by SPEC §4 P3-D2. A resolver script may later live inside `/sc:impact`'s own protocol skill, not as a new unit, if E-3 (allowlist matching) and E-4 (resolver cost) pass and the written procedure misses call sites (INV-024).
- **Risk**: Low.

### Change 12: Open points and name conflict
- **Source**: Advocate C concession (spec line 210 says `/sc:codegraph`); debate Convergence Assessment
- **Target**: Base, new final section (insert)
- **Rationale**: an unresolved name conflict and gated items must be visible.
- **Integration point**: list `/sc:graph` vs `/sc:codegraph`; E-1/G-FRESH; G-BACKTEST/OQ-10; E-2 for `--file`; E-3/E-4 for the resolver; whether reflect and pr-submit ignore the extra artifact (A-004, UNVERIFIED); per-call token cost (A-005, UNVERIFIED).
- **Risk**: Low.

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|------------|-------------------|---------------------------|
| S-002, X-004 | A: third command `/sc:test-scope` | C 90% and B=C 92%; A's advocate conceded the duplication. Its value is unmeasured: `affected` was never run (A l.29; BRS NFR-08) |
| C-001, X-001 | B: `sc-graph-grounding` skill as the seam | SPEC §4 P3-D2 decides a core guide and rejects a skill ref; B's advocate conceded the rules point |
| C-003 | B: `resolve-callsite.sh` now | INV-019 (script allowlists unproven until E-3); text-output drift (BRS §8.2); SPEC §2.2 rank 5 plans a written procedure. Kept as a deferred option (Change 11) |
| C-004 | A/B: `--file <path>` input | C 65%. BRS K-2: "`--file` pinning waits on E-2"; whether CLI `callers` takes a file is UNVERIFIED (BRS §8.2) |
| C-008 | B: explain, load and cleanup-audit as callers of a shared skill | explain and load get guide pointers only (SPEC rank 14); cleanup-audit is deferred behind G-SPIKE (SPEC §2.3) |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1-8, 10-12 | Low | Wording or added fields only | Revert to the base sentence |
| 9 | Medium | A caller named or dropped wrongly | Revert to base caller list; re-check against SPEC §2.2 |

## Review Status
- [x] Auto-approved (default)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-10-29T18:07:00Z
