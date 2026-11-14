# Round 1: Advocate for Variant 1 (Proposal A, "keep the questions read off and park the live tests")

Mode A, depth quick, Round 1. Sources checked this round: `merged-requirements.md` (MR) lines 230-265, 528-537, 598-607, 975-1004, 1150-1161; `alignment-findings-adjudicated.md` (ADJ) lines 170-200, 330-334, 760-817; the three variants, `diff-analysis.md` and `question.md`. The code line `observe/commands.py:63-67` was not re-read by me; it is taken from `question.md` and MR:234 (UNVERIFIED by this advocate).

## 1. Position summary

Proposal A is the lowest-risk answer: it keeps the guard off, writes no seeded messages and makes the program independent of a live Orca app, and it is the only variant whose outcome is the same whether or not anyone needs the panel soon. Its main weakness, conceded below, is that its re-open trigger ("release 3 is opened") cannot fire on its own, because release 3 is itself blocked by the flip it parks.

## 2. Steelman of each opposing variant

**Proposal B (scope now: "any Run my terminal holds"; build the flip in parallel).** The strongest form of B: the only Run the owner's pass names, `run_93bfa00cae2b`, is an old "Claim issue 375" Run (ADJ:192, INV-003; MR:235), so a "this Run only" flip gives a panel that works for no live Run. Q-1 failed, so only the holder terminal can read a Run's questions at all (MR:239, INV-024); "any Run my terminal holds" therefore names the only access path Orca offers, not a widening. Writing that sentence now costs nothing if the seeded test fails (the PR is closed unmerged, as B says), and it saves a second owner round trip. B keeps every safety prerequisite: it still refuses to merge before OB-03, OB-04 and OB-05 (B line 11), which matches A-001 (all three refuse a flip before the seeded test).

**Proposal C (test now, scope after the evidence).** The strongest form of C: it is the spec's own recommended answer, almost word for word. MR:533 says "do not flip before the seeded test; the scope sentence is the owner's", and ADJ:776 says "after it, the scope sentence is yours". C runs OB-03 now, so X-016 (unproven both ways at 61 percent, ADJ:333) gets its first diagnostic evidence, and it keeps the owner's choice open until OB-04 shows whether the panel is even usable, which is exactly the case the stop rule at MR:1001 ("hold OB-06; ask the owner whether to narrow scope") was written for. C also carries the explicit stop rule from MR:1000 (U-003).

## 3. Strengths claimed

1. **It is the safe state the spec already falls back to.** MR:533 (default column): "ADJ: guard stays off"; MR:979: "no answer to Q6 means the guard stays off"; MR:254: "Default if Q6 is unanswered: the guard stays off and this PR is not opened." A makes that default a deliberate, dated choice with a named trigger, instead of an unanswered question.
2. **It removes the live-Orca lane dependency from W1.** MR:604 defines ORCA-AVAILABLE and says "Every live lane needs it: ... OB-03, OB-04"; "The probe found the app not reachable on 2026-11-13". OB-03 is also blocked by Q24, LIVE, TB-CONSUME, XC-10 and its own grant row (MR:251); OB-04 by Q30, LIVE and its own grant row, and "if no such Run exists, OB-04 is held and OB-06 waits" (MR:252). A deletes all of those edges from the current program at once.
3. **Zero chance of losing a coordinator question.** X-016 is unproven both ways (ADJ:333). The sufficiency table says a seeded pass does not cover a live Run's `--wait` listeners and acknowledge cycle (MR:1156; ADJ:174). OB-04 deliberately runs the read inside a live coordinator's holder terminal (MR:252). That is a live risk to a real mailbox that A never takes.
4. **No outward writes and no new permission rows.** OB-03 writes seeded messages to a throwaway Run (MR:251, MR:984 "except OB-03's seeded writes"), and each needs a `GRANT(OB-03,seeded-write)` or `GRANT(OB-04,live-read)` row (MR:607). A needs none.
5. **The evidence would be fresh when it is used.** A-009 / OB-05 exist because a different Orca build may change `--all` (MR:1156). Running OB-03 now and flipping much later relies on the build pin; running it when the panel is actually needed tests the build then in use.
6. **No commitment ahead of evidence.** Like C and unlike B, A asks for no scope sentence before X-016 has any evidence; the scope question is asked again when it matters (A line 5).

## 4. Weaknesses identified in the others

1. **B commits to the widest scope before any evidence, against the debate record.** ADJ Part 8 (line 814) lists "recommend scope 'any Run the terminal holds' now (V5 D5(ii))" among rejected proposals; ADJ:776 notes that recommendation "was withdrawn". B concedes this itself (B line 24).
2. **B's enforcement test rests on an unestablished mechanism.** B requires code that refuses "a Run the terminal does not hold" without `run-use` (MR:984 forbids `run-use` on a live coordinator), and B itself marks the holder detection UNVERIFIED (B line 22; diff-analysis C-004). 28 of 53 Runs have no holder (MR:239). OB-06 (a) needs "a test shows a Run outside scope is refused" (MR:254); B has no shown way to write that test.
3. **B spends build work before the test that can cancel it.** B line 23: "may be wasted work if the test fails". OB-06 is a worker plus a PR session plus a `/sc:pr-submit --monitor 3` grant (MR:254); that is not small.
4. **C still carries every live dependency A removes.** C line 23 concedes Orca reachability, Q24, Q30 and permission rows. If the app stays unreachable or no disposable representative Run exists (MR:252 (4)), C ends exactly where A starts, but with a W1 lane held open.
5. **C asks the owner twice.** C line 21: "A second owner question later ... adding one round of owner latency."
6. **Both B and C still take the live-mailbox risk in OB-04**, which the spec itself says the seeded test cannot rule out (MR:1156).

## 5. Concessions

1. **The re-open trigger is circular.** A parks until "release 3 is opened". But OB-09 (release 3, Decision Desk) lists OB-06 in its blocked-by column and its acceptance says "a release 3 package cites OB-02, OB-06 and the QUESTION-LINK record" (MR:257). Release 3 cannot open while OB-06 is parked, so under A the trigger never fires by itself. A would need a different trigger (for example "the owner names a near-term user of the panel" or "Q19 picks Decision Desk").
2. **A works against the stated target state.** MR:242: the target state includes "the questions read is switched on only for the scope the owner wrote, after a seeded consumption test, a live-layout attempt and a build pin". ADJ:192 action 4 "Unblocks: a usable questions panel". A defers that part of the target state out of the program.
3. **X-016 stays open, and with it two unverified cautions.** ADJ:333 names the seeded test as the next step; MR:261 makes Q10 depend on OB-03. A leaves the sweep's caution and the observer's caution both resting on no evidence (A line 22).
4. **The evidence-loss argument (U-001) is weaker than A states.** OB-01 blocks OB-08 as well as OB-06 (MR:249), so OB-01 still has a reason to run under A. A's parking removes one reason to commit the sibling records, not the only one.
5. **Parking does not remove the scope problem.** The pass names one old Run (ADJ:192); whoever reopens it faces the same question with the same lack of evidence.
6. **A answers "flip before the seeded test?" by refusing both the flip and the test**, which the spec default does not ask for: the default is "do not flip before the seeded test", not "do not run the seeded test" (MR:533, ADJ:776).

## 6. Shared assumptions

- **A-003 (a near-term user of the questions panel exists): QUALIFY.** No variant cites evidence of near-term demand, and A's answer is right only if there is none. The sources do show the program presumes an eventual user: the target state includes the switch-on (MR:242), release 3 depends on OB-06 (MR:257), and Q19's recommended answer is "Fleet Quilt or Decision Desk first" (ADJ:789). Whether "eventual" means this program or later is the owner's knowledge, not something the files settle.
- **A-004 (evidence on one build carries until the build changes, and OB-05 catches the change): QUALIFY.** OB-05 (2) does specify "a build check or a test fails when the build string changes" (MR:253), so a change is detected. But detection is not re-validation: after a failed build check, the seeded test must be re-run, and the spec does not say who re-runs it. A second host stays UNVERIFIED (MR:986). The assumption holds for a short W1-to-W2 gap on one host; it weakens the longer the gap.

## 7. Per-point positions

| Point | Better approach | Confidence | Reason |
|---|---|---|---|
| S-001 | Tie (A named) | 50% | All three use the same five sections; no difference of substance. |
| C-001 (does OB-03 run now?) | C | 65% | The seeded test is the only route to X-016 evidence (ADJ:333) and writes only to a throwaway Run; A's parking is defensible only if no user exists. |
| C-002 (when is scope given?) | C | 75% | Matches MR:533 and ADJ:776 and the MR:1001 stop rule; B's early scope is the rejected V5 D5(ii) (ADJ:814). |
| C-003 (when is OB-06 built?) | C | 70% | Built once, after the evidence and the sentence; B risks wasted work, A never builds it. |
| C-004 (how scope is enforced) | C | 75% | C's test works for either sentence; B's "held by this terminal" detection is UNVERIFIED and constrained by the `run-use` ban (MR:984). |
| C-005 (live Orca, Q24, Q30 dependence) | A | 70% | A alone removes the ORCA-AVAILABLE, Q24, Q30 and grant-row edges (MR:251-252, MR:604). |
| X-001 (scope before evidence?) | C | 75% | Evidence first, owner's sentence second, is the spec's own design; B commits blind, A defers the question entirely. |
| X-002 (build flip before test?) | C | 65% | No wasted build, no indefinite park. |
| A-003 (near-term user exists) | C | 55% | C is robust either way: it buys the evidence cheaply and lets the owner decline the flip; A is best only under "no user". |
| A-004 (build evidence carries) | A | 55% | A tests on the build in use when the panel is needed; B and C rely on OB-05 detecting drift across the W1-to-W2 gap. |

## 8. Overall verdict

The owner should pick **Proposal C**, confidence **70 percent**: it is the spec's recommended answer (MR:533, ADJ:776), gets the first evidence on X-016 without committing to a scope, and keeps "no flip" available after the evidence; A is the right fallback only if the owner knows no one will use the panel soon, and then it needs a trigger other than "release 3 is opened" (MR:257 makes that trigger circular).
