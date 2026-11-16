# Round 2.5 invariant probe (fault-finder) on the emerging consensus B1-B10, N1 — plan TASK-WF-loosenBlockerCla-20261115-133045

Citations: "plan:N" = the plan file, "spec:N" = merged-requirements.md, "plan-input:N" = 09-plan-input.md, all in the folders named in the brief; repo paths are relative to the worktree root. Every citation was Read or Grepped in this session on 2026-11-15. Read, Grep and Glob only; no file other than this one was edited.

ID: INV-001
CATEGORY: sufficiency_challenge
ASSUMPTION: B7's fix (rewrite the 8 label-based FAIL bullets in rf-qa-qualitative.md) removes every "FAIL by label" verdict bullet that sits beside a digest the plan moves to v2.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: `src/superclaude/templates/documents/agent_template_qa.md:158` "- **FAIL** — Any CRITICAL or IMPORTANT issue exists. ... MINOR issues never fail the review." sits 3 lines above the definition at `:161` that Task 34 replaces. Task 34 names only "line 161 definition, line 85 merge rule, line 333 Rule 6 text" for this file (plan:405), and its checks look only for the digest, `more severe rating` and the definition sentence (plan:408-410). Strict T2 at Task 39 scans for the definition sentence only (plan:459). The same Grep finds the bullet nowhere else outside rf-qa-qualitative.md. Falsifying condition for "B7 fix alone resolves it": after Phase 5 the QA-agent template carries the v2 digest ("the label ... is information, never the grade") and a FAIL-on-label bullet together, and every QA agent generated from it inherits the conflict. No later step detects it.

ID: INV-002
CATEGORY: guard_conditions
ASSUMPTION: The final-gate sweep that Task 22 wires in at stage 2 (and that B3's fix would copy into the task skill) is a shadow observer, consistent with "the old definition still decides every gate outcome".
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: plan:250 "a row whose flawed text or figure appears, uncorrected, in a decision-basis section of the final deliverable becomes Blocking at that gate"; plan:261 "The old definition still decides every gate outcome"; spec:946 stage 2 "reviewers emit `rests_on` while the old definition still decides". Medium rows exist under the legacy rule: `src/superclaude/output-styles/pragmatic.md:230` "Among minor findings, one that describes a real but non-blocking weakness ... is Medium. A Medium finding is a warning: it never fails a review". So a live stage-2 sweep at Gate 5 (plan:273) turns a legacy Medium into a FAIL, which contradicts the live legacy rule and the shadow contract. No task says the stage-2 sweep only records. T12 and REQ-22 test only the classifier (plan:192, 197). Falsifying condition for B3: copying Task 22's sweep wording into Task 21 spreads the same authority leak to every /task run.

ID: INV-003
CATEGORY: sufficiency_challenge
ASSUMPTION: Task 30's L3 edit at task/SKILL.md:258 applies L3 (three choices at the cap) wherever the spec puts it.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: spec:272 gives L3's location as "`rf-qa.md:402-415` [E]; `task/SKILL.md:258` [V], `372` [E]". Task 30 edits only "line 258 (Conditional Proceed)" (plan:361), and Task 27 has no L3 step (plan:328: L1, L2 and L6 only). After Task 30, the task skill still holds the plain halt at `src/superclaude/skills/task/SKILL.md:372` "6. **Escalation:** After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings" and at `:409` (fidelity loop), and `src/superclaude/agents/rf-qa.md:402` keeps "HALT and escalate to the user". Task 30's check "The escalation text lists the three choices" (plan:366) passes on line 258 alone. The result is one skill with two different cap behaviours, and no later task notices.

ID: INV-004
CATEGORY: interaction_effects
ASSUMPTION: B9's fix (add a per-run offer to Task 22's tech-research wiring) gives tech-research runs exactly one offer per run.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: tech-research runs inside /task. `src/superclaude/skills/tech-research/SKILL.md:614` "**Execution transfers to /task**", `:616` "/task adds phase-gate QA on top. This results in intentional, acceptable double QA at gate phases", `:621` "/task does NOT read this SKILL.md during execution". Task 21 already makes every /task run end "with one offer per run" (plan:261). Adding a second offer in the tech-research items that get baked into the task file gives two offers in one run, against spec:946 ("the per-run offer"). Both paths also write `qa/follow-ups.md` (plan:265, 276) under the single-writer rule REQ-08 (plan:157). The fix has to be one offer, owned by /task, with Task 22 only checking that it fires. That also places the escalation-halt offer (spec:323) at task/SKILL.md:258, 372 and 409.

ID: INV-005
CATEGORY: interaction_effects
ASSUMPTION: Gate 5 is "the last gate before delivery" for tech-research, so B3's fix (add a sweep to the task skill) plus Task 22's Gate 5 sweep give one correct final sweep.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: plan:250 places GR7 "at the last gate before delivery". In a tech-research run, Gate 5 (`tech-research/SKILL.md:415` "Gate 5: Anti-Omission (Phase 6, after Gate 4)") is followed by /task's phase gate and then its final validation: `task/SKILL.md:290` "After the LAST phase's phase-gate QA passes and BEFORE marking the task 'Done,' run a final validation pass". So Task 22's sweep (plan:273) runs before the final gate. With B3's fix the run gets two sweeps, and only the /task one is final. The fix needs a single sweep at /task's final validation, and Task 22's Gate 5 call removed or made a no-op.

ID: INV-006
CATEGORY: interaction_effects
ASSUMPTION: B2 can be fixed either by registering refs/rule.md as a registry row or by exempting it from T2.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: rule.md carries a v2 fence from Task 7 (plan:101 "between the HTML-comment fence lines `review-severity:digest v2 begin` and `review-severity:digest v2 end`"). Registering it breaks other rules. (a) At `legacy`, Task 18's own check, "With every registry row at `legacy` and every installed carrier legacy, the check reports no mismatch" (plan:230), sees an installed carrier holding v2 under a legacy row. (b) At `v2`, it breaks "all at digest version `legacy`" (plan:150) and spec:945 "registry rows all `legacy`". (c) Either way it breaks "exactly the 11 carriers" (plan:150). Task 39 also copies the folder to `plugins/superclaude/skills/sc-review-severity/` (plan:459), and T2 scans `plugins/` (plan:237), so a second fence-holding file appears. Only an exemption written for both the source and the plugin copy of rule.md fits every check. The consensus leaves the choice open.

ID: INV-007
CATEGORY: sufficiency_challenge
ASSUMPTION: Adding fmea_classifier.py and remediate_parser.py to the Task 33 allow-list (B6) is enough for the T5 scan to pass.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: The new skill files will hold the phrases themselves. Task 7 copies "the guardrails GR1 to GR12 of section 8.1" into rule.md (plan:101), and spec:651 GR5 ends "without re-creating 'highest severity wins'". Task 8 writes "one row per family of spec section 9.3" (plan:113), and spec:746 is the row "`sc-auggie-review-protocol/SKILL.md:228` ('keep the higher severity')". Neither `refs/rule.md` nor `refs/scale-map.md` is on the allow-list ("the scale-map rows ... and the stage 4 files", plan:394, 399). Task 39 then mirrors both into `plugins/` (plan:459), where the scan also runs (plan:394). Task 33's check (plan:397) catches this, but the executor must choose between rewording copied spec text and allow-listing the skill folder on both surfaces. Separately, the code-file hit `remediate_parser.py:365` ("Higher severity wins") matches only a case-insensitive scan, and the plan does not fix the case rule.

ID: INV-008
CATEGORY: interaction_effects
ASSUMPTION: Task 31 can re-pin the cap fixtures by editing only `tests/skills/fixtures/*.yaml`, and Task 30's three-choice escalation does not touch any pinned fixture string.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: The fixtures are pinned in two ways. (a) `tests/skills/test_review_severity_rule.py:275-283` (`test_ej_fixtures_are_byte_copies_of_the_plan_tables`) requires each fixture to be byte-equal to `.dev/review-severity-rule/cap-edits.yaml` or `sweep-edits.yaml`, and both files exist (Glob). Task 31 never names them (plan:372), so any fixture edit fails test_ej. (b) `:252-265` requires every cap row's `new` string to stay in its file. Rows C-107 and C-110 (`review_severity_cap_edits.yaml:893`, `:917`) pin "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings — log all remaining issues" in task/SKILL.md. Task 30 rewrites that line 258 escalation into three choices (plan:361). Task 31 lets fixture rows change only "whose new text is the digest or the once-per-run cadence" (plan:376), so the C-107 row cannot follow the L3 rewrite.

ID: INV-009
CATEGORY: sufficiency_challenge
ASSUMPTION: B4's fix (stop after Phase 1 for the owner's go) is enough because Phase 1 writes "the stage 0 result".
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: Task 5 rewrites the spec so that "steps 0a and 0c are not skipped" (plan:77), but no task runs 0a. Task 2 is 0b and Task 3 is 0c (plan:40, 50), and Grep finds "0a" in the plan only at plan:77. Spec:944 defines 0a as "the scored table and five runs with a fixture or approved judge". The only existing result is a stand-in: plan-input:14 "Five runs with a Claude judge on a text-only variant ... This is not a Jev run", and judge approval (OD3) is left open (plan:21). Stage 1's entry needs "stage 0 result written; owner go" (spec:945), and no task writes that combined result or states 0a's status. An owner stop alone shows the owner a stage 0 with a required step missing, and Task 5 itself made that step required.

ID: INV-010
CATEGORY: sufficiency_challenge
ASSUMPTION: For B5, one deferral sentence about fresh findings fully covers plan-input item 4, because Task 4 already supplies "findings a reviewer called minor that later proved real".
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: plan-input:16 asks for "fresh findings that were not in the 318, plus findings a reviewer called minor that later proved real". Task 4 adds "the stage 0b sample of Task 2 as a separate set of findings that a reviewer called minor" (plan:66): the whole random sample, with no proved-real label. The escape-test hit is not carried into the held-out file (plan:69 lists only the ids and the seed). spec:614 states that the table "cannot show a real blocker a reviewer called minor ... The audit in section 8 supplies those cases", and that audit belongs to the pilot. So the second half is also unproduced, and a deferral that names only fresh findings leaves it wrongly marked as covered.

ID: INV-011
CATEGORY: sufficiency_challenge
ASSUMPTION: For B8, adding per-input row counts to Task 16's output gives the measurement plan-input item 3 needs.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: plan-input:15 asks for M, C and E to run "only when code supplies the required-item list, the constraint lines and the verified evidence, and report how many rows had each", and keeps the M-or-C row off "until a run with those inputs has been measured". No task builds those code suppliers. Task 10 only documents a "Needs from code" column (plan:138). Task 14's judges are `FixtureJudge` (recorded answers) and `ReviewerJudge` (plan:180). Task 16 reads "findings plus a judge answers file" (plan:203). With B8's fix alone, every count prints zero, and the measurement plan-input:15 waits for can never take place inside this plan. The plan must either build the suppliers or record that both the counts and the measurement wait for them.

ID: INV-012
CATEGORY: count_divergence
ASSUMPTION: Task 39's acceptance text agrees with Task 11 on how many installed-only spec-panel variants exist.
STATUS: UNADDRESSED
SEVERITY: LOW
EVIDENCE: plan:464 "the two installed-only spec-panel variants are outside the scan". plan:146 and plan:151 name five (`spec-panel-armb`, `-diffgate`, `-ledger`, `-ponytail`, `-stoprule`), and spec:725 also lists five. A Grep of `~/.claude/commands/sc/spec-panel*.md` finds all five installed, each with one cap or definition hit, while `src/superclaude/commands/` holds only `spec-panel.md` (Glob). This is a wording slip at plan:464, separate from the consensus slips at plan:150 and 399.

ID: INV-013
CATEGORY: state_variables
ASSUMPTION: (N1) Task 30's criterion assumes the task skill holds `CANONICAL_CAP_TEXT` word for word and that the constant pins it there.
STATUS: ADDRESSED (debate-surfaced N1; verified here)
SEVERITY: LOW
EVIDENCE: N1 is confirmed. A Grep of `src/superclaude/skills/task/SKILL.md` for "at most 2 fix cycles|then escalate to the user" finds nothing. The cap sentences are "After 2 fix cycles (3 reviews), HALT" at `:258`, `:372` and `:409`. `tests/skills/test_review_severity_rule.py:228-230` asserts `CANONICAL_CAP_TEXT` against the style file and `canonical_rule_bullets()` only. The task skill's real pin is the at-cap clause through fixture rows C-107, C-110 and C-111 (`:216-218`, `:233-246`), so the corrected Task 30 check should use that clause. This also bears on INV-008.

ID: INV-014
CATEGORY: guard_conditions
ASSUMPTION: The "Depends on" lines state every prerequisite, so a resumed or reordered /sc:implement run cannot start a task before its inputs exist.
STATUS: UNADDRESSED
SEVERITY: LOW
EVIDENCE: I checked every Depends-on line against task order. There is no cycle, and no task depends on a later task. Three prerequisites are missing and are satisfied only because tasks run in plan order. (a) Tasks 21 and 22 call "the classifier ... in shadow mode" (plan:261, 273) but depend only on Tasks 12, 17 and 20 (plan:259, 271), not on Task 14 or 16. (b) Task 26 needs rule.md's digest, the registry row and T1 (Tasks 7, 11, 19) but depends only on Task 25 (plan:314), and Task 25 has no dependency line (plan:303-305). (c) Task 34 has no dependency line at all (plan:403-405). The phase stops at plan:20 make this low risk.

## Checked

- **state_variables:** registry version state across Tasks 11, 26-30, 35 and 39 (plan:146-151, 316-361, 416-419, 459); the legacy Medium class in `pragmatic.md:218-232`; the cap text in `task/SKILL.md:258, 372, 409` (N1 confirmed, INV-013); `CANONICAL_CAP_TEXT` and `canonical_rule_bullets()` (`test_review_severity_rule.py:78-96, 215-230`).
- **guard_conditions:** every Depends-on line for Tasks 1-39 (no cycles; INV-014); stage-2 sweep authority (INV-002); the stage gates at spec:940-948 and plan:20.
- **count_divergence:** at least 8 cited counts and lines spot-checked, and these match the live repo: definition sentence in 11 files and 11 lines (Grep over src and plugins, with no plugin hit); merge-rule phrases on 13 lines in 10 files plus auggie:228, and 5 code lines case-insensitive (fmea_classifier.py:304, 323; remediate_parser.py:55, 301, 365); tasklist 7 lines; `review/__init__.py:19-29` with 9 subcommands; `WORKER-CONTRACT.md:33, 39`; rf-qa.md lines 83, 108, 152, 162, 170, 183, 221, 316, 327, 333, 334, 476, 548; rf-qa-qualitative.md 84, 108, 990 and the 8 FAIL bullets at 240, 291, 362, 429, 500, 567, 746, 784; rf-analyst.md:75; template lines 85, 161, 333, 466, 644, 655, 828; rule-prompt lines 11, 27, 28, 27; stage 4 merge lines (tech-reference 510, 513; readme 542, 547; tdd 122; operational-guide 511); tech-research 415, 490, 519, 555, 562; spec-panel.md 259-261, 372, 455; task-builder 875; rf-task-builder 385-389, 419-420; `test_invariant_preservation_NFR_6_through_10.py:96, 98`; `test_review_rules_text.py:92`; plugin skills 4 entries. Mismatches: plan:464 "two" variants (INV-012); `hooks/hooks.json` is absent at the root, and the source registration is at `src/superclaude/hooks/hooks.json:173` (already in the consensus).
- **collection_boundaries:** T2 and T5 scan the `src/` and `plugins/` trees, including the new skill folder and its plugin mirror (INV-006, INV-007); the `.claude/` and `tests/` trees are outside the scan. `spec-panel.md:332` holds a third `follow-up candidates` outside Task 38's named lines 259-261; Task 38's grep check (plan:452) catches it, so it is not listed. Every named test file exists: test_review_severity_rule, _mapping, test_implement_severity_static, test_review_loop_extension, test_review_prompt_overrides, test_spec_panel_review_loop, test_task_builder_merge, test_worker_contract, test_cli_doctor, test_install_retired_mcp, test_update_command, test_review_cli, test_review_rules_text, and both fixtures. The new test files the plan creates do not exist yet, as expected.
- **interaction_effects:** the B2 fix against Task 11, Task 18 and the Task 39 mirror (INV-006); the B3 and B9 fixes against tech-research running inside /task (INV-004, INV-005); the Task 30 L3 rewrite against the fixtures and test_ej (INV-008); the B7 rewrite against the hash in `test_severity_floor_unweakened.py`, which covers only `## Critical Rules` from line 983, while the 8 bullets sit at lines 240-784, so there is no conflict; `test_dnsp_all_agents_fail_bypass.py` pins rf-team-lead's Fix Cycles rule, not the FAIL bullets, so there is no conflict.
- **sufficiency_challenge:** B1 (falsifier: T1 and Task 18 together, INV-006); B2 (INV-006); B3 (INV-002, INV-005); B4 (INV-009); B5 (INV-010); B6 (INV-007); B7 (INV-001); B8 (INV-011); B9 (INV-004); B10: spec:680 and 987 give a procedure that an executor can run, and I found no further downstream condition beyond what the consensus already states (sizing and building the set), so no entry.



