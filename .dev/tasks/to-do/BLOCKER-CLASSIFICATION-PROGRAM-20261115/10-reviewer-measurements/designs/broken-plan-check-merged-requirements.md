---
topic: "Which attributes of the Weak check edit made reviewers grade the tokenize.py stdlib clash Blocking, and the smallest addition to the stage 3c reviewer text that keeps only those"
adversarial_status: pass
convergence_score: 0.93
base_variant: "haiku:qa (V3), with V1 and V2 elements"
created: 2026-11-20
---
<!-- Provenance: produced by /sc:brainstorm via sc-adversarial-protocol; base V3 (haiku:qa) -->

# Merged requirements: isolate the tokenize attribute

## 1. Attribution (what the data shows)

The Weak check edit (`arms/s3c-weak.md` against `arms/s3c.md`) is step 5 (probe + edge-input walk) plus one "Weak check" bullet. Three attributes match the tokenize result. <!-- Source: V1, V2, V3 section 1 -->

| Attribute | Evidence | Kept |
|---|---|---|
| A1 anchor: the defect breaks a check the plan itself states, so an acceptance check changes and the Decision condition is met on a named check | All four Y-B tokenize rows (card-1 row 1, card-2 row 1, card-3 row 2, card-4 row 1) say T1/T5 `uv run pytest` can "fail or be unrunnable as written" | Yes |
| A2 routing: a plan defect is not a "no-spec correctness gap", so it goes in the Deviations table | X-B/card-3 raised the same clash but put it under Correctness gaps and wrote "The spec is silent on file names"; the stage 3c text (lines 30, 103, 115, 123) sends that to the non-gating table. Test 2 to test 3 in `B-rerun3/wording.md` (lines 92, 128) shows the same flip when the plan-defect sentence was added | Yes (load-bearing) |
| A3 example "a module name that shadows the standard library" | Y-B/card-4 row 1 quotes it. The sibling example "a command no task creates" did not move its class (1 of 4 in both arms, SCORES-ROUND3 line 24) | Provisional, and tuned on spec B |

Cannot be separated: noticing versus grading (X-B cards 1, 2, 4 never raised the clash, so routing explains at most 1 of 4 X cards; the probe step E1 or the example may have raised noticing); A1 and A2 were never tested apart; the sentence was only tested inside the Weak check bullet, not as a separate bullet after line 123. Four cards per arm, one model family, one scorer. <!-- Source: V1, V2, V3 -->

## 2. Left out, with the rows that show why

Each raised Blocking rows with no new caught target (E targets 4 of 4 in both arms; SCORES-ROUND3).

- Three-part naming as a Blocking licence, plus the anti-downgrade and "plausible" clauses: blank lines (Y-E card-1 row 4, card-2 row 6, card-3 row 5, card-4 row 6), key order (card-2 row 2, card-4 row 2), rows already written (card-1 row 3, card-2 row 5, card-4 row 4), count-only "8 words" (Y-B/card-2 row 4), interior apostrophes (Y-B/card-2 row 3).
- The spec-silent exact-value clause: undefined `<n>` (Y-E card-1 row 5, card-2 row 4, card-4 row 7) and literal `FILE` (Y-B card-1 row 3, card-4 row 3).
- E1 probe and edge-input walk: the blank-line Missing rows (Y-E card-2 row 6, card-3 row 5, card-4 row 6, which cites "Plan edge-input walk"). It did not move the B targets it was built for (tie at the cut and no-words file stay 0 of 4 Blocking).

Corrections to the inputs found during the debate: Y-B literal `FILE` rows are cards 1 and 4 only (card-2 graded it Medium, card-3 has no such row), matching the 2 of 4 in SCORES; X-E/card-3 row 5 already grades blank-line tests Blocking (Missing) inside a combined T4 row, while SCORES counts 0 of 4. <!-- Source: V1, V2, V3 -->

## 3. Requirements for the addition

1. Exactly one new line; every existing line of `arms/s3c.md` stays byte-identical (`diff -u` shows one `+` line and no `-` lines). Placement: directly after line 123 ("- This grading applies ...") and before blank line 124 (`## Boundaries` is line 125; "Minor findings" is line 120, above the insertion).
2. Trigger: a defect in the plan's own choices that can make a check the plan itself states fail or become unrunnable as written. "Can make", not "whatever is implemented" (Y-B/card-1 row 1: which module wins "depends on import mode").
3. Routing: an explicit exception to the no-spec routing rules above (plural, so lines 30, 103, 115 and 123 are covered); report in the Deviations table, not the Correctness gaps table, even if the spec is silent on the choice.
4. Grade: `Blocking (Decision):`, or `Blocking (Missing):` when a step the plan leaves out is the cause. The row names the plan choice, the check and the step that fails (checkable by a read-only reviewer).
5. Exclusions: a check that is absent, a check a wrong implementation could pass, or an expected value that depends on a choice the spec leaves open are graded by the existing rules; the line never demotes them.
6. No probe step, no three-part naming, no "do not downgrade" clause, no "plausible" definition, no spec-silent exact-value clause.
7. Disclosure: the example names the tokenize case, so the line is tuned on spec B. A B tokenize score is tuning evidence, not held out.
8. Acceptance (next measurement): paired arms (with the example, without), 4 cards per arm per spec, same briefs, blinded labels, second scorer, noticing/placement/grade scored apart. Pass: tokenize Blocking in at least 3 of 4 on B; at most 4.5 Blocking rows per E card and 2.75 per B card; per class, no new promotion of blank lines, `<n>`, rows written, key order, `FILE`, apostrophes, count-only; prefix, no-output, writer and codepoint catches held at X levels.
<!-- Source: V3 requirements 1 to 8, V1 requirements 4 to 12, V2 R1 to R9 -->

## 4. The addition (the tested variant)

```markdown
- **Broken plan check.** A defect in the plan's own choices that can make a check the plan itself states fail or become unrunnable as written (for example, a module name that shadows the standard library) is not a no-spec correctness gap, even if the spec is silent on that choice. As an exception to the no-spec routing rules above, report it in the Deviations table, not the Correctness gaps table, and grade it `Blocking (Decision):`, or `Blocking (Missing):` when a step the plan leaves out is the cause, naming the plan choice, the check and the step that fails. This does not cover a check that is absent, a check a wrong implementation could pass, or an expected value that depends on a choice the spec leaves open; grade those by the rules above.
```

Control (not measured in this round): the same line without the parenthetical, saved at `reflect-reviewer-control-no-example.md`.

## 5. Predicted effect and open risks

| Row class | Prediction | Why |
|---|---|---|
| B tokenize | up from 0 of 4; 2 to 4 of 4 | routing and anchor fix grade; recall may need E1 or the example |
| E blank lines, `<n>`, rows written, key order | unchanged | excluded (absent check, wrong build passes, spec-open value) |
| B `FILE`, apostrophes, count-only | unchanged | same |
| E and B targets | unchanged at X levels | line never demotes |

Open: INV-001 (sufficiency, recall), INV-004 (speculative unrunnable claims), A-004 unresolved in the debate, placement untested (A-002). Lines 30 and 103 still say "NEVER in the 4-class Deviations table"; the byte-identical rule prevents editing them, so the exception wording must carry it.
