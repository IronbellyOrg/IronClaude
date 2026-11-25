# F: Inventory of clayphi (Clay) work against ironbelly's earlier work

Read-only analysis, 2026-11-20. Sources: gh issues, PRs, timelines and comments in IronbellyOrg/IronClaude; origin/master docs. Times are UTC.

## Summary

1. The suspicion that the watcher was built without checking earlier work is NOT supported: #655 names #331, #447, #448, #485, #548, #584 and #591, says it "replaces #450", lists what was carried over and dropped, and reuses the #447 code. It IS partly supported for the wider orchestrator: #655 says #423 and #444 were "not read in full", and neither #655 nor the spec cites the alignment work (#587 to #589) or the 11-17 `issue-pipeline` analysis.
2. The main finding is replacement (class C), not duplication: #682 (merged 11-20) deleted `cli/issue_pipeline/` (about 4,600 lines; ironbelly's #584/#591 of 11-17), and open #686 removes the trigger label, approval and Project code of #447. The stated reasons are Clay's rulings of 11-18 and 11-19.
3. No ironbelly comment, review, assignment, label or reaction exists on #655, #681, #682, #683, #684, #686 or #690. Clay merged #681 to #684 themselves between 00:02Z and 02:01Z on 11-20. Ironbelly did reply to Clay elsewhere (#571, #658) and merged #661, #666, #670.
4. Wording risk: in #655, #681 and the spec, "the owner" means Clay ("approved by the owner (Clay)"). In #571, #409 and ironbelly's comments, "owner" means ironbelly (Clay calls them "Ryan").
5. The rest of Clay's work (closeout, work report, `/sc:issue --plan`, worktree cleanup, PR log, 6.x removals, ccsession) is complementary (A) or builds on owner work (D). The removals were approved in #571 by ironbelly; ironbelly reversed the swarm removal on 11-17.
6. UNVERIFIED: any chat, ClickUp or spoken agreement; the IronFlow repo (outside the allowed scope).

## Identity

- Permission on the repo: clayphi `maintain`, ironbelly `admin`. `gh api orgs/IronbellyOrg/members` listed clayphi (role not shown).
- No CODEOWNERS file; CONTRIBUTING.md names no roles. Docs naming Clay (`docs/designs/orchestrator.md`, `sc-closeout.md`, release notes, v5 test guides) use Clay as the orchestrator's user and the ruling authority, not as a repo role.
- #409 comment by clayphi (11-11): "@ironbelly (Ryan)". #571 body: "Ryan asked Clay (2026-11-16) to lead cleaning out unused commands". No source read gives a pronoun for either person.
- Clay has authored about 75 PRs since 2026-06 (ccsession, pr-submit, routing guide, releases).

## Owner (ironbelly) timeline used for comparison

#331 filed 10-30, closed 11-08. #447/#448 merged 11-08 (the `issue-watch` poller). #450 rollout 11-08. #485 11-10. #548 11-14 (owner's "option 3"). #339 orchestrator 11-01; #409 dashboard 11-06; #423 11-07; #444 11-08. #539 sweep merged 11-14. Alignment docs #587 to #589 on 11-17 (chain: watcher, then orchestrator, then dashboard; the handoff marked DEFERRED). #584 and #591 merged 11-17 ("owner decision 6 = B", coordinator handoff). Status reviews on #339, #409, #423, #444, #450 on 11-17.

## Table

| Item | Date | What | Class | Owner work it relates to | Cites it? | Evidence |
|---|---|---|---|---|---|---|
| #450 comment | 11-18 17:00 | Eight-point design proposal to "@ironbelly ... What do you think?" | D/C | #331, #450 | yes (the thread) | No reply on #450 (its last comment is Clay's). #450 and #331 timelines show cross-references from #651 and #655 |
| #655 (open) | 11-18 19:55 | Issue-polling orchestrator, "replaces #450"; 64 KB, 15 comments, all by clayphi | C and D (watcher); B-lite (orchestrator name) | #331, #447, #448, #450, #485, #548, #584, #591; #339, #444 | yes: "replaces #450 and the open parts of #331 and of the coordinator handoff"; "Same area, not read in full: #423 and #444" | History comment (20:57) gives the reasons: trigger label, approval label, Project/Backlog, plan gate, separate watcher session and cron are "one more thing a person ... has to set". Carry-over list is item by item (FU-3 to FU-12, Q1 to Q4). Assigned to clayphi only; no reactions |
| #681 | 11-19 22:32; merged 11-20 00:02 by clayphi | Adds `docs/designs/orchestrator.md` (1,412 lines) | D | #655; names #331, #450, #339, #444 inside | yes, in the doc ("replacing #450"; step O5 "close #450 ... after the switch-on") | The doc's "Inputs read in full" lists #655, its history, the coordinator spec, #651, the accuracy check and the Orca skill; #331, #450, #339, #444 are not on it. No ironbelly review |
| #682 (PR D) | 11-19 22:56; merged 11-20 00:02 by clayphi | Deletes `cli/issue_pipeline/`, WC-17 and G2 rule 1 (36 files, -4,599 lines) | C | #584, #591 (11-17), Q2 option 3 (#548) | partly: cites #655 and #665 finding F14; not #584/#591 | Body: "Nothing runs this code: the issue watcher has `enabled: false`". States an independent review of the guard change. Only a bot review. Ironbelly's 11-17 14:40 request to Clay in #571 asked to ingest the `issue-pipeline` analysis |
| #686 (PR A, open) | 11-20 00:25 | Poll wakes the repo's orchestrator; hold label; 62-reason audit table (59 files, +14,256 / -16,637) | D and C | #447 code in `issue_watch/` | yes: "Refs #655"; "issue_pipeline ... already deleted by PR D" | Reuses runner, record, audit and launch; removes claim launch, approval, trigger and Project reads. The poll gains its first GitHub write (a label). Owner decision D2 ("poller never assigns, comments or moves Project items") appears in #655 only as "FU-7 (revisit D1 and D2): it becomes this redesign" |
| #684 (PR C) | 11-19 23:31; merged 11-20 02:01 by clayphi | Moves `agent-work-report` from IronFlow into IronClaude; living report | A | none found; purpose is near `/sc:sweep` (#539) and the observer (#409) | no | Source is Clay's coordinator spec of 10-27 (UNVERIFIED; repo not read). No mention of sweep or observe in #684, #655 or the spec |
| #683 / #668 closeout | 11-19 23:07; merged 11-20 01:16 | `/sc:closeout`; adopts Jay Wedgeworth's skill (Apache-2.0, Simple-With-Us) | A, small B | #339 text "runs sc:close on that session" (session close, not PR/issue close) | yes: #668 lists #339, #331, #444, each "Not a duplicate ... (Matched on title only)" | #339's 11-17 status review says `sc:close` is not built. A search of issues and PRs created before 11-18 found no earlier closeout issue of this kind |
| #689, #690 (open); #651, #661 | 11-18 to 11-20 | Plan sections in `/sc:issue`, `--plan`, `--remaining`, plan at create, an "other" mode | D | owner's `/sc:issue` (#302, #344) and claim chains | #651 cites #450 as out of scope; #690 cites #655 | #661 merged by ironbelly 11-19. #689 would move brainstorm and design from claim to create, which changes the owner's claim chain; 0 comments |
| #687 (open) | 11-20 | Daily cleanup of merged worktrees | A | #339 comment of 11-05 lists worktree and branch cleanup as an orchestrator duty; #356 | no | Adapted from Jay's tools; nothing built |
| #669 / #670 | 11-19 | Daily log of merged PRs per person | E | none found | no | #670 merged by ironbelly. Body says it has "nothing to do with the daily work report or the orchestrator" |
| #665, #674, #675 | 11-19 | Open review findings of #655 and #668 | D | #655, #668 | yes | Internal to Clay's work |
| #571, #647, #615 to #633, #650, #653, #656 to #659 | 11-16 to 11-18 | 6.0.0 and 6.1.0 removals and releases | D | owner request of 11-16 | yes ("Ryan asked Clay") | Ironbelly approved wave 1 and reversed swarm removal (11-17). #652 and the `/sc:task` removal were withdrawn when "Ryan's list" could not be verified. #658 was squash-merged by ironbelly by mistake |
| #409 comment | 11-11 | Clay's answer on dashboard value | D | #409 | yes | Posted on ironbelly's request ("You asked me on 2026-11-07 to leave it here") |
| #499, #570, #608, #619, #628, #630, #641, #666 and older ccsession and pr-submit PRs | 06-03 to 11-19 | Fixes, features, docs | A/E | none in conflict | n/a | #499, #608, #619, #628, #630, #666 merged by ironbelly; Clay authored ccsession from #123 |
| #663, #652 (closed) | 11-18/19 | Superseded or withdrawn PRs | E | none | n/a | Not used |

## Evidence for and against, by piece

**Watcher and orchestrator (#655, #682, #686).**
For overlap or ignored prior work:
- #655 admits #423 and #444 were "not read in full", and the spec's "read in full" list omits #331, #450, #339, #444, #584, #591 (it cites their code and design docs instead).
- The owner's 11-14 and 11-17 decisions (Q2 option 3, then Plan B) were replaced about 24 hours after #591 merged, and the 11-17 request to Clay named `issue-pipeline`.
- Ironbelly did not answer Clay's 17:00 question on #450; #655 was filed 2 h 55 min later.
- #682 deleted the code with no human review.
- The spec claims the name `/sc:orchestrator` (OQ5) while #444 calls it "proposed", and lists "how #444 joins" as unverified (U19).

Against:
- #655 states the replacement, the reasons and the carry-over in writing, in the issue and a history comment.
- The proposal was posted to the owner's own issue with an @mention before the build.
- The build reuses the owner's poller code and its safety features instead of duplicating them.
- The spec puts the general #339 orchestrator out of scope and plans to close #450 only after switch-on.
- The owner's alignment chain (watcher drives an orchestrator) points the same way; it marks the handoff DEFERRED, not rejected.

Conclusion: a documented replacement (C), plus an unresolved naming and scope overlap with #339, #444 and #423 (B-lite). Whether ironbelly agreed off GitHub is UNVERIFIED.

**Work report, closeout, cleanup, PR log.** No dated owner work was found that these repeat. Closeout and cleanup touch duties that #339 lists for the owner's orchestrator, so they are candidates to fold into #339's scope.

## Interaction history

- Ironbelly on Clay's items: comments on #571, #572, #658 and older ones (#381 to #393, #311, #304, #289, #290); none on the 11-18 to 11-20 set. Review requests: none. Assignee: clayphi alone on #655, #668, #651, #647.
- Merged by clayphi: #681 to #684 (44 of 78 merged Clay PRs). Merged by ironbelly: #661, #666, #670, #658, #619, #608, #499.
- Clay's #681 body says the PR "is not merged by the session that opened it ... the owner reviews and merges"; clayphi then merged it. "Owner" there is Clay.

## Grouping

- **Fold-in candidates (A/D):** `/sc:closeout`, agent-work-report, `/sc:issue --plan` and the plan sections (#661 already merged), worktree cleanup #687, PR log #670, the 6.x removals approved in #571.
- **Overlap to resolve:** `/sc:orchestrator` name and scope against #339, #444 and #423; the work report against sweep and observer; #689's change to the claim chain; the dashboard #409 against the report.
- **Replacements that conflict with owner decisions:** #682 and #686 against #584/#591 (Plan B, 11-17), Q2 option 3 (#548) and D2; #655 "replaces #450" while #450 stays open and assigned to ironbelly. This needs an explicit ruling from ironbelly.

## Caveats

No GitHub write was made. Org role, chat decisions and IronFlow contents were not read. "Not cited" means a text search of the bodies read found no number, not that the work was unread.
