<!-- template-note: The status check that the orchestrator sends to one running worker (wave 5), with
     `orca orchestration send --to dispatch:<dispatch id> --type status`. The step copies this file first
     (stub first), fills the `{{name}}` slots from the state file (`{{repo}}`, `{{number}}`, `{{message_id}}`,
     `{{report_dir}}`), and sends everything below the MESSAGE marker line as the message body. The step
     deletes this note. The worker's answer arrives by `orca orchestration check`, never by terminal text, and
     the orchestrator reads it from there. -->
<!-- MESSAGE -->
Status check for `{{repo}}#{{number}}`. Reply with `ack {{message_id}} applied` first (WC-12), then these fields.

- State: one of `working`, `question`, `blocked`, `done`
- Last step: what you finished last
- Next step: what you do next
- Blocked by: what blocks you, or "none"
- PR: the pull request number, or "none"
- Evidence: a path under `{{report_dir}}`
