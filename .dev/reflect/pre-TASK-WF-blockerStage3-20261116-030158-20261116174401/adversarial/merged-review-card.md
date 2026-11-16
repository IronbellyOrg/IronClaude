<!-- Merged review card. Base variant: variant-2-original.md (reviewer-2, qa persona, opus class). Merge date: 2026-11-16. Non-base sources incorporated: variant-1-original.md (reviewer-1, haiku class) and invariant-probe.md (fault-finder). -->
<!-- Aliases: PLAN = .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md; SRC = .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/source.md; S0 = .dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044/TASK-WF-blockerStage0-20261116-021044.md; S1 = .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md; S2 = .dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md; SPEC = .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md; README = .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/stage-requests/README.md. All other paths are repo-relative. -->

## Verdict

NEEDS-REVISION: 3 blocking findings (F1 to F3) and 13 non-blocking (F4 to F16). The revision fixed the first review's findings F1, F2, F4, F5, F6 and most of F7 and F3, but the Task 5 gate runs after the edit it protects (F1), the Task 3 recall lines have no controlling variant or threshold on a reduced panel (F2), and two instruction lines in each QA agent still contradict the new rule (F3). Debate: 8 of 9 diff points agreed after Round 2; the one open point (the gate order) was settled by evidence for the blocking reading; the two HIGH items of the invariant probe (INV-001, INV-003) are F1 and F2.

## First-review findings

- First F1 (entry checks before any spawn): fixed. Task 1 spawns no agent and edits nothing outside `./artifacts/` (PLAN:37).
- First F2 (old-rule confound through the hook): fixed in text; residue in F4. PLAN:78 names the hook confound.
- First F3 (gate outcomes): partly fixed. Outcome words and the hash-bound ruling exist (PLAN:82, PLAN:94); the controlling variant and the reduced-panel threshold are missing (F2).
- First F4 (release, refresh, install steps): fixed (PLAN:232).
- First F5 (registry drift check): fixed (PLAN:129, PLAN:134, PLAN:195).
- First F6 (revert triggers): fixed (PLAN:231).
- First F7 (baselines): fixed for M1, M12 and M10b; residue in F9.

## Findings

<!-- Source: base: none (new from reviewer-1 F1, upgraded to the first finding by the debate); incorporated: reviewer-1 F1; debate X-001, U-001, A-003; probe INV-001, INV-002, INV-011 -->
F1 | severity MAJOR | blocking true | unpassable-check | The seeded-recall gate that protects the live-rule edit is checked after the edit. Task 5 edits `pragmatic.md` and sets the registry row (PLAN:125); the gate is its first acceptance line (PLAN:128). `/sc:implement` runs Q1 EXEC (the edit) before Q3 REVIEW (the acceptance check) (SKILL.md:131, SKILL.md:140). When a line is not PASS and no ruling is recorded, the one fix pass has no legal fix because PLAN:21 forbids editing the result file or the ledger (SKILL.md:145), and every halt exit leaves the edit in the working tree (retry.md:109, retry.md:158). So the source request's "the rule switch cannot start unless the first tasks pass" (SRC:11) and PLAN:20 hold only for Tasks 6 to 13. A `/sc:implement` Ruling can also complete Task 5 with the edit kept on any clear user confirmation (qa.md:248, qa.md:254), without the line id, date and SHA-256 that PLAN:94 requires; PLAN:21's "counts only as Task 3 defines it" does not bind that path. Task 3 reads the old arm "at run time" from the live file (PLAN:76), so a re-run after such a halt reads the edited file as the old arm. Blast radius: an uncommitted source file; the installed style does not change until the refresh, so nothing ships; the harm is a switched tree and an ungated ruling path. Debate: Variant 1's advocate withdrew this in Round 2 (PLAN:20 and the constraints read at SKILL.md:129); Variant 2's advocate and the fault-finder rejected the retreat. Fix: Task 5's body starts by reading the result file, its SHA-256 and the ruling and stops before any edit when the gate fails; keep the acceptance line; state that only the PLAN:94 ruling counts; freeze the old-arm block in Task 3 as a recorded copy with its SHA-256. | citations:
- PLAN:20 "no later task starts unless Task 1 and the seeded-recall gate of Task 5 pass"
- PLAN:21 "Gates are read, never edited."
- PLAN:76 "The old arm holds today's rule text"
- PLAN:94 "A line that is not PASS lets Task 5 proceed only when the stage ledger row in PF holds an owner ruling"
- PLAN:125 "Edit `src/superclaude/output-styles/pragmatic.md`: replace the three definition bullets"
- PLAN:128 "exists and each of R1, R1b, R2a, R2b and R3 reads PASS"
- SRC:11 "so the rule switch cannot start unless the first tasks pass"
- src/superclaude/skills/sc-implement-protocol/SKILL.md:131 "Q1 EXEC    Implement only that task."
- src/superclaude/skills/sc-implement-protocol/SKILL.md:140 "Q3 REVIEW  Load refs/qa.md."
- src/superclaude/skills/sc-implement-protocol/SKILL.md:145 "exactly one fix pass"
- src/superclaude/skills/sc-implement-protocol/refs/retry.md:109 "Every halt in procedure steps 3-5 leaves failed attempt k in the worktree; nothing has been reverted."
- src/superclaude/skills/sc-implement-protocol/refs/retry.md:158 "the A5 tree stays for the operator"
- src/superclaude/skills/sc-implement-protocol/refs/qa.md:248 "clear user confirmation of the explained scoped acceptance"
- src/superclaude/skills/sc-implement-protocol/refs/qa.md:254 "A clear user confirmation in the current conversation is sufficient"

<!-- Source: base: none (new from reviewer-1 F3); incorporated: reviewer-1 F3; debate U-002; probe INV-003 -->
F2 | severity MAJOR | blocking true | unpassable-check | Task 3 gives two recall variants but one outcome word per line, no controlling variant, and no threshold for a reduced panel. PLAN:78 requires the recall lines "both with and without" the grades of a new-arm reviewer who quoted the old rule; PLAN:80 defines a found defect as one reported by at least 2 of the 3 reviewers; PLAN:82 allows exactly one outcome word per line; PLAN:128 turns that word into the Task 5 gate. With one reviewer dropped the rule becomes 2 of 2, stricter than the old arm's 2 of 3; with two dropped it cannot be met, so recall is 0 and R1b fails by construction. A contaminated PASS and a clean FAIL can reach Task 5 with no rule saying which decides. Fix: state before dispatch which variant decides each outcome word, the found threshold on a reduced panel (a majority of the remaining valid reviewers, with at least 2 valid reviewers), and a non-PASS outcome that needs a ruling when fewer than 2 valid reviewers remain. | citations:
- PLAN:78 "report the recall lines both with and without that reviewer's grades"
- PLAN:80 "A defect is found when at least 2 of the 3 reviewers report it"
- PLAN:82 "each with exactly one outcome word"
- PLAN:128 "exists and each of R1, R1b, R2a, R2b and R3 reads PASS"

<!-- Source: base: reviewer-2 F1 (widened); incorporated: reviewer-1 F2; debate C-001, A-002; probe INV-008 -->
F3 | severity MAJOR | blocking true | contradiction | Both QA agents keep instruction lines that contradict the new digest and that no task edits. Rule 8 reads "an unverified or 'probably fine' claim is blocking" in `rf-qa.md` and `rf-qa-qualitative.md`, while the digest makes an unverified claim blocking only under a named condition (an unverified safety claim stays open) and says everything else never blocks. Rule 9 ("When in doubt, fail it and explain why.") sits at `rf-qa.md:548` and `rf-qa-qualitative.md:993`; SPEC:853 assigns line 548 (and 494) to stage 3. None of these is in the Task 6 or Task 7 edit lists, and the frozen patterns of S0:34 match none of them. Debate: Variant 1's advocate argued that SPEC:201 and SPEC:211 keep the reviewer's label for an unknown consumer; Variant 2's advocate answered that those lines cover only a consumer-unknown row, not a doubt about any finding. The line `rf-qa-qualitative.md:810` was dropped (it counts issues, and :805 limits FAIL to an open blocking finding); `rf-qa-qualitative.md:796` ("For each blocking (CRITICAL or IMPORTANT) issue") is label shorthand and a minor remark. Consequence: the pilot agents ship the digest next to instructions that block on doubt, so M12 can stay flat for the wrong reason; rule 9 of the qualitative agent lies inside the `## Critical Rules` block whose hash Task 11 re-pins. Fix: add rules 8 and 9 of both agents to Tasks 6 and 7 with a `grep -c` acceptance line each, keeping the safety exception. | citations:
- src/superclaude/agents/rf-qa.md:100 "an unverified or 'probably fine' claim is blocking"
- src/superclaude/agents/rf-qa-qualitative.md:99 "an unverified or 'probably fine' claim is blocking"
- src/superclaude/agents/rf-qa.md:548 "When in doubt, fail it and explain why."
- src/superclaude/agents/rf-qa-qualitative.md:993 "When in doubt, fail it and explain why."
- src/superclaude/agents/rf-qa-qualitative.md:796 "For each blocking (CRITICAL or IMPORTANT) issue flagged in the previous report:"
- SPEC:199 "An unverified safety claim stays open for verification; it is not a Note."
- SPEC:203 "Everything else is recorded and never blocks, never starts a fix pass and never appears in a reviser brief."
- SPEC:853 "and 494, 548 [E: plan review]"
- S0:34 "`= FAIL`, `that's a FAIL`"
- PLAN:140 "take the more severe rating for shared items"
- PLAN:154 "the eight verdict pairs that fail a review on"

<!-- Source: base: reviewer-2 F3; debate U-004 (qualified by the hook, PLAN:78) -->
F4 | severity MINOR | blocking false | other | The two arms of the seeded test differ in scope, and the text Task 5 ships is in neither. The old arm is the block of `pragmatic.md` from line 221 to the spec-panel bullet; the new arm is the digest alone; PLAN:76 says only the rule text differs. Qualification from the debate: the hook injects the installed old style into every subagent (PLAN:78), so both arms hold the old brief bullets anyway and the loss of the defect-hunt brief is not established. What remains true: the REQ-04 reviewer-brief change and the once-per-run Medium wording that Task 5 ships are in neither arm. Fix: state the asymmetry in the result file, or hold the new arm as the block Task 5 will leave and record its SHA-256. | citations:
- PLAN:76 "from the \"Every review agent MUST review as an independent reader\" bullet to the spec-panel scale bullet"
- PLAN:78 "Every subagent receives the installed"
- PLAN:125 "Edit `src/superclaude/output-styles/pragmatic.md`: replace the three definition bullets"
- src/superclaude/output-styles/pragmatic.md:221 "never to meet a quota"
- SPEC:214 "**[REQ-04]** The reviewer brief at `pragmatic.md:221`"

<!-- Source: base: reviewer-2 F2; debate U-005 -->
F5 | severity MINOR | blocking false | unpassable-check | Task 6's acceptance line on the fixed FAIL triggers checks only the lines of the stage 0 frozen inventory. The Task 6 body names those triggers by text (the spec gives their `rf-qa.md` lines as 170, 327, 389 and 476), but the frozen patterns (`= FAIL`, `that's a FAIL`, ...) miss "= overall FAIL", so a skipped rewrite of a named trigger passes the check. Task 7's first acceptance line greps only the eight "Any CRITICAL or IMPORTANT issue exists" verdict pairs (PLAN:157); the other frozen hits of the qualitative agent (for example the "= FAIL" examples) have no check. Fix: a `grep -c` acceptance line for each named trigger of Task 6, and an every-inventory-line check for Task 7. | citations:
- PLAN:144 "Every FAIL-trigger line in the stage 0 frozen inventory for `rf-qa.md`"
- PLAN:140 "take the more severe rating for shared items"
- S0:34 "`= FAIL`, `that's a FAIL`"
- src/superclaude/agents/rf-qa.md:170 "Any CRITICAL or IMPORTANT gap = overall FAIL"
- src/superclaude/agents/rf-qa-qualitative.md:184 "\"System should be fast\" = FAIL"

<!-- Source: base: reviewer-2 F4; debate U-006 -->
F6 | severity MINOR | blocking false | other | Task 5 rewrites the reviewer-brief bullet that holds a pinned sentence and does not run the pin. `pragmatic.md:221` holds "never to meet a quota"; `tests/skills/test_review_prompt_overrides.py:244` asserts it; Task 5 asks only that reviewers hunt for defects and name their consequence and lists a narrower test run, so a dropped sentence is caught late in Task 10, which does not own `pragmatic.md`. Fix: name the sentence as kept in Task 5 and run that test there. | citations:
- src/superclaude/output-styles/pragmatic.md:221 "never to meet a quota"
- tests/skills/test_review_prompt_overrides.py:244 `assert "never to meet a quota" in flat`
- PLAN:134 "uv run pytest tests/skills/test_review_severity_registry.py tests/skills/test_review_brief_rests_on.py -v"
- PLAN:192 "must still pass unchanged"

<!-- Source: base: reviewer-2 F5; debate U-007 -->
F7 | severity MINOR | blocking false | other | Task 1 compares the digest section of `refs/rule.md` with "the REQ-01 block of the spec once whitespace is collapsed", but the spec block is a blockquote with `> ` markers and the fence lines surround it; neither Task 1 nor Task 5 says which bytes the SHA-256 covers. Task 1 can FAIL for no real reason and halt the run, and no checked file may be edited to clear it. Fix: say "after removing the leading `> ` markers" and define the hashed bytes once. | citations:
- PLAN:43 "equals the REQ-01 block of the spec (spec section 4.1) once whitespace is collapsed"
- SPEC:195 "> Grade each finding by what changes if the flawed text is corrected."

<!-- Source: base: reviewer-2 F6; debate U-008 -->
F8 | severity MINOR | blocking false | missing-requirement | The L5 rule that Medium and Note findings are never rechecked loses its place in the output style. SPEC:274 maps it to `pragmatic.md:226`, whose text reads "Minor findings are not rechecked in later rounds"; Task 5 replaces that bullet with the digest, and the digest has no recheck sentence. The two pilot agents keep the rule in their own fix-cycle text, so the M1 and M12 gates are unaffected; other reviewers that rely on the style lose it. Fix: keep the sentence after the pointer line, or record that the spec drops it. | citations:
- SPEC:274 "Medium and Note findings are never rechecked."
- src/superclaude/output-styles/pragmatic.md:226 "Minor findings are not rechecked in later rounds"
- src/superclaude/agents/rf-qa.md:393 "Do not recheck minor findings from the previous report"
- src/superclaude/agents/rf-qa-qualitative.md:800 "Do not recheck minor findings from the previous report"

<!-- Source: base: reviewer-2 F7 (end-point claim of reviewer-2 F9 dropped); debate C-003, U-009; probe INV-005 -->
F9 | severity MINOR | blocking false | missing-requirement | Task 13 would tell the owner that no baseline exists for metrics that have one. PLAN:230 asks each of M1, M4, M5, M6, M9, M10b, M11 and M12 for "its baseline from Task 2 or the statement that none exists", but Task 2 counts only M1, M12 and M10b. The M6 baseline (the share of `consumer-unknown` rows) is a stage 2 number the recount prints (S2:138) and RT7's threshold is "a placeholder to set from stage 2"; the M9 and M11 baselines are in the spec; M5's is Task 3. Fix: Task 13 (or Task 2) copies M6 from `./artifacts/shadow-recount.md`, M9 and M11 from the spec, M5 from Task 3. | citations:
- PLAN:230 "each with its baseline from Task 2 or the statement that none exists"
- S2:138 "the share of rows tagged `consumer-unknown` among non-blocking rows"
- SPEC:970 "Gate 1 of run 2: 2 findings in 1 fix pass"
- SPEC:973 "run 2 Gate 1: the second cycle was forced by the fix-induced NEW-1 and NEW-2"

<!-- Source: base: reviewer-2 F8 and the hash-description part of reviewer-2 F9 (end-point claim dropped); debate X-002, U-010; probe INV-008 -->
F10 | severity MINOR | blocking false | other | Task 11 leaves audit pins unaligned with the rewritten QA text. The zero-trust test keeps `BLOCKING_SEVERITIES = frozenset({"CRITICAL", "IMPORTANT"})`, which drives the scorer that Task 11 does not touch (it re-pins only the bullet strings), so the suite passes while asserting that the label is the grade. PLAN:203 says the hash re-pin includes "the rewritten verdict pairs", but those pairs (lines 240 to 784) lie outside the `## Critical Rules` block that starts at line 983. The floor test rejects "typically" among its softening tokens, which an OD16 option (b) Rule 6 wording may use. Fix: update or label the scorer as a legacy fixture, correct the description, and state the Rule 6 wording constraint. | citations:
- tests/audit/test_nfr_conv_9_zero_trust.py:95 `BLOCKING_SEVERITIES = frozenset({"CRITICAL", "IMPORTANT"})`
- PLAN:203 "including the rewritten verdict pairs"
- src/superclaude/agents/rf-qa-qualitative.md:983 "## Critical Rules"
- tests/audit/test_severity_floor_unweakened.py:197 "SOFTENING_TOKENS = ["

<!-- Source: base: none (new from reviewer-1 F4); incorporated: reviewer-1 F4; debate U-003 -->
F11 | severity MINOR | blocking false | contradiction | Task 12 still describes a plugin mirror that revision 2 forbids. PLAN:214 says the stage 4 package "adds the plugin mirror of `refs/rule.md` to the allow-list and the registry before it copies the skill folder"; the shared decisions say "Do not create any new plugin surface". The stage 3 scan is unaffected. Fix: delete that clause and keep the stage 4 removal of the six file exemptions. | citations:
- PLAN:214 "adds the plugin mirror of `refs/rule.md` to the allow-list and the registry before it copies the skill folder"
- .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/stage-requests/revision2-brief.md:16 "Do not create any new plugin surface"

<!-- Source: base: reviewer-2 F10; debate U-012; probe INV-012 -->
F12 | severity MINOR | blocking false | missing-requirement | Nothing tells the owner to record on the stage 3 ledger row what Tasks 1, 3 and 5 read from it. The ledger has one column "Owner go (date, where)" and the instruction says only "Record the go and the package id in the table below", while Task 1 needs a date, the folder list and the confirmation-file path, and Task 5 needs a ruling with a line id and a SHA-256. Each missing item is a Task 1 FAIL that halts the package. SRC:41 already lists the need as a cross-stage item. Fix: add those fields to the README instructions. | citations:
- README:11 "Record the go and the package id in the table below"
- README:15 "| Stage | Request file | Base tasks (revised plan) | Package id | Owner go (date, where) |"
- SRC:41 "the stage ledger row for stage 3 must name the folders and the confirmation file"
- PLAN:39 "an empty file means none was confirmed after the rows were reviewed"

## Follow-up candidates

<!-- Source: base: none (new from the invariant probe); probe INV-007 -->
F13 | severity MINOR | blocking false | other | The L3 text added beside the cap sentence must follow the sentence, not split it. The cap-edit fixture rows end their `new` strings with "...open blocking findings." and the test fails a row when its `new` string is not in the file; Task 10 allows fixture edits only for digest or cadence rows. | citations:
- tests/skills/test_review_severity_rule.py:256 `if row["old"] in text or row["new"] not in text:`
- tests/skills/fixtures/review_severity_cap_edits.yaml:29 `new: "Maximum 2 fix cycles. After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings."`
- PLAN:196 "The two fixtures change only rows whose new text is the digest or the once-per-run cadence"

<!-- Source: base: none (new from the invariant probe); probe INV-009 -->
F14 | severity MINOR | blocking false | other | Tasks 6 and 7 record kept mechanical gates in `refs/scale-map.md` with no section or row format, while stage 1's acceptance lines require that file to hold no `src/superclaude` path and Task 12 parses one section of it. | citations:
- PLAN:140 "record the keep, with its reason, in `refs/scale-map.md`"
- S1:74 "`grep -n \"src/superclaude\" src/superclaude/skills/sc-review-severity/refs/scale-map.md` prints nothing"

<!-- Source: base: none (new from the invariant probe); probe INV-010 -->
F15 | severity MINOR | blocking false | other | The new fix-cycle text names `superclaude review fixcheck`, but the installed agent runs in other projects whose CLI may lack it; the stage 2 sweep paragraph has a "missing command" clause and the L2 text has none. | citations:
- PLAN:140 "the fix agent runs `superclaude review fixcheck` over the lines it edited"
- S2:72 "a missing `superclaude` command or a non-zero exit is printed as one line and the run continues"

<!-- Source: base: none (new from the invariant probe); probe INV-004 -->
F16 | severity MINOR | blocking false | other | An empty confirmation file and a one-gate baseline are not covered. PLAN:39 says an empty file means none was confirmed, but the stage 2 script prints "not computable" only for a missing file and its test list has no empty-file case; PLAN:62 handles gates with no countable file but not a mean over one gate for the RT5 threshold. | citations:
- PLAN:39 "an empty file means none was confirmed after the rows were reviewed"
- S2:138 "without that file it prints \"not computable: N unreviewed rows carry safety vocabulary\""

## Checked

- Task numbers 1 to 13 are contiguous; every `Depends on` points to a lower task; Task 13 depends on Tasks 1 to 12.
- The producing plans create what Task 1 reads: S0:106 seeded set and planted deliverable, S0:34 inventory freeze, S1:49 rule.md, S1:66 scale-map and allow-list format, S1:223 registry test, S2:138 shadow_summary.py with `--confirmed-misses`.
- The live lines the plan cites hold: pragmatic.md lines 221 to 231, rf-qa.md lines 83, 108 to 111, 152, 162, 168 to 170, 182 to 183, 327, 402, 476, 549, rf-qa-qualitative.md lines 84, 240, 809, 990, 994, hooks.json:173.
- The merge-phrase scan hits only allow-listed files, the two retired lines in skills/task/SKILL.md and the four files Tasks 6 to 8 edit; none under plugins/.
- The Critical Rules slice hash window (from three lines above the header to six below) does not reach Rule 6. The seven review subcommands Task 4 expects exist.
- No commands or tests were run by the reviewers; this is a source-based plan review.

## Self-report

confidence: 0.84
reviewer_model_self_report: merged by the adversarial pipeline; base reviewer-2 (opus class), incorporated reviewer-1 (haiku class) and the fault-finder probe (sonnet class)
