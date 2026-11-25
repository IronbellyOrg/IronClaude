Title: [FEATURE] Release 1.705: add the automated tests the gap map names
Draft id: EPIC-11-STORY-02
Parent: EPIC-11 (Release 1.705); grandparent umbrella #727
Labels: enhancement, release:1.705 (new)
Issue type: Feature (the repo issue type the /sc:issue skill picks for a feature)
Complexity (proposed): Medium
Needs a person in the session: yes (BMAD workflows ask at menus)
Status: DRAFT on disk. Do not file until the owner schedules Release 1.705.
Label note: `enhancement` exists in the repo today. Labels marked (new) do not exist; `/sc:issue` never creates labels, so a person creates them once or the coordinator drops them.

---

## What was tried

Nothing built yet. Drafted on 2026-11-22 from the owner's roadmap in issue #727 ("Dashboard becomes two-way: voting and responding, roadmap to version 2.0"). Source lines: owner text, item for release 1.705.

Why this feature exists: Each gap group becomes tests that fail on the build that contained the bug and pass on the fixed build.

## Relevant files and links

- Owner roadmap: GitHub issue #727, body saved at `.dev/issues/727/issue-body.md` (owner text at its end)
- Observer code on origin/master: `src/superclaude/cli/observe/` (view.py, questions.py, commands.py, export.py, adapter.py, collector.py, keys.py, snapshot.schema.json), tests in `tests/observe/`, guide `docs/user-guide/observer.md`
- Test conventions: `uv run pytest`, `tests/observe/` (golden files, fake runner seam); house rule: UV only, never bare pip

## Done when

- For each gap group, a test exists that fails on the buggy build and passes on the fixed build (shown once, recorded in the story).
- The new tests run in the normal suite and in CI.

## Who it is for

IronClaude workers; stories written in a BMAD session.

## Start user-story planning (BMAD)

Run each step in a fresh context window (the bmad-help skill advises this). The person in the session answers every BMAD menu; BMAD and the agent never decide for them. Each BMAD workflow keeps its own .memlog.md; do not edit SPEC.md or the architecture spine by hand (they are derived from the memlog). After each step, tick its box under Progress and comment on this issue with the output path.

Before step 1: read `EPIC-11` (the epic) and the owner goal that every epic keeps: the dashboard replaces talking to the coordinator sessions directly; it is the one place where the person reads and answers everything the coordinators need (release 1.8 is where responses and answers start going through the dashboard to the coordinator); decisions are made there, with as many coordinator questions as possible reduced to binary or multiple-choice questions, and when that fails, demands to the coordinator for more context, a better explanation, a debate of several proposals, extra validation, research, fact checking, or use of specific plugins or tools (for example ponytail).

Steps:

1. `/bmad-create-epics-and-stories`
   - Say first: one story per gap group of the gap map; acceptance criteria: Given the buggy build, When the new test runs, Then it fails; Given the fixed build, Then it passes
   - Produces: story entries in this release's epic file
   - Done check: FR coverage map covers every gap group
2. `/bmad-check-implementation-readiness`
   - Say first: nothing to add; the skill reads the planning artifacts itself
   - Produces: readiness report
   - Done check: no blocking gap
3. `/bmad-sprint-planning`
   - Say first: nothing to add; the skill reads the planning artifacts itself
   - Produces: refreshed `sprint-status.yaml`
   - Done check: story keys present

## Story seeds (turn these into user stories with BMAD; edit freely)

- As the maintainer of IronClaude, I want a failing-then-passing test for each gap group, so that the same bug cannot return unseen.

Story rules from BMAD (`bmad-create-epics-and-stories`): each story is completable by one dev agent, has Given/When/Then acceptance criteria, and never depends on a later story.

## Hand-off to IronClaude

Hand-off (applies once the stories of this feature exist and are ready):
1. Gate: `/bmad-check-implementation-readiness` passes and `/bmad-sprint-planning` lists the stories (status `backlog`, then `ready-for-dev` when handed over).
2. Build the hand-off packet FOLDER `.dev/issues/<this-issue>/bmad/` (template agent1/templates/handoff-packet.md): one index file for the feature plus one self-contained story file per story (`story-<N>-<M>-<slug>.md`: the story and its acceptance criteria with stable ids `S<N>.<M>-AC<n>` copied verbatim, the `AD-n` rows that bind it, constraints, paths it touches or 'new area', complexity, dependencies, previous-story notes).
3. The IronClaude coordinator runs its acceptance checklist on the packet and, on the owner's go, files one sub-issue per story under this feature. Per story, in order, in one feature worktree: `/sc:spec-panel @<story file>`, then `/sc:workflow <story file> --depth <quick|standard> --handoff none`, then the owner's plan approval in chat, then `/sc:implement <plan path>` (run by a person until `/sc:implement` has an unattended mode). After the last story: `/sc:pr-submit --monitor 3` in a separate top-level session opened in the feature worktree (not in the coordinator's session), then `/sc:closeout <PR> --issue <N>`. A code-grounded spec (`/sc:brainstorm` plus `/sc:adversarial`) is added for a story only when a trigger fires. The exact chain is settled in shared/CONSENSUS.md.
4. Write-back, by the coordinator only (workers never write it): packet accepted = `ready-for-dev`, first implement task started = `in-progress`, PR opened = `review`, PR merged and closeout done = `done` (never regress); a progress comment on each story issue at each event; a BMAD story record `<story_key>.md` when the story is implemented; close each story issue when its acceptance rows pass and the feature issue with its last story.

Feature-specific: Whether `/bmad-qa-generate-e2e-tests` writes any of these tests or IronClaude's own test conventions do is open (question Q6 in agent1/RELEASE-PLAN.md S5.2); default in these drafts: IronClaude conventions.

## Progress (kept current by the write-back; edit by hand only if the write-back is down)

- [ ] Step 1: /bmad-create-epics-and-stories
- [ ] Step 2: /bmad-check-implementation-readiness
- [ ] Step 3: /bmad-sprint-planning
- [ ] Stories pass readiness and are in sprint-status.yaml
- [ ] Hand-off packet written and accepted by the coordinator
- [ ] Story issues filed under this feature
- [ ] IronClaude tasklist package created (path recorded here)
- [ ] PR merged and `/sc:closeout` done; sprint-status keys at `done`
