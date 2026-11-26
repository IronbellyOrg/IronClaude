# Iteration 3 (IronClaude): the work files

Generated Wed 25 Nov 2026 20:14 Central from the reviewed iteration plan. The planning run lives in the IronFlow repository at `.dev/research/release-planning-20261124/`; paths such as `plan/...` and `scripts/...` named in these files' header lines are in that folder, not in IronClaude. Iteration 3 ends Sunday 6 December; milestone `rel-7.0.0`.

## How each owner starts

Start only after the pull request that adds this folder to `integration` has merged. Then open your file below and paste its section 1 (the kickoff prompt) into a new Claude session in an IronClaude checkout of `integration`. That session leads your epic: it reads the file, starts one agent per lane that can start now, and gives each agent its story file. Nothing else needs to be read.

| Owner | Epic | File | Stories | Lanes that start now |
|---|---|---|---|---|
| Ryan | E1: The watcher and the coordinator carry an approved issue to a merged pull request without a person passing it along, and their docs match what they do | `epics/E1-ryan.md` | 23 | 18 |
| Clay | E2: Claiming, releasing and session tooling work reliably on integration, and the team's rules for worktrees, branches and changes are written down | `epics/E2-clay.md` | 21 | 19 |
| Leandro | E3: Workers can run unattended within safe limits, and the repo's tests and CI can be trusted | `epics/E3-leandro.md` | 12 | 12 |
| swill-ib | E4: Swarm runs always leave a reliable completion marker and their results, on integration | `epics/E4-swill-ib.md` | 2 | 2 |

## What is in this folder

| Path | For | What it holds |
|---|---|---|
| `epics/<epic>-<owner>.md` | the owner's lead session | kickoff prompt, what the owner approves, epic goal, how to run it, lanes, between people, the story workflow, every story in order |
| `stories/<issue>.md` | the agent of one story | that story's start check, decisions, route and steps, self-contained |
| `stories.json` | scripts | the same facts as data, one record per story |
| `WORK-MAP.md`, `work-map.json` | people planning | the reviewed map the files are built from |
| `ORDER-BY-OWNER.md` | people | one table per owner in order of completion |

## Not automatic yet

- **Launching agents from the claim.** The claim skill refuses `--pipeline worktree` or `full` on a real issue until the launch-guard observations of #442 pass (its ship gate), so for now each story's agent runs `/sc:issue --claim <issue> --pipeline none` in a worktree the lead made.
- **Carrying decisions into a launched agent.** The claim has no way to take a story's decided answers, so the agent appends them to the claim's `issue-summary.md` itself (story workflow, step 4).
- **GitHub "blocked by" links.** The claim reads them since #848 (merged into `integration` on 25 Nov) and stops with `E-BLOCKED` while a blocker is open, but only in a workspace whose installed IronClaude has that change (it reaches the workspace image through `master`). Every start check also reads the prerequisite issue's state directly (`gh issue view <issue> --json state`), so the order holds either way.
