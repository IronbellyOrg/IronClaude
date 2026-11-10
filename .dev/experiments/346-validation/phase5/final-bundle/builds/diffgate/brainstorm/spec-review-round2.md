# Spec Review, Round 2

review: 2 of 3

Target: `.dev/brainstorms/346-diffgate/SPEC.md`
Prior review: `.dev/brainstorms/346-diffgate/spec-review.md` (verdict FAIL, B1 to B7 blocking, m1 to m11 minor)

Reviewer: rf-qa, adversarial, read-only on every file except this report. Date: 2026-11-08.
Counts: prior blocking 7 resolved, 0 open, 0 regressed; new findings 4 blocking, 6 minor.

## Prior blocking findings

| id | status | SPEC.md line | evidence |
|----|--------|--------------|----------|
| B1 | resolved | 149 (and 112) | C3 now reads "on a mismatch `check` exits 5, steps out of order, and writes no `reject-r<N>.txt`"; exit code 5 at line 112 lists "spec edited during a review". Matches merged-output.md line 188. |
| B2 | resolved | 77 | Bullet 1 now says a non-zero exit stops the run "except where `## Diffgate` names the next step (`check` exit 1: one repair and one rerun; `begin` exit 5: run the step `status` names)". Consistent with `## Diffgate` bullets 2 and 5 (lines 92, 95). |
| B3 | resolved | 103-125 | Subcommand table with all JSON fields and `status` semantics, exit codes, report block, line forms with `::`, `withdrawn quote= reason=`, `fr`, `side=old`, `via_quote`, `cites`. Matches merged lines 91-96 and 177-179. New defects in the added text: N1, N4. |
| B4 | resolved | 215-218, 259 | R3 "about 3.0 to 3.5", flg-r1-like "about 4 to 5", flg-r2-like "about 1 to 2", growth "about 20% to 27%", F1 "about 0.5 to 0.55", P(both at 3 or fewer) "0.2 to 0.25". All equal merged lines 478-482. |
| B5 | resolved | 259-265 | F1 to F6 labelled, merged F4 restored verbatim (line 262), former item 6 moved to "Reported but not part of the pre-registered rule" (line 265). New defect in F6 wording: N3. |
| B6 | resolved | 229 | Keeps 9 to 17 on the critical+major proxy and records it as a deliberate change. Stated reason checked true: flg-r1 review 1 graded 11 blocking (`exp346-ab-flg-r1/.dev/orca-command-refactor/review/spec-panel.md` line 154 "11 blocking (2 CRITICAL, 9 MAJOR)", line 188; `disposition.md` line 39 "21 applied (11 blocking, 10 minor)", the one rejected row being MINOR); "13 to 17" traces to `variant-1-opus-architect.md` line 393 ("expect 13 to 17 blockers as in Arm B"), an estimate. |
| B7 | resolved | 229 | Adds accepted `check` for reviews 1 to 3, accepted `fixcheck` for both cycles, unchanged hashes, no `origin/master` read, completion rate per arm. New defect in the added rule: N3. |

## New findings

| id | grade | SPEC line | issue | evidence | fix |
|----|-------|-----------|-------|----------|-----|
| N1 | blocking | 117-122 vs 125, 149 | The new report-block example, which line 101 says SKILL.md carries verbatim and `## Diffgate` bullet 4 tells reviewers to follow "exactly", numbers its findings R2.1, R2.3, R2.4. That breaks the rule stated two lines later ("`j` from 1 with no gap", line 125) and C2 ("contiguous", line 149): the shipped example is a report `check` must reject, and a fixture built from it fails. Merged line 171-174 has R2.1 to R2.4. | SPEC lines 120-122, 125, 149; merged-output.md lines 171-174. | Renumber the example to R2.1, R2.2, R2.3, or restore merged's `FINDING R2.2 sev=minor at=223 hunk=H2.6 anchor="--output <dir> by default" :: index-repo has no such flag` line. |
| N2 | blocking | 156 vs 73 | The m8 fix changed edit 3 to keep the `**Read**` bullet and delete only its path clause, but the drift-guard test still compares `## Tool Coordination` "after the one deleted line". No line is deleted now, so a test written to line 156 fails against a correct command file, or pushes the implementer to delete the whole Read bullet, which is the m8 defect back. | SPEC line 73 ("keep the bullet ... delete only its clause"); SPEC line 156 ("`## Tool Coordination` after the one deleted line"); `src/superclaude/commands/spec-panel.md` line 220 is the one Read bullet carrying the clause. | Line 156: "`## Tool Coordination` equal after removing the `; src/superclaude/examples/release-spec-template.md ...` clause from its `**Read**` bullet". |
| N3 | blocking | 229, 264 vs 206, 215, 223, 33 | A clean PASS before review 3 is a success route ("or a clean PASS sooner", lines 215 and 223; "An early PASS carries its document forward", line 206; the loop closes at a derived PASS, line 33). The new Validity rule makes such a replicate not valid (it requires an accepted `check` for reviews 1 to 3 and an accepted `fixcheck` for both fix cycles, which an early PASS never produces), and F6 now reads "a replicate delivers no review 3", so an early PASS also falsifies the design. Merged F6 said "A replicate stalls (no review 3 delivered)"; the qualifier "stalls" was dropped. The pre-registered rules therefore void or fail the best outcome. | SPEC lines 33, 206, 215, 223, 229, 264; merged-output.md lines 469, 496. | Line 229: "an accepted `check` for every review the loop ran (reviews 1 to 3, or up to the review that reached a clean PASS) and an accepted `fixcheck` for every fix cycle that ran". Line 264: "F6, stall: a replicate stalls before review 3 without a derived PASS". |
| N4 | blocking | 149 (C6) vs 121, 29, 81 | C6 says the anchor occurrence must overlap a changed token of "the cited hunk", "checked for every anchor and `via_quote` in the line". A `via` finding's anchor sits by definition on an unchanged line (step 6 line 29, bullet 5 line 81), so C6 as written rejects every `via` finding, including the new example R2.3 (line 121, anchor on unchanged line 312). Merged C6 scopes the anchor overlap to `hunk=` findings and only asks `via_quote` to overlap the `via` hunk. This is unchanged rule text, graded here because the new example line depends on it. | SPEC lines 29, 81, 121, 149; merged-output.md lines 190-192. | C6: "from review 2, a `hunk=` finding's anchor occurrence overlaps a changed token of that hunk (or a removed token with `side=old`); a `via=` finding's `via_quote` overlaps a changed token of the `via` hunk and its anchor sits on the unchanged line it names". |
| n1 | minor | 229 | "the range across all six earlier runs" omits AB-REPORT's "Original run" column, whose review-1 proxy is 18, outside 9 to 17. The six listed values are right. | AB-REPORT.md lines 10, 13. | Write "all six controlled A/B runs (the uncontrolled original run had 18)". |
| n2 | minor | 229 | "`disposition.md` line 39" has no folder; the review's own total is in its report. | `exp346-ab-flg-r1/.dev/orca-command-refactor/review/disposition.md` line 39; `spec-panel.md` line 154 there. | Give the full path, or cite `spec-panel.md` line 154 ("11 blocking (2 CRITICAL, 9 MAJOR)"). |
| n3 | minor | 229 | The no-`origin/master` rule voids a treatment replicate for a peek, while the comparator baseline keeps ctl-r2 and flg-r1, which peeked. The text says peeks "are recorded for every arm" but not that comparators are kept as published. | ARMB-REPORT.md line 36 (post-hoc exclusion not used). | Add "comparator replicates are kept as published; their peeks are reported beside the result". |
| n4 | minor | 101 | "SKILL.md carries these two definitions verbatim" is followed by four blocks (subcommand table, exit codes, report block, line forms). | SPEC lines 101-125. | Write "carries the following verbatim". |
| n5 | minor | 112 | Exit 5 drops merged's "no open round" case. | merged-output.md line 107. | Add "no open round". |
| n6 | minor | 154 | No test covers `check` exit 5 for a spec edited during a review (C3 after the B1 fix); the listed "spec edited after `fixcheck` exits 5" is a `begin` case. | SPEC lines 149, 154. | Add "spec edited between `begin` and `check`: `check` exits 5 and writes no `reject-r<N>.txt`". |

## Required-text check (task item 3)

- Review Loop bullet 4 (line 80) contains `at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings` and `HALT and escalate to the user with the open blocking findings` (both True when run against `CANONICAL_CAP_TEXT` and `AT_CAP_CLAUSES[1]` imported from the test file).
- No `src/superclaude` string in Review Loop bullets 1 to 7 (lines 77-83) or `## Diffgate` bullets 1 to 6 (lines 91-96).
- `CAP_REGRESSION`, `BANNED_SEVERITY_PHRASES`, `_sweep_hits` and `ZERO_TOLERANCE` from `tests/skills/test_review_severity_rule.py` give no hit on lines 77-83, 91-96, the SKILL.md text that ships verbatim (lines 103-125) or the reviser brief line (192).

## Self-Audit

- Read SPEC.md in full (281 lines, two reads) and the prior review. Read merged-output.md lines 85-234, 320-339 and 460-534 (subcommands, exit codes, checker rules, Review Loop text, validity, forecasts, F1 to F6, costs).
- B6 reason: grepped the flg-r1 review folder; `spec-panel.md` lines 154 and 188 and `disposition.md` line 39 confirm 11 blocking in review 1; grepped the brainstorm folder for "13 to 17" (variant-1 line 393, debate transcript, invariant probe INV-039, refactor plan line 268).
- Numbers in the Validity paragraph: AB-REPORT.md lines 10-17 and ARMB-REPORT.md lines 11-20 and 34-37 (review-1 proxies 11, 12, 9, 9, 16, 17; peeks ctl-r2 every step, flg-r1 7 Bash calls; original run 18).
- Citations in changed text: `spec-panel.md` lines 216-222 (Read bullet and clause), `test_workflow_archive.py` lines 20-29 (loader ends at 28), `~/.claude/WORKER-CONTRACT.md` line 60 (WC-7 text matches line 187), DECISIONS.md line 45 (D9 heading).
- Severity-rule test: imported `tests/skills/test_review_severity_rule.py` with `uv run` and ran its matchers line by line over the proposed command bullets, the `## Diffgate` bullets, the verbatim SKILL.md text and the brief line: no hit. Em dashes in SPEC.md: 0.
- Not re-checked by rule: minors m2, m3 and m6 from review 1 (still as before; for example C8, C9 and M3 summaries and the cost figures are unchanged). Not checked: whether the "13 to 17" range was ever a measured value in any proposal other than variant 1.
- Monotonicity: open blocking findings went from 7 to 4.

Confidence: Verified 10/10 check groups (7 prior findings, changed hunks, required text, evidence numbers) | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%.
Tool engagement: Read: 9 | Grep: 0 | Glob: 0 | Bash: 4. No web research.

verdict: FAIL
