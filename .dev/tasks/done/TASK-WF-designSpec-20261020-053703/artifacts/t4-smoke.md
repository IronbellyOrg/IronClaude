T4 live smoke (2026-10-20)

env check (before any spawn):
CLAUDE_CODE_SUBAGENT_MODEL=unset
CLAUDE_CODE_SUBAGENT_MODEL_FORCE=unset
-> FORCE not set; auggie-reviewer agent type available in this session (frontmatter model: opus) -> BLOCKED-ENV does not apply.

smoke 1: Agent(subagent_type=auggie-reviewer, model=sonnet), prompt asked for its model id
reported: MODEL_ID=claude-sonnet-5-5[1m]
check: reported id contains "sonnet" -> PASS (frontmatter says opus, so the per-invocation model overrode it)
note: the reported model id is self-reported by the spawned agent; it is corroboration only, not proof.

smoke 2: Agent(subagent_type=auggie-reviewer, model=connect)
result: rejected by the Agent tool schema before any spawn. Rejection text:
InputValidationError: [{"code": "invalid_value", "values": ["sonnet","opus","haiku","fable"], "path": ["model"], "message": "Invalid option: expected one of \"sonnet\"|\"opus\"|\"haiku\"|\"fable\""}]
check: rejected by schema, no spawn -> PASS

overall: PASS
