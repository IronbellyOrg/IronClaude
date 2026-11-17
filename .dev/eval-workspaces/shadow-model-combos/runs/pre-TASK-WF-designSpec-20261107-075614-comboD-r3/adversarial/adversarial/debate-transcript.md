# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2 (Round 2 appended below)
- Convergence threshold: 0.80
- Focus areas: correctness, coverage, deviation-classification
- Advocate count: 3 (general-purpose agents, model inherited from the orchestrator session: claude-gw-tier1b; the three variants were written by Sonnet, Haiku and GPT 6 Luna classes)

## Round 1: Advocate Statements

### Variant 1 Advocate (reviewer-1, analyzer)

**Position summary.** Variant 1 is the most accurate on severity. The Wave 0 wording tension is real, but it is minor, because the plan and spec text let an implementer write a passing test. Variant 1 is too narrow, and it wrongly claims Tasks 3 and 4 leave no spec row without a criterion. Variant 2 has the most real gaps but inflates one to MAJOR. Variant 3 finds a real but minor ambiguity.

**Steelman V2.** Its strongest case is that acceptance criteria which cannot fail on a wrong implementation defeat the audit purpose. Spec section 10 (line 366) requires a criterion "that a wrong implementation would fail". Verified true gaps: `auto_merge_armed` in engage notes (Task 4, line 73, asserts only `action`, `reason`, `cause`); `original_is_draft` on a first skip (Task 3, line 60); `--to ready` idempotency (Task 7, line 111 tests only the draft side); no CI-fix scenario in Task 11 (line 166). Critique: F1 is MAJOR when it should be MINOR. F2 is overstated, because Task 11 lines 170-172 assert event order, real `detect_crash_window` and `resolve_crash_window` calls, and forbidden `gh` calls. F5 ignores that Task 12 (line 182) also adds protocol-test assertions. Four spec citations are wrong: lines 369, 280, 270 and 268 do not hold the quoted text; the real lines are 333, 244, 234 and 232.

**Steelman V3.** Its strongest case is spec 251 and 4.6, which demand exactly one source for the cycle id. Task 8 (line 124) says the ref mints it "in the single place named by Task 1 O1". Task 10 (line 150) says the Wave 3 bullet "mints the cycle id". A literal reader could write two minting sites. Its F2 is also correct: Task 12 shares the protocol test file with Tasks 9 and 10 without depending on them, and spec 10 asks for complete dependency lines. Critique: both texts route to `fix_cycle_id` and `next_cycle_number`; Task 8's criterion (line 127) requires the ref to match O1; no check becomes unpassable, so it is not blocking.

**Strengths claimed.** F1 cites plan 137-140 and spec 241; plan 137 narrows the test to "`L3 only` or `draft` gate wording"; spec 59 and 241 themselves say the bullet prints the off line "at L3", so the tension is inherited from the spec, and spec 378 says to test "wording and position". F2 is real: Task 8 cites sections 3, 4.1, 4.5, 4.6 and 5 (line 124) and omits 4.2 and 4.4 (spec 182-185). Its citations are accurate.

**Weaknesses identified.** The claim that no spec row of Tasks 3 and 4 lacks a criterion is false (V2 F3 and F7). F2 overclaims: Task 3 (line 62) pins the `:a<k>` suffix; the unpinned parts are the payload fields and the `guard:<run_id>:<cycle_id>:<to>` prefix. It missed the cycle-id duplication and the dependency gap, and rated Task 12 ordering "sound" without checking the shared test file.

**Concessions.** V2's F3, F7, F10 and F12 are TRUE gaps. V3's F2 is TRUE. Accepted as MINOR.

**Shared assumptions.** A-001: QUALIFY (holds if the quoted text, not the line number, decides). A-002: QUALIFY (holds under sequential /sc:implement; spec 10 still requires complete `Depends on:` lines). A-003: QUALIFY (a gap counts only where spec 366 or 378 requires a failing-wrong-implementation criterion; not the `RunConfig` note or the PR body).

| Point | Correct position | Finding TRUE/FALSE | Severity | Evidence |
|---|---|---|---|---|
| S-001 | none | n/a | MINOR | Layout only. V2 read its brief in `runs/` and saw two post-execution test file names. |
| C-001 | V1 | TRUE (tension), not blocking | MINOR | Plan 137 narrows to "gate wording". Spec 241 and 322 pair "not gated" with "prints the off line". |
| C-002 | V3 (V2 F4 partly) | TRUE (ambiguity); V2 F4 TRUE | MINOR | Plan 124 and 150 both name minting via `fix_cycle_id`. Plan 170 checks order, not `cycle_id` equality. |
| C-003 | V1 | TRUE | MINOR | Plan 124 omits 4.2 and 4.4. Plan 62 pins `:a<k>` only. |
| C-004 | V2 | TRUE (F3, F7, F10, F12); F6 trivial | MINOR | Plan 73 and 60 assert fewer fields than spec 143 and 200. Plan 111 tests the draft side only. |
| C-005 | V3 | FALSE (mostly) | MINOR | Plan 170-172 are behavioural criteria. |
| C-006 | none | FALSE (weak) | MINOR | Plan 182 adds protocol-test assertions. |
| C-007 | V2 (F8 true, F9 partly) | F8 TRUE, F9 partly FALSE | MINOR | Plan 154 uses start-text constants. Plan 150 says each test is gated on L3 and `draft`. |
| C-008 | none | TRUE (gap), out of build scope | MINOR | Plan 33 records the gate. No task opens the PR. |
| C-009 | V3 | TRUE | MINOR | Plan 179-180 depends on 6 and 8 only. |
| X-001 | V1 | V1 TRUE, V2 MAJOR FALSE | MINOR | A passable test exists. |
| X-002 | V2 | V2 TRUE, V1 claim FALSE | MINOR | Plan 60 and 73 omit `original_is_draft` and `notes`. |
| X-003 | V3 | TRUE | MINOR | Execution is sequential in listed order. |
| X-004 | V3 | V2 F2 mostly FALSE | MINOR | Plan 170-172. |

### Variant 2 Advocate (reviewer-2, qa)

**Position summary.** Variant 2 is the only card that tests the plan's acceptance criteria one by one. Most of its findings (F3, F4, F6, F7, F9, F10, F12) hold as non-blocking gaps. Its one blocking finding (F1) is overstated, and four of its spec line numbers are wrong. I defend the coverage and withdraw the severity of F1.

**Steelman V1.** The plan reproduces the spec's own wording tension on the Wave 0 bullet; an implementer can resolve it by testing only gating wording, and plan line 137 narrows the test to "no `L3 only` or `draft` gate wording". V1 also finds a real gap no other card finds: Task 8's sources (line 124) omit spec 4.2 and 4.4. Critique: its notes say "no spec row of Tasks 3 and 4 lacks a criterion", which is false (`auto_merge_armed`, `original_is_draft`); it says "dependencies look sound" without checking the shared test file.

**Steelman V3.** Minting the cycle id is a one-source rule and Tasks 8 (line 124) and 10 (line 150) both say "mints"; Task 12 edits `test_merge_guard_protocol.py` without depending on Tasks 9 and 10. Critique: Task 8 defers minting to "the single place named by Task 1 O1"; Task 1's criterion (line 37) requires exactly one place; Task 10's Wave 3 bullet is the SKILL side of the same step; an ambiguity, not a guaranteed double mint, not blocking.

**Strengths claimed.** F4 exact (spec 251 vs plan 170 order only). F7 exact (plan 56 vs 60). F10 exact (plan 111 vs spec 234). F12 exact (plan 166 "section 5 table" has no CI-fix row; spec 61 requires one). F3 exact (spec 143 vs plan 73).

**Weaknesses identified.** Four spec citations are at the wrong lines: F3 cites 369 (quote at 333); F5 cites 280 (quote at 244); F10 cites 270 and 268 (quotes at 234 and 232). F1 claims plan line 140 "fails any L3 wording", but line 137 narrows the test to gate wording, so it is passable. F2 says Task 11 checks only names, but plan 170-172 assert event order, real recovery windows and forbidden `gh` calls; only "no event at ordinals 0-2" is unasserted. F5 and F8 depend on how strictly the wording is read.

**Concessions.** F1 should be MINOR. F2 mostly false. The four wrong line numbers. V1's U-001 is real and was missed. V3's F2 is valid.

**Shared assumptions.** A-001: QUALIFY (holds only after re-reading). A-002: QUALIFY (holds under sequential execution; Task 12 shares a file but does not consume 9 or 10 output). A-003: QUALIFY (holds for fold, `guard_status`, resume reasons, `applied_edits`; for protocol prose, wording tests are enough).

| Point | Correct position | Finding TRUE/FALSE | Severity | Evidence |
|---|---|---|---|---|
| S-001 | none | n/a | MINOR | Layout differences only. |
| C-001 | V1 | TRUE (tension), not blocking | MINOR | Plan 137 narrows the test; spec 241 and 59 carry both texts. |
| C-002 | none (V2 on the gap, V3 overstated) | V3 MAJOR claim FALSE; V2 F4 TRUE | MINOR | Plan 124 defers to the O1 place; plan 127 and 37 require one place; plan 170 omits a `cycle_id` equality check. |
| C-003 | V1 | TRUE | MINOR | Plan 124 omits 4.2 and 4.4; spec 182-185 define the fields and key; criterion 62 covers only the `:a<k>` suffix. |
| C-004 | V2 | TRUE | MINOR | Plan 73, 60, 111, 166. |
| C-005 | V3 | F2 mostly FALSE | MINOR | Plan 170-172. |
| C-006 | V2 (weak) | TRUE but thin | MINOR | Plan 185 and 198 verify by grep and reading; Task 12 adds assertions (line 182); V2's spec cite 280 is wrong. |
| C-007 | V2 | TRUE, marginal | MINOR | Plan 154 "literal start text"; plan 150 says tests are "gated on L3 and `draft`". |
| C-008 | V2 | TRUE | MINOR | Plan 33 and 182 state the PR body gate; no task authors a PR body. |
| C-009 | V3 | TRUE | MINOR | Plan 179-180 depends on 6 and 8 only; Tasks 9, 10, 12 edit the same test file. |
| X-001 | V1 | V1 correct; V2 FALSE as blocking | MINOR | Plan 137 versus 140. |
| X-002 | V2 | V2 TRUE; V1 note FALSE | MINOR | Plan 60 and 73 versus spec 143 and 200. |
| X-003 | V3 (partial) | TRUE as hygiene | MINOR | Order is fine for sequential execution. |
| X-004 | V3 | V2 F2 mostly FALSE | MINOR | Plan 170-172. |

### Variant 3 Advocate (reviewer-3, refactorer)

**Position summary.** My variant's cycle-id finding points at real wording overlap but overstates it as MAJOR. Variant 2's MAJOR on the Wave 0 bullet is the larger overstatement. Both blocking claims fail on the text; the only live disputes are MINOR acceptance gaps.

**Steelman V1.** The Wave 0 clash comes from the spec, not the plan; plan line 137 narrows the test to "no `L3 only` or `draft` gate wording", so the check is passable and MINOR is right. Its Task 8 omission of spec 4.2 and 4.4 is real. Weakness: the blanket claim that dependencies are sound and no Task 3 or 4 criterion is missing; `original_is_draft` (plan 56 vs 60) and `auto_merge_armed` (plan 70 vs 73) contradict it.

**Steelman V2.** pytest-only criteria let a hollow implementation pass; F3, F7, F10, F12 are valid (plan 111 tests only `--to draft`; spec 234 makes `--to` idempotent in both directions). Critique: F1 inflated to MAJOR; spec lines 270, 268, 280 are wrong; F2 ignores plan 170-172; F9 ignores "each gated on L3 and `draft`" at plan 150; F8 and F11 are thin.

**Strengths claimed.** Every V3 citation is accurate (plan 124, 150, spec 251, the Task 12, 9 and 10 ranges). V3 alone names the minting overlap and the shared-test-file ordering.

**Weaknesses identified.** Only two findings; Tasks 3, 4, 11 unchallenged. F1 reads as blocking, yet Task 8 says the ref mints "in the single place named by Task 1 O1" and its criterion requires the ref to state that place; spec 4.6 puts minting in the SKILL and Task 10's Wave 3 bullet "mints the cycle id", so the ref refers to that place and is not a second mint. F2 applies selectively: `tests/skills/test_worker_contract.py` is also shared by Tasks 7, 8 and 12.

**Concessions.** V3 F1 is MINOR at most (wording clarity). V2 F4 is the better-targeted version of the same worry. V1 and V2 each caught real gaps V3 missed.

**Shared assumptions.** A-001: QUALIFY (V2's spec line numbers 270, 268, 280 are wrong; accept citations only after a re-read). A-002: ACCEPT (sequential order; Task 12 sits after Task 11). A-003: QUALIFY (a defect only when the omission could let a wrong implementation pass; true for F3, F7, F10, not F6 or F11).

| Point | Correct position | Finding TRUE/FALSE | Severity | Evidence |
|---|---|---|---|---|
| S-001 | none | n/a | MINOR | Cosmetic. |
| C-001 | V1 | TRUE as tension, FALSE as unpassable | MINOR | Plan 137 narrows; line 140 is looser phrasing. |
| C-002 | V2 (V3 overstated) | V3 F1 FALSE as blocking; V2 F4 TRUE | MINOR | Task 8 defers to the O1 place; Task 10 names the SKILL Wave 3 bullet. |
| C-003 | V1 | TRUE | MINOR | Task 8 omits 4.2 and 4.4. |
| C-004 | V2 | TRUE for F3, F7, F10, F12; F6 weak | MINOR | Plan 60, 73. |
| C-005 | V3 (partly) | Half TRUE | MINOR | Plan 170-172 behavioural; the other tests name-only. |
| C-006 | V2 | Weakly TRUE | MINOR | Plan 185 and 198 grep only for the flag token. |
| C-007 | V2 | F8 TRUE, F9 FALSE | MINOR | Plan 154 start text only; line 150 gates each bullet test. |
| C-008 | none | FALSE | MINOR | No task opens the PR. |
| C-009 | V3 technically; V1 in practice | TRUE only under a parallel executor | MINOR | Order puts Task 12 after Task 11. |
| X-001 | V1 | V2 MAJOR FALSE | MINOR | Same as C-001. |
| X-002 | V2 | TRUE | MINOR | Plan 56 vs 60. |
| X-003 | V1 | V3 F2 weakly TRUE | MINOR | Listed-order execution; Task 13 follows Task 12. |
| X-004 | V3 (partly) | V2 F2 half TRUE | MINOR | Plan 170-172 vs name-only list at 169. |

## Round 2: Rebuttals

### Variant 1 Advocate (reviewer-1)

**Response to criticisms.** Conceded: Task 4 line 73 asserts only `action`, `reason`, `cause`, so `auto_merge_armed` in `notes` is untested (spec 143); Task 3 line 60 leaves `original_is_draft` on a first skip untested (spec 200). Partly conceded: Tasks 9, 10 and 12 all extend `test_merge_guard_protocol.py` additively (plan 137, 150, 182) and Task 12 consumes none of their output. Conceded in part: plan 62 pins the `:a<k>` suffix; the unpinned parts are the payload fields and the `guard:<run_id>:<cycle_id>:<to>` prefix (spec 184).

**Updated assessment.** C-006 MINOR weak (Task 12 line 182 adds assertions for flag row, argument-hint and new section; Task 13 criteria at line 198 are grep plus reading; the spec requires no test for command file or user guides; `docs/user-guide/` is outside the scanned roots, spec 255). C-008 MINOR, out of build scope (plan 33 records the gate and that the PR-opening run must pass `--merge-guard off`; spec 326 gives the statement to the owner's release step). C-009 / X-003 / A-002 MINOR hygiene; A-002 QUALIFY (holds under sequential /sc:implement; Task 10 also omits a direct line for Task 8, reached through Task 9).

**New evidence.** N1: Task 13 lacks a direct `Depends on: Task 1` (plan 190-193 lists Tasks 2, 10, 11, 12; lines 195 and 199 compare with "the base-commit record of Task 1"), MINOR. N2: no criterion asserts FR-16, the one retry of a failed release with "already in target state" counted as confirmed (spec 165, 315): Task 8 line 124 says "one retry", criteria 126-130 do not assert it, Task 11's case list (166) omits release failure, criterion 169 requires only the test name `test_guard_release_failure_retries_once_and_reports`, MINOR. N3: no criterion asserts the engage-failure message naming `--merge-guard off` and printing the clear command (spec 274; Task 8 criterion 129 requires only `terminal_halted` reason `draft_guard_unavailable`), MINOR. Dropped: the corrupt-line raise (spec 208) is already pinned by an existing test. No MAJOR found.

### Variant 2 Advocate (reviewer-2)

**Response to criticisms.** F1 conceded, now MINOR: plan 137 narrows the test to "no `L3 only` or `draft` gate wording", so a passing test can be written; residual tension is in spec 59 and 241. F2 mostly withdrawn (plan 170-172 assert order, real recovery windows, forbidden calls; only "no event at ordinals 0-2 or `off`", spec 309, is unasserted). F9 conceded (plan 150 says each test is gated on L3 and `draft`). F8 marginal (plan 154 pins start text, as spec 377 allows). F3, F4, F7, F10, F12 stand, all MINOR. Corrected spec lines for its four wrong citations: F3 333 (not 369); F5 244 (not 280); F10 234 (not 270) and 232 (not 268).

**Rulings.** N1 TRUE MINOR (Task 1 reached through Task 2, execution unaffected). N2 TRUE MINOR (plan 127-130 do not assert the retry; 169 requires only the name). N3 TRUE MINOR (plan 129 requires only `terminal_halted` with the reason). C-006 weakly true MINOR; C-008 conceded, MINOR out of scope. None of its findings is MAJOR.

**New evidence.** FR-16 (release failure) has no end-to-end criterion in any task, MINOR and the largest cluster: plan 60 lists `settled(draft, failed)` but not `settled(ready, failed)` (spec 205); the `settled(any, skipped, user_override)` row (spec 206) and `settled(ready, confirmed, changed)` row (spec 203) are not named; Task 4's named resume cases (76-77) skip rows 7 and 8 (`RETRY_RELEASE`, `HOLD(ownership_unproven)`, spec 169-170); all rest on the umbrella "every row" wording (plan 60, 70, 73). Task 9's literal `off` line has no "printed once" check (plan 137, 140; spec 216), MINOR.

### Variant 3 Advocate (reviewer-3)

**Response to criticisms.** C-002 decided by Task 1 criterion (plan 37), which requires O1 to "name one single place" where the id is minted; Task 8 (124) mints "in the single place named by Task 1 O1" and its criterion (127) requires the ref to match; Task 10's Wave 3 bullet (150) is the SKILL side of that same place (spec 251). The real gap: Task 10's criteria (153) never check that the bullet names the O1 place. F2: Task 12 depends on Task 8, which creates the test file; listed order puts it after Tasks 9 and 10; matters only under parallel execution. N1 TRUE but trivial (Task 2 depends on Task 1). N2 and N3 conceded MINOR. Advocate 2's unnamed fold and resume rows conceded MINOR. Task 9's "printed once" conceded MINOR.

**Updated assessment.** F1 MINOR, not blocking. F2 MINOR hygiene. C-009, X-003, A-002 MINOR hygiene, final.

**New evidence.** No order problem (every criterion runs against artifacts created earlier). No file of spec section 6 is left out. Plan constraint 23 (no `file:NNN` pointers in protocol prose) has no enforcing criterion: Task 8's test (128) asserts only the absence of `src/superclaude` plus fence and repo-scope rules; Tasks 9, 10, 12 have no such check, MINOR. "No python fence" in the new ref is untested: Task 8 text (124) says so, criterion 128 does not assert it (only the `SKILL.md` fence count, 143 and 154), MINOR. Task 9 criterion 142 names Tasks 2, 5, 7, 8 for expectation edits though Task 6 also edits `test_skill_parse.py`; it only adds a test, cosmetic.

## Convergence after Round 2
All 17 diff points reach a common verdict: S-001 cosmetic; C-001 MINOR; C-002 MINOR; C-003 MINOR; C-004 MINOR (F3, F7, F10, F12 true; F6 trivial); C-005 mostly false; C-006 weak MINOR; C-007 F8 marginal, F9 withdrawn; C-008 MINOR out of scope; C-009 MINOR; X-001 V1 correct; X-002 V2 correct; X-003 weak; X-004 V3 correct; A-001, A-002, A-003 all QUALIFY.
