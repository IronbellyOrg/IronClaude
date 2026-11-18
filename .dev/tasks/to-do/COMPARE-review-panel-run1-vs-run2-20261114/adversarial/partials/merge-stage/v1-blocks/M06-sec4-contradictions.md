<!-- Source: Variant 1, Section 4 (lines 735-780) — merged per Change #M-06; ids prefixed R1- -->
### 4.8 Run 1 contradictions and track coverage

Run 1's contradictions table, coverage self-check and Critical and Important rows by track, with the `Track` mapping kept. R1-M1 to R1-M4 are run 1's track names for its migration steps (the steps are carried in 8.4). <!-- Source: new (lead per Change #M-06) -->

#### R1 4.1 Contradictions between research files and which finding has the stronger evidence

| # | Contradiction | Files | Stronger finding and why |
|---|---|---|---|
| 1 | R1-D2 and R1-D11 "NOT covered by tests" vs both pinned in the defect direction | hand-off section 8, scope 02 section 6 vs `research/12` section 3 | `research/12`: test bodies were read (`test_review_ledger.py:376-385`, `test_review_panel_exclusion.py:97-98,:208-213`). |
| 2 | "No skill or command calls `review panel resolve`, `merge` or `ledger`" vs prompt line `document_review_loop_prompts.md:70` and reflect shadow step 1 | scope 02 R1-D14, hand-off vs `research/04` section 9, `research/09` section 7 | `research/09`: direct grep 2026-11-14 with per-subcommand table. The gap stays Critical (R1-D14): the only callers are one prose paragraph and a shadow path no consumer enables. |
| 3 | "4 verdicts flipped" vs 3 named flips | hand-off R1-D1, CR:292 vs `research/02` section 4.2 | `research/02`: `AD/summary.md:20`, `audit2.json` `verdict_flip`, `flags.tsv` re-counted (4 EXCLUDE lines, 3 merges). |
| 4 | "195 of 1398 rows with 3 or more members" vs 1398 being all rows | `AD/summary.md:29`, scope 01 R1-H16 vs `research/03` section 7 | `research/03`: `audit2.py:140-145,:154` shows `rows_total` counted before the filter. |
| 5 | "`confidence` computed but never used" vs printed in the merged report | hand-off R1-D4 vs `research/02` section 1.4 | `research/02`: `ledger.py:435,:473`. Display only; no decision reads it. |
| 6 | `tests/cli/reflect/` "twelve files" vs 37 or 38 files | task prompt, `research-notes.md:46` vs `research/12` (37) and QA (38) | `research/12` collection run (353 tests agree); the 37 vs 38 file count stays unresolved. |
| 7 | "No Python writer of `return-contract.yaml`" (original `research/08`) vs `ensemble.py:886-895` | `research/08` before fix cycle 1 vs `research/13` section 4 | `research/13`: code read; true only for the skill-path 1.8.0 contract. |
| 8 | Calibrator "re-grades on the 5-dim reflection rubric" vs a 6-dim troubleshoot rubric | `SKILL.md:631,416` vs `confidence-calibrator.md:48,61,67` (`research/05` section 4) | `research/05`: the agent file is the implementation; the skill text is documentation. Which rubric recorded calibrators applied was never sampled (R1-G-09). |
| 9 | Shadow15 parity failure attributed to defects fixed by `9874d63fb` and `c2e3347d3` vs shadow15 running after `9874d63fb` and still failing | `research/07` section 5.1 vs `research/11` section 8 | `research/11` section 8 (run-by-run classification); use it for run classification (R1-G-60). |
| 10 | `cluster_agreement` "null for every listed run" and "1.000 everywhere" | scope 04 vs `research/03` section 6 and `stage0a-report.md:247-291` | `research/03`: 11 of 14 shadow runs are 1.0 only because they have no blocking cluster; shadow09 is 0.9328. |
| 11 | Variants "only in the bundle" vs installed in `~/.claude/` | hand-off R1-D14, `research/01`, `research/02` wording vs `research/09` section 2.4 and `research/02` section 6 | `research/09`: `ls` of `~/.claude/` 2026-11-14. Neither is in `src`. |
| 12 | "Sonnet alone gives most catches per token" vs E2's valid-era tables | `COMBO/PLAN.md:18-24` via scope 04 vs `research/11` section 6 | `research/11`: pilot-only claim (n=1 per package, pre-source era). |
| 13 | "`--coverage` edits are branch-only after #519" vs an empty `git diff --stat origin/master HEAD -- src/superclaude/cli/review` | `research-notes.md:39` vs `research/09` section 1.1 | `research/09`: git evidence; the E1 kernel is master code. |
| 14 | Enabling the panel for skill-path consumers is "a reflect flag change (`--t2-engine`)" vs only `--t2-engine shadow` being passable | `research/09` :159, :183, :259 vs `SKILL.md:87,:338` | `SKILL.md`: say "shadow only today" (R1-G-93). |
| 15 | Log severity "No gap is Critical" vs Critical rows here | `gaps-and-questions.md` vs this table | Different scales: the log rates whether a gap blocks a required report part; this table rates impact on the target state and applies control R1-C8 to unwired in-scope capabilities. The 15 Critical rows are 11 distinct gaps plus 4 restatement rows (R1-DOC-20, R1-DOC-63 to R1-DOC-65): 7 distinct gaps are raised by control R1-C8 (R1-D14, R1-MS-11, R1-MS-14, R1-ENS-1, R1-ENS-3, R1-ENS-4, R1-ENS-5) and 4 are rated Critical on impact (R1-D1, R1-D3, R1-D4, R1-ENS-2; the Notes cell of each states its basis). Where R1-C8 raises a rating (R1-MS-14 from log R1-G-03 Important; R1-ENS-4 from research grade Medium; R1-ENS-3 from High) the row says so. |
| 16 | "Tier 2 is driven by the parsed-sparse flag" (MR:142, MR:556; `research/11` section 12 item 4) vs the R1-C-14 debate recount | MR and `research/11` vs `reviews/adversarial/panel-size-cost/adversarial/return-contract.yaml` and `adversarial/recount_tier_decision.py` | The recount: the flag was set in 35 of 39 non-shadow runs (34 of 38 Tier 2 runs) and was decisive in 0 for certain and at most 1; 29 of the 34 flagged Tier 2 runs also have a recorded escalate row 4, 5 or 6. The script re-read the 39 `tier_decision.yaml` files and the ambiguous runs' cards; the older figures were counts without a decisiveness test. Caveat: the recorded fields are model-written. |

#### R1 4.2 Coverage self-check

| Check | Result |
|---|---|
| Rows in the gap table | 145: R1-D1..R1-D16 (16), R1-BL-01 to R1-BL-23 (23), R1-MS-01 to R1-MS-24 (24), R1-ENS-01 to R1-ENS-09 (9), R1-OPEN-01 to R1-OPEN-02 (2), R1-DOC-01 to R1-DOC-77 (71 rows: R1-DOC-01 to R1-DOC-70 plus one combined row for the seven QA notes R1-D-71 to R1-D-77). |
| Every Notes cell begins with `Track:` and uses only R1-M1, R1-M2, R1-M3, R1-M4 or `none (drop: <reason>)` | Yes, checked by script: R1-M1 56, R1-M2 21, R1-M3 18, R1-M4 16, none 34. |
| Severity | Critical 15, Important 66, Minor 64. Critical rows by track: R1-M1 R1-D1, R1-D3, R1-D4, R1-MS-11, R1-DOC-20; R1-M2 R1-MS-14; R1-M3 R1-D14, R1-ENS-1 to R1-ENS-5, R1-DOC-63 to R1-DOC-65. |
| All sixteen defects R1-D1..R1-D16 present with status and file:line | Yes (rows R1-D1..R1-D16): 16 of 16 confirmed at current code (scope 02 rated R1-D9 "partly confirmed" because the brief side was out of its slice; `research/05` section 10 read the brief side); R1-D4 "confidence unused" partly contradicted; R1-D11, R1-D12, R1-D7 hand-off lines moved; R1-D14 corrected (one prose caller exists). |
| PR and rf-qa blockers with file:line | Yes: R1-BL-01 to R1-BL-23 (closed lens tuple R1-BL-01, spec-only categories R1-BL-02, 3-level severity R1-BL-03, anchor-only merge R1-BL-04, single document R1-BL-05, anchor clustering R1-BL-06, id regex R1-BL-07, templates bind models R1-BL-08, `--kind` R1-BL-09, telemetry strata R1-BL-10, no monotonicity halt R1-BL-11, read-only versus in-place fixing R1-BL-12, three verdict contracts R1-BL-13, closed PR reviewer set R1-BL-14, and the PR router, rubric and rf-qa wording blockers R1-BL-15 to R1-BL-23). |
| Missing shared pieces | R1-MS-01 finding contract, R1-MS-02 clusterer, R1-MS-03 merge and verdict, R1-MS-04 run record, R1-MS-05 brief template, R1-MS-06 resolver policy, R1-MS-07 to R1-MS-10 consumer hooks. |
| Every [CODE-CONTRADICTED] or [STALE DOC] finding of the log has a row | R1-DOC-01 to R1-DOC-70 and the combined QA-note row (log R1-D-01 to R1-D-77). |
| Unwired in-scope capabilities (control R1-C8) | 11 rows carry the R1-C8 remediation note (7 distinct gaps: R1-D14, R1-MS-11, R1-MS-14, R1-ENS-1, R1-ENS-3, R1-ENS-4, R1-ENS-5; R1-DOC-20 and R1-DOC-63 to R1-DOC-65 restate four of them). The 15 Critical rows are therefore 11 distinct gaps (these 7 plus R1-D1, R1-D3, R1-D4, R1-ENS-2, rated on impact) and 4 restatement rows. No remediation task was created (report-only run). |
| Important rows with `Track: none` | R1-MS-23, R1-DOC-11, R1-DOC-15, R1-DOC-27, R1-DOC-47: each states why no migration track applies (pending external input, or a wording correction whose underlying gap is tracked at another row). |
| Known-contradicted claims not built on | variants only in the bundle (R1-DOC-15), audits B/C/E/F summaries (R1-DOC-45), 4 verdict flips (R1-DOC-11), alias GT3 (R1-DOC-61), hand-off line numbers for R1-D7, R1-D11, R1-D12 (R1-DOC-16, R1-DOC-21), `merge_round` docstring on clearing (R1-DOC-09). |
| Items outside this report part (carried by other syntheses) | Overlap matrix, value inventory, conflict log, per-panel E2 results and Tier 2 cost-versus-worth (`research/11` sections 6, 12), the E2 tier and panel recommendations, singleton-handling statistics (`web-01` section 3.4) and the bias-battery recommendations (`web-03`) beyond the rows above, and all Section 8 and Section 9 content. Excluded here because Sections 3 and 4 define the target and list gaps; their evidence is cited where a gap row needs it. |

#### R1 4.3 Critical and Important rows by track (input for Section 8)

| Track | Critical rows | Important rows |
|---|---|---|
| R1-M1 shared-core contract | R1-D1, R1-D3, R1-D4, R1-MS-11, R1-DOC-20 | R1-D2, R1-D5, R1-D6, R1-D7, R1-D8, R1-D9, R1-D11, R1-D13, R1-D15, R1-D16, R1-BL-01 to R1-BL-08, R1-BL-23, R1-MS-01 to R1-MS-06, R1-MS-17, R1-MS-19 to R1-MS-22, R1-OPEN-01, R1-DOC-09, R1-DOC-34 |
| R1-M2 reflect onto core | R1-MS-14 | R1-MS-12, R1-MS-13, R1-MS-15, R1-MS-16, R1-MS-18, R1-MS-24, R1-ENS-7, R1-OPEN-02, R1-DOC-08, R1-DOC-28, R1-DOC-41, R1-DOC-62 |
| R1-M3 tasklist and spec consumers | R1-D14, R1-ENS-1 to R1-ENS-5, R1-DOC-63 to R1-DOC-65 | R1-MS-07, R1-MS-08, R1-ENS-6, R1-ENS-9, R1-DOC-66 |
| R1-M4 future consumers | none | R1-BL-11 to R1-BL-18, R1-BL-20, R1-DOC-03, R1-DOC-51 |
| none (drop) | none | R1-MS-23, R1-DOC-11, R1-DOC-15, R1-DOC-27, R1-DOC-47 |
