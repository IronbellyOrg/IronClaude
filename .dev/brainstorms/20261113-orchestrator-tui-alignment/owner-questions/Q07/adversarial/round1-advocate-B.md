# Round 1 advocate statement: proposal B (variant-2-original.md)

- Debate: Q7, sc:adversarial Mode A, depth quick, Round 1
- Advocate for: proposal B (owner confirms authorship in one dated sentence; a records-only PR copies the files verbatim now)
- Written: 2026-11-14

Evidence read for this statement (all read-only, 2026-11-14): the three variants and `diff-analysis.md`; `../question.md`; `merged-requirements.md` lines 230-265 and 530-560; `alignment-findings-adjudicated.md` lines 128, 142, 191, 328, 457, 478, 777; in the sibling worktree `issue-409-mvp`: `git status --short`, `git log --oneline -4`, `git show --stat` of `1ae72e1a1` and `f104ca51a`, the first 5 lines of `owner-pass-record-20261112.md`, and `release-gates.md` lines 18-26.

New fact from this read, used below (call it F-1): both sibling commits that hold owner records were made with git author `coder` (`1ae72e1a1`, 2026-11-12, adds `owner-decisions-20261112.md`; `f104ca51a`, 2026-11-13, adds `owner-pass-record-20261112.md`). `coder` is also this host's single git user (session git status header). So on this host an owner commit and an agent commit show the same author; git cannot record "the owner, not an agent, made this commit" under any proposal. (Whether the owner ever commits under a different identity: UNVERIFIED.)

## 1. Position summary

Proposal B gets every at-risk owner record onto master now, through a byte-checked, records-only PR the owner reviews and merges, and replaces an unobservable authorship condition ("the owner typed or committed it") with the only observable one this host can produce: a dated owner statement in the ledger. Its real cost is that two written conditions (OB-01 (3) and OB-06 (d)) must be reworded and that an agent session does the mechanical copy, which the owner has to accept explicitly.

## 2. Steelman of each opposing variant

**Proposal A (owner does both, before the sibling is cleaned).** A is the spec's own recommended answer, word for word (`merged-requirements.md:534`; ADJ:777, "Yes, both, before that worktree is cleaned"). It changes nothing in OB-01 or OB-06: OB-01 (3) already says "the owner, not an agent, is the author of the pass record" (`merged-requirements.md:249`) and OB-06 (d) already says "the owner-written pass record is committed in this PR" (`:254`); ADJ line 191 says "The guard-flip PR itself must commit the owner's pass record". A keeps the strictest reading of the project rule "agents may cite, never write it" (`release-gates.md:22`): no agent touches owner text at all. It lets the owner re-read and re-confirm the record in their own words, which is the strongest content check that the files say what the owner meant (it bears directly on A-001). Its best argument: an owner who does the commit personally has no ambiguity to explain to a reviewer later.

**Proposal C (freeze the sibling, decide when the switch-on is scheduled).** C costs the owner nothing now, and owner attention is the scarcest input in this program (33 owner questions, `merged-requirements.md:530-560`, several of which block more work). If Q6 parks the switch-on, the pass record, which names one Run (`run_93bfa00cae2b`, `merged-requirements.md:235`) for one switch-on, never needs to reach master, and the program avoids committing a record for an event that does not happen. C is honest about its own weakness ("an instruction, not a mechanical guard", `variant-3-original.md:24`) and gives the most exact inventory of what is at risk, including `handoff-mvp-brainstorm.md`, which the spec does not name (confirmed untracked in the sibling, read 2026-11-14). It matches the spec's default for an unanswered Q7 but makes it a dated choice.

## 3. Strengths claimed

1. **It removes the single-disk loss risk soonest.** The records are untracked files or in commits no remote branch holds (`question.md` fact row 2; `merged-requirements.md:234`: "remote branch `409-Phase2` is gone"). The spec names this risk (`merged-requirements.md:264`: "Cleaning `issue-409-mvp` before OB-01 deletes records the flip PR must cite"). B's PR is opened now and waits for no other gate; A waits for the owner's own time, and C waits indefinitely.
2. **It decouples saving records from a switch-on that may never happen.** OB-06 is blocked by SW-04, Q6, Q23, OB-01, OB-03, OB-04, OB-05, TB-CONSUME, Q25 and a grant (`merged-requirements.md:254`), and OB-03/OB-04 need live Orca and owner choices (Q24, Q30, `:551`, `:557`). Under A, the pass record reaches master only "inside the switch-on pull request" (`variant-1-original.md:10`), so if the switch-on is parked the pass record stays on one disk. B saves it either way. The diff analysis rates this contribution High (U-002).
3. **Its authorship evidence is the only kind this host can show.** By F-1, every commit here has author `coder`. A's defence, "the person who typed the record is the owner" (`variant-1-original.md:18`), may be true but cannot be observed later. ADJ itself says "git cannot show authorship, so Q7" (line 478). A dated owner sentence in the XC-01 ledger is a positive, checkable owner statement.
4. **Verbatim plus byte check limits the agent to transport.** B requires "byte for byte, with no edits ... checked by a byte comparison in the PR" (`variant-2-original.md:5`, `:9`) and staging "those named paths only" (`:10`). The agent writes no owner sentence; it moves bytes the owner then reviews and merges. Note also F-1: the pass record and the 2026-11-12 record are already inside agent-made commits in the sibling (`f104ca51a`, `1ae72e1a1`, both of which also change code or `release-gates.md`). The status quo already has an agent session as committer of owner text; B adds an owner statement and an owner merge on top of that.
5. **Lowest owner effort that still puts an owner act on record.** One sentence plus one merge (`variant-2-original.md:18`). The owner still performs the consequential act (the merge).
6. **It follows the project's PR route.** Fresh branch from `origin/master` (required: `origin/master` is not an ancestor of the sibling HEAD, ADJ:128), `/sc:pr-submit` on the fork (`CLAUDE.md` PR rule), named paths only, under a permission row (consistent with the GRANT rows used for OB-06 and OB-07, `merged-requirements.md:254-255`).
7. **It unblocks OB-08 earlier.** OB-01 blocks OB-08 (`merged-requirements.md:249`), and the #409 body is wrong in 23 places (`:240`). Records on master let OB-08 cite master paths sooner.

## 4. Weaknesses identified in the others

1. **A ties the pass record's safety to the switch-on.** A puts four records on master in W1 but leaves the pass record to "enter master inside the switch-on pull request" (`variant-1-original.md:10`), and then says "After OB-01 is recorded, the sibling worktree may be cleaned" (`:11`). Read literally, A permits cleaning the sibling while the pass record exists only in unpushed commit `f104ca51a`. That gap closes only if A is read to save the pass record in OB-01 too, which OB-01 (1) as worded does not list explicitly (it names "the 2026-11-12 record", singular, `merged-requirements.md:249`).
2. **A's authorship guarantee is unobservable here.** By F-1, an owner commit and an agent commit look the same. A concedes: "If the existing pass record ... is simply re-confirmed rather than re-typed, the authorship evidence is the same as today" (`variant-1-original.md:24`). So A's extra cost buys no extra recorded evidence unless the owner retypes the file, which would create a second, different version of a record that `release-gates.md` in the sibling already cites (changed in `f104ca51a`).
3. **A leaves the commit route open.** A admits "The owner's commit route on this host is not specified in the spec (which session, which worktree)" (`variant-1-original.md:23`). Project rules require worktrees to be created through Orca with an agent (`CLAUDE.md`), so in practice the owner's commit will likely happen in an agent-attached worktree too, which narrows A's practical difference from B. (How the owner commits by hand on this host: UNVERIFIED.)
4. **C keeps the one risk every variant agrees is real.** A-003 is stated by all three (`diff-analysis.md`; `merged-requirements.md:264`). C's guard is "an instruction, not a mechanical guard" (`variant-3-original.md:24`) and does nothing about disk loss or a mistaken `git worktree remove` (`:21`). C has no end date: it re-asks "when the switch-on pull request is actually scheduled" (`:5`), which may be never.
5. **C keeps reviewers citing records they cannot open.** ADJ A-015 (83 percent, line 328); C admits this persists (`variant-3-original.md:22`) and that OB-08 waits (`:23`).
6. **C's saving on owner attention is small.** B's owner cost is one sentence and one merge; C trades that for an open-ended loss risk on the records the "observer first, TUIBBS later" direction rests on (ADJ INV-002, line 457).

## 5. Concessions (proposal B's real weaknesses)

1. **It changes written conditions.** OB-01 (3) ("the owner, not an agent, is the author of the pass record", `merged-requirements.md:249`), OB-06 (d) ("committed in this PR", `:254`) and ADJ line 191 must be reworded. These are owner decisions, not facts B can assume.
2. **It sits close to "agents may cite, never write it" (`release-gates.md:22`).** That rule is stated for the direction-selection record, not for every owner record (`question.md` fact row 6), so applying it here is an inference either way. A reviewer may still read an agent commit of owner text as writing. B's defence (verbatim, byte check, owner merge, owner sentence) is an interpretation the owner must adopt explicitly.
3. **The owner sentence can cover files the owner has not re-read.** If A-001 is false, B's "confirm the existing files" sentence would put the owner's name on text the owner did not write. A's re-read protects better. B as written says only that the PR is "for the owner to review and merge" (`variant-2-original.md:5`); it should require the owner to read the diff before writing the sentence.
4. **It can leave two versions of the pass record** if the owner later rewrites it for a different Q6 scope (`variant-2-original.md:25`).
5. **The copying session is still to be named** ("a session the owner names", `variant-2-original.md:10`), much like A's open commit route.
6. **It omits the spec's archive alternative.** OB-01 allows "a named archive the owner chose" (`merged-requirements.md:249`); B names master only.
7. **Inclusion of `handoff-mvp-brainstorm.md` is open** (`variant-2-original.md:29`), as in A.

## 6. Shared assumptions

- **A-001 (the sibling's files are unedited owner text): QUALIFY.** It cannot be accepted as stated: the pass record and the 2026-11-12 record sit in agent-run commits (F-1), and the untracked files have no history at all. It should not be rejected either: the pass record opens "Written by the owner." (sibling file, lines 1-3). The right treatment is an explicit owner check: the owner reads the byte-identical diff (B) or re-reads the files (A) and records a dated sentence only after that. Only the owner can close A-001.
- **A-002 (the owner accepts these records in the repository): QUALIFY.** The repository is the private fork (`CLAUDE.md` PR rule), and one owner record, `owner-decisions-20261111.md`, is already on master (ADJ E-16, line 142), which suggests the owner has accepted such records there before. But the others contain personal statements, and the spec offers "a named archive the owner chose" (`merged-requirements.md:249`). Whichever variant is picked should keep that archive alternative; B as written does not.

## 7. Per-point positions

| Point | Better approach | Confidence | Reason |
|---|---|---|---|
| S-001 (section set) | none (A, B and C tie) | 90% | Same five sections; nothing to choose. |
| C-001 (who makes the commit) | B | 60% | The committer shows as `coder` whoever acts (F-1); B adds a byte check and an owner merge. A is cleaner against the rule text, so confidence is moderate. |
| C-002 (when records reach master) | B | 80% | Now, independent of the switch-on; A's W1 timing is close but leaves the pass record tied to OB-06. |
| C-003 (how the pass record reaches master) | B | 70% | Saving it does not depend on a switch-on that may be parked; A matches the spec as written. |
| C-004 (authorship evidence) | A | 60% | An owner re-read in their own words closes A-001 better; B's sentence is more observable but should follow that read. Close call. |
| C-005 (protecting the sibling until records are safe) | B | 75% | "After the merge is verified" is checkable on the remote; A's "after OB-01" may leave the pass record unsaved; C's is an instruction only. |
| X-001 (may an agent commit owner text?) | A | 55% | Against the written rule, A is safer; B's position needs an explicit owner ruling. |
| X-002 (must OB-06 (d) stay "committed in this PR"?) | B | 65% | "Already on master and cited" serves the same purpose and survives a parked switch-on; the owner must reword the spec. |
| A-001 (files are unedited owner text) | A | 60% | A's owner re-read addresses it directly; B does only if the owner reads the diff before the sentence. |
| A-002 (owner accepts records in the repo) | A | 55% | A keeps the spec's named-archive alternative explicitly (`variant-1-original.md:5`); B omits it. |

## 8. Overall verdict

An owner should pick **a combination: B's timing and scope with A's owner re-read and archive option** (confidence 70 percent): all sibling-only records, the pass record included, go to master (or a named archive) now in one records-only, byte-checked PR, made by the owner or by a session the owner names if the owner rules a verbatim copy acceptable; the owner re-reads them, records a dated ledger sentence, and merges; OB-06 (d) is reworded to "on master and cited". Reason: saving every record now, independent of the switch-on, removes the one risk all three variants agree on, while the owner's re-read and dated statement are the only authorship evidence this host can actually show. If the owner will not reword OB-06 (d), plain A is next best, provided OB-01 also saves the pass record before the sibling is cleaned; C is weakest because it leaves the records on one disk with no end date.
