# Round 2: Variant 1 advocate rebuttal (haiku:analyzer; agent id adcff8e824f153068)

Persisted by the orchestrator from the hand-back.

## Replies to Variant 2's criticisms
1. F2 too narrow: concede coverage, qualify consequence. SPEC:853 includes "494, 548", but rf-qa.md:548 "When in doubt, fail it" is not by itself proof of incorrect blocking: SPEC:201 says "Unknown is not no" and SPEC:211 preserves an unknown-consumer IMPORTANT as blocking. Round 1 steelman overstated this contradiction.
2. "Checked and sound" overclaims: concede the scorer (zero-trust test:95, :118-119 returns FAIL from labels alone; PLAN:203 changes bullet strings only). Reject the quota allegation as an independent defect: PLAN:192 says the prompt-override test "must still pass unchanged".
3. Baseline F7: concede the omission. S2:138 produces the M6 share; PLAN:230 asks each baseline "from Task 2". M6 needs carrying forward.
4. All findings "Drift": category and consequence are separate; Variant 1 supplies both.

## Settled open points
- (a) qualitative:810 only says "flag this as a systemic problem"; :805 limits FAIL to an open blocking finding: weak. :796 "blocking (CRITICAL or IMPORTANT)" is stale label shorthand worth correcting but starts from already-blocking issues. rf-qa:548 is overbroad wording, not decisive; SPEC:201-211 expressly permits some uncertainty to remain blocking.
- (b) Variant 2 F3 is minor: PLAN:76 says "the same brief"; :78 supplies the installed old style to both arms.
- (c) F6 (missing "never rechecked") is a real preservation loss: SPEC:274; PLAN:125 removes the bullet; SPEC:203 forbids fix passes and reviser briefs but not later rechecking. Merits blocking.
- (d) No demonstrated PLAN:28 violation: Task 6's acceptance lines :143-148 concern rewritten text, registry state, tokens and a registry test.
- (e) F1 (gate after edit) is weaker than claimed: PLAN:20 expressly requires the gate; :128 says it does not rely on Depends on; the executor reads global constraints before execution (SKILL:129); retry:109 covers only "procedure steps 3-5".

## Updated assessment
| Diff point | Superior | Conf % | Blocking or minor | Evidence |
|---|---|---:|---|---|
| S-001 | 1 | 98 | Minor | Category and blocking fields convey different facts. |
| C-001 | 2, qualified | 87 | Blocking core | Rule 8 remains overbroad; SPEC:211 weakens the doubt argument. |
| C-002 | 2 | 97 | Minor | Scorer still uses labels; PLAN:192 protects the quota test. |
| C-003 | 2 | 98 | Minor | S2:138 produces M6, omitted from Task 2. |
| X-001 | 2, qualified | 85 | Minor | PLAN:20 supplies a global gate. |
| X-002 | 2 | 99 | Minor | Qualitative:983 starts the hash block after the verdict pairs. |
| U-001 | 2, qualified | 85 | Minor | retry:109 does not prove this gate leaves edits behind. |
| U-002 | 1 | 98 | Blocking | PLAN:78 reports both variants without selecting which controls :82. |
| U-003 | 1 | 99 | Minor | PLAN:214 contradicts revision2:16. |
| U-004 | 2, qualified | 94 | Minor | PLAN:76-78 preserves the common brief and injected style. |
| U-005 | 2 | 91 | Minor | PLAN:144 checks a narrower inventory than :140's named edits. |
| U-006 | 1 | 97 | Minor, drop | PLAN:192 requires the quota test unchanged. |
| U-007 | 2 | 86 | Minor | PLAN:43 leaves blockquote normalization unclear. |
| U-008 | 2 | 98 | Blocking | SPEC:274's no-rechecking requirement is not restored by :125. |
| U-009 | 2 | 98 | Minor | PLAN:230 overlooks M6's producer. |
| U-010 | 2 | 98 | Minor | Zero-trust:118-119 derives FAIL from labels alone. |
| U-011 | 1 | 97 | Minor, drop | Tasks 10-11 do not invalidate Task 6's acceptance lines. |
| U-012 | 2 | 93 | Minor | README:11 omits fields required by SRC:41. |
