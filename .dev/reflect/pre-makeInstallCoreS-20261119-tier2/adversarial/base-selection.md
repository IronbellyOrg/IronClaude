# Base Selection (Step 3)

Judge: neutral, not a debater. Inputs: variant-1-original.md (V1, reviewer 1, analyzer), variant-2-original.md (V2, reviewer 2, qa), diff-analysis.md, debate-transcript.md, the four advocate files, invariant-probe.md, source.md, t1-card.md.

Requirements (from t1-card.md, quote-pinned to source.md line 1): INF-001 use the shared `same_content`; INF-002 no stale filecmp cache answers; INF-003 a test in tests/cli for install_core; INF-004 same-size same-mtime rewrite reported as different; INF-005 existing `tests/cli -k install` stay green.

Scope note: the invariant-probe findings (INV-001 to INV-014) are not in either variant's text. They earn neither variant any credit below. They go into the merge as a separate section (see refactor-plan.md).

## 1. Quantitative scoring (50%)

### RC: requirement coverage

| Req | V1 (quote or section) | V2 (quote or section) |
|---|---|---|
| INF-001 | Coverage verdict: "The shared function is used: Task 1 makes `install_core` use it" | "the shared comparison" (Coverage verdict, first bullet) |
| INF-002 | "The stale cache is gone: `install_core` itself has no `filecmp` left" | "removal of stale-cache answers" |
| INF-003 | "A test in `tests/cli`: Task 2 adds it" | "an installer test" |
| INF-004 | "Same-size, same-time rewrite is reported as different" | "a same-size same-mtime rewrite detected as different" |
| INF-005 | "Existing `tests/cli -k install` tests stay green" | "preservation of existing install tests" |

- V1: 5 of 5, RC = 1.00.
- V2: 5 of 5, RC = 1.00.

### IC: internal consistency

Rule: a contradiction is two statements inside the same variant that cannot both be true. A claim that later evidence shows to be wrong is a correctness matter (qualitative, Correctness 1), not an internal contradiction, so it is not counted twice here.

- V1: 37 claims counted (F1 to F5 and the two new notes: 20; Coverage verdict: 9; Risks: 4; Recommendation: 4). Contradictions: 0. The only tension is "Accept the plan and the implementation as they are" next to an optional follow-up; the text says "If you want a follow-up", so both can be true. IC = 1 - 0/37 = 1.00.
- V2: 20 claims counted (Findings 1; Coverage verdict 8; Risks 6; Recommendation 3; closing note 2). Contradictions: 0. IC = 1 - 0/20 = 1.00.

### SR: specificity

Concrete = carries a file:line, a quote, a count, a command, or a named symbol. Vague = a conclusion with no anchor.

- V1: 34 concrete, 3 vague ("This is a form problem only", "Nothing else", "If you want a follow-up"). SR = 34/37 = 0.919.
- V2: 17 concrete, 3 vague ("None." under Findings, "None found within the requested scope", "Its acceptance checks cover the complete spec"). SR = 17/20 = 0.850.

### DC: internal reference resolution

Labels F1 to F5 in V1 point at the first run's list, which lives outside the variant, so they are excluded. Each V1 bullet restates the substance next to its label.

- V1: 3 internal references ("described above" in Risks resolves to the last Findings bullet; "extend it" resolves to the F5 extension; "this check is a one-off manual step" resolves to the preceding sentence). 3 of 3 resolve, DC = 1.00.
- V2: 2 internal references (header "see reviewer_model_self_report" resolves to the last line; "These are observable acceptance checks" resolves to the preceding sentence). 2 of 2 resolve, DC = 1.00.

### SC: structure

Both use four H2 sections (Findings, Coverage verdict, Risks the first run missed, Recommendation). V1 4/4 = 1.00; V2 4/4 = 1.00.

### Quant

quant = 0.30 RC + 0.25 IC + 0.15 SR + 0.15 DC + 0.15 SC

| | RC | IC | SR | DC | SC | quant |
|---|---|---|---|---|---|---|
| V1 | 1.00 | 1.00 | 0.919 | 1.00 | 1.00 | 0.30 + 0.25 + 0.138 + 0.15 + 0.15 = **0.988** |
| V2 | 1.00 | 1.00 | 0.850 | 1.00 | 1.00 | 0.30 + 0.25 + 0.128 + 0.15 + 0.15 = **0.978** |

The quantitative metrics barely separate the two. They measure form, not whether the content is right.

## 2. Qualitative scoring (50%)

Format: criterion, then V1 and V2 as Claim (evidence) and verdict. Pass 1 is the order V1 then V2. Pass 2 is the reverse order, evaluated independently. Only disagreements between the passes are listed in the reconciliation after the table. A cell shows the pass-1 verdict first; where pass 2 differed and was resolved, the final verdict follows after an arrow.

### Completeness

| # | Criterion | V1 | V2 |
|---|---|---|---|
| 1 | Covers all explicit requirements | MET. Coverage verdict lists five bullets, one per requirement | MET. "All five inferred requirements are covered" with the five listed |
| 2 | Edge cases and failure scenarios | MET. "unreadable files ... already reported as stale"; "fails with an `IndexError`" | MET. "Unreadable or missing files"; "Missing destination and forced installation"; "False-positive stale reports" |
| 3 | Dependencies and prerequisites | MET. "Import cycle: `install_keep` imports only `filecmp`, `shutil`, `datetime` and `pathlib`"; "The other installers ... already used the shared function" | NOT MET. No prerequisite or dependency is named |
| 4 | Success or completion criteria | MET. "To verify, run `uv run pytest tests/cli/test_how_we_work_install.py -q`" | MET. "nine passing file-level tests ... 352 passing existing install tests with one skip" |
| 5 | Out of scope stated | MET. "outside the spec ... The spec covers only `install_core`" | MET, weak. "The spec does not require a new installer-level error test"; "within the requested scope" |

### Correctness

| # | Criterion | V1 | V2 |
|---|---|---|---|
| 1 | No factual errors or hallucinated claims | MET. Debate checked every citation; the sibling item is tagged "[INFERRED]" and is not claimed as a defect | NOT MET. "None. No blocking, minor, or wording findings were established" and "None found within the requested scope" were found wrong as written (debate C-001, C-002, X-002; the V2 advocate conceded). The `IndexError` weakness shows in the very log V2 cites |
| 2 | Technical approaches feasible | MET. The one-line `assert "NOT updated" in message, message` is sound | MET (pass 2: NOT MET, resolved MET). It proposes nothing new and endorses the plan's negative control, which the debate found sound |
| 3 | Terminology consistent | MET. `same_content`, `_same_content`, "stale cache" used the same way throughout | MET. "shared comparison", "negative control" used the same way |
| 4 | No internal contradictions | MET. 0 counted above | MET. 0 counted above |
| 5 | Claims supported by evidence | MET. Each claim carries a file:line, or an "[INFERRED]" tag, or a disclosure that the pre-change file was not read | MET. Each claim carries a file:line or a log line range |

### Structure

| # | Criterion | V1 | V2 |
|---|---|---|---|
| 1 | Logical section order | MET. Findings, Coverage verdict, Risks, Recommendation | MET. Same order |
| 2 | Consistent hierarchy | MET. Four H2 sections, severity-tagged bullets | MET. Four H2 sections, bullets |
| 3 | Separation of concerns | MET. Plan findings, coverage, missed risks, action are in separate sections; the out-of-scope note is labelled "advisory, outside the spec" | MET. Same separation |
| 4 | Navigation aids or cross-references | MET. "Cites:" lines with file:line on each finding | MET. "Source:" lines with file:line on each bullet |
| 5 | Follows reviewer card conventions | MET. persona, model, Findings, Coverage verdict, risks, Recommendation, `reviewer_model_self_report` | MET. Same elements |

### Clarity

| # | Criterion | V1 | V2 |
|---|---|---|---|
| 1 | Unambiguous language | MET. "Accept the plan and the implementation as they are. If you want a follow-up, add one line" | MET. "Accept the plan without changes" |
| 2 | Concrete, not abstract | MET. Line numbers and names throughout | MET. Line numbers and log ranges throughout |
| 3 | Each section has one clear purpose | MET | MET |
| 4 | Terms defined on first use | MET (pass 2: NOT MET, resolved MET). Each "I confirm Fn" label is followed by the restated substance, so the label is not needed to follow it | MET. "negative control with cache clearing disabled" is glossed inline |
| 5 | Actionable next steps | MET. Exact assert line, exact pytest command, exact backlog target | NOT MET. "Accept ... without changes" is a decision, with no step, file or verifier |

### Risk Coverage

| # | Criterion | V1 | V2 |
|---|---|---|---|
| 1 | At least 3 risks with likelihood and impact | NOT MET. Impact appears ("costs speed only", "harder to read") but no likelihood is stated for any risk | NOT MET. No risk is listed; the three checked cases carry no likelihood or impact |
| 2 | Mitigation for each | MET (pass 2: NOT MET, resolved MET). Both missed risks have one: the assert line; the backlog item. F4 is declared speed-only and accepted | NOT MET. No risk, so no mitigation |
| 3 | Failure modes and recovery | MET. "without the fix the new test fails with an `IndexError`" plus the readable-assertion fix | MET (pass 1: NOT MET, resolved MET). "The shared comparison catches `OSError` and returns false" is a failure mode with its handling |
| 4 | External dependencies and their failures | MET. The process-wide `filecmp` cache is named, and a stale answer is the failure; reliance on the quoted diff for the pre-change file is disclosed | NOT MET. Only reliance on the supplied log is disclosed, which is a limit of the review, not a dependency of the change |
| 5 | A validation mechanism | MET. The pytest command and the Grep for leftover `_same_content` | MET. The negative control with cache clearing disabled, and the log lines |

### Invariant and Edge Case Coverage (variant text only; probe findings not credited)

| # | Criterion | V1 | V2 |
|---|---|---|---|
| 1 | Collection boundaries | MET. "That works because PRINCIPLES.md is not empty"; "Grep ... finds `filecmp` only in `install_keep.py` and `orca_worktree.py`" | NOT MET (pass 1: MET, resolved NOT MET). "Missing destination" is a branch question (criterion 3), and "unshipped files under both force settings" is a partition, not a boundary |
| 2 | State interactions across components | MET. "`same_content` empties the `filecmp` result cache, which is shared by the whole process"; "the new test's first install call ... fills the cache" | NOT MET. No shared-state discussion |
| 3 | Guard condition gaps | MET. "uses `force=False`, so it fills the cache ... without overwriting the kept file"; unreadable file turned into False | MET. "Missing destination and forced installation ... use the copying branch, not the changed comparison" |
| 4 | Count divergence | NOT MET. No counts compared | NOT MET. Counts are quoted ("nine", "352", "one skip") but not compared for divergence |
| 5 | Interaction effects | MET. "does not change behaviour on unreadable files ... The only behaviour change is the cache clear" | NOT MET. No interaction effect is discussed |

### Pass reconciliation

Pass 2 (reverse order, V2 then V1) disagreed with pass 1 on these cells. Each was re-evaluated once.

| Cell | Pass 1 | Pass 2 | Re-evaluation | Final |
|---|---|---|---|---|
| V2 Correctness 2 | MET | NOT MET (nothing proposed to judge) | V2 endorses the plan's negative control, which the debate and INV-005 found sound; the criterion asks whether the approach in play is feasible | MET |
| V2 Completeness 5 | MET | NOT MET (one sentence is not a scope statement) | "The spec does not require a new installer-level error test" and "within the requested scope" do mark a boundary | MET |
| V2 Risk 3 | NOT MET | MET (OSError is a failure mode plus handling) | The quoted sentence names a failure and its handling; the negative-control failure adds nothing more. Standard applied the same way to V1 | MET |
| V2 Invariant 1 | MET | NOT MET | The "missing destination" quote is a branch/guard point, already credited under criterion 3; no empty, one or many boundary is stated. Applied the same standard to V1, whose "PRINCIPLES.md is not empty" is an empty-input boundary | NOT MET |
| V1 Clarity 4 | MET | NOT MET (labels F1 to F5 undefined inside the card) | Every label is followed by its restated substance, so the reader needs no outside list | MET |
| V1 Risk 2 | MET | NOT MET (F4 has no mitigation) | F4 is declared a speed-only note and accepted; the risks V1 raises as missed both have a mitigation | MET |

Counts: pass 1 gave V1 28 of 30 and V2 20 of 30. Pass 2 gave V1 26 of 30 and V2 18 of 30. After the six re-evaluations above the finals are V1 28 and V2 20:

| Dimension | V1 | V2 |
|---|---|---|
| Completeness | 5 | 4 |
| Correctness | 5 | 4 |
| Structure | 5 | 5 |
| Clarity | 5 | 4 |
| Risk Coverage | 4 | 2 |
| Invariant and Edge Case | 4 | 1 |
| **Total met** | **28** | **20** |

qual: V1 = 28/30 = **0.933**; V2 = 20/30 = **0.667**.

Edge-case floor: the last dimension scores 4 for V1 and 1 for V2. Neither is below 1, so both are eligible as base. The floor does not decide the outcome, but V2's 1 of 5 is a weakness the merge must repair.

## 3. Combined score

combined = 0.5 quant + 0.5 qual

| | quant | qual | combined |
|---|---|---|---|
| V1 | 0.988 | 0.933 | **0.961** |
| V2 | 0.978 | 0.667 | **0.822** |

The gap is 0.139, far outside the 5 percent band. **The tiebreaker is not applied.** For the record, the debate scoring matrix gives V1 five wins (S-001, C-001, C-002, C-003, X-002), V2 two (C-004, X-001), and two qualified points (A-001 credited to V2's disclosure, A-003 credited to V1). It points the same way.

## 4. Selected base

**Base: Variant 1.**

Rationale:
- It is the only variant with a finding the debate confirmed as real: the new test fails with an `IndexError` instead of a readable assertion. The plan itself prescribes that expression (plan:36), the log shows the error (t2-checks.log:8-10), and the V2 advocate conceded the point.
- It gives an actionable recommendation (file, line, command), which V2 lacks.
- It covers shared-state and interaction effects (process-wide cache, first-call fill, unreadable-file behaviour) that V2 does not touch; this is where V2 loses most (Invariant dimension 1 of 5).
- V2's "None" findings and "None" risks were judged wrong as written by its own advocate.

Strengths to preserve from V1:
- Severity-labelled findings (S-001).
- The `IndexError` finding and its one-line fix.
- The old-versus-new helper comparison (old helper differs only by the cache clear; unreadable-file behaviour unchanged).
- The import-cycle and other-callers checks.
- The "[INFERRED]" honesty tag on the sibling-file item.
- The non-empty `PRINCIPLES.md` condition (A-003).

Strengths of V2 to incorporate:
- The requirement-to-acceptance-check mapping with log line citations (C-004, U-005).
- The existing-test safeguards as counter-evidence against overstating risk (U-004): `test_how_we_work_install.py:28-34,79-99,102-115` and `test_install_keep.py:38-45`.
- The explicit statement that test and lint outcomes are supplied evidence, not independently repeated (A-001 QUALIFY, credited to V2).
- The narrow X-001 judgment: F1 (bare line numbers) and F2 (unspecified byte change) are not decision-relevant against the plan as written.

Not incorporated: V2's "None" findings and "None" risks (wrong as written); V1's recommendation to file a backlog issue for `orca_worktree.py` as a firm action (the V1 advocate conceded it is a lead only).
