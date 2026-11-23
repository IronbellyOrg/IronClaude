Title: [FEATURE] Release 2.0: demands to the coordinator (more context, explanation, debate, validation, research, fact check, plugins)
Draft id: EPIC-15-STORY-02
Parent: EPIC-15 (Release 2.0); grandparent umbrella #727
Labels: enhancement, release:2.0 (new)
Issue type: Feature (the repo issue type the /sc:issue skill picks for a feature)
Complexity (proposed): Complex
Needs a person in the session: yes (BMAD workflows ask at menus)
Status: DRAFT on disk. Do not file until the owner schedules Release 2.0.
Label note: `enhancement` exists in the repo today. Labels marked (new) do not exist; `/sc:issue` never creates labels, so a person creates them once or the coordinator drops them.

---

## What was tried

Nothing built yet. Drafted on 2026-11-22 from the owner's roadmap in issue #727 ("Dashboard becomes two-way: voting and responding, roadmap to version 2.0"). Source lines: owner text, item 'Implement feedback from 1.9 and additional write/respond features for 2.0 release' and the goal paragraph.

Why this feature exists: When a question cannot be reduced to a decision, the person can send a demand to the coordinator instead of switching terminals: more context, a better explanation, a debate of several proposals, extra validation, research, fact checking, or use of a named plugin or tool (for example ponytail).

## Relevant files and links

- Owner roadmap: GitHub issue #727, body saved at `.dev/issues/727/issue-body.md` (owner text at its end)
- Candidate IronClaude commands behind each demand (agent 2 confirms in shared/CONSENSUS.md): `/sc:brainstorm` for a debate of proposals, `/sc:research`, `/sc:adversarial`, `/sc:reflect`; plugin invocation by name

## Done when

- Each demand type has a one-key action, a defined message to the coordinator, an expected result type and a time limit message.
- The result of the demand returns to the dashboard and can lead to the decision.

## Who it is for

IronClaude workers; stories in a BMAD session.

## Start user-story planning (BMAD)

Run each step in a fresh context window (the bmad-help skill advises this). The person in the session answers every BMAD menu; BMAD and the agent never decide for them. Each BMAD workflow keeps its own .memlog.md; do not edit SPEC.md or the architecture spine by hand (they are derived from the memlog). After each step, tick its box under Progress and comment on this issue with the output path.

Before step 1: read `EPIC-15` (the epic) and the owner goal that every epic keeps: the dashboard is not meant to replace talking to the coordinator sessions; it is where decisions are made, with as many coordinator questions as possible reduced to binary or multiple-choice questions, and when that fails, demands to the coordinator for more context, a better explanation, a debate of several proposals, extra validation, research, fact checking, or use of specific plugins or tools (for example ponytail).

Steps:

1. `/bmad-create-epics-and-stories`
   - Say first: one story per demand type; epic number fixed to this EPIC number
   - Produces: story entries
   - Done check: each demand type has a story and criteria
2. `/bmad-check-implementation-readiness`
   - Say first: nothing to add; the skill reads the planning artifacts itself
   - Produces: readiness report
   - Done check: no blocking gap
3. `/bmad-sprint-planning`
   - Say first: nothing to add; the skill reads the planning artifacts itself
   - Produces: refreshed `sprint-status.yaml`
   - Done check: story keys present

## Story seeds (turn these into user stories with BMAD; edit freely)

- As the owner (supervises the coordinators and makes the decisions), I want to ask the coordinator for more context with one key, so that I can decide without leaving the dashboard.
- As the owner (supervises the coordinators and makes the decisions), I want to demand a debate of several proposals, so that I see the options argued before I choose.
- As the owner (supervises the coordinators and makes the decisions), I want to demand research or a fact check, so that a claim is verified before I rely on it.
- As the owner (supervises the coordinators and makes the decisions), I want to ask for a named plugin or tool to be used (for example ponytail), so that the coordinator applies the method I trust.

Story rules from BMAD (`bmad-create-epics-and-stories`): each story is completable by one dev agent, has Given/When/Then acceptance criteria, and never depends on a later story.

## Hand-off to IronClaude

Hand-off (applies once the stories of this feature exist and are ready):
1. Gate: `/bmad-check-implementation-readiness` passes and `/bmad-sprint-planning` lists the stories (status `backlog`, then `ready-for-dev` when handed over).
2. Build the hand-off packet FOLDER `.dev/issues/<this-issue>/bmad/` (template agent1/templates/handoff-packet.md): one index file for the feature plus one self-contained story file per story (`story-<N>-<M>-<slug>.md`: the story and its acceptance criteria with stable ids `S<N>.<M>-AC<n>` copied verbatim, the `AD-n` rows that bind it, constraints, paths it touches or 'new area', complexity, dependencies, previous-story notes).
3. The IronClaude coordinator runs its acceptance checklist on the packet and, on the owner's go, files one sub-issue per story under this feature. Per story, in order, in one feature worktree: `/sc:spec-panel @<story file>`, then `/sc:workflow <story file> --depth <quick|standard> --handoff none`, then the owner's plan approval in chat, then `/sc:implement <plan path>` (run by a person until `/sc:implement` has an unattended mode). After the last story: `/sc:pr-submit --monitor 3` in a separate top-level session opened in the feature worktree (not in the coordinator's session), then `/sc:closeout <PR> --issue <N>`. A code-grounded spec (`/sc:brainstorm` plus `/sc:adversarial`) is added for a story only when a trigger fires. The exact chain is settled in shared/CONSENSUS.md.
4. Write-back, by the coordinator only (workers never write it): packet accepted = `ready-for-dev`, first implement task started = `in-progress`, PR opened = `review`, PR merged and closeout done = `done` (never regress); a progress comment on each story issue at each event; a BMAD story record `<story_key>.md` when the story is implemented; close each story issue when its acceptance rows pass and the feature issue with its last story.

## Progress (kept current by the write-back; edit by hand only if the write-back is down)

- [ ] Step 1: /bmad-create-epics-and-stories
- [ ] Step 2: /bmad-check-implementation-readiness
- [ ] Step 3: /bmad-sprint-planning
- [ ] Stories pass readiness and are in sprint-status.yaml
- [ ] Hand-off packet written and accepted by the coordinator
- [ ] Story issues filed under this feature
- [ ] IronClaude tasklist package created (path recorded here)
- [ ] PR merged and `/sc:closeout` done; sprint-status keys at `done`
