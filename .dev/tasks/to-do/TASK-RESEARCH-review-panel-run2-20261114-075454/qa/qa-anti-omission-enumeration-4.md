# Anti-Omission Enumeration 4

Assigned inputs: research/24-value-ledger-evidence-consumers.md, synthesis/synth-08-value-inventory.md (ledgers 19-23 moved to agents 1, 2, 3 by qa/gate5-partition.md).
Status: Complete (COUNT lines: 24-value-ledger-evidence-consumers.md 589; synth-08-value-inventory.md 344)

## File 1: research/24-value-ledger-evidence-consumers.md (ledger 24, one entry per ledger row)

Format: `n. ID | kind | ledger destination -> inventory destination | statement (first 100 chars) | class | synth-08 line`.
Class: REP = represented (row present in Appendix A = synth-08 under its destination, Statement/Kind/Source byte-equal to the ledger row, checked by a read-only join); DEDUP = COVERED-BY-DEDUP (row is `DROP[duplicate]` and names the kept row); MOVED = destination changed with a recorded reason.
Join result: 589 ledger rows, 589 found in synth-08, 0 Statement differences, 0 Kind differences, 5 destination changes (VL-24-153, 159, 167, 172 to DROP duplicate of a DR row; VL-24-181 CORE to MODULE-reflect), each with its reason in the row.

1. VL-24-001 | fix | MODULE-reflect -> MODULE-reflect | Commit 9874d63fb fixes three shadow-run defects in SKILL.md and reviewer-spec.md (card model: copied | REP | L1248
2. VL-24-002 | fix | MODULE-reflect -> MODULE-reflect | Commit c2e3347d3 makes the reviewer brief name the exact findings heading (second prompt-only fix) | REP | L1249
3. VL-24-003 | artifact | EVAL -> EVAL | Evidence commit 792cf8c52 adds 736 files / 86921 insertions (combo workspace, troubleshoot report, p | REP | L3035
4. VL-24-004 | finding | KNOWLEDGE -> KNOWLEDGE | Since the kernel merge the only src/test changes are 3 skill-doc files and 2 test files; cli/reflect | REP | L4036
5. VL-24-005 | artifact | DROP -> DROP | Untracked .dev/issues/531/ listed at session start | REP | L5895
6. VL-24-006 | requirement | EVAL -> EVAL | Experiment input is ONE package (TASK-WF-designSpec-20261107-075614, tasklist sha 044809e3, spec sha | REP | L3036
7. VL-24-007 | strategy | HARNESS -> HARNESS | Combo matrix A pilot-baseline, B sonnet-orchestrator, C true-haiku, D luna-replaces-opus, E study-ha | REP | L3588
8. VL-24-008 | strategy | HARNESS -> HARNESS | Schedule: 3 blocks r1..r3, A-E launched together in random order, memory restored from frozen copies | REP | L3589
9. VL-24-009 | requirement | EVAL -> EVAL | Decision rule fixed before launch: descriptive only; a lead needs non-overlapping ranges, median gap | REP | L3037
10. VL-24-010 | lesson | EVAL -> EVAL | At n=3 complete separation happens 2 times in 20 by chance (10%) with about 40 metric-pair compariso | REP | L3038
11. VL-24-011 | open | EVAL -> EVAL | Optional blind ground-truth scoring of the 15 runs needs separate approval and was NOT done (also O- | REP | L3039
12. VL-24-012 | open | HARNESS -> HARNESS | Gateway /v1/models lacks muse-ember-1.0; raw ids as ANTHROPIC_DEFAULT_* values UNVERIFIED (also O-11 | REP | L3590
13. VL-24-013 | open | CORE -> CORE | Models of the advocate and merge-executor roles UNVERIFIED in the experiment | REP | L761
14. VL-24-014 | risk | HARNESS -> HARNESS | Contention risk at 5 concurrent runs | REP | L3591
15. VL-24-015 | finding | EVAL -> EVAL | E2 study scope as quoted by PLAN.md: reviewer role only, /sc:spec-panel --mode critique of tasklists | REP | L3040
16. VL-24-016 | finding | EVAL -> EVAL | E2 panel table: haiku+2x luna 2.2/14 found, 1.2/8 real blocking, 3.0 wrong blockers; ember+2x luna 1 | REP | L3041
17. VL-24-017 | finding | EVAL -> EVAL | E2 did not test the calibrator, debate/merge or orchestrator roles | REP | L3042
18. VL-24-018 | defect | CORE -> CORE | E2 deterministic merge silently dropped anchors longer than 200 chars, losing 49 blocking findings;  | REP | L762
19. VL-24-019 | lesson | EVAL -> EVAL | Only 3 E2 effects survive permutation tests; 1/1/1 rows are anecdotes; confounders: merge drops, sou | REP | L3043
20. VL-24-020 | finding | EVAL -> EVAL | No E2 panel lifts the ceiling past about 2.5/14 (GT1, GT2, GT10, alias GT4 never caught); transfer t | REP | L3044
21. VL-24-021 | finding | CORE -> CORE | Reflect model control surface: orchestrator = session model, reviewer class passed per Agent call an | REP | L763
22. VL-24-022 | defect | CORE -> CORE | review panel resolve gives identical resolution under every combo env; shadow step passes --env anth | REP | L764
23. VL-24-023 | requirement | CORE -> CORE | Not controllable without a code or prompt change: whether the class is passed on each Agent call, wh | REP | L765
24. VL-24-024 | finding | EVAL -> EVAL | Recount: every minute, confidence, clustered, compliance, token and cost figure in FINDINGS/results  | REP | L3045
25. VL-24-025 | finding | EVAL -> EVAL | All 15 combo runs published, reviewers_complete 3/3, exit 0, no .dev/tasks/done/<id> citation leak i | REP | L3046
26. VL-24-026 | finding | EVAL -> EVAL | Combo wall time sums to 489.2 min; per run 18.2 min (D1) to 67.9 min (A2) | REP | L3047
27. VL-24-027 | finding | EVAL -> EVAL | Orchestrator-stated cost totals USD 478.4 (a name-based Claude Code estimate, not billed) and 4,119, | REP | L3048
28. VL-24-028 | finding | CORE -> CORE | Orchestrator produces 0.38-0.87 of output tokens (median 0.59) over 15 runs, so reviewer-slot choice | REP | L766
29. VL-24-029 | finding | EVAL -> EVAL | Per-combo median (min-max) minutes: A 63.9 (19.4-67.9), B 24.9 (23.4-38.5), C 33.4 (33.3-34.0), D 27 | REP | L3049
30. VL-24-030 | finding | EVAL -> EVAL | Calibrated confidence medians: A 0.767, B 0.71, C 0.74, D 0.65, E 0.59 | REP | L3050
31. VL-24-031 | finding | EVAL -> EVAL | Clustered finding medians: A 21, B 12, C 19, D 16, E 19 (counted before the evidence gate) | REP | L3051
32. VL-24-032 | finding | EVAL -> EVAL | First-pass compliance: A 0.667 x3, B/C/D 1.0 x3 each, E 1.0 / 0.6667 / 0.3333; mean 0.867 over 15 | REP | L3052
33. VL-24-033 | finding | EVAL -> EVAL | Class to served-model map from stream logs: A1/A2/B served gpt-6.1-sol in the haiku slot; A3 all rev | REP | L3053
34. VL-24-034 | defect | CORE -> CORE | Dispatch collapse: pilot 6 of 9 tier3-orchestrated runs ran all reviewers on the sonnet alias, A3 1  | REP | L767
35. VL-24-035 | finding | HARNESS -> HARNESS | Lead 1: orchestrator tier changes wall time (A 64 and 68 min vs B 23-39 min); cause not isolated (al | REP | L3592
36. VL-24-036 | finding | EVAL -> EVAL | Lead 2: calibrated confidence in D (0.62-0.66) and E (0.53-0.68) lies below A (0.75-0.84), but E ove | REP | L3054
37. VL-24-037 | finding | EVAL -> EVAL | Lead 3: A's first-pass compliance 0.667 x3 vs 1.0 x9 elsewhere; A3 notes show a citation-path typo f | REP | L3055
38. VL-24-038 | finding | EVAL -> EVAL | Non-findings: clustered-count ranges overlap across all five combos, C vs B no separation on any mea | REP | L3056
39. VL-24-039 | finding | EVAL -> EVAL | FINDINGS wording "parity and lint problems in all combinations" is inexact: parity fails in 4 of 15  | REP | L3057
40. VL-24-040 | defect | CORE -> CORE | Parity failure reasons: A1/A2 legacy model text is neither a mapped id nor a class name; A3 a card h | REP | L768
41. VL-24-041 | finding | CORE -> CORE | Real content of the combo exit run: 9 of 15 runs degrade to single-vendor with allow_single_vendor=F | REP | L769
42. VL-24-042 | defect | CORE -> CORE | cluster_agreement over combo runs is min 0.143 / median 0.336 / max 1.000 vs 1.0 in every pilot run; | REP | L770
43. VL-24-043 | finding | EVAL -> EVAL | Cross-reviewer clustering overlap is nearly absent: combos 216 clusters / 255 members, 203 single-re | REP | L3058
44. VL-24-044 | finding | EVAL -> EVAL | calibration_coverage equals clustered findings in every combo run (findings carry per-finding number | REP | L3059
45. VL-24-045 | finding | DROP -> DROP | Snapshot counts: 91 pre-* dirs, 15 shadow-named, 14 with panel/manifest.json, 553 tracked shadow fil | REP | L5896
46. VL-24-046 | finding | EVAL -> EVAL | Stage 2 exit today: 13 of 20 shadow runs counted, EV-1 8/13 vs legacy 3/39, parity fails 6/13, lint  | REP | L3060
47. VL-24-047 | lesson | CORE -> CORE | All 8 pilot EV-1 failures are layout, naming or contract-writing failures (a return-contract.yaml th | REP | L771
48. VL-24-048 | finding | EVAL -> EVAL | All 30 pilot+combo runs are forced --tier 2 (28 of 30 parsed-sparse, composite 3.5-9.0), so the evid | REP | L3061
49. VL-24-049 | finding | EVAL -> EVAL | Cluster structure of the 13 counted pilot runs: 71 clusters, 127 members, 52 single, 13 multi, 4 blo | REP | L3062
50. VL-24-050 | finding | MODULE-tasklist -> MODULE-tasklist | Plan-defect family: constraints or bullets with no matching acceptance criterion (shadow04/06/08/10/ | REP | L1591
51. VL-24-051 | finding | MODULE-tasklist -> MODULE-tasklist | Plan-defect family: escape-hatch acceptance criteria (memory lines 26, 42, 54) | REP | L1592
52. VL-24-052 | finding | MODULE-tasklist -> MODULE-tasklist | Plan-defect family: grep-count or name-only acceptance criteria (memory lines 18, 68, 85, 97) | REP | L1593
53. VL-24-053 | finding | KNOWLEDGE -> KNOWLEDGE | Plan-defect family: hand-maintained mirror drift in plugins/superclaude/* not covered by make sync-d | REP | L4037
54. VL-24-054 | finding | MODULE-tasklist -> MODULE-tasklist | Plan-defect family: spec holes inherited by plans (memory lines 8-9, 19) | REP | L1594
55. VL-24-055 | lesson | CORE -> CORE | Post-execution temporal misattribution: shadow14/15 reviewers cited HEAD text added by PR #513 after | REP | L772
56. VL-24-056 | finding | MODULE-tasklist -> MODULE-tasklist | Plan-defect family: amendments appended after plan generation never propagate (memory line 67) | REP | L1595
57. VL-24-057 | finding | MODULE-tasklist -> MODULE-tasklist | Plan-defect family: absolute-count rot (named only in the V-27 row) | REP | L1596
58. VL-24-058 | lesson | CORE -> CORE | Debate withdraws reviewer blockers lacking a traced wrong outcome (6 of 6 withdrawn in E-r3, 2 of 2  | REP | L773
59. VL-24-059 | finding | MODULE-spec -> MODULE-spec | Only the invariant probe found some spec gaps no reviewer found, and probe items rated HIGH were dow | REP | L1656
60. VL-24-060 | finding | KNOWLEDGE -> KNOWLEDGE | Reviewer-correctness positive case (memory line 34) | REP | L4038
61. VL-24-061 | lesson | EVAL -> EVAL | Shadow runs re-audit archived done/ packages against an evolved HEAD (memory lines 12, 33, 56, 62);  | REP | L3063
62. VL-24-062 | lesson | CORE -> CORE | Brief carrying the literal heading, fence and one example line gives 3/3 first-parse compliance (sha | REP | L774
63. VL-24-063 | artifact | CORE -> CORE | findings-v2 schema and parser asset: src/superclaude/cli/review/findings_v2.py (304 lines) with caps | REP | L775
64. VL-24-064 | defect | CORE -> CORE | Claims over 300 chars fail silently in the pilot (memory lines 29, 71) | REP | L776
65. VL-24-065 | defect | CORE -> CORE | Card-write corruption seen 3 times when the orchestrator persists cards (memory line 29) | REP | L777
66. VL-24-066 | requirement | CORE -> CORE | An EMPTY findings block counts as complete only with a coverage.json entry listing the observed rows | REP | L778
67. VL-24-067 | defect | CORE -> CORE | judge_identity values containing ": " must be quoted in YAML or EV-1 trips (memory line 36) | REP | L779
68. VL-24-068 | artifact | CORE -> CORE | Run manifest asset: ordered stages, frozen hashes, attempt rows (manifest.py 534, manifest_cmd.py 24 | REP | L780
69. VL-24-069 | requirement | CORE -> CORE | Manifest per-attempt rows must be recorded BEFORE advancing the closing stage (memory line 58) | REP | L781
70. VL-24-070 | artifact | CORE -> CORE | verify-citations pre-check asset (verify_cmd.py 184 lines, precheck.json): quote-not-found is the ch | REP | L782
71. VL-24-071 | defect | CORE -> CORE | verify-citations root must equal the common ancestor of citation paths and snapshot paths need the s | REP | L783
72. VL-24-072 | defect | CORE -> CORE | Reviewer self-reports are unreliable alias echoes (shadow03 reviewers 2 and 3 self-reported claude-g | REP | L784
73. VL-24-073 | requirement | CORE -> CORE | Record the served model per reviewer call from the sidechain transcript (identity_source: observed)  | REP | L785
74. VL-24-074 | defect | CORE -> CORE | The sc-adversarial return contract names no judge, so judge_identity is unknown (7 of 15 combo runs, | REP | L786
75. VL-24-075 | finding | KNOWLEDGE -> KNOWLEDGE | First clean-judge run shadow08: judge claude-gw-tier3 distinct from all three debater classes, judge | REP | L4039
76. VL-24-076 | artifact | KNOWLEDGE -> KNOWLEDGE | Troubleshoot report .dev/troubleshoot/shadow-failures-20261113014240/REPORT.md (45 lines, only file  | REP | L4040
77. VL-24-077 | defect | KNOWLEDGE -> KNOWLEDGE | Parity root cause: the skill called card model: "the resolved model id" without saying copy from pan | REP | L4041
78. VL-24-078 | decision | KNOWLEDGE -> KNOWLEDGE | Rejected option: let the aggregator fall back to model_class when model is an unmapped alias (would  | REP | L4042
79. VL-24-079 | decision | KNOWLEDGE -> KNOWLEDGE | Rejected option: make the exit script accept nested or .md-only verdict files (recommend against loo | REP | L4043
80. VL-24-080 | finding | EVAL -> EVAL | Post-fix comparison: parity failing 4/15 vs 6/13, EV-1 failing 3/15 vs 8/13, mean compliance 0.867 v | REP | L3064
81. VL-24-081 | artifact | EVAL -> EVAL | Stage 0a replay report .dev/tasks/done/TASK-WF-implementStages0-20261111-202912/artifacts/stage0a-re | REP | L3065
82. VL-24-082 | lesson | KNOWLEDGE -> KNOWLEDGE | Committed report is a dated snapshot: pre-* dirs 74 to 91, card dirs 43 to 59, merged verdicts 34 to | REP | L4044
83. VL-24-083 | finding | EVAL -> EVAL | Stage 0a conversion (gate O-7): 712 units (689 findings + 23 unlisted cards), 479 converted, 67.28%, | REP | L3066
84. VL-24-084 | finding | EVAL -> EVAL | Conversion by card shape: yaml-blocking-minor 33 cards 69.87%, yaml-other-severity 49 cards 78.02%,  | REP | L3067
85. VL-24-085 | finding | EVAL -> EVAL | Unconverted causes: 104 no path:line reference, 54 "citations must be a list of N to N", 31 path not | REP | L3068
86. VL-24-086 | finding | EVAL -> EVAL | cluster_v2 over recorded cards: 689 findings, 461 clusters, 392 single, 55 multi-reviewer (29 not ch | REP | L3069
87. VL-24-087 | finding | EVAL -> EVAL | Agreement between recorded merged verdicts and cluster_v2 multi-reviewer clusters: 24/358 = 6.70% ov | REP | L3070
88. VL-24-088 | finding | EVAL -> EVAL | Null convergence scores: 8 of 64 contracts (skipped-similar 0, single-reviewer-fallback 2, illegal m | REP | L3071
89. VL-24-089 | finding | EVAL -> EVAL | Recorded calibration before shadow mode: embedded 34 cards / 271 findings, sidecar 61 / 347, none 20 | REP | L3072
90. VL-24-090 | artifact | EVAL -> EVAL | AI-label sheet design: seed 20261111, 50 pairs (merged 25 same-file, apart 13 same-file + 12 cross-f | REP | L3073
91. VL-24-091 | strategy | HARNESS -> HARNESS | AI labelling method: 3 labelers (opus, sonnet, opus-skeptical), 46 unanimous, 4 split (P01, P09, P12 | REP | L3593
92. VL-24-092 | finding | EVAL -> EVAL | AI-label recount reproduces README: 50 pairs, TP=21 FP=4 FN=1 TN=24, precision 0.8400 (21/25), recal | REP | L3074
93. VL-24-093 | lesson | EVAL -> EVAL | Recall 0.9545 is not population recall: apart pool 4031 vs merged pool 41; the only FN (P38) is the  | REP | L3075
94. VL-24-094 | risk | EVAL -> EVAL | AI-label caveats: labelers and cluster_v2 share a model family, labeler B did not open cards, claim  | REP | L3076
95. VL-24-095 | open | EVAL -> EVAL | Same-reviewer pairs (the P09 bundled-finding case) are excluded by design; supplementary set NOT BUI | REP | L3077
96. VL-24-096 | open | EVAL -> EVAL | Owner hand labels PENDING (pilot-design.md:250) and Stage 0 exit PENDING (pilot-design.md:257); blan | REP | L3078
97. VL-24-097 | defect | CORE -> CORE | cluster_v2 weakness W-1: a bundled finding clusters with findings that match only one part (V-31) | REP | L787
98. VL-24-098 | defect | CORE -> CORE | cluster_v2 weakness W-2: refs_norm takes P1 from "D-P1" (pair P12 false merge; findings.py:29 "re-re | REP | L788
99. VL-24-099 | defect | CORE -> CORE | cluster_v2 weakness W-3: spec:N resolved against the short source.md brief (V-31) | REP | L789
100. VL-24-100 | lesson | EVAL -> EVAL | cluster_v2 weakness W-4: precision/recall are sample figures, not rates (cluster-v2-known-weaknesses | REP | L3079
101. VL-24-101 | finding | EVAL -> EVAL | S-ID probe (artifacts/s-id-results.md, 38 lines): self-reports match the pin 0 of 3 by name; transcr | REP | L3080
102. VL-24-102 | requirement | CORE -> CORE | The read-only reviewer allowlist survives the Agent model override 3 of 3 (no Write/Edit/Bash; harne | REP | L790
103. VL-24-103 | decision | EVAL -> EVAL | Conversion gate T-9 redefined by the owner on 2026-11-12: recorded cards are the baseline only; gate | REP | L3081
104. VL-24-104 | artifact | CORE -> CORE | shadow-standalone-evaluation.md (132 lines) classifies E1 components generic vs reflect-specific (ta | REP | L791
105. VL-24-105 | finding | EVAL -> EVAL | Reflect's shadow variant produces no verdict of its own and reuses the legacy reviewers' dispatch (S | REP | L3082
106. VL-24-106 | decision | CORE -> CORE | Decision D-7: extract a generic shadow harness only after 20 real shadow runs PASS and a second cons | REP | L792
107. VL-24-107 | artifact | EVAL -> EVAL | artifacts/pilot-design.md (257 lines): quality measurement design with arms A-D, seeded defects (60) | REP | L3083
108. VL-24-108 | finding | CORE -> CORE | artifacts/consumer-inventory.md (405 lines): 3423 files searched, 320 hit files (producer 51, valida | REP | L793
109. VL-24-109 | open | DROP -> DROP | Slice did not read stage2-entry-inventory.md (411), stage2-entry-inventory-diff.md (65), lint-test-d | REP | L5897
110. VL-24-110 | script | HARNESS -> HARNESS | scripts/reflect_stage0a_replay.py (896 lines; collect :434, render :511, main :867): converts record | REP | L3594
111. VL-24-111 | test | HARNESS -> HARNESS | Test tests/review/test_reflect_stage0a_replay.py | REP | L3595
112. VL-24-112 | script | HARNESS -> HARNESS | scripts/reflect_cluster_pairs.py (559 lines): sample (50-pair sheet, seed 20261111), form, score (TP | REP | L3596
113. VL-24-113 | test | HARNESS -> HARNESS | Test tests/review/test_reflect_cluster_pairs.py | REP | L3597
114. VL-24-114 | script | HARNESS -> HARNESS | scripts/reflect_verdict_replay.py (184 lines): offline derive_verdict replay of recorded 1.8.0 contr | REP | L3598
115. VL-24-115 | test | HARNESS -> HARNESS | Test tests/cli/reflect/test_verdict_replay_script.py (190 lines) | REP | L3599
116. VL-24-116 | script | HARNESS -> HARNESS | scripts/reflect_shadow_exit.py (410 lines; EXIT :57, collect :203, build_report :282): Stage 2 exit  | REP | L3600
117. VL-24-117 | test | HARNESS -> HARNESS | Test tests/cli/reflect/test_shadow_exit_script.py (319 lines, 20 tests) | REP | L3601
118. VL-24-118 | script | HARNESS -> HARNESS | scripts/reflect_consumer_inventory.py (535 lines): consumer grep of contract fields; not re-run by t | REP | L3602
119. VL-24-119 | test | HARNESS -> HARNESS | Test tests/review/test_reflect_consumer_inventory.py | REP | L3603
120. VL-24-120 | script | HARNESS -> HARNESS | .dev/eval-workspaces/shadow-model-combos/analysis/extract.py (193 lines): builds results.jsonl and r | REP | L3604
121. VL-24-121 | artifact | CORE -> CORE | Kernel code src/superclaude/cli/review/: 5086 lines over 16 files (card_convert 517, cluster 487, cl | REP | L794
122. VL-24-122 | artifact | MODULE-reflect -> MODULE-reflect | Reflect-side code src/superclaude/cli/reflect/{panel_lint,contract,ensemble,fallback,runner,...}.py  | REP | L1250
123. VL-24-123 | test | CORE -> CORE | Kernel tests tests/review/ (19 files incl. test_review_manifest, _panel, _cluster, _findings_v2, _ve | REP | L795
124. VL-24-124 | test | MODULE-reflect -> MODULE-reflect | Reflect tests tests/cli/reflect/ (40 .py files incl. __init__ and conftest, 8206 lines total) | REP | L1251
125. VL-24-125 | finding | EVAL -> EVAL | The four shadow-related test files pass: 82 passed in 40.17 s (uv run pytest on test_shadow_exit_scr | REP | L3084
126. VL-24-126 | artifact | CORE -> CORE | review-telemetry/1 (telemetry.py 447 lines, telemetry_cmd.py 98) is NOT called by shadow mode (shado | REP | L796
127. VL-24-127 | finding | DROP -> DROP | .dev/benchmarks/ holds only v2.20-baseline (roadmap-gate benchmark, README measures F-001..F-006); n | REP | L5898
128. VL-24-128 | threshold | EVAL -> EVAL | Threshold T-1 (H-A superiority): T2 recall minus T1 recall on seeded defects at least 15 points (M 0 | REP | L3085
129. VL-24-129 | threshold | EVAL -> EVAL | Threshold T-2 (H-B non-inferiority): panel-parity T2 recall and precision within 10 points, one-side | REP | L3086
130. VL-24-130 | threshold | EVAL -> EVAL | Threshold T-3 (H-C cost): median panel-T2 tokens at most 1.05 x legacy (pilot-design.md:19); never r | REP | L3087
131. VL-24-131 | threshold | EVAL -> EVAL | Threshold T-4 (H-C cost): p95 at most 65k claude tokens, also the kill line (pilot-design.md:20, 11: | REP | L3088
132. VL-24-132 | threshold | EVAL -> EVAL | Threshold T-5 safety list, zero events: forbidden model/executor-class collision when the executor i | REP | L3089
133. VL-24-133 | threshold | EVAL -> EVAL | Threshold T-6 within-arm noise: d0 at least 0.8 x d between arms means indistinguishable (pilot-desi | REP | L3090
134. VL-24-134 | threshold | EVAL -> EVAL | Threshold T-7 non-sparse quota: at least 25% of plans with labelled requirement ids; 34 of 38 record | REP | L3091
135. VL-24-135 | threshold | EVAL -> EVAL | Threshold T-8 test level: one-sided 95% (z 1.645) with 80% power (z 0.842) (pilot-design.md:24) | REP | L3092
136. VL-24-136 | threshold | EVAL -> EVAL | Threshold T-9 conversion gate: at least 90% of findings with unambiguous (path,line) on cards writte | REP | L3093
137. VL-24-137 | threshold | EVAL -> EVAL | Threshold T-10 pooled headline: only if the heterogeneity check is not significant (no test named, S | REP | L3094
138. VL-24-138 | open | EVAL -> EVAL | Pilot stop rule S-0..S-5 is PROPOSED in the Stage 0 package's own note (pilot-design.md:188-218); th | REP | L3095
139. VL-24-139 | requirement | EVAL -> EVAL | Stop rule S-2: safety STOP in arm C/D, STOP on event 5 in any arm and event 4 in any arm; LOG events | REP | L3096
140. VL-24-140 | requirement | EVAL -> EVAL | Stop rule S-3: spend ceilings per unit, block-level test; a killed run is not rerun and counts above | REP | L3097
141. VL-24-141 | requirement | EVAL -> EVAL | Stop rule S-4: never stop on interim results | REP | L3098
142. VL-24-142 | requirement | EVAL -> EVAL | Stop rule S-5: write the stop record to stop-record.md | REP | L3099
143. VL-24-143 | requirement | EVAL -> EVAL | Stage 2 exit: 20 shadow runs, MALFORMED = 0, EV-1 failure rate no higher than the legacy baseline, p | REP | L3100
144. VL-24-144 | requirement | MODULE-reflect -> MODULE-reflect | Lint/exit hard lines in force: frozen 1.8.0 stable-key list (L2), bump rule (B), L6 EV-1 merged adve | REP | L1252
145. VL-24-145 | requirement | EVAL -> EVAL | Dispatch-collapse acceptance rule: "If B-E also collapse dispatch in most runs, the reviewer contras | REP | L3101
146. VL-24-146 | decision | EVAL -> EVAL | Decision D-2: pilot arm C uses the development-build --t2-engine panel, NOT shadow, because shadow k | REP | L3102
147. VL-24-147 | decision | HARNESS -> HARNESS | Decision D-8: experiment runs kept out of .dev/reflect/ so the Stage 2 exit count is not polluted (P | REP | L3605
148. VL-24-148 | open | EVAL -> EVAL | Open O-1: no decision on whether to keep running pilot shadow runs, accept combo runs as shadow runs | REP | L3103
149. VL-24-149 | open | EVAL -> EVAL | Open O-6: pilot stop rule S-0..S-5, reading of "6 repeats of arm B" (SD-3), SD-6, SD-8, spend ceilin | REP | L3104
150. VL-24-150 | open | HARNESS -> HARNESS | Open O-9: the finding-level T-9 measurement script is NOT BUILT (conversion-gate-redefinition.md:31) | REP | L3606
151. VL-24-151 | requirement | CORE -> CORE | Rule: the orchestrator must not remap, edit or normalize findings; the first-parse compliance metric | REP | L797
152. VL-24-152 | artifact | CORE -> CORE | cluster_v2 asset: path-aware clustering with calibrated support and cluster_agreement (cluster.py 48 | REP | L798
153. VL-24-153 | defect | HARNESS -> DROP | Defect X-1: the exit script treats an empty legacy baseline as 0.0 (reflect_shadow_exit.py:313 if (s | MOVED | L5899
154. VL-24-154 | defect | MODULE-reflect -> MODULE-reflect | Defect X-2: EV-1 lint counts cards only when named reviewer-N-card.<yaml/yml/md> (panel_lint.py:188  | REP | L1253
155. VL-24-155 | defect | CORE -> CORE | Defect X-3: merged-verdict.yaml must be at adversarial/merged-verdict.yaml but the sc-adversarial ch | REP | L799
156. VL-24-156 | defect | CORE -> CORE | Defect X-4: the recorded panel_parity: true was wrong in 2 pilot runs (shadow05, shadow07) and 4 com | REP | L800
157. VL-24-157 | defect | CORE -> CORE | Defect X-5: contract diversity telemetry is blind to dispatch collapse (A3: calibrator_diversity: fu | REP | L801
158. VL-24-158 | defect | CORE -> CORE | Defect X-6: the "no stable-contract change" shadow promise is violated: new top-level keys in 7 of 2 | REP | L802
159. VL-24-159 | defect | HARNESS -> DROP | Defect X-7: Stage 0a replay cannot read panel/cards/ findings-v2 blocks, so it reports shadow runs a | MOVED | L5900
160. VL-24-160 | defect | CORE -> CORE | Defect X-8: evidence-validator drop_rate is inconsistent with the counts (shadow03 metrics drop_rate | REP | L803
161. VL-24-161 | defect | CORE -> CORE | Defect X-9: merged-verdict.yaml has no uniform schema, so blocking/medium/minor are None in 13 of 15 | REP | L804
162. VL-24-162 | defect | HARNESS -> HARNESS | Defect X-10: the 15 combo runs used an installed skill that lags src/ (installed reviewer-spec sha b | REP | L3607
163. VL-24-163 | defect | HARNESS -> HARNESS | Defect X-11: PLAN.md:1-3 and combos.json:4 still say "designed, NOT run" next to FINDINGS reporting  | REP | L3608
164. VL-24-164 | defect | CORE -> CORE | Defect X-12: .dev/reflect/runs.jsonl holds 14 of 15 combo rows (A-r2 missing), non-uniform ids, and  | REP | L805
165. VL-24-165 | defect | CORE -> CORE | Defect X-13: E1 had 7 reviewer-agent calls vs 3 in the other 14 runs, reason unrecorded in FINDINGS  | REP | L806
166. VL-24-166 | defect | DROP -> DROP | Defect X-14: untracked grounding checkout runs/...comboC-r3/artifacts/base-e8db2fe6/ left behind by  | REP | L5901
167. VL-24-167 | defect | MODULE-reflect -> DROP | Defect X-15: memory write-back leaks run lessons into docs/memory/reflect/*.md (live file 100 lines, | MOVED | L5902
168. VL-24-168 | defect | DROP -> DROP | Defect X-16: memory lesson "fenced yaml calibration not parsed by cluster" (memory line 64) contradi | REP | L5903
169. VL-24-169 | defect | CORE -> CORE | Defect X-17: shadow02 aborted at the clustering step: all 11 findings chained into one cluster becau | REP | L807
170. VL-24-170 | defect | MODULE-reflect -> MODULE-reflect | Defect X-18: shadow01 ran as legacy because the installed CLI lacked review panel resolve options/su | REP | L1254
171. VL-24-171 | defect | HARNESS -> HARNESS | Defect X-19: extract.py quirks: non-uv subprocess (sys.executable at extract.py:86 [CODE-VERIFIED]), | REP | L3609
172. VL-24-172 | defect | HARNESS -> DROP | Defect X-20: weak test test_the_current_repository_reports_without_crashing asserts only that the la | MOVED | L5904
173. VL-24-173 | defect | HARNESS -> HARNESS | Defect X-21: combos.json common.panel_resolution_all_combos records class rotation only, and resolut | REP | L3610
174. VL-24-174 | defect | DROP -> DROP | Defect X-22: E1-E3 reviewer 3 self-reported claude-gw-tier4[1m] while the stream log shows it served | DEDUP of VL-24-072 | L5905
175. VL-24-175 | artifact | CORE -> CORE | Panel resolver asset: panel.py 707, panel_cmd.py 129, tier file review-tiers.default.json, templates | REP | L808
176. VL-24-176 | artifact | CORE -> CORE | Deterministic merge asset review merge (merge_cmd.py 118); the E2 study merged with it (PLAN.md:12-1 | REP | L809
177. VL-24-177 | strategy | HARNESS -> HARNESS | Model-combination experiment protocol: PLAN.md sections 3-4, combos.json, launch recipe, results sch | REP | L3611
178. VL-24-178 | risk | EVAL -> EVAL | N-4: served models were read from stream logs of one window (2026-11-13T02:59Z to about 05:46Z); tie | REP | L3105
179. VL-24-179 | risk | EVAL -> EVAL | N-6: generalization limit: one package (designSpec), already-executed work audited against post-impl | REP | L3106
180. VL-24-180 | defect | HARNESS -> HARNESS | N-9: per-run skill hash is recorded only for the 15 combos; pre-fix vs post-fix membership of shadow | REP | L3612
181. VL-24-181 | strategy | CORE -> MODULE-reflect | Shadow authority rule and the 10 shadow steps (SKILL.md 4.3a): variant under test, authoritative pat | MOVED | L1255
182. VL-24-182 | artifact | EVAL -> EVAL | Experiment outputs results.jsonl (15 lines), results.md (47), FINDINGS.md (42): 15 rows, no quality  | REP | L3107
183. VL-24-183 | artifact | HARNESS -> HARNESS | .dev/eval-workspaces/shadow-model-combos/runs/pre-...combo*/ (15 run dirs, most of the 91M) and logs | REP | L3613
184. VL-24-184 | artifact | HARNESS -> HARNESS | .dev/reflect/pre-*shadow* (15 dirs, 13 counted) as regression fixtures for the exit script and lint  | REP | L3614
185. VL-24-185 | test | MODULE-reflect -> MODULE-reflect | Test tests/cli/reflect/test_shadow_skill_contract.py (307 lines) pins prose strings of the skill (pr | REP | L1256
186. VL-24-186 | conflict | EVAL -> EVAL | Conflict C-01: E2 PLAN-quoted result "sonnet alone 2/16 ... more catches per token than 3-6 model pa | REP | L3108
187. VL-24-187 | conflict | EVAL -> EVAL | Conflict C-02: E2's best blocking panel haiku + 2x luna (1.2/8, PLAN.md:20) vs E1 combo E (same mode | REP | L3109
188. VL-24-188 | conflict | CORE -> CORE | Conflict C-03: alias/class dispatch (E1: ANTHROPIC_DEFAULT_* env plus class per Agent call, collapse | REP | L810
189. VL-24-189 | conflict | EVAL -> EVAL | Conflict C-04: ground truth E1 seeded defects plus union ledger (pilot-design.md:55-64) vs E2 implem | REP | L3110
190. VL-24-190 | conflict | KNOWLEDGE -> KNOWLEDGE | Conflict C-05: evidence-grade conflict inside E1: PLAN/FINDINGS say descriptive/leads only and shado | REP | L4045
191. VL-24-191 | conflict | HARNESS -> HARNESS | Conflict C-07: experiments run on installed ~/.claude skills while dev fixes live in src/ and .claud | REP | L3615
192. VL-24-192 | finding | CORE -> CORE | Overlap: E2 dispatched reviewer panels by claude -p --model <raw id> per reviewer plus superclaude r | REP | L811
193. VL-24-193 | finding | EVAL -> EVAL | Overlap: evidence validator (citation re-read) in E1 vs blind judges against ground truth in E2 | REP | L3111
194. VL-24-194 | finding | CORE -> CORE | Overlap: pilot stop rule S-0..S-5 (proposed) vs E3 stoprule/ledger (kernel dir has ledger.py 494 lin | REP | L812
195. VL-24-195 | requirement | CORE -> CORE | Architecture: thin modules own only lens, citation roles, brief template, grounding hunks, contract/ | REP | L813
196. VL-24-196 | requirement | CORE -> CORE | Architecture: the shadow/variant machinery is prose executed by an LLM orchestrator; a shared core t | REP | L814
197. VL-24-197 | requirement | CORE -> CORE | Architecture: orchestrator-dominant cost and layout/naming failure classes point to a deterministic  | REP | L815
198. VL-24-198 | requirement | MODULE-reflect -> MODULE-reflect | Exposure sc:reflect Tier 2 (UC-1 pre): 13 pilot and 15 combo shadow runs, exit gates, Stage 0a basel | REP | L1257
199. VL-24-199 | requirement | MODULE-tasklist -> MODULE-tasklist | Exposure sc:workflow tasklist review (Wave 4 calls /sc:reflect --mode pre, shadow-standalone-evaluat | REP | L1597
200. VL-24-200 | requirement | MODULE-spec -> MODULE-spec | Exposure spec review: findings-v2 lens list is "reflect + spec only" (shadow-standalone-evaluation.m | REP | L1657
201. VL-24-201 | requirement | MODULE-pr-review -> MODULE-pr-review | Exposure PR code review: reflect-post roles source, diff exist (cluster.py:67-69 [CODE-VERIFIED]); f | REP | L1722
202. VL-24-202 | requirement | MODULE-rfqa -> MODULE-rfqa | Exposure rf-qa replacement: evidence validator, verify-citations and the read-only reviewer invarian | REP | L1760
203. VL-24-203 | open | HARNESS -> HARNESS | Exposure cross-skill shadow/variant comparison: second-consumer candidates are the spec-panel loop,  | REP | L3616
204. VL-24-204 | requirement | CORE -> CORE | Exposure model-routing and tier policy: combos, tier file review-tiers.default.json (exists at src/s | REP | L816
205. VL-24-205 | requirement | CORE -> CORE | Exposure cost control: orchestrator token share, kill line T-4 65k, USD estimates; T-3/T-4 never mea | REP | L817
206. VL-24-206 | open | CORE -> CORE | G-6 / O-8: cluster_agreement support semantics under W-1 unverified; the 7 multi-reviewer clusters o | REP | L818
207. VL-24-207 | open | EVAL -> EVAL | G-8: quality of the 15 runs' findings is unscored; whether B's 12 vs C's 19 clustered findings refle | REP | L3112
208. VL-24-208 | risk | DROP -> DROP | G-9: the slice's rerun outputs under /tmp/e1-recount-slice11/ (exit-ref.txt, exit-combo.txt, stage0a | REP | L5906
209. VL-24-209 | open | DROP -> DROP | Slice 11 did not read transcripts (logs/*.jsonl, runs/*/ debate files), per-run REPORT.md and review | REP | L5907
210. VL-24-210 | artifact | MODULE-spec -> MODULE-spec | A1 base command src/superclaude/commands/spec-panel.md (490 lines; Review Loop section lines 256-264 | REP | L1658
211. VL-24-211 | defect | KNOWLEDGE -> KNOWLEDGE | The plugin mirror plugins/superclaude/commands/spec-panel.md is stale (18 changed lines, not 25: dif | REP | L4046
212. VL-24-212 | artifact | MODULE-spec -> MODULE-spec | A2 src/superclaude/rules/prompts/document_review_loop_prompts.md (74 lines) in src, installed (diff  | REP | L1659
213. VL-24-213 | artifact | CORE -> CORE | A3 variant skill sc-review-ledger (SKILL.md 118 lines, scripts/review_ledger.py 2668 lines) is insta | REP | L819
214. VL-24-214 | artifact | CORE -> CORE | A4 variant skill sc-spec-panel-stoprule-protocol (SKILL.md 65, scripts/stoprule.py 2050, refs/rubric | REP | L820
215. VL-24-215 | artifact | CORE -> CORE | A5 variant skill sc-diffgate (SKILL.md 59, scripts/diffgate.py 1740) installed-only; bundle builds/d | REP | L821
216. VL-24-216 | artifact | MODULE-spec -> MODULE-spec | A6 variant skill sc-fix-audit (SKILL.md 65, scripts/fix_audit.py 1131, refs/auditor-brief.md 58) ins | REP | L1660
217. VL-24-217 | defect | DROP -> DROP | A stray scripts/__pycache__/fix_audit.cpython-311.pyc sits in the installed sc-fix-audit skill | REP | L5908
218. VL-24-218 | artifact | CORE -> CORE | A7 agent finding-grader.md (35 lines; tools Read, model sonnet, maxTurns 10, permissionMode plan) in | REP | L822
219. VL-24-219 | artifact | MODULE-spec -> MODULE-spec | A8 command spec-panel-ledger.md (475 lines) installed-only (~/.claude/commands/sc/); bundle builds/l | REP | L1661
220. VL-24-220 | artifact | MODULE-spec -> MODULE-spec | A8 command spec-panel-stoprule.md (481 lines) installed-only; bundle copy under builds/stoprule/ | REP | L1662
221. VL-24-221 | artifact | MODULE-spec -> MODULE-spec | A8 command spec-panel-diffgate.md (481 lines) installed-only; bundle copy under builds/diffgate/ | REP | L1663
222. VL-24-222 | artifact | MODULE-spec -> MODULE-spec | A8 command spec-panel-ponytail.md (483 lines) installed-only; bundle copy under builds/ponytail/ | REP | L1664
223. VL-24-223 | artifact | EVAL -> EVAL | A8 command spec-panel-armb.md (472 lines) installed-only; found only under measurements/diffgate/rev | REP | L3113
224. VL-24-224 | defect | DROP -> DROP | A stale backup spec-panel.md.bak.20261111T164114Z sits in ~/.claude/commands/sc/ (28 changed lines v | REP | L5909
225. VL-24-225 | test | CORE -> CORE | A9 tests for the ledger variant live only in the bundle: test_review_ledger_script.py (1578 lines) a | REP | L823
226. VL-24-226 | test | CORE -> CORE | A9 tests for stoprule live only in the bundle: test_stoprule_script.py (1998) and test_spec_panel_st | REP | L824
227. VL-24-227 | test | CORE -> CORE | A9 tests for diffgate live only in the bundle: test_diffgate_script.py (1145) and test_spec_panel_di | REP | L825
228. VL-24-228 | test | MODULE-spec -> MODULE-spec | A9 tests for fix-audit live only in the bundle: test_fix_audit_script.py (1196) and test_spec_panel_ | REP | L1665
229. VL-24-229 | test | DROP -> DROP | A9 minfix test test_sc_fixcheck.py (1069 lines) in the bundle (7909 lines of variant tests in total, | REP | L5910
230. VL-24-230 | finding | KNOWLEDGE -> KNOWLEDGE | Tracked archive footprint: .dev/experiments/346-validation/phase5 1997 files, .dev/experiments/346-v | REP | L4047
231. VL-24-231 | defect | CORE -> CORE | CONSEQUENCE: the variant skills, commands and agent exist as product source nowhere in src/superclau | REP | L826
232. VL-24-232 | finding | MODULE-spec -> MODULE-spec | Variant commands are small diffs of base spec-panel.md: changed-line counts ledger 51, stoprule 69,  | REP | L1666
233. VL-24-233 | finding | EVAL -> EVAL | spec-panel-armb.md = control arm B with pre-#478 Review Loop wording: bullet 2 "MAJOR blocking only  | REP | L3114
234. VL-24-234 | finding | CORE -> CORE | superclaude review CLI on this branch: slice lists 15 modules and states 5131 lines (panel 707, mani | REP | L827
235. VL-24-235 | requirement | MODULE-spec -> MODULE-spec | B1 loop scope: --mode critique only; re-review needs --re-review plus --baseline, otherwise a first  | REP | L1667
236. VL-24-236 | requirement | CORE -> CORE | B2 provenance: header records SHA-256 of candidate and baseline and "the reviewer model actually use | REP | L828
237. VL-24-237 | requirement | CORE -> CORE | B3 grading by consequence: CRITICAL blocking; MAJOR or FR-8/FR-9 blocking only with "a concrete wron | REP | L829
238. VL-24-238 | requirement | MODULE-spec -> MODULE-spec | B4 grading check sentence "An implementer who follows the stated text as written builds X, and X is  | REP | L1668
239. VL-24-239 | requirement | CORE -> CORE | B5 verdict: last line verdict: PASS or verdict: FAIL; a missing or ambiguous final verdict, a re-rev | REP | L830
240. VL-24-240 | requirement | CORE -> CORE | B6 cap: 2 fix cycles and 3 reviews, header review: N of 3, prior review: 3 plus FAIL = HALT and esca | REP | L831
241. VL-24-241 | requirement | CORE -> CORE | B7 re-review output: prior-findings table resolved/open/regressed, then findings on changed lines (o | REP | L832
242. VL-24-242 | requirement | CORE -> CORE | B8 reviser contract: Reviser brief above the final verdict listing only blocking ids, omitted at rev | REP | L833
243. VL-24-243 | requirement | CORE -> CORE | B9 precedence: a brief may narrow, never widen; never "apply all findings", never grade minor as blo | REP | L834
244. VL-24-244 | requirement | CORE -> CORE | B10 rf-qa coupling: spec-panel.md l.262 says the re-check of prior blocking findings follows steps 1 | REP | L835
245. VL-24-245 | requirement | MODULE-spec -> MODULE-spec | B11 hard gate (spec-panel.md l.266-268): read ~/.claude/rules/prompts/document_review_loop_prompts.m | REP | L1669
246. VL-24-246 | requirement | CORE -> CORE | B12 findings block (prompts l.56-62): ## Findings block, fence info string findings-v1, one JSON obj | REP | L836
247. VL-24-247 | requirement | CORE -> CORE | B13 fix map (prompts l.64-66): ## Fix map, fence fixmap-v1, {"id","action":"applied/rejected","reaso | REP | L837
248. VL-24-248 | requirement | CORE -> CORE | B14 review panel paragraph (prompts l.68-70): reviewers from superclaude review panel resolve --run- | REP | L838
249. VL-24-249 | conflict | CORE -> CORE | B15 two different ledgers collide in name: CLI schema review-ledger/1 (ledger.py l.17) with statuses | REP | L839
250. VL-24-250 | requirement | CORE -> CORE | B16 docs/reference/review-panel-live7.md l.1-45 defines @live7 = 7 reviewers (t1b fixed 1, t2 random | REP | L840
251. VL-24-251 | finding | EVAL -> EVAL | B16 numeric claims of the doc: "1 Sonnet + 6 Haiku" fixes 19.3 and 17.7 of 44 per run vs 15.7 and 15 | REP | L3115
252. VL-24-252 | defect | CORE -> CORE | B17 lint_cmd and estimate_cmd are registered as optional modules in cli/review/__init__.py l.18-28 b | REP | L841
253. VL-24-253 | finding | MODULE-spec -> MODULE-spec | B18 existing consumers of the loop: only /sc:spec-panel; sc-reflect-protocol/SKILL.md and tests/cli/ | REP | L1670
254. VL-24-254 | requirement | CORE -> CORE | Gap: the master loop has no lens/role concept (experts are simulated personas in spec-panel.md l.49- | REP | L842
255. VL-24-255 | requirement | MODULE-pr-review -> MODULE-pr-review | Gap: no PR-code location type (file+line) in the master loop | REP | L1723
256. VL-24-256 | requirement | MODULE-tasklist -> MODULE-tasklist | Gap: no tasklist location type (task id plus roadmap id) in the master loop | REP | L1598
257. VL-24-257 | requirement | CORE -> CORE | Owner ruling common to all variants (issue #346): review and reviser sessions run only calls that wr | REP | L843
258. VL-24-258 | strategy | CORE -> CORE | C1 ledger idea: "find once at review 1, then only verify ledger rows at reviews 2 and 3, one sweep a | REP | L844
259. VL-24-259 | script | CORE -> CORE | C1 review_ledger.py (2668 lines) has 11 subcommands (init 730, find 912, answer 1095, revert-unclaim | REP | L845
260. VL-24-260 | requirement | CORE -> CORE | C1 state ledger.json keys schema, profile, doc, cap_reviews, round, fix_cycles, phase, seq, snapshot | REP | L846
261. VL-24-261 | defect | CORE -> CORE | C1 profile mechanism: PROFILES["spec-panel"] grades CRITICAL/MAJOR/MINOR, blocking = grade == CRITIC | REP | L847
262. VL-24-262 | requirement | CORE -> CORE | C1 loop decision: ESCALATE if not I or X > 0; PASS if U == 0; CONTINUE if k < 3; else ESCALATE (SKIL | REP | L848
263. VL-24-263 | requirement | MODULE-spec -> MODULE-spec | C1 location type: anchor must occur exactly once in snapshots/r<k>.md (whitespace-normalised); hunks | REP | L1671
264. VL-24-264 | requirement | CORE -> CORE | C1 exit codes 0,1,2,3,4 plus verdict exits 0 PASS / 10 CONTINUE / 11 ESCALATE / 12 PENDING (script l | REP | L849
265. VL-24-265 | requirement | CORE -> CORE | C1 owner counting rule (SKILL l.117, DECISIONS D14 l.74 (1), L9): a deferred, demoted, withdrawn or  | REP | L850
266. VL-24-266 | finding | EVAL -> EVAL | C1 measured: new CRITICAL+MAJOR labels per review 13 / 9 / 3, final 70,565 bytes, 22.16% growth, ESC | REP | L3116
267. VL-24-267 | requirement | CORE -> CORE | C1 needs from a core: finding rows with frozen fields, snapshots per round, hunk diff engine, status | REP | L851
268. VL-24-268 | strategy | CORE -> CORE | C2 stoprule idea: the reviewer never writes a verdict; stoprule.py computes it from a sealed claim l | REP | L852
269. VL-24-269 | script | CORE -> CORE | C2 stoprule.py (2050 lines) has 14 subcommands (begin 401, seal 517, grade-prep 769, apply-grades 83 | REP | L853
270. VL-24-270 | requirement | CORE -> CORE | C2 ledger is a fenced stoprule-ledger JSON-lines block in the report; the reviewer writes only kinds | REP | L854
271. VL-24-271 | requirement | CORE -> CORE | C2 claim schema (SKILL l.41): claimed critical/major/minor, quote (20-300 non-space chars, unique),  | REP | L855
272. VL-24-272 | requirement | MODULE-spec -> MODULE-spec | C2 rubric v1: BLOCKING needs B1 quote, B2 concrete outcome, B3 kind among (a) contradiction (b) sour | REP | L1672
273. VL-24-273 | requirement | CORE -> CORE | C2 failure table (SKILL l.50-57): grader reply invalid twice or Agent tool unavailable gives claims  | REP | L856
274. VL-24-274 | defect | CORE -> CORE | C2 live-trial defect: the verify-transcript extractor recognises only Agent/Task tool_use/tool_resul | REP | L857
275. VL-24-275 | finding | EVAL -> EVAL | C2 measured: review 1 only, "6 machine-confirmed blockers from 8 sealed claims", no completed loop ( | REP | L3117
276. VL-24-276 | requirement | CORE -> CORE | C2 needs from a core: blind independent heterogeneous grader, sealed claim format, rubric hashing, v | REP | L858
277. VL-24-277 | strategy | CORE -> CORE | C3 diffgate idea: compute the re-review surface from the diff, require a machine-readable ## Diffgat | REP | L859
278. VL-24-278 | script | CORE -> CORE | C3 diffgate.py (1740 lines) has 4 subcommands (begin 1108, check 1304, fixcheck 1394, status 1471);  | REP | L860
279. VL-24-279 | requirement | CORE -> CORE | C3 exit codes 0..6 (SKILL l.34): 4 loop closed (halt: pass/escalate/invalid), 5 steps out of order,  | REP | L861
280. VL-24-280 | requirement | CORE -> CORE | C3 finding grammar: ids R<N>.<j>; location at=<line or a-b> of doc-r<N>.md, hunk=H<k>.<n> or via=H<k | REP | L862
281. VL-24-281 | finding | EVAL -> EVAL | C3 measured: 7 / 2 / 2 labels, final 63,717 bytes (frozen snapshot), 10.31% growth vs control mean 6 | REP | L3118
282. VL-24-282 | requirement | CORE -> CORE | C3 needs from a core: change-surface computation (diff plus via), machine-checkable finding grammar, | REP | L863
283. VL-24-283 | strategy | MODULE-spec -> MODULE-spec | C4 ponytail/fix-audit idea: one audit per loop after cycle-2 fixes and before review 3 asks Q1 neces | REP | L1673
284. VL-24-284 | script | MODULE-spec -> MODULE-spec | C4 fix_audit.py (1131 lines): prepare 299, check 740, apply 772, verdict 992; checks K1-K10 on audit | REP | L1674
285. VL-24-285 | defect | MODULE-spec -> MODULE-spec | C4 dependency outside the repo: the auditor invokes Skill ponytail:ponytail-review (a plugin skill f | REP | L1675
286. VL-24-286 | finding | EVAL -> EVAL | C4 measured: 9 / 7 / 0 labels; endpoint 70,579 to 70,488 bytes after audit (91 bytes, 0.1575 percent | REP | L3119
287. VL-24-287 | defect | MODULE-spec -> MODULE-spec | C4 defect (1): cmd_verdict appends unparseable: no resolution table rows in the review-3 report when | REP | L1676
288. VL-24-288 | defect | MODULE-spec -> MODULE-spec | C4 defect (2): the spec is written by atomic_write(s, data) at l.877 BEFORE apply-log.md (l.898), cl | REP | L1677
289. VL-24-289 | requirement | MODULE-spec -> MODULE-spec | C4 needs from a core: an optional severity/necessity audit stage between fix cycle 2 and review 3, w | REP | L1678
290. VL-24-290 | finding | EVAL -> EVAL | C5 ARM B (/sc:spec-panel-armb) has no skill and no script; it is the control arm and exists only to  | REP | L3120
291. VL-24-291 | strategy | DROP -> DROP | C6 minfix (proposed, never built): budget-based fix limiter; build halted at task 3 of 8; "recorded  | REP | L5911
292. VL-24-292 | finding | CORE -> CORE | C7 matrix, who computes the verdict: master loop reviewer writes verdict: and merge CLI; ledger scri | REP | L864
293. VL-24-293 | finding | CORE -> CORE | C7 matrix, finding location: exact-text anchor 12-200 chars (master), anchor exactly once in snapsho | REP | L865
294. VL-24-294 | finding | CORE -> CORE | C7 matrix, severity vocabulary: CRITICAL/MAJOR/MINOR in every variant and SEVERITIES of the CLI; mas | REP | L866
295. VL-24-295 | finding | CORE -> CORE | C7 matrix, blocking rule: consequence sentence (master), grade==CRITICAL or FR-8/9 or MAJOR+wrong_ou | REP | L867
296. VL-24-296 | finding | CORE -> CORE | C7 matrix, re-review surface: changed lines plus prior blockers in prose (master), plan-r<k>.md rows | REP | L868
297. VL-24-297 | finding | CORE -> CORE | C7 matrix, fix-agent hand-off: Reviser brief with blocking ids (master), answer claims on provisiona | REP | L869
298. VL-24-298 | finding | CORE -> CORE | C7 matrix, cap: 3 reviews in master, ledger (CAP_REVIEWS), stoprule (--cap, exit 4) and diffgate (co | REP | L870
299. VL-24-299 | finding | DROP -> DROP | C7 matrix, where each lives: master in src (plus plugin mirror), variants in ~/.claude plus a .dev a | DEDUP of VL-24-231 | L5912
300. VL-24-300 | finding | EVAL -> EVAL | C8 provenance check (2026-11-14): sha256sum of all 17 installed variant files (5 commands, 1 agent,  | REP | L3121
301. VL-24-301 | finding | KNOWLEDGE -> KNOWLEDGE | C8 the base ~/.claude/commands/sc/spec-panel.md changed after the install: install-log l.2 records s | REP | L4048
302. VL-24-302 | finding | EVAL -> EVAL | ARM B text equals PR #427 exactly: diff of final-bundle/provenance/spec-panel-427.md (sha256 prefix  | REP | L3122
303. VL-24-303 | defect | MODULE-spec -> MODULE-spec | All five variants are built on the PR #427 base and lack the later master clauses: none contains fol | REP | L1679
304. VL-24-304 | defect | DROP -> DROP | Doc/code discrepancy: coordinator-log l.45 says all four variant commands gained a ## Activation hea | REP | L5913
305. VL-24-305 | open | KNOWLEDGE -> KNOWLEDGE | No REFACTOR-SPEC.md and no phase5/design-session/ exist in the repo; SNAPSHOT-STATE.txt l.3 says a f | REP | L4049
306. VL-24-306 | open | DROP -> DROP | Phase-5 files read by the slice: FINAL-REPORT.md (259 lines), SNAPSHOT-STATE.txt (3), DESIGN-BRIEF.m | REP | L5914
307. VL-24-307 | finding | EVAL -> EVAL | D1.1 headline: "PR 427 is not proven to make review loops converge. None of the completed, measured  | REP | L3123
308. VL-24-308 | finding | EVAL -> EVAL | D1.2 controls: last-review CRITICAL+MAJOR label count averaged 6 before 427 and 5.5 with it, require | REP | L3124
309. VL-24-309 | finding | EVAL -> EVAL | D1.3 flagged-427 arm: mean 3.5 last-review labels, improvement 2.5, larger proxy spread 5, growth pa | REP | L3125
310. VL-24-310 | finding | EVAL -> EVAL | D1.4 loop table (new CRITICAL+MAJOR labels at reviews 1/2/3, final bytes, baseline 57,763): Historic | REP | L3126
311. VL-24-311 | finding | EVAL -> EVAL | D1.5 residual measures (FINAL-REPORT l.113-121): diffgate new final label 2, unresolved prior 0, aud | REP | L3127
312. VL-24-312 | threshold | EVAL -> EVAL | D1.6 screen thresholds: control mean final proxy 6 (limit 3), control mean growth 63.51% (limit 44.4 | REP | L3128
313. VL-24-313 | risk | EVAL -> EVAL | D1.7 validity: single scenario (Orca worker-contract spec, 57,763 bytes, base commit 2cb683f5c1f0dfb | REP | L3129
314. VL-24-314 | finding | EVAL -> EVAL | D1.8 4 of 5 historical incidents used review tools other than spec-panel (S2 /sc:reflect pre, S3 pla | REP | L3130
315. VL-24-315 | lesson | CORE -> CORE | L1 limit revisions to confirmed blocking defects and explicitly authorized edits ("Reuse 427's exist | REP | L871
316. VL-24-316 | lesson | CORE -> CORE | L2 track finding identity, disposition and changed anchors mechanically (diffgate fix maps, ledger r | REP | L872
317. VL-24-317 | lesson | MODULE-spec -> MODULE-spec | L3 optional bounded severity/necessity audit before the final review with explicit edit consent and  | REP | L1680
318. VL-24-318 | lesson | CORE -> CORE | L4 honest final coverage statement: a scoped PASS must not imply whole-document safety, any separate | REP | L873
319. VL-24-319 | lesson | CORE -> CORE | L5 parsing and provenance fail closed (ponytail parser and stoprule transcript check failed on real  | REP | L874
320. VL-24-320 | decision | KNOWLEDGE -> KNOWLEDGE | L6 report's stance: do not ship a combined variant as a proven convergence fix; do not finish minfix | REP | L4050
321. VL-24-321 | requirement | EVAL -> EVAL | L7 refactor spec must retain 6 items (FINAL-REPORT l.183-190): 3 reviews and 2 fix cycles; separate  | REP | L3131
322. VL-24-322 | requirement | EVAL -> EVAL | L8 future validation must use the same instrument in every arm, preserve model continuity, validate  | REP | L3132
323. VL-24-323 | requirement | CORE -> CORE | L10 owner rule: a flag in the brief counts as consent for one scripted edit or revert (DECISIONS D14 | REP | L875
324. VL-24-324 | risk | HARNESS -> HARNESS | L11 machine fact (DECISIONS D9 l.46, probe V1 in two replicates): personal ~/.claude/commands/sc/<cm | REP | L3617
325. VL-24-325 | risk | HARNESS -> HARNESS | L12 environment-drift confounds: WORKER-CONTRACT.md present in phase 5 but absent in control arms; a | REP | L3618
326. VL-24-326 | defect | CORE -> CORE | L13 model continuity failed: ponytail final review requested claude-opus-5-5 but recorded gpt-6.1-so | REP | L876
327. VL-24-327 | finding | EVAL -> EVAL | Build stage: five teams built on origin/master 0423fe5f (DECISIONS D13); spec lengths ponytail 332,  | REP | L3133
328. VL-24-328 | finding | EVAL -> EVAL | Build results: diffgate 12/12 tasks 86 new tests, stoprule 14/14 92, ledger 12/12 104, ponytail 12/1 | REP | L3134
329. VL-24-329 | finding | EVAL -> EVAL | Build caveat: stoprule control-r1 replay gives 8 anchored / 0 late-found, not the 5/3 its spec predi | REP | L3135
330. VL-24-330 | open | EVAL -> EVAL | Build caveat: stoprule grader, canaries and PASS-time audit "never run against a live model" at buil | REP | L3136
331. VL-24-331 | defect | KNOWLEDGE -> KNOWLEDGE | Builder protocol slips: adviser answer saved before adviser B returned; a helper deleted a sweep ref | REP | L4051
332. VL-24-332 | finding | EVAL -> EVAL | Planning-stage /sc:reflect advisory results on the five variant plans: minfix FAIL 4 blocking (M-F1. | REP | L3137
333. VL-24-333 | strategy | HARNESS -> HARNESS | Variant mechanism: the variants copy the 472-line Arm B file byte for byte and use command-token sub | REP | L3619
334. VL-24-334 | requirement | KNOWLEDGE -> KNOWLEDGE | A ## Activation heading (+2 lines) was added to satisfy make lint-architecture Check 6 (coordinator- | REP | L4052
335. VL-24-335 | defect | MODULE-spec -> MODULE-spec | Variants omit the Unattended section (matches the 472-line arm file), so no variant supports --unatt | REP | L1681
336. VL-24-336 | risk | KNOWLEDGE -> KNOWLEDGE | Stalls: minfix implement stalled on API errors at 19:32Z and 22:32Z (coordinator-log l.44, l.51); "R | REP | L4053
337. VL-24-337 | defect | KNOWLEDGE -> KNOWLEDGE | Authorization defect: the first-run independent review returned FAIL on one blocking issue: repeat-p | REP | L4054
338. VL-24-338 | open | EVAL -> EVAL | Four exploratory first-review reports and one automatically launched reviser exist under final-bundl | REP | L3138
339. VL-24-339 | defect | HARNESS -> HARNESS | Fidelity review issue 3: SHA256SUMS lists 192 measurement files but none of the 30 ledger files nor  | REP | L3620
340. VL-24-340 | defect | EVAL -> EVAL | Fidelity review minor notes: rounded control mean (issue 2), asymmetric limit presentation (issue 4: | REP | L3139
341. VL-24-341 | lesson | HARNESS -> HARNESS | Lesson for any panel program: an orchestrator must not self-authorise follow-up runs; its own claim  | REP | L3621
342. VL-24-342 | open | EVAL -> EVAL | Open D5.1: which of diffgate's diff enforcement, fewer minor edits or run variation caused its 10.31 | REP | L3140
343. VL-24-343 | open | EVAL -> EVAL | Open D5.2: whether any audit or sweep finding is independent of the endpoint blockers (overlap uncer | REP | L3141
344. VL-24-344 | open | EVAL -> EVAL | Open D5.3: whether a bounded severity audit has any causal effect (ponytail: 91 bytes) | REP | L3142
345. VL-24-345 | open | EVAL -> EVAL | Open D5.4: whether stoprule's blind grader works live (the integrity check failed at transport, not  | REP | L3143
346. VL-24-346 | open | EVAL -> EVAL | Open D5.5: whether the owner wants the refactor spec (never produced) and the paused repeats (paused | REP | L3144
347. VL-24-347 | risk | CORE -> CORE | Plugin-mirror state (checked 2026-11-14): plugins/superclaude/skills/ holds only confidence-check, s | REP | L877
348. VL-24-348 | finding | DROP -> DROP | E1 /sc:workflow (SKILL.md 107 lines, refs/quality-gates.md 41) Wave 3 local schema gate (SKILL l.79- | REP | L5915
349. VL-24-349 | finding | MODULE-tasklist -> MODULE-tasklist | E1 Wave 4 (l.85-93): codegraph pre-check (advisory, ## Pre-check in <pkg>/artifacts/codegraph-ground | REP | L1599
350. VL-24-350 | requirement | MODULE-tasklist -> MODULE-tasklist | E1 result recorded as reflect_status / reflect_report_path in return-contract.yaml contract 1.1 (l.8 | REP | L1600
351. VL-24-351 | requirement | MODULE-tasklist -> MODULE-tasklist | E1 advisory rule: "never edit, delete, or regenerate <id>.md from findings, and never change the wor | REP | L1601
352. VL-24-352 | finding | MODULE-tasklist -> MODULE-tasklist | E1 has no review loop, no fix agent and no cap of its own: the single reflect call is the whole revi | REP | L1602
353. VL-24-353 | requirement | MODULE-tasklist -> MODULE-tasklist | E1 plug-in point: swap or wrap the Wave 4 reflect call with a panel kind "plan-vs-spec"; contract ke | REP | L1603
354. VL-24-354 | requirement | MODULE-tasklist -> MODULE-tasklist | E1 needs from a core: spec-vs-tasklist coverage lens; location type = task id / source requirement i | REP | L1604
355. VL-24-355 | finding | MODULE-tasklist -> MODULE-tasklist | E1 has no severity vocabulary or blocking rule of its own (adopts reflect's; advisory) | REP | L1605
356. VL-24-356 | defect | CORE -> CORE | E1 plan-review reflect findings use heterogeneous id schemes (M-F1, C-003, F-01, QA-001, INV-001) | REP | L878
357. VL-24-357 | finding | MODULE-tasklist -> MODULE-tasklist | E2 /sc:tasklist (src/superclaude/skills/sc-tasklist-protocol/SKILL.md 1798 lines; templates 153 + 20 | REP | L1606
358. VL-24-358 | finding | MODULE-tasklist -> MODULE-tasklist | T1 Stage 6 Self-Check (20 structural checks) plus gate-results.txt (l.1275-1277 checks 18-20; inline | REP | L1607
359. VL-24-359 | finding | MODULE-tasklist -> MODULE-tasklist | T2 Stage 7 Roadmap Validation: 2N parallel agents (Task/Agent), split = ceil(task_count / 2) per pha | REP | L1608
360. VL-24-360 | requirement | MODULE-tasklist -> MODULE-tasklist | T2 finding fields Severity High/Medium/Low, Task ID T<PP>.<TT>, Problem, Roadmap evidence, Tasklist  | REP | L1609
361. VL-24-361 | finding | MODULE-tasklist -> MODULE-tasklist | T2 orchestrator merge: collect, dedup same issue same task, sort High first (l.1410-1412) | REP | L1610
362. VL-24-362 | requirement | CORE -> CORE | DNSP synthetic finding for a failed reviewer (tasklist l.1400-1409; same in rf-qa F1.7: DM-003 7-fie | REP | L879
363. VL-24-363 | finding | MODULE-tasklist -> MODULE-tasklist | T2 is a hand-rolled 2-agent-per-phase panel with homogeneous agents (no model diversity) and lens =  | REP | L1611
364. VL-24-364 | finding | MODULE-tasklist -> MODULE-tasklist | T3 Stages 8-10 patch loop: PatchChecklist (l.1435-1533) to sc:task --compliance strict delegation (l | REP | L1612
365. VL-24-365 | conflict | CORE -> CORE | T3 P2 bounded loop: "at most ONE re-patch pass (2 TOTAL passes ... NOT task-builder's 3-cap)" (l.160 | REP | L880
366. VL-24-366 | requirement | CORE -> CORE | T3 halt strings Regression detected on Item X.Y -- previously PASS at cycle N, now FAIL. Halt overri | REP | L881
367. VL-24-367 | conflict | CORE -> CORE | T3 blocking = High + Medium (l.1537, l.1567), Low = notes, unresolved High/Medium at termination HAL | REP | L882
368. VL-24-368 | finding | MODULE-tasklist -> MODULE-tasklist | T4 Stage 10.5 Pre-Reflect Sign-off (l.1619-1646): one /sc:reflect --mode pre --remediate --tasklist  | REP | L1613
369. VL-24-369 | requirement | MODULE-tasklist -> MODULE-tasklist | T4 verdicts recorded per phase as reflect_pre: PASS (depth=<d>, coverage=<pct>); the bundle ships re | REP | L1614
370. VL-24-370 | requirement | MODULE-tasklist -> MODULE-tasklist | T4 per-phase depth from deterministic COMPLEXITY_SCORE = 3*n_strict + 3*n_cpo + 2*n_high_risk + 1*ce | REP | L1615
371. VL-24-371 | finding | MODULE-tasklist -> MODULE-tasklist | T5 per-phase post-execution gate: terminal task T<PP>.<final> -- Post-Execution Reflection appended  | REP | L1616
372. VL-24-372 | requirement | MODULE-tasklist -> MODULE-tasklist | T5 the gate also FAILs at exit 0 if the contract's derived reflect_post.verdict != pass, adversarial | REP | L1617
373. VL-24-373 | requirement | CORE -> CORE | T5 executor_model_class from phase frontmatter is excluded from the reviewer pool (l.1165, l.1177):  | REP | L883
374. VL-24-374 | requirement | MODULE-reflect -> MODULE-reflect | superclaude reflect run verdict exit codes "pass 0 / halted 10 / degraded 11 / blocked 2" (src/super | REP | L1258
375. VL-24-375 | requirement | MODULE-reflect -> MODULE-reflect | Constants a unified core must reproduce or alias: reflect --depth quick/standard/deep, --tier 1/2/au | REP | L1259
376. VL-24-376 | requirement | MODULE-tasklist -> MODULE-tasklist | Tasklist index metadata reflect_pre_summary: {pass, partial, fail} (l.1640), index column "Pre-Refle | REP | L1618
377. VL-24-377 | requirement | MODULE-tasklist -> MODULE-tasklist | E2 plug-in (a): replace T2 plus T3 with one panel review of tasklist-vs-roadmap using the 5 dimensio | REP | L1619
378. VL-24-378 | requirement | MODULE-reflect -> MODULE-reflect | E2 plug-in (b): T4 and T5 already call reflect, so the panel enters through reflect Tier 2 (E1), not | REP | L1260
379. VL-24-379 | requirement | MODULE-tasklist -> MODULE-tasklist | E2 needs from the core: lenses = the 5 Stage-7 dimensions; location type task id T<PP>.<TT> plus roa | REP | L1620
380. VL-24-380 | open | DROP -> DROP | The tasklist CLI wrapper src/superclaude/cli/tasklist exists but was not read; E2's branch (tasklist | REP | L5916
381. VL-24-381 | finding | MODULE-spec -> MODULE-spec | E3 /sc:brainstorm (SKILL.md 462 lines, refs 170 + 240 + 222) has no reviewer on its output: Wave 3 d | REP | L1682
382. VL-24-382 | finding | MODULE-spec -> MODULE-spec | E3 Wave 4 handoff (l.322-355): none/design/tasklist/task; design is print-only (l.334); tasklist nee | REP | L1683
383. VL-24-383 | finding | MODULE-spec -> MODULE-spec | E3 has no panel-shaped step between merge and handoff; zero grep matches for spec-panel, reflect or  | REP | L1684
384. VL-24-384 | requirement | MODULE-spec -> MODULE-spec | E3 plug-in point: a new Wave 3.5 "spec review" over merged-requirements.md between Wave 3 PASS/PARTI | REP | L1685
385. VL-24-385 | requirement | MODULE-spec -> MODULE-spec | E3 needs from the core: spec-document review kind (loop contract B1-B14 fits); fixed output location | REP | L1686
386. VL-24-386 | finding | KNOWLEDGE -> KNOWLEDGE | The brainstorm skill is also the mechanism of the five #346 variant "brainstorm teams" (DECISIONS D1 | REP | L4055
387. VL-24-387 | finding | MODULE-spec -> MODULE-spec | E4 /sc:design (src/superclaude/commands/design.md 149 lines; plugin mirror differs) has no external  | REP | L1687
388. VL-24-388 | requirement | MODULE-spec -> MODULE-spec | E4 plug-in point: after Document (new step 6) or an opt-in --review handing the written design file  | REP | L1688
389. VL-24-389 | open | DROP -> DROP | DESIGN-BRIEF.md (phase5 l.28) intended to run Skill sc:design ... --type component --format spec --o | DEDUP of VL-24-305 | L5917
390. VL-24-390 | requirement | MODULE-spec -> MODULE-spec | E4 needs from the core: design-document review kind = spec kind plus architecture lenses (layering,  | REP | L1689
391. VL-24-391 | artifact | MODULE-pr-review -> MODULE-pr-review | E5 /sc:pr-submit (src/superclaude/pr_submit/ 6511 lines in 12 modules; skill sc-pr-submit-protocol 3 | REP | L1724
392. VL-24-392 | finding | MODULE-pr-review -> MODULE-pr-review | E5 reviewers are EXTERNAL bots only: REVIEWERS = ("augment", "codex") (reviewers.py l.41), Codex hin | REP | L1725
393. VL-24-393 | requirement | MODULE-pr-review -> MODULE-pr-review | E5 finding model (models.py l.168-207): path, line, body, severity_hint, category, confidence, in_di | REP | L1726
394. VL-24-394 | requirement | MODULE-pr-review -> MODULE-pr-review | E5 severity: 5 tiers CRITICAL, HIGH, MEDIUM, LOW, NIT (models.py l.106-113) re-graded by remap_sever | REP | L1727
395. VL-24-395 | requirement | MODULE-pr-review -> MODULE-pr-review | E5 FSM: DEFAULT_MAX_ROUNDS = 2, HARD_CAP_MAX_ROUNDS = 5 (fsm.py l.32-33, --max-rounds above 5 is an  | REP | L1728
396. VL-24-396 | conflict | CORE -> CORE | Cap vocabulary conflict (a unit difference more than a numeric one: research/12 s4 and :219 find mos | REP | L884
397. VL-24-397 | finding | MODULE-pr-review -> MODULE-pr-review | E5 fix agent: /sc:troubleshoot (Skill sc:troubleshoot-protocol) seeded by seed_troubleshoot (fsm.py  | REP | L1729
398. VL-24-398 | requirement | MODULE-pr-review -> MODULE-pr-review | E5 plug-in point: add a third reviewer kind "panel" next to augment/codex in reviewers.py, or reuse  | REP | L1730
399. VL-24-399 | requirement | MODULE-pr-review -> MODULE-pr-review | E5 needs from the core: file+line location with in_diff, original_line, is_outdated; category from t | REP | L1731
400. VL-24-400 | finding | MODULE-pr-review -> MODULE-pr-review | E6 /sc:auggie-review (SKILL.md 402 lines; refs severity-rubric 172, remediation-handoff 161, auggie- | REP | L1732
401. VL-24-401 | requirement | MODULE-pr-review -> MODULE-pr-review | E6 severity: five tiers with decision meaning (severity-rubric.md l.11-61): Critical blocks merge, H | REP | L1733
402. VL-24-402 | finding | MODULE-pr-review -> MODULE-pr-review | E6 remediation chain (remediation-handoff.md l.5-9, l.24-133): Phase A /sc:design --format spec, B s | REP | L1734
403. VL-24-403 | requirement | MODULE-pr-review -> MODULE-pr-review | E6 plug-in point: Wave 2 (Auggie pass) as one reviewer among panel members, Wave 3 as the merge/vali | REP | L1735
404. VL-24-404 | requirement | MODULE-pr-review -> MODULE-pr-review | E6 needs from the core: code-review kind; diff-locality (in_diff); category floor/ceiling; no-nits r | REP | L1736
405. VL-24-405 | conflict | MODULE-rfqa -> MODULE-rfqa | E7 /sc:implement review per task by ONE reviewer: "One reviewer per review; never 2+ reviewer agents | REP | L1761
406. VL-24-406 | requirement | CORE -> CORE | E7 severity blocking/minor/note is DERIVED by the parent from four yes/no checklist answers (ac-outc | REP | L885
407. VL-24-407 | finding | MODULE-rfqa -> MODULE-rfqa | E7 after all tasks, for legacy sources with N>1, one independent FINAL reviewer pass vs the full spe | REP | L1762
408. VL-24-408 | finding | CORE -> CORE | E8 prior art for lenses: src/superclaude/cli/swarm/ LENSES registry (lenses/__init__.py l.1-72) with | REP | L886
409. VL-24-409 | finding | CORE -> CORE | E8 sc-bare-review/SKILL.md (80 lines) is "a thin caller over superclaude swarm run --lens bare-revie | REP | L887
410. VL-24-410 | defect | CORE -> CORE | The review CLI templates have no role, lens or brief field: slot keys in review-panel.default.json a | REP | L888
411. VL-24-411 | open | DROP -> DROP | sc-review-translation-protocol (228 lines) is a domain-specific review skill with its own scoring; n | REP | L5918
412. VL-24-412 | finding | MODULE-rfqa -> MODULE-rfqa | F1.1 rf-qa.md (551 lines) frontmatter: memory: project, permissionMode: bypassPermissions, tools inc | REP | L1763
413. VL-24-413 | requirement | MODULE-rfqa -> MODULE-rfqa | F1.2 spawn prompt contract: QA phase (research-gate, synthesis-gate, report-validation, task-integri | REP | L1764
414. VL-24-414 | requirement | MODULE-rfqa -> MODULE-rfqa | F1.3 checklists: research gate 10 items (l.150), synthesis gate 12 (l.196), report validation 19 (l. | REP | L1765
415. VL-24-415 | requirement | MODULE-rfqa -> MODULE-rfqa | F1.4 severity CRITICAL/IMPORTANT/MINOR; "Review severity rule" l.106-111: blocking vs minor graded b | REP | L1766
416. VL-24-416 | requirement | MODULE-rfqa -> MODULE-rfqa | F1.5 verdict PASS/FAIL per report; output # QA Report with Items Reviewed table (check, PASS/FAIL, e | REP | L1767
417. VL-24-417 | requirement | CORE -> CORE | F1.6 fix cycle phase (l.381-418): read the previous QA report, verify each blocking fix applied and  | REP | L889
418. VL-24-418 | requirement | MODULE-rfqa -> MODULE-rfqa | F1.7 partitioning: the orchestrator partitions when "typically >6 files"; DNSP and cohort machinery  | REP | L1768
419. VL-24-419 | requirement | MODULE-rfqa -> MODULE-rfqa | F1.8 confidence gate: confidence = VERIFIED / (TOTAL - UNVERIFIABLE) * 100; PASS needs at least 95%  | REP | L1769
420. VL-24-420 | requirement | MODULE-rfqa -> MODULE-rfqa | F1.9 verification principles incl. 0 "Independent stance: ... there is no minimum count" and 10 "Cal | REP | L1770
421. VL-24-421 | requirement | MODULE-rfqa -> MODULE-rfqa | F1.10 critical rule 1: never one-shot an output file (create the header, then append) (l.540) | REP | L1771
422. VL-24-422 | finding | MODULE-rfqa -> MODULE-rfqa | rf-qa-qualitative.md (1154 lines): 8 qualitative phase sections PRD (l.144), research report (l.244) | REP | L1772
423. VL-24-423 | finding | MODULE-rfqa -> MODULE-rfqa | rf-analyst.md (428 lines): completeness verification (8-item checklist l.117), cross-validation (l.2 | REP | L1773
424. VL-24-424 | requirement | MODULE-rfqa -> MODULE-rfqa | /task phase-gate QA (skills/task/SKILL.md l.188-286): agent-count floors by phase output size 6/8/10 | REP | L1774
425. VL-24-425 | requirement | MODULE-rfqa -> MODULE-rfqa | /task standard lenses: 4 structural (template conformance, internal consistency, evidence quality, c | REP | L1775
426. VL-24-426 | requirement | CORE -> CORE | /task consolidation into qa-phase-[N]-consolidated-findings.md with dedup and "highest severity when | REP | L890
427. VL-24-427 | requirement | CORE -> CORE | /task ONE fix agent (rf-qa fix_authorization: true) applies ALL blocking fixes and "No other agent m | REP | L891
428. VL-24-428 | requirement | MODULE-rfqa -> MODULE-rfqa | /task verification round of at least 2 agents exempt from the 6-agent floor (l.256), max 2 fix cycle | REP | L1776
429. VL-24-429 | finding | MODULE-reflect -> MODULE-reflect | sc-reflect-protocol/SKILL.md l.632-633 lists rf-qa (UC-2 structural, fix_authorization: false, fallb | REP | L1261
430. VL-24-430 | strategy | HARNESS -> HARNESS | F2 census unit U1 = a line with a structured spawn parameter subagent_type: rf-<agent> (regex subage | REP | L3622
431. VL-24-431 | strategy | HARNESS -> HARNESS | F2 census unit U2 = a line in SKILL.md containing spawn/Spawn/SPAWN/subagent_type AND an rf-<agent>  | REP | L3623
432. VL-24-432 | finding | MODULE-rfqa -> MODULE-rfqa | U1 per skill (SKILL.md only): task-builder 23, roadmap 12, task 4, tdd 1, prd 1, tech-reference 1, t | REP | L1777
433. VL-24-433 | finding | MODULE-rfqa -> MODULE-rfqa | U1 in refs files adds 8 (tdd/refs/build-request-template.md 4, prd/refs/build-request-template.md 3, | REP | L1778
434. VL-24-434 | finding | MODULE-rfqa -> MODULE-rfqa | Total mentions of the eight rf-* names in SKILL.md: 623 across 10 files (roadmap 98, readme 108, ope | REP | L1779
435. VL-24-435 | finding | MODULE-rfqa -> MODULE-rfqa | U2 task-builder: qualitative 17, qa 22, analyst 8, family total 47; other rf-* spawn lines rf-task-b | REP | L1780
436. VL-24-436 | finding | MODULE-rfqa -> MODULE-rfqa | U2 tech-research: qualitative 18, qa 17, analyst 7, family total 42; rf-assembler 2, rf-task-builder | REP | L1781
437. VL-24-437 | finding | MODULE-rfqa -> MODULE-rfqa | U2 roadmap: qualitative 9, qa 12, analyst 12, family total 33; rf-task-builder 2, rf-task-researcher | REP | L1782
438. VL-24-438 | finding | MODULE-rfqa -> MODULE-rfqa | U2 readme: qualitative 4, qa 10, analyst 4, family total 18; rf-assembler 2, rf-task-builder 2, rf-t | REP | L1783
439. VL-24-439 | finding | MODULE-rfqa -> MODULE-rfqa | U2 operational-guide: qualitative 7, qa 6, analyst 2, family total 15; rf-assembler 3, rf-task-build | REP | L1784
440. VL-24-440 | finding | MODULE-rfqa -> MODULE-rfqa | U2 task: qualitative 6, qa 8, analyst 1, family total 15; no other rf-* spawn lines | REP | L1785
441. VL-24-441 | finding | MODULE-rfqa -> MODULE-rfqa | U2 tech-reference: qualitative 12, qa 2, analyst 1, family total 15; rf-assembler 3, rf-task-builder | REP | L1786
442. VL-24-442 | finding | MODULE-rfqa -> MODULE-rfqa | U2 prd: family total 0; rf-task-builder 3, rf-task-researcher 3 (reaches rf-qa only through the BUIL | REP | L1787
443. VL-24-443 | finding | MODULE-rfqa -> MODULE-rfqa | U2 tdd: family total 0; rf-task-builder 3, rf-task-researcher 3 (reaches rf-qa only through the BUIL | REP | L1788
444. VL-24-444 | finding | MODULE-rfqa -> MODULE-rfqa | Slice 12's family column sums to 185 (47+42+33+18+15+15+15) but that figure is NOT reproducible: [CO | REP | L1789
445. VL-24-445 | finding | MODULE-rfqa -> MODULE-rfqa | U1 per (skill, agent) for the QA family: roadmap rf-qa-qualitative 2, rf-qa 4, rf-analyst 7; task rf | REP | L1790
446. VL-24-446 | finding | MODULE-rfqa -> MODULE-rfqa | Interpretation: every rf-qa consumer is a document/artifact-production pipeline (research, synthesis | REP | L1791
447. VL-24-447 | risk | DROP -> DROP | Census not counted: spawn sites in src/superclaude/commands/*.md, refs files (except the 8 U1 hits), | REP | L5919
448. VL-24-448 | defect | MODULE-pr-review -> MODULE-pr-review | G1.1 location type: loop and CLI findings anchor on exact candidate TEXT (12-200 chars) (prompts l.6 | REP | L1737
449. VL-24-449 | defect | CORE -> CORE | G1.2 category vocabulary: 6 spec categories (contradiction, unpassable-check, data-loss, safety, mis | REP | L892
450. VL-24-450 | conflict | CORE -> CORE | G1.3 severity model: master loop CRITICAL/MAJOR/MINOR plus a derived non-blocking "Medium" warning;  | REP | L893
451. VL-24-451 | defect | MODULE-pr-review -> MODULE-pr-review | G1.4 blocking rule: the loop uses a consequence sentence; PR review has no verdict, only a route per | REP | L1738
452. VL-24-452 | conflict | DROP -> DROP | G1.5 round cap: 3 reviews/2 fix cycles vs DEFAULT_MAX_ROUNDS = 2, hard cap 5; each PR round is one p | DEDUP of VL-24-396 | L5920
453. VL-24-453 | defect | MODULE-pr-review -> MODULE-pr-review | G1.6 re-review surface: loop = changed lines vs --baseline file hash; PR = commit-based rereview_req | REP | L1739
454. VL-24-454 | defect | MODULE-pr-review -> MODULE-pr-review | G1.7 reviewer roles/lenses: panel templates carry model tiers only; a PR panel needs lens briefs (se | REP | L1740
455. VL-24-455 | conflict | CORE -> CORE | G1.8 fix hand-off: PR fix = /sc:troubleshoot --fix with seed {scope, issue, type, route}, per-file b | REP | L894
456. VL-24-456 | requirement | CORE -> CORE | G1.9 outward-action safety: the PR path posts comments, replies, resolves threads and pushes under t | REP | L895
457. VL-24-457 | finding | MODULE-pr-review -> MODULE-pr-review | G1.10 external-reviewer dependence: Augment and Codex are third-party bots detected on the PR (revie | REP | L1741
458. VL-24-458 | defect | CORE -> CORE | G1.11 evidence gate: pr-submit's evidence-validator agent confirms each finding's file:line (SKILL l | REP | L896
459. VL-24-459 | defect | DROP -> DROP | G1.12 plugin gap: pr_submit and its skill are not in the plugin mirror | DEDUP of VL-24-347 | L5921
460. VL-24-460 | risk | MODULE-pr-review -> MODULE-pr-review | G1.13 cost: repo CLAUDE.md says Auggie "is free and costs little to no tokens"; PR bots run outside  | REP | L1742
461. VL-24-461 | defect | MODULE-rfqa -> MODULE-rfqa | G2.1 rf-qa is read-write (fixes in place when fix_authorization is given, partitions files, writes i | REP | L1792
462. VL-24-462 | defect | MODULE-rfqa -> MODULE-rfqa | G2.2 rf-qa is checklist-driven, not finding-driven: 10/12/19/27-item checklists with PASS/FAIL per i | REP | L1793
463. VL-24-463 | defect | MODULE-rfqa -> MODULE-rfqa | G2.3 /task has eight named lenses and agent-count floors (6/8/10/12) while panel templates define re | REP | L1794
464. VL-24-464 | defect | MODULE-rfqa -> MODULE-rfqa | G2.4 orchestration inside skills: nine skills spawn rf-* agents (seven the QA family; prd and tdd on | REP | L1795
465. VL-24-465 | defect | CORE -> CORE | G2.5 synthetic-DNSP machinery (7-field contract, closed vocab, three-path guard, INV-012/021, R-126) | REP | L897
466. VL-24-466 | conflict | CORE -> CORE | G2.6 severity vocabulary CRITICAL/IMPORTANT/MINOR (+ HIGH synthetic) in rf-qa vs CRITICAL/MAJOR/MINO | REP | L898
467. VL-24-467 | defect | CORE -> CORE | G2.7 monotonicity/regression halts (byte-exact strings) exist in rf-qa l.403-418 and tasklist l.1610 | REP | L899
468. VL-24-468 | defect | MODULE-rfqa -> MODULE-rfqa | G2.8 document types: 8 qualitative review phases (PRD, report, TDD, tech-ref, ops-guide, README, tas | REP | L1796
469. VL-24-469 | risk | MODULE-rfqa -> MODULE-rfqa | G2.9 coupling in both directions: spec-panel Review Loop reuses rf-qa Fix Cycle steps 1-5 (B10) and  | REP | L1797
470. VL-24-470 | open | DROP -> DROP | G2.10 rf-qa's own tests were not examined; grep of tests/ for rf-qa behaviour was not run [UNVERIFIE | REP | L5922
471. VL-24-471 | requirement | CORE -> CORE | H need Lenses: spec-panel N (11 simulated experts in-prompt, spec-panel.md l.49-90), workflow N, tas | REP | L900
472. VL-24-472 | requirement | CORE -> CORE | H need Reviewer model diversity: spec Y (@live7, default 4), workflow P via reflect Tier 2, tasklist | REP | L901
473. VL-24-473 | requirement | CORE -> CORE | H need Roles (candidate/baseline/prior): spec Y (prompts l.39-43), tasklist P (--base single ref for | REP | L902
474. VL-24-474 | requirement | CORE -> CORE | H need Location type: spec exact-text anchor, workflow task id, tasklist T<PP>.<TT> + R-###, brainst | REP | L903
475. VL-24-475 | conflict | CORE -> CORE | H need Severity vocabulary: spec CRITICAL/MAJOR/MINOR, workflow reflect's, tasklist High/Medium/Low, | REP | L904
476. VL-24-476 | conflict | CORE -> CORE | H need Blocking rule: spec consequence sentence, workflow advisory only, tasklist High+Medium block, | REP | L905
477. VL-24-477 | conflict | CORE -> CORE | H need Cap: spec 3 reviews, workflow none (one call), tasklist 2 passes (P2), brainstorm none, desig | REP | L906
478. VL-24-478 | conflict | CORE -> CORE | H need Fix-agent hand-off: spec Reviser brief + fixmap-v1, workflow none, tasklist PatchChecklist to | REP | L907
479. VL-24-479 | requirement | CORE -> CORE | H need Templates/briefs: spec document_review_loop_prompts.md, workflow reflect's, tasklist Stage 7  | REP | L908
480. VL-24-480 | requirement | CORE -> CORE | H need Re-review surface: spec changed lines + prior blockers, tasklist full re-run of the Stage 7 s | REP | L909
481. VL-24-481 | requirement | CORE -> CORE | H need Headless / --unattended + return-contract: spec Y (spec-panel.md l.455-465), workflow Y, task | REP | L910
482. VL-24-482 | requirement | CORE -> CORE | H need Provenance (model actually used, hashes): spec Y (l.258), pr-submit P (review_id), all others | REP | L911
483. VL-24-483 | requirement | CORE -> CORE | H need Fail-closed on a missing/ambiguous report: spec Y (l.260), workflow P (reflect_status: failed | REP | L912
484. VL-24-484 | requirement | DROP -> DROP | H need Synthetic "reviewer failed" finding: tasklist Y (DNSP l.1400), rf-qa Y (DNSP rf-qa l.84), all | DEDUP of VL-24-362 | L5923
485. VL-24-485 | requirement | DROP -> DROP | H need Plugin/installed availability: spec plugin stale, workflow plugin ok, tasklist not in plugin, | DEDUP of VL-24-347 | L5924
486. VL-24-486 | conflict | DROP -> DROP | Conflict I1: "Medium" has four meanings [CODE-CONTRADICTED by research/12 s3 and :218: at least six  | DEDUP of VL-24-450 | L5925
487. VL-24-487 | conflict | DROP -> DROP | Conflict I2: caps differ [CODE-CONTRADICTED in the repo's own unit by research/12 s4 and :219: count | DEDUP of VL-24-396 | L5926
488. VL-24-488 | conflict | DROP -> DROP | Conflict I3: seven severity vocabularies in E3 alone [UNVERIFIED count: research/12 s2.2 and :67, :2 | DEDUP of VL-24-475 | L5927
489. VL-24-489 | conflict | CORE -> CORE | Conflict I4: who writes the verdict: master reviewer report ends verdict: PASS/FAIL with fail-closed | REP | L913
490. VL-24-490 | conflict | CORE -> CORE | Conflict I5: four machine-readable finding formats in E3: findings-v1 JSON lines (prompts l.58-62),  | REP | L914
491. VL-24-491 | conflict | DROP -> DROP | Conflict I6: two ledgers with the same job (CLI review-ledger/1 vs variant schema 1 with different s | DEDUP of VL-24-249 | L5928
492. VL-24-492 | conflict | DROP -> DROP | Conflict I7: unified panel vs sc:implement "No 6-agent panel" (qa.md l.11): exempt sc:implement or a | DEDUP of VL-24-405 | L5929
493. VL-24-493 | conflict | DROP -> DROP | Conflict I8: rf-qa fixes in place (fix_authorization) vs read-only panel reviewers and /task lens ag | DEDUP of VL-24-461 | L5930
494. VL-24-494 | conflict | DROP -> DROP | Conflict I9: variants built on the PR #427 text (472 lines, c8d80346a96c) while master has #478 and  | DEDUP of VL-24-303 | L5931
495. VL-24-495 | conflict | DROP -> DROP | Conflict I10: master loop depends on rf-qa Fix Cycle steps (spec-panel.md l.262) vs an rf-qa replace | DEDUP of VL-24-244 | L5932
496. VL-24-496 | conflict | DROP -> DROP | Conflict I11: DECISIONS D9 l.46 (a user copy of a command beats the project .claude copy) vs CLAUDE. | DEDUP of VL-24-324 | L5933
497. VL-24-497 | conflict | DROP -> DROP | Conflict I12: src spec-panel has --unattended etc. but plugins/superclaude/commands/spec-panel.md la | DEDUP of VL-24-211 | L5934
498. VL-24-498 | conflict | DROP -> DROP | Conflict I13: brainstorm convergence_score thresholds 0.65/0.50 vs review PASS/FAIL on blocking find | DEDUP of VL-24-385 | L5935
499. VL-24-499 | conflict | DROP -> DROP | Conflict I14: coordinator-log l.45 says all four variants have ## Activation but installed commands  | DEDUP of VL-24-304 | L5936
500. VL-24-500 | conflict | DROP -> DROP | Conflict I15: cli/review/__init__.py l.18-28 lists lint_cmd and estimate_cmd but the files do not ex | DEDUP of VL-24-252 | L5937
501. VL-24-501 | conflict | CORE -> CORE | Conflict I16: packaged default panel has 4 reviewers (default.json: tier1b 1 + tier2 1 + tier3 2) wh | REP | L915
502. VL-24-502 | conflict | DROP -> DROP | Conflict I17: repeat-plan l.3 (corrected) says PAUSED while the coordinator had claimed authorizatio | DEDUP of VL-24-337 | L5938
503. VL-24-503 | requirement | MODULE-pr-review -> MODULE-pr-review | J1 PR code review: first stress on the core is file+line anchors, diff locality, 18 categories, GitH | REP | L1743
504. VL-24-504 | requirement | MODULE-rfqa -> MODULE-rfqa | J2 rf-qa replacement: read-write agent semantics, checklists with computed confidence, lens packs, a | REP | L1798
505. VL-24-505 | requirement | MODULE-tasklist -> MODULE-tasklist | J3 tasklist review (Stage 7 + P2 + 10.5 + post gate): task-id locations, High/Medium/Low with Medium | REP | L1621
506. VL-24-506 | requirement | MODULE-spec -> MODULE-spec | J4 spec review of brainstorm output: needs a new Wave between 3 and 4; the convergence signal must s | REP | L1690
507. VL-24-507 | requirement | MODULE-spec -> MODULE-spec | J5 design review: needs a new step after Document and a headless return contract (E4) | REP | L1691
508. VL-24-508 | requirement | MODULE-rfqa -> MODULE-rfqa | J6 /sc:implement per-task and FINAL review: explicit no-panel rule, derive-severity-from-answers, an | REP | L1799
509. VL-24-509 | requirement | MODULE-tasklist -> MODULE-tasklist | J7 workflow plan review (Wave 4): keep the reflect_status / reflect_report_path contract keys (E1) | REP | L1622
510. VL-24-510 | requirement | MODULE-rfqa -> MODULE-rfqa | J8 roadmap validation and tdd/prd/tech-research/readme/ops-guide gates: all call rf-qa through task- | REP | L1800
511. VL-24-511 | requirement | CORE -> CORE | J9 variant revival (diffgate/ledger/stoprule/ponytail): rebase on the master base, one finding forma | REP | L916
512. VL-24-512 | requirement | HARNESS -> HARNESS | J10 cross-model experiments (E1 model combination): actual per-response model evidence, same instrum | REP | L3624
513. VL-24-513 | requirement | DROP -> DROP | J11 plugin installs: the plugin mirror carries only 4 skills and no rf agents; stale spec-panel | DEDUP of VL-24-347 | L5939
514. VL-24-514 | requirement | DROP -> DROP | J12 headless/orchestrated runs: --unattended plus return-contract.yaml plus WORKER-CONTRACT.md for n | DEDUP of VL-24-481 | L5940
515. VL-24-515 | test | MODULE-spec -> MODULE-spec | Test tests/skills/test_spec_panel_review_loop.py (174 lines; t1 usage line l.70, t2 section once bef | REP | L1692
516. VL-24-516 | test | MODULE-spec -> MODULE-spec | Test tests/skills/test_review_loop_extension.py (127 lines); presence/wording tests | REP | L1693
517. VL-24-517 | test | MODULE-spec -> MODULE-spec | Test tests/review/test_review_rules_text.py (92 lines); wording tests of the review rules text | REP | L1694
518. VL-24-518 | test | CORE -> CORE | Test tests/review/test_review_ledger.py (566 lines) for the CLI ledger | REP | L917
519. VL-24-519 | artifact | CORE -> CORE | Packaged templates in src/superclaude/cli/review/data/: review-panel.{default,live7,reflect-enterpri | REP | L918
520. VL-24-520 | strategy | DROP -> DROP | K1 Review Loop bullets 1-7 (spec-panel.md l.258-264): cap, fail-closed verdict, scoped-PASS statemen | DEDUP of VL-24-236 | L5941
521. VL-24-521 | strategy | DROP -> DROP | K2 document_review_loop_prompts.md (74 lines): the three briefs to the spec module, the roles table  | DEDUP of VL-24-212 | L5942
522. VL-24-522 | strategy | DROP -> DROP | K3 findings-v1 / fixmap-v1 (prompts l.56-66; cli/review/findings.py) to CORE; categories stay spec-s | DEDUP of VL-24-246 | L5943
523. VL-24-523 | strategy | CORE -> CORE | K4 the Medium warning tier plus follow-up candidates as a non-blocking tier in CORE; resolve the "Me | REP | L919
524. VL-24-524 | strategy | CORE -> CORE | K5 review_ledger.py (2668 lines) and SKILL.md: archive the script; CORE takes frozen row fields, sna | REP | L920
525. VL-24-525 | strategy | CORE -> CORE | K6 stoprule.py (2050), rubric (15), canaries (58), finding-grader.md (35): an optional "blind confir | REP | L921
526. VL-24-526 | strategy | CORE -> CORE | K7 diffgate.py (1740): archive the script; CORE takes the computed re-review surface (via, MERGE_GAP | REP | L922
527. VL-24-527 | strategy | DROP -> DROP | K8 fix_audit.py (1131) plus refs/auditor-brief.md: optional module or drop; if kept, fix the write-o | DEDUP of VL-24-216 | L5944
528. VL-24-528 | strategy | DROP -> DROP | K9 spec-panel-armb.md dropped as product; minfix package archived (84 tests passed but task 3 failed | DEDUP of VL-24-223 | L5945
529. VL-24-529 | strategy | DROP -> DROP | K10 FINAL-REPORT lessons L1-L13 are requirements for the core's acceptance criteria and for E1's exp | DEDUP of VL-24-315 | L5946
530. VL-24-530 | strategy | EVAL -> EVAL | K11 DECISIONS D6/D10-D14 bars and owner rulings: the experiment protocol for any future panel evalua | REP | L3145
531. VL-24-531 | requirement | EVAL -> EVAL | K12 phase-5 numbers table (FINAL-REPORT l.94-107, l.113-121): archive as evidence and cite only with | REP | L3146
532. VL-24-532 | artifact | DROP -> DROP | K13 final_report_check.py, final-summary.json, REPORT-STAGE-INVENTORY.sha256: archive; not run by th | REP | L5947
533. VL-24-533 | strategy | CORE -> CORE | K14 variant tests (7909 lines in the bundle): archive; port only the replay and tamper tests the kep | REP | L923
534. VL-24-534 | strategy | DROP -> DROP | K15 master tests (test_spec_panel_review_loop.py 174, test_review_loop_extension.py 127, test_review | DEDUP of VL-24-515 | L5948
535. VL-24-535 | strategy | DROP -> DROP | K16 /task lens gate (task SKILL l.188-286): 8 lenses, floors 6/8/10/12, consolidation, single fix ag | DEDUP of VL-24-424 | L5949
536. VL-24-536 | strategy | DROP -> DROP | K17 rf-qa confidence gate (l.484-534), monotonicity/regression halts (l.403-418), DNSP synthetic (l. | DEDUP of VL-24-362 | L5950
537. VL-24-537 | strategy | DROP -> DROP | K18 tasklist Stage 7 five dimensions, DNSP, P2 loop, Stage 10.5 depth formula, post gate: a tasklist | DEDUP of VL-24-359 | L5951
538. VL-24-538 | strategy | MODULE-pr-review -> MODULE-pr-review | K19 pr_submit Finding, severity_router category table, fix_key, dedup_groups, FSM: the code-review m | REP | L1744
539. VL-24-539 | strategy | DROP -> DROP | K20 auggie-review severity rubric (172 lines): the code-review severity module; pr-submit already im | DEDUP of VL-24-401 | L5952
540. VL-24-540 | strategy | DROP -> DROP | K21 sc-implement-protocol/refs/qa.md derive-severity-from-four-answers plus anchor read-back: an ide | DEDUP of VL-24-406 | L5953
541. VL-24-541 | strategy | DROP -> DROP | K22 brainstorm Wave 3 convergence thresholds: keep, separate from review (I13) | DEDUP of VL-24-381 | L5954
542. VL-24-542 | strategy | DROP -> DROP | K23 CLI review modules (15, 5131 lines), 9 packaged templates and docs/reference/review-panel-live7. | DEDUP of VL-24-234 | L5955
543. VL-24-543 | open | EVAL -> EVAL | K24 / Q5 installed-only artifacts (5 commands, 4 skills, 1 agent): archive and decide uninstall or k | REP | L3147
544. VL-24-544 | defect | DROP -> DROP | K25 stale plugin mirror plugins/superclaude/commands/spec-panel.md: fix with the core change (I12) | DEDUP of VL-24-211 | L5956
545. VL-24-545 | defect | DROP -> DROP | K26 INST/commands/sc/spec-panel.md.bak.20261111T164114Z and skills/sc-fix-audit/scripts/__pycache__: | DEDUP of VL-24-217 | L5957
546. VL-24-546 | strategy | DROP -> DROP | K27 operational lessons of the phase-5 run (section L) are requirements for any panel evaluation har | DEDUP | L5958
547. VL-24-547 | lesson | HARNESS -> HARNESS | Phase-5 lesson L1: rate limits stalled whole runs ("API429 all-credentials cooling-down" recurring f | REP | L3625
548. VL-24-548 | lesson | HARNESS -> HARNESS | Phase-5 lesson L2: elapsed time is not active time; recorders separate interruption windows; no cros | REP | L3626
549. VL-24-549 | lesson | CORE -> CORE | Phase-5 lesson L3: the scripted variants shifted much work onto a coordinator (begin/check/fixcheck/ | REP | L924
550. VL-24-550 | lesson | CORE -> CORE | Phase-5 lesson L4: brief-fill mistakes were found by the reviser itself (ledger T08 range "R18-R33"  | REP | L925
551. VL-24-551 | lesson | HARNESS -> HARNESS | Phase-5 lesson L5: installed files were watched by sampled hash monitors (20 s samples for 30 min, r | REP | L3627
552. VL-24-552 | lesson | HARNESS -> HARNESS | Phase-5 lesson L6: the diffgate live target was externally revised at 01:19Z (live sha 56b859139c1c  | REP | L3628
553. VL-24-553 | lesson | HARNESS -> HARNESS | Phase-5 lesson L7: exit-code semantics of orchestrated runs matter ("Driver exit13 faithfully repres | REP | L3629
554. VL-24-554 | lesson | KNOWLEDGE -> KNOWLEDGE | Phase-5 lesson L8: pause by exact-dispatch message failed (worker_identity_changed), fallback was a  | REP | L4056
555. VL-24-555 | finding | EVAL -> EVAL | FINAL-REPORT-QA.md "Overall Verdict: PASS" (l.67, l.90) with 66+ source rows reviewed from sibling w | REP | L3148
556. VL-24-556 | finding | DROP -> DROP | Hand-off claim "Additive experimental commands were installed earlier under separate names" (FINAL-R | DEDUP of VL-24-300 | L5959
557. VL-24-557 | finding | KNOWLEDGE -> KNOWLEDGE | Hand-off claim "Variant build worktrees contain staged task packages and uncommitted product changes | REP | L4057
558. VL-24-558 | finding | KNOWLEDGE -> KNOWLEDGE | Hand-off claim "No commits or pushes in this reporting step" is superseded: git log -- .dev/experime | REP | L4058
559. VL-24-559 | defect | DROP -> DROP | Hand-off claim "ponytail script can write the spec before writing later audit log files" (FINAL-REPO | DEDUP of VL-24-288 | L5960
560. VL-24-560 | defect | DROP -> DROP | Hand-off claim "stoprule ... the extractor recognizes Agent/Task tool-result records" (FINAL-REPORT  | DEDUP of VL-24-274 | L5961
561. VL-24-561 | defect | DROP -> DROP | Hand-off claim "fix_audit.py cmd_verdict explicitly adds an unparseable condition when no prior rows | DEDUP of VL-24-287 | L5962
562. VL-24-562 | finding | DROP -> DROP | Hand-off claim "Minfix ... recorded 84 passing tests did not establish acceptance" (FINAL-REPORT l.1 | DEDUP of VL-24-291 | L5963
563. VL-24-563 | finding | DROP -> DROP | Hand-off claim "tests tie CAP_REVIEWS to 'at most 2 fix cycles (3 reviews)'": the sentence is presen | DEDUP of VL-24-240 | L5964
564. VL-24-564 | open | EVAL -> EVAL | Hand-off claim in docs/reference/review-panel-live7.md l.3: the data sit on branch 346Claude-ab-expe | REP | L3149
565. VL-24-565 | finding | KNOWLEDGE -> KNOWLEDGE | .dev/research/346-review-loop-experiments/exp346/... duplicates .dev/experiments/346-validation/...  | REP | L4059
566. VL-24-566 | finding | KNOWLEDGE -> KNOWLEDGE | Summary: E3 has four layers: (1) the shipped master Review Loop (spec-panel.md l.256-268, prompts fi | REP | L4060
567. VL-24-567 | finding | DROP -> DROP | Summary: the bundle's 7909 lines of tests are 6840 for the four built variants plus 1069 for unfinis | DEDUP of VL-24-229 | L5965
568. VL-24-568 | finding | DROP -> DROP | Summary: consumers reach review in 8 different ways: loop CLI/prose (spec-panel), single reflect cal | DEDUP | L5966
569. VL-24-569 | finding | DROP -> DROP | Summary: hard blockers for PR review (location type, category set 18 vs 6, severity scale 5 vs 3, ca | DEDUP | L5967
570. VL-24-570 | finding | DROP -> DROP | Summary: 17 conflicts logged in section I; the most consequential are the meanings of "Medium" (I1;  | DEDUP of VL-24-486 | L5968
571. VL-24-571 | finding | DROP -> DROP | Summary: most reusable value (not code): owner counting rule, scoped-PASS coverage statement, fail-c | DEDUP of VL-24-265 | L5969
572. VL-24-572 | open | DROP -> DROP | Slice-12 gap 1: per-variant comparison.md, metrics.json, validity.md (under final-bundle/measurement | DEDUP of VL-24-306 | L5970
573. VL-24-573 | open | EVAL -> EVAL | Slice-12 gap 2: .dev/research/346-review-loop-experiments/ (6523 tracked files: FINAL-RESULTS.md 24  | REP | L3150
574. VL-24-574 | open | DROP -> DROP | Slice-12 gap 3: src/superclaude/cli/tasklist/ and cli/roadmap/, sc-roadmap-protocol, sc-validate-roa | REP | L5971
575. VL-24-575 | open | DROP -> DROP | Slice-12 gap 4: sc-implement-protocol/refs/retry.md, refs/managed-workspace.md beyond grep, and the  | REP | L5972
576. VL-24-576 | open | DROP -> DROP | Slice-12 gap 5: rf-qa behaviour tests (tests/ grep for rf-qa) not searched (G2.10) | DEDUP of VL-24-470 | L5973
577. VL-24-577 | open | DROP -> DROP | Slice-12 gap 6: sc-pr-submit-protocol refs (14 files), finding-verify.md, troubleshoot-dispatch.md,  | REP | L5974
578. VL-24-578 | open | DROP -> DROP | Slice-12 gap 7: variant source was read only at constants, profiles, subcommand lists and the three  | REP | L5975
579. VL-24-579 | open | DROP -> DROP | Slice-12 gap 8: whether personal-over-project shadowing (DECISIONS D9) holds with the current Claude | DEDUP of VL-24-324 | L5976
580. VL-24-580 | open | DROP -> DROP | Slice-12 gap 9: plugin mirror differences for design.md and brainstorm.md were detected (diff -q) bu | REP | L5977
581. VL-24-581 | open | DROP -> DROP | Slice-12 gap 10: rf-qa-qualitative's 8 per-document checklists and rf-analyst output formats were co | REP | L5978
582. VL-24-582 | question | CORE -> CORE | Open question Q1: which severity scale is canonical in the unified core and does "Medium" survive as | REP | L926
583. VL-24-583 | question | CORE -> CORE | Open question Q2: is a per-consumer cap (3 reviews vs 2 passes vs 2/5 rounds) acceptable, or must ta | REP | L927
584. VL-24-584 | question | DROP -> DROP | Open question Q3: verdict ownership: reviewer-typed (master) or script-computed (variants, phase-5 o | DEDUP of VL-24-489 | L5979
585. VL-24-585 | question | DROP -> DROP | Open question Q4: keep the CLI ledger (resolved_check) or the variant ledger (fixed/verified/reopene | DEDUP of VL-24-249 | L5980
586. VL-24-586 | question | DROP -> DROP | Open question Q6: may sc:implement get a panel (qa.md l.11 forbids it) or stay exempt (I7) | DEDUP of VL-24-405 | L5981
587. VL-24-587 | question | KNOWLEDGE -> KNOWLEDGE | Open question Q7: does the owner want the never-produced REFACTOR-SPEC (DESIGN-BRIEF.md) or treat ma | REP | L4061
588. VL-24-588 | question | MODULE-rfqa -> MODULE-rfqa | Open question Q8: should the rf-qa replacement start with /task phase gates (which already have lens | REP | L1801
589. VL-24-589 | question | CORE -> CORE | Open question Q9: which code-review lens pack (security, concurrency, architecture, tests) belongs t | REP | L928

COUNT 24-value-ledger-evidence-consumers.md: 589

## File 2: synthesis/synth-08-value-inventory.md (6,127 lines; 5,779 `VL-` + 171 `DR-` = 5,950 rows, recounted below)

Recount (read-only): `grep -c '^| VL-' synth-08` = 5779; `grep -c '^| DR-' synth-08` = 171; sum 5950 = the report's 8.1.0 total. An awk pass by heading range gave the same per-ledger-by-destination matrix as the 8.1.0 table (0 differences), 0 rows whose Destination column differs from the heading they sit under, rows at lines 45 to 6034, each group's last row is the line before the next heading.
Scope of this list: (I) every prose item of the file (preamble, 8.1.0, 8.1.1, 8.1.3, 8.1.4, verification paragraph); (II) the ten destination groups; (III) the P3-011, P3-012 and P3-014 table entries; (IV) every ledger-by-destination row group (cells; the rows of ledgers 19 to 23 are enumerated row by row by agents 1 to 3, the rows of ledger 24 are in File 1 above); (V) every defect-register row DR-001 to DR-171 individually.
Class: REP = represented in report Section 8.1 / Appendix A (report line cited); checked by meaning and by a line-by-line `diff` of the carried text against the file.

1. Preamble: Date 2026-11-14, Status Complete, Report section 8.1 deliverable (b), Item 5.08 | REP report 4242-4244 (source note)
2. 8.1.0 table row Ledger 19: 139/23/13/15/7/5/95/32/56/501 = 886 | REP report 4252
3. 8.1.0 table row Ledger 20: 100/3/11/3/3/2/284/137/15/310 = 868 | REP report 4253
4. 8.1.0 table row Ledger 21: 113/1/184/2/4/1/489/58/247/586 = 1,685 | REP report 4254
5. 8.1.0 table row Ledger 22: 107/4/94/0/4/1/287/167/47/244 = 955 | REP report 4255
6. 8.1.0 table row Ledger 23: 253/216/6/9/4/2/74/19/25/188 = 796 | REP report 4256
7. 8.1.0 table row Ledger 24: 168/14/32/39/23/42/116/42/26/87 = 589 | REP report 4257
8. 8.1.0 table row Defect register 17: 68/17/0/1/0/0/20/12/0/53 = 171 | REP report 4258
9. 8.1.0 table Total row: 948/278/340/69/45/53/1,365/467/416/1,969 = 5,950 | REP report 4259
10. Reconciliation: 886+868+1,685+955+796+589 = 5,779 ledger rows + 171 DR rows = 5,950 in, 5,950 out, no row dropped, merged or summarised | REP report 4261
11. `grep -c '^| DR-'` on file 17 returns 216 (45 crosswalk and corrections lines); the register is the 171 rows DR-001 to DR-171 | REP report 4261
12. VL/DR duplicate pairs: 161 rows marked `DROP: duplicate of` (118 ledger rows name a DR row, 43 register rows name a ledger row; 114 and 39 before the Gate 2 fix) | REP report 4261 (recount: 118 and 43, matches)
13. The 161 rows cover 162 of 171 register rows; the other 9 register rows have no ledger twin | REP report 4261
14. 3 ledger rows duplicate a row of another ledger (VL-21-131 of VL-22-017, VL-23-576 of VL-24-519, VL-22-583 of VL-20-299) | REP report 4261 (all three confirmed in the file)
15. DROP rows by reason: duplicate 1,753; obsolete 126; out of scope or evidence-free 86; CODE-CONTRADICTED 4 = 1,969 | REP report 4263 (recount: 1753/126/86/4, matches)
16. 27 non-DROP rows carry a [CODE-CONTRADICTED] tag, kept on purpose (VL-19-204, VL-20-109, VL-20-472 carry the 14 terra plus 2 luna correction); "16 empty terra reviews" never quoted as fact | REP report 4263 (recount 27, matches)
17. Rule 1: rows processed one ledger at a time, copied byte for byte by a read-only script, script not a deliverable | REP report 4267
18. Rule 2: exactly one destination per row, from the ledger destination (or first word of the DR Fix owner) unless a rule changed it, change written in the Reason column | REP report 4267
19. Rule 3: only [CODE-VERIFIED] claims stated as fact; [UNVERIFIED] and [CODE-CONTRADICTED] tags kept inside the text | REP report 4267
20. Rule 4: report only, no roadmap, branch plan, PR plan or risk register | REP report 4267
21. Rule 5: run-1 folder and queued-run note not read; `.dev/tasks/` excluded from repo-wide searches; the one extra input is qa-consolidated-findings-phase3.md table 1b | REP report 4267
22. Authority rule (P3-012): register row re-verified (REPRODUCED, TRACED, partly TRACED) means the DR Fix owner is the kept destination and each ledger twin becomes `DROP: duplicate of DR-nnn` | REP report 4269
23. Authority rule: register row UNVERIFIED means the ledger destination is kept and the DR row becomes `DROP: duplicate of VL-NN-nnn`, Fix owner text kept in the Reason | REP report 4269
24. Authority rule: a ledger row already DROP stays DROP with the note `same defect as DR-nnn (kept row)` | REP report 4269
25. Authority rule: first-word rule for dual-owner cells (`HARNESS / CORE` is HARNESS); OPS rows resolved against their ledger twin | REP report 4269
26. DR-167 (verified, owner EVAL, untracked checkout) is DROP because cleaning it is a mutation outside a report-only task | REP report 4269
27. Result: 162 register rows have at least one ledger twin, 208 register/ledger pairs, 99 pairs differed before the pass (Gate 1 reviewer found 51 as a lower bound) | REP report 4269
28. Gate 2 found eight further pairs (DR-039, DR-098, DR-103, DR-147 UNVERIFIED; VL-20-241, VL-23-535, VL-23-007, VL-19-351 against re-verified rows), same rule applied | REP report 4269
29. Pairs naming no single kept ledger row or read differently by two reviewers were not changed (limit 3b); no new full re-scan; "one kept row" claimed for the listed pairs only | REP report 4269
30. Twin-finding method: join of the register slice:line cites to the ledger Source column, confirmed by the defect id token, read row by row; hand-added pairs from the crosswalk (file 17 Open item (c)) | REP report 4269
31. Cross-ledger duplicates P3-011 resolution: exchange layer CORE (optional), tier and roster data and templates and panel-resolution tests CORE, merged-report renderer CORE (reviser wording MODULE-spec plug-in), telemetry strata CORE, judge skip rule HARNESS, `_REF_TOKEN` CORE with per-target syntax a MODULE-tasklist plug-in | REP report 4271
32. Decided-roster recommendations VL-20-122 to VL-20-125 and VL-20-143 stay MODULE-tasklist | REP report 4271
33. Scan of 3,989 non-DROP rows: no identical statement, 29 cross-ledger pairs sharing a cite, all different facts, except VL-19-036 and VL-20-345 (same /tmp execution defect, both HARNESS) | REP report 4271
34. A full semantic comparison of all 5,779 ledger rows against each other was not done | REP report 4271
35. Provenance routing P3-014: every MODULE-tasklist row of ledgers 21 (214), 22 (124), 20 (23) read and re-judged by who would use the item; the recommended split (core keeps finding contract, merge, ledger, verdict kernel, dispatch identity, tier data, H1/H2 slots, card schema, counts-only telemetry, optional exchange layer; modules keep category/lens/ref sets, brief text, classes, extractors, catalogues, roles, schedules) | REP report 4273
36. 70 rows moved (ledger 20: 9, 21: 28, 22: 30, 23: 2, 24: 1) with `moved from <old>: <why>` in the Reason | REP report 4273 (ledger 24 row VL-24-181 confirmed in File 1)
37. 278 MODULE-tasklist rows of ledgers 21 and 22 that stay carry `HOIST-CANDIDATE: spec, pr-review, rf-qa`; five downward ties of ledger 23 and four tie rows of ledger 24 (G-L7) carry `HOIST-CANDIDATE: CORE` | REP report 4273 (recount: 4 ledger-24 rows VL-24-055, 106, 144, 525; 5 MODULE-reflect ledger-23 rows)
38. 73 MODULE rows, 41 CORE rows naming one module, 67 CORE rows about reflect code read; VL-23-479 MODULE-reflect to CORE; VL-24-181 CORE to MODULE-reflect; VL-23-629 stays CORE; VL-23-267 EVAL to CORE; other rows not re-judged one by one | REP report 4273
39. 8.1.2 column key (ID, Source, Statement, Kind, Destination, Reason or conflict link) and Source code (`L<n> <slice:line>`, `17 <id>; <slice:line>; evidence`) and the rule that added text starts with `moved from`, `DROP[...]`, a `[...]` note or a trailing `HOIST-CANDIDATE:` | REP report 4280
40. P3-011 group: seal, hook, resume, session id (VL-21-130, 131, 163, 835; VL-22-017, 018, 328, 472, 825, 910, 613), CORE as optional exchange capability, 20 ledger-21 and 29 ledger-22 rows moved with them | REP report 4322
41. P3-011 group: tier and roster data (VL-19-041..043, 313, 624; VL-20-017, 024, 055, 318, 319, 320, 571, 610; DR-015..017), CORE | REP report 4323
42. P3-011 group: packaged panel templates and review-tiers.default.json (VL-23-576, VL-24-519, VL-20-318), CORE | REP report 4324
43. P3-011 group: merged-report renderer `review: n of cap` (VL-19-595, VL-23-147, DR-055), CORE with MODULE-spec reviser wording | REP report 4325
44. P3-011 group: telemetry strata hard-coded (VL-19-045, VL-23-267, DR-022), CORE | REP report 4326
45. P3-011 group: judge skip rule `judge-one.sh:7` (VL-20-299, VL-22-583, DR-036, DR-083), HARNESS | REP report 4327
46. P3-011 group: `_REF_TOKEN` at findings.py:29 (DR-007, DR-061, VL-19-046, VL-19-228), CORE with MODULE-tasklist plug-in | REP report 4328
47. P3-014 table row ledger 21: 214 read, 28 to CORE, 2 DROP duplicate, 184 stay tagged | REP report 4382
48. P3-014 table row ledger 22: 124 read, 30 to CORE, 0 DROP, 94 stay tagged | REP report 4383
49. P3-014 table row ledger 20: 23 read, 9 to CORE, 3 DROP, 11 stay untagged | REP report 4384
50. P3-014 moved-to-CORE list: exchange layer (49 rows) | REP report 4388
51. P3-014 moved-to-CORE list: tier data, packaged templates, panel-resolution tests (7 rows) | REP report 4389
52. P3-014 moved-to-CORE list: named source document in the brief H1 (3 rows) | REP report 4390
53. P3-014 moved-to-CORE list: card schema, optional row block, post-run quote checks (3 rows) | REP report 4391
54. P3-014 moved-to-CORE list: per-target extension point (4 rows) | REP report 4392
55. P3-014 moved-to-CORE list: other single-row moves VL-20-067, VL-23-267, VL-23-479, VL-24-181 (4 rows) | REP report 4393
56. 8.1.4 limit 1: re-validation targeted not row by row (MODULE-tasklist rows of 20/21/22, 73 + 41 + 67 rows read; other rows keep the ledger destination) | REP report 4399 (plus a labelled report note)
57. 8.1.4 limit 2: register/ledger join uses slice:line cites; the 9 register rows without a ledger twin are DR-052, 066, 068, 089, 093, 094, 095, 101, 150 | REP report 4400
58. 8.1.4 limit 3: 59 register rows UNVERIFIED (Gate 1 minor P3-015); ledger destination won; Fix owner text only in the DR Reason | REP report 4401
59. 8.1.4 limit 3a: exchange layer to CORE follows research/09 Summary and ledger 22 Gap Q3; placement not quality claim; if the owner decides there is no exchange the moved rows become DROP or MODULE-tasklist backlog | REP report 4402
60. 8.1.4 limit 3b: pairs named by Gate 2 and not changed: DR-084, DR-138, and weaker overlaps DR-135/VL-23-444, DR-082/VL-20-195, DR-128/VL-23-449, DR-154/VL-23-664, DR-080/VL-20-309, DR-004/VL-20-777 | REP report 4403
61. 8.1.4 limit 4: DROP labels derived by keyword from the ledgers' Reason text; CODE-CONTRADICTED DROP rows cite the code only as far as the row does | REP report 4404
62. 8.1.4 limit 5: statements, kinds, source cites are the ledgers' own; no new fact about code; [UNVERIFIED] tags kept | REP report 4405
63. Verification paragraph: 5,950 unique-ID rows, six columns, all present, Statement/Kind/Source equal to source, every row under the heading equal to its Destination, DROP prefix check, repeated after Gate 2 | REP report 4407

### Part II: the ten destination groups (heading line, rows, per-source split)
64. group CORE | heading line 45 | 948 rows | L19=139 L20=100 L21=113 L22=107 L23=253 L24=168 LDR=68 | REP report 4283-4293 (heading line and row count match) 
65. group MODULE-reflect | heading line 997 | 278 rows | L19=23 L20=3 L21=1 L22=4 L23=216 L24=14 LDR=17 | REP report 4283-4293 (heading line and row count match) 
66. group MODULE-tasklist | heading line 1279 | 340 rows | L19=13 L20=11 L21=184 L22=94 L23=6 L24=32 | REP report 4283-4293 (heading line and row count match) 
67. group MODULE-spec | heading line 1623 | 69 rows | L19=15 L20=3 L21=2 L23=9 L24=39 LDR=1 | REP report 4283-4293 (heading line and row count match) 
68. group MODULE-pr-review | heading line 1696 | 45 rows | L19=7 L20=3 L21=4 L22=4 L23=4 L24=23 | REP report 4283-4293 (heading line and row count match) 
69. group MODULE-rfqa | heading line 1745 | 53 rows | L19=5 L20=2 L21=1 L22=1 L23=2 L24=42 | REP report 4283-4293 (heading line and row count match) 
70. group EVAL | heading line 1802 | 1365 rows | L19=95 L20=284 L21=489 L22=287 L23=74 L24=116 LDR=20 | REP report 4283-4293 (heading line and row count match) 
71. group HARNESS | heading line 3171 | 467 rows | L19=32 L20=137 L21=58 L22=167 L23=19 L24=42 LDR=12 | REP report 4283-4293 (heading line and row count match) 
72. group KNOWLEDGE | heading line 3642 | 416 rows | L19=56 L20=15 L21=247 L22=47 L23=25 L24=26 | REP report 4283-4293 (heading line and row count match) 
73. group DROP | heading line 4062 | 1969 rows | L19=501 L20=310 L21=586 L22=244 L23=188 L24=87 LDR=53 | REP report 4283-4293 (heading line and row count match) 

### Part III: P3-012 table entries (defect-register Fix owner versus ledger destination)
74. P3-012 DR-016 | Fix owner CORE | Repro REPRODUCED | kept row DR-016 (CORE) | REP report 4334-4375
75. P3-012 DR-017 | Fix owner CORE | Repro REPRODUCED | kept row DR-017 (CORE) | REP report 4334-4375
76. P3-012 DR-070 | Fix owner CORE | Repro TRACED | kept row DR-070 (CORE) | REP report 4334-4375
77. P3-012 DR-073 | Fix owner CORE | Repro TRACED | kept row DR-073 (CORE) | REP report 4334-4375
78. P3-012 DR-133 | Fix owner CORE | Repro TRACED | kept row DR-133 (CORE) | REP report 4334-4375
79. P3-012 DR-134 | Fix owner CORE | Repro TRACED | kept row DR-134 (CORE) | REP report 4334-4375
80. P3-012 DR-135 | Fix owner MODULE-reflect | Repro TRACED | kept row DR-135 (MODULE-reflect) | REP report 4334-4375
81. P3-012 DR-146 | Fix owner CORE | Repro UNVERIFIED | kept row VL-23-479 (CORE) | REP report 4334-4375
82. P3-012 DR-117 | Fix owner CORE | Repro UNVERIFIED | kept row VL-23-116 (EVAL) | REP report 4334-4375
83. P3-012 DR-118 | Fix owner CORE | Repro TRACED | kept row DR-118 (CORE) | REP report 4334-4375
84. P3-012 DR-124 | Fix owner CORE | Repro TRACED | kept row DR-124 (CORE) | REP report 4334-4375
85. P3-012 DR-139 | Fix owner MODULE-reflect | Repro UNVERIFIED | kept row VL-23-618 (MODULE-reflect) and VL-23-629 (CORE) | REP report 4334-4375
86. P3-012 DR-140 | Fix owner MODULE-reflect | Repro REPRODUCED by reading | kept row DR-140 (MODULE-reflect) | REP report 4334-4375
87. P3-012 DR-156 | Fix owner MODULE-reflect | Repro REPRODUCED by reading | kept row DR-156 (MODULE-reflect) | REP report 4334-4375
88. P3-012 DR-157 | Fix owner MODULE-reflect | Repro UNVERIFIED | kept row VL-24-155 (CORE) | REP report 4334-4375
89. P3-012 DR-158 | Fix owner MODULE-reflect | Repro UNVERIFIED | kept row VL-24-156 (CORE) | REP report 4334-4375
90. P3-012 DR-160 | Fix owner MODULE-reflect | Repro TRACED | kept row DR-160 (MODULE-reflect) | REP report 4334-4375
91. P3-012 DR-161 | Fix owner MODULE-reflect | Repro UNVERIFIED | kept row VL-24-160 (CORE) | REP report 4334-4375
92. P3-012 DR-138 | Fix owner MODULE-reflect | Repro UNVERIFIED | kept row DR-138 (MODULE-reflect) | REP report 4334-4375
93. P3-012 DR-147 | Fix owner MODULE-reflect | Repro UNVERIFIED | kept row VL-23-518 (EVAL) | REP report 4334-4375
94. P3-012 DR-166 | Fix owner EVAL | Repro UNVERIFIED | kept row VL-24-165 (CORE) | REP report 4334-4375
95. P3-012 DR-148 | Fix owner OPS | Repro UNVERIFIED for the installed CLI of tha | kept row VL-24-170 (MODULE-reflect) | REP report 4334-4375
96. P3-012 DR-154 | Fix owner HARNESS | Repro REPRODUCED | kept row DR-154 (HARNESS) | REP report 4334-4375
97. P3-012 DR-163 | Fix owner OPS | Repro UNVERIFIED | kept row VL-24-162 (HARNESS) | REP report 4334-4375
98. P3-012 DR-164 | Fix owner EVAL | Repro UNVERIFIED | kept row VL-24-163 (HARNESS) | REP report 4334-4375
99. P3-012 DR-169 | Fix owner EVAL | Repro UNVERIFIED | kept row VL-24-171 (HARNESS) | REP report 4334-4375
100. P3-012 DR-170 | Fix owner EVAL | Repro UNVERIFIED | kept row VL-24-173 (HARNESS) | REP report 4334-4375
101. P3-012 DR-091 | Fix owner EVAL | Repro REPRODUCED | kept row DR-091 (EVAL) | REP report 4334-4375
102. P3-012 DR-097 | Fix owner EVAL | Repro UNVERIFIED | kept row VL-20-652 and VL-20-774 (EVAL) | REP report 4334-4375
103. P3-012 DR-102 | Fix owner EVAL | Repro partly TRACED | kept row DR-102 (EVAL) | REP report 4334-4375
104. P3-012 DR-105 | Fix owner EVAL | Repro UNVERIFIED | kept row VL-20-655 (HARNESS) | REP report 4334-4375
105. P3-012 DR-087 | Fix owner DROP | Repro REPRODUCED | kept row DR-087 (DROP) | REP report 4334-4375
106. P3-012 DR-045 | Fix owner DROP | Repro REPRODUCED read-only | kept row DR-045 (DROP) | REP report 4334-4375
107. P3-012 DR-049 | Fix owner DROP | Repro REPRODUCED | kept row DR-049 (DROP) | REP report 4334-4375
108. P3-012 DR-050 | Fix owner DROP | Repro UNVERIFIED | kept row VL-19-091 (EVAL) | REP report 4334-4375
109. P3-012 DR-077 | Fix owner DROP | Repro UNVERIFIED | kept row VL-19-463 and VL-19-464 (KNOWLEDGE) | REP report 4334-4375
110. P3-012 DR-039 | Fix owner EVAL | Repro UNVERIFIED | kept row VL-19-036 and VL-20-345 (HARNESS) | REP report 4334-4375
111. P3-012 DR-086 | Fix owner EVAL | Repro REPRODUCED | kept row DR-086 (EVAL) | REP report 4334-4375
112. P3-012 DR-042 | Fix owner CORE | Repro REPRODUCED by Glob | kept row DR-042 (CORE) | REP report 4334-4375
113. P3-012 DR-098 | Fix owner EVAL | Repro UNVERIFIED | kept row VL-20-743 (CORE) | REP report 4334-4375
114. P3-012 DR-103 | Fix owner EVAL | Repro UNVERIFIED | kept row VL-20-113 (KNOWLEDGE) | REP report 4334-4375

### Part IV: ledger-by-destination row groups (rows of ledgers 19-23 are enumerated row by row by agents 1-3; ledger 24 rows are File 1)
115. ledger 19 rows under CORE: 139 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 1) 
116. ledger 19 rows under MODULE-reflect: 23 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 1) 
117. ledger 19 rows under MODULE-tasklist: 13 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 1) 
118. ledger 19 rows under MODULE-spec: 15 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 1) 
119. ledger 19 rows under MODULE-pr-review: 7 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 1) 
120. ledger 19 rows under MODULE-rfqa: 5 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 1) 
121. ledger 19 rows under EVAL: 95 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 1) 
122. ledger 19 rows under HARNESS: 32 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 1) 
123. ledger 19 rows under KNOWLEDGE: 56 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 1) 
124. ledger 19 rows under DROP: 501 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 1) 
125. ledger 20 rows under CORE: 100 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 2) 
126. ledger 20 rows under MODULE-reflect: 3 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 2) 
127. ledger 20 rows under MODULE-tasklist: 11 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 2) 
128. ledger 20 rows under MODULE-spec: 3 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 2) 
129. ledger 20 rows under MODULE-pr-review: 3 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 2) 
130. ledger 20 rows under MODULE-rfqa: 2 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 2) 
131. ledger 20 rows under EVAL: 284 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 2) 
132. ledger 20 rows under HARNESS: 137 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 2) 
133. ledger 20 rows under KNOWLEDGE: 15 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 2) 
134. ledger 20 rows under DROP: 310 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 2) 
135. ledger 21 rows under CORE: 113 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 2) 
136. ledger 21 rows under MODULE-reflect: 1 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 2) 
137. ledger 21 rows under MODULE-tasklist: 184 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 2) 
138. ledger 21 rows under MODULE-spec: 2 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 2) 
139. ledger 21 rows under MODULE-pr-review: 4 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 2) 
140. ledger 21 rows under MODULE-rfqa: 1 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 2) 
141. ledger 21 rows under EVAL: 489 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 2) 
142. ledger 21 rows under HARNESS: 58 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 2) 
143. ledger 21 rows under KNOWLEDGE: 247 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 2) 
144. ledger 21 rows under DROP: 586 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 2) 
145. ledger 22 rows under CORE: 107 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 3) 
146. ledger 22 rows under MODULE-reflect: 4 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 3) 
147. ledger 22 rows under MODULE-tasklist: 94 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 3) 
148. ledger 22 rows under MODULE-pr-review: 4 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 3) 
149. ledger 22 rows under MODULE-rfqa: 1 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 3) 
150. ledger 22 rows under EVAL: 287 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 3) 
151. ledger 22 rows under HARNESS: 167 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 3) 
152. ledger 22 rows under KNOWLEDGE: 47 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 3) 
153. ledger 22 rows under DROP: 244 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 3) 
154. ledger 23 rows under CORE: 253 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 3) 
155. ledger 23 rows under MODULE-reflect: 216 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 3) 
156. ledger 23 rows under MODULE-tasklist: 6 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 3) 
157. ledger 23 rows under MODULE-spec: 9 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 3) 
158. ledger 23 rows under MODULE-pr-review: 4 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 3) 
159. ledger 23 rows under MODULE-rfqa: 2 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 3) 
160. ledger 23 rows under EVAL: 74 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 3) 
161. ledger 23 rows under HARNESS: 19 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 3) 
162. ledger 23 rows under KNOWLEDGE: 25 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 3) 
163. ledger 23 rows under DROP: 188 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 3) 
164. ledger 24 rows under CORE: 168 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 4 (File 1)) 
165. ledger 24 rows under MODULE-reflect: 14 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 4 (File 1)) 
166. ledger 24 rows under MODULE-tasklist: 32 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 4 (File 1)) 
167. ledger 24 rows under MODULE-spec: 39 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 4 (File 1)) 
168. ledger 24 rows under MODULE-pr-review: 23 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 4 (File 1)) 
169. ledger 24 rows under MODULE-rfqa: 42 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 4 (File 1)) 
170. ledger 24 rows under EVAL: 116 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 4 (File 1)) 
171. ledger 24 rows under HARNESS: 42 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 4 (File 1)) 
172. ledger 24 rows under KNOWLEDGE: 26 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 4 (File 1)) 
173. ledger 24 rows under DROP: 87 rows | REP Appendix A (group range in report 4283-4293; per-row substance checked by agents 4 (File 1)) 

### Part V: defect-register rows DR-001 to DR-171, one entry each (id | destination | repro | statement start | class | Appendix A line)
174. DR-001 | CORE | REPRODUCED  |  A finding whose anchor/anchor2 > 200, claim > 300, refs > 8, id > 16, bad sever | REP | L929
175. DR-002 | CORE | REPRODUCED |  Partial-panel failure is invisible: merge refuses only when no reviewer has a v | REP | L930
176. DR-003 | CORE | REPRODUCED  |  Docstring says an invalid-block reviewer "is skipped for clearing"; the clearin | REP | L931
177. DR-004 | CORE | REPRODUCED  |  Union-find over same_defect with 3-line tolerance chains distinct defects; the  | REP | L932
178. DR-005 | CORE | TRACED |  A ref mismatch splits one defect; refs are scraped from free text [CODE-VERIFIE | REP | L933
179. DR-006 | CORE | REPRODUCED |  Missing anchor kept with span None; anchor_status/anchor_ambiguous computed and | REP | L934
180. DR-007 | CORE | REPRODUCED |  Task ids such as T01.02 are not refs; same pattern in telemetry [CODE-VERIFIED] | REP | L935
181. DR-008 | CORE | TRACED |  Any single blocking finding fails the round; confidence is computed and printed | REP | L936
182. DR-009 | CORE | REPRODUCED  |  A refound row takes the current round's blocking call; a one-reviewer re-review | REP | L937
183. DR-010 | CORE | TRACED |  Cluster matches only the first existing row (break) [CODE-VERIFIED]  | REP | L938
184. DR-011 | CORE | REPRODUCED  |  ledger revise can run twice and remap spans twice; no new-text hash stored [COD | REP | L939
185. DR-012 | CORE | TRACED |  merge always exits 0; ledger verdict maps 0/10/11 [CODE-VERIFIED]  | REP | L940
186. DR-013 | CORE | TRACED |  A --report id missing from --resolution gets model None; no cross-check [CODE-V | REP | L941
187. DR-014 | CORE | REPRODUCED  |  distinct_across_slots silently falls back to duplicates when exclusion empties  | REP | L942
188. DR-015 | CORE | REPRODUCED  |  Gateway environment has an empty launch map  | REP | L943
189. DR-016 | CORE | REPRODUCED |  muse-ember-1.0 absent from tier data  | REP | L944
190. DR-017 | CORE | REPRODUCED |  Excluded Qwen/glm models remain in the tier lists  | REP | L945
191. DR-018 | CORE | REPRODUCED |  Environment is guessed from $T3Model01; the other slot variables are never read | REP | L946
192. DR-019 | CORE | REPRODUCED  |  Re-review resolves to the single fixed anchor (apply_to: ["first"])  | REP | L947
193. DR-020 | CORE | REPRODUCED |  round_robin uses today's date when --sequence is absent  | REP | L948
194. DR-021 | CORE | TRACED |  No automatic caller of append_record; the one caller is the manual review telem | REP | L949
195. DR-022 | CORE | TRACED |  Telemetry strata hard-code sonnet/haiku  | REP | L950
196. DR-023 | CORE | TRACED |  The reviewer brief never names the source document  | REP | L951
197. DR-024 | CORE | TRACED |  Parser limits (claim <= 300, refs <= 8, id <= 16, MINOR not blocking) are not s | REP | L952
198. DR-025 | CORE | REPRODUCED  |  Blocking semantics conflict between spec-panel text, prompt and parser  | REP | L953
199. DR-027 | CORE | TRACED |  No anchor guidance for missing-requirement, uniqueness, whitespace  | REP | L954
200. DR-029 | CORE | TRACED |  Reviewers are not told one blocking row from any reviewer fails the round  | REP | L955
201. DR-042 | CORE | REPRODUCED by Glob  |  lint_cmd and estimate_cmd are registered in the review group but no such module | REP | L956
202. DR-043 | CORE | TRACED |  Round 4 is accepted after ESCALATE; --cap is ignored on an existing ledger; ver | REP | L957
203. DR-052 | CORE | REPRODUCED  |  A refound row never updates fp, refs, claim or category; after revisions move s | REP | L958
204. DR-053 | CORE | REPRODUCED  |  defer has no status precondition, rewrites the stored last-round verdict/decisi | REP | L959
205. DR-054 | CORE | REPRODUCED  |  Fix-map items for non-open rows are skipped without an output entry; the table  | REP | L960
206. DR-055 | CORE | REPRODUCED  |  ## Other findings lists only rows with blocking=False; a blocking row that is r | REP | L961
207. DR-056 | CORE | REPRODUCED  |  Line-model mismatch: locate and _blocks_after count \n, section_of and opcodes  | REP | L962
208. DR-057 | CORE | REPRODUCED |  A two-token fence info string does not match, the block is not found  | REP | L963
209. DR-058 | CORE | REPRODUCED |  A quoted example block plus the real block -> "more than one block", ok=False;  | REP | L964
210. DR-059 | CORE | TRACED |  merge --out and capture --out writes are not atomic and capture does not create | REP | L965
211. DR-060 | CORE | REPRODUCED |  An empty claim is accepted  | REP | L966
212. DR-061 | CORE | REPRODUCED |  _REF_TOKEN is case-sensitive, lowercase ac-1 is not a ref; free-text tokens (UT | REP | L967
213. DR-064 | CORE | REPRODUCED by Grep  |  claude-fable-5-1 is available and launchable in anthropic-only but is in no tie | REP | L968
214. DR-066 | CORE | TRACED via slice  |  Three or four model registries: reflect skill aliases, reflect CLI T2Model0N, t | REP | L969
215. DR-070 | CORE | TRACED |  The ladder is a hand-kept map not read from the tier file and includes muse-emb | REP | L970
216. DR-071 | CORE | REPRODUCED  |  A fixed slot ignores the soft exclusion; only strict_distinct or hard_exclude f | REP | L971
217. DR-073 | CORE | TRACED  |  Test gaps: exact length boundaries; four of six categories never parsed in a te | REP | L972
218. DR-079 | CORE | TRACED  |  merge is not re-runnable for a round: an existing ledger gives "the ledger expe | REP | L973
219. DR-080 | CORE | TRACED for the two code sides |  Three category vocabularies: ground-truth classes (unpassable-ac, missing-task, | REP | L974
220. DR-090 | CORE | REPRODUCED  |  The product tier3 list is exactly the two owner-excluded models (glm-5.3, Qwen3 | REP | L975
221. DR-100 | CORE | TRACED  |  A refusal is recorded as verdict: FAIL with an empty findings block (39 of 51 i | REP | L976
222. DR-107 | CORE | REPRODUCED  |  Clearing by absence: a resolved_check row becomes resolved when no member of th | REP | L977
223. DR-108 | CORE | REPRODUCED |  A row with no span can never be moved to resolved_check by a fix: it goes to na | REP | L978
224. DR-109 | CORE | REPRODUCED  |  A fixed slot with count > 1 resolves to the same model N times even with distin | REP | L979
225. DR-111 | CORE | REPRODUCED  |  The packaged reflect templates cannot resolve in the gateway environment: launc | REP | L980
226. DR-112 | CORE | REPRODUCED |  A deferred row that is re-found as blocking keeps status deferred and is ignore | REP | L981
227. DR-113 | CORE | REPRODUCED |  v1 annotate raises KeyError: 'anchor' on a findings-v2 line with citations and  | REP | L982
228. DR-114 | CORE | REPRODUCED |  The stored verdict is not derived: after revise or defer the stored last-round  | REP | L983
229. DR-115 | CORE | REPRODUCED |  review panel validate does not apply the reflect profile when no tier file is g | REP | L984
230. DR-116 | CORE | TRACED  |  The telemetry loader drops changed duplicates silently (INSERT OR IGNORE on rec | REP | L985
231. DR-118 | CORE | TRACED |  cluster_cmd never passes lens to findings_v2.parse_block, so the lens-dependent | REP | L986
232. DR-119 | CORE | TRACED |  Inconsistent strictness between sibling commands: verify-citations --coverage f | REP | L987
233. DR-120 | CORE | REPRODUCED by Grep  |  Dead or decorative API in the E1 code: channel_of, V1_FIELDS, COMPLETION_STATES | REP | L988
234. DR-123 | CORE | TRACED  |  The v2 fingerprint has no section (always empty) and equality still needs non-e | REP | L989
235. DR-124 | CORE | TRACED  |  Design/code drift: the cluster.py docstring admits the code divides by each rev | REP | L990
236. DR-125 | CORE | REPRODUCED  |  Policy hard-coded in code: env names gateway / anthropic-only and T3Model01, st | REP | L991
237. DR-126 | CORE | TRACED  |  The ledger holds one document (doc path, line-range spans), so a multi-file tar | REP | L992
238. DR-127 | CORE | TRACED  |  The "no document text in a record" rule is a convention: validate_record checks | REP | L993
239. DR-133 | CORE | TRACED  |  Convergence thresholds differ: 0.75 / 0.60 in the skill, 0.80 in the wrapper, < | REP | L994
240. DR-134 | CORE | TRACED  |  Single vendor is warn-only in the skill but a DEGRADE in the wrapper unless --a | REP | L995
241. DR-171 | CORE | UNVERIFIED |  Self-reported model identity is an alias echo: E1-E3 reviewer 3 reported claude | REP | L996
242. DR-128 | MODULE-reflect | TRACED  |  The code-driven reflect engine emits contract_version "1.0" and keys outside th | REP | L1262
243. DR-129 | MODULE-reflect | TRACED |  The code engine sets merge_method = "adversarial" whenever there are two or mor | REP | L1263
244. DR-131 | MODULE-reflect | UNVERIFIED |  Code-engine swarm reviewers see only the tasklist body (no diff, spec or hunks) | REP | L1264
245. DR-135 | MODULE-reflect | TRACED |  t2_model_class_diversity is full \ | REP | L1265
246. DR-136 | MODULE-reflect | REPRODUCED by Grep |  reflection-rubric.md names the deviation classes {Aligned, Refinement, Drift, R | REP | L1266
247. DR-137 | MODULE-reflect | UNVERIFIED |  The calibrator class capability ordering {opus, sonnet, haiku, qwen, kimi, deep | REP | L1267
248. DR-138 | MODULE-reflect | UNVERIFIED  |  The Stage 2 shadow-exit result: 8 of 13 shadow runs fail EV-1 against 3 of 39 l | REP | L1268
249. DR-140 | MODULE-reflect | REPRODUCED by reading |  test_the_current_repository_reports_without_crashing accepts any documented exi | REP | L1269
250. DR-141 | MODULE-reflect | UNVERIFIED |  HEAD-relative pins in test_shadow_skill_contract.py guard only uncommitted edit | REP | L1270
251. DR-142 | MODULE-reflect | TRACED  |  The cli/reflect/__init__.py docstring is stale: it describes a subprocess fan-o | REP | L1271
252. DR-143 | MODULE-reflect | REPRODUCED by Grep |  The contract.py docstring cites SKILL.md:754 for the needs_human_decision invar | REP | L1272
253. DR-144 | MODULE-reflect | REPRODUCED by reading |  A runner comment says --no-promote is the hard default; the Click default is -- | REP | L1273
254. DR-145 | MODULE-reflect | REPRODUCED for  |  commands/reflect.md and the reflect CLI do not list --t2-engine (the skill docu | REP | L1274
255. DR-149 | MODULE-reflect | REPRODUCED by Grep  |  reviewer_briefs_materialized is emitted by reviewer-spec.md:78 but is not in th | REP | L1275
256. DR-150 | MODULE-reflect | UNVERIFIED  |  --reviewers is 2-3 (default 3) in the skill and the command, the wrapper clamps | REP | L1276
257. DR-156 | MODULE-reflect | REPRODUCED by reading |  The Stage 2 exit script treats an empty legacy baseline as 0.0, so any shadow E | REP | L1277
258. DR-160 | MODULE-reflect | TRACED  |  The Stage 0a replay cannot read the panel/cards/ findings-v2 blocks, reports sh | REP | L1278
259. DR-026 | MODULE-spec | TRACED |  Report-ending conflict: last line verdict: vs last section ## Findings block  | REP | L1695
260. DR-035 | EVAL | TRACED |  Stale merges (n2-terra, r2-sol, n5-sol, n5-terra)  | REP | L3151
261. DR-046 | EVAL | REPRODUCED by reading  |  Both hand-offs and CR:292 label per-model drop counts (luna 30, ember 33, wonde | REP | L3152
262. DR-047 | EVAL | REPRODUCED  |  "106 row folders in combos/": the tree holds 96 directories (git ls-tree -d --n | REP | L3153
263. DR-048 | EVAL | REPRODUCED by reading  |  "4 verdict flips": audit-D lists 3 flips (g3-sonnet-luna-ember-r3/alias, g5-emb | REP | L3154
264. DR-051 | EVAL | REPRODUCED for the  |  Raw-file count disagreement: hand-offs say 3,041 untracked files; the committed | REP | L3155
265. DR-076 | EVAL | REPRODUCED  |  E2 notes say combos/ holds 107 entries (SPEC.md + 106 row dirs); the tree has 9 | REP | L3156
266. DR-078 | EVAL | TRACED via slice  |  manifest.md:5 says "(local, never pushed)", which is stale  | REP | L3157
267. DR-083 | EVAL | TRACED  |  The judge counts "blocking" by a blocking-flagged ledger row, ignoring blocking | REP | L3158
268. DR-084 | EVAL | UNVERIFIED |  Row names hid composition (r2 treated as a muse row); "valid era" was chosen by | REP | L3159
269. DR-086 | EVAL | REPRODUCED |  tools/tmp-scripts/README.md lists checks-gate8 as a key script; the file is abs | REP | L3160
270. DR-089 | EVAL | UNVERIFIED  |  Counts disagree: Qwen slots ("all 3" at PILOT-REPORT.md:12, "4 reviewer ids" pe | REP | L3161
271. DR-091 | EVAL | REPRODUCED  |  fullpkg() resolves the control package to designSpec (12-character prefix test) | REP | L3162
272. DR-092 | EVAL | REPRODUCED for audit D only |  Batch j1 (45 runs, evidence for the "sonnet + 2x luna" decision update) is in n | REP | L3163
273. DR-093 | EVAL | prose lines TRACED |  Audit-A summary prose does not match its own flags file (59 vs 54 for E2; 9 vs  | REP | L3164
274. DR-094 | EVAL | UNVERIFIED  |  Audit D explains 92 dropped findings by validity rules but 109 were dropped net | REP | L3165
275. DR-095 | EVAL | UNVERIFIED  |  "16 empty terra reviews in valid-era rows" is 14 terra and 2 luna by slice 04's | REP | L3166
276. DR-099 | EVAL | UNVERIFIED |  elapsed sums the slowest reviewer per package and excludes quarantined re-runs  | REP | L3167
277. DR-101 | EVAL | UNVERIFIED  |  Benchmark concentration: three defects (DS GT3, DS GT7, AL GT2) account for 131 | REP | L3168
278. DR-102 | EVAL | partly TRACED |  Six different "valid-era" predicates give different row populations (71, 76, 66 | REP | L3169
279. DR-104 | EVAL | REPRODUCED |  three-way.py prints the first eight characters of each package id (TASK-WF-) as | REP | L3170
280. DR-030 | HARNESS | TRACED |  Cyclic fallback ladder spun and ran excluded models  | REP | L3630
281. DR-031 | HARNESS | TRACED |  On fallback, expected_model in meta is the fallback model (MODEL="$NEXT" before | REP | L3631
282. DR-032 | HARNESS | TRACED |  Attempt counter resets per fallback model, so attempt files overwrite and cost  | REP | L3632
283. DR-033 | HARNESS | TRACED |  BLOCK_OK only greps the fence line (^findings-v1), not the parse  | REP | L3633
284. DR-067 | HARNESS | TRACED |  Harness: an API-error-only result with the right model and block never enters t | REP | L3634
285. DR-068 | HARNESS | UNVERIFIED  |  Harness reviewer sessions disallow only Edit, Write, NotebookEdit; Bash is not  | REP | L3635
286. DR-069 | HARNESS | TRACED via slice  |  Harness hard-codes /tmp/evalsb/{repo,cand} and an absolute worktree path for so | REP | L3636
287. DR-081 | HARNESS | TRACED |  Harness: the variadic --disallowedTools swallowed the positional prompt, so eve | REP | L3637
288. DR-082 | HARNESS | TRACED |  Harness: source.md was not shipped to the reviewer sandbox; terra and sol retur | REP | L3638
289. DR-088 | HARNESS | REPRODUCED by reading at the tip |  45 merges have no saved merge-stdout.txt, so even the first-error warning is lo | REP | L3639
290. DR-154 | HARNESS | REPRODUCED  |  Hygiene: the memory file docs/memory/reflect/deviation-patterns-brainstorm-refl | REP | L3640
291. DR-155 | HARNESS | REPRODUCED  |  The lib/ rule in the root .gitignore silently excludes every lib/ folder from g | REP | L3641
292. DR-028 | DROP | TRACED  |  Harness category unpassable-ac vs parser unpassable-check  | DROP (reason in row) | L5982
293. DR-034 | DROP | UNVERIFIED  |  Stale attempt files inflate cost for 5 runs  | DEDUP of VL-19-252 | L5983
294. DR-036 | DROP | UNVERIFIED  |  An API-error judge left a plausible score  | DEDUP of VL-19-254 | L5984
295. DR-037 | DROP | UNVERIFIED  |  Blocking counted by grep without space tolerance  | DROP (reason in row) | L5985
296. DR-038 | DROP | UNVERIFIED  |  attrib.py credits by ledger membership  | DROP (reason in row) | L5986
297. DR-039 | DROP | UNVERIFIED here  |  Analysis scripts read or exec /tmp copies  | DEDUP of VL-19-036 | L5987
298. DR-040 | DROP | UNVERIFIED  |  12 concurrent workers caused gateway model-identity bleed  | DEDUP of VL-19-257 | L5988
299. DR-041 | DROP | UNVERIFIED  |  claude binary replaced mid-run three times (exit 127)  | DEDUP of VL-19-258 | L5989
300. DR-044 | DROP | UNVERIFIED  |  Review-ledger, diffgate, stoprule, fix-audit skills, the finding-grader agent a | DEDUP of VL-19-050 | L5990
301. DR-045 | DROP | REPRODUCED read |  The hand-off (and the E2 comparison at cmp:22) attribute the RV changes to #518 | DROP (reason in row) | L5991
302. DR-049 | DROP | REPRODUCED  |  "55 files + README" (run2:74) vs 55 files including the README: git ls-tree -r  | DROP (reason in row) | L5992
303. DR-050 | DROP | UNVERIFIED  |  Run-1 says "alias GT3 found once"; the legend maps the once-found defect to B6  | DEDUP of VL-19-091 | L5993
304. DR-062 | DROP | UNVERIFIED  |  confidence-calibrator is troubleshoot-shaped (6 dimensions, escalation rubric)  | DEDUP of VL-19-727 | L5994
305. DR-063 | DROP | UNVERIFIED  |  reflect-reviewer output is UC-2-shaped, yet Tier 2 spawns it for every mode inc | DEDUP of VL-19-728 | L5995
306. DR-065 | DROP | UNVERIFIED  |  The tasklist skill text says reflect "offers a Tier-3 task-builder remediation" | DEDUP of VL-19-729 | L5996
307. DR-072 | DROP | UNVERIFIED  |  A project or user file silently overrides the packaged default, and only templa | DEDUP of VL-19-612 | L5997
308. DR-074 | DROP | REPRODUCED by re |  The E2 notes claim "159" test functions; the per-file column sums to 179  | DROP (reason in row) | L5998
309. DR-075 | DROP | UNVERIFIED  |  Run-2 notes say T2bModel01 is not referenced anywhere in src/ or tests/; slice  | DROP (reason in row) | L5999
310. DR-077 | DROP | UNVERIFIED  |  Internal inconsistencies of the comparison note: "four facts" against eight row | DEDUP of VL-19-463 | L6000
311. DR-085 | DROP | UNVERIFIED  |  Pilot arms B and C used randomly drawn compositions per package (arm B: designS | DEDUP of VL-20-470 | L6001
312. DR-087 | DROP | REPRODUCED  |  COMBO-REPORT.md:292 says the merge discards findings "with no error"; the code  | DROP (reason in row) | L6002
313. DR-096 | DROP | UNVERIFIED  |  "2x luna + 2x ember has 2.75-3.25 more wrong blockers than every comparator" co | DEDUP of VL-20-772 | L6003
314. DR-097 | DROP | UNVERIFIED  |  48 tests with no multiplicity correction, n = 4-6 per panel, a permutation mini | DEDUP of VL-20-652 | L6004
315. DR-098 | DROP | UNVERIFIED  |  Reviewer outputs were hand-edited (.catfix.md, category rename) and merged inst | DEDUP of VL-20-743 | L6005
316. DR-103 | DROP | UNVERIFIED here  |  COMBO-REPORT.md above line 289 still shows retracted numbers (n2-sonnet-src 8/1 | DEDUP of VL-20-113 | L6006
317. DR-105 | DROP | UNVERIFIED  |  untried.py ok() does not exclude i1/i2 or "invalid" rows and uses judge-blockin | DEDUP of VL-20-655 | L6007
318. DR-106 | DROP | UNVERIFIED  |  Unverifiable artifacts: gt2-hits.txt has no generator script; the blind re-judg | DEDUP of VL-20-656 | L6008
319. DR-110 | DROP | UNVERIFIED  |  Telemetry column output_by_severity is created but always NULL; records populat | DEDUP of VL-23-108 | L6009
320. DR-117 | DROP | UNVERIFIED  |  model_scores can count a run's cost twice when it has two non-superseded outcom | DEDUP of VL-23-116 | L6010
321. DR-121 | DROP | UNVERIFIED  |  The run manifest has no lock: advance and record_attempt are load-modify-save,  | DEDUP of VL-23-121 | L6011
322. DR-122 | DROP | UNVERIFIED  |  card_convert is lossy: medium/important/should-fix/low/nit/info map to MINOR no | DEDUP of VL-23-122 | L6012
323. DR-130 | DROP | UNVERIFIED  |  The code engine's deviation signal defaults to CLEAN unless the adversarial sea | DEDUP of VL-23-608 | L6013
324. DR-132 | DROP | UNVERIFIED  |  The code engine has no executor-class exclusion, calibrator, evidence validator | DEDUP of VL-23-610 | L6014
325. DR-139 | DROP | UNVERIFIED  |  The orchestrator writes unknown top-level keys (zero_drop_flag, memory_status,  | DEDUP of VL-23-618 | L6015
326. DR-146 | DROP | UNVERIFIED  |  Shadow cards live at panel/cards/reviewer-<N>.md, the EV-1 lint expects reviewe | DEDUP of VL-23-479 | L6016
327. DR-147 | DROP | UNVERIFIED  |  cluster_agreement is 1.000 in all 9 runs that recorded it (min = median = max); | DEDUP of VL-23-518 | L6017
328. DR-148 | DROP | UNVERIFIED for the installed CLI of that day  |  shadow01 ran as legacy because the 2026-11-12 installed CLI lacked the panel op | DEDUP of VL-24-170 | L6018
329. DR-151 | DROP | UNVERIFIED  |  The reflect skill directory carries 25 lines that mention src/superclaude (CLAU | DEDUP of VL-23-710 | L6019
330. DR-152 | DROP | UNVERIFIED  |  test_no_nesting_guard.py keeps an xfail marker although the test XPASSes now  | DEDUP of VL-23-749 | L6020
331. DR-153 | DROP | REPRODUCED  |  The memory lesson "Fenced yaml calibration blocks are NOT parsed by cluster; us | DROP (reason in row) | L6021
332. DR-157 | DROP | UNVERIFIED  |  merged-verdict.yaml must be at adversarial/merged-verdict.yaml; the child skill | DEDUP of VL-24-155 | L6022
333. DR-158 | DROP | UNVERIFIED  |  Recorded panel_parity: true was wrong in 2 pilot runs and 4 combo runs (recorde | DEDUP of VL-24-156 | L6023
334. DR-159 | DROP | UNVERIFIED  |  Contract diversity telemetry is blind to dispatch collapse: A3 reported calibra | DEDUP of VL-24-157 | L6024
335. DR-161 | DROP | UNVERIFIED  |  Evidence-validator drop_rate is inconsistent with its counts (shadow03: drop_ra | DEDUP of VL-24-160 | L6025
336. DR-162 | DROP | UNVERIFIED  |  merged-verdict.yaml has no uniform schema: blocking/medium/minor are None in 13 | DEDUP of VL-24-161 | L6026
337. DR-163 | DROP | UNVERIFIED  |  The experiment ran on an installed skill that lags src/ (reviewer-spec hash b10 | DEDUP of VL-24-162 | L6027
338. DR-164 | DROP | UNVERIFIED  |  PLAN.md:1-3 and combos.json:4 still say "designed, NOT run"  | DEDUP of VL-24-163 | L6028
339. DR-165 | DROP | UNVERIFIED  |  runs.jsonl has 14 of 15 combo rows (A-r2 missing), non-uniform ids, and wall_cl | DEDUP of VL-24-164 | L6029
340. DR-166 | DROP | UNVERIFIED  |  E1 made 7 reviewer-agent calls and the reason is unrecorded  | DEDUP of VL-24-165 | L6030
341. DR-167 | DROP | REPRODUCED  |  An untracked grounding checkout runs/...comboC-r3/artifacts/base-e8db2fe6/ sits | DROP (reason in row) | L6031
342. DR-168 | DROP | UNVERIFIED  |  shadow02 aborted at clustering: all 11 findings cited the same tasklist and cha | DEDUP of VL-24-169 | L6032
343. DR-169 | DROP | UNVERIFIED  |  analysis/extract.py has a non-uv subprocess, "cur" in dir() and tuple medians  | DEDUP of VL-24-171 | L6033
344. DR-170 | DROP | UNVERIFIED  |  combos.json records only the class rotation, not the served model; resolution.j | DEDUP of VL-24-173 | L6034

COUNT synth-08-value-inventory.md: 344
