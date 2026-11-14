# Adversarial Debate Transcript: Q6 owner-answer proposals

## Metadata
- Depth: quick
- Rounds completed: 1 (Round 2 skipped: depth=quick; Round 2.5 invariant probe skipped: --depth quick; Round 3 skipped: depth=quick)
- Convergence achieved: 100% (10 of 10 points agreed by at least 2 of 3 advocates; 6 unanimous)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 3 (spawned in parallel as separate agents; each wrote its own file: round1-advocate-A.md, -B.md, -C.md)
- Variant mapping: variant-1 = proposal A, variant-2 = proposal B, variant-3 = proposal C

## Round 1: Advocate Statements

### Advocate for proposal A (source file: round1-advocate-A.md)

## Round 1: Advocate for Variant 1 (Proposal A, "keep the questions read off and park the live tests")

Mode A, depth quick, Round 1. Sources checked this round: `merged-requirements.md` (MR) lines 230-265, 528-537, 598-607, 975-1004, 1150-1161; `alignment-findings-adjudicated.md` (ADJ) lines 170-200, 330-334, 760-817; the three variants, `diff-analysis.md` and `question.md`. The code line `observe/commands.py:63-67` was not re-read by me; it is taken from `question.md` and MR:234 (UNVERIFIED by this advocate).

### 1. Position summary

Proposal A is the lowest-risk answer: it keeps the guard off, writes no seeded messages and makes the program independent of a live Orca app, and it is the only variant whose outcome is the same whether or not anyone needs the panel soon. Its main weakness, conceded below, is that its re-open trigger ("release 3 is opened") cannot fire on its own, because release 3 is itself blocked by the flip it parks.

### 2. Steelman of each opposing variant

**Proposal B (scope now: "any Run my terminal holds"; build the flip in parallel).** The strongest form of B: the only Run the owner's pass names, `run_93bfa00cae2b`, is an old "Claim issue 375" Run (ADJ:192, INV-003; MR:235), so a "this Run only" flip gives a panel that works for no live Run. Q-1 failed, so only the holder terminal can read a Run's questions at all (MR:239, INV-024); "any Run my terminal holds" therefore names the only access path Orca offers, not a widening. Writing that sentence now costs nothing if the seeded test fails (the PR is closed unmerged, as B says), and it saves a second owner round trip. B keeps every safety prerequisite: it still refuses to merge before OB-03, OB-04 and OB-05 (B line 11), which matches A-001 (all three refuse a flip before the seeded test).

**Proposal C (test now, scope after the evidence).** The strongest form of C: it is the spec's own recommended answer, almost word for word. MR:533 says "do not flip before the seeded test; the scope sentence is the owner's", and ADJ:776 says "after it, the scope sentence is yours". C runs OB-03 now, so X-016 (unproven both ways at 61 percent, ADJ:333) gets its first diagnostic evidence, and it keeps the owner's choice open until OB-04 shows whether the panel is even usable, which is exactly the case the stop rule at MR:1001 ("hold OB-06; ask the owner whether to narrow scope") was written for. C also carries the explicit stop rule from MR:1000 (U-003).

### 3. Strengths claimed

1. **It is the safe state the spec already falls back to.** MR:533 (default column): "ADJ: guard stays off"; MR:979: "no answer to Q6 means the guard stays off"; MR:254: "Default if Q6 is unanswered: the guard stays off and this PR is not opened." A makes that default a deliberate, dated choice with a named trigger, instead of an unanswered question.
2. **It removes the live-Orca lane dependency from W1.** MR:604 defines ORCA-AVAILABLE and says "Every live lane needs it: ... OB-03, OB-04"; "The probe found the app not reachable on 2026-11-13". OB-03 is also blocked by Q24, LIVE, TB-CONSUME, XC-10 and its own grant row (MR:251); OB-04 by Q30, LIVE and its own grant row, and "if no such Run exists, OB-04 is held and OB-06 waits" (MR:252). A deletes all of those edges from the current program at once.
3. **Zero chance of losing a coordinator question.** X-016 is unproven both ways (ADJ:333). The sufficiency table says a seeded pass does not cover a live Run's `--wait` listeners and acknowledge cycle (MR:1156; ADJ:174). OB-04 deliberately runs the read inside a live coordinator's holder terminal (MR:252). That is a live risk to a real mailbox that A never takes.
4. **No outward writes and no new permission rows.** OB-03 writes seeded messages to a throwaway Run (MR:251, MR:984 "except OB-03's seeded writes"), and each needs a `GRANT(OB-03,seeded-write)` or `GRANT(OB-04,live-read)` row (MR:607). A needs none.
5. **The evidence would be fresh when it is used.** A-009 / OB-05 exist because a different Orca build may change `--all` (MR:1156). Running OB-03 now and flipping much later relies on the build pin; running it when the panel is actually needed tests the build then in use.
6. **No commitment ahead of evidence.** Like C and unlike B, A asks for no scope sentence before X-016 has any evidence; the scope question is asked again when it matters (A line 5).

### 4. Weaknesses identified in the others

1. **B commits to the widest scope before any evidence, against the debate record.** ADJ Part 8 (line 814) lists "recommend scope 'any Run the terminal holds' now (V5 D5(ii))" among rejected proposals; ADJ:776 notes that recommendation "was withdrawn". B concedes this itself (B line 24).
2. **B's enforcement test rests on an unestablished mechanism.** B requires code that refuses "a Run the terminal does not hold" without `run-use` (MR:984 forbids `run-use` on a live coordinator), and B itself marks the holder detection UNVERIFIED (B line 22; diff-analysis C-004). 28 of 53 Runs have no holder (MR:239). OB-06 (a) needs "a test shows a Run outside scope is refused" (MR:254); B has no shown way to write that test.
3. **B spends build work before the test that can cancel it.** B line 23: "may be wasted work if the test fails". OB-06 is a worker plus a PR session plus a `/sc:pr-submit --monitor 3` grant (MR:254); that is not small.
4. **C still carries every live dependency A removes.** C line 23 concedes Orca reachability, Q24, Q30 and permission rows. If the app stays unreachable or no disposable representative Run exists (MR:252 (4)), C ends exactly where A starts, but with a W1 lane held open.
5. **C asks the owner twice.** C line 21: "A second owner question later ... adding one round of owner latency."
6. **Both B and C still take the live-mailbox risk in OB-04**, which the spec itself says the seeded test cannot rule out (MR:1156).

### 5. Concessions

1. **The re-open trigger is circular.** A parks until "release 3 is opened". But OB-09 (release 3, Decision Desk) lists OB-06 in its blocked-by column and its acceptance says "a release 3 package cites OB-02, OB-06 and the QUESTION-LINK record" (MR:257). Release 3 cannot open while OB-06 is parked, so under A the trigger never fires by itself. A would need a different trigger (for example "the owner names a near-term user of the panel" or "Q19 picks Decision Desk").
2. **A works against the stated target state.** MR:242: the target state includes "the questions read is switched on only for the scope the owner wrote, after a seeded consumption test, a live-layout attempt and a build pin". ADJ:192 action 4 "Unblocks: a usable questions panel". A defers that part of the target state out of the program.
3. **X-016 stays open, and with it two unverified cautions.** ADJ:333 names the seeded test as the next step; MR:261 makes Q10 depend on OB-03. A leaves the sweep's caution and the observer's caution both resting on no evidence (A line 22).
4. **The evidence-loss argument (U-001) is weaker than A states.** OB-01 blocks OB-08 as well as OB-06 (MR:249), so OB-01 still has a reason to run under A. A's parking removes one reason to commit the sibling records, not the only one.
5. **Parking does not remove the scope problem.** The pass names one old Run (ADJ:192); whoever reopens it faces the same question with the same lack of evidence.
6. **A answers "flip before the seeded test?" by refusing both the flip and the test**, which the spec default does not ask for: the default is "do not flip before the seeded test", not "do not run the seeded test" (MR:533, ADJ:776).

### 6. Shared assumptions

- **A-003 (a near-term user of the questions panel exists): QUALIFY.** No variant cites evidence of near-term demand, and A's answer is right only if there is none. The sources do show the program presumes an eventual user: the target state includes the switch-on (MR:242), release 3 depends on OB-06 (MR:257), and Q19's recommended answer is "Fleet Quilt or Decision Desk first" (ADJ:789). Whether "eventual" means this program or later is the owner's knowledge, not something the files settle.
- **A-004 (evidence on one build carries until the build changes, and OB-05 catches the change): QUALIFY.** OB-05 (2) does specify "a build check or a test fails when the build string changes" (MR:253), so a change is detected. But detection is not re-validation: after a failed build check, the seeded test must be re-run, and the spec does not say who re-runs it. A second host stays UNVERIFIED (MR:986). The assumption holds for a short W1-to-W2 gap on one host; it weakens the longer the gap.

### 7. Per-point positions

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

### 8. Overall verdict

The owner should pick **Proposal C**, confidence **70 percent**: it is the spec's recommended answer (MR:533, ADJ:776), gets the first evidence on X-016 without committing to a scope, and keeps "no flip" available after the evidence; A is the right fallback only if the owner knows no one will use the panel soon, and then it needs a trigger other than "release 3 is opened" (MR:257 makes that trigger circular).

### Advocate for proposal B (source file: round1-advocate-B.md)

## Round 1: Advocate for variant 2 (proposal B)

Debate: Q6 owner-answer proposals, sc:adversarial Mode A, depth quick, Round 1.
Abbreviations: MR = `.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md`; ADJ = `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md`. Line numbers below were re-read on 2026-11-14.

### 1. Position summary

The owner should write the scope sentence now, "any Run my terminal holds", because it is the only scope that matches how Orca lets anyone read a Run's questions (Q-1 failed), while keeping every evidence gate before the flip merges. The strongest part of B is the scope choice; its weakest part is building the flip pull request in W1, which I concede below.

### 2. Steelman of each opposing variant

**Variant 1 (A, park everything).** Nothing reads any mailbox, so no coordinator question can be lost; the X-016 consumption question is unproven both ways at 61 percent (ADJ:333), and a Run's questions are the one place where a silent loss hurts. Parking also removes two live Orca lanes from W1 at a time the Orca app was not reachable (MR:604, "The probe found the app not reachable on 2026-11-13") and removes the Q24 and Q30 dependencies. If no one needs the panel before release 3, paying for live tests now is cost without a user.

**Variant 3 (C, evidence first, scope after).** It is the spec's own default and ADJ's: "do not flip before the seeded test; after it, the scope sentence is yours" (ADJ:776; MR:533). It keeps the owner uncommitted until OB-03 and OB-04 records exist, so if the live attempt shows the panel unusable or lossy the owner can pick the narrow scope or no flip at all (MR:1001, "hold OB-06; ask the owner whether to narrow scope"). It keeps the work-item order the spec already wrote: OB-06 is blocked by OB-01, OB-03, OB-04, OB-05 and others (MR:254) and sits in W2 (MR:533). It also honours ADJ's rejection of recommending "any Run the terminal holds" now (ADJ:814).

### 3. Strengths claimed

1. **"Any Run my terminal holds" is the only scope with a practical use.** The pass record names one Run, `run_93bfa00cae2b`, an old "Claim issue 375" Run (ADJ:458, INV-003; MR:235). "This Run only" therefore yields a flip that reads a Run nobody watches (diff-analysis U-001 rates this observation High).
2. **The scope matches the only access path Orca gives.** Q-1 ("an unbound terminal cannot read another terminal's Run") failed on 2026-11-11 (MR:239; ADJ:465, INV-024: "only the terminal holding the Run can read"). A scope wider than "held by this terminal" would not work; a narrower one is the old Run above. The evidence OB-03 and OB-04 produce does not discriminate between the two scope options: OB-04 reads a disposable Run the owner names under Q30 (MR:252), never `run_93bfa00cae2b`, so waiting for it adds no information to the scope choice, only to the flip-or-not choice.
3. **B closes INV-003's hole by code, not by default.** Today `check_run_id` checks syntax only, so after any flip every `--run <id>` would read (MR:234; ADJ:458). B requires a test that refuses a Run the terminal does not hold, which is exactly OB-06 (a) ("a test shows a Run outside scope is refused", MR:254).
4. **B keeps every evidence gate.** "Do not flip before the seeded test" stands; the PR merges only after OB-03, OB-04 and OB-05 records are linked, and is closed unmerged if OB-03 shows consumption, the same stop rule the spec writes (MR:1000, "stop OB-06; record 'consumes'").
5. **The spec's own stop rule already absorbs B's main risk.** If OB-04 shows the panel unusable, MR:1001 says "hold OB-06; ask the owner whether to narrow scope". So an early wide scope is not locked in; it is revisable at the one point where evidence arrives.
6. **One fewer owner round trip.** C needs a second owner answer in W2; B gets it now. Section 6.5 stops a lane whenever a gated question is unanswered when its wave opens (MR:998, "A gated Q is unanswered when its wave opens"), so a W2 that waits on the owner is a real stall, not a formality.
7. **There is owner intent behind switching on.** The target state is that "the questions read is switched on only for the scope the owner wrote" (MR:242), and the owner already gave a "Do it" pass (ADJ:814). This weighs against A's assumption that nobody needs the panel.

### 4. Weaknesses identified in the others

**Variant 1 (A).**
1. It leaves X-016 unproven inside this program, so both programs keep unverified cautions (ADJ:333; ADJ:813, "Both programs keep their cautions"). The seeded test is cheap relative to that: one throwaway Run, `run-create` only (MR:251).
2. It contradicts the program's target state (MR:242) and the owner's recorded "Do it" (ADJ:814) without citing any evidence of no demand (diff-analysis A-003: "no variant cites evidence of demand").
3. Its own risk list admits that parking weakens the reason to commit the sibling-only owner records (Q7), raising evidence-loss risk if `issue-409-mvp` is cleaned (MR:235; variant-1 "What it costs or risks").
4. "Ask again when release 3 opens" is a second owner question too, just later, against staler code (the two unpushed switch-on commits already need a fresh branch, MR:234).

**Variant 3 (C).**
1. It defers a choice the coming evidence does not inform (strength 2): neither OB-03 (throwaway Run) nor OB-04 (disposable Run) tests `run_93bfa00cae2b`, so in W2 the owner faces the same two scope options with the same facts.
2. It adds an owner round trip in W2, and section 6.5 makes an unanswered gated question a lane stall (MR:998).
3. It leaves the scope sentence open ("whichever sentence the owner writes"), so the enforcement test cannot be designed until W2.

### 5. Concessions

1. **Building OB-06 in W1 conflicts with the spec as written.** OB-06 is blocked by SW-04, Q6, Q23, OB-01, OB-03, OB-04, OB-05, TB-CONSUME, Q25 and its pr-submit grant (MR:254), and its default is "this PR is not opened". An open-but-unmerged PR that lacks (b) and (c) does not meet the item's definition. The parallel-build half of B is its weakest part; C is right there.
2. **How the code detects "held by this terminal" is UNVERIFIED.** `run-current` is a read verb the spec names (MR:604; OB-03 records it, MR:251), but the observer reads only three argv shapes today (MR:233), so adding a fourth is a change; whether `run-current` reliably reports the terminal's held Run is not established here. 28 of 53 Runs have no holder (MR:239).
3. **No debate verdict backs a wide scope.** The only recommendation to widen (V5 D5(ii)) was withdrawn (ADJ:776), and ADJ lists "recommend scope 'any Run the terminal holds' now" among changes not being made (ADJ:814). My reply is that ADJ rejected an agent recommending the scope, and its rationale lists "the owner's own scope sentence" as a prerequisite, which B supplies; but the rejection is real and an owner should weigh it.
4. **A seeded pass is necessary, not sufficient** (ADJ:174; MR:1156). A wide scope multiplies the number of live Runs exposed if the one disposable OB-04 Run is not representative.
5. **Wasted work if OB-03 fails.** The variant admits it.

### 6. Shared assumptions

- **A-003 (a near-term user of the panel exists): QUALIFY.** No variant cites demand evidence, but the files are not silent: the target state is a switched-on read (MR:242) and the owner gave a "Do it" pass (ADJ:814). That is intent, not measured use; how often anyone works in the holder terminal of a coordinator Run is unchecked (UNVERIFIED) and is the owner's knowledge, as diff-analysis says.
- **A-004 (evidence on one build carries until the build changes, and OB-05 catches the change): QUALIFY.** OB-05 requires "a build check or a test fails when the build string changes" (MR:253), so the second half holds by design. The first half holds only for the conditions tested: one throwaway Run plus one disposable live Run; live `--wait` listeners and ack cycles on other Runs are outside it (MR:1156). Build divergence is already real (ADJ:363, A-009, 67 percent: design lock `.780594c521aa` against host `.9cfecdd30b2a`). This qualification bites harder on B's wide scope than on C's.

### 7. Per-point positions

| Point | Better variant | Confidence | Reason |
|---|---|---|---|
| S-001 | Tie (A = B = C) | 50% | Identical section sets; nothing to choose |
| C-001 | B = C | 85% | Running OB-03 in W1 is the only way X-016 gets diagnostic evidence; A leaves it at 61 percent unproven |
| C-002 | B | 60% | The coming evidence does not discriminate between the two scopes (section 3, item 2); MR:1001 still allows narrowing later |
| C-003 | C | 65% | OB-06's blockers and "not opened" default (MR:254) make a W1 flip PR non-compliant; build cost may be wasted |
| C-004 | C | 60% | C's refusal test does not depend on an UNVERIFIED holder-detection read; B's is more concrete but rests on it |
| C-005 | B = C | 60% | Keeping the live dependency is the price of evidence; A's removal is cheaper but leaves the question open |
| X-001 | B | 55% | Scope can usefully be chosen now because only one scope has a use; ADJ:814 and the withdrawn V5 D5(ii) keep this close |
| X-002 | C | 65% | Same reason as C-003 |
| A-003 | B = C | 60% | Target state (MR:242) and the "Do it" pass (ADJ:814) favour testing now over A's park |
| A-004 | C | 60% | C keeps the scope decision open until build-specific evidence exists, which limits exposure if A-004 fails |

### 8. Overall verdict

Variant 3 (C), with B's scope observation added, at 60 percent confidence: C keeps the spec's gate order intact (OB-06 in W2, MR:254, MR:533) and the owner loses little by waiting because MR:1001 lets scope be revisited anyway, but the owner should be told now that "this Run only" names an old Run nobody watches, so in W2 the realistic choice is "any Run my terminal holds" or no flip.

### Advocate for proposal C (source file: round1-advocate-C.md)

## Round 1 statement: advocate for variant 3 (proposal C)

Debate: Q6, scope and timing of switching on the observer's coordinator-questions read. Mode A, depth quick, Round 1.

Abbreviations: M = `.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md`; ADJ = `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md`. Every line number below was re-read on 2026-11-14 for this statement.

### 1. Position summary

Run the seeded consumption test (OB-03), the one live-layout attempt (OB-04) and the build pin (OB-05) now, in W1, and have the owner write the scope sentence only after reading those records; open the flip pull request (OB-06) in W2. This is the spec's own default for Q6 (ADJ:776), and it is the only variant that both produces evidence on the open consumption question and avoids committing to a scope before that evidence exists.

### 2. Steelman of each opposing variant

**Variant A (park everything until release 3).** The strongest case for A: the guard is already off and costs nothing to leave off (M:233, "Guard off: `QUESTION_GATE_PASSED = False`"); the program has no evidence that anyone needs the panel now (diff-analysis A-003: "no variant cites evidence of demand"); the live lanes depend on an Orca app that was not reachable on 2026-11-13 (M:604) and on two more owner answers (Q24, Q30) plus two permission rows. OB-03 writes seeded messages into a Run, which is an outward action the spec gates separately (M:575, "OB-03 needs `GRANT(OB-03,seeded-write)`"). Parking removes all of that risk and all of that coordination, and the question is re-asked when a real consumer (release 3, Decision Desk) exists, at which point the Orca build will have moved anyway and fresh evidence would be needed regardless (OB-05's build pin, M:253). A is the cheapest correct answer if the panel truly has no near-term user.

**Variant B (scope "any Run my terminal holds" now, build the flip in parallel).** The strongest case for B: Q-1 failed, so only the terminal that holds a Run can read its questions (M:239; ADJ:465 INV-024). "Any Run my terminal holds" is therefore not a widening in practice; it is the only access path Orca gives. The pinned Run `run_93bfa00cae2b` is an old "Claim issue 375" Run (ADJ:458 INV-003), so "this Run only" gives a flip that works for nobody (diff-analysis U-002, rated High). Given that, deferring the sentence only buys a second round of owner latency for a choice whose answer is already forced. B also keeps every safety gate: the PR stays unmerged until OB-03, OB-04 and OB-05 records are linked, and is closed if OB-03 shows consumption. The parallel build turns W2 into a merge step instead of a build step.

### 3. Strengths claimed

1. **It is the spec's recommended answer, verbatim.** ADJ:776: "Default (no debate verdict): do not flip before the seeded test; after it, the scope sentence is yours; no answer means the guard stays off." M:533 carries the same default and assigns "W1 (test), W2 (flip)", which is exactly C's wave plan. Neither A nor B matches that row.
2. **It gets the first diagnostic evidence on X-016.** X-016 is "UNRESOLVED ... UNPROVEN BOTH WAYS" at 61 percent (ADJ:333), and the owner's own measurement is non-diagnostic (ADJ:813). C runs OB-03 in W1, so both the observer's caution and the sweep's caution stop being unverified claims (ADJ:333 action column: "seeded test ... cite the help text, pin the build"). A leaves X-016 open indefinitely.
3. **The scope choice is made on evidence, including the usability evidence that decides it.** OB-04 records "whether any question disappeared, and whether the panel was usable" (M:252). The spec's own failure table reacts to those outcomes: OB-03 missing a message means "stop OB-06; record 'consumes'" (M:1000); OB-04 unusable means "hold OB-06; ask the owner whether to narrow scope" (M:1001). The sufficiency table says OB-06 alone may not give a usable panel because "28 of 53 Runs have no `coordinator_handle`" and "OB-04's record decides" (M:1157). C puts the owner's sentence after the record that decides it.
4. **It honours ADJ's "Do not" list exactly.** ADJ:195: "flip the guard before action 4 (a) and (b)". ADJ:814 lists "recommend scope 'any Run the terminal holds' now (V5 D5(ii))" as a change *not being made*, with the reason that "the seeded consumption test, the live-layout attempt, the build pin and the owner's own scope sentence are prerequisites". C is the only variant consistent with both lines.
5. **It does not depend on an unverified holder-detection mechanism at decision time.** OB-06 (a) requires "a test shows a Run outside scope is refused" (M:254). C's enforcement is "whichever sentence the owner writes" (diff-analysis C-004), so the code is written once, against a known sentence. B commits to "held by this terminal" now while B itself marks how the observer detects holding without `run-use` as UNVERIFIED; the observer never runs `run-use` (ADJ:465 INV-024), and `run-use` on a live coordinator is "forbidden for the observer" (ADJ:459 INV-005).
6. **No wasted build if OB-03 fails.** If OB-03 shows any seeded message missing, OB-06 stops (M:1000). C writes no flip code before that is known; B accepts "may be wasted work" as a cost.

### 4. Weaknesses identified in the others

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

### 5. Concessions

1. **B's U-002 point is largely right.** `run_93bfa00cae2b` is an old "Claim issue 375" Run (ADJ:458). Whether it still has a holder terminal is UNVERIFIED, but "this Run only" is very likely a flip of little practical use. So C's deferred choice is in practice between "any Run my terminal holds" and "no flip", not between two useful scopes. Deferral buys less than C's text implies.
2. **The spec's own failure row assumes a scope may already be wide.** M:1001 says on an unusable panel "ask the owner whether to narrow scope", which reads as if a wider scope could be stated before OB-04. The spec does not forbid an early sentence; it only says the sentence is the owner's (ADJ:776).
3. **C costs one extra owner round** (the scope sentence in W2) and keeps the panel dark longer than B.
4. **C keeps every live dependency A removes:** Orca reachable (M:604, not reachable on 2026-11-13), Q24, Q30, and the permission rows `GRANT(OB-03,seeded-write)` and `GRANT(OB-04,live-read)` (M:251-252). If those stay unresolved, C degrades to A in effect (OB-04 "is held and OB-06 waits", M:252) without A's clean ledger entry.
5. **C is necessary-not-sufficient evidence, like B.** One disposable Run in OB-04 says nothing about every other live Run (M:1156); C does not close that gap either.

### 6. Shared assumptions

- **A-003 (a near-term user of the questions panel exists): QUALIFY.** No variant cites direct demand, as the diff analysis says. But there is indirect evidence: the owner recorded a pass on 2026-11-12 (M:235) and a "Do it" record that ADJ:814 declines to treat as sufficient for a flip, which only makes sense if the owner wanted the flip; ADJ Part 2.1 action 4 lists "Unblocks: a usable questions panel" (ADJ:192). That supports "some owner demand", not "a named regular user". C's W1 tests are worth running on that basis; if the owner says there is no user, A becomes the better answer.
- **A-004 (evidence on one build carries until the build changes, and OB-05 catches the change): QUALIFY.** OB-05 does require "a build check or a test fails when the build string changes" (M:253), so the build axis is covered by design. But the assumption is incomplete: evidence can be invalidated without a build change, because a live Run's `--wait` listeners and ack cycle differ from the throwaway Run (M:1156). The ADJ A-009 "67 percent" figure quoted in the diff analysis was not opened here (UNVERIFIED). Both B and C rely on OB-04 to cover the non-build axis, and C is slightly better placed because the scope sentence is written after OB-04's record.

### 7. Per-point positions

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

### 8. Overall verdict

The owner should pick **variant C**, confidence **70 percent**: it is the spec's own default (ADJ:776, M:533), it is the only answer that both produces evidence on the unresolved consumption question and respects ADJ's rejection of an early wide scope (ADJ:814). If the owner already knows the answer will be "any Run my terminal holds" and accepts possibly wasted build work, B is a reasonable second; if the owner says no one needs the panel this program, A is right.

## Scoring Matrix

Positions are each advocate's section 7 table. "B = C" counts as a vote for both.

| Diff Point | Level | Advocate A | Advocate B | Advocate C | Winner | Confidence | Evidence Summary |
|---|---|---|---|---|---|---|---|
| S-001 | L1 | tie | tie | tie | tie (no winner) | 50% | Identical five-section structure in all three. |
| C-001 | L3 | C | B = C | C = B | C (with B) | 85% | Running OB-03 now is the only route to evidence on consumption (ADJ X-016, line 333); A leaves it open. |
| C-002 | L2 | C | B | C | C | 65% | Matches the spec row (merged-requirements.md:533, ADJ:776); B's argument that the coming evidence does not discriminate the two scopes lowered confidence. |
| C-003 | L2 | C | C | C | C | 75% | OB-06's blockers and "not opened" default (merged-requirements.md:254) make a W1 flip PR non-compliant; B conceded. |
| C-004 | L3 | C | C | C | C | 70% | C's refusal test is written once against a known sentence; B's holder detection is UNVERIFIED. |
| C-005 | L2 | A | B = C | A | A | 65% | A alone removes the live Orca, Q24, Q30 and permission-row dependencies (merged-requirements.md:251-252, :604). |
| X-001 | L3 | C | B | C | C | 65% | ADJ:814 rejects recommending the wide scope now; OB-04 decides usability (merged-requirements.md:1157). B dissents: only one scope has practical use. |
| X-002 | L2 | C | C | C | C | 70% | No wasted build before the test can cancel it (merged-requirements.md:1000); B conceded. |
| A-003 | L2 | C | B = C | C = B | C (with B) | 60% | All three QUALIFY: indirect owner demand exists (the 2026-11-12 pass, target state merged-requirements.md:242), no named user. |
| A-004 | L3 | A | C | C | C | 55% | All three QUALIFY: OB-05 detects a build change but does not re-run the test; non-build differences on live Runs remain (merged-requirements.md:1156). |

Shared-assumption responses: A-003 QUALIFY x3; A-004 QUALIFY x3. No omissions.

## Overall verdicts (section 8 of each statement)

| Advocate | Picks | Confidence |
|---|---|---|
| A (for park) | C | 70% |
| B (for scope now) | C, with B's scope observation added | 60% |
| C (for evidence first) | C | 70% |

All three advocates, including the two arguing for other proposals, chose C: 3 of 3. Mean confidence 67%.

## Convergence Assessment
- Points resolved: 10 of 10 (majority rule); unanimous: S-001, C-001, C-003, C-004, X-002, A-003
- Alignment: 100%
- Threshold: 80%
- Taxonomy coverage: L1 (S-001), L2 (C-002, C-003, C-005, X-002, A-003), L3 (C-001, C-004, X-001, A-004): all levels covered
- Invariant probe gate: not applied (Round 2.5 skipped at quick depth)
- Status: CONVERGED
- Unresolved points: none. Dissent recorded: B on C-002 and X-001; A and C on C-005 (favouring A).
