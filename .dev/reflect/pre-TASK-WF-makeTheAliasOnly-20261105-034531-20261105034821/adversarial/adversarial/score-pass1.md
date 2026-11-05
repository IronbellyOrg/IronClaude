# Hybrid Scoring, Pass 1 (input order V1, V2, V3)

Variants: V1 = reviewer-1 card (analyzer, claude-sonnet-5-5); V2 = reviewer-2 card (qa, glm-5.3); V3 = reviewer-3 card (refactorer, claude-opus-5-5).
Inputs read: variant-1/2/3-original.md, diff-analysis.md, debate-transcript.md (for the tiebreaker), artifacts/coverage-matrix.json (INF-001..INF-013), plan TASK-WF-makeTheAliasOnly-20261105-034531.md (129 lines).

## Quantitative layer

### Counts

| Metric | V1 | V2 | V3 |
|---|---|---|---|
| RC: INF ids addressed / 13 | 10/13 (001,003,005,006,007,008,009,010,011,013) | 11/13 (adds 004 via allow-list completeness check) | 11/13 (adds 004 via R3-1 allow-list reading) |
| RC: INF ids not addressed | 002, 004, 012 | 002, 012 | 002, 012 |
| IC: internal contradictions / scorable claims | 1/23 (verdict "No defect ... would make a task fail" vs R1-8 "would fail"; diff X-001) | 0/16 | 0/30 |
| SR: concrete / (concrete + vague) | 24/26 (vague: "could be tripped" line 17, "worth stating" line 28) | 16/16 | 29/29 ("may be a picker ID" at line 16 is a quote, not a hedge) |
| DC: resolved / total internal refs | 16/18 (unresolved: "see t1 grounding" not in card or plan; R1-6 "wrong module": plan:116 names no module) | 18/18 (plan:34,36,62,65,72,75,98,104; R2-3, R2-4; INF-011; Tasks 1,3,4,6,7,8,9) | 31/31 (plan:30,32,33,34,36,42,52,56,66,76,86,94,98,104,107,123,125,129; R3-2, R3-5; INF-010, INF-011; Tasks 1-9) |
| SC: H2 count / max (4) | 4/4 | 4/4 | 4/4 |

### Ratios and quant score (RC*0.30 + IC*0.25 + SR*0.15 + DC*0.15 + SC*0.15)

| Variant | RC | IC | SR | DC | SC | quant |
|---|---|---|---|---|---|---|
| V1 | 0.769 | 0.957 | 0.923 | 0.889 | 1.000 | 0.892 |
| V2 | 0.846 | 1.000 | 1.000 | 1.000 | 1.000 | 0.954 |
| V3 | 0.846 | 1.000 | 1.000 | 1.000 | 1.000 | 0.954 |

Spot check for K1 (V3 R3-4): src/superclaude/agents has 48 agent .md files plus README.md; 16 start a line with `model:` and 17 contain `model:` anywhere. R3-4's "48 files, 17 with model:" holds on the looser count, so it is not scored as an error.

## Qualitative layer (Claim-Evidence-Verdict)

C1 | V1: MET - "every clause of source.md lines 1-9 checked" | V2: MET - "Checked every requirement-bearing span of source.md lines 1, 5-9" | V3: MET - coverage audit walks source.md:1, :5, templates, INF-010/011
C2 | V1: MET - R1-8 env leak: "would fail or pass by accident" | V2: MET - R2-1 executor writing mandated bullet "fails the grep" | V3: MET - R3-3 check "depends on the runner's environment"
C3 | V1: MET - R1-4 mapping "true only after the launcher change" | V2: NOT MET - no prerequisite or ordering dependency raised | V3: MET - R3-9 "Tasks 2 and 3 link to a page Task 6 creates"
C4 | V1: MET - each finding ends "Recommendation: ..." (e.g. R1-2 add D12:235) | V2: MET - R2-1 "Fix: change the AC grep to grep -n -- --models" | V3: MET - R3-1 fix: whole policy file passes, "./artifacts/final-policy.log"
C5 | V1: MET - "Could not run git, pytest or cmp" | V2: MET - R2-2 "cli_portify comment/regex stays"; residual docs/ breadth | V3: MET - R3-8 "characterization tests are not requested by spec items (1)-(4)"
K1 | V1: NOT MET - R1-6 "wrong module" refuted: plan:116 names no module | V2: MET - R2-1 substring claim checks against plan:62/65 | V3: MET - R3-1 claims match plan:30, :33, :52
K2 | V1: MET - R1-10 extend AST scan, allow-list ccsession-tag | V2: MET - one-line AC grep replacement in R2-1 | V3: MET - R3-1 comment without literal id; add final policy run
K3 | V1: MET - blocking/minor labels, "ladder"/"rungs" used consistently | V2: MET - "blocking"/"minor", "AC" used consistently | V3: MET - "blocking"/"minor", "allow-list" used consistently
K4 | V1: NOT MET - verdict "No defect ... would make a task fail" vs R1-8 | V2: MET - FAIL with one blocker; coverage "none beyond R2-4 and R2-3" | V3: MET - FAIL with "Two blocking defects"; R3-1, R3-2 blocking
K5 | V1: MET - every finding cites file:line (defaults.sh:48, retry.md:162) | V2: MET - "plan:65", "chains.md:11-13,21", "commands.md:849,859" | V3: MET - "test_ccsession_tiers.py:332-341" and plan line cites
T1 | V1: MET - Verdict, Findings, Coverage audit, Self-confidence order | V2: MET - same order; blocking R2-1 first | V3: MET - same order; blockers R3-1, R3-2 first
T2 | V1: MET - H1 card, H2 sections, flat id bullets | V2: MET - H1, H2 sections, id bullets | V3: MET - H1, H2 sections, id bullets
T3 | V1: MET - one issue per finding (diff S-002 "12 flat findings") | V2: MET - five findings, one concern each | V3: NOT MET - R3-9 "bundles about 7 nits" (diff S-002)
T4 | V1: MET - ids R1-1..R1-12 | V2: MET - ids R2-1..R2-5; cross-ref "R2-4 and R2-3" | V3: MET - ids R3-1..R3-9; cross-refs "(R3-5)", "(R3-2)"
T5 | V1: MET - Verdict, Findings, Coverage audit, Self-confidence 0.78 | V2: MET - all four sections; Self-confidence 0.86 | V3: MET - all four sections; Self-confidence 0.85
L1 | V1: NOT MET - "would fail or pass by accident"; "could be tripped" | V2: MET - "An executor who writes the mandated bullet fails the grep" | V3: MET - "fails with a KeyError rather than because the exports are missing"
L2 | V1: MET - "suggest_alternate_model("opus") returns "sonnet"" | V2: MET - exact grep command and plan line numbers | V3: MET - exact recorded env keys listed in R3-2
L3 | V1: MET - four sections, each single-purpose | V2: MET - four sections, each single-purpose | V3: MET - four sections plus "Verified correct" block
L4 | V1: NOT MET - "t1 grounding", "rungs" undefined | V2: NOT MET - "AC-1", "matcher false negative" undefined | V3: NOT MET - "brief's coverage slice", INF-010 undefined
L5 | V1: MET - "Recommendation: add D12 line 235 to Task 2" | V2: MET - "Fix: name a grep or drop it" | V3: MET - "Fix: name line 411 and tiers.md:40"
R1 | V1: NOT MET - severity given, no probability | V2: NOT MET - severity given, no probability | V3: NOT MET - severity given, no probability
R2 | V1: NOT MET - R1-5 and R1-11 carry no recommendation | V2: MET - every finding R2-1..R2-5 has "Fix:" | V3: NOT MET - R3-9 nits carry no fix
R3 | V1: MET - R1-8 failure mode plus "state the capture addition" | V2: MET - R2-1 grep failure plus one-line recovery | V3: MET - R3-2 KeyError failure plus scratch-run recovery
R4 | V1: MET - R1-1 workspace defaults.sh activates non-Claude ladder | V2: NOT MET - no external dependency failure raised | V3: MET - R3-3 inherited `os.environ` "exports real ids today"
R5 | V1: MET - "add a Task 5 acceptance criterion recording the activation" | V2: MET - R2-5 "no verification procedure ... name a grep" | V3: MET - final policy-file run saved to artifacts log
E1 | V1: MET - R1-10 frontmatter misses `commands/*.md`; scan only cli/ | V2: MET - R2-3 scan "covers only src/superclaude/cli/**/*.py" | V3: MET - R3-4 "48 agent files, only 17 have a model: line"
E2 | V1: MET - R1-8 `os.environ.copy()` carries defaults.sh ANTHROPIC_DEFAULT_* | V2: NOT MET - no cross-component state interaction raised | V3: MET - R3-3 `_launch_env` copies os.environ; fixture does not clear
E3 | V1: MET - R1-10 "guard-strength gap"; R1-7 grep guard | V2: MET - R2-2 sweep "has no acceptance criterion" | V3: MET - R3-1 "no task runs the whole" policy file; R3-9 EXT_PROFILE
E4 | V1: NOT MET - no count divergence claim | V2: MET - "six expected-red tests are red ... other two pass" | V3: MET - R3-4 17 of 48 vs "every file" reading
E5 | V1: MET - R1-7 Task 5 grep tripped by Task 1/Task 6 files | V2: MET - R2-1 Task 3 AC vs Task 3 mandated text | V3: MET - R3-1 Task 2 edit breaks Task 1 test

### Qualitative subtotals

| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness (C1-C5) | 5 | 4 | 5 |
| Correctness (K1-K5) | 3 | 5 | 5 |
| Structure (T1-T5) | 5 | 5 | 4 |
| Clarity (L1-L5) | 3 | 4 | 4 |
| Risk coverage (R1-R5) | 3 | 3 | 3 |
| Invariant and edge-case (E1-E5) | 4 | 4 | 5 |
| Total / 30 | 23 | 25 | 26 |
| qual | 0.767 | 0.833 | 0.867 |

Edge-case floor: V1 4, V2 4, V3 5; none at 0, so all three are eligible as base.

## Combined scores (0.5*quant + 0.5*qual)

| Variant | quant | qual | Combined | Rank |
|---|---|---|---|---|
| V1 | 0.892 | 0.767 | 0.829 | 3 |
| V2 | 0.954 | 0.833 | 0.894 | 2 |
| V3 | 0.954 | 0.867 | 0.910 | 1 |

Tiebreaker: V3 and V2 are within 0.05 (gap 0.016), so it applies. Debate diff points won outright (debate-transcript.md scoring matrix; ALL and shared points excluded): V3 8 (S-001, C-005, C-006, C-007, C-008, C-012, X-001, X-002), V2 3 (C-004, C-009, A-002), V1 4 (S-002, C-001, C-002, C-013). V3 wins the tiebreaker at the first rule. The correctness count (V2 5, V3 5) is not needed.

Pass-1 base selection: V3 (0.910).
