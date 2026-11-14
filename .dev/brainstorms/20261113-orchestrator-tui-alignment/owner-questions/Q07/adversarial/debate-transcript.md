# Adversarial Debate Transcript: Q7 owner-answer proposals

## Metadata
- Depth: quick
- Rounds completed: 1 (Round 2 skipped: depth=quick; Round 2.5 invariant probe skipped: --depth quick; Round 3 skipped: depth=quick)
- Convergence achieved: 100% (10 of 10 points agreed by at least 2 of 3 advocates; 2 unanimous)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 3 (spawned in parallel as separate agents; each wrote its own file)
- Variant mapping: variant-1 = proposal A, variant-2 = proposal B, variant-3 = proposal C

## Round 1: Advocate Statements

### Advocate for proposal A (source file: round1-advocate-A.md)

## Round 1 statement: advocate for variant 1 (proposal A)

- Debate: Q7 (owner authorship of the pass record; saving the sibling-only records)
- Mode A, depth quick, Round 1
- Date: 2026-11-14
- Abbreviations: MR = `.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md`; ADJ = `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md`; sibling = `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp`.

### 1. Position summary

Proposal A is the spec's own recommended answer ("Yes, both, before that worktree is cleaned", ADJ:777, MR:534): the owner personally writes or re-confirms the pass record in their own words and personally commits or archives the sibling-only records before `issue-409-mvp` is cleaned. It is the only variant that matches OB-01 and OB-06 exactly as written. On reflection, though, it leaves one real gap: the pass record stays on one disk until a switch-on that may never happen. Proposal B closes that gap.

### 2. Steelman of each opposing variant

**Proposal B (verbatim copy now, one dated owner sentence).** The strongest form of B: the records are at risk today, and A ties the pass record to the switch-on. That switch-on is gated on live-Orca tests (OB-03 and OB-04 need Q24 and Q30, MR:251-252) and on Q6, whose default is "the guard stays off and this PR is not opened" (MR:254). So under A the pass record can sit in unpushed commits indefinitely. B saves every file, the pass record included, in one records-only PR now. It does not ask an agent to *write* anything: it copies bytes and proves it with a byte comparison, so the letter of the rule "agents may cite, never write it" (sibling `release-gates.md:22`) is not breached. B is also closer to how the spec already expects commits to happen. The flip PR is opened "by the PR session" (MR:254, OB-06 (h)), and Q32's recommended answer is "the PR session commits named paths" (MR:559). So even under A's preferred route, an agent session would commit the pass record in OB-06. B just does it earlier, with an explicit owner sentence on top.

**Proposal C (freeze now, decide when the switch-on is scheduled).** The strongest form of C: owner attention is the scarcest resource in this program, and Q7 blocks less work than questions like Q1. If Q6 parks the switch-on, the pass record never needs to reach master at all, so any effort spent on it now is wasted. C still turns the spec's silent default (MR:534) into a dated, explicit ledger entry with an exact inventory, including `handoff-mvp-brainstorm.md`, which neither the spec nor A nor B names. C is honest that its guard is only an instruction.

### 3. Strengths claimed

1. **It is the spec's recommended answer, word for word.** ADJ:777 and MR:534 both give "Yes, both, before that worktree is cleaned". A needs no spec rewording. B needs OB-06 (d) and ADJ:191 changed, which B concedes itself (variant-2 line 24).
2. **It satisfies OB-01 as written, including its routing column.** OB-01's "runs in" cell says "owner's choice of branch (the commit is the owner's ...)" (MR:249), and its criterion (3) says "the owner, not an agent, is the author of the pass record (INV-014)". A gives both the commit and the authorship to the owner. B moves the OB-01 commit to an agent session, which contradicts that cell.
3. **It gives the strongest authorship evidence available.** INV-014 says: "the owner writes the record, agents cite it; git cannot show authorship, so Q7" (ADJ:478). If the owner types or re-reads the record in their own words, the owner is the person who produced the text. That is more than B's dated sentence confirming an existing file.
4. **It keeps the archive escape hatch.** A says "commits ... to master, or archives them in a named place of the owner's choosing" (variant-1 line 5), matching OB-01 (1) "(or in a named archive the owner chose)" (MR:249). B goes to master only. This matters for shared assumption A-002.
5. **It tests shared assumption A-001 instead of inheriting it.** The commits that hold the pass record were made in an agent-run worktree: `git log` in the sibling shows that commit `f104ca51a` ("cite the owner-written pass record ...") carries a `Co-Authored-By: Claude Code` trailer (read 2026-11-14; the trailer of `1ae72e1a1` is UNVERIFIED). An owner re-read in their own words is the only step in any variant that would catch an agent edit to text marked "Written by the owner." (sibling `owner-pass-record-20261112.md` lines 1-3).
6. **It names a real practical gap.** A states that the spec does not say which route the owner uses to commit on this host (which session, which worktree) (variant-1 line 23; U-001 in diff-analysis.md). That gap exists whichever variant is picked.

### 4. Weaknesses identified in the others

**Proposal B**

1. **It contradicts OB-01's routing cell.** MR:249 says "the commit is the owner's"; B has "a session the owner names" make the commit. That is a spec change B does not list. B lists only OB-06 (d).
2. **Its authorship evidence is weaker than its framing suggests.** One sentence confirming "the named files exactly as they stand" (variant-2 line 9) confirms whatever the files hold today, including any agent edit made in the agent-run sibling commits. It records consent, not authorship.
3. **It risks two versions of the pass record on master** if the owner later rewrites it for the actual flip. B concedes this (variant-2 line 25).
4. **It needs a permission row and a named session** before anything moves (variant-2 line 10). B's "smallest owner effort" claim leaves out that setup.

**Proposal C**

1. **It accepts a single-disk evidence-loss risk that the spec explicitly names.** "Cleaning `issue-409-mvp` before OB-01 deletes records the flip PR must cite (INV-002)" (MR:264). The pass record and the 2026-11-12 decision record exist only in local commits `1ae72e1a1` and `f104ca51a`, and `git branch -r --contains 1ae72e1a1` returned nothing (read 2026-11-14).
2. **Its guard is an instruction, not a mechanism.** C concedes this (variant-3 line 24).
3. **It keeps OB-08 blocked.** OB-01 blocks OB-08 (MR:249, MR:256), so the #409 body stays wrong in 23 places for longer (MR:240).
4. **It leaves authorship unresolved** (variant-3 line 28), which is half of the question asked.

### 5. Concessions

1. **A leaves the pass record exposed.** A says "After OB-01 is recorded, the sibling worktree may be cleaned" (variant-1 line 11). But OB-01 (1) lists `owner-decisions-20261108.md`, "the 2026-11-12 record", `live-test-guide.md` and `tuibbs-review/` (MR:249), and the pass record goes to master only inside the flip PR (OB-06 (d), MR:254). If the flip never opens (the Q6 default, MR:254), cleaning after OB-01 could lose the pass record. MR:249 does not say which file "the 2026-11-12 record" means: the decision record or the pass record, which are both dated 2026-11-12. A inherits that ambiguity. This is A's most serious flaw, and B fixes it.
2. **A's stance that the owner, not an agent, commits is inconsistent with the spec's own commit model.** The flip PR that A relies on is opened by "the PR session" (MR:254 (h)), and Q32 recommends that "the PR session commits named paths" (MR:559). So under A an agent session would commit the pass record anyway. The rule at `release-gates.md:22` forbids agents from *writing* owner records, not from committing them. A's X-001 position ("the person who typed the record is the owner, which is the only defence") is about who typed the text. It does not actually require the owner to be the person who commits.
3. **Re-confirmation adds nothing over today.** A admits that if the owner re-confirms rather than re-types, "the authorship evidence is the same as today" (variant-1 line 24). In that case A's authorship strength collapses to B's.
4. **A costs the most owner time:** a branch, a commit and a PR through `/sc:pr-submit`, or an archive decision. It also leaves open which route the owner uses to commit.
5. **A does not mention `handoff-mvp-brainstorm.md`** in its plan, only under "unresolved" (variant-1 line 28). C inventories it.

### 6. Shared assumptions

- **A-001 (the sibling's files are unedited owner text): QUALIFY.** It is plausible but unproven. The commits that hold the pass record were made in an agent-run worktree (`f104ca51a` carries a `Co-Authored-By: Claude Code` trailer, read 2026-11-14), and git cannot show who typed it (ADJ:478). Whichever variant wins should require the owner to read the files once before they are saved (A's re-read step), so the assumption is checked rather than assumed.
- **A-002 (the owner accepts these records in the repository): QUALIFY.** The repository is the owner's private fork (CLAUDE.md, "PR Target = Fork"). One owner record, `owner-decisions-20261111.md`, is already on master (MR:235), which suggests acceptance, but that is an inference, not an owner statement. A's archive option covers the case where it is false, and B should carry the same option.

### 7. Per-point positions

| Point | Better variant | Confidence | Reason |
|---|---|---|---|
| S-001 (section set) | A (tie) | 50% | All three use the same five sections; there is no real difference. |
| C-001 (who commits) | B | 60% | The spec's own model has an agent PR session commit (MR:254 (h), MR:559), and a byte-checked verbatim copy is not writing. A matches OB-01's "the commit is the owner's" cell, which keeps this close. |
| C-002 (when records reach master) | B | 70% | B saves everything now, independent of a switch-on gated on Q6, Q24 and Q30. A's W1 timing covers the four files but not the pass record. |
| C-003 (how the pass record reaches master) | B | 70% | B removes the window in which the pass record lives only in unpushed commits; A's route depends on OB-06 ever opening. Cost: OB-06 (d) and ADJ:191 must be reworded. |
| C-004 (authorship evidence) | A | 60% | An owner re-read or re-type in their own words is stronger than a one-sentence confirmation. The advantage vanishes if the owner only re-confirms. |
| C-005 (protection until safe) | B | 70% | "Clean only after the merge is verified" covers every file, including the pass record. A's "after OB-01 is recorded" can miss the pass record (concession 1), and C's protection is an instruction only. |
| X-001 (may an agent commit owner text?) | B | 60% | `release-gates.md:22` forbids writing, not committing, and the spec already plans agent commits of owner text. A reviewer may still read it as a breach, hence the modest confidence. |
| X-002 (keep OB-06 (d) as "committed in this PR"?) | B | 55% | INV-001's purpose is that the record survives until it is committed (ADJ:478), and B meets that earlier. A avoids spec churn, which keeps this near even. |
| A-001 (files are unedited owner text) | A | 65% | Only A includes an owner re-read step that tests the assumption. |
| A-002 (owner accepts records in the repo) | A | 60% | Only A keeps the named-archive option (matching MR:249 (1)) for the case where the owner does not want them on master. |

### 8. Overall verdict

Pick **a combination led by B, with three additions:**

- **From B:** a records-only PR now, with the pass record included, byte-checked, and the sibling cleaned only after the merge is verified.
- **From A:** the owner re-reads each file before the copy, and the named-archive option stays available.
- **From C:** the full inventory, with `handoff-mvp-brainstorm.md` decided explicitly, and a dated "do not clean" ledger entry that holds until the merge is verified.

Confidence: 70 percent. Reason: B is the only variant that removes the single-disk loss risk for every record, including the pass record, whether or not the switch-on ever happens, and A's re-read step is the cheapest way to make its authorship claim real rather than assumed. If the owner must pick one unmodified variant, B over A at about 60 percent.

### Advocate for proposal B (source file: round1-advocate-B.md)

## Round 1 advocate statement: proposal B (variant-2-original.md)

- Debate: Q7, sc:adversarial Mode A, depth quick, Round 1
- Advocate for: proposal B (owner confirms authorship in one dated sentence; a records-only PR copies the files verbatim now)
- Written: 2026-11-14

Evidence read for this statement (all read-only, 2026-11-14): the three variants and `diff-analysis.md`; `../question.md`; `merged-requirements.md` lines 230-265 and 530-560; `alignment-findings-adjudicated.md` lines 128, 142, 191, 328, 457, 478, 777; in the sibling worktree `issue-409-mvp`: `git status --short`, `git log --oneline -4`, `git show --stat` of `1ae72e1a1` and `f104ca51a`, the first 5 lines of `owner-pass-record-20261112.md`, and `release-gates.md` lines 18-26.

New fact from this read, used below (call it F-1): both sibling commits that hold owner records were made with git author `coder` (`1ae72e1a1`, 2026-11-12, adds `owner-decisions-20261112.md`; `f104ca51a`, 2026-11-13, adds `owner-pass-record-20261112.md`). `coder` is also this host's single git user (session git status header). So on this host an owner commit and an agent commit show the same author; git cannot record "the owner, not an agent, made this commit" under any proposal. (Whether the owner ever commits under a different identity: UNVERIFIED.)

### 1. Position summary

Proposal B gets every at-risk owner record onto master now, through a byte-checked, records-only PR the owner reviews and merges, and replaces an unobservable authorship condition ("the owner typed or committed it") with the only observable one this host can produce: a dated owner statement in the ledger. Its real cost is that two written conditions (OB-01 (3) and OB-06 (d)) must be reworded and that an agent session does the mechanical copy, which the owner has to accept explicitly.

### 2. Steelman of each opposing variant

**Proposal A (owner does both, before the sibling is cleaned).** A is the spec's own recommended answer, word for word (`merged-requirements.md:534`; ADJ:777, "Yes, both, before that worktree is cleaned"). It changes nothing in OB-01 or OB-06: OB-01 (3) already says "the owner, not an agent, is the author of the pass record" (`merged-requirements.md:249`) and OB-06 (d) already says "the owner-written pass record is committed in this PR" (`:254`); ADJ line 191 says "The guard-flip PR itself must commit the owner's pass record". A keeps the strictest reading of the project rule "agents may cite, never write it" (`release-gates.md:22`): no agent touches owner text at all. It lets the owner re-read and re-confirm the record in their own words, which is the strongest content check that the files say what the owner meant (it bears directly on A-001). Its best argument: an owner who does the commit personally has no ambiguity to explain to a reviewer later.

**Proposal C (freeze the sibling, decide when the switch-on is scheduled).** C costs the owner nothing now, and owner attention is the scarcest input in this program (33 owner questions, `merged-requirements.md:530-560`, several of which block more work). If Q6 parks the switch-on, the pass record, which names one Run (`run_93bfa00cae2b`, `merged-requirements.md:235`) for one switch-on, never needs to reach master, and the program avoids committing a record for an event that does not happen. C is honest about its own weakness ("an instruction, not a mechanical guard", `variant-3-original.md:24`) and gives the most exact inventory of what is at risk, including `handoff-mvp-brainstorm.md`, which the spec does not name (confirmed untracked in the sibling, read 2026-11-14). It matches the spec's default for an unanswered Q7 but makes it a dated choice.

### 3. Strengths claimed

1. **It removes the single-disk loss risk soonest.** The records are untracked files or in commits no remote branch holds (`question.md` fact row 2; `merged-requirements.md:234`: "remote branch `409-Phase2` is gone"). The spec names this risk (`merged-requirements.md:264`: "Cleaning `issue-409-mvp` before OB-01 deletes records the flip PR must cite"). B's PR is opened now and waits for no other gate; A waits for the owner's own time, and C waits indefinitely.
2. **It decouples saving records from a switch-on that may never happen.** OB-06 is blocked by SW-04, Q6, Q23, OB-01, OB-03, OB-04, OB-05, TB-CONSUME, Q25 and a grant (`merged-requirements.md:254`), and OB-03/OB-04 need live Orca and owner choices (Q24, Q30, `:551`, `:557`). Under A, the pass record reaches master only "inside the switch-on pull request" (`variant-1-original.md:10`), so if the switch-on is parked the pass record stays on one disk. B saves it either way. The diff analysis rates this contribution High (U-002).
3. **Its authorship evidence is the only kind this host can show.** By F-1, every commit here has author `coder`. A's defence, "the person who typed the record is the owner" (`variant-1-original.md:18`), may be true but cannot be observed later. ADJ itself says "git cannot show authorship, so Q7" (line 478). A dated owner sentence in the XC-01 ledger is a positive, checkable owner statement.
4. **Verbatim plus byte check limits the agent to transport.** B requires "byte for byte, with no edits ... checked by a byte comparison in the PR" (`variant-2-original.md:5`, `:9`) and staging "those named paths only" (`:10`). The agent writes no owner sentence; it moves bytes the owner then reviews and merges. Note also F-1: the pass record and the 2026-11-12 record are already inside agent-made commits in the sibling (`f104ca51a`, `1ae72e1a1`, both of which also change code or `release-gates.md`). The status quo already has an agent session as committer of owner text; B adds an owner statement and an owner merge on top of that.
5. **Lowest owner effort that still puts an owner act on record.** One sentence plus one merge (`variant-2-original.md:18`). The owner still performs the consequential act (the merge).
6. **It follows the project's PR route.** Fresh branch from `origin/master` (required: `origin/master` is not an ancestor of the sibling HEAD, ADJ:128), `/sc:pr-submit` on the fork (`CLAUDE.md` PR rule), named paths only, under a permission row (consistent with the GRANT rows used for OB-06 and OB-07, `merged-requirements.md:254-255`).
7. **It unblocks OB-08 earlier.** OB-01 blocks OB-08 (`merged-requirements.md:249`), and the #409 body is wrong in 23 places (`:240`). Records on master let OB-08 cite master paths sooner.

### 4. Weaknesses identified in the others

1. **A ties the pass record's safety to the switch-on.** A puts four records on master in W1 but leaves the pass record to "enter master inside the switch-on pull request" (`variant-1-original.md:10`), and then says "After OB-01 is recorded, the sibling worktree may be cleaned" (`:11`). Read literally, A permits cleaning the sibling while the pass record exists only in unpushed commit `f104ca51a`. That gap closes only if A is read to save the pass record in OB-01 too, which OB-01 (1) as worded does not list explicitly (it names "the 2026-11-12 record", singular, `merged-requirements.md:249`).
2. **A's authorship guarantee is unobservable here.** By F-1, an owner commit and an agent commit look the same. A concedes: "If the existing pass record ... is simply re-confirmed rather than re-typed, the authorship evidence is the same as today" (`variant-1-original.md:24`). So A's extra cost buys no extra recorded evidence unless the owner retypes the file, which would create a second, different version of a record that `release-gates.md` in the sibling already cites (changed in `f104ca51a`).
3. **A leaves the commit route open.** A admits "The owner's commit route on this host is not specified in the spec (which session, which worktree)" (`variant-1-original.md:23`). Project rules require worktrees to be created through Orca with an agent (`CLAUDE.md`), so in practice the owner's commit will likely happen in an agent-attached worktree too, which narrows A's practical difference from B. (How the owner commits by hand on this host: UNVERIFIED.)
4. **C keeps the one risk every variant agrees is real.** A-003 is stated by all three (`diff-analysis.md`; `merged-requirements.md:264`). C's guard is "an instruction, not a mechanical guard" (`variant-3-original.md:24`) and does nothing about disk loss or a mistaken `git worktree remove` (`:21`). C has no end date: it re-asks "when the switch-on pull request is actually scheduled" (`:5`), which may be never.
5. **C keeps reviewers citing records they cannot open.** ADJ A-015 (83 percent, line 328); C admits this persists (`variant-3-original.md:22`) and that OB-08 waits (`:23`).
6. **C's saving on owner attention is small.** B's owner cost is one sentence and one merge; C trades that for an open-ended loss risk on the records the "observer first, TUIBBS later" direction rests on (ADJ INV-002, line 457).

### 5. Concessions (proposal B's real weaknesses)

1. **It changes written conditions.** OB-01 (3) ("the owner, not an agent, is the author of the pass record", `merged-requirements.md:249`), OB-06 (d) ("committed in this PR", `:254`) and ADJ line 191 must be reworded. These are owner decisions, not facts B can assume.
2. **It sits close to "agents may cite, never write it" (`release-gates.md:22`).** That rule is stated for the direction-selection record, not for every owner record (`question.md` fact row 6), so applying it here is an inference either way. A reviewer may still read an agent commit of owner text as writing. B's defence (verbatim, byte check, owner merge, owner sentence) is an interpretation the owner must adopt explicitly.
3. **The owner sentence can cover files the owner has not re-read.** If A-001 is false, B's "confirm the existing files" sentence would put the owner's name on text the owner did not write. A's re-read protects better. B as written says only that the PR is "for the owner to review and merge" (`variant-2-original.md:5`); it should require the owner to read the diff before writing the sentence.
4. **It can leave two versions of the pass record** if the owner later rewrites it for a different Q6 scope (`variant-2-original.md:25`).
5. **The copying session is still to be named** ("a session the owner names", `variant-2-original.md:10`), much like A's open commit route.
6. **It omits the spec's archive alternative.** OB-01 allows "a named archive the owner chose" (`merged-requirements.md:249`); B names master only.
7. **Inclusion of `handoff-mvp-brainstorm.md` is open** (`variant-2-original.md:29`), as in A.

### 6. Shared assumptions

- **A-001 (the sibling's files are unedited owner text): QUALIFY.** It cannot be accepted as stated: the pass record and the 2026-11-12 record sit in agent-run commits (F-1), and the untracked files have no history at all. It should not be rejected either: the pass record opens "Written by the owner." (sibling file, lines 1-3). The right treatment is an explicit owner check: the owner reads the byte-identical diff (B) or re-reads the files (A) and records a dated sentence only after that. Only the owner can close A-001.
- **A-002 (the owner accepts these records in the repository): QUALIFY.** The repository is the private fork (`CLAUDE.md` PR rule), and one owner record, `owner-decisions-20261111.md`, is already on master (ADJ E-16, line 142), which suggests the owner has accepted such records there before. But the others contain personal statements, and the spec offers "a named archive the owner chose" (`merged-requirements.md:249`). Whichever variant is picked should keep that archive alternative; B as written does not.

### 7. Per-point positions

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

### 8. Overall verdict

An owner should pick **a combination: B's timing and scope with A's owner re-read and archive option** (confidence 70 percent): all sibling-only records, the pass record included, go to master (or a named archive) now in one records-only, byte-checked PR, made by the owner or by a session the owner names if the owner rules a verbatim copy acceptable; the owner re-reads them, records a dated ledger sentence, and merges; OB-06 (d) is reworded to "on master and cited". Reason: saving every record now, independent of the switch-on, removes the one risk all three variants agree on, while the owner's re-read and dated statement are the only authorship evidence this host can actually show. If the owner will not reword OB-06 (d), plain A is next best, provided OB-01 also saves the pass record before the sibling is cleaned; C is weakest because it leaves the records on one disk with no end date.

### Advocate for proposal C (source file: round1-advocate-C.md)

## Round 1: advocate for variant 3 (proposal C, "not now; freeze the sibling worktree")

Debate: Q7, sc:adversarial Mode A, depth quick, Round 1. Written 2026-11-14.

Evidence I re-read for this statement (2026-11-14): `merged-requirements.md` lines 230-265 and 530-560; `alignment-findings-adjudicated.md` (ADJ) lines 128, 142, 191, 328, 457, 478, 777; sibling `issue-409-mvp` `git status --short`, `git log --oneline -4`, `git branch -r --contains` for `1ae72e1a1` and `f104ca51a` (both returned no remote branch); sibling `.dev/issues/409/bmad/spec-orca-observer/release-gates.md` line 22.

### 1. Position summary

C says: move nothing now, write a dated "do not clean `issue-409-mvp`" entry that names every file at risk, and ask Q7 again when the switch-on pull request is actually scheduled. Its real value is the freeze entry and the exact inventory, which cost almost nothing. As a full answer to Q7 it is weaker than A, because it leaves the only copies of the owner's records on one disk for an open-ended time.

### 2. Steelman of each opposing variant

**A (owner does both, before cleaning).** A is the answer the spec and ADJ already recommend, word for word ("Yes, both, before that worktree is cleaned", ADJ:777; `merged-requirements.md:534`). It is the only variant that fully meets OB-01 as written: OB-01 (3) requires "the owner, not an agent, is the author of the pass record", and its "runs in" cell says "the commit is the owner's" (`merged-requirements.md:249`). It keeps OB-06 (d) unchanged ("the owner-written pass record is committed in this PR", `merged-requirements.md:254`; ADJ:191 "The guard-flip PR itself must commit the owner's pass record"), so no spec row has to be reworded. It also offers the archive route, so an owner who does not want personal records in the repository still has a compliant path. Under A, the person who commits is the person who wrote the text, which is the strongest answer available to "git cannot show who typed it" (ADJ:478, INV-014).

**B (one owner sentence; a records-only PR copies the files byte for byte now).** B removes the evidence-loss risk fastest. Every owner record, the pass record included, lands on master in days, and that does not depend on the switch-on, which is gated on live-Orca tests (Q24, Q30) that may never run. A byte comparison makes the copy auditable: what reaches master is provably identical to what sits in the sibling. One dated sentence in the ledger is a concrete owner statement, tied to named files and a date, which is more precise than "re-confirm". Owner cost is one sentence and one merge. OB-08 can then cite master paths early.

### 3. Strengths claimed

1. **It names the full risk precisely.** C is the only variant that lists every file at risk with where it lives: the pass record and `owner-decisions-20261112.md` in unpushed local commits `1ae72e1a1` and `f104ca51a`, plus the untracked `owner-decisions-20261108.md`, `live-test-guide.md`, `tuibbs-review/` and `handoff-mvp-brainstorm.md`. I re-checked this on 2026-11-14: the sibling `git status` shows those four paths as untracked, `git log` shows the two commits at HEAD, and `git branch -r --contains` returns no remote branch for either commit. A's OB-01 list leaves out the pass record (A sends it through OB-06 later) and does not mention `handoff-mvp-brainstorm.md`.
2. **It costs the least now.** It needs no branch, no pull request and no `/sc:pr-submit` run. The owner's attention goes to questions that block more work. The spec's own default for an unanswered Q7 is the same freeze ("`issue-409-mvp` must not be cleaned", `merged-requirements.md:534`). C turns that silent default into a dated, explicit choice.
3. **It does not force a decision on a switch-on that may never happen.** OB-06 is held unless Q6 is answered ("Default if Q6 is unanswered: the guard stays off and this PR is not opened", `merged-requirements.md:254`). The pass record names one Run, `run_93bfa00cae2b` (`merged-requirements.md:235`). Committing it before anyone knows whether the flip will happen risks a record that is stale or later rewritten. B itself names this risk ("two versions on master").
4. **It matches the trigger ADJ actually set.** ADJ's timing is "Waits for: before the sibling worktree is cleaned" (ADJ:191), and A-015's timing is "before the sibling worktree is cleaned / unblocks the flip PR" (ADJ:328). Neither says "now". C keeps that ordering and makes the "not cleaned" half explicit.
5. **It is never in conflict with the "agents may cite, never write" rule** (`release-gates.md:22`), because no agent touches the owner's text.

### 4. Weaknesses identified in the others

1. **A's own clean-up step can lose the pass record.** A says "After OB-01 is recorded, the sibling worktree may be cleaned". But under A the pass record is not in OB-01; it reaches master only "inside the switch-on pull request". If OB-01 is done and the sibling is then cleaned before OB-06 opens (or if OB-06 never opens), the pass record and the switch-on commits are deleted. They exist only in `1ae72e1a1` and `f104ca51a`, which no remote branch holds. The same gap exists in OB-01 as the spec writes it. The fix is either to put the pass record in OB-01's archive set, or to hold the clean-up until OB-06 lands, which is C's freeze.
2. **A's authorship defence is thinner than it reads.** A admits that if the existing record is "simply re-confirmed rather than re-typed, the authorship evidence is the same as today". So unless the owner re-types the record, A's "unambiguous" authorship comes down to who makes the commit, not who wrote the file.
3. **A leaves the commit route unspecified.** A admits "The owner's commit route on this host is not specified" (U-001). Until that route is chosen, A does not make anything safer than C does.
4. **B puts an agent in the committer seat for owner text.** The rule is "agents may cite, never write it" (`release-gates.md:22`; stated for the direction-selection record), and OB-01 (3) and its "runs in" cell put the commit with the owner (`merged-requirements.md:249`). B concedes that "a reviewer may read it as the agent being the committer of owner text". The byte check proves the bytes are unchanged; it does not prove who typed them (A-001).
5. **B requires spec edits.** OB-06 (d) (`merged-requirements.md:254`) and ADJ:191 ("The guard-flip PR itself must commit the owner's pass record") would both have to be reworded. That turns a yes/no owner question into a change request to two documents.
6. **B commits a record for a decision that has not been made.** The pass record scopes a switch-on whose scope is still Q6's open question (`merged-requirements.md:533`). If Q6 changes the scope, master ends up with an outdated owner record.

### 5. Concessions

1. **The single-disk risk is real, and C prolongs it.** Untracked files and unpushed commits in one worktree have no other copy. A worktree removal, disk loss or mistaken clean-up deletes them. The spec names this risk ("Evidence loss. Cleaning `issue-409-mvp` before OB-01 deletes records the flip PR must cite", `merged-requirements.md:264`). C's freeze addresses only deliberate cleaning, not accidents.
2. **The freeze is an instruction, not a guard.** A ledger entry stops nobody who does not read the ledger.
3. **C keeps the #409 issue wrong longer.** OB-08 is blocked by OB-01 (`merged-requirements.md:249`, `:256`), and the #409 body is wrong in 23 places (`merged-requirements.md:240`).
4. **Reviewers keep citing records they cannot open.** ADJ A-015 gives this 83 percent (ADJ:328), and C does nothing about it.
5. **C answers neither half of the question.** Authorship of the pass record and the final location of the records are both left unresolved. C is a postponement, not an answer.
6. **C's inventory is not complete for the whole worktree.** The sibling `git status` on 2026-11-14 also shows untracked `.dev/brainstorms/20261108-132433-orca-observer-mvp/` and four `.dev/reflect/...` directories. These are not owner records, and whether anyone needs them is UNVERIFIED, but a "do not clean" entry that names files should say whether they are covered.

### 6. Shared assumptions

- **A-001 (the sibling's files are unedited owner text): QUALIFY.** The pass record's first lines say "Written by the owner." (`question.md`, quoting the sibling file). But it sits in commits made in an agent-run worktree, and git cannot show who typed it (ADJ:478, INV-014). Only the owner can confirm it. A and B both commit on that assumption. C does not commit, so it does not depend on the assumption yet, but it only postpones the check. Every variant should ask the owner to confirm the files' content before anything is saved under their name.
- **A-002 (the owner accepts these records in the repository): QUALIFY.** IronClaude is a private fork (CLAUDE.md, PR-target rule), which lowers the exposure. But the records contain personal statements, and the owner has not said they accept them on master. A and OB-01 already allow "a named archive the owner chose" (`merged-requirements.md:249`); B allows only master. C does not depend on A-002, and its freeze is the natural bridge if the owner prefers an archive outside git.

### 7. Per-point positions

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

### 8. Overall verdict

The owner should pick **A, amended in two ways from C**: (1) today, write C's dated "do not clean `issue-409-mvp`" ledger entry with the full inventory; (2) put the pass record (and the two switch-on commits) into OB-01's commit or archive set, or keep the freeze until OB-06 lands, so that cleaning after OB-01 cannot delete them. **Confidence: 70%.**

Reason: A is the only answer that keeps owner authorship and the spec rows intact, and C's cheap freeze closes the gap A leaves open both before OB-01 and between OB-01 and OB-06.

## Scoring Matrix

| Diff Point | Level | Advocate A | Advocate B | Advocate C | Winner | Confidence | Evidence Summary |
|---|---|---|---|---|---|---|---|
| S-001 | L1 | tie | tie | tie | tie (no winner) | 50% | Same five sections. |
| C-001 | L2 | B 60 | B 60 | A 75 | B | 60% | The spec's own model has the PR session commit (merged-requirements.md:254 (h), :559); C's advocate holds that OB-01 (3) makes the commit the owner's (:249). |
| C-002 | L2 | B 70 | B 80 | B 60 | B | 85% | Unanimous: saving now shortens the single-disk loss window (:264). |
| C-003 | L2 | B 70 | B 70 | A 55 | B | 65% | Under A the pass record reaches master only inside a switch-on that may be parked (A's advocate concession 1). |
| C-004 | L2 | A 60 | A 60 | B 55 | A | 60% | An owner re-read in their own words tests authorship; a one-line confirmation alone does not. |
| C-005 | L3 | B 70 | B 75 | C 65 | B | 65% | "Clean only after the merge is verified" covers every file; C's freeze starts today but is only an instruction. |
| X-001 | L3 | B 60 | A 55 | A 75 | A | 60% | Against the written rule (`release-gates.md:22`, OB-01 (3)), the owner committing is safer; an agent copy needs an explicit owner ruling. B's own advocate voted A here. |
| X-002 | L3 | B 55 | B 65 | A 70 | B | 60% | "On master and cited" serves the purpose of OB-06 (d) and survives a parked switch-on; needs owner rewording. |
| A-001 | L3 | A 65 | A 60 | C 55 | A | 65% | All three QUALIFY: the files sit in agent-run commits (a co-author trailer on `f104ca51a`); only the owner can confirm; A's re-read step tests it. |
| A-002 | L2 | A 60 | A 55 | A 65 | A | 80% | Unanimous: keep the spec's "named archive" alternative (merged-requirements.md:249); B as written omits it. |

Shared-assumption responses: A-001 QUALIFY x3; A-002 QUALIFY x3. No omissions.

## Overall verdicts (section 8 of each statement)

| Advocate | Picks | Confidence |
|---|---|---|
| A (for owner does it in W1) | Combination led by B: records-only PR now including the pass record, plus A's owner re-read and archive option, plus C's inventory and freeze | 70% (B over A at 60% if unmodified) |
| B (for records-only PR now) | Combination: B's timing and scope with A's owner re-read and archive option; agent copy only if the owner rules it acceptable | 70% |
| C (for freeze and defer) | A amended with C's freeze entry today, and the pass record added to OB-01's save set (or the freeze kept until OB-06 lands) | 70% |

Agreement on the headline: 2 of 3 chose a B-led combination; 1 of 3 chose an A-led combination. All three combinations share the same core: save every record, the pass record included, before any cleaning and without waiting for the switch-on; owner reads the files first; keep the archive option; write a dated freeze entry now. The remaining disagreement is who makes the commit (owner, or a named session on an explicit owner ruling).

## Convergence Assessment
- Points resolved: 10 of 10 (majority rule); unanimous: C-002, A-002 (S-001 tie unanimous)
- Alignment: 100%
- Threshold: 80%
- Taxonomy coverage: L1 (S-001), L2 (C-001 to C-004, A-002), L3 (C-005, X-001, X-002, A-001): all covered
- Invariant probe gate: not applied (Round 2.5 skipped at quick depth)
- Status: CONVERGED (per-point); headline verdict 2 of 3
- Unresolved points: none by majority rule. Standing dissent: C's advocate on C-001, C-003, X-002 (favouring A).
