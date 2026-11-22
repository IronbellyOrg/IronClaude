# X01 FINAL: mark the report items deferred in issues 716, 718 and the plan

Reconciled 2026-11-22 from A-0, B-0, A-3, B-3. Read-only checks by the reconciler: gh reads of 716, 718, 719, 720; SPEC.md lines 256 to 259, 499, 500, 778, 786; DECISIONS.md lines 17 and 462; git ls-remote for the tag. Hour figures are estimates. This is a recommendation until the owner says go in chat.

## 1 Unified proposal
Defer, do not drop. Close nothing, add no label, leave #719 and #720 as filed. Edit the bodies of 716 and 718, add one comment to each, edit five local plan spots. One scripted run by the coordinator. Same words in both issues, so a search for DEFERRED finds every one.

Issue edits (anchor each by its exact text, never by line number):
1. Top line of each body: "Status 2026-11-21: the report items (716: C14 and the entry line of C8; 718: D1 to D4) are deferred, not dropped. The owner decided in chat not to restore the report skill now. Trigger and steps: #720. Server fix that gates any restore: #719." In 716 only if the finished body is 65,000 characters or less; if not, drop this line first. Item lines are never dropped.
2. One line under the title of 716 C14 and 718 D1 and D2: "DEFERRED 2026-11-21 (owner decision in chat): the report skill is not restored now. Do not start this until it is; trigger and steps are in #720." Add: "Remove this line only when the restore, the living half and the report-entry writer (S15c) have all landed (#720)." C14 also gets: "Stage S15c is trigger (b) in #720, so the restore and this writer are done together."
3. 716 C8, only the S05-F18 entry line and the "also: a test edits a claimed issue as another login" line: the same DEFERRED line and removal rule, plus "The rest of C8 (body hash at handoff, re-read each status pass, S08-F8) is not deferred." Watch-out "Needs the report-skill restore decision first." becomes "Deferred 2026-11-21: waits for the restore and the writer (#720)."
4. 718 D3 and D4: "PART DEFERRED 2026-11-21: only the config change and its test (D3) or the diff check (D4) wait for the restore (#720). The owner's chat answer can be given now; #720 'Ask first' step 2 lists the same question, and one answer serves both. Remove this line when #720 is merged."
5. Review point 4 (both issues): replace the "One owner decision gates the report items ..." sentence with "The owner decided on 2026-11-21 not to restore the report skill now (tag archive/pr-684-agent-work-report; steps in #720; server fix gate #719; SPEC Appendix B.3, action 1). The report items are deferred, not dropped." Replace "so they need the same decision before they are built" with "so they wait for the same restore". Keep the D3 and D4 sentences.
6. "Decisions and risks" bullet (both): replace the whole bullet with "The owner decided on 2026-11-21 not to restore the report skill now (#720). This defers D1, D2, the config change of D3, the diff part of D4, C14 and the entry line of C8. Still open: where the report session and its state live (D3); the owner's chat answer can be given now."
7. "Order to complete" point 3 (both): "after C14 and the report-skill restore" becomes "after C14 and the report-skill restore (deferred, #720)".
8. One comment on each issue, posted last, after both edits read back clean, no names: "Owner decision 2026-11-21: the report skill is not restored now. Marked DEFERRED in this issue: <items>. Nothing closed or dropped. Trigger and restore steps: #720. Server fix that gates any restore: #719."

Plan files (local, not pushed), SPEC.md in /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/ (anchor by text):
- Appendix B.3 action 1 (line 786): "DECIDED by the owner in chat 2026-11-21: not now; tag archive/pr-684-agent-work-report (d7d645ddd); restore steps in issue 720, server fix gate issue 719. FR-45, FR-46, FR-48 stay requirements, marked deferred, not dropped."
- Line 778 "blocked until the skill is restored" becomes "deferred by owner decision 2026-11-21; applied when the skill is restored (#720); they stay requirements".
- Prefix "DEFERRED (owner 2026-11-21, #720): " on FR-45, FR-46, FR-48 (lines 256, 257, 259). S15 row (499): add "FR-48 deferred with the restore, #720; S15c is the trigger". S16 row (500): add "FR-45, FR-46 deferred, #720". FR-47, FR-49, FR-50 untouched.
- DECISIONS.md: one new dated paragraph after line 17: "Update 2026-11-21: the owner decided in chat not to restore the report skill now; tag archive/pr-684-agent-work-report (d7d645ddd); restore steps in issue 720, server fix gate issue 719. Statements below that the restore is an owner decision are answered: deferred, not dropped." Nothing existing edited.
- STATE.md: one dated line with the owner's go and the result.

Order: plan files, then 718 body (smaller, the rehearsal), then 716 body, read back each, then the two comments, then STATE.md.

## 2 Context
On 2026-11-21 the owner decided in chat not to restore the report skill agent-work-report now. The archive tag is on origin (checked: refs/tags/archive/pr-684-agent-work-report, commit d7d645ddd). Issue 719 (report server fix, merge gate) and issue 720 (restore steps and trigger) are open. Issues 716 and 718 were last edited 2026-11-21 15:01Z, before 719 and 720 were filed at 20:06Z, have no comments, and still say the owner must decide. 720 already lists "issue 716 items C8 (entry line) and C14, issue 718 D1 to D4" as waiting, but the items do not point back.

## 3 Implications
- Changes: the text of 716 and 718 (public) and five spots in the local plan. 720's trigger becomes the one place the wait ends.
- Stays blocked: C14, the entry line of C8, D1, D2 (all work on report entries, the living half), the config change of D3 and the diff check of D4. Stays unblocked: the rest of C8, and the owner's D3 and D4 answers any time.
- Stays as filed: 719, 720, FR-47, FR-49, FR-50. Nothing is closed, relabeled or rescoped.

## 4 Benefits
The issues, the plan and 720 agree. No builder starts C14 or D1 to D4 against a missing skill. The owner is not asked the restore question again. Clay and IB-JonathanB are told by a comment, not surprised by a silent change. Reversible: saved old bodies re-apply, and the plan edits are five local lines.

## 5 Risks and containment
- Whole-body overwrite on the shared login ironbelly (gh issue edit replaces the body): save both bodies, re-read and abort if updatedAt or the body hash changed, read back after the write.
- Missed or doubled text: the script asserts each old text occurs exactly once; diff printed in chat as a record.
- 716 over the size limit: 63,136 characters now, about 1,200 to 1,500 added; cap 65,000 in the script (the 65,536 GitHub limit is from memory); drop the 716 top line first.
- A line removed too early: each DEFERRED line states its own removal rule; C14, C8, D1, D2 clear only after the writer lands.
- Public wording reads as discarding Clay's work: it says "owner decision" and "deferred", names no person.
- A tool that parses the bodies: ids, titles and checkboxes are untouched (whether any tool parses them is UNVERIFIED).

## 6 Costs (estimate)
Agent: 0.75 to 1.5 hours. Basis: about 16 scripted body edits, 2 comments, about 10 plan edits, a diff and read-back, no builder work. Owner: about 2 minutes (one sentence). The judge put this wording work at 1 to 2 hours (VERDICT.md section 7); the range here is lower because it is scripted and limited to named spots.

## 7 The sentence the owner says in chat
"Go: mark the report items deferred in issues 716 and 718 as proposed, add one comment on each, update the plan files, close nothing."

## 8 What an agent does after it
The coordinator records the go in STATE.md. Then, in one `uv run python` run: save both live bodies as backups in /home/coder/workspaces/IronClaude/.dev/brainstorms/20261122-owner-actions-debate/X01/; re-check the tag on origin, 719 and 720 open, 716 and 718 unchanged; apply each replacement (exactly-once assert, 65,000 character cap); print the diff in chat; run `gh issue edit N --repo IronbellyOrg/IronClaude --body-file <file>`, 718 first, then 716; read back and compare; post the two comments; edit the plan files; record the result. If anything changed since the snapshot, stop and re-plan.

## 9 Consensus: full
Round 3 had one point left: A wanted C14 and C8 lines cleared only when the writer lands, B first wanted "when #720 is merged" there. B conceded after reading 720 ("What stays blocked even after this restore" lists the S15c writer, and the living half is left out if the trigger is (a)). I checked that text and agree. B then applied the same rule to D1 and D2; I checked 718 and agree: D1 "skips every issue that has a living-report entry" and D2 "each report entry" both depend on the living half. A's round 3 text still gave D1 and D2 the merge rule; I adopt B's stricter one. DECISIONS.md paragraph: A yielded.
Residual (optional strikes, same go): (1) the DECISIONS.md paragraph; if struck, the record still says the restore is open and a later agent may ask again. (2) the 716 top status line; if struck, the item lines still protect each item. Nothing else is open.

## 10 Not verified
- The 65,536 character issue limit is from memory, not tested.
- Whether any tool parses issue bodies (ids, checkboxes).
- Final character count of the edited bodies (computed only when the script runs).
- That D3's config change is not done inside #720 commit 2 (it covers the per-user state path); if it is, the D3 line clears at merge, as written.
- The plan line numbers hold today (read this round) but anchor by text, since other edits can shift them.
- Who else reads the comment notifications (Clay, IB-JonathanB): assumed, not checked.
