# Description given to /sc:issue --create

Re: orchestrator mode/ skill that we are speccing out.   Invoke /sc:issue --create "Orchestrator v2 - Proactive Holistic"

Record the following in the issue

Key objective is that each Orchestrator catalogues and uses knowledge of what all agents across all work spaces are doing in order to maintain a holistic perspective.  The catelogue should be updated based on either a timer or by the child sessions reporting backat checkpoints or accomplishments or we have cheaper faster agents doing session searches or diffing logs and summarizing and feeding into a process of determining the relevance of that information to all other agents with work in progress or unmerged PRs

It should conduct regular reviews of the work of the agents to determine how they impact each other, detect duplicate functionality that could be reused or instanced/referenced directly, research that might inform the work of other agents that should be shared, issues/bugs/failures whose fixes could inform others, instances of multiple agents solving the same issue, overlapping work that touches the same files that could be done better ina specific order, proactive course corrections or changes resulting from lessons learned.

This warrants its own dedicated /tech-reseach pass to find techniques of how multiagent memory and context is used elsewhere and how its leveraged to enrich other agents or course correct them.  This research can be done ahead of. The rest of the work and saved to the issue.

The issue should state that an /sc:brainstorm --depth deep --handoff design should be the starting point and that this is a separate future release after the v1 orchestrator is complete.  The architecture around this should retain flexibility for oother harnesses outside claude code or even to one like Mastra and should follow @docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md

Flags given: --mode feature --type skill --depth standard
