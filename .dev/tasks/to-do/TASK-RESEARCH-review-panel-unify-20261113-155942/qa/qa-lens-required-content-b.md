## Required-Content QA Report (Partition b of 2: Sections 6-10)

**Report reviewed:** `.dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/RESEARCH-REPORT-review-panel-unification.md` (4241 lines; this instance evaluates Sections 6 to 10, lines 1146-4241)
**Lens:** required-content (a)-(e) plus the Section 8 structure check (f); fix authorization false
**Date:** 2026-11-14
**Checked:** header and Table of Contents (lines 1-90); Section 6 in full (conflict index C01-C20, all 20 conflict blocks, 6.D defects D1-D16, 6.X, Options Comparison); Section 7 in full (7.1.1-7.1.4, 7.2, 7.3, 7.4); Section 8 (8.1 value inventory all 691 rows by script, 8.2 tracks M1-M4, 8.3, 8.4, 8.5, 8.6); Section 9 (9.5 and the opening rows); Section 10 (all sub-sections). Required part (a) lives in Section 2.6 and belongs to instance a; it was not evaluated here.

[PARTITION NOTE: Cross-section checks are limited to Sections 6-10. Part (a) (overlap matrix, Section 2.6) is covered by instance a; merge both reports for the full lens verdict.]

### Required-part table

| Required part | Present? | Where (section) | Complete? | Missing elements |
|---|---|---|---|---|
| (a) component overlap matrix | Not in partition | Section 2.6 (instance a) | Not evaluated here | n/a for instance b |
| (b) value inventory with destination or DROP per row | Yes | 8.1 (lines 2915-3607) | Yes | None. 691 rows (V-001 to V-691, no gap or duplicate); 0 rows lack a destination or a DROP; 91 DROP rows all carry a reason; 600 rows name one of the 16 core components or 6 thin modules (plus the `Core CLI surface` row type) |
| (c) conflict log | Yes | 6.0 index plus C-01 to C-20 and 6.D | Yes | None. All 11 required topics are covered (C01 schema and severities, C02 anchor handling incl. the 200-character drop, C03 model and tier config, C04 distinctness, C05 who judges, C06 calibration, C07 run recording, C08 identity, C09 dispatch, C10 brief and input contract, C11 merge path and contract bump) plus 9 more (C12-C20); D1-D16 each have options, file:line evidence and a recommended fix; all 4 UNDECIDED conflicts (C03, C05, C13, C14) carry a recorded adversarial result |
| (d) target architecture: shared core and thin modules | Yes | 7.1.1 (diagram), 7.1.2 (data flow), 7.1.3 (16 core components), 7.1.4 (6 thin modules) | Yes | None. Core has finding contract, panel resolution, run manifest, clustering, citation checks, calibration, merge and verdict, telemetry (plus identity, dispatch, brief, decider hook, round model, audits, rollout). Modules: sc:reflect UC-1 and UC-2, workflow and tasklist review, spec review for brainstorm and design, PR code review, rf-qa and rf-qa-qualitative replacement |
| (e) future-use-case check: PR code review and rf-qa replacement | Yes | 7.2 (X1-X13 plus location and registry rows) and 7.3 (blockers) | Yes | None. Lenses, categories, roles, templates and review kinds, and model-role mapping and strata are all named with form, consumer, today's blocker (file:line) and the change needed |
| (f) Section 8 value-capture and migration plan, no roadmap | Yes | 8 (heading and owner-scope paragraph), 8.2, 8.3, 8.4 | Yes | None. Migration path (M1-M4, 19 + 10 + 9 + 7 steps), no-regression gate list (G1-G11, G-all, G-exit, G-replay, G-sync, G-bench, G-new), branch options A-E; the git ref constraint that `feat/review-panel` and `feat/review-panel/<name>` cannot both exist is stated at line 3836 and repeated in 8.6; no dates, sprints or ordering commitments |

### Executor-note checks

| Note | Result | Evidence |
|---|---|---|
| 1. Four `partial` debates (C-03, C-05, C-13, C-14) with unaddressed HIGH invariants are legitimate open items if stated as open | PASS: stated as open everywhere | Status lines 1369, 1525, 2034, 2099 say "UNDECIDED-BY-EVIDENCE, resolved by adversarial debate (partial ...)"; invariant counts (2, 11, 10, 3) match across Section 6, the Section 7 risk table, Section 8 "Binding facts", 9.5 (Q-47 to Q-57) and the Section 10 debate table |
| 2. Core-verdict `[CONTRADICTION]` in Section 7 is an allowed flag | Allowed; carried consistently | Raised at line 2756 (7.1.3), counted at 2889, carried in M1-07, M1-08, M1-16, M3-08 and 8.5, recorded as Q-54; not resolved silently |
| 3. "Tier 2 driven by the parsed-sparse flag in 35 of 39 runs" as measured fact is BLOCKING | PASS: no such sentence presented as fact in Sections 6-10 | Every hit of "35 of 39", "driven by the flag" and "37 of 38" in lines 1146-4241 (1175, 1838, 2044, 2073, 2088, 2091, 2103, 2616, 2882, 2888, 2897, 3232, 3282, 3589, 3653, 3949, 4124) is either the recount (flag set in 35 of 39 non-shadow runs, 34 of 38 Tier 2 runs, decisive in 0 for certain and at most 1) or is quoted as a superseded older claim (V-316, V-366, V-673, D-59, 7.4.2 exclusion row) |
| 4. E2 cited at commit 4a22d74213f93837d00c2c314075dd967b9a98e3 only | PASS | Only one 40-hex SHA appears in lines 1146-4241 (8 occurrences, all `4a22d74213f93837d00c2c314075dd967b9a98e3`); the only other commit ids are E1 `792cf8c52`, `9874d63fb`, `d2d8a2d16`; no reference to the E2 branch tip |
| 5. Report-only, no roadmap | PASS | Heading "(value-capture and migration plan; not a roadmap)"; step ids "carry no order, date or sprint" (3611); 8.4 "commits to no order, date or sprint"; grep for sprint, week, milestone, timeline, roadmap in 3609-3899 finds only disclaimers |

### Findings

| # | Severity | Section | Finding | Proposed Fix |
|---|---|---|---|---|
| 1 | MINOR | 6.0 index C04 (line 1165) against C-04 Status (line 1433) | The index labels C04 `DECIDED-BY-EVIDENCE`, but the C-04 Status says "split decision": the `replicas` part is a design option resting on one uncorrected p-value and the per-consumer default is an owner decision (G-11). The open half has no debate result. It is stated as open in the body, in Q-16 and in the Section 7 adopted-resolutions table, so nothing is hidden. | Optionally relabel the index status as "DECIDED-BY-EVIDENCE (part 1); part 2 open, owner G-11". |
| 2 | MINOR | C-19 (lines 2367-2429) against 7.1.3 Merge and verdict (line 2756) | C-19 is `DECIDED-BY-EVIDENCE` with "Adversarial result: n/a" and its Option A text says "with an optional PENDING"; the verdict-word-set contradiction with the C-05 and C-13 merges is raised only in Section 7, Section 8 and Q-54, not in the C-19 block itself. The flag is an allowed open item (note 2), so this is a cross-reference nit only. | Optionally add one sentence to C-19 pointing to Q-54. |
| 3 | MINOR | 8.1 rows V-415, V-416, V-420, V-426 | Four rows use the destination "Round model (ledger), deferred to O-1", and V-426 (bundle contents) maps to a component only by deferral. A destination is named and a reason given, so the row is not missing either; the mapping is weak. | Optionally give V-426 an explicit DROP (preservation only) or a clearer destination. |

Out-of-lens observation (not graded; for the consistency or content lenses): Section 9 (line 3906) carries a second `[CONTRADICTION]` flag (no gap Critical in Section 9 versus 15 Critical in Section 4), while 7.4.3 (line 2889) states that exactly one `[CONTRADICTION]` flag was raised. Only the Section 7 flag is covered by executor note 2.

### Summary

- Required parts present and complete in Sections 6-10: (b), (c), (d), (e), (f) = 5 of 5; part (a) is outside this partition.
- Findings: 0 CRITICAL, 0 IMPORTANT, 3 MINOR (notes, never fail).
- Confidence: Verified: 14/15 | Unverifiable: 1 (part (a), assigned to instance a) | Unchecked: 0 | Confidence: 100.0% (14 / (15 - 1))
- Tool engagement: Read: 16 | Grep: 3 | Glob: 0 | Bash: 10 (awk and grep over the 691-row inventory table, structure markers of C-01 to C-20, status labels, SHA and roadmap-term scans, spot-check of `findings_v2.py:36`, `panel.py:73`, `findings.py:104,108,118`, `ledger.py:254-258`, `ledger_cmd.py:13` and `__init__.py:19-36`, all of which match the report's citations). Read plus Grep plus Glob (19) exceeds the 15 checklist items.
- Not re-verified (out of lens): numbers inside E2-sourced figures, the contents of the debate folders under `reviews/adversarial/`, and the accuracy of cited line numbers beyond the six spot-checked.

Verdict: PASS (0 critical + 0 important; minor findings listed as notes)

## QA Complete
