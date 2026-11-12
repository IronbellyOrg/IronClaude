# QA Report — Fix Cycle (report-qualitative, source-fidelity gate, cycle 1 verification)

**Topic:** Orchestrator mode Phase 1 (issue #339) research report
**Date:** 2026-11-08
**Phase:** fix-cycle (report-qualitative lens)
**Fix cycle:** 2 (third and last review of the Phase 6 fidelity gate)
**Fix authorization:** false (report not edited)
**Inputs:** `RESEARCH-REPORT-orchestrator-mode.md` (1740 lines), `qa/qa-fidelity-consolidated-findings-cycle1.md` (C1-01 to C1-04), `qa/qa-fidelity-fix-log-cycle1.md`

---

## Overall Verdict: PASS (with notes)

All four cycle-1 blocking findings (C1-01 to C1-04) are RESOLVED. No new blocking finding. Open blocking: 0. MINOR notes are recorded below and do not fail the review.

## Findings (C1-01 to C1-04)

| ID | Status | Evidence (report lines, 1740-line version) |
|---|---|---|
| C1-01 | RESOLVED | "Rule 1's condition" (row settled, brief `report blocked`, or an `/sc:implement` Ruling halt E-HALT-QA / E-NO-RULING) appears in every statement. Rule 1 and its skip are at `:113`. Rule 4's contract halves are gated by it at `:113` and `:116` ("A blocked contract counts under 4a or 4b-contract only when rule 1's condition holds"). The 3.1 diagram is conditional at `:371-385`. The 3.1 policy bullet is conditional at `:406`. GQ-02 is conditional at `:525`, and the GQ-96 accepted-gap row at `:579`. The Option A1 diagram is conditional at `:957-958`. Step 1.3 is conditional at `:1224` (4a counts `blocked_question` only under the condition; 4b-contract freezes on `blocked` only under it; the skipped case gets policy "could not determine" with the may-be-re-running note, never "not frozen"). Step 1.8 fixtures at `:1234`: 4a uses a settled row; GQ-96 uses a settled row or `report blocked`; there is a live ask-the-coordinator case (no class from 1/4a/4b-contract) and a live E-HALT-QA case ((a) and frozen). The gap-to-step GQ-96 row is conditional at `:1358`. Checked against `WORKER-CONTRACT.md`: WC-2 `:30`, WC-3 `:52-57`, the freeze rule `:133`. The fixtures no longer contradict each other: the rule-1 skip fixture and the 4a fixture now use different inputs. |
| C1-02 | RESOLVED | The 8.2 row at `:1414` now reads "S9 rows 8, 9, 30, 51, 53" and "all five", and Blocks reads "WC-14 rule id, ...". It states that G6 / GQ-09 / S9 row 7 is settled by the sources. S9 rows 8, 9, 30, 51, 53 (`:1526`, `:1527`, `:1548`, `:1570`, `:1572`) are GQ-10, GQ-11, GQ-35, GQ-61, GQ-63, the same five that §7 `:1076` and step 1.0b `:1216` name. A sweep of the whole report for "all six", "six decisions", "G6 wording" and "rows 7, 8" finds none left. The only "all six" is `:1288` "all six modules", which counts package modules and is unrelated. Every GQ-09 mention (`:68`, `:324`, `:443`, `:531`, `:649`, `:1076`, `:1216`, `:1324`, `:1414`, `:1525`, `:1596`, `:1660`) says it is settled. |
| C1-03 | RESOLVED | Step 1.2 `:1223`: WorktreeState has `unpushed` and `dev_tasks_unsaved`. Step 1.4 `:1225`: the git allowlist includes `status`. Step 1.8 `:1234`: `patch_git` fixtures for a branch with no upstream, a branch ahead of upstream, an untracked path and an unstaged path under `.dev/tasks/`, plus `CalledProcessError`. Step 1.9 `:1235`: one safe-to-close case per fixture asserting "worktree removable: no" with the condition named, plus a failed-git case asserting `None` and "could not determine". SC-4 at `:458` names these tests. This covers `seed-brief.md:60` and `:68`. |
| C1-04 | RESOLVED | The rollback rationale at `:1284` now covers the step 1.21(b) "Orca coordination" bullets ("removed command" argument). The "Four registries" row at `:1292` reverts the coordinator-runs-`/sc:sweep` bullet and the `/sc:sweep` mention in the never-as-worker bullet, and re-copies the plugin byte copy after both reverts (and in the follow-up PR if part (b) moved there, matching step 1.23). |

## New blocking findings

None.

## Items Reviewed

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Problem statement matches findings | PASS | The fixes stay within Phase 1 classification, safe-to-close and rollback; none moves into adjacent topics. |
| 2 | Current state analysis is current | PASS | WC-2 `:30`, WC-3 `:52-57`, WC-5 `:58`, WC-10 `:45`, `:108` and the freeze rule `:133` were re-read in `WORKER-CONTRACT.md`; the report's citations match. |
| 3 | Options are genuinely distinct | PASS | The fixes did not change the option set; A1 to A4 are still distinct. |
| 4 | Recommendation follows from analysis | PASS | §7 `:1076` recommends A1, and the Option A1 diagram `:957-958` is aligned with the new rule 1 condition. |
| 5 | Implementation plan is actionable | PASS | Steps 1.2, 1.3, 1.4, 1.8 and 1.9 (`:1223-1235`) name the fields, conditions, fixtures and assertions a developer needs. |
| 6 | Gaps are honest | PASS | The source-to-source conflict (Section C rule 1 and 4a and GQ-96 are stated unconditionally, versus WC-3) is named. GQ-96 stays an accepted gap with conditional wording (`:579`). |
| 7 | External research is relevant | PASS | No external research was added by the fixes, and none was needed for this review. |
| 8 | Scale claims are substantiated | PASS | No scale claims were added. Safe-to-close "worktree removable" is still never "yes" in Phase 1. |
| 9 | Risk assessment is complete | PASS | The rollback now covers the 1.21(b) bullets (`:1284`, `:1292`). `.dev/tasks/` is never disposable (`seed-brief.md:60`) and is tested in step 1.9. |
| 10 | Evidence trail is complete | PASS | The new claims cite `WORKER-CONTRACT.md` and `seed-brief.md` lines, and the cited lines say what the report says. |
| 11 | No circular reasoning | PASS | The rule 1 condition rests on WC-3 and WC-4 in the source contract, not on the report's own synthesis. |
| 12 | Conclusion is proportionate | PASS | A1 is still recommended with five open owner decisions as working defaults. Nothing claims more certainty than before. |
| S1 | No fix contradicts another section | PASS | The C1-01 sweep (rule 1, 4a, 4b-contract, GQ-96, the diagrams and the fixtures) found every statement conditional. The C1-02 sweep found no "six decisions" left. Line 484 ("frozen plan is waiting on a person") is consistent with the conditional rule. |
| S2 | Section 8 plans the option Section 7 recommends | PASS | §7 `:1076` recommends A1, and §8 `:1169` plans A1. |
| S3 | WC-10 holds (absence of a signal is never death) | PASS | "Stalled" needs Orca stall proof (rule 2). The rule-1 skip gives "could not determine", never stalled and never "not frozen". The SC-5 test is still in place. |
| S4 | Option A4 is not recommended | PASS | A4 is rejected at `:1171`. |
| S5 | Later phases are recorded, not designed | PASS | `:1300-1311` gives each later phase one line with its blockers, and no design. |
| S6 | NB-4 record and both [CONTRADICTION] markers kept | PASS | Present and unchanged (the fix log's `grep -c` was re-checked by reading the marked areas). |

## MINOR notes (not blocking, not rechecked)

1. The fix log labels a "Section 7 (precedence diagram)" fix. Section 7 has no diagram; the diagrams are in 3.1 (`:371-385`) and at `:956-958`. This is a log mislabel only.
2. "Falls through to 5 or 7" for the skipped case leaves out rules 2, 3 and 4's agentWait half, which can still match.
3. The step 1.8 assertion "working or could not determine" for the live ask-the-coordinator fixture is not deterministic unless the fixture fixes agentWait. Pin it to keep SC-4 "deterministic" literal.
4. The 4a contract half needs rule 1's condition, but rule 1 has already matched those inputs, so it cannot be reached. The 4a fixture therefore duplicates the rule-1 settled fixture.
5. The step 1.2 policy value list ("frozen / not frozen", unknown prints "unknown") does not include the "could not determine" value that step 1.3 now prints for the skipped case.
6. `:133` (the freeze rule reads the latest contract) is cited as support for "could not determine". The report does not name the tension between `:133` and WC-3's re-run replacement.
7. The skipped-case policy wording is applied to non-implement contracts too, where no Ruling halt can occur. This is harmless but broader than the source.
8. Step 1.4 does not say how `git status --branch --porcelain` output is parsed for "no upstream" and "ahead".
9. For a failed git call, the "could not determine" string alone cannot tell it apart from other could-not-determine cases. The `None` field assertion can.
10. The `:363` git command list leaves out `stash list`, which the step 1.4 allowlist (`:1225`) has. This is older text.
11. The `:1298` partial-revert sentence does not mention the 1.21(b) bullet, while the `:1292` row does.

## Confidence gate

- **Confidence:** Verified: 18/18 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 16 | Grep: 2 | Glob: 0 | Bash: 7. Read + Grep (18) is at least the 18 checks. No web research was done, so Tavily was not needed.

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- No `## Inherited Structural Verdict` block was in the spawn prompt. I fell back to standalone checking and relied on no rf-qa PASS item. I did not re-run the fix log's NB-4 / CONTRADICTION `grep -c` counts; I checked those areas by reading them.

**(b) Independent semantic checks (≥1 required, INV-019):**
- Rule 1's condition is consistent everywhere. I swept `:113`, `:116`, `:371-385`, `:406`, `:525`, `:579`, `:957-958`, `:1224`, `:1234` and `:1358` with windowed Reads, and checked them against `WORKER-CONTRACT.md` WC-2 `:30`, WC-3 `:52-57` and `:133`.
- No "six decisions" remain. I grepped the whole report for "all six", "six decisions", "G6 wording" and "rows 7, 8", and printed S9 rows 7, 8, 9, 30, 51 and 53 (`:1525-1572`) to check that the five decisions match.
- The git safe-to-close tests are traceable from the step 1.2 fields through the step 1.4 allowlist to the step 1.8 fixtures, the step 1.9 assertions and SC-4 `:458`.
- I read the rollback rows `:1284`, `:1292` and `:1298` against step 1.21(b).

## Verdict: PASS
