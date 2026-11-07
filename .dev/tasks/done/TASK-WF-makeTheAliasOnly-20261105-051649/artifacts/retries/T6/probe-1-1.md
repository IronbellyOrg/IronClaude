40950c4008013a396f395a09d8206bc392d6458a
family=present-tense-outside-claim
defect form: text that says the aliases keep Claude Code's meaning outside a tier workspace as a present fact, while the workspace defaults file sets the three variables today
command: grep -n -E "Claude Code's (own )?meaning|none of the three|nothing is set" docs/reference/model-aliases.md docs/reference/README.md src/superclaude/skills/sc-issue-protocol/refs/chains.md
before:
docs/reference/model-aliases.md:6:tier models through three environment variables. Outside one nothing is set, so
docs/reference/model-aliases.md:7:the aliases keep Claude Code's own meaning. Issue #384 records the decision.
docs/reference/model-aliases.md:36:Outside a ccsession tier workspace none of the three is set by the launcher, so
docs/reference/model-aliases.md:37:`opus`, `sonnet` and `haiku` keep Claude Code's meaning.
src/superclaude/skills/sc-issue-protocol/refs/chains.md:21:- The brainstorm model list defaults to `opus,sonnet,haiku`, rotated across proposals, and takes aliases only; the brainstorm rows use these defaults. In a ccsession tier workspace the aliases map to `claude-gw-tier1a`, `claude-gw-tier1b` and `claude-gw-tier2` once the launcher sets `ANTHROPIC_DEFAULT_*_MODEL`; outside one they keep Claude Code's meaning (`docs/reference/model-aliases.md`). The session tier itself is pinned by the `/model` line (default D25).
coupled sites: docs/reference/model-aliases.md intro paragraph and the mapping paragraph; src/superclaude/skills/sc-issue-protocol/refs/chains.md:21 already reads "once the launcher sets ANTHROPIC_DEFAULT_*_MODEL" and is outside this task's files (not edited)
after:
8:outside a tier workspace the launcher sets nothing and the aliases keep Claude
39:workspace it sets none of the three, so `opus`, `sonnet` and `haiku` keep Claude
