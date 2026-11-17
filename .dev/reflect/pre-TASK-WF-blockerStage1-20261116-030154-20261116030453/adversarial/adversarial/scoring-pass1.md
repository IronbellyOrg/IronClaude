# Scoring pass 1 (input order: V1, V2, V3)

Variants: V1 = reviewer 1 analyzer (sonnet class); V2 = reviewer 2 qa (haiku class); V3 = reviewer 3 refactorer (opus class).
Plan under audit: PLAN:<n> = `.dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md`. Spec: SPEC:<n> = `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md`.
Ground-truth defects: C-001 Task 7 grep (PLAN:115); C-002 stoprule family has no repo file (PLAN:62/87/209); C-003 allow-list narrower than stage 3 scan; C-004 no review-ledger/1 mapping (SPEC:404, 945); C-005 scale-map layout/root not fixed; C-007 Task 10 lacks dependency on Task 7.

## A. Quantitative metrics

Own checks made by Read/grep before scoring: PLAN:24, 62, 65, 72, 87, 113, 115, 134, 136, 139, 146, 148, 197, 209; SPEC:145, 404, 485, 582, 880, 920, 945; source.md:12, 17 (22 lines); remediate_parser.py:55, 301; fmea_classifier.py:304, 323; pyproject.toml:179-180; pragmatic.md:227; rf-qa.md:111; card_convert.py:82; auggie SKILL.md:228; test_review_cli.py:44-48; `cli/review/__init__.py` (9 names listed, only 7 modules on disk: lint_cmd.py and estimate_cmd.py absent); `git ls-files` (stoprule / finding-grader files only under `.dev/experiments/`).

| Metric | V1 | V2 | V3 |
|---|---|---|---|
| RC: real defects raised (of 6) | 6: C-001 (F3), C-002 (F1), C-003 (F2), C-004 (F6 "ledger adapters"), C-005 (F4), C-007 (F6 second half) = 6/6 = 1.000 | 3: C-001 (F1), C-002 (F2), C-004 (F3) = 3/6 = 0.500 | 2: C-001 (F2), C-002 (F1) = 2/6 = 0.333 |
| IC: refuted claims / scorable claims | refuted 4 (F3 verify-sync half, F4 wording "only through Task 9", F5 `.dev/pr-monitor/`, Checked "9 review subcommands"); scorable 21 (8 atomic finding claims + 13 Checked claims); IC = 1 - 4/21 = 0.810 | refuted 1 (F3 graded blocking; non-blocking by 2 of 3); scorable 6 (3 findings + 3 Checked); IC = 1 - 1/6 = 0.833 | refuted 3 (F1 tie of "never reads ~/.claude" to T4, F3, F4); scorable 18 (5 finding claims + 13 Checked); IC = 1 - 3/18 = 0.833 |
| SR: concrete / (concrete + vague) | 40 / 43 = 0.930 (vague: "likely" Tasks 12 and 13, "executor can hardcode", one verdict sentence) | 17 / 20 = 0.850 (vague: verdict line, "substituting an unrelated file would misrepresent", "Checked existing pytest paths, command registration, make targets") | 30 / 32 = 0.938 (vague: F3 "may contain", F4 hypothetical) |
| DC: cited quotes found at cited line | 15 of 15 finding cites read, plus 5 Checked-list cites (pragmatic.md:227, rf-qa.md:111, doctor.py:17, test_review_cli.py:47, `__init__.py:19-29`) = 20/20 = 1.000 | 7 of 7 finding cites + PLAN:193-226 range = 8/8 = 1.000 | 14 of 14 finding and Checked cites read (PLAN:62, 209, 115, 148, 24, 197, 139; SPEC:145, 880; source.md:17; pyproject:179-180; pragmatic:227; card_convert:82; rf-qa:111) = 1.000 |
| SC: H2 sections / max (5) | 5 (Verdict, Findings, Checked, Self-report, Calibration) = 1.000 | 5/5 = 1.000 | 5/5 = 1.000 |
| quant_score | 0.30(1.000) + 0.25(0.810) + 0.15(0.930) + 0.15(1.000) + 0.15(1.000) = 0.942 | 0.30(0.500) + 0.25(0.833) + 0.15(0.850) + 0.15 + 0.15 = 0.786 | 0.30(0.333) + 0.25(0.833) + 0.15(0.938) + 0.15 + 0.15 = 0.749 |

## B. Qualitative rubric: 90 lines (CLAIM / EVIDENCE / VERDICT)

Standard applied to all three: MET needs quotable evidence in the card; hedged key claims, undefined terms, and missing fix or detection statements are NOT MET for every variant alike.

### Completeness

Cmp-1 covers all explicit requirements of source.md
- V1: Covers all source requirements / EVIDENCE: Checked names only base findings F3, F4, F5, F9, F12, F13, F15; no whole-source claim / NOT MET
- V2: Covers all source requirements / EVIDENCE: Checked "Compared all 22 source-request lines with the 24 inferred coverage rows" (source.md is 22 lines, verified) / MET
- V3: Covers all source requirements / EVIDENCE: Checked lists only the earlier findings "resolved in Tasks 2, 3, 5, 6 and 15"; no whole-source claim / NOT MET

Cmp-2 edge cases and failure scenarios of the plan
- V1: Failure scenarios / EVIDENCE: F1 unpassable Task 3 vs Task 5, F2 stage 3 scan fails, F3 line false after Task 10 / MET
- V2: Failure scenarios / EVIDENCE: F1 "correct reuse makes the earlier acceptance check false", F3 "tests can pass without the required result" / MET
- V3: Failure scenarios / EVIDENCE: F2 "`__pycache__/*.pyc` also show up in the grep", F1 executor "cannot bring them into the repo" / MET

Cmp-3 dependencies and prerequisites
- V1: Dependencies / EVIDENCE: F4 "Tasks 9 and 12 do not depend on Task 3", F6 "declares only `Depends on: Task 9`", Checked "`Depends on:` edges are acyclic" / MET
- V2: Dependencies / EVIDENCE: No finding or Checked line on task order, files or packages; "Checked existing pytest paths ..." gives no result / NOT MET
- V3: Dependencies / EVIDENCE: Checked "pyproject has pyyaml as a dependency and the wheel packages src/", "origin_repo.py exists" / MET

Cmp-4 defines what would resolve each finding
- V1: Resolution criteria / EVIDENCE: no finding says what edit or check resolves it (F1 to F6 state only the defect) / NOT MET
- V2: Resolution criteria / EVIDENCE: F1 to F3 state defects only; no resolving condition / NOT MET
- V3: Resolution criteria / EVIDENCE: F1 to F4 state defects only; F2 points to the plan's rule but gives no resolving edit / NOT MET

Cmp-5 out of scope or not checked
- V1: Not-checked statement / EVIDENCE: "Not verified: `origin_repo.py`, `reuse-auditor`, `ledger.py` and `findings_v2.py`" / MET
- V2: Not-checked statement / EVIDENCE: "Read-only inspection only; no tests executed ... Future implementation behaviour remains unverified" / MET
- V3: Not-checked statement / EVIDENCE: "I did not check whether the '7 lines' claim ... or Task 1's stage-ledger check. I did not run any test." / MET

### Correctness

Cor-1 no factual errors or hallucinated claims
- V1: No errors / EVIDENCE: Checked "9 `review` subcommands in `cli/review/__init__.py:19-29`" (only 7 modules exist); F3 verify-sync half and F5 refuted by PLAN:25 and PLAN:72 / NOT MET
- V2: No errors / EVIDENCE: no refuted factual claim; F2 "installed-only" matches SPEC:582 and SPEC:880 (the F3 blocking grade is a grading dispute) / MET
- V3: No errors / EVIDENCE: F1 ties "without reading `~/.claude`" to T4, but the clause belongs to T3 (PLAN:209) / NOT MET

Cor-2 technical claims feasible with the repo as it is
- V1: Repo claims accurate / EVIDENCE: says all 9 subcommands exist and that Task 1's `verify-sync` line turns false although PLAN:25 orders `make sync-dev` after every edit / NOT MET
- V2: Repo claims accurate / EVIDENCE: every repo claim checks out (SPEC:404 text, PLAN:115/148 text) / MET
- V3: Repo claims accurate / EVIDENCE: "ruff excludes .dev/" (pyproject.toml:179-180 verified), `__pycache__` exists, lint_cmd.py and estimate_cmd.py absent noted correctly / MET

Cor-3 terminology used consistently and accurately
- V1: Terminology / EVIDENCE: Task N, T4, "Spec T5", blocking true/false used consistently / MET
- V2: Terminology / EVIDENCE: T1–T4 and "undermine T4" used consistently / MET
- V3: Terminology / EVIDENCE: attaches the "never reads `~/.claude`" rule to T4 where PLAN:209 puts it in T3 / NOT MET

Cor-4 no internal contradictions
- V1: Consistency / EVIDENCE: Verdict "Three defects are blocking" matches F1 to F3 blocking true; F6 "partly resolved" matches F3 / MET
- V2: Consistency / EVIDENCE: Verdict "two acceptance checks ... and the required ledger mapping" matches F1 to F3; "F6 remains through F1" matches / MET
- V3: Consistency / EVIDENCE: Verdict "Two acceptance checks cannot pass" matches F1 and F2 blocking; F3 and F4 minor / MET

Cor-5 claims supported by cited evidence
- V1: Citations / EVIDENCE: each finding has 2 to 4 cites with quotes, all 15 read and found at the cited line / MET
- V2: Citations / EVIDENCE: each finding has 2 cites with quotes, all found (PLAN:115/148, PLAN:59-62, SPEC:582/404, PLAN:110-115) / MET
- V3: Citations / EVIDENCE: each finding has 1 to 4 cites with quotes, all found (SPEC:145, SPEC:880, source.md:17, PLAN:209, pyproject:179-180) / MET

### Structure

Str-1 logical ordering
- V1: Order / EVIDENCE: "## Verdict", "## Findings", "## Checked", "## Self-report" / MET
- V2: Order / EVIDENCE: same four sections in that order / MET
- V3: Order / EVIDENCE: same four sections in that order / MET

Str-2 consistent hierarchy
- V1: Hierarchy / EVIDENCE: H2 sections, then one `Fn |` line per finding, bullets in Checked / MET
- V2: Hierarchy / EVIDENCE: same pattern / MET
- V3: Hierarchy / EVIDENCE: same pattern / MET

Str-3 separation of blocking and minor
- V1: Blocking vs minor / EVIDENCE: every finding has `MAJOR | blocking true` or `MINOR | blocking false` fields / MET
- V2: Blocking vs minor / EVIDENCE: F1 to F3 each `MAJOR | blocking true` (the field is present and consistent) / MET
- V3: Blocking vs minor / EVIDENCE: F1, F2 `MAJOR | blocking true`; F3, F4 `MINOR | blocking false` / MET

Str-4 navigation aids
- V1: Navigation / EVIDENCE: ids F1 to F6, "(F3 below)", cites with file:line / MET
- V2: Navigation / EVIDENCE: ids F1 to F3, "F6 remains through F1", cites with file:line / MET
- V3: Navigation / EVIDENCE: ids F1 to F4, "(see F2)", cites with file:line / MET

Str-5 required card format
- V1: Format / EVIDENCE: persona/model header, Verdict, `id | SEV | blocking | category | text | cites:`, Checked, Self-report with confidence / MET
- V2: Format / EVIDENCE: same fields present / MET
- V3: Format / EVIDENCE: same fields present / MET

### Clarity

Cla-1 unambiguous language
- V1: Unambiguous / EVIDENCE: blocking F3 says "Tasks 12 and 13 likely do the same" / NOT MET
- V2: Unambiguous / EVIDENCE: no hedged key claim in F1 to F3 / MET
- V3: Unambiguous / EVIDENCE: F3 "`doctor.py` may contain the fence-opener text" / NOT MET

Cla-2 concrete not abstract
- V1: Concrete / EVIDENCE: names files with lines (`remediate_parser.py:55`, `fmea_classifier.py:304`), Task numbers / MET
- V2: Concrete / EVIDENCE: names Task 7, Task 10, SPEC:404, PLAN:115 quotes / MET
- V3: Concrete / EVIDENCE: names `card_convert.py:82`, `pyproject.toml:179-180`, OD10 / MET

Cla-3 each finding states its consequence in one sentence
- V1: Consequence / EVIDENCE: F6 ends "no task builds or drops them" and "declares only `Depends on: Task 9`" with no stated consequence / NOT MET
- V2: Consequence / EVIDENCE: F1 "false at final review"; F2 "An installed path fails that acceptance check"; F3 "those tests can pass without the required result" / MET
- V3: Consequence / EVIDENCE: F3 ends "The plan does not say whether code files are exempt" with no failure stated / NOT MET

Cla-4 terms defined on first use (PLAN, SPEC, T3, T4)
- V1: Definitions / EVIDENCE: "T4", "Spec T5", "stage 3 scan" used without definition / NOT MET
- V2: Definitions / EVIDENCE: "T4", "T1–T4" used without definition / NOT MET
- V3: Definitions / EVIDENCE: "T4", "T3", "OD10" used without definition / NOT MET

Cla-5 actionable next step or decision identifiable
- V1: Next step / EVIDENCE: Verdict "NEEDS-REVISION", three named blocking defects; F3 names the missing "until Task N" / MET
- V2: Next step / EVIDENCE: Verdict "NEEDS-REVISION", F3 names the missing mapping decision / MET
- V3: Next step / EVIDENCE: Verdict "NEEDS-REVISION"; F1 names the undecided OD10 / MET

### Risk coverage

Rsk-1 at least 3 distinct risks with consequence
- V1: Risks / EVIDENCE: F1 (unpassable), F2 (stage 3 scan fails), F3 (line false), F4 (map drifts) / MET
- V2: Risks / EVIDENCE: F1, F2, F3 each with a stated consequence / MET
- V3: Risks / EVIDENCE: F1 (executor cannot comply), F2 (grep false), F4 ("breaks when the program folder is archived") / MET

Rsk-2 gives a fix or mitigation direction for each
- V1: Mitigation / EVIDENCE: none of F1 to F6 states an edit direction / NOT MET
- V2: Mitigation / EVIDENCE: none of F1 to F3 states an edit direction / NOT MET
- V3: Mitigation / EVIDENCE: none of F1 to F4 states an edit direction / NOT MET

Rsk-3 failure modes of the plan's later stages
- V1: Later stages / EVIDENCE: F2 "The stage 3 scan reads this list, so it fails on those files" / MET
- V2: Later stages / EVIDENCE: only the same package's final review (F1); no later stage named / NOT MET
- V3: Later stages / EVIDENCE: F4 test importing the sketch "breaks when the program folder is archived"; F3 T2 scan over `src/` / MET

Rsk-4 external dependencies (installed files, other stages)
- V1: External / EVIDENCE: F1 only copies under `.dev/experiments/`; SPEC:582 "only under `~/.claude/agents/`"; F2 stage 3 / MET
- V2: External / EVIDENCE: F2 "actual finding-grader definition is installed-only" / MET
- V3: External / EVIDENCE: F1 "exist only in installed copies", OD10, SPEC:145 "installed only" / MET

Rsk-5 includes a way to detect the risk (check or grep)
- V1: Detection / EVIDENCE: F1 "a grep of `src` for `stoprule\|finding-grader` finds nothing" / MET
- V2: Detection / EVIDENCE: names only the plan's own PLAN:115 grep; no detection check of its own / NOT MET
- V3: Detection / EVIDENCE: names only the plan's own grep and the `__pycache__` noise; no new detection check / NOT MET

### Invariant and edge-case coverage

Inv-1 collection boundaries (empty or single, grep that matches nothing)
- V1: Boundaries / EVIDENCE: F1 grep of `src` finds nothing; F3 "No `follow_ups` command wiring exists" / MET
- V2: Boundaries / EVIDENCE: no empty-set or no-match case in F1 to F3 or Checked / NOT MET
- V3: Boundaries / EVIDENCE: Checked "None of the 11 carriers contains `src/superclaude`, so the T3 check passes"; `lint_cmd.py`/`estimate_cmd.py` absent but optional / MET

Inv-2 state across task boundaries
- V1: Cross-task state / EVIDENCE: F3 Task 10 imports Task 7's reader; F4 `scale-map.md` from Task 3 read by Tasks 9 and 12 / MET
- V2: Cross-task state / EVIDENCE: F1 Task 7's grep versus Task 10's reuse (PLAN:115 vs PLAN:148) / MET
- V3: Cross-task state / EVIDENCE: F2 Task 10 imports Task 7's reader into `classifier_inputs.py` / MET

Inv-3 guard conditions (preconditions of acceptance commands)
- V1: Guards / EVIDENCE: F1 Task 5's `.dev/` grep cannot hold with Task 3's rows; F3 grep false after Task 10 / MET
- V2: Guards / EVIDENCE: F1 the PLAN:115 grep rejects correct reuse by Task 10 / MET
- V3: Guards / EVIDENCE: F2 `__pycache__/*.pyc` matches change the PLAN:115 grep result / MET

Inv-4 count divergence (counts asserted vs real files)
- V1: Counts / EVIDENCE: Checked affirms "9 `review` subcommands" while only 7 modules exist (`lint_cmd.py`, `estimate_cmd.py` absent) / NOT MET
- V2: Counts / EVIDENCE: no plan-asserted count checked against a real file (22 lines vs 24 rows is the card's own inference) / NOT MET
- V3: Counts / EVIDENCE: Checked "old definition sentence appears in exactly 11 files", "4*5*5*4*4*4 = 6,400", notes `lint_cmd.py`/`estimate_cmd.py` absent / MET

Inv-5 interaction effects with existing tests and make targets
- V1: Interactions / EVIDENCE: Checked "`test_review_cli.py:47` checks only four subcommand names", no name clash for `classify` / MET
- V2: Interactions / EVIDENCE: only "Checked existing pytest paths, command registration, make targets" with no specifics / NOT MET
- V3: Interactions / EVIDENCE: Checked "`_has_corresponding_command(\"sc-review-severity\")` returns False", "`test_review_cli.py:44-48` is not affected", banned-phrase scans / MET

## C. Subtotals

| Dimension (5 each) | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 3 | 3 | 3 |
| Correctness | 3 | 5 | 3 |
| Structure | 5 | 5 | 5 |
| Clarity | 2 | 4 | 2 |
| Risk coverage | 4 | 2 | 3 |
| Invariant and edge-case | 4 | 2 | 5 |
| Total MET of 30 | 21 | 21 | 21 |
| qual_score | 0.700 | 0.700 | 0.700 |

## D. Edge-case floor check

Invariant and edge-case dimension: V1 4/5, V2 2/5, V3 5/5. All three are at least 1 of 5, so none is ineligible as base. No warning needed.

## E. Combined scores and ranking

combined = 0.5 quant + 0.5 qual.

| Rank | Variant | quant | qual | combined |
|---|---|---|---|---|
| 1 | V1 (analyzer) | 0.942 | 0.700 | 0.821 |
| 2 | V2 (qa) | 0.786 | 0.700 | 0.743 |
| 3 | V3 (refactorer) | 0.749 | 0.700 | 0.725 |

Top two (V1 0.821, V2 0.743) are not within 5 percent: gap 0.078 (9.5 percent of V1). V2 and V3 are within 5 percent of each other (gap 0.019). The qualitative rubric ties all three at 21/30, so the order comes only from the quantitative side, driven by requirement coverage (V1 6/6, V2 3/6, V3 2/6). V1 carries the most errors (4 refuted claims: verify-sync half, "only through Task 9" wording, `.dev/pr-monitor/`, "9 subcommands") yet still ranks first. V2 has the cleanest accuracy. V3 has the strongest invariant coverage but the narrowest defect coverage.
