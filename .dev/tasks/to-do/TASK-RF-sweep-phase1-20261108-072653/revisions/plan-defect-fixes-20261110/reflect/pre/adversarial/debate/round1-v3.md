# Debate round 1, advocate for VARIANT 3 (reviewer 3, refactorer, calibrated 0.86)

Run: sc:reflect UC-1 run 4, sc:adversarial Step 2 (steelman). Date 2026-11-10. Advocate: V3.
Abbreviations as in the prompt: ADV = `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/revisions/plan-defect-fixes-20261110/reflect/pre/adversarial`; TL = the plan `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md`; DESIGN = `docs/designs/orchestrator-mode.md`; ADD = `.../revisions/chat-output-exception-20261109-133150/design-addendum.md`; R2-BR = `.../revisions/plan-defect-fixes-20261110/BUILD-REQUEST.md`; R1-DM = `.../revisions/chat-output-exception-20261109-133150/delta-manifest.md`; R2-DM = `.../revisions/plan-defect-fixes-20261110/delta-manifest.md`; BASE = `.../revisions/plan-defect-fixes-20261110/baseline/task-before-rev2.md`; MX = `.../reflect/pre/coverage-matrix.yaml`.

Limits: read-only tools only. I did not run the plan. Where I re-checked a claim with `diff`/`grep` I say so; where I rely on diff-analysis.md without re-checking I say so.

## Section 0. Where I stand in one paragraph

V3 reported three findings, all LOW. After re-checking them against the files: R3-F1 was true when read and is now closed (kept as a LOW that drove a real fix); R3-F3 stands (LOW, inside the 85 labels); R3-F2 does not hold up and I withdraw it as a defect. V3 missed the two defects that matter most (7.17 Verification and the 7.24 safety lens), so V3's F-01 "fixed" is true for F-01's own targets and silent on the optional branch as a whole. I concede that to V2. Where V3 wins is calibration: on every point where the cards disagree about severity of a fact all three agree on (R1-F1, R1-F2, R1-F4, R1-F5, the 7.24 exit path), the lower rating is the one the files support.

## Section 1. Facts re-verified this round (my own checks)

- F-A. 7.17 is untouched by R2 and absent from both manifests. `diff` of lines 1266-1275 of BASE against TL printed `SAME_7.17_BLOCK`. `grep -c '7\.17'` on R1-DM and R2-DM printed `0` and `0`. R2-BR:17: "Allowed: the 82 labels of R1 (`../chat-output-exception-20261109-133150/delta-manifest.md`, DM:21-117) plus 13.1, 8.19 and 10.5."
- F-B. 7.24 is inside the 82 labels and R2 changed only its Context line. R1-DM:27: "| 7.24 | Read-only safety lens | Add scoped inputs; distinguish build-time Markdown edit from runtime writes/probes. |". `diff` of line 1321 (BASE vs TL) matched (`SAME_7.24_ACTION_LINE_1321`); line 1320 differs (`DIFF_7.24_CONTEXT_LINE_1320`).
- F-C. 13.18 and 13.22 are inside the 82 labels; their Action lines are untouched by R2. R1-DM:73: "| 13.18 | Serialized fix cycle1 | Explicit authority/style/evidence Context, canonical communication-file scope and immutable authority/severity boundary; ..."; R1-DM:76 gives 13.22 "Same bounded Context/allowlist/protection as cycle1"; R1-DM:100: "| 14.25 | ... four-source hash guard; ...". `diff` of TL:2384 against BASE:2384 shows only line 2383 (Context) differing; TL:2412 matched (`SAME_13.22_ACTION_LINE_2412`) and holds 0 `sha256`.
- F-D. The coverage matrix is closed. MX:1: "Tier 1, run 4 (revision plan-defect-fixes-20261110). Rows carried from run 3 and re-verified against the edited plan; INF-A06 and INF-A08 changed to covered by the second revision." MX:7 now reads `run: 4` (file mtime 06:00:13). The only `status: partial` is MX:225 (INF-017). So diff-analysis O-003 ("line 7 still reads `run: 3`") is stale on disk.
- F-E. F-06 counts: `grep -c 'Pre-7.10 source anchor for the style scope'` on TL printed 58; `grep -c 'Current source anchor for the style scope'` on TL printed 1 (TL:1209) and 59 on BASE. 58 + 1 = 59, as V3 said.
- F-F. STYLE restatements (V3 did not count these; V1 did). `grep -n 'DONE / NEXT' src/superclaude/output-styles/pragmatic.md` prints lines 22, 25, 53, 58, 60, 69, 80, 90. Line 22 is the primary rule, line 25 the length budget, 53/58/60/69/80/90 are the six later restatements. Expected 6 at TL:1293 is right (V1 correct, U-006).
- F-G. DESIGN line drift. DESIGN:557 "is a template change and needs the same owner note", DESIGN:559 "cursor template is not in the set", DESIGN:993 "a `--json` need goes to the owner", DESIGN:995 "no cursor template". TL:1267 still says "DESIGN line 552 ... line 550 ... line 971 ... line 973".

## Section 2. V3's own findings, tested again

### R3-F1 (stale coverage matrix) - kept as LOW, now closed
Evidence then: V3 quoted MX:1 as "... run 3 (revision chat-output-exception-20261109-133150)" and MX:256 as listing only the coordinator case. Evidence now: F-D. The audit log shows the finding was acted on: `audit.log` step `1B.refresh` (05:56:15): "coverage-matrix.yaml rebuilt after reviewer 3 (R3-F1) and the Tier 1 analyst (L9) found INF-A06 and INF-A08 now covered by 7.10 (second revision F-03)". V3's verifier ("`grep -n 'status: partial'` ... prints only line 225") is met on disk.
Honest limits: this is a reflect artifact, not a plan label, so it is outside the 85 by nature (n.a.). It never threatened a correct run (V3 said so: "the stale status is the more cautious one").
Concession: A-008 is CONTRADICTED for the matrix exactly as diff-analysis says; V3 read the earlier file.

### R3-F2 (13.1 credits 5.2) - WITHDRAWN as a defect
What V3 claimed: 13.1 says ticked 5.2 produced the current DESIGN R2 wording. What TL:2265 actually says: "(DESIGN line 716 at the time of this revision; item 5.2 aligned it with master's 5-minute sweep bound at `src/superclaude/core/WORKER-CONTRACT.md:110`)". That sentence is true as written: TL:776 (ticked 5.2 Action) says "also align the cadence with master's contract line 110 ... replace \"**The coordinator sweeps on every wake.**\" with \"**The coordinator sweeps on every wake, at most once every 5 minutes.**\"". The current bullet text (DESIGN:716, "runs `/sc:sweep` on every wake, at most once every 5 minutes, beside \"The sweep.\"") did come later from R4-F5 (`qa/r4/fix-log-cycle1.md:41`: "R4-F5: WC-16 now says `/sc:sweep` is an added read beside master's \"The sweep.\" ... Touches `:672`, `:677`, `:714`, `:831`."), but TL:2265 does not claim otherwise, and it already tells the executor how to handle the gap: "if it differs from this text, the DESIGN text wins and the difference is logged in `### Phase 13 Findings`. Do not edit ticked item 5.2, which keeps the older sentence as history."
What remains true: ticked 5.2's own grep (TL:778, `grep -c 'sweeps on every wake, at most once every 5 minutes\.\*\*'` returns 1) would now return 0 against DESIGN:716. Nothing re-runs it; TL:2267 even adds an expect-0 check for `sweeps on every wake`.
Position: not a defect. I drop it rather than defend it. (Diff-analysis U-011 gave it "Low"; I go lower.) 13.1 is inside the surface (R2-BR:17) so an optional wording tweak was allowed, but it is not needed.

### R3-F3 (13.18 and 13.22 have no sha256 guard on DESIGN) - kept, LOW, inside the 85
Verbatim: TL:2384 "The fix agent edits only `src/superclaude/` and `tests/` sources, the docs and `CHANGELOG.md`, never a `.claude/` or installed HOME path" and "DESIGN with its append, SPEC, revision authority and severity-test modules are immutable, with any required authority change left OPEN for escalation." Against TL:2614 (14.25): "Before spawning the agent, record the output of `sha256sum docs/designs/orchestrator-mode.md .dev/brainstorms/.../merged-requirements.md ... design-addendum.md ... BUILD-REQUEST.md` in the fix log; after it returns, re-run that command first and append a PASS line only when all four sums are unchanged". `sha256sum` occurs only at TL:1363, 1391, 2614, 2642, 2705, 2733 (grep of TL), none on 2384 or 2412.
Why it is a real inconsistency and not a taste point: R1 deliberately gave 14.25 "four-source hash guard" (R1-DM:100) and gave 13.18 only "immutable authority/severity boundary" (R1-DM:73) while "docs" in the 13.x allowlist covers `docs/designs/`. A DESIGN edit by a 13.x fixer would be invisible to the 14.25 guard, because 14.25 hashes at its own start (the already-edited DESIGN becomes the baseline).
Why LOW: the 13.18 preamble also says "Edit only the files the findings name", the lenses of the docs gate read DESIGN, and DESIGN is told to be left OPEN. No default-path run fails; it is a guard-parity gap. Origin: pre-existing, not R2 (F-C). In scope: yes, 13.18 and 13.22 are R1-DM rows; owner words cover "F-01 to F-10" (R2-BR:7) but the surface rule is label-based (R2-BR:17-18).

## Section 3. What V3 got right that the others did not
1. Closed-loop verification of the F-closure that nobody else did: 13.1 against DESIGN:716 character by character; F-06 counts (F-E); 14.19 at TL:2572 (read it again: "the owner decisions OQ-1 to OQ-8, plus any recorded OQ-17 or OQ-18 decision, reflected where they apply" - confirmed).
2. The only reviewer who checked the reflect artifacts against the plan, which produced a real fix (audit.log 1B.refresh).
3. The only reviewer who looked for guard parity across fix cycles (R3-F3). V1 found the same family at 7.30/7.34 (R1-F3/F4); V3 found the gap at 13.x. Both are guard-parity findings and both are LOW.
4. Severity discipline: three LOW, none inflated.

## Section 4. What V3 missed (conceded)
1. 7.17 Verification (TL:1274) and Completion gate (TL:1275) against the resolved resume (TL:1272). V3's self_audit lists no read of 7.17 and no read of the 7.24 Action line (TL:1321); it read the 7.24 Context lens-input wording (TL:1320) and called F-01 "fixed". The "12 lens lines" claim is true and misses the point: TL:1320 says the inputs include "any OQ-17 or OQ-18 decision record in that folder that item 7.17 wrote" while TL:1321 hard-codes "ALLOWED_ORCA holds ten templates".
2. The STYLE restatement count (F-F); I stated I did not check it.
3. A-002: V3 (and T1) judged as a careful reader. For text that the plan elsewhere writes resume-aware (see 7.10 Branch 1, Section 6), that is not safe.

## Section 5. Variant 2 (qa): steelman, test, critique

### R2-F1 (7.17 Verification and Completion gate vs the resolved resume)
Steelman. Item 7.17 is the only place where a "record PENDING" check and a "resume to RESOLVED" step live in one item. Its HALT STOPs the item (TL:1143: "Branch 1 (PENDING or empty `Chosen:`) applies the HALT rule with the `blocker_reason` the item names and STOPS"; TL:1270 "It then HALTs before step 1.2 under the Phase 7 preamble Branch 1 rule"). So the Verification clause is first reached after the resume, when the file is no longer PENDING. The clash is then literal:
- TL:1272: "it sets `status: RESOLVED`, appends the decision to `### Execution Log`, resets the task `status` to \"🟠 Doing\", and clears `blocker_reason`."
- TL:1274: "When the owner allowlist branch fires, confirm that each decision file exists with `needs_human_decision: true`, `status: PENDING` and the empty `Chosen:`, `Decided by:` and `Decision source:` lines; ... and that the task is halted (frontmatter `status` and `blocker_reason` set by the HALT rule) before any step 1.2 item runs."
- TL:1275: "The facts file is written with no open HALT."
Test against files: all three quotes are verbatim on the cited lines. Three of the four sub-checks fail after a correct resume (PENDING, empty lines, halted); the fourth passes (the `HALT (PENDING)` row count stays 1 because the Execution Log is append-only). The task skill re-enters at the first unchecked item (`src/superclaude/skills/task/SKILL.md:535` "Find the first unchecked item - Scan for the first `- [ ]` item. This is where execution resumes."), and 7.17 is unticked while halted.
Extra support nobody cited: the plan's own house pattern keeps the two apart. 7.1 is the record item ("7.1 - Record decision GQ-10 ... PENDING", TL:1145) with Verification "Verify: `status: PENDING`, both options quoted ... and the four empty decision lines" (TL:1149), and 7.2 is a separate HALT item (TL:1152). 7.17 merges them and kept the record-time Verification. That makes the clash a design slip, not an intended reading.
Where V2 is weaker than it sounds: "When the owner allowlist branch fires" can be read as a first-halt condition (diff-analysis agrees). A careful executor could run the PENDING checks at the halt moment and the Completion gate at resume. But that reading is not written, and the same Verification paragraph says earlier "in either case stop before marking this item complete until the blocker is resolved" (TL:1274), i.e. it presents itself as the completion test.
Verdict: V2 is right. Severity: H, conditional on the branch firing. Reason for H and not M: a correct run (approval or refusal resume) cannot satisfy the item as written, and 7.17 has no named exit. 7.17's Verification offers only "stop before marking this item complete until the blocker is resolved" for its sample-missing cases, and there is no gate item after 7.17 whose job is to take this finding (contrast R2-F2 below). I did not trace which later items depend on 7.17 being ticked, so I do not rely on that.
Scope: outside the 85 (F-A). V2's "needs a bounded authorization extension" is correct. A short appended note (R2-BR:17 "A short additive note may be appended after the existing R1 note") would not change the item's literal Verification, so it is not an in-surface fix.
Related, same item (O-001): TL:1270 step 1 says "The branch first writes a decision file ..." with `status: PENDING`. A resume that re-enters 7.17 and reads its Action top-down would write PENDING over the RESOLVED record. Step 3 (TL:1272) says what the resume does but no text says step 1 is skipped when the file exists. Inference (no run); same gap seen from the Action side; same item, same scope answer.

### R2-F2 (7.24 safety lens vs an approved allowlist change)
Steelman. After owner approval, 7.17 step 2 (TL:1271) changes the 7.16 forbidden list "to allow the approved argv and a re-capture of it" and the 8.10/10.3 count "from the literal 10 to the approved count". The follow-up list names 7.3, 11, 12, 15.1, 8.10, 10.3, 7.16 and 6.5-6.22. It does not name 7.24. TL:1321 still says: "that no forbidden token (worker-read, gate-list, check, inbox, --include-remote, git stash, run-current --json) was run", "that ALLOWED_ORCA holds ten templates with the two worktree ps --agent-wait forms as templates 9 and 10" and "Each breach is BLOCKING." DESIGN:559: "it is added only after step 1.0a captures the cursor field, as one extra template" and DESIGN:557 "is a template change and needs the same owner note". So a correctly approved cursor template or `run-current --json` re-capture produces a BLOCKING finding.
Test: quotes verified (TL:1271, TL:1321 read this round). Same-item inconsistency exists on disk: TL:1320 (Context, changed by R2) lists "any OQ-17 or OQ-18 decision record in that folder that item 7.17 wrote" as input; TL:1321 (Action, unchanged since BASE, F-B) rejects what such a record would approve.
Where V2 overreaches: HIGH. The consequence path is: BLOCKING in the 7.24 report -> 7.29 consolidation -> 7.30 fixer. The fixer cannot repair a plan prompt, and the 7.30 allowlist says "it may never change a decision's `Chosen:` line or re-run a live Orca command. A finding that needs the owner or a new capture is left OPEN with that reason." (TL:1363). After two cycles, 7.37 step (d) (TL:1412) names the exit: "write `Decisions gate: HALT after 2 fix cycles, open findings: <ids>`, apply the HALT rule ... and escalate the open BLOCKING and MAJOR findings to the user." So the plan has a designed owner escalation for exactly this kind of leftover finding. That is a real nuisance (an unneeded gate HALT, two fix cycles spent) but it is a workaround-bearing defect, i.e. MEDIUM on the stated scale. Also unreachable on the default path and on the refusal path (TL:1272 keeps ten templates on refusal).
Scope: inside the 85 (F-B): 7.24 is an R1-DM row and only the Action line needs a clause. V2's own fix text is small. The owner wording "F-01 to F-10" does not name it (R2-BR:7), but R2-BR:17 defines the surface by label.
Verdict: V2 right on the fact; MEDIUM, not HIGH.

### R2 summary on V2
V2's "no shell, no hash recomputation" limits are honestly stated, its glob trace is confirmed (diff-analysis U-009 ran the match), and its origin statement ("predate R2") is correct (F-A, F-B). V2's weakness is calibration of R2-F2 and the absence of any LOW findings: it read the consumers deeply and the guard/pattern items not at all, so it missed R1-F3/F4 and R3-F3.

## Section 6. Variant 1 (analyzer): steelman, test, critique

General steelman for V1: it is the only card that traced the 7.10 lifecycle (first run, no authorization, failed check, resume) and compared 7.10 with ADD sentence by sentence, and all of its quotes are real. Its facts hold; its severities run one level high (calibration 0.68, ESCALATE, fits). It was also honest about what it did not read (7.17 text, 7.27-7.29, 7.31-7.33, 13.1, 8.19, 10.5).

### R1-F1 (7.20 accepts the planning authorization)
Steelman. TL:1293 makes the match target the R2 section: "the quote must match the owner's words in the `## Authorization (direct, by the owner)` section of `.../plan-defect-fixes-20261110/BUILD-REQUEST.md` or, when the separate execution authorization is a later dated owner message, that message as supplied with the fresh reports; a quote written by the executor is a record of that authorization, not independent evidence, so a mismatch or an empty section is a FAIL". The words in that section (R2-BR:7) are "Fix the plan first ... Do not start 7.10. Authorize a second bounded revision now ... then execute", and TL:3020 says "Separate execution authorization remains required after fresh revision checks/PRE." The "later dated owner message" branch has no file to compare. True.
Test. The match target was put there on purpose: R2-DM:28 "| B2-1 | 1293 (7.20) | The execution-authorization quote is compared with the `## Authorization (direct, by the owner)` section of the R2 `BUILD-REQUEST.md`, or with a later dated owner message supplied with the fresh reports |". The same section designates the execution direction: R2-BR:9 "the owner's earlier direct instruction \"Already approved plan is confirmed proceed with implementation\" and this answer's \"then execute\" are recorded as the owner's execution direction; the executor re-confirms in its result file before the style edit". So the authority text points both ways (R2-BR:9 vs TL:3020), which is the root cause, and it sits in a BUILD-REQUEST, not a plan label. 7.20 also still demands the dated quote and "the paths of the fresh structural, alignment, qualitative and PRE reports as supplied with it" (TL:1293), and 7.10 Branch 1 (TL:1210) refuses to start without "fresh revision structural/alignment/operational-QA/PRE sign-off or separate direct execution authorization". V1's "Today 7.20 returns PASS" for a quote of "Do not start 7.10" is not literal: the quote must also be dated and accompanied by report paths. V1's fix (drop the R2 section as a match target, add a saved-message file) reverses a deliberate edit and needs a file the plan never creates.
Verdict: real weakness (record check on text the executor writes), overstated. LOW.

### R1-F2 (resume or retry of 7.10)
Steelman. Branch 2 says "only after first writing the dated verbatim text ... into ... under the heading `## Execution authorization (verbatim)` BEFORE the first style edit" and nowhere says "unless it exists"; a retry after a failed bounded check would re-apply "Qualify the six later mandatory restatements ... with `Except for the sweep chat-summary exception above,`" to an already edited file.
Test. V1's quotes are right, but V1 missed that Branch 1 of the same line already handles the resume case: TL:1210 "(look first for the `## Execution authorization (verbatim)` section in the result file named in Output, because a resumed session does not remember the chat)". TL:1211 adds "(later content is appended below it, never overwriting it)". So the plan authors did write resume-aware text for the section; what is left is a one-clause gap ("if the section exists, do not write it again; if the style file already holds the exception, verify instead of re-applying"). Consequences (second section, double prefix) are inference.
Verdict: real text gap, small. LOW. (This is also why I do not accept the careful-reader premise for 7.17: where the authors thought about resume they wrote it, and for 7.17 they did not.)

### R1-F3 (sha256 baseline in the fix-log file)
Steelman. TL:1363: "record the output of `sha256sum ...` in `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/decisions/fix-log-cycle1.md` (hash only the OQ-6 record ...)" and, later, the agent is told "Write a fix log listing each finding id, the change, and the `file:line` after the change." and the output path is the same fix-log file. A stub-first Write by the agent erases the baseline.
Test. Quotes verified (TL:1363, read this round). The F-07 requirement as the cards state it (sums recorded before the spawn, compared after) is met: "after the agent returns, re-run that command first and append a PASS line only when all four sums are unchanged". The orchestrator holds the sums in its session. The same pattern appears in 14.25 (TL:2614 "in the fix log") and the other `sha256sum` sites (TL:2642, 2705, 2733), i.e. it is the house pattern of six items, not an R2 slip. The cost of loss is the written baseline (audit trail) and a resume case, not the check in a normal run.
Verdict: V1's strongest finding; real, cheap to fix in 7.30/7.34 (a separate `sha256-before-cycleN.txt`), but a consistent fix would also touch 14.25/14.29/14.38/14.42 (all R1-DM rows). LOW (borderline Medium-Low; I hold 0.55 on L).

### R1-F4 (re-run lists omit the section check; no hash on the 7.10 result file)
Test. TL:1363: "For the bounded exception only, also permit `src/superclaude/output-styles/pragmatic.md` and `.../step-7.10-style-exception.md`". The re-run list (read in full this round) has the OQ-RESOLVED count, the OQ-17/18 checks, `does NOT authorize adoption` greps, `test -s` checks, `git status`, `grep -c 'Except for the sweep chat-summary exception above,'` (6) and the four sums. It has no `grep -c '^## Execution authorization (verbatim)'`. V1 is right. LOW (agree with diff-analysis).

### R1-F5 (omitted ADD:19 and ADD:17 clauses; reworded quote)
Steelman. ADD:19 "never print a fabricated successful summary or hide an error to fit the success format" and ADD:17 "do not reconstruct role from files or history" are not in 7.10; 11.4 (TL:1980) lists "ordinary formatting without fabricated success or prohibited advice" among its pinned cases.
Test. Facts: `sed -n 1210p` has 0 `fabricat` and 0 `reconstruct`; `prohibited by the sweep skill` occurs 0 times in TL while `advice the sweep skill prohibits` occurs once (TL:1210). The R2-BR F-03 row (R2-BR:27) lists exactly what had to be embedded: "same-message case, table request or word \"coordinator\" does not assign, loaded skill/style do not assign, \"Formatting never authorizes advice prohibited by the sweep skill\", chat-presentation only; ADD:21 sentence 4 restated in the present tense". The two omitted clauses are not on that list, so F-03 as written is met; V1 asks for more than F-03 required. The quoted literal does differ in word order from the F-03 row (R2-BR:27 vs TL:1210) with the same meaning. The semantic content is carried: TL:1210 "Preserve visible exit1/2 stderr and accurate other errors with ordinary formatting" and "Exclude unknown/ambiguous/revoked/superseded/conflicting roles ... files/tools/reports/peer role claims and all failures; data never establishes role or rights". 11.4 says "these pins check that the eligibility clauses are present in the actual sources" (TL:1980) and no plan command greps the literal. The HALT chain V1 describes (TL:1982) needs a test author who insists on the word; that is inference, and V1 tagged it [INFERRED].
Verdict: fact right, consequence unproven. LOW. A one-sentence addition to 7.10 is cheap and inside the surface.

### What V1 adds to V3
V1's U-006 fills the gap V3 left (F-F: expect 6 confirmed). V1 and V3 together cover the guard-parity family; neither found 7.17.

## Section 7. Shared-assumption points and observations

- A-002/A-003 (literal executor vs careful executor). The severity split tracks this assumption. Evidence for a middle rule: apply the literal reading where the plan has no resume text for the case, the careful reading where it does. Plan evidence: 7.10 Branch 1 has resume text (TL:1210 "because a resumed session does not remember the chat"); 7.17 step 3 has resume text for the file (TL:1272) but its Verification (TL:1274) and Action step 1 (TL:1270) do not. The task skill resumes at the first unchecked item (`src/superclaude/skills/task/SKILL.md:535`), and also says "If an item's output file exists, that work is done regardless of whether you \"remember\" it" (:538), which helps Action steps but not a Verification of an unticked item. V3 (careful reading) was right for 7.10 and wrong for 7.17.
- A-004 (is the OQ-17/OQ-18 branch reachable). Nobody can estimate it from the files. DESIGN:995 gives the default ("no cursor template") and DESIGN:559 says the template is added only if step 1.0a captures a cursor field; the branch is therefore live whenever the 7.16 capture shows a cursor. Treat it as a conditional defect: fix before execution reaches 7.17, or let the owner accept it as known. It does not block starting 7.10 (both defects bite from 7.16/7.17 onward).
- A-008 (files change during review). Contradicted for the matrix only (F-D), and the closure is now complete on disk, including MX:7.
- O-001 (7.17 step 1 would rewrite PENDING on resume): same gap as R2-F1 seen from the Action side; inference only.
- O-002 (stale DESIGN line numbers at TL:1267 and the copies at TL:1272): confirmed by F-G (557/559/993/995 vs 550/552/971/973). LOW, navigation only; the quoted sentences are intact and findable; 7.17 is outside the 85.
- O-003 (matrix line 7 `run: 3`): no longer true (F-D: MX:7 `run: 4`).

## Section 8. Positions

Format: `POINT <id>: winner <variant or none>, confidence <0-1>, final severity <H/M/L>, in-scope-of-85 <yes/no/n.a.>`. In-scope means a fix can sit inside the 85 allowed labels (R2-BR:17).

Structural and content points
POINT S-001: winner V2, confidence 0.70, final severity H, in-scope-of-85 n.a.   (the profile that matches the files is 1 H-conditional, 1 M, several L; V2 found the top two, V3 and V1 are right on every LOW they report)
POINT S-002: winner none, confidence 0.60, final severity L, in-scope-of-85 n.a.   (slice differences explain the 7.17 miss; V3's slice never included 7.17)
POINT S-003: winner V2, confidence 0.70, final severity L, in-scope-of-85 n.a.
POINT S-004: winner V3, confidence 0.65, final severity L, in-scope-of-85 n.a.   (only V3 opened the reflect artifacts; that produced the matrix refresh)
POINT S-005: winner V1 on R1-F3's remedy, V2 on 7.17's remedy, confidence 0.55, final severity L, in-scope-of-85 yes   (7.30/7.34 paths and the 7.24 clause are in-surface; the 7.17 split is not)
POINT S-006: winner none, confidence 0.80, final severity L, in-scope-of-85 n.a.
POINT S-007: winner none, confidence 0.80, final severity L, in-scope-of-85 n.a.
POINT C-001: winner V2, confidence 0.75, final severity H, in-scope-of-85 no   (7.17 outside; F-01 as scoped is fixed)
POINT C-002: winner V3, confidence 0.65, final severity L, in-scope-of-85 yes
POINT C-003: winner V1, confidence 0.55, final severity L, in-scope-of-85 yes
POINT C-004: winner V3, confidence 0.65, final severity L, in-scope-of-85 yes
POINT C-005: winner V2, confidence 0.85, final severity H, in-scope-of-85 no   (7.17 outside; 7.24 and 13.18/13.22 inside, so the discipline point is: 7.17 needs an owner extension, the others do not)
POINT C-006: winner V2, confidence 0.90, final severity H, in-scope-of-85 n.a.   (neither HIGH nor MEDIUM defect is caused by the 73 changed lines: F-A, F-B)
POINT C-007: winner none, confidence 0.70, final severity L, in-scope-of-85 n.a.

Contradictions
POINT X-001: winner V2, confidence 0.75, final severity H, in-scope-of-85 no   (F-01 targets fixed; the optional branch is not coherent end to end; T1's "coherent end to end" overreaches)
POINT X-002: winner V3, confidence 0.70, final severity L, in-scope-of-85 yes   (F-04 requirement met at TL:1210, 1211, 1293; residuals are R1-F2/F4, both LOW)
POINT X-003: winner V1, confidence 0.55, final severity L, in-scope-of-85 yes   (fixed as specified with a LOW residual)
POINT X-004: winner V2, confidence 0.90, final severity H, in-scope-of-85 n.a.
POINT X-005: winner V3, confidence 0.65, final severity L, in-scope-of-85 yes   (B2-1 made the R2 section the match target on purpose; the ambiguity is in R2-BR:9)
POINT X-006: winner V3, confidence 0.90, final severity L, in-scope-of-85 n.a.   (true when read, now closed including MX:7)
POINT X-007: winner V3, confidence 0.65, final severity L, in-scope-of-85 yes   (V1 right on the fact, V3 right on the severity)

Unique contributions
POINT U-001: winner V3, confidence 0.65, final severity L, in-scope-of-85 yes   (R1-F1)
POINT U-002: winner V3, confidence 0.60, final severity L, in-scope-of-85 yes   (R1-F2; Branch 1 already has the look-first clause)
POINT U-003: winner V1, confidence 0.55, final severity L, in-scope-of-85 yes   (R1-F3)
POINT U-004: winner V1, confidence 0.70, final severity L, in-scope-of-85 yes   (R1-F4)
POINT U-005: winner V3, confidence 0.65, final severity L, in-scope-of-85 yes   (R1-F5; not on the R2-BR F-03 list)
POINT U-006: winner V1, confidence 0.90, final severity L, in-scope-of-85 n.a.   (not a defect; confirms expect 6)
POINT U-007: winner V2, confidence 0.70, final severity H, in-scope-of-85 no   (R2-F1; conditional on the branch; no named exit; 0.30 residual weight on the first-halt reading giving M)
POINT U-008: winner V2, confidence 0.75, final severity M, in-scope-of-85 yes   (R2-F2; real, but 7.30/7.37 give a named owner escalation, so not H)
POINT U-009: winner V2, confidence 0.85, final severity L, in-scope-of-85 n.a.   (verification method, not a defect)
POINT U-010: winner V3, confidence 0.90, final severity L, in-scope-of-85 n.a.   (R3-F1, closed)
POINT U-011: winner none, confidence 0.70, final severity L, in-scope-of-85 yes   (R3-F2 withdrawn by its own advocate; TL:2265 is true as written; no defect)
POINT U-012: winner V3, confidence 0.70, final severity L, in-scope-of-85 yes   (R3-F3; 13.18/13.22 are R1-DM rows; Action lines unchanged by R2)
POINT U-013: winner V3, confidence 0.75, final severity L, in-scope-of-85 n.a.   (13.1 quote equals DESIGN:716; not a defect)

Shared assumptions and observations
POINT A-002: winner V2, confidence 0.60, final severity M, in-scope-of-85 n.a.   (literal where the plan has no resume text, careful where it has)
POINT A-004: winner none, confidence 0.50, final severity M, in-scope-of-85 n.a.   (unquantifiable; keep the defects conditional)
POINT A-008: winner V3, confidence 0.90, final severity L, in-scope-of-85 n.a.
POINT O-001: winner V2, confidence 0.50, final severity M, in-scope-of-85 no   (inference; same item and same gap as U-007)
POINT O-002: winner none, confidence 0.85, final severity L, in-scope-of-85 no   (stale DESIGN line numbers in 7.17)
POINT O-003: winner V3, confidence 0.85, final severity L, in-scope-of-85 n.a.   (no longer true on disk)

## Section 9. My ranked defect list for the edited plan (V3 advocate's view)

1. 7.17 Verification (TL:1274) and Completion gate (TL:1275) cannot be satisfied by a correct resume of the owner allowlist branch; Action step 1 (TL:1270) would also rewrite PENDING over RESOLVED. HIGH if the branch fires. Outside the 85 (needs an owner extension; an appended note does not change the literal Verification).
2. 7.24 safety lens (TL:1321) rejects an approved cursor template or `run-current --json` re-capture and is missing from the 7.17 step 2 follow-up list (TL:1271). MEDIUM (named escalation at TL:1363 and TL:1412). Inside the 85.
3. LOW, all inside the 85: sha256 baseline shares a file with the fix log at 7.30/7.34 (and the same pattern at 14.25/14.29/14.38/14.42); 7.30/7.34 re-run lists omit the `## Execution authorization (verbatim)` count; 7.10 has no "section already exists" clause for Branch 2; 7.10 omits ADD:19/ADD:17 clauses and rewords the ADD:19 quote; 13.18/13.22 lack a DESIGN hash guard; 7.20 matches a record the executor writes (deliberate B2-1, authority ambiguity at R2-BR:9 vs TL:3020).
4. LOW, outside the 85: 7.17 Context cites DESIGN lines 550/552/971/973 that now sit at 557/559/993/995.
5. Not defects after checking: R3-F2 (withdrawn), R3-F1 (closed on disk), the matrix `run: 3` residue (gone).

Net on V3: three LOW findings, one closed, one withdrawn, one kept; two HIGH-or-MEDIUM defects missed. On the reading of "true defects of the edited plan" the answer is V2 for the top two, V3 and V1 for the LOW tail, with severity set as in Section 8.

Unchecked by me: 8.19 and 10.5 bodies, 7.22/7.25 count wording, 7.27-7.29 and 7.31-7.33, any execution of the plan or of the greps.
