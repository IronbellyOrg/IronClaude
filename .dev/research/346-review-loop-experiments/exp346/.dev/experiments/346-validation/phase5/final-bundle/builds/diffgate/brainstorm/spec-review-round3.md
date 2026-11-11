# Spec Review, Round 3

review: 3 of 3

Target: `.dev/brainstorms/346-diffgate/SPEC.md`
Prior review: `.dev/brainstorms/346-diffgate/spec-review-round2.md` (verdict FAIL, N1 to N4 blocking, n1 to n6 minor)

Reviewer: rf-qa, adversarial, read-only on every file except this report. Date: 2026-11-08.

Counts: prior blocking 4 resolved, 0 open, 0 regressed; new findings 0 blocking, 7 minor.

## Prior blocking findings

| id | status | SPEC.md line | evidence |
|----|--------|--------------|----------|
| N1 | resolved | 120-122 | The example now reads `FINDING R2.1 ... hunk=H2.2`, `FINDING R2.2 ... via=H2.3`, `FINDING R2.3 ... cites=R1.9`: ids 1, 2, 3 with no gap, matching line 125 ("`j` from 1 with no gap") and C2 ("contiguous", line 149). Grep for `R2\.[0-9]` finds no leftover `R2.4` anywhere in SPEC.md. The chain example on line 33 (`R1.5 -> R2.1 -> R3.2`) still fits: `R1.5 resolved by=H2.2` and `R2.1 hunk=H2.2`. Each form the block shows (hunk, via, cites) is still legal under C6 to C8. |
| N2 | resolved | 156 (and 73) | Line 156 now reads "`## Tool Coordination` equal after removing the clause that names `src/superclaude/examples/release-spec-template.md` from its `**Read**` bullet". This matches edit 3 on line 73 (keep the bullet, delete only the clause). Checked against `src/superclaude/commands/spec-panel.md`: heading on line 218, the clause on line 220 is the only `src/superclaude` string in the file, and removing it leaves exactly `- **Read**: Specification content analysis and parsing`. So the drift guard and the "no `src/superclaude` string anywhere in the command" assertion can both pass on a correct file. The leftover phrase "after the one deleted line" is gone (grep). |
| N3 | resolved | 229, 264 | Line 229: "an accepted `check` for every review the loop ran (reviews 1 to 3, or up to the review that reached a derived PASS) and an accepted `fixcheck` for every fix cycle that ran". Line 264: "**F6, stall:** a replicate stalls before review 3 without a derived PASS." An early PASS (line 33, "At a derived PASS (any review)") is now valid and does not fire F6. Grep finds no leftover "delivers no review 3". New notes on these lines: m1, m2, m7. |
| N4 | resolved | 149 (C6) | C6 now reads "from review 2, a `hunk=` finding's anchor occurrence overlaps a changed token of that hunk (or a removed token with `side=old`); a `via=` finding's `via_quote` overlaps a changed token of the `via` hunk and its anchor sits on the unchanged line `at=` names". This matches merged-output.md line 191, step 6 (line 29), Review Loop bullet 5 (line 81) and the example R2.2 (line 121, anchor on unchanged line 312). A `via` finding is no longer rejected by construction. New notes on this rule: m3 to m6. |

## New findings

All minor. None is a wrong claim on a changed line that changes what an implementer builds. m7 is the one the owner should read before the run.

| id | grade | SPEC line | issue | evidence | fix |
|----|-------|-----------|-------|----------|-----|
| m1 | minor | 264 | F6 "stalls before review 3" is narrower than merged F6 "stalls (no review 3 delivered)": a replicate that opens review 3 and then stops (for example a permission prompt, or a session that dies before `check` is accepted) is outside F6 as written, and inside F4 only when the cause is a script error. It cannot be a success either way (no review-3 count), so the outcome does not change. | merged-output.md line 496; SPEC lines 262, 264. | "a replicate ends without an accepted review-3 `check` and without a derived PASS". |
| m2 | minor | 229, 264 | Under the new Validity text every stall leaves a review or fix cycle that ran without an accepted `check` or `fixcheck`, so a stalled replicate is "not valid". The spec says what happens to a void replicate but not to a not-valid one, so whether F6 is assessed on a replicate the validity rule already excluded is unstated. Line 254 ("A stall costs a replicate (recorded as a failed attempt)") points to the intended reading. | SPEC lines 229, 254, 264. | Add to line 229: "A replicate that is not valid fills its attempt slot as a failed attempt and is still assessed against F4 and F6." |
| m3 | minor | 149 (C6) | "its anchor sits on the unchanged line `at=` names" is singular, while `at=` may be a range `a-b` (line 125). | SPEC lines 125, 149. | "sits on the unchanged lines `at=` names". |
| m4 | minor | 251 | The anchor-gaming row still says "C6 needs overlap with a changed token at the cited line". After the N4 fix that holds for `hunk=` findings only; for a `via=` finding the overlap is on `via_quote`, and the cited line is by rule unchanged. Unchanged line that depends on the changed C6. | SPEC lines 149, 251. | "C6 needs overlap with a changed token (by the anchor for `hunk=`, by `via_quote` for `via=`)". |
| m5 | minor | 125, 149 | The line form on line 125 puts `hunk=` in every `FINDING` line except those that anchor through `via=` or `cites=`, and C6 starts "from review 2". Nothing says a review-1 finding omits `hunk=` (review 1 has no surface), so a literal parser would reject every review-1 finding under C2. Merged C6 (merged-output.md line 191) closed this with "in review 1 there is no surface and `hunk`, `via` are not allowed". Line 125 is unchanged; I could not confirm whether the round-2 C6 carried the review-1 clause, because no earlier copy of SPEC.md exists (the folder is untracked and the file history has none). | SPEC lines 24, 125, 149; merged-output.md lines 177, 191. | Append to C6: "in review 1 there is no surface, a `FINDING` line carries no `hunk=` or `via=`, and C6 and C7 do not apply". |
| m6 | minor | 154 | The script tests have no positive `via` case (a `via=` finding with its anchor on an unchanged line and `via_quote` on a changed token is accepted) and no negative one (`via_quote` off the hunk). The round-2 N4 defect would have passed every listed case. Unchanged line. | SPEC line 154 ("third `via` deferred" is the only `via` case). | Add "a `via` finding with its anchor on an unchanged line is accepted; with `via_quote` outside the `via` hunk it is rejected". |
| m7 | minor | 229 vs 204, 215, 223 | The N3 fix rightly makes a replicate that closes at a derived PASS before review 3 valid. For a clean PASS the bar has a rule ("or a clean PASS sooner", lines 215, 223). For a scoped PASS before review 3 (reachable: lines 33 and 96, and C9 lets `withdrawn` force `scoped`) there is none: `R3-proxy-all` counts only review-3 items (line 204), so read literally it is 0, and blocking-grade findings deferred or withdrawn in review 2 drop out of the bar. That is the "winning by deferring" route the metric was built to close (merged-output.md line 466), and open question 10 asks for a function that "cannot be argued either way afterwards". The gap sits in unchanged lines 204, 215 and 223 (it was hidden before the fix, because such a replicate was not valid), so by the scope rule it is graded minor; the owner should still settle it before any run. | SPEC lines 33, 96, 204, 215, 223, 229, 280; merged-output.md line 466. | Add to line 204: "A replicate that closes at a scoped PASS before review 3 is scored on its closing review with the same function, deferred and withdrawn items included; only a clean PASS sooner meets the bar without a count." |

## Self-Audit

- Read SPEC.md in full (281 lines), spec-review-round2.md in full, merged-output.md lines 160-199 (report block, line forms, C1 to C12) and 460-499 (validity, predictions, F1 to F6).
- N1: Read lines 116-125; grep `R2\.[0-9]` over SPEC.md (hits only lines 120-122); checked the line-33 chain against the example.
- N2: grep `^## |src/superclaude|release-spec-template` over `src/superclaude/commands/spec-panel.md` (one `src/superclaude` hit, line 220); Read lines 216-227 for the exact bullet and clause; grep for "deleted line" in SPEC.md (no hit).
- N3: grep `clean PASS|derived PASS|delivers no review` over SPEC.md; compared lines 229 and 264 with merged lines 469 and 496, and with lines 33, 96, 204, 206, 215, 223, 254.
- N4: compared C6 on line 149 with merged line 191, step 6 (line 29), bullet 5 (line 81) and example line 121.
- Searched `~/.claude/file-history` for an earlier SPEC.md copy to test m5 as a possible regression: none found, so m5 stays a minor note on unchanged text.
- Em dashes in SPEC.md: 0 (grep count). This report uses none.
- Scope kept: n1 to n6 from round 2 and minors from round 1 not rechecked; no finding from an earlier review reopened. Not checked: whether the scoped early PASS in m7 is likely enough to matter at n=2.
- Monotonicity: open blocking findings went 7, 4, 0.

Confidence: Verified 6/6 check groups (N1, N2, N3, N4, changed-line sweep, em dashes) | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%.
Tool engagement: Read: 6 | Grep: 2 | Glob: 0 | Bash: 2. No web research.

verdict: PASS
