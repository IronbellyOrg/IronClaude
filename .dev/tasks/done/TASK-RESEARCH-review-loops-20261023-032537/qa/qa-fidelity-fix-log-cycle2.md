# QA Report: Phase 6 Source-Fidelity Corrections, Cycle 2

**Topic:** Repeated review failures after fixes in `/sc:workflow` plans and `/sc:implement` tasks (`R/RESEARCH-REPORT-review-loops.md`)
**Date:** 2026-10-24
**Phase:** Phase 6 fidelity gate, Step 6.32
**Fidelity fix cycle:** 2 of 2
**Package root (R):** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/`
**Mode:** `fix_authorization: true`, but the parent applies every write. I edited no package file. I built and checked all patches on private `/tmp` copies (`/tmp/p6c2.*`), replayed them in memory against the live files, and then deleted the workspace. I ran no Git command. I did not open the parent session log `dfade920-…jsonl`. I read the Orca planning log only by line number (records 821, 856, 858).
**Scope:** K1-K6 from `phase-outputs/plans/fidelity-gate-decision.md`, plus its User-Authorized Cycle 2 Record ("Run round 2, keep", task log entry `[2026-10-24T07:09Z]`). J1, the stale status lines at Report:5, :1238 and :1290, was accepted by the user and is not fixed here.
**Input identity:** the report has 1,313 lines and sha256 `a94475caee954ae9942c4b4e8d609e4fc4bfb898fa134026045c78657f18ccf2`. I re-measured it before and after this work, and it is unchanged on disk.

---

## Overall Verdict

Verdict: FAIL

The input set fails because all six open groups, K1-K6, are present in the on-disk files. I prepared a source-backed correction for each of them. The patches are pending parent application, and the Step 6.32 cycle-2 verifiers still have to check them. No correction changes a rank, a ranked cause, the order V1 > V3 > V2 > V5 > V4 or any pair tally.

## Items Reviewed

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Templates and scope read | Done | `fidelity-gate-decision.md` read in full, including K1-K6 and the cycle-2 record. Both cycle-1 verifications and `qa/qa-fidelity-fix-log.md` (all 42 cycle-1 patches) were also read in full. The report was read in full, lines 1-1313, along with case 04 (615 lines) and `gaps-and-questions.md`. |
| 2 | K1: Git object reads in the case and scope files | Defect confirmed | I grepped `research/*.md` (cases 01-06, scope files, evidence deck, research notes, web-01). Only cases 03 and 06 record analyst Git object reads. Case 06 inspected tree `7ac64e6a…` (`06:94`) and tree `d9f262a4…` (`06:283`), and its controls say "Checked historical source through preserved Git objects" and "read-only … Git object inspection" (`06:292-293`). In case 01, 04 and 05, Git appears only as subject matter (for example `05:145` "`git diff --name-only`" inside the historical plan). `evidence-deck.md:257` restates the case-03 trees and records no new read. |
| 3 | K1: wider sweep for Git commands | One unresolved record | I searched for Git subcommand names in `qa/`, `phase-outputs/`, `reviews/` (recursive), `resume-analysis/` and `synthesis/`. Every hit falls in the Step 6.3-6.20 records, or is a citation form or disclosure text, with one exception: `qa/analyst-synthesis-tracing-1.md:134` (Step 5.15) says "`git status` is clean for those paths", while `:158` of the same file says no Git operations were performed. |
| 4 | K2: case-04 line shift | Defect confirmed | Comparing the current case 04 with the cycle-1 C-01/C-02 patch text: the inserted lines are 120-121 and 298-299. Old lines 119-294 map to +3 and old lines 295 onward map to +5. Every re-anchored target line was read (table below). |
| 5 | K2 (structural N-04): gap-register shift | Defect confirmed | The G-01 marker is at current lines 36-37. Removing those two lines gives sha256 `0c4904e5…`, which is the cycle-1 before-hash, so every older citation into the register (report, synth-01/02/03/04/06, web-01) uses the pre-insertion numbering. |
| 6 | K3: 7.7 pointer | Defect confirmed | Report:768 credits Section 4 with the authorization. Report:379 (Section 4, Orca row) says only "narrowed review and unreviewed final amendment". Report:271 (Section 2.6) does carry raw 858, 885 and 889. |
| 7 | K4: the "unrecoverable" partial pair | Defect confirmed | Second-review `adversarial/merged-verdict.yaml:154` (M-06, rename) ends "(the M-05 fix is partial)". That file's own M-05, at `:125-132`, is the Task 5 header check, so the reference is to cycle-0 M-05, which is baseline parsing and partial in case 04 at `:133`. `:240-246` (M-11) calls boundary-guard optional hardening ("M-10 of cycle 0"). |
| 8 | K5: who narrowed the review | Defect confirmed | Orca log `ac2cd1fd…jsonl`. Record 821 (assistant): "re-check only the two high items rather than run a third full review". Record 856: "**Recommended action:** have one fresh reviewer check only N-01 and N-12 against plan v3 … instead of a third full review". Record 858 (user, 15:54:59.545Z): "have one fresh reviewer check only N-01 and N-12 against plan v3". `research/01-session-ac2cd1fd.md:77-78,305` agrees. |
| 9 | K6: where the A-001 rule came from | Defect confirmed | `diff-analysis.md:64` says "Promote A-001: none supplies a common comparison rule". `:69` gives the status "OPEN: each advocate must ACCEPT, REJECT or QUALIFY and give a comparison rule", with the impact note "…is not automatically less likely than broader evidence…". The reach-first rule appears in Round 1 at `debate-transcript.md:47,65,143,182,196` and in Round 2 at `:277,316,356,397,438`. In Round 2, V2 says "not population likelihood", V3 "not measured likelihood", and V4 and V5 "not percentages or population likelihood". |
| 10 | Patch mechanics | PASS | There are 41 patches. Each `before` was asserted to occur exactly once at its turn, in array order. A fresh in-memory replay on the live originals reproduced all five `/tmp` after-hashes. |
| 11 | Mechanical check of every `04-session-43582de1.md:<n>` citation in the patched files | PASS | 21 citation strings across the report (:151, :168, :254, :281, :349, :848, :951), synth-01 (:56, :73, :159, :186), synth-02 (:54) and gaps (:69). Each target line was printed and matched to its claim (Re-anchoring Table). |
| 12 | Gap-register numbering after the move | PASS | Lines 1-63 of the patched `gaps-and-questions.md` hash to `0c4904e5bc83285a7d1502b14b877cea93c2ee59f32b4d964b934fd98c9019ed`, the pre-cycle-1 file. All 31 report and synthesis citations into the register (for example :11, :29-35, :35,59, :53-59, :56, :57-59, :7-63) land on their original rows. :56 is again "Are installed and checkout protocol copies still identical?" and :59 is again "Were the historical Orca source contradictions resolved?". |
| 13 | Contradiction sweep on the patched copies | PASS | Searched for "unrecoverable", "cannot be recovered", "partial pair", "no surviving source", "itemizes", "disclosed sets", "user's instruction", "user-directed", "comparison rule A-001" and "Unresolved Contradictions)". The only remaining hits are the retained `[CONTRADICTION: …]` bracket text, the new ":168 the other cannot be recovered", "three disclosed sets" at :904, and an unrelated "user's instruction had been 'no Git'" at :8. |
| 14 | Table integrity | PASS | The per-line pipe counts of all four patched table files are identical before and after. |

## Summary

- Groups in scope: 6 (K1-K6). Resolved by a prepared patch: 6. Unresolved: 0. (K1 IMPORTANT, K2 IMPORTANT, K3 MINOR, K4 MINOR, K5 MINOR, K6 MINOR; 2 + 4 = 6.)
- Patches: 41 in total. The report has 24, synth-01 has 13, synth-02 has 1, synth-04 has 1 and `gaps-and-questions.md` has 2 (24 + 13 + 1 + 1 + 2 = 41). By group: K1 4, K2 21 (17 case-04 re-anchors plus 2 gap-register moves plus the 2 pointer changes inside those rows, counted with K2), K3 2, K4 6, K5 6, K6 4, identity note 1. Some K2 and K4 changes share a row and are separate patches.
- Case files changed: 0. `research/04-session-43582de1.md` keeps its current bytes (`b89b16d7…`), so its lines do not shift any further.
- Re-anchored case-04 citation tokens: 31 old to new mappings over 12 citation sites (table below).
- Out-of-scope stale case-04 citations, logged and not patched: 2 (`phase-outputs/discovery/fidelity-source-map.md:296` `:377`, now :382; `resume-analysis/B-evidence-digest.md:68` `:263`, a historical recovery note that predates cycle 1). Several QA records also cite old numbers, but they are historical review records.
- Corrections that change a rank: 0.
- **Confidence:** Verified: 14/14 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%. One known limit: the Coder Git objects themselves were not re-read, because Git was not allowed. K1 only discloses that they were read.
- **Tool engagement:** Read: 21 | Grep: 0 (searches ran inside Bash) | Glob: 0 | Bash: 22. The Bash calls were read-only `sed`, `grep`, `jq`, `wc`, `sha256sum` and `od`, `cp` into `/tmp`, two `uv run --no-project python` patch builder and replay scripts that wrote only under `/tmp`, and `rm -rf` of the private `/tmp` workspace. No web research.

## Issues Found

| Group | Old issue | Evidence (path:line) | Resolution | Status | Rank impact |
|---|---|---|---|---|---|
| K1 | Report:8, :324 and :904 disclosed only the IronClaude reads (Steps 6.3-6.20) and the case-03 Coder reads. :904 said "two disclosed sets", which implied a complete list. The case-06 analyst's Phase 2 Coder Git object inspection was undisclosed. | `research/06-session-0690ee9f.md:47-48,92-94,277,283,292-293`; task log entry `[2026-10-24T07:09Z]`; `qa/analyst-synthesis-tracing-1.md:134,158` | Rc2-K1-scope-third-set (:8) adds a third disclosed departure: trees `7ac64e6a…` and `d9f262a4…` and other preserved objects, their purposes, the fact that no tool or repository path is named, no mutation, no authorization on record, where the report relies on them, and the user's keep decision. Rc2-K1-constraints-third-set (:324) and Rc2-K1-separate-auth-count/-third-set (:904) list all three sets the same way. :904 now says "three disclosed sets" and "This list is not certified complete", reports the grep results, and names the unresolved Step 5.15 `git status` record. | RESOLVED (kept and disclosed, per the user) | None |
| K2 | The cycle-1 case-04 insertions (lines 120-121 and 298-299) moved every anchor after old line 118. The cycle-1 F-07 citations used pre-insertion numbers. The gap-register G-01 insertion shifted register lines 36 onward by +2 (structural N-04). Together these caused the P3-C11 regression. | Current case-04 lines in the Re-anchoring Table; `gaps-and-questions.md:36-37` (current) | 17 re-anchors in the report, synth-01 and synth-02, plus the marker in the gap register. The case file is not touched. The G-01 block is moved to a dated, attributed section at the end of `gaps-and-questions.md` (new line 69), so lines 1-63 again match the pre-cycle-1 file (hash proven). The pointers in Report:254 and synth-01:159 now name `gaps-and-questions.md:69`. | RESOLVED | None; P3-C11's links (Report:848 → `:475-476`, Report:951 → `:598`) land on the hashes and the package name again |
| K3 | Report:768 and synth-04:300 said Section 4 holds the authorized narrowing and the unreviewed v4 edit. | Report:379 (no authorization); Report:165, :271 (authorization present) | The pointer now names Section 2.2 and Section 2.6, and states that Section 4 records only the narrowed review and the unreviewed amendment, without their authorization. Raw 856 was added to the record list. | RESOLVED | None |
| K4 | The 2.5 row said "no surviving source itemizes them", and Report:168 and synth-01:73 said the pair "cannot be recovered", but the final merged verdict names one member. | Second review `adversarial/merged-verdict.yaml:125-132,154`; `research/04-session-43582de1.md:133,146` | Report:254, synth-01:159 and the gap marker now state that M-06 records "(the M-05 fix is partial)", that in context this is cycle-0 M-05 (baseline parsing, case 04 `:133`), that the verdict's own M-05 is the header check, that the second partial is not named anywhere, and that M-18 is not shown to be it. Report:168 and synth-01:73 name M-05 and say the other cannot be recovered. The bracketed marker is unchanged on purpose, so that it stays identical to the case-04 erratum copy, which may not be patched. It reads "final partial pair is unrecoverable", which stays true of the pair as a whole. | RESOLVED | None |
| K5 | Report:165, :271 and synth-01:70, :176 said the user directed the two-item review. | Orca records 821, 856, 858; `research/01-session-ac2cd1fd.md:77-78,305` | The text now says the review was narrowed "on the orchestrator's recommendation (raw 821, 856), which the user adopted (raw 858)". The transition list gains "narrowed-review recommendation 856 → user authorization 858". In 2.6 it is "orchestrator-recommended, user-authorized … (raw 821, 856, 858)". | RESOLVED | None |
| K6 | Report:88/:90 and synth-01:14/:16 credited `diff-analysis.md` with the reach-first rule's content. | `diff-analysis.md:64,69`; `debate-transcript.md:47,65,143,182,196,277,316,356,397,438` | The text now says the diff analysis promoted A-001 as an open shared assumption with its "not automatically less likely" caution, that the advocates supplied the reach-first rule in Rounds 1-2, and that V2-V5 said it was not population or measured likelihood. The Evidence line cites the transcript. Report:716 was already accurate and is unchanged. | RESOLVED | None |

## Re-anchoring Table (K2)

Mapping rule, proven from the cycle-1 C-01/C-02 patch text and the current file: old lines ≤118 stay the same, old 119-294 become +3, and old ≥295 become +5.

| Location | Old → new | Target text verified at the new line |
|---|---|---|
| Report:151, synth-01:56 | `275-309` → `278-314` | 278 `<!-- phase3-correction: ci-final-outcome-and-reviewer-dispositions -->` through 314 "The completed review is not ready with partial evidence status…" (supplement cutoff and final outcome) |
| Report:168, synth-01:73 | `120-248` → `123-251` | 123 "## 5. Finding-level disposition of the original 18 concerns" through 251 "The record does **not** establish context exhaustion…" |
| same | `275-309` → `278-314` | as above |
| same | `334-451` → `339-456` | 339 "## 3. Final merged finding inventory" through 456 "These are evidence of defects in proposed remediation instructions…" |
| same | `511-568` → `516-573` | 516 "## Complete eight-entry disposition" through 573 "The reason an earlier reviewer missed any particular valid example remains unknown…" |
| same | `570-610` → `575-615` | 575 "## 12. Summary and recommended action" through 615, the end of the file |
| same (unchanged) | `102-104`, `114-118` | 102 raw 791 premature claim; 104 "810 / 821 … “16 fixed, 2 partial”"; 114-118 key takeaways (before the insertion) |
| Report:254, synth-01:159 (cycle-1 F-07 citation) | `145` → `148` | "…In the second debate, reviewer 1 conceded this and downgraded boundary-file comparison to optional hardening." |
| same (cycle-1 F-07) | `361` → `366` | "The final report repeats “16 original findings fixed, two partly fixed.”…" |
| same (cycle-1 F-07) | `130` → `133` | "Baseline parsing and tooling-output scope behavior are underspecified (M-05) … **Partial:** rename handling remains undefined…" |
| same (cycle-1 F-07) | `143` → `146` | "Dependency lines misstate real dependencies (M-18) … Direct predecessors partly corrected…" |
| same, Evidence column (cycle-1 F-07) | `117-118,130,143,145,294,361` → `117-118,133,146,148,297,366` | 117-118 intermediate-assessment takeaways; 297 "The final report’s verdict and counts are at lines 21-25…"; others as above |
| Report:281, synth-01:186 | `240-244` → `243-247` | 243 "3. **The regeneration was initially declared complete without finding-by-finding verification.**" through 247 "5. **Readiness judgments were inconsistent with findings.** … “ready with notes”…" |
| same | `511-610` → `516-615` | 516 eight-entry disposition through the end of the file |
| Report:349, synth-02:54 | `240` → `243` | premature every-note-applied claim (item 3) |
| same | `244` → `247` | "Reviewer 1 initially returned “ready with notes”… Debate changed that verdict." |
| same (cycle-1 F-07) | `361` → `366` | "The final report repeats “16 original findings fixed, two partly fixed.”" |
| Report:848 (P3-C11) | `470-471` → `475-476` | 475 "Original plan … `dcb320b5…`", 476 "Regenerated plan … `895dcd6b…`" |
| Report:872 | `line 167` → `line 170` | "### 6.2 Pull-request search filters are specified but not verified" |
| Report:872 | `line 405` → `line 410` | "## 5. New probe concern: half-edited advisory header" |
| Report:873 | `line 207` → `line 210` | "## 7. Supported repair-induced structural defect" |
| Report:951 (P3-C11) | `593` → `598` | "**Source frames:** … Regenerated plan means `…/.dev/tasks/done/TASK-WF-specR1-20261023-031725/…`" |
| gaps marker, now line 69 (cycle-1 F-07) | `117-118,145,294,361` → `117-118,133,148,297,366` | as above. `133` is added for the named M-05 partial. |
| Not patched (out of scope) | `fidelity-source-map.md:296` `:377` (now 382, `pull-sync-framework.yml:89-108`); `resume-analysis/B-evidence-digest.md:68` `:263` | Review and recovery records may not be patched here. Logged for follow-up. |

## Actions Taken

- Verified each group against primary sources: Orca records 821, 856 and 858 (read with `jq` by line number), second-review `merged-verdict.yaml:1-30,125-251`, `REPORT.md:15-29`, `round2-v1.md`, `consensus-summary.md`, `diff-analysis.md:60-70`, 11 debate-transcript lines, and case 06 lines 1-130 and 266-325.
- Built 41 patches on `/tmp` copies of five files, asserting at each step that the `before` text occurs once. Replayed the array in memory against the live files and got matching after-hashes. Deleted the `/tmp` workspace.
- Chose to move the gap-register G-01 block instead of re-numbering 31 citations in five files. The move is the only way to fix `research/web-01-gap-applicability.md`, a case-tier file this step may not patch. Lines 1-63 now hash to the pre-cycle-1 identity.
- Left `synth-02:31` and `synth-05:102` unchanged. The first is a prescriptive constraint. The second's "None was performed here" covers only its own list, which does not include Git access. Neither states which Git reads were performed.
- Did not patch case files, cards, `reviews/adversarial/**`, captures, logs, plans, gate decisions, the source map or the task file.

## Exact Patches If Direct Writes Are Prohibited

**(a) File hashes** (paths relative to R). After-hashes are from the `/tmp` copies, reproduced by an in-memory replay on the live files.

| `RESEARCH-REPORT-review-loops.md` | `a94475caee954ae9942c4b4e8d609e4fc4bfb898fa134026045c78657f18ccf2` | `a10cef088fb1be687fc65a72553910a8a522b4ef8eccb8081e4e2e48972469c7` |
| `synthesis/synth-01-problem-current-state.md` | `8d9c4db1a23877c84cc13efbd05bc95503fefd2c206256bbc26e345eb3b0d337` | `c883202055e5b86cc2a9255a4bc49c6b12833d0ef47efc0c4aff3aed60c50ba6` |
| `synthesis/synth-02-target-gaps.md` | `bcc1bdb3d8cedf536eb4eb1ebaaf5619ec6e58a5b2707c5a1db5c49d97775d13` | `f93dd82777caed9603132d1bf08be32fd81aae148609216fbaec60d31bee0ea8` |
| `synthesis/synth-04-options-recommendation.md` | `f0e20bd9362e13ee95ab8c0c0d24fbcc2c3413ab230fcd9810fc4fea606430b0` | `b3ca26784c0b8d5d906bd3450f888b2b8c03c7bd1e2f1d7d5f90318321d04884` |
| `gaps-and-questions.md` | `9a688abf99e2db931a19b2170ad221c44be6d283524018b5b1fc576ecacdb890` | `a1a2da8c8717ee02bb2f6d244822b22edfc046ebbcfc91b6106953a9ea0a3ea2` |

**(b) Patch array.** Apply in array order. Each `before` occurs exactly once at its turn. Files are relative to R.

```json
[
 {
  "id": "Rc2-K6-a001-attribution",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "It therefore promoted rule A-001, under which explanatory reach across contexts counts first and direct evidence for a particular transition counts second (`reviews/adversarial/adversarial/diff-analysis.md:64,69`; Section 6.0).",
  "after": "It therefore promoted A-001 as an open shared assumption: each advocate had to accept, reject or qualify it and give a comparison rule, and its impact note says that strong narrow evidence \"is not automatically less likely than broader evidence\" (`reviews/adversarial/adversarial/diff-analysis.md:64,69`). The rule itself came from the advocates: in Rounds 1 and 2 they ranked explanatory reach across contexts first and direct evidence for a particular transition second, and in Round 2 the V2-V5 advocates said the result was not population or measured likelihood (`reviews/adversarial/adversarial/debate-transcript.md:47,65,143,182,196,277,316,356,397,438`; Section 6.0)."
 },
 {
  "id": "Rc2-K6-a001-evidence",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "/reviews/adversarial/adversarial/diff-analysis.md:64,69` (comparison rule A-001);",
  "after": "/reviews/adversarial/adversarial/diff-analysis.md:64,69` (A-001 promoted as an open point); `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/reviews/adversarial/adversarial/debate-transcript.md:47,65,143,182,196,277,316,356,397,438` (the advocates' comparison rule);"
 },
 {
  "id": "S1c2-K6-a001-attribution",
  "file": "synthesis/synth-01-problem-current-state.md",
  "before": "It therefore promoted rule A-001, under which explanatory reach across contexts counts first and direct evidence for a particular transition counts second (`reviews/adversarial/adversarial/diff-analysis.md:64,69`; Section 6.0).",
  "after": "It therefore promoted A-001 as an open shared assumption: each advocate had to accept, reject or qualify it and give a comparison rule, and its impact note says that strong narrow evidence \"is not automatically less likely than broader evidence\" (`reviews/adversarial/adversarial/diff-analysis.md:64,69`). The rule itself came from the advocates: in Rounds 1 and 2 they ranked explanatory reach across contexts first and direct evidence for a particular transition second, and in Round 2 the V2-V5 advocates said the result was not population or measured likelihood (`reviews/adversarial/adversarial/debate-transcript.md:47,65,143,182,196,277,316,356,397,438`; Section 6.0)."
 },
 {
  "id": "S1c2-K6-a001-evidence",
  "file": "synthesis/synth-01-problem-current-state.md",
  "before": "/reviews/adversarial/adversarial/diff-analysis.md:64,69` (comparison rule A-001);",
  "after": "/reviews/adversarial/adversarial/diff-analysis.md:64,69` (A-001 promoted as an open point); `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/reviews/adversarial/adversarial/debate-transcript.md:47,65,143,182,196,277,316,356,397,438` (the advocates' comparison rule);"
 },
 {
  "id": "Rc2-K2-boundary-range",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "04-session-43582de1.md:66-87,275-309`.",
  "after": "04-session-43582de1.md:66-87,278-314`."
 },
 {
  "id": "S1c2-K2-boundary-range",
  "file": "synthesis/synth-01-problem-current-state.md",
  "before": "04-session-43582de1.md:66-87,275-309`.",
  "after": "04-session-43582de1.md:66-87,278-314`."
 },
 {
  "id": "Rc2-K5-orca-narrowing",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "Authorized v3 receives a targeted review, narrowed at the user's instruction to two items (raw 858), that remains partial.",
  "after": "Authorized v3 receives a targeted review, narrowed to two items on the orchestrator's recommendation (raw 821, 856), which the user adopted (raw 858); it remains partial."
 },
 {
  "id": "Rc2-K5-orca-transitions",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "→ Write 841 → targeted result 874 → no-review recommendation 885",
  "after": "→ Write 841 → narrowed-review recommendation 856 → user authorization 858 → targeted result 874 → no-review recommendation 885"
 },
 {
  "id": "S1c2-K5-orca-narrowing",
  "file": "synthesis/synth-01-problem-current-state.md",
  "before": "Authorized v3 receives a targeted review, narrowed at the user's instruction to two items (raw 858), that remains partial.",
  "after": "Authorized v3 receives a targeted review, narrowed to two items on the orchestrator's recommendation (raw 821, 856), which the user adopted (raw 858); it remains partial."
 },
 {
  "id": "S1c2-K5-orca-transitions",
  "file": "synthesis/synth-01-problem-current-state.md",
  "before": "→ Write 841 → targeted result 874 → no-review recommendation 885",
  "after": "→ Write 841 → narrowed-review recommendation 856 → user authorization 858 → targeted result 874 → no-review recommendation 885"
 },
 {
  "id": "Rc2-K4-ci-row-partial-pair",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "Which two findings that final count treats as partial cannot be recovered (Section 2.5 contradiction marker).",
  "after": "The final merged verdict names one of the two partials, cycle-0 M-05, baseline parsing (second review `adversarial/merged-verdict.yaml:154`); the other cannot be recovered (Section 2.5 contradiction marker)."
 },
 {
  "id": "Rc2-K2-ci-row-range",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "04-session-43582de1.md:102-104,114-118,120-248,275-309,334-451,511-568,570-610`",
  "after": "04-session-43582de1.md:102-104,114-118,123-251,278-314,339-456,516-573,575-615`"
 },
 {
  "id": "S1c2-K4-ci-row-partial-pair",
  "file": "synthesis/synth-01-problem-current-state.md",
  "before": "Which two findings that final count treats as partial cannot be recovered (Section 2.5 contradiction marker).",
  "after": "The final merged verdict names one of the two partials, cycle-0 M-05, baseline parsing (second review `adversarial/merged-verdict.yaml:154`); the other cannot be recovered (Section 2.5 contradiction marker)."
 },
 {
  "id": "S1c2-K2-ci-row-range",
  "file": "synthesis/synth-01-problem-current-state.md",
  "before": "04-session-43582de1.md:102-104,114-118,120-248,275-309,334-451,511-568,570-610`",
  "after": "04-session-43582de1.md:102-104,114-118,123-251,278-314,339-456,516-573,575-615`"
 },
 {
  "id": "Rc2-K2-2.5-concession-anchors",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "(`round2-v1.md:5`; `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/04-session-43582de1.md:145,361`).",
  "after": "(`round2-v1.md:5`; `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/04-session-43582de1.md:148,366`)."
 },
 {
  "id": "Rc2-K4-2.5-named-partial",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "Do not choose which two findings the final count treats as partial: no surviving source itemizes them. Case 04's table (M-05 partial at `:130`, M-18 partly corrected at `:143`) fits a 16/2 count but does not prove it is the same pair.",
  "after": "The final debate-merged verdict names one of the two partials: its M-06 (rename handling) ends \"(the M-05 fix is partial)\" (`adversarial/merged-verdict.yaml:154`). In context this is cycle-0 M-05, baseline parsing, which case 04's table marks partial (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/04-session-43582de1.md:133`); that verdict's own M-05 (`adversarial/merged-verdict.yaml:125-132`) is the Task 5 header check, not a fix. No surviving source names the second partial, so the pair cannot be completed; do not choose it. Case 04's M-18, partly corrected (`:146`), fits a 16/2 count but is not shown to be that second partial."
 },
 {
  "id": "Rc2-K4-2.5-evidence-verdict-lines",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "`REPORT.md:21`, `adversarial/merged-verdict.yaml:8`, `adversarial/consensus-summary.md:3`, `adversarial/round2-v1.md:5,16,33`; CI log",
  "after": "`REPORT.md:21`, `adversarial/merged-verdict.yaml:8,125-132,154`, `adversarial/consensus-summary.md:3`, `adversarial/round2-v1.md:5,16,33`; CI log"
 },
 {
  "id": "Rc2-K2-2.5-evidence-anchors",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/04-session-43582de1.md:117-118,130,143,145,294,361`; `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/gaps-and-questions.md` (Unresolved Contradictions). |",
  "after": "`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/04-session-43582de1.md:117-118,133,146,148,297,366`; `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/gaps-and-questions.md:69` (Unresolved Contradictions, fidelity addition at the end of the file). |"
 },
 {
  "id": "S1c2-K2-2.5-concession-anchors",
  "file": "synthesis/synth-01-problem-current-state.md",
  "before": "(`round2-v1.md:5`; `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/04-session-43582de1.md:145,361`).",
  "after": "(`round2-v1.md:5`; `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/04-session-43582de1.md:148,366`)."
 },
 {
  "id": "S1c2-K4-2.5-named-partial",
  "file": "synthesis/synth-01-problem-current-state.md",
  "before": "Do not choose which two findings the final count treats as partial: no surviving source itemizes them. Case 04's table (M-05 partial at `:130`, M-18 partly corrected at `:143`) fits a 16/2 count but does not prove it is the same pair.",
  "after": "The final debate-merged verdict names one of the two partials: its M-06 (rename handling) ends \"(the M-05 fix is partial)\" (`adversarial/merged-verdict.yaml:154`). In context this is cycle-0 M-05, baseline parsing, which case 04's table marks partial (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/04-session-43582de1.md:133`); that verdict's own M-05 (`adversarial/merged-verdict.yaml:125-132`) is the Task 5 header check, not a fix. No surviving source names the second partial, so the pair cannot be completed; do not choose it. Case 04's M-18, partly corrected (`:146`), fits a 16/2 count but is not shown to be that second partial."
 },
 {
  "id": "S1c2-K4-2.5-evidence-verdict-lines",
  "file": "synthesis/synth-01-problem-current-state.md",
  "before": "`REPORT.md:21`, `adversarial/merged-verdict.yaml:8`, `adversarial/consensus-summary.md:3`, `adversarial/round2-v1.md:5,16,33`; CI log",
  "after": "`REPORT.md:21`, `adversarial/merged-verdict.yaml:8,125-132,154`, `adversarial/consensus-summary.md:3`, `adversarial/round2-v1.md:5,16,33`; CI log"
 },
 {
  "id": "S1c2-K2-2.5-evidence-anchors",
  "file": "synthesis/synth-01-problem-current-state.md",
  "before": "`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/04-session-43582de1.md:117-118,130,143,145,294,361`; `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/gaps-and-questions.md` (Unresolved Contradictions). |",
  "after": "`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/04-session-43582de1.md:117-118,133,146,148,297,366`; `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/gaps-and-questions.md:69` (Unresolved Contradictions, fidelity addition at the end of the file). |"
 },
 {
  "id": "Rc2-K5-2.6-narrowing",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "the user-directed two-item targeted review (raw 858)",
  "after": "the orchestrator-recommended, user-authorized two-item targeted review (raw 821, 856, 858)"
 },
 {
  "id": "S1c2-K5-2.6-narrowing",
  "file": "synthesis/synth-01-problem-current-state.md",
  "before": "the user-directed two-item targeted review (raw 858)",
  "after": "the orchestrator-recommended, user-authorized two-item targeted review (raw 821, 856, 858)"
 },
 {
  "id": "Rc2-K2-2.6-anchors",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "04-session-43582de1.md:102-104,114-118,240-244,511-610`",
  "after": "04-session-43582de1.md:102-104,114-118,243-247,516-615`"
 },
 {
  "id": "S1c2-K2-2.6-anchors",
  "file": "synthesis/synth-01-problem-current-state.md",
  "before": "04-session-43582de1.md:102-104,114-118,240-244,511-610`",
  "after": "04-session-43582de1.md:102-104,114-118,243-247,516-615`"
 },
 {
  "id": "Rc2-K2-gap-row-anchors",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "04-session-43582de1.md:102-104,114-118,240,244,361`",
  "after": "04-session-43582de1.md:102-104,114-118,243,247,366`"
 },
 {
  "id": "S2c2-K2-gap-row-anchors",
  "file": "synthesis/synth-02-target-gaps.md",
  "before": "04-session-43582de1.md:102-104,114-118,240,244,361`",
  "after": "04-session-43582de1.md:102-104,114-118,243,247,366`"
 },
 {
  "id": "Rc2-K3-7.7-pointer",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "(raw 858, 885, 889) are in Section 2.2 (Orca row) and Section 4 (Key Takeaway Coverage, Orca planning row), not in Sections 6-7 |",
  "after": "(raw 856, 858, 885, 889) are in Section 2.2 (Orca row) and Section 2.6 (Orca planning row). Section 4 (Key Takeaway Coverage, Orca planning row) records only the narrowed review and the unreviewed final amendment, without their authorization. Neither is in Sections 6-7 |"
 },
 {
  "id": "S4c2-K3-7.7-pointer",
  "file": "synthesis/synth-04-options-recommendation.md",
  "before": "(raw 858, 885, 889) are in Section 2.2 (Orca row) and Section 4 (Key Takeaway Coverage, Orca planning row), not in Sections 6-7 |",
  "after": "(raw 856, 858, 885, 889) are in Section 2.2 (Orca row) and Section 2.6 (Orca planning row). Section 4 (Key Takeaway Coverage, Orca planning row) records only the narrowed review and the unreviewed final amendment, without their authorization. Neither is in Sections 6-7 |"
 },
 {
  "id": "Rc2-K1-scope-third-set",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "On 2026-10-24 the user accepted keeping it, disclosed (\"Keep, disclosed\"; task log entry `[2026-10-24T06:32Z]`).\n**Package inventory at assembly:**",
  "after": "On 2026-10-24 the user accepted keeping it, disclosed (\"Keep, disclosed\"; task log entry `[2026-10-24T06:32Z]`). **Third disclosed departure (Coder Git objects, Phase 2):** during the Phase 2 credential case analysis, the case-06 analyst also inspected preserved Git objects for the credential work in the Coder worktree (`research/06-session-0690ee9f.md:47-48`): tree `7ac64e6a91f624362b19daf46ea9544ad8a4edcd`, to confirm that historical README line 161 was a table separator and not lint evidence (`research/06-session-0690ee9f.md:92-94`), and tree `d9f262a48f82c55b18f883826428f2fd8d2d7be5`, for the historical manual-page load-order content behind the narrow task-body omission (`:277,283`). Its controls record \"Checked historical source through preserved Git objects where present-day content had changed\" and \"read-only ... Git object inspection\" (`:292-293`). The source names neither the tool nor the repository path, and no Git mutation is recorded. No authorization for these reads is on record, and neither acceptance above covers them. The report relies on this evidence for the README separator (Section 4, proof-and-provenance gap row; Option D Support) and for the narrow task-body omission that qualifies the credential pass (Section 2.2 credential row; Section 2.6 credential row). On 2026-10-24 the user accepted keeping it, disclosed (\"Run round 2, keep\"; task log entry `[2026-10-24T07:09Z]`).\n**Package inventory at assembly:**"
 },
 {
  "id": "Rc2-K1-constraints-third-set",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "on 2026-10-24 the user accepted keeping that evidence, disclosed (header Scope line). Proposed investigations remain",
  "after": "on 2026-10-24 the user accepted keeping that evidence, disclosed (header Scope line). Third disclosed departure: during the Phase 2 credential case analysis, the case-06 analyst inspected preserved Coder Git trees `7ac64e6a91f624362b19daf46ea9544ad8a4edcd` and `d9f262a48f82c55b18f883826428f2fd8d2d7be5` and other preserved Git objects (read-only object inspection, no Git mutation recorded), with no authorization on record (`research/06-session-0690ee9f.md:94,283,292-293`); on 2026-10-24 the user accepted keeping that evidence, disclosed (header Scope line). Proposed investigations remain"
 },
 {
  "id": "Rc2-K1-separate-auth-count",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "None was performed here, except two disclosed sets of read-only Git reads (header Scope line). First,",
  "after": "None was performed here, except three disclosed sets of read-only Git reads (header Scope line). First,"
 },
 {
  "id": "Rc2-K1-separate-auth-third-set",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "on 2026-10-24 the user accepted keeping that evidence, disclosed (task log entry `[2026-10-24T06:32Z]`). |",
  "after": "on 2026-10-24 the user accepted keeping that evidence, disclosed (task log entry `[2026-10-24T06:32Z]`). Third, during the Phase 2 credential case analysis, the case-06 analyst inspected the preserved Coder Git trees `7ac64e6a91f624362b19daf46ea9544ad8a4edcd` and `d9f262a48f82c55b18f883826428f2fd8d2d7be5` and other preserved Git objects (`research/06-session-0690ee9f.md:94,283,292-293`), with no authorization on record and no recorded Git mutation; on 2026-10-24 the user accepted keeping that evidence, disclosed (task log entry `[2026-10-24T07:09Z]`). This list is not certified complete. At Task Step 6.32 a search of every case and scope file in `research/` found no other Git object reads by a research agent, and a search for Git subcommand names in the `qa/`, `phase-outputs/`, `reviews/`, `resume-analysis/` and `synthesis/` records found no Git command recorded as run outside Task Steps 6.3-6.20 except one unresolved record: the Task Step 5.15 synthesis source-tracing analyst reports that \"`git status` is clean\" for the six protocol source paths (`qa/analyst-synthesis-tracing-1.md:134`) but also states that no Git operations were performed (`:158`). |"
 },
 {
  "id": "Rc2-K2-replay-hashes",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "still match `research/04-session-43582de1.md:470-471`",
  "after": "still match `research/04-session-43582de1.md:475-476`"
 },
 {
  "id": "Rc2-K2-step2.1-lines",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "CI planning case, section 6.2 (line 167) and supplement section 5, \"New probe concern: half-edited advisory header\" (line 405)",
  "after": "CI planning case, section 6.2 (line 170) and supplement section 5, \"New probe concern: half-edited advisory header\" (line 410)"
 },
 {
  "id": "Rc2-K2-step2.2-line",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "\"Supported repair-induced structural defect\" (line 207)",
  "after": "\"Supported repair-induced structural defect\" (line 210)"
 },
 {
  "id": "Rc2-K2-q7-package",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "(`research/04-session-43582de1.md:593`)",
  "after": "(`research/04-session-43582de1.md:598`)"
 },
 {
  "id": "Rc2-identity-note",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "and the Task Step 6.29 source-fidelity corrections later changed synth-01, synth-02 and synth-04 (`qa/qa-fidelity-fix-log.md`); the hashes above",
  "after": "and the Task Step 6.29 source-fidelity corrections and the Task Step 6.32 fidelity cycle-2 corrections later changed synth-01, synth-02 and synth-04 (`qa/qa-fidelity-fix-log.md`, `qa/qa-fidelity-fix-log-cycle2.md`); the hashes above"
 },
 {
  "id": "Gc2-K2-remove-g01-at-36",
  "file": "gaps-and-questions.md",
  "before": "[CONTRADICTION: Orca source.md decision script consumes pre-fetched files, while its repository-self-check rule says before any upstream call.] This remains unresolved in final planning v4 according to historical reconstruction; implementation outcome is a separate incident. These are verified specification contradictions, not claims current runtime is definitely broken.\n\n[CONTRADICTION: reviewer 1's \"16 fixed, 2 partial\" (CI log 821) vs the completed second review's own closure \"fixes 16 of the 18 cycle-0 findings in full and the other 2 in part\" (REPORT.md:21; CI log 1052, 1084); the merged verdict (:8) and consensus summary (:3) carry no itemized cycle-0 checklist, so the final partial pair is unrecoverable] Added 2026-10-24 by the Task Step 6.29 source-fidelity fixer (finding F-07 in `qa/qa-fidelity-consolidated-findings.md`). Both statements are kept: `research/04-session-43582de1.md:117-118` calls the count one reviewer's intermediate assessment that later debate corrected, while the completed second review keeps the same count. Debate changed the readiness verdict and narrowed one partial's boundary-file reading to optional hardening; no surviving source names the final partial pair. Sources: `research/04-session-43582de1.md:117-118,145,294,361`; second CI review `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/reflect/pre-TASK-WF-specR1-20261023-031725-20261023032025/REPORT.md:21`, `adversarial/merged-verdict.yaml:8`, `adversarial/consensus-summary.md:3`, `adversarial/round2-v1.md:5,16,33`; CI log `/config/.claude/projects/-config-workspace-IronClaude/43582de1-c41b-4b6a-806c-f19f1488095c.jsonl` records 821, 1052 and 1084.\n",
  "after": "[CONTRADICTION: Orca source.md decision script consumes pre-fetched files, while its repository-self-check rule says before any upstream call.] This remains unresolved in final planning v4 according to historical reconstruction; implementation outcome is a separate incident. These are verified specification contradictions, not claims current runtime is definitely broken.\n"
 },
 {
  "id": "Gc2-K2-append-g01-at-end",
  "file": "gaps-and-questions.md",
  "before": "Gap compilation is updated through the named research-gate correction verification, whose two independent reports verify both current report defects resolved without new or regressed research findings. Historical contradictions, unavailable or unobserved facts, and clustered modification-time selection remain disclosed limits rather than reasons to invent stronger conclusions. The separate full Task Phase 3 review, synthesis/ranking and final-report gates remain pending. Deliverables stay local Markdown; no production work, Git action, investigated-plan execution or external publication is authorized.\n",
  "after": "Gap compilation is updated through the named research-gate correction verification, whose two independent reports verify both current report defects resolved without new or regressed research findings. Historical contradictions, unavailable or unobserved facts, and clustered modification-time selection remain disclosed limits rather than reasons to invent stronger conclusions. The separate full Task Phase 3 review, synthesis/ranking and final-report gates remain pending. Deliverables stay local Markdown; no production work, Git action, investigated-plan execution or external publication is authorized.\n\n## Unresolved Contradictions: Fidelity Addition (2026-10-24)\n\nMoved here at Task Step 6.32 (fidelity cycle 2) from its Task Step 6.29 position after line 35, so that existing line citations into this file keep their original numbers. It continues the Unresolved Contradictions section above.\n\n[CONTRADICTION: reviewer 1's \"16 fixed, 2 partial\" (CI log 821) vs the completed second review's own closure \"fixes 16 of the 18 cycle-0 findings in full and the other 2 in part\" (REPORT.md:21; CI log 1052, 1084); the merged verdict (:8) and consensus summary (:3) carry no itemized cycle-0 checklist, so the final partial pair is unrecoverable] Added 2026-10-24 by the Task Step 6.29 source-fidelity fixer (finding F-07 in `qa/qa-fidelity-consolidated-findings.md`); corrected at Task Step 6.32 (`qa/qa-fidelity-fix-log-cycle2.md`). Both statements are kept: `research/04-session-43582de1.md:117-118` calls the count one reviewer's intermediate assessment that later debate corrected, while the completed second review keeps the same count. Debate changed the readiness verdict and narrowed one partial's boundary-file reading to optional hardening. The final merged verdict names one of the two partials: its M-06 ends \"(the M-05 fix is partial)\", which in context is cycle-0 M-05, baseline parsing (`research/04-session-43582de1.md:133`). No surviving source names the second partial, so the pair cannot be completed. Sources: `research/04-session-43582de1.md:117-118,133,148,297,366`; second CI review `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/reflect/pre-TASK-WF-specR1-20261023-031725-20261023032025/REPORT.md:21`, `adversarial/merged-verdict.yaml:8,125-132,154`, `adversarial/consensus-summary.md:3`, `adversarial/round2-v1.md:5,16,33`; CI log `/config/.claude/projects/-config-workspace-IronClaude/43582de1-c41b-4b6a-806c-f19f1488095c.jsonl` records 821, 1052 and 1084.\n"
 }
]
```

## Preservation Checks

| Check | Result | Evidence |
|---|---|---|
| Ranks, displayed order and tallies unchanged | PASS | Report: "V1 > V3 > V2 > V5 > V4" 5→5, "3 of 5" 6→6, "2 of 5" 5→5, "5 of 5" 4→4. synth-04: 3→3, 4→4, 4→4, 3→3. Report lines 673-709 (7.1-7.2) are byte-identical. |
| J1 untouched | PASS | Report:5, :1238 and :1290 are byte-identical before and after. |
| Report line numbers unchanged | PASS | The report stays at 1,313 lines. Every report patch is in-line, so no report citation shifts. |
| Case 04 not patched again | PASS | No patch targets `research/`. Case 04 keeps `b89b16d7…` (615 lines). |
| Gap-register numbering restored | PASS | Patched lines 1-63 equal the pre-cycle-1 file (`0c4904e5…`). The marker sits at line 69, under a dated heading that says it was moved. |
| Synthesis mirrors | PASS | Every report change that carries synth text is mirrored in synth-01, synth-02 or synth-04 (13 + 1 + 1 patches). No synthesis file other than those three changed. |
| No invented evidence or false certainty | PASS | Every new fact traces to a line or record I read. The second CI partial stays unnamed. The Step 5.15 `git status` record is reported as unresolved, not as a confirmed read. The Coder object contents were not re-read. |
| Placeholders | PASS | Grep for `TODO`, `TBD`, `FIXME`, `{{` and `RF_PLACEHOLDER` in all five patched copies: 0 hits. |
| No Git, no parent-log read, no package writes | PASS | All work was read-only or confined to `/tmp`. The workspace was removed, and the live report hash is still `a94475ca…` afterward. |
| Monotonicity input for Step 6.32 | Recorded | Open groups at cycle 1: 6 (K1-K6). Expected at cycle 2 if verified: 0. P3-C11's links are restored (Report:848 → `:475-476`, Report:951 → `:598`), and P3-C11 should be re-checked explicitly. |

## QA Complete

**Verdict: FAIL** for the input set: K1-K6 are open in the on-disk files. All six are RESOLVED by prepared patches pending parent application. No correction changes a rank or a ranked cause.

| Status | Result |
|---|---|
| DONE | Verified K1-K6 against primary sources: Orca records 821/856/858, the second review's `merged-verdict.yaml:125-154`, `diff-analysis.md:64,69`, the A-001 lines of the debate transcript, and case 06:92-94,277-293. |
| DONE | Re-anchored every case-04 citation after old line 118, including the cycle-1 F-07 citations, without touching the case file. Each target line was checked mechanically. Moved the gap-register marker to the end of its file, which restores the pre-cycle-1 numbering exactly. |
| DONE | Disclosed the case-06 Coder Git reads consistently at Report:8, :324 and :904, and stopped calling the list complete. The research sweep found no other Git object reads. The wider sweep found one unresolved Step 5.15 `git status` record. |
| NEXT | Parent: confirm the five before-hashes, apply the JSON array in order, confirm the five after-hashes, and persist this text to `R/qa/qa-fidelity-fix-log-cycle2.md`. |
| NEXT | Cycle-2 verifiers: re-check K1-K6 and P3-C11, and decide whether the Step 5.15 `git status` record needs a user ruling. |
## Parent Application Record (2026-10-24)

| Item | Record |
|---|---|
| Persistence | The parent copied this report verbatim from the restricted fixer's final transcript text (record 233 of `subagents/agent-ap6-fid-fixer-c2-*.jsonl`) into the prepared stub. The parent did not edit the fixer text above this section. |
| Application | `/tmp/apply_p6.py qa/qa-fidelity-fix-log-cycle2.md` applied all 41 JSON patches in array order; each `before` occurred exactly once; all five start and end hashes matched before any write. |
| Files written | `RESEARCH-REPORT-review-loops.md` (1,313 lines, sha256 a10cef08...), `synthesis/synth-01`, `synth-02`, `synth-04`, `gaps-and-questions.md`. |
| Not written | Case files (case 04 unchanged at b89b16d7...), cards, `reviews/adversarial/**`, raw captures, logs, plans, gate decisions, the task file. J1 not fixed, by user decision. |
| Git | None run. |
| Verification | Pending: `qa/qa-fidelity-verification-structural-cycle2.md` and `qa/qa-fidelity-verification-content-cycle2.md`. |

## Column Note (Phase 6 /task gate, 2026-10-24, finding G6-48)

**Attribution:** appended by the Phase 6 /task phase-gate fixer, applied by the parent. The fixer text above is unchanged.

The hash table under "(a) File hashes" has no header or separator row, so it does not render as a Markdown table. Its three columns are: file (path relative to the package root), SHA-256 before, SHA-256 after.
