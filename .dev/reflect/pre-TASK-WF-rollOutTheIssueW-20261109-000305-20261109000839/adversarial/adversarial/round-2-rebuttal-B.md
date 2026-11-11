### Variant B Rebuttal

#### Responses to A and corrections to my Round 1

Source shorthand: `plan` and `source.md` mean the files in `.dev/tasks/to-do/TASK-WF-rollOutTheIssueW-20261109-000305/`; test paths are checkout-relative.

1. **F1: concede the acceptance blocker.** Repair size does not measure impact. Task 2's zero-miss loop (plan:65) blocks literal acceptance and Task 3 depends on Task 2 (plan:72). I withdraw my Round 1 implication that its one-line repair makes it inconsequential. A and B both recognize the defect; B's runtime evidence is not uniquely deterministic either.
2. **Coverage: correct my overstatement.** A's self-audit does check Task 1's status-line uniqueness; “A never touches Task 1” was false. B's F2 spans the owner capture handover and Task 5 verification, not Task 1's status edit. Task 5's fixture-to-consumer findings alone sustain B's coverage advantage, without claiming a complete review.
3. **QA-02: retract my source-ambiguity concession.** `source.md:22` requires “every guessed” fixture; “about 12+” is explicitly effort reasoning (:24), not an exception. The plan requires one capture per fixture (:108), then permits uncaptured fixtures (:110, :117), conflicting with its all-19 goal (:15). This is a plan inconsistency. Keep medium severity and separate the gate contradiction from the unverified coverage-matrix allegation; I do not rely on that allegation.
4. **QA-03: retain, narrowly.** Plan:110 already accommodates stderr in the existing layout, so non-`payload` files are not all equally uncovered. The decisive counterexample is `tests/issue_watch/test_github.py:562-563`, which loads the include-response fixture and passes `fixture["raw"]` to the runner. Instructions limited to replacing `payload` do not establish replacement of that consumed `raw` envelope. Name the consumed destination and capture stream; do not broaden this into a parser rewrite.
5. **QA-04: retract “no sanctioned way.”** Plan:120 allows the whole `test_github.py` file; :112 expressly directs only the metadata-test change but does not forbid other expected-value updates. The omission remains: `tests/issue_watch/test_github.py:566-568` asserts a fixed login, id and Date. A capture with a different retained Date fails that assertion; not every real capture necessarily does. Make expected-value updates explicit and distinguish them from parser-shape failures, which plan:114 sends to a follow-up.
6. **F2: agree on verification, not a proven leak.** Plan:29 retains redacted captures in the package; :78 requires redaction before handover; :118 verifies only fixtures. The instruction and the check cover different surfaces. Extend verification to retained captures without claiming a secret was found or that the token pattern proves all private identifiers absent. Continue staging task artifacts.
7. **F3–F5 and calibration: accept A's corrections.** Plan:96 already means two schedule occurrences, so F3 is clarification, not a defect. F5 is navigation advice; retain F4 only as the low-severity section-map omission, not a Task 4 blocker. B's missing self-audit, mixed IDs and larger confidence gap remain weaknesses; consequential findings do not validate the original high QA-02 grade.
8. **Shared assumptions: qualify rather than invent coverage.** Plan:23 anticipates shifted fixture citations and requires new text to cite sections/rows. Plan:20-22 preserves the false configuration and owner-only live actions/record. Neither card validates Task 3 as a whole; its builder and preservation criteria (plan:82, :85) remain outside this rebuttal's validation scope.

#### Final positions

Moved? is relative to my Round 1 table; changed reasoning alone is noted separately.

| Diff Point | Superior | Moved? | Reason |
|---|---|---|---|
| S-001 | A | No | Checked-negative self-audit evidence beats a plan-path note, but proves neither completeness nor Task 5 coverage. |
| S-002 | A | No | Consistent IDs marginally ease reconciliation; this is presentation, not substantive correctness. |
| S-003 | B | No | QA-03/04 have consequential fixture/test effects; this does not defend QA-02's original high severity. |
| C-001 | B | No | Task 5 coverage wins on consequences; retract the claim that A never checks Task 1. |
| C-002 | A | Yes, from TIE | F1 is an explicit impossible acceptance check; F2 is a missing verification gate, not an established leak. Discarding F3 does not erase F1. |
| C-003 | B | No | The consumed `raw` field and fixed expected Date connect the instruction gap to concrete test behavior. |
| C-004 | A | No | A's smaller calibration gap remains a relative advantage; B's confidence and bundled high finding were overstated. |
| A-001 | TIE | No; rationale corrected | Verified findings fit plan-gap; the effort estimate does not demonstrate a source defect or weaken “every.” |
| A-002 | TIE | No | Snapshot citations require refreshing after edits; plan:23 already anticipates the shift. Neither card is immune. |
| A-003 | TIE | No | Both preserve owner-only live actions and the false configuration; neither establishes runtime execution evidence. |
| A-004 | TIE | No | Both leave Task 3 without a full review; absence of a finding is not proof its acceptance criteria are sound. |
