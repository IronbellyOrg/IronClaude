# Refactoring Plan: Merge into Base (Variant A)

## Overview
- Base: Variant A (Proposal A, Sweep-Sheet-shaped; `variant-1-original.md`), selected by the tiebreaker (final scores A 0.8685, B 0.8591, margin 0.94%; Level 1 debate performance A 5 vs B 4; Level 2 correctness A 2 vs B 0). See `base-selection.md`.
- Incorporating strengths from: Variant B (Proposal B, Recipe-Ledger-shaped; `variant-2-original.md`).
- Output file: `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/reviews/adversarial/process-redesign-modules/merged-output.md`.
- Nature of the merge: the merged file is the RESOLUTION of slot X-13 as the debate itself produced it: Proposal A's section structure and its surviving positions, rewritten so that every changed statement equals what the two advocates agreed in Round 2 (`round2-advocate-A.md` section 5, `round2-advocate-B.md` sections 4 and 6) or what the debate scored (`debate-transcript.md` scoring matrix). The merge-executor makes no strategic decision and adds no content the debate did not conclude; where the debate left a point open, the merged file states it as open.
- Planned changes: 15
- Risk level: Medium overall (restructuring of sections 1, 2, 5; the rest additive)

Source key for the "Source" fields below: R1A, R1B = `round1-advocate-A.md`, `round1-advocate-B.md`; R2A, R2B = `round2-advocate-A.md`, `round2-advocate-B.md`; DT = `debate-transcript.md`; IP = `invariant-probe.md`; DA = `diff-analysis.md`; VA = `variant-1-original.md`; VB = `variant-2-original.md`.

## Planned Changes

### Change 1: Position becomes the converged hybrid (from the debate; A section 1 rewritten)
- **Source**: R2A section 0 and section 5; R2B section 0 and section 6; DT "Points on which the two advocates agree after Round 2".
- **Target**: VA section 1 (replace). Keep VA's opening claim that classes are module data and that extractors are decided class by class behind an offline gate; replace "script-first and advisory-only" with: record-only reviewer row block as the built-now carrier, script extractors reserved, advisory-only checks, no demotion or promotion.
- **Rationale**: 13 of 29 points scored Hybrid (DT scoring matrix: C-001, C-002, C-003, C-005, C-007, C-008, C-009, C-011, X-001, X-004, X-005, X-007, A-004); both advocates' Round 2 position text is the same hybrid.
- **Integration point**: replaces the single paragraph of VA section 1.
- **Risk**: Medium; restructures the headline claim. Rollback: restore VA section 1.

### Change 2: Core inventory replaced (VA section 2 "Adds only (a)(b)(c)")
- **Source**: R2A section 5 items 1 to 7; R2B section 6 components 1 to 7; VB section 3 items 4, 5 and 7.
- **Target**: VA section 2, "Adds only" bullet (replace) and "Does not add" bullet (revise: VA's line "a per-row verdict block" is removed from the list because the merge adds the record-only row block; what stays excluded is a per-row consequence, demotion, promotion, a lens-to-model binding, class constants, and any change to `findings_v1`/`findings_v2` grammar, `review-ledger/1`, `derive_verdict` or the reflect contract).
- **Rationale**: C-001 Hybrid (73%): A's card loader and one writer entry point plus B's record-only row block and separate rowcheck file. C-004 B (90%): second file keeps `review-precheck/1` byte-identical, A conceded and withdrew its part (c) (R2A section 0 item 1). Built now: (1) card format and loader with validator (fields as MR2 3.0.3 as relayed, plus `requires_tools` and tool-keyed `search_forms`; no `extractor` field until an extractor exists; no class constants); (2) row block `rows-v1`; (3) one entry point writing `panel/coverage.json` and `panel/rowcheck.json`; (4) check rules; (5) counts-only telemetry with a leak test; (6) uniform per-module binding; (7) tool-wall lint. Not added: demotion, promotion, overlay, profile value, slot key, precheck flags, CB-2 in the core, changes to findings v1 or v2, `review-ledger/1`, `derive_verdict`, reflect contract 1.8.0 and its 36-test matrix, reviewer-side shell, class constants.
- **Integration point**: VA section 2 "Shared core" bullets 2 and 3 ("Adds only", "Does not add"); the "Item answers travel through what exists" bullet (VA line 20: items answered through `coverage_rows` or an open key such as `probe`) is replaced by the row block of Change 3, because both advocates agreed A's "existing mechanism" for a no-finding item is hollow (R1A concession 1); the "Telemetry" bullet is replaced by item (5) of this change.
- **Risk**: Medium (modifies existing). Rollback: restore VA section 2.

### Change 3: Row block specification (new subsection under section 2)
- **Source**: R2B section 6 component 2 and section 4.1 (iii); R2A section 5 item 3; R2A section 3 point 11; DT scoring matrix C-002, C-006, X-007.
- **Target**: new subsection "2.1 The row block" in the merged file.
- **Content to state (and only this)**: record-only fenced block with its own info string `rows-v1` (name subject to the collision rule; `recipes` is excluded); row fields `row`, `class`, `verdict` (OK, PROBLEM, UNSURE), optional `quote_plan`, `quote_other`, `problem`, `ran`; limits stated as Variant B's Round 2 proposal (R2B component 2: `quote_plan` 12 to 200 flattened characters, `quote_other` at most 200 and checked only when 12 or more, `problem` at most 300, row cap set by the module); A did not accept or reject the values, only asked that rows have their own limit and a rule for over-length (R2A section 8 item 6), and IP INV-010 and INV-009 record the boundaries as open; placement before the findings block in the v1 loop (`document_review_loop_prompts.md:33, :58`) and after it in v2 (`reviewer-spec.md:39`, `SKILL.md:344`); a truncated row block never invalidates a complete findings block; `observed` is computed from parsed rows and never declared by an orchestrator; the hard consequence of the rows exists only for an EMPTY findings block (`findings_v2.py:291-298`), one finding plus zero rows is valid, so the row block does not prove examination (R2A section 8 item 1, R2B section 9 item 1). State the open items D-6 (does UNSURE count as observed) and the IP findings INV-006, INV-007, INV-010, INV-014 as unaddressed gaps in the row grammar, quote limits and card-to-row-id rule.
- **Risk**: Medium.

### Change 4: Single writer entry point and id map (new subsection under section 2)
- **Source**: R2B section 6 component 3 and section 4.2 row "2"; R2A section 5 item 2 and section 3 point 6; IP INV-001 to INV-005.
- **Target**: new subsection "2.2 The entry point".
- **Content**: one CLI entry point, deterministic and idempotent, writing (a) `panel/coverage.json` with `assigned` from the module's bound cards and `observed` from parsed row ids, one entry per card including `{}`, with the id map between resolution id, card stem and `--report` id; (b) `panel/rowcheck.json`, schema `review-rowcheck/1`, advisory only, changes no flag, status, verdict or finding. Record BOTH Round 2 lists and state that they differ on one point and that the debate did not settle it: A's component 2 "fills `assigned` only" (R2A section 5 item 2, tagged "Agreement"); B's AMEND of that component (R2B section 4.2 row "2") also computes `observed` from the parsed rows, citing recorded orchestrator-written sidecars that are partial and sometimes not a subset (R2B section 2 last bullets: comboC-r3, comboA-r3, comboA-r2). A did not accept B's amendment in a later round (no Round 3 at depth=standard). Both advocates agree that `observed` must not be orchestrator-declared (R2A section 8 item 7; R2B section 6 component 3); the merged file states that as the agreed point and the writer split as open (IP INV-001). State INV-001 (HIGH, UNADDRESSED: `SKILL.md:345` still tells the orchestrator to write the sidecar), INV-002, INV-004 and INV-005 as open.
- **Risk**: Medium.

### Change 5: Check rules and snapshot boundary (extend section 3.3)
- **Source**: R2B section 6 component 4; R2A section 5 item 4; DT scoring matrix A-004 (Hybrid, 73%); R2A section 3 point 8 and R2B section 2 item d (472 of 510 flags are `not-in-snapshot`, re-run by both).
- **Target**: VA section 3.3 (two bullets): bullet 1 (advisory-only as "the code's own rule") is revised so that it no longer calls `ledger.py:3-4` the code's own rule for "no component edits a reviewer finding" (both advocates agree `ledger.py:3-4` is a status rule; the surviving grounds are `ledger.py:210-213`, `SKILL.md:343`, C-02 and the C-03 fail-closed choice, R2A section 2 weakness 5); bullet 2 (the quote-check and snapshot bullet) is kept and extended with the new text, and its "not re-run by me" tag on the 472 of 510 counts is changed to "re-run by both advocates" (R2A section 3 point 8, R2B section 2 item d).
- **Content**: `quote_plan` is tested against the candidate file with the shared normaliser (one function imported, equality pinned by test); `quote_other` only against a path in the input snapshot; a printed tool line, a path outside the snapshot and any `quote_other` on the v1 loop (no snapshot) are `check_skipped`; script-attached evidence is restricted to snapshot paths by a test; the check is advisory and carries no consequence.
- **Risk**: Low (additive; refines A's snapshot-boundary rule).

### Change 6: Binding (uniform per module; slot-keyed binding reserved)
- **Source**: R2A section 5 items 6 and 8; R2B section 4.1 (ii); DT scoring matrix X-005 (Hybrid, 63%) and C-013 (Neither, 65%).
- **Target**: VA section 3.2 last sentences and section 2; new short paragraph.
- **Content**: every reviewer of a module gets the same cards (the loop's same-brief sentence at `document_review_loop_prompts.md:70` holds and `_SLOT_KEYS` at `panel.py:46` stays unchanged); a slot-keyed binding is reserved in the document only, under a name other than `recipes` (`cli/swarm/recipes/` exists), with a golden test of the `review panel resolve` output, an explicit decision on the `review-panel/1` hash, and a slot-to-card-stem map.
- **Risk**: Low.

### Change 7: Tool wall and card format (extend section 3.2)
- **Source**: R2A section 5 item 7; R2B section 6 components 1 and 7; VB section 3 item 1 and E10; DT scoring matrix X-004 (Hybrid, 73%), C-003 (Hybrid, 70%).
- **Target**: VA section 3.2.
- **Content**: no card may require a tool outside the bound agent's allowlist (`reflect-reviewer.md:5, 8`); a test fails otherwise; a class whose only form needs a shell is not bound to a read-only agent; script extractors for C4 and C8 reserved; for a read-only slot C4 would keep only a Grep form whose equivalence to the shell dialect is UNVERIFIED (the Grep tool is ripgrep).
- **Risk**: Low.

### Change 8: Evidence section additions (section 3, new 3.7 and an evidence table)
- **Source**: VB section 4 rows E7, E8, E9, E12 (table form, S-002 and S-003 won by B at 60%); R2A section 3 points 1 to 11; R2B section 2 items a to g; IP "Facts the advocates marked [UNVERIFIED] that this probe verified".
- **Target**: VA section 3 (append subsection 3.7 "Facts established in the debate").
- **Content (each with its tag and the file:line the debate re-read)**: the v1 loop has no snapshot, sidecar, cluster or precheck step anywhere (verified by absence); three reviewer-id spaces (`panel.py:668`, `cluster_cmd.py:146`, `merge_cmd.py:86-90`) plus a fourth legacy `-card` stem (IP INV-002); `_brief_ids` lists only blocking open or regressed rows (`ledger.py:99-104`) and a re-found row's flag is recomputed (`ledger.py:210-218`); quote exactness measured at 31 of 313 quoted citations (9.9 percent per quote; 18.8 percent for a two-quote row, which assumes the two failures are independent and the advocate notes independence is low; failures sit in 8 of 29 runs and range from 2 to 57 percent in those 8) with the transfer from findings-v2 citation quotes to row quotes stated as an assumption; `ledger.py:3-4` is a status rule (both advocates agree); `ledger.py:467-474` lists ledger rows only; the INV-N mirror pins exist (`tests/skills/test_review_brief_placement.py:73-103, 129-138`; `tests/review/test_review_rules_text.py:34-43, 65-73`) and exclude `commands/spec-panel.md` from prompt edits (IP INV-015).
- **Risk**: Low (additive).

### Change 9: Invariants section extended (VA section 4)
- **Source**: VB section 5 (Preserved and Endangered lists, kept where the debate did not contradict them); IP summary and table.
- **Target**: VA section 4 (extend), plus a table of the 20 probe findings by ID, category, status and severity (copy of the IP table columns ID, Category, Status, Severity and a short assumption).
- **Content**: Preserved: reflect contract 1.8.0 and the 36-test matrix (no cards in any packaged reflect template; `panel_lint.py:185, 318`), finding grammar and `review-ledger/1`, reviewers blind and read-only (INV-G), telemetry ids and counts (INV-H, with the closed-record gap INV-017), installed-path rule. Endangered or open: the 16 UNADDRESSED findings, with HIGH INV-001 and INV-019 and the 13 MEDIUM items named, the LOW INV-008.
- **Risk**: Low.

### Change 10: Measurement section replaced with ordered gates (VA section 5)
- **Source**: R2A section 5 items 13 to 17; R2B section 6 items 13 to 17; DT scoring matrix C-007 (Hybrid, 75%), X-008 (A conditional, 55%).
- **Target**: VA section 5 (replace M1..M5 with G-0..G-4, keep M1 as G-1).
- **Content**: G-0 code tests (no model, no harness): `_SLOT_KEYS` and resolve output unchanged by golden test; a row fence leaves `findings.parse_block` and `findings_v2.parse_block` results identical including `ok` and `state` (before the heading in v1, after the block in v2, truncated); card-to-tool lint; telemetry text-leak test; no-cards byte identity of the brief files, `coverage.json` and the resolution; `review-precheck` golden bytes unchanged; the writer rejects duplicate ids and range tokens, writes one entry per card, sets `observed` only from parsed rows; the id-map test; normaliser equality; extractor determinism where one exists. B's T-B1 "golden rendered briefs" has nothing to hash because no brief renderer exists in `cli/review` (B conceded, R1B concession 1); it becomes a golden test of the resolution output plus a pin of the loop prompt file. G-1 per class offline recall (A's M1; needs ground truth and X-14's rule). G-2 compliance spike. G-3 arms Z0, K, RL, SS on one ground truth (RL must beat K by the pre-registered margin or K wins; SS only for classes that passed G-1). G-4 demotion safety (B's M-B3) before any `apply` exists, plus the three prerequisites both advocates named: per-row persistence across rounds (`ledger.py:99-104, 210-218`), a merge hook (`merge_cmd.py:71`) and a severity rewrite for v2 reflect lines (`findings_v2.py:161-162`) (R2A section 5 item 17; R2B section 6 reserved item 11). Gate order as agreed. Variant A's M2 (shadow-mode comparison reporting found-at-any-severity and found-at-blocking separately), M3 (against arm K), M4 (non-regression and wrong-blocker limits: wrong blockers no more than the control plus 1.0) and M5 (the unmodified `tests/review/` and `tests/cli/reflect/` suites pass; `panel_lint` passes a run with rows) were not dropped by either Round 2 list and were not placed by them; the merged file keeps M2 and M4 under G-3, M3 as the K arm of G-3 and M5 under G-0, and states that this placement is the merge's, not a debate conclusion.
- **Risk**: Medium (replaces existing section).

### Change 11: Consistency with C-01, C-02, C-03 (VA section 6 kept, updated)
- **Source**: VA section 6; VB section 2 (content only; the table format of VB section 2 is not adopted, because S-004 was left unresolved and VA's labelled-prose format is kept); IP INV-018 (ADDRESSED).
- **Target**: VA section 6 (text), plus the lines elsewhere that conflict with Changes 2, 3, 4 and 6: the precheck-flag references sit in VA section 2 "Adds only (c)", VA section 3.3 and the VA section 4 "Endangered" bullet on `precheck.json` byte-identity (all revised per Changes 2, 5 and 9, not in section 6); VA section 6 lines 88-89 (item link through `coverage_rows`, or an open key under v1, validated by the module's own check) and line 98 (replica assignment, an item to 2 of 3 reviewers) are revised: the item link becomes the row block of Change 3, and replica assignment is replaced by uniform per-module binding (Change 6); the statement that replica assignment is a module rule, not a quorum, and does not feed C-03's `min(2, requested)` floor is kept only if it still applies to uniform binding, and otherwise removed.
- **Content**: keep VA's statements that still hold; add B's finding that the row block is a separate fence that leaves `findings`, `priors` and `ok` unchanged in both parsers (`findings.py:73, 143-150`; `findings_v2.py:233`, IP INV-018 ADDRESSED), and that recipes and rows apply to the first review only (`apply_to: ["first"]`). Add, tagged as the merge's inference and not a debate conclusion, that with no demotion or promotion built the C-03 union and fail-closed interaction that B flagged (VB section 2 table) is not engaged. State the residual path (truncation of the findings block behind a longer row block in v1; IP INV-011).
- **Risk**: Low.

### Change 12: Modules (VA section 2 modules list and section 7)
- **Source**: R2A section 5 items 18 to 21; R2B section 6 items 18 to 21; DT scoring matrix C-005 (Hybrid, 60%), C-011 (Hybrid, 55%), C-012 (B, 60%).
- **Target**: VA section 2 "Modules" and VA section 7.
- **Content**: spec review loop (v1): uniform cards, row block before the findings block, advisory rowcheck on `quote_plan` against the candidate, no consequence, wired in prose only after G-2 and G-3 per B; per A it is one new prose edit; state D-5 as unresolved; tasklist and workflow via reflect UC-1 (v2): items are the Coverage slice rows, class-row ids namespaced apart from requirement rows, row block after the findings block, verbatim copy into the panel card via a prose edit of reflect step 5 (D-7 unresolved; IP INV-002 and INV-016); reflect default and UC-2: no cards, byte-identical; PR review and rf-qa: reserved; reverse-dependency and whole-tree searches run in a script for untrusted diffs; the OK, UNSURE, missing to `[x]`, `[?]`, `[ ]` mapping is a design inference, not a tested equivalence.
- **Risk**: Medium.

### Change 13: Strongest objection and answer rewritten (VA section 8)
- **Source**: VA section 8; VB section 8; R2A section 2; R2B section 3.
- **Target**: VA section 8.
- **Content**: keep A's objection (build size, selection recall, lister-only classes, false positives, unobservable compliance) with A's answers that survived; record B's objection (the recipe ledger asks the model to police itself; demotion could turn a blocker into PASS) as answered by the agreement that demotion and promotion are not built, citing the three grounds the debate added (`ledger.py:99-104, 210-218`, no merge hook at `merge_cmd.py:71`, quote exactness 9.9 percent per quote). Record the concessions both advocates made (A: observed mechanism for a no-finding item is hollow, no v1 host, flags withdrawn; B: no brief renderer, overlay needs a merge hook, `recipes` name collision, sidecar key is the card stem, `ledger.py:468` cite wrong).
- **Risk**: Low.

### Change 14: Conditions and non-claims (new section, from B section 9 and the invariant probe)
- **Source**: VB section 9 (S-003, B 60%); IP INV-019, INV-020; DT metadata.
- **Target**: new final-but-one section "What this resolution does not claim and the conditions under which it holds".
- **Content**: no claim that RL beats the Sweep Sheet or K; no effect size from planning values (+1.33, +1.05 items); D2 (0.12 x 14 = 1.68 items) exceeds both designs' own central estimates and is a pre-registration choice for the owner (VA 3.6; GQ-135 covers the related +35 percent elapsed limit); A-001 (the harness, ground truth and pre-registration of slot X-14) is a precondition for every effect claim; the built-now set alone is dormant (no module declares cards before G-2 and G-3; no brief renderer; prose edits are module wiring), which is IP INV-019 (HIGH, UNADDRESSED); the rows give a hard consequence only for the empty report and `observed` proves a reviewer typed an id, not that it ran the step (`ran` unverified until C-08); the value of the advisory output depends on a named reader of `rows_missing` and the PROBLEM-without-finding list (IP INV-020).
- **Risk**: Low.

### Change 15: Resolution table and open points (new appendix)
- **Source**: DT scoring matrix and convergence assessment; IP; R2A section 6 and R2B section 7.
- **Target**: new appendix "Per-point resolution and open points".
- **Content**: the 29-point table (point, level, winner, confidence) copied from the DT scoring matrix; the unresolved point S-004 (format of the consistency and invariant presentation; the merged file keeps VA's labelled-prose format and says S-004 is open); residual disagreements D-1 (does the row duty crowd out the free review; settled by G-2 and the Z0 versus RL arms), D-2 (do script-made items beat card-derived rows on C4 and C8; settled by G-1 and the SS versus RL arms), D-5, D-6 and D-7 (each with the evidence that would settle it as the advocates stated; D-3 and D-4 are closed by agreement in R2B section 7); convergence 96.55% (28 of 29), status BLOCKED_BY_INVARIANTS because of INV-001 and INV-019; the 16 UNADDRESSED invariants by ID and severity.
- **Risk**: Low.

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach (or base approach dropped) | Rationale for Not Making the Change |
|------------|-----------------------------------------------|-------------------------------------|
| X-002, X-003 | B's demotion and promotion in the core behind a switch (`rowcheck: apply`, overlay, `src=rows` promoted line) | Scored Variant A at 95% and 80%; B conceded both. Grounds: `ledger.py:99-104, 210-218`, no merge hook (`merge_cmd.py:71`), 9.9 percent per-quote failure on recorded data. Reserved behind G-4 in the document only; no schema key; prerequisites named by both advocates: per-row persistence across rounds, a merge hook, a v2 severity rewrite. |
| X-005 | B's `recipes` slot key in `_SLOT_KEYS` | Hybrid (63%): uniform per-module binding now; name `recipes` collides with `cli/swarm/recipes/`; `SKILL.md:340` requires the unmodified resolve output. |
| C-010, X-006 | B's CB-2 route through the row block (PROBLEM row listed under follow-up candidates by the report builder) | Scored Variant A (73%, B conceded): `ledger.py:467-474` lists ledger rows only. Modules may ask reviewers to copy a PROBLEM sentence into follow-up candidates by brief text. |
| C-004 | A's additive item-evidence flags in `precheck.json` (VA part (c)) | Scored Variant B (90%, A conceded and withdrew): `_check` reaches only findings-v2 citations (`verify_cmd.py:133-143`); byte-identity pins. |
| X-001, C-009 | A's script pre-pass and extractors built now | Hybrid: reserved per class behind the offline gate (G-1); no extractor code exists. |
| C-003 | `extractor` field on the card now | An unread field; added when the first extractor exists. |
| C-002 | A's `observed` supplied by the orchestrator / "existing mechanism" for a no-finding item | A conceded it is hollow (R1A concession 1); `observed` is computed from parsed rows. |
| C-007 | B's T-B1 as "golden rendered briefs" | No brief renderer exists (B conceded); replaced by a golden test of the resolution output plus a pin of the loop prompt file. |
| C-008 | A's "degrades to loader plus card text" fallback as having value | Equals arm K with a loader (both advocates); the merged leftover is the carrier plus rowcheck, which is measurable. |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1 | Medium | Headline claim misstates the converged hybrid | Restore VA section 1 |
| 2 | Medium | Core inventory disagrees with Round 2 component lists | Restore VA section 2 |
| 3, 4 | Medium | Row grammar or entry-point text goes beyond what the debate concluded | Remove the new subsection |
| 5, 6, 7 | Low | Additive | Remove inserted paragraphs |
| 8, 9 | Low | A cited fact not matching its source | Remove the cited line and re-check against R2A and R2B |
| 10 | Medium | Gate list diverges from agreed order | Restore VA section 5 |
| 11, 13, 14, 15 | Low | Additive or restating | Remove inserted section |
| 12 | Medium | Module behaviour misreports an open point (D-5, D-7) | Restore VA sections 2 and 7 |

## Review Status
- [x] Auto-approved (default)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-14
- Analytical review: `plan-review.md` (agent `x13-plan-reviewer`) found 11 defects in the first draft (change 4 settled INV-001, D-1 and D-2 dropped, G-4 prerequisites omitted, wrong targets in change 11, a "Does not add" contradiction in change 2, B's row limits stated as settled, GQ-135 misattributed, lost caveats in change 8, M2/M4/M5 silently dropped, S-004 format adopted, an inference not tagged); all 11 are corrected in this version.
