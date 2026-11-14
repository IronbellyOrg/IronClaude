# Accepted answers (12 of 33 owner questions)

**Provenance.** On 2026-11-14 the owner told the orchestrating session to take the debated recommendation for every question that is safe to leave to an agent, and to separate out the rest (see `01-classification.md`). Each answer below is the final recommendation of a quick three-way debate (`Q<nn>/final.md`, debate record in `Q<nn>/adversarial/`). They are recorded as answers delegated by the owner, not as owner-written rows: the owner can reverse any of them by saying so, and a reversed answer voids the unsent drafts and grants that rest on it.

**Why these 12 were judged safe.** Each one is easy to undo, grants no authority, accepts no risk in writing, affects only this program, needs none of the owner's own knowledge, and the three debaters converged. Each equals the spec's recommended answer or refines it. One refinement changes a work item: Q10 corrects only one sentence of the sweep's wording, so the spec's SW-07 acceptance criterion (3) needs rewording. Q27 and Q18 were close calls and are explained in `01-classification.md`.

**What accepting does NOT do.** It grants no push, no merge, no issue or comment post, no live test, no worktree creation, and no change to the allow-list. Every one of those still needs its own per-action grant from the owner (merged spec 6.8). Where an answer says something is posted later (Q10, Q18), the post itself is a separate grant.

Questions: Q5, Q6, Q9, Q10, Q11, Q12, Q17, Q18, Q21, Q23, Q27, Q32.

---

## Q5: How the worker dashboard and the sweep report should fit together

Debate: Winner: proposal B (keep both programs separate, joined by one written contract note, no runtime link in version 1), confidence 75 percent. Agreement: 3 of 3; all three advocates, including those for 


Keep both programs and write one contract note: draft it now on a branch from master, and land it with its comparison test and links after PR #539 merges and the real-id comparison runs. The note's word table states each program's stale threshold. Once the comparison is recorded, ask Q17 (an observer panel for sweep facts) once more; if the answer is then "yes", the panel reads a copy captured from the coordinator's regular pass and never runs the sweep itself. The #409 correction pass records this choice so the #409 body stops proposing the opposite. Confidence 75 percent. Strongest reason: it removes the confusion that exists today without coupling two independently built programs, and every other option still needs the note.

Equals the spec's recommended answer: yes ("One note; keep both programs"), with the debate's additions above. The full merged text is `merged-proposal.md`.


## Q6: When to switch on the dashboard's "coordinator questions" panel, and for which work sessions (Q6)

Debate: - Winner: proposal C (run the tests now, flip later, owner writes the scope after seeing the evidence). Confidence 67 percent (mean of the three advocates' overall verdicts: 70, 60, 70).


Do not switch the questions read on yet. Run the seeded consumption test, the one live-layout attempt and the build pin first (wave W1); after reading their records, the owner writes the scope sentence, knowing that "this Run only" covers just one old Run, so the realistic choice then is "any Run my terminal holds" or no switch-on. If the live tests cannot run, record a dated park. Confidence 67 percent.

Single strongest reason: the consumption question is unproven both ways, and the seeded test is the only planned evidence; switching on, or choosing the wide scope, before it would point the read at live mailboxes whose loss is not measured.

Equals the spec's recommended answer: yes, with two additions (the plain-words note about the old Run, from B, and the park fallback, from A). Neither changes the spec's ordering.


## Q9: Whether to keep the worker-status sweep's machine-readable output (Q9)

Debate: - Winner: proposal A (not now; when a named reader needs it, capture from stdout first), merged with parts of B and C. Confidence 73 percent (mean of the advocates' verdicts: 75, 70, 75).


Not now. Write one sentence into the planned contract note now: the sweep JSON is a stdout-only reply with no stored form until a named reader asks for it. When a reader (v2, a status record, or the observer if Q17 becomes yes) names its need, try in order: the caller saves stdout; else the sweep embeds the JSON inside its one report, before the "Report complete" line, in a backtick-safe block, with a test that both copies match; and only then a separate file, which relaxes NFR-001. Confidence 73 percent.

Single strongest reason: no reader exists to define what should be kept, where, or for how long, and today's reports are not durable, so storing now buys nothing and closing the door for good contradicts the review.

Equals the spec's recommended answer: yes, with two additions (the stdout-only sentence now, and the embedded-copy step before any NFR-001 change).


## Q10: Whether the worker-status sweep may read the coordinator's pending questions (Q10)

Debate: - Winner: proposal C (the observer's alone for now; correct the sweep's text now), amended. Confidence 73 percent (mean of the advocates' verdicts: 75, 70, 75).


The sweep does not read questions; only the observer may, for now. After PR #539 merges, correct only the sweep's bullet that says questions "cannot be read without consuming them" (`report.py:534-535`) to: "This command reads no messages. A plain `check` consumes them. Whether `check --all --types question` consumes on a live Run is not established." Keep the header "Messages coverage: partial" (`report.py:199`), which is true. Any future sweep read needs a new owner-signed allow-list entry. Reopen Q10 when the seeded and live consumption tests have results, or if Q6 parks the observer's read; if the seeded test shows consumption, the answer becomes "neither program reads questions". Confidence 73 percent.

Single strongest reason: it removes the sweep's one unproven claim now, without depending on any live test and without widening the allow-list, and the coordinator already gets its questions through its own loop.

Equals the spec's recommended answer: partly. The answer is the same ("observer's alone for now; correct the sweep's two sentences"), but the correction applies to the bullet only, so SW-07's acceptance criterion (3), which says both lines carry the exact text (`merged-requirements.md:196`), needs rewording; and a reopen condition is added.


## Q11: What the coordinator's "static report in chat" should be (owner question 11)

Debate: Q11 is owner question 11 in the merged requirements (merged-requirements.md:538). Proposal A is "both reports, now"; proposal B is "the sweep summary only, until the contract note exists"; proposal C 


Answer: the static chat report is the sweep's counts-and-path reply only, until the contract note exists; record in the ledger that no recurring loop exists yet, so no "every 3 to 5 minutes" cadence is claimed as met; and before the observer's text ever joins, check that `superclaude observe --once --run <run>` from the coordinator's own terminal shows that coordinator's Run. Confidence: 85 percent. Strongest reason: the #409-layout report the owner asked for already exists as the sweep's report file, so this answer meets the owner's recorded scope with no edit. Equals the spec's recommended answer: yes, with two added caveats (no cadence claimed; the Q-1 check) taken from proposals C and A (merged-proposal.md).


## Q12: Make the observer dashboard findable in the routing guide (owner question 12)

Debate: Q12 is owner question 12 in the merged requirements (merged-requirements.md:539). Proposal A is "no entry for now"; proposal B is "one sentence in the guide's prose Orca section, not a table row"; pro


Answer: yes, one row in the routing table (not the other-commands table) for `superclaude observe`, copied byte-for-byte to the plugin mirror, in its own small PR after PR #539 merges; the worker runs the routing tests before naming any test edit; the row describes only what works on master today and says "Coordinator or person only, never a worker", the same words the `/sc:sweep` entry uses (HOW-WE-WORK.md:335). Confidence: 78 percent. Strongest reason: only a routing-table row is read by `/sc:recommend`, so it is the only entry that makes the tool findable by both people and the recommender. Equals the spec's recommended answer: yes, with the table named and the test-edit claim narrowed (merged-proposal.md).


## Q17: Should the worker dashboard also show the sweep report's facts? (Q17)

Debate: Winner: proposal B (no sweep-facts panel now; ask again later; only a later "yes" makes storage of the sweep's JSON a real requirement). Confidence 65 percent. The advocates agreed 3 of 3: the advocat


No sweep-facts panel on the observer screen now. Record a trigger to ask again: when Q19 picks Decision Desk or observer release 3 is scheduled, and only after PR #539 has merged. Keep the rule that any later panel prints the sweep's own words and the report's age, and add that sweep facts are always older than the live Orca rows beside them.

Confidence: 65 percent.

Single strongest reason: every input a panel would need (the merged sweep, a stored or captured copy of its JSON, a scheduled Decision Desk) is still open, and the only measured judgement on the point says "not now".

Equals the spec's recommended answer: yes. The merged additions (trigger, freshness note, layout room) refine it without changing it.


## Q18: Should the dashboard's data file be copied to your TUIBBS machine? (Q18)

Debate: Winner: proposal A (no channel now; the channel item, CO-04, opens only when the observer reaches its release 4, the remote fleet, or when the owner states that a TUIBBS screen is planned). Confidence


No copy channel now. Keep CO-04 deferred until observer release 4 or until you state that a TUIBBS screen is planned. When it opens, its design must name five things before any code: transport, identity of the source workspace, an age rule, re-cleaning of untrusted text, and who may read the copy (including whether the whole snapshot or only part leaves the host). Tell Coder#477 that no channel exists and one is deferred.

Confidence: 70 percent.

Single strongest reason: the only fact that could justify a yes or a no is your own plan for TUIBBS, and your recorded position is "background, not deciding"; deferring with written triggers keeps every option open at almost no cost.

Equals the spec's recommended answer: yes. The merged additions (the fifth design piece and the guard sentence) refine it.


## Q21: Should the sweep report mark sessions that a program started, not a person?

Debate: Winner: proposal B ("yes, in Phase 2, reading Orca's agent rows, only after the watcher's first live test shows what they hold"), confidence 78 percent. Agreement: 2 of 3 advocates favoured proposal B


Yes, in Phase 2, reading Orca's `worktree ps` agent rows only in the shape the watcher's first live test (FU-1) records, with three additions from the debate: (1) the label may only turn "unknown" into "machine-started", never into "person-started", and a missing or unrecognised signal stays "could not determine"; (2) if the recorded row carries no usable signal, the label work stops and records that, and the named alternative is the watcher's versioned store `dispatch.json`, which would need its own owner approval; (3) the blind spot is written into the sweep design now. Confidence 78 percent. Strongest reason: it adds no new input or permission to the sweep and refuses to guess. Equals the spec's recommended answer: partly; the answer is the same, the three additions are new (merged text: `merged-proposal.md`).


## Q23: Should a "reclaimable" worker count as running, finished, or neither?

Debate: Winner: proposal C ("its own state, shown with Orca's word, until its meaning is known"), confidence 75 percent. Agreement: 2 of 3 advocates judged C best overall; the proposal A advocate itself chose


Record `reclaimable` as its own state, shown with Orca's word, neither live nor historical, with the sample facts written next to it as observations; apply the same rule to `release_pending` and `release_unknown`. Reopen it through the shared read-only Orca capture (XC-03, wave W1): add Orca's help text for terminal states and one detail read of one reclaimable worker. If that shows release is automatic and the session has exited, hide it with the historical workers (proposal A); if release needs a person, label it "not historical: awaiting release" (proposal B). Confidence 75 percent. Strongest reason: it is correct whether or not a reclaimable worker's session has exited, and costs nothing now. Equals the spec's recommended answer: yes, with a named reopen step added (merged text: `merged-proposal.md`).


## Q27: Can the plan for the git-safety fix ship inside PR #539?

Debate: Winner: proposal C (yes, commit SW-02's own plan package in PR #539). Confidence 88 percent. All three advocates picked C (3 of 3), including the advocate assigned to proposal A, who found the evidenc


Yes. SW-02's own plan package is written in the #539 checkout and committed in PR #539 with the fix, by named paths, including its progress record, its artifacts and its move from `to-do/` to `done/`. Before writing it, the #539 author records that the existing Done sweep task does not cover SW-02. The plan's review reports written outside the package stay uncommitted, and nothing else from the alignment program enters #539. Confidence 88 percent.

Strongest reason: the plan executor only runs a plan that sits in the same checkout as the code it changes, so every other placement either fails or needs heavier machinery.

Equals the spec's recommended answer: yes, with three commit-scope details added. The debate also found that the spec's default for this question cannot run.


## Q32: Should helper sessions save their own work as a local commit? (Q32)

Debate: Winner: proposal B ("no; workers never commit; the PR session commits"), confidence 65 percent (the mean of the three advocates' own judgments: 65, 70, 60). The advocates agreed 3 of 3, including the 


Answer "no: workers leave their changes uncommitted, and the PR session commits named paths". Pair it with one guard recorded in the ledger: the coordinator does not remove, clean or reuse a worker's worktree until its PR session has committed. Confidence 65 percent. Strongest reason: it is the only option that does not depend on an unverified reading of the worker contract and adds no owner questions. This equals the spec's recommended answer ("No; the PR session commits"), with the guard added. The guard closes the one real weakness the debate found.


---
**Caveat on Q6.** Only the "do not switch the questions read on before the seeded test" half is accepted. The scope sentence (this Run only, or any Run your terminal holds) is yours to write after the test evidence exists. It will come back to you then as a separate question.
