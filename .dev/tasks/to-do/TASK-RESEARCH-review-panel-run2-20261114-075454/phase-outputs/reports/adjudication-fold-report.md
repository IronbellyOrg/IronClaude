# Adjudication fold report (Item 5.50)

Date: 2026-11-15
Status: Complete (written incrementally; the last check ran after the final edit, see section 5)

Scope: fold of the 15 `ADJUDICATION-RESULT.md` files under `reviews/adversarial/` into `synthesis/synth-05-options.md`, `synth-06-conflict-log.md`, `synth-07-recommendation-architecture.md`, `synth-09-sequence-and-gates.md` and `synth-10-questions-evidence.md`. All paths are relative to `.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/` unless they start with `src/`, `tests/` or `scripts/`.

Inputs read in full: `phase-outputs/discovery/undecidable-conflicts.md`, the 15 `ADJUDICATION-RESULT.md` files, and the five synthesis files named above. `phase-outputs/plans/debate-slot-*-not-used.md`: none exist (Glob returned no file). No debate artifact below the result files (merged outputs, transcripts, invariant probes) was re-read; every outcome, condition, invariant and path in the fold comes from the 15 result files and the undecidable-conflicts file.

Slot names: X-13, X-14 and X-15 are the synth-06 slots C-13, C-14 and C-15. Both names are kept visible in every synth-06 and synth-07 edit.

## 1. Outcome table (15 debates)

| Slot (synth-06 name) | Slug | Winner (base + hybrid) | Status of the debate | Folder |
|---|---|---|---|---|
| C-01 | core-shape-and-finding-contract | Hybrid on Variant B: thin shared contract now, per-module engines; one engine-local change from A (anchor status in the per-row `### Lx` block); convergence to one engine only on triggers T-a, T-b, T-c | partial; BLOCKED_BY_INVARIANTS (1 HIGH) | `reviews/adversarial/core-shape-and-finding-contract/` |
| C-02 | ledger-clearing-and-verdict-authority | Hybrid on Variant B: explicit per-row clearing by a quorum gate over distinct valid reviewers, silence never clears, typed `blocking` plus CRITICAL floor, `defer` terminal and counted open, verdict derived on read | partial; BLOCKED_BY_INVARIANTS (3 HIGH) | `reviews/adversarial/ledger-clearing-and-verdict-authority/` |
| C-03 | merge-verdict-policy-and-quorum | Hybrid on Variant A: any-blocking union as a pluggable policy, quorum as a merge-time refusal, B's falsifiers and offline adjudicated policy added | partial; BLOCKED_BY_INVARIANTS (2 HIGH) | `reviews/adversarial/merge-verdict-policy-and-quorum/` |
| C-04 | reflect-tier2-engine-composition | Hybrid on Variant 1 (A): code-owned write side behind a gated shell; no engine moves now | partial; no HIGH invariant (CONVERGED) | `reviews/adversarial/reflect-tier2-engine-composition/` |
| C-05 | consumer-entry-effect-and-delivery | Hybrid on Variant A: reflect UC-1 stays the only entry; advisory at Wave 4, "advisory-blocking" at Stage 10.5, blocking at T5; no plugin copy | partial; BLOCKED_BY_INVARIANTS (7 HIGH) | `reviews/adversarial/consumer-entry-effect-and-delivery/` |
| C-06 | limits-repair-policy | Hybrid on Variant B: itemised drop record, dropped-blocking refusal, cut of the three location fields to 200 in code behind `repair=False`, re-ask; claim cut unresolved | partial; BLOCKED_BY_INVARIANTS (4 HIGH) | `reviews/adversarial/limits-repair-policy/` |
| C-07 | dispatch-and-launch-mechanism | Hybrid on Variant 2 (B): the core launches nothing, a reviewer is launched with its `launch` word as the Agent `model` argument, no packaged gateway fill, claude-p launcher gated | partial; BLOCKED_BY_INVARIANTS (1 HIGH) | `reviews/adversarial/dispatch-and-launch-mechanism/` |
| C-08 | run-record-and-served-model-capture | Hybrid on Variant 1 (A): per-run `events.jsonl`, transcript adapter gated by measurement M1, manifest lock, `review-telemetry/1` with `strict`, no `/2` | partial; BLOCKED_BY_INVARIANTS (13 HIGH) | `reviews/adversarial/run-record-and-served-model-capture/` |
| C-09 | panel-resolution-and-tier-source | Hybrid on Variant B: package tier file as the reviewed copy held in step by one guard test, soft distinctness stays the default, scarcest-first order in the CLI, record always written | partial; no HIGH invariant (CONVERGED) | `reviews/adversarial/panel-resolution-and-tier-source/` |
| C-10 | pr-review-wire-format-and-slot | Hybrid on Variant A (C10-R): separate pre-step, pure panel-to-Finding converter, sibling `panel` field, report-only first release | partial; BLOCKED_BY_INVARIANTS (5 HIGH) | `reviews/adversarial/pr-review-wire-format-and-slot/` |
| C-11 | rfqa-first-step-and-readonly-scope | Hybrid on Variant B: lens-level first change (one new read-only lens agent plus a replay oracle; no panel engine in any rf-qa gate; conditional switch at `/task` steps 3-4) | partial; BLOCKED_BY_INVARIANTS (6 HIGH) | `reviews/adversarial/rfqa-first-step-and-readonly-scope/` |
| C-12 | collaboration-exchange-capability | Staged hybrid on Variant A: H1, H2, H3, H4 principle and a per-module static kit (`kit: off`) now; no exchange code built; build and enable triggers | partial; BLOCKED_BY_INVARIANTS (2 HIGH) | `reviews/adversarial/collaboration-exchange-capability/` |
| X-13 (C-13) | process-redesign-modules | Hybrid on Variant A (Sweep-Sheet-shaped): card format, record-only row block, advisory rowcheck, dormant until a module declares cards; demotion and promotion not built | partial; BLOCKED_BY_INVARIANTS (2 HIGH) | `reviews/adversarial/process-redesign-modules/` |
| X-14 (C-14) | eval-acceptance-and-harness-owner | Hybrid on Variant A: three-tier acceptance, metric of record, tested `scripts/` set; kernel `verify-run` deferred, not rejected | partial; BLOCKED_BY_INVARIANTS (12 HIGH) | `reviews/adversarial/eval-acceptance-and-harness-owner/` |
| X-15 (C-15) | tasklist-medium-and-fidelity-vocab | Hybrid on Variant B: module-data label map, nothing new in the core, fidelity prompt outside the core; Medium question (H+ versus A+) unresolved | partial; BLOCKED_BY_INVARIANTS (2 HIGH) | `reviews/adversarial/tasklist-medium-and-fidelity-vocab/` |

No debate returned `NOT ADJUDICATED`. Every debate ran at standard depth (no Round 3); every return contract has status `partial`.

## 2. Change log (file, section, before and after in one line)

### 2.1 synth-06-conflict-log.md

| # | Section | Before | After |
|---|---|---|---|
| 6-1 | 6.12.9 table, slot column of three rows | `C-13`, `C-14`, `C-15` | `C-13 (debate slot name X-13)`, `C-14 (debate slot name X-14)`, `C-15 (debate slot name X-15)`; every other cell of the rows and every row kept |
| 6-2 | new 6.12.9.1 "Adjudication outcomes" (before 6.12.10) | no outcome per undecidable row | one row per slot (15 rows): outcome (winner), rationale (the debate's own scores), conditions and the debate folder path; all 15 slots adjudicated, none `NOT ADJUDICATED` |
| 6-3 | 6.12.10, after the "15 slots" paragraph | residue sentence only | adds an adjudication-status paragraph: all 55 routed rows have an outcome; X-13/X-14/X-15 naming; axis 6.10 has no slot and is carried as synth-10 Q-38 |

### 2.2 synth-05-options.md

| # | Section | Before | After |
|---|---|---|---|
| 5-1 | line 7 (rule of the file) | "No winner is picked here ... route it to a debate." | same sentence plus a pointer: winners are recorded only in the new section "Adjudicated winners by axis"; no option text above it was changed |
| 5-2 | new section "Adjudicated winners by axis" (before "Interactions between axes") | axis status summary only | one row per axis (6.1, 6.2, 6.3, 6.4, 6.5, 6.5.b, 6.6, 6.7, 6.8, 6.8.b, 6.8.c, 6.9, 6.9.b, 6.10, 6.11, tasklist Medium): debate slot and folder, winning option, what it takes from the other options, status. 6.1 winner = Option C; 6.2 = Option 1 with shared parts; 6.3 = Option 4 as modified; 6.4 = Option 2; 6.5 = Option 1 shipped, Option 2 gated; 6.5.b = option (a) as modified; 6.6 = Option 2 (kit off); 6.7 = Option 1 shape built as Option 4 pieces; 6.8 = Option 1 now plus code-owned helpers; 6.9 = Options 4 + 3 + 2 as three tiers; 6.11 = Option 2; 6.10 not adjudicated |

### 2.3 synth-07-recommendation-architecture.md

| # | Section | Before | After |
|---|---|---|---|
| 7-1 | header "Source" line | research files only | adds the 15 `ADJUDICATION-RESULT.md` files and the X-13/X-14/X-15 naming |
| 7-2 | 7.0 "Recommended approach" paragraph | "One Review Panel Core with Module Profiles" (single core, v2 kernel default, modules as profile data) | renamed "One Shared Review Panel Core: a Thin Shared Contract with Per-Module Engines"; the paragraph states the shared contract (ids, limits, repair, refs, hashes, tier source, run record, dispatch contract, scripts) and the two engines (v1 for spec review, v2 kernel for reflect and PR) |
| 7-3 | new 7.0.1 | none | name and owner-wording note (the design is describable as "one shared core in `cli/review/` with thin modules" but the core is a contract plus two engines, not one engine); a 15-row table of what each outcome adds; a 6-row table of tensions CT-1 to CT-6 with the combination the results support and the open question (Q-41 to Q-46) |
| 7-4 | line "Verified facts that bound the design to ONE shape" | "they do not decide between the v2 kernel, the v1 package and a thin shared contract (axis 1, slot C-01, marker A-15)" | "decided by debate C-01 in favour of the thin shared contract with per-module engines" |
| 7-5 | axes table intro sentence | "carry a default and are listed in the adjudication table" | "were adjudicated by debate; their Chosen cell names the result; axes 1, 2, 4, 5, 8 overturned an earlier default" |
| 7-6 | axes table row 1 (core shape): Chosen, Why, Trade-off cells | "A, the recommended default; PENDING (marker A-15, slot C-01)" | "C, thin shared contract with per-module engines, adjudicated (C-01), OVERTURNS the default A"; scores, tiebreaker, triggers T-a/T-b/T-c, open INV-003 (Q-43) |
| 7-7 | axes table row 2 (finding contract) | "Default (option 2): one superset record, locator-agnostic annotate, ext namespace, prior lines in the core grammar. PENDING A-16, A-14" | option 1 with shared parts (ids, limits module, one repair step behind `repair=False`, one refs list), open unknown keys, no `ext`, `prior` unchanged; PR wire format = pure converter (C-10); locator-agnostic annotate and citation-keyed ledger rows withdrawn |
| 7-8 | axes table row 3 (limits) | "exact-prefix truncation for the three length failures, one re-ask" | cut of `anchor`, `anchor2`, citation `quote` to 200 behind `repair=False`, itemised drops, dropped-blocking refusal, one re-ask; claim cut unresolved |
| 7-9 | axes table row 4 (quorum and verdict) | "defer carries owner, reason and expiry; DEGRADED (exit 11) never PASS; row clears only through an explicit answer from a recorded examining reviewer" | C-02 and C-03 outcomes: quorum-gated `prior ... resolved` with veto, typed `blocking` plus CRITICAL floor, `defer` terminal with no expiry, any-blocking union, merge-time quorum refusal (exit 12, `min(2, requested)`), DEGRADED only in `degrade` profiles; three places differ from the earlier default |
| 7-10 | axes table row 5 (dispatch) | "a raw-id lane covers gateway models" | the core launches nothing; Agent class word = `launch` word ships; raw-id `claude -p` launcher gated by G1-G3; no packaged gateway fill; advocates' post-G1-G3 split recorded |
| 7-11 | axes table row 6 (collaboration) | "PENDING: marker A-18, slot C-12" | staged hybrid: H1, H2, H3, H4 principle, static kit `kit: off`; exchange not built; build and enable triggers; [POST-BASELINE] premise open (Q-39) |
| 7-12 | axes table row 7 (process redesign) | "PENDING: marker A-19, slot C-13" | optional cards, `rows-v1`, advisory `rowcheck.json`, dormant until a module declares cards; extractors, slot binding, demotion and promotion reserved |
| 7-13 | axes table row 8 (reflect engine) | "engine B data model is the shared core inside engine A's shell; shadow steps move into core CLI writers" | no engine moves now; engine A stays production Tier 2; write-side helpers write comparison siblings; D1 fixes now; CV-5 deferred; single-engine decision named, not scheduled (Q-09) |
| 7-14 | axes table row 9 (evaluation) | "a `verify-run` ... PENDING A-11, A-20" | three tiers, metric of record per item with unmatched blocking rows, tested `scripts/` set, kernel `verify-run` deferred, status wording, two reflect-gate repairs |
| 7-15 | axes table rows 10 and 11 | row 10 trade-off without 6.10; row 11 "PENDING: marker A-17, slot C-11" | row 10 trade-off adds the owner decision Q-38; row 11 names the PR converter (C-10) and the lens-level rf-qa first change (C-11) |
| 7-16 | choices table (A-3 to A-20): intro, header, 18 rows | 18 rows with a recommended default and a `[PENDING-ADJUDICATION: <slug>] (slot C-nn)` marker | header renamed (adjudicated outcome; debate result: winner, conditions, folder); every one of the 18 markers replaced by the debate result and the folder path; 12 rows differ in whole or part from the earlier default (A-3, A-4, A-5, A-6, A-7, A-8, A-10, A-11, A-15, A-16, A-17, A-20), 6 confirm it with added conditions (A-9, A-12, A-13, A-14, A-18, A-19) |
| 7-17 | 7.1 intro, diagram, modules table, core contract elements 1-6, 8, 9 | single core with one record, one fingerprint, locator-agnostic annotate, `verify-run` in the kernel, strict distinct default, manifest revision check | diagram shows the shared thin contract over two engines plus a dispatch contract and the reflect shell; modules and elements rewritten to the adjudicated outcomes; invariant I-3 and five rows of the defect-owner table updated |
| 7-18 | 7.2 intro, 7.2.1 rows 1, 5, 9, 10, 12, verdict; 7.2.2 rows 1, 2, 3, 6, verdict; 7.2.3 Stage 7 row; 7.2.4 table | locator-agnostic annotate, passthrough fields, multi-file target, adapter; per-slot lens; checklist mode now | PR: pure converter, sibling `panel` field, report-only first release, T-a trigger for a revise loop; rf-qa: lens-level first change, per-slot lens withdrawn, replay oracle first; every "marker A-n" reference replaced by "choice A-n" |
| 7-19 | adjudication register table and slot coverage line | recommended default column; "all 15 slots, 18 markers" | adjudicated outcome and folder columns; X-13/X-14/X-15 names; "every one adjudicated" |
| 7-20 | [UNVERIFIED] item 1 and the Rules check line | "marker A-3 holds only a default"; "the 18 adjudication markers ... each marker appears once" | item 1 names the adjudicated floor and Q-42; the rules check states that no pending marker remains and points to 7.3 and synth-10 9.10 |
| 7-21 | new 7.3 "Debate Invariants" (before "End of synthesis 07.") | none | legend table (15 slots, counts, addressed-by-debate counts) and 244 invariant rows: HIGH 60, MEDIUM 161, LOW 23 (the table is reproduced in section 4 of this report) |

Verification run after these edits: Grep `\[PENDING-ADJUDICATION` over `synthesis/` returned no match without an error (the final check is in section 5).

### 2.4 synth-09-sequence-and-gates.md

| # | Section | Before | After |
|---|---|---|---|
| 9-1 | (a) Binding constraints, after row C14 | 14 constraints (C1-C14) | 15 constraint rows added, C15 to C29, each a condition a winner requires with its source (the result file and the code lines it cites) and the test or rule that enforces it (or "none"): reflect comparison-artifact rule (C-04), weak reading of "no change to `cli/reflect`" (C-01, C-04, C-12), `repair=False` and the pins at `test_review_findings.py:113,117` (C-01, C-06), tests rewritten with the clearing change and the `### Lx` placement (C-02, C-01), reflect `shortfall: visible` and `degrade` profiles (C-03), `gateway.launch` stays `{}` and the launcher gates (C-07), the tier guard test and `tiers_sha256` (C-09), run-record edit fence and `:228` (C-08), PR module purity and report-only (C-10), tasklist and workflow call sites unchanged and the engine switch release (C-05), rf-qa switch conditions (C-11), tasklist Medium pins (X-15), process-redesign byte-identity (X-13), harness placement, `.gitignore:13` and CI collection (X-14), collaboration off-state test (C-12) |
| 9-2 | (b) No-regression gates, after row G16 | 16 gates (G1-G16) | 11 gate rows added, G17 to G27, each with its source: C-01 test set T1-T5, clearing and quorum replay, reflect helper promotion and seam probe, engine-switch contract-compat and smoke, limits-repair measurements and kill lines, dispatch launcher gates and shape tests (named so they are not confused with rows G1-G3), run-record measurements M1-M3, PR measurements, process-redesign gates G-0 to G-4, acceptance tiers and offline tests M-6, M-7, tasklist F1-F3 |
| 9-3 | (c) Dependency facts D9, D11, D16, D23 | evidence cells without the debate outcomes | one adjudication note appended to each evidence cell (C-01: citation-only finding kept out of the v1 ledger, fact stays true for trigger T-a; C-11: per-slot `lens` withdrawn from the first change; X-14: verifier is a script, kernel `verify-run` deferred; C-10: converter on the `pr_submit` side, sibling `panel` field); no row removed |

All additions are constraints and gates with sources; no plan step, schedule, branch plan or risk register was added.

### 2.5 synth-10-questions-evidence.md

| # | Section | Before | After |
|---|---|---|---|
| 10-1 | Section 10, "Conflict Debates" table | one row `ADJUDICATION-FOLD-PENDING` ("The debate folders ... are added by the later adjudication fold item") | an intro paragraph and 15 rows (slug and slot, folder path, result file, winner); the placeholder string no longer occurs |
| 10-2 | Section 10, new "Conflict debate artifacts" table under "Conflict Debates" | no debate path in the Evidence Trail | one row per debate folder listing every file found by `find` (top level and `adversarial/`, 15 folders, 4 + 14 to 19 files each) plus the paths of the fold report and of `undecidable-conflicts.md` |
| 10-3 | new Section 9.10 (before Section 10) | Section 9 ended at 9.9 with Q-37 | 56 rows Q-38 to Q-93: 2 premise and owner items (Q-38 variants keep versus archive, Q-39 [POST-BASELINE] C-12 premise), Q-40 wording, Q-41 to Q-46 cross-debate tensions, Q-47 to Q-88 invariant groups, Q-89 to Q-93 owner decisions and unresolved debate points; each with impact, suggested resolution and source |

## 3. Decisions the fold made and flags for the orchestrator

1. Name. "One Review Panel Core with Module Profiles" no longer describes the design (debate C-01 overturned the default that the v2 kernel is the single engine of the core). Renamed to "One Shared Review Panel Core: a Thin Shared Contract with Per-Module Engines" in synth-07 section 7.0. The owner-approved wording ("one shared Review Panel core in `src/superclaude/cli/review/`, with thin modules for reflect, tasklist and workflow, spec review, and later PR review") still describes the design in two respects (one core location; thin modules) and differs in one: the core is a shared contract plus two engines side by side in the package, not one engine with profiles. This is flagged in synth-07 7.0.1 and as owner question Q-40. The old name appears nowhere else in the synthesis folder (Grep); it may appear in task-file text outside the synthesis folder, which this fold did not edit.
2. Design overturned by the debates (the default of synth-07 before the fold): axis 1 (v2 kernel as the single core), axis 2 (one superset record and locator-agnostic `annotate`), axis 4 (defer expiry, module code predicate for `blocking`, quorum with a distinct-served-model test, DEGRADED exit 11 as the partial-panel outcome in every profile), axis 5 (raw-id launch lane beside the Agent lane), axis 8 (engine B inside engine A's shell now), the kernel half of axis 9 (`verify-run`), and the strict-distinct default of choice A-6.
3. The 15 outcomes combine into one design (synth-07 7.0.1 table). Six real tensions are listed there as CT-1 to CT-6 and in synth-10 as Q-41 to Q-46; none was resolved silently: reflect edit boundary (CT-1), repair against pins (CT-2), the `requested` denominator across four debates (CT-3), identity `unrecorded` blocks acceptance (CT-4), Medium against the CRITICAL floor (CT-5), gateway reach (CT-6).
4. Axis 6.10 (keep versus archive of the installed-only variants) has no debate; it is carried as synth-10 Q-38 and in synth-06 and synth-05.
5. The C-12 [POST-BASELINE] item is synth-10 Q-39 (impact: the defer half and the build-trigger order of C-12; resolution: fold into the work tracked by GitHub issue #550 and re-check the C-12 outcome). The issue number comes from the orchestrator's fact list; the fold did not open the issue.
6. Invariants: all 244 unaddressed invariants (60 HIGH, 161 MEDIUM, 23 LOW) are in the table of section 4 and in synth-07 7.3. A script check (section 5) confirmed that each of the 221 HIGH and MEDIUM rows names an open question of synth-10 9.10 that cites the same slot and invariant id. No HIGH or MEDIUM invariant is marked addressed by the recommended design: the fold added no resolution the debates did not produce.
7. Limits of the fold. Only the 15 result files and `undecidable-conflicts.md` were read; the merged outputs, transcripts, probes and return contracts were not re-read, so every number quoted in the fold (scores, margins, convergence, counts) is as the result files state it. The two synth-05 axis tables (rows with pre-existing column-count mismatches at lines 130, 159, 561-569, 623) were not touched.
8. Other synthesis files not in scope (synth-01 to synth-04, synth-08) were not edited; if any quotes a default that a debate overturned (for example axis 1 as "A, the recommended default"), the assembly step should take the folded synth-07 as the source.

## 4. Invariant table

Every invariant the 15 debates left unaddressed (60 HIGH, 161 MEDIUM, 23 LOW = 244 rows). The table is the one placed at the end of synth-07 as `### 7.3 Debate Invariants` (copied from that file, rows unchanged); its fourth column names the synth-10 section 9.10 open question that holds each HIGH and MEDIUM row, and LOW rows are CARRIED in the debates' merged outputs. Debate slot legend: C-01 `core-shape-and-finding-contract`, C-02 `ledger-clearing-and-verdict-authority`, C-03 `merge-verdict-policy-and-quorum`, C-04 `reflect-tier2-engine-composition`, C-05 `consumer-entry-effect-and-delivery`, C-06 `limits-repair-policy`, C-07 `dispatch-and-launch-mechanism`, C-08 `run-record-and-served-model-capture`, C-09 `panel-resolution-and-tier-source`, C-10 `pr-review-wire-format-and-slot`, C-11 `rfqa-first-step-and-readonly-scope`, C-12 `collaboration-exchange-capability`, X-13 (C-13) `process-redesign-modules`, X-14 (C-14) `eval-acceptance-and-harness-owner`, X-15 (C-15) `tasklist-medium-and-fidelity-vocab`.


| Invariant | Severity | Debate | Where addressed in the report | Status |
|---|---|---|---|---|
| C-01 INV-001: anchor status can be surfaced for every blocking row from data `render_merged_report` already has (the row stores neither flag) | MEDIUM | C-01 | synth-10 Q-47 | OPEN |
| C-01 INV-002: adding `T<PP>.<TT>` to the shared token list leaves ledgers already on disk behaving the same | MEDIUM | C-01 | synth-10 Q-47 | OPEN |
| C-01 INV-003: a repair step inside both `parse_block` functions can rescue over-limit lines while every existing pin stays unmodified (`test_review_findings.py:113,117`) | HIGH | C-01 | synth-10 Q-43 (7.0.1 CT-2) | OPEN |
| C-01 INV-004: the same repair gives the same benefit in the v2 parser (any error invalidates the whole v2 block) | MEDIUM | C-01 | synth-10 Q-47 | OPEN |
| C-01 INV-009: the 3-line clustering tolerance means the same thing in both engines (0-based half-open against 1-based inclusive) | MEDIUM | C-01 | synth-10 Q-47 | OPEN |
| C-01 INV-010: the two parsers hold the only copies of the limits and one repair is the only repair (`card_convert.py` has a third copy and its own truncation) | MEDIUM | C-01 | synth-10 Q-47 | OPEN |
| C-01 INV-014: a round whose only reviewer has only a repaired line merges like any other round | MEDIUM | C-01 | synth-10 Q-47 | OPEN |
| C-01 INV-015: a stuck row is one row, so surfacing its status once is enough (empty refs open a new span-less row each round) | MEDIUM | C-01 | synth-10 Q-47 | OPEN |
| C-01 INV-016: the merged T2 gate catches every shared-contract change (a `refs_norm` change passes a parser-output gate but changes fingerprints) | MEDIUM | C-01 | synth-10 Q-47 | OPEN |
| C-01 INV-017: adding the token once in `refs_norm` updates every reference-token reader (`telemetry.py` keeps its own copy) | MEDIUM | C-01 | synth-10 Q-47 | OPEN |
| C-01 INV-018: shared helpers can move into a new module without touching pinned tests (`test_module_does_not_import_v1_cluster`) | MEDIUM | C-01 | synth-10 Q-47 | OPEN |
| C-01 INV-020: "no change to `cli/reflect`" means the reflect results do not change (shadow steps call the v2 parser and `refs_norm`) | MEDIUM | C-01 | synth-10 Q-47 (see Q-41) | OPEN |
| C-01 INV-021: the merged T2 has committed v1 ledger fixtures to replay | MEDIUM | C-01 | synth-10 Q-47 | OPEN |
| C-01 INV-022: whatever repair policy C-06 picks leaves locating and clustering of the rescued line well defined | MEDIUM | C-01 | synth-10 Q-47 | OPEN |
| C-01 INV-024: the consensus alone resolves FX-1 and leaves C-06 free to choose the repair policy (the repair reaches 2 of 3 validation paths) | MEDIUM | C-01 | synth-10 Q-47 | OPEN |
| C-01 INV-008: one constant per limit is safe when equal numbers mean different things; the literal list omits `findings_v2.py:128` | LOW | C-01 | debate result C-01 (listed here only) | CARRIED (LOW) |
| C-02 INV-001: `need = min(Q, requested)` can be 0 if `--resolution` carries an empty reviewers list (`merge_cmd.py:73-83`), re-opening the silence clear; no `max(1, ...)` floor is specified | HIGH | C-02 | synth-10 Q-42 | OPEN |
| C-02 INV-002: a valid `prior open` plus a same-round non-blocking re-find leaves a `regressed` non-blocking row in none of `brief_ids`, `verify_ids`, `held_ids` | HIGH | C-02 | synth-10 Q-48 | OPEN |
| C-02 INV-003: empty `brief_ids` with non-empty `verify_ids` stays REVISE (exit 10); exit-code-only callers run an empty reviser; `next` is only in `ledger verdict` JSON | HIGH | C-02 | synth-10 Q-49 | OPEN |
| C-02 INV-004: `--resolution` absent: either fallback fails (one bypasses Q, one deadlocks) | MEDIUM | C-02 | synth-10 Q-42 | OPEN |
| C-02 INV-005: `pending_new_sha256` can wedge the loop; no force path | MEDIUM | C-02 | synth-10 Q-50 | OPEN |
| C-02 INV-006: the derived VM-6 pre-check must not fail on an empty ledger and must not block after a PASS | MEDIUM | C-02 | synth-10 Q-50 | OPEN |
| C-02 INV-007: `refound_deferred` is unreachable in the one-row D-11 shape (held-only is ESCALATE, then VM-6 refuses the round) | MEDIUM | C-02 | synth-10 Q-50 | OPEN |
| C-02 INV-008: no undefer command; `--owner ""` satisfies "required" | MEDIUM | C-02 | synth-10 Q-50 | OPEN |
| C-02 INV-009: an invalid-block reviewer's `prior open` is collected but ignored; an "incomplete" reviewer with a valid block counts toward `need` | MEDIUM | C-02 | synth-10 Q-50 | OPEN |
| C-02 INV-010: dissent does not re-anchor the row; `apply_revision` still needs a hunk touching its span | MEDIUM | C-02 | synth-10 Q-50 | OPEN |
| C-02 INV-011: prior ids are ledger ids `L<n>` while reviewers see `F<n>`; whether PRIOR is the merged report is unverified | MEDIUM | C-02 | synth-10 Q-50 | OPEN |
| C-02 INV-013: an unexamined `prior resolved` clears; the quote is recorded, not gating | MEDIUM | C-02 | synth-10 Q-50 | OPEN |
| C-02 INV-014: the text hash exists only if `revise` ran | MEDIUM | C-02 | synth-10 Q-50 | OPEN |
| C-02 INV-016: the CRITICAL floor keys on reviewer-typed severity; a re-classification to MAJOR non-blocking still drops the row | MEDIUM | C-02 | synth-10 Q-45 | OPEN |
| C-02 INV-018: older binaries read `last["verdict"]` and fail; stored per-round verdicts cannot be reconstructed | MEDIUM | C-02 | synth-10 Q-50 | OPEN |
| C-02 INV-020: a non-blocking `resolved_check` row is outside `verify_ids` and stays `resolved_check`; harmless to the verdict | LOW | C-02 | debate result C-02 (listed here only) | CARRIED (LOW) |
| C-03 INV-006: the union merges every parsable finding including those of a reviewer whose block is invalid (`ledger.py:127-138`); no test pins it | HIGH | C-03 | synth-10 Q-51 | OPEN |
| C-03 INV-007: `requested = max(len(resolution.reviewers), len(--report))` can collapse to 1 because `panel.resolve` drops skipped slots; then one valid empty block passes | HIGH | C-03 | synth-10 Q-42 | OPEN |
| C-03 INV-001: a refusal records nothing, so refusal rate, retries and reviews-to-cap are not measurable | MEDIUM | C-03 | synth-10 Q-52 | OPEN |
| C-03 INV-002: after exit 12, `ledger verdict` shows the previous round's stored decision; no rule says not to consult it | MEDIUM | C-03 | synth-10 Q-52 | OPEN |
| C-03 INV-003: which layer owns the profile, `min_complete` and the `requested` default is unspecified (`merge_round` has no such parameter; 24 test call sites) | MEDIUM | C-03 | synth-10 Q-52 | OPEN |
| C-03 INV-004: `--resolution` is not checked for kind or run (a first-kind resolution with a single-reviewer re-review inflates `requested`; a stale one deflates it) | MEDIUM | C-03 | synth-10 Q-42 | OPEN |
| C-03 INV-005: `complete` is not checked for distinct, current reviewers (unknown ids, identical report text, duplicate ids, stale reports reused on retry) | MEDIUM | C-03 | synth-10 Q-52 | OPEN |
| C-03 INV-009: between the floor and `requested` the shortfall is silent; the merged report prints "panel of N reviewers" from the reports passed | MEDIUM | C-03 | synth-10 Q-52 | OPEN |
| C-03 INV-010: the N=1..5 by five-state test matrix distinguishes only three input states at the CLI; the zero-valid refusal pin asserts message text the new refusal object lacks | MEDIUM | C-03 | synth-10 Q-52 | OPEN |
| C-03 INV-016: the union runs over rows that may already hold a `same_defect` mistake (a new blocking defect matched to a `deferred` row never fails the round) | MEDIUM | C-03 | synth-10 Q-52 | OPEN |
| C-03 INV-012: `defer` is the only non-quorate route to a stored PASS and is reachable when quorum keeps failing | LOW | C-03 | debate result C-03 (listed here only) | CARRIED (LOW) |
| C-03 INV-013: `make verify-sync` does not cover the loop-prompt copies; installed prompt skew leaves callers without `--resolution` until reinstall | LOW | C-03 | debate result C-03 (listed here only) | CARRIED (LOW) |
| C-04 INV-001: a helper writes a comparison sibling, not the legacy file, in shadow; the consensus never says where it reads the mode (`manifest.py:123-127, :496-500`) | MEDIUM | C-04 | synth-10 Q-53 | OPEN |
| C-04 INV-002: `calibrated` as a helper-owned stage: `SKILL.md:345` has the orchestrator fix `panel/cards/` after `calibrated`; a rerun raises `Conflict` and a hand fix leaves a stale hash | MEDIUM | C-04 | synth-10 Q-53 | OPEN |
| C-04 INV-003: Arm A and M-B cannot each be read off the exit script as a clean 20-run set (`collect` counts every published shadow run) | MEDIUM | C-04 | synth-10 Q-53 | OPEN |
| C-04 INV-005: name-only validation over the stable and telemetry lists; `degraded_components` is read only at top level while the lint allows both placements | MEDIUM | C-04 | synth-10 Q-53 | OPEN |
| C-04 INV-006: "helper refuses", "helper advances its own stage" and shadow's "continue as legacy" are not shown compatible (`advance_stage` raises `OutOfOrder`) | MEDIUM | C-04 | synth-10 Q-53 | OPEN |
| C-04 INV-007: M-A's "every recorded run yields a lint-clean contract" fails for runs with a leaked key under a refusing serializer; 3 unparseable alias contracts not exercised | MEDIUM | C-04 | synth-10 Q-53 | OPEN |
| C-04 INV-008: "exactly one verdict-read key outside the frozen lists": A counts 19, B 18, both miss alias reads; "137 names" is 136 distinct | MEDIUM | C-04 | synth-10 Q-53 | OPEN |
| C-04 INV-009: D1's CV-8 and CV-1 line lists may be incomplete (`executor-disjoint` at further lines; `0.75` on 10 `SKILL.md` lines plus 2 in `refs/grader-extensions.md`) | MEDIUM | C-04 | synth-10 Q-53 | OPEN |
| C-04 INV-011: M-B cannot require zero parity failures over 20 runs (a 2-of-3 shortfall run fails parity on a card-count mismatch) | MEDIUM | C-04 | synth-10 Q-53 | OPEN |
| C-04 INV-012: D1's fix at `reflect_shadow_exit.py:313` does not close all of CV-9; the meaning of "no baseline" is unstated | MEDIUM | C-04 | synth-10 Q-53 | OPEN |
| C-04 INV-013: the presence rule and a refusing finalizer do not cover every run shape (no-merge fallback run, `reviewers_resolved: 0`) | MEDIUM | C-04 | synth-10 Q-53 | OPEN |
| C-04 INV-014: the exit rule and `reflect_verdict_replay.py` read fixed paths and pair by directory name, so code-built siblings are unreadable without more change | MEDIUM | C-04 | synth-10 Q-53 | OPEN |
| C-04 INV-015: the card writer's target differs between the two advocates' texts; CV-9 card-name regex mismatch (`panel_lint.py:188` against `reflect_shadow_exit.py:59`) | MEDIUM | C-04 | synth-10 Q-53 | OPEN |
| C-04 INV-017: "helpers that advance their own stage make skipping detectable": the orchestrator can advance with its own or an empty payload; the hash-versus-file check is optional | MEDIUM | C-04 | synth-10 Q-53 | OPEN |
| C-04 INV-019: "comparison siblings let promotion be decided without risk": the absence path is never exercised in shadow; promotion is an engine flip with a new invocation | MEDIUM | C-04 | synth-10 Q-53 | OPEN |
| C-04 INV-010: the reviewer-count value 1 and the I2 witness (`test_ensemble_stub_integration.py:174-196`) have no named replacement | LOW | C-04 | debate result C-04 (listed here only) | CARRIED (LOW) |
| C-04 INV-016: widening the fence is not only bookkeeping: `SKILL.md:703` and `:1480-1481` are legacy-path instructions outside `### 4.3a`; the 3/39 baseline predates the new prose | LOW | C-04 | debate result C-04 (listed here only) | CARRIED (LOW) |
| C-05 INV-001: "advisory at Wave 4 and Stage 10.5": Stage 10.5 halts on `needs_human_decision` and ends `blocked` unattended (`sc-tasklist-protocol/SKILL.md:1640-1646`); the effect of an engine switch on halt frequency is open | HIGH | C-05 | synth-10 Q-54 | OPEN |
| C-05 INV-002: Stage 10.5 always passes `--remediate`, a write path that can nest reflect, workflow and reflect (`sc-reflect-protocol/SKILL.md:369-371,383-385`); unpriced | HIGH | C-05 | synth-10 Q-54 | OPEN |
| C-05 INV-003: the depth-policy remedy changes the remediation route and forces Tier 2 under the legacy engine at Wave 4 | HIGH | C-05 | synth-10 Q-54 | OPEN |
| C-05 INV-005: the reach share has no working instrument (the only aggregator globs shadow-run panel manifests and cannot see unreached phases or tasklist consumer directories) | HIGH | C-05 | synth-10 Q-55 | OPEN |
| C-05 INV-007: "only `status`, `coverage_pct`, `tier_reached`" is too narrow; two of the three fields are fixed before the engine is read | HIGH | C-05 | synth-10 Q-56 | OPEN |
| C-05 INV-013: the replay that decides every disputed point has no ground-truth scorer, no engine selector for arm R, a harness that denies Bash, Agent, Task and `mcp__*`, and no numeric threshold | HIGH | C-05 | synth-10 Q-55 | OPEN |
| C-05 INV-014: the consensus does not show consumers receive the panel's benefit without a second entry and without pin changes (no panel-to-status map) | HIGH | C-05 | synth-10 Q-56 | OPEN |
| C-05 INV-004: a call-site depth flag is not "pin-safe": both workflow trees need the edit and "defaults for every other flag" becomes false and unpinned | MEDIUM | C-05 | synth-10 Q-57 | OPEN |
| C-05 INV-006: the reach-share denominator is undefined (no-run populations, `--budget-remaining` downgrade, forced-deep boundary) | MEDIUM | C-05 | synth-10 Q-57 | OPEN |
| C-05 INV-008: a default flip reaches every UC-1 caller (task-builder PRE gate, auggie-review, troubleshoot); more than four kinds of `reflect_status` reader exist | MEDIUM | C-05 | synth-10 Q-57 | OPEN |
| C-05 INV-010: "one reflect-side switch" is prose in three places with no staged selector; shadow-first doubles Tier-2 reviewer spend | MEDIUM | C-05 | synth-10 Q-57 | OPEN |
| C-05 INV-011: a contract-compat test against the 36-test matrix does not cover the panel lint rules or define a panel-to-status map | MEDIUM | C-05 | synth-10 Q-57 | OPEN |
| C-06 INV-001: the dropped-blocking refusal sees only the current round's drops; a blocking line lost in a FAIL round can be forgotten when a later round passes | HIGH | C-06 | synth-10 Q-58 | OPEN |
| C-06 INV-017: a 200-character prefix can locate at more than one place while the full anchor locates once; `annotate` takes the first and `anchor_ambiguous` is read nowhere | HIGH | C-06 | synth-10 Q-58 | OPEN |
| C-06 INV-018: in reflect, `cluster_cmd` and `verify_cmd` run at step 6, after the `collected` commit of steps 3-4, so the re-ask, the attempt-2 record and the first-pass carrier cannot be driven as written | HIGH | C-06 | synth-10 Q-59 | OPEN |
| C-06 INV-023: cut plus itemise plus refusal does not alone close the PASS-by-loss defect and the v2 loss unit (forgotten cross-round drop, prefix absorbed by a deferred row, truncated block) | HIGH | C-06 | synth-10 Q-58 | OPEN |
| C-06 INV-002: the manifest `completion` value is a third first-pass carrier the text does not name | MEDIUM | C-06 | synth-10 Q-60 | OPEN |
| C-06 INV-003: a refused v1 merge records nothing, so the refusal-driven re-ask leaves no ledger trace and K4/K5 are not measurable live | MEDIUM | C-06 | synth-10 Q-60 | OPEN |
| C-06 INV-005: `blocking_state` from the line's own `blocking` flag is untrusted (CRITICAL with `blocking: false` is accepted by both checkers) | MEDIUM | C-06 | synth-10 Q-60 | OPEN |
| C-06 INV-006: the acknowledgement is not bound to the dropped item ids or hashes | MEDIUM | C-06 | synth-10 Q-60 | OPEN |
| C-06 INV-007: a dropped `prior` line (a lost veto) has no stated `blocking_state` | MEDIUM | C-06 | synth-10 Q-60 | OPEN |
| C-06 INV-008: both checkers return the first fault only; a line with two faults is dropped again after the single re-ask | MEDIUM | C-06 | synth-10 Q-60 | OPEN |
| C-06 INV-010: a cut can invent a reference token (`FR-12` cut to `FR-1`) and change `refs_norm`, `fp` and `same_defect` | MEDIUM | C-06 | synth-10 Q-60 | OPEN |
| C-06 INV-016: a rescued line whose prefix does not locate becomes a kept row with no span that no fix can touch | MEDIUM | C-06 | synth-10 Q-60 | OPEN |
| C-06 INV-019: the unchanged Normalize text and the additive sentence use "invalid" for two different states | MEDIUM | C-06 | synth-10 Q-60 | OPEN |
| C-06 INV-024: the cut removes the v2 loss unit only for the length share | MEDIUM | C-06 | synth-10 Q-60 | OPEN |
| C-06 INV-025: a truncated block loses its tail with no line to itemise; truncation stays outside the guard | MEDIUM | C-06 | synth-10 Q-60 | OPEN |
| C-06 INV-026: after the cut the refusal fires on 0 of 264, so K5 passes trivially and the code path is not exercised | MEDIUM | C-06 | synth-10 Q-60 | OPEN |
| C-06 INV-004: additive keys carry no parser or policy version; `block_ok` changes meaning | LOW | C-06 | debate result C-06 (listed here only) | CARRIED (LOW) |
| C-06 INV-011: `original_chars`, `kept_chars` and `repaired_lines_rate` have no single unit | LOW | C-06 | debate result C-06 (listed here only) | CARRIED (LOW) |
| C-06 INV-020: two refusals can occur in sequence (quorum, then `dropped_blocking`, both exit 12) and record nothing | LOW | C-06 | debate result C-06 (listed here only) | CARRIED (LOW) |
| C-06 INV-022: `card_convert.py` has its own claim cut; two implementations if a claim cut is adopted | LOW | C-06 | debate result C-06 (listed here only) | CARRIED (LOW) |
| C-07 INV-017: the ship-now set does not close the A-r3 collapse: calibrator Agent calls carry a null word in six of 15 runs, an omitted `model` falls back to `model: sonnet`, the only mechanical guard (S7) is unbuilt | HIGH | C-07 | synth-10 Q-61 | OPEN |
| C-07 INV-001: a class-word binding written as data is not compared with the session's binding before dispatch; the combo runs disagreed with the pin in 11 of 15 runs | MEDIUM | C-07 | synth-10 Q-62 | OPEN |
| C-07 INV-003: S5 is stated in two forms (`find_path` override against `--tiers`); the `find_path` form silently replaces the packaged tiers for every shadow resolve | MEDIUM | C-07 | synth-10 Q-62 | OPEN |
| C-07 INV-005: S1 does not govern calibrator calls; a replay over every Agent row would flag six runs and falsify its own prediction | MEDIUM | C-07 | synth-10 Q-62 | OPEN |
| C-07 INV-006: S4 passes if the model declines in prose; no effective-tool-list source on the Agent path; `permissionMode: plan` may block instead of the allowlist | MEDIUM | C-07 | synth-10 Q-62 | OPEN |
| C-07 INV-007: G2 has no "reads its inputs and returns a valid findings block" criterion; `--restricted` confines file tools to the working directories | MEDIUM | C-07 | synth-10 Q-62 | OPEN |
| C-07 INV-009: three reviewers on three class words leave no class for a disjoint blind calibrator; `calibrator_diversity` "full" occurs only in the collapsed run | MEDIUM | C-07 | synth-10 Q-62 | OPEN |
| C-07 INV-010: S6's "same panel for any run id" is false for the `x2` templates; exclusion paths are untested and the floor is N=2 | MEDIUM | C-07 | synth-10 Q-62 | OPEN |
| C-07 INV-011: the transcript reader's key (reviewer id or attempt id) is not stated; attempts are not reviewers | MEDIUM | C-07 | synth-10 Q-62 | OPEN |
| C-07 INV-014: executor-class exclusion expands through model-id classes, not class words; with `haiku` bound to a non-Claude model the executor's own served model can review its own work | MEDIUM | C-07 | synth-10 Q-62 | OPEN |
| C-07 INV-015: S1 and the shadow fence: applied to shadow dispatch it stops shadow being shadow; applied only under the `panel` engine it has no consumer until Stage 3 | MEDIUM | C-07 | synth-10 Q-62 | OPEN |
| C-07 INV-016: once `claude-p` is a permitted `launch` value the reflect check tests the value, not the model; a `claude-p` reviewer's tool surface lives in launcher argv with no static test | MEDIUM | C-07 | synth-10 Q-62 | OPEN |
| C-07 INV-018: the ship-now set does not change behaviour in a gateway workspace: `--env gateway` still refuses and no S item makes any caller pass an explicit tier file and environment | MEDIUM | C-07 | synth-10 Q-46 (7.0.1 CT-6) | OPEN |
| C-07 INV-002: a static fixture copy of the tier file tests its own aliases, not the packaged ones | LOW | C-07 | debate result C-07 (listed here only) | CARRIED (LOW) |
| C-07 INV-004: S1's "`launch: null` is a dispatch error" contradicts D4's legacy-rotation rule and can fire only for generic templates | LOW | C-07 | debate result C-07 (listed here only) | CARRIED (LOW) |
| C-07 INV-012: `resolve` prints a launch word for the primary pick only; a fallback model may have no word | LOW | C-07 | debate result C-07 (listed here only) | CARRIED (LOW) |
| C-08 INV-001: a torn final line from a killed writer is not handled; one torn or glued line breaks `export`, `summary` and the gate for that run | HIGH | C-08 | synth-10 Q-63 | OPEN |
| C-08 INV-002: `ingest` is called idempotent but a row for an unfinished sidechain is frozen by skip-if-present and by `export`'s deterministic `record_id` plus `INSERT OR IGNORE` | HIGH | C-08 | synth-10 Q-63 | OPEN |
| C-08 INV-005: the interactive layout stores sub-agent messages in separate `subagents/agent-<id>.jsonl` files with `parent_tool_use_id` null; the adapter as specified finds zero sidechains there | HIGH | C-08 | synth-10 Q-63 | OPEN |
| C-08 INV-006: neither join works as written: the Agent-call `description` equalled a reviewer id in 0 of 12 measured calls; the ordinal join misattributes in the permuted case | HIGH | C-08 | synth-10 Q-63 | OPEN |
| C-08 INV-009: per-event usage summation over-counts 2.0x to 2.6x (one event per content block repeats the message usage); dedup by `message.id` is not specified | HIGH | C-08 | synth-10 Q-63 | OPEN |
| C-08 INV-010: M1(c) measured at 0 of 15 runs within 2 percent on the E1 logs; there is no `modelUsage` in an interactive session | HIGH | C-08 | synth-10 Q-63 | OPEN |
| C-08 INV-011: a non-Anthropic sidechain reports `output_tokens` 0 and no cache key as readable values, so `usage_complete` would be true for a zero-cost record | HIGH | C-08 | synth-10 Q-63 | OPEN |
| C-08 INV-013: `record_absent` is printed by `export` only; a skipped `ingest` is invisible to the aggregator and passes as `requested-pinned`; no E1 run has `panel/events.jsonl` | HIGH | C-08 | synth-10 Q-64 | OPEN |
| C-08 INV-016: the `refused` row composes with C-03's quorum refusal only if raised as `LedgerError` inside the `try`; the enum has no `quorum` value; `merge_cmd.py` writes the report before `led.save` | HIGH | C-08 | synth-10 Q-64 | OPEN |
| C-08 INV-017: SKILL step 9 (identity) precedes step 10 (`ingest`); at step 9 no `events.jsonl` exists; the copy is an LLM transcription | HIGH | C-08 | synth-10 Q-64 | OPEN |
| C-08 INV-020: the hybrid alone does not close the A3 identity gap: `model_requested` is None on A3 so the mismatch is vacuous; `calibrator_diversity` stays orchestrator-computed; no code reads `identity_source` | HIGH | C-08 | synth-10 Q-44 (7.0.1 CT-4) | OPEN |
| C-08 INV-021: the hybrid alone does not close C-03 INV-001: the refused row exists only with `--events`, only for `LedgerError`, a failed events write is a stderr warning, and nothing consumes `refused` rows | HIGH | C-08 | synth-10 Q-65 | OPEN |
| C-08 INV-022: the hybrid alone does not close cost under-reporting: `cost_per_confirmed_tp` stays reviewer-only; adapter readings are wrong on the measured formats; the orchestrator snapshot is 0 or stale | HIGH | C-08 | synth-10 Q-65 | OPEN |
| C-08 INV-003: the last `orchestrator_snapshot` by events-file order can be a stale one; no monotone key | MEDIUM | C-08 | synth-10 Q-66 | OPEN |
| C-08 INV-004: one run is assumed to be one transcript file; resumes and restarts split sidechains and a partial ingest looks complete | MEDIUM | C-08 | synth-10 Q-66 | OPEN |
| C-08 INV-007: `init` has no manifest yet for the lock; one `lock_timeout` cascades through stage order; no lock-acquisition order is stated | MEDIUM | C-08 | synth-10 Q-66 | OPEN |
| C-08 INV-008: what `export` does when `strict` refuses one record is unstated; the 80-character rule passes an underscore-joined sentence; `strict` changes the existing `telemetry append` CLI | MEDIUM | C-08 | synth-10 Q-66 | OPEN |
| C-08 INV-012: the events-side `attempt` and the manifest `attempt_id` are numbered independently; a retried reviewer yields two `reviewer_run` records | MEDIUM | C-08 | synth-10 Q-66 | OPEN |
| C-08 INV-015: a served id is not normalised (`qwen3.8-max` against `Qwen3.8-max`); "collapse" as id-equality or class-equality is unwritten | MEDIUM | C-08 | synth-10 Q-66 | OPEN |
| C-08 INV-018: deterministic `record_id` makes `export` idempotent per id only; a record from another route under a different id is counted twice; the append-time refusal breaks a pinned test | MEDIUM | C-08 | synth-10 Q-66 | OPEN |
| C-09 INV-001: the environment is detected once from the process env alone (`$T3Model01`), which may differ from the workspace view ccsession uses | MEDIUM | C-09 | synth-10 Q-67 | OPEN |
| C-09 INV-005: "the packaged file is the file `panel resolve` reads" fails when an override tier file replaces it; the guard reads only the packaged file | MEDIUM | C-09 | synth-10 Q-67 | OPEN |
| C-09 INV-009: "Coder slot first, then the repo edits" has no gate; merging the `T4Model04` line before every workspace env carries it breaks tier mode there | MEDIUM | C-09 | synth-10 Q-67 | OPEN |
| C-09 INV-010: `requested_slots` follows `apply_to`, not the kind name; no test takes the branch where `apply_to` holds both kinds | MEDIUM | C-09 | synth-10 Q-67 | OPEN |
| C-09 INV-012: the ascending-count sort key; the agreed tests cannot tell the two candidate keys apart (this is C-007) | MEDIUM | C-09 | synth-10 Q-67 | OPEN |
| C-09 INV-019: scarcest-first with two excluded classes on `live7` falls below the optimum in 27 of 1840 resolutions and below template order in 3 | MEDIUM | C-09 | synth-10 Q-67 | OPEN |
| C-09 INV-021: the spec loop does not hand the resolution to merge, so `requested_slots` does not reach the denominator of C-03 INV-007 there | MEDIUM | C-09 | synth-10 Q-42 | OPEN |
| C-09 INV-026: "the loop gains distinct gateway panels" is true of requested ids only; the gateway has no dispatch mapping and served identity belongs to C-08 | MEDIUM | C-09 | synth-10 Q-46 (7.0.1 CT-6) | OPEN |
| C-09 INV-003: library and CLI orders differ without a trace in the artifact | LOW | C-09 | debate result C-09 (listed here only) | CARRIED (LOW) |
| C-09 INV-004: statistics cover `fixed` and `random` slots only; a `round_robin` slot depends on the date | LOW | C-09 | debate result C-09 (listed here only) | CARRIED (LOW) |
| C-09 INV-011: a fixed anchor with count above 1 can resolve two reviewers to one model | LOW | C-09 | debate result C-09 (listed here only) | CARRIED (LOW) |
| C-09 INV-017: the ember insertion index changes `fallback_depth` of Haiku | LOW | C-09 | debate result C-09 (listed here only) | CARRIED (LOW) |
| C-09 INV-018: the ember edit list omits the `profiles` and `picker` entries that `MODEL-TIERS.md:189-192` names | LOW | C-09 | debate result C-09 (listed here only) | CARRIED (LOW) |
| C-10 INV-002: panel standing, reviewed SHA and dropped list have no durable home across `--resume`; a new run-log event edits `models.py` and pinned tests | HIGH | C-10 | synth-10 Q-68 | OPEN |
| C-10 INV-007: "requested" is defined as the dispatched count, so a slot that fails to launch makes a 2-of-3 panel read present | HIGH | C-10 | synth-10 Q-69 | OPEN |
| C-10 INV-008: a reviewer with an empty findings block is invalid unless a non-empty Coverage slice was assigned (`findings_v2.py:291-298`); a PR has no Coverage rows, so a clean panel can never read present | HIGH | C-10 | synth-10 Q-69 | OPEN |
| C-10 INV-011: "present when every requested reviewer is complete" is vacuously true for an empty requested set | HIGH | C-10 | synth-10 Q-69 | OPEN |
| C-10 INV-012: AM-1 splits by category only; a same-category cluster still pairs the maximum severity with the representative's unrelated claim and line | HIGH | C-10 | synth-10 Q-70 | OPEN |
| C-10 INV-001: the standing enum has no stale value; after a fix push the report is absent or present for an old SHA | MEDIUM | C-10 | synth-10 Q-71 | OPEN |
| C-10 INV-003: the checkout the reviewers see is not shown to equal the PR head tree used for `snapshot_file_list` and `changed_ranges` | MEDIUM | C-10 | synth-10 Q-71 | OPEN |
| C-10 INV-006: missing `changed_ranges` degrading to `in_diff` unset (True) is permissive for editing; nothing says the rule is report-only-only | MEDIUM | C-10 | synth-10 Q-71 | OPEN |
| C-10 INV-009: the unit of "dropped" differs from the unit of "cluster", so a CRITICAL can be lost while standing stays present | MEDIUM | C-10 | synth-10 Q-71 | OPEN |
| C-10 INV-010: `blocking_clusters` counts the reviewer-typed boolean, so a run can say clean beside a CRITICAL non-blocking cluster | MEDIUM | C-10 | synth-10 Q-71 | OPEN |
| C-10 INV-014: no rule excludes panel Findings from `dedup_groups` input, so a panel Finding could raise a bot group's route | MEDIUM | C-10 | synth-10 Q-71 | OPEN |
| C-10 INV-015: the "not clean" wording rule covers the run summary only, not the posted thread or the literal `terminal_clean` status (eight sites in `fsm.py`) | MEDIUM | C-10 | synth-10 Q-71 | OPEN |
| C-10 INV-018: the converter's inputs cannot be produced by existing machinery (`review cluster` writes no parsed records; `parse_block` carries no category set); the invocation path is unspecified | MEDIUM | C-10 | synth-10 Q-71 | OPEN |
| C-10 INV-019: `finding_from_comment` needs a positive int `comment_id`; a key map that passes the v2 finding id or cluster id raises for every cluster | MEDIUM | C-10 | synth-10 Q-71 | OPEN |
| C-11 INV-002: the lens-identity check is undefined when a report's first line names no lens (only 37 of 517 reflect-reviewer returns start with the mandated heading); identity is self-declared | HIGH | C-11 | synth-10 Q-72 | OPEN |
| C-11 INV-009: "the dispatched slot's path" is not unique for partition instances of one lens; no slot id exists in `/task` once the per-slot key was withdrawn, so N1's overwrite can recur | HIGH | C-11 | synth-10 Q-72 | OPEN |
| C-11 INV-012: the hash and lens-line checks sit in step 10, after consolidation (6), fix (7), verification (8) and the proceed decision (9) | HIGH | C-11 | synth-10 Q-73 | OPEN |
| C-11 INV-015: the sha256 is taken over the executor's own write, proving later non-clobber, not equality with the returned text; return volume and the returned-not-yet-written window are not handled | HIGH | C-11 | synth-10 Q-73 | OPEN |
| C-11 INV-016: arm 0 and arm 1a differ in more than the tool list (content lenses run `rf-qa-qualitative` in arm 0); "zero-trust section" exists only in the dropped fix-cycle section (`rf-qa.md:418`) | HIGH | C-11 | synth-10 Q-74 | OPEN |
| C-11 INV-017: pre-computed counts exist in the oracle but no changed gate step adds a pre-computation step at a production gate; single-document seeds cannot exercise the multi-file or partitioned checks | HIGH | C-11 | synth-10 Q-74 | OPEN |
| C-11 INV-001: the oracle's parent permission mode, installed hook set and model alias are not pre-registered | MEDIUM | C-11 | synth-10 Q-75 | OPEN |
| C-11 INV-003: the tree-hash scope is unspecified: excluding `qa/` blinds it to N1's class; git state and `/tmp` scratch are not covered | MEDIUM | C-11 | synth-10 Q-75 | OPEN |
| C-11 INV-004: the subset guard checks the source file; runtime resolves project `.claude/agents/` then `~/.claude/agents/` (`verify-sync` does not cover the installed copy); the reflect guard parses only the inline `tools:` form | MEDIUM | C-11 | synth-10 Q-75 | OPEN |
| C-11 INV-007: "the standard eight lens dimensions" does not map one-to-one onto what a gate spawns; eight per-dimension pass decisions with no multiplicity control | MEDIUM | C-11 | synth-10 Q-75 | OPEN |
| C-11 INV-008: the audit misses nested spawns and renamed tool names; its counts are regex-dependent and already differ between advocates | MEDIUM | C-11 | synth-10 Q-75 | OPEN |
| C-11 INV-010: the Confidence Gate formula is undefined at TOTAL = UNVERIFIABLE and rewards capability loss; no production cap on the UNVERIFIABLE share | MEDIUM | C-11 | synth-10 Q-75 | OPEN |
| C-11 INV-013: `test_c_s1_s3_copied_verbatim` iterates a fixed 10-file tuple and does not reach a new agent file; an `rf-`-named file triggers the Tavily parity tests | MEDIUM | C-11 | synth-10 Q-75 | OPEN |
| C-11 INV-014: the `rf-qa.md` body and the installed SubagentStart hook tell agents to write their output file, which pushes a read-only agent to write or to return only a pointer | MEDIUM | C-11 | synth-10 Q-75 | OPEN |
| C-11 INV-018: the conditional switch does not name the other spawn sites in `task/SKILL.md`, and the step-8 verifier protocol lives in the dropped fix-cycle section | MEDIUM | C-11 | synth-10 Q-75 | OPEN |
| C-11 INV-006: the reflect-reviewer allowlist refused 7 calls across 517 runs, not 2; no rule for adding read-only tools as names change | LOW | C-11 | debate result C-11 (listed here only) | CARRIED (LOW) |
| C-12 INV-005: H1 reaches reflect through the reflect brief with no call-site change, but the brief is built in `cli/reflect/ensemble.py:601-630` and does not carry `spec_path`, so naming the driving spec needs an edit in `cli/reflect` | HIGH | C-12 | synth-10 Q-41 (7.0.1 CT-1) | OPEN |
| C-12 INV-009: H2 (a repair, possibly a re-ask) is core now and compatible with C-01's placement inside both `parse_block` functions while C-01 INV-003 and C-06 are open | HIGH | C-12 | synth-10 Q-43 (7.0.1 CT-2) | OPEN |
| C-12 INV-002: the served-model and act-rate probe record has a home | MEDIUM | C-12 | synth-10 Q-76 | OPEN |
| C-12 INV-003: a reserved `exchange` key is "a pin, not an implementation" (`panel.py:37-46,160-176` rejects unknown panel keys, so it is code and changes the template hash) | MEDIUM | C-12 | synth-10 Q-76 | OPEN |
| C-12 INV-004: the off-state byte test coexists with H1 shipping unconditionally (baseline undefined) | MEDIUM | C-12 | synth-10 Q-76 | OPEN |
| C-12 INV-006: a single kit cost figure can gate `kit: on` (elapsed against token metric, panel size) | MEDIUM | C-12 | synth-10 Q-76 | OPEN |
| C-12 INV-007: a hold-out of at least 4 unseen defects is satisfiable on the 16-item ground truth | MEDIUM | C-12 | synth-10 Q-76 | OPEN |
| C-12 INV-008: a sidecar keyed by reviewer id and finding id is unambiguous across rounds and merged rows | MEDIUM | C-12 | synth-10 Q-76 | OPEN |
| C-12 INV-010: one catalogue source per module, rendered from the installed form, a single data source with X-13 | MEDIUM | C-12 | synth-10 Q-76 | OPEN |
| C-12 INV-011: "quorum counts over own-origin lines only" is a quantity C-02 and C-03 compute | MEDIUM | C-12 | synth-10 Q-76 | OPEN |
| C-12 INV-013: the A-layer alone gives mutually blind reviewers (the reflect isolation snapshot is pinned off, `models.py:92-100`) | MEDIUM | C-12 | synth-10 Q-76 | OPEN |
| C-12 INV-014: the enable trigger can be met on a lane that can host exchange (tasklist review reaches the panel through reflect, which has no hook-capable lane at HEAD) | MEDIUM | C-12 | synth-10 Q-76 | OPEN |
| C-12 INV-015: the A-layer alone is cost-safe (H2 re-ask spend is not priced or capped) | MEDIUM | C-12 | synth-10 Q-76 | OPEN |
| C-12 INV-016: the premise "no exchange arm has been measured against the static kit" still holds at the current E2 head | MEDIUM | C-12 | synth-10 Q-76 (see Q-39) | OPEN |
| X-13 INV-001: `observed` is said to have one writer (the new entry point) but `SKILL.md:345` still tells the orchestrator to write `panel/coverage.json` itself; the two Round 2 lists disagree on whether the writer computes `observed` | HIGH | X-13 | synth-10 Q-77 | OPEN |
| X-13 INV-019: the built-now set alone cannot make process-catchable defects get examined: no module declares cards before G-2 and G-3, no brief renderer exists, `_SLOT_KEYS` stays closed | HIGH | X-13 | synth-10 Q-78 | OPEN |
| X-13 INV-002: in reflect the file the entry point would parse is the orchestrator-assembled `panel/cards/reviewer-<N>.md`; a model-made copy can drop, merge or invent a row; a fourth reviewer-id space exists | MEDIUM | X-13 | synth-10 Q-79 | OPEN |
| X-13 INV-004: step 4 parses the card before the sidecar is written at step 6; a compliant clean reviewer can be judged invalid | MEDIUM | X-13 | synth-10 Q-79 | OPEN |
| X-13 INV-005: the entry point writes fixed paths with no round or review-kind argument; a re-run overwrites round 1 evidence | MEDIUM | X-13 | synth-10 Q-79 | OPEN |
| X-13 INV-006: no row-id grammar or type rule; recorded ids include slugs, a `/` and a range token; a non-string id aborts a whole command | MEDIUM | X-13 | synth-10 Q-79 | OPEN |
| X-13 INV-007: the check rules need a path and a quote kind that no row field carries; `ran` has no bound; unknown row keys unspecified | MEDIUM | X-13 | synth-10 Q-79 | OPEN |
| X-13 INV-009: `assigned`, `observed`, `rows_total`, the module row cap and the 12 of E2 are inconsistent (21 of 69 recorded entries exceed 12 assigned rows; uniform binding multiplies rows) | MEDIUM | X-13 | synth-10 Q-79 | OPEN |
| X-13 INV-010: row quote boundaries disagree (12-character minimum against C4/C8 short literals; whole-candidate test against the line-window basis of the measured failure rates) | MEDIUM | X-13 | synth-10 Q-79 | OPEN |
| X-13 INV-011: compliance feeds quorum arithmetic only through the empty-block rule; the paths differ by engine (v1 truncation behind a longer row block; v2 invalid clean reviewers drop out) | MEDIUM | X-13 | synth-10 Q-79 | OPEN |
| X-13 INV-014: what `assigned` holds per card, what the loader does with a bad card, and the rule for duplicate row ids are unspecified | MEDIUM | X-13 | synth-10 Q-79 | OPEN |
| X-13 INV-015: the v1 loop edit is the rules file plus its plugin byte copy, not `commands/spec-panel.md`; the pinned "last section" sentence constrains a row block before the findings block | MEDIUM | X-13 | synth-10 Q-79 | OPEN |
| X-13 INV-016: in shadow mode the card body still reaches the legacy debate; the manifest freezes the sha256 of `refs/reviewer-spec.md`; the order against the `reviewer_model_self_report` line is unstated | MEDIUM | X-13 | synth-10 Q-79 | OPEN |
| X-13 INV-017: `review-telemetry/1` reviewer records are closed; new counters fit only in `context` or a new schema version; the leak test is trivially true if the counters go nowhere | MEDIUM | X-13 | synth-10 Q-79 | OPEN |
| X-13 INV-020: advisory checks need a reader and a route to the fix (the v1 merge report prints ledger rows only; the v2 host is opt-in shadow mode that feeds nothing) | MEDIUM | X-13 | synth-10 Q-79 | OPEN |
| X-13 INV-008: UNSURE counts as observed, so an all-UNSURE clean report passes the guard (open as D-6) | LOW | X-13 | debate result X-13 (listed here only) | CARRIED (LOW) |
| X-14 INV-001: a rule committed after C-02 lands can still be measuring a kernel that C-03 and C-06 later change; an offline run on the 71 stored rows may not predict the live metric | HIGH | X-14 | synth-10 Q-80 | OPEN |
| X-14 INV-002: git commit order is not execution order, nothing stamps the rule commit sha into the run record, and a squash merge can rewrite order | HIGH | X-14 | synth-10 Q-80 | OPEN |
| X-14 INV-003: re-parse conservation can give false flags when parser or policy version drifts; the ledger entry stores no version and C-06 puts the cut behind `repair=False` | HIGH | X-14 | synth-10 Q-80 | OPEN |
| X-14 INV-005: no expected-cells manifest exists in any adjudicated output or E2 run; a post-hoc manifest of the surviving cells would pass completeness | HIGH | X-14 | synth-10 Q-81 | OPEN |
| X-14 INV-006: a verifier record that is all `unrecorded`, or a truncated `flags.tsv`, satisfies a "record exists" refusal; flags-only output makes a crashed verifier read as clean | HIGH | X-14 | synth-10 Q-81 | OPEN |
| X-14 INV-007: the judge writes its own three counts and `gt_covered_blocking` has no (GT id, row id) map, so the wrapper equation is only arithmetic self-consistency | HIGH | X-14 | synth-10 Q-81 | OPEN |
| X-14 INV-013: the unit of analysis is not named (the 71 rows hold 32 multisets; 81 of 89 catches sit on two items), so a row-level test is anti-conservative | HIGH | X-14 | synth-10 Q-82 | OPEN |
| X-14 INV-019: the adjudicated C-06 hybrid already adds `repaired` and `dropped` keys to each reviewer entry; the verifier must read them and give an acknowledged drop a defined flag state | HIGH | X-14 | synth-10 Q-83 | OPEN |
| X-14 INV-021: the verifier reports `unrecorded` where C-08's identity gate maps a skipped `ingest` to `requested-pinned`; two readers of one file have different absent-input semantics | HIGH | X-14 | synth-10 Q-44 (7.0.1 CT-4) | OPEN |
| X-14 INV-025: the metric of record and the conservation law are defined on `review-ledger/1` rows; no acceptance metric exists for the reflect Tier 2 panel, UC-1, UC-2, PR review or rf-qa | HIGH | X-14 | synth-10 Q-84 | OPEN |
| X-14 INV-026: the answer-key and tool-use defect class has no component; if C-08's M1 fails, identity stays `unrecorded`, Tier S can never be `pass` and "accepted" is unreachable for every use case | HIGH | X-14 | synth-10 Q-44 (7.0.1 CT-4) | OPEN |
| X-14 INV-027: inline enumeration: an identity swap, a dispatch-skipped cell, a judge row mismatch with consistent counts and a post-hoc rule each pass every gate; only parser drift fails a gate, and falsely | HIGH | X-14 | synth-10 Q-85 | OPEN |
| X-14 INV-004: ledgers written before and after C-02 are read differently (stored `verdict`/`decision`/`brief_ids` against derived on read) | MEDIUM | X-14 | synth-10 Q-86 | OPEN |
| X-14 INV-008: the single severity policy file decides the audit-clean population, yet the pre-registered set does not name it | MEDIUM | X-14 | synth-10 Q-86 | OPEN |
| X-14 INV-011: "71" is not one population and the denominators 8 and 14 ignore the control's 2 items | MEDIUM | X-14 | synth-10 Q-86 | OPEN |
| X-14 INV-012: part of the 89 against 38 gap may be rejected blocking lines (C-06), not severity typing, so M-7 cannot attribute a move to C-02 | MEDIUM | X-14 | synth-10 Q-86 | OPEN |
| X-14 INV-015: the expected cell has no attempt component; an empty manifest passes completeness vacuously; cells absent from the manifest get no flag | MEDIUM | X-14 | synth-10 Q-86 | OPEN |
| X-14 INV-016: the headline and "control found" are undefined for a package with zero blocking-in-implement items | MEDIUM | X-14 | synth-10 Q-86 | OPEN |
| X-14 INV-017: M-6 may not show the gate bites: on real data the repaired gate can only move FAIL to INSUFFICIENT-RUNS (15 tracked runs against 20 required) | MEDIUM | X-14 | synth-10 Q-86 | OPEN |
| X-14 INV-018: one run per cell and one judge pass per (package, label) leave the noise floor unknown | MEDIUM | X-14 | synth-10 Q-86 | OPEN |
| X-14 INV-020: "ledger row typed blocking" is not one stable field after C-02's CRITICAL floor; the rule must name the field and the merge-policy version | MEDIUM | X-14 | synth-10 Q-86 | OPEN |
| X-14 INV-022: `.gitignore:13` (`lib/`, `build/`, `dist/`, `parts/`, `var/`) can hide harness modules that pass locally and are missing in CI | MEDIUM | X-14 | synth-10 Q-86 | OPEN |
| X-14 INV-023: path-less CI `pytest -n auto --maxfail=3` collecting harness tests over untracked study data fails or skips on a clean clone | MEDIUM | X-14 | synth-10 Q-86 | OPEN |
| X-14 INV-028: the 16-item ground truth has unrecorded authorship and one implement run per plan; Tier G has no owner | MEDIUM | X-14 | synth-10 Q-86 | OPEN |
| X-14 INV-029: a post-run verifier finds a bad run after the judge cost is paid; the identity-overwrite fix sits in a launcher that is untracked at HEAD | MEDIUM | X-14 | synth-10 Q-86 | OPEN |
| X-15 INV-017: "nothing loosens before measurement, so H+ is behaviour-preserving" does not hold: the H+ block routes its Low class away from `SK:1439, :1537, :1571, :1608, :1614`, which count Medium today | HIGH | X-15 | synth-10 Q-87 | OPEN |
| X-15 INV-018: "grading block + tie-break-up + dedup-highest makes the boundary safe" does not hold: `SK:1608` re-runs the full Stage 7 set with fresh agents; dedup acts inside one run; the only evidence is F3 on 2 samples | HIGH | X-15 | synth-10 Q-87 | OPEN |
| X-15 INV-001: `ValidationReport.md` is written once from the first Stage 7 merge; a Medium or Low first seen at a re-run is listed nowhere | MEDIUM | X-15 | synth-10 Q-88 | OPEN |
| X-15 INV-003: no CRITICAL floor exists in code yet and it covers CRITICAL only; H+ puts the dropped-criterion class in unprotected MAJOR | MEDIUM | X-15 | synth-10 Q-45 (7.0.1 CT-5) | OPEN |
| X-15 INV-004: `SK:1410` leaves "the same issue on the same task" to the model; keep-highest may drop the entry whose `Exact fix` covers the defect | MEDIUM | X-15 | synth-10 Q-88 | OPEN |
| X-15 INV-005: the containment test T2(a) and (b) cannot pass as written; a static test catches deleted phrases, not changed meaning | MEDIUM | X-15 | synth-10 Q-88 | OPEN |
| X-15 INV-007: `F_k` counts post-dedup findings while the loop works on task ids; a re-grade can lower the size of `F_k` with no patch | MEDIUM | X-15 | synth-10 Q-88 | OPEN |
| X-15 INV-008: `SK:1703, :1705, :1716, :1766` and the totals line `SK:1462` state severities, are in neither edit list and are unpinned | MEDIUM | X-15 | synth-10 Q-88 | OPEN |
| X-15 INV-010: (A+ only) the clean template has a slot for Low notes only; a Medium-only bundle's report is unspecified | MEDIUM | X-15 | synth-10 Q-88 | OPEN |
| X-15 INV-011: F1 to F3 rest on two archived bundles and per-finding thresholds; no threshold fixes bundles, repeats or unit | MEDIUM | X-15 | synth-10 Q-88 | OPEN |
| X-15 INV-013: tie-break-up enlarges the blocking set; a Low-graded PASS item re-graded Medium trips the regression halt; a `blocked` retry re-samples the graders | MEDIUM | X-15 | synth-10 Q-88 | OPEN |
| X-15 INV-014: H+ keeps `SK:1421-1422` MEDIUM while the adopted block calls omissions High; A+ regrades them High but the CLI keeps missing TDD coverage MEDIUM | MEDIUM | X-15 | synth-10 Q-88 | OPEN |
| X-15 INV-019: eleven filters sit between a Stage 7 finding and the verdict; seven are "not shown" until measured or specified | MEDIUM | X-15 | synth-10 Q-88 | OPEN |
| X-15 INV-020: F1 cannot fail H+ by construction and cannot test the High/Medium line (both archived bundles have High 0); no registered outcome withdraws the Low class | MEDIUM | X-15 | synth-10 Q-88 | OPEN |
| X-15 INV-002: the byte-equal fixture guard skips when the plan copy is absent and does not assert the 12-row group; an insertion after `SK:1391` shifts every SK line cite | LOW | X-15 | debate result X-15 (listed here only) | CARRIED (LOW) |
| X-15 INV-009: the "76 lines in 10 files" against "88 lines in 14 files" count is unreconciled | LOW | X-15 | debate result X-15 (listed here only) | CARRIED (LOW) |
| X-15 INV-012: a one-task phase has one grader, so dedup and tie-break-up cannot act | LOW | X-15 | debate result X-15 (listed here only) | CARRIED (LOW) |

## 5. Final checks (run 2026-11-15 after the last edit)

| Check | Result |
|---|---|
| Grep with the escaped pattern `\[PENDING-ADJUDICATION` over `synthesis/` (content mode) | "No matches found" (a normal empty result, no error message); before the fold it matched 18 lines of synth-07 |
| Grep `ADJUDICATION-FOLD-PENDING` over `synthesis/` | "No matches found" (normal empty result); before the fold it matched one row of synth-10 |
| Grep `marker A-` over `synthesis/` | one hit remains, in the synth-07 research coverage table (a different "marker A-8" sentence), edited to "choice A-8, adjudicated in debate C-04 as an analysis too"; no pending marker remains |
| Every undecidable conflict slot has an outcome | 15 of 15 rows in synth-06 6.12.9.1; none `NOT ADJUDICATED`; the 6.12.9 slot column shows both names for C-13 (X-13), C-14 (X-14), C-15 (X-15) |
| synth-07: 18 markers replaced | The 18 choices A-3 to A-20 each carry winner, conditions and folder path; the three slugs with two markers (ledger-clearing-and-verdict-authority, core-shape-and-finding-contract, eval-acceptance-and-harness-owner) are covered by A-4 and A-9, A-15 and A-16, A-11 and A-20 |
| Invariant table | 244 rows (60 HIGH, 161 MEDIUM, 23 LOW) counted by Grep in synth-07 7.3; a Python read-only check mapped each of the 221 HIGH and MEDIUM rows to a Q row of synth-10 9.10 that cites the same slot and invariant id (0 mismatches; 56 Q rows, Q-38 to Q-93) |
| Table shape | A column-count check of every table block in the five files found no mismatch in any table the fold added; the 12 mismatches found in synth-05 are in pre-existing tables (lines 130, 159, 561-569, 623) and were not touched |
| Files edited | `synthesis/synth-05-options.md`, `synth-06-conflict-log.md`, `synth-07-recommendation-architecture.md`, `synth-09-sequence-and-gates.md`, `synth-10-questions-evidence.md`; this report. The task file was not read beyond line 444 and not edited; `TASK-RESEARCH-review-panel-unify-20261113-155942/` and `REVIEW-PANEL-UNIFY-RUN2-QUEUED.md` were not read, listed, searched or cited |

Status: Complete
