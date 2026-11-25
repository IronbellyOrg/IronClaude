# Section 07 analysis: The work report, and watching the pull request and merging
Counts: COVERED 22, CONFLICT 7, NOT-COVERED 10

Source: issue 655 body lines 90-105 (section 7), plus acceptance criteria lines 221, 222, 223, 226, 227, 228.
Paths used below: SPEC = .dev/brainstorms/20261120-pr686-unify/spec/SPEC.md, DEC = .dev/brainstorms/20261120-pr686-unify/DECISIONS.md, VERD(x) = .dev/brainstorms/20261120-pr686-unify/debates/x/VERDICT.md, MREQ = .dev/brainstorms/20261120-pr686-unify/brainstorm/run/merged-requirements.md, TECHREF = .dev/brainstorms/20261120-pr686-unify/techref/OBSERVER-SWEEP-DASHBOARD-TECHNICAL-REFERENCE.md (all under /home/coder/workspaces/IronClaude).
Important background: PR 700 removed the work-report skill (`agent-work-report`) and the design doc from master (SPEC Appendix B; SPEC:786 asks the owner whether to restore the skill). Every report-entry row below therefore depends on that open owner decision.

### S07-F1 Same design as Clay's coordinator spec; the IronFlow copy is kept in sync
- 655 says: Section 7 is "one design with Clay's coordinator spec" (`SPEC-AGENT-WORK-COORDINATOR-20261027.md`, FR-1, FR-7, FR-9, FR-19, FR-20, FR-21 cited); the orchestrator is that spec's `/agent-coordinator`; the IronFlow copy is kept in sync, not the home (body line 92; acceptance line 228).
- Status: NOT-COVERED
- Current plan: none found; searched SPEC, DEC, FOLLOW-UPS, MREQ, all VERDICT.md files for "IronFlow", "SPEC-AGENT-WORK-COORDINATOR", "agent-coordinator". The plan never read that spec.
- Component (NOT-COVERED only): OTHER, a document and process task (keep two spec copies aligned), no code in any of the four components.
- Feature statement (NOT-COVERED only): Reconcile Clay's IronFlow coordinator spec with the unified coordinator spec and say which copy is the home.
- Done when: a short note in the repo names the home copy of the coordinator spec and lists which Clay FR numbers (FR-1, FR-7, FR-9, FR-13, FR-19 to FR-21) are kept, changed or dropped.
- Depends on: 655 acceptance line 228 (the other skills and state move to the orchestrator repo), S07-F11, S07-F14.
- Evidence from our documents: VERD(D11):108 "The IronFlow coordinator spec was not read."; VERD(D15):264 "The coordinator spec (IronFlow), `RULINGS.md`, Q26 text ... were not read."; TECHREF:255 "FR-9 ... spec not in the repo [UNVERIFIED]".
- Concerns: The plan removed the separate orchestrator repo (D07 item 2, DEC:325 "Remove ... `IronbellyOrg/IronOrchestrator`"), so "state moves to the orchestrator repo" has no home under the current plan. The wording "orchestrator" is also retired for the role (FR-62, SPEC:319).

### S07-F2 No session-manager skill; the coordinator does every check-in itself, typing included
- 655 says: There is no session-manager skill, now or later; the orchestrator does every check-in itself, including typing into a worker's terminal (body line 92; acceptance line 222).
- Status: COVERED
- Current plan: FR-40 (SPEC:242) lets the coordinator type into worker terminals under four typing rules; D15 row D14 "adopt with change" (DEC:582, VERD(D15):98). No separate session-manager skill appears anywhere in the plan.
- Depends on: none
- Evidence from our documents: n/a (COVERED).
- Concerns: The typing rules are narrower than 655 (see S07-F3). The wording of `agent-work-report/SKILL.md:12` ("The orchestrator (`/sc:orchestrator`) does every check-in itself") is to be corrected to "coordinator" (VERD(D08):63), but that file is gone from master after PR 700.

### S07-F3 The orchestrator approves a worker's permission prompts (FR-23, FR-24)
- 655 says: The orchestrator types into a worker's terminal and approves its permission prompts under FR-23 and FR-24; "always allow" is never sent; refused on unsent typing or fresh output, except the one interrupt (body line 92; acceptance line 222).
- Status: CONFLICT
- Current plan: FR-40 (SPEC:242) "never approve a permission prompt; never interrupt a worker"; D15 row D14 "Reject approving permission prompts (WC:122, WC:137); drop approval rules and test cases" (VERD(D15):98); D15 row D9 interrupt N7 REJECT (DEC:582); OD-7 "No interrupt of a running worker" (SPEC:103). 655's approving of prompts and the one interrupt are REJECTED.
- Depends on: none
- Evidence from our documents: DEC:603 "The coordinator never merges alone, never tags or publishes, never answers a permission prompt, never interrupts a worker."
- Concerns: The owner's WORKER-CONTRACT lines WC:122 and WC:137 (cited in VERD(D15):98) are the stated reason. Unsent-typing and fresh-output refusal rules survive in the plan only as typing rules 1, 2, 3, 5.

### S07-F4 The check-in template and the playbook are part of the skill's one pull request
- 655 says: "the check-in template and the playbook are part of the skill's one PR" (body line 92).
- Status: NOT-COVERED
- Current plan: none found; searched SPEC, DEC, MREQ, VERD(*) for "playbook", "check-in", "check-in template", "session-manager". Only the hourly check wording of the flag `--hourly` (FR-24, SPEC:226) exists. The plan builds the coordinator in stages S12 to S16, several pull requests (SPEC:499 splits S15 alone into four PRs), not one pull request.
- Component (NOT-COVERED only): COORDINATOR, templates and playbook are skill content.
- Feature statement (NOT-COVERED only): Ship a check-in template and a worker-watching playbook with the coordinator skill, with a test that each check-in uses the template.
- Done when: `/sc:coordinator` skill files contain a check-in template and a playbook, and a test fails when a check-in message does not use the template.
- Depends on: 655 sections on the four template files and the hourly worker status check (other analysts), S07-F2.
- Evidence from our documents: SPEC:499 "S15 transport, cap, restart, audit, hand-back, `report-entry`, cleanup `list` (four PRs: S15a ... S15d)" contradicts the "one PR" packaging.
- Concerns: The "one skill PR" packaging cannot be kept; ask the owner only if packaging matters.

### S07-F5 Report entry follows the work report's item template
- 655 says: The entry follows the work report's item template (body line 94; acceptance line 221).
- Status: COVERED
- Current plan: D15 row E5 "Plain-English item template: adopt with change, generic wording" (VERD(D15):113, DEC:585); D11 item 4 (DEC:450); FR-48 `report-entry` is the only writer of an entry file (SPEC:259); FR-46 (SPEC:257).
- Depends on: none
- Evidence from our documents: n/a (COVERED), but see concern.
- Concerns: Conditional. PR 700 removed the report skill from master; DEC:462 "Every action that builds on PR 684's report skill ... (the living report, ... the item template) is SUPERSEDED"; SPEC:786 asks the owner whether to restore it, and says if no, "FR-45, FR-46 and FR-48 are dropped or rewritten".

### S07-F6 The entry carries one of eight FR-9 follow-up states
- 655 says: The entry shows an FR-9 state (working, question, gated, delivered, claimed-missing, stalled, failed, not-started) and the last update (body line 94; acceptance line 221).
- Status: CONFLICT
- Current plan: D11 item "Entry files store only `session_id`; the class is read from the sweep at display time" (VERD(D11), DEC:450; FR-46, SPEC:257), so the state shown is a sweep class, not a stored FR-9 state. The sweep has its own eight classes (VERD(D11):43). 655's stored FR-9 state vocabulary is REJECTED as the stored field.
- Depends on: S07-F1 (FR-9 lives in Clay's spec)
- Evidence from our documents: TECHREF:255 "Orchestrator FR-9: 8 states ... mapping to `worker-list` fields not stated, spec not in the repo [UNVERIFIED] ... `working` and `stalled` occur in more than one set"; TECHREF:917 "Keep UNVERIFIED: ... FR-9 mapping."
- Concerns: Two vocabularies already collide on `working` and `stalled`. A builder may show an FR-9-style label only as a display mapping from the sweep class, never store it.

### S07-F7 Entry shows the human assignee, the holding coordinator and the worker session as links that open in Orca
- 655 says: The entry shows the human assignee, the orchestrator that holds the issue and the worker's session, the last two as links that open in Orca; "no live session" with the reason when none (body line 94; acceptance line 221).
- Status: NOT-COVERED
- Current plan: partly. Entries store only `session_id` (FR-46, SPEC:257); the observer shows fields only from an owner-named allowlist and "titles and links only while `report-entry` is absent" (FR-80, SPEC:263). No requirement names the assignee field, the coordinator link or the Orca-open link. Searched: SPEC, DEC, TECHREF for "orca://", "deep link", "click", "assignee".
- Component (NOT-COVERED only): TUI-DASHBOARD, it is what the owner sees in the report and observer.
- Feature statement (NOT-COVERED only): Show, in each report entry, the human assignee and links to the holding coordinator session and the worker session that open in Orca, or "no live session" with a reason.
- Done when: a test renders an entry for a live and a dead worker; the live one carries an `orca://` link, the dead one reads "no live session" and a reason.
- Depends on: S07-F5, SPEC FR-41 (`session_id` and `worktree_path` in sweep JSON).
- Evidence from our documents: TECHREF:891 "6 deep links (no click-to-open) open"; TECHREF:841 "links must be `http(s)://` or `orca://`"; TECHREF:1235 "`prefs.py answer ... <session url>` cannot answer a 'Needs you' entry (C8-8, DEFECT-CANDIDATE)".
- Concerns: Click-to-open does not exist today (TECHREF:891). The observer's allowlist rule (FR-80) may forbid free text but allows links. Defect candidate C8-8 touches `orca://session` urls.

### S07-F8 The entry is added at claim and updated only at milestones, not on every message
- 655 says: Added at claim; updated at plan done, blocked or asking, PR opened, review rounds summarized, PR ready, merged; not on every worker message or CI change, not hourly for a green PR that waits (body line 94).
- Status: NOT-COVERED
- Current plan: none found for the cadence. FR-48 only names the single writer (SPEC:259), FR-37 says write an escalation or entry first (SPEC:239), SEC-21 says show the age of a waiting PR (SPEC:310). Searched SPEC, DEC, MREQ for "milestone", "update cadence", "every worker message".
- Component (NOT-COVERED only): COORDINATOR, it decides when to call `report-entry`.
- Feature statement (NOT-COVERED only): Call `report-entry` at claim and at a fixed list of milestones only, and never on a worker message, a CI change or an hourly timer for a waiting green PR.
- Done when: a test drives a worker through the milestones and a stream of chatter and counts entry writes: exactly one per milestone.
- Depends on: S07-F5, SPEC FR-48.
- Evidence from our documents: no evidence found in our documents.
- Concerns: SEC-21's "age of the wait" must still be shown without a write; the age can be computed at display time, so no conflict if a builder avoids a periodic write.

### S07-F9 The entry leaves the report when the issue closes
- 655 says: When the issue closes, the entry leaves the report (body line 94; acceptance line 221 "removed at close").
- Status: COVERED
- Current plan: `/sc:closeout` (PR 683, merged) settles the work report entry as one of its three items, only through the entry command (`~/.claude/skills/sc-closeout-protocol/SKILL.md:21`); D13 item 1 (DEC:502), D15 row F1 "adopt as is" (VERD(D15):120); FR-38 (SPEC:240); FR-48 (SPEC:259).
- Depends on: S07-F5
- Evidence from our documents: n/a (COVERED), see concerns.
- Concerns: Closeout calls `superclaude orchestrator report-entry`, a verb that does not exist yet (TECHREF:836 "`settle.sh` `cmd_entry` (calls the absent `report-entry` verb; ends `surface_absent`)"); the plan renames the verbs to `superclaude coordinator ...` (FR-63, SPEC:320), so closeout's text needs the rename too. DEC:519 "Its step that settles a work-report entry depended on PR 684's skill, which is gone (effect UNVERIFIED)."

### S07-F10 Escalations and notices about an orchestrated issue are lines of that issue's own entry
- 655 says: Escalations and notices are lines of the issue's own entry (ruling 24) (body line 94).
- Status: COVERED
- Current plan: FR-37 "Write an escalation or entry first" (SPEC:239); FR-49 AU lines "as lines of the issue's entry" (SPEC:260); OD-5 (DEC:829); SEC-21 (SPEC:310).
- Depends on: S07-F5
- Evidence from our documents: n/a (COVERED).
- Concerns: none

### S07-F11 The daily run no longer touches issue entries; the daily report is phased out
- 655 says: The daily run covers only ClickUp tasks and messages, direct messages, mentions, items with no issue, sessions not under an orchestrator, and a missed-update sweep; the daily report is being phased out; this changes Clay's spec FR-2 and FR-19 (body line 96; acceptance line 221 "daily run no longer touches issue entries (test)").
- Status: NOT-COVERED
- Current plan: none found; searched SPEC, DEC, VERD(D11), VERD(OAG1) for "daily report", "daily run", "phased out", "FR-19", "FR-2". The plan keeps the daily report and relies on it: D11 keeps the report as "the one plain-English report" (DEC:448) and OAG1 uses it as the re-listing surface for an unanswered entry.
- Component (NOT-COVERED only): TUI-DASHBOARD, it is the owner-facing report's scope; the scheduled job itself is an Orca automation outside the repo.
- Feature statement (NOT-COVERED only): Make the daily report skip every issue that has an entry file, and cover only the non-issue sources listed.
- Done when: a test with one entry file and one daily item shows the issue absent from the daily output and the non-issue items present.
- Depends on: S07-F5, the owner decision SPEC:786 (restore the report skill), S07-F1.
- Evidence from our documents: VERD(OAG1) `adversarial/adversarial/base-selection.md:76` "The daily report as the existing re-listing surface for an unanswered entry (`agent-work-report/SKILL.md:22,30`), with the caveat that it is configured for one named person today."; VERD(D11):107 "Whether Clay uses the daily report ... not checked."; TECHREF:809 `exclude.py` removes an entry's issue url, pr_url and `orca://session/<id>` from the daily items (an exclusion mechanism already existed in the removed skill).
- Concerns: Phasing the daily report out would remove the surface the plan uses for OA-25a (a waiting go is re-listed). Ask the owner before adopting "phased out".

### S07-F12 The worker pushes its own branch and opens its own pull request
- 655 says: "The worker pushes its own branch and opens its pull request; it never merges or force-pushes" (body line 98; acceptance line 223).
- Status: CONFLICT
- Current plan: FR-30 binds every worker at guard level `worktree`, not Full Submit (SPEC:232); FR-32 has the coordinator commit after `worker_done` and push worker commits "only on a typed go, after showing them to the person" (SPEC:234); Q04 "a worker never runs `/sc:pr-submit` (Clay's ADD1 stays rejected)" (DEC:743); SEC-05, SEC-22 (SPEC:294, :311); OA-20 "later open level FS" only after the probe (SPEC:583). 655's worker push and PR is REJECTED for the first build.
- Depends on: none
- Evidence from our documents: DEC:750 "Breaks: ... Clay's ADD1 worker route"; DEC:266 level FS is "provisional" and staged behind a live probe.
- Concerns: If the owner opens level FS later, a worker push of a feature branch could become allowed, but only under Q04's go rule; this row stays CONFLICT until then.

### S07-F13 The worker never merges and never force-pushes
- 655 says: The worker never merges or force-pushes (body line 98).
- Status: COVERED
- Current plan: SEC-13 guard "narrows honest drift", SEC-02 no `--admin`/`--auto` (SPEC:302, :291); D05 item 1 "never merge, never push to `master`" (DEC:266); FR-32 (SPEC:234); Q04 fence "no force push" (SPEC:311).
- Depends on: none
- Evidence from our documents: n/a (COVERED).
- Concerns: SEC-13 (SPEC:302) states a worker's own script can still push a feature branch, comment, or on one shared admin login `gh pr merge --admin`; the guard does not close that.

### S07-F14 The orchestrator itself merges when every condition holds
- 655 says: "Only the orchestrator merges", when the conditions of S07-F15 hold, with no person's go; "this issue takes merges and closing off that list" of Clay's spec FR-13 (human-only) (body line 98; acceptance line 223).
- Status: CONFLICT
- Current plan: SEC-01 "Merge only on a person's typed go ... A passing gate never triggers a merge" (SPEC:290); SEC-06 "Carry no standing `pr.merge` or `issue.close`" (SPEC:295); D06 item 1 (DEC:293); D15 row D7 "standing `pr.merge`/`issue.close` and autonomous merge: reject" (DEC:582, VERD(D15)). 655's autonomous merge is REJECTED.
- Depends on: none
- Evidence from our documents: DEC:306 "Clay's wave 7 autonomous merge becomes 'show the gate output and wait for the go'"; DEC:309 "`master` is unprotected ... a person's go is the only brake".
- Concerns: SPEC:48 "a person's go is a procedure, not a block, until an admin sets a ruleset" (FR-75).

### S07-F15 Merge readiness conditions (checks green on the final head, reviewers finished on that head, no open thread, no changes requested, worker_done)
- 655 says: Merge only when every check is green on the final head, every review agent the repo lists has finished on that head, no review thread is open, no review is left at "changes requested", and the worker sent `worker_done` (body line 98; acceptance line 223).
- Status: COVERED
- Current plan: SEC-02 `merge-gate`, 13 closed reasons run before the go and again before the merge, head-pinned (SPEC:291); D06 item 3 lists the refusal reasons `checks_pending`, `review_pending`, `threads_open`, `worker_not_done`, `head_moved`, `snapshot_incomplete` (VERD(D06):16, DEC:295); D15 row D1 (VERD(D15):85).
- Depends on: none
- Evidence from our documents: n/a (COVERED).
- Concerns: They gate a person's go in the plan, they do not trigger a merge (see S07-F14). `merge-gate` is design only, not built (MREQ:586).

### S07-F16 A review left at "changes requested" is a hard refusal that no recorded OK overrides
- 655 says: A review at "changes requested" is "a hard refusal that no recorded OK overrides" (body line 98; acceptance line 227).
- Status: COVERED
- Current plan: OA-13c "`changes_requested` stays a hard refusal" 95% (SPEC:112, DEC:999); SEC-03 (SPEC:292); D15 row D2 "adopt as is" (VERD(D15):86).
- Depends on: none
- Evidence from our documents: n/a (COVERED).
- Concerns: The owner still has to confirm it (VERD(D06):61 lists it as an Owner DECISION; OA-13c records 95% confidence).

### S07-F17 A failing check is never merged without the human's explicit OK
- 655 says: A failing check is never merged without the human's explicit OK (body line 98).
- Status: COVERED
- Current plan: SEC-03 "only `checks_failing` and `merge_safety` may be overridden, each with its own key" (SPEC:292); SEC-08 four checks on a recorded go (SPEC:297); D06 item 3 (DEC:295).
- Depends on: none
- Evidence from our documents: n/a (COVERED).
- Concerns: The OK must be typed by a person in their own session; `answer-check` cannot tell a person from a script (SEC-09, SPEC:298).

### S07-F18 A review agent that does not run or finish holds the pull request; `reviewers: none` means no hold
- 655 says: A review agent that does not run or finish holds the pull request and escalates (row 9); `reviewers: none` means no hold (body line 98).
- Status: COVERED
- Current plan: SEC-04 merge-time hold: owner-set `reviewers` list (`none` an explicit exception), re-request on the final head, wait 60 minutes (UNVERIFIED), then escalate (SPEC:293); OA-13b (SPEC:111, DEC:983); D15 row D3 (VERD(D15):87). SEC-10 makes `reviewers: none` fail closed unless an owner record names it (SPEC:299).
- Depends on: none
- Evidence from our documents: n/a (COVERED).
- Concerns: The plan is stricter: `reviewers: none` needs a recorded owner OK, 655 treats it as a plain config value. The 60-minute wait is UNVERIFIED (SPEC:293).

### S07-F19 Merge-safety hold: CI and merge-gate files wait for the owner's OK tied to `merge_safety:<PR>:<head sha>`
- 655 says: A PR changing a file on `merge_safety_files` waits for explicit OK even when green; the OK is tied to key `merge_safety:<PR>:<head sha>`; a new push needs a new OK; the OK for a failing check never clears it; the file list is the paginated REST list with old and new paths; an unreadable list is a hold (body line 98; acceptance lines 223, 227).
- Status: COVERED
- Current plan: SEC-03 `merge_safety` overridable only with its own key (SPEC:292); SEC-08 question key `merge_safety:<PR>:<head sha>` (SPEC:297); D15 rows D1 "fail-closed file list" and D2 "`merge_safety` hold: adopt as is" (VERD(D15):85-86); D06 strengths note a rename out of `.github/workflows/` is visible to the gate (VERD(D06):34); SEC-10 refuses `merge_safety_files: []` (SPEC:299).
- Depends on: none
- Evidence from our documents: n/a (COVERED).
- Concerns: none

### S07-F20 Default content of `merge_safety_files`
- 655 says: `merge_safety_files` defaults to workflows, branch protection and ruleset files, CODEOWNERS, and the files the repo's merge gate reads (body line 98).
- Status: NOT-COVERED
- Current plan: none found; searched SPEC, DEC, MREQ, VERD(D06) for "CODEOWNERS", "workflows", "merge_safety_files". The key exists (MREQ:354, SEC-10 SPEC:299) but no default content is stated. FR-12 says "an absent authority key means the most restrictive value" (SPEC:202), which is a different rule from a default list.
- Component (NOT-COVERED only): COORDINATOR, it is per-repo configuration the coordinator reads at merge time.
- Feature statement (NOT-COVERED only): Define the default `merge_safety_files` list and say how it combines with the "absent means most restrictive" rule.
- Done when: a config test shows that a repo with the key absent gets the stated default list, and an empty list is refused.
- Depends on: S07-F19, SPEC FR-12, SEC-10.
- Evidence from our documents: SPEC:48 "`master` is unprotected today (`protected: false`, no ruleset, no CODEOWNERS ...)"; FR-75 adds CODEOWNERS later (SPEC:339).
- Concerns: A default that names ruleset or CODEOWNERS files is moot in IronClaude until FR-75 lands.

### S07-F21 The merge method is the repo's own (`merge_method`, `release_merge_method`)
- 655 says: The merge method comes from `repos.yaml` (`merge_method`, `release_merge_method`); IronClaude squashes ordinary pull requests and merges a release pull request with a merge commit (body line 98).
- Status: COVERED
- Current plan: D07 item 5 "optional per-repo `merge` settings block (`merge_method`, `release_head`, `release_merge_method`, `can_merge`, `reviewers`, `merge_safety_files`)" (DEC:328); MREQ:354 lists the same keys in the per-repo config; VERD(D06):44 keeps per-repo `merge_method` and `release_merge_method` ("the go names the method and the gate checks it"); SEC-01 the go names the method (SPEC:290). The file is per-repo JSON, not `repos.yaml` (FR-12, SPEC:202; R-3 DEC:593).
- Depends on: none
- Evidence from our documents: n/a (COVERED).
- Concerns: No SPEC requirement row names `merge_method` (searched SPEC.md; only DEC, MREQ and VERD(D06) do), so the loader support for the key has no FR number. VERD(D06):44 gives the reason (squash merge of release 6.1.0 (#658) was reverted by #662). One source (VERD(D07) variant-2, `adversarial/variant-2-original.md:25`) words the IronClaude split as "`integration` with a merge commit and `master` with a squash"; which wording is right for the repo is UNVERIFIED.

### S07-F22 Every `gh` call is pinned to the issue's own repo, never to an upstream parent
- 655 says: Every `gh` call is pinned to the issue's own repo, never to an upstream parent (body line 98).
- Status: COVERED
- Current plan: SEC-02 the merge command is `gh pr merge <N> --repo <R> --<method> --match-head-commit <sha>` (SPEC:291); the project rule (CLAUDE.md "PR Target = Fork") and brainstorm topic constraint "every gh call passes `--repo IronbellyOrg/IronClaude`" (`brainstorm/TOPIC.md:20`).
- Depends on: none
- Evidence from our documents: n/a (COVERED).
- Concerns: The plan pins the merge command by `<R>` from config; a requirement that every other coordinator `gh` call carries `--repo` is not stated as an FR (searched SPEC; only SEC-02 and the project rules say it). Also note the pin in 655 means the issue's own repo, while the project rule fixes this fork's `gh` target as `IronbellyOrg/IronClaude`.

### S07-F23 For this build no pull request is merged by the orchestrator session or any worker; the owner does the QA and merge
- 655 says: For THIS build no pull request is merged by the orchestrator session or any worker; each stops at green and the owner does the QA and the merge (body line 98).
- Status: COVERED
- Current plan: SEC-01 no merge without the person's typed go (SPEC:290); D06 item 1 (DEC:293); SEC-21 shows a PR waiting for a go as "waiting on a person" (SPEC:310).
- Depends on: none
- Evidence from our documents: n/a (COVERED).
- Concerns: The plan makes this permanent, not only for this build.

### S07-F24 Readiness reuses the `superclaude.pr_submit` core and the poll scripts of `/sc:pr-submit --monitor 3`
- 655 says: Readiness reuses the `superclaude.pr_submit` core and the poll scripts of `/sc:pr-submit --monitor 3` (body line 98).
- Status: NOT-COVERED
- Current plan: none found; searched SPEC, DEC, VERD(D06), MREQ for "pr_submit", "superclaude.pr_submit", "poll scripts". The plan builds `merge-gate` as new code (MREQ:586 "DESIGN ONLY ... in none of master, pr-a or pr-p") and only keeps `/sc:pr-submit`'s silent-reviewer skip in its own loop (SEC-04, SPEC:293).
- Component (NOT-COVERED only): COORDINATOR, it is how the merge-gate reads PR readiness.
- Feature statement (NOT-COVERED only): Make `merge-gate` read PR readiness through the existing `superclaude.pr_submit` core instead of new GitHub-reading code.
- Done when: `merge-gate` imports from `superclaude.pr_submit` for the check, thread and review reads, and a test shows one shared function answers both.
- Depends on: SPEC SEC-02 (`merge-gate`), the reuse-auditor check in a later review.
- Evidence from our documents: VERD(D06):39 "Read-only merge gate ... Why: the owner's rules are prose; no hook binds the coordinator."; DEC:311 "UNVERIFIED: ... `merge-gate` and `answer-check` exist nowhere."
- Concerns: Whether the pr_submit core exposes what the 13 reasons need is UNVERIFIED (not read). The owner rule SEC-05 forbids running `/sc:pr-submit` as a worker; reusing its library is a different thing.

### S07-F25 Worker pull requests link the issue with `Fixes` only when fully done, otherwise `Refs`
- 655 says: Every worker PR links its issue with `Fixes <repo>#<number>` only when it fully addresses the issue and `Refs <repo>#<number>` otherwise (rulings 26 and 38); a wrongly written `Fixes` still closes the issue and no script checks it (K28) (body line 100).
- Status: NOT-COVERED
- Current plan: only the hazard is stated. SEC-12 "state that a `Fixes` line still closes at merge" (SPEC:301); OD-10 "A `Fixes` line in the PR body still closes the issue at merge with no coordinator write" (DEC:909); RK-10 "Closeout or a `Fixes` line closes unfinished work" (SPEC:654). The worker-side rule of when to write `Fixes` or `Refs` is not a requirement. Searched SPEC, DEC, VERD(*) for "Fixes", "Refs".
- Component (NOT-COVERED only): COORDINATOR, it belongs in the handoff brief and the worker's PR text template.
- Feature statement (NOT-COVERED only): Put the `Fixes`/`Refs` rule into the worker brief template and state in the skill that no script checks it.
- Done when: the handoff template test finds the rule text, and the skill text names the unchecked-`Fixes` limit.
- Depends on: 655 section 5 handoff nine sections (other analyst), S07-F12 (who opens the PR).
- Evidence from our documents: SPEC:654 RK-10 "Closeout or a `Fixes` line closes unfinished work ... | close only under the go | SEC-12, FR-45 tests".
- Concerns: Because the plan does not let the worker open the PR in the first build (S07-F12), who writes the PR body is open; the rule applies to whoever pushes.

### S07-F26 After any merge, including one made by a person, the next wave calls `/sc:closeout <PR>`
- 655 says: After a merge, including a merge made by a person, wave 8 calls `/sc:closeout <PR>`, the separate skill from #668, merged before the live test (body line 100; acceptance line 226).
- Status: COVERED
- Current plan: FR-38 "call `/sc:closeout <PR>` per merged PR under a go naming the close" (SPEC:240); D13 (DEC:502-503); D15 row F1 adopt as is (VERD(D15):120); PR 683 merged, KEEP (SPEC:392); SEC-05 never run closeout as a worker (SPEC:294).
- Depends on: none
- Evidence from our documents: n/a (COVERED).
- Concerns: FR-38 attaches the go condition (see S07-F28). Closeout has no tests with a fake in the plan; 655's "PR B's tests use a fake" has no equivalent, but PR B is not started (SPEC:389).

### S07-F27 Closeout decides "done" from the issue's own criteria, never from the words Fixes, Closes or Refs
- 655 says: It decides whether the issue is done by reading the issue's own criteria (Fix approach, Test plan, acceptance criteria, "Done when") against what the PR and linked PRs delivered, never by `Fixes`, `Closes` or `Refs` (ruling 32); unclear after investigating is escalated (row 9) (body line 100).
- Status: COVERED
- Current plan: the built skill does exactly this: `~/.claude/skills/sc-closeout-protocol/SKILL.md:24` "The words `Fixes`, `Closes` and `Refs` are read as data and decide nothing"; `refs/done-check.md:26-28` (`done`, `not_done`, `unclear_escalate`). The plan adopts it as is (VERD(D15):120; SPEC:465 F1).
- Depends on: none
- Evidence from our documents: n/a (COVERED).
- Concerns: none

### S07-F28 Closeout closes a done issue by itself, with one note; the orchestrator runs no `gh issue close`
- 655 says: When done, closeout "closes the issue with one note; the orchestrator no longer runs `gh issue close`" (body line 100; acceptance line 226 "closes only a done issue").
- Status: CONFLICT
- Current plan: OD-10 "One per-PR go, bound to the head sha, covers both the merge and the close ... no standing `issue.close`" (DEC:909, SPEC:106); SEC-12 (SPEC:301); SEC-06 (SPEC:295); FR-38 "under a go naming the close" (SPEC:240). Closeout therefore runs only under a person's recorded go that names the close. 655's unconditional close is REJECTED; "the coordinator runs no `gh issue close`" is consistent.
- Depends on: none
- Evidence from our documents: DEC:911 "Wave 8 changes so closeout runs only under a go that names the close."; DEC:909 "`E-NO-GRANT` covers only writes made through the orchestrator's own verbs and closeout writes the close through `scripts/settle.sh`".
- Concerns: DEC:913 UNVERIFIED "that no other check stops closeout's close; whether the verbs see closeout's write".

### S07-F29 Not done: closeout leaves the issue open with one note, returns the unmet criteria and starts nothing
- 655 says: A closeout that finds the PR did not finish the issue leaves it open with one note, returns the unmet criteria and starts nothing (body line 102).
- Status: COVERED
- Current plan: the built skill: `~/.claude/skills/sc-closeout-protocol/SKILL.md:85` "`ISSUE settled how=left_open remaining=<k>`, one marked note, the issue is never closed; the block hands back (`issue.handback: remaining`)"; D15 row D18 notes "Closeout prints `left_open` and nothing consumes it" (VERD(D15):102).
- Depends on: none
- Evidence from our documents: n/a (COVERED).
- Concerns: none

### S07-F30 Hand-back bookkeeping: record `round` and `remaining`, wait until the old worker is final, never stop it, release it
- 655 says: The orchestrator records what remains (`round`, `remaining` in the state file; the entry says "merged, the issue is not finished: ... (round n)"), waits until the old worker is final (`worker_done` received; it never stops a worker), then releases it (body line 102).
- Status: COVERED
- Current plan: FR-35 "Run the hand-back loop (`handback` ... old worker final first; idempotent re-plan marker)" (SPEC:237); FR-29 per-issue state file (SPEC:231); D15 row D18 "wait until the old worker is final" (VERD(D15):102); OD-7 no interrupt of a running worker (SPEC:103); FR-40 (SPEC:242). `handback` is a pure function over the saved closeout result and the state file and makes no GitHub call (D15 round-2 rebuttal, `debates/D15/adversarial/adversarial/rounds/round2-rebuttal-1-ours.md:154`).
- Depends on: S07-F29
- Evidence from our documents: n/a (COVERED).
- Concerns: The entry wording "merged, the issue is not finished ... (round n)" is not in the plan (see S07-F8 for entry content rules).

### S07-F31 Re-plan through `/sc:issue --plan <N> --remaining <file>`
- 655 says: The orchestrator updates the plan through `/sc:issue --plan <N> --remaining <file>` (body line 102; acceptance line 226).
- Status: COVERED
- Current plan: FR-35 "round 2 re-plans with `/sc:issue --plan <N> --remaining <file> --depth <d>`" (SPEC:237); FR-53 adapts PR 690 before merge (SPEC:274); D15 rows A7 and A8 (DEC:570).
- Depends on: none
- Evidence from our documents: n/a (COVERED).
- Concerns: PR 690 is still an open draft (SPEC:385); `--remaining` has no caller until `handback` exists (DEC:783 "PR 690's `--remaining` gets its first caller").

### S07-F32 The next round starts without the person re-approving, and the issue stays in flight
- 655 says: A new worker starts on a new branch through waves 4 to 9 straight after the re-plan; "the issue stays in flight" (body line 102).
- Status: CONFLICT
- Current plan: OD-2 "re-plan the body, then the person re-applies the approval ... pass the start gate again" (DEC:781, SPEC:98); FR-35 "enters `waiting_reapproval` (outside the cap ...), then the poll gives a NEW wake id and the whole start gate repeats" (SPEC:237); OD-13 "A waiting step does not count toward `max_in_flight`" (DEC:957, SPEC:109); SEC-21 (SPEC:310). 655's no-re-approval restart and "stays in flight" are REJECTED.
- Depends on: none
- Evidence from our documents: DEC:781 "a body edit after approval voids the approval, so a re-plan without re-approval would start a worker on a body nobody approved; Clay's text has no round-2 gate and Clay's advocate conceded this."
- Concerns: SPEC FR-35 (SPEC:237) lets a waiting hand-back expire to `stopped` only on an owner-set limit with no default. The owner may pick option (b) of OD-2 instead (DEC:781), which would drop the re-approval step.

### S07-F33 New branch `issue-<N>-r<n>` in the reused worktree; the guard looks at tracked changes only
- 655 says: The new worker starts on a new branch `issue-<N>-r<n>` in the reused worktree through waves 4 to 9; "the guard looks at tracked changes only" (body line 102).
- Status: NOT-COVERED
- Current plan: partly. D15 row D18 and the round-2 text say the hand-back "makes a new branch and starts a new worker" (`debates/D15/adversarial/adversarial/rounds/round2-rebuttal-1-ours.md:154`), but no requirement names the branch pattern or the worktree reuse. FR-30 binds each worker start with a new `pending` marker (SPEC:232). Searched SPEC, DEC, VERD(*) for "issue-<N>-r", "reused worktree", "tracked changes".
- Component (NOT-COVERED only): COORDINATOR, it starts the worker.
- Feature statement (NOT-COVERED only): Start each hand-back round on a new branch `issue-<N>-r<n>` in the issue's existing worktree, with the start-time worktree check looking at tracked changes only.
- Done when: a test drives a round 2 and finds the branch name `issue-<N>-r2`, the same worktree path, and a start that passes with only untracked files present and is refused with tracked changes.
- Depends on: S07-F32, SPEC FR-30, FR-33 (cap 1 until claim agents get their own worktree).
- Evidence from our documents: DEC:331 "claim agents launch into the same `Coordinator` worktree as the standing coordinator, against 'one live agent per worktree'"; SPEC:235 FR-33 "first build enforces 1 until claim agents have their own worktree".
- Concerns: "The guard looks at tracked changes only" is UNVERIFIED (which guard check is meant is not stated; not found in our documents). Reuse of a worktree after `release-worker` interacts with the one-agent-per-worktree rule.

### S07-F34 Hand-back bounds: at most 3 hand-backs (4 rounds); stop when a round leaves the same unmet criteria
- 655 says: The `handback` verb bounds the loop at 3 hand-backs (4 rounds) and stops when a round leaves the same unmet criteria (body line 102; acceptance line 226).
- Status: COVERED
- Current plan: FR-35 "`HANDBACK_MAX` 3 'not measured', `no_progress`, stop on empty list" (SPEC:237); D15 row D18 (VERD(D15):102); round-2 rebuttal "stopping on `cap`, `no_progress` or `no_remaining`" (`round2-rebuttal-1-ours.md:154`).
- Depends on: none
- Evidence from our documents: n/a (COVERED).
- Concerns: The cap value is labelled "not measured" (VERD(D15):102; DEC:785 "`HANDBACK_MAX` = 3 is 'not measured'"). What counts as "no progress" is UNVERIFIED beyond the name.

### S07-F35 A stop, a failed re-plan or an unusable worktree during hand-back is escalated in the issue's own entry
- 655 says: "a stop, a failed re-plan or an unusable worktree is row 9 in the issue's own entry" (body line 102).
- Status: NOT-COVERED
- Current plan: partly. FR-35 lists three stops (empty list, `HANDBACK_MAX`, `no_progress`) (SPEC:237); FR-37 writes an escalation or entry first (SPEC:239). A failed re-plan and an unusable worktree are not named as stops. FR-47 uses the nine-row table "in the notice step only" (SPEC:258), so there is no row-9 gate. Searched SPEC, DEC for "failed re-plan", "unusable worktree", "row 9".
- Component (NOT-COVERED only): COORDINATOR, it owns the hand-back verb and the escalation writer.
- Feature statement (NOT-COVERED only): Make `handback` return a named stop and write an entry line for a failed re-plan and for an unusable worktree, as well as the three existing stops.
- Done when: tests force a failing `--plan --remaining` call and a missing worktree, and each ends with a stop reason and one escalation line in the issue's entry, no worker started.
- Depends on: S07-F30, S07-F10.
- Evidence from our documents: DEC:959 "Using `escalated` is not stated in Clay's design (line 616 says nothing is escalated for a hand-back), so this is a recommendation with checks."
- Concerns: The nine-row table is only an inventory in the plan (D06 item 10 DEC:302), so "row 9" must be mapped to an entry line, not a notice.

### S07-F36 Audit: eight checks AU1 to AU8 on the pull request that landed, whoever merged it
- 655 says: `superclaude orchestrator audit` runs eight checks adapted from Jay's audit on the PR that landed, whoever merged it: AU1 force push, AU2 review dismissed, AU3 thread resolved with no real reply, AU4 merged over a change request, a pending review request or an unresolved thread, AU5 conflict markers, AU6 baseline or tests loosened, AU7 merge-safety control changed, AU8 a bot fix after a "@codex fix this" style request (a warning only) (body line 104; acceptance line 227).
- Status: COVERED
- Current plan: FR-36 "Run audit AU1-AU8 (AU5 narrowed to `<<<<<<< ` or `>>>>>>> `) and state it cannot see a push with no PR" (SPEC:238); `audit` is one of the `superclaude coordinator` verbs (FR-26, SPEC:228); D15 row D15 "Keep after a go as well" (VERD(D15):99); D06 strengths "it can find a merge the gate did not make, including a raw `gh pr merge`" (VERD(D06):46); stage S15c (SPEC:499).
- Depends on: none
- Evidence from our documents: n/a (COVERED).
- Concerns: AU5 is narrowed by the plan (655's AU5 wording differs). The verb is named `superclaude coordinator audit`, not `superclaude orchestrator audit` (FR-63, SPEC:320). The plan adds a test that fails if the design says the audit covers a push with no PR (DEC:270). The check definitions lived in the design doc removed by PR 700 (SPEC:389), so the AU1 to AU8 text must come from the archive branch.

### S07-F37 The audit uses no model and writes nothing to GitHub
- 655 says: The audit is "no model" and has "no GitHub write" (body line 104; acceptance line 227).
- Status: COVERED
- Current plan: implied by the verb design. FR-26 makes `audit` a verb of the script group with one JSON contract (SPEC:228); `handback` is described as a pure function making no GitHub call (`round2-rebuttal-1-ours.md:154`); FR-82 names the only two code paths that may write to GitHub, neither is the audit (SPEC:218).
- Depends on: none
- Evidence from our documents: n/a (COVERED).
- Concerns: "No model" is not stated as a requirement in the plan; it is implied (UNVERIFIED as a test).

### S07-F38 The audit result goes into the entry, and only AU4a, AU4c and AU5 reach Clay
- 655 says: The result goes into the entry. Only AU4a, AU4c and AU5 reach Clay (row 8); warnings never do (body line 104; acceptance line 227).
- Status: CONFLICT
- Current plan: OD-5 and FR-49: the three findings are written as lines of the issue's own entry, marked as waiting on a person; the push notice is reserved and built only after three triggers (owner says a push is wanted and a cap number, a notice sender is built and tested, row 8 usable alone) (DEC:829, SPEC:260, SPEC:101); SEC-21 "no push notice in the first build" (SPEC:310). 655's reach-Clay channel is REJECTED for the first build; "warnings never reach the person" agrees with OD-5.
- Depends on: S07-F10
- Evidence from our documents: DEC:831 "A conflict marker found by AU5 can sit until the report is read (known limit)."; DEC:833 "UNVERIFIED: whether any notice sender exists or works".
- Concerns: The plan's confidence on OD-5 is only 60% (DEC:122).

### S07-F39 The orchestrator opens no follow-up issue after an audit finding
- 655 says: "the orchestrator opens no follow-up issue" (body line 104).
- Status: COVERED
- Current plan: SEC-07 lists the only grants the owner may give: `issue.assign`, `issue.comment`, `issue.body.append_plan_sections`, `issue.status.move`; none opens an issue (SPEC:296). FR-82 limits GitHub writers (SPEC:218). OD-5 says one escalation per pull request, in the entry (DEC:829).
- Depends on: none
- Evidence from our documents: n/a (COVERED).
- Concerns: none

## Section summary
- 39 features: 22 covered, 7 conflict, 10 not covered. The conflicts all come from one rule: the current plan keeps a person in every outward step. 655's autonomous merge (F14), worker push and PR (F12), automatic close (F28), no-re-approval hand-back (F32), approving permission prompts (F3), a push notice to Clay for audit findings (F38) and a stored FR-9 state (F6) are rejected.
- Merge gate conditions, changes_requested, merge-safety hold, reviewer hold, merge method, closeout, hand-back bounds and the audit AU1 to AU8 are covered, but as design text that is not built yet (MREQ:586 "DESIGN ONLY"); only `/sc:closeout` exists.
- Not-covered work: coordinator items (check-in template and playbook F4, milestone-only entry updates F8, default `merge_safety_files` F20, readiness reuse of the pr_submit core F24, Fixes/Refs rule in the worker brief F25, hand-back branch and worktree reuse F33, more hand-back stops F35), dashboard items (assignee and Orca links F7, daily-run scope F11) and one process item (F1, IronFlow spec reconciliation).
- Every report-entry row (F5 to F11) depends on the owner's open decision whether to restore the removed work-report skill (SPEC:786). F11 also clashes with the plan's own use of the daily report as a re-listing surface.
- Concern for builders: the built `/sc:closeout` still calls `superclaude orchestrator report-entry`, a verb that does not exist and that the plan renames (TECHREF:836, FR-63).


