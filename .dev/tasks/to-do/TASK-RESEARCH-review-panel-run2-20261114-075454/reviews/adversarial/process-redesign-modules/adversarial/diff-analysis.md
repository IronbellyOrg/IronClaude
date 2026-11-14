# Diff Analysis: process-redesign-modules (slot X-13, synth-06 C-13) Comparison

## Metadata
- Generated: 2026-11-14 (orchestrator, single pass; both variants read in full; five code facts spot-checked, see Verification notes)
- Variants compared: 2 (Variant A = Proposal A, Sweep-Sheet-shaped, `variant-1-original.md`; Variant B = Proposal B, Recipe-Ledger-shaped, `variant-2-original.md`)
- Focus areas: correctness, risk, test-coverage
- Total differences found: 29 debate points (4 structural, 13 content, 9 contradictions, 3 promoted shared assumptions) plus 17 unique contributions listed without a debate ID
- Categories: structural (4), content (13), contradictions (9), unique (17), shared assumptions (5 surfaced, 3 promoted)
- Taxonomy column (L1 surface, L2 structural, L3 state mechanics) is the auto-tag required by the debate-topic taxonomy; each point has exactly one level.

## Structural Differences

| # | Area | Variant A | Variant B | Severity | Level |
|---|------|-----------|-----------|----------|-------|
| S-001 | Section set and order | 8 H2 sections: position, design consequence, evidence (3.1-3.6), invariants, test, consistency with C-01..C-03, PR/rf-qa effect, objection. Consistency section comes after the evidence. | 9 H2 sections: position, consistency with C-01..C-03 (a table), design consequence, evidence (E1-E16), invariants, test, PR/rf-qa effect, objection, non-claims. Consistency comes before the design. | Low | L1 |
| S-002 | Evidence presentation | Prose subsections 3.1-3.6 with inline tags | Numbered table E1-E16 with a tag column | Low | L1 |
| S-003 | Closing section | None; limits are conceded inside section 8 ("What A concedes") | Section 9 "What this proposal does not claim" | Low | L1 |
| S-004 | Invariant naming and consistency format | Invariants named by descriptive label (INV-G, INV-H, INV-C) inside prose bullets | Consistency with adjudicated slots as a two-column table; invariants INV-A..INV-N in a Preserved / Endangered list | Low | L2 |

## Content Differences

| # | Topic | Variant A Approach | Variant B Approach | Severity | Level |
|---|-------|-------------------|-------------------|----------|-------|
| C-001 | What the core adds | (a) card-file loader and validator, (b) one CLI entry point that runs a module's extractors and writes per-reviewer sheets and the sidecar `assigned` lists, (c) additive advisory flags in `precheck.json`. No per-row verdict block, no demotion, no promotion, no lens-to-model binding. | (1) recipe cards as module data, (2) slot key `recipes` in `_SLOT_KEYS`, (3) brief renderer appends recipe text, (4) row block `rows-v1`, (5) `review-rowcheck/1` second output, (6) overlay with demotions and promotions, (7) counts-only telemetry. All optional and data-driven. | High | L2 |
| C-002 | Per-item answer and what `observed` means | A reviewer writes a normal finding with `coverage_rows: [<item id>]` (v2) or an open key such as `probe` (v1); an item with no finding is reported in `observed` through the existing mechanism; `observed` is a declaration. | Reviewer writes one row per recipe step (OK / PROBLEM / UNSURE, `quote_plan`, `quote_other`, `problem`, `ran`); `assigned` is computed from recipes, `observed` from parsed rows; empty block is complete only if every assigned row is observed. | High | L3 |
| C-003 | Class card schema | Fields per MR2 3.0.3: definition, question template, extractor, route, applies_to, instances, known weakness. | Same card plus `search_forms` keyed by tool name and `requires_tools`; `extractor` optional and unused; `recipe_text` at most 120 words. | Low | L2 |
| C-004 | Post-run check output | Reuses `verify_cmd._check` unchanged; additive item-evidence flags in `precheck.json`, emitted only when a sheet exists. | Second output file `review-rowcheck/1`; `review-precheck/1` and its `reread_set` stay byte-identical; `check_skipped` for tool-line quotes. | Medium | L2 |
| C-005 | Module-by-module scope | Tasklist: all 8 classes, first extractors C4 and C8 plus candidate listers C5 and C2. Spec review: E1, E2, E5, E7 on v1. Reflect: reuses Wave 1B requirement-row extraction for C2, v2 engine. PR review and rf-qa: E3 and E4 in the script. | Spec loop: primary target, profile default `rowcheck: advisory`. Tasklist and workflow via reflect UC-1: same cards. Reflect: no `recipes`, `rowcheck: off`. PR review and rf-qa: section 7. | Medium | L2 |
| C-006 | Dependence on the engine chosen in C-01 | Works on either engine; on v1 the item link is an unvalidated key, so the module's own advisory check must validate it against the sheet. | "observed is computed" holds only in the v2 parser; in v1 the row block is advisory and a missing block is counted as `rows_missing`. | Medium | L3 |
| C-007 | Measurement plan | M1 offline per class (recall at or above a pre-registered floor, beats random, runtime, byte-identity), M2 shadow mode with found-at-any and found-at-blocking reported separately, M3 against arm K, M4 non-regression and precision, M5 invariants. | Code tests T-B1..T-B7 (golden briefs, slot-key rejection, fence isolation, overlay rules, card lint, telemetry, reflect matrix), M-B1 compliance spike, M-B2 four arms (Z0, K, RL, SS), M-B3 demotion safety offline. | Medium | L3 |
| C-008 | What remains if the gates fail | Degrades by construction to the card loader plus the sidecar entry point (synth-05 option 4, "absorb the reusable pieces"); a failing class ships as card text with no extractor. | Demotion and promotion stay off in every packaged profile until M-B3 passes; the third option (adopt neither) is explicitly not argued. | Medium | L2 |
| C-009 | Build size and upkeep framing | Admits one extractor at a time; commitment unit is an extractor; acknowledges no extractor exists and synth-05 rates the option XL, High risk. | No pre-pass and no extractor, so no script to keep in step with module documents; E2 planning values about 760 lines against 1,100 to 1,250 (planning values, unverified); tie rule favours Recipe Ledger. | Medium | L2 |
| C-010 | CB-2 versus the Medium routing (CO-24) | CB-2 not adopted into the core; brief lines 31-32 stay; a module wanting CB-2 declares it in its own brief profile; measurement reports two severities separately. | Grading and Medium routing stay; CB-2's aim is carried by the row block: a PROBLEM row with no finding is listed under follow-up candidates, and promoted into the findings block only when the profile enables promotion. | Medium | L2 |
| C-011 | Future PR code review | Reverse-dependency and whole-tree searches (E3, E4) run in the script (codegraph callers allowed); reviewers stay shell-free. | A code-review lens is a recipe card bound to a slot through `recipes` (for example C8 in PR form using `codegraph_callers`); rows never reach `pr_submit`; a promoted `src=rows` line can be discarded or mapped to Low. | Medium | L2 |
| C-012 | rf-qa replacement | Adopt the sidecar and cards as one container shared with reflect and PR review; states that A gives no per-row proof of examination. | Maps OK, UNSURE and missing row to rf-qa marks `[x]`, `[?]`, `[ ]` (design inference, not a tested equivalence); per-slot `recipes` as restricted checklist; does not supply agent-count floors, the read-only change or the replay oracle. | Medium | L2 |
| C-013 | Naming | No block named "ledger"; a later per-row carrier would need a different noun (`<noun>-v<N>` convention). | `rows-v1`, `review-rowcheck/1`, tag `src=rows`, counter `rows_missing`; slot key named `recipes` for stated reasons. | Low | L1 |

## Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Impact | Level |
|---|-------------------|-------------------|-------------------|--------|-------|
| X-001 | Does the process layer need a script that runs before the review? | "Deterministic scripts (no model, stdlib only) build typed pre-pass items; each reviewer receives its assigned items with the script's tool output attached" (A section 1). | "Nothing runs before the review (no pre-pass, no extractor), so the process adds no script that has to be kept in step with each module's documents" (B section 1). | High | L2 |
| X-002 | May the core carry demotion of an unsupported finding and promotion of an unlinked PROBLEM row? | "No demote or promote in the core" (A 3.3, GQ-130); checks are advisory exactly as `verify-citations` is. | The core can carry both behind a switch, off in every packaged profile; a CRITICAL finding is never demoted; a promoted line is MINOR, non-blocking, tagged `src=rows` (B sections 3 item 6, 8). | High | L3 |
| X-003 | Does demotion or promotion break the repository's single-authority rule for finding status and drops? | Yes in spirit: "At HEAD no component edits a reviewer finding before the merge" (`ledger.py:3-4`: "Only this module changes a finding's status"); promotion "writes a finding the reviewer did not write". | No: a promoted line is non-blocking and "cannot change a verdict"; demotion only lowers one reviewer's own flag; reviewer report files are never edited and nothing is dropped (B section 8 point 4). Concedes B presses on C-03's fail-closed asymmetry and that the UNION case (another reviewer's flag holds) covers only the multi-reporter case. | High | L3 |
| X-004 | Can recipes be run by the read-only reviewer? | The E2 recipes R-C4 ("run it on a scratch string with Bash") and R-C8 (`git grep -l -F`) need a shell that `reflect-reviewer` lacks (`reflect-reviewer.md:5, :8`); a recipe telling a reviewer to run Bash excludes the read-only agents from PR review and reflect; so shell work belongs in the script. | Rewrite per tool: `search_forms` keyed by tool name, `requires_tools` lint against the module's reviewer tool list, test T-B5; cost stated: C4 loses its script-run test and keeps a Grep form whose equivalence to the shell dialect is UNVERIFIED; `ran` is recorded and unverified. | Medium | L2 |
| X-005 | Does the design need a binding from process content to a slot or model (GQ-131)? | No: the script assigns items per reviewer and the sidecar already keys by `reviewer-<N>`; "nothing binds to a model name". | Yes: slot keys are closed (`_SLOT_KEYS`, `panel.py:46`, rejection at `:214-216`), so a deliberate `recipes` key is added; binding by `slot_id`, never by model name. | Medium | L3 |
| X-006 | Is CB-2's aim ("list every defect, non-blocking too") inside or outside the core? | Outside: not adopted into the core; the conflict with Medium routing is removed by not adopting it. | Inside via the row block: PROBLEM rows without a finding appear under follow-up candidates; promotion into findings is switch-gated. B calls this a [DESIGN] answer, not a finding. | Medium | L2 |
| X-007 | Does a per-row verdict carry evidence that an assigned item was examined? | No: "`observed` is a declaration, so a reviewer can rubber-stamp"; the per-row verdict is "also a self-report" (A section 8); A concedes the core cannot prove examination. | Rows make `observed` computed and an unobserved empty report refused (`findings_v2.py:291-298`, verified); but `ran` is "recorded and unverified" until the C-08 transcript adapter, and in v1 the block is advisory. | Medium | L3 |
| X-008 | Which design has the evaluable-without-a-model first gate? | A: its first gate (pre-pass recall, rank beats random) is a pure script run over recorded plans, while the Recipe Ledger's first gate (`ledger_missing` at most 10 percent) needs a model spike. | B: its M-B1 compliance spike is the first gate and is a model run; it states that no arm has run for either design and that D2 fails either design if it meets its own central estimate. B does not dispute A's claim that its own gate needs a model. | Medium | L3 |
| X-009 | Which design is the larger build and which risks more? | A: "no extractor exists ... synth-05 rates the option XL with High risk"; commitment per extractor. | B: Recipe Ledger about 760 lines against about 1,100 to 1,250 for the Sweep Sheet, and E2's tie rule adopts Recipe Ledger if both pass within 0.05; both tagged planning values, UNVERIFIED. | Medium | L2 |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | A | Per-class offline gate M1 (no model tokens) with pre-registered recall floor, random baseline and byte-identity | High |
| U-002 | A | "Empty sheet equals the isolated brief by hash" as the no-cards invariant (MR2 REQ-23, UNVERIFIED as text) | Medium |
| U-003 | A | Snapshot-boundary rule: every path a script attaches must be in the input snapshot or `verify-citations` flags it `missing-file` (92.5 percent of recorded flags are `not-in-snapshot`) | High |
| U-004 | A | Reports found-at-any-severity and found-at-blocking separately because the CB-2 routing differs | Medium |
| U-005 | A | Extractor determinism requirement (directory order, locale, `git grep` ordering) pinned by unit tests; otherwise the offline gate is meaningless | Medium |
| U-006 | A | Lister-only classes (C1, C3, C7) ship as card text with no extractor and say so | Medium |
| U-007 | A | The card loader must not import class names into `findings_v2` vocabularies (class constants leaking into the core) | Medium |
| U-008 | A | Replica assignment is a module rule, not a quorum, and does not feed C-03's `min(2, requested)` floor | Medium |
| U-009 | B | `recipes` slot key bound by `slot_id` with a rationale for the name against `lens`, `cards`, `classes` and `ledger`; grep shows no `recipe` word in `cli/review` | Medium |
| U-010 | B | Second output file `review-rowcheck/1` keeps `review-precheck/1` and `reread_set` byte-identical | High |
| U-011 | B | Containment rules for demotion: off by default, never CRITICAL, own flag only, `check_skipped` for tool-line quotes, finding stays visible with the reason | High |
| U-012 | B | Card lint: a test fails when a card is bound to a slot whose agent lacks a tool the card's only form needs | High |
| U-013 | B | Code-level tests T-B1..T-B7, including a telemetry test that no record serialises a quote or `problem` string | High |
| U-014 | B | Recorded sidecar use is ad hoc: 13 `coverage.json` files, 11 with a row id assigned more than once, 2 with `observed` empty for every reviewer (UNVERIFIED, r10 Unit 10) | Medium |
| U-015 | B | rf-qa mark mapping `[x]`/`[?]`/`[ ]` to OK/UNSURE/missing and the `rf-qa` formula (`rf-qa.md:484-510`, verified by B) | Medium |
| U-016 | B | M-B3: demotion safety measured offline on M-B2 outputs; the switch stays off unless no true blocker is demoted | High |
| U-017 | B | Four-arm design Z0, K, RL, SS on one ground truth, with a rule that the cheaper form wins if RL does not beat K by 0.04 | High |

## Shared Assumptions

Agreement points scanned: both variants (1) accept the C-01, C-02 and C-03 outcomes; (2) say nothing of either redesign exists in code; (3) make classes module data, never core constants; (4) keep reflect contract 1.8.0 byte-identical and the 36-test verdict matrix untouched; (5) reuse the `{assigned, observed}` sidecar as the assignment container; (6) reuse `verify_cmd._norm` and `_check` for quote checks; (7) keep telemetry to ids and counts; (8) apply the process to the first review only; (9) say every gate G0 and D1-D7 is a design choice and D2 (0.12 x 14 = 1.68 items) is stricter than the design's own central estimates (+1.33 and +1.05); (10) name arm K (plain-words checklist) as the competitor; (11) leave the Medium routing and grading rule as shipped.

| A-NNN | Assumption | Source Agreement | Classification | Impact | Status |
|-------|------------|------------------|----------------|--------|--------|
| A-001 | A measurement harness, ground truth and the pre-registration rule exist and will be built (slot X-14 is undecided; no arm, extractor, hold-out or planted set exists at HEAD). A's M1..M5 and B's M-B1..M-B3 both depend on it. | (9), (10) | UNSTATED in A (A never names X-14); STATED in B (names X-14's rule) | High: either design is unfalsifiable without it | Promoted |
| A-002 | A reviewer-side duty (sheet items or recipe rows) is complied with often enough not to crowd out the free review. | (5), (8) | STATED (A: displacement and rubber-stamping; B: `ledger_missing`, M-B1) | Medium | Not promoted |
| A-003 | Every module's coordinator can host one more deterministic step (A's pre-pass and sheet writer, B's rowcheck and overlay) without a new engine hook; the spec review loop on v1 has no such hook documented in either variant. | (5), (8) | UNSTATED | Medium: both designs add a step, neither shows where the spec loop would run it | Promoted |
| A-004 | Quote and path evidence that items or rows cite lies inside the input snapshot, so the existing check can verify it. | (6) | STATED by both but CONTRADICTED by recorded data: 472 of 510 flagged citations are `not-in-snapshot`; B's demotion rests on `quote_other` being checkable "against a snapshot file" and does not say what a `not-in-snapshot` result does to a row | High for B's demotion; Medium for A's attached evidence | Promoted |
| A-005 | The eight classes C1-C8 are a stable, separable taxonomy that generalises beyond one owner's plan pipeline. | (3) | STATED (A 3.4 and B E13 both cite r10 Unit 7: "evidence about one repository") | Medium | Not promoted |

## Summary
- Total structural differences: 4
- Total content differences: 13
- Total contradictions: 9
- Total unique contributions: 17
- Total shared assumptions surfaced: 5 (UNSTATED: 2, STATED: 2, STATED but CONTRADICTED by recorded data: 1); 3 promoted to debate points (A-001, A-003, A-004)
- total_diff_points for convergence = 4 + 13 + 9 + 3 = 29
- Highest-severity items: C-001, C-002, X-001, X-002, X-003, A-001, A-004
- Taxonomy coverage: L1 = S-001, S-002, S-003, C-013 (4); L2 = S-004, C-001, C-003, C-004, C-005, C-008, C-009, C-010, C-011, C-012, X-001, X-004, X-006, X-009, A-003 (15); L3 = C-002, C-006, C-007, X-002, X-003, X-005, X-007, X-008, A-001, A-004 (10). All three levels are covered by points that the advocates must address.

## Verification notes (orchestrator spot checks at the working tree, 2026-11-14)
- `_SLOT_KEYS = {"slot_id", "tier", "count", "strategy", "seed"}` at `src/superclaude/cli/review/panel.py:46`; unknown-key error at `panel.py:214-216`. Both variants cite these correctly.
- `ledger.py:3-4` reads "Only this module changes a finding's status; a reviewer's own prior lines are recorded as notes and never change one." (A's citation is correct; B cites `ledger.py:1` for the "ledger" naming, also correct.)
- `findings_v2.py:291-298`: empty block complete only with an observation for every assigned row (B E7 correct).
- Neither variant cites a file that does not exist at the points checked. The `ledger.py:187` (union) and `ledger.py:468` (non-blocking rows listed) cites by B and the `verify_cmd.py` and `reflect-reviewer.md` cites by both were not re-read by the orchestrator; advocates and the fault-finder re-read them.
