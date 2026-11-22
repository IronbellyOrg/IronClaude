# Draft notes

Leave a list empty (write "None") when there is nothing to report. The orchestrator asks the user one question only when either list has an item.

## New material

<!-- Facts added to the issue body that the description did not contain, one per line, each with its source (path:line or command). -->

- #339 is the linked v1 prerequisite and covers supervision, child reporting and recovery/cleanup. Source: `gh issue view 339 --repo IronbellyOrg/IronClaude --json title,body`; the user's drafting instructions identify it as v1.
- #409 concerns a read-only human-observation dashboard, distinct from proactive agent coordination. Source: `gh issue view 409 --repo IronbellyOrg/IronClaude --json title,body`.
- #331 proposes intake/routing of tagged, human-approved backlog issues to a project's Orchestrator. Source: `gh issue view 331 --repo IronbellyOrg/IronClaude --json title,body`.
- #326 concerns Git/GitHub communication and collaboration across commands and skills. Source: `gh issue view 326 --repo IronbellyOrg/IronClaude --json title,body`.
- The required developer guide is an existing architecture integration surface, including coordinator/worker separation. Source: Read of `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`, sections 1 and 7.7.
- `src/superclaude/core/WORKER-CONTRACT.md` is an existing integration surface containing coordinator, worker-report and cross-session follow-up rules. Source: Read of that file, sections 1–4, including WC-12.
- `src/superclaude/commands/pm.md` and `src/superclaude/skills/sc-pm-protocol/SKILL.md` are existing project-management orchestration and memory/checkpoint surfaces to review for reuse. Source: Read of the command's Behavioral Summary and Activation sections and the skill's Session Lifecycle section.
- `src/superclaude/commands/spawn.md` provides existing task decomposition and delegation instructions and is a boundary-review surface, not a confirmed implementation target. Source: Read of its Behavioral Flow and Prompt Construction Rules.
- `~/.claude/skills/orchestration/SKILL.md` is an installed discovery stub that loads the Orca binary's version-matched guide, not a repository-owned implementation. Source: Read of that installed file, discovery-stub explanation and Load the version-matched guide section; also developer guide section 7.7.
- The scoped repository search did not locate a dedicated v1/v2 orchestrator command or skill; new implementation paths remain unknown. Source: Glob searches for `src/superclaude/**/*orchestrat*`, `.claude/**/*orchestrat*`, `**/orchestration/SKILL.md` and `plugins/**/*orchestrat*`, plus Grep searches of repository commands and skills for orchestration/Orca references.
- The component pass used Glob/Grep/Read because Codegraph and Auggie tools were not available to this worker; no live Orca or performance validation was performed. Source: available tool set and this worker's static inspection following `~/.claude/commands/sc/analyze.md`, without a depth flag. Its output is limited to Components Affected in the issue body.

## Contradictions

<!-- Each place where the description disagrees with the code, one per line, with path:line evidence. -->

- None
