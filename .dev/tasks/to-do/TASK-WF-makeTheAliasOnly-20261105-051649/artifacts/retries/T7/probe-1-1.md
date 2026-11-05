53e8754295e29b763fadb39a076e50e10422d9dd
family=overbroad-alias-claim
defect form: a sentence says other agent, skill or command files name aliases, though files without a model: line name no model
command: grep -n -E "other agent|name aliases|name an alias|use aliases|all other" src/superclaude/skills/sc-issue-protocol/refs/tiers.md docs/user-guide/brainstorm.md docs/user-guide/commands.md docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md
before:
src/superclaude/skills/sc-issue-protocol/refs/tiers.md:42:Within the scope of `tests/skills/test_model_alias_policy.py`, the issue workers are the files that pin a picker ID in frontmatter `model:`; t
docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:450:An agent that coordinates other agents without doing the work itself. Manages sequencing, scoring, and handoffs.
coupled sites: tiers.md line 42 only
after:
src/superclaude/skills/sc-issue-protocol/refs/tiers.md:42:Within the scope of `tests/skills/test_model_alias_policy.py`, the issue workers are the files that pin a picker ID in frontmatter `model:`; t
docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:450:An agent that coordinates other agents without doing the work itself. Manages sequencing, scoring, and handoffs.
