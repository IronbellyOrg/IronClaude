# CONSENSUS (bmad-planner = agent 1, ic-planner = agent 2)

STATUS: Round 3 text complete for (a) to (g) and the deliverables list (2026-11-22). Agent 2 has signed; agent 1's signature is the last open line. Nothing below is agreed by the agents until both signatures at the bottom are filled. Positions: agent1/RELEASE-PLAN.md S5.1 (agent 1) and agent2/IRONCLAUDE-SIDE.md (agent 2).

Each topic states: decision, owner of each step, division of labour, deliverables BMAD planning must produce, open disagreements (if any) and each agent's reason.

## (a) When a BMAD user story is handed to IronClaude, and the hand-off contract
DRAFT by agent 1 (2026-11-22), from messages 02 and 03. Items marked AGREED were accepted by both agents in writing; PENDING items wait for the other agent's reply.

**Decision (AGREED, D1).** The hand-off unit is a FEATURE (2 to 6 ready stories: one PRD feature group, one GitHub feature sub-issue). The planning and execution unit inside IronClaude is a STORY (one `/sc:workflow` run, one plan package, one ledger per story). The worktree and the PR are per feature (one PR per feature, from a worktree based on `origin/master`; owner decision O4 confirms). Stories of a feature run in order in that one feature worktree.

**When.** After, and only after: `/bmad-check-implementation-readiness` passed for the epic, `/bmad-sprint-planning` lists the story at `backlog`, the story has numbered criteria `S<N>.<M>-AC<n>`, the packet folder is built, and the owner has said go in chat (H1.1 to H1.9, IRONCLAUDE-SIDE.md 3.2). BMAD does NOT run `bmad-create-story`, `bmad-dev-story`, `bmad-code-review` for these stories (AGREED).

**The contract (the packet).** A FOLDER `.dev/issues/<feature-issue>/bmad/` (AGREED shape; location subject to owner decision O2): `INDEX.md` (feature level) plus one self-contained `story-<N>-<M>-<slug>.md` per story. Templates: `agent1/templates/handoff-packet.md` (v2). Each story file carries: the story and its acceptance criteria verbatim with stable ids, the `AD-n` rows that bind it, constraints and out-of-scope (headings `## Constraints` and `## Out of scope`, which `/sc:implement` treats as global constraints), paths touched or "new area", type and complexity by the repo rubric, dependencies, previous-story notes, and an empty "IronClaude execution" section.

**Who accepts.** The IronClaude coordinator runs H1 and writes `status: accepted` or `status: rejected: <failing row>` in INDEX.md. A rejection returns to BMAD; IronClaude never repairs criteria (AGREED).

**Owner of each step.**

| Step | Owner | Attended? |
|---|---|---|
| Brief, research, PRD, UX, architecture, SPEC, epics and stories, readiness, sprint planning | BMAD (person in a BMAD session) | yes (no headless for epics and stories) |
| Document-level independent review before stories are cut | BMAD side (`/sc:spec-panel` on SPEC.md as a gate, or BMAD review skills) | worker or person |
| Build the packet folder from the epics file | BMAD-side person (v0 by hand; no script before the first trial, D5 AGREED) | yes |
| Intake check H1, accept or reject | IronClaude coordinator | no |
| Per story: spec panel, plan, plan approval, implement | IronClaude (workers under coordinator; implement run by a person until it has an unattended mode, PENDING build B4) | partly |

**Deliverables BMAD must produce per feature:** the approved epics-file stories with criteria ids; the readiness report; the `sprint-status.yaml` entries; INDEX.md; one story file per story; one story-issue description per story. For stories that carry an open design question: the question, the options BMAD considered.

**D7 (AGREED in message 04).** No `/sc:design` by default; added only when INDEX marks "Design question open: yes", then the existing medium or complex chain applies. A story that creates a new interface or schema with no BMAD design is a Spec Gap Report ("design missing") to BMAD, not an IronClaude design; a design result that differs from an `AD-n` returns as a change request through `bmad-correct-course`.

**Open.** Owner decision O2 (packet location and tracking) and H1.9 (owner's go) are the owner's.

Agent 1's reason: the BMAD story is already the unit of acceptance and status, and a story-sized plan gives a clean ledger per story; the feature unit keeps BMAD's feature group intact for review, worktree and PR.
Agent 2's reason: `/sc:workflow` takes exactly one source and snapshots only it, so each story file must be self-contained (`_bmad-output/` is untracked per clone and absent from a new worktree); a plan per story gives one ledger per story (write-back reads one `progress.md`), failure isolation, and avoids relying on story-id tokens surviving a batch plan (UNVERIFIED). Agent 2 agrees with the decision, the timing and the acceptance rule as written. Agent 2 note: H1.8 (the story issue exists) is met by `/sc:issue --create` at hand-off; that command sets the Complexity field from its `--depth` flag (quick = Simple, standard = Medium, deep = Complex; `~/.claude/skills/sc-issue-protocol/refs/labels.md`), so the filing command line must pass the `--depth` that matches the complexity class in the story file.

## (b) Who writes the spec or PRD, and the default

**IronClaude position (agent 2), Round 2 draft.** Full text: `agent2/IRONCLAUDE-SIDE.md` section 4; the brainstorm run behind it: `agent2/brainstorm-b/merged-requirements.md` (quick depth, convergence 0.654 against 0.75, so not fully converged; its two proposals and mine reach the same default, which is weak evidence: same kind of model, topic file written by agent 2).

**Decision proposed.** BMAD owns the PRD, the architecture, the epics and the stories. The BMAD story (packet story file) is the spec; IronClaude reviews it once with `/sc:spec-panel` and plans from it. IronClaude writes its own code-grounded spec (`/sc:brainstorm`) and merges it with the story (`/sc:adversarial --compare`) only for a story where a trigger fires.

**Triggers (checked by the coordinator without a script; the list is frozen during a trial release):** S1 a path the story names is missing at HEAD, or the story names no paths; S2 the named paths drifted since the story was written (starting guess: 3 commits, UNVERIFIED); S3 complexity is complex by the repo rubric, or the story changes stored data shape or a protocol; S4 the panel reports a blocking finding on code facts (Dev Notes, constraints, tasks), not on criterion text.

**Merge rules for the alternate arm:** BMAD acceptance criteria are a floor (never renumbered, dropped or reworded except through a logged row with evidence, status `proposed` until the coordinator or owner approves); IronClaude-added criteria are `[IC-n]` in a separate list; the adversarial output is an input, never the spec; a factual conflict is settled for the code and logged; a normative conflict or an `AD-n` conflict goes to BMAD as a Spec Gap Report and the story waits.

**`/sc:design`:** not in the chain by default; only when the packet INDEX marks "Design question open: yes" (agreed with agent 1, D7). A story that needs a new interface with no BMAD design is a Spec Gap Report, not an IronClaude design.

**Document-level review** (PRD, architecture, epics, SPEC) is BMAD's gate (BMAD review skills; `/sc:spec-panel` on `SPEC.md` first). It is not repeated per story.

**Trial.** A plan-only pilot first (pilot candidate: issue 706 item 6, scale tests; `agent2/IRONCLAUDE-SIDE.md` section 10.4), then a trial release measuring per story: path taken, triggers fired, calls and minutes per step, conflicts missed by the default arm, criteria lost, escalations. No scripts (`story-gate`, `ac-map-check`) are built before the trial; both agents agree.

**BMAD position (agent 1), 2026-11-22.** Agreed with the IronClaude text above, with these additions from the BMAD side:
1. The default is BMAD-only. Evidence for a mandatory document-level review before stories are cut: issue 409's BMAD set needed 63 blocking fixes in review (`.dev/issues/409/bmad/handoff-step5.md`). So the order is: BMAD document skills, then an independent review of the SPEC (`/sc:spec-panel @SPEC.md` first; BMAD's own `/bmad-review-adversarial-general` and `/bmad-review-edge-case-hunter` may add), then `bmad-create-epics-and-stories`. The story-level panel afterwards checks the story as written for execution, not the documents again.
2. Dual authorship at the DOCUMENT level (not story level) remains for one case: where the owner's own text asks for IronClaude's help in planning, that is `/sc:brainstorm ... --depth deep` in EPIC-01 features 4 and 6 (attended; the output is an input to `bmad-architecture`; BMAD decides). EPIC-05 is a decision record and uses no dual authorship.
3. Criteria added by IronClaude in the alternate arm (`[IC-n]`) are reported to BMAD in the story record and at the retrospective; BMAD may adopt one by appending the next `S<N>.<M>-AC<n>` through `bmad-correct-course`. IronClaude never appends to BMAD's numbering itself. (Agent 2 confirms, 2026-11-22: IronClaude never appends to BMAD's numbering; BMAD adopts an `[IC-n]` criterion only through `bmad-correct-course`.)
4. The trial starts with the plan-only pilot on issue 706 item 6; the story must first be written in BMAD form by a person in a BMAD session (a pilot needs a real story file, not a summary).

**Open disagreements:** none between the agents so far; the thresholds are guesses to be set with the owner after the pilot. Point 3 above is confirmed by agent 2.

## (c) How progress flows back into the BMAD plan and the GitHub epics and sub-issues
DRAFT by agent 1 (2026-11-22). Source: IRONCLAUDE-SIDE.md section 5 and messages 02, 03.

**Decision (AGREED in principle).** Workers never write progress. The coordinator is the single writer to BMAD and GitHub, and writes only from machine-written files it has read (ledger `progress.md`, `return-contract.yaml`, PR and closeout results). Events E0 to E10 and where each is read are in IRONCLAUDE-SIDE.md 5.2.

**BMAD write-back (AGREED, D3).**

| Event | `sprint-status.yaml` | BMAD story record |
|---|---|---|
| packet accepted | story `ready-for-dev` (meaning "packet accepted") | none |
| first implement task started | story `in-progress`; epic lifts from `backlog` | none |
| implemented and reviewed | none | coordinator writes `{implementation_artifacts}/<story_key>.md` from `agent1/templates/story-record.md` |
| PR opened | `review` | update Status |
| PR merged, closeout done | `done` | update Status |
| all stories of the epic `done` | epic `done` set by the coordinator (BMAD sets it manually per its state machine) | none; `/bmad-retrospective` is the next BMAD step |

Rules, from `bmad-quick-dev/sync-sprint-status.md` (read in full by agent 1): idempotent; never regress (`review` is later than `in-progress`, `done` later than both); epic lift only when the target is `in-progress`; refresh `last_updated`; preserve comments and STATUS DEFINITIONS. A script copying these rules is build item B6 (P1); until it exists the coordinator edits the YAML by hand under the same rules.

**Why the story record is needed (verified by agent 1):** `bmad-retrospective` reads each story's file and extracts the sections Dev Notes, Review, Lessons Learned and Technical Debt (SKILL.md line 241 onward); `bmad-create-story` reads the previous story's Dev Agent Record. `bmad-sprint-status` reads only the YAML.

**GitHub side.** One progress comment per story issue, edited in place with a marker comment (IRONCLAUDE-SIDE 5.3, marker name proposed by agent 2), no free text from workers. The feature issue gets one comment per finished story. GitHub's own sub-issue counter (`sub_issues_summary`, read on issues 727 and 609) gives the roll-up bar for epics and features.

**Ledger home (AGREED in substance, D2).** One `sprint-status.yaml`, in the release (planning) worktree, written only by the coordinator; tracked in git so that it survives and other clones can read it. Feature worktrees never need it. Owner decision O2 settles tracking and the packet location.

**Open.** Marker name; whether BMAD tooling accepts a story record written this way (a trial item, UNVERIFIED); whether a second writer race exists between `bmad-sprint-planning` re-runs in a planning session and the coordinator's edits (small, a trial item).

Agent 2 note on (c): agrees with the table and the rules. Two additions. (1) Every write here is the coordinator's and each needs the owner's instruction naming it (WORKER-CONTRACT "Git and GitHub ownership"): editing the tracked `sprint-status.yaml` is a file edit in the release worktree, but committing it, posting or editing the GitHub progress comment, and mirroring the Project Status are outward or git actions; owner decision O6 is the standing instruction. (2) The table lists the BMAD writes only; the coordinator also reads halts and spec defects (events E6 and E10 in IRONCLAUDE-SIDE.md 5.2): a halt freezes the story and no BMAD status changes until the owner's Ruling or a BMAD answer to the Spec Gap Report.

## (d) How the coordinator drives BMAD work versus IronClaude work (worktrees, sessions, sequential or parallel)

DRAFT by agent 2 (ic-planner), Round 2. Full reasoning and file facts: `agent2/IRONCLAUDE-SIDE.md` sections 6 and 7.

**Decision.** One release coordinator (a session the owner opens, one Orca Run per release) drives IronClaude work in Mode C: it plans each story's Tasks itself and writes each Task's brief from the template in `~/.claude/WORKER-CONTRACT.md` section 5; it does not use the issue watcher for stories in v0. BMAD skills run in attended sessions the person opens; the coordinator never runs, dispatches, messages or types into them.

**Sessions.**
- Release coordinator: accepts packets (H1 checklist, topic a), creates Tasks and workers, reads contracts and ledgers, runs `/sc:sweep` on each wake, does every outward action on the owner's instruction (filing issues, progress comments, local commits, `/sc:closeout`; `/sc:pr-submit --monitor 3` runs in a separate top-level session opened in the feature worktree, because it must run on the PR's head branch (`pr_head_mismatch`) and is an attended loop that would stop the coordinator's wait loop; the coordinator reads its result), is the only writer of `sprint-status.yaml` and of the story record.
- BMAD planning sessions (attended, any number the owner opens, in the release worktree): all `/bmad-*` skills in v0. They appear in the sweep as `person session (active)`.
- Story workers (one per Task, `--unattended`): `/sc:spec-panel`; on the alternate arm `/sc:brainstorm` and `/sc:adversarial`; `/sc:workflow`.
- Implement: person-run until `/sc:implement` has an unattended mode (it has none today: no `## Unattended mode` in its command file or skill, also on master), then a worker.

**Worktrees** (all created by Orca; never raw `git worktree add`).
- One release worktree: the coordinator, BMAD planning, the tracked ledger (`sprint-status.yaml`), the planning artifacts.
- One feature worktree per BMAD feature being built, an Orca child (`worker-start --worktree new-child --base-branch origin/master --setup skip`). The stories of the feature run one after another inside it; each story's panel, workflow and implement Tasks run in that same worktree, because a managed plan must be implemented in the checkout where `/sc:workflow` wrote it (`E-MANAGED-INVALID` otherwise). Later Tasks use `--worktree path:<that worktree>`. One plan package per story.
- Feature worktrees do not hold the ledger. One PR per feature from its worktree, after a rebase on `origin/master`, through `/sc:pr-submit --monitor 3` in a top-level session (owner decision O4; a documented exception to the contract's "children merge back" rule).

**Order per story.** Coordinator checks H1 and the triggers (no model call), copies the packet folder into the feature worktree (it is untracked there unless owner decision O2 tracks it; copy proof by `diff -r`, as step 5 of the 409 hand-off recorded), then: panel Task; (alternate arm: brainstorm Task, adversarial Task, panel Task on the merged spec); workflow Task; plan approval by the owner in chat (O3); implement; coordinator reads the ledger, commits locally under the owner's instruction (explicit paths plus `.dev/tasks`, `git commit --only`, never `--no-verify`), writes the status and the story record, starts the next story. Each Task is created only after its predecessor settled and was read.

**Sequential or parallel.**
- BMAD planning of release n+1 runs in parallel with IronClaude execution of release n (different worktrees; the one shared file is `sprint-status.yaml`, edited by never-regress rules only; a trial item).
- Stories inside a feature: sequential. Features: parallel when they declare no dependency and name different paths; start with 2 at once (owner decision O7; no cap is documented in the files read).
- Panel, workflow and implement of one story: sequential. Two workers never write in one worktree at once.

**Where IronClaude helps BMAD before hand-off (not a hand-off).** The owner's deliverable 1, `/sc:brainstorm --depth deep --research deep --codebase --blind` on storage, per-project Postgres and session and decision history (EPIC-01 features 4 and 6), run in an attended session, because under `--unattended` the Socratic dialogue and deep research are skipped. Its output is an input to `bmad-architecture`; BMAD decides. Also `/sc:spec-panel` on `SPEC.md` as the document-level gate before stories are cut (first run on `SPEC.md` alone).

**While BMAD planning waits on the person**, the coordinator runs its execution queue and the sweep, reads the planning worktree read-only for stories ready for a packet, and tells the owner when a packet is ready or rejected.

**Decisions that need a person** (the inventory the dashboard roadmap, issue 727, can reduce to binary or multiple-choice questions): owner go per epic or feature; packet rejected (return or override); plan approval; Ruling after `E-HALT-QA`; Spec Gap Report outcome; push, PR, merge, closeout; concurrency.

**Deliverables BMAD planning must produce for this topic:** story files with ids, complexity class and paths (topic a); the packet INDEX with "Design question open" marked; nothing else is needed from BMAD for the coordinator design.

**Open for the owner:** O1 (Mode C), O3 (plan approval policy), O4 (PR topology), O5 (build `/sc:implement` unattended first), O6 (standing instruction), O7 (features at once).

**Reasons.** Agent 2: the watcher flow has no implement step and a closed brief template with no story rows, and its launch levels are gated, so stories cannot run end to end there today; the contract already describes this coordinator; the safety property that no issue text reaches a brief is kept. Agent 1 agrees (2026-11-22). Reasons from the BMAD side: BMAD planning sessions are attended by design (`bmad-create-epics-and-stories` has no headless mode and halts at every menu; `bmad-forge-idea` has none), so a coordinator cannot run them and must not wait on them; BMAD's own sprint ledger expects agents to update statuses as they work (`bmad-sprint-planning` workflow notes: "Agents will update statuses as they work"), so one coordinator writer under the never-regress rule fits it. Requests accepted by agent 2: the run notes keep the BMAD story key next to the Task and Dispatch ids. BMAD-side planning of release n+1 in parallel with execution of release n is safe for BMAD artifacts as long as `bmad-sprint-planning` is only re-run by a person who first checks that the coordinator is not mid-write (small race, trial item).

## (e) How GitHub issues are created and updated throughout
DRAFT by agent 1 (2026-11-22). Source: IRONCLAUDE-SIDE.md 8.1 to 8.3, agent1/issue-drafts/README.md.

**Decision (AGREED in messages 02, 03).** Every filing is a GitHub write made only by the coordinator, on the owner's instruction naming it.

| Object | Filed when | By what | Draft |
|---|---|---|---|
| Epic issue (container), one per release, native sub-issue of umbrella #727 | when the owner schedules that release (owner rule, issue 727) | `gh issue create --repo IronbellyOrg/IronClaude --title <title> --body-file <body>` where the body is the part of the draft below the `---` line; label and type as proposed in the draft | `agent1/issue-drafts/EPIC-NN-<slug>.md` (15) |
| Feature sub-issue (container) | with its epic | same | `EPIC-NN-STORY-MM-<slug>.md` (73; "STORY" in the file name follows PROTOCOL.md, these are the owner's "features") |
| Story issue (the claimable unit) | at hand-off, not earlier | `/sc:issue --create @<description file> --mode feature --type <area> --depth <quick|standard|deep, matching the story's complexity class: simple|medium|complex>` (sets issue type, Complexity field from the depth, label) (corrected by agent 2: `--depth` is not fixed at quick) | `agent1/templates/story-issue-description.md` |
| Sub-issue links epic to feature to story | at filing | PRIMARY (agent 2's correction, agent 1 confirmed in `gh issue create --help`, flags read not run): file each container with `gh issue create ... --parent <parent number or URL>` so creation and link are one call; epics use `--parent 727`. A story filed through `/sc:issue --create` has no `--parent`: link it afterwards with `gh issue edit <story> --parent <feature issue>` (`gh issue edit --help` lists `--parent`, `--add-blocked-by`; read, not run; agent 2, 2026-11-22). FALLBACK for linking an existing issue: GitHub REST `POST /repos/IronbellyOrg/IronClaude/issues/{parent_number}/sub_issues` with body field `sub_issue_id` = the child's NUMERIC issue id (not its number); id from `gh api repos/IronbellyOrg/IronClaude/issues/<n> --jq .id`. REST shape read in docs.github.com (rest/issues/sub-issues) by agent 1; NOT run by either agent | none |

**Updates.** The progress comment per story (see (c)); Project Status mirror only when the owner has authorised it; closure through `/sc:closeout`; the feature closes with its last story; the epic closes with a comment linking the BMAD retrospective.

**Labels.** Only `enhancement` (and `bug`, `documentation`, `question`) exist in the repo. The drafts propose `epic` and `release:<version>`, marked (new): a person creates them once, or the coordinator drops them; `/sc:issue` never creates labels.

**Open.** Whether container issues should instead use `/sc:issue --create` templates (agent 2 argues they are a worse fit: Priority, Fix approach, Test plan; and it posts with no preview). Agent 1 accepts plain `gh issue create` for containers because the drafts already follow the ISSUE-BACKLOG and ISSUE-HANDOFF headings (global rule 10). The "Complexity" field on containers: set by hand or skipped (not decided).

Agent 2 corrections to (e), from a read-only `gh issue create --help` (gh 2.103.3 on this host) and `~/.claude/skills/sc-issue-protocol/refs/labels.md`: (1) plain `gh issue create` has `--parent <number or URL>` (adds the new issue as a sub-issue of the parent), `--type <name>` (issue type), `--milestone`, `--project`, `--blocked-by` and `--blocking`; so container issues can be filed and linked in one call, and the REST `sub_issues` call in the table is a fallback, not the plan; `--blocked-by` can carry the story dependency order. It has no flag for the Complexity issue field, so a container's Complexity is by hand or skipped. (2) `/sc:issue --create` sets Complexity from `--depth` (quick = Simple, standard = Medium, deep = Complex) and only the area values `cicd, command, skill, agent, hook, cli, core, docs, tests, install, other` for `--type`; a story that touches the observer uses `--type cli`. It also files with no preview and creates no labels, issue types or fields. (3) A milestone per dashboard release (`--milestone`) is a candidate home for "release 1.1"; not decided, owner's call (nothing in the repo records a dashboard release number: `VERIFIED` only that `VERSION` here says 3.7). (4) The flags above were read in help output, not run.

## (f) How the pipeline treats "BMAD owns higher-level planning, IronClaude owns implementation planning, execution and rapid iteration"

**IronClaude position (agent 2), Round 2 draft.** Full text: `agent2/IRONCLAUDE-SIDE.md` section 8.4.

| Step | Owner |
|---|---|
| Brief, research, PRD, UX, architecture (`AD-n`), SPEC, epics, stories and acceptance criteria (ids `S<N>.<M>-AC<n>`), story order, the sprint ledger values, retrospectives, course corrections | BMAD, in attended sessions |
| Document-level review of those artifacts | BMAD side |
| Intake check H1, story-level spec review, optional code-grounded spec, tasklist, implementation, per-task QA, final review, retries, PR, review loop, CI fixes, closeout | IronClaude |
| Write-back: story status, story record, progress comments, issue closure | the coordinator (the only IronClaude writes into BMAD artifacts: status values in `sprint-status.yaml` and the story record) |
| Spec defects found during execution | IronClaude detects, BMAD decides, through a Spec Gap Report and `bmad-correct-course` |
| Owner decisions | the owner |

**Rule.** Loops that stay inside implementation never go back to BMAD: a failed task, a failed review, a PR review finding, a CI failure and the retries are handled in IronClaude (the retry ladder, `/sc:troubleshoot`, the PR monitor). Only a spec defect goes back: a criterion that is wrong, ambiguous, impossible, or in conflict with an `AD-n`. IronClaude never rewrites a criterion, an `AD-n`, the PRD, the architecture or the epics; it never contradicts an `AD-n`.

**Division of effort in the pipeline.** BMAD is attended and conversational; IronClaude is unattended per story except where it needs a person (plan approval, Ruling). The limit of "rapid iteration" today: `/sc:implement` has no unattended mode, so execution is person-run until it is built (owner decision O5).

**BMAD position (agent 1), 2026-11-22: agree with the table and the rule.** Additions from the BMAD side:
1. BMAD's artifact set is the owner's "higher-level planning": product brief or PRFAQ if needed, research, PRD with feature groups and FR ids, UX (`DESIGN.md`, `EXPERIENCE.md`), architecture spine with stable `AD-n`, SPEC with `CAP-n` and companions, epics and stories with numbered criteria, readiness report, sprint ledger, retrospectives, change proposals. The GitHub epics, features and stories are the issue form of those artifacts.
2. The two IronClaude writes into BMAD artifacts (status values in `sprint-status.yaml`, the story record) are allowed because they are the same writes BMAD's own dev workflow makes (`bmad-dev-story` may change only Status, checkboxes, Dev Agent Record, File List and Change Log; `bmad-create-story` and sprint planning expect agents to update statuses), moved to the coordinator. Nothing else in a BMAD artifact is edited by IronClaude; a derived file (SPEC.md, the spine) is never hand-edited by anyone (`bmad-spec` rule).
3. "Rapid iteration" is IronClaude's, so BMAD does not re-open a story for a failed task, review or CI run. BMAD re-opens only through a Spec Gap Report. A Spec Gap Report is a file next to the packet (failing criterion id, evidence `path:line`, options, who decides) that the BMAD session reads as the input of `/bmad-correct-course`.
4. The pipeline's limit today is IronClaude's, not BMAD's: until `/sc:implement` has an unattended mode (O5, B4) the "rapid" part runs person-attended. Agent 1 recommends the owner decide O5 early because every later release depends on it.

**Open disagreements:** none so far.

## (g) What is reusable: agents, skills, templates, commands (existing and to build)
DRAFT by agent 1 (2026-11-22), merged with IRONCLAUDE-SIDE.md section 9 (agent 2's list, which I accept and do not repeat). Priority P0 = needed for the plan-only pilot, P1 = for a trial release, P2 = later. Owners are proposals.

**Exists today, reuse.** BMAD: all `bmad-*` skills in `.claude/skills/` (BMAD 6.9.0); agent personas John, Mary, Winston, Sally, Paige (`bmad-agent-*`); `bmad-customize` for `_bmad/custom/*.toml`; `bmad-sprint-status` data mode; the worked example `.dev/issues/409/bmad/` on master. IronClaude: the commands and agents in IRONCLAUDE-SIDE 9.1 (`/sc:spec-panel`, `/sc:brainstorm`, `/sc:adversarial`, `/sc:workflow`, `/sc:implement`, `/sc:pr-submit`, `/sc:closeout`, `/sc:sweep`, `/sc:issue`; the coordinator machinery of WORKER-CONTRACT). From this planning: `agent1/issue-drafts/` (15 epics, 73 feature sub-issues) with `agent1/tools/` (generator and data), `agent1/templates/handoff-packet.md` (v2), `agent1/templates/story-issue-description.md`, `agent1/templates/story-record.md`.

**To build (BMAD side; agent 2's items B1 to B11 are in IRONCLAUDE-SIDE 9.2):**

| # | Item | Kind | P | Notes |
|---|---|---|---|---|
| A1 | `project-context.md` for IronClaude that points to CLAUDE.md and lists only what BMAD workflows need | file via `/bmad-generate-project-context` | P0 | loaded by default by most BMAD workflows |
| A2 | `_bmad/custom/bmad-create-epics-and-stories.toml` (team override) with `persistent_facts`: number criteria `S<N>.<M>-AC<n>`; add `Complexity`, `Paths` per story; epic number fixed to the EPIC number | config via `/bmad-customize` | P0 | UNVERIFIED that a fact line is followed (trial); `_bmad/` untracked per clone today (O2) |
| A3 | Multi-release epics recipe (one epic per run, sharded `epics/` folder, `epics/index.md`) tried once | trial in EPIC-01 feature 7 | P0 | risk R1 in RELEASE-PLAN S3.5 |
| A4 | Packet builder: story files and INDEX.md from the epics file | v0 by hand using the template; skill or script only if hand-building loses ids | P2 | agrees with D5 |
| A5 | Status sync script with the never-regress rules (agent 2's B6; BMAD side supplies the rules) | script | P1 | rules in (c) |
| A6 | Story record writer (agent 2's B6 second half) using `agent1/templates/story-record.md` | script or coordinator by hand | P1 | needed by `bmad-retrospective` |
| A7 | Spec Gap Report template | template (agent 2's B3) | P0 | input of `/bmad-correct-course` |
| A8 | Release cycle epic and feature templates: the generator `agent1/tools/render.py` and its two cycle templates (validation, tests) | exists as drafts | done | reuse for every later release by changing version and inputs |
| A9 | Release coordinator duties text (agent 2's B7) with a BMAD section: which BMAD artifacts to read read-only on each wake (`sprint-status.yaml`, epics, readiness report) | doc | P1 | no new `/sc:` command |
| A10 | Label creation (`epic`, `release:<version>`) | owner or maintainer action, once | P2 | optional; drafts work without them |

**Not needed (agreed):** a new hand-off command; a new spec-review agent; a second issue filer; a release-planner agent (the owner's "agents" are the existing BMAD personas for planning and the IronClaude workers for execution).

**Proposed trial path (for the owner):** (1) EPIC-01 feature 7 tries the multi-release recipe and creates epics for EPIC-01 and EPIC-02; (2) plan-only pilot on issue 706 item 6 (story written in BMAD form by a person, story file built, H1 run, `/sc:spec-panel`, `/sc:workflow`, read the plan, stop before implement); (3) second pilot adds a person-run `/sc:implement`, the write-back and the story record; (4) first trial release with 2 features at once. Each step records what failed; the pipeline text is revised from those records.

## Deliverables the BMAD planning must produce (list)
DRAFT by agent 1. For the whole roadmap (program level, EPIC-01): `project-context.md`; a case file of the current observer; research documents; PRD (Update of the 409 PRD) with feature groups and FR ids; UX pair; architecture spine (new `AD-n`, none renumbered); SPEC with companions; an independent review of those; epics and stories for EPIC-01 and EPIC-02; readiness report; `sprint-status.yaml`; the written review of the release list (owner's Deliverable 1); the owner's dated record of which releases are scheduled. For each later release (just in time): change proposal if scope moved; PRD or spine updates if needed; that release's epic file with stories; readiness; refreshed `sprint-status.yaml`; then per feature the packet folder (INDEX.md, story files, story-issue descriptions); at the end `/bmad-retrospective`.

## Owner decisions pending (not disagreements between the agents)

Both agents recommend the same option on each. Reasons and consequences: `agent2/IRONCLAUDE-SIDE.md` section 11.3. Nothing here is decided until the owner says so in chat.

| # | Decision | Recommendation (both agents) | If the owner says otherwise |
|---|---|---|---|
| O1 | Drive stories in Mode C (coordinator-written briefs) or wait for the watcher flow | Mode C | the pipeline waits for `/sc:implement` unattended mode, story rows in the worker brief and the launch-level ship gate; none is scheduled |
| O2 | Track `_bmad-output/` and `_bmad/custom/*.toml` in git (remove the two `.git/info/exclude` lines, which cover all worktrees of a clone); where the packet lives | track both; packet under `.dev/issues/<feature>/bmad/` (409 precedent), copied into each feature worktree | the ledger stays per clone and only one clone may run the pipeline |
| O3 | Plan approval before implement | every medium and complex story, plus the first story of each feature | the `Plan approval:` line is dropped from briefs, which weakens the stop before code is written |
| O4 | PR topology | one PR per feature, from a worktree based on `origin/master`, rebased before the PR (an exception to the contract's "children merge back") | one PR per release, which the contract supports as written |
| O5 | Build `/sc:implement` unattended mode first (B4) | yes, as IronClaude work item 1 | implement stays person-run and the pipeline is unattended only up to the plan |
| O6 | Standing instruction for the coordinator: local commit per settled story, progress comment edits, Project Status mirror, issue filing | give it in chat once per release, naming each action | each action is asked at the moment |
| O7 | Features running at once | 2 for the first release | 1 is safest; 3 or more has no documented cap |

## No consensus
None. Every topic (a) to (g) has the same decision from both agents. The only open items are the owner decisions above, the UNVERIFIED items listed in each section, and the trial thresholds, which are guesses to set after the plan-only pilot.

## Signatures
- agent 1 agrees: 2026-11-22 (bmad-planner). I re-read the whole file after agent 2's edits and signature. The only text I changed after agent 2 signed is the (e) table row "Sub-issue links" (now PRIMARY `gh issue create --parent`, FALLBACK REST), which agent 2 asked for in message 06; the top STATUS line was changed by agent 2. My signature covers the decisions in (a) to (g), the deliverables list and the owner-decisions table as written. Not agreed by anyone yet, only recommended to the owner: O1 to O7. Still UNVERIFIED and listed as trial items: whether a `persistent_facts` line makes BMAD number criteria `S<N>.<M>-AC<n>`; whether the second `bmad-create-epics-and-stories` run overwrites `epics.md`; whether BMAD tooling accepts the coordinator-written story record; the `gh --parent` and REST sub-issue calls (read, never run).
- agent 2 agrees: 2026-11-22 (ic-planner). Signed on the text as it stood after my edits in this round: the (d) copy-of-packet and commit-path additions, the (e) `--depth` correction and the owner-decisions table. If agent 1 changes any decision text after this line, agent 2's signature does not cover that change until agent 2 re-reads it.


## Owner rulings, 2026-11-23 (appended by the coordinator; signed text above is unchanged)
- O1, O2, O4, O5, O6, O7: approved by the owner in chat ("01 02 04 05 06 07 all approved"). O3 (plan approval before implement): not answered yet.
- Branch model (changes O4): each dashboard release is an integration branch (owner wrote dash1.3); each user story is a sub-branch of it (dash1.3/story1); the release branch merges into the default branch (owner wrote main; this repo uses master) when the release is done, then 1.4. Open: git cannot hold both a branch named dash1.3 and one named dash1.3/story1, so the release branch needs a name such as dash1.3/release (or dash-1.3 with dash-1.3/story1). Both agents must reconcile (d) and the packet and worktree text with this model.
- Every decision and completed phase goes in PIPELINE-RECORD.md (owner, 2026-11-23).
- O3 (answered 2026-11-23, owner in chat): no human plan approval. The /sc:workflow plan must pass review panel scrutiny and have no blockers before implement starts. This replaces the 'Plan approval:' line and the coordinator stop before code: the gate is a panel verdict (blocking findings = none), not a person. Coordinator reading, to confirm in trial: the panel is /sc:spec-panel; at most 3 reviews, then escalate to the owner with the open blocking findings (house review-loop rule). Both agents must reconcile topics (a) to (d) and the briefs with this.
- 2026-11-23: /sc:adversarial run on four branching proposals (three researched with Tavily, one from the PrivateRepoE repo draft). Result: .dev/brainstorms/20261123-branching-strategy/UNIFIED-BRANCHING-PROPOSAL.md (base variant 1, combined 0.935 vs 0.920; 87.9% point convergence; INV-017 accepted with mitigation, to verify by trials T4 and T7). Eight owner decisions pending in its section 10.
