# Issue drafts (agent 1, bmad-planner), generated 15 epics and 73 feature sub-issues

DRAFTS ON DISK. Nothing is filed on GitHub. The coordinator files them after the owner reviews shared/CONSENSUS.md.

File naming follows PROTOCOL.md: `EPIC-NN-<slug>.md` is an epic issue; `EPIC-NN-STORY-MM-<slug>.md` is a feature sub-issue of that epic. In the owner's words the sub-issues are the "features"; the BMAD user stories are written later, by the workflow each sub-issue names (see the story layer in agent1/RELEASE-PLAN.md S3.1).

Each file starts with metadata lines (Title, Draft id, Parent, Labels, Issue type, Complexity, Status), then `---`, then the issue body. The body headings follow the house issue template shape (ISSUE-BACKLOG for epics, ISSUE-HANDOFF for features: What was tried, Relevant files and links, Done when, Pick-up note or Who it is for) plus the sections the owner asked for (start user-story planning with BMAD, hand-off to IronClaude, progress). The repo's `/sc:issue --create` feature templates are an alternative shape; the agreed way (shared/CONSENSUS.md (e)) is plain `gh issue create` for these containers.

How the coordinator files a draft (only after the owner reviews and instructs; flags read in `gh issue create --help`, not run): copy the part below the `---` line into a body file, then `gh issue create --repo IronbellyOrg/IronClaude --title "<Title line>" --body-file <body file> --parent <parent number>` (epics: `--parent 727`; features: the epic's number). Labels marked (new) need creating once or dropping.

Repo labels that exist today (read with `gh label list --repo IronbellyOrg/IronClaude`): bug, documentation, duplicate, enhancement, good first issue, help wanted, invalid, question, wontfix. Labels marked (new) in the drafts do not exist yet.

Regenerate: `uv run python agent1/tools/render.py` (data in agent1/tools/plan_unique.py and plan_cycles.py).

| Draft id | Release | Title | Features | Schedule state |
|---|---|---|---|---|
| EPIC-01 | Release 2 prep | Release 2 prep: evaluate the dashboard and decide the architecture, storage and Postgres database for a two-way platform | 7 | OWNER MARKED FIRST (precedence over the release list); file when the owner says go |
| EPIC-02 | Release 1.1 | Release 1.1: human validation, bug filing and fixes | 4 | UNSCHEDULED (file only when the owner schedules this release) |
| EPIC-03 | Release 1.105 | Release 1.105: automated tests and CI that would have caught the high and medium bugs, plus regression tests | 5 | UNSCHEDULED (file only when the owner schedules this release) |
| EPIC-04 | Release 1.2 | Release 1.2: feedback from current usage | 4 | UNSCHEDULED (file only when the owner schedules this release) |
| EPIC-05 | Release 1.3 slot (unnumbered in the owner's list) | Zellij port and Coder workspace canvas button: review and go or no-go | 3 | UNSCHEDULED (file only when the owner schedules it) |
| EPIC-06 | Release 1.4 | Release 1.4: testing and integration (Zellij and Coder canvas, per the EPIC-05 decision) | 5 | UNSCHEDULED; conditional on EPIC-05 |
| EPIC-07 | Release 1.5 | Release 1.5: human validation, bug filing and fixes | 4 | UNSCHEDULED (file only when the owner schedules this release) |
| EPIC-08 | Release 1.505 | Release 1.505: automated tests and CI that would have caught the high and medium bugs, plus regression tests | 5 | UNSCHEDULED (file only when the owner schedules this release) |
| EPIC-09 | Release 1.6 | Release 1.6: recreate 2 to 4 more screens from the mockups in the TUI | 4 | UNSCHEDULED (file only when the owner schedules this release) |
| EPIC-10 | Release 1.7 | Release 1.7: human validation, bug filing and fixes | 4 | UNSCHEDULED (file only when the owner schedules this release) |
| EPIC-11 | Release 1.705 | Release 1.705: automated tests and CI that would have caught the high and medium bugs, plus regression tests | 5 | UNSCHEDULED (file only when the owner schedules this release) |
| EPIC-12 | Release 1.8 | Release 1.8: first write and respond features (decision cards, notices, answer delivery) | 8 | UNSCHEDULED (file only when the owner schedules this release) |
| EPIC-13 | Release 1.9 | Release 1.9: human validation, bug filing and fixes | 5 | UNSCHEDULED (file only when the owner schedules this release) |
| EPIC-14 | Release 1.905 | Release 1.905: automated tests and CI that would have caught the high and medium bugs, plus regression tests | 5 | UNSCHEDULED (file only when the owner schedules this release) |
| EPIC-15 | Release 2.0 | Release 2.0: implement the 1.9 feedback and additional write and respond features | 5 | UNSCHEDULED (file only when the owner schedules this release) |
