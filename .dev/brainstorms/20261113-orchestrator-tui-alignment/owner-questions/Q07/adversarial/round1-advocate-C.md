# Round 1: advocate for variant 3 (proposal C, "not now; freeze the sibling worktree")

Debate: Q7, sc:adversarial Mode A, depth quick, Round 1. Written 2026-11-14.

Evidence I re-read for this statement (2026-11-14): `merged-requirements.md` lines 230-265 and 530-560; `alignment-findings-adjudicated.md` (ADJ) lines 128, 142, 191, 328, 457, 478, 777; sibling `issue-409-mvp` `git status --short`, `git log --oneline -4`, `git branch -r --contains` for `1ae72e1a1` and `f104ca51a` (both returned no remote branch); sibling `.dev/issues/409/bmad/spec-orca-observer/release-gates.md` line 22.

## 1. Position summary

C says: move nothing now, write a dated "do not clean `issue-409-mvp`" entry that names every file at risk, and ask Q7 again when the switch-on pull request is actually scheduled. Its real value is the freeze entry and the exact inventory, which cost almost nothing. As a full answer to Q7 it is weaker than A, because it leaves the only copies of the owner's records on one disk for an open-ended time.

## 2. Steelman of each opposing variant

**A (owner does both, before cleaning).** A is the answer the spec and ADJ already recommend, word for word ("Yes, both, before that worktree is cleaned", ADJ:777; `merged-requirements.md:534`). It is the only variant that fully meets OB-01 as written: OB-01 (3) requires "the owner, not an agent, is the author of the pass record", and its "runs in" cell says "the commit is the owner's" (`merged-requirements.md:249`). It keeps OB-06 (d) unchanged ("the owner-written pass record is committed in this PR", `merged-requirements.md:254`; ADJ:191 "The guard-flip PR itself must commit the owner's pass record"), so no spec row has to be reworded. It also offers the archive route, so an owner who does not want personal records in the repository still has a compliant path. Under A, the person who commits is the person who wrote the text, which is the strongest answer available to "git cannot show who typed it" (ADJ:478, INV-014).

**B (one owner sentence; a records-only PR copies the files byte for byte now).** B removes the evidence-loss risk fastest. Every owner record, the pass record included, lands on master in days, and that does not depend on the switch-on, which is gated on live-Orca tests (Q24, Q30) that may never run. A byte comparison makes the copy auditable: what reaches master is provably identical to what sits in the sibling. One dated sentence in the ledger is a concrete owner statement, tied to named files and a date, which is more precise than "re-confirm". Owner cost is one sentence and one merge. OB-08 can then cite master paths early.

## 3. Strengths claimed

1. **It names the full risk precisely.** C is the only variant that lists every file at risk with where it lives: the pass record and `owner-decisions-20261112.md` in unpushed local commits `1ae72e1a1` and `f104ca51a`, plus the untracked `owner-decisions-20261108.md`, `live-test-guide.md`, `tuibbs-review/` and `handoff-mvp-brainstorm.md`. I re-checked this on 2026-11-14: the sibling `git status` shows those four paths as untracked, `git log` shows the two commits at HEAD, and `git branch -r --contains` returns no remote branch for either commit. A's OB-01 list leaves out the pass record (A sends it through OB-06 later) and does not mention `handoff-mvp-brainstorm.md`.
2. **It costs the least now.** It needs no branch, no pull request and no `/sc:pr-submit` run. The owner's attention goes to questions that block more work. The spec's own default for an unanswered Q7 is the same freeze ("`issue-409-mvp` must not be cleaned", `merged-requirements.md:534`). C turns that silent default into a dated, explicit choice.
3. **It does not force a decision on a switch-on that may never happen.** OB-06 is held unless Q6 is answered ("Default if Q6 is unanswered: the guard stays off and this PR is not opened", `merged-requirements.md:254`). The pass record names one Run, `run_93bfa00cae2b` (`merged-requirements.md:235`). Committing it before anyone knows whether the flip will happen risks a record that is stale or later rewritten. B itself names this risk ("two versions on master").
4. **It matches the trigger ADJ actually set.** ADJ's timing is "Waits for: before the sibling worktree is cleaned" (ADJ:191), and A-015's timing is "before the sibling worktree is cleaned / unblocks the flip PR" (ADJ:328). Neither says "now". C keeps that ordering and makes the "not cleaned" half explicit.
5. **It is never in conflict with the "agents may cite, never write" rule** (`release-gates.md:22`), because no agent touches the owner's text.

## 4. Weaknesses identified in the others

1. **A's own clean-up step can lose the pass record.** A says "After OB-01 is recorded, the sibling worktree may be cleaned". But under A the pass record is not in OB-01; it reaches master only "inside the switch-on pull request". If OB-01 is done and the sibling is then cleaned before OB-06 opens (or if OB-06 never opens), the pass record and the switch-on commits are deleted. They exist only in `1ae72e1a1` and `f104ca51a`, which no remote branch holds. The same gap exists in OB-01 as the spec writes it. The fix is either to put the pass record in OB-01's archive set, or to hold the clean-up until OB-06 lands, which is C's freeze.
2. **A's authorship defence is thinner than it reads.** A admits that if the existing record is "simply re-confirmed rather than re-typed, the authorship evidence is the same as today". So unless the owner re-types the record, A's "unambiguous" authorship comes down to who makes the commit, not who wrote the file.
3. **A leaves the commit route unspecified.** A admits "The owner's commit route on this host is not specified" (U-001). Until that route is chosen, A does not make anything safer than C does.
4. **B puts an agent in the committer seat for owner text.** The rule is "agents may cite, never write it" (`release-gates.md:22`; stated for the direction-selection record), and OB-01 (3) and its "runs in" cell put the commit with the owner (`merged-requirements.md:249`). B concedes that "a reviewer may read it as the agent being the committer of owner text". The byte check proves the bytes are unchanged; it does not prove who typed them (A-001).
5. **B requires spec edits.** OB-06 (d) (`merged-requirements.md:254`) and ADJ:191 ("The guard-flip PR itself must commit the owner's pass record") would both have to be reworded. That turns a yes/no owner question into a change request to two documents.
6. **B commits a record for a decision that has not been made.** The pass record scopes a switch-on whose scope is still Q6's open question (`merged-requirements.md:533`). If Q6 changes the scope, master ends up with an outdated owner record.

## 5. Concessions

1. **The single-disk risk is real, and C prolongs it.** Untracked files and unpushed commits in one worktree have no other copy. A worktree removal, disk loss or mistaken clean-up deletes them. The spec names this risk ("Evidence loss. Cleaning `issue-409-mvp` before OB-01 deletes records the flip PR must cite", `merged-requirements.md:264`). C's freeze addresses only deliberate cleaning, not accidents.
2. **The freeze is an instruction, not a guard.** A ledger entry stops nobody who does not read the ledger.
3. **C keeps the #409 issue wrong longer.** OB-08 is blocked by OB-01 (`merged-requirements.md:249`, `:256`), and the #409 body is wrong in 23 places (`merged-requirements.md:240`).
4. **Reviewers keep citing records they cannot open.** ADJ A-015 gives this 83 percent (ADJ:328), and C does nothing about it.
5. **C answers neither half of the question.** Authorship of the pass record and the final location of the records are both left unresolved. C is a postponement, not an answer.
6. **C's inventory is not complete for the whole worktree.** The sibling `git status` on 2026-11-14 also shows untracked `.dev/brainstorms/20261108-132433-orca-observer-mvp/` and four `.dev/reflect/...` directories. These are not owner records, and whether anyone needs them is UNVERIFIED, but a "do not clean" entry that names files should say whether they are covered.

## 6. Shared assumptions

- **A-001 (the sibling's files are unedited owner text): QUALIFY.** The pass record's first lines say "Written by the owner." (`question.md`, quoting the sibling file). But it sits in commits made in an agent-run worktree, and git cannot show who typed it (ADJ:478, INV-014). Only the owner can confirm it. A and B both commit on that assumption. C does not commit, so it does not depend on the assumption yet, but it only postpones the check. Every variant should ask the owner to confirm the files' content before anything is saved under their name.
- **A-002 (the owner accepts these records in the repository): QUALIFY.** IronClaude is a private fork (CLAUDE.md, PR-target rule), which lowers the exposure. But the records contain personal statements, and the owner has not said they accept them on master. A and OB-01 already allow "a named archive the owner chose" (`merged-requirements.md:249`); B allows only master. C does not depend on A-002, and its freeze is the natural bridge if the owner prefers an archive outside git.

## 7. Per-point positions

| Point | Better approach | Confidence | Reason |
|---|---|---|---|
| S-001 | A (tie; all three use the same sections) | 50% | No real difference. |
| C-001 (who commits) | A | 75% | OB-01 (3) and "the commit is the owner's" (`merged-requirements.md:249`); `release-gates.md:22`. |
| C-002 (when records reach master) | B | 60% | Sooner shortens the single-disk risk (`:264`); A's W1 timing is close behind; C's open-ended delay is the worst. |
| C-003 (how the pass record reaches master) | A | 55% | Matches OB-06 (d) and ADJ:191 with no spec edit, but only if the pass record is also archived or the sibling is held until OB-06 lands (weakness 4.1). |
| C-004 (authorship evidence) | B | 55% | A dated owner sentence naming the files is more concrete than "re-confirm", which A admits adds nothing. A re-typed record (A at full strength) would beat both. |
| C-005 (protecting the sibling until the records are safe) | C | 65% | The only explicit, dated, named-file protection that starts today; A and B rely only on the order of steps. |
| X-001 (may an agent commit owner text?) | A | 75% | `release-gates.md:22`; OB-01 (3); B concedes how a reviewer may read it. |
| X-002 (keep OB-06 (d) as written?) | A | 70% | No rewording of `merged-requirements.md:254` or ADJ:191 is needed. |
| A-001 | C | 55% | The only variant not yet committing on the assumption; none of them actually checks it. |
| A-002 | A | 65% | Offers the master-or-archive choice that OB-01 allows; B forces master. |

## 8. Overall verdict

The owner should pick **A, amended in two ways from C**: (1) today, write C's dated "do not clean `issue-409-mvp`" ledger entry with the full inventory; (2) put the pass record (and the two switch-on commits) into OB-01's commit or archive set, or keep the freeze until OB-06 lands, so that cleaning after OB-01 cannot delete them. **Confidence: 70%.**

Reason: A is the only answer that keeps owner authorship and the spec rows intact, and C's cheap freeze closes the gap A leaves open both before OB-01 and between OB-01 and OB-06.
