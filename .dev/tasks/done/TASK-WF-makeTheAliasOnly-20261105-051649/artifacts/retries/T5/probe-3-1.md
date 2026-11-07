a24bee3484cfe56ddbb5f08758649b66709e5d2a
family=notes-accuracy
defect form: a statement in t5-notes.md about which model an adviser runs on, or what the ladder did before the change, that is not backed by the ladder rules (retry.md:164-179) for the workspace's real slot values
command: grep -n -E "Before the change|adviser A was|adviser B was|any other|haiku|every adviser|No adviser" .dev/tasks/to-do/TASK-WF-makeTheAliasOnly-20261105-051649/artifacts/t5-notes.md
before:
55:| any other model, e.g. `claude-sonnet-5-5` (`T1Model03`, defaults.sh 71, not a rung) | `unknown` | `claude-opus-5-5` (top rung) | `gpt-6.1-sol` | 2x `claude-opus-5-5` | 164, 167, 168, 172 |
64:- In this workspace every adviser, including the critique adviser (which uses
66:  `gpt-6.1-sol`. No adviser runs on `glm-5.3` or `gpt-6.1-terra`.
71:## Before the change
73:The fallback table (`refs/retry.md:176-179`) applied: adviser A was `sonnet`
74:for a `haiku` executor and `opus` otherwise, adviser B was the GPT T1 model, and
75:escalation 2 was 2x `opus`. No row puts an adviser on `haiku`. A workspace that
coupled sites: t5-notes.md lines 45-66 (adviser table and its notes), lines 73-75 (before-the-change paragraph)
after:
70:- In this workspace every adviser, including the critique adviser (which uses
72:  `gpt-6.1-sol`. No adviser runs on `glm-5.3` or `gpt-6.1-terra`.
77:## Before the change
81:table (`refs/retry.md:176-179`) names the `haiku`, `sonnet` and `opus` aliases,
83:(`refs/retry.md:164`). In this workspace the `haiku` alias is `glm-5.3`
