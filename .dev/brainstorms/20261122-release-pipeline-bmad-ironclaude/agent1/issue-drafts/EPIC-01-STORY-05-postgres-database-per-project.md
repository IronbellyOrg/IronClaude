Title: [FEATURE] Release 2 prep: a Postgres database per project (schema, provisioning, lifecycle)
Draft id: EPIC-01-STORY-05
Parent: EPIC-01 (Release 2 prep); grandparent umbrella #727
Labels: enhancement, release:2-prep (new)
Issue type: Feature (the repo issue type the /sc:issue skill picks for a feature)
Complexity (proposed): Complex
Needs a person in the session: yes (BMAD workflows ask at menus)
Status: DRAFT on disk. Do not file until the owner schedules Release 2 prep.
Label note: `enhancement` exists in the repo today. Labels marked (new) do not exist; `/sc:issue` never creates labels, so a person creates them once or the coordinator drops them.

---

## What was tried

Nothing built yet. Drafted on 2026-11-22 from the owner's roadmap in issue #727 ("Dashboard becomes two-way: voting and responding, roadmap to version 2.0"). Source lines: owner text, paragraph "Release 2 prep" and "Deliverable 1" (creation of a postgres database per project).

Why this feature exists: The owner's stated direction: one Postgres database per project, so decisions and sessions of all coordinators in a project survive restarts and can be read by every coordinator and developer of that project.

## Relevant files and links

- Owner roadmap: GitHub issue #727, body saved at `.dev/issues/727/issue-body.md` (owner text at its end)
- Storage evaluation: sibling feature `state-persistence-and-storage-evaluation` (this feature builds on its decision)
- Not known yet: where the database runs (Coder workspace, local, shared host) and how credentials are provided; never print or store a credential in an issue

## Done when

- An epic-altitude architecture spine covers: where the database runs, how it is created per project without manual steps, schema ownership and migrations, backup and restore, local fallback when no database is reachable, credentials handling, and what happens when the database is down.
- Each open point is decided, deferred with a revisit condition, or an open question, as the architecture skill requires; nothing is invented.
- After the owner says go: stories exist for provisioning and the first schema (tables created only by the story that needs them, BMAD rule) and are handed to IronClaude.

## Who it is for

The owner (supervises the coordinators and makes the decisions) and the maintainer of IronClaude; BMAD architect session; IronClaude executes the stories after the owner's go.

## Start user-story planning (BMAD)

Run each step in a fresh context window (the bmad-help skill advises this). The person in the session answers every BMAD menu; BMAD and the agent never decide for them. Each BMAD workflow keeps its own .memlog.md; do not edit SPEC.md or the architecture spine by hand (they are derived from the memlog). After each step, tick its box under Progress and comment on this issue with the output path.

Before step 1: read `EPIC-01` (the epic) and the owner goal that every epic keeps: the dashboard replaces talking to the coordinator sessions directly; it is the one place where the person reads and answers everything the coordinators need (release 1.8 is where responses and answers start going through the dashboard to the coordinator); decisions are made there, with as many coordinator questions as possible reduced to binary or multiple-choice questions, and when that fails, demands to the coordinator for more context, a better explanation, a debate of several proposals, extra validation, research, fact checking, or use of specific plugins or tools (for example ponytail).

Steps:

1. `/bmad-architecture`
   - Say first: epic altitude: scope the run folder to this feature; inherit the program spine as binding constraints; decide database placement, provisioning, schema ownership, migrations, backup, fallback
   - Produces: `ARCHITECTURE-SPINE.md` in an epic-scoped run folder
   - Done check: reviewer gate passes; no whole structural dimension left silent (deployment and operations included)
2. `/bmad-spec`
   - Say first: adopt the spine as a companion and derive the SPEC kernel for the database capability
   - Produces: `SPEC.md` and companions in `_bmad-output/specs/spec-<slug>/`
   - Done check: capabilities have intent and success; non-goals explicit
3. `/bmad-create-epics-and-stories`
   - Say first: stories for provisioning and the first schema only, after the owner's go
   - Produces: story entries in the epic file for this release
   - Done check: each story passes the BMAD story rules; readiness check passes

## Story seeds (turn these into user stories with BMAD; edit freely)

- As a developer who runs coordinator sessions and uses the dashboard, I want a project database created for me without manual setup, so that the dashboard works the first time.
- As the maintainer of IronClaude, I want schema changes made by migrations owned by one story each, so that no story creates tables it does not need.
- As the owner (supervises the coordinators and makes the decisions), I want a clear fallback when the database is unreachable, so that the dashboard still shows the current coordinator questions.

Story rules from BMAD (`bmad-create-epics-and-stories`): each story is completable by one dev agent, has Given/When/Then acceptance criteria, and never depends on a later story.

## Hand-off to IronClaude

Hand-off (applies once the stories of this feature exist and are ready):
1. Gate: `/bmad-check-implementation-readiness` passes and `/bmad-sprint-planning` lists the stories (status `backlog`, then `ready-for-dev` when handed over).
2. Build the hand-off packet FOLDER `.dev/issues/<this-issue>/bmad/` (template agent1/templates/handoff-packet.md): one index file for the feature plus one self-contained story file per story (`story-<N>-<M>-<slug>.md`: the story and its acceptance criteria with stable ids `S<N>.<M>-AC<n>` copied verbatim, the `AD-n` rows that bind it, constraints, paths it touches or 'new area', complexity, dependencies, previous-story notes).
3. The IronClaude coordinator runs its acceptance checklist on the packet and, on the owner's go, files one sub-issue per story under this feature. Per story, in order, in one feature worktree: `/sc:spec-panel @<story file>`, then `/sc:workflow <story file> --depth <quick|standard> --handoff none`, then the owner's plan approval in chat, then `/sc:implement <plan path>` (run by a person until `/sc:implement` has an unattended mode). After the last story: `/sc:pr-submit --monitor 3` in a separate top-level session opened in the feature worktree (not in the coordinator's session), then `/sc:closeout <PR> --issue <N>`. A code-grounded spec (`/sc:brainstorm` plus `/sc:adversarial`) is added for a story only when a trigger fires. The exact chain is settled in shared/CONSENSUS.md.
4. Write-back, by the coordinator only (workers never write it): packet accepted = `ready-for-dev`, first implement task started = `in-progress`, PR opened = `review`, PR merged and closeout done = `done` (never regress); a progress comment on each story issue at each event; a BMAD story record `<story_key>.md` when the story is implemented; close each story issue when its acceptance rows pass and the feature issue with its last story.

Feature-specific: Only the provisioning and schema stories go to IronClaude, and only after the owner records a go. The packet must carry the credential rule: no secret is read, printed or committed.

## Progress (kept current by the write-back; edit by hand only if the write-back is down)

- [ ] Step 1: /bmad-architecture
- [ ] Step 2: /bmad-spec
- [ ] Step 3: /bmad-create-epics-and-stories
- [ ] Stories pass readiness and are in sprint-status.yaml
- [ ] Hand-off packet written and accepted by the coordinator
- [ ] Story issues filed under this feature
- [ ] IronClaude tasklist package created (path recorded here)
- [ ] PR merged and `/sc:closeout` done; sprint-status keys at `done`
