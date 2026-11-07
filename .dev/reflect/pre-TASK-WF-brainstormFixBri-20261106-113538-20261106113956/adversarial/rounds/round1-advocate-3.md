# Round 1 advocate statement: Variant 3 (opus:refactorer card)

Debate: sc:adversarial Mode A, Round 1. Subject: plan `.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/TASK-WF-brainstormFixBri-20261106-113538.md` ("plan") against its brief `source.md` in the same folder. Focus: correctness, coverage, deviation-classification. Citations were re-read in this round unless marked otherwise.

## Position

The plan is ready to run after one P2 fix. That fix is a whole-text acceptance check for the fenced texts of Tasks 1, 2, 3 and 6. V3's form of the fix (R3-2) is the best of the three, with one correction I make below. Everything else on V3's card is P3 or is dropped, and I drop two of my own findings (R3-1, R3-8) on the evidence.

The P2 does not depend on the shared assumption A-001. The brief requires it directly. source.md:34 says: "For each [correction], the task acceptance criteria of the new plan must contain a check equivalent to its verifier." The verifiers of F-1 (source.md:45, "carries the live-check sentence and the companion sentence byte for byte") and F-3 (source.md:71, "Tasks 1-3 carry the applied text byte for byte") are byte-equality checks. No acceptance criterion in plan:43-47, :59-62, :74-77 or :142-145 is equivalent to them; every one is a substring pin or a diff shape. This is a coverage gap against an explicit brief rule, so P2 holds even if `/sc:implement`'s QA reviewer would notice a paraphrase (E-3).

## Steelman of V1 (sonnet:analyzer)

V1 is the only card that tests whether the amended sentence is *correct as a check*, not only whether the plan copies it. That matters because plan:133 carries the brief's claim "no known false FAIL on a correct run" (source.md:239), and a reviewer should test that claim. V1 finds two real paths that challenge it:
- R1-F6 is grounded better than the card itself shows. The archived lc10 result says, "Step 5 condition 2 also covers the nested calls" (`.dev/tasks/done/TASK-WF-p1LivePlanBrief-20261105-164506/artifacts/lc10-result.md:13`). Spec step 5 condition 2 requires "the Skill or command call is a top-level message, not a subagent message" (spec:296). The amended sentence explicitly accepts an analyze `Skill` call "in one of its subagent files" (plan:128). Under the lc10 reading, the same correct run passes the step-4 extra and fails condition 2. That is a known false-FAIL path the plan does not mention.
- R1-F3(b): `/sc:analyze` prints its refusal "in chat only" (`src/superclaude/commands/analyze.md:97`), so the "did not refuse that directory" clause has no recorded marker. A checker that misses the refusal requires a folder that was never written.
- R1-F2 ("only when" gives a necessary condition, not a sufficient one) is a true reading of plan:128.
V1 also has the cleanest honesty section: an explicit `unverified` list (V1:151-153).

## Steelman of V2 (haiku:qa)

V2 is the only card that does the deviation-classification job the focus asks for. It holds each of the 17 printed Verifiers against the plan text, one row each (V2:150-167), and checks Part 4 and Part 5 separately (V2:169-185). Two of its findings follow from that method and are correct on the text:
- R2-05: Part 4 is headed "copy exactly, do not paraphrase" (source.md:213), and the residual risks are part of Part 4 (source.md:237). I compared plan:134-138 with source.md:240-244. Risks 3 and 5 match. Risks 1, 2 and 4 are reworded: "Related: INV-022" is dropped, "(spec:62)" and "(spec:302 says only ...)" become prose, "INFERRED" becomes "inferred", and "spec:300 then blocks" becomes "the spec then blocks". The plan records no deviation for this.
- R2-03: F-12's verifier (source.md:161, "Every pin added under F-3 contains `no nested directory and no nested contract`") cannot pass alongside F-3, which requires the separate ``only by a `/sc:analyze` call`` pin (source.md:63). This is a contradiction inside the brief, and a literal per-verifier audit is the only way to surface it.
V2's verifier table is the artifact a later QA gate can use as it stands.

## Strengths claimed (V3)

1. **The best mechanism for the P2 (C-001, X-002).** R3-2 covers all four fenced-text tasks (V1 covers Task 6 only). It gives a runnable check (`grep -cF -f <saved text> <file>`, and `grep -cxF` printing 2 for the Task 2 bullet), where V2 says only "compare exactly". A fixed-string pattern read from a file also avoids shell quoting of the backticks and double quotes in plan:128. It also resolves the F-7 conflict correctly. F-7's "exactly these pins" (source.md:111) governs the pin list. The byte check is required separately by source.md:34 together with the F-1 and F-3 verifiers, so it is mandated and is not an extra pin.
2. **Structural consistency findings that no other card made** (U-007, U-008, U-009):
   - R3-3: Tasks 1, 2 and 6 each have a `git diff --stat` shape criterion (plan:46, :61, :145); Task 3 has none (plan:74-77). `_unattended_section` reads the whole `## Unattended mode` section (`tests/skills/test_worker_contract.py:483-491`), so text placed on a new line after the bullet still passes every Task 3 and Task 5 check.
   - R3-4: Task 4 guards its `git show HEAD:` greps with `git cat-file -e` (plan:95); Task 5's identical check has none (plan:111). With a wrong path, `git show` fails, `grep -c` prints 0 and the check passes on nothing. This is a vacuous check, the same class the brief's F-4 fixed.
   - R3-7: plan:153 says "it writes only the logs under `./artifacts/`" and, two clauses later, "the one non-log file it writes there".
3. **The checked_clean list is specific and re-checkable.** For example, `_remove` uses `text.replace(tok, '')` on every occurrence (`test_worker_contract.py:530-531`), so "before-count plus 2" holds (V3:135). I re-checked this citation in this round.

## Weaknesses identified in V1 and V2

**V1**
- R1-F1 covers Task 6 only. Tasks 1-3 carry the same "copied character for character" instruction (plan:35, :66) and the same byte-for-byte verifier (source.md:71) with no whole-text check. V1's own checked_clean compares those texts by eye (V1:146), which is the kind of check the finding says is missing.
- R1-F7 is void on the spec text. Risk 4 is already conditioned on "when it is missing or ambiguous" (plan:137). In that case spec:300 says "Step 5 is then not passed, the live check is not recorded as passed ... the phase is not reported PASS until the owner accepts the gap in writing". The same session file drives both clauses, so risk 4's claim is true for the case it names. Narrowing it would also move the plan further from Part 4's copy-exact rule.
- R1-F5 (lint baseline) is weakened by E-2: `make lint` exits 0 today.
- R1-F4 is not violated today (E-1). It is still a sound guard against drift before the run.

**V2**
- R2-01 has the right scope but no mechanism, and its verifier is marked `[INFERRED]` (V2:27). An executor cannot run "compare exactly" as written.
- R2-02 proposes removing a negative pin (plan:144: does not contain ``a `Skill`, `Agent` or `Task` tool call``). That pin is the only mechanical guard against the M-01 defect that the owner amendment fixed (source.md:215, plan:20). Removing it to satisfy a literal "exactly" would delete the most valuable regression check in Task 6. The right classification is an unrecorded deviation that helps: record it, keep it.
- R2-04's suggested fix makes things worse. The negative criterion at plan:45 ("does not contain 'only for a nested command that ran'") is the mechanical enforcement of F-14's intent. Rewording it to avoid the literal would remove the check to satisfy the verifier's wording. F-14's verifier is about the applied text (source.md:179-181), and that text is clean.
- R2-03 and R2-06 are rated P2 but are not plan defects. R2-03 is a contradiction inside the brief; the plan does the right thing (it keeps both pins). R2-06 is about the review's own coverage matrix, a review artifact, not about the plan.
- R2-05 (copy verbatim) is correct, but V2 did not test whether risk 4's text is true. It is (see the R1-F7 point above), so the verbatim copy is safe. V2 did not show that.
- V2's checked_clean row "the approved timeout, refusal, tool-error and not-verifiable qualifications are retained" (V2:189) checks that the clauses are present, not that they can be tested. It misses V1's refusal-marker and condition-2 paths (X-003).

## Concessions

- **R3-1 is void (E-1).** `git status --porcelain -- .dev/tasks` shows no `??` line outside this package and no `AM` line. The two earlier brainstorm packages are already staged. I drop it.
- **R3-8 is wrong on the spec text.** I said nothing routes a not-verifiable step-4 extra to written owner acceptance. spec:300 makes step 5 "not passed" and blocks the phase PASS until the owner accepts in writing, whenever the session file is missing, ambiguous, unreadable or holds no tool calls. Risk 4 names exactly those cases, and the extra's own text says "never PASS". Risk 4 is accurate. I drop R3-8 and side with V2 on X-001: copy the risk verbatim.
- **R3-5 is mostly hypothetical (E-2).** Lint passes today. Only the exit-code point remains: the logs record no exit status, yet plan:156-157 asks them to "show ... exiting 0". It stays P3, narrowed to "append `exit=<status>` to each log".
- **R3-6 is not violated today (E-1).** It stays a P3 guard, merged with R1-F4.
- **R3-2 has a self-reference flaw.** If the executor types the fenced text into `./artifacts/t6-*.txt` itself, a paraphrase can go into both the artifact and the spec, and `grep -cF -f` still prints 1. The reference text must come from the brief, not from the executor. The corrected form: extract the reference mechanically from `./source.md` (line 219 is exactly the live-check sentence and line 223 exactly the companion sentence; for Tasks 1-3, the quoted span inside source.md:231-233), then run `grep -cF -f` against the edited file.
- **V3 did not probe the sentence's behaviour as a check** (X-003). V1 did, and V1 is right there.
- **V3 missed C-005 (the paraphrased risks), C-002 and C-003.** These were found by V2's per-verifier method, which V3 lacked (S-001).
- I did not re-run a byte comparison of plan:38/:54/:69/:122/:128 against source.md in this round. V1 and V3 both report a match by side-by-side reading.

## Per-point positions

| Point | Superior | Reason |
|---|---|---|
| S-001 | V2 | A per-verifier table is the direct deviation-classification output, and it alone found C-002, C-003, C-004 and C-005. |
| S-002 | V1 | An explicit `unverified` list shows what is unproven; V2 and V3 bury it. |
| C-001 | V3 (with the source-extraction correction) | Full scope (Tasks 1-3 and 6), a runnable fixed-string mechanism, and grounded in source.md:34 together with the F-1 and F-3 verifiers, not only in A-001. |
| C-002 | V1 | Keep the negative pin (it guards the M-01 regression) and record it as a deviation; V2's removal loses the best check. |
| C-003 | V2 | A real literal contradiction (source.md:161 vs :63), but it belongs to the brief, so an owner note at P3, not P2. |
| C-004 | V2 (detection only) | Literally true, but the proposed fix removes F-14's enforcement; no plan change. |
| C-005 | V2 | Risks 1, 2 and 4 are paraphrased (checked plan:134-138 against source.md:240-244), against Part 4's copy-exact rule. |
| C-006 | V2 | The only card that noticed it, but it concerns the review artifact, not the plan. |
| C-007 | V1 | A true reading of "only when"; owner-only wording. |
| C-008 | V1 | analyze.md:97 confirms the refusal is chat-only with no marker. |
| C-009 | all equal (V1, V3) | The same guard; not violated today (E-1). |
| C-010 | V3 | Adds exit-code recording; E-2 voids the baseline half for both V1 and V3. |
| C-011 | V1 | Grounded by lc10-result.md:13 ("condition 2 also covers the nested calls") against spec:296 and plan:128. |
| C-012 | V2 | spec:300 makes risk 4 true for the cases it names; V1 and V3 are wrong. |
| C-013 | none (V1 and V2 right to stay silent) | R3-1 is void per E-1. |
| C-014 | V3 | Task 3 is the only wording task without a diff-shape criterion (plan:74-77). |
| C-015 | V3 | plan:111 lacks the `git cat-file -e` guard that plan:95 has; without it the check can pass on nothing. |
| C-016 | V3 | plan:153 contradicts itself; minor. |
| X-001 | V2 | Copy risk 4 verbatim: the plan may not narrow Part 4 text on its own, and the text is accurate under spec:300. |
| X-002 | V3 | The byte check is required by source.md:34 together with the F-1 and F-3 verifiers, so it does not compete with F-7's pin list. |
| X-003 | V1 | Condition 2 (lc10-result.md:13, spec:296) and the chat-only refusal (analyze.md:97) are known false-FAIL paths that plan:133 denies. |

## A-001 response: QUALIFY

As stated ("QA checks only the acceptance criteria"), A-001 is contradicted by E-3. The `/sc:implement` reviewer receives the task text (`~/.claude/skills/sc-implement-protocol/refs/qa.md:9`) and compares the diff to "explicit instructions on the task" (qa.md:17), and "Missing" includes "AC/instruction not in the diff" (qa.md:21). So a paraphrase *may* be caught.

C-001 stays P2 for two reasons that do not depend on A-001:
1. The brief requires an acceptance check equivalent to each verifier (source.md:34), and the F-1 and F-3 verifiers are byte-for-byte checks (source.md:45, :71). The missing criterion is a coverage gap against the brief, whoever reviews.
2. qa.md:21 records "Missing" only "with a confirmed B1 or B2 finding". An LLM reviewer reading a 1,000-character sentence by eye is not a byte check. A dropped pair of backticks, or a dropped clause such as "(not a `Task` or `Agent` call whose prompt only names `/sc:analyze`)", can pass review. A one-line `grep -cF` costs nothing and removes the doubt.

## Priority table

| Card | Finding | Recommended | Note |
|---|---|---|---|
| V1 | R1-F1 | P2 (merge) | Merge into one fix with R2-01 and R3-2; extend to Tasks 1-3. |
| V1 | R1-F2 | P3 owner note | Owner wording; the plan copies the text byte for byte. |
| V1 | R1-F3 | P3 | Add a residual-risk line for the chat-only refusal and the literal `--report-dir` match; the sentence is unchanged. |
| V1 | R1-F4 | P3 (merge with R3-6) | Six-file clean check in Task 1; not violated today (E-1). |
| V1 | R1-F5 | P3 (merge with R3-5, narrowed) | Baseline half moot under E-2; keep the rule for findings outside the six files. |
| V1 | R1-F6 | P3 owner note, top of the owner list | A known false-FAIL path that contradicts plan:133; record it as an owner item, no spec edit. |
| V1 | R1-F7 | drop | Risk 4 is already conditioned and is true under spec:300. |
| V2 | R2-01 | P2 (merge) | Same fix as R3-2, with the mechanism and source extraction from R3-2. |
| V2 | R2-02 | P3 | Keep the negative pin; record it as a deviation next to the F-7 note at plan:131. |
| V2 | R2-03 | P3 owner note | The contradiction is in the brief; the plan is right to keep both pins. |
| V2 | R2-04 | drop | Verifier wording only; the proposed fix would remove F-14's enforcement. |
| V2 | R2-05 | P3 | Copy risks 1, 2 and 4 verbatim from source.md:240, :241 and :243. |
| V2 | R2-06 | P3 (review process, not the plan) | Fix it in the review's coverage matrix; no plan change. |
| V3 | R3-1 | drop | Void per E-1. |
| V3 | R3-2 | P2 | Corrected: reference text extracted from `./source.md`, not typed by the executor. |
| V3 | R3-3 | P3 | Add a `git diff --stat` criterion to Task 3. |
| V3 | R3-4 | P3 | Add the `git cat-file -e` guard to Task 5, and narrow "the pins fail" or add the second pin to the HEAD grep. |
| V3 | R3-5 | P3 (narrowed) | Only "append `exit=<status>` to each log"; the baseline half is dropped per E-2. |
| V3 | R3-6 | P3 (merge with R1-F4) | Not violated today; a cheap guard. |
| V3 | R3-7 | P3 (optional) | Reword the sentence after F-13's text; keep F-13's text verbatim. |
| V3 | R3-8 | drop | Conceded: spec:300 covers risk 4's cases. |
