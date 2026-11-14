# Round 1 statement: advocate for variant 3 (proposal C)

Debate: Q6, scope and timing of switching on the observer's coordinator-questions read. Mode A, depth quick, Round 1.

Abbreviations: M = `.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md`; ADJ = `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md`. Every line number below was re-read on 2026-11-14 for this statement.

## 1. Position summary

Run the seeded consumption test (OB-03), the one live-layout attempt (OB-04) and the build pin (OB-05) now, in W1, and have the owner write the scope sentence only after reading those records; open the flip pull request (OB-06) in W2. This is the spec's own default for Q6 (ADJ:776), and it is the only variant that both produces evidence on the open consumption question and avoids committing to a scope before that evidence exists.

## 2. Steelman of each opposing variant

**Variant A (park everything until release 3).** The strongest case for A: the guard is already off and costs nothing to leave off (M:233, "Guard off: `QUESTION_GATE_PASSED = False`"); the program has no evidence that anyone needs the panel now (diff-analysis A-003: "no variant cites evidence of demand"); the live lanes depend on an Orca app that was not reachable on 2026-11-13 (M:604) and on two more owner answers (Q24, Q30) plus two permission rows. OB-03 writes seeded messages into a Run, which is an outward action the spec gates separately (M:575, "OB-03 needs `GRANT(OB-03,seeded-write)`"). Parking removes all of that risk and all of that coordination, and the question is re-asked when a real consumer (release 3, Decision Desk) exists, at which point the Orca build will have moved anyway and fresh evidence would be needed regardless (OB-05's build pin, M:253). A is the cheapest correct answer if the panel truly has no near-term user.

**Variant B (scope "any Run my terminal holds" now, build the flip in parallel).** The strongest case for B: Q-1 failed, so only the terminal that holds a Run can read its questions (M:239; ADJ:465 INV-024). "Any Run my terminal holds" is therefore not a widening in practice; it is the only access path Orca gives. The pinned Run `run_93bfa00cae2b` is an old "Claim issue 375" Run (ADJ:458 INV-003), so "this Run only" gives a flip that works for nobody (diff-analysis U-002, rated High). Given that, deferring the sentence only buys a second round of owner latency for a choice whose answer is already forced. B also keeps every safety gate: the PR stays unmerged until OB-03, OB-04 and OB-05 records are linked, and is closed if OB-03 shows consumption. The parallel build turns W2 into a merge step instead of a build step.

## 3. Strengths claimed

1. **It is the spec's recommended answer, verbatim.** ADJ:776: "Default (no debate verdict): do not flip before the seeded test; after it, the scope sentence is yours; no answer means the guard stays off." M:533 carries the same default and assigns "W1 (test), W2 (flip)", which is exactly C's wave plan. Neither A nor B matches that row.
2. **It gets the first diagnostic evidence on X-016.** X-016 is "UNRESOLVED ... UNPROVEN BOTH WAYS" at 61 percent (ADJ:333), and the owner's own measurement is non-diagnostic (ADJ:813). C runs OB-03 in W1, so both the observer's caution and the sweep's caution stop being unverified claims (ADJ:333 action column: "seeded test ... cite the help text, pin the build"). A leaves X-016 open indefinitely.
3. **The scope choice is made on evidence, including the usability evidence that decides it.** OB-04 records "whether any question disappeared, and whether the panel was usable" (M:252). The spec's own failure table reacts to those outcomes: OB-03 missing a message means "stop OB-06; record 'consumes'" (M:1000); OB-04 unusable means "hold OB-06; ask the owner whether to narrow scope" (M:1001). The sufficiency table says OB-06 alone may not give a usable panel because "28 of 53 Runs have no `coordinator_handle`" and "OB-04's record decides" (M:1157). C puts the owner's sentence after the record that decides it.
4. **It honours ADJ's "Do not" list exactly.** ADJ:195: "flip the guard before action 4 (a) and (b)". ADJ:814 lists "recommend scope 'any Run the terminal holds' now (V5 D5(ii))" as a change *not being made*, with the reason that "the seeded consumption test, the live-layout attempt, the build pin and the owner's own scope sentence are prerequisites". C is the only variant consistent with both lines.
5. **It does not depend on an unverified holder-detection mechanism at decision time.** OB-06 (a) requires "a test shows a Run outside scope is refused" (M:254). C's enforcement is "whichever sentence the owner writes" (diff-analysis C-004), so the code is written once, against a known sentence. B commits to "held by this terminal" now while B itself marks how the observer detects holding without `run-use` as UNVERIFIED; the observer never runs `run-use` (ADJ:465 INV-024), and `run-use` on a live coordinator is "forbidden for the observer" (ADJ:459 INV-005).
6. **No wasted build if OB-03 fails.** If OB-03 shows any seeded message missing, OB-06 stops (M:1000). C writes no flip code before that is known; B accepts "may be wasted work" as a cost.

## 4. Weaknesses identified in the others

**Variant A**

1. **It leaves the central fact unresolved with no end date.** X-016 stays at 61 percent "unproven both ways" (ADJ:333); both programs keep unverified cautions. A's own "What stays unresolved" admits this.
2. **It works against owner intent on record.** The owner gave a 2026-11-12 pass and a "Do it" record (ADJ:814 refers to flipping "on the owner's 'Do it' record alone"; M:235 the pass record). That is the owner signalling the panel is wanted; A re-asks a question the owner has already partly answered. (The full text of the "Do it" record was not opened here; UNVERIFIED beyond the ADJ:814 quote.)
3. **It raises evidence-loss risk.** A itself notes that parking removes one reason to commit the sibling-only records (Q7), which "exist only in the sibling worktree `issue-409-mvp`" (M:235), and the two switch-on commits keep ageing against master (M:234).
4. **Its trigger is weak.** "Release 3 is opened" is a future event the program does not control; Decision Desk is "release 3, gated" (ADJ:187). Nothing guarantees the question is ever re-asked.

**Variant B**

1. **It commits to a scope against an explicit adjudicated "not being made" decision.** ADJ:814 names "recommend scope 'any Run the terminal holds' now (V5 D5(ii))" as rejected; ADJ:776 notes V5 D5(ii) "was withdrawn". B has no debate verdict behind it.
2. **Its enforcement test is unspecified.** "A test refuses a Run the terminal does not hold" needs the observer to know which Run the terminal holds. B marks this UNVERIFIED; the only verb I can see the spec name for that is `run-current` (M:251 records it before and after in OB-03), and whether the observer may call it in normal operation is not settled here (UNVERIFIED). Q6's pass "does not authorize `run-use` or mailbox writes in normal observer operation" (M:573).
3. **The "matches the only access path" argument is weaker than it looks.** If Orca already refuses non-holder reads (Q-1 FAIL), then "any Run my terminal holds" adds no restriction the code must enforce beyond what Orca does, and OB-06 (a) needs the code to enforce it anyway (M:254). It also says nothing about consumption: holder terminals are exactly the ones with live `--wait` listeners and an ack cycle that a throwaway Run lacks (M:1156). The wide scope points the read at the riskiest Runs before that risk is measured.
4. **Parallel build can be wasted work** if OB-03 fails (M:1000) or OB-04 shows the panel unusable (M:1001), and the PR's scope test would have to be rewritten if the owner later narrows.

## 5. Concessions

1. **B's U-002 point is largely right.** `run_93bfa00cae2b` is an old "Claim issue 375" Run (ADJ:458). Whether it still has a holder terminal is UNVERIFIED, but "this Run only" is very likely a flip of little practical use. So C's deferred choice is in practice between "any Run my terminal holds" and "no flip", not between two useful scopes. Deferral buys less than C's text implies.
2. **The spec's own failure row assumes a scope may already be wide.** M:1001 says on an unusable panel "ask the owner whether to narrow scope", which reads as if a wider scope could be stated before OB-04. The spec does not forbid an early sentence; it only says the sentence is the owner's (ADJ:776).
3. **C costs one extra owner round** (the scope sentence in W2) and keeps the panel dark longer than B.
4. **C keeps every live dependency A removes:** Orca reachable (M:604, not reachable on 2026-11-13), Q24, Q30, and the permission rows `GRANT(OB-03,seeded-write)` and `GRANT(OB-04,live-read)` (M:251-252). If those stay unresolved, C degrades to A in effect (OB-04 "is held and OB-06 waits", M:252) without A's clean ledger entry.
5. **C is necessary-not-sufficient evidence, like B.** One disposable Run in OB-04 says nothing about every other live Run (M:1156); C does not close that gap either.

## 6. Shared assumptions

- **A-003 (a near-term user of the questions panel exists): QUALIFY.** No variant cites direct demand, as the diff analysis says. But there is indirect evidence: the owner recorded a pass on 2026-11-12 (M:235) and a "Do it" record that ADJ:814 declines to treat as sufficient for a flip, which only makes sense if the owner wanted the flip; ADJ Part 2.1 action 4 lists "Unblocks: a usable questions panel" (ADJ:192). That supports "some owner demand", not "a named regular user". C's W1 tests are worth running on that basis; if the owner says there is no user, A becomes the better answer.
- **A-004 (evidence on one build carries until the build changes, and OB-05 catches the change): QUALIFY.** OB-05 does require "a build check or a test fails when the build string changes" (M:253), so the build axis is covered by design. But the assumption is incomplete: evidence can be invalidated without a build change, because a live Run's `--wait` listeners and ack cycle differ from the throwaway Run (M:1156). The ADJ A-009 "67 percent" figure quoted in the diff analysis was not opened here (UNVERIFIED). Both B and C rely on OB-04 to cover the non-build axis, and C is slightly better placed because the scope sentence is written after OB-04's record.

## 7. Per-point positions

| Point | Better variant | Confidence | Reason |
|---|---|---|---|
| S-001 | none (C named as tie) | 50% | The three share the same five sections; no structural edge. |
| C-001 | C (equal with B) | 80% | Running OB-03 is the only path to resolving X-016 (ADJ:333); A leaves it open. |
| C-002 | C | 65% | Matches ADJ:776 and M:533; concession 1 lowers confidence because the narrow option is weak. |
| C-003 | C | 60% | Avoids building before OB-03 (M:1000); B's time saving is real if the test passes. |
| C-004 | C | 65% | Scope test written against a known sentence; B's holder detection is UNVERIFIED. |
| C-005 | A | 75% | A alone removes the dependence on live Orca, Q24, Q30 and two grants (M:604, M:251-252). |
| X-001 | C | 65% | ADJ:814 rejects choosing the wide scope now; OB-04 decides usability (M:1157). |
| X-002 | C | 60% | Building before the test is avoidable waste; small PR, so B's gain is modest. |
| A-003 | C (equal with B) | 55% | Indirect owner demand exists (M:235, ADJ:814); A assumes none. |
| A-004 | C | 55% | Both rely on OB-05 for builds; C sets scope after OB-04, which covers the non-build axis. |

## 8. Overall verdict

The owner should pick **variant C**, confidence **70 percent**: it is the spec's own default (ADJ:776, M:533), it is the only answer that both produces evidence on the unresolved consumption question and respects ADJ's rejection of an early wide scope (ADJ:814). If the owner already knows the answer will be "any Run my terminal holds" and accepts possibly wasted build work, B is a reasonable second; if the owner says no one needs the panel this program, A is right.
