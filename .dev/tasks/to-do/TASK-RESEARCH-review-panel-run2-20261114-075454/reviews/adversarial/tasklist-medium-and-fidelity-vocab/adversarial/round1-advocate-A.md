# Round 1 advocate for Variant A (slot X-15, tasklist Medium and fidelity vocabulary)

Role: advocate for Variant A (Medium is a non-blocking warning in the tasklist module; fidelity prompt becomes a tasklist-module vocabulary under the core). Round 1 of 2. HEAD `50d4d2b9d`.
Tags: [CODE-VERIFIED] = re-read in this session; [UNVERIFIED] = not re-read or an interpretation. Paths are repo-relative. `SK` = `src/superclaude/skills/sc-tasklist-protocol/SKILL.md`; `PM` = `src/superclaude/output-styles/pragmatic.md`.

## Position Summary

Variant A is right on the decision (a tasklist Medium must not block), because every other written Medium in the repo is non-blocking, including the one inside the protocol that rule S4 itself offers as its example of "its own severity model". A is not right on everything: its reviewer-union mitigation does not fit Stage 7, its role-table claim overreaches, and it has no measurement behind the "omissions are High" regrade. A is the better position only with a written grading block and the omission rule; without them B's caution is justified.

## Steelman of Variant B

B's strongest case, in its best form:

1. The Medium-blocks rule is explicit text, not an accident. Nine sites in the skill say "High and Medium (blocking)" or "High or Medium" (SK:1439, 1531, 1537, 1567, 1571, 1608, 1610, 1614 and the unattended phrase). The sweep fixture records the intent in its `tasklist` group line: "open High/Medium findings HALT at the cap (B3-10)" (`tests/skills/fixtures/review_severity_sweep_edits.yaml:29`). Twelve rows pin it. [CODE-VERIFIED]
2. B's change is the smaller one: it only adds a definition and an S4 sentence, touches no pinned row, and loosens no gate. Flipping a deliberate rule to match a CLI nobody documented as a model is the riskier move.
3. B has the only data. Two archived ValidationReports, six Medium findings, and two of them are real omissions graded Medium by actual reviewers (v3.66 M2 omits Developer Guide section 9.7; test1 M1 is a Phase 1 exit criterion with no task). Both bundles report High 0, so a label-preserving flip lets them skip Stages 9 and 10.
4. The CLI's non-gating Medium has a plain cause: a one-shot report has no fixer. The skill has a fixer and acts on what it finds.
5. A's safety rests on a behavior nobody measured: reviewers typing omissions as High. B's blocking Medium is safe against that miss whatever reviewers type.

What B gets right: the skill gives Medium no definition (SK:1384-1391); A's union mitigation has no cluster to act on (X-009); the loosening is real; the sweep did record High/Medium; the core has no module-declared role table today.

## Strengths Claimed

1. **Every other written Medium in the repo is non-blocking, including S4's own exemplar.** [CODE-VERIFIED]
   - `/sc:implement`'s severity model, which `PM:228` names as the example of a protocol applying "its own severity model", maps words as: "high = any confirmed checklist yes = blocking; medium, IMPORTANT without a yes, low-medium, low and cosmetic = minor or note" (`src/superclaude/skills/sc-implement-protocol/refs/qa.md:81`).
   - The legacy card converter sends `medium` to MINOR and `high` to MAJOR (`src/superclaude/cli/review/card_convert.py:71-83`, `MINOR_WORDS` holds "medium").
   - The CLI gate counts Medium and exits on High only: semantic checks read only `high_severity_count` (`src/superclaude/cli/tasklist/gates.py:34-45`; `src/superclaude/cli/roadmap/gates.py:195-240`, high count at `:231-232`); `tasklist_ready` is true when the high count is 0 (`src/superclaude/cli/tasklist/prompts.py:99-100`); the test names it (`tests/tasklist/test_tasklist_fidelity.py:208-226`).
   - The repo rule: Medium "never fails a review, never triggers a fix pass and never appears in a reviser brief" (`PM:230`).
   - Against these, only the skill and one sweep mapping say Medium blocks. S4 cannot shelter a Medium-blocks model, because the exemplar S4 cites classes Medium as minor.
2. **The skill's rule is label-driven with no definition, which is what S5 tells reviewers not to do.** `SK:1384-1391` lists `High | Medium | Low` and defines none; `PM:229` says "grade by the definition above, not by the label". The only written definitions in the product are the CLI's (`prompts.py:51-69`): HIGH omits, contradicts or misrepresents so the tasklist "cannot be used as-is"; MEDIUM is "insufficient detail, ambiguous language, or minor misalignment" (examples: effort estimate diverges, acceptance criteria weaker, verification method differs); LOW is formatting. A adopts these and grades by definition.
3. **The history shows a bucket mapping, not a Medium decision.** Before #343 the loop applied "all corrections" and short-circuited on "zero findings"; it ended advisory ("the bundle still ships; the loop is an advisory remediation, not a hard blocker", fixture S-130 `old`). The sweep had to carve Low out as notes. Its stated rule has only two buckets and puts MEDIUM in neither: "blocking (CRITICAL / IMPORTANT ...) or minor (MINOR / LOW ...)" (fixture header lines 4-6). The commit message names the tasklist patch loop only for the cap and says nothing about Medium (`git show -s 80f934de5`). The edit is recorded (concession below) but it is a mapping made without a definition.
4. **B's reading of the archived reports does not hold up on re-reading.** I read both reports (`.dev/releases/archive/v3.66-tdd-skill-refactor-v2/validation/ValidationReport.md`, first 50 lines; `.dev/test-fixtures/results/test1-tdd-prd-v2/validation/ValidationReport.md`, first 40 lines; every Medium finding is inside those ranges). Of six Medium findings, by the CLI definitions:
   - Omission, High under A: v3.66 M2 (section 9.7 omitted from T01.03); test1 M1 (Phase 1 exit criterion with no task).
   - Weaker but present, Medium under A: v3.66 M1 (line numbers stated as facts); M3 (task Steps mention the retention template, only the acceptance criteria omit it); M4 (the report says "Deliverables correctly lists all 5 refs/ files"; only the acceptance bullets name 4); test1 M2 (step text says 60%, "the acceptance criteria correctly state both targets").
   - B's E6 describes M4 as "an acceptance list missing one of five required files" and counts it with omissions; the report says the deliverable is present. So the sample is 2 omissions and 4 weaker-but-present items, not "mostly an omitted or unmatched roadmap requirement". Caveat: one reader, six findings, [UNVERIFIED] as a measurement.
5. **B's blocking Medium widens the false-halt channel.** The P2 loop re-runs the full Stage 7 set with fresh agents every pass (SK:1608) and halts on `Regression detected ...` when a previously-PASS item "is FAILing with a High or Medium (blocking) finding" (SK:1610). Medium-class findings (ambiguity, weaker criteria) are where reviewer variance is highest, so under B a fresh agent adding a new Medium on a task that passed at pass 1 halts the skill and, under `--unattended`, ends the run `blocked` (SK:1615). That is a code-grounded mechanism; its frequency is [UNVERIFIED]. Under A only a High triggers it.
6. **A's cost is bounded and visible; it is not silent.** A Medium that should have been High stays in the Medium section of `ValidationReport.md` (SK:1478) and is listed as a follow-up candidate, so a human sees it; the cost is a missed patch, not a hidden defect.
7. **A is statically testable, B adds unpinned text.** T1 rewrites 12 literal rows (`tests/skills/test_review_severity_rule.py:268-272` requires `old` gone and `new` present) plus the two worker-contract phrases (`tests/skills/test_worker_contract.py:777`, `:1861`), and keeps the byte-equality check with the tracked plan copy (`:275-283`). T2 adds a parity test over the skill grading block and `build_tasklist_fidelity_prompt`. B's new Medium definition and S4 sentence have no pin, and its M-X15-3 ("run the existing pins unchanged") cannot detect a wrong definition.
8. **Both maps parse; A's must not set `reflect_category`.** v1 rejects only MINOR plus blocking (`src/superclaude/cli/review/findings.py:100-101`); v2's label-determined rule fires only when `reflect_category` is set (`src/superclaude/cli/review/findings_v2.py:155-162`), which would force MAJOR to blocking. A states this hazard; B does not. [CODE-VERIFIED]

## Weaknesses Identified in Variant B

1. **B's S4 premise holds only after B's own edit, and S4's exemplar contradicts it.** B calls Medium-blocks "the skill's own model" (B section 1) and then concedes "the skill states no model and no definition of Medium" (B section 8; X-002). S4 says a protocol that defines a model "applies that model" (`PM:228`). Adding the sentence "this skill applies its own model under S4" after the fact does not make the model exist before the edit. The one S4 exemplar maps `medium` to minor or note (`qa.md:81`). [CODE-VERIFIED]
2. **B's own definition of Medium is a dilemma.** B promises "a Medium definition" and gives no text. If B copies the only written one (`prompts.py:58-64`: insufficient detail, ambiguity, minor misalignment), that Medium fails S1's blocking test (wrong behaviour, false claim, missing deliverable, security risk; `PM:225`) and a blocking fix pass on it violates S2 (`PM:226`). If B instead defines Medium so that it meets S1's blocking test, the CLI already calls that HIGH (`prompts.py:51-57`) and the label is redundant. Either way blocking-Medium collapses to a label kept for continuity.
3. **B leaves two opposite readiness answers to one question.** The CLI says a tasklist with Medium deviations is ready (`tasklist_ready` true at high count 0, `prompts.py:99-100`; `roadmap/gates.py:231-232`; test at `test_tasklist_fidelity.py:208-226`). The skill says the same kind of bundle does not ship clean while a Medium is open (SK:1614). Both answer "is this tasklist faithful enough to execute against this roadmap?". B's "no fixer, so no gate" (E5) is its inference; no comment, doc or test gives that reason (X-007), and the CLI prompt's own MEDIUM text ("could lead to execution issues") shows its authors placed Medium under the line on purpose.
4. **B's E6 and E7 overstate the archive.** Section Strengths 4 above: 2 of 6 Mediums are omissions, and B's E7 replay is label-preserving by construction (it ignores that a grading block would move omissions to High). E7 is a statement about the old labels, not about what A does to those bundles: under A, v3.66 M2 and test1 M1 become High, so neither bundle short-circuits.
5. **Medium-blocking widens the regression halt** (Strengths 5), a mechanism B does not price. B's section 4 prices stalls only through "monotonicity halt, the 2-pass cap, `blocked`" and says they end in a human decision; it does not say that a fresh agent's new Medium on a passed task halts immediately (SK:1610).
6. **B's new text is unpinned and its measurement cannot lose cleanly.** The Medium definition and S4 sentence have no test (B section 4 says so). M-X15-1 has a "mixed" band from 1/3 to 2/3 that "is not a win for either position", and it measures reviewer behavior under a skill that has no definition, so it cannot show whether a definition changes behavior.
7. **B's `card_convert.py` caution (U-012) supports A.** The converter that B warns against sends `medium` to MINOR; B treats this as a trap, but it is a fourth repo source for Medium as non-blocking (Strengths 1).

## Concessions

- **X-004 (what the flip does to the archive).** Conceded in part. A read no archived report; B's two reports are the only data in either variant. They show reviewers, under today's definition-less skill, did grade two real omissions Medium. A's regrade to High is a design assumption: the reports predate any grading block, so nothing shows reviewers will follow one. If M1 (blind grade of seeded defects) fails, A fails. A should not be adopted before M1, or an equivalent run of the pre-registered kind, has been done.
- **X-009 (union mitigation).** Conceded fully. `SK:1351-1368` assigns each task to exactly one agent (A: tasks 1 to `split`; B: `split+1` to `task_count`), so there is no reviewer cluster for C-03's union to act on. A's mitigation 4.2 item 4 must be dropped. Replacement: the grading block, the omission-is-High rule, T2, M1. Also, merge step 2 (SK:1410) keeps "only one entry" for duplicates and does not say which severity survives; A must add "keep the highest severity". [CODE-VERIFIED]
- **A-008 / variance is narrowed, not removed.** Under A a fresh pass-2 agent can type a High on a task that was Medium-only at pass 1, and SK:1610 would read that as a regression. Same channel as in Strengths 5, but only at the High boundary.
- **X-003 (history).** A's "records no decision about Medium" is true of the commit message only. The sweep fixture's `tasklist` group line records "open High/Medium findings HALT at the cap" (fixture `:29`), and the new text was written on purpose. The edit was deliberate; what A contests is whether it was a Medium decision or a bucket mapping, and the header (lines 4-6) supports the second reading only by omission.
- **X-001 and X-006 (S1-S5 reach).** `PM:228` allows a protocol its own model and `PM:229` names CRITICAL/IMPORTANT/MINOR, not High/Medium/Low. A's "the skill does not follow S1-S5 as written" overstates. A's narrower claim, shown above, is that S4's own exemplar classes Medium as non-blocking.
- **X-005 (role table).** B is right that no code lets a module declare which roles or pairs are legal: `ROLES` is a closed set (`findings_v2.py:35`). A's section 2.3 "role table" is a design intention, not an existing feature. The layering guard stays prompt text plus its test (`test_tasklist_fidelity.py:101-108`). Not load-bearing for the Medium decision.
- **X-008 (one product).** A fact 13 (skill does not call the CLI) and answer 3 ("one product") are in tension. The accurate claim is one product family and one readiness question, not one code path.
- **X-010.** A's grep count (76 lines in 10 files) is `.py`-only; the diff analysis found 88 lines in 14 files. Not load-bearing.
- **A's edit list is incomplete.** The pinned phrase "the unresolved High or Medium HALT resolves as blocked" is not in the skill: it is at `src/superclaude/commands/tasklist.md:113` (grep in this session); the skill says "this HALT resolves as blocked" (SK:1615). T1 must edit `commands/tasklist.md:113` as well as the two test pins. [CODE-VERIFIED]
- **Form 2 is A's weakest part.** `reflect_category`'s rule also forces `category` into `REFLECT_CATEGORIES` (`findings_v2.py:155-162`), so it cannot be reused as is, and C-02 ruled out a core category predicate. A should take Form 1 (brief plus grading block plus T2) and defer Form 2.
- **A loosens a gate** (4.2 items 2 and 3): a Medium-only run now completes with follow-up candidates where it used to HALT. This is a user-visible behavior change.

## Shared-assumption responses (A-004 to A-009)

| ID | Response | Reason |
|---|---|---|
| A-004 | QUALIFY | A's "follow-up marker" is not needed for the Medium decision. The map works with Medium as MAJOR and `blocking: false` plus the label that the Stage 7 prose entry already carries (`Severity: Medium`, SK:1386). The parse edge validates the keys it names (`findings.py:90-109`); whether an extra key survives the ledger merge is [UNVERIFIED]. Drop the marker from A; keep it only if C-02's merge is shown to preserve it. |
| A-005 | QUALIFY | True that Stage 7 findings are prose today (SK:1384-1391; no findings block). That favors A: A's change takes effect on the skill's own Stage 8-10 text whether or not a core engine ever hosts the module. Note for both: v1 also requires `category` in a closed set (`findings.py:15-22`, `:102-103`), so a tasklist drift or omission needs a mapped category, and v2's lens set is closed (`findings_v2.py:36`). Neither variant addresses this; it does not change the Medium decision. |
| A-006 | QUALIFY | Skill versus CLI is not the only Medium conflict: the skill's Medium also disagrees with `qa.md:81` and `card_convert.py:81-83`. Other uses (Risk Medium at SK:565, 581, 964, 1699 per the diff analysis, [UNVERIFIED] here) are not about blocking and a regrade must leave them and the TDD table's uppercase MEDIUM labels alone except the two checks regraded to High. |
| A-007 | ACCEPT | Evidence that S1-S5 reaches the tasklist loop: the #343 message lists "sc:tasklist's patch loop" among the loops that halt at the cap; the sweep fixture applies "Rule applied (S1/S2)" to 12 tasklist rows (fixture header, `:29`). The P2 loop is an initial patch plus one re-patch, so 2 fix cycles, inside S3's cap (SK:1604, `PM:227`). The assumption is load-bearing for A: if S2 reaches the loop, "minor findings never trigger a fix pass" reaches it too. |
| A-008 | QUALIFY | True for first-pass Stage 7: one agent grades each task (SK:1351-1368), so the typed label is the label that gates; merge step 2 (SK:1410) does not say which severity survives a duplicate. But a pass-2 full re-validation re-grades every task with fresh agents (SK:1608) when F_1 is non-empty. And the exposure is symmetric: under B a Medium typed Low, or a MAJOR typed `blocking: false`, drops the row. The boundary moves from Medium/Low (B) to High/Medium (A); it does not disappear in either. |
| A-009 | ACCEPT | Re-read in this session: `group: tasklist` count is 12 (grep); `test_j` asserts 139 rows (`test_review_severity_rule.py:268-272`, not re-counted here); the CLI Medium-passes test is at `test_tasklist_fidelity.py:208-226`. No test was run. The two worker-contract pins at `test_worker_contract.py:777`, `:1861` exist, and the phrase's skill-side home is `commands/tasklist.md:113` (see Concessions). |

## Per-point positions

Key: A = Variant A, B = Variant B, Hybrid = stated combination, Neither.

| Point | Position | One-line reason |
|---|---|---|
| S-001 | A | An inputs table up front lets a reader check the dependencies before the argument. |
| S-002 | A | One fact per row with its own tag is checkable; B's E1 bundles six line cites. |
| S-003 | Neither | Heading depth does not change the argument. |
| S-004 | Hybrid | Keep A's three-part split (core, module, CLI) but label the CLI part "unchanged gate, shared definitions", as B does. |
| S-005 | Hybrid | A's static tests T1-T4 plus B's pre-registered threshold (A left its threshold unset). |
| S-006 | Neither | A "Not claimed" section and B's header paragraph both state scope. |
| S-007 | B | B's stop condition ("if M-X15-1 finds most Medium are wording, the objection stands") is more useful than A's list of costs. |
| C-001 | A | Medium non-blocking; every other written Medium agrees (`qa.md:81`, `card_convert.py:81-83`, CLI gate, `PM:230`). |
| C-002 | A | S4's own exemplar maps medium to minor; B's S4 premise exists only after B's edit. |
| C-003 | Hybrid | Form 1 now (brief, grading block, T2 parity test); defer Form 2 until a tasklist lens exists (`reflect_category` cannot be reused). |
| C-004 | A | A gives definitions and moves the omission checks to High; B promises a definition and gives no text. |
| C-005 | A | B's edit is smaller but leaves nine sites that gate on a label with no definition. |
| C-006 | B | B churns no pins; A's cost is bounded: 12 rows, 2 test phrases, `commands/tasklist.md:113`. |
| C-007 | A | S2 says minor findings do not trigger a fix pass; B enlarges the regression-halt channel (SK:1610); A states its loosening. |
| C-008 | Hybrid | Leave the CLI gate, fields, exit code and guard untouched (B); share one definition text with a parity test T2 (A); defer role table and adapter. |
| C-009 | B | The shared six-field contract with `SPEC_FIDELITY_GATE` is a clean reason to leave the CLI alone; A agrees and uses the same fact. |
| C-010 | B | B has the data; A's re-reading (Strengths 4) corrects B's interpretation but does not replace the data. |
| C-011 | Hybrid | B's pre-registered 2/3 threshold applied to A's M1 (seeded defects) plus T1-T4. |
| C-012 | Neither | Boundary exposure exists under both; A's union mitigation is withdrawn. |
| C-013 | A | The CLI MEDIUM text is the only written definition; B gives none. |
| C-014 | A | A Medium that is a warning matches the rf-qa and `/sc:implement` rule; B's "same result as rf-qa" holds only for omissions, which A regrades to High. Adopt B's `card_convert.py` caution as a note. |
| X-001 | A | The S4 exemplar classes Medium as minor; neither reading is forbidden by the text, so this is a judgment, not a violation. |
| X-002 | A | B's S4 premise follows its own edit (B section 8). |
| X-003 | B | The fixture records High/Medium HALT as the intent; A contests only the framing (bucket mapping versus Medium decision). |
| X-004 | Hybrid | B on the evidence that reviewers graded omissions Medium; A on the correction of E6 (2 of 6, not most). Resolve by running M1 before adoption. |
| X-005 | B | No module-declared role table exists today. |
| X-006 | B | `PM:229` names CRITICAL/IMPORTANT/MINOR; A generalized. |
| X-007 | Neither | "Gap" and "no fixer" are both inferences; nothing on disk gives the reason. |
| X-008 | B | A's "one product" wording was loose; B's family reading is closer. |
| X-009 | B | Each task has one grader; the union mitigation does not apply. |
| X-010 | A | A's line ranges match the code (`roadmap/gates.py:195-240`, `prompts.py:51-69`); B's `:28-62` and `:195-233` cut short; A's count is `.py`-only. |

Verified in this session: SK:1340-1625; `pragmatic.md:218-233`; `qa.md` severity lines (grep); `findings.py:10-109`; `findings_v2.py:150-165`; `card_convert.py:64-91`; `tasklist/prompts.py:1-115`; `tasklist/gates.py:15-47`; `roadmap/gates.py:195-240`; both archived reports (first 50 and 40 lines); fixture header and tasklist rows; `test_worker_contract.py:770-780`, `:1855-1866`; `test_review_severity_rule.py:181-192`, `:266-284`; `test_tasklist_fidelity.py:101-108`, `:206-226`; `git show -s 80f934de5`. Not re-read: the C-01/C-02/C-03 adjudication files beyond one grep of C-02; research files; `executor.py`; `commands.py`.
