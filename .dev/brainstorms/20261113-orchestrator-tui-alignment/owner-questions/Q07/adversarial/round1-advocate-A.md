# Round 1 statement: advocate for variant 1 (proposal A)

- Debate: Q7 (owner authorship of the pass record; saving the sibling-only records)
- Mode A, depth quick, Round 1
- Date: 2026-11-14
- Abbreviations: MR = `.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md`; ADJ = `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md`; sibling = `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp`.

## 1. Position summary

Proposal A is the spec's own recommended answer ("Yes, both, before that worktree is cleaned", ADJ:777, MR:534): the owner personally writes or re-confirms the pass record in their own words and personally commits or archives the sibling-only records before `issue-409-mvp` is cleaned. It is the only variant that matches OB-01 and OB-06 exactly as written. On reflection, though, it leaves one real gap: the pass record stays on one disk until a switch-on that may never happen. Proposal B closes that gap.

## 2. Steelman of each opposing variant

**Proposal B (verbatim copy now, one dated owner sentence).** The strongest form of B: the records are at risk today, and A ties the pass record to the switch-on. That switch-on is gated on live-Orca tests (OB-03 and OB-04 need Q24 and Q30, MR:251-252) and on Q6, whose default is "the guard stays off and this PR is not opened" (MR:254). So under A the pass record can sit in unpushed commits indefinitely. B saves every file, the pass record included, in one records-only PR now. It does not ask an agent to *write* anything: it copies bytes and proves it with a byte comparison, so the letter of the rule "agents may cite, never write it" (sibling `release-gates.md:22`) is not breached. B is also closer to how the spec already expects commits to happen. The flip PR is opened "by the PR session" (MR:254, OB-06 (h)), and Q32's recommended answer is "the PR session commits named paths" (MR:559). So even under A's preferred route, an agent session would commit the pass record in OB-06. B just does it earlier, with an explicit owner sentence on top.

**Proposal C (freeze now, decide when the switch-on is scheduled).** The strongest form of C: owner attention is the scarcest resource in this program, and Q7 blocks less work than questions like Q1. If Q6 parks the switch-on, the pass record never needs to reach master at all, so any effort spent on it now is wasted. C still turns the spec's silent default (MR:534) into a dated, explicit ledger entry with an exact inventory, including `handoff-mvp-brainstorm.md`, which neither the spec nor A nor B names. C is honest that its guard is only an instruction.

## 3. Strengths claimed

1. **It is the spec's recommended answer, word for word.** ADJ:777 and MR:534 both give "Yes, both, before that worktree is cleaned". A needs no spec rewording. B needs OB-06 (d) and ADJ:191 changed, which B concedes itself (variant-2 line 24).
2. **It satisfies OB-01 as written, including its routing column.** OB-01's "runs in" cell says "owner's choice of branch (the commit is the owner's ...)" (MR:249), and its criterion (3) says "the owner, not an agent, is the author of the pass record (INV-014)". A gives both the commit and the authorship to the owner. B moves the OB-01 commit to an agent session, which contradicts that cell.
3. **It gives the strongest authorship evidence available.** INV-014 says: "the owner writes the record, agents cite it; git cannot show authorship, so Q7" (ADJ:478). If the owner types or re-reads the record in their own words, the owner is the person who produced the text. That is more than B's dated sentence confirming an existing file.
4. **It keeps the archive escape hatch.** A says "commits ... to master, or archives them in a named place of the owner's choosing" (variant-1 line 5), matching OB-01 (1) "(or in a named archive the owner chose)" (MR:249). B goes to master only. This matters for shared assumption A-002.
5. **It tests shared assumption A-001 instead of inheriting it.** The commits that hold the pass record were made in an agent-run worktree: `git log` in the sibling shows that commit `f104ca51a` ("cite the owner-written pass record ...") carries a `Co-Authored-By: Claude Code` trailer (read 2026-11-14; the trailer of `1ae72e1a1` is UNVERIFIED). An owner re-read in their own words is the only step in any variant that would catch an agent edit to text marked "Written by the owner." (sibling `owner-pass-record-20261112.md` lines 1-3).
6. **It names a real practical gap.** A states that the spec does not say which route the owner uses to commit on this host (which session, which worktree) (variant-1 line 23; U-001 in diff-analysis.md). That gap exists whichever variant is picked.

## 4. Weaknesses identified in the others

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

## 5. Concessions

1. **A leaves the pass record exposed.** A says "After OB-01 is recorded, the sibling worktree may be cleaned" (variant-1 line 11). But OB-01 (1) lists `owner-decisions-20261108.md`, "the 2026-11-12 record", `live-test-guide.md` and `tuibbs-review/` (MR:249), and the pass record goes to master only inside the flip PR (OB-06 (d), MR:254). If the flip never opens (the Q6 default, MR:254), cleaning after OB-01 could lose the pass record. MR:249 does not say which file "the 2026-11-12 record" means: the decision record or the pass record, which are both dated 2026-11-12. A inherits that ambiguity. This is A's most serious flaw, and B fixes it.
2. **A's stance that the owner, not an agent, commits is inconsistent with the spec's own commit model.** The flip PR that A relies on is opened by "the PR session" (MR:254 (h)), and Q32 recommends that "the PR session commits named paths" (MR:559). So under A an agent session would commit the pass record anyway. The rule at `release-gates.md:22` forbids agents from *writing* owner records, not from committing them. A's X-001 position ("the person who typed the record is the owner, which is the only defence") is about who typed the text. It does not actually require the owner to be the person who commits.
3. **Re-confirmation adds nothing over today.** A admits that if the owner re-confirms rather than re-types, "the authorship evidence is the same as today" (variant-1 line 24). In that case A's authorship strength collapses to B's.
4. **A costs the most owner time:** a branch, a commit and a PR through `/sc:pr-submit`, or an archive decision. It also leaves open which route the owner uses to commit.
5. **A does not mention `handoff-mvp-brainstorm.md`** in its plan, only under "unresolved" (variant-1 line 28). C inventories it.

## 6. Shared assumptions

- **A-001 (the sibling's files are unedited owner text): QUALIFY.** It is plausible but unproven. The commits that hold the pass record were made in an agent-run worktree (`f104ca51a` carries a `Co-Authored-By: Claude Code` trailer, read 2026-11-14), and git cannot show who typed it (ADJ:478). Whichever variant wins should require the owner to read the files once before they are saved (A's re-read step), so the assumption is checked rather than assumed.
- **A-002 (the owner accepts these records in the repository): QUALIFY.** The repository is the owner's private fork (CLAUDE.md, "PR Target = Fork"). One owner record, `owner-decisions-20261111.md`, is already on master (MR:235), which suggests acceptance, but that is an inference, not an owner statement. A's archive option covers the case where it is false, and B should carry the same option.

## 7. Per-point positions

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

## 8. Overall verdict

Pick **a combination led by B, with three additions:**

- **From B:** a records-only PR now, with the pass record included, byte-checked, and the sibling cleaned only after the merge is verified.
- **From A:** the owner re-reads each file before the copy, and the named-archive option stays available.
- **From C:** the full inventory, with `handoff-mvp-brainstorm.md` decided explicitly, and a dated "do not clean" ledger entry that holds until the merge is verified.

Confidence: 70 percent. Reason: B is the only variant that removes the single-disk loss risk for every record, including the pass record, whether or not the switch-on ever happens, and A's re-read step is the cheapest way to make its authorship claim real rather than assumed. If the owner must pick one unmodified variant, B over A at about 60 percent.
