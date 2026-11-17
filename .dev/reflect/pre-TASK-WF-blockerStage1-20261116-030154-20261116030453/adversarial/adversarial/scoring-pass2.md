# Scoring Pass 2 (reverse order: variant 3, then 2, then 1)

Scorer: independent judge, hybrid scoring step. Plan under audit: PLAN = `.dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md`. Spec: SPEC = `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md`. Variants: V3 = reviewer 3 (refactorer), V2 = reviewer 2 (qa), V1 = reviewer 1 (analyzer).
Verified-real defects used for RC: C-001 (PLAN:115 false after Tasks 10 and 12), C-002 (stoprule/finding-grader has no file in the repository), C-003 (allow-list narrower than stage 3 scan), C-004 (no review-ledger/1 mapping decision), C-005 (scale-map layout and root not fixed), C-007 (Task 10 lacks Depends on Task 7).

## Verification I did myself (Read/grep this session)
- PLAN:24, 62, 65, 72, 87, 110-115, 134, 136, 146, 148, 197, 209 quoted text present as cited by the variants.
- SPEC:145 and 880 ("installed only"), 404 ("A mapping rule from its rows to `review-ledger/1` rows is left to the `/sc:workflow` plan"), 485, 582, 920, 945 present as cited.
- `remediate_parser.py:55,301` and `fmea_classifier.py:304,323` hold the phrases (C-003 real). `git ls-files src plugins` has no stoprule/finding-grader file; the only tracked copies are under `.dev/experiments/` (C-002 real).
- `src/superclaude/cli/review/__init__.py:19-29` lists 9 module names but only 7 exist (no `lint_cmd.py`, `estimate_cmd.py`); V1's "9 review subcommands" is wrong. `__pycache__` exists in `cli/review/` (V3 F2 point is true).
- 11 files under src/ hold the old definition sentence, 0 of them contain `src/superclaude`, 0 under plugins/ (V3 Checked true). The tasklist skill has 7 lines that tie Medium to blocking (V1 Checked true).
- `origin_repo.py` exists at `src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py` (V3 "exists" true, V1 could not check). `pyproject.toml:38` pyyaml (true). `pyproject.toml:179-180` extend-exclude with `.dev/` (V3 F4 cite true).

## (A) Quantitative table

| Metric | V3 | V2 | V1 | Counts used |
|---|---|---|---|---|
| RC requirement_coverage | 0.333 | 0.500 | 1.000 | V3 raises C-001 (F2), C-002 (F1) = 2/6. V2 raises C-001 (F1), C-002 (F2), C-004 (F3) = 3/6. V1 raises C-001 (F3), C-002 (F1), C-003 (F2), C-005 (F4), C-007 (F6 second sentence), C-004 (F6 "ledger adapters", SPEC:945, same gap, raised as minor) = 6/6 |
| IC internal_consistency | 0.800 | 0.857 | 0.688 | V3: 15 scorable (4 findings + 11 Checked bullets); refuted 3 (F1 T4 tie, F3, F4) = 12/15. V2: 7 (3 + 4 Checked); refuted 1 (F3 graded blocking) = 6/7. V1: 16 (6 findings + 10 Checked statements; the closing "Not verified" line is a disclaimer, not scored); refuted 5 (F2 blocking grade, F3 verify-sync half, F4 "only through Task 9" wording, F5, "9 subcommands" bullet) = 11/16 |
| SR specificity_ratio | 0.949 | 0.833 | 0.966 | Concrete / (concrete + vague), headings and metadata excluded. V3 37/39 (vague: F3 "plan does not say whether exempt", F4 "does not say where"). V2 20/24 (vague: "Checked existing pytest paths, command registration, make targets...", "Read-only inspection only", "Future implementation behaviour remains unverified", F2 "misrepresent the scale"). V1 56/58 (vague: F4 "map and code drift" clause, one hedge "likely") |
| DC dependency_completeness | 1.000 | 1.000 | 1.000 | Checked 12 of 12 for V3 (PLAN:62, 209 twice, 115, 148, 24, 197; source.md:17; SPEC:145, 880; pyproject:179-180) and 6 Checked-list cites (pragmatic.md:227, card_convert.py:82, rf-qa.md:111, auggie SKILL.md:228, test_review_cli.py:44-48): all quoted text found. V2 7 of 7 (PLAN:59-62, 110-115, 115, 148, 193-226; SPEC:404, 582). V1 16 of 16 cites (PLAN:24, 62, 65, 72, 87, 115, 134, 136, 146, 148; SPEC:485, 582, 920, 945; remediate_parser.py:55; fmea_classifier.py:304) plus doctor.py:17, test_review_cli.py:47. Extrapolated 1.0 |
| SC section_coverage | 1.000 | 1.000 | 1.000 | Each variant has 5 H2 sections (Verdict, Findings, Checked, Self-report, Calibration); max = 5 |
| **quant_score** | **0.7424** | **0.7893** | **0.9168** | 0.30 RC + 0.25 IC + 0.15 SR + 0.15 DC + 0.15 SC |

Arithmetic: V3 = 0.1000 + 0.2000 + 0.1424 + 0.1500 + 0.1500 = 0.7424. V2 = 0.1500 + 0.2143 + 0.1250 + 0.1500 + 0.1500 = 0.7893. V1 = 0.3000 + 0.1719 + 0.1449 + 0.1500 + 0.1500 = 0.9168.

## (B) Qualitative rubric: 90 CEV lines

### Completeness

**V3**
- C1 CLAIM: covers all explicit source request requirements / EVIDENCE: no comparison with source.md in Checked; only "earlier review's findings ... resolved" / NOT MET
- C2 CLAIM: edge cases and failure scenarios / EVIDENCE: F2 "Matches in `__pycache__/*.pyc` also show up in the grep"; F3 doctor fence text / MET
- C3 CLAIM: dependencies and prerequisites / EVIDENCE: Checked "pyproject has pyyaml as a dependency", "origin_repo.py exists" / MET
- C4 CLAIM: defines what would resolve each finding / EVIDENCE: No evidence found (F1 to F4 state problems, no resolution criterion) / NOT MET
- C5 CLAIM: says what was not checked / EVIDENCE: "I did not check whether the '7 lines' claim ... or Task 1's stage-ledger check. I did not run any test." / MET

**V2**
- C1 CLAIM: covers source request requirements / EVIDENCE: Checked "Compared all 22 source-request lines with the 24 inferred coverage rows; no requirement-bearing span was absent" / MET
- C2 CLAIM: edge cases and failure scenarios / EVIDENCE: F3 "those tests can pass without the required result"; F2 "An installed path fails that acceptance check" / MET
- C3 CLAIM: dependencies and prerequisites / EVIDENCE: only "Checked existing pytest paths, command registration, make targets" with no named item / NOT MET
- C4 CLAIM: defines what would resolve each finding / EVIDENCE: No evidence found / NOT MET
- C5 CLAIM: says what was not checked / EVIDENCE: "Read-only inspection only; no tests executed ... Future implementation behaviour remains unverified" / MET

**V1**
- C1 CLAIM: covers source request requirements / EVIDENCE: No evidence found (Checked compares plan with spec and disk, not with source.md) / NOT MET
- C2 CLAIM: edge cases and failure scenarios / EVIDENCE: F2 stage 3 scan fails on `remediate_parser.py:55`; F5 verbatim copy fails Task 5 grep / MET
- C3 CLAIM: dependencies and prerequisites / EVIDENCE: F4 "Tasks 9 and 12 do not depend on Task 3"; F6 "declares only `Depends on: Task 9`"; Checked "`Depends on:` edges are acyclic" / MET
- C4 CLAIM: defines what would resolve each finding / EVIDENCE: No evidence found / NOT MET
- C5 CLAIM: says what was not checked / EVIDENCE: "Not verified: `origin_repo.py`, `reuse-auditor`, `ledger.py` and `findings_v2.py`" / MET

### Correctness

**V3**
- K1 CLAIM: no factual errors / EVIDENCE: F1 ties "never reads `~/.claude`" to T4; it belongs to T3 (PLAN:209), conceded in debate; F3 and F4 refuted / NOT MET
- K2 CLAIM: technical claims feasible with the repo as it is / EVIDENCE: `__pycache__` present in cli/review; no stoprule file under src/ (git ls-files); 11-file count true / MET
- K3 CLAIM: terminology used accurately / EVIDENCE: F1 "T4 needs each row's file to exist, without reading `~/.claude`" mislabels the test id / NOT MET
- K4 CLAIM: no internal contradictions / EVIDENCE: No evidence found of any; Checked and findings agree / MET
- K5 CLAIM: claims supported by cited evidence / EVIDENCE: every finding has `cites:` with quoted text, all 12 verified / MET

**V2**
- K1 CLAIM: no factual errors / EVIDENCE: all stated facts hold (PLAN:115/148, SPEC:404, 582); only grade of F3 is contested, a judgment not a fact / MET
- K2 CLAIM: technical claims feasible / EVIDENCE: F2 "no task adds it" matches git ls-files; F1 reuse makes grep false / MET
- K3 CLAIM: terminology accurate / EVIDENCE: uses T7, T1 to T4 and "review-ledger/1" as in the plan and spec / MET
- K4 CLAIM: no internal contradictions / EVIDENCE: No evidence found of any / MET
- K5 CLAIM: supported by cited evidence / EVIDENCE: F1 to F3 each carry two quoted cites that exist / MET

**V1**
- K1 CLAIM: no factual errors / EVIDENCE: Checked "the 9 `review` subcommands in `cli/review/__init__.py:19-29`" (only 7 exist); F5 `.dev/pr-monitor/` refuted; F4 "only through Task 9" refuted (PLAN:169 lists Tasks 7, 9, 10) / NOT MET
- K2 CLAIM: technical claims feasible / EVIDENCE: F3 "Task 1's `verify-sync` line has the same problem" is false because PLAN:25 orders `make sync-dev` after every edit / NOT MET
- K3 CLAIM: terminology accurate / EVIDENCE: "Spec T5", "stage 3 scan", "Task 3 allow-list" match the spec (SPEC:920) / MET
- K4 CLAIM: no internal contradictions / EVIDENCE: No evidence found of any; verdict list (3 blocking) matches the F1 to F3 flags / MET
- K5 CLAIM: supported by cited evidence / EVIDENCE: 16 cites each with quoted text, all found, e.g. `remediate_parser.py:55` "higher severity wins (BLOCKING > WARNING > INFO)" / MET

### Structure

**V3**
- S1 CLAIM: logical ordering / EVIDENCE: sections run Verdict, Findings, Checked, Self-report, Calibration / MET
- S2 CLAIM: consistent hierarchy / EVIDENCE: all findings use the same `F# | grade | blocking | category | text | cites` line / MET
- S3 CLAIM: separation of blocking and minor / EVIDENCE: F1, F2 "MAJOR | blocking true", F3, F4 "MINOR | blocking false" / MET
- S4 CLAIM: navigation aids / EVIDENCE: ids F1 to F4, "(see F2)" in Checked / MET
- S5 CLAIM: follows the required card format / EVIDENCE: persona/model header, Verdict, Findings, Checked, Self-report with confidence present / MET

**V2**
- S1 CLAIM: logical ordering / EVIDENCE: same five-section order / MET
- S2 CLAIM: consistent hierarchy / EVIDENCE: F1 to F3 in the same line format / MET
- S3 CLAIM: separation of blocking and minor / EVIDENCE: all three marked "blocking true"; the flag exists on every finding; no minor section needed / MET
- S4 CLAIM: navigation aids / EVIDENCE: ids F1 to F3; "F6 remains through F1" / MET
- S5 CLAIM: required card format / EVIDENCE: required sections present (absolute paths in cites instead of repo-relative, cosmetic per S-002) / MET

**V1**
- S1 CLAIM: logical ordering / EVIDENCE: same five-section order / MET
- S2 CLAIM: consistent hierarchy / EVIDENCE: F1 to F6 in the same line format; Checked uses nested bullets / MET
- S3 CLAIM: separation of blocking and minor / EVIDENCE: F1 to F3 "blocking true", F4 "MAJOR | blocking false", F5 and F6 "MINOR | blocking false" / MET
- S4 CLAIM: navigation aids / EVIDENCE: ids F1 to F6, "(F3 below)" in the verdict / MET
- S5 CLAIM: required card format / EVIDENCE: all required sections and fields present / MET

### Clarity

**V3**
- L1 CLAIM: unambiguous language / EVIDENCE: F3 "`doctor.py` may contain the fence-opener text" leaves open whether it is a defect / NOT MET
- L2 CLAIM: concrete not abstract / EVIDENCE: F2 quotes PLAN:115 and PLAN:148 and names `classifier_inputs.py` / MET
- L3 CLAIM: each finding states its consequence in one sentence / EVIDENCE: F3 ends "The plan does not say whether code files are exempt" with no consequence stated / NOT MET
- L4 CLAIM: terms defined on first use / EVIDENCE: "T3", "T4", "OD10", "PLAN", "SPEC" used with no definition / NOT MET
- L5 CLAIM: actionable next step or decision identifiable / EVIDENCE: "NEEDS-REVISION" plus F1, F2 "blocking true" / MET

**V2**
- L1 CLAIM: unambiguous language / EVIDENCE: F3 "tests the codec contract, not the missing mapping" has one reading / MET
- L2 CLAIM: concrete not abstract / EVIDENCE: F1 names Task 7, Task 10, PLAN:115 and the reused reader / MET
- L3 CLAIM: each finding states its consequence / EVIDENCE: F1 "makes the earlier acceptance check false at final review"; F2 "An installed path fails"; F3 "can pass without the required result" / MET
- L4 CLAIM: terms defined on first use / EVIDENCE: "T7 failure condition", "T1–T4" undefined / NOT MET
- L5 CLAIM: actionable next step or decision / EVIDENCE: "NEEDS-REVISION" plus three blocking flags / MET

**V1**
- L1 CLAIM: unambiguous language / EVIDENCE: F3 "Tasks 12 and 13 likely do the same" mixes a hedge into a blocking finding / NOT MET
- L2 CLAIM: concrete not abstract / EVIDENCE: F2 names `remediate_parser.py:55` and `:301`, `fmea_classifier.py:304` / MET
- L3 CLAIM: each finding states its consequence / EVIDENCE: F6 "no task builds or drops them" states a gap with no consequence / NOT MET
- L4 CLAIM: terms defined on first use / EVIDENCE: "T4", "T5", "PF", "stage 4 files" undefined / NOT MET
- L5 CLAIM: actionable next step or decision / EVIDENCE: "NEEDS-REVISION. Three defects are blocking" lists which / MET

### Risk coverage

**V3**
- R1 CLAIM: at least 3 distinct risks with consequence / EVIDENCE: F1 unpassable check, F2 false line at final review, F4 test breaks on archive / MET
- R2 CLAIM: gives fix or mitigation direction for each / EVIDENCE: No evidence found (F1, F2 state no fix) / NOT MET
- R3 CLAIM: failure modes of later stages / EVIDENCE: F2 "false by the final review"; F3 T2 scan over `doctor.py` / MET
- R4 CLAIM: external dependencies / EVIDENCE: F1 "exist only in installed copies", "OD10 is undecided" / MET
- R5 CLAIM: way to detect the risk / EVIDENCE: No evidence found (no new check or grep proposed for the findings) / NOT MET

**V2**
- R1 CLAIM: at least 3 distinct risks with consequence / EVIDENCE: F1, F2, F3 each with consequence / MET
- R2 CLAIM: fix or mitigation direction / EVIDENCE: No evidence found / NOT MET
- R3 CLAIM: failure modes of later stages / EVIDENCE: F1 "false at final review"; F2 "undermine T4" / MET
- R4 CLAIM: external dependencies / EVIDENCE: F2 "actual finding-grader definition is installed-only", SPEC:582 / MET
- R5 CLAIM: way to detect the risk / EVIDENCE: No evidence found / NOT MET

**V1**
- R1 CLAIM: at least 3 distinct risks with consequence / EVIDENCE: F1, F2, F3 blocking with consequences, plus F4, F5 / MET
- R2 CLAIM: fix or mitigation direction / EVIDENCE: No evidence found (F4 only notes that Task 3 fixes no layout) / NOT MET
- R3 CLAIM: failure modes of later stages / EVIDENCE: F2 "the stage 3 scan reads this list, so it fails" / MET
- R4 CLAIM: external dependencies / EVIDENCE: F1 SPEC:582 "exists only under `~/.claude/agents/`"; F2 stage 3 scan / MET
- R5 CLAIM: way to detect the risk / EVIDENCE: F1 "a grep of `src` for `stoprule\|finding-grader` finds nothing" / MET

### Invariant and edge-case coverage

**V3**
- I1 CLAIM: collection boundaries / EVIDENCE: Checked "None of the 11 carriers contains `src/superclaude`" (a grep matching nothing); F2 `.pyc` extra matches / MET
- I2 CLAIM: state across task boundaries / EVIDENCE: F2 Task 10 imports Task 7 reader into `classifier_inputs.py` / MET
- I3 CLAIM: guard conditions / EVIDENCE: F2 the grep reads compiled `__pycache__` files, a precondition of the acceptance command / MET
- I4 CLAIM: count divergence / EVIDENCE: Checked "exactly 11 files ... matches the 11 digest rows", "4*5*5*4*4*4 = 6,400" / MET
- I5 CLAIM: interaction effects with existing tests and make targets / EVIDENCE: Checked "test_review_cli.py:44-48 is not affected by a new `classify` subcommand"; F4 ruff excludes `.dev/` / MET

**V2**
- I1 CLAIM: collection boundaries / EVIDENCE: No evidence found / NOT MET
- I2 CLAIM: state across task boundaries / EVIDENCE: F1 Task 10 reuses Task 7 reader, adds a match / MET
- I3 CLAIM: guard conditions / EVIDENCE: No evidence found / NOT MET
- I4 CLAIM: count divergence / EVIDENCE: "22 source-request lines with 24 coverage rows" compares the request with itself, not plan counts with files / NOT MET
- I5 CLAIM: interaction effects / EVIDENCE: "Checked existing pytest paths, command registration, make targets" names no file or result / NOT MET

**V1**
- I1 CLAIM: collection boundaries / EVIDENCE: F1 grep of `src` for stoprule/finding-grader finds nothing; F5 `.dev/` grep over the skill folder / MET
- I2 CLAIM: state across task boundaries / EVIDENCE: F3 Task 10 `classifier_inputs.py` names `follow_ups`; F6 Task 10 reuses Task 7 / MET
- I3 CLAIM: guard conditions / EVIDENCE: F1 Task 5 grep `.dev/` as guard on Task 3 content; F5 same / MET
- I4 CLAIM: count divergence / EVIDENCE: Checked "7 Medium-blocking lines", "14 worked cases", "11 files ... match the 11 digest rows" (the "9 subcommands" count is wrong) / MET
- I5 CLAIM: interaction effects / EVIDENCE: F1 Task 3 vs Task 5 vs T4; Checked "`test_review_cli.py:47` checks only four subcommand names" / MET

## Subtotals (criteria MET)

| Dimension | V3 | V2 | V1 |
|---|---|---|---|
| Completeness | 3/5 | 3/5 | 3/5 |
| Correctness | 3/5 | 5/5 | 3/5 |
| Structure | 5/5 | 5/5 | 5/5 |
| Clarity | 2/5 | 4/5 | 2/5 |
| Risk coverage | 3/5 | 3/5 | 4/5 |
| Invariant and edge-case | 5/5 | 1/5 | 5/5 |
| **Total** | **21/30** | **21/30** | **22/30** |
| **qual_score** | **0.700** | **0.700** | **0.733** |

## Edge-case floor check

Invariant and edge-case dimension: V3 5/5, V2 1/5, V1 5/5. Floor is "below 1 of 5 is ineligible": V2 scores exactly 1, so no variant is ineligible as base. No warning needed (not all score 0).

## Combined scores and ranking

combined = 0.5 quant + 0.5 qual.

| Rank | Variant | quant | qual | combined |
|---|---|---|---|---|
| 1 | V1 (analyzer) | 0.9168 | 0.7333 | **0.8251** |
| 2 | V2 (qa) | 0.7893 | 0.7000 | **0.7446** |
| 3 | V3 (refactorer) | 0.7424 | 0.7000 | **0.7212** |

Top two within 5 percent: no. V1 leads V2 by 0.081 (about 10.8 percent relative, 8.1 points absolute). V2 and V3 are 0.024 apart.

Notes for the merge: V1 is the strongest base because it alone raises C-003, C-005 and C-007 and covers all 6 verified defects; fold in V1 with these corrections from the debate: drop F5, drop the verify-sync half of F3, correct F4's "only through Task 9" wording (Task 12 depends on Tasks 7, 9, 10), grade F2 non-blocking, and replace "9 review subcommands" with 7 (INV-005). Take from V3 the `__pycache__` point and the OD10/source.md:17 support for C-001 and C-002. Take from V2 the C-004 mapping-decision gap, graded non-blocking.
