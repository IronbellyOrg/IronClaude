# Q6 final: when to switch on the observer's coordinator-questions read, and for which Runs

Q6 is owner question 6 of the alignment spec. It is about the observer (`superclaude observe`, the read-only terminal dashboard of Orca workers): it has a built panel that reads a coordinator's open questions from Orca, switched off by one setting (the "guard", `QUESTION_GATE_PASSED = False`). "Flipping" the guard means switching that read on. A Run is one coordinated piece of work in Orca, with its own mailbox of messages. OB-nn ids are the observer's work items in the spec (OB-03 seeded test, OB-04 live-layout attempt in a real coordinator terminal, OB-05 build pin, OB-06 switch-on pull request); waves W0 to W5 are the spec's ordered batches of work (W1 is the first batch after intake, W2 the next).

## Debate result

- Winner: proposal C (run the tests now, flip later, owner writes the scope after seeing the evidence). Confidence 67 percent (mean of the three advocates' overall verdicts: 70, 60, 70).
- Agreement: 3 of 3. All three advocates, including the two arguing for the other proposals, picked C as the owner's best answer. On the ten individual debate points, all ten had a majority; six were unanimous.
- Deciding evidence: whether Orca's question read removes ("consumes") messages on a live coordinator Run is unproven both ways (ADJ X-016: ADJ is the adjudicated alignment findings document, `alignment-findings-adjudicated.md`, and X-016 is its contradiction number 16, line 333). The seeded consumption test (OB-03, a test that puts known messages in a throwaway Run's mailbox and checks they survive the observer's read) is the only planned way to get evidence, and the spec forbids building the switch-on pull request before it (OB-06's blocked-by list, `merged-requirements.md:254`; ADJ line 195).

Proposal A (park everything: no test, no flip, guard off). Strength: no live risk, no dependency on the Orca app (unreachable on 2026-11-13, `merged-requirements.md:604`) or on two further owner answers (Q24, who runs live Orca reads; Q30, which Run the live attempt reads). Weakness: it leaves the consumption question open indefinitely, and its re-open trigger "release 3 is opened" can never fire, because release 3 (Decision Desk, OB-09) is itself blocked by the flip (`merged-requirements.md:257`). Its own advocate conceded this and voted C.

Proposal B (write the scope "any Run my terminal holds" now and build the flip in parallel). Strength: the only Run the owner's existing pass names, `run_93bfa00cae2b`, is an old "Claim issue 375" Run (invariant-probe finding INV-003, ADJ line 458), and only the terminal holding a Run can read its questions anyway (gate test Q-1, "an unbound terminal cannot read another terminal's Run", failed; probe finding INV-024, ADJ line 465), so the narrow scope has little practical use. Weaknesses: building the pull request in wave W1 breaks OB-06's own prerequisites (conceded by B's advocate); how the code would detect "held by this terminal" is UNVERIFIED; and the adjudicated document explicitly declines to recommend the wide scope now (ADJ line 814).

Proposal C (spec's answer). Strength: it gets evidence first and asks for the scope sentence only after the seeded test and the live-layout attempt (OB-04), using the spec's stop rules (`merged-requirements.md:1000-1001`). Weakness: it costs a second owner question later, keeps the panel dark longer, and still needs live Orca, Q24 and Q30; and the evidence it waits for does not really discriminate between the two scopes (C's advocate conceded B's point).

The merged answer (`Q06/merged-answer.md`) is C plus two additions: tell the owner that "this Run only" means the old pinned Run, and if the live tests cannot run, record a dated park with the trigger "the Orca app answers a read verb and Q24 and Q30 are answered".

## Final recommendation

Do not switch the questions read on yet. Run the seeded consumption test, the one live-layout attempt and the build pin first (wave W1); after reading their records, the owner writes the scope sentence, knowing that "this Run only" covers just one old Run, so the realistic choice then is "any Run my terminal holds" or no switch-on. If the live tests cannot run, record a dated park. Confidence 67 percent.

Single strongest reason: the consumption question is unproven both ways, and the seeded test is the only planned evidence; switching on, or choosing the wide scope, before it would point the read at live mailboxes whose loss is not measured.

Equals the spec's recommended answer: yes, with two additions (the plain-words note about the old Run, from B, and the park fallback, from A). Neither changes the spec's ordering.

## What would change the answer

If the owner says no one will use the questions panel during this program, proposal A (park, with the non-circular trigger) becomes better, because the live tests then buy evidence nobody needs yet.

## Criticality rating

- Security or trust boundary: low
- Reversibility: easy
- Who is affected: only this program
- Needs the owner's own intent, taste or knowledge that no file holds: partly
- Cost if the answer is wrong: medium
- Does it grant authority or accept a risk in writing: no
- Debate: converged
- Suggested handling: SAFE-FOR-AGENT-RECOMMENDATION
- Reason for the suggested handling in two sentences: The recommended answer only orders the work (test first, flip later) and matches both the spec default and the guard's current off state, so nothing is switched on and nothing is granted by it; the seeded test still needs its own permission row. The part that truly needs the owner, the scope sentence, is deferred by this answer to a later, separate owner question after the evidence exists.

## Debate record

- Folder: `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/Q06/adversarial/`
- fallback_mode: false (three advocates spawned in parallel as separate agents; merge by a merge-executor agent; depth quick, Round 1 only)
