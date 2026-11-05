# Actionability QA Report

**Report reviewed:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/RESEARCH-REPORT-review-loops.md` (full file, 1,263 lines, read lines 1-1263)
**Lens:** Actionability (QA phase `report-lens-actionability`, Task Step 6.6)
**Date:** 2026-10-24
**Reviewer:** rf-qa-qualitative, report-only (`fix_authorization: false`). No file was edited.
**Intended output path:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/qa/qa-lens-actionability.md`. My harness instructions forbid writing report files, so this complete text is returned for the parent to save at that path.
**Governing template:** `/config/.claude/skills/tech-research/SKILL.md:1042-1149` (Lens-Specific QA Agent Prompt Template, Actionability Checklist a-d at `:1090-1094`, output format at `:1134-1149`)
**Step contract:** Task file Step 6.6 (`TASK-RESEARCH-review-loops-20261023-032537.md:397-399`)
**Inherited Structural Verdict:** None was supplied in the spawn prompt, so this review checks everything on its own.

---

## Overall Verdict: FAIL

Six real issues: 3 IMPORTANT and 3 MINOR. Research-only scope holds throughout, and every file cited as a next-check target exists. The failures are about whether another investigator could carry out and judge the recommended checks without making their own decisions:

- The first recommended step is described with two incompatible procedures.
- No rule says how check results would change the ranking.
- One recommended step quietly depends on Git access and a repository location that the report never names.

---

## Findings

| # | Severity | Section | Finding | Proposed Fix |
|---|----------|---------|---------|-------------|
| 1 | IMPORTANT | Section 7 header (line 635), 7.6 order 1 (line 724), 7.6 trade-offs (line 729), Section 6 Option A Falsification (line 495), Section 8 Phase 2 row 1 (line 846) | **The first recommended step has two incompatible procedures.** Option A, which 7.6 order 1 points to, says "build a minimal counterexample for each later finding" on "the preserved version that first passed", and asks whether "the check actually used accepts wrong behavior". Its source card spells it out: "Run the described check against the counterexample" (`synthesis/hypothesis-01.md:141-142`). For the oracle, "the check actually used" is the 67 default and 78 acceptance tests (line 491), so this means running tests. Section 8's matching row instead says "Compare the recorded acceptance predicate with a wrong-behavior example **already established by review**", which is a read-only comparison of existing records. Line 729 then says steps 1-3 "stay read-only", while Section 8's own constraints (lines 878-879) class any "replay" or "test" as separately authorized execution in a disposable copy. "First-passing version" is also never pinned down for the two planning contexts: neither Orca nor CI planning ever passed a semantic review, and Option A's reuse row lists Orca v1-v4 and "CI original and regenerated plans" without saying which one is meant. An investigator cannot tell whether the approval being requested covers building and executing counterexamples, or only comparing records. | Choose one procedure for 7.6 order 1 and use it in Option A, 7.6 and Section 8. If counterexamples are built and checks are run, remove "stay read-only" at line 729 and name the execution and isolation approval as a prerequisite. If only recorded predicates are compared, rewrite Option A's falsification to match. For each of the four contexts, name the exact artifact version (for example, Orca v1 rebuilt from Write 544/545; the CI original plan path from case 04 §2). |
| 2 | IMPORTANT | 7.6 "What would change the ranking" column (lines 724-726), Section 7 rationale (line 639), Section 8 Phase 2 rows 1-5 (lines 846-850) | **No pass/fail decision rule connects check results to the ranking.** Section 8 gives only per-transition "strengthens/weakens" directions. Order 1 says "If the checks actually used already rejected the counterexamples, V1 loses its lead" but sets no denominator or threshold. The per-context "later finding" sets differ widely and include items that are not defects: Orca's 20 numbered items include a duplicate and a non-defect note (line 145), CI has 18 original concerns versus 16 merged items (lines 148, 350), and the monitor has seven verdicts (line 149). Nothing says whether V1 loses its lead when all, most or any transitions weaken. Order 2 states that its result "Neither replaces the reach-weighting judgment", and line 639 says replays of the six incidents "cannot by themselves settle" the disputed placements. So the column headed "What would change the ranking" names no result that would change the displayed middle placement. Option C's paired adjudication also depends on reviewers (line 558), but no repeat count or agreement rule is given for judging that a verdict change is "contract-only". | For each of orders 1-3, state: (a) the exact finding set, after the Phase 3 "Adjudicate the finding before explaining it" filter; (b) the result that counts as weakening for that check; and (c) how that result changes the rank under rule A-001. For example: "V1 loses first place if fewer than N of the M adjudicated old-defect transitions show the used check accepting the counterexample." Alternatively, state plainly that steps 1-3 cannot change any placement, and drop the "What would change the ranking" claims for order 2. For Option C, state how many independent adjudications are run per finding and what agreement counts as a contract-only change. |
| 3 | IMPORTANT | Section 6 Option D Reuse and Effort (lines 580, 582), 7.6 order 3 (line 726), Section 8 Phase 2 row 4 (line 849), Section 8 Constraints "Separate authorization" (line 878) | **A Git prerequisite is assumed without being stated.** Option D's falsification ("Reconstruct the true pre-task state") relies on "Preserved trees `f60d2c3…`, `3c5fdfa…` and `00d8f4a…`". Its Effort is rated "S" because the trees are "already identified". Problems: (a) Sections 6-8 give only shortened IDs and never name the repository. The case report gives the full IDs (`research/03-session-6f744b87.md:216,229,237`), but the only root it names is the historical worktree `/config/workspace/Coder/.claude/worktrees/issue-358-litellm-key-env` (case 03 line 20), and that path no longer exists (verified: "No such file or directory"). (b) Reading those trees is a Git operation. The report's scope says "no ... Git action" (header line 8), and the gap register says "no new Git operation ... is authorized" (`gaps-and-questions.md:12`). Yet Section 8's list of activities needing separate authorization (replay, adjudication, test, renderer, model run, workflow run, code or protocol change) does not mention Git reads. Unlike the `t10-markdownlint.log` note at line 582, the report never says tree availability must be confirmed first. | Name the repository that holds the three objects (most likely the parent Coder repository), give the full object IDs in Option D's reuse row, and add "confirm object availability before any approved replay". Add "read-only Git object access" to the Section 8 separate-authorization list and to 7.6 order 3's prerequisites. Change Option D's Effort rationale so it does not assume availability. |
| 4 | MINOR | 7.6 order 4 (line 727), Section 8 Phase 2 last row (line 851), Open Question 1 (line 920) | **The broader-sample step has no selection rule and no decision criterion.** It applies the C-001 labels (verified at `reviews/adversarial/adversarial/debate-transcript.md:270`) to "additional, independently selected sessions" and says "A broader count ... could settle the middle and bottom pairs; no outcome is predicted". No selection rule, minimum sample, or count pattern is given that would settle either pair. Without those, the user cannot judge whether the scope decision is worth approving, and a second investigator could not judge the result. | Add the minimum design needed for the scope decision: how sessions are selected (for example, matching `/sc:implement`/`/sc:workflow` invocations outside the four clustered work families), a minimum count, and the comparison that would decide each pair (for example, "V3 above V2 holds if contract or re-entry transitions occur in more independent contexts than absent-before/present-after introductions"). |
| 5 | MINOR | 7.6 order 3 (line 726) | **Wrong counting units for Option D.** "Option D and E checks on their two incidents each" is wrong for Option D under the report's own counting rules (Section 2.1, line 101). Option D's direct contexts are one selected incident (the credential follow-up FINAL) plus two controls: the initial credential package is a "fail-fix-pass control" (line 150), and documentation Task 2 is "A separate Task 2 control" (line 147). Option D's own Scope row says "two selected sessions and three package/task contexts" (line 575). This mislabels the scope of the approved step. | Change to "Option D on its one incident and two controls (three contexts in two sessions); Option E on its two incidents". |
| 6 | MINOR | Section 8 Phase 2 row 1 Files (line 846) | **One file locator does not resolve.** "CI planning case, retained acceptance findings" matches no section in `research/04-session-43582de1.md`. That file has two separate numbering series (main §1-11 and supplement §1-8, which includes a second "§5"). Option A cites the same evidence precisely as "section 6.2 and supplement section 5" (line 491). Section 8 is less precise than Section 6 at the point where work would start. | Replace with "CI planning case, §6.2 (search filters) and supplement §5 (half-edited advisory header)". |

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| a | Every Section 7 recommendation can be carried out without re-research (names files, functions, integration points) | FAIL | Targets are named and exist (see Self-Audit). Order 1's procedure is ambiguous (finding 1). Order 3 depends on an unnamed repository (finding 3). |
| b | Each Section 8 step states an action, target file(s) and expected outcome | FAIL (minor) | All Phase 1-3 rows have Action, Files and "Expected observation" columns (lines 819-868). One Files locator does not resolve (finding 6). |
| c | Success criteria are testable pass/fail, not aspirational | FAIL | Direction-only criteria, with no denominator or decision rule (finding 2). The order 4 row has no criterion (finding 4). |
| d | A developer new to the investigation could start from Section 8 alone | FAIL | They could start Phase 1 binding. They could not resolve the first recommended step's procedure, judge outcomes, or locate the Option D Git objects without investigating further (findings 1-3). |
| Step 6.6-1 | Falsification can be attempted by another investigator | FAIL | Same blockers as a and c. The falsification directions exist for all five options (lines 495, 522, 549, 576, 600). |
| Step 6.6-2 | No prerequisite or approval dependency silently assumed | FAIL | Git object access and repository location are not named (finding 3). Approval is otherwise stated explicitly (lines 720, 867-868, 878). |
| Step 6.6-3 | Research-only scope preserved; no new code or remediation tasklist required to pass | PASS | Section 7 "Run no remediation" (line 634). Section 8 "UNEXECUTED" (line 781) and "not an implementation tasklist" (line 787). The Integration Checklist marks code, migration and rollback N/A with reasons (lines 905-908). None of my proposed fixes asks for code or a remediation plan. |
| Step 6.6-4 | Unknown implementation details not invented | PASS | Section 8 line 905 refuses to invent signatures. No function names or interfaces are proposed. Historical unknowns stay unknown (lines 866, 921-923). |
| Step 6.6-5 | Section 8 next-check targets exist | PASS | All 11 Phase 1 inputs, the 3 rendering targets, the oracle artifact directory and `t12-held-back-before-authorization.json`, the Orca and CI plan and review artifacts, all 6 session JSONL logs, and the `t10-markdownlint.log` candidate exist (Self-Audit 2). |

---

## Summary

- Total findings: 6
- Critical: 0
- Important: 3
- Minor: 3
- Checks passed: 3 of 9 (template a-d plus five Step 6.6 clauses)
- Issues fixed in place: 0 (report-only)

---

## Self-Audit

**(a) Reliance list (rf-qa PASS items skipped for structural re-check):**
- None. No Inherited Structural Verdict was supplied, so I relied on no earlier structural PASS. Other Phase 6 lenses (template, consistency, evidence, completeness) had not reported, and none of their results was used.

**(b) Independent semantic checks (at least one required, INV-019):**
1. Section 8 Phase 1 input table, all 11 paths: confirmed to exist with `ls -la` (6 case files, evidence deck, rule map, `historical-review-rules.json`, applicability record, gap register).
2. Rendering targets and their claimed line content (lines 830-834):
   - Plan lines 81-87 contain Task 6 and the clause "`man -l` renders both without a warning when `man` is available".
   - `t6-fix-evidence.log` lines 1-3 read "groff=none nroff=none mandoc=none man=/usr/bin/man" and record a 275-byte notice.
   - `progress.md` lines 14-18 hold the blocked verdict, the `head-moved` halt, the T6 Ruling, the `cannot-verify` completion and the FINAL pass.
   - All three match what the report claims.
3. Option A, C and E inputs:
   - The oracle artifact directory under `/config/workspace/IronClaude/.dev/worktrees/auggie-claim-gate/.../TASK-WF-designV2-20261020-132032/artifacts/` exists and contains `t12-held-back-before-authorization.json`, `t12-review-1.md` and `t12-review-2.md`.
   - `historical-review-rules.json` contains `records`, `before` and `after` keys (lines 4, 5, 13), as Section 8 row 3 cites.
4. Orca and CI artifacts listed in case 01 lines 27-54 and case 04 lines 22-66 all exist (13 Orca and 9 CI paths), including the first `coverage-matrix.yaml` and both `merged-verdict.yaml` files. The 6 session JSONL logs from the evidence-deck path register (lines 117-143) all exist.
5. The order 4 label source `debate-transcript.md:270` contains the C-001 transition labels. Credential case line 381 holds the "no `T6: Ruling:`" disposition. Rendering case lines 173-178 hold raw records 498/503/506. All match Section 8 Phase 3.
6. Finding 1 cross-check: `synthesis/hypothesis-01.md:141-142` says "construct its minimal counterexample ... Run the described check against the counterexample". This confirms the execution reading, which conflicts with Section 8 line 846 and the "read-only" claim at line 729.
7. Finding 3 cross-check: the full tree IDs are at case 03 lines 216, 229 and 237. The historical worktree root `/config/workspace/Coder/.claude/worktrees/issue-358-litellm-key-env` returned "No such file or directory". The "no new Git operation" limit is at `gaps-and-questions.md:12`.
8. Every case-file section locator in Section 8 (oracle §4.4/§6, rendering §2-5, monitor 5.2-5.4, credential §3-5, Orca §3-5 and original-repair supplement) was matched against the actual headings with `grep '^#'`. Only the CI "retained acceptance findings" locator failed (finding 6).

**Answers to the mandatory Self-Audit questions:**
1. Claims independently checked against source files: 31. These are the 11 inputs, 3 rendering files with 3 line-content claims, the oracle directory and JSON file, 3 JSON keys, 22 Orca and CI artifact paths counted as one existence claim per case, 6 session logs counted as one claim, 4 anchor-content claims, 9 section-locator claims, the hypothesis-01 procedure text, the 3 Git tree IDs, and the missing worktree path.
2. Files read: the full report, task file lines 340-449, `tech-research/SKILL.md` lines 1040-1149, `BUILD-REQUEST.md` (full), `gaps-and-questions.md` (full), `synthesis/hypothesis-01.md` lines 134-153, `merged-root-cause-analysis.md` lines 60-68, case 03 lines 173-178 and 210-240, case 06 line 381, debate transcript line 270, and the three Coder rendering files at the cited lines. Headings were read for all six case files.
3. This review did find issues. Each one cites exact report lines and the checking tool output above.
4. No web research was needed or done. No Tavily or fallback call was made.

**Items I could not verify:** Whether the three Git objects are still readable in the parent Coder repository. Blocker: my instructions prohibit Git commands. This does not weaken finding 3, which is about the report failing to name the repository and the required access, not about whether the objects survive.

---

## Confidence Gate

- **Confidence:** Verified: 9/9 | Unverifiable: 0 (one sub-fact, Git object availability, is noted above but is not a checklist item) | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 11 | Grep: 0 as a separate tool (searches ran inside Bash) | Glob: 0 | Bash: 8 (one batched inspection script with 13 checks, plus focused grep, sed and ls checks). Read plus Bash (19) exceeds the 9 checklist items.
- PASS was not possible because six real findings exist. The verdict is FAIL whatever the confidence score.

---

## Recommendations

- Send findings 1-3 to the single serialized fixer in Step 6.18, limited to Sections 6 (Option A and D rows), 7.6 and 8 and their source components `synthesis/synth-04-options-recommendation.md` and `synthesis/synth-05-implementation-plan.md`. Fixes must not add code, a remediation tasklist, or invented thresholds the evidence cannot support. If the evidence cannot support a numeric decision rule, the honest fix is to state that steps 1-3 cannot change any placement.
- Findings 4-6 are wording and locator corrections in the same sections.
- Note for consolidation: the report header (line 10) records that the synthesis gate advanced without cycle-2 verification. Sections 6-8 come from `synth-04` and `synth-05`, which cycle 2 changed (line 1187). This lens has now reviewed the post-cycle-2 text of those sections for actionability only.

## Status

| Status | Result |
|---|---|
| DONE | Read the full report, Step 6.6, the lens template, BUILD-REQUEST and the gap register. Checked every Section 8 next-check target on disk. |
| DONE | Verdict FAIL: 6 findings (3 IMPORTANT, 3 MINOR). No files edited. |
| NEXT | Parent saves this text at `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/qa/qa-lens-actionability.md` and includes it in the Step 6.17 consolidation. |

## QA Complete