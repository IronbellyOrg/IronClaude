---
card: reviewer-2
persona: qa
model_class: opus
agent_type: reflect-reviewer
reviewer_agent_id: a8fcf47976cac48d7
persisted_by: orchestrator (the reviewer has no Write tool)
---

## First-review findings

- F1: fixed. Task 1 spawns no agent and edits nothing outside artifacts, recounts the runs and halts on a short count: PLAN:37 "Spawn no agent and edit no file outside `./artifacts/` in this task", PLAN:40, PLAN:45.
- F2: fixed. PLAN:78 names the hook confound, the apply-only-this-text instruction, the lower-bound reading and the reviewers to list. PLAN:76 says the model class and brief are the same in both arms.
- F3: fixed. PLAN:92 defines the outcome words (advisory classes, zero bases), PLAN:94 the hash-bound owner ruling, and PLAN:128 the gate.
- F4: fixed. PLAN:232 covers the release, the refresh, `make doctor` and the `grep -c` on the installed style. PLAN:233 gives the revert path for rows with no registry row.
- F5: fixed. The SHA chain is at PLAN:50, :102 and :129. The `v2` row checks are at PLAN:129, :145 and :159. The registry test runs at PLAN:134, :148, :161 and :195.
- F6: fixed. PLAN:231 judges RT1 (seeded part) and RT3, and marks only the window-dependent triggers as pending.
- F7: fixed for M1, M12 and M10b (PLAN:59-61). New F7 below covers the M6 gap.

## Findings

F1. Blocking: yes. Lines that contradict the new digest stay in both QA agents and are not in any edit list.
Evidence:
- src/superclaude/agents/rf-qa.md:100 "an unverified or 'probably fine' claim is blocking". The same text is at rf-qa-qualitative.md:99.
- rf-qa-qualitative.md:796 "For each blocking (CRITICAL or IMPORTANT) issue flagged in the previous report:"
- rf-qa.md:548 "When in doubt, fail it and explain why."
- The spec lists rf-qa 548 for stage 3: SPEC:853 "and 494, 548 [E: plan review]".
- None of these is named in PLAN:140 or PLAN:154, and the REQ-30 patterns frozen at S0:34 match none of them.
Consequence: rf-qa and rf-qa-qualitative ship the digest next to text that blocks every unverified claim and treats a label as the grade. The digest's precedence sentence does not settle it, because both sit in the same agent's instructions. M12 can then stay flat for the wrong reason.
Fix: add these lines, plus rf-qa-qualitative.md:810 (it counts all issues, not blocking ones), to Tasks 6 and 7, and add a `grep` acceptance line for each.

F2. Blocking: no. Task 6's FAIL-trigger check can pass without the edits it names.
Evidence: PLAN:144 checks only "Every FAIL-trigger line in the stage 0 frozen inventory for `rf-qa.md`". The frozen patterns (S0:34: "`= FAIL`, `that's a FAIL`, ...") miss rf-qa.md:170 "Any CRITICAL or IMPORTANT gap = overall FAIL", :327 "Flag exact duplicates as IMPORTANT." and :389 and :476. Task 7 has no inventory line at all, so frozen hits such as rf-qa-qualitative.md:184 "\"System should be fast\" = FAIL" go unchecked.
Consequence: a skipped rewrite of a named trigger passes Task 6's check.
Fix: add a `grep -c` acceptance line for each named trigger. Give Task 7 an every-inventory-line check.

F3. Blocking: yes. The two arms of the seeded-recall test differ in more than the rule.
Evidence: PLAN:76 "only the rule text differs". The old arm runs from pragmatic.md:221 to :231, which includes the reviewer brief, the zero-finding rule, :224 "Every review agent MUST produce a binary verdict: PASS or FAIL." and the Medium bullet at :230. The new arm is the digest alone. The REQ-04 brief and the once-per-run Medium wording that Task 5 ships are in neither arm.
Consequence: R1 to R3 gate the rule switch, but they measure the loss of the defect-hunt brief and the verdict bullets together with the definition change. They do not test the text that actually ships.
Fix: make the new arm lines 221 to 231 as Task 5 will leave them, and hash that block. If not, state the asymmetry, as stage 0c (S0:69) uses it too.

F4. Blocking: no. Task 5 rewrites a bullet that holds a pinned sentence.
Evidence: pragmatic.md:221 holds "never to meet a quota", and tests/skills/test_review_prompt_overrides.py:244 asserts `"never to meet a quota" in flat`. Task 5's tests (PLAN:134) leave that test out, and PLAN:192 says it "must still pass unchanged".
Consequence: if the rewrite drops the sentence, Task 10 fails and Task 10 does not own pragmatic.md.
Fix: name the sentence as kept in Task 5 and run that test there.

F5. Blocking: no. Task 1's digest comparison does not say how to treat the blockquote formatting.
Evidence: PLAN:43 says "once whitespace is collapsed", but the spec block is a blockquote (SPEC:195 "> Grade each finding by what changes"). Neither Task 1 nor Task 5 says which bytes the SHA covers: raw or collapsed, with or without the fence lines.
Consequence: Task 1 can FAIL for no real reason and halt the run, and no checked file may be edited to clear it.
Fix: say "after removing the leading `> ` markers", and define the hashed bytes once.

F6. Blocking: no. The "never rechecked" rule (L5) disappears from the output style.
Evidence: SPEC:274 "Medium and Note findings are never rechecked" locates it at pragmatic.md:226, where the text reads "Minor findings are not rechecked in later rounds". Task 5 replaces that bullet with the digest, and the digest has no such sentence (SPEC:203).
Consequence: after Task 5, nothing in the output style that reaches every subagent says Medium and Note findings are not rechecked.
Fix: keep that sentence after the pointer line, or record that the spec drops it on purpose.

F7. Blocking: no. Task 13 would tell the owner that no M6 baseline exists when one does.
Evidence: PLAN:230 "each with its baseline from Task 2 or the statement that none exists". Task 2 does not count M6, but the Task 1 recount script prints it (S2:138 "the share of rows tagged `consumer-unknown` among non-blocking rows"). RT7's threshold is "a placeholder to set from stage 2" (SPEC:991).
Consequence: the owner summary would carry a false "none exists".
Fix: Task 2 copies M6 from `./artifacts/shadow-recount.md`.

F8. Blocking: no. A re-pinned audit test keeps grading by label.
Evidence: tests/audit/test_nfr_conv_9_zero_trust.py:95 `BLOCKING_SEVERITIES = frozenset({"CRITICAL", "IMPORTANT"})` drives `_score_rf_qa_verdict`, which tests/audit/test_invariant_preservation_NFR_6_through_10.py imports. Task 11 (PLAN:203) re-pins only the bullet strings.
Consequence: the suite passes while it asserts the label-is-the-grade rule that the reworded bullet removes.
Fix: Task 11 updates the scorer, or labels it as a legacy fixture.

F9. Blocking: no. Missing end points and one wrong description.
Evidence: Task 6 turns test_nfr_conv_9_zero_trust.py and the S1 to S3 pins red, but has no "until Task 10/11" line like PLAN:161 "is red from this task until Task 11". PLAN:203 re-pins the hash "including the rewritten verdict pairs", but those pairs (lines 240 to 784) sit outside `## Critical Rules` (rf-qa-qualitative.md:983).
Fix: add the end points and correct the description.

F10. Blocking: no. Nothing tells the owner to put the folder list and confirmation file on the stage 3 ledger row.
Evidence: README:11 says only "Record the go and the package id in the table below", while SRC:41 says "the stage ledger row for stage 3 must name the folders and the confirmation file".
Consequence: Task 1 halts by construction unless the owner already knows to add them.
Fix: add those two fields to the README instructions.

## Checked and sound

- The live lines the plan cites hold what it says:
  - pragmatic.md:221 to :231
  - rf-qa.md:83, :108 to :111, :152, :162, :168 to :170, :182 to :183, :327, :389, :402, :476, :549
  - rf-qa-qualitative.md:84, :240 and the other seven FAIL bullets, :809, :990, :994
  - hooks.json:173
- The seven `*_cmd.py` modules exist, and every test path in Tasks 4, 9 and 10 exists (stage 2 files aside, as expected).
- The phrase scan has hits only in the allow-listed files, the two lines of task/SKILL.md and the four files being edited. There are none under `plugins/`.
- The Critical Rules slice hash (from the header minus 3 to the header plus 6) does not reach Rule 6.
- The `Depends on` edges and the 13 tasks in 5 phases are consistent.
- The revision2 decisions hold: no edit to task or task-builder, no plugin surface beyond the pinned twins, `refs/qa.md` untouched.
- The coverage matrix rows are covered. INF-019 is mapped to Task 4 but is really covered by PLAN:219.
- Every file listed in the brief was readable.

## Self-report

confidence: 0.80
