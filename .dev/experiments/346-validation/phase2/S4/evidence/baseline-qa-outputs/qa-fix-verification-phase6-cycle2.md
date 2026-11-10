# QA Report - Gate 3 Fix Verification, Fix Cycle 2 (last cycle), Agent 1 of 2

**Topic:** BMAD first-use directory creation in a project that never had BMAD
**Status:** Complete
**Date:** 2026-11-08
**Phase:** fix-cycle (fix_authorization: false)
**Inputs:** `qa/qa-consolidated-findings-phase6-cycle2.md` (5 blocking rows), `qa/qa-fix-log-phase6-cycle2.md`, `RESEARCH-REPORT-bmad-first-use.md` (1795 lines, line count unchanged by the fixes)

---

## Part A. The five blocking rows (report re-read at the cited lines)

| # | Finding | Result | Evidence |
|---|---|---|---|
| 1 | F-1: D2 left at "S (4 files)" | FIXED | L1137 D2 cell now "**L** as planned in Section 8 (S on the researched minimum)" with the 8-file list shown (new `20-*.json`, `Dockerfile.coder`, `main.tf`, `test-73`, `manifest.yaml`, `README.md`, new test, `coder-ci-aidev02-contract.yml`); L1227 Table 1 D2 cell "L as planned (8 files; S on the researched minimum, 4 files; one delivery layer, image)"; L1299 Stage 1 "Why" names D2 (8 files). Rubric L1004 says L = 8 or more files, so L is consistent with the stated count. Grep for `S (4 files)` returns no match. The fix deviates from the proposed M and shows why. |
| 2 | B-1: Phase 4 gate order stated four ways | FIXED | One order now in every place: L1463 heading ("none is shipped or relied on before the gate below has observed its facts on the candidate build"); L1478 gate heading "Gate before relying on any branch (observed on the candidate build of the chosen branch, steps 4B.1 and 4B.2, or 4D.1 to 4D.3 for D3, or 4D.6 for D2, drafted and not shipped)"; L1488 Rule row "A failed Fact 1 discards the draft"; L1300 Stage 2 "Before relying on the chosen branch, observe on its candidate build (drafted, not shipped)"; L1669 "observed on the candidate build of the chosen branch (drafted, not shipped) before B or D is relied on"; L1694 row 4 "on the candidate build of the chosen branch (drafted, not shipped) before relying on B or D". Grep for `Gate before any branch` and the old L1669 wording: no match. Grep `candidate build|Phase 4 gate` over the whole file shows no contradicting variant (L1497, L1517, L1600, L1681, L1705, L1709, L1713 only refer to "the Phase 4 gate"). |
| 3 | B-2: open owner defaults recorded as `(constraint)` | FIXED | L1452 Phase 3 header: defaults of steps 3.2 to 3.4 are `--type assumption` ("plan default pending owner, Section 9 rows 5, 6, 10"), owner inputs `--type question`, only step 3.6 prohibitions `--type constraint`, the owner answer a superseding `--type decision`; CAP-8 success text says the command and predicate are defaults until rows 5, 6, 10 are answered. Same wording at L1298 (Stage 0 (c)), L1383 (step 1.1) and L1656 (checklist). Source claims re-read: `.claude/skills/bmad-spec/SKILL.md:54` (memlog canonical, append-only, never edited), `:61` (types decision, constraint, capability, assumption, question, direction, note, event), `_bmad/scripts/memlog.py:164-177` (`cmd_append` only appends at the end; `cmd_set` at :180 edits front matter only; no entry edit or delete), `memlog.py:116-119` (`touch` stamps `updated`). All hold. Remaining `(constraint)`/`type constraint` hits: L409 (describes the existing memlog), L1298, L1383, L1452, L1656 (all limited to step 3.6 as the consolidated fix prescribed). |
| 4 | B-3: "cheapest" while Effort is disclaimed | FIXED | Grep `cheapest` returns no match in the report. L1091 Pros now "Lowest risk of the three (no certain break, 0 layers)". L1311 Rationale 4 rests on "Risk, Image layers, HOME persistence rows (the grounds)" and names "Effort, Image rebuild rows (the price)" with "highest Effort of the skill deliveries as planned (L, against S for B1)". L1465 Phase 4 Goal says "evidence-ranked mechanism". L1299 and L1311 no longer disagree. |
| 5 | B-4: "template push only" for B3 and D3 | FIXED | Cells aligned: L1083 (B3 row: template push for `modules.tf` plus the `manifest.yaml` retag as planned), L1087 (B3 Effort L, two delivery layers), L1088 (Risk: "the only rebuild is the retag"), L1091, L1137 and L1141 (D3), L1227 (Effort L), L1234 ("Template push plus catalogue-hash retag as planned"), L1311, L1494 (4B.1), L1515 (4D.1), L1615 (7.7), L625 (K-05), L1691 (row 1). The one remaining `template push only` (L204) is the general root-`.tf` rule and stays true. Evidence re-read in code: `templates/VSCode-AIDev02/main.tf:74` (`catalogue_sha256` hashes `catalogue/**`), `:104-106` (folded into `image_inputs_sha256`), `:111` (image tag from it), `Dockerfile.coder:593` (`COPY --chown=0:0 catalogue /catalogue`, an existing COPY so 0 layers). Steps 4B.6 (L1499) and 4D.7 (L1521) do edit `manifest.yaml`, so the claim is consistent with the plan. |

Part A result: 5 of 5 blocking rows fixed.

---

## Part B. New blocking issue introduced by the fixes?

| # | Check | Result | Evidence |
|---|---|---|---|
| B1 | New false claims in the edited text (cited lines) | PASS | Every code citation added or touched by the fixes was re-read: `main.tf:74, 104-106, 111`, `Dockerfile.coder:139, 142, 143, 593`, `modules.tf:82, 109` (Grep), `memlog.py:116-119, 164-177`, `SKILL.md:54, 61`. All match the report wording. Rubric arithmetic: B3 = 6 files + 2 new tests = M by files, L by two delivery layers (image + Terraform); D3 = L by two layers; D2 = 8 files = L; B2 = 6 files = M; consistent with L1004. |
| B2 | Broken tables | PASS | Cell counts checked on every edited table row: L1083 (5 cells), L1087 and L1137 (4 cells), L1227 and L1234 (11 cells = criterion + A, B1, B2, B3, C, D1, D2, D3, E, F), L1299 and L1311 (3 and 3 cells), L1488 (2 cells). No raw pipe inside an edited cell. |
| B3 | Placeholders | PASS | Grep `TODO|TBD|FIXME|placeholder|XXX|lorem` over the report: no match. |
| B4 | Stale Table of Contents | PASS | Grep `^#{2,4} ` over the report: Sections 1 to 10 and every ToC subentry (2.1 to 2.6, 3.1 to 3.3, 4.1 to 4.5, 5.1 to 5.3, 6.0, options, comparison, 7 parts, 8 phases plus Persistence and Integration Checklist, 9 and 9.1, 10 parts) exist as headings at L10-L1786. |
| B5 | Hallucinated paths | PASS | Files named by the fix and checked: `.github/workflows/coder-ci-orca-proof.yml` and `coder-ci-aidev02-contract.yml` (Glob, exist), `templates/VSCode-AIDev02/modules.tf` and `image/catalogue/bmad/manifest.yaml` (Glob, exist), `_bmad/scripts/memlog.py`, `.claude/skills/bmad-spec/SKILL.md` (Read). Proposed new file `test-80-bmad-first-use.sh` is labelled "name proposed"; Glob shows tests run to test-79, so the number is free. |
| B6 | Contradictions between sections | PASS with notes | Full-file Grep for every term the fixes touched (`cheapest`, `template push`, `Effort`, `B3|D3`, `candidate build|Phase 4 gate`, `(constraint)`) found no remaining contradiction with the edited statements. Residual notes below (M-1 to M-6) are wording or count nits, not false statements about the rating, order or record type. |
| B7 | Document-only claim in Sections 2, 6, 7, 8 | PASS | The fixes added no external-docs claim; the doc-only gate content at L1478 and L1483 was already tagged `[UNVERIFIED - doc-only]` and is never the sole basis of a rating. |

Part B result: 7 of 7 checks pass; 0 new blocking issues.

## Part C. Structure

| # | Check | Result | Evidence |
|---|---|---|---|
| C1 | 10-section structure intact | PASS | `## 1. Problem Statement` L59, `## 2.` L74, `## 3.` L547, `## 4.` L634, `## 5.` L767, `## 6. Options Analysis` L986, `## 7. Recommendation` L1276, `## 8. Implementation Plan` L1351, `## 9. Open Questions` L1685, `## 10. Evidence Trail` L1746. Line count 1795 before and after (wc -l). |

---

## Notes (MINOR, not blocking, not required for the verdict)

| # | Location | Note |
|---|---|---|
| M-1 | L1004 vs L1022 vs L1137 | The D2 count of 8 files includes `README.md`, while the rubric says documents every option needs (row 12, which names the `README.md:241` reconcile) are not counted. Without `README.md` D2 is 7 files (M). The count is shown openly in L1137 and matches how Option A (L1056) and B3 (L1087) count README, so it is a rubric-wording gap, not a false statement. Not rechecked further. |
| M-2 | L1461 (step 3.6) vs L1452 | Step 3.6 is headed "Fixed prohibitions" yet its `bmad-` prefix rule is called open at the same step (Section 9 rows 2 and 3). The fix follows the consolidated proposal ("keep `--type constraint` only for the fixed prohibitions of step 3.6"), so it is not a defect of the fix; an implementer may still record that one rule as a constraint. |
| M-3 | L367 | Section 2.4 still says "the cheap variants ... B2, B3, D2 or D3", which sits oddly beside Effort L for B3, D3 and D2. Wording from the research summary. |
| M-4 | L1227 | "plan adds 2 new tests" (B3) and "3 new tests" (D3) do not count the step 5.4 check that `superclaude install --force` leaves the stub or hook unchanged (L1535); B3 would be 3 and D3 4. Class stays L (layers) and M for B3's file/test count. |
| M-5 | L1478 | For D2 the gate cites only step 4D.6; the hook body of 4D.3 also applies to the drop-in's command. |
| M-6 | L1230, L1236 | Table 1 "Integration complexity" for B3 and D3 ("1 file + 1 pin") and the "Pinned tests that break" cells for B3 and D3 (no `test-19`, `test-49`, `test-2` BREAKS-IF) describe the researched minimum and omit the planned `manifest.yaml` welcome edit that Option A (L1236) lists. Table 5.1 (L1568-1571, L1576) covers those tests for all options. Also L1746 `## 10.` follows a paragraph with no blank line (renders; MD022 style only). |
| M-7 | Option C (L1112) | The fix log observes C is rated M as planned and a count like D2's could reach 7 to 8 files; no finding names it; counts depend on the conditional step 5.4 case. Left to the owner. |

---

## Self-Audit

What I actively checked (tool evidence, this session):
- Read the cycle-2 consolidated findings (29 lines) and fix log (46 lines) in full, and line 407 of the task file (my embedded prompt).
- Read these report ranges in full with Read: L202-205, 365-368, 405-409, 622-627, 995-1342, 1326-1349, 1351-1625 (all of Section 8 Phases 1 to 7 up to Phase 7), 1626-1705 (Persistence checks, Integration Checklist, Section 9 rows 1 to 15), 1706-1715, 1744-1795, and L1-60 (ToC). Section 6 Options A to E, I, Table 1, Table 2, Section 7, and all of Section 8 and 9 rows 1 to 19 were read line by line.
- Ran Grep over the whole report for: `cheapest|template push|template push only|S \(4 files\)|Gate before any branch|before B or D is relied|no rebuild`; `B3|D3` (every hit with context); `Effort` (every hit); `candidate build|Phase 4 gate|gate before`; `(constraint)|type constraint|canonical`; headings `^#{2,4} `; `TODO|TBD|FIXME|placeholder`. Each of the five rows was reproduced by reading the cited line, not from the fix log.
- Verified in code: `main.tf:74, 80, 104-106, 111`; `Dockerfile.coder:139, 142-143, 593`; `modules.tf:82, 109`; `memlog.py:110-199`; `SKILL.md:44-68`; Glob of contract tests, workflows and manifests; `wc -l` of the report (1795).

What I did NOT read in full: report L60-201, 206-364, 368-404, 410-621, 628-994 (Sections 1 to 5 and parts of 2 and 4). I only grepped those ranges for the terms above and for the K-05 and SC-14 lines that the fixes touched (L611, L615, L625). A contradiction there that uses different words than my search terms is UNVERIFIED. The fixes edited no line in L60-994 except L625, which I read.

Why the finding count is credible: 0 blocking findings and 7 minor notes. The five rows each had specific textual claims that I located and compared at every cited line and by whole-file search; two of them (rows 1 and 5) could have failed on a missed cell and the grep for stale phrases came back clean. I looked for new defects in the most likely places (rating cells that were re-rated, the rubric arithmetic, the memlog record types against `SKILL.md:61`, the gate order in all six places, the Table 1 cell counts) and found only count or wording nits that do not make a statement false. The notes M-1 and M-2 were weighed as possible new blocking issues and rejected because the report shows the counting basis openly (M-1) and the fix follows the consolidated finding's own proposed wording (M-2).

## Confidence (Confidence Gate Protocol)

- **Confidence:** Verified: 13/13 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 24 | Grep: 14 | Glob: 3 | Bash: 1 (wc -l and git status of the report)
- Limit: the unread ranges named in the Self-Audit are grep-checked only.

## Summary

- Checks passed: 13 / 13 (5 blocking rows, 7 new-issue checks, 1 structure check)
- Checks failed: 0
- Blocking issues (unfixed or new): 0 (CRITICAL 0, IMPORTANT 0)
- Minor notes: 7 (M-1 to M-7), not blocking
- Issues fixed in place: 0 (fix_authorization: false; only this report file was written)

## Overall Verdict: PASS

All five cycle-2 blocking rows are fixed in the cited report sections, no new blocking issue was introduced, and the 10-section structure and Table of Contents are intact.

## QA Complete
