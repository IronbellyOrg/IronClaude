# Round 1: Advocate for variant 2 (proposal B)

Debate: Q6 owner-answer proposals, sc:adversarial Mode A, depth quick, Round 1.
Abbreviations: MR = `.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md`; ADJ = `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md`. Line numbers below were re-read on 2026-11-14.

## 1. Position summary

The owner should write the scope sentence now, "any Run my terminal holds", because it is the only scope that matches how Orca lets anyone read a Run's questions (Q-1 failed), while keeping every evidence gate before the flip merges. The strongest part of B is the scope choice; its weakest part is building the flip pull request in W1, which I concede below.

## 2. Steelman of each opposing variant

**Variant 1 (A, park everything).** Nothing reads any mailbox, so no coordinator question can be lost; the X-016 consumption question is unproven both ways at 61 percent (ADJ:333), and a Run's questions are the one place where a silent loss hurts. Parking also removes two live Orca lanes from W1 at a time the Orca app was not reachable (MR:604, "The probe found the app not reachable on 2026-11-13") and removes the Q24 and Q30 dependencies. If no one needs the panel before release 3, paying for live tests now is cost without a user.

**Variant 3 (C, evidence first, scope after).** It is the spec's own default and ADJ's: "do not flip before the seeded test; after it, the scope sentence is yours" (ADJ:776; MR:533). It keeps the owner uncommitted until OB-03 and OB-04 records exist, so if the live attempt shows the panel unusable or lossy the owner can pick the narrow scope or no flip at all (MR:1001, "hold OB-06; ask the owner whether to narrow scope"). It keeps the work-item order the spec already wrote: OB-06 is blocked by OB-01, OB-03, OB-04, OB-05 and others (MR:254) and sits in W2 (MR:533). It also honours ADJ's rejection of recommending "any Run the terminal holds" now (ADJ:814).

## 3. Strengths claimed

1. **"Any Run my terminal holds" is the only scope with a practical use.** The pass record names one Run, `run_93bfa00cae2b`, an old "Claim issue 375" Run (ADJ:458, INV-003; MR:235). "This Run only" therefore yields a flip that reads a Run nobody watches (diff-analysis U-001 rates this observation High).
2. **The scope matches the only access path Orca gives.** Q-1 ("an unbound terminal cannot read another terminal's Run") failed on 2026-11-11 (MR:239; ADJ:465, INV-024: "only the terminal holding the Run can read"). A scope wider than "held by this terminal" would not work; a narrower one is the old Run above. The evidence OB-03 and OB-04 produce does not discriminate between the two scope options: OB-04 reads a disposable Run the owner names under Q30 (MR:252), never `run_93bfa00cae2b`, so waiting for it adds no information to the scope choice, only to the flip-or-not choice.
3. **B closes INV-003's hole by code, not by default.** Today `check_run_id` checks syntax only, so after any flip every `--run <id>` would read (MR:234; ADJ:458). B requires a test that refuses a Run the terminal does not hold, which is exactly OB-06 (a) ("a test shows a Run outside scope is refused", MR:254).
4. **B keeps every evidence gate.** "Do not flip before the seeded test" stands; the PR merges only after OB-03, OB-04 and OB-05 records are linked, and is closed unmerged if OB-03 shows consumption, the same stop rule the spec writes (MR:1000, "stop OB-06; record 'consumes'").
5. **The spec's own stop rule already absorbs B's main risk.** If OB-04 shows the panel unusable, MR:1001 says "hold OB-06; ask the owner whether to narrow scope". So an early wide scope is not locked in; it is revisable at the one point where evidence arrives.
6. **One fewer owner round trip.** C needs a second owner answer in W2; B gets it now. Section 6.5 stops a lane whenever a gated question is unanswered when its wave opens (MR:998, "A gated Q is unanswered when its wave opens"), so a W2 that waits on the owner is a real stall, not a formality.
7. **There is owner intent behind switching on.** The target state is that "the questions read is switched on only for the scope the owner wrote" (MR:242), and the owner already gave a "Do it" pass (ADJ:814). This weighs against A's assumption that nobody needs the panel.

## 4. Weaknesses identified in the others

**Variant 1 (A).**
1. It leaves X-016 unproven inside this program, so both programs keep unverified cautions (ADJ:333; ADJ:813, "Both programs keep their cautions"). The seeded test is cheap relative to that: one throwaway Run, `run-create` only (MR:251).
2. It contradicts the program's target state (MR:242) and the owner's recorded "Do it" (ADJ:814) without citing any evidence of no demand (diff-analysis A-003: "no variant cites evidence of demand").
3. Its own risk list admits that parking weakens the reason to commit the sibling-only owner records (Q7), raising evidence-loss risk if `issue-409-mvp` is cleaned (MR:235; variant-1 "What it costs or risks").
4. "Ask again when release 3 opens" is a second owner question too, just later, against staler code (the two unpushed switch-on commits already need a fresh branch, MR:234).

**Variant 3 (C).**
1. It defers a choice the coming evidence does not inform (strength 2): neither OB-03 (throwaway Run) nor OB-04 (disposable Run) tests `run_93bfa00cae2b`, so in W2 the owner faces the same two scope options with the same facts.
2. It adds an owner round trip in W2, and section 6.5 makes an unanswered gated question a lane stall (MR:998).
3. It leaves the scope sentence open ("whichever sentence the owner writes"), so the enforcement test cannot be designed until W2.

## 5. Concessions

1. **Building OB-06 in W1 conflicts with the spec as written.** OB-06 is blocked by SW-04, Q6, Q23, OB-01, OB-03, OB-04, OB-05, TB-CONSUME, Q25 and its pr-submit grant (MR:254), and its default is "this PR is not opened". An open-but-unmerged PR that lacks (b) and (c) does not meet the item's definition. The parallel-build half of B is its weakest part; C is right there.
2. **How the code detects "held by this terminal" is UNVERIFIED.** `run-current` is a read verb the spec names (MR:604; OB-03 records it, MR:251), but the observer reads only three argv shapes today (MR:233), so adding a fourth is a change; whether `run-current` reliably reports the terminal's held Run is not established here. 28 of 53 Runs have no holder (MR:239).
3. **No debate verdict backs a wide scope.** The only recommendation to widen (V5 D5(ii)) was withdrawn (ADJ:776), and ADJ lists "recommend scope 'any Run the terminal holds' now" among changes not being made (ADJ:814). My reply is that ADJ rejected an agent recommending the scope, and its rationale lists "the owner's own scope sentence" as a prerequisite, which B supplies; but the rejection is real and an owner should weigh it.
4. **A seeded pass is necessary, not sufficient** (ADJ:174; MR:1156). A wide scope multiplies the number of live Runs exposed if the one disposable OB-04 Run is not representative.
5. **Wasted work if OB-03 fails.** The variant admits it.

## 6. Shared assumptions

- **A-003 (a near-term user of the panel exists): QUALIFY.** No variant cites demand evidence, but the files are not silent: the target state is a switched-on read (MR:242) and the owner gave a "Do it" pass (ADJ:814). That is intent, not measured use; how often anyone works in the holder terminal of a coordinator Run is unchecked (UNVERIFIED) and is the owner's knowledge, as diff-analysis says.
- **A-004 (evidence on one build carries until the build changes, and OB-05 catches the change): QUALIFY.** OB-05 requires "a build check or a test fails when the build string changes" (MR:253), so the second half holds by design. The first half holds only for the conditions tested: one throwaway Run plus one disposable live Run; live `--wait` listeners and ack cycles on other Runs are outside it (MR:1156). Build divergence is already real (ADJ:363, A-009, 67 percent: design lock `.780594c521aa` against host `.9cfecdd30b2a`). This qualification bites harder on B's wide scope than on C's.

## 7. Per-point positions

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

## 8. Overall verdict

Variant 3 (C), with B's scope observation added, at 60 percent confidence: C keeps the spec's gate order intact (OB-06 in W2, MR:254, MR:533) and the owner loses little by waiting because MR:1001 lets scope be revisited anyway, but the owner should be told now that "this Run only" names an old Run nobody watches, so in W2 the realistic choice is "any Run my terminal holds" or no flip.
