# Merge Log

- Base: variant-1-original.md (V1 analyzer/sonnet), per base-selection.md.
- Plan: refactor-plan.md (7 planned changes, 6 rejected alternatives; auto-approved 2026-11-17T06:56Z).
- Additional inputs named by the orchestrator: debate-transcript.md (final rulings table), round-2-v3.md section 4 (10-item candidate list and its notes line), invariant-probe.md (34 findings).
- Output: /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/reflect/pre-phase3OfTheOrcaT-20261117062037/adversarial/adversarial/merged-review-card.md
- Files written: this log and the merged card only. The plan, the code, the specs and the variants were not edited.

## Planned changes (refactor-plan.md)

| # | Source | Status | Before (base) | After (merged card) |
|---|---|---|---|---|
| 1 | base F3 | applied | F3, MEDIUM Regression, view.py:78-81; fix "separate link-on help line; or state the link-off help is unchanged" | C-002, BLOCKING Regression, citation view.py:914; fix = round-2-v3 §4 item 2 (`QUESTIONS_LINK_KEYS_LINE`, selected only when link is on) |
| 2 | base F6 | applied | F6, MEDIUM Gap, citation export.py:75-86 (the record writer); fix "use dispatch ids absent from the rows, or assert only the `questions` group" | C-003, BLOCKING Gap, citation export.py:195 with export.py:131-145 and :148-170 in reality; fix = V2 F1 fix as worded in round-2-v3 §4 item 3 (exclusion limited to the `questions` group, linked worker's `rows[].dispatchId` kept, byte-identity kept) |
| 3 | V2 F3 | applied | no link-off screen check in the base | C-002 fix carries the acceptance criterion: link-off selects `QUESTIONS_KEYS_LINE` (literal pinned) and `screen_lines` at 160/116/80 is byte-identical to a reference captured before Task 4; V3's lighter option recorded as "noted, not chosen" |
| 4 | V2 F4 | applied | not in base | C-009, MEDIUM Gap: desk missing-value and STALE/`as of` assertions; `_field` in place of `text_of(row.raw.worktree_id)` (round-2-v3 §4 item 7) |
| 5 | V3 F6 | applied | not in base | C-011, MEDIUM Drift: amend AD-18 (ARCHITECTURE-SPINE.md:178) and the CAP-12 row (:285) in Task 7 (round-2-v3 §4 item 8) |
| 6 | V3 F8 | applied | not in base | C-012, MEDIUM Drift: extend `make_question_rows` (conftest.py:239-271) instead of a new builder; never-kept test row carries distinctive `body` and `to_handle` (round-2-v3 §4 item 9) |
| 7 | V3 F9 | applied | not in base | C-013, MEDIUM Gap: rendering-rules.md lines 21, 24 and the line-43 R3 clause, plus the evicted-selection desk note; V3's line 40 dropped (round-2-v3 §4 item 10) |

Applied 7, failed 0, skipped 0.

## Rejected alternatives (refactor-plan.md "Changes NOT Being Made")

All six kept out of the card as instructed: C-007 stays NOTE with the "append a sentence, keep the pinned assertion" fix (V3's assertion edit not used); C-008 stays NOTE; C-010 stays NOTE (split optional); C-014 stays NOTE; C-015 stays NOTE and is folded into C-001's test; V2's "a realistic linked fixture cannot pass" wording not used (C-003's wrong_outcome says the check cannot pass on the found-worker fixture).

## Orchestrator-directed content beyond the 7 planned changes

The launching agent's instruction set the card's content wider than refactor-plan.md. Each item below is logged so it is not mistaken for improvisation.

| Item | Source | Status | Note |
|---|---|---|---|
| Renumber base F1-F8 to debate ids | diff-analysis.md C-points | applied | F1 -> C-001, F2 -> C-004, F3 -> C-002, F4 -> C-005, F5 -> C-006, F6 -> C-003, F7 -> C-008 (note), F8 -> C-007 (note) |
| `supported_by` field on every finding | variants, debate-transcript.md final rulings | applied | not a base field; added per the requested format |
| C-001 fix text | round-2-v3 §4 item 1 | applied | base F1 fix replaced by the consensus plan edit (both Collector sites, `--once` test with argv check) |
| C-004 fix and per-focus key table | round-2-v3 §4 item 4; A-002 ruling | applied | table: list `n`/`p` select, `Esc` clears; filter `n`/`p` typed, `Esc` leaves filter; inspector `n`/`p` ignored, `Esc` to list keeping the selection. Filter rows checked against view.py:982-988 |
| C-005, C-006 fix text | round-2-v3 §4 items 5, 6 | applied | base F4, F5 kept, fixes replaced by the consensus edits |
| NOTES block | round-2-v3 §4 notes line; base F7, F8; V3 F4, F10, F12; S-003 | applied | C-007, C-008, C-010, C-014, C-015, marker clash, record-suffix assertion, register line 33 correction |
| "Invariant probe additions" section | invariant-probe.md | applied | 2 HIGH (INV-008, INV-021, first, marked convergence BLOCKED_BY_INVARIANTS) and 11 MEDIUM (INV-001, 004, 009, 010, 011, 012, 013, 015, 016, 017, 018). Fixes for INV-008, 015, 016, 017, 018 and 021 are the probe's own; the other seven are labelled "derived" (stated from the probe's gap text, no new requirement) |
| `amended_by` cross-references | invariant-probe.md | applied | added to C-001, C-002, C-005, C-006, C-009, C-012, C-013 so a consensus fix and the probe fix that narrows it are not read as contradicting each other |
| header `confidence` and `convergence` lines | S-002 ruling; probe Summary | applied | confidence not carried; convergence states BLOCKED_BY_INVARIANTS for INV-008 and INV-021 |

## Citation re-verification

Every file:line in the card was re-Read in this merge before it was written (list in the card's `checked` section). Corrections against the inputs:
- C-003: base citation export.py:75-86 is inside `record_text` (export.py:71-86); replaced by export.py:195 (snapshot rows) and :131-145 (`_row_dict`), per change 2.
- C-001: "the call at line 355" in the plan is the `questions=` keyword line of the interactive call at commands.py:350-356; the card cites 218-220 and 350-356. Grep confirms these are the only two `Collector(` sites in src/superclaude/cli/observe.
- C-002: QUESTIONS_KEYS_LINE measured at 107 characters (view.py:78-81); with "  n/p question" 121, matching V1.
- Register note: acceptance-tests.md ends at T56 (line 62), confirmed by Grep; unverified-register.md:33 exists today.
- Not re-verified: adapter-contract.md:41 and SPEC.md:66 (carried from V1's `checked` list, marked so in the card).

## Post-merge validation

- Heading structure: PASS. Top-level card keys in variant order (persona, model_class, verdict, confidence, findings, notes, uncovered_requirements, checked), then one `##` section "Invariant probe additions" with two `###` subsections ("Not converged", "MEDIUM"). No skipped heading levels. The `##` section is placed last so the card's key fields do not fall under it.
- Finding fields: PASS. All 10 BLOCKING/MEDIUM findings carry id, task, severity, class, citation, plan_says, reality, wrong_outcome, fix, supported_by (grep counts 10 each).
- Finding set: PASS. BLOCKING: C-001, C-002, C-003. MEDIUM: C-004, C-005, C-006, C-009, C-011, C-012, C-013. NOTE: C-007, C-008, C-010, C-014, C-015, marker clash, record-suffix assertion, register line 33 correction. Matches debate-transcript.md "Final rulings after Round 2" (no severity differs).
- Internal references: PASS. Every C- id referenced is defined in the card. Every INV id referenced (INV-001 to INV-024, 027, 028, 031, 032, 033) exists in invariant-probe.md; the 8 LOW ids referenced only from `amended_by`/notes are stated as not listed. 15 provenance comments, one per finding or section.
- Contradiction re-scan: PASS with two flagged tensions, both resolved by cross-reference, not by editing consensus text: (1) C-006's consensus replacement text drops "in `all_rows`" while INV-015 says restore it; C-006 carries `amended_by: INV-015`. (2) C-012's fix moves the builder to `make_question_rows`, whose default sender `term_synthetic` (conftest.py:259) undercuts the linked case; C-012 and C-001 carry `amended_by: INV-016`. No finding states a fact another finding denies; the register line 33 note explicitly retracts V3's earlier claim.
- Convergence status: the card does not claim the debate's CONVERGED status covers the probe: INV-008 and INV-021 are marked BLOCKED_BY_INVARIANTS.
