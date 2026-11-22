# Section 04 analysis: The skill's structure and templates
Counts: COVERED 15, CONFLICT 7, NOT-COVERED 16

Paths used below. `W` = /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify. `SPEC` = W/spec/SPEC.md. `D15` = W/debates/D15/VERDICT.md. `QG2` = W/debates/QG2/VERDICT.md. `ISSUE` = the saved body of issue 655 (line numbers are body lines). The current plan says "coordinator" where 655 says "orchestrator"; the two are matched as the same role (decision D08).

Where 655 names a thing "orchestrator" and the plan names it "coordinator", the row is COVERED and the Concerns line says the builder must use the coordinator name (D08 item 2 pins a test: no `commands/orchestrator.md`, no `sc-orchestrator-protocol`).

## Command file

### S04-F1 Command file `/sc:orchestrator`, a thin file at `src/superclaude/commands/orchestrator.md`
- 655 says: the command is a thin file at `src/superclaude/commands/orchestrator.md` (ISSUE line 62).
- Status: COVERED
- Current plan: FR-24 (SPEC:226) "Provide role "coordinator", command `/sc:coordinator`, skill `sc-coordinator-protocol` ... no `commands/orchestrator.md`"; D08 item 2 (W/debates/D08/VERDICT.md:18); interface row 8 (SPEC:178). The plan names no "thin file" size rule, only the existence and the name.
- Depends on: S04-F3 (the skill the command calls)
- Evidence from our documents: W/debates/D08/VERDICT.md:18 "Test: no `commands/orchestrator.md` and no `sc-orchestrator-protocol` exists after the unified work."
- Concerns: the file must be named `commands/coordinator.md` (or the installed equivalent). The project rule in the repo CLAUDE.md (a `/sc:` command must invoke its skill first) applies to it. The command does not exist in the checkout today (checked: no coordinator or orchestrator file under `src/superclaude/commands` or `src/superclaude/skills`).

### S04-F2 Command flags `--wake <wake_id>`, `--hourly`, `--resume`, `--take <owner/repo#N>`
- 655 says: the command's usage lists exactly these four flags (ISSUE line 62).
- Status: COVERED
- Current plan: FR-24 (SPEC:226) lists the same four flags and adds `--sub` (evaluation only, issue 444); FR-25 (SPEC:227) "Treat flag-less `/sc:coordinator` as person-opened: no grant, no merge; grants have one door (`--wake` or `--take`)"; D15 G2 (D15:130).
- Depends on: none
- Evidence from our documents: SPEC:226-227 quotes above.
- Concerns: 655 has no rule for a flag-less call; the plan adds one (person-opened, no grant, no merge). `--wake` and `--take` are the only door for grants (D08 item 4), so `--hourly` and `--resume` must not give any grant.

## Protocol skill layout

### S04-F3 Protocol skill `sc-orchestrator-protocol`, modelled on `sc-issue-protocol`, `sc-pr-submit-protocol`, `sc-troubleshoot-protocol`
- 655 says: the skill lives in `src/superclaude/skills/sc-orchestrator-protocol/` and follows the layout of three existing protocol skills (ISSUE line 62).
- Status: COVERED
- Current plan: FR-24 (SPEC:226) names `sc-coordinator-protocol`; interface row 8 (SPEC:178); stage S14 builds "`/sc:coordinator` command and skill" (SPEC:498). The plan does not say which existing skills it is modelled on.
- Depends on: S04-F1
- Evidence from our documents: SPEC:498 "S14 merge path as one unit plus bound worker route | SEC-01 to SEC-13, FR-30 to FR-32, `/sc:coordinator` command and skill".
- Concerns: name must be `sc-coordinator-protocol`. The skill is edited under `src/superclaude/`, then `make sync-dev` (NFR-06, SPEC:344).

### S04-F4 Mandatory Activation section in the skill
- 655 says: the skill has a mandatory Activation section, like the three model skills (ISSUE line 62).
- Status: NOT-COVERED
- Current plan: none found; searched: "Activation", "SKILL.md", "sc-coordinator-protocol" in SPEC, D15, W/DECISIONS.md, W/spec/FOLLOW-UPS.md, W/brainstorm/run/merged-requirements.md. Only FR-24 names the skill; no document describes its sections.
- Component (NOT-COVERED only): COORDINATOR (the skill is the coordinator session's protocol)
- Feature statement (NOT-COVERED only): The coordinator skill opens with an Activation section that makes the model load the skill before any other output when `/sc:coordinator` is typed.
- Done when (NOT-COVERED only): A test reads `SKILL.md` and finds an Activation section, as the existing protocol skills pass today.
- Depends on: S04-F3
- Evidence from our documents: no evidence found in our documents. (The repo's own CLAUDE.md, "ABSOLUTE RULE: Custom Command Skill Invocation", already requires the invocation for every `/sc:` command.)
- Concerns: none; the repo rule makes this cheap and not optional.

### S04-F5 `SKILL.md` with numbered waves 0 to 9, each wave naming its ref, commands, template and ending check; the skill loads Orca's own `orchestration` skill at run time
- 655 says: `SKILL.md` carries numbered waves (ISSUE line 62; the wave table is lines 35-46; acceptance line 217 "lists waves 0 to 9 with ref, commands, template and ending check"; line 220 "loads Orca's own `orchestration` skill at run time; each wave names its Orca commands").
- Status: NOT-COVERED
- Current plan: none found; searched: "wave", "numbered", "orca skills get", "orchestration skill", "run-create" in SPEC, W/DECISIONS.md, all debates VERDICT.md, merged-requirements.md. The plan has stages for the BUILD (S0 to S17) but no runtime wave list for the coordinator. D08 only says "Orchestration" names Orca's layer (W/debates/D08/VERDICT.md:33 area).
- Component (NOT-COVERED only): COORDINATOR
- Feature statement (NOT-COVERED only): The coordinator skill describes its runtime workflow as numbered waves, each with a ref file, its Orca and SC commands, its template and the check that ends it, and loads Orca's own `orchestration` skill first.
- Done when (NOT-COVERED only): A test parses the skill's wave table and finds, for every wave, a ref file that exists, a template (or "none") and a stated ending check.
- Depends on: 655 section 2 (the wave contents, owned by another analyst); S04-F8 (refs)
- Evidence from our documents: W/techref/ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md:343 "18 Binding of coordinator-started workers | NOT BUILT" shows the wave that starts workers is itself unbuilt; SPEC:62 "NOT BUILT anywhere | Coordinator command and skill".
- Concerns: the wave contents must be rewritten to the plan's rules (assignment is not the trigger, FR-01; no standing merge, SEC-01; hand-back re-approval, FR-35). Copying 655's wave table as it stands would import contested rules. The `orchestration` skill name here is Orca's layer name and stays (FR-62, SPEC:319).

### S04-F6 "Will Do" and "Will Not Do" lists in the skill
- 655 says: `SKILL.md` has Will Do and Will Not Do lists (ISSUE line 62).
- Status: COVERED
- Current plan: D15 D8 (D15:92) "scan test of skill text for commands outside "Will Not Do""; FR-26 (SPEC:228) closed `refuse(argv)` list with a failing test per pattern; stage S14 deliverable "skill-text scan" (SPEC:498).
- Depends on: S04-F17 (the refusal function that the Will Not Do list matches)
- Evidence from our documents: D15:92 quote above.
- Concerns: the plan's Will Not Do list is narrower in one place: no interrupt (OD-7, SPEC:103) and tag/publish refused unconditionally (SEC-11, SPEC:300); 655 section 9 has an interrupt exception.

### S04-F7 Error table with named STOP codes in `SKILL.md`
- 655 says: the skill has an error table with named STOP codes (ISSUE line 62).
- Status: NOT-COVERED
- Current plan: none found for a skill-level table; searched: "STOP code", "error table", "E-" prefixes in SPEC, D15, W/DECISIONS.md. Partial neighbours exist: `E-NO-GRANT` for a grantless write (SEC-07, SPEC:296), the 13 closed merge-gate reasons (SEC-02, SPEC:291) and the closed reason table of the poll (D15 E6, D15:114). None is a skill STOP table.
- Component (NOT-COVERED only): COORDINATOR
- Feature statement (NOT-COVERED only): The coordinator skill carries one table of named STOP codes (code, when it fires, what the model does next) and a test that every code in the skill text is in the table and the reverse.
- Done when (NOT-COVERED only): A test lists every `E-...` token in the skill files and the verbs and finds each in the table.
- Depends on: S04-F14 (verbs raise some codes); 655 section 9 (escalation rows that follow a STOP)
- Evidence from our documents: W/techref/ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md:1611 shows the claim skill already has 13 prose STOP codes; the same file at line 1708 notes `tests/skills/test_issue_protocol.py:350` "every warning code has a remedy line", so the pattern and a test style exist.
- Concerns: names must not clash with the codes of `sc-issue-protocol` (the coordinator runs the claim) or with `E-NO-GRANT`.

### S04-F8 One lazy-loaded ref per wave under `refs/`
- 655 says: one ref file per wave, loaded only at that wave (ISSUE lines 33 and 62).
- Status: NOT-COVERED
- Current plan: none found; searched: "refs/" (hits are only the existing `sc-issue-protocol` refs and PR 690's `refs/intake.md`, DECISIONS.md:221 and :769), "lazy", "load only" in SPEC and DECISIONS.md.
- Component (NOT-COVERED only): COORDINATOR
- Feature statement (NOT-COVERED only): The coordinator skill keeps its per-wave instructions in separate ref files that the session reads only when it reaches that wave.
- Done when (NOT-COVERED only): `SKILL.md` has no wave body longer than a short pointer, and every pointer resolves to an existing `refs/<name>.md`.
- Depends on: S04-F5, S04-F12 (the file-table test)
- Evidence from our documents: no evidence found in our documents. (W/DECISIONS.md:769 notes the PR 690 `refs/intake.md` table is UNVERIFIED, which concerns plan depth, not this layout.)
- Concerns: the context-size saving is a design aim of 655, not measured anywhere (UNVERIFIED).

### S04-F9 `refs/playbook.md` (the rules the coordinator applies to worker questions and permission prompts)
- 655 says: a playbook ref sits beside the wave refs; wave 5 "applies the playbook and the permission rules" (ISSUE lines 42 and 62; the "playbook (FR-23)" is 655's own FR-23, not the plan's).
- Status: NOT-COVERED
- Current plan: none found; searched: "playbook" (no hit in SPEC, DECISIONS.md, any VERDICT.md, merged-requirements.md). Typing into worker terminals is covered separately by FR-40 (SPEC:242) and D15 D14 (D15:98) but that is a rule set, not a playbook file.
- Component (NOT-COVERED only): COORDINATOR
- Feature statement (NOT-COVERED only): The coordinator skill has a playbook ref that says how to answer a worker's question and when to escalate, and it never tells the coordinator to approve a permission prompt.
- Done when (NOT-COVERED only): The playbook file exists, the file-table test lists it, and a scan finds no instruction in it to approve a prompt or send "always allow".
- Depends on: S04-F8; 655 section 5 (watching, the worker rules FR-23 and FR-24 of 655)
- Evidence from our documents: D15:98 "Reject approving permission prompts (WC:122, WC:137); drop approval rules and test cases". SPEC:242 FR-40 "Type into worker terminals only under the four typing rules (never approve a permission prompt)".
- Concerns: 655 acceptance line 222 says the orchestrator does "typing and approvals included"; that part conflicts with FR-40 and D15 D14 and must not enter the playbook. Mark for the section 5 analyst.

### S04-F10 Stub-first templates in the skill
- 655 says: the skill's templates are "stub-first" (ISSUE line 62): the session writes the file's header first, then fills it.
- Status: NOT-COVERED
- Current plan: none found; searched: "stub", "stub-first", "header first" in SPEC, DECISIONS.md, FOLLOW-UPS.md, merged-requirements.md. The nearest rule is FR-37 (SPEC:239) "Write an escalation or entry first, send nothing if refused", which is about write-before-send, not about a stub.
- Component (NOT-COVERED only): COORDINATOR
- Feature statement (NOT-COVERED only): The coordinator writes each output file (entry, escalation, handoff) as a stub with all headers, then fills sections one by one, so a kill leaves a readable partial file.
- Done when (NOT-COVERED only): A kill test after the stub write leaves a file that a reader labels incomplete and a re-run finishes without a second file.
- Depends on: S04-F20 (the templates), S04-F21 to S04-F37 (each template's content)
- Evidence from our documents: SPEC:239 quote above; no further evidence found in our documents.
- Concerns: the plan insists on kill-and-restart tests at every persistence boundary (FR-29, SPEC:231; S15a, SPEC:499); a stub-first rule must be included in those tests.

### S04-F11 Return contract printed last
- 655 says: the skill prints a return contract as its last output (ISSUE line 62; wave 9 prints it, line 46).
- Status: NOT-COVERED
- Current plan: none found; searched: "return contract", "return-contract" in SPEC, FOLLOW-UPS.md, DECISIONS.md and all VERDICT.md (hits are only the debate runs' own `return-contract.yaml` files, which are not a coordinator feature).
- Component (NOT-COVERED only): COORDINATOR
- Feature statement (NOT-COVERED only): At the end of a run, the coordinator prints one machine-readable return contract that says what was done, what is left and what waits on a person.
- Done when (NOT-COVERED only): A run on a throwaway issue ends with a contract whose fields a test parses; a run that stops early still prints one.
- Depends on: 655 section 2 wave 9; S04-F5
- Evidence from our documents: no evidence found in our documents.
- Concerns: SPEC:228 (FR-26) already sets "one JSON contract" for the verbs; a builder should decide whether the return contract is the same schema (UNVERIFIED; the plan does not say).

### S04-F12 File table in the skill that a test checks in both directions
- 655 says: `SKILL.md` has a file table, and a test checks that every listed file exists and every file in the skill folder is listed (ISSUE line 62).
- Status: NOT-COVERED
- Current plan: none found; searched: "file table", "both directions", "dual surface" in SPEC and DECISIONS.md. Stage S13 extends `tests/skills/test_primitive_dual_surface_lookup.py` (SPEC:497), which is about installed-path lookups, not a file table.
- Component (NOT-COVERED only): COORDINATOR
- Feature statement (NOT-COVERED only): A test fails when a file in `sc-coordinator-protocol/` is missing from the skill's file table or a listed file does not exist.
- Done when (NOT-COVERED only): Deleting a ref, or adding an unlisted file, makes the test fail.
- Depends on: S04-F8
- Evidence from our documents: no evidence found in our documents. (The repo has similar file-table checks elsewhere, for example the swarm tests `tests/swarm/test_contract_surface.py:227`; the existing protocol skills' own check is UNVERIFIED here.)
- Concerns: none.

### S04-F13 Installed paths for any other primitive (no `src/superclaude/` paths inside the skill)
- 655 says: the skill names other primitives by installed path (ISSUE line 62, "repo CLAUDE.md").
- Status: COVERED
- Current plan: NFR-06 (SPEC:344) "installed primitives name only installed paths (MC-9)"; MC-9 (SPEC:478) the grep `grep -rn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks}`; S13 and S14 run MC-9 (SPEC:497-498).
- Depends on: none
- Evidence from our documents: SPEC:344 and SPEC:478 quotes above.
- Concerns: none; the plan keeps the repo rule.

## The twelve verbs and the two modules

### S04-F14 Eleven verbs of `superclaude orchestrator`: `wake-check`, `wake-ack`, `state`, `merge-gate`, `plan-check`, `repos`, `report-entry`, `escalate`, `answer-check`, `audit`, `handback`
- 655 says: the deterministic steps are verbs of `superclaude orchestrator` in `src/superclaude/cli/orchestrator/` (ISSUE line 62).
- Status: COVERED
- Current plan: FR-26 (SPEC:228) "Provide one verb group `superclaude coordinator` (wake-check, wake-ack, state, plan-check, repos, merge, merge-gate, answer-check, audit, report-entry, escalate, handback) with one JSON contract, one state lock and a closed `refuse(argv)` list". The group is renamed (D08, FR-63, SPEC:320). Each verb has its own requirement: merge-gate SEC-02, answer-check SEC-09, audit FR-36, handback FR-35, escalate and report-entry FR-37, FR-48.
- Depends on: none
- Evidence from our documents: D15 R-7 (D15:33) "Verb count: 12 listed at D:510 include `lease` (deferred) and an interrupt option (rejected) and have no merge verb"; SPEC:62 "NOT BUILT anywhere ... `superclaude coordinator` verbs, `merge-gate`, `answer-check`".
- Concerns: the plan adds a `merge` verb that 655 does not have (655 runs `gh pr merge` directly, wave 7); the plan requires one named merge verb (D15 D1, D15:85). The plan also adds one JSON contract and one state lock for the group (FR-26), which 655 does not state. `repos` must read the per-repo config, not the `IronOrchestrator` repo list (registry repo rejected, D15 C5, D15:77).

### S04-F15 Verb `lease`
- 655 says: `lease` is one of the twelve verbs (ISSUE line 62).
- Status: CONFLICT
- Current plan: FR-26 (SPEC:228) "no lease, no interrupt"; OD-8 (SPEC:104) "No lease comment now; reserved with a trigger"; section 7 row C8 (SPEC:456) "C8 lease comment | DEFER ... reserved with trigger (FR-40)"; FR-40 (SPEC:242) "reserve the lease comment (trigger: a second host or user polls; stale-lease rule first; marker `sc:coordinator:lease`)". 655's version is REJECTED for the first build.
- Depends on: none
- Evidence from our documents: D15:80 "C8 | Lease comment (DQ3 layer 4) | Defer | No second host or user polls; a crashed lease wedges an issue and no stale rule exists (G-1)".
- Concerns: the verb count becomes twelve only because the plan has `merge` where 655 has `lease`; a builder must not add `lease` back to hit "twelve". The twelve-verb number in 655 acceptance text is not a plan requirement.

### S04-F16 "No `hold` verb: the poll alone writes the hold label"
- 655 says: there is no `hold` verb, because the poll alone writes the `hold:plan` label (ISSUE line 62; hold rules at line 25).
- Status: CONFLICT
- Current plan: FR-06 (SPEC:196) "Write nothing to GitHub in a poll cycle (NG-2): strip the label writer of PR 686"; D09 and Q03 rows (SPEC:85, SPEC:95) "Replace PR 686's label-writing code with a read-only variant now"; section 7 row A5 (SPEC:443) "`hold:plan` label write | REJECT now; deferred PR". The "no hold verb" half agrees with the plan (FR-26 has no hold verb); the "poll writes the label" half is REJECTED. OA-28b (SPEC:119) lets init create the trigger label once on the owner's chat OK, not the hold label.
- Depends on: 655 section 1 item 3 (the hold, owned by another analyst)
- Evidence from our documents: SPEC:443 "return only with a shown reader, NG-2 amendment, 24-hour shadow run, cron write test".
- Concerns: the plan's hold is a read-only skip (`held_incomplete`, FR-05, SPEC:195) with the label set by a person. Any 655 text or test that expects `hold:plan` on an issue has no source in the plan.

### S04-F17 `limits.py`: the refusal function behind the "may never" list
- 655 says: a module `limits.py` (not a verb) holds the refusal function of section 9 (ISSUE line 62; acceptance line 225 "every line of the "may never" list has a test and passes through `refuse`").
- Status: COVERED
- Current plan: FR-26 (SPEC:228) "closed `refuse(argv)` list with a failing test per pattern" in `tests/coordinator/test_refuse_argv.py`; D15 D8 (D15:92) "Closed "may do" list and `refuse(argv)` with one test per pattern ... N6 (release, tag) becomes an unconditional refusal with no `answer_ref` pass; N7 interrupt removed"; SEC-11 (SPEC:300); stage S13 builds `refuse(argv)` (SPEC:497). The plan does not name the file `limits.py`.
- Depends on: none
- Evidence from our documents: D15:92 quote above.
- Concerns: the list differs from 655's in two places: no interrupt (OD-7, SPEC:103) and tag/publish never passable by a recorded OK (OD-6, SPEC:102; 655 acceptance line 224 says "a release tag or publish needs a recorded human OK"). Also, in the plan `refuse(argv)` binds the verbs only (D15:92 "Binds the verbs only"); U42 (a hook for commands outside the verbs) is UNVERIFIED (D15:260 area). The 655 line 225 "the one interrupt is sent only after its escalation is written" is REJECTED by OD-7.

### S04-F18 `names.py`: the check that no agent or model is named in user-facing text
- 655 says: a module `names.py` implements "the rule that no agent or model is named in anything user-facing" (ISSUE line 62).
- Status: COVERED
- Current plan: FR-37 (SPEC:239) "scan only `report-entry` and `escalate`, after U54"; OD-3 (SPEC:99) "Naming rule scope B: scan only `report-entry` and `escalate`; measure U54 first"; OD-4 (SPEC:100) "A refused mandatory escalation fails open: written, span masked visibly, original logged"; QG2:53 "Build `names_check` as fail open in the coordinator verb group ... (`names.py`)".
- Depends on: S04-F19
- Evidence from our documents: QG2:53 quote above.
- Concerns: the plan's check is narrower and fail-open (see S04-F19); U54 (false refusals over the last 50 titles) must run before the check is switched on (UNVERIFIED until run).

### S04-F19 Naming rule applies to "anything user-facing", including what workers write
- 655 says: no agent or model is named in anything user-facing (ISSUE line 62); the handoff prompt repeats it as "no attribution line that names an agent or a model" (line 66).
- Status: CONFLICT
- Current plan: OD-3 (SPEC:99) scope B; D15 D19 (D15:103) "Defer ... 25 of the last 30 merged PR bodies carry "Generated with" (G-4)"; QG2:12 "Scan only the coordinator's own two writers ... workers' PR bodies keep today's practice". 655's wider scope is REJECTED by default; the owner may still choose scope A or C in chat (OD-3 is open until then).
- Depends on: S04-F18
- Evidence from our documents: QG2:12 "no check can read a worker's PR body before it is written (D:847), 25 of the last 30 merged PR bodies carry "Generated with" ... and ruling 15 is Clay's ruling, not shown to be an owner ruling".
- Concerns: this repository's own commit and PR practice adds attribution lines that name Claude Code (the system attribution rule for commits and PR bodies). A rule that forbids them in worker output would contradict current practice. 655 line 66 carves out "the one commit trailer" only.

## The four templates

### S04-F20 Four templates, each a file with its own test, and a test that every writing or sending step names its template
- 655 says: four template files (handoff prompt, report entry update, escalation, worker check-in); "each file with its own test; each step that writes or sends names its template, and a test checks that" (ISSUE lines 64 and 53; acceptance line 220).
- Status: NOT-COVERED
- Current plan: none found for the general rule; searched: "template", "templates/", "names its template" in SPEC, DECISIONS.md, FOLLOW-UPS.md, all VERDICT.md files and merged-requirements.md. Partial neighbours: QG2:17 keeps "the offline scan of every template, fixture and end-to-end body" (for the naming rule only) and FR-47 (SPEC:258) keeps an "exactly nine rows" test for the escalation table.
- Component (NOT-COVERED only): COORDINATOR
- Feature statement (NOT-COVERED only): The coordinator skill ships four template files, each with a test, and a test fails when a step that writes or sends a message does not name one of them.
- Done when (NOT-COVERED only): Removing a template file, or adding a sending step with no template name, fails a test.
- Depends on: S04-F12 (file-table test), S04-F21, S04-F32, S04-F34, S04-F37
- Evidence from our documents: QG2:17 "The offline scan of every template, fixture and end-to-end body, and the fake `launch.effective` test, stay".
- Concerns: none.

### S04-F21 Handoff prompt template: a coordinator-owned prompt for the worker's first message, carrying the launch marker
- 655 says: `templates/handoff-prompt.md` is the task spec of `worker-start` (ISSUE lines 64 to 66 and 71).
- Status: COVERED
- Current plan: FR-30 (SPEC:232) "marker `[sc-launch:v1:<nonce>]` in the first prompt (restored `brief.py`)"; FR-61 (SPEC:282) "Hand the `--pipeline none` worker a chain from the coordinator's own template that names the filed plan"; D12 (D15:96) one supervised `worker-start` route. The plan does not say whether the carrier is a file named `handoff-prompt.md` or the restored `brief.py` with its template.
- Depends on: S04-F20
- Evidence from our documents: W/brainstorm/run/merged-requirements.md:305 (K3) "The restored `brief.py` ... is the one builder of the worker's first prompt; there is no second `handoff-prompt.md`", against W/debates/D05/VERDICT.md:20 "a new line in Clay's `templates/handoff-prompt.md`". After PR 700 the old package is back on master (SPEC Appendix B.1), so `brief.py` exists again; the old tests are golden briefs with "one marker line" (W/techref/ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md:2394).
- Concerns: UNVERIFIED which carrier wins (K3 vs D05; SPEC FR-30 says `brief.py`; which verb exposes `brief.build` is checked at S6, SPEC:671). 655's nine sections have no launch-marker line; FR-30 needs one. SEC-17 (SPEC:306) says marker-bearing text must never reach a coordinator session.

### S04-F22 Handoff prompt has nine sections in a fixed order (issue link, repo, worktree and base branch; goal; Orca task-spec fields; do-not-touch rules; reporting duties; stop condition)
- 655 says: nine sections in this order: (1) issue link, repo, worktree, base branch; (2) goal; (3) plan sections; (4) Orca task-spec fields (target, change, constraints, ownership, observable acceptance); (5) do-not-touch and safety; (6) SC command chain; (7) never merge, never force-push; (8) reporting duties; (9) stop condition (ISSUE line 66). Rows (3), (5), (6), (7), (8) and parts of (9) are classified in S04-F23 to S04-F31.
- Status: NOT-COVERED
- Current plan: none found for the section list or order; searched: "nine sections", "handoff", "task-spec", "task spec", "target, change", "stop condition", "observable acceptance" in SPEC, DECISIONS.md, all VERDICT.md files, merged-requirements.md and both techrefs (only `brief.py` golden tests and the marker line appear).
- Component (NOT-COVERED only): COORDINATOR
- Feature statement (NOT-COVERED only): The worker's first prompt is built from one template with fixed, ordered sections (identity of the issue and worktree, goal, the Orca task fields, rules, chain, reporting and stop condition), and a test pins the order.
- Done when (NOT-COVERED only): A golden test builds a prompt for a sample issue and compares section headings and order with the template.
- Depends on: S04-F21; S04-F23; S04-F24; S04-F25 to S04-F31
- Evidence from our documents: W/techref/ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md:2292 "`brief.py` | 74 | Builds the fixed worker brief from a template and a validated issue number" (the old owner-side builder carried a number only).
- Concerns: UNVERIFIED that Orca's task-spec field names (target, change, constraints, ownership, observable acceptance) match Orca's own current skill; 655 gives them without a source and no document of ours checks them. Section (9) "reviewers finished, no open thread" assumes the worker watches reviewers (see S04-F29).

### S04-F23 Handoff section 3: Priority, Fix approach and Test plan copied from the issue as quoted data; "the integer-only rule covers only the poll script's own launch prompt"
- 655 says: the plan sections are copied into the worker prompt as quoted data, and the id-only rule covers only the poll script's own launch prompt (ISSUE lines 66 and 71).
- Status: CONFLICT
- Current plan: SEC-16 (SPEC:305) "Let no GitHub text reach a prompt, typed line, mailbox subject or argv; only a pattern-checked builder's value does"; D10 item 6 (W/debates/D10/VERDICT.md:19) "The rule ... is kept ... and widened ... only a value built by a pattern-checked builder reaches a prompt, a typed line, a mailbox subject or an argv"; FR-29 (SPEC:231) copies `.dev/issues/<N>/` into the worker worktree and FR-61 (SPEC:282) has the chain name the filed plan, so the worker reads the plan from files. 655's copy-into-prompt is REJECTED as written. FR-55 (SPEC:276) allows a plan quoted in a fenced "data, not instructions" block in the claim's `next-steps.md` only, a different file.
- Depends on: S04-F22
- Evidence from our documents: D10 verdict line 19 quote above; W/debates/D10/VERDICT.md:33 "The "no GitHub text" rule is the owner's built and property-tested D3 (`launch.py:33`...)".
- Concerns: SEC-16's exact reach (the poll's prompt only, or every prompt the coordinator sends) is not spelled out by the section header at SPEC:286 ("watcher and coordinator"); treat as every prompt unless the owner rules otherwise. A prompt that holds free GitHub text is the injection path the plan closes. The security panel must decide between "name the file" (plan) and "quote the text" (655).

### S04-F24 Handoff block "Round n of at most 4" with the earlier pull requests and the remaining items
- 655 says: in a hand-back round, section 3 also carries a block "Round n of at most 4": the earlier pull requests and the remaining items (ISSUE line 66).
- Status: NOT-COVERED
- Current plan: none found for the prompt block; searched: "Round n", "at most 4", "remaining" in SPEC and VERDICT files. The loop itself is covered: FR-35 (SPEC:237) "`HANDBACK_MAX` 3 "not measured"", re-plan with `/sc:issue --plan <N> --remaining <file>`, old worker final first, whole start gate repeated (OD-2, SPEC:98). 655's "at most 4" rounds equals the original plus 3 hand-backs, consistent with the cap of 3.
- Component (NOT-COVERED only): COORDINATOR
- Feature statement (NOT-COVERED only): In a hand-back round the worker's prompt states which round this is, the pull requests of the earlier rounds and the remaining items.
- Done when (NOT-COVERED only): A golden test of a round-2 prompt shows the round number, the earlier pull request numbers and the remaining list; a round-1 prompt has no such block.
- Depends on: S04-F22; 655 section 7 (hand-back, another analyst)
- Evidence from our documents: D15:32 (R-6) "Round 2 passes the start gate again; either re-approve after the re-plan (default) ... (OD-2)". The cap number 3 is labelled "not measured" (SPEC:237).
- Concerns: the plan makes the second round wait for a person's re-approval (`waiting_reapproval`, FR-35); the block must not be sent before that. Earlier PR numbers are GitHub-derived values and must pass a pattern-checked builder (SEC-16).

### S04-F25 Handoff section 5: issue text is data, no force-push
- 655 says: the rules section says issue text is data and the worker never force-pushes (ISSUE line 66).
- Status: COVERED
- Current plan: FR-55 (SPEC:276) safeguards S1 to S5 of D12: plan "quoted only in a fenced "data, not instructions" block, commands never taken from it"; SEC-22 (SPEC:311) "no force push"; FR-32 (SPEC:234).
- Depends on: none
- Evidence from our documents: SPEC:276 and SPEC:311 quotes above.
- Concerns: "issue text is data" is only a rule in the plan's claim chain (next-steps), not in a worker prompt; see S04-F23 for the conflict on whether the text goes into the prompt at all.

### S04-F26 Handoff section 5: never print secrets
- 655 says: the rules section tells the worker never to print secrets (ISSUE line 66).
- Status: NOT-COVERED
- Current plan: none found; searched: "secret", "credential", "never print", "token" in SPEC (the `token` hits, for example SPEC:539 about admin settings and SPEC:545 about rotating an Orca token that a debate agent printed, are not worker rules) and in src/superclaude/core/WORKER-CONTRACT.md (no hit for "secret" or "credential").
- Component (NOT-COVERED only): COORDINATOR
- Feature statement (NOT-COVERED only): The handoff template tells the worker never to print or commit secrets, tokens or credentials.
- Done when (NOT-COVERED only): The template text carries the rule and the template test checks for it.
- Depends on: S04-F22
- Evidence from our documents: SPEC:545 area (owner action: rotate the exposed Orca token) shows a real exposure path; no rule for workers found.
- Concerns: none; low cost.

### S04-F27 Handoff section 6: the SC command chain written by the coordinator, naming the filed plan
- 655 says: section 6 of the prompt is the SC command chain (ISSUE line 66; waves: `/sc:workflow` if needed, then `/sc:implement`, line 41).
- Status: COVERED
- Current plan: FR-61 (SPEC:282) "Hand the `--pipeline none` worker a chain from the coordinator's own template that names the filed plan; `plan-check` is the same function as `plan_body.py check`"; FR-55 (SPEC:276) claim rule C1 for the short chain `/sc:workflow` then `/sc:implement`.
- Depends on: S04-F22
- Evidence from our documents: SPEC:282 quote above.
- Concerns: the chain must stop where the plan stops: `/sc:pr-submit` is not part of it (see S04-F29).

### S04-F28 PR body names the issue by `Fixes <repo>#<number>` only when the pull request fully addresses it, else `Refs <repo>#<number>` (ruling 38)
- 655 says: the PR body keyword rule is part of handoff section 6 (ISSUE line 66; ruling 38, line 155).
- Status: NOT-COVERED
- Current plan: none found for the rule; searched: "Fixes", "Refs", "ruling 38", "fully addresses" in SPEC, DECISIONS.md, all VERDICT.md files, merged-requirements.md. The plan only treats the risk: SEC-12 (SPEC:301) "state that a `Fixes` line still closes at merge"; RK-10 (SPEC:654) "Closeout or a `Fixes` line closes unfinished work".
- Component (NOT-COVERED only): COORDINATOR
- Feature statement (NOT-COVERED only): The text that opens the pull request uses `Fixes` only for a pull request that fully addresses its issue and `Refs` otherwise, so a partial pull request cannot close the issue at merge.
- Done when (NOT-COVERED only): A test of the template and of the PR body check shows a partial pull request carries `Refs`; a throwaway merge of a `Refs` pull request leaves the issue open.
- Depends on: S04-F22; 655 section 7 (closeout and hand-back, another analyst)
- Evidence from our documents: W/DECISIONS.md:909 "A `Fixes` line in the PR body still closes the issue at merge with no coordinator write"; W/debates/D15/VERDICT.md:143 "the `Fixes` line bypass is stated as a limit".
- Concerns: in the plan the pull request is opened by a person's typed `/sc:pr-submit --monitor 3` run (SEC-22) and a worker never runs it (SEC-05), so a prompt line alone does not reach the PR body. The rule must live where the body is written (the pr-submit template or a body check). UNVERIFIED who writes the body under the plan.

### S04-F29 Handoff sections 6 to 9: the worker pushes its own branch, opens its pull request and runs the review loop to "green, reviewers finished, no open thread"
- 655 says: after implementation the worker runs `/sc:pr-submit --monitor 3` (ISSUE line 41), pushes and opens its PR (acceptance line 223), and its stop condition is green, reviewers finished, no open thread (line 66, section 9).
- Status: CONFLICT
- Current plan: SEC-05 (SPEC:294) "Never run `/sc:pr-submit` or `/sc:closeout` as a `worker-start` worker."; FR-32 (SPEC:234) the coordinator commits after `worker_done` and "push the worker commits only on a typed go ... the coordinator never types it"; SEC-22 (SPEC:311) the person's typed run line is the go for that run's pushes; D15 D11 (D15:95) "a worker never runs `/sc:pr-submit`". 655's version is REJECTED.
- Depends on: 655 section 2 wave 4 (chain) and section 5
- Evidence from our documents: src/superclaude/core/WORKER-CONTRACT.md:41 "never pushes"; D15:95 "ADD1's worker runs `/sc:pr-submit` ... worker route: reject".
- Concerns: the stop condition in 655 (reviewers finished, no open thread) belongs to the pull request watch (wave 6), which the plan keeps with the coordinator's `merge-gate` (D06). If this prompt is copied, the worker would push and open a PR with no person's go and no guard binding.

### S04-F30 Handoff section 7: never merge, never force-push
- 655 says: the prompt tells the worker never to merge and never to force-push (ISSUE line 66).
- Status: COVERED
- Current plan: SEC-01 (SPEC:290) merge only on a person's typed go; SEC-02 (SPEC:291) never `--auto`, `--admin`; SEC-22 (SPEC:311) "no force push"; FR-32 (SPEC:234).
- Depends on: none
- Evidence from our documents: SPEC:290 and SPEC:311.
- Concerns: SEC-13 (SPEC:302) says a worker's own script can still push a feature branch or, on one shared admin login, `gh pr merge --admin`; a prompt line narrows this and does not close it.

### S04-F31 Handoff section 8: reporting duties (preamble IDs, heartbeat, `ask`, `worker_done`)
- 655 says: the prompt names the worker's reporting duties (ISSUE line 66).
- Status: COVERED
- Current plan: D12 (D15:96) one supervised `worker-start` route "mailbox, one message handled once per id, check-ins, restart"; SEC-20 (SPEC:309) "a bound worker's `send` and `ask` are one plain call, no `--to`"; the existing contract src/superclaude/core/WORKER-CONTRACT.md:7 says the Orca dispatch preamble is the authority for verb syntax and heartbeat cadence and the file never copies them.
- Depends on: none
- Evidence from our documents: WORKER-CONTRACT.md:7 "The dispatch preamble that Orca gives each worker is the authority for Orca verb syntax and heartbeat cadence."
- Concerns: the plan does not put a reporting section into the prompt; the contract and the Orca preamble carry it. 655's wording must not copy Orca's syntax into the prompt (the contract says it never does).

## Report entry, escalation and check-in templates

### S04-F32 Report entry update template that follows the work report's item template
- 655 says: `templates/report-entry-update.md` follows the work report's item template; written at claim and at the milestones of section 7 (ISSUE line 67).
- Status: COVERED
- Current plan: D15 E5 (D15:113) "Plain-English item template | Adopt with change ... Generic wording"; D15 E7 (D15:115) `report-entry` as the one writer; FR-48 (SPEC:259) "Make `report-entry` the only writer of an entry file"; FR-46 (SPEC:257) store only `session_id` in entry files.
- Depends on: S04-F20; 655 section 7 (when entries are written)
- Evidence from our documents: SPEC:259 quote above; SPEC:778 (Appendix B.2) "FR-45, FR-46, FR-48 ... blocked until the skill is restored (they stay requirements)".
- Concerns: the work report skill (`agent-work-report`) was removed from master by PR 700 (SPEC:777); the item template it holds is not on master until the owner decides to restore it from the archive branch (SPEC Appendix B.3 item 1). This template cannot be built against the item template until then. The plan has no "at milestones only" cadence; that rule is for the section 7 analyst.

### S04-F33 Report entry fields: human assignee, session links, follow-up state, last update, PR and CI state
- 655 says: the entry "shows the assignee, the session links, the follow-up state, the last update, the PR and CI state" (ISSUE line 67).
- Status: NOT-COVERED
- Current plan: none found for this field list; searched: "assignee", "follow-up state", "last update", "CI state", "milestone" (no hit) in SPEC, DECISIONS.md and all VERDICT.md files. The plan lets the observer show entry fields only from an owner-named allowlist, which the owner has not filled: FR-80 (SPEC:263) and stage S16 (SPEC:500) "owner fills the FR-80 allowlist and cap"; OA-17a (SPEC:116).
- Component (NOT-COVERED only): COORDINATOR (writes the fields; the dashboard reads them under FR-80)
- Feature statement (NOT-COVERED only): `report-entry` writes the five fields into each entry through the template, and the owner's allowlist names which of them the dashboard may show.
- Done when (NOT-COVERED only): An entry file for a test issue holds the five fields; the observer shows exactly the allowlisted ones.
- Depends on: S04-F32; FR-80 allowlist (owner action)
- Evidence from our documents: SPEC:263 "Show observer entry fields only from an owner-named allowlist, never `recommend` or `suggested` (model-written ...)".
- Concerns: `recommend` and `suggested` are model-written and never shown (FR-80); keep them out of the template. FR-46 stores only `session_id`, so a "session link" is built at read time, not stored.

### S04-F34 Escalation template: the nine rows with old rule numbers, and the lines `Why this reaches you:`, `Low-stakes options:`, `If you do not answer:`
- 655 says: `templates/escalation.md` holds the nine rows of section 9 with their old rule numbers and three named lines (ISSUE line 68).
- Status: COVERED
- Current plan: D15 D16 (D15:100) "Nine-row "what reaches the person" table, entry shape lines, "if you do not answer" waits, no default | Adopt with change ... keep the "exactly nine rows" test; owner decision"; FR-47 (SPEC:258) "Use the nine-row table in the notice step only ("the person"; exactly nine rows)"; FR-37 (SPEC:239) write the entry first; D20 (D15:104) an answer is always typed.
- Depends on: S04-F20
- Evidence from our documents: D15:100 quote above; W/debates/D06/VERDICT.md:61 lists "nine-row list" among open owner decisions.
- Concerns: the nine rows are adopted subject to an owner decision (D06 item 11); the wording "Clay" must read "the person" (D15:100); a refused mandatory escalation still writes, fail-open (OD-4, SPEC:100). The sweep and the observer never pick a row (D15:100).

### S04-F35 Escalation reaches the person "in three ways": issue-entry lines, an Orca decision gate, and the notice
- 655 says: the template names the three ways it reaches the human (ISSUE line 68; line 137 lists "lines of the issue's own entry, an Orca decision gate, and the notice"; notices capped at `reach_daily_max`, 5 per repo per 24 hours).
- Status: CONFLICT
- Current plan: for the notice: OA-25a (SPEC:113) "No push notice in the first build; a waiting PR is shown with the age of the wait"; SEC-21 (SPEC:310); FR-49 (SPEC:260) "reserve a push notice until the owner asks with a cap number, a sender is built and tested"; D15 D17 (D15:101) cap key default 0, "no generator writes 5". The entry-line way is COVERED (FR-49, QG2 OD-5 at QG2:14). 655's notice way is REJECTED for the first build.
- Depends on: S04-F36
- Evidence from our documents: QG2:14 "entry lines only in the first build, with a reserved notice ... none exists in master, pr-a or pr-p".
- Concerns: the cap of 5 is "ruling 39", which our debates treat as Clay's, not the owner's (W/debates/OAG1/VERDICT.md:37). A builder must write the template with the notice line absent or inert until the three triggers hold.

### S04-F36 Orca decision gate as a channel to the person
- 655 says: one of the three ways an escalation reaches the human is an Orca decision gate (`gate-create`, `gate-resolve`) (ISSUE lines 42, 44 and 137).
- Status: NOT-COVERED
- Current plan: none found; searched: "gate-create", "gate-resolve", "decision gate" in SPEC, DECISIONS.md, all VERDICT.md files and merged-requirements.md (one hit, a verb inventory row in W/techref/OBSERVER-SWEEP-DASHBOARD-TECHNICAL-REFERENCE.md:976 that lists `gate-create/resolve` among Orca verbs).
- Component (NOT-COVERED only): COORDINATOR (creates the gate); TUI-DASHBOARD would show it
- Feature statement (NOT-COVERED only): An escalation can open an Orca decision gate for the person, and the coordinator treats the gate's resolution as an answer only after `answer-check`.
- Done when (NOT-COVERED only): A throwaway escalation opens a gate; resolving it in Orca is accepted as an answer only if `answer-check` confirms a person typed it for the right question and head.
- Depends on: S04-F34; 655 section 9
- Evidence from our documents: SPEC:297 (SEC-08) "typed by a person in their own session, never relayed"; D15:104 (D20) "An answer is always typed".
- Concerns: a gate resolved in the Orca interface may not satisfy SEC-08 (typed in live chat, never relayed); UNVERIFIED how Orca records who resolved a gate. The owner's rule "approvals through chat, never files" also applies. Treat the gate as a display channel until the owner rules.

### S04-F37 Worker check-in template: the status message and the fields of the answer
- 655 says: `templates/worker-checkin.md` holds the status message the coordinator sends a worker (hourly) and the fields of the worker's answer (ISSUE line 69; waves line 42).
- Status: NOT-COVERED
- Current plan: none found; searched: "check-in", "checkin", "hourly", "status message", "worker status" in SPEC, DECISIONS.md, all VERDICT.md files and merged-requirements.md. Only D12 (D15:96) lists "check-ins" as one part of the supervised route with no format, and `--hourly` is a flag (FR-24, SPEC:226). Typing into worker terminals is bound by FR-40 (SPEC:242) and D15 D14 (D15:98).
- Component (NOT-COVERED only): COORDINATOR
- Feature statement (NOT-COVERED only): The coordinator sends each running worker an hourly status request from one template and reads the worker's answer from fixed fields.
- Done when (NOT-COVERED only): A test of the template shows the request carries only ids and fixed text (no GitHub text), and a worker answer missing a field is treated as no answer.
- Depends on: S04-F9 (playbook and typing rules); S04-F20; 655 section 5
- Evidence from our documents: D15:98 "Reject approving permission prompts (WC:122, WC:137)"; SPEC:242 FR-40 "never interrupt a worker".
- Concerns: the status message is typed or sent into a worker's session, so it falls under FR-40's four typing rules and SEC-16 (no GitHub text in a typed line). 655 acceptance line 222 says the check-in includes "approvals"; that part is REJECTED (D15 D14). The "Monday to Friday, 24 hours" schedule in line 222 has no source in the plan (UNVERIFIED).

## Delivery

### S04-F38 The skill lands as one pull request after T1 to T13 pass, with their results in its description
- 655 says: "The skill lands as one pull request after T1 to T13 pass, with their results in its description" (acceptance line 217).
- Status: CONFLICT
- Current plan: section 8 rules (SPEC:474) "one reviewable PR" per stage and "a stage never enables a later one"; S13 substrate (SPEC:497), S14 merge path with the command and skill (SPEC:498), S15 four PRs a to d (SPEC:499), S17 live tests last (SPEC:501); D15 G1 (D15:129) adopts the tests T1 to T13 with change, at order O4 to O7. 655's single PR after all tests is REJECTED: the plan builds in stages and runs the live tests at S17, after the code lands.
- Depends on: 655 section 13 (work split, another analyst)
- Evidence from our documents: SPEC:503 "S17 does not include raising the cap, Pipeline-field governed launches, label writes ...; those are separate future changes."
- Concerns: the plan's T1, T3, T4, T8, T10, T11 logic is rewritten and T12 is rewritten for the hand-back (SPEC:467); 655's T-list cannot be used as it stands.

## Section summary

- 38 features: the command, flags, skill name, verbs, `limits.py`, `names.py`, installed-path rule and the escalation and report-entry templates are covered by FR-24, FR-26, FR-37, FR-47, FR-48, D08, D15 and NFR-06 (under the coordinator name).
- Seven parts of 655 are rejected: the `lease` verb, the poll writing the hold label, the naming rule reaching worker output, issue text quoted into the worker prompt, the worker pushing and running `/sc:pr-submit`, the push notice as a third way to reach the person, and landing the skill as one PR after all live tests.
- The structural rules of the skill (Activation, waves with refs, STOP code table, playbook, stub-first, return contract, file table test) and the content of the handoff, check-in, report-entry fields, `Fixes`/`Refs` rule and decision-gate channel are not in the plan; they go to the COORDINATOR backlog. None belongs to the WATCHER.
- Builders must not copy 655's handoff text as it stands: sections 3, 5 (attribution line), 6 and 9 collide with SEC-16, QG2 OD-3, SEC-05, FR-32 and SEC-22. Open points marked UNVERIFIED: which file carries the handoff prompt (`brief.py` or `handoff-prompt.md`), Orca's task-spec field names, and who writes the PR body under the plan.
- Dependency on PR 700: the report-entry template needs the `agent-work-report` item template, which is off master until the owner decides to restore it (SPEC Appendix B.3 item 1).


