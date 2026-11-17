# Round 2 rebuttal: Advocate for Variant 3 (reviewer 3, refactorer, opus class)

- Round 2, third and last advocate. Responds to all Round 1 statements and to the Round 2 statements of Advocates 1 and 2.
- Keys: P4 = `.dev/tasks/to-do/TASK-WF-blockerStage4-20261116-030206/TASK-WF-blockerStage4-20261116-030206.md`; S1, S3 = the stage 1 and stage 3 plans (`TASK-WF-blockerStage1-20261116-030154`, `TASK-WF-blockerStage3-20261116-030158`); S3-request = `BLOCKER-CLASSIFICATION-PROGRAM-20261115/stage-requests/stage3-request.md`; Ledger = the same folder's `README.md`; MAP = `tests/skills/test_review_severity_mapping.py`; Panel = `src/superclaude/commands/spec-panel.md`, PPanel = `plugins/superclaude/commands/spec-panel.md`; V1, V2, V3 = the three `variant-N-original.md` cards.
- Grading rule: blocking = a requirement or check that cannot be met, a wrong or missing result, or data loss; minor = wording or format; drop = not a defect of the plan.
- Every line cited below was re-read or re-run in this round (2026-11-16). Nothing was edited except this file; no test was run.

## 1. Criticisms of Variant 3, answered

| # | Criticism (who) | Answer |
|---|---|---|
| 1 | V3's Task 6 "Step 7: no failure expected apart from F2 and F3" hides the MAP failure (A1 R1, A2 R1) | **Conceded in scope, defended in fact.** The sentence covers only the three tests at P4:102 (`test_review_merge_rule_scan.py`, `test_review_severity_plugin_parity.py`, `test_review_severity_registry.py`), and none of them reads spec-panel. A grep of `tests/` for `follow-up candidates\|once per loop` hits only MAP (A1 R2 4.3 reports the same). So Step 7 is true about those three tests and says nothing about MAP. V3 missed C-002; that is a missed finding, not a false claim. X-001 is therefore not a contradiction (all three advocates now drop it). |
| 2 | V3's verdict "the files edited by several tasks end up consistent" is too strong (A1 R1, A2 R1) | **Conceded for one pair, kept for the rest.** `plugins/superclaude/rules/prompts/document_review_loop_prompts.md` must stay a byte copy of the source (`tests/skills/test_review_brief_placement.py:134`). Task 2 edits the source (P4:50), Task 5 hand-edits the plugin twin (P4:84), and no P4 pytest line runs the placement test. Identity can be reached but is never checked, so this is a minor verification gap under C-006 (A1 and A2 both fold X-002 there). V3's other consistency claims still hold. The allow-list end state: S3:144 lists 8 paths, Task 1 removes 2, Task 3 removes 4 and Task 6 adds the plugin mirror. The registry end state: 11 `digest`, 2 `pointer-only`, 5 `installed-only` and 2 `canonical` (S1:96, S1:100). |
| 3 | C-013 is a wording point because parity covers the mirror's content (A2 R1, R2) | **Agreed that it is minor. The defect is narrower and sharper than V3 wrote.** S1:209 defines T2 as "a reverse scan of the tracked `src/` and `plugins/` trees". P4:99 copies the folder "by hand" and runs the tests with no staging step; staging is only implied later, by P4:105 (`git diff --cached`). New this round: the merge-rule scan is NOT limited to tracked files. S3:144 says it "reads Markdown files only (`*.md`), under ... `plugins/superclaude`", selected by directory. P4:102 makes two claims. "Accepted ... by the merge-rule scan through the allow-list" is a real check. Only "accepted by the reverse scan through its `canonical` row" passes without reading the file. No wrong result follows, because T15 parity ties the mirror to the scanned source. Minor. Fix: stage `plugins/superclaude/skills/sc-review-severity/` before the P4:102 run. |
| 4 | C-014 over-reads one sentence: the upstream text itself says stage 4 "adds its plugin mirror" (A1 R1) | **Partly conceded.** S1:96 reads "One row of kind `canonical`: `skills/sc-review-severity/refs/rule.md` (the one source digest; the stage 4 package adds its plugin mirror)". The same sentence says each row has "the logical path relative to the install root" plus "surfaces (source, installed, project `.claude/`, plugin, ...)". As A1 says, the ambiguity starts in S1. But P4:99 is the step that must choose ("as a `canonical` row", with a repo path), and it does not say which reading it means. Minor, with S1:96 named as the origin. |
| 5 | C-015 is speculative (A1 R2 3.3, A2 R1) | **Conceded; changed from minor to drop.** A1 R2 shows that the MDTM digest sits in the I16 QA verdict block, while P4:70 puts the consumer line on each phase output. P4:102 re-runs T1 before the package closes, so a bad placement would be caught inside the package. No result is wrong. |
| 6 | V3 did no requirement traceability against the request or base Tasks 41 to 46 (my own Round 1 concession) | Unchanged. The merge should take V2's U-003 and U-004 as they stand. |

## 2. Do Advocates 1 and 2 now agree on C-002 and C-010, and does their evidence hold?

**Agreement.** Both now grade C-002 blocking and C-010 drop (A1 R2 sections 1.4 and 3.1; A2 R2 section 1 and the C-010 table row). My Round 1 grades were C-002 blocking and C-010 minor. C-002 is now unanimous. For C-010 I move to drop (section 3).

**Re-read of the claims that carry a blocking grade (six claims, plus the C-010 facts; all re-read this round):**

| # | Claim | What I re-read | Holds? |
|---|---|---|---|
| R1 | C-001: the stage 3 summary is written before the window and says so | S3:158 "State that the audit window runs after this package and is observed by the owner or operator"; S3:162 "no revert trigger can be judged until the audit window has run"; S3:163 the file "ends with the sentence that the owner's go for stage 4 is given in chat and not by this file"; P4:37 "exists and states that one audit window has passed" | **Yes.** S3:163 adds something no card cited: the producing contract itself points to the chat and the ledger as the place where the post-window record lives. That supports V3's remedy (check the go row at P4:36, or a separate window record) and rules out a hand edit of a finished stage 3 file. |
| R2 | C-002: MAP pins the phrase in both spec-panel copies | MAP:24-29: `SPEC_PANELS` holds the source and plugin paths, used through `parametrize("rel", SPEC_PANELS)`; MAP:58 requires "otherwise it is Medium (a warning listed under `follow-up candidates`)" in bullet 2; MAP:71 requires "`follow-up candidates`" and MAP:72 "asks the user once per loop" in bullet 3 | **Yes.** |
| R3 | C-002: the pinned text is live today in both copies | Panel:259, :260 and :332 and PPanel:257, :258 and :330 all contain `follow-up candidates`; Panel:260 and PPanel:258 contain "asks the user once per loop" | **Yes.** |
| R4 | C-002: stage 3 may not edit spec-panel, so the literals are unchanged at stage 4 entry | S3-request:20 "No template, rule-prompt, builder, researcher or spec-panel edit (stage 4)" | **Yes.** |
| R5 | C-002: S3 Task 8 does not name the spec-panel pins | S3:122: MAP "(the Medium and cadence pins move from "once per loop" to the once-per-run wording and to assertions on `refs/rule.md` and `refs/scale-map.md`)"; S3:125: MAP must pass; S3:127 "No pinning test is deleted wholesale; each changed pin is replaced by a pin on the new text" | **Yes, with A2's correction.** A2 R2 is right that S3:127 does not literally forbid replacing a pin on unchanged text; A1 R2 1.4 reads a ban into it. S3:125 does imply one further constraint. With spec-panel unchanged, an S3 executor cannot move MAP:72 to "once-per-run" wording on spec-panel, because that assertion would fail. Line 72 can only stay, or be deleted and replaced elsewhere. Either way, MAP:58 and MAP:71 are not cadence pins, and nothing in S3 tells anyone to move them. |
| R6 | C-002: no stage 4 task runs MAP | P4's only pytest lines are P4:41, :55, :63, :74, :88 and :102; none names `test_review_severity_mapping.py` | **Yes.** I also checked that the two tests Task 5 does run do not pin the phrase. `test_spec_panel_review_loop.py` and `test_review_loop_extension.py` pin the bullet order and other literals, and neither contains `follow-up candidates`. So P4:88 will pass while MAP is red. |
| R7 | C-010 facts | Ledger:18-21: the Package id and Owner go cells for stages 1 to 4 are empty | **Yes.** The facts hold. Whether a plan edit could fix them is the grade question (section 3). |

**One point I do not accept in A1 R2: the percentages.** A1 R2 1.4 gives "about 80 percent" and "60 to 65 percent", but no measurement supports either figure; A2 R2 says the same. The grade does not need them. Under the grading rule a missing result is blocking. Here the missing result is that no stage 4 task owns or runs MAP after deleting a phrase that MAP pins today and that no predecessor task is told to unpin. That holds without any probability.

## 3. Updated final grades

The table lists every point where two advocates still differed after Round 2, every point where I changed my mind, and the two points the brief asks about. Grades are shown as A1 R2 / A2 R2 / my Round 1, then my final grade.

| Point | A1 R2 / A2 R2 / A3 R1 | A3 final | Changed? | Reason |
|---|---|---|---|---|
| C-001 | blocking / blocking / blocking | **blocking** | no | R1 above; S3:163 confirms where the post-window record lives. |
| C-002 | blocking / blocking / blocking | **blocking** (conditional on S3 as written) | no | R2 to R6 above. Fix: Task 5 states which MAP pins it re-pins (58 and 71 on both files, and 72 if still present), and MAP is added to the P4:88 and P4:102 runs. |
| C-010 | drop / drop / minor | **drop** | **yes, minor to drop** | Ledger:18-21 confirms the empty cells, but no edit to the plan text can change when it was generated. P4:20 and P4:36 already fail closed at run time. It stays a process note for the orchestrator, outside the finding list. |
| C-012 | drop / drop / minor | **drop** | **yes, minor to drop** | The coverage matrix is a reflect-run file, and P4:19 already implements the package-id sentence. Not a defect of the plan. |
| C-015 | drop / drop / minor | **drop** | **yes, minor to drop** | Section 1 row 5. |
| S-002 | drop / drop / minor | **drop** | **yes, minor to drop** | It is a property of V2's card, not of the plan. S-001 is dropped on the same ground, and a minor here would be inconsistent with that. |
| X-001 | drop / drop / blocking | **drop as a separate point** | **yes** | Its whole weight is C-002. Counting it again would double one defect. |
| X-002 | minor (merged into C-006) / drop (folded into C-006) / minor | **no separate grade; its evidence goes into C-006 (minor)** | yes, wording | A1 and A2 differ only in the label. Both put the substance under C-006, and so do I. |
| C-011 | minor / minor / minor | minor | no | A1 moved from drop to minor in Round 2, so the three advocates now agree. |
| C-013 | minor / minor / minor | minor | no (scope narrowed) | Section 1 row 3: only the reverse-scan half of P4:102 is vacuous. |
| C-014 | minor / minor / minor | minor | no (origin added) | Section 1 row 4: the ambiguity starts at S1:96. |

Unchanged and unanimous, so not repeated in the table: C-003, C-004, C-005 (folded under C-002), C-006, C-007 (with A1's widened evidence), C-008 and C-009 are minor; S-001 and X-003 are dropped.

## 4. What single piece of evidence would settle each point still contested

All three advocates now agree on every grade. What remains is the conditions under which some of those grades hold. For each, this is the one fact that would settle it:

| Point | Open question | Settling evidence |
|---|---|---|
| C-002 | Does MAP still assert the spec-panel literals when stage 4 starts? | The stage 3 package's re-pinned MAP, run after S3 Task 8: `grep -n "follow-up candidates\|once per loop" tests/skills/test_review_severity_mapping.py`. A hit on a `SPEC_PANELS` test means the 4 parametrized cases fail after Task 5 (blocking holds). No hit means stage 3 moved them, and the defect shrinks to "Task 5 does not run MAP" (minor). |
| C-013 | Does T2 really read tracked files only? | The stage 1 `tests/skills/test_review_severity_registry.py`: does its T2 file list come from `git ls-files` (as `tests/skills/test_review_severity_rule.py:39` does) or from a filesystem walk? |
| C-014 | One row with a `plugin` surface, or a second row? | The stage 1 `registry.yaml` schema and the T1 and T3 resolver: whether a row path is resolved per surface. If it is, the second `canonical` row duplicates the first one's logical path. |
| X-002 / C-006 | Does the plugin rules prompt stay a byte copy? | `cmp src/superclaude/rules/prompts/document_review_loop_prompts.md plugins/superclaude/rules/prompts/document_review_loop_prompts.md` after Task 5, or a run of `tests/skills/test_review_brief_placement.py`. |
| N-1 (new, section 5) | Does any tracked, unregistered file hold the fence opener when strict T2 is switched on? | `git grep -n "review-severity:digest" -- src plugins` after stage 1, compared with the registry rows. |

## 5. New evidence: one more scan of Tasks 1 to 7 for a check that cannot be met

I re-checked every acceptance line against the live tree or the stage 1 and stage 3 contracts. One new conditional defect turned up. The other lines can be met as written.

### N-1 (new; minor, conditional, promote to blocking if the settling grep hits): strict T2 can fail on stage 1's own non-carrier files

- S1:209 defines T2 as failing "on any file that holds the old definition sentence **or a fence opener** and has no registry row of any kind". It covers every tracked file under `src/` and `plugins/`, Python included; only `canonical` and `pointer-only` rows count as registered.
- The fence opener is `review-severity:digest v2 begin` (S1:46; spec REQ-01, `merged-requirements.md:193`).
- Stage 1 creates files that must name or match the fence but get no registry row. S1:197 adds `_check_review_severity_digests` to `src/superclaude/cli/doctor.py`, which "compares the digest versions held by the installed carriers": to read a version it has to recognise the fence line. The `sc-review-severity` skill's `SKILL.md` and `refs/scale-map.md` may describe the fence as well. S1:96 lists the registry rows (11 `digest`, 1 `canonical`, 2 `pointer-only`, 5 `installed-only`); `doctor.py` and the skill's `SKILL.md` are not among them.
- In stages 1 to 3, strict mode is off ("strict mode is a switch, off in this phase", S1:209), so no earlier package is forced to notice a hit. Task 6 then switches T2 to strict (P4:99) and requires the registry test to pass (P4:102). If `doctor.py` (or any other unregistered file) holds the opener literal, P4:102 cannot pass without an edit that no task names: registering, exempting or rewording that file.
- Today `git grep -n "review-severity:digest" -- src plugins` prints nothing, because stage 1 has not run. So this is conditional on how stage 1 writes its matcher. A regex built from parts would not trip it; a literal string would.
- Fix: add one step to Task 6 before the strict switch. Run `git grep -n "review-severity:digest" -- src plugins`, and for every hit outside a `digest` or `canonical` row, either register it or record it as a named exemption in T2.
- None of the three cards raised this. V3's Task 6 walk (Step 5) checked only the old-sentence half of T2 ("the old sentence is in exactly 11 files"), not the fence-opener half.

### Acceptance lines re-checked and meetable (no new defect)

- **Task 3 grep (P4:62).** A re-run of `grep -rniE "highest severity|more severe rating|higher severity"` over the four skill folders hits exactly the six named lines (tech-reference :510 and :513, readme :542 and :547, `tdd/refs/build-request-template.md:122`, operational-guide :511), and nothing else in those whole folders. Meetable.
- **Task 1 (P4:38).** `agent_template_analysis.md` holds `more severe rating` only at :466. Meetable.
- **Task 4 (P4:75).** `grep -c` for the quoted cap sentence in `task-builder/SKILL.md` prints 1. Meetable.
- **Task 5 (P4:88).** "at most 2 fix cycles (3 reviews)" is at Panel:261, and the `## Unattended mode` section exists (Panel:455). One trap remains: `test_spec_panel_review_loop.py:83-89` requires every non-blank line of the Review Loop section to be one of the seven numbered bullets. A pointer added there as its own line fails that test, but Task 5 runs the test (P4:88), so the error is caught inside the task. Not a defect.
- **Task 6 (P4:104).** `grep -rln "Grade every review finding as blocking or minor" src/superclaude plugins/superclaude` lists exactly the 11 `digest` carriers and nothing else. The five spec-panel variants are not in `src/superclaude/commands/` (directory listing this round), so "outside the scan" is true. Meetable once stages 3 and 4 replace those 11.
- **T3 path check after the flip to `v2`.** T3's "no carrier contains `src/superclaude`" applies to `digest` rows (S1:209). `grep -c src/superclaude` gives 0 in all 11 digest carriers today, so flipping the 8 stage 4 rows to `v2` cannot trip T3 unless the new text adds such a path. Meetable.
- **Task 7 (P4:114-116).** Every named test file exists by Task 7 (T15's parity test is created in Task 6). Meetable.

## 6. Summary for the merge

- **Blocking:** C-001, C-002 (conditional on S3 as written; settle with the grep in section 4).
- **Minor:** C-003, C-004, C-005 (under C-002), C-006 (with X-002), C-007, C-008, C-009, C-011, C-013 (reverse-scan half only), C-014 (origin S1:96), and **N-1 (new, conditional)**.
- **Drop:** S-001, S-002, X-001, X-003, C-010 (process note only), C-012, C-015.

**Final grades for the two points asked: C-002 blocking; C-010 drop.**
