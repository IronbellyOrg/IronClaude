# Merge Execution Log

## Metadata

- Base: Variant C (option-c.md)
- Executor: merge-executor agent
- Changes applied: 12 of 12
- Status: success
- Timestamp: 2026-10-29T18:08:24Z (system clock; the plan's approval timestamp reads 2026-10-29T19:05:00Z, which is later than the clock, so it is recorded as written)
- Output: `../merged-recommendation.md` (114 lines)

## Changes Applied

### Change 1: Closed `graph:*` degraded vocabulary (from Variant B)

- Status: APPLIED
- Source: Variant B, Commands and skills item 1
- Target: `/sc:impact`, Fail-open bullet; Shared rules paragraph
- Before: "returns `status: partial` with Grep-based results and `degraded: [codegraph]`"
- After: "returns `status: partial` with Grep-based results and a `graph:*` token from the closed list in BRS FR-02 (for example `graph:absent`, `graph:not_initialized`, `graph:stale`, `graph:truncated`), listed in the guide". Shared rules now name the vocabulary as guide content.
- Provenance tag: `Base (original, modified) — ... fail-open token per Change #1`
- Validation: all four example tokens are in the BRS FR-02 list (BRS line 269).

### Change 2: Advisory test list with a per-test source (from Variant A)

- Status: APPLIED
- Source: Variant A, Commands item 2
- Target: `/sc:impact`, Tests bullet
- Before: "with `--tests` the test files from `codegraph affected` plus the path heuristic"
- After: `tests[]` with `source: heuristic|affected|both`, `selection_source: advisory|heuristic_only`; adds tests, never removes; no gate change until G-BACKTEST (BRS FR-13 stage 0, NFR-08).
- Provenance tag: `... --tests per Change #2`
- Validation: `selection_source` values are a subset of BRS K-3 (line 246); FR-13 stage 0 and NFR-08 confirmed (lines 280, 302).

### Change 3: Separate depth flag for test mapping (from Variant A)

- Status: APPLIED
- Source: Variant A, `/sc:test-scope [--depth N]`
- Target: `/sc:impact` signature and Tests bullet
- Before: no test depth flag
- After: `[--test-depth N, default unset]`, used only with `--tests`, passed to `affected --depth`; codegraph's own default marked UNVERIFIED until BRS OQ-10.
- Provenance tag: `... signature extended per Change #3`
- Validation: EVAL §3 line 96 lists `impact <symbol> [--depth]` and `affected [... --depth ...]` separately; BRS OQ-10 exists (line 391).

### Change 4: Readiness fields and nested-worktree guard on `/sc:graph`

- Status: APPLIED
- Source: Variant B item 1; BRS K-4
- Target: `/sc:graph` section
- Before: "`/sc:graph [status|init] [--output-dir <dir>]`: readiness (state, version, counts, next action) and the only place `codegraph init --yes` runs, only when the user typed `init`."
- After: signature with `[--worktree-local]` and default `status`; Status bullet with `cli_version`, `pin_match`, `index_state` (6 values), `worktree_relation`, counts, `telemetry` with opt-out, `next_action`; Init bullet with nested-worktree refusal, `init -i`, `status: blocked`, no `sync` (D-18). Outputs and Fail-open bullets added from BRS K-4 to meet the brief's per-command field list.
- Provenance tag: `Base (original, modified) — signature, status fields and nested-worktree guard per Change #4 ...; default and fail-open line from BRS K-4 ...`
- Validation: BRS K-4 (lines 256-260) confirms default `status`, refusal, `init -i`, no `sync` and the "never stops a caller" fallback; EVAL §5.8 lines 231-233 confirm the nested-worktree warning and `init -i`. The `index_state` list follows the plan's 6 values (BRS line 224 also has `error`; not added, per plan).

### Change 5: One probe path, inline

- Status: APPLIED
- Source: debate X-002 and A-005
- Target: `/sc:graph`, Callers and mode bullet
- Before: "Callers use `/sc:graph status --output-dir <dir>` (or simply read the guide's one-call readiness check) as their probe."
- After: plan text verbatim: skills never call `/sc:graph`; calling skills run the guide's readiness check (one `codegraph status` call, timing UNVERIFIED per BRS NFR-01); `/sc:impact` runs it itself; `/sc:graph status` is for users and is the pointer named by `/sc:load` and the guide's `not_initialized` message.
- Provenance tag: `... probe paragraph replaced per Change #5`
- Validation: BRS NFR-01 line 295 says "`status` timing stays UNVERIFIED until measured". The Strengths bullet "No per-run skill invocation" was narrowed to "No per-run grounding-skill invocation by every consumer" so it does not clash with each command invoking its own protocol skill.

### Change 6: Freshness label on every result

- Status: APPLIED
- Source: debate A-003 (REJECT x3); BRS FR-05
- Target: `/sc:impact`, Freshness bullet (new)
- Before: none
- After: `index_state` and `checked_at` on every result; advisory until E-1; no "no dependents" or "no tests" conclusion from empty, stale or foreign results (BRS FR-05, FR-07).
- Provenance tag: `... freshness per Change #6`
- Validation: BRS FR-05 (line 272) and FR-07 (line 274) confirmed.

### Change 7: `--diff` mapping rule

- Status: APPLIED
- Source: debate A-002; BRS K-2
- Target: `/sc:impact`, Diff input bullet (new)
- Before: none
- After: hunk-to-symbol mapping through `codegraph query --json` spans; unmapped files to `unmapped_files[]` with file-level scope; non-Python accuracy UNVERIFIED (BRS OQ-4).
- Provenance tag: `... --diff rule per Change #7`
- Validation: EVAL §6.1 line 262 "no diff-to-symbol mapping"; BRS K-2 line 234; BRS OQ-4 line 385. The UNVERIFIED note comes from the plan's rationale (OQ-4 open).

### Change 8: Partition, truncation and call-site budget

- Status: APPLIED
- Source: debate A-006; scoring Invariant 4; C-003
- Target: `/sc:impact`, Dependents and Call sites bullets
- Before: "call sites confirmed by Grep inside the caller and Read"
- After: FR-09 partition; FR-08 shown/total with one re-query at 100 or fewer, else `truncated`; FR-06 `resolution` field, cited rows only, 5 per symbol and 20 per run, failing rows dropped; procedure lives in the guide.
- Provenance tag: `... partition, truncation and call-site budget per Change #8`
- Validation: BRS FR-06, FR-08, FR-09 (lines 273, 275, 276) confirmed.

### Change 9: Caller list aligned with SPEC §2.2 and §2.3

- Status: APPLIED
- Source: C-008 (Variant B coverage); SPEC §2.2 ranks 7, 8, 11, 12, 13; SPEC §2.3
- Target: Callers section (restructured into "Active callers of `/sc:impact`" table and "Deferred callers" list)
- Before: one bullet listing implement Q1 and Q6, task STRICT step 7, troubleshoot `--fix`, pr-submit Wave 4 and VG-1, auggie-review Wave 1, reflect 1B.3 and UC-2, workflow; plus a `/sc:graph status` bullet.
- After: 9 table rows with step, mode and ground (reflect rank 7 logged; pr-submit Wave 4 and troubleshoot `--fix` rank 8 warning; auggie-review Wave 1 and pr-submit Wave 3 rank 11 context; implement Q1 rank 12 warning; implement Q6 and pr-submit VG-1 rank 13 advisory; task STRICT step 7 UNVERIFIED). Troubleshoot Tier 1 note (rank 10, FR-15). Deferred: reflect UC-2 (I-14), workflow (I-13), implement post-edit (I-07 post).
- Provenance tag: `Base (original, modified) — restructured per Change #9 (Variant B coverage, C-008); every row cites a SPEC §2.2 rank or BRS FR`
- Validation: SPEC §2.2 lines 148-155 and §2.3 lines 164-167 re-read and matched. pr-submit Wave 3 is new versus the base; it is the second target of rank 11 (SPEC line 152), added because the plan says "list callers per rank". Rank 14 (explain, load) is handled as pointers only, in Overlap and `/sc:graph`.

### Change 10: Overlap section

- Status: APPLIED
- Source: Variant A, Callers (`/sc:test`); CTX criterion 6
- Target: new H2 "Overlap with existing commands", after Callers
- Before: none
- After: three rows: `/sc:test`, `/sc:explain`, `/sc:index-repo`.
- Provenance tag: `Variant A, Callers (`/sc:test` as a caller) — merged per Change #10; fills CTX criterion 6`
- Validation: SPEC rank 14 (line 155) and SPEC §2.4 D-21 (line 180) confirmed.

### Change 11: Not adopted, and a fold-back rule for the resolver

- Status: APPLIED
- Source: Variant A (`/sc:test-scope`); Variant B (`sc-graph-grounding`, `resolve-callsite.sh`); Advocate B fold-back proposal
- Target: new H2 "Not adopted"
- Before: none
- After: three-row table with reason and reopen trigger per unit.
- Provenance tag: `Variant A, Commands item 2 and Variant B, Commands and skills item 1 — merged per Change #11, with Advocate B's fold-back proposal`
- Validation: SPEC §4 line 197 rejects a skill ref; BRS INV-019 and INV-024 (lines 370, 374), NFR-08 (line 302) and SPEC rank 5 (line 146) confirmed.

### Change 12: Open points and name conflict

- Status: APPLIED
- Source: Advocate C concession; debate Convergence Assessment
- Target: new final H2 "Open points"
- Before: none
- After: 7 bullets: name conflict, E-1/G-FRESH, G-BACKTEST/OQ-10, E-2 for `--file`, E-3/E-4, extra artifact (A-004, UNVERIFIED), per-call token cost (A-005, UNVERIFIED).
- Provenance tag: `Base (original, modified) — new final section per Change #12 ...`
- Validation: SPEC line 210 says `/sc:codegraph` and line 197 says `sc-codegraph-protocol` (re-grepped, since the spec may change). Debate A-004 and A-005 wording confirmed (transcript lines 59-60, 105-106).

## Post-Merge Validation

### Structural Integrity

- Heading hierarchy: PASS. One H1; 7 H2 (Commands, Callers, Overlap with existing commands, Strengths, Weaknesses, Not adopted, Open points); 5 H3 (three under Commands, two under Callers). No skipped levels.
- Header comments: 3 of 3 present (Provenance, Base, Merge date).
- Source tags: 11, one per section or significant block.
- Length: 114 lines (limit about 140).

### Internal References

- Markdown anchor links: 2 of 2 resolve (`#callers` to "Callers"; `#scgraph` to "`/sc:graph`").
- Prose cross-references: 1 of 1 resolves ("the resolver script fold-back above" to the "Not adopted" row).
- Abbreviations: CTX, EVAL, BRS, SPEC defined once (line 11); 0 undefined abbreviations (a draft used `BS` three times; corrected to `BRS`).
- UNVERIFIED markers: 7 lines carry one (OQ-4 mapping accuracy, `--test-depth` default, `status` timing, task STRICT step 7, CLI `callers` file argument, A-004, A-005).

### Contradiction Re-Scan

- A skill calling `/sc:graph`: none. The Callers table lists only `/sc:impact`; the note after it says `/sc:graph status` has no skill callers, matching Change 5.
- A SPEC §2.3 deferred caller still listed as active: none. Reflect UC-2, the workflow note and the implement post-edit check appear only under Deferred callers.
- "No per-run skill invocation" against each command invoking a protocol skill: resolved by narrowing the Strengths wording (see Change 5).
- `--test-depth` default: "default unset" in the signature agrees with the open point on OQ-10.
- Cross-document naming difference (not a contradiction inside the merged document): BRS K-2 and FR-12 name the output `blast-radius.md` and the flag `--output <dir>`; the merged document uses `impact.md` and `--output-dir`, per the base, CTX's callable-skill convention and the orchestrator brief. The auggie-review row cites FR-12 stage 1 without naming the file. Reported for the orchestrator; not changed.
- New contradictions found: 0.

## Summary

All 12 planned changes were applied in order, with 0 failed and 0 skipped. The merged document keeps the base's two-command shape and sections, adds Overlap, Not adopted and Open points, and every added fact was checked against CTX, EVAL, BRS or SPEC. Validation passed: heading levels correct, 3 of 3 references resolve, 0 new internal contradictions. One cross-document naming difference (`blast-radius.md` and `--output` in BRS against `impact.md` and `--output-dir` here) is reported for the orchestrator to decide.
