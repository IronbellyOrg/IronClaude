# Merge Execution Log

## Metadata
- Base: Variant B (sonnet:analyzer), `variant-2-sonnet-analyzer.md`
- Executor: merge-executor agent
- Changes applied: 32 of 32 (0 partial, 0 skipped)
- Status: success
- Timestamp: 2026-10-29T17:42:24Z
- Output: `merged-output.md` (391 lines)
- Debate status carried: BLOCKED_BY_INVARIANTS (INV-001 accepted as risk; E-1 blocking prerequisite at rank 1 and in §2.3, per the plan's carried condition)

Validation markers: S = structural integrity, R = references, C = contradictions. "pass" means the check found no issue for that change after the post-merge fixes below.

## Changes Applied

### Change 1: Scope statement, 1:1 exclusion and ground-truth front matter
- **Status**: Applied
- **Source**: Variant A, line 13 scope paragraph and `ground_truth`; Variant C line 4
- **Target**: Base front matter and Notation paragraph
- **Before**: B front matter without `ground_truth`; Notation defined EVAL and INV only by path.
- **After**: Front matter carries the required fields plus `ground_truth`; Notation defines EVAL, INV, INV-NNN and the evidence classes (P-minus added); a Scope paragraph excludes the installer phase, the Python CLI and the 1:1 swaps (D-22).
- **Provenance tag**: `<!-- Source: Base (original, modified) — Notation paragraph extended with scope and INV definitions per Change #1 ... -->`
- **Validation**: S pass | R pass | C pass

### Change 2: Correct EVAL fact errors and overstatements
- **Status**: Applied
- **Source**: R2-B #4, #6, #7, #9; R2-A B-2; diff-analysis X-017, X-019, X-020, X-021; A-003
- **Target**: §1 bullets, §2.1 row 1, I-04, D-01, D-05
- **Before**: "23 callers reported ... the rest were tests"; "Grep sees every static reference"; "a broken caller can never surface today"; "irrelevant at 30-60 calls"; explore drop justified by auggie being free.
- **After**: "20 of 23 shown: 2 production, 18 tests; 3 uninspected; one symbol"; coverage claim deleted; I-04 cites the downgrade at `:218` and chunking only at 16-30 files; the latency line is labelled arithmetic; X-019 written as UNVERIFIED both ways in E-2; `status` timing UNVERIFIED in NFR-01; D-01 rests on size and noise, fallback Grep/Read.
- **Provenance tag**: `<!-- Source: Base (original, modified) — bullets corrected per Change #2 ... -->`
- **Validation**: S pass | R pass | C pass

### Change 3: Nine-vector coverage table in §1
- **Status**: Applied
- **Source**: Variant C §1 nine-vector coverage map
- **Target**: §1 (insert); base §4 vector bullets (removed)
- **Before**: Vector check as bullets in §4.
- **After**: Table in §1 with the plan's rows. The plan text names a "net position" column that its sample table omitted; the column was filled from Variant C's net positions, adapted to the merged rules (for example test selection now reads "advisory until G-BACKTEST"). D-19 and I-09 were added to the onboarding row because both are onboarding items in the merged doc.
- **Provenance tag**: `<!-- Source: Variant C, §1 "Nine-vector coverage map" — merged per Change #3 ... -->`
- **Validation**: S pass | R pass | C pass

### Change 4: One state field and one closed vocabulary
- **Status**: Applied
- **Source**: Variant A FR-03; Variant A C-1 output
- **Target**: I-01, K-1/K-2 output, FR-01/02/03/05/14, all degraded examples
- **Before**: `codegraph_state`/`graph_state` with `ready/stale/uninitialized/foreign-index/absent/error`; `codegraph:<x>` tokens.
- **After**: `index_state: fresh|stale|not_initialized|foreign_index|absent|disabled|error`; `graph:{...}` closed vocabulary of 14 tokens in FR-02; consumers invent none.
- **Provenance tag**: listed in the §1 and §7 Functional Source tags (`#4 (terminology)`, `FR-02 per Change #4`)
- **Validation**: S pass | R pass | C pass

### Change 5: Access model v1 rules and MCP-stage trigger
- **Status**: Applied
- **Source**: Variant A §2.1 classes A-G; R2-B #9; R2-C #6; INV-025
- **Target**: §2.1 rows 1 and 5 (replace), new row; B1 stance
- **Before**: Rows without a Bash column; interactive commands allowed MCP explore; no MCP-stage row; B1 proposed a future `CODEGRAPH_MCP_TOOLS` list.
- **After**: Bash column (unrestricted / closed / none); unrestricted row = troubleshoot, reflect, implement, workflow; interactive row has no explore allowance; "MCP stage (deferred)" row with the three-part global trigger. B1 stance now points to that trigger only, so the base's suggested list no longer competes with it.
- **Provenance tag**: `<!-- Source: Base (original, modified) — rows 1 and 5 replaced, Bash column and MCP-stage row added per Change #5 ... -->`
- **Validation**: S pass | R pass | C pass

### Change 6: Blocker table additions
- **Status**: Applied
- **Source**: Variant A §2.2 B2, B5; INV-001, INV-019, INV-020; R2-B NE1
- **Target**: §2.2
- **Before**: B1-B8; B2 owner included `/sc:load --index`.
- **After**: B2 owner = user-typed `/sc:graph init` (K-4, I-09); B9 telemetry, B10 freshness without a daemon, B11 CLI flag gap, B12 allowlist matching added with owners and stances. B5 and B7 owners renamed to K-2/K-1 per Change 26.
- **Provenance tag**: `<!-- Source: Base (original, modified) — ... B2 owner replaced and B9-B12 added per Change #6 ... -->`
- **Validation**: S pass | R pass | C pass

### Change 7: Shared seam `sc-graph-grounding`
- **Status**: Applied
- **Source**: Variant A §6 C-1; base N-1; Variant C §2 contract; R2-B #1
- **Target**: §6 N-1 (now K-1), I-01
- **Before**: `sc-codegraph-probe` with probe, citation contract and script.
- **After**: K-1 with the PROBE→CALL→VERIFY→DEGRADE body, `refs/capability-map.md` (MCP names `mcp__codegraph__codegraph_<tool>`, none for `affected`), `refs/citation-contract.md`, `refs/degraded-vocab.md`, the resolver script and the Change 7 output schema. The resolver interface gained `--def-line <n>`, which the Change 13 binding rule needs; its output rows are `unresolved` until the caller's Read sets `call-site-verified`.
- **Provenance tag**: `<!-- Source: Variant A §6 C-1 ... + Base N-1 ... + Variant C §2 contract sequence — merged per Change #7, #12, #13, #27 -->`
- **Validation**: S pass | R pass | C pass

### Change 8: Blocking prerequisite E-1 and G-FRESH
- **Status**: Applied
- **Source**: invariant-probe.md INV-001 closure note; EVAL §4, §5.4, §5.7
- **Target**: new §2.3; gate columns in §3 and §4
- **Before**: Section did not exist.
- **After**: E-1 (eight steps, Outcomes A and B), G-FRESH gate row and the freshness-dependent definition. I-08 s0 and I-13 were added to the freshness-independent list: the plan's list omitted them, and by its own definition neither changes a severity, gate, verdict or finding class nor runs after an in-run write. P-01 is rank 1.
- **Provenance tag**: `<!-- Source: invariant-probe.md INV-001 closure note — merged per Change #8 ... -->`
- **Validation**: S pass | R pass | C pass

### Change 9: E-2, E-3 and E-4
- **Status**: Applied
- **Source**: R2-B NE1; R2-C NE3; R2-A NE3; INV-011, INV-019, INV-020
- **Target**: §2.3 after E-1
- **Before**: Section did not exist.
- **After**: E-2 help capture (P-02), E-3 permission matching (P-03), E-4 resolver timing, each with its interim rule.
- **Provenance tag**: `<!-- Source: Round 2 new evidence and invariant probe (INV-011, INV-019, INV-020) — merged per Change #9 -->`
- **Validation**: S pass | R pass | C pass

### Change 10: Split latch, debounce and persisted graph numbers
- **Status**: Applied
- **Source**: R2-B #3; R2-C #3; R1-A Conc 4; INV-002, INV-003
- **Target**: FR-01, FR-05, §8.2 stale-index bullet
- **Before**: FR-01 probe once per run; FR-05 pending → stale.
- **After**: FR-01 latches availability, provenance and version; FR-05 re-checks before each batch after an in-run write, invalidates cache, has the 3 s debounce, the Outcome B rule, persistence labelling and resume rule, and "no sync".
- **Provenance tag**: `FR-01/FR-05 per Change #10` in the §7 Functional tag; §8.2 tag
- **Validation**: S pass | R pass | C pass

### Change 11: Version-mismatch provenance hardening
- **Status**: Applied
- **Source**: INV-004; base FR-03, NFR-04, NFR-09; Variant A NFR-05
- **Target**: FR-03, NFR-09 (append); NFR-12
- **Before**: FR-03 equality check only; NFR-09 record version.
- **After**: Mismatch emits `graph:version_mismatch` and `graph:provenance_unproven`, leads only; live-binary fixture re-recording in NFR-12. Post-merge fix: FR-03 now states that `index_root: unknown` counts as a match only while the nested-worktree warning is absent (see Contradiction Re-Scan item 3).
- **Provenance tag**: `FR-03 per Change #11`, `NFR-09 per Change #11`
- **Validation**: S pass | R pass | C pass (after fix)

### Change 12: Telemetry on the CLI path
- **Status**: Applied
- **Source**: Variant A §2.2 B5, §8 Telemetry; R1-B Conc 3; INV-005, INV-020
- **Target**: B9, K-1 output, new FR-22
- **Before**: Base had no telemetry requirement.
- **After**: FR-22: the probe records `codegraph telemetry status`, emits `graph:telemetry_on`, primitives never prefix calls with the env var, `/sc:graph status` shows the state, installer handoff, accepted risk in §8.4 (INV-005 row). Reconciled with FR-04/FR-23: "never run the `telemetry` subcommand" is written as "never run `telemetry on` or `telemetry off`", because the plan itself has the probe read `telemetry status`; the FR-23 grep pattern is `telemetry (on|off)`. The user opt-out shown by K-4 is the EVAL §1 env form (`CODEGRAPH_TELEMETRY=0` or `DO_NOT_TRACK=1` in the shell profile), so `commands/graph.md` stays clean under FR-23.
- **Provenance tag**: `FR-22 per Change #12`; K-4 tag `telemetry display per Change #12`
- **Validation**: S pass | R pass | C pass (after reconciliation)

### Change 13: Citation resolver and contract rewrite
- **Status**: Applied
- **Source**: Variant A I-02, FR-04; R2-A NE6; Variant C FR-03; INV-011, INV-012, INV-024
- **Target**: I-02, FR-06, K-1 resolver
- **Before**: `query --limit 5`, Grep for the callee name in the span, status always lead-unverified.
- **After**: Typed `resolution`, `--limit 20`, `(file, startLine == def_line)` binding, call-expression Grep with string/comment/assignment rejection, multi-match rule, drop-never-repair, budget 5 per symbol and 20 per run, validator byte-identical. The context-only rule for auggie-review and reflect now names its one exception, FR-12 stage 3, which Change 19 enables (see Contradiction Re-Scan item 2).
- **Provenance tag**: `FR-06 per Change #13`; I-02 row in the §3 tag
- **Validation**: S pass | R pass | C pass (after reconciliation)

### Change 14: Allowlists, mutation grep and containment
- **Status**: Applied
- **Source**: Base FR-04; Variant C FR-06; R2-B NE3; R2-C #8, NE4, NE5; Variant A NFR-03; INV-019
- **Target**: FR-04 (replace), FR-23, NFR-10 (insert)
- **Before**: FR-04 with the `/sc:load --index` `init` exception.
- **After**: Per-subcommand patterns, no wildcard, only `/sc:graph init` may run `init`, exact-path script patterns per E-3; FR-23 grep with the `commands/graph.md` exception; NFR-10 containment from baseline 0.
- **Provenance tag**: `FR-04 per Change #14`, `FR-23 per Change #14`, `NFR-10 per Change #14`
- **Validation**: S pass | R pass | C pass

### Change 15: Explore policy and routing block
- **Status**: Applied
- **Source**: Variant A FR-05; base I-03, FR-10; R2-B #12
- **Target**: I-03, FR-10, FR-21
- **Before**: Explore banned only in budgeted waves and subagents; interactive `maxFiles` 5 or less allowed.
- **After**: No primitive names explore or context; interactive allowance removed (D-27); routing block of 12 lines or less kept with a "do not call explore" line; D-01 reworded; reopen condition recorded. Post-merge fix: the FR-10 grep allowance covers the "do not use" notes in both the capability map and the FR-21 routing block (see Contradiction Re-Scan item 1).
- **Provenance tag**: `FR-10/FR-21 per Change #15`
- **Validation**: S pass | R pass | C pass (after fix)

### Change 16: Staged test selection through `/sc:test-scope`
- **Status**: Applied
- **Source**: Base I-08, FR-13; Variant A FR-07; Variant C FR-05; R2-C NE1; R2-B NE2; INV-017
- **Target**: I-08 (split into s0 and s1 rows), FR-13, K-3
- **Before**: One I-08 row ("S advisory, M union"), `--stdin` input.
- **After**: Positional inputs filtered to existing paths; stage 0 advisory; stage 1 union behind G-FRESH and G-BACKTEST with `git ls-files`, collect-only pre-pass, collection-error fallback and the 200-file escalation; `selection_source`; docs-only rule; CLI-only.
- **Provenance tag**: `FR-13 per Change #16`; K-3 tag
- **Validation**: S pass | R pass | C pass

### Change 17: Backtest redesign (G-BACKTEST)
- **Status**: Applied
- **Source**: INV-023, INV-016; base NFR-08; R2-B NE2; R2-C NE1
- **Target**: NFR-08 (replace); §2.3 gate row
- **Before**: Recall "at least that of `<changed-area>`", median 25 files.
- **After**: Indexed-language sample of 20 or more, parent-commit index, benefit metric (affected-only failures or seeded mutations), cost caps, recall criterion deleted.
- **Provenance tag**: `NFR-08 per Change #17`; gate table tag
- **Validation**: S pass | R pass | C pass

### Change 18: Reflect truncation and calibration rules (G-SHADOW-REFLECT)
- **Status**: Applied
- **Source**: Base I-05, FR-09, FR-14; INV-009, INV-010; A-007
- **Target**: I-05, FR-09 (append), §2.3 gate row
- **Before**: Severity counts distinct production caller symbols at once.
- **After**: Lists are floors; truncated, stale or unproven lists use the chain 4b Grep count; shadow mode logs both counts for 10 runs before a written review; calibration note kept in §8.2; D-29 records the superseded rule.
- **Provenance tag**: `FR-09 per Change #18`; gate table tag
- **Validation**: S pass | R pass | C pass

### Change 19: auggie-review staging (G-SHADOW-AUGGIE)
- **Status**: Applied
- **Source**: Base I-04, FR-12; Variant A I-09; R2-B #7; INV-013, INV-024
- **Target**: I-04 (split into s1 and s2-3 rows), FR-12, §2.3 gate row
- **Before**: One I-04 row; FR-12 exemption when the call site is Read-verified.
- **After**: Stage 1 context via `/sc:impact --diff`, stage 2 shadow counts, stage 3 exemption only after G-SHADOW-AUGGIE (20 reviews, 3 true hits, false-positive rate 20% or less, G-FRESH) and only for `call-site-verified` rows; I-04 V = 3 in the ranked list.
- **Provenance tag**: `FR-12 per Change #19`; §3 tag `#19 (I-04 split)`
- **Validation**: S pass | R pass | C pass

### Change 20: Troubleshoot Tier 1 merged callers step
- **Status**: Applied
- **Source**: Variant A I-04; base I-06, FR-15
- **Target**: I-06 mechanism column
- **Before**: `callers --limit 20`, cap 40 rows, no budget citation.
- **After**: `query --json` plus `callers --limit 20` into `tier1-callers.md` (40 rows, 6 KB), within the ~3K Wave 1 budget at `:218`, with the note that `:256` is Wave 1.5; typed rows; fallback unchanged.
- **Provenance tag**: §3 tag `#20 (I-06)`
- **Validation**: S pass | R pass | C pass

### Change 21: Implement pre-edit warning plus post-edit check
- **Status**: Applied
- **Source**: Variant A I-05; R2-A NE5; base I-07, FR-16
- **Target**: I-07, FR-16
- **Before**: Post-edit `untouched_dependents` only.
- **After**: Pre-edit `/sc:impact` warning for rename, delete or signature tasks (cap 10 files, never widens Q1 edits) plus post-edit check behind G-FRESH.
- **Provenance tag**: `FR-16 per Change #21`
- **Validation**: S pass | R pass | C pass

### Change 22: Pre-fix impact in remediation chains (I-11)
- **Status**: Applied
- **Source**: Variant A I-10
- **Target**: §3 new row I-11
- **Before**: Row did not exist.
- **After**: I-11 row (value M, effort S, risk L, Grep fallback, warning only).
- **Provenance tag**: §3 tag `added I-11 (#22, Variant A I-10)`
- **Validation**: S pass | R pass | C pass

### Change 23: Cleanup-audit asymmetric rule (I-12)
- **Status**: Applied
- **Source**: Variant C I-07; R2-B #4, NE5; R1-A Conc 5
- **Target**: D-05 (replaced), §3 new row I-12, FR-07 example, G-SPIKE
- **Before**: Base dropped the cleanup-audit graph check.
- **After**: I-12 row (orchestrator only, nonzero → REVIEW, zero proves nothing) behind G-SPIKE and G-FRESH; D-05 now drops only zero-caller evidence; FR-07 carries the example.
- **Provenance tag**: §3 tag `I-12 (#23, Variant C I-07)`; `FR-07 per Change #23`
- **Validation**: S pass | R pass | C pass

### Change 24: Workflow informational step; tasklist stays dropped (I-13)
- **Status**: Applied
- **Source**: Variant A I-13; R2-B X-011; R2-C #3
- **Target**: D-07 (narrowed), D-06 (reason extended), §3 new row I-13
- **Before**: D-07 dropped the whole touch-set preview.
- **After**: I-13 informational note only for existing symbols; D-07 drops graph numbers in acceptance criteria or tiering; D-06 adds Variant C's concession.
- **Provenance tag**: §3 tag `I-13 (#24, Variant A I-13)`; §5 tag `D-07 narrowed per Change #24`
- **Validation**: S pass | R pass | C pass

### Change 25: Onboarding light edits; withdraw `--index`, defer `sc-structure-brief`
- **Status**: Applied
- **Source**: Variant A I-14, I-16; R2-B #2, #5; R2-A B-7
- **Target**: I-09, I-10 (replace), FR-17, FR-18 (delete), N-3 (to drops)
- **Before**: I-09 `/sc:load --index`; I-10 structure brief; FR-17, FR-18; N-3.
- **After**: I-09 = `/sc:graph` owner; I-10 = explain one-hop plus load status line; FR-17 and FR-18 text deleted and their IDs retired with a one-line "withdrawn, not reused" note so later IDs stay stable; N-3 recorded as D-21.
- **Provenance tag**: `FR-17/FR-18 withdrawn per Change #25`; §6 tag `N-3 moved to D-21 per Change #25`
- **Validation**: S pass | R pass | C pass

### Change 26: Four candidates, each with callers
- **Status**: Applied
- **Source**: Variant A §6 C-1..C-4; base N-1/N-2; Variant C C-3 fields; INV-022
- **Target**: §6 (restructure)
- **Before**: N-1 probe skill, N-2 `sc-blast-radius`, N-3 structure brief.
- **After**: K-1 `sc-graph-grounding`, K-2 `/sc:impact` (absorbs N-2), K-3 `/sc:test-scope`, K-4 `/sc:graph [status|init]` without `sync`. The plan gave no effort for K-2 or K-3: K-2 takes base N-2's L (it carries the blast-radius scope), K-3 takes M (Variant A's "S-M" normalized to one value per Change 28). K-2's output file keeps base N-2's name `blast-radius.md` so FR-12's `inputs/blast-radius.md` matches. K-3 interface is Variant A's C-3 form.
- **Provenance tag**: `<!-- Source: Variant A §6 C-1..C-4 slots with Base §6 N-1/N-2 content and Variant C C-3 fields — restructured per Change #26 ... -->` plus one tag per K-section
- **Validation**: S pass | R pass | C pass

### Change 27: Rollback and kill switches
- **Status**: Applied
- **Source**: Variant A FR-16; base NFR-07, §8 Rollback; R2-A NE1, NE2; R2-C NE2; INV-018
- **Target**: §8.2 Rollback (replace), new FR-24
- **Before**: "Remove the probe step or uninstall the binary".
- **After**: Three switches (release header, runtime binary absence, user-level `IRONCLAUDE_CODEGRAPH=off`); the MCP de-registration claim and deletion-as-rollback are not carried.
- **Provenance tag**: `FR-24 per Change #27`; §8.2 tag
- **Validation**: S pass | R pass | C pass

### Change 28: One ranked list with single S/M/L effort
- **Status**: Applied
- **Source**: Variant A §4 Layer 0; base §4 V × C ÷ E
- **Target**: §4 (replace); effort column of every §3 row
- **Before**: Ten-row list; I-07 labelled P but scored with C = 0.3; mixed efforts ("S-M", "S advisory, M union").
- **After**: The plan's 19-row table verbatim, method stated (Layer 0, then V × C ÷ E, tie order), one effort per §3 row, I-14 added to §3 from Variant A I-08 to match the table.
- **Provenance tag**: `<!-- Source: Variant A §4 Layer 0 + Base §4 V × C ÷ E — merged per Change #28 ... -->`
- **Validation**: S pass | R pass | C pass

### Change 29: Merged drops table
- **Status**: Applied
- **Source**: Base §5 D-01..D-12; Variant A §5; Variant C §5; Round 2 deferrals
- **Target**: §5 (replace)
- **Before**: D-01..D-12.
- **After**: D-01..D-29, each with a reason drawn from the cited source.
- **Provenance tag**: `<!-- Source: Base §5 D-01..D-12 (original, modified) + Variant A §5 + Variant C §5 + Round 2 deferrals — merged per Change #29 ... -->`
- **Validation**: S pass | R pass | C pass

### Change 30: Risks, invariants and edge cases
- **Status**: Applied
- **Source**: Variant A §8 INV-1..INV-4 and Markdown bullet; Variant C §8 edge-case table; invariant-probe.md LOW items
- **Target**: §8 (append; split into 8.1-8.4)
- **Before**: One bullet list.
- **After**: 8.1 Variant A's four invariants, renamed "Invariant 1-4" so they cannot be confused with probe IDs INV-NNN or the INV inventory; 8.2 base risks plus the Markdown bullet; 8.3 Variant C's edge-case table with corrected rows; 8.4 the INV-001 accepted-risk statement and a table of all 19 UNADDRESSED probe items with handling, so every INV-NNN reference resolves inside the document.
- **Provenance tag**: one tag per subsection (8.1 Variant A, 8.2 Base modified, 8.3 Variant C, 8.4 invariant-probe.md)
- **Validation**: S pass | R pass | C pass

### Change 31: Requirements consolidation
- **Status**: Applied
- **Source**: Variant A NFR-04, NFR-05; Variant C FR-07; base NFR-01, NFR-02, NFR-06; INV-011
- **Target**: NFR-01 (replace), NFR-02 (amend), NFR-11..NFR-13 (append)
- **Before**: NFR-01 single latency target; NFR-02 batching for all generated queries.
- **After**: NFR-01 per phase with logged query counts; NFR-02 known-target only, resolver not batched; NFR-11 mirror parity; NFR-12 version honesty; NFR-13 per-run cache invalidated by the FR-05 re-check.
- **Provenance tag**: §7 Non-functional tag
- **Validation**: S pass | R pass | C pass

### Change 32: Open questions update
- **Status**: Applied
- **Source**: Base §9; Variant A §9 Q-4, Q-8
- **Target**: §9 (replace)
- **Before**: Eight numbered questions.
- **After**: Closed items stated (MCP listing, probe skill vs ref); OQ-1..OQ-10 (kept: `affected` quality, `status` format, daemon on init, non-Python mapping, pin ownership; added: Skill-call cost, daemon detection, telemetry handoff, foreground-agent MCP, `affected --depth` default). Reuse-auditor and skill-vs-ref questions removed as closed or deferred (D-08).
- **Provenance tag**: `<!-- Source: Base §9 (original, modified) + Variant A §9 Q-4, Q-8 — updated per Change #32 -->`
- **Validation**: S pass | R pass | C pass

## Post-Merge Validation

### Structural Integrity
- Heading hierarchy: pass. One H1; H2 sections 1-9 in the required order; H3 only under §2 (2.1-2.3), §6 (K-1..K-4), §7 (Functional, Non-functional) and §8 (8.1-8.4). No level gaps and no orphan H3 (every H2 with an H3 has at least two).
- Section ordering: pass. Summary (with nine-vector table), access model (with blockers, E-1..E-4 and gates), ideas table, ranked list, drops D-01..D-29, candidates K-1..K-4, FR/NFR, risks with INV-001 accepted risk, open questions.
- Document flow: pass. 391 lines (limit about 480); 25 `<!-- Source: ... -->` tags covering every section and significant block; no emojis; body text cites no "Change N" (those appear only in provenance comments, which name refactor-plan.md).

### Internal References
- Total references: 529 (510 ID references across 137 distinct IDs: I-, D-, K-, E-, P-, B-, G-*, FR-, NFR-, OQ-, INV-; plus 19 "section N" references to 7 targets)
- Resolved: 529
- Broken: 0
- Notes: FR-17 and FR-18 resolve to the retired-ID line. INV-NNN references resolve to the §8.4 table. Debate point IDs (X-, C-, A-, U-, R2-) appear only in this log and in provenance comments.

### Contradiction Re-Scan
- New contradictions introduced: 0 remaining. Four were found during drafting and the re-scan, all plan-internal tensions that the merge made visible, and each was fixed with the narrowest wording that keeps both changes:
  1. FR-10 grep "one allowed hit, the capability map note" vs FR-21 routing block that tells the model not to call explore (both from Change 15). Fix: the grep allowance covers the "do not use" notes in both places.
  2. FR-06 "call-site-verified rows cannot lift a downgrade" in auggie-review (Change 13) vs FR-12 stage 3 exemption (Change 19). Fix: FR-06 names FR-12 stage 3 as the single exception, consistent with the base §8 "single verified class" wording.
  3. FR-03 "use results only when `index_root` equals the worktree root" vs K-1 output `index_root|unknown` (normal `status` prints no root, INV-004). Fix: `unknown` counts as a match only while the nested-worktree warning is absent.
  4. Change 12 "primitives never run the `telemetry` subcommand" and the FR-23 grep on `codegraph telemetry` vs the probe reading `codegraph telemetry status` (same change). Fix: forbidden forms are `telemetry on|off`; FR-04 allows the `status` read; the K-4 opt-out text uses the EVAL §1 env form.
- Checked and consistent: explore allowance removed everywhere (§2.1, I-03, FR-10, D-27); `/sc:load --index` and `sc-structure-brief` appear only as drops (D-19, D-21); every `init` path goes through K-4; no primitive `sync`; gate lists in §2.3, §3 and §4 agree; efforts in §3 match §4; all codegraph tool names match EVAL §3 (`codegraph_<tool>` MCP names, `mcp__codegraph__codegraph_<tool>` only in the capability-map description, `mcp__codegraph__*` only as the EVAL permission pattern).

## Summary
- Total changes planned: 32
- Successfully applied: 32
- Failed: 0
- Skipped: 0
- Merge-time adjustments (no new capability, all logged above): net-position column filled from Variant C (Change 3); I-08 s0 and I-13 classed freshness-independent by the plan's definition (Change 8); resolver `--def-line` argument (Change 7); K-2 and K-3 efforts and the `blast-radius.md` file name (Change 26); FR-17/FR-18 IDs retired, not reused (Change 25); Variant A invariants renamed (Change 30); four contradiction fixes above.
- Post-merge validation: PASS
