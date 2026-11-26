# OB-H2 real claim, issue 827 (level worktree), taken 2026-11-25

- Claim: `/sc:issue --claim 827 --pipeline worktree --stage debug` by the coordinator; launch result in the Coordinator worktree `.dev/issues/827/launch-result.json` (status launched, enforcement_hook installed, L1 effective, L2 owned).
- Session id: 2af36456-5c21-4e57-812f-ead421204a71; session file content `worktree`.
- U8 (session file before the first tool call): the session file's change time (ctime 04:24:43) equals the first UserPromptSubmit probe line (04:24:43); the first PreToolUse is 04:24:52. Bound 9 s before the first tool call. (Its birth time 04:23:59 is the launch-time pending record, which the guard hard-links, so birth time is not the bind time.)
- U7 (exact first prompt and marker position): `[sc-launch:v1:<32 hex>] Read .dev/issues/827/launch-prompt.md and follow it.` The marker is the first characters of the prompt; no Orca preamble precedes it in the payload.
- Hook HOME and CLAUDE_CONFIG_DIR (probe fields): HOME=/home/coder, CLAUDE_CONFIG_DIR unset.
- IR-4: the preflight passed (enforcement_hook installed).
- Not observed: LL-NOBIND visibility on a real claim (only seen if a bind fails); partly seen in rehearsal A (see evidence/rehearsal/).
