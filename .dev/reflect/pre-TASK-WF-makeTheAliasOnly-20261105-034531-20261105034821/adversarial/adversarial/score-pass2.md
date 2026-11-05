# Qualitative scoring, pass 2 (reverse order V3, V2, V1)

C1 | V3: MET - R3-1..R3-9 touch Tasks 1-9; verified list covers Tasks 3,5 | V2: MET - "Checked every requirement-bearing span of source.md lines 1, 5-9" | V1: MET - "every clause of source.md lines 1-9 checked"; Tasks 1-9 cited
C2 | V3: MET - R3-2 "fails with a KeyError rather than because exports missing" | V2: MET - R2-1 "executor who writes the mandated bullet fails the grep" | V1: MET - R1-8 "'not set' assertion would fail or pass by accident"
C3 | V3: MET - R3-9 "Tasks 2 and 3 link to a page Task 6 creates later" | V2: NOT MET - no task dependency or prerequisite finding | V1: MET - R1-4 "true only after the launcher change"
C4 | V3: MET - R3-1 "whole policy test file passes, saved to ./artifacts/final-policy.log" | V2: MET - R2-1 "Fix: change the AC grep to grep -n -- --models" | V1: MET - R1-2 "Recommendation: add D12 line 235 to Task 2"
C5 | V3: MET - R3-8 "Task 8 is scope creep ... not requested by spec" | V2: MET - R2-2 "parser machinery ... state the cli_portify comment/regex stays" | V1: MET - Self-confidence "Could not run git, pytest or cmp"
K1 | V3: MET - R3-1 claim matches plan:30,33,52; commit claim flagged [INFERRED] | V2: MET - R2-1 substring claim holds against plan:62,65 | V1: NOT MET - "No defect found that would make a task fail" misses Task 3 grep; R1-6 wrong (plan names no module)
K2 | V3: MET - R3-5 fixes keep ccsession-tag read-only via allow-list | V2: MET - R2-1 one-line grep change within constraints | V1: MET - R1-10 "extend the AST scan ... ccsession-tag allow-listed"
K3 | V3: MET - consistent blocking/minor, Task N, plan:line usage | V2: MET - consistent blocking/minor and plan:line citations | V1: MET - consistent minor labels and file:line citations
K4 | V3: MET - FAIL verdict matches two blocking findings | V2: MET - FAIL verdict matches one blocking finding | V1: NOT MET - "no defect that would make a task fail" vs R1-9 tiers.md:40 unedited
K5 | V3: MET - each finding cites plan:line and repo file:line | V2: MET - "chains.md:11-13,21", "plan:62", "plan:65" cited | V1: MET - "defaults.sh:48,37,69,67", "retry.md:162" cited
T1 | V3: MET - Verdict, blocking findings first, Verified, Coverage, Self-confidence | V2: MET - Verdict, blocking R2-1 first, Coverage audit, Self-confidence | V1: MET - Verdict, Findings, Verified, Coverage audit, Self-confidence
T2 | V3: MET - H2 sections with bulleted R3-n findings | V2: MET - H2 sections with bulleted R2-n findings | V1: MET - H2 sections with bulleted R1-n findings
T3 | V3: NOT MET - R3-9 bundles about seven unrelated nits in one finding | V2: MET - five findings, one issue each | V1: MET - twelve findings, one issue each
T4 | V3: MET - ids R3-1..R3-9 with plan:line cross-references | V2: MET - ids R2-1..R2-5 with plan:line cross-references | V1: MET - ids R1-1..R1-12 with file:line cross-references
T5 | V3: MET - Verdict, Findings, Coverage audit, Self-confidence 0.85 present | V2: MET - Verdict, Findings, Coverage audit, Self-confidence 0.86 present | V1: MET - Verdict, Findings, Coverage audit, Self-confidence 0.78 present
L1 | V3: MET - R3-1 states exact path, text and missing check | V2: MET - R2-1 names exact grep and exact substring | V1: MET - R1-1 names exact variables and values
L2 | V3: MET - "48 agent files, only 17 have a model: line" | V2: MET - "src/superclaude/cli/cli_portify/steps/discover_components.py:60,121" | V1: MET - "docs/testing/v5.0.0/user/D12-reflect.md:235 pins --model claude-opus-4-8"
L3 | V3: MET - each H2 section has distinct role | V2: MET - each H2 section has distinct role | V1: MET - each H2 section has distinct role
L4 | V3: NOT MET - "INF-010", "brief's coverage slice", "match score is none 0.5" undefined | V2: NOT MET - "INF-011 is a matcher false negative" undefined; "AC-1" undefined | V1: MET - "legacy T1Model slots" explained via defaults.sh:63-65
L5 | V3: MET - "Fix:" stated in R3-1..R3-8 | V2: MET - "Fix:" stated in every finding R2-1..R2-5 | V1: MET - "Recommendation:" in most findings, e.g. R1-1, R1-2, R1-9
R1 | V3: NOT MET - severities given but no probability for any risk | V2: NOT MET - severities only; "Residual risk" has no probability | V1: NOT MET - all "minor"; no probability statements
R2 | V3: NOT MET - R3-9 nits carry no fix | V2: MET - every finding R2-1..R2-5 has a Fix | V1: NOT MET - R1-5 and R1-11 carry no recommendation
R3 | V3: MET - R3-2 KeyError failure mode plus scratch-run recovery | V2: MET - R2-1 unsatisfiable grep failure plus replacement grep | V1: MET - R1-7 grep tripped by new files; "note in Tasks 1 and 6"
R4 | V3: MET - R3-3 "depends on the runner's environment", workspace exports ids | V2: NOT MET - no external dependency or its failure discussed | V1: MET - R1-1 /etc/aidev02/aienv.d/defaults.sh exports activate ladder
R5 | V3: MET - final acceptance criterion running whole policy test file | V2: MET - R2-5 "Fix: name a grep or drop it" | V1: MET - R1-1 "add a Task 5 acceptance criterion recording the activation"
E1 | V3: MET - R3-4 files lacking model: line; commands/issue.md "matches nothing today" | V2: NOT MET - scan scope only, no empty/missing-element boundary | V1: NOT MET - scope gaps only, no empty/missing-element boundary
E2 | V3: MET - R3-3 _launch_env copies os.environ; _isolated fixture leaves ANTHROPIC_DEFAULT_* | V2: NOT MET - no cross-component state interaction raised | V1: MET - R1-1 workspace exports turn on retry.md primary ladder
E3 | V3: MET - R3-9 launcher checks CCSESSION_EXT_PROFILE != 1, rule omits it | V2: MET - R2-2 sweep "has no acceptance criterion" | V1: MET - R1-10 "Today no violations exist (guard-strength gap)"
E4 | V3: MET - R3-4 "48 agent files, only 17 have a model: line" | V2: MET - "six expected-red tests are red ... other two pass" | V1: MET - mirrors "404 lines ... 175 lines ... equal line counts"
E5 | V3: MET - R3-1 "Task 2 breaks the Task 1 claude-gw-tier test" | V2: MET - "no test pins an edited string" across edited files | V1: MET - R1-7 Task 5 grep tripped by Task 1 test or Task 6 doc

## Subtotals per dimension

| Dimension | V3 | V2 | V1 |
|---|---|---|---|
| Completeness (C1-C5) | 5 | 4 | 5 |
| Correctness (K1-K5) | 5 | 5 | 3 |
| Structure (T1-T5) | 4 | 5 | 5 |
| Clarity (L1-L5) | 4 | 4 | 5 |
| Risk coverage (R1-R5) | 3 | 3 | 3 |
| Invariant and edge-case coverage (E1-E5) | 5 | 3 | 4 |
| **Total (of 30)** | **26** | **24** | **25** |
