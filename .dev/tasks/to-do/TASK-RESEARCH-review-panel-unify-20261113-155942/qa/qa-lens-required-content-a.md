## Required-Content QA Report

**Report reviewed:** `.dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/RESEARCH-REPORT-review-panel-unification.md` (4241 lines; partition rule >3000 lines applies)
**Lens:** required contents (a)-(e) plus the Section 8 shape check (f), partition instance a (Assigned sections: 1-5)
**Date:** 2026-11-14
**Fix authorization:** false (report only; the document was not modified)
**Checked:** Header and Table of Contents (lines 1-88), Section 1 (90-103), Section 2 citation key and Sections 2.5-2.6 (105-122, 384-478), Section 3 (480-570), Section 4 rows D1-D16, BL-01 to BL-23, MS-01 to MS-23, ENS-1 to ENS-6 (572-650), plus Grep sweeps of the whole file for the 35-of-39 wording, the E2 commit id, `feat/review-panel` and roadmap language. Sections 6-10 belong to instance b and were read only where this lens needed a cross-reference.

### Required-part table

| Required part | Present? | Where (section) | Complete? | Missing elements |
|---|---|---|---|---|
| (a) Component overlap matrix across E1/E2/E3 | Yes | 2.6 (lines 435-460) | Yes | None. 18 rows, matching the 18 required rows one-to-one: finding contract, severity scale, parser limits, clustering, merge and ledger, verdict and blocking, calibration, panel templates, tier and class config, identity check, dispatch, brief and input contract, run manifest, telemetry, audits, shadow harness, evaluation harness, tests. Columns E1, E2, E3, Same purpose?, Same data contract?, Same code?, Divergent choices, Evidence. No empty cell; rows 16 (shadow harness) and 18 (tests) use `none` or `n/a` with a reason. |
| (b) Value inventory, every row has a destination or DROP with reason | Outside my partition (8.1 is instance b) | 8.1 (line 2899) | Not evaluated here | Not evaluated by instance a. Section 4 row MS-23 shows the "Track: none (drop: ...)" form is used upstream. |
| (c) Conflict log incl. defects D1-D16, debate results | Outside my partition (Section 6 and 6.D are instance b) | 6.0-6.D, C-01 to C-20 | Not evaluated here | Upstream input checked: Section 4 holds all of D1-D16 (lines 582-597, each with current state, target state, severity, track, evidence). D1 states the 200-character anchor limit and the silent loss (49 blocking findings, 24 anchor, 14 anchor2, 10 claim, 1 refs). |
| (d) Target architecture, shared core plus thin modules | Outside my partition (7.1 is instance b); a sketch is in Section 3 | 3 (lines 493-519), 7.1 | Not evaluated here | See finding 1 (Section 3 sketch omits calibration and citation checks). |
| (e) Future-use-case check, PR review and rf-qa replacement | Outside my partition (7.2, 7.3 are instance b); upstream inputs in Sections 2.5, 3 and 4 | 2.5, 3 (C-E, SC-14), 4 (BL-01 to BL-23) | Not evaluated here | Upstream input checked: BL-01 to BL-23 name the blockers per consumer (closed lens tuple, spec-only categories, three-level severity, location types, single-document candidate, document-relative clustering, id regex, model-bound templates, `--kind`, strata, halts, read-only versus fixing, verdict contracts, closed PR reviewer set, and more). |
| (f) Section 8 value-capture and migration plan, no roadmap, branch options | Outside my partition (Section 8 is instance b) | 8, 8.4 | Not evaluated here | In Sections 1-5: no roadmap, dates, sprints or `/sc:workflow` plan found (Grep for roadmap, Sprint, Week, milestone, Phase 1: only scope statements at lines 7, 64, 101 and 1075 saying "no roadmap"). Section 1 (line 101) states the git constraint that `feat/review-panel` and `feat/review-panel/<name>` cannot both exist. |

### Executor-note checks that fall inside Sections 1-5

| Check | Result | Evidence |
|---|---|---|
| 35-of-39 wording presented as measured fact that the flag drove Tier 2 | Not present, PASS | Line 163 states counts only: 38 of 39 selected Tier 2, flag set in 35 of 39 (34 of the 38 Tier 2 runs), decisive in 0 for certain and at most 1, "counts only, cause not established". Section 4 row DOC-59 (line 713) and contradiction row 16 (line 746) say the "driven by the flag" conclusion is not carried. Grep for `driven by` and `35 of 39` over the whole file found no sentence outside Sections 1-5 that asserts the causal claim as current fact either (every other hit is a correction or a hedge; line 637 "probably driven by combo A's GLM/Qwen orchestrator" is about a different claim and is hedged). |
| E2 cited at commit 4a22d74213f93837d00c2c314075dd967b9a98e3 only | PASS | Full hash at lines 6, 92, 101, 122, 557, 643; short `4a22d742` in `git show` forms at lines 122, 178, 237. The only other `git log` or `git diff` hashes (`d2d8a2d16`, lines 280 and 724) are E1/master commits, not E2. No other E2 commit id appears. |
| Report-only, no roadmap in Sections 1-5 | PASS | See table row (f). |
| Debates C-03, C-05, C-13, C-14 `partial` stated as open | Outside my partition | Section 6/9.5, instance b. Section 1 and Section 4 do not claim these as settled. |
| `[CONTRADICTION]` vocabulary in Section 7 | Outside my partition | Instance b. |

### Findings

| # | Severity | Section | Finding | Proposed Fix |
|---|---|---|---|---|
| 1 | MINOR | 3 (lines 493-519) | The Section 3 "Desired behavior" paragraph and ASCII core diagram list resolver, brief renderer, dispatch, finding contract, clusterer, merge and verdict, run record and telemetry. They do not name calibration or citation checks, which required part (d) lists as shared-core elements. Section 7.1 does mention calibration (lines 2701, 2743, 2753), so the required content exists elsewhere; the Section 3 sketch is only a shorter version. Not blocking. I did not verify that 7.1 lists citation checks; instance b owns that. | Add "calibration (optional module) and citation checks" to the Section 3 diagram, or state that 7.1 is the full target architecture. |

### Summary

- Required parts in my partition: (a) present and complete. (b) to (f) fall in Sections 6-8 and belong to instance b; their upstream inputs in Sections 1-5 (D1-D16, BL-01 to BL-23, consumer table, no-roadmap, branch constraint) are present.
- Findings: 0 CRITICAL, 0 IMPORTANT, 1 MINOR (note only).
- Confidence: Verified: 6/6 in-partition checks (matrix (a), D1-D16 upstream coverage, BL upstream coverage, 35-of-39 wording, E2 commit, no roadmap in 1-5) | Unverifiable in this partition: 5 (full checks of (b) to (f) live in Sections 6-8) | Unchecked: 0 | Confidence: 100.0% of in-partition items. This is not a verdict on (b) to (f); instance b must cover them.
- Tool engagement: Read: 4 | Grep: 10 | Glob: 0 | Bash: 0 (Read+Grep+Glob = 14 calls against 11 checks).
- Cross-partition note: [PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-section verification requires merging both partition reports.]

Verdict: PASS (0 critical + 0 important; minor findings listed as notes)

## QA Complete
