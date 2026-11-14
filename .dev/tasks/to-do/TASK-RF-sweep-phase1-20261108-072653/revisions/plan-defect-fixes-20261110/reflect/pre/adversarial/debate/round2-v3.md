# Debate round 2 (rebuttals), advocate for VARIANT 3 (reviewer 3, refactorer, calibrated 0.86)

Run: sc:reflect UC-1 run 4, sc:adversarial Step 2. Date 2026-11-10. Advocate: V3. Round 2 reads round1-v1.md, round1-v2.md and my round1-v3.md first.
Abbreviations as in round 1: TL = the plan `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md`; DESIGN = `docs/designs/orchestrator-mode.md`; R2-BR = `.../revisions/plan-defect-fixes-20261110/BUILD-REQUEST.md`; R1-DM = `.../revisions/chat-output-exception-20261109-133150/delta-manifest.md`; PC = `.../revisions/plan-defect-fixes-20261110/qa/preservation-check.json`.
Limits: read-only tools. I did not run the plan. Every "this round" check below was a grep, sed or JSON read of the file on disk.

## Section 0. Where I stand after round 1, in one paragraph

Three positions moved. (1) 7.24 (U-008): I move from MEDIUM to HIGH-conditional. My MEDIUM rested on "7.37 names an owner escalation". That is only true for the second cycle; the first-cycle halt at 7.33 names none. (2) R1-F3 (sha256 baseline shares the fix-log file): I move from LOW to MEDIUM, because the 7.30 and 7.34 lines holding it were changed by R2 itself and the overwrite is ordinary agent behaviour. (3) R3-F2 stays withdrawn and R3-F1 stays closed; R3-F3 stays LOW and inside the 85, and I drop one of its two fixes. Everything else I held in round 1 survives V1's and V2's rebuttals.

## Section 1. New facts verified this round

- N-1. TL:1384 (7.33) has no escalation wording. `sed -n 1384p TL | grep -c escalate` printed `0`. The line says "(b) Monotonicity: if `|F_1| >= |F_0|`, write `[HALT-MONOTONICITY] |F|=<n>` with `<n>` = `|F_1|`, and apply the HALT rule (set frontmatter `status` to "⚪ Blocked", put the halt line in `blocker_reason`, append it to `### Execution Log`, STOP, and do not tick this item)". Only 7.37 (TL:1412) says "and escalate the open BLOCKING and MAJOR findings to the user".
- N-2. A single unfixable BLOCKING finding reaches that halt in cycle 1. TL:1384: "build `F_1` = the `F_0` ids that either verifier marks OPEN". TL:1363: "A finding that needs the owner or a new capture is left OPEN with that reason." With `|F_0|` = 1 and the finding left OPEN, `|F_1|` = 1, and `1 >= 1` gives HALT-MONOTONICITY at 7.33. 7.37 is never reached.
- N-3. The approval follow-up is written to run at the resume of 7.17, before 7.17 completes. TL:1272: "An approval resumes into the step 2 follow-up." TL:1271: "an owner approval triggers this follow-up work: a DESIGN edit item for 7.3, 11, 12 and 15.1 with its own review gate; the 8.10 and 10.3 count source changed from the literal 10 to the approved count ... and a re-run of the R5 review gate (6.5 to 6.22)". 7.17 is item 1266 and the lens items are 1298-1404, so by that text DESIGN 7.3 is already edited when 7.24 runs. The plan names no item or slot for the DESIGN edit, so this order is the natural reading, not a stated rule.
- N-4. The fixer of 7.30 may edit the very section the lens reads. TL:1363: "The fix agent may correct ... the R5 DESIGN edits listed in item 6.3 (sections 7.3, 11, 12, 13 and 15.1, the GQ-109 row and the `### Fix cycle 3` R5 row)". So a literal fixer given the finding "ALLOWED_ORCA holds eleven templates, not ten" has an in-allowlist way to revert the approved template. TL:1363 also says "Never change revision authority/design append/decision choice", which a careful fixer would read as a block. That reading is inference; I list it as a risk, not as a fact.
- N-5. R2 changed the 7.30 and 7.34 Action lines, the lines that carry the hash baseline. PC `changed_by_label`: `{'7.30': [1362, 1363], '7.34': [1390, 1391], '7.24': [1320], '13.18': [2383], '13.22': [2411], ...}`. 7.17 is not in `changed_by_label` (`[k for k in ['7.17','13.18','13.22'] if k not in c]` printed `['7.17']`). 13.18 and 13.22 changed only their Context lines (2383, 2411); their Action lines 2384 and 2412 are untouched. Consequence for X-004 and C-006: "R2 did not cause the defect" is true of 7.17, 7.24's Action line and 13.18/13.22, but it is not true of R1-F3, which sits in R2's own changed lines (TL:1363, TL:1391).
- N-6. 14.25 lists `docs/` in the same fix-agent edit scope as 13.18. TL:2614: "The fix agent edits only `src/superclaude/`, `tests/`, `docs/`, `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.`..." and 14.25 then hashes DESIGN. TL:2384 (13.18): "The fix agent edits only `src/superclaude/` and `tests/` sources, the docs and `CHANGELOG.md`". The scope words are the same; the guard is not.
- N-7. The frozen hash I named in R3-F3's second fix is not in the plan. `grep e4a06d0c` over the task folder matched only reflect briefs and cards (`reviewer-briefs/common.md`, the three reviewer-3 files, `reflection-card-t1.yaml`), not TL. I withdraw that second fix option (see Section 4).
- N-8. The R2 owner authorization is worded by surface, not by finding. R2-BR:9: "This authorizes: plan-text edits to exactly the surface below, and the re-run of every mandatory check." R2-BR:17: "Allowed: the 82 labels of R1 ... plus 13.1, 8.19 and 10.5." R2-BR:18: "only existing Context/Action/Output/Verification/Completion-gate lines of those labels may change". The owner's own question text says "covering F-01 to F-10" (R2-BR:7). Both facts go into the scope column below.
- N-9. The manifest rows for the 14.x guards exist. R1-DM:100 (14.25), :103 (14.29), :110 (14.38), :113 (14.42) all say "hash". So a parity edit to 14.x is inside the 85. R1-DM:73 and :76 give 13.18 and 13.22; R1-DM:27 gives 7.24; there is no 7.17 row.

## Section 2. The criticisms made of V3 in round 1, and my answers

### 2.1 "V3 said F-01 is fixed and the OQ-17/OQ-18 branch is coherent end to end" (V1 3.4; V2 section 2 C-001)

Strongest version: V3's slice never contained TL:1274 or TL:1321, so "fixed" and T1's "coherent end to end" cannot be a finding about the optional branch.
Test: true. My self_audit lists no read of 7.17 and no read of the 7.24 Action. My F-01 line says the lens-input wording is on "all 12 lens lines (1299..1404)", which is true and does not touch TL:1321.
Answer: conceded in full. F-01 as scoped is fixed ("fixed (scope) / open (branch)", a label V1 and V2 now share). I have no defence of "coherent end to end".

### 2.2 "V3 judged F-07 fixed and missed where the baseline is written" (V1 3.4; V2 section 3)

Strongest version: TL:1363 records the sums "in `.../qa/decisions/fix-log-cycle1.md`" and tells the fixer to write its fix log to that same path.
Test: verbatim at TL:1363: "record the output of `sha256sum ...` in `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/decisions/fix-log-cycle1.md`" and "Write a fix log listing each finding id, the change, and the `file:line` after the change." and "Pass it ... the output path `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/decisions/fix-log-cycle1.md`". TL:1391 repeats it for cycle 2. N-5 shows these are R2's own changed lines.
Answer: conceded as a miss. See Section 6 for the severity.

### 2.3 "V3 called the reworded ADD:19 quote not blocking because no check greps it, which is a fact about today, not a protection" (V1 3.4)

Strongest version: 11.4 (TL:1980) is where the pin lives, so "no check greps it" can change when that item runs.
Test: TL:1980 (read in round 1) says the 11.4 pins check "that the eligibility clauses are present in the actual sources", and TL:1982 routes a style failure to a HALT. R2-BR:27 (the F-03 row) lists the clauses to embed and does not name "fabricated" or "reconstruct". TL:1210 has no `fabricat` and no `reconstruct` (round-1 check).
Answer: V1 is right that "no check greps it" is not a guarantee. It is still a LOW: the F-03 list is met, the substance of both ADD clauses is in TL:1210 in other words, and the HALT chain needs a test author who insists on one word. I accept the cheap fix as worth doing.

### 2.4 "V3 withdrew R3-F2, so V3 wins U-011" (V2 section 4)

V2 gave U-011 to V3 at 0.92 and called it LOW. I keep my round-1 position: the defect claim fails. TL:2265 says "item 5.2 aligned it with master's 5-minute sweep bound" and also "if it differs from this text, the DESIGN text wins". It does not credit 5.2 with the R4-F5 wording. The one true fact (ticked 5.2's grep would now return 0) has no reader. Winner none, no defect.

### 2.5 "V3 has no HIGH or MEDIUM finding" (V1 3.4; V2 section 5)

Accepted. V3's value is the verification breadth (13.1 against DESIGN:716, F-06 counts, 14.19), the reflect-artifact check that led to the matrix refresh, and the guard-parity finding at 13.x. I do not claim defect discovery on the optional branch.

## Section 3. The disputed point: 7.24 severity, HIGH or MEDIUM

### 3.1 Strongest version of the HIGH case (V1 section 2.2; V2 section 2)

After an approved cursor template or `run-current --json` change, 7.17 changes the count source from the literal 10 to the approved count (TL:1271), while the 7.24 lens still hard-codes TL:1321: "that ALLOWED_ORCA holds ten templates with the two worktree ps --agent-wait forms as templates 9 and 10", "that no forbidden token (worker-read, gate-list, check, inbox, --include-remote, git stash, run-current --json) was run" and "Each breach is BLOCKING." The finding cannot be fixed, so it deadlocks the Decisions gate through the monotonicity halt.

### 3.2 Tests

- Facts: TL:1271, TL:1321 verbatim as above. DESIGN:559: "it is added only after step 1.0a captures the cursor field, as one extra template (SPEC line 320)." DESIGN:557: "that is a template change and needs the same owner note as any other allowlist change". So an approved cursor template makes eleven templates, and an approved `--json` changes the run-current template. Either one breaks a literal TL:1321 check.
- Origin: TL:1321 is untouched by R2 (PC shows only 7.24 line 1320). R1-DM:27 puts 7.24 in the 82. So a fix is inside the 85 mechanically (N-9, N-8).
- Chain: N-2 and N-1. The finding is left OPEN under TL:1363; `|F_1| >= |F_0|` when it is the only finding; 7.33 halts without naming an escalation. If other findings are fixed, `|F_1| < |F_0|`, cycle 2 runs, and 7.37 (TL:1412) halts at "hard cap ... escalate the open BLOCKING and MAJOR findings to the user".
- Ordering (N-3): TL:1272 "An approval resumes into the step 2 follow-up", so DESIGN 7.3 is edited before the 7.21-7.28 panel runs. If the follow-up were instead placed after 7.37, the ten-template check would pass at 7.24 time; the plan does not say. This is the weakest link in the HIGH case and I give it 0.3 weight.

### 3.3 What I withdraw and what I keep

Withdrawn: my round-1 reason for MEDIUM ("the plan has a designed owner escalation ... 7.37 step (d) names the exit"). N-1 and N-2 show that for a single unfixable finding the halt is at 7.33, which has no escalation wording. I had cited only 7.37.
Kept as a caveat: the lens agent reads the OQ-17/OQ-18 record, since TL:1320 now lists "any OQ-17 or OQ-18 decision record in that folder that item 7.17 wrote" among its inputs (an R2 edit). A judgment-minded agent may mark the breach MINOR. But the prompt says "Each breach is BLOCKING", and the lens is a count and a token list, so I do not rate that mitigation above 0.35.
Also new (N-4): a literal 7.30 fixer is allowed to edit DESIGN 7.3, so the failure mode may be a reverted approved template, not only a halt. Inference; it points the same way (worse, not better).

### 3.4 Position

HIGH, conditional on (a) the owner allowlist branch firing, (b) the owner approving, and (c) the follow-up landing before 7.24 (TL:1272 supports this order). On the default path and on refusal (TL:1272 keeps ten templates) there is no effect. By the prompt's scale ("a correct run fails") an approved, correct run does not clear the Decisions gate, and no item in the plan can clear it. Unconditionally the effect is MEDIUM, which is why I hold 0.55, not 0.8. It is the same conditionality as 7.17, so the two should carry the same label.

POINT U-008: winner V2, confidence 0.55, final severity H, in-scope-of-85 yes

### 3.5 Scope of the 7.24 fix

In the 85 by the label rule (R1-DM:27; R2-BR:17-18; TL:1321 is an existing Action line). Two honest qualifications. First, it is not one of F-01 to F-10, and the owner's question says "covering F-01 to F-10" (R2-BR:7), while R2-BR:9 authorizes "exactly the surface below". The prompt defines in-scope as the 85 labels, so I answer yes, and I flag that a reader who ties the authorization to the ten findings would want the owner to accept this edit by name. Second, the smallest fix (V2's clause: "when the owner allowlist branch of 7.17 was approved, check the approved argv, template count and re-capture recorded in the 1.0a facts file instead of the ten-template and run-current rules; with no approval, keep them") goes on TL:1321 only, so it does not fix 7.17.

## Section 4. R3-F3 (13.18 and 13.22 lack a DESIGN hash guard): settled

Strongest version of the other side (V2 section 4, U-012): the same lines already say DESIGN is immutable and tell the fixer to leave authority changes OPEN, so a correct fixer is not authorized to edit DESIGN; the gap is a mistake guard, not a loophole.

Test: TL:2384: "DESIGN with its append, SPEC, revision authority and severity-test modules are immutable, with any required authority change left OPEN for escalation." The 13.18 fix preamble, which I quoted from TL:2614 and which 13.18 shares, says "Edit only the files the findings name". Against that: the edit scope names "the docs" (TL:2384) and `docs/` (TL:2614, N-6); DESIGN sits under `docs/designs/`. `grep -n sha256sum` on TL prints lines 1363, 1391, 2614, 2642, 2705, 2733 and none on 2384 or 2412. 14.25 hashes at its own start (TL:2614: "Before spawning the agent, record the output of `sha256sum docs/designs/orchestrator-mode.md ...`"), so a DESIGN edit made by a 13.x fixer is already inside 14.25's baseline and is not caught. R1 gave 14.25, 14.29, 14.38 and 14.42 a "hash guard" (R1-DM:100, :103, :110, :113) and gave 13.18 and 13.22 none (R1-DM:73, :76 say "immutable authority/severity boundary" and "Same bounded Context/allowlist/protection").

Conclusions:
- Real parity gap, LOW. A correct run does not fail. The protection is prose instead of a check, and the fixer is told to leave it OPEN.
- Pre-existing: TL:2384 and TL:2412 are not in PC changed lines (N-5).
- Inside the 85: 13.18 and 13.22 are R1-DM rows. A hash step on the Action lines is allowed under R2-BR:18.
- Fix: keep only the first fix (record and re-check the four-file sha256sum before and after the spawn, as 14.25 does). Withdraw the second ("compare DESIGN against the brief's frozen hash e4a06d0c"): N-7 shows that hash is not in the plan.
- Build the fix with Section 6 in mind: write the 13.x baseline to a separate orchestrator-owned file, not the fix log, or the parity fix copies R1-F3.
- [INFERRED] stays on the claim, since it needs a fixer to act against an explicit prohibition.

POINT U-012: winner V3, confidence 0.70, final severity L, in-scope-of-85 yes

## Section 5. 7.17: V3 concedes and records the in-scope answer

V2's R2-F1 stands. Re-verified verbatim: TL:1272 "it sets `status: RESOLVED`, appends the decision to `### Execution Log`, resets the task `status` to "🟠 Doing", and clears `blocker_reason`"; TL:1274 "confirm that each decision file exists with `needs_human_decision: true`, `status: PENDING` and the empty `Chosen:`, `Decided by:` and `Decision source:` lines ... and that the task is halted (frontmatter `status` and `blocker_reason` set by the HALT rule) before any step 1.2 item runs"; TL:1275 "The facts file is written with no open HALT." Also TL:1143 (the preamble): "Branch 1 (PENDING or empty `Chosen:`) applies the HALT rule ... and STOPS; Branch 2 ... sets `status: RESOLVED` ... and clears `blocker_reason`." So the plan's own preamble has two branches for two states, and 7.17 Verification checks only the first state. That supports HIGH over MEDIUM under the middle rule from round 1 (read literally where the plan has no resume text for the case).

Two additions from this round:
- TL:1268 shows a second resume path in 7.17 that the Verification also ignores: "A resume of this field-name HALT requires the same follow-up work as step 2 of the owner allowlist branch below". That path has a halt too, and TL:1274's PENDING checks are scoped to "the owner allowlist branch", so they do not cover it either. It reinforces that the Verification was written for the first-halt moment only.
- Scope: 7.17 has no row in R1-DM and is not in PC (N-5). A fix needs an owner extension. R2-BR:17 allows "a short additive note ... after the existing R1 note (TL:3010+)", which cannot alter the literal text at TL:1274, so I hold it does not bring the fix inside the 85.

POINT U-007: winner V2, confidence 0.75, final severity H, in-scope-of-85 no
POINT O-001: winner V2, confidence 0.50, final severity M, in-scope-of-85 no (inference; same item, so it needs the same extension)
POINT O-002: winner none, confidence 0.85, final severity L, in-scope-of-85 no (TL:1267 cites DESIGN lines 550/552/971/973; DESIGN:557 and :559 hold the quoted sentences now)

## Section 6. R1-F3 and the other V1 findings

### 6.1 R1-F3 (sha256 baseline shares the fix-log file): move to MEDIUM

I held LOW in round 1 (0.55) because the orchestrator that ran `sha256sum` holds the output. V1 (Medium, "an ordinary Write replaces a file") and V2 ("retain MEDIUM") argue the other way, and the files back them in three places. First, TL:1363 gives the fixer the same path as its output and tells it to "Write a fix log", so a fresh Write is the expected action, not a hostile one. Second, N-5: these are R2's own changed lines, so the defect is new in R2. Third, TL:1210 says a resumed session "does not remember the chat", so the in-context copy of the sums is not a durable control. What keeps it from HIGH: in an unresumed session the check still works from memory, and the fix (a separate file for the sums) is one clause.
MEDIUM matches "real impact with a workaround". The same shared-file pattern is at TL:2614, TL:2642, TL:2705 and TL:2733 (14.x). Those are R1 text, not R2's changes, but R1-DM:100/103/110/113 put them in the 85, so a parity fix is mechanically allowed.

POINT U-003: winner V1, confidence 0.55, final severity M, in-scope-of-85 yes
POINT C-003: winner V1, confidence 0.55, final severity M, in-scope-of-85 yes
POINT X-003: winner V1, confidence 0.60, final severity M, in-scope-of-85 yes (F-07 as specified is met; "fixed with a MEDIUM residual")

### 6.2 R1-F1, R1-F2, R1-F4, R1-F5

These stay LOW; V1 itself downgraded R1-F1, R1-F2 and R1-F5 in round 1, and V2 gave them LOW. Nothing new moves them. For completeness, the text that decides each:
- R1-F1 (7.20 and the R2 section): TL:1293 requires "a dated verbatim quote of the owner's separate execution authorization and the paths of the fresh structural, alignment, qualitative and PRE reports as supplied with it". A "Do not start 7.10" quote (R2-BR:7) fails that. The R2-BR:9 / TL:3020 ambiguity is the root cause and sits outside any plan label.
- R1-F2 (7.10 resume): TL:1210 Branch 1 already says "look first for the `## Execution authorization (verbatim)` section in the result file named in Output, because a resumed session does not remember the chat"; TL:1211 "later content is appended below it, never overwriting it". Branch 2 has no "if it exists" clause. One clause closes it.
- R1-F4 (re-run lists): the lead-in "re-run the item 7.20 commands" in TL:1363 arguably includes the section count, so V2 is right that the weakness is uneven specificity. One `grep -c` closes it.
- R1-F5 (omitted ADD:17 and ADD:19 clauses): see 2.3.

POINT U-001: winner V3, confidence 0.65, final severity L, in-scope-of-85 yes
POINT U-002: winner none, confidence 0.65, final severity L, in-scope-of-85 yes
POINT U-004: winner V1, confidence 0.70, final severity L, in-scope-of-85 yes
POINT U-005: winner V3, confidence 0.65, final severity L, in-scope-of-85 yes

## Section 7. Closed or withdrawn points

- R3-F1 (matrix): closed on disk, as V1, V2 and diff-analysis X-006 agree. My round-1 check read line 7 as `run: 4`. This is a reflect artifact, so it is outside the label list by nature.
- R3-F2 (13.1 provenance): withdrawn as a defect (2.4). 13.1 is an added label (R2-BR:17), so an optional wording tweak would be allowed.
- Diff-analysis U-013 (13.1 equals DESIGN:716): not a defect.

## Section 8. Which defects fall inside what the revision may fix

| Defect | Where | Final | Inside the 85 labels? | Evidence |
|---|---|---|---|---|
| 7.17 Verification and Completion gate vs resumed state; Action step 1 twin | TL:1270-1275 | H (conditional) | no | no 7.17 row in R1-DM; 7.17 absent from PC `changed_by_label`; R2-BR:17 |
| 7.24 lens vs approved allowlist change | TL:1321 | H (conditional) | yes | R1-DM:27; Action line unchanged by R2 (PC 7.24: [1320]); not among F-01 to F-10 (R2-BR:7) |
| sha256 baseline shares the fix-log file | TL:1363, 1391 (and 2614, 2642, 2705, 2733) | M | yes | R1-DM:32, :35, :100, :103, :110, :113; 7.30/7.34 lines changed by R2 (PC) |
| 13.18 and 13.22 lack a DESIGN hash guard | TL:2384, 2412 | L | yes | R1-DM:73, :76; Action lines unchanged by R2 |
| 7.10 resume clause; omitted ADD clauses; 7.20 match target; re-run list | TL:1210, 1293, 1363, 1391 | L | yes | R1-DM:21, :23, :32, :35 |
| 7.17 Context cites stale DESIGN lines | TL:1267, TL:2992 | L | no | 7.17 outside; TL:2992 is the open-question section, not a label |
| 13.1 provenance wording | TL:2265 | none (withdrawn) | yes (13.1 added) | R2-BR:17 |
| coverage matrix | reflect artifact | closed | n.a. | not a plan label |

## Section 9. Final table of POINT lines

Format: `POINT <id>: winner <variant or none>, confidence <0-1>, final severity <H/M/L>, in-scope-of-85 <yes/no/n.a.>`.

Structural and content points
POINT S-001: winner V2, confidence 0.75, final severity H, in-scope-of-85 n.a.
POINT S-002: winner none, confidence 0.60, final severity L, in-scope-of-85 n.a.
POINT S-003: winner V2, confidence 0.70, final severity L, in-scope-of-85 n.a.
POINT S-004: winner V3, confidence 0.65, final severity L, in-scope-of-85 n.a.
POINT S-005: winner V1 on the R1-F3 remedy (a separate sums file), V2 on the 7.17 remedy, confidence 0.55, final severity M, in-scope-of-85 yes (7.17 itself: no)
POINT S-006: winner none, confidence 0.80, final severity L, in-scope-of-85 n.a.
POINT S-007: winner none, confidence 0.80, final severity L, in-scope-of-85 n.a.
POINT C-001: winner V2, confidence 0.75, final severity H, in-scope-of-85 no
POINT C-002: winner V3, confidence 0.65, final severity L, in-scope-of-85 yes
POINT C-003: winner V1, confidence 0.55, final severity M, in-scope-of-85 yes
POINT C-004: winner V3, confidence 0.65, final severity L, in-scope-of-85 yes
POINT C-005: winner V2, confidence 0.80, final severity H, in-scope-of-85 no (7.17 outside; 7.24, 7.30/7.34 and 13.18/13.22 inside)
POINT C-006: winner V2, confidence 0.85, final severity H, in-scope-of-85 n.a. (true for the two H defects and 13.18/13.22; not true for R1-F3, which sits in R2-changed lines)
POINT C-007: winner none, confidence 0.70, final severity L, in-scope-of-85 n.a.

Contradictions
POINT X-001: winner V2, confidence 0.75, final severity H, in-scope-of-85 no
POINT X-002: winner V3, confidence 0.70, final severity L, in-scope-of-85 yes
POINT X-003: winner V1, confidence 0.60, final severity M, in-scope-of-85 yes
POINT X-004: winner V2, confidence 0.85, final severity H, in-scope-of-85 n.a. (the two H defects pre-date R2)
POINT X-005: winner V3, confidence 0.65, final severity L, in-scope-of-85 yes
POINT X-006: winner V3, confidence 0.90, final severity L, in-scope-of-85 n.a.
POINT X-007: winner V3, confidence 0.65, final severity L, in-scope-of-85 yes

Unique contributions
POINT U-001: winner V3, confidence 0.65, final severity L, in-scope-of-85 yes
POINT U-002: winner none, confidence 0.65, final severity L, in-scope-of-85 yes
POINT U-003: winner V1, confidence 0.55, final severity M, in-scope-of-85 yes
POINT U-004: winner V1, confidence 0.70, final severity L, in-scope-of-85 yes
POINT U-005: winner V3, confidence 0.65, final severity L, in-scope-of-85 yes
POINT U-006: winner V1, confidence 0.90, final severity L, in-scope-of-85 n.a. (not a defect; expect 6 is right)
POINT U-007: winner V2, confidence 0.75, final severity H, in-scope-of-85 no
POINT U-008: winner V2, confidence 0.55, final severity H, in-scope-of-85 yes
POINT U-009: winner V2, confidence 0.85, final severity L, in-scope-of-85 n.a. (method, not a defect)
POINT U-010: winner V3, confidence 0.90, final severity L, in-scope-of-85 n.a. (closed)
POINT U-011: winner none, confidence 0.75, final severity L, in-scope-of-85 yes (withdrawn; TL:2265 is true as written)
POINT U-012: winner V3, confidence 0.70, final severity L, in-scope-of-85 yes
POINT U-013: winner V3, confidence 0.75, final severity L, in-scope-of-85 n.a. (not a defect)

Shared assumptions and observations
POINT A-002: winner V2, confidence 0.60, final severity M, in-scope-of-85 n.a. (read literally where the plan has no resume text for the case; careful where it has)
POINT A-004: winner none, confidence 0.50, final severity M, in-scope-of-85 n.a. (the branch is designed (TL:1269) but unquantifiable; keep both H findings labelled conditional)
POINT A-008: winner V3, confidence 0.90, final severity L, in-scope-of-85 n.a.
POINT O-001: winner V2, confidence 0.50, final severity M, in-scope-of-85 no
POINT O-002: winner none, confidence 0.85, final severity L, in-scope-of-85 no
POINT O-003: winner V3, confidence 0.85, final severity L, in-scope-of-85 n.a. (no longer true on disk)

## Section 10. Ranked defect list for the edited plan (V3 advocate, round 2)

1. 7.17 Verification and Completion gate cannot be met by a correct resume (TL:1272 vs 1274-1275); Action step 1 would also rewrite PENDING. HIGH if the branch fires. Outside the 85. Needs an owner extension.
2. 7.24 lens rejects an approved allowlist change and then deadlocks the Decisions gate (TL:1321, 1363, 1384). HIGH if the branch fires and the owner approves; MEDIUM unconditionally. Inside the 85. Fix on TL:1321 only.
3. MEDIUM, inside the 85: the sha256 baseline shares a file with the fix log at 7.30 and 7.34 (R2's own lines) and at 14.25/14.29/14.38/14.42.
4. LOW, inside the 85: 7.30/7.34 re-run lists omit the `## Execution authorization (verbatim)` count; 7.10 has no "section already exists" clause; 7.10 omits the ADD:17 and ADD:19 clauses and rewords the ADD:19 quote; 13.18/13.22 lack a DESIGN hash guard; 7.20 matches a record the executor writes (R2-BR:9 against TL:3020).
5. LOW, outside the 85: stale DESIGN line numbers in 7.17 (TL:1267; also TL:2992).
6. Not defects after checking: R3-F2 (withdrawn), R3-F1 (closed), the matrix `run:` field (gone).

Unchecked by me: 8.19 and 10.5 bodies, the 7.22/7.25 count wording, 7.27-7.29 and 7.31-7.33 beyond TL:1384, and any execution of the plan or the greps. The ordering of the step-2 follow-up against the 7.21-7.28 panel rests on one sentence (TL:1272) and is the main uncertainty under U-008.
