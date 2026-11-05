# QA Report: Phase 6 Qualitative Fix Verification, Cycle 2

**Topic:** Fresh content check of the report-gate cycle-2 corrections (groups G1-G9) to `RESEARCH-REPORT-review-loops.md` (Task Step 6.21, cycle 2)
**Date:** 2026-10-24
**Phase:** report-validation verification (qualitative), fix cycle 2 of 3
**Fix authorization:** false. Report only. No file was edited.
**Package root (R):** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/`
**Target state checked:** the report has 1,310 lines and SHA-256 `23531e10a42591e053cb6992f222b1fd08244989d36fabc3c1669afdb25b2a21`, which matches the prompt. synth-04 is `d85b9761…`, 367 lines. `qa/qa-fix-log.md` is `c6c30ccc…`, 344 lines. Both match the "after" hashes in `qa/qa-fix-log-cycle2.md:79-80`.
**Templates read first:** the Standard QA Report Output Format and the content-lens prompts in `/config/.claude/skills/task/SKILL.md:349-506`; the content-lens and domain-lens checklists in `/config/.claude/skills/tech-research/SKILL.md:1088-1139`; the rf-qa-qualitative report-qualitative checklist.

---

## Overall Verdict

Verdict: FAIL

- **G1-G9:** 8 of 9 groups are resolved. G1 is only partly resolved: the Git disclosure gets the step range and the command list wrong, and one of its three locations leaves out the verifier reads.
- **New issue from the corrections:** 1 (N3). The G3 change at :759 now contradicts the unchanged :837.
- **Open issues:** 3, all IMPORTANT. 0 CRITICAL, 0 MINOR.
- **Regressions:** none. Every content and domain criterion that passed at cycle 0 or cycle 1 still passes.
- **Monotonicity:** the merged failure set goes from 9 at cycle 1 to 3 at cycle 2, a strict shrink.
- **Ranking:** intact. The order V1 > V3 > V2 > V5 > V4 is still labelled non-consensus and keeps its tallies. The P6-04 shared-install disclosure is intact, ranks are unchanged, and any debate rerun is left to the user.

## Items Reviewed

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Each of G1-G9 rechecked against the corrected text and its sources | FAIL (G1) | Per-group history below. All 1,310 report lines were read. Each of the 15 cycle-2 "after" strings was found at its target line. |
| 2 | Content and domain criteria that passed before (frozen set) | PASS | All still hold (frozen-criteria history below). None of the 12 changed lines (5, 8, 167, 322, 586, 613, 759, 844, 901, 1235, 1287, 1298) is a rank, tally, control or case line. |
| 3 | Ranking evidence and the P6-04 overlap | PASS | Report:578, :580, :581, :646, :732 disclose the shared 2026-10-22T20:29:54Z install as timing evidence and leave the rerun to the user. Primary checks: installed `qa.md` and `retry.md` mtime is 2026-10-22 20:29:54.0176Z, and `qa.md` hashes to `faff03b7…d2e7d5`. Monitor log record 874 is at 20:34:06.655Z and 884 at 20:34:18.637Z, and they read `refs/ledger.md` and `SKILL.md`. |
| 4 | Displayed order, non-consensus label, tallies, and scores read as document quality | PASS | Report:663, :676-679, :693-707, :1282. V1 is first 5/5. V3 above V2 is 3/5. V4 above V5 is 3/5, and the displayed V5 above V4 sits on the 2-of-5 side. These match `reviews/adversarial/adversarial/debate-transcript.md:477-484` and `merged-root-cause-analysis.md:37-43`. Report:486-494 and :713-716 say writing scores measure document quality, not probability. Every "probabilit" hit (14 lines) is a negation. The order string appears 5 times in the report and 3 times in synth-04, as before. |
| 5 | Original acceptance criteria still valid | PASS | Report:165, :169, :575 are unchanged in substance: the credential chain 1215 → 1230 → nested `:61`, the oracle requirement satisfiable before freeze, and the weak render guard. |
| 6 | All controls kept with their limits | PASS | §2.2 :173-182, §4 :362-367, Opposition rows :522, :549, :576, :603, :627, 7.7 :777-784, step 3.1 :886. |
| 7 | Recommendations stay research-only, and execution needs are labelled as needing approval | PASS | :750, :790, :893-905. Option C now reads "dispatched reviewers working on a disposable copy (separate approval required)" (:586), and Option D reads "needs separately authorized read-only Git object access" (:613). Nothing is presented as already approved. |
| 8 | All real cases and causal classes kept | PASS | Six cases at :162-169. Six-class taxonomy at :309. The 3+1+2 subset at :115-120. |
| 9 | No new claim without a source | FAIL (N1) | The step range "6.4-6.18" and the command list "(`git show`, `git reflog`)" at :8, :322 and :901 are contradicted by the Phase 6 lens reports (see N1). Every other added fact was verified (check 10). |
| 10 | Primary-source recheck of the cycle-2 text | PASS (except N1) | CI log record 1087 (2026-10-23T04:07:09.883Z, user, human origin): "I am running that in another session.  What are the next steps once it completes?" This matches :148 and :167. `qa/qa-fix-verification.md:133` and `qa/qa-fix-verification-qualitative.md:123` are the verifier Git-use lines that :8 cites. Task log entry `[2026-10-24T05:24Z]` (task file :683) is the decision that :8 cites. `wc -l` of the evidence deck gives 900, and its mtime is 2026-10-23 16:51:42Z (G8). The cycle-1 fix-log erratum is present, and the file is 344 lines (333 + 11) (G9). |
| 11 | Internal consistency of the corrected text | FAIL (N2, N3) | :901 against :8 and :322. :837 against :759, :613 and :637. |
| 12 | Report-qualitative items 1-12 | PASS except the issues listed | The recommendation follows the debate tallies. The gaps and the external N/A are honest. There are no scale or probability claims, and the conclusions stay provisional (:663, :706). |
| 13 | G1 disclosure honest, consistent, and not worded as authorized in advance | FAIL (N1, N2) | Wording is correct on authorization: :8 says "not authorized at the time", :322 says "without authorization at the time", :901 says "without user authorization at the time", and acceptance is dated afterwards (2026-10-24). Factual scope is wrong (N1), and the three locations disagree (N2). |
| 14 | Protected artifacts unchanged | PASS | mtimes: cards 2026-10-24 03:48:49Z; debate transcript 2026-10-23 05:32Z; return contract 15:04Z; evidence deck 16:51Z; `research/` latest 2026-10-23 21:50Z. All are before cycle 2. |
| 15 | Regression check, then monotonicity | PASS | No frozen PASS identity now fails. |F| goes from 9 to 3. |

## Summary

- Checks passed: 11 of 15. Checks failed: 4 (checks 1, 9, 11 and 13).
- Critical issues: 0. Important: 3. Minor: 0.
- Issues fixed in place: 0 (fixes not authorized).
- G1-G9: 8 resolved; G1 partly resolved. New issue introduced by the corrections: 1 (N3).
- **Confidence:** Verified 15/15 | Unverifiable 0 | Unchecked 0 | Confidence 100.0%. This measures check coverage, not a PASS.
- **Tool engagement:** Read 15 (plus 1 Read over the size limit, retried in a smaller range) | Grep 0 (grep ran through Bash) | Glob 0 | Bash 9. Three of the Bash calls were bounded read-only batch scripts. Each ended with `BATCH_OK failures=0` and removed its own private directory. Web research: none. Tavily, WebSearch and WebFetch were not used.
- **Git:** no Git command of any kind was run.

## Issues Found

| ID | Severity | Location (path:line) | Issue | Evidence | Required fix |
|---|---|---|---|---|---|
| N1 | IMPORTANT (inaccurate disclosure; G1 not fully resolved) | `RESEARCH-REPORT-review-loops.md:8`, `:322`, `:901` | **The disclosure gets wrong where the unauthorized Git reads happened and which commands they used.** All three lines say the reads were made at "Task Steps 6.4-6.18". :8 calls them "read-only Git object reads (`git show`, `git reflog`)". In fact, the Step 6.3 internal-consistency lens also read Git, and the lenses also ran `git log` and `git diff`, which are not object reads. | `qa/qa-lens-internal-consistency.md:9` ("Task Step 6.3") and `:61` ("Bash: 21 (… git log/diff/reflog)"); `:25` cites `git reflog` for the 03:42:30Z switch. `qa/qa-lens-crossref-chain.md:27` (`git diff`) and `:53` (`git log`), Task Step 6.8. `qa/qa-lens-domain-accuracy.md:55` (`git diff`, `git reflog`, `git show`), Step 6.9. The parent's direction record, task log `[2026-10-24T05:12Z]` (task file :687), names only "Steps 6.4-6.18". So does the recorded decision, `[2026-10-24T05:24Z]` (:683). | At :8, :322 and :901, change "Task Steps 6.4-6.18" to "Task Steps 6.3-6.18". At :8, change "read-only Git object reads (`git show`, `git reflog`)" to "read-only Git reads (`git show`, `git log`, `git diff`, `git reflog`)". Do not say who directed the Step 6.3 reads, because the direction record does not cover Step 6.3. Tell the user that their recorded "Keep, disclosed" decision was based on a 6.4-6.18 description and that Step 6.3 also read Git. Whether the decision covers that is the user's call. |
| N2 | IMPORTANT (contradiction) | `RESEARCH-REPORT-review-loops.md:901` versus `:8`, `:322` | **:901 says no Git access was performed except at Steps 6.4-6.18, but :8 and :322 also disclose the Step 6.19-6.20 verifier reads.** By listing only one exception, :901 implies that no other read-only Git object access occurred, and that is false. | `qa/qa-fix-verification.md:133` (Step 6.19: `git show`, `git log`, `git reflog`, `git rev-parse`, `git merge-base --is-ancestor`, `git status --short`). `qa/qa-fix-verification-qualitative.md:123` (Step 6.20: `git show`, `git diff`, `merge-base`, `rev-parse`). Report:322 includes "(and repeated by the Task Step 6.19-6.20 verifiers)". :901 does not. | Add the same clause to :901: "…made at Task Steps 6.3-6.18 (and repeated by the Task Step 6.19-6.20 verifiers) without user authorization at the time…". This also carries the N1 range. |
| N3 | IMPORTANT (contradiction introduced by C2-G3-2) | `RESEARCH-REPORT-review-loops.md:837` versus `:759`, `:613`, `:637` | **Section 8 still says orders 1-3 are replays that run in a disposable copy, while the corrected :759 says order 3 is read-only analysis.** :837: "Any approved replay (Section 7.6 orders 1-3) would run on these historical artifacts, in a disposable copy." Since cycle 2, :759 says "Step 3 is read-only analysis: Option D needs separately authorized read-only Git object access … and Option E executes nothing", and only steps 1-2 carry execution risk. Before cycle 2, :759 and :837 agreed. Changing :759 alone moved the inconsistency that Q6-02 named to :837. | Report:837 (unchanged since Step 6.18). Report:759 (C2-G3-2). The Option D and Option E Files rows say "Read-only" (:613, :637). The replay table's "Used by" cells list order 3 for the oracle and documentation inputs (:841, :847). | Change :837 to: "Any approved replay or paired adjudication (Section 7.6 orders 1-2) would run on these historical artifacts, in a disposable copy. Order 3 only reads them; Option D also needs separately authorized read-only Git object access. Availability was observed…". Leave :841 "copy it before any run" as it is: it is conditional on an order-1 run. |

### PASS/FAIL set history for G1-G9

Cycle 0 is the Phase 6 consolidation (31 issues). Cycle 1 is the gate merge into G1-G9 (`phase-outputs/plans/report-gate-decision.md:35-45`), all FAIL.

| Group | Cycle 1 | Cycle 2 | Basis |
|---|---|---|---|
| G1 | FAIL | **FAIL** | The disclosure now exists at :8, :322 and :901. It says the reads were unauthorized at the time, that there was no mutation, that the user accepted afterwards on 2026-10-24, and that no Git command is to be run from then on. Remaining problems: N1 (wrong range and command list) and N2 (verifier reads left out at :901). |
| G2 | FAIL | PASS | :5 and :1235 record that the 11 lenses ran (Steps 6.2-6.12; FAIL, 31 issues), the Step 6.18 pass, both verification FAILs, the gate FAIL at cycle 1 of 3, and cycle 2 pending, and that fidelity and anti-omission have not run. This matches task log :685-:691 and gate decision :11, :24-25. :1287 now says "first" and records cycle 2. |
| G3 | FAIL | PASS (but see N3) | :586 now names dispatched reviewers, the disposable copy, the approval requirement, the 45 `subagents/` transcripts and "No production system". :759 now separates steps 1-2 (execution) from step 3 (read-only). The new contradiction with :837 is N3. |
| G4 | FAIL | PASS | :8 names master `2165ae25` (read-only `git show`) and the installed layer read at 2026-10-24T04:36Z, consistent with :188, :199 and :746. |
| G5 | FAIL | PASS | :167 quotes record 1087 exactly and says it "points to work outside this session", matching :148. Verified against the CI log. |
| G6 | FAIL | PASS | :613 reads "(needs separately authorized read-only Git object access)", consistent with :612 and :901. |
| G7 | FAIL | PASS | :844 reads "Orders 1 and 2; steps 2.1, 2.2 and 2.3". |
| G8 | FAIL | PASS | :1298 and synth-04:327 both say "The producer recorded 901 lines; corrected to 900 by `wc -l` at Task Step 6.18". The count is 900 and the deck mtime is 16:51:42Z. |
| G9 | FAIL | PASS | The `## Parent-Cycle-2 Erratum` was appended to `qa/qa-fix-log.md`, with attribution. 161 + 9 + 10 + 1 = 181. The file hash matches the stated "after" value, and the file is 344 lines. |

### Frozen criteria history (cycle 0 PASS, cycle 1 PASS, cycle 2)

- **actionability 6.6-3, 6.6-4, 6.6-5:** PASS → PASS → PASS. There is still no code or remediation tasklist (:661-665, :790-796, :928-932). N1 and N2 are about how honestly the disclosure is scoped, not about remediation work, so they are new issues, not regressions.
- **numbers b, d, S1-S6:** PASS → PASS → PASS. The scale at :651 is unchanged. There is no probability. The unit separation at :124-135 is unchanged.
- **crossref d, g:** PASS → PASS → PASS. The path key at :478 is unchanged.
- **domain b, c, f:** PASS → PASS → PASS. Installed `qa.md:82` and `managed-workspace.md:43` were rechecked.
- **feasibility f, g, h:** PASS → PASS → PASS. Approvals are still covered at :750 and :893-905. N3 is on the approval-label topic, which was FAIL at cycle 1 (Q6-02), so it is not a frozen identity.
- **reproducibility d, S1, S5:** PASS → PASS → PASS. Lines unchanged.
- **Cycle-1 qualitative PASS checks 2, 3, 4, 5, 6, 8, 10, 12, 13, 14:** all PASS at cycle 2 (checks 2-8, 10, 12, 14 and 15 above).

## Actions Taken

None. Report only. No file was written or edited, no agent was spawned, and no test was run.

- **Git:** no Git command of any kind was run.
- **Not read:** the 10.9 MB parent session log. CI record 1087 was read from the separate 4.5 MB CI session log. Monitor records 874 and 884 were read from the monitor session log.

## Recommendations

- Send N1, N2 and N3 to one serialized cycle-2 fixer, which will be cycle 3 of 3. Limit it to `RESEARCH-REPORT-review-loops.md:8`, `:322`, `:837` and `:901`. N1 and N2 share :901, so apply them together.
- Before or with that fix, tell the user in plain words that the Git reads they accepted were described as Steps 6.4-6.18, but the Step 6.3 internal-consistency lens also ran `git log`, `git diff` and `git reflog`. Ask whether "Keep, disclosed" also covers Step 6.3.
- **Out-of-scope observation (not counted; the task file is not a fix target):** task log entry `[2026-10-24T04:12Z]` (task file :691) says "This task … made no Git action", but the lens reports from Steps 6.3, 6.8 and 6.9, completed before that entry, record read-only Git reads. If the parent wants its own log to be accurate, it should append a correction note and not rewrite the entry.
- Afterwards, run a fresh structural verifier and a fresh content verifier, with no Git command, as cycle 3 of 3.

## Self-Audit

**(a) What I relied on without re-checking:**
- The Git-derived citations (the `2165ae25`, `6dc56b1a` and `00448800` hashes and line numbers) on lines cycle 2 did not change. I relied on the cycle-1 verifiers for these because Git is now prohibited. I independently checked the installed-layer side instead: the hash, the mtimes and the cited lines.
- The fixer's list of changed lines. I confirmed every "after" string at its target line, but I did not byte-diff against the pre-cycle-2 file.

**(b) Independent content checks (my own tool work):**
- **G1 scope:** I searched every `qa/qa-lens-*.md` for Git commands and read the step and tool lines. This found the Step 6.3 reads and the `git log` and `git diff` use (N1). I compared all three disclosure locations with each other (N2).
- **G5:** I read CI log record 1087 directly, including its timestamp and the human origin field.
- **P6-04:** monitor records 874 and 884 (timestamps and paths read), plus the installed-file mtimes and hash.
- **Ranking:** debate transcript :476-486 and :241-245, and merged analysis :35-45, against §7.1-7.2 and :1282.
- **Approval labels:** I read every Files row (:532, :559, :586, :613, :637) and :750-759, :837-847 and :893-905 together, which found N3.

## QA Complete

| Status | Result |
|---|---|
| DONE | Rechecked G1-G9 and every frozen criterion against the report and primary sources, without running Git. Verdict FAIL: 8 of 9 groups resolved, 3 IMPORTANT issues open, no regression, |F| from 9 to 3. |
| DONE | Confirmed the ranks, the non-consensus order V1 > V3 > V2 > V5 > V4, its tallies and the P6-04 disclosure are unchanged, and that the rerun is still left to the user. |
| NEXT | One fixer, as cycle 3 of 3, fixes N1-N3 at report :8, :322, :837 and :901. Then two fresh verifiers run. |
| NEXT | The parent tells the user that Step 6.3 also read Git and asks whether "Keep, disclosed" covers it. |