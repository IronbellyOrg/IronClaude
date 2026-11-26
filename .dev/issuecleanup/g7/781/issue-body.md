Thank you, Ryan, for the issue watcher and the standing coordinator ([pull request 707](https://github.com/IronbellyOrg/IronClaude/pull/707), merged). Thank you also for the written reasons on [Coder issue 515](https://github.com/IronbellyOrg/PrivateRepoF/issues/515#issuecomment-7062617492), in the comment of 2026-11-21. This builds on that work. It is a question and an offer, not a decision.

## Feature Summary

Could a small set of contact agents sit beside the dashboard, giving a person one place to ask about a bounded set of coordinators and to send a message to the right one? Could we try both routes at small scale before choosing, while keeping Ryan's watcher and standing coordinator design?

## Problem Statement

Clay expects 20 or more pull requests a day across several projects. Each project has its own standing coordinator, the agent that supervises that project's workers. A person has no single place to ask "where does this stand?" or send one message to one coordinator. Jumping between coordinator sessions will not scale.

The planned answer today is dashboard first. Issue 727 plans voting, responding and routing messages from the dashboard. Its newest review lists "routing to the correct coordinator" as something still to specify. A dashboard alone gets harder to navigate as the number of coordinators and pull requests grows. Clay's own work already runs through agents rather than screens. Many people are also moving away from human screens toward agents.

What exists today, checked against `origin/master` at `f2894fc44`:

- `superclaude observe` is a read-only terminal view. Its guide says it "never approves, retries, terminates, dispatches, merges or messages" (`docs/user-guide/observer.md:156`). Every count covers the local host only (`docs/user-guide/observer.md:154`).
- Issue 727 plans the two-way part. The [contact-agent comment already posted there](https://github.com/IronbellyOrg/IronClaude/issues/727#issuecomment-7140363834) is the starting point, not a separate dashboard proposal.
- Sending a message to one individual coordinator is only partly planned. It is a review item in 727, with no design yet.
- Issue 409, the terminal dashboard parent, lists an "orchestrator of orchestrators" and relaying to a management server in plan item 3. Those later phases are recorded, not scheduled.
- Issue 604, the observer's cross-host view, is backlog and not built.
- Nearby work includes 606, visual parity, closed; 706, observer summaries, links, named steps and scale tests; and 726, a vote on each question.

## User Story

As a person supervising many coordinators, I want one place to ask "where does this stand?" and to send a message to one coordinator, so that I do not jump between coordinator sessions.

## Proposed Solution

Ryan's decision in the Coder 515 comment is one coordinator per project, no agent above the coordinators, and a central dashboard run by code with one feed or one pane per coordinator. His reason is that research and debate on one agent for everything "all came back with a series of scaling issues" with 5 projects of 10 to 15 worktrees each. The agent cannot keep up, and things get lost in the flood of updates. The contract also says one coordinator per project (`src/superclaude/core/WORKER-CONTRACT.md:294`). We respect that.

Could two or three contact agents sit beside that dashboard? Each would follow a bounded set of coordinators, for example three or four projects, not all of them. Each would do only two jobs:

1. Answer "where does this stand?" for the coordinators it follows.
2. Pass a person's message to the right coordinator.

How this could fit Ryan's decision:

- A contact agent does not run work, direct a coordinator or approve anything. It reports and relays.
- A person's typed go for a push or a merge stays with the person.
- The proposed contact agents would read the same code-generated feed as the dashboard. The data would be shared, and the dashboard would remain one view of it. This shared feed is a proposal, not a claim that today's observer already supports contact agents.
- A bounded set might avoid the flood that one agent for everything hits. We have not tested that.

Could both routes be tried on a small scale, for example one project and one contact agent, before choosing? The same question applies to the "orchestrator of orchestrators" line in 409 and the cross-host view in 604. We are happy to help write this up. We are also happy to fold it into 727 if Ryan prefers.

**What is not known**

- **Routing.** How does a contact agent find the right coordinator for a message? UNVERIFIED: how the "routing to the correct coordinator" item in 727 will work. One check would settle it: read the routing section of the 727 design once it is written.
- **Relay.** What carries the message? Candidates are Orca messages, or the planned wake path in 757 and 770. UNVERIFIED: which fits. One check would settle it: establish whether the wake path in 757 and 770 can carry a person's message, not only a claim.
- **Location and start.** Does this need an agent file or a skill? By default agent work here is a skill, so could it be a skill installed with the other skills, started by a person or a long-lived session for a given project set? UNVERIFIED: where it lives and how it starts. One check would settle it: review a proposed skill or agent-file entry point and record the chosen location and invocation in the design.
- **Feed coverage.** Is a read-only feed with no question text on disk enough to answer "where does this stand?" Issue 727 keeps the rule that question text stays on screen only. UNVERIFIED: whether that feed is enough. One check would settle it: try representative status questions against the permitted feed in the small trial, without storing question text.

**Open questions**

- How many contact agents, and how are coordinators grouped: by project, person or team?
- Who owns it?
- Should this fold into issue 727 if Ryan prefers?

## Acceptance Criteria

- [ ] There is a written answer on whether to try contact agents on one project alongside the dashboard. It records the reasons without assuming either route wins.
- [ ] The design specifies how a message finds the correct coordinator and what carries it. It records the check against the routing work in 727 and the message-carrying limits of the candidates in 757 and 770.
- [ ] The design records whether this lives in a skill or an agent file, where it is installed, how a person starts it, and which coordinators it follows.
- [ ] The contact agent's limits are written and checked: reporting and relay only, no direction of coordinators, no project-state writes, and no approval of work. A person's typed go for a push or merge stays with the person.
- [ ] A small comparison of the dashboard route and contact-agent route has a recorded result, or a recorded decision not to run it with the reason. If tried, it covers status questions, one message to the intended coordinator, and whether the feed works without question text on disk.
- [ ] The result records the remaining UNVERIFIED items, grouping and ownership questions, and whether the work should stay here or fold into 727.

## Out of Scope

- Building the dashboard in issue 727 or replacing it.
- Replacing Ryan's merged watcher and standing coordinator design.
- Changing who approves anything.
- An agent that directs coordinators, or one agent above all coordinators.
- Reintroducing Clay's earlier rolled-back 655 design.
- Coordinator-to-coordinator read-only questions, covered separately by 725.

## Components Affected (from `/sc:analyze`)

These are existing places to assess, not a decision to change all of them:

- `src/superclaude/cli/observe/adapter.py`: the observer's limited, read-only Orca connection. Keep message relay separate from that read-only boundary.
- `src/superclaude/cli/observe/collector.py`: collection of the observer's status data. Assess whether it supplies what the proposed shared feed needs.
- `src/superclaude/cli/observe/export.py`: plain-text records and JSON snapshots. Assess feed coverage without adding question text to stored output.
- `docs/user-guide/observer.md`: the current local-host, read-only and screen-only question-text limits.
- `src/superclaude/core/WORKER-CONTRACT.md`: the one-coordinator-per-project rule and coordinator duties. Preserve those duties and approval boundaries.
- `src/superclaude/skills/`: existing skill packages. `src/superclaude/skills/sc-sweep-protocol/SKILL.md` is an existing example of a narrowly limited skill that reads and reports. The contact skill's name and final location are not decided.
- `tests/skills/test_worker_contract.py`: existing checks of contract wording. Add tests for a new skill under `tests/skills/` if that route is chosen.
- `tests/observe/test_adapter.py` and `tests/observe/test_export.py`: existing checks around observer calls and stored output. Extend them only if those components change.

## Related Issues/PRs

- [PR 707](https://github.com/IronbellyOrg/IronClaude/pull/707): merged issue watcher and standing coordinator, the design this builds on.
- [#727](https://github.com/IronbellyOrg/IronClaude/issues/727): two-way dashboard, voting and responding, with a roadmap to version 2.0. The [contact-agent comment](https://github.com/IronbellyOrg/IronClaude/issues/727#issuecomment-7140363834) is already there.
- [#409](https://github.com/IronbellyOrg/IronClaude/issues/409): terminal dashboard parent. Plan item 3 mentions an "orchestrator of orchestrators" and a management-server relay.
- [#604](https://github.com/IronbellyOrg/IronClaude/issues/604): observer cross-host fleet view, backlog and not built.
- [#606](https://github.com/IronbellyOrg/IronClaude/issues/606): observer visual parity, closed.
- [#706](https://github.com/IronbellyOrg/IronClaude/issues/706): observer follow-up for summaries, links, named steps and scale tests.
- [#726](https://github.com/IronbellyOrg/IronClaude/issues/726): a vote on each question.
- [#777](https://github.com/IronbellyOrg/IronClaude/issues/777): map of the manual pieces per issue in the watcher and coordinator chain.
- [#770](https://github.com/IronbellyOrg/IronClaude/issues/770): watcher hands each claim to the coordinator, with results coming back to it.
- [#757](https://github.com/IronbellyOrg/IronClaude/issues/757): run the coordinator sweep outside the session and wake it only on change.
- [#761](https://github.com/IronbellyOrg/IronClaude/issues/761): the possible watcher and coordinator gaps this question came from.
- [#725](https://github.com/IronbellyOrg/IronClaude/issues/725): nearby but separate. It covers coordinator-to-coordinator read-only questions before asking a human, not a person's contact agent.
- [IronbellyOrg/PrivateRepoF#515](https://github.com/IronbellyOrg/PrivateRepoF/issues/515): Ryan's reasons for one coordinator per project and a dashboard run by code. See the [comment of 2026-11-21](https://github.com/IronbellyOrg/PrivateRepoF/issues/515#issuecomment-7062617492).

## Priority

Medium: a planned feature (Priority set by Clay).

## Fix approach

Repo: IronbellyOrg/IronClaude. Base branch: master.

Commands, in order: `/sc:brainstorm` first because the design is open, then `/sc:workflow`, then `/sc:implement <the printed plan path>`, then `/sc:pr-submit --monitor 3` when shipping is authorized.

Steps, in order:

- Step 1: Use `/sc:brainstorm` to answer the routing, relay, skill-or-agent, grouping and ownership questions with Ryan. Compare the dashboard route with the bounded contact-agent route. Use `docs/user-guide/observer.md`, `src/superclaude/core/WORKER-CONTRACT.md` and the linked 727 design as constraints. Assumption: implementation waits for the written decision to try this; the issue itself grants no approval.
- Step 2: Inspect `src/superclaude/cli/observe/adapter.py`, `collector.py` and `export.py` to specify the permitted shared feed. Check the 757 and 770 wake-path proposal for a person's message. Keep relay outside the observer's read-only connection. Assumption: a separate relay boundary can be specified without making the observer send messages; this must be checked, not treated as built.
- Step 3: Use `/sc:workflow` to write a small trial plan. If the skill route is chosen, place its canonical package under `src/superclaude/skills/` and its tests under `tests/skills/`. Record the actual name, invocation and bounded coordinator set before implementation. If an agent file is chosen instead, record its location in that plan rather than inventing one here.
- Step 4: Use `/sc:implement` only after the trial plan is approved. Add the selected entry point and tests. Preserve `WORKER-CONTRACT.md` boundaries and the observer's stored-output limits. Update `docs/user-guide/observer.md` only where the agreed integration needs explanation. Edit canonical source first and use `make sync-dev` for generated development copies.
- Step 5: Run the small comparison, record what worked and what remains UNVERIFIED, and review whether to continue or fold the work into 727. Run the regression gate before any authorized submission through `/sc:pr-submit --monitor 3`. A trial result does not choose a route on Ryan's behalf.

## Test plan

- Tests to add or change: assuming the skill route is selected, add a new test file under `tests/skills/` for the chosen skill. Check its bounded coordinator set, status answers from permitted evidence, and routing of one person's message to the intended coordinator. Check that the contact agent never writes project state or approves work, and refuses requests to dispatch, direct a coordinator, push or merge. The relay must not turn a person's message into approval. Use simulated calls before any live trial. Assumption: the exact test filename and relay test cases follow the design decision, not an invented transport here.
- Observer checks: if observer code changes, extend `tests/observe/test_adapter.py` to keep its calls read-only and `tests/observe/test_export.py` to keep question text out of stored output. Compare the permitted feed with representative status questions. Missing evidence must stay missing rather than become a made-up answer.
- Regression gate: after canonical edits and `make sync-dev`, run `uv run pytest`, `make lint` and `make verify-sync`. These are planned checks, not claimed passes.
- How a reviewer verifies: read the written decision, routing specification and start instructions. Run the new skill tests and affected observer tests, then the full regression gate. Review a small trial of the dashboard route and contact-agent route on one project. Confirm the intended coordinator received the test message, the status answer used permitted evidence, no project-state write or approval occurred, and no question text was stored. Assumption: a live relay trial happens only after the person explicitly authorizes its recipient and message. If the decision is not to trial, review the recorded reason instead of treating a trial as passed.

<!-- sc:issue:create template=issue-feature-simple -->

