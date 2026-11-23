Title: [FEATURE] Release 1.7: file and triage bugs from the test pass
Draft id: EPIC-10-STORY-02
Parent: EPIC-10 (Release 1.7); grandparent umbrella #727
Labels: enhancement, release:1.7 (new)
Issue type: Feature (the repo issue type the /sc:issue skill picks for a feature)
Complexity (proposed): Medium
Needs a person in the session: yes (severity confirmation by the owner); filing by the coordinator
Status: DRAFT on disk. Do not file until the owner schedules Release 1.7.
Label note: `enhancement` exists in the repo today. Labels marked (new) do not exist; `/sc:issue` never creates labels, so a person creates them once or the coordinator drops them.

---

## What was tried

Nothing built yet. Drafted on 2026-11-22 from the owner's roadmap in issue #727 ("Dashboard becomes two-way: voting and responding, roadmap to version 2.0"). Source lines: owner text, item for release 1.7 (bug filing).

Why this feature exists: Findings from the pass become GitHub issues with a severity, so that only high and medium bugs block the release and the rest are recorded.

## Relevant files and links

- Owner roadmap: GitHub issue #727, body saved at `.dev/issues/727/issue-body.md` (owner text at its end)
- Severity rule proposed for the owner to confirm (the owner said 'high/medium' without defining them): High = a wrong decision shown, a lost or hidden question, a crash or data loss; Medium = wrong or unclear display or behaviour with a workaround; Low = cosmetic. UNVERIFIED until the owner confirms.
- Bug issue creation: `/sc:issue --create "<description>" --mode bug` (flags read in `~/.claude/commands/sc/issue.md`); the coordinator files, BMAD does not

## Done when

- Every failed guide row is either a filed bug (with severity, steps to reproduce, evidence) or marked not-a-bug with the reason.
- Each high or medium bug has a case file (what happens, evidence grade, suspected area) so the fix story can be written without a second investigation.
- The bug list is attached to this feature as sub-issues; the count per severity is posted as a comment.

## Who it is for

The owner (supervises the coordinators and makes the decisions) confirms severity; BMAD investigates; the coordinator files the issues.

## Start user-story planning (BMAD)

Run each step in a fresh context window (the bmad-help skill advises this). The person in the session answers every BMAD menu; BMAD and the agent never decide for them. Each BMAD workflow keeps its own .memlog.md; do not edit SPEC.md or the architecture spine by hand (they are derived from the memlog). After each step, tick its box under Progress and comment on this issue with the output path.

Before step 1: read `EPIC-10` (the epic) and the owner goal that every epic keeps: the dashboard is not meant to replace talking to the coordinator sessions; it is where decisions are made, with as many coordinator questions as possible reduced to binary or multiple-choice questions, and when that fails, demands to the coordinator for more context, a better explanation, a debate of several proposals, extra validation, research, fact checking, or use of specific plugins or tools (for example ponytail).

Steps:

1. `/bmad-investigate`
   - Say first: one case per high or medium finding: the finding text, the build, the evidence; area exploration of `src/superclaude/cli/observe/` as needed
   - Produces: case files under `_bmad-output/implementation-artifacts/`
   - Done check: each case file grades its claims Confirmed, Deduced or Hypothesis
2. `/sc:issue --create "<bug description>" --mode bug --type cli --depth standard`
   - Say first: run by the coordinator, one bug at a time, using the case file as the description (`@path` works for a file)
   - Produces: GitHub issue and `.dev/issues/<N>/` folder
   - Done check: issue has the Bug type and the `bug` label; the URL is recorded in the case file

## Story seeds (turn these into user stories with BMAD; edit freely)

- As the owner (supervises the coordinators and makes the decisions), I want each failure filed with a severity and steps to reproduce, so that the fix needs no questions back.
- As the maintainer of IronClaude, I want an evidence-graded case file for each high or medium bug, so that stories are written from facts.

Story rules from BMAD (`bmad-create-epics-and-stories`): each story is completable by one dev agent, has Given/When/Then acceptance criteria, and never depends on a later story.

## Hand-off to IronClaude

No hand-off to IronClaude from this feature. Its output is a document or a decision made by people with BMAD. If a story appears that needs code or tests, file it as a new feature under the epic and use the hand-off text of a build feature.

## Progress (kept current by the write-back; edit by hand only if the write-back is down)

- [ ] Step 1: /bmad-investigate
- [ ] Step 2: /sc:issue --create "<bug description>" --mode bug --type cli --depth standard
