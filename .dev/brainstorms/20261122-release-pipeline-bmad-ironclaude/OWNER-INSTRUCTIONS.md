# Owner instructions, 2026-11-22 (verbatim; the owner's own words)

The roadmap the instructions refer to ("the plan as laid out above") is the owner's text in GitHub issue 727 (IronbellyOrg/IronClaude, "Dashboard becomes two-way: voting and responding, roadmap to version 2.0"); its body is saved at /home/coder/workspaces/IronClaude/.dev/issues/727/issue-body.md and ends with the owner's roadmap word for word. Read that file first.

---

Regarding the roadmap planning to release 2.0, our next objective is to build a release planning pipeline that involves BMAD for upfront planning and Ironclaude for impelementation planning and execution.

Spawn 2 subagents
- give them both the plan as laid out above and have:
- agent 1 invoke: /bmad-help to lay down the the multi-release plan, including all epics stories and a step by step invocation of the relevant bmad commands for every step of the way with the deliverables being the epics are issues in GitHub with the features under them being subissues containing instructions on the bmad workflow to invoke to begin user story planning.  - Agent 1 must communicate and collaborate with agent 2 as it approaches the handoff planning to discuss collaborate and debate to reach consensus on how Bmad hands off to Ironclaude or even how it can use Ironclaude during planning.  Consensus must be acheived to finalize ownership, division of labour and the details of the deliverables from the BMAD planning

Agent 2:
/sc:recommend
BMAD must then hand off the user stories to ironclaude for brainstorming design and sc:workflow for tasklist generation and execution.  BMAD owns the higher level planning and collaboration which create the individual release plans as issues, with epics and user stories while ironclaude owns implementation planning and execution and rapid iteration
- Agent 2 must communicate, discuss and debate with agent 1 about Ironclaudes requirements to generate and implement the tasklist with sc:workflow and sc:implement.
  -- To invoke sc:brainstorm to debate the benefit of using Ironclaude to geenrate the specs/prds with sc:brainstorm in addition to BMAD and the debating and merging the two specs with sc:adversarial
  --- if only BMAD then invoking spec-panel to review and improve the spec/prd
- To determine when does the userstory from BMAD get handed off to Ironclaude for tasklist generation and execution
- Determine best way to update progress in the bmad plan as ironclaude agents and sessions complete the execution of tasklists
- To determine how the Coordinator orchestrates the bmad vs ironclaude efforts and handoffs from the coordinator session and if the planning and execution of a single release  happens in a single worktree or multiple worktrees over the course of the release, what happens in a single session vs separate sessions, what is sequential vs parallel
-- Ensuring that the coordinator and Ironclaudes orchestration mode is used throughout with GitHub issues being created and updated to ensure progress and planning are reflected accurately and frequently

The ultimate objective is to determine, through brainstorming and trial and error to create a reusable release planning and execution pipeline, agents, skills, templates that mixes BMAD and Ironclaude as per the details outlined above.
