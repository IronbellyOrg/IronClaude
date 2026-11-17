# E4 validation report (M-30)

File: `MERGED-review-panel-unification.md`
Result: PASS

Run by `adversarial/partials/merge-scripts/e4_validate.py` (read-only; this report is its only output).

## 1 H2 sections: Merge Notes, ToC, Baseline, 1-10 in order, Appendix A-F; no other H2: PASS

19 H2 headings
- Merge Notes
- Table of Contents
- Baseline and Conventions
- 1. Problem Statement
- 2. Current State Analysis
- 3. Target State
- 4. Gap Analysis
- 5. External Research Findings
- 6. Options Analysis
- 7. Recommendation
- 8. Value Inventory, Migration and Value-Capture Content, and Inputs for a Later Plan
- 9. Open Questions
- 10. Evidence Trail
- Appendix A: Value Inventory Rows (separate file in the report package)
- Appendix B: Synthesis Notes Carried from synth-01
- Appendix C: Contradiction register (run 1 vs run 2)
- Appendix D: Compare-debate invariant probe
- Appendix E: Corrections applied and counts with units
- Appendix F: Provenance index

## 2 Heading levels: one H1, no level gaps: PASS

H1 at lines [7]
level jumps: 0

## 3 Every block carries a Source comment (provenance header first): PASS

39 parts checked; first three lines are the provenance header: True

## 4 No `Closed item R1-C-` / `GQ:R1-C-` / `GQ R1-C-` token (R3-B1 escalation): PASS

R1-CLS-nn tokens in the merged file: 107
bad tokens: 0

## 5 The four deleted `**Dependencies:**` lines (V1:3829, 3860, 3879, 3897) are absent: PASS

V1:3829 `**Dependencies:** none outside this track for M1-01 to M1-06; M1-07 an...`: absent
V1:3860 `**Dependencies:** M1-02, M1-06, M1-09, M1-10, M1-11 and M1-12 for the ...`: absent
V1:3879 `**Dependencies:** M1-01, M1-09, M1-10, M1-11, M1-15 and M1-16 for the ...`: absent
V1:3897 `**Dependencies:** core: M1-01 to M1-06 and M1-09 (the open registry, l...`: absent
lines starting `**Dependencies:**` in 8.4: []

## 6 All 48 run 1 step ids R1-M1-01..R1-M4-07 appear in 8.4 with a status: PASS

step rows with status: 48; counts {'CONFLICTS': 13, 'PARTLY COMPATIBLE': 14, 'COMPATIBLE': 21}

## 7 Appendix C has all 63 X rows: PASS

rows 63, unique 63

## 8 Every promoted shared assumption is addressed (Merge Notes, 9.12, Appendix C/D/E): PASS

| A id | Where (first hits) |
|---|---|
| A-002 | Appendix D (line 9850); E.3 (line 9948) |
| A-006 | Appendix D (line 9868); E.3 (line 9948) |
| A-008 | E.3 (line 9952) |
| A-012 | E.3 (line 9953) |
| A-018 | E.3 (line 9954) |
| A-019 | E.3 (line 9955) |
| A-024 | E.3 (line 9956) |
| A-027 | E.3 (line 9957) |
| A-036 | Appendix D (line 9850); E.3 (line 9948) |
| A-037 | E.3 (line 9958) |
| A-038 | E.3 (line 9959) |
| A-041 | E.3 (line 9960) |
| A-052 | E.3 (line 9961) |
| A-055 | E.3 (line 9962) |
| A-056 | E.3 (line 9963) |
| A-057 | E.3 (line 9964) |
| A-058 | Appendix D (line 9868); E.3 (line 9948) |
| A-059 | E.3 (line 9965) |

## 9 Git-ref constraint in base C4 and in 8.7; owner prefix `feat_review-panel/<name>` in 8.7: PASS

C4 rows: 1; phrase in C4: True
phrase in 8.7: 2 times
`feat_review-panel/<name>` in 8.7: 1 times

## 10 `no-regression` occurs in run 2's 8.2(b) and in run 1's 8.5: PASS

lines in 8.2(b): 1; lines in 8.5: 2
lines per part: Merge Notes: 1; Table of Contents: 1; 8. Value Inventory ... (8.1, 8.2): 1; 8.5 Run 1 no-regression gates: 2; 9.11 Run 1 open questions: 2; 9.12 Open items raised by the compare debate: 1; Appendices D and E: 3; Appendix F: Provenance index: 3

## 11 High-value unique rows of both variants have a home (token check): PASS

High U rows in diff-analysis.md: 62 (V1 20, V2 42)
Prompt tokens: Appendix A pointer: yes; C29: yes; G27: yes; AE-15: yes; ENS-4: yes; MS-24: yes; R1-D1: yes; R1-C-14: yes; R1-V-001: yes; R1-M1-01: yes; G-133: yes
U-099: only the git constraint is required; the layout table V1:4063-4069 is dropped on purpose (M-19, M-23)

| U id | Report | Token(s) | Found |
|---|---|---|---|
| U-001 | V1 | `R1-MS-14`, `unauthorized_deviation_present` | yes |
| U-002 | V1 | `R1-MS-24` | yes |
| U-003 | V1 | `R1-ENS-4` | yes |
| U-005 | V1 | `R1 4.3 Critical and Important rows by track` | yes |
| U-010 | V1 | `R1-SC-6`, `R1-SC-10` | yes |
| U-018 | V2 | `G-03/G-17` | yes |
| U-020 | V2 | `G-14`, `G-15` | yes |
| U-021 | V2 | `G-70` | yes |
| U-022 | V2 | `Sweep Sheet` | yes |
| U-023 | V2 | `044809e3` | yes |
| U-024 | V2 | `model_scores` | yes |
| U-025 | V2 | `G-133` | yes |
| U-026 | V2 | `G-146` | yes |
| U-027 | V2 | `G-55` | yes |
| U-029 | V2 | `G-86` | yes |
| U-031 | V2 | `G-108` | yes |
| U-032 | V2 | `D-14` | yes |
| U-035 | V2 | `ec259f1b7` | yes |
| U-036 | V2 | `insufficient` | yes |
| U-037 | V2 | `reflect_shadow_exit.py:313` | yes |
| U-040 | V2 | `lib/` | yes |
| U-042 | V2 | `snap.py:4` | yes |
| U-044 | V2 | `install_commands.py:41-79` | yes |
| U-045 | V2 | `T2bModel01` | yes |
| U-046 | V2 | `P-d` | yes |
| U-047 | V2 | `DR-171` | yes |
| U-048 | V2 | `tasklist validate` | yes |
| U-049 | V2 | `lint-architecture` | yes |
| U-051 | V2 | `verify-run` | yes |
| U-054 | V2 | `--bare` | yes |
| U-056 | V2 | `rdjson` | yes |
| U-058 | V1 | `Reflect v2 shares it?` | yes |
| U-064 | V1 | `R1 5.2` | yes |
| U-065 | V1 | `R1 5.4` | yes |
| U-066 | V1 | `R1 5.3` | yes |
| U-068 | V1 | `R1 5.5` | yes |
| U-071 | V2 | `189` | yes |
| U-072 | V2 | `60 HIGH` | yes |
| U-073 | V2 | `INV-N` | yes |
| U-074 | V2 | `17 of 17` | yes |
| U-075 | V2 | `CO-14` | yes |
| U-076 | V2 | `M14` | yes |
| U-077 | V2 | `CO-34` | yes |
| U-086 | V1 | `R1-D-1`, `R1-C-14` | yes |
| U-087 | V1 | `R1 6.D` | yes |
| U-088 | V1 | `R1 6.E` | yes |
| U-096 | V1 | `R1-M1-01`, `R1-M4-07` | yes |
| U-097 | V1 | `R1-G2` | yes |
| U-098 | V1 | `1182`, `R1-G-pr` | yes |
| U-099 | V1 | ``feat/review-panel/<name>`` | yes |
| U-100 | V1 | `review-panel-manifest/1` | yes |
| U-101 | V1 | `##### Gap coverage` | yes |
| U-102 | V1 | `R1-X14`, `R1 7.2` | yes |
| U-110 | V2 | `synth-08-value-inventory` | yes |
| U-111 | V2 | `P3-014` | yes |
| U-112 | V2 | `C29` | yes |
| U-113 | V2 | `D26` | yes |
| U-114 | V2 | `AE-15` | yes |
| U-115 | V2 | `A-20` | yes |
| U-116 | V2 | `7.2.4` | yes |
| U-117 | V2 | `rowcheck` | yes |
| U-118 | V2 | `Q-40` | yes |

## 12 Internal references in new text resolve to headings: PASS

`Section n.m` / `Appendix X` references in new text: 72; unresolved: 0
merged-numbering pointers checked: 24; missing headings: []

## 13 New text adds no roadmap, schedule, PR plan or branch plan (every hit justified): PASS

new-text lines scanned: 394; hits: 6

| Line | Word | Justification | Context |
|---|---|---|---|
| 76 | `roadmap` | negation or scope exclusion (states that the document adds no such content) | **(h) Scope.** This document adds no roadmap, no branch plan, no pull-request plan a |
| 76 | `branch plan` | negation or scope exclusion (states that the document adds no such content) | **(h) Scope.** This document adds no roadmap, no branch plan, no pull-request plan and no schedule. |
| 76 | `pull-request plan` | negation or scope exclusion (states that the document adds no such content) | **(h) Scope.** This document adds no roadmap, no branch plan, no pull-request plan and no schedule. Run 1's migration step |
| 76 | `schedule` | negation or scope exclusion (states that the document adds no such content) | **(h) Scope.** This document adds no roadmap, no branch plan, no pull-request plan and no schedule. Run 1's migration steps, gates and ris |
| 8855 | `branch plan` | names the run 1 content that was dropped as a branch plan | Run 1's five-layout options table (V1:4063-4069) is a branch plan and is not carried; the git constraint |
| 9372 | `scheduled` | negation or scope exclusion (states that the document adds no such content) | 043, X-054) / Is engine A (`ensemble.py`) fixed in place now? / No engine moves now; production Tier 2 stays engine A; the single-engine decision is n |

## 14 Contradiction re-scan against Appendix C: PASS

- PASS: X-021: no `195 of 1,398` left in base or carried text
- PASS: X-025: every `3 of 3 slots` in carried text carries the X-025 correction
- PASS: X-026: no `3 plus a merge that lost` left in carried text
- PASS: X-030/X-048: no `reflect's 5 [UNVERIFIED]` left
- PASS: X-017: base count "SKILL.md` (6)" corrected (9790)
- PASS: X-031: run 1 `same_defect` line carries the both-empty-refs branch
- PASS: pr_submit count: no uncorrected `50 ... files` statement in base or carried text
- PASS: X-036: every base line citing arXiv 2606.19544 is marked withdrawn (unmarked lines outside base: 3122 (5.6 Run 1 external f))
- PASS: X-020/X-049/X-053: base `KeyError` lines are corrected or are the two kept sites (uncorrected base lines: 692; 7460)
- PASS: X-022/X-029/X-061: every carried `43 call sites` carries the unit note
- PASS: Appendix C: every `Where handled` section exists and every verdict equals the regenerated matrix
- PASS: Appendix C OPEN rows are carried as open items (9.12) or as the label split (X-051, Merge Notes) (open rows ['X-040', 'X-041', 'X-051', 'X-056', 'X-057', 'X-058'])

## 15 No stale debate numbers in new text; no leftover markers; no double prefixes; V2:108 note de-duplicated: PASS

stale tokens: 0
markers left: 0
duplicate origin/master note: []
double prefixes: 0

## 16 Table of Contents: every entry matches exactly one heading; every H2/H3 has an entry; `---` after the ToC: PASS

entries 146 (H2 18, H3 98, H4 entries for 6.13 and 7.4 30)
entries without exactly one heading: 0
H2/H3 without an entry: 0
`---` after ToC: True

## 17 Counts (report): INFO

total lines: 10109; bytes: 2629571
headings by level: {1: 1, 2: 19, 3: 98, 4: 194, 5: 115}
R1- prefixed tokens: 8128; R1-CLS-nn: 107; R25-INV-nnn: 172
new-text lines (assembler list): 394

| H2 section | Start line | Lines | Headings (H2-H6) |
|---|---|---|---|
| Merge Notes | 20 | 62 | 1 |
| Table of Contents | 82 | 153 | 1 |
| Baseline and Conventions | 235 | 36 | 1 |
| 1. Problem Statement | 271 | 15 | 1 |
| 2. Current State Analysis | 286 | 1270 | 26 |
| 3. Target State | 1556 | 222 | 8 |
| 4. Gap Analysis | 1778 | 522 | 15 |
| 5. External Research Findings | 2300 | 974 | 70 |
| 6. Options Analysis | 3274 | 3119 | 185 |
| 7. Recommendation | 6393 | 989 | 29 |
| 8. Value Inventory, Migration and Value-Capture Content, and Inputs fo | 7382 | 1539 | 40 |
| 9. Open Questions | 8921 | 458 | 18 |
| 10. Evidence Trail | 9379 | 357 | 20 |
| Appendix A: Value Inventory Rows (separate file in the report package) | 9736 | 4 | 1 |
| Appendix B: Synthesis Notes Carried from synth-01 | 9740 | 28 | 1 |
| Appendix C: Contradiction register (run 1 vs run 2) | 9768 | 76 | 1 |
| Appendix D: Compare-debate invariant probe | 9844 | 45 | 1 |
| Appendix E: Corrections applied and counts with units | 9889 | 82 | 4 |
| Appendix F: Provenance index | 9971 | 139 | 3 |
