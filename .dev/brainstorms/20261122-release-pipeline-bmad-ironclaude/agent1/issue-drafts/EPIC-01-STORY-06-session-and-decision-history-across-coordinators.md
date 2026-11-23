Title: [FEATURE] Release 2 prep: organise session and decision history across coordinators and developers
Draft id: EPIC-01-STORY-06
Parent: EPIC-01 (Release 2 prep); grandparent umbrella #727
Labels: enhancement, release:2-prep (new)
Issue type: Feature (the repo issue type the /sc:issue skill picks for a feature)
Complexity (proposed): Complex
Needs a person in the session: yes (BMAD workflows ask at menus)
Status: DRAFT on disk. Do not file until the owner schedules Release 2 prep.
Label note: `enhancement` exists in the repo today. Labels marked (new) do not exist; `/sc:issue` never creates labels, so a person creates them once or the coordinator drops them.

---

## What was tried

Nothing built yet. Drafted on 2026-11-22 from the owner's roadmap in issue #727 ("Dashboard becomes two-way: voting and responding, roadmap to version 2.0"). Source lines: owner text, paragraph "Release 2 prep" and "Deliverable 1" (vectorized, or organized in whatever way provides most benefit for least work).

Why this feature exists: The owner wants every coordinator in a project, across all human developers, to know what the other coordinators did and decided. The method (vector search or something simpler) is to be chosen by benefit for the least work.

## Relevant files and links

- Owner roadmap: GitHub issue #727, body saved at `.dev/issues/727/issue-body.md` (owner text at its end)
- Related open issue: #725 (coordinators must ask the peer project's coordinator, read-only, before asking a human)
- Related open issues: #409 (TUI dashboard), #706 (observer follow-up), #604 (observer remote fleet), #716 (coordinator next release), #717 (issue watcher), #718 (dashboard items from the 655 split)

## Done when

- The candidate ways of organising history are compared on retrieval quality, effort, running cost and fit with a per-project Postgres database, with the evidence for each (vector search is one candidate, plain tables and text search are others).
- One way is chosen for the first release that needs it, with the reason, and a revisit condition for the others.
- The choice is an `AD-n` in the spine and a story set is ready, or the decision is deferred with an owner-visible reason.

## Who it is for

The owner (supervises the coordinators and makes the decisions) decides; BMAD architect session with an IronClaude deep brainstorm.

## Start user-story planning (BMAD)

Run each step in a fresh context window (the bmad-help skill advises this). The person in the session answers every BMAD menu; BMAD and the agent never decide for them. Each BMAD workflow keeps its own .memlog.md; do not edit SPEC.md or the architecture spine by hand (they are derived from the memlog). After each step, tick its box under Progress and comment on this issue with the output path.

Before step 1: read `EPIC-01` (the epic) and the owner goal that every epic keeps: the dashboard is not meant to replace talking to the coordinator sessions; it is where decisions are made, with as many coordinator questions as possible reduced to binary or multiple-choice questions, and when that fails, demands to the coordinator for more context, a better explanation, a debate of several proposals, extra validation, research, fact checking, or use of specific plugins or tools (for example ponytail).

Steps:

1. `/bmad-technical-research`
   - Say first: ways to organise session and decision history for retrieval by agents: vector search, full-text search, structured tables; cost and effort of each
   - Produces: research document under `_bmad-output/planning-artifacts/research/`
   - Done check: each option has evidence and effort noted; UNVERIFIED claims labelled
2. `/sc:brainstorm "organising session and decision history across coordinators and developers of one project: most benefit for least work" --depth deep --research deep --codebase --blind --output .dev/brainstorms/<date>-history-organisation/`
   - Say first: run ATTENDED in a person's own session; pass the research document and the storage decision
   - Produces: brainstorm package
   - Done check: merged proposal with the rejected options recorded; BMAD decides from it
3. `/bmad-architecture`
   - Say first: update the spine with the chosen organisation (new AD ids, nothing renumbered)
   - Produces: updated spine and memlog
   - Done check: reviewer gate passes

## Story seeds (turn these into user stories with BMAD; edit freely)

- As a coordinator agent, I want the recorded decisions and sessions of the other coordinators of my project, so that I do not ask a human something a peer already settled.
- As a developer who runs coordinator sessions and uses the dashboard, I want to see what other developers' coordinators decided, so that my coordinator does not repeat or contradict it.

Story rules from BMAD (`bmad-create-epics-and-stories`): each story is completable by one dev agent, has Given/When/Then acceptance criteria, and never depends on a later story.

## Hand-off to IronClaude

Hand-off (applies once the stories of this feature exist and are ready):
1. Gate: `/bmad-check-implementation-readiness` passes and `/bmad-sprint-planning` lists the stories (status `backlog`, then `ready-for-dev` when handed over).
2. Build the hand-off packet FOLDER `.dev/issues/<this-issue>/bmad/` (template agent1/templates/handoff-packet.md): one index file for the feature plus one self-contained story file per story (`story-<N>-<M>-<slug>.md`: the story and its acceptance criteria with stable ids `S<N>.<M>-AC<n>` copied verbatim, the `AD-n` rows that bind it, constraints, paths it touches or 'new area', complexity, dependencies, previous-story notes).
3. The IronClaude coordinator runs its acceptance checklist on the packet and, on the owner's go, files one sub-issue per story under this feature. Per story, in order, in one feature worktree: `/sc:spec-panel @<story file>`, then `/sc:workflow <story file> --depth <quick|standard> --handoff none`, then the owner's plan approval in chat, then `/sc:implement <plan path>` (run by a person until `/sc:implement` has an unattended mode). After the last story: `/sc:pr-submit --monitor 3` in a separate top-level session opened in the feature worktree (not in the coordinator's session), then `/sc:closeout <PR> --issue <N>`. A code-grounded spec (`/sc:brainstorm` plus `/sc:adversarial`) is added for a story only when a trigger fires. The exact chain is settled in shared/CONSENSUS.md.
4. Write-back, by the coordinator only (workers never write it): packet accepted = `ready-for-dev`, first implement task started = `in-progress`, PR opened = `review`, PR merged and closeout done = `done` (never regress); a progress comment on each story issue at each event; a BMAD story record `<story_key>.md` when the story is implemented; close each story issue when its acceptance rows pass and the feature issue with its last story.

Feature-specific: No code is built in this feature unless the owner records a go; the first stories land in the release the owner schedules.

## Progress (kept current by the write-back; edit by hand only if the write-back is down)

- [ ] Step 1: /bmad-technical-research
- [ ] Step 2: /sc:brainstorm "organising session and decision history across coordinators and developers of one project: most benefit for least work" --depth deep --research deep --codebase --blind --output .dev/brainstorms/<date>-history-organisation/
- [ ] Step 3: /bmad-architecture
- [ ] Stories pass readiness and are in sprint-status.yaml
- [ ] Hand-off packet written and accepted by the coordinator
- [ ] Story issues filed under this feature
- [ ] IronClaude tasklist package created (path recorded here)
- [ ] PR merged and `/sc:closeout` done; sprint-status keys at `done`
