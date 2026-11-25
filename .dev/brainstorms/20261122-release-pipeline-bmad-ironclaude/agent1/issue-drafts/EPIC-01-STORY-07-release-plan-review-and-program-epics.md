Title: [FEATURE] Release 2 prep: review the release list and plan the program epics and stories
Draft id: EPIC-01-STORY-07
Parent: EPIC-01 (Release 2 prep); grandparent umbrella #727
Labels: enhancement, release:2-prep (new)
Issue type: Feature (the repo issue type the /sc:issue skill picks for a feature)
Complexity (proposed): Complex
Needs a person in the session: yes (BMAD workflows ask at menus)
Status: DRAFT on disk. Do not file until the owner schedules Release 2 prep.
Label note: `enhancement` exists in the repo today. Labels marked (new) do not exist; `/sc:issue` never creates labels, so a person creates them once or the coordinator drops them.

---

## What was tried

Nothing built yet. Drafted on 2026-11-22 from the owner's roadmap in issue #727 ("Dashboard becomes two-way: voting and responding, roadmap to version 2.0"). Source lines: owner text, "Deliverable 1: Review of release plan below, breaking down the main changes and features".

Why this feature exists: Deliverable 1 asks for a written review of the release list that breaks out the main changes and features of each step. The same planning run produces the epics and stories for the first releases and proves that BMAD can plan several releases in sequence.

## Relevant files and links

- Owner roadmap: GitHub issue #727, body saved at `.dev/issues/727/issue-body.md` (owner text at its end)
- Plan and pipeline text: `.dev/brainstorms/20261122-release-pipeline-bmad-ironclaude/agent1/RELEASE-PLAN.md` and `shared/CONSENSUS.md`
- Release map: `agent1/RELEASE-PLAN.md` section S2 (15 epics)
- Epic file risk R1 (second `bmad-create-epics-and-stories` run may overwrite the first): trial in this feature

## Done when

- A written review of the release list: for each release the main changes and features, the inputs it needs, and its exit check.
- A SPEC (or PRD plus spine) that passes an independent review, then `epics` with stories for EPIC-01 and EPIC-02 and `sprint-status.yaml` created.
- The multi-release recipe (one epic per run, sharded `epics/` folder, epic number fixed by a `persistent_facts` line) is tried once and the result is recorded: it works, or what failed.
- The owner has recorded in chat which releases are scheduled (condition from issue 727: Deliverable 1 is finished and the owner has recorded which releases are scheduled).

## Who it is for

The owner (supervises the coordinators and makes the decisions) approves; BMAD session; the coordinator files the scheduled epics.

## Start user-story planning (BMAD)

Run each step in a fresh context window (the bmad-help skill advises this). The person in the session answers every BMAD menu; BMAD and the agent never decide for them. Each BMAD workflow keeps its own .memlog.md; do not edit SPEC.md or the architecture spine by hand (they are derived from the memlog). After each step, tick its box under Progress and comment on this issue with the output path.

Before step 1: read `EPIC-01` (the epic) and the owner goal that every epic keeps: the dashboard replaces talking to the coordinator sessions directly; it is the one place where the person reads and answers everything the coordinators need (release 1.8 is where responses and answers start going through the dashboard to the coordinator); decisions are made there, with as many coordinator questions as possible reduced to binary or multiple-choice questions, and when that fails, demands to the coordinator for more context, a better explanation, a debate of several proposals, extra validation, research, fact checking, or use of specific plugins or tools (for example ponytail).

Steps:

1. `/bmad-spec`
   - Say first: distill the two-way PRD, UX and architecture into the SPEC kernel plus companions
   - Produces: `SPEC.md` and companions
   - Done check: self-validate coherence and preservation passes recorded in the memlog
2. `/bmad-review-edge-case-hunter`
   - Say first: run on the SPEC folder path for orthogonal coverage next to the adversarial review
   - Produces: review report
   - Done check: blocking findings fixed
3. `/bmad-create-epics-and-stories`
   - Say first: create epic 1 and epic 2 only (EPIC-01 and EPIC-02); number epics by EPIC number; write to a sharded epics folder
   - Produces: epic file(s) under `_bmad-output/planning-artifacts/epics/`
   - Done check: FR coverage map complete; trial of the multi-release recipe recorded
4. `/bmad-check-implementation-readiness`
   - Say first: nothing to add; the skill reads the planning artifacts itself
   - Produces: readiness report
   - Done check: no blocking gap
5. `/bmad-sprint-planning`
   - Say first: nothing to add; the skill reads the planning artifacts itself
   - Produces: `_bmad-output/implementation-artifacts/sprint-status.yaml`
   - Done check: keys `epic-1`, `1-1-...`, `epic-1-retrospective` exist; file validates with `/bmad-sprint-status` validate mode

## Story seeds (turn these into user stories with BMAD; edit freely)

- As the owner (supervises the coordinators and makes the decisions), I want a review of the release list with the main changes of each step, so that I can decide which releases to schedule.
- As the maintainer of IronClaude, I want stories for the first two releases in the BMAD ledger, so that the first hand-off can be rehearsed.

Story rules from BMAD (`bmad-create-epics-and-stories`): each story is completable by one dev agent, has Given/When/Then acceptance criteria, and never depends on a later story.

## Hand-off to IronClaude

Hand-off (applies once the stories of this feature exist and are ready):
1. Gate: `/bmad-check-implementation-readiness` passes and `/bmad-sprint-planning` lists the stories (status `backlog`, then `ready-for-dev` when handed over).
2. Build the hand-off packet FOLDER `.dev/issues/<this-issue>/bmad/` (template agent1/templates/handoff-packet.md): one index file for the feature plus one self-contained story file per story (`story-<N>-<M>-<slug>.md`: the story and its acceptance criteria with stable ids `S<N>.<M>-AC<n>` copied verbatim, the `AD-n` rows that bind it, constraints, paths it touches or 'new area', complexity, dependencies, previous-story notes).
3. The IronClaude coordinator runs its acceptance checklist on the packet and, on the owner's go, files one sub-issue per story under this feature. Per story, in order, in one feature worktree: `/sc:spec-panel @<story file>`, then `/sc:workflow <story file> --depth <quick|standard> --handoff none`, then the owner's plan approval in chat, then `/sc:implement <plan path>` (run by a person until `/sc:implement` has an unattended mode). After the last story: `/sc:pr-submit --monitor 3` in a separate top-level session opened in the feature worktree (not in the coordinator's session), then `/sc:closeout <PR> --issue <N>`. A code-grounded spec (`/sc:brainstorm` plus `/sc:adversarial`) is added for a story only when a trigger fires. The exact chain is settled in shared/CONSENSUS.md.
4. Write-back, by the coordinator only (workers never write it): packet accepted = `ready-for-dev`, first implement task started = `in-progress`, PR opened = `review`, PR merged and closeout done = `done` (never regress); a progress comment on each story issue at each event; a BMAD story record `<story_key>.md` when the story is implemented; close each story issue when its acceptance rows pass and the feature issue with its last story.

Feature-specific: First rehearsal of the hand-off: pick one ready story, build its packet and run the IronClaude chain on it once the owner says go.

## Progress (kept current by the write-back; edit by hand only if the write-back is down)

- [ ] Step 1: /bmad-spec
- [ ] Step 2: /bmad-review-edge-case-hunter
- [ ] Step 3: /bmad-create-epics-and-stories
- [ ] Step 4: /bmad-check-implementation-readiness
- [ ] Step 5: /bmad-sprint-planning
- [ ] Stories pass readiness and are in sprint-status.yaml
- [ ] Hand-off packet written and accepted by the coordinator
- [ ] Story issues filed under this feature
- [ ] IronClaude tasklist package created (path recorded here)
- [ ] PR merged and `/sc:closeout` done; sprint-status keys at `done`
