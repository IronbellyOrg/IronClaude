## Anti-Omission Report

**Report reviewed:** `.dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/RESEARCH-REPORT-review-panel-unification.md` (4283 lines)
**Input files checked:** `research/web-01-panel-aggregation.md`, `research/web-02-severity-harmonization.md`, `research/web-03-judge-calibration.md`, `research/web-04-finding-fingerprinting.md`, `synthesis/synth-05-recommendation-architecture.md`, `synthesis/synth-06-value-migration-plan.md`, `synthesis/synth-07-questions-evidence.md`, `gaps-and-questions.md`, `research/scope/04-this-session-artifacts.md`, `research/scope/05-master-loop-and-consumers.md`; 345 numbered enumeration positions (see Summary)
**Date:** 2026-11-14
**Agent:** anti-omission agent 4 of 4 (fix_authorization: false; report only)

Method: each input file was read in full; every distinct finding, claim, rule, recommendation, lesson, decision, inventory row, migration step, gate, branch option, risk, open question and gap was enumerated; coverage was judged by meaning in the final report (not by ID). Report-gate and fidelity-gate corrections count as represented when the report states the correction.

---

## Enumeration (written incrementally, one input file at a time)

Status key: REPRESENTED (cite where) | OMITTED | COVERED-BY-DEDUP. Report locations are report section numbers (Section 5 = external research; 8.1 = value inventory).

### File 1: research/web-01-panel-aggregation.md

| # | Source finding | Source file | Status | Where in report or deduped into |
|---|---|---|---|---|
| 1 | 1.1 Union ("any flags") 82.7% recall / 85.0% FPR vs weighted 37.7% / 35.3% | web-01 | REPRESENTED | 5.1.1 row 1; 5.5.1 #1 |
| 2 | 1.2 Cross-judge majority and calibrated weighted voting (simulation-only) | web-01 | REPRESENTED | 5.1.1 row 2; 5.1.5 opt 4 |
| 3 | 1.3 Self-Agg n=10 recall gain, F1 stays ~22%, plateau 5-10 runs | web-01 | REPRESENTED | 5.1.1 row 3 |
| 4 | 1.4 Agreeableness: TPR>96%/TNR<25%, minority veto n=4, missing-vote handling | web-01 | REPRESENTED | 5.1.1 row 4; 5.5.1 #5 |
| 5 | 1.5 LLM reviewers over-reject; symptom 98.2% vs cause 59.1% | web-01 | REPRESENTED | 5.1.1 row 5 |
| 6 | 2.1 PoLL panel beats single large judge | web-01 | REPRESENTED | 5.3.1 row 1 |
| 7 | 2.2 Nine Judges ~2 effective votes; best single >= panel | web-01 | REPRESENTED | 5.3.1 row 2; 5.3.5; 5.5.2 #1 |
| 8 | 2.3 Self-preference (GPT-4 0.520; LinkedIn 20x claim unverified) | web-01 | REPRESENTED | 5.3.2 GPT-4 row; 5.5.3 |
| 9 | 2.4 Debate amplifies bias; meta-judge more resistant | web-01 | REPRESENTED | 5.3.1 row 4 |
| 10 | 3.1 Cursor Bugbot pipeline | web-01 | REPRESENTED | 5.1.2 row 1 |
| 11 | 3.2 Cloudflare coordinator and approval bias | web-01 | REPRESENTED | 5.1.2 row 2 |
| 12 | 3.3 LinkedIn overlap = confidence, singletons verified | web-01 | REPRESENTED | 5.1.2 row 3 |
| 13 | 3.4 Zenodo 56.8% single-model defects; second reviewer biggest step | web-01 | REPRESENTED | 5.1.2 row 4; 5.5.1 #3 |
| 14 | 3.5 Recall-oriented aggregation; 93.4% figure unverified | web-01 | REPRESENTED | 5.1.2 row 5; 5.5.3 |
| 15 | 3.6 Mozilla.ai Star Chamber and Ellipsis | web-01 | REPRESENTED | 5.1.2 row 6; 5.5.2 #8 |
| 16 | 3.7 Inference: singleton handling depends on independence | web-01 | REPRESENTED | 5.1.4 row 1; 5.5.2 #3 |
| 17 | 4.1 Common dedup shape; verifier severity overrides finder | web-01 | REPRESENTED | 5.1.3 row 1; 5.1.5 opt 5 |
| 18 | 4.2 Embedding-based dedup (fallback only) | web-01 | REPRESENTED | 5.1.3 row 2 |
| 19 | 4.3 Gaps: no clustering error data; no spec/tasklist panel study | web-01 | REPRESENTED | 5.1.4; 5.5.4 |
| 20 | Discrepancy: `confidence` only partly "unused" (display-only) | web-01 | REPRESENTED | 5.1.4; 5.5.2 #6 |
| 21 | Discrepancy: reflect DEGRADED on 1 reviewer vs ledger PASS on 1 valid reviewer | web-01 | REPRESENTED | 5.1.4 |
| 22 | Rec 1 split candidate from blocking | web-01 | REPRESENTED | 5.1.5 opt 1; 5.5.5 #1 |
| 23 | Rec 2 no hard quorum; overlap as routing; wire `confidence` | web-01 | REPRESENTED | 5.1.5 opt 2 |
| 24 | Rec 3 blind adjudicator not debate; measure TNR; panel vs best single | web-01 | REPRESENTED | 5.3.5 row 2; 5.3.6 opt 4; 5.5.5 #5 |
| 25 | Rec 4 invalid block = abstention; PASS needs >= 2 valid reviewers | web-01 | REPRESENTED | 5.1.5 opt 3; 5.5.5 #3 |
| 26 | Rec 5 tune thresholds on human labels; weights later | web-01 | REPRESENTED | 5.1.5 opt 4 |
| 27 | Rec 6 typed-field dedup, keep reviewer ids, cross-round dedup | web-01 | REPRESENTED | 5.1.5 opt 5 |
| 28 | Rec 7 state verdict bias; log blockers dropped | web-01 | REPRESENTED | 5.1.5 opt 6; 5.5.5 #7 |
| 29 | Rec 8 measure outcome not volume | web-01 | REPRESENTED | 5.1.5 opt 7 |
| 30 | Rec 9 3 heterogeneous reviewers + 1 adjudicator | web-01 | REPRESENTED | 5.1.5 opt 8 |

### File 2: research/web-02-severity-harmonization.md

| # | Source finding | Source file | Status | Where in report or deduped into |
|---|---|---|---|---|
| 31 | 1.1 SARIF `level` values, `kind`/`none` | web-02 | REPRESENTED | 5.2.1 row 1 |
| 32 | 1.2 SARIF `rank` 0-100, no cut points | web-02 | REPRESENTED | 5.2.1 row 2 |
| 33 | 2 GitHub security-severity, precision, problem.severity, gate as repo policy | web-02 | REPRESENTED | 5.2.1 row 3 (sub-details not carried: 75th-percentile CVSS derivation, 0.0 = no severity, defaultConfiguration.level default; MINOR, see Omissions #1) |
| 34 | Auggie demotion on low confidence vs GitHub precision beside severity | web-02 | REPRESENTED | 5.2.1 row 3; 5.2.5 opt 4 |
| 35 | 3.1 GitLab resolution order, buckets, `error` read as High | web-02 | REPRESENTED | 5.2.1 row 4 |
| 36 | 3.2 DefectDojo / Perforce QAC / DEV-post mappings | web-02 | REPRESENTED | 5.2.1 row 5 |
| 37 | 4.1 CodeQL two scales, consequence definitions, precision | web-02 | REPRESENTED | 5.2.2 row 1 |
| 38 | 4.2 Semgrep alias migration; impact x likelihood; confidence about rule | web-02 | REPRESENTED | 5.2.2 row 2 |
| 39 | 5.1 Google Nit/Optional/FYI; unlabelled = mandatory; archive claim UNVERIFIED | web-02 | REPRESENTED | 5.2.2 row 3; 5.5.3 |
| 40 | 5.2 Conventional Comments (blocking)/(non-blocking)/(if-minor); category floors | web-02 | REPRESENTED | 5.2.2 row 4 |
| 41 | 6.1 SonarQube legacy to MQR mapping and staff regret | web-02 | REPRESENTED | 5.2.2 row 5; 5.2.4 |
| 42 | 6.2 CodeRabbit severities, category badge, Quiet profile | web-02 | REPRESENTED | 5.2.2 row 6 |
| 43 | 6.3 P0-P3 are priority; Codex definitions UNVERIFIED | web-02 | REPRESENTED | 5.2.2 row 7; 5.5.3 |
| 44 | 6.4 OWASP matrix with Note floor | web-02 | REPRESENTED | 5.2.2 row 8 |
| 45 | 6.5 Cross-tool equivalence table | web-02 | REPRESENTED | 5.2.3 table |
| 46 | 7.1 SARIF property-bag guidance; sarif-tools #43 | web-02 | REPRESENTED | 5.2.1 row 6 |
| 47 | 7.2 Strategies S1-S7 | web-02 | REPRESENTED | 5.2.3 strategies table |
| 48 | 7.3 5-to-3 collapse not invertible; router routes align with error/warning/note | web-02 | REPRESENTED | 5.2.3 collapse paragraph |
| 49 | 8 rows 1-19 mapping of our vocabularies | web-02 | REPRESENTED (loss points) | 5.2.3 loss table; per-row proposals flagged in 5.5.3. Row 13 (rf-qa synthetic-dnsp HIGH) is carried in 7.2 (severity-mapping row) and inventory row for the rf-qa vocabulary; verified by search for "synthetic-dnsp" |
| 50 | Rec 1 five-tier core, SARIF export, rank | web-02 | REPRESENTED | 5.2.5 opt 1 |
| 51 | Rec 2 blocking separate, per consumer | web-02 | REPRESENTED | 5.2.5 opt 2 |
| 52 | Rec 3 `medium` first-class; fix card_convert collapse | web-02 | REPRESENTED | 5.2.5 opt 3 |
| 53 | Rec 4 five fields; confidence not folded into severity | web-02 | REPRESENTED | 5.2.5 opt 4 |
| 54 | Rec 5 one consequence sentence per tier | web-02 | REPRESENTED | 5.2.5 opt 5 |
| 55 | Rec 6 deviation classes / advisory as non-severity | web-02 | REPRESENTED | 5.2.5 opt 6 |
| 56 | Rec 7 versioned alias table; keep extremes | web-02 | REPRESENTED | 5.2.5 opt 7 |
| 57 | Rec 8 own rank cut points and category rule for export | web-02 | REPRESENTED | 5.2.5 opt 8 |
| 58 | Rec 9 P0-P3 priority hint; confirm Codex definitions | web-02 | REPRESENTED | 5.2.5 opt 9 |
| 59 | Gaps: GitLab rank table; snippet-only; no validated 3-to-5 algorithm | web-02 | REPRESENTED | 5.2.4; 5.5.4 |

### File 3: research/web-03-judge-calibration.md

| # | Source finding | Source file | Status | Where in report or deduped into |
|---|---|---|---|---|
| 60 | 1.1 Self-recognition / self-preference (Panickssery) | web-03 | REPRESENTED | 5.3.2 row 1 |
| 61 | 1.2 Reanalysis: 89.6% explained by uncertainty | web-03 | REPRESENTED | 5.3.2 row 2; 5.3.5 |
| 62 | 1.3 Perplexity-based self-preference | web-03 | REPRESENTED | 5.3.2 row 3 |
| 63 | 1.4 Filename/author-label bias; E2 combo-name leak | web-03 | REPRESENTED | 5.3.2 row 5 |
| 64 | 1.5 Identity-bias guidance; blinded-vs-unblinded metric | web-03 | REPRESENTED | 5.3.2 row 6 |
| 65 | 2.1 MT-Bench biases; reference-guided judging | web-03 | REPRESENTED | 5.3.2 row 7 |
| 66 | 2.2 CALM 12 biases; bias injection | web-03 | REPRESENTED | 5.3.2 row 8 |
| 67 | 2.3 Rubric-order position bias; freeze content, permute presentation | web-03 | REPRESENTED | 5.3.2 row 9 |
| 68 | 2.4 21-judge verbosity figure (UNVERIFIED) | web-03 | REPRESENTED (excluded) | 5.3.5 last row; 5.5.3 |
| 69 | 2.5 EACL code-judge surface-feature bias | web-03 | REPRESENTED | 5.3.2 row 10 |
| 70 | 3.1 PoLL vs single blind Opus judge; agreement as calibrator | web-03 | REPRESENTED | 5.3.1 row 1 |
| 71 | 3.2 Practitioner judge-ensemble guidance | web-03 | REPRESENTED | 5.3.1 row 6 |
| 72 | 4.1 Rubric-guided scoring ICC; held-out calibration | web-03 | REPRESENTED | 5.3.3 row 1 |
| 73 | 4.2 Rubric-in-prompt did not help (LOW) | web-03 | REPRESENTED | 5.3.3 row 2 |
| 74 | 4.3 RULERS evidence gate | web-03 | REPRESENTED | 5.3.3 row 3 |
| 75 | 4.4 Blind vs informed: evidence gap | web-03 | REPRESENTED | 5.3.3 row 4 |
| 76 | 5.1 Xiong verbalized confidence AUROC 62.7% | web-03 | REPRESENTED | 5.3.3 row 5 |
| 77 | 5.2 Tian "Just Ask for Calibration" | web-03 | REPRESENTED | 5.3.3 row 6 |
| 78 | 5.3 Ownership bias up to 26% | web-03 | REPRESENTED | 5.3.3 row 7 |
| 79 | 5.4 Overconfidence; LLM-as-a-Fuser +47.14% | web-03 | REPRESENTED | 5.3.1 row 5 |
| 80 | 5.5 Top-skewed confidence; per-model thresholds | web-03 | REPRESENTED | 5.3.3 row 8 |
| 81 | 5.6 Confidence vs annotator agreement; escalate to human | web-03 | REPRESENTED | 5.3.3 row 9 |
| 82 | 6.1 Platt/isotonic calibrators; staleness | web-03 | REPRESENTED | 5.3.4 row 1 |
| 83 | 6.2 Claim-level verification, same-family correlated error | web-03 | REPRESENTED | 5.3.1 row 7 |
| 84 | 6.3 Apollo vendor-level diversity; per-model severity offsets | web-03 | REPRESENTED | 5.3.1 row 3 |
| 85 | 6.4 Confidence filters; audit sample | web-03 | REPRESENTED | 5.3.4 row 2 |
| 86 | 6.5 Evidence gap: no defect-finding panel study | web-03 | REPRESENTED | 5.3.4 row 3; 5.5.4 |
| 87 | Recs 1-8 | web-03 | REPRESENTED | 5.3.6 opt 1-8; 5.5.5 #5 |
| 88 | Discrepancies (a) class vs vendor, (b) E2 schema leak, (c) confidence studies disagree | web-03 | REPRESENTED | 5.5.2 #4, #7; 5.3.2 row 5; 5.3.5 |
| 89 | Context slip "shadow runs 0 of 689" | web-03 | REPRESENTED (corrected) | 5.3 preface states 0/689 is legacy, shadow 142/142 |

### File 4: research/web-04-finding-fingerprinting.md

| # | Source finding | Source file | Status | Where in report or deduped into |
|---|---|---|---|---|
| 90 | F1 SARIF fingerprints / partialFingerprints / correlationGuid | web-04 | REPRESENTED | 5.4.1 row 1 |
| 91 | F2 Logical location more resilient; v2 empty section contradicts | web-04 | REPRESENTED | 5.4.1 row 1 |
| 92 | A1 GitHub matching via primaryLocationLineHash + ruleId + path | web-04 | REPRESENTED | 5.4.1 row 2 |
| 93 | A2 Empty hash degrades to order matching | web-04 | REPRESENTED | 5.4.1 row 3 |
| 94 | A3 Alerts shown only if all lines in diff; in_diff out of key | web-04 | REPRESENTED | 5.4.1 row 4 |
| 95 | H1 CodeQL rolling 100-char hash, `:n` suffix | web-04 | REPRESENTED | 5.4.1 row 5 |
| 96 | H2 SARIF region/snippet/contextRegion; limits | web-04 | REPRESENTED | 5.4.1 row 6 |
| 97 | H3 DefectDojo SARIF fingerprint vs hash; 5 locations = 5 findings | web-04 | REPRESENTED | 5.4.1 row 7 |
| 98 | S1 SonarQube ordered match rules | web-04 | REPRESENTED | 5.4.1 row 8 |
| 99 | M1 DefectDojo per-tool identity; no merge on empty location | web-04 | REPRESENTED | 5.4.2 row 1 |
| 100 | M2 Merging multi-tool SARIF; stable tool names | web-04 | REPRESENTED | 5.4.2 row 2 |
| 101 | M3 DefectDojo track-as-location-changes | web-04 | REPRESENTED | 5.4.2 row 3 |
| 102 | P1 GitHub review-comment location model; Outdated | web-04 | REPRESENTED | 5.4.2 row 4 |
| 103 | C1 Single-linkage chaining; complete linkage | web-04 | REPRESENTED | 5.4.3 row 1 |
| 104 | C2 ER literature; 64% closure precision; black-hole threshold; Center | web-04 | REPRESENTED | 5.4.3 row 2 |
| 105 | C3 Size cap (VL-Dedup), snippet-only | web-04 | REPRESENTED | 5.4.3 row 3; 5.5.3 |
| 106 | X1 Semgrep two fingerprints; index after hash; deterministic representative | web-04 | REPRESENTED | 5.4.1 row 9 |
| 107 | X2 GitLab scope + offset; run-varying ids break tracking | web-04 | REPRESENTED | 5.4.1 row 10 |
| 108 | X3 Code Climate default fingerprint; occurrence suffix | web-04 | REPRESENTED | 5.4.1 row 11 |
| 109 | D1 LinkedIn / Cloudflare central dedup | web-04 | REPRESENTED | 5.4.2 row 5 |
| 110 | D2 Practitioner rules: location + defect shape; root-cause link | web-04 | REPRESENTED | 5.4.2 row 6; 5.4.4 |
| 111 | R1-R10 recommendations | web-04 | REPRESENTED | 5.4.5; 5.5.5 #6 |
| 112 | Caveats: no category gate in codebase key; low-reliability sources | web-04 | REPRESENTED | 5.4.4; 5.4.2 row 4 |

### File 5: synthesis/synth-05-recommendation-architecture.md (report Section 7)

Method note: synth-05 was assembled into report Section 7. Coverage was tested by meaning, not by ID: every table row's first cell and every prose paragraph were searched in the report as text, and each non-identical row was compared by length and content with its report counterpart. Of 150 table rows, 133 are byte-identical in the report and 17 differ; none of the 17 is shorter in substance (they carry later gate corrections, for example the grader class-disjoint wording in Rationale 7, the `anthropic-only` fallback wording at report line 2834, and the `KeyError` wording at line 2835).

| # | Source finding | Source file | Status | Where in report or deduped into |
|---|---|---|---|---|
| 113 | Header facts: effort tags, verification marks, track labels, citation form and 2026-11-14 spot-check list | synth-05 | REPRESENTED | Section 7 "Conventions used in Section 7" table |
| 114 | Known-contradicted claims not built on (variants only in bundle; audits B/C/E/F; "4 verdicts flipped"; alias GT3; D7/D11/D12 lines; `merge_round` docstring) | synth-05 | REPRESENTED | Section 7 intro paragraph |
| 115 | Corrected parsed-sparse figure (35 of 39 flag set, decisive in 0 certain / at most 1; 29 of 34 with escalate row) | synth-05 | REPRESENTED | Section 7 "One figure corrected here"; 8.1 V-673 |
| 116 | Recommended approach: Option B built through Option A's code; Option C rejected | synth-05 | REPRESENTED | Section 7 Recommended approach |
| 117-123 | Rationale 1 to 7 (options comparison; A is B's first stage; core vs module split; decided vs debate-resolved conflicts; thin quality evidence; default panel size and Step A/B/C; cost trade-offs) | synth-05 | REPRESENTED | Section 7 Rationale 1-7 (Rationale 7 reworded by a later gate) |
| 124-143 | Conflict resolutions C-01 to C-20 as adopted (20 rows) | synth-05 | REPRESENTED | Section 7 "Conflict resolutions adopted" table |
| 144-147 | Open design risks of the four partial debates C-03, C-05, C-13, C-14 (4 rows, invariants, owner decisions, assumptions) | synth-05 | REPRESENTED | Section 7 open-risk table |
| 148-153 | External context rows (finder/coordinator, union vs weighted, panel independence, severity interchange, finding identity, judge calibration) | synth-05 | REPRESENTED | Section 7 "External context used" table |
| 154-169 | Core components 7.1.3 (16): finding contract; severity scale and mapping; panel resolution; identity check; dispatch; brief and grounding; run manifest; telemetry; clustering; citation checks; calibration; blocking decider hook; round model; merge and verdict (with the [CONTRADICTION] on verdict vocabulary); built-in run audits; rollout and evaluation instrument | synth-05 | REPRESENTED | Section 7.1.3 (16 rows) |
| 170 | 7.1.1 layer diagram and 7.1.2 data-flow diagram | synth-05 | REPRESENTED | Section 7.1.1 and 7.1.2 |
| 171-176 | Thin modules 7.1.4 (6): reflect UC-1; reflect UC-2 incl. code-driven engine; workflow/tasklist; spec review brainstorm/design/spec-panel; PR code review; rf-qa replacement | synth-05 | REPRESENTED | Section 7.1.4 (6 rows) |
| 177-198 | Exposure list 7.2 (22 rows): lenses; categories; roles; templates/kinds; model-role/strata; severity mapping; blocking predicate; four location kinds; multi-artifact; clustering key; brief slots; rubric/grader; fix-agent hand-off; verdict format; provenance; verification gate; finder adapters; run-record profile; CLI reachability | synth-05 | REPRESENTED | Section 7.2 |
| 199-233 | Blockers in today's designs 7.3 (35 rows, from "resolution is not what runs" to "five spec-panel variants are full forks") | synth-05 | REPRESENTED | Section 7.3 (the "Gateway environment" and "Merge path is v1-only" rows were reworded by later gates, content kept) |
| 234-246 | What stays unchanged 7.4.1 (13 constraints: contract 1.8.0, merge_method set, wrapper semantics, C5/C11/C12, reflect text pins, code-driven caller, ledger surface, v1 lines valid, seven-bullet loop, read-only reviewers, dated facts, E2 commit, repository rules) | synth-05 | REPRESENTED | Section 7.4.1 |
| 247-260 | Findings not carried 7.4.2 (14 exclusions with rationale) | synth-05 | REPRESENTED | Section 7.4.2 |
| 261-263 | 7.4.3 consistency notes: nothing overridden; superseded synth-04 sentences corrected; one [CONTRADICTION]; corrections to inherited wording; items needing an owner before Section 8 | synth-05 | REPRESENTED | Section 7.4.3 (owner-item list also carried in 8.5 and 8.6 and Q-47 to Q-61) |

### File 6: synthesis/synth-06-value-migration-plan.md (report Section 8)

Method note: tested by meaning. All 691 inventory rows V-001 to V-691 exist in the report (691 of 691 by row count), and each row's item text (first 45 characters) was searched in the report: 686 found verbatim; the 5 that differ are V-029 (rewritten to state 106 scored runs, 71 valid-era rows, 665 reviewer runs), V-042 (carried), V-224 and V-616 (docstring wording corrected to `findings_v2.py:3-5`), V-362 (carried). Of 912 table rows in synth-06 (inventory, steps, gap coverage, gates, branch options, risks), 849 are byte-identical in the report and 63 differ; none is materially shorter.

| # | Source finding | Source file | Status | Where in report or deduped into |
|---|---|---|---|---|
| 264 | 8 intro: owner scope (not a roadmap) and five binding facts (four partial debates with HIGH-invariant counts; [CONTRADICTION]; parsed-sparse correction; E2 commit; known-contradicted claims) | synth-06 | REPRESENTED | Section 8 intro |
| 265 | 8.1 method note and abbreviation/destination tables | synth-06 | REPRESENTED | Section 8.1 header tables |
| 266 | V-001 to V-024: product artifacts, E2 artifacts, scripts (findings.py, ledger, panel, telemetry, packaged data, loop prompt, tests, PILOT/COMBO reports, SPEC, manifest, audits A-F, tables, scripts, transcripts, run data, GT packages, runner, judge, anon scripts, unreferenced scripts) | synth-06 | REPRESENTED | 8.1 rows V-001 to V-024 |
| 267 | V-025 to V-064: E2 study design, metrics, eras, scale, results R1-R6, model roles, harness incidents, audits A-F findings, "not shown" items | synth-06 | REPRESENTED | 8.1 rows V-025 to V-064 |
| 268 | V-065 to V-080: hand-off defects D1-D16 | synth-06 | REPRESENTED | 8.1 rows V-065 to V-080 |
| 269 | V-081 to V-090+: E2 lessons (worked, failed, do differently) and decisions | synth-06 | REPRESENTED | 8.1 rows V-081 onward |
| 270 | V-091 to V-311: remaining hand-off, scope 01/02/03 items, research 01-13 findings, contracts, test pins | synth-06 | REPRESENTED | 8.1 rows (each checked by item text) |
| 271 | V-312 to V-411: all of scope slice 04 (see File 9 for item-by-item mapping) | synth-06 | REPRESENTED | 8.1 rows V-312 to V-411 |
| 272 | V-412 to V-468: all of scope slice 05 (see File 10) | synth-06 | REPRESENTED | 8.1 rows V-412 to V-468 |
| 273 | V-469 to V-691: research 01-13 findings, web findings, closed items GQ:C-01 to C-25 and stale-doc rows GQ:D-01 to D-77 | synth-06 | REPRESENTED | 8.1 rows; D-nn rows V-615 to V-691 |
| 274 | 8.2 Track M1 steps M1-01 to M1-19 (19 steps with files, details, closes-gaps) | synth-06 | REPRESENTED | Section 8.2 Track M1 (M1-10 reworded slightly, content kept) |
| 275 | 8.2 Track M2 steps M2-01 to M2-10 | synth-06 | REPRESENTED | Section 8.2 Track M2 |
| 276 | 8.2 Track M3 steps M3-01 to M3-09 | synth-06 | REPRESENTED | Section 8.2 Track M3 |
| 277 | 8.2 Track M4 steps M4-01 to M4-07 | synth-06 | REPRESENTED | Section 8.2 Track M4 |
| 278 | Track goals and dependencies for M1-M4 | synth-06 | REPRESENTED | Section 8.2 Goal and Dependencies lines (verified by phrase search) |
| 279 | Gap coverage table A: 15 Critical and 65 Important synth-02 gaps mapped to steps or DROP (80 rows) | synth-06 | REPRESENTED | Section 8.2 Gap coverage |
| 280 | Gap coverage table B: 30 open Important gaps of gaps-and-questions mapped to steps or DROP | synth-06 | REPRESENTED | Section 8.2 Gap coverage (second table) |
| 281 | 8.3 gates G1-G11, G-all, G-exit, G-replay, G-sync, G-bench, G-new (17 gates with command, guard, must-change-on-purpose) | synth-06 | REPRESENTED | Section 8.3 |
| 282 | 8.4 git branch-name constraint, shaping facts, options A-E | synth-06 | REPRESENTED | Section 8.4 |
| 283 | 8.5 risk register inputs (24 risks with source, likelihood, impact, mitigation) | synth-06 | REPRESENTED | Section 8.5 |
| 284 | 8.6 integration checklist (16 items) | synth-06 | REPRESENTED | Section 8.6 (items extended by later gates, e.g. SC-18 to SC-23) |

### File 7: synthesis/synth-07-questions-evidence.md (report Sections 9 and 10)

Method note: tested by meaning. 263 table rows; 255 byte-identical in the report, 8 differ. The 8 are: D-02 and D-59 (wording corrected by later gates, content kept in the 9.4 register), the "(this file)" row of the evidence trail, and 5 other rows that differ in later-added gate content (none is shorter than its synthesis row). The report has 122 Q rows against 114 in synth-07 (Q-58 onward were added by the QA gates).

| # | Source finding | Source file | Status | Where in report or deduped into |
|---|---|---|---|---|
| 285 | Header: severity statement (no Critical gap, 30 Important all carried, 64 Minor carried), row labels, source key | synth-07 | REPRESENTED | Section 9 intro (verified by phrase search) |
| 286 | Q-01 to Q-06 owner items O-1 to O-6 | synth-07 | REPRESENTED | Section 9 Q-01 to Q-06 |
| 287 | Q-07 to Q-30 Important gaps (24 rows) | synth-07 | REPRESENTED | Section 9 Q-07 to Q-30 |
| 288 | Q-31 to Q-44 Minor-group rows (14 rows naming each Minor gap) | synth-07 | REPRESENTED | Section 9 Q-31 to Q-44 |
| 289 | Q-45 and Q-46 web UNVERIFIED items and web evidence gap | synth-07 | REPRESENTED | Section 9 Q-45, Q-46 |
| 290 | Q-47 to Q-57 debate and QA-gate decisions | synth-07 | REPRESENTED | Section 9.5 |
| 291 | 9.1 gap coverage index (every G-nn once; every Q row once) | synth-07 | REPRESENTED | Section 9.1 |
| 292 | 9.2 [UNVERIFIED] and [CODE-CONTRADICTED] claims carried as open questions | synth-07 | REPRESENTED | Section 9.2 |
| 293 | 9.3 closed items C-01 to C-25 | synth-07 | REPRESENTED | Section 9.3 (25 rows) |
| 294 | 9.4 D-01 to D-77 register (settled or open per row) | synth-07 | REPRESENTED | Section 9.4 |
| 295 | 10 Evidence trail: codebase research (13), web research (4), synthesis files (7), scope inputs (7), debate outputs (4), QA reports, gaps log | synth-07 | REPRESENTED | Section 10 (all subsections present) |

### File 8: gaps-and-questions.md

Method note: every G-nn, D-nn, C-nn and O-n was searched in the report (all 94 G ids, 77 D ids, 25 closed items, 6 owner items found; closed items C-01 to C-25 each have their own row in 9.3). Meaning-level coverage of the 94 gaps is through Section 9 rows Q-01 to Q-44 and the 8.1 inventory.

| # | Source finding | Source file | Status | Where in report or deduped into |
|---|---|---|---|---|
| 296 | Section 1: gaps G-01 to G-94 (30 Important, 64 Minor, no Critical) | gaps-and-questions | REPRESENTED | 9.1 index maps each G to a Q row; Important ones are own rows Q-07 to Q-30 |
| 297 | Section 2: contradicted and stale-doc rows D-01 to D-77 (CC, SD, QN) | gaps-and-questions | REPRESENTED | 9.4 register; V-615 to V-691 |
| 298 | Section 3: owner items O-1 to O-6 | gaps-and-questions | REPRESENTED | Q-01 to Q-06 |
| 299 | Section 3 closing list of Important owner-type gaps (G-01, 03, 04, 05, 06, 11, 12, 18, 20, 46, 66, 78, 87) | gaps-and-questions | REPRESENTED | Q-08, Q-10 to Q-14, Q-16 to Q-19, Q-23, Q-28, Q-29, Q-30 |
| 300 | Section 4: closed items C-01 to C-25 | gaps-and-questions | REPRESENTED | 9.3 |
| 301 | Section 5 counts (94/77/6/25; effort, closure, type splits) | gaps-and-questions | REPRESENTED (in substance) | 9.1 header text and Section 10 Gaps Log line state 94 / 77 / 6 / 25; the effort/closure/type split counts are not repeated (MINOR note in Omissions #4) |
| 302 | Research gate verdict (PASS after 2 fix cycles plus 1 extra fix) and E2-commit rule | gaps-and-questions | REPRESENTED | Section 10 Gaps Log |

### File 9: research/scope/04-this-session-artifacts.md

Method note: scope-slice items count as represented when they have an inventory row with a destination or a DROP reason (executor note 2). Each item below was mapped to its inventory row by text, then confirmed by reading the row.

| # | Source finding | Source file | Status | Where in report or deduped into |
|---|---|---|---|---|
| 303 | F-1 legacy card conversion 67.28% (479/712) | scope/04 | REPRESENTED | V-328; V-386 |
| 304 | F-2 compliance 0.704 over 9 shadow runs under findings-v2 brief | scope/04 | REPRESENTED | V-362 |
| 305 | F-3 combo compliance 1.0 B/C/D, 0.67 in A | scope/04 | REPRESENTED | V-363 |
| 306 | F-4 cluster_v2 precision 0.84 / recall 0.95 (AI labels) | scope/04 | REPRESENTED | V-335; Q-05 |
| 307 | F-5 6.70% agreement with recorded merged verdicts | scope/04 | REPRESENTED (DROP as correctness measure) | V-330; 9.3 C-08 |
| 308 | F-6 0 of 689 numeric calibrations | scope/04 | REPRESENTED | V-332; Calibration component |
| 309 | F-7 8 null convergence scores, 4 illegal `merge_method` values | scope/04 | REPRESENTED | V-331 |
| 310 | F-8 parity failure root causes | scope/04 | REPRESENTED | V-342 |
| 311 | F-9 EV-1 root cause (no step writes merged-verdict.yaml) | scope/04 | REPRESENTED | V-343; M2-02 |
| 312 | F-10 compliance root cause (brief had no schema) | scope/04 | REPRESENTED | V-344 |
| 313 | F-11 dispatch collapse to sonnet alias | scope/04 | REPRESENTED | V-347; Dispatch component |
| 314 | F-12 "haiku" slot served by gpt-6.1-sol; pins honoured 2/3 | scope/04 | REPRESENTED | V-336; V-400 |
| 315 | F-13 record shows class not served model; self-reports 0/3 | scope/04 | REPRESENTED | V-336; Identity check |
| 316 | F-14 / F-15 combo speed and confidence leads | scope/04 | REPRESENTED (DROP as unscored) | V-352; V-364 |
| 317 | F-16 combo counts overlap; no blind GT scoring | scope/04 | REPRESENTED | V-365; V-395 |
| 318 | F-17 shadow measures side signals, not quality | scope/04 | REPRESENTED | V-337 |
| 319 | F-18 Stage 2 exit FAIL (13 of 20) | scope/04 | REPRESENTED | V-353; V-393 |
| 320 | F-19 37 of 38 pre runs escalate; parsed-sparse | scope/04 | REPRESENTED (corrected) | V-366; Section 7 corrected-figure note |
| 321 | F-20 PN1 spec-panel gain came from a revise loop | scope/04 | REPRESENTED (DROP) | V-315 |
| 322 | F-21 cluster_v2 weaknesses W-1 to W-4 | scope/04 | REPRESENTED | V-334 |
| 323 | F-22 executor class unknown 9 of 9 | scope/04 | REPRESENTED | V-353; MR open item O-6 (unknown executor in workflow path) in V-322 |
| 324 | F-23 seven final-review rounds, prose convergence | scope/04 | REPRESENTED | V-341; V-380 |
| 325 | Lessons (14): shadow mode; manifest freeze; exit script; stop rule; thresholds table; blind AI labelling; adversarial debates; zero-dispatch replay; gate redefinition; observed identity; chain-of-single-changes; BG_WAIT_CEILING; user-level install; remove claims; telemetry-not-routing | scope/04 | REPRESENTED | V-367 to V-381 (15 rows) |
| 326 | Decisions made (11): architecture C; reject B / defer E'; cap 3; ledger not used; T-9 redefined; pilot arm C; observed identity; calibration_coverage; shadow extraction deferred; AI labels; archive after review 7; combo runs outside .dev/reflect | scope/04 | REPRESENTED | V-382 to V-391 (combo-runs convention in V-348) |
| 327 | Open items (11): Stage 0 exit; Stage 2 exit; stop rule/SD-3/ceilings; blind scoring of combo; confirmatory spend; MR sign-off; O-4/O-6/O-8/O-9/O-11; W-1 pair set; calibrator agent file; EV-1 jump cause; orchestrator-drives-dispatch | scope/04 | REPRESENTED | V-392 to V-398 |
| 328 | Overlap section 5 (9 topics: source/spec; identity; reviewer mix; merge; roles tested; ground truth; ceiling; format compliance; gateway availability) | scope/04 | REPRESENTED | V-399 to V-407 |
| 329 | Artifact inventory rows 1-26 (MR, pilot design, stage0a, gate redefinition, pair sheets, AI labels, forms, weaknesses, consumer inventory, lint design, S-ID, shadow evaluation, stage2 inventory, addenda, final reviews, stop-rule files, check logs, TS, PLAN, FINDINGS, shadow runs, exit script, measurement scripts, kernel code, commits) | scope/04 | REPRESENTED | V-312 to V-361 |
| 330 | Section 6 Phase-2 assignments 1-10 | scope/04 | REPRESENTED (DROP with reason: answered by research files) | V-408 |
| 331 | Section 7 gaps and questions (unread files; UNVERIFIED claims; second-hand facts; #525-#530; BG_WAIT rationale; exit-script head; compliance mean 9 vs 13; shadow01-03 reuse; comboC-r3 Makefile; anthropic-only vs gateway; MR draft status) | scope/04 | REPRESENTED | V-409, V-410, V-411 |
| 332 | 0.x reading notes with code spot-checks (kernel modules exist; t2_engine only in manifest files; ROLES/LENSES/CHANNELS; review-tiers tier2 and stand_ins) | scope/04 | REPRESENTED | V-354 |
| 333 | 0.8 candidate consumers of a generic shadow harness (spec-panel loop, troubleshoot, workflow) and UNVERIFIED overlap with sc-cli-eval, eval_runner.py, ab_test_workflows.py | scope/04 | OMITTED (detail) | V-337 and V-408 carry the harness decision and DROP the assignment, but the candidate-consumer list and the unverified overlap check are not recorded; see Omissions #2 |

### File 10: research/scope/05-master-loop-and-consumers.md

| # | Source finding | Source file | Status | Where in report or deduped into |
|---|---|---|---|---|
| 334 | 1A inventory: spec-panel.md, loop prompts file, review CLI, five command variants, installed skills (ledger, stoprule, diffgate, fix-audit), finding-grader, five test files | scope/05 | REPRESENTED | V-412 to V-424; V-006 |
| 335 | Hand-off claim check ("only in bundle" is [CODE-CONTRADICTED, partially]) and final bundle contents | scope/05 | REPRESENTED | V-425; V-426; D-15 in 9.4 |
| 336 | Section 2 loop sequence steps 1 to 8 (resolve; briefs and findings-v1; merge; ledger rounds; revise; record revision; stop rule and exit codes; fallback) | scope/05 | REPRESENTED | V-427 to V-434 |
| 337 | Verify-only does NOT exist on master; experiment profile and blocking predicate; stoprule hands blocking to the grader | scope/05 | REPRESENTED | V-435; V-417; V-419 (CAP_REVIEWS value and "grades outside PROFILES" note not carried: Omissions #3) |
| 338 | Two blocking rules coexist on master | scope/05 | REPRESENTED | V-436; Q-13; C-16 |
| 339 | Plug-in points: workflow Wave 4, tasklist Stage 10.5 and post gate, brainstorm (none), design (none) | scope/05 | REPRESENTED | V-437 to V-441 |
| 340 | Future consumers rf-qa, rf-qa-qualitative, rf-analyst; call sites 19 files/521 lines (corrected to 43 call sites/11 files); pinning tests; rf-qa.md:41 "zero is suspect" | scope/05 | REPRESENTED | V-442 to V-447; V-668 (D-54 correction) |
| 341 | 1D PR review: auggie-review, auggie-prompts, severity-rubric, pr_submit models/router/other modules, pr-submit protocol, evidence-validator, confidence-calibrator | scope/05 | REPRESENTED | V-448 to V-454; V-255; V-256 |
| 342 | Section 3 per-consumer needs and blockers (5 consumers) | scope/05 | REPRESENTED | V-455 to V-459; Section 7.2 and 7.3 |
| 343 | Section 4 severity and finding vocabularies table (12 sources) and reconciliation notes | scope/05 | REPRESENTED | V-460 to V-463 (truth-basis names and evidence-validator status precedence not carried: Omissions #3) |
| 344 | Section 5 Phase-2 assignments 1-9 | scope/05 | REPRESENTED (DROP) | V-464 |
| 345 | Section 6 gaps: installed-only variants; bundle caveat; two blocking rules; "tasklist review in sc:workflow"; no verify-only on master; spec-panel never names CLI; rf-qa wording; Auggie rubric vs router; not-read list; hand-off D8/D9/D14 and questions 1, 7 | scope/05 | REPRESENTED | V-465 to V-468; V-447; Q-01, Q-03, Q-13, Q-18, Q-29; M3-01 |

### Omissions Found

| # | Source finding | Source file | Status (OMITTED / COVERED-BY-DEDUP) | If deduped, by which report item | Severity |
|---|---|---|---|---|---|
| 1 | Sub-details inside represented web-02 rows: GitHub `security-severity` derivation (75th-percentile CVSS of the CWE's CVEs), "0.0 or out-of-range = no security severity", `defaultConfiguration.level` default `warning`; Semgrep Supply Chain severity from CVSS with EPSS shown separately; SonarQube generic-issue import default (Maintainability + Medium); Tweag and colinsalmcorner suite-filter note | web-02 (sections 2, 4.1, 4.2, 6.1) | OMITTED (detail only; the findings themselves are carried in 5.2.1 and 5.2.2) | n/a | MINOR |
| 2 | Candidate consumers of a generic shadow harness (`/sc:spec-panel` loop, `sc-troubleshoot-protocol`, `sc-workflow-protocol`) and the UNVERIFIED overlap of that harness with `sc-cli-eval`, `scripts/eval_runner.py` and `scripts/ab_test_workflows.py` | scope/04 section 0.8 and Phase-2 assignment 7 | OMITTED (V-337 records the harness decision and its trigger; V-408 drops the assignment with the reason "answered"; G-84 covers only the `eval_runner.py` body) | n/a | MINOR |
| 3 | Figure-level details inside represented inventory rows: stage0a citation split (2084 citations, 1801 with path+line); shadow-standalone sizing (~1,700 lines in play, about a third shared, complexity Medium to Large); pair-label ruling label P38 as the only departure from plain majority; experiment `sc-review-ledger` `CAP_REVIEWS = 3` and the note that `status` metrics and the `close` tail name grades outside `PROFILES`; telemetry truth-basis names (catalog-v1, theme-v1, adjudicated-v1); evidence-validator status precedence (failed > blocked > partial > success); `spec-panel-armb.md` found in the bundle only under measurements paths (no `builds/armb`); bundle files `repeat-screen-draft.json` and `provenance/spec-panel-427.md` | scope/04, scope/05 | OMITTED (detail only; every parent item is represented) | n/a | MINOR |
| 4 | gaps-and-questions section 5 effort, closure and type split counts (E1 43 / E2 9 / ..., 44 C1 / 31 C2 / 19 C3, 35 owner decision / 27 unverified / ...) | gaps-and-questions | OMITTED (counts only; totals 94, 77, 6, 25 are stated) | n/a | MINOR |

No item was found OMITTED at CRITICAL or IMPORTANT. No item was found COVERED-BY-DEDUP at a distinct-finding level (the report did not merge distinct findings into one; where it dropped an item it did so as an inventory DROP row with a reason, which counts as represented).

### Summary

**Input files checked:** `research/web-01-panel-aggregation.md`, `research/web-02-severity-harmonization.md`, `research/web-03-judge-calibration.md`, `research/web-04-finding-fingerprinting.md`, `synthesis/synth-05-recommendation-architecture.md`, `synthesis/synth-06-value-migration-plan.md`, `synthesis/synth-07-questions-evidence.md`, `gaps-and-questions.md`, `research/scope/04-this-session-artifacts.md`, `research/scope/05-master-loop-and-consumers.md` (10 files, all read in full).

**Findings enumerated:** 345 numbered positions in this report. Positions 1-112 (the four web files) and 303-345 (scope slices 04 and 05) list items one by one. Positions 113-302 cover the synthesis files and the gaps log; there the large mechanical sets are enumerated as ranges that were each verified item by item: the 691 value-inventory rows and 912 table rows of synth-06 (of which 691 are inventory rows), the 150 table rows of synth-05, the 263 table rows of synth-07, the 94 gaps, the 77 stale-doc rows, the 25 closed items and the 6 owner items. Those sets were checked by searching each row's text in the report (not by ID), plus a length and content comparison of every row that was not byte-identical.

| Measure | Count |
|---|---|
| Numbered enumeration positions | 345 |
| Positions with status OMITTED | 1 (position 333, MINOR) |
| Positions REPRESENTED but with a MINOR detail not carried inside the represented item | 4 (positions 33, 301, 337, 343) |
| All other positions REPRESENTED (including DROP-with-reason rows and items corrected by a later gate) | 340 |
| COVERED-BY-DEDUP | 0 |
| Omissions at CRITICAL | 0 |
| Omissions at IMPORTANT | 0 |
| Omissions at MINOR | 4 notes (never fail) |

Checks that support the verdict: (1) report holds 691 of 691 inventory rows and 122 Q rows against 114 in synth-07; (2) every G, D, C and O id of `gaps-and-questions.md` appears; (3) of 1,325 synthesis table rows, only 88 differ from the report, and none is materially shorter; the differences are the deliberate later corrections (parsed-sparse figure, grader class-disjoint wording, `anthropic-only` fallback wording, `KeyError` wording, D-02 docstring wording, V-029 run counts, QA-gate additions); (4) the four web files are represented section by section in Section 5, with excluded or unverified claims listed in 5.5.3.

Coverage limits: the four adversarial debates are `partial` and E2 is read at commit 4a22d74213f93837d00c2c314075dd967b9a98e3 only; the report states both (Sections 7, 8 and 10).

**Verdict: PASS (0 omitted at CRITICAL or IMPORTANT)**

