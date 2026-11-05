af2ce147e76f70e3832c3689e17e2104819bdb57
family: docs-overclaim
defect form: text says the aliases resolve through the tier ids for the Agent call (the Agent-call model parameter), which neither probe exercised
command: grep -n "Agent call" CHANGELOG.md docs/reference/model-aliases.md docs/user-guide/brainstorm.md docs/user-guide/commands.md src/superclaude/skills/sc-issue-protocol/refs/tiers.md src/superclaude/skills/sc-issue-protocol/refs/chains.md
before:
CHANGELOG.md:47:- In a ccsession tier workspace the launcher now exports `ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a`, `ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b` and `ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tie
src/superclaude/skills/sc-issue-protocol/refs/tiers.md:23:1. Claude Code resolves a subagent's model in this order: the Agent call's `model` parameter, then the agent file's `model:` frontmatter, then `CLAUDE_CODE_SUBAGE
src/superclaude/skills/sc-issue-protocol/refs/tiers.md:24:2. The Agent call's `model` parameter accepts only the aliases `sonnet`, `opus`, `haiku`, `fable`. It cannot carry a picker ID, and if passed it overrides the fro
coupled sites: CHANGELOG.md:47 (the flagged sentence); docs/reference/model-aliases.md already says the probes did not exercise the Agent-call parameter and states the Agent-call limits as the documentation's, not as probe results
after:
src/superclaude/skills/sc-issue-protocol/refs/tiers.md:23:1. Claude Code resolves a subagent's model in this order: the Agent call's `model` parameter, then the
src/superclaude/skills/sc-issue-protocol/refs/tiers.md:24:2. The Agent call's `model` parameter accepts only the aliases `sonnet`, `opus`, `haiku`, `fable`. It 
