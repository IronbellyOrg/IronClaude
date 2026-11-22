# Position: DO NOT RESTORE the work-report skill (`agent-work-report`)

Advocate for NOT restoring. Date of reading: 2026-11-21. All reads were read-only. Master head when read: `2ea524514`. Archive branch: `origin/clayphi/archive-orchestrator-655-20261120`, tip `d7d645ddd`.

Marks used below: a quote has its file and line. "UNVERIFIED" means I could not confirm it. `git show` paths are on the archive branch unless I say master.

## 1 Thesis

The owner should not restore `agent-work-report` as it stands: it is a one-person daily reporting tool of about 6,500 lines that was merged in two and a half hours with no owner review on GitHub, still carries a Medium security finding its author called real, and is a reader of entry files that nothing writes. The plan already gets what the owner needs (what each session is doing, who waits on a person, where each issue stands) from the owner's own sweep, `issue-watch status` and the observer, and Appendix B.3 action 1 already spells out the "No" branch: FR-45, FR-46 and FR-48 are "dropped or rewritten". The code stays safe on the archive branch, so the right move is to answer NO now, unblock the report items in issues 716 and 718, and lift pieces back later only when a named requirement asks for them.

## 2 What the skill is and does today

Every fact here I read myself unless marked.

**Size and files** (`git ls-tree` and `wc -l` on the archive branch, folder `src/superclaude/skills/agent-work-report/`):

- `SKILL.md` (the 15-step instruction file) 194 lines; `config.json` (person, orgs, schedule) 21 lines.
- 16 Python scripts, 5,777 lines in all. The largest: `run.py` (run lock, gate, refresh) 887, `clickup.py` (ClickUp reader and DM sender) 642, `render.py` (writing sheet) 626, `common.py` (shared helpers, entry-file contract) 507, `sessions.py` (reads Claude transcripts per Orca terminal) 444, `waker.py` (starts the coordinator session at 07:00) 405, `page.py` (builds the web page and starts a local server) 387. The PR 684 body says "the 15 scripts and 7 templates copied from IronFlow ... plus the new `scripts/exclude.py`", which is 16.
- 7 templates, 479 lines (item card, needs-you card, overview sheet, QA report, HTML page, page JavaScript, summary).
- A test file `tests/skills/test_agent_work_report.py`, 4,005 lines. PR 684 in all: 28 files, +10,488 lines, 0 deletions (`gh pr view 684`).

**What the daily run does** (SKILL.md, execution table lines 78-95 of the file): collects open issues, PRs and project boards from both orgs (`config.json`: `IronbellyOrg`, `IronbellyGroup`); reads ClickUp through its API with the person's own token; reads every Claude Code session's transcript in Orca; joins them into one card per piece of work; compares with yesterday; has a model write the judgment parts; runs `check.py` until it passes; builds `report.html`; then posts the summary in the session, sends it as a ClickUp direct message and opens a browser tab; then closes the run and the model makes a git commit of the state folder (Step 14). It is woken by two Orca automations at 07:00 and 09:00 local time, Monday to Friday (SKILL.md line 30).

**What the living report adds** (SKILL.md line 16): one entry file per issue the orchestrator holds, in `.dev/coordinator/orchestrated/`. `exclude.py` keeps the daily run from listing such issues; `run.py refresh` rebuilds the shared page from the last daily report plus the entry files with no model call.

**Nothing writes the entry files.** The technical reference says the entry-file fields are written today by "nobody in the snapshot; designed writer `superclaude orchestrator report-entry` (PR B); tests build entries by hand" (`techref/OBSERVER-SWEEP-DASHBOARD-TECHNICAL-REFERENCE.md:805`), and the only entry-file writer in the snapshot is the skill's own `move_to_closed` (same file, line 806). I confirmed the archive branch has no `src/superclaude/cli/orchestrator/` folder (`git ls-tree` printed nothing). So the living report is a reader without a writer.

**Side effects outside its own folder** (techref line 799, marked CODE-VERIFIED there): a ClickUp DM to the token owner; an Orca unread mark; text typed into the coordinator's Orca terminal (`/clear`, a wake line, `ccsession coordinator`) and a new terminal; an Orca browser tab; a detached `python -m http.server 8765 --bind 127.0.0.1 --directory <.dev/coordinator>` that "serves the whole folder (`settings.json` with ClickUp user and DM channel ids, `action-log.jsonl`, run folders)"; and a git commit by the model. I also saw the server start in the archived `page.py` lines 322-326 and no `Host` check anywhere in that file.

**Built for one person.** `config.json` has `"person": "clayphi"` and `"person_name": "Clay"`. The frontmatter description begins "The daily helper: gather all of Clay's open work across both Ironbelly GitHub orgs". The word "Clay" appears 58 times in `SKILL.md`. SKILL.md line 12 still says "The orchestrator (`/sc:orchestrator`) does every check-in itself", the name the owner ruled out in D08 (`debates/D08/VERDICT.md:53`: "`/sc:coordinator` and `sc-coordinator-protocol`; no `/sc:orchestrator`").

**What depends on it today.** On master (`2ea524514`) nothing runs it; the skill was removed by PR 700 (`SPEC.md:758`). One kept feature touches its idea: `/sc:closeout` (PR 683) calls `superclaude orchestrator report-entry` and, when that command is missing, prints `ENTRY escalated key=<k> why=surface_absent` (`settle.sh:1037-1039` on master). That command does not exist with or without the skill. Plan items that depend on the decision: FR-45, FR-46, FR-48 (`SPEC.md:778`, "blocked until the skill is restored"); section 7 rows E1 and E2 (`SPEC.md:464`); issue 716 items C14 and the entry line of C8; issue 718 items D1, D2, D3 (config part) and D4 (diff part) (`716` and `718` review sections: "The owner decides whether to restore the report skill (blocks D1, D2, the config change of D3, the diff part of D4 and the report-entry items C14 and C8)"). I found no item in issue 717 that names the report.

## 3 Arguments against restoring

**A1. The code has never had an owner review, and its own author rolled it back.**
PR 684 was opened 2026-11-19 23:31:53Z and merged by `clayphi` at 2026-11-20 02:01:07Z, 2 hours 29 minutes later, with `reviewDecision` empty (`gh pr view 684 --json`). The inventory says "none of #681, #682, #683, #684, #686, #690 has a review or comment by `ironbelly` on GitHub ... That is not proof the owner did not see them elsewhere (chat), UNVERIFIED" (`inventory/clay-prs.md:48`). PR 700 then removed it; its body says it rolls back #684 "at Clay's request (2026-11-20)". A restore PR would be the first time anyone but the author and three review bots reads 10,488 added lines. That is a large review for a feature that is not on the plan's critical path (A7).

**A2. It ships a Medium security finding that its author agreed was real and left open.**
Codex's security review on PR 684 raised "Authenticate the localhost report server": a rebound `Host` header lets a web page read everything under `.dev/coordinator/`, because `page.py` serves the whole folder with a directory listing. Clay's reply in that thread: "Not changed in this pull request: the local report server ... is moved unchanged from IronFlow ... The finding looks real (a rebound Host header and the directory listing expose the whole state folder). Recorded as a security follow-up for the report skill: serve only report.html, reject any Host other than 127.0.0.1:8765, and disable the listing." The thread was marked resolved without a fix (36 of 36 threads show resolved, `gh api graphql`). The Codex summary comment lists it as the one of five advisory findings without the "Resolved" tag. The archived `page.py:322-326` still starts the server on the whole folder. I searched open and closed issues for a follow-up (`gh issue list --search`) and found none (a weak search; UNVERIFIED that none exists). The served folder holds ClickUp ids, the DM channel id, an action log and run folders with transcript excerpts (`techref:799`). The skill also reads other people's GitHub and ClickUp text and feeds it to a model; the review thread list has at least four more prompt-injection and symlink findings (instruction-shaped titles and activity text, symlinked ancestors, `javascript:` links) that the threads show as resolved in turn (I did not check each fix).

**A3. It is a one-person tool, and installing it ships it to every user.**
`config.json` names `clayphi` and `Clay`; the description says "gather all of Clay's open work"; "Clay" appears 58 times in `SKILL.md`; the ClickUp sender writes to the token owner's own DM channel; the automations and the coordinator tag are fixed (`session_tag: "coordinator"`, `automation_prefix: "coordinator-"`), which clashes with the owner's `COORD-<RepoName>` name (D08 verdict, `SPEC.md:226`). PR 684's own check shows `superclaude install` puts it in `~/.claude/skills/agent-work-report/`. So a plain restore puts a Clay-specific helper, with a description that matches "what's on my plate", into every host. The plan already says this must change: FR-46 "Remove person-specific config from the report (`"person": "clayphi"`), make the state path per-user" (`SPEC.md:257`). A restore is therefore "restore and then rewrite config, state path, entry schema, naming and session reads", not a clean move. The skill also bakes personal rulings into its text ("Clay, 2026-11-03" at SKILL.md line 24; "owner ruling 1, 2026-11-19" in Step 4b, line 116). The plan records at least one such ruling as Clay's and not the owner's (ruling 39, the cap: `DECISIONS.md:456`), and issue 718 item D1 says who made "owner ruling 1" is UNVERIFIED and "do not treat the phase-out as an owner decision".

**A4. Restoring buys a reader with no writer.**
The living report, `exclude.py`, `run.py refresh` and the entry-file schema only matter when `report-entry` writes entries. That verb is plan stage S15c (`SPEC.md:499`: "S15c AU1-AU8, handback, `report-entry`, `escalate`"), which comes after S13 and S14, and "Nothing of the unified flow has run live" (`SPEC.md:65`). The plan already tells the observer what to do until then: FR-80 "titles and links only while `report-entry` is absent" and OA-17a. So restoring now adds about 6,500 lines whose new part (the living report) cannot do anything until a stage that is months of review and live tests away.

**A5. It overlaps the owner's sweep and observer, and it is the one piece that writes.**
The inventory notes "#684 overlaps sweep and observer" (`inventory/clay-prs.md:159-160, 189`). The D11 verdict keeps the owner's read-only rule for the sweep and observer ("'Recommend nothing' on the sweep and navigation only on the observer; Options, DM and commit only in the report or the orchestrator session", `debates/D11/VERDICT.md:64`), which means the report is the only piece of the three that sends a ClickUp DM, commits its state folder and carries Options and a Recommendation (line 44). I do not claim the verdict forbids that; I claim it makes the report the one part the plan must keep fenced. The skill also types text into an Orca terminal and starts terminals (`waker.py:172-207`, `orca_term.py`); the plan governs typing into worker terminals by four rules and a closed `refuse(argv)` list (FR-40, FR-26, `SPEC.md:226, 242`), and the report's typist sits outside both (my reading; the plan does not mention it). The techref also notes that "Why the observer, sweep and report skill have three separate Orca wrappers is not stated" (line 1303). Restoring adds a third Orca reader that the plan then has to reconcile (FR-45's live side-by-side run exists only to reconcile it).

**A6. The plan already works without it, and the plan's own requirements show how.**
The observer needs only the sweep JSON and `issue-watch status --json` (FR-44, FR-79, FR-80, FR-81, none of which needs the skill). The sweep gets `session_id` and `worktree_path` (FR-41) and a saved JSON file (FR-42). Waiting-on-a-person lines are entry lines (FR-49) and a waiting PR is "shown with the age of the wait" (OA-25a, `SPEC.md:113`). The D11 verdict itself rated its HYBRID answer at 72% and wrote that confidence "would drop ... if the owner wants the report replaced entirely by the dashboard" (`debates/D11/VERDICT.md:97`). Appendix B.3 action 1 already writes the "No" branch as a normal outcome, not a breakage.

**A7. Size, order and churn favour waiting.**
The owner already has a long queue: B.3 lists five new owner actions, the spec was "NOT re-reviewed" after PR 700 (`SPEC.md:754`), and issues 716 to 718 add 27 plus 15 plus 4 items. A restore PR is a 6,471-line skill (plus its 4,005-line test) reviewed ahead of anything that runs. Meanwhile the archive branch loses nothing by waiting. And a second landing re-opens the host problem: "a host that installed master between 00:02 and 15:07 UTC needs `superclaude update` (a plain install skips existing files)" (`SPEC.md:763`). Whether `update` removes the old skill folder is UNVERIFIED.

**A8. The only known user's need is already served outside IronClaude.**
PR 684's body says the skill was "copied from IronFlow (a04c2754)", that re-pointing Clay's two automations to the new copy "is the owner's step O3", and "nothing here touches them or the IronFlow copy". So Clay's daily report keeps running from the IronFlow copy whatever IronClaude does. PR 700 changed nothing for it. Whether it still runs is UNVERIFIED (D11 verdict line 107: "Whether Clay uses the daily report and whether its Orca waker automations were re-pointed after PR 684 ... not checked"). This means NO breaks no running thing I can find, while YES asks the owner to adopt and maintain Clay's tool.

## 4 What the plan already covers without the skill, and what it would lose

**Already covered, with no part of the skill needed**

| Need | Where the plan covers it |
|---|---|
| One source of session facts: what each session is doing, which wait on a person, "could not determine" | The owner's `/sc:sweep` (PR 539, eight classes, WC-16 one coordinator sweep per 5 minutes) is kept as the one source; FR-41 adds `session_id` and `worktree_path` to the JSON rows; FR-42 saves the JSON beside the Markdown report; D11 "One data source" (`debates/D11/VERDICT.md:17-21`), DECISIONS.md:24 "The sweep-as-source and observer parts are UNCHANGED" |
| One screen | FR-44 the observer reads `issue-watch status --json` and the saved sweep JSON, shows held issues, stranded deliveries and a zero-repos run, with three states for empty, zero rows and "could not read"; FR-79 shows window, `observed_at` and age and never reads a missing or old file as "no sessions"; FR-81 labels the questions panel exception |
| Per-issue lines for the person | FR-48 `report-entry` as the only writer of an entry file; FR-80 the observer shows entry fields only from an owner-named allowlist, "titles and links only while `report-entry` is absent" |
| Post-merge findings waiting on a person | FR-49 AU4a, AU4c, AU5 as lines of the issue's entry "marked so the sweep lists them as waiting on a person"; OA-25a a waiting PR "shown with the age of the wait" |
| Per-issue state and restart | FR-29 `issues/<repo-key>__<N>.json`, the one adoption record; FR-26 verb group with `report-entry` and `escalate` in it; FR-37 "Write an escalation or entry first" |
| Closing the loop on merged work | FR-38 `/sc:closeout` per merged PR (PR 683, kept) |
| The owner's display rule | "automated checks show outstanding user decisions only, no heartbeat chatter" (D11 verdict, "Our strengths that must be kept", line 67) |

**What the plan would lose** (said plainly)

1. **Plain-English per-issue text** (done, still to do, needs you, links). D11 calls it Clay's strongest point: "the only piece that gives the person, per issue, what is done, what is left, whether it needs them and a link" (`VERDICT.md:48`).
2. **ClickUp.** `clickup.py` (642 lines) reads tasks, comments and chat and joins tasks to issues. Nothing else in the plan reads ClickUp. (Under the plan's own text, the ClickUp send in C27 had no sender before either: DEC:1021 "no escalation notice sender exists in master".)
3. **The silent-loss gate.** `check.py` and `run.py gate`: "A failed read carries items and never closes them, unread sources are listed under 'Not checked', and delivery waits for `check.py`" (`VERDICT.md:49`); "The sweep has no such check (searched; OURS conceded)".
4. **The transcript-since-last-report reader**: up to 30 MB on a first run, against the sweep's 256 KiB tail (`VERDICT.md:50`).
5. **A daily rhythm**: the 07:00 run, the missed-run check, the DM.
6. **A re-listing surface for an unanswered entry.** Issue 718 D1 quotes `OAG1 base-selection.md:76`: "The daily report as the existing re-listing surface for an unanswered entry". Under NO, the observer and sweep show the waiting item with its age every time they are read instead.

The nine-row table and the cap of 5 are not on this list: D11 says both are "spec text only" with "no `escalate` verb ... no `asks.json` exist" (`VERDICT.md:45`), and the cap is a proposal with default 0.

## 5 Costs and risks of NOT restoring, and how to contain each

**R1. The person loses per-issue plain-English text and the ClickUp view.** This is the real cost.
Containment: (a) Clay's daily report keeps running from the IronFlow copy (A8; UNVERIFIED that it still runs, so ask Clay in chat, which is item D4's first half). (b) The owner's interim surface is the chat report, which D11's own action list names: "the report answers issue 409 alignment items 3 and 7 (report owns GitHub reads and text; the chat report is the interim surface)" (`VERDICT.md:84`). (c) When the owner wants it in the observer, add at most five fixed fields (done, left, needs a person, link, last update) to the entry file that `report-entry` writes in S15c and let FR-80's allowlist show them. No ClickUp read, no model call, no DM, no server.

**R2. The silent-loss guarantee has no carrier.**
Containment: keep the property, not the code. The sweep already says "could not determine"; FR-79 already bans reading a missing file as "no sessions". Add one S16 test: a failed or partial read is shown as "could not read", never as done or empty. For GitHub items the coordinator reads the live issue each pass (issue 716 C8 line S08-F8). This is one test and one rule, not 887 lines of `run.py`.

**R3. `/sc:closeout` keeps printing `ENTRY escalated ... why=surface_absent`.**
This is not a cost of saying NO: `report-entry` is missing on the archive branch too, so YES does not fix it. Containment: the owner decides in S15c whether to build `report-entry` or to drop the entry item from closeout; until then the escalation is the designed behaviour (`settle.sh:1037-1039`, `docs/designs/sc-closeout.md:368`).

**R4. Rebuilding later costs more than restoring now.** True in lines, small in practice.
A restore later is a copy of 25 files and one test file from the archive branch. The cost I would add by saying NO is only the loss of the branch. Only `archive/pr-682-issue-pipeline-removal` is tagged (`git tag -l 'archive/*'`); the report's commit `d7d645ddd` has no tag. Containment: ask the owner to tag it (an owner GitHub write; I made none), for example `archive/pr-684-agent-work-report`, before anyone deletes the branch. Also keep the entry-file field names compatible with `common.py:133-151` when S15c writes `report-entry`, because PR 684's body says "PR B's `report-entry` must write the same ones" (the fixed field names are "this PR's choice"). That keeps the door open at near zero cost.

**R5. Drift between the IronFlow copy and IronClaude (issue 718 D4).**
Containment: with NO there is nothing to keep in step; the owner records in chat that the IronFlow copy is Clay's own and IronClaude does not track it.

**R6. Relationship and signal.** Saying NO to a second Clay piece can read as rejecting Clay's work.
Containment: say it is a sequencing decision, point to the archive tag, and offer a path: a smaller owner-reviewed PR for named parts when a requirement asks for them. Note that Clay removed the skill himself in PR 700, so NO matches the state Clay chose.

**R7. The D11 HIGH finding remains for the observer.** Reading only the sweep's session ids drops sessions of removed worktrees (`debates/D11/VERDICT.md:24`, `DECISIONS.md:455`).
Containment: it moves from the report to FR-79 and S16: record it as a known limit, keep FR-45's live side-by-side idea as a one-time check of the observer's session list against Orca before the first live enable (S17), and show the sweep `window` and age so a gap is visible.

**R8. Two of my own reads are weaker than I would like.** (a) "Nothing breaks for Clay" rests on PR 684's body and not on a live check. (b) I read FR-47 and FR-50 as also losing their carrier (FR-50's check names `skills/test_agent_work_report.py`, `SPEC.md:261`), although Appendix B.2 lists only FR-45, FR-46 and FR-48. The owner should confirm that reading.

## 6 The other side's strongest arguments, and my answers

**O1. "It is built and tested: 4,005 test lines, 102 moved cases plus 28 new, 23,260 tests passing, a throwaway-HOME install checked. Why rebuild?"**
Those results are in PR 684's body and I did not rerun them. They show the skill does what Clay designed, not what the plan needs. The plan requires changes to its config, state path, entry schema (only `session_id`, FR-46), naming (D08) and session reads (FR-45), so a restore is a restore plus a rewrite of the parts the tests pin. I grant a real core can be reused: GitHub collection (`collect.py` 317 lines), joining (`match.py` 283), sorting (`classify.py` 147), comparing (`compare.py` 197), checking (`check.py` 350). That is the case for option 3 (lift parts later when a requirement names them), not for restoring the whole skill, its server, its waker and its ClickUp sender now.

**O2. "D11 and D15 rows E1 to E5 already adopted it; the plan is built around it."**
Those adoptions assumed a follow-up PR on a skill sitting on master. The plan now says every action that builds on it is "SUPERSEDED BY PR 700" (`DECISIONS.md:24`, `:33`) and that the carrier of OD-5, OD-9, OA-9, OA-17a, OA-17b and OA-25a "is gone from master. Restoring it is an owner decision" (`:35`). The answers to those six decisions stay UNCHANGED under NO. I read OA-9, OA-17a, OA-17b and OA-25a as needing only the sweep, the observer and entry lines, not the skill; OD-5 names entry lines and OD-9 names "info streams", which I think the coordinator's own `report-entry` can carry but did not read in full (UNVERIFIED for OD-9). D11's own confidence was 72% with stated drop conditions (`VERDICT.md:97`).

**O3. "The report is the only thing that gives the person a per-issue plain-English view. Clay asked for it on issue 409."**
I concede the need (section 4, loss 1). A need is not this implementation. The owner's chosen end state is "one dashboard", the observer (D11 verdict). Per-issue text can live as five allowlisted fields of the entry file (R1c) shown by the observer. Nothing in the spec says that text must be written by a model each morning and mailed through ClickUp.

**O4. "PR 700 was an unreviewed self-merge; restoring corrects a rule breach (B.3 action 3)."**
PR 684 was also self-merged without an owner review (A1). Restoring in order to undo one unreviewed act by re-instating another is not a correction. Both sides already agree the restore must come in "a later owner-approved PR"; my point is that the first review of the code should decide whether it fits, and the findings in A2 and A3 say it does not fit as built.

**O5. "Without the skill, entry files have no schema owner (D11 verdict line 89: 'their format needs one owner and a fixed schema')."**
The schema owner is the coordinator package: `report-entry` is the only writer (FR-48) and FR-26 puts it in the one verb group with one JSON contract. The current schema is a small, documented contract (`common.py:133-151`, `techref:801-807`) that S15c can copy, with a test. The skill is not needed to own it. The only part of the schema that is Clay's choice is the field names (PR 684 body), and R4 keeps them compatible.

**O6. "A rebuild of silent-loss and the gate will cost more than restoring them."**
See R2: the property is one test plus the sweep's existing "could not determine". I agree it would cost more to rebuild the gate's sha256 chain and carry-forward checks (techref line 791). The plan does not ask for those on a screen that shows only the sweep and entry lines, and where it does, a later partial restore of `check.py` is allowed under NO.

**O7. "One owner-reviewed restore PR is cheap; deferring only adds work."**
Restoring as it stands cannot satisfy FR-46, and carries A2. A PR that fixes the server (serve only `report.html`, reject other hosts, no listing, per Clay's own recorded fix), removes person config, renames the coordinator tag and automation prefix and reworks the session read is not cheap to review at 6,471 skill lines plus its test. If the owner later wants that PR, the archive branch and tag make it a day of work, not a loss.

**O8. "Hosts that installed in the window already have the skill; flipping again confuses installs."**
NO needs no new action there beyond the existing B.3 item 5 (`superclaude update` for those hosts). YES adds a second install change for every host.

**O9. "The skill gives C27 a ClickUp DM sender."** True (`clickup.py:596 send_dm`). But C27's own watch-out says a ClickUp DM "needs a ClickUp credential and path; none is described in the plan and the ruling-17 secret rule (S10-F18) applies" and "The owner must say a push is wanted". The plan's default is no push in the first build (OA-25a). The Orca unread mark already exists in the poll (FR-13). I found no recorded owner request for the ClickUp sender.

## 7 Implications if the owner says NO

**Issue 718 (TUI dashboard and report views, items D1 to D4)**

| Item | Fate under NO | Why |
|---|---|---|
| D1 daily run skips issues that have an entry | Dropped | Its own watch-out says "Moot on master today: the daily pipeline and `exclude.py` live in the removed skill". With no daily pipeline in IronClaude there is no double listing to prevent |
| D2 entry shows the human assignee, coordinator link and worker link, or "no live session" with a reason | Rewritten and merged into C14 | The display moves to the observer (S16, FR-80 allowlist). The session link is built from the sweep row's `session_id` (FR-41) at read time; the entry stores only ids (FR-46's good half) |
| D3 where the report session and its state live | Mostly dropped | The report session disappears. The state location for entry files is already settled by the plan's state folder and NFR-02 (one writer per file), as issue 716 C15 says. The "no person in shipped config" test has nothing to test, since no report config ships |
| D4 keep the daily report and the IronFlow copy in step | Half answered, half dropped | The owner's chat answer (which copy runs the daily report, who updates the IronFlow copy) is still worth one line, my proposal: "the IronFlow copy is Clay's own; IronClaude does not track it". The post-restore diff check is dropped |

Issue 718 shrinks from four items to one rewritten item (D2 inside C14) and one chat answer (D4).

**Issue 716 (coordinator, items C1 to C27)**

- **C14** (report entry: content, milestones-only updates, removal at close) stays, rewritten as an S15c task against the coordinator's own entry schema. Drop "work report" wording and the skill's `refresh` and `exclude` stages. Keep the milestone list and the "one write per milestone" test. Entry path follows the state folder, not `.dev/coordinator/orchestrated/`.
- **C8's entry line** (S05-F18: one line when the issue body is edited by another login) is unblocked. Its own watch-out says it "Needs the report-skill restore decision first"; under NO it is simply a line written by `report-entry`.
- **C27** loses its ClickUp option (no sender in IronClaude); the Orca unread mark remains the only notice channel, which also avoids the ClickUp credential and secret-scan questions in its watch-out.
- C21 (text hygiene on `report-entry` and `escalate`) and C22 to C26 are unaffected. Issue 717 (watcher) is unaffected.

**Plan requirements (`spec/SPEC.md`)**

- FR-45 dropped. Its question (sessions of removed worktrees) moves to FR-79 as a known limit (R7).
- FR-46 dropped, except its half "store only `session_id` in entry files", which moves into FR-48.
- FR-47: the nine-row table stays in the notice step only; the cap stays a proposal with default 0 (both are plan text, not skill code).
- FR-48 kept: `report-entry` is the only writer of an entry file, and the schema is defined in the coordinator package.
- FR-49 kept. FR-50 reduced to one S16 test ("a failed read is shown as could not read") as in R2. (My reading; B.2 lists only FR-45, FR-46, FR-48.)
- Section 7 rows E1 and E2 become "not adopted now; archive branch kept"; E4 and E5 dropped for now; E3 reduced to the one test; E7 kept.
- FR-41 to FR-44, FR-79 to FR-81 and the sweep and observer rows of D11 do not change. Section 6.1 row for PR 684 changes from "SUPERSEDED BY PR 700" to "NOT RESTORED: owner decision recorded".
- Out of scope, as you said: `docs/designs/orchestrator.md` (G6).

**What replaces the report**

The sweep with its saved JSON for session facts; `issue-watch status --json` for held issues; the observer as the one screen; the coordinator's entry file (via `report-entry`) for per-issue lines and waiting-on-a-person lines; and the chat report as the interim human view (D11 action line 84).

**Cost of rebuilding later** (if the owner changes mind): a `git checkout origin/clayphi/archive-orchestrator-655-20261120 -- <25 skill files> <1 test file>` restores the code in minutes; the real cost is the rewrite FR-46 and A2 demand, which is the same cost YES would pay now. Insurance: tag `d7d645ddd` (R4) and keep S15c's entry field names compatible with `common.py:133-151`.

**What Clay's design loses.** The living report (E2) and `exclude.py` as IronClaude code; the daily helper's home in IronClaude; the 07:00 waker and ClickUp DM as IronClaude features. It keeps: the entry-file idea (FR-48, FR-49), the item template as the model for the five allowlisted fields, the nine-row table (FR-47), and its own IronFlow copy.

**Who is affected.** Clay (his daily report stays on IronFlow; UNVERIFIED that it runs); the owner (fewer decisions and fewer review items); the builders of S15c and S16 (they own the entry schema); users of `/sc:closeout` (the entry item keeps escalating until S15c or an owner change to closeout); hosts that installed the skill in the 00:02 to 15:07 UTC window (they need `superclaude update`, B.3 item 5).

## 8 What would make me concede

I would move to "restore, in an owner-reviewed PR" if any one of these holds.

1. **C1. A second user.** The owner records in chat that the daily plain-English report with ClickUp is wanted as an IronClaude product for the owner or another named person, not only for Clay. Then the reusable core (about 3,200 lines in `collect.py`, `match.py`, `classify.py`, `compare.py`, `check.py`, `render.py`, `page.py` and `run.py`, or 3,701 with `common.py`) beats a rebuild.
2. **C2. Sweep gap proven.** One live side-by-side run (D11's first UNVERIFIED item) shows the sweep's session map misses sessions that the report's map finds, and the owner wants those sessions on the observer. Then the transcript reader and its session map earn a place.
3. **C3. A small, clean restore.** Someone offers a PR that already fixes the server finding (serve only `report.html`, reject other hosts, no listing), removes `"person": "clayphi"` and the Clay text, renames the tag and prefix to the D08 names, and keeps the archive's tests green, so the owner's review is of a diff and not of 10,488 lines.
4. **C4. The observer must show per-issue prose.** The owner flips OA-17a to "show entry text word for word" and schedules S15c; then `render.entry` and `page.py` code is needed and lifting it is cheaper than rewriting.
5. **C5. The IronFlow copy is dead.** Evidence that Clay's IronFlow copy no longer runs and nobody maintains it (D4, UNVERIFIED today), so IronClaude would be its only home.
6. **C6. A named requirement for the silent-loss gate.** The owner says a failed GitHub or ClickUp read must never silently drop an item on the person's screen, and the S16 test in R2 is judged not enough.

Conditions C1, C4 and C6 would make me argue for restoring only the parts they name (option 3), not the whole skill.

## 9 Recommendation to the owner

Answer NO to Appendix B.3 action 1, in chat, in these words or close to them: "Do not restore `agent-work-report` as it stands. Keep it on the archive branch. Rebuild only what a named requirement needs, inside the coordinator and observer stages." Then (a) ask for `d7d645ddd` to be tagged `archive/pr-684-agent-work-report` so the code cannot be lost; (b) record the one-line answer to issue 718 D4 (the IronFlow copy is Clay's own and IronClaude does not track it) after asking Clay whether it still runs; (c) have the plan reword FR-45 to FR-50 as in section 7 (drop FR-45 and most of FR-46, keep FR-48 and FR-49, reduce FR-50 to one S16 test) and mark rows E1 and E2 "not adopted now"; (d) close or rewrite issue 718 D1 to D4 and unblock C14 and the entry line of C8. The reason is simple: the skill is a large, one-person tool with an unfixed Medium security finding and no owner review, its new part has no writer until stage S15c, and the plan already shows the owner what the sweep, `issue-watch status` and the observer can show. What the owner gives up is per-issue plain-English text, ClickUp and the silent-loss gate; the plan can cover the first and third in small ways (five allowlisted entry fields, one S16 test), and ClickUp has no recorded owner request. If the owner wants the daily report as a product for more than Clay, section 8 names the evidence that should flip this, and the archive branch keeps that door open.
