## What was tried

Nothing has been built for this yet. Filed from the owner's note of 2026-11-22.

State read on 2026-11-22 (so the next person starts from facts):
- The observer dashboard (`superclaude observe`) is read-only by design. Its user guide (`docs/user-guide/observer.md` on master) says it "never approves, retries, terminates, dispatches, merges or messages". It shows the coordinator's questions (questions screen and Decision Desk) but has no way to answer them; the person answers in the coordinator's own terminal.
- It keeps no database. Questions live in process memory; the only stored files are an export record and a snapshot under the observer state folder.
- The first small step toward this roadmap is already filed: issue 726 (a vote on each question, kept as a local record). Its open decision is whether the read-only rule may be relaxed. This note is the owner's direction on that rule: the dashboard is meant to become two-way.

## Relevant files and links

- Related issues: #409 (TUI dashboard, open), #706 (observer follow-up, open), #604 (observer remote fleet, open), #606 (visual parity, closed; holds the Zellij go or no-go), #718 (dashboard items from the 655 split), #716 (coordinator next release), #726 (vote on interventions).
- Code today: `src/superclaude/cli/observe/` (`view.py`, `questions.py`, `commands.py`, `export.py`), tests in `tests/observe/`, guide `docs/user-guide/observer.md`.
- The design mockups and "Clay's html dashboards" mentioned in the note: location Not known yet (the 20 synthetic designs are in the design package on branch `docs/409-orca-dashboard-designs`).

## Done when

Deliverable 1 is finished and the owner has recorded in chat which releases are scheduled:
- A written review of the release list below that breaks out the main changes and features of each step.
- A result from `/sc:brainstorm --depth deep` on the architecture, data storage and database needs of the later releases, including the per-project Postgres database and vectorised or otherwise organised session and decision history across coordinators and developers.
- Release 2 prep done first: use and evaluation of the current version, research of requirements, best approaches and similar GitHub projects, and the state and storage needs of a dashboard that becomes a two-way communication platform.

Each release in the list then gets its own issue when the owner schedules it; this issue closes when they exist or the owner drops them.

## Pick-up note

Do not build anything from this issue before the owner says go. The owner's order: the architecture and preliminary evaluation come first and take precedence over the release list; the priority is checking what is needed to support the two-way dashboard and building or changing it, including a Postgres database per project. Dashboard, watcher and coordinator work are meant to be developed together as needed.

The goal stated by the owner is NOT to replace talking to the coordinator sessions. It is that the dashboard is where decisions are made, with as many coordinator questions as possible reduced to binary or multiple-choice questions for the person, and, when that fails, demands to the coordinator for more context, a better explanation, a debate of several proposals, extra validation, research, fact checking, or use of specific plugins or tools (for example ponytail).

Reading notes (UNVERIFIED, mine): "Zelij" is read as Zellij; "1\n5 release" is read as 1.5; the version numbers such as 1.105 are kept as the owner wrote them.

Owner's text, verbatim (2026-11-22):

> Backlog voting and responding for version 2.0 release
>
> Below is a high level roadmap of Dashboard work leading up to version 2 (With any supporting work on watcher / coordinator included in dashboard release. These 3 should be developed in lockstep as needed)
>
> Release 2 prep: First step is usage and evaluation of current version and evaluation and research of requirements, best approaches and any similar github projects to learn from that overlap to achieve the following below, especially initial voting and responding from the dashboard. Evaluate needs for state persistence and data storage related to the dashboard becoming a central bidirectional communication platform instead of simply an informational platform. The ultimate goal is NOT to replace interacting with the coordinator sessions, but it will be where all decisions should be made with as many of the coordinator interactions being boiled down to binary or multiple choice questions to the user or if that fails then demands to the orchestrator for more context, a better explanation, debating multiple proposals, extra validation, research, fact checking or invoking specific plugins(ie: ponytail or tools) as the need arises.
>
> This architectural and prelim eval takes precedence over the release 2 roadmap below. Priority is evaluating the needs and validating or building/ changing what is needed to support those and future needs, including the creation of a postgres database per project with the eventual goal of having current and past sessions and decisions vectorized(or organized in whatever way provides most benefit for least work) of all coordinators within a project, across all human developers have context about the activities of the other coordinators
>
> Release 2 and beyond: Moving past release 2 will be more user feedback systems used to gather data used to fine tune when and how the user is prompted
>
> Deliverable 1: Review of release plan below, breaking down the main changes and features and the invoke /sc:brainstorm --depth deep to brainstorm any changes in architecture or data storage or database needs to accomodate the following releases
>
> - Human validation of all features and desired functionality
> - Filing and fixing bugs for a version 1.1 with any high/medium issues.
> - 1.105 release: Additional automated tests or ci needed to have caught any high/medium bugs without needing human validation as well as regression tests
> - Filing Feedback based on current usage with a version 1.2 release
> - Review porting dashboard to Zelij and accessing it directly from Coder Workspace canvas with a new button
> - Planning testing and integration for a 1.4 release
> - Human testing, bug filing and fixing for 1 (line break) 5 release
> - 1.505 release: Additional automated tests or ci needed to have caught any high/medium bugs without needing human validation as well as regression tests
> - Review addition screens from initial tui mockups and Clays html dashboards, picking 2-4 more to recreate in TUI for version 1.6
> - Human testing, Bug filing a fixing for version 1.7
> - 1.705: Additional automated tests or ci needed to have caught any high/medium bugs without needing human validation as well as regression tests
> - Planning, brainstorming and implementation of first write/Respond features for a 1.8 release. This will involve boiling the coordinators needs into digestible multiple choice or binary decisions to the user or notifications that the user is needed in the coordinator session for a q&a or longer conversation
> - Human testing, feedback/feature requests, validation, bug filing and fixing for 1.9 release
> - 1.905: Additional automated tests or ci needed to have caught any high/medium bugs without needing human validation as well as regression tests
> - Implement feedback from 1.9 and additional write/respond features for 2.0 release
