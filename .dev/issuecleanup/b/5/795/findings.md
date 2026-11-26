# Round 2 findings: issue #795 (C14) Report entry: content, milestones-only updates, removal at close

Checked 2026-11-24 against master ancestor f2894fc44 (branch ironbelly/Realign). Plan files read read-only from `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/` (SPEC = `spec/SPEC.md`, DEC = `DECISIONS.md`, VERDICT = `debates/<id>/VERDICT.md`). R38 = `.dev/releases/backlog/issue-watcher-zero-setup/requirements.md:64`. Round 1: `/home/coder/workspaces/worktrees/IronClaude/Analyze716/.dev/issuecleanup/a716/5/795/findings.md`. Static analysis: `/home/coder/workspaces/worktrees/IronClaude/Realign/.dev/issuecleanup/b/5/analyze/analyze-report.md`.

## Alignment with architectural decisions
Overall: partly aligned in design, in conflict with the current direction on timing. The writer rules fit the plan; the base the plan built on (the report skill) was removed and the owner parked the report tool.

| Source | What it says | Verdict | Evidence |
|---|---|---|---|
| R38 (C) | "living work report ... not adopted"; no element of Clay's design is adopted. | in conflict (softened by the owner's later park note) | requirements.md:64 |
| Owner status note on #716, 2026-11-22 | The work-report tool is parked, not dropped; C14 and C8's entry line are on hold until the owner asks for a daily report page or the writer stage (S15c) starts. Repeated by the 2026-11-24 backlog review, step 3. | aligned with "keep parked"; differs in strength from R38 (park vs not adopted) | #716 comments 2026-11-22 11:06 and 2026-11-24 14:23 |
| DEC D11 and D15 rows E1 to E5 | Adoption of the report skill and living report is "SUPERSEDED BY PR 700"; the answers that rely on it keep their wording but their carrier is gone. | in conflict (base removed) | DECISIONS.md:24, :33, :35 |
| SPEC FR-45, FR-46, FR-48 | Stay requirements, "blocked until the skill is restored"; the owner action to restore the PR 684 skill is open. | partly aligned: blocked, not dropped | SPEC.md:778, :786 (Appendix B.3 action 1) |
| FR-48 and NFR-02 | `report-entry` is the only writer of an entry file; one writer per file. | aligned: C14's writer is exactly this | SPEC.md:259, :215 |
| FR-46 and FR-80 | Entries hold only `session_id` for session facts; the observer shows fields only from an owner-named allowlist and never `recommend` or `suggested`. | aligned (the item's own watch-outs say so) | SPEC.md:263; item #795 Watch out |
| OA-17a | Titles and links only while `report-entry` is absent. | aligned: master shows no entry data today | SPEC.md:116 |
| D11 VERDICT | The entry files become the dashboard data, "their format needs one owner and a fixed schema"; entry creation depends on D01 to D08. | partly aligned: no schema exists on master | D11/VERDICT.md:89 |
| D15 E7 | `report-entry` adopt with change (rename; part of the verb list). | aligned | D15/VERDICT.md:115 |
| FR-26 verb group | `report-entry` belongs to `superclaude coordinator`. Master's only caller, closeout, runs `superclaude orchestrator report-entry`. | in conflict on the group name | SPEC.md:228; src/superclaude/skills/sc-closeout-protocol/scripts/settle.sh:1037-1042 |
| SPEC stage S15c | `report-entry` and `escalate` are built in S15c, after the transport stages. | aligned (C14 extends S15c) | SPEC.md:499, :364 |
| Worker contract WC-9, WC-11 | Workers write nothing outward; two writers never share a file. | aligned | src/superclaude/core/WORKER-CONTRACT.md:41, WC-11 |
| R24 and R38 (D) | The coordinator posts the result comment and moves the Status, never closes an issue itself. "Removal at close" must be triggered by closeout after the person's merge, not by the coordinator closing. | aligned if so wired | requirements.md:50, :64 |
| Closeout contract | The first-word contract `moved`, `already_closed`, `no_entry` of `report-entry --closed` "is not written anywhere yet". | partly aligned: C14 would define it | src/superclaude/skills/sc-closeout-protocol/refs/settle.md:99 |

Internal tension found in round 2: the done-when says the entry changes only at the named milestones (plan done, blocked or asking, PR opened, review rounds, PR ready, merged), but the open item #789 (C8) requires "a test edits a claimed issue as another login and the entry gains exactly one new line". An issue edit is not on C14's milestone list.

## Complementary issues
- #720 (restore the report skill, parked) and #719 (page server serves the whole state folder): C14 is blocked by the owner's trigger and by that restore (SPEC FR-45, FR-46, FR-48 are blocked on it). #719 gates the restore, not the skeleton.
- #718 (TUI dashboard and report views): D2 shows the same links or "no live session"; D1 excludes entry issues from the daily run. #716's review point 3 says build the content once in C14. Interface: C14 writes the entry file; #718 renders it and must not write.
- #789 (C8): writes the issue body hash and the entry line at handoff into the same entry; shares the owner decision to restore. Conflict on the milestone list above.
- #771 (closeout and worktrees wired into the coordinator's finish): closeout calls `report-entry --closed`; C14's "removed at close" supplies the verb that call needs.
- #791 (C10, check-in template and hourly pass): C14 says never write on an hourly timer; C10's pass is a typed check-in, not an entry write; they must stay separate.
- #784 (C3, return contract printed last): the contract lists what waits on a person; the entry holds the same facts per issue.
- #800 (C19, settle each worker): the entry's "no live session with the reason" comes from the settled worker state.
- #706 and #409 (observer): display only, allowlist of entry fields (OA-17a, FR-80).
- #808 (C27): both write per-issue files; one writer per file (NFR-02), no overlap.

## Closest overlap
#718 (TUI dashboard and report views, items D1 and D2): D2 asks for the same content as C14's "What to build" (assignee, coordinator and worker links, or "no live session" with a reason), and D1 depends on the same entry files; #716's review point 3 already records the duplication. Shared: the entry content and its schema. Estimate: about 20% of this item's done-when (the "entry holds the five fields, observer shows the allowlisted ones" bullet; D2's render test); it does not cover the milestone-only update or the removal at close.
Next closest: #789 (C8), about 15% (a write into the same entry, but at claim and edit time); #771, about 10% (consumer of the removal at close).

## Standalone or merge
Verdict: stand alone, as a parked item. Test against #718:
- Owner: C14 is the coordinator side (the writer); #718 is the report and dashboard side (readers). Different roles.
- Acceptance test: C14 counts entry file writes per milestone and the file's removal at close; #718 renders entries and checks that a daily run leaves them byte-identical.
- Files touched: C14 a new `report-entry` writer and entry template under the coordinator group; #718 the restored skill's `exclude.py` and display code, plus observer rows.
- Build phase: C14 sits in the phase 2 cluster of #716 but is parked; #718 waits for the same restore and also for owner decisions D3 and D4, which the owner says are not pursued.
- Risk if merged: the writer would take on #718's retirement of the daily report (needs a separate owner decision) and D3 and D4, and the whole coordinator phase 2 cluster would sit behind the report restore. Standing alone keeps the writer's tests free of the display.
Merging would be right in one case: if the owner confirms R38 (C) "living work report not adopted" as final. Then #718 D1 and D2 and C14 (and C8's entry line) should all be closed together as dropped, not merged into one another.

## Closed issues and merged PRs checked
- PR #684 (merged then rolled back by PR #700, 2026-11-20): imported the report skill; the code now only exists at the archive tag `archive/pr-684-agent-work-report`. Does not deliver C14.
- PR #700 (merged 2026-11-20): removed the skill, kept `/sc:closeout`; this is why the entry writer has no home on master.
- PR #683 and issue #668 (closeout, merged and completed): closeout's step "settle the work report entry" calls the absent `superclaude orchestrator report-entry`; today the step escalates with `why=surface_absent`. C14 would turn that into a result.
- #655 (closed not planned): source of the item; the owner's closure keeps uncovered features in #716 to #718.
- #806 (C25, merged into #782): the template-test requirement carries over to #782, so C14's "template" is one of the templates #782 must name; there is no separate C25 issue now.
- #809 (W1, merged into #716), #796 (C15, closed not planned), #804 (C23, closed not planned): none changes C14.
- PR #701 (merged): worker-contract gaps only.
Nothing delivers C14; PR #700 removed its base.

## Updated recommendation
Keep open (parked) with changes, priority P3, complexity medium, size M. Unchanged from round 1 on action, priority, complexity and size. Round 2 adds:
1. Put "parked; blocked by #720 and #719 and the owner trigger" in the issue text, and remove C14 and C8's entry line from the phase 2 cluster in #716's review so the skeleton is not held.
2. Name the five fields (the "What to build" line names assignee, coordinator link, worker link, the "no live session" reason and a last-update time, which may be the five, but S04-F33 does not list them) and the verb group (`coordinator` per FR-26 against `orchestrator` in closeout's script).
3. Reconcile the milestone list with #789: add "issue body changed" as a named milestone, or change C8's test.
4. Ask the owner once whether R38 (C) or the park note stands; if R38 stands, close #795, #718 D1 and D2 and C8's entry line together.

## Scan record
- Lists read in full: open-issues.tsv 134 of 134 rows, closed-issues.tsv 157 of 157, merged-prs.tsv 508 of 508.
- Search terms: report, entry, living, dashboard, closeout, observer, milestone, status, check-in, settle, worker, sweep, daily.
- Opened with gh (read-only): open #716 (body and five comments), #718, #719, #720, #771, #784, #789, #791, #799, #800, #808, #782 (12); closed #655, #668, #796, #804, #806, #809; merged PRs #683, #700 (bodies; review threads not read; #701 known only from the #716 review comment). PR #684 not opened in full (1189 lines fetched, only #700, #718 and #720's descriptions of it read).
- Master check: `/sc:analyze src/superclaude/cli/issue_pipeline --focus architecture --depth quick`; Grep for `report-entry`, `report_entry`, `orchestrator` verb group in src and tests: the only hit is `settle.sh:1037-1042` and closeout's docs.
- UNVERIFIED: which five fields the item means (not listed in the issue text); the content of the archived report skill's entry schema (archive tag not opened); whether Orca supports the session link form `orca://session/<id>` for click-to-open (#718 says to recheck).
