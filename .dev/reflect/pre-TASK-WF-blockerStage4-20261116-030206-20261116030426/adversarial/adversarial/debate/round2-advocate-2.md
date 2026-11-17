# Round 2 rebuttal — Advocate for Variant 2

Date: 2026-11-16. Round 2, second advocate, responding to all Round 1 statements and Advocate 1's Round 2 statement.

Grading rule: **blocking** = a requirement or check that cannot be met, a wrong or missing result, or data loss; **minor** = wording or format; **drop** = not a defect of the plan. Card-quality observations are recorded separately, not counted as plan findings.

## 1. C-002: concession after reading the actual predecessor and tests

**I change C-002 from minor to blocking.** My Round 1 statement that S3 Task 8 “migrates/replaces those pins before entry” was stronger than the words support. I withdraw that assertion. The failure remains conditional on which pins stage 3 actually leaves, not an observed or inevitable future test failure.

Citation keys, all under `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/`:

- P4 = `.dev/tasks/to-do/TASK-WF-blockerStage4-20261116-030206/TASK-WF-blockerStage4-20261116-030206.md`.
- S3 = `.dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md`; S3-request = the sibling `source.md`.
- MAP = `tests/skills/test_review_severity_mapping.py`.
- Request = P4's sibling `source.md`; S1 = `.dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md`.
- Ledger = `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/stage-requests/README.md`.
- V1/V2/V3 = the three `variant-N-original.md` files in this debate's parent directory.

### What S3:118–127 actually says

The relevant exact words at S3:122 are:

> `tests/skills/test_review_severity_mapping.py` (the Medium and cadence pins move from "once per loop" to the once-per-run wording and to assertions on `refs/rule.md` and `refs/scale-map.md`)

S3:125 requires the named tests, including MAP, to pass. S3:127 says:

> No pinning test is deleted wholesale; each changed pin is replaced by a pin on the new text.

**There are no words here specifically naming the spec-panel pins, `SPEC_PANELS`, or `follow-up candidates`.** “Medium and cadence pins” is broad enough to allow an executor to consider them, but it does not establish that they all migrate. S3-request:20 explicitly forbids a spec-panel edit at stage 3. I therefore cannot use stage 3's generic re-pin instruction as proof that stage 4 enters without the spec-panel literals.

### What I personally re-read in MAP:20–110

| Lines | Actual input and assertion | Consequence |
|---|---|---|
| 24–29 | `SPEC_PANELS` parametrizes source and plugin command files | These are not output-style-only assertions. |
| 50–62 | Grading bullet 2 must contain `otherwise it is Medium (a warning listed under `follow-up candidates`)` (58) | Removing that phrase fails this test on both surfaces if its pin remains. |
| 66–76 | Verdict bullet 3 must contain `follow-up candidates` (71) and `asks the user once per loop` (72) | This is a second pair of source/plugin cases, not the pragmatic cadence assertion. |
| 95–103 | FR-8/FR-9 assertions require the concrete-outcome wording, `otherwise it is Medium`, and `graded like FR-8` | They do not themselves require the follow-up-list parenthetical; do not claim removing only that parenthetical breaks them. |

I also read MAP:117–137: the separate test reads `STYLE` and asserts the output-style cadence at 128. This directly exposes the conflation in my Round 1 defense: a migration required for pragmatic wording does not prove the command-bullet pins are gone.

### Why the grade changes, without inventing certainty

P4:84 changes the command and plugin twin; P4:89 requires the list phrase to disappear. P4:88 runs two other tests and P4:102 runs three other tests. Neither run includes MAP; neither task owns a spec-panel re-pin. A stage 3 result that preserves the still-valid spec-panel list pins is compatible with the generic S3 wording. In that entry state, stage 4's required edit makes four parametrized cases fail while its named acceptance runs miss the failure. That is a concrete wrong final test state, not capitalization or formatting.

The correction is to give Task 5 responsibility for checking MAP's actual entry state, replacing any remaining spec-panel literals with assertions on the new behavior, and running MAP after the command changes. If stage 3 already replaced them correctly, verification will establish that and no duplicate re-pin is needed. I accept Advocate 1's missing-ownership finding, not an unconditional “the suite will be red” prediction.

One qualification to Advocate 1's Round 2 reasoning: S3:127 does **not** literally say that a pin may change only if its original target file changed. It requires replacement pins rather than wholesale deletion. I will not turn that sentence into a prohibition it does not contain, or adopt the unsupported numerical likelihoods. The blocker is the unowned, unchecked compatibility at the stage boundary.

## 2. Replies to criticisms of Variant 2 and my Round 1 grades

| Criticism | Answer and final treatment |
|---|---|
| V2 missed C-002; my Round 1 minor grade assumed stage 3 removes command pins (A1 and A3) | Conceded. Section 1 supplies the direct re-read and changes the grade to blocking, conditional on the pins that survive stage 3. A potentially safe predecessor interpretation is not proof that the dependency has been handled. |
| V2 “never opened the tests directory” (A1) | Its saved card does not show the necessary mapping/byte-parity inspection and missed both dependencies. That omission is established; the card alone does not establish every file the original reviewer opened. I concede the review's missing evidence, not an unobserved tool history. |
| V2 D1/C-010 mistakes generation history for a plan blocker (A1 and A3) | Agree; retain my Round 1 **drop** as a plan finding. Request:3 and Ledger:9 explicitly require prior generation authorization; empty recorded-go cells (Ledger:20–21) are a genuine provenance concern. P4:20 and :36 still prohibit execution without prerequisites and recorded go. No edit to the proposed task instructions retroactively changes generation history. Do not call the request satisfied, and do not infer that go exists; keep the process concern outside plan-content blockers. A1's Round 2 also now drops it. |
| D1/D2 say MAJOR/blocking and MEDIUM; D3/D4 also carry a second LOW label (A1 and A3) | Fully conceded: V2:21 and :23 have two genuinely conflicting labels, not a documented mapping between scales; :25 and :27 also mix scales. I cannot honestly choose whichever label favors my argument. Replace both scales with the present rubric: D1 drops as a plan finding, D2 is blocking, D3 is minor, D4 drops as a plan finding. Card-quality defect: minor; **S-002 drops from the plan finding list**, and X-003 is not a second count. |
| Deviation-table format instead of F-lines makes merging harder (A1 and A3) | True of the saved card, but it does not make the reviewed plan wrong. **S-001 drop**, changed from my Round 1 minor. Normalize during merge; do not count reviewer layout as plan work. |
| The self-reported model name conflicts with the assigned class (A1 and A3) | V2's header and self-report disagree. I cannot verify actual provider/model identity from those self-reports. Do not claim verified model diversity, but do not change the grade of re-readable evidence because of an identity string. No plan defect is established. |
| D3/C-011 is redundant because T1 equality includes the cap (A1 Round 1) | Accept the substantive safeguard: S1:46 and :50 require the canonical digest to end with the cap; P4:53 and :55 require the new digest and registry test. Thus there is no demonstrated lost cap. Keep **minor** only for the requested by-content preservation wording (Request:12), absent from Task 2's explicit checks while sibling Tasks 3/4 spell it out. A1 Round 2 now agrees. Do not describe this as an unprotected cap or a missing safety result. |
| D4/C-012 is about a review artifact, not the plan (A1) | Agree; change my Round 1 minor to **drop**. INF-002 of the reflect coverage matrix ends before Request:7's package-id instruction, but P4:19 supplies that instruction. The matrix can be corrected as review bookkeeping; no extra implementation task belongs in the plan. |
| V2's acceptance-endpoint reassurance ignores red connected tests (A1 and A3) | Conceded as a limitation. V2:55 talks about one task falsifying another acceptance line, not about the entire suite. It cannot support a green-suite claim. **X-001 drops separately** because the actual dependency defect is C-002; neither V2's narrow sentence nor V3's three-test walk logically contradicts it. |
| In-place editing can break the prompt byte-identity invariant (A1 and A3) | The invariant is real: `tests/skills/test_review_brief_placement.py:134` compares complete bytes. P4:50 edits the source and :84 edits the plugin later, with no run of that test in the named final suite. Concede the missed verification dependency, retain it as **C-006 minor**. Separate in-place editing can still produce byte-identical output; no inevitable wrong final state is shown. **X-002 drops as a separate finding**, folded into that verification gap. A1 Round 2 explicitly accepts attainability. |
| C-004 should not imply a blocking literal-case failure | Agree. P4:64 protects the cap by content, not by an explicit case-sensitive command. Lowercase “after” is a minor wording mismatch only; keep minor. |
| C-007 should also mention the unwritten parity assertion (A1 Round 2) | Accept the widened wording finding. P4:90 asks for both a common pointer/ledger sentence and a parity assertion in the registry test; :84 does not explicitly assign those additions. The acceptance line makes the result inferable and attainable, so minor, not blocking. The separate Task 7 final-sentence ordering note remains minor, not another pointer defect. |
| C-015 speculates about inserting a consumer line inside the digest (A3 concession; A1 Round 2) | Agree; keep my Round 1 drop. P4:70 asks for a phase-output consumer line, not a fence insertion, and :102 reruns registry equality before completion. A hypothetical bad edit is not a defect commanded by the plan; the useful earlier-check suggestion belongs under C-006. |

## 3. Updated final grades

These grades apply to the **plan finding list**, not to the formatting quality of an input card. “Drop” does not erase a useful process note or the evidence folded into a different finding.

| Point | My Round 1 | Final | Reason / disposition |
|---|---|---|---|
| C-002 | minor | **blocking** | Section 1: I withdraw the assertion that S3 guarantees migration of the spec-panel pins. Task 5 owns neither their compatibility nor a run of MAP after removing their required phrase. State the predecessor dependency, not a certain future failure. |
| C-004 | minor | **minor** | Case mismatch in the cap reference; the plan protects content and does not specify a case-sensitive cap grep. |
| C-007 | minor | **minor** | Explicit pointer and parity-assertion instructions are missing from the edit body, but the acceptance line supplies an attainable result. Include A1's widened evidence. |
| C-010 | drop | **drop** | Generation authorization/provenance concern, not a demonstrated wrong execution instruction; recorded-go execution hold remains. |
| C-011 | minor | **minor** | Requested explicit by-content cap preservation is not stated in Task 2's checks; canonical digest equality already protects the cap's result. |
| C-012 | minor | **drop** | Coverage accounting is outside the reviewed plan; the actual plan already includes package-id evidence lookup. |
| C-015 | drop | **drop** | No instruction places the consumer text inside a fence; final registry equality also catches a bad insertion. |
| S-001 | minor | **drop** | Reviewer-card layout, not a plan defect. |
| S-002 | minor | **drop** | Genuine conflicting card labels, acknowledged as minor card quality in section 2, not an implementation finding. |
| X-001 | drop | **drop** | Different scopes of statement, not an independent contradiction; all substantive weight sits on C-002. Do not add a second blocker. |
| X-002 | drop | **drop** | Byte equality is attainable by in-place edits. Retain the missing final byte-test reminder under C-006 minor, not a separate inconsistent-state finding. |
| X-003 | drop | **drop** | Duplicate of S-002, also not a plan defect. |

Remaining content points, to leave no ambiguity about the merge:

| Point | Final | Reason / disposition |
|---|---|---|
| C-001 | **blocking** | A post-window attestation is demanded from a summary whose producing contract places the window afterward. Distinct from the generation-history concern. |
| C-003 | **minor** | Name the allow-list's actual reference-file location instead of calling it the scan test's list. |
| C-005 | **minor** | Whole-file list-phrase removal reaches FR-8 outside the listed anchors; keep as a subpoint of C-002, with no false claim that the FR-8 assertions pin that parenthetical. |
| C-006 | **minor** | Missing final runs of affected pinning/byte-parity tests are verification wording gaps except for C-002's concrete old-phrase conflict. Fold X-002 here. |
| C-008 | **minor** | The existing execution constraint forbids early work, but the in-task check would be clearer before edits; no committed loss is shown. |
| C-009 | **minor** | Content/command references in acceptance lines are loose, not missing attainable functionality. |
| C-013 | **minor** | The tracked-only reverse-scan claim needs accurate coverage wording or tracking before the run; separate parity covers mirror contents. Conditional on the predecessor scan contract. |
| C-014 | **minor** | Clarify logical registry row plus plugin surface versus a separate repository-path row. Conditional on the predecessor registry design, not a proven resolver crash. |

## 4. Additional evidence and boundaries for the merge

1. **The direct-input distinction changes my position, not just its phrasing.** Section 1's MAP re-read separates the two spec-panel bullet tests from the output-style test. My earlier reliance on the generic migration sentence did not answer that distinction. I now accept C-002 as a conditional compatibility blocker rather than defending minor on an unproved precursor fix.
2. **The predecessor restriction must not be overextended.** S3:126 restricts changes to “the two fixtures”; it is not itself a restriction on every assertion in MAP. S3:127 demands replacement pins, not an explicit ban on replacing a command literal while its command text is unchanged. This makes alternative stage-3 implementations possible. It still does not tell stage 4 that MAP is compatible or assign anyone to verify that result.
3. **C-001 remains independently verified.** S3:158 says “State that the audit window runs after this package”; S3:162 says “no revert trigger can be judged until the audit window has run.” That is the producing contract, not a post-window attestation. It cannot supply P4's requested evidence without another assigned record/update. The ledger-go check and summary-content check are separate requirements; conflating them would change the plan rather than satisfy it.
4. **No new standalone finding is added.** The new contribution is the correction of my predecessor assumption and the exact limits of the S3 language. I do not claim executed stage-3 state, measured failure probabilities, or a completed future test result.

Shared assumptions remain: **A-001 qualify** (predecessor plans are contracts, not completed evidence); **A-002 qualify** (enforce substantive results, do not invent case-sensitive commands for prose references); **A-003 accept** (P4 names the summary itself, separately from the go row).

**Merge recommendation:** retain C-001 and the qualified C-002 as blocking; keep the minor wording/verification points from section 3, fold duplicates, and leave reviewer-card quality and generation provenance outside the plan finding list. Task 5 needs explicit ownership and verification of its mapping-test compatibility; the owner-go execution gate must not be bypassed.

Verification limit: I read all requested cards and debate statements, the complete P4 and S3 plans, MAP's requested lines and its output-style assertions, and the supporting excerpts cited here. I did not implement the plans, change source/tests, or run tests. Only this requested rebuttal file was written.

**Final requested grades: C-002 blocking; C-010 drop.**
